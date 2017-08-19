import sys,os
import pickle
import ROOT 
from array import array
from printcolor import printc
from BetterConfigParser import BetterConfigParser
from TreeCache import TreeCache
from math import sqrt
from copy import copy
import time

class HistoMaker:
    def __init__(self, samples, path, config, optionsList,GroupDict=None):
        #samples: list of the samples, data and mc
        #path: location of the samples used to perform the plot
        #config: list of the configuration files
        #optionsList: Dictionnary containing information on vars, including the cuts
        #! Read arguments and initialise variables

        print "Start Creating HistoMaker"
        print "=========================\n"
        self.path = path
        self.config = config
        self.optionsList = optionsList
        self.nBins = optionsList[0]['nBins']
        self.xMin = optionsList[0]['xMin']
        self.lumi = 0.
        self.cuts = []
        for options in optionsList:
            self.cuts.append(options['cut'])
        # created cached tree i.e. create new skimmed trees using the list of cuts
        self.tc = TreeCache(self.cuts,samples,path,config)
        self._rebin = False
        self.mybinning = None
        self.GroupDict=GroupDict
        self.calc_rebin_flag = False
        VHbbNameSpace=config.get('VHbbNameSpace','library')
        ROOT.gSystem.Load(VHbbNameSpace)

        print ""
        print "Done Creating HistoMaker"
        print "========================\n"

    def get_histos_from_tree(self,job,quick=True):
        start_time = time.time()

        print "=============================================================\n"
        print "THE SAMPLE IS ",job.name
        print "=============================================================\n"

        '''Function that produce the trees from a HistoMaker'''
         
        print "Begin to extract the histos from trees (get_histos_from_tree)"
        print "=============================================================\n"

        if self.lumi == 0: 
            lumi = self.config.get('Plot_general','lumi')
            print("You're trying to plot with no lumi, I will use ",lumi)
            self.lumi = lumi
         
        hTreeList=[]

        #get the conversion rate in case of BDT plots
        TrainFlag = eval(self.config.get('Analysis','TrainFlag'))

        # #Remove EventForTraining in order to run the MVA directly from the PREP step
        if not 'PSI' in self.config.get('Configuration','whereToLaunch'):
#            BDT_add_cut='((evt%2) == 0 || Alt$(isData,0))'
            BDT_add_cut='((evt%2) == 0 || isData)'
        else:
            UseTrainSample = eval(self.config.get('Analysis','UseTrainSample'))
            if UseTrainSample:
                BDT_add_cut='EventForTraining == 1'
            else:
                BDT_add_cut='EventForTraining == 0'

        plot_path = self.config.get('Directories','plotpath')
        addOverFlow=eval(self.config.get('Plot_general','addOverFlow'))

        # get all Histos at once
        #print "The tree in the job is ", job.tree
        CuttedTree = self.tc.get_tree(job,'1')# retrieve the cuted tree
        # print 'CuttedTree.GetEntries()',CuttedTree.GetEntries()
#        print 'begin self.optionsList',self.optionsList
        # print 'end self.optionsList'

        #! start the loop over variables (descriebed in options) 
        First_iter = True
        for options in self.optionsList:
            if First_iter: print 'The name of the job is', job.name
            name=job.name
            if self.GroupDict is None:
                group=job.group
            else:
                group=self.GroupDict[job.name]
            treeVar=options['var']
            if First_iter: print("START %s"%treeVar)
            name=options['name']
            # print 'options[\'name\']',options['name']
            if self._rebin or self.calc_rebin_flag:
                nBins = self.nBins
            else:
                nBins = int(options['nBins'])
            xMin=float(options['xMin'])
            xMax=float(options['xMax'])
            weightF=options['weight']
            #Include weight per sample (specialweight)
            #weightF="("+weightF+")*(" + job.specialweight +")"

            treeCut='%s'%(options['cut'])

            if 'BDT' in treeVar:
                if '_Up' in treeVar or '_Down' in treeVar:
                    treeCut = '{}'.format(options['sys_cut'])
            elif 'CMVAV2' in treeVar:
                print 'ELIFCMVAV2'
                if options.get('sys_cut'):
                    treeCut = '{}'.format(options['sys_cut'])
            elif options.get('sys_cut'):
                print 'ELIFSYSCUT'
                treeCut = '{}'.format(options['sys_cut'])
            
            hTree = ROOT.TH1F('%s'%name,'%s'%name,nBins,xMin,xMax)
            hTree.Sumw2()
            hTree.SetTitle(job.name)
            #print('hTree.name() 1 =',hTree.GetName())
            #print('treeVar 1 =',treeVar)
            drawoption = ''
            print 'weightF: %s'%(weightF)
            print 'treeVar: %s'%(treeVar)
            print 'treeCut: %s'%(treeCut)
            
            #print("START DRAWING")
            if job.type != 'DATA':
              if CuttedTree and CuttedTree.GetEntries():
                if 'BDT' in treeVar or 'bdt' in treeVar or 'OPT' in treeVar:#added OPT for BDT optimisation
                    drawoption = '(%s)*(%s && %s)'%(weightF,BDT_add_cut,treeCut)
                    #if First_iter: print "I'm appling: ",BDT_add_cut
                    print "I'm appling: ",BDT_add_cut
                    # drawoption = 'sign(genWeight)*(%s)*(%s & %s)'%(weightF,treeCut,BDT_add_cut)
                    #print drawoption
                else: 
                    #drawoption = '(%s)*(%s)'%(weightF,treeCut)
                    drawoption = '(%s)*(%s && %s)'%(weightF,BDT_add_cut,treeCut)
                #print ('Draw: %s>>%s' %(treeVar,name), drawoption, "goff,e")
                print 'drawoptions are', drawoption
                nevents = CuttedTree.Draw('%s>>%s' %(treeVar,name), drawoption, "goff,e")
                if First_iter: print 'Number of events are', nevents
                #print 'nevents:',hTree.GetEntries(),' hTree.name() 2 =',hTree.GetName()
                full=True
            elif job.type == 'DATA':
                if options['blind']:
                    print 'FROGGINBULLFISH'
                    lowLimitBlindingMass    = 90
                    highLimitBlindingMass   = 140
                    lowLimitBlindingBDT     = 0.3
                    lowLimitBlindingDR      = 0.8
                    highLimitBlindingDR     = 1.6
                    if 'H' in treeVar and 'mass' in treeVar:
                        lowLimitBlindingMass =hTree.GetBinLowEdge(hTree.FindBin(lowLimitBlindingMass))
                        highLimitBlindingMass =hTree.GetBinLowEdge(hTree.FindBin(highLimitBlindingMass))+ hTree.GetBinWidth(hTree.GetBin(highLimitBlindingMass))
                        veto = ("(%s <%s || %s > %s)" %(treeVar,lowLimitBlindingMass,treeVar,highLimitBlindingMass))
                        if First_iter: print "Using veto:",veto
                        CuttedTree.Draw('%s>>%s' %(treeVar,name),veto +'&'+' %(cut)s' %options, "goff,e")
                    elif 'BDT' in treeVar or 'bdt' in treeVar or 'nominal' in treeVar in treeVar:
                        lowLimitBlindingBDT = hTree.GetBinLowEdge(hTree.FindBin(lowLimitBlindingBDT))
                        veto = "(%s <%s)" %(treeVar,lowLimitBlindingBDT)
                        if First_iter: print "Using veto:",veto
                        CuttedTree.Draw('%s>>%s' %(treeVar,name),veto +'&'+' %(cut)s'%options, "goff,e")
                    #elif 'dR' in treeVar and 'H' in treeVar:
                    #    lowLimit   = hTree.GetBinLowEdge(hTree.FindBin(lowLimitBlindingDR))
                    #    highLimit  = hTree.GetBinLowEdge(hTree.FindBin(highLimitBlindingDR))
                    #    veto = ("(%s <%s || %s > %s)" %(treeVar,lowLimitBlindingMass,treeVar,highLimitBlindingMass))
                    #    if First_iter: print "Using veto:",veto
                    #    CuttedTree.Draw('%s>>%s' %(treeVar,name),veto +'&'+' %(cut)s'%options, "goff,e")
                    else:
                        CuttedTree.Draw('%s>>%s' %(treeVar,name),'%s' %treeCut, "goff,e")
                else:
                    #treeCut = '({}) * sb_weight'.format(treeCut)
                    #treeCut = '({}) * ((-0.8<BDT_Znn_HighPt.nominal &&-0.7586>=BDT_Znn_HighPt.nominal )*1.315e-03+(-0.7586<BDT_Znn_HighPt.nominal &&-0.7118>=BDT_Znn_HighPt.nominal )*1.706e-03+(-0.7118<BDT_Znn_HighPt.nominal &&-0.6614>=BDT_Znn_HighPt.nominal )*2.227e-03+(-0.6614<BDT_Znn_HighPt.nominal &&-0.6164>=BDT_Znn_HighPt.nominal )*2.893e-03+(-0.6164<BDT_Znn_HighPt.nominal &&-0.5606>=BDT_Znn_HighPt.nominal )*3.340e-03+(-0.5606<BDT_Znn_HighPt.nominal &&-0.5156>=BDT_Znn_HighPt.nominal )*4.461e-03+(-0.5156<BDT_Znn_HighPt.nominal &&-0.4742>=BDT_Znn_HighPt.nominal )*6.089e-03+(-0.4742<BDT_Znn_HighPt.nominal &&-0.4238>=BDT_Znn_HighPt.nominal )*4.908e-03+(-0.4238<BDT_Znn_HighPt.nominal &&-0.3806>=BDT_Znn_HighPt.nominal )*6.032e-03+(-0.3806<BDT_Znn_HighPt.nominal &&-0.3374>=BDT_Znn_HighPt.nominal )*7.458e-03+(-0.3374<BDT_Znn_HighPt.nominal &&-0.278>=BDT_Znn_HighPt.nominal )*7.862e-03+(-0.278<BDT_Znn_HighPt.nominal &&-0.2366>=BDT_Znn_HighPt.nominal )*9.586e-03+(-0.2366<BDT_Znn_HighPt.nominal &&-0.179>=BDT_Znn_HighPt.nominal )*9.221e-03+(-0.179<BDT_Znn_HighPt.nominal &&-0.134>=BDT_Znn_HighPt.nominal )*1.004e-02+(-0.134<BDT_Znn_HighPt.nominal &&-0.0764>=BDT_Znn_HighPt.nominal )*1.180e-02+(-0.0764<BDT_Znn_HighPt.nominal &&-0.0242>=BDT_Znn_HighPt.nominal )*1.206e-02+(-0.0242<BDT_Znn_HighPt.nominal &&0.0208>=BDT_Znn_HighPt.nominal )*1.684e-02+(0.0208<BDT_Znn_HighPt.nominal &&0.064>=BDT_Znn_HighPt.nominal )*1.671e-02+(0.064<BDT_Znn_HighPt.nominal &&0.1126>=BDT_Znn_HighPt.nominal )*1.788e-02+(0.1126<BDT_Znn_HighPt.nominal &&0.1594>=BDT_Znn_HighPt.nominal )*1.755e-02+(0.1594<BDT_Znn_HighPt.nominal &&0.2044>=BDT_Znn_HighPt.nominal )*1.921e-02+(0.2044<BDT_Znn_HighPt.nominal &&0.2476>=BDT_Znn_HighPt.nominal )*2.284e-02+(0.2476<BDT_Znn_HighPt.nominal &&0.307>=BDT_Znn_HighPt.nominal )*2.502e-02+(0.307<BDT_Znn_HighPt.nominal &&0.3556>=BDT_Znn_HighPt.nominal )*2.656e-02+(0.3556<BDT_Znn_HighPt.nominal &&0.3988>=BDT_Znn_HighPt.nominal )*3.016e-02+(0.3988<BDT_Znn_HighPt.nominal &&0.442>=BDT_Znn_HighPt.nominal )*3.339e-02+(0.442<BDT_Znn_HighPt.nominal &&0.4942>=BDT_Znn_HighPt.nominal )*3.882e-02+(0.4942<BDT_Znn_HighPt.nominal &&0.55>=BDT_Znn_HighPt.nominal )*3.722e-02+(0.55<BDT_Znn_HighPt.nominal &&0.604>=BDT_Znn_HighPt.nominal )*5.587e-02+(0.604<BDT_Znn_HighPt.nominal &&0.6436>=BDT_Znn_HighPt.nominal )*6.009e-02+(0.6436<BDT_Znn_HighPt.nominal &&0.7084>=BDT_Znn_HighPt.nominal )*6.077e-02+(0.7084<BDT_Znn_HighPt.nominal &&0.7444>=BDT_Znn_HighPt.nominal )*7.424e-02+(0.7444<BDT_Znn_HighPt.nominal &&0.8326>=BDT_Znn_HighPt.nominal )*1.060e-01+(0.8326<BDT_Znn_HighPt.nominal &&0.8848>=BDT_Znn_HighPt.nominal )*1.769e-01+(0.8848<BDT_Znn_HighPt.nominal &&1.0>=BDT_Znn_HighPt.nominal )*2.080e-01)'.format(treeCut)
                    if First_iter:
                        print 'DATA drawoptions', '%s>>%s' %(treeVar,name),'%s' %treeCut
                    CuttedTree.Draw('%s>>%s' %(treeVar,name),'%s' %treeCut, "goff,e")
                full = True
              
            if job.type != 'DATA':
                #if 'BDT' in treeVar or 'bdt' in treeVar or 'OPT' in treeVar:
                if TrainFlag:
                    MC_rescale_factor=2. ##FIXME## only dataset used for training must be rescaled!!
                    print 'I RESCALE BY 2.0'
                else: 
                    MC_rescale_factor = 1.

                # For LHE scale shapes we need a different norm
                if 'LHE_weights_scale_wgt[0]' in weightF:
                    ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 0)*MC_rescale_factor
                elif 'LHE_weights_scale_wgt[1]' in weightF:
                    ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 1)*MC_rescale_factor
                elif 'LHE_weights_scale_wgt[2]' in weightF:
                    ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 2)*MC_rescale_factor
                elif 'LHE_weights_scale_wgt[3]' in weightF:
                    ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 3)*MC_rescale_factor
                else:
                    ScaleFactor = self.tc.get_scale(job, self.config)*MC_rescale_factor
                #else:
                #    # For LHE scale shapes we need a different norm
                #    if 'LHE_weights_scale_wgt[0]' in weightF:
                #        ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 0)
                #    elif 'LHE_weights_scale_wgt[1]' in weightF:
                #        ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 1)
                #    elif 'LHE_weights_scale_wgt[2]' in weightF:
                #        ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 2)
                #    elif 'LHE_weights_scale_wgt[3]' in weightF:
                #        ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 3)
                #    else:
                #        ScaleFactor = self.tc.get_scale(job, self.config)

                if ScaleFactor != 0:
                    hTree.Scale(ScaleFactor)
                integral = hTree.Integral()
                print '\t-->import %s\t Integral: %s'%(job.name,integral)
                print("job:",job.name," ScaleFactor=",ScaleFactor)
                print("END RESCALE")
                print("START addOverFlow")
                # !! Brute force correction for histograms with negative integral (problems with datacard) !!
                if integral<0:
                    hTree.Scale(-0.001)
                    print "#"*30
                    print "#"*30
                    print "original integral was:",integral
                    print "now is:", hTree.Integral()
                    print "#"*30
                    print "#"*30
            if addOverFlow:
                uFlow = hTree.GetBinContent(0)+hTree.GetBinContent(1)
                oFlow = hTree.GetBinContent(hTree.GetNbinsX()+1)+hTree.GetBinContent(hTree.GetNbinsX())
                uFlowErr = ROOT.TMath.Sqrt(ROOT.TMath.Power(hTree.GetBinError(0),2)+ROOT.TMath.Power(hTree.GetBinError(1),2))
                oFlowErr = ROOT.TMath.Sqrt(ROOT.TMath.Power(hTree.GetBinError(hTree.GetNbinsX()),2)+ROOT.TMath.Power(hTree.GetBinError(hTree.GetNbinsX()+1),2))
                hTree.SetBinContent(1,uFlow)
                hTree.SetBinContent(hTree.GetNbinsX(),oFlow)
                hTree.SetBinError(1,uFlowErr)
                hTree.SetBinError(hTree.GetNbinsX(),oFlowErr)
            hTree.SetDirectory(0)
#            print("STOP addOverFlow")
#            print("START rebin")
            gDict = {}
            if self._rebin:
                gDict[group] = self.mybinning.rebin(hTree)
                del hTree
            else: 
                #print 'not rebinning %s'%job.name 
                gDict[group] = hTree
#            print("STOP %s"%treeVar)
            hTreeList.append(gDict)
            First_iter = False
        if CuttedTree: CuttedTree.IsA().Destructor(CuttedTree)
        del CuttedTree
        print "Finished to extract the histos from trees (get_histos_from_tree)"
        print "================================================================\n"
        print "get_histos_from_tree DONE for ",job.name," in ", str(time.time() - start_time)," s."
        return hTreeList
       
    @property
    def rebin(self):
        return self._rebin

    @property
    def rebin(self, value):
        if self._rebin and value:
            return True
        elif self._rebin and not value:
            self.nBins = self.norebin_nBins
            self._rebin = False
        elif not self._rebin and value:
            if self.mybinning is None:
                raise Exception('define rebinning first')
            else:
                self.nBins = self.rebin_nBins
                self._rebin = True
                return True
        elif not self._rebin and not self.value:
            return False

    # Reverted rebinner version taken from V25_Diboson17 branch
    def calc_rebin(self, bg_list, nBins_start=1000, tolerance=0.25):
        #print "START calc_rebin"
        self.calc_rebin_flag = True
        self.norebin_nBins = copy(self.nBins)
        self.rebin_nBins = nBins_start
        self.nBins = nBins_start
        i=0
        #add all together:
        print '\n\t...calculating rebinning...'
        for job in bg_list:
            #print "job",job
            htree = self.get_histos_from_tree(job)[0].values()[0]
            print "Integral",job,htree.Integral()
            if not i:
                totalBG = copy(htree)
            else:
                totalBG.Add(htree,1)
            del htree
            i+=1
        #_rootfile = ROOT.TFile.Open('datahist.root', 'recreate')
        #_rootfile.cd()
        #totalBG.Write()
        #_rootfile.Close()
        #raise SystemExit
        ErrorR=0
        ErrorL=0
        TotR=0
        TotL=0
        binR=self.rebin_nBins
        binL=1
        rel=1.0
        #print "START loop from right"
        #print "totalBG.Draw("","")",totalBG.Integral()
        #---- from right
        while rel > tolerance:
            TotR+=totalBG.GetBinContent(binR)
            ErrorR=sqrt(ErrorR**2+totalBG.GetBinError(binR)**2)
            binR-=1
            if binR < 0: break
            if TotR < 1.: continue
            # print "TotR",TotR
            # print "ErrorR",ErrorR
            # print "rel",rel
            if not TotR <= 0 and not ErrorR == 0:
                rel=ErrorR/TotR
                print rel
        #print 'upper bin is %s'%binR
        print "END loop from right"

        #---- from left
        rel=1.0
        print "START loop from left"
        while rel > tolerance:
            TotL+=totalBG.GetBinContent(binL)
            ErrorL=sqrt(ErrorL**2+totalBG.GetBinError(binL)**2)
            binL+=1
            if binL > nBins_start: break
            if TotL < 1.: continue
            if not TotL <= 0 and not ErrorL == 0:
                rel=ErrorL/TotL
                #print rel
        #it's the lower edge
        print "STOP loop from left"
        binL+=1
        #print 'lower bin is %s'%binL

        inbetween=binR-binL
        stepsize=int(inbetween)/(int(self.norebin_nBins)-2)
        modulo = int(inbetween)%(int(self.norebin_nBins)-2)

        print 'stepsize %s'% stepsize
        print 'modulo %s'%modulo
        binlist=[binL]
        for i in xrange(0,int(self.norebin_nBins)-3):
            binlist.append(binlist[-1]+stepsize)
        binlist[-1]+=modulo
        binlist.append(binR)
        binlist.append(self.rebin_nBins+1)
        print 'binning set to %s' % binlist
        print 'bin edges set to %s' % [totalBG.GetBinLowEdge(i) for i in binlist]
        #print "START REBINNER"
        self.mybinning = Rebinner(int(self.norebin_nBins),array('d',[totalBG.GetBinLowEdge(i) for i in binlist]),True)
        # Uncomment for custom bins
        #custom_BDT_bins = [-1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
        #self.mybinning = Rebinner(len(custom_BDT_bins)-1, array('d', custom_BDT_bins), True)
        self._rebin = True
        print '\t > rebinning is set <\n'

    # Modified rebinner from old commit on V25_Moriond17 branch
    #def calc_rebin(self, bg_list, nBins_start=1000, tolerance=0.25):
    #    #print "START calc_rebin"
    #    self.calc_rebin_flag = True
    #    self.norebin_nBins = copy(self.nBins)
    #    self.rebin_nBins = nBins_start
    #    self.nBins = nBins_start
    #    i=0
    #    #add all together:
    #    print '\n\t...calculating rebinning...'
    #    for job in bg_list:
    #        #print "job",job
    #        htree = self.get_histos_from_tree(job)[0].values()[0]
    #        print "Integral",job,htree.Integral()
    #        if not i:
    #            totalBG = copy(htree)
    #        else:
    #            totalBG.Add(htree,1)
    #        del htree
    #        i+=1
    #    #_rootfile = ROOT.TFile.Open('datahist.root', 'recreate')
    #    #_rootfile.cd()
    #    #totalBG.Write()
    #    #_rootfile.Close()
    #    #raise SystemExit
    #    ErrorR=0
    #    ErrorL=0
    #    TotR=0
    #    TotL=0
    #    binR=self.rebin_nBins
    #    binL=1
    #    rel=1.0
    #    #print "START loop from right"
    #    #print "totalBG.Draw("","")",totalBG.Integral()
    #    #---- from right
    #    while rel > tolerance:
    #        TotR+=totalBG.GetBinContent(binR)
    #        ErrorR=sqrt(ErrorR**2+totalBG.GetBinError(binR)**2)
    #        binR-=1
    #        # print 'is this loop infinite ?'
    #        # print "TotR",TotR
    #        # print "ErrorR",ErrorR
    #        # print "rel",rel
    #        if not TotR == 0 and not ErrorR == 0:
    #            rel=ErrorR/TotR
    #            print rel
    #    #print 'upper bin is %s'%binR
    #    print "END loop from right"

    #    #---- from left
    #    rel=1.0
    #    print "START loop from left"
    #    while rel > tolerance:
    #        TotL+=totalBG.GetBinContent(binL)
    #        ErrorL=sqrt(ErrorL**2+totalBG.GetBinError(binL)**2)
    #        binL+=1
    #        if not TotL == 0 and not ErrorL == 0:
    #            rel=ErrorL/TotL
    #            #print rel
    #    #it's the lower edge
    #    print "STOP loop from left"
    #    binL+=1
    #    #print 'lower bin is %s'%binL

    #    inbetween=binR-binL
    #    stepsize=int(inbetween)/(int(self.norebin_nBins)-2)
    #    modulo = int(inbetween)%(int(self.norebin_nBins)-2)

    #    #print 'stepsize %s'% stepsize
    #    #print 'modulo %s'%modulo
    #    binlist=[binL]
    #    for i in range(0,int(self.norebin_nBins)-3):
    #        binlist.append(binlist[-1]+stepsize)
    #    binlist[-1]+=modulo
    #    binlist.append(binR)
    #    binlist.append(self.rebin_nBins-1)
    #    print 'binning set to %s'%binlist
    #    print 'binlist BDT values:', array('d',[-1.0]+[totalBG.GetBinCenter(i) for i in binlist])
    #    print 'bin low edge array:', array('d',[self.xMin]+[totalBG.GetBinLowEdge(i) for i in binlist])
    #    #print 'all possible bins', [totalBG.GetBinLowEdge(i) for i in xrange(1, self.rebin_nBins+1)]
    #    #print "START REBINNER"
    #    self.mybinning = Rebinner(int(self.norebin_nBins),array('d', [self.xMin] + [totalBG.GetBinLowEdge(i) for i in binlist]),True)
    #    # Uncomment for custom bins
    #    #custom_BDT_bins = [-1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
    #    #self.mybinning = Rebinner(len(custom_BDT_bins)-1, array('d', custom_BDT_bins), True)
    #    self._rebin = True
    #    print '\t > rebinning is set <\n'

    # Newest rebinner from V25_Moriond17 branch
    #def calc_rebin(self, bg_list, nBins_start=1000, tolerance=0.25):
    #    self.calc_rebin_flag = True
    #    self.norebin_nBins = copy(self.nBins)
    #    self.rebin_nBins = nBins_start
    #    self.nBins = nBins_start
    #    for i, job in enumerate(bg_list):
    #        htree = self.get_histos_from_tree(job)[0].values()[0]
    #        if i == 0:
    #            totalBG = copy(htree)
    #        else:
    #            totalBG.Add(htree, 1)
    #        del htree
    #    # Merge last (right-most) bin.
    #    index, count, error, stat_unc = nBins_start, 0, 0, 1
    #    while index > 0:
    #        count += totalBG.GetBinContent(index)
    #        error = sqrt(error**2 + totalBG.GetBinError(index)**2)
    #        if count and error:
    #            stat_unc = error / count
    #        if stat_unc < tolerance:
    #            print 'Stop rebin from right, stat. unc. = {!s}'.format(stat_unc)
    #            break
    #        index -= 1
    #    start_last_bin = index
    #    # Merge first (left-most) bin.
    #    index, count, error, stat_unc = 1, 0, 0, 1
    #    while index <= nBins_start:
    #        count += totalBG.GetBinContent(index)
    #        error = sqrt(error**2 + totalBG.GetBinError(index)**2)
    #        if count and error:
    #            stat_unc = error / count
    #        if stat_unc < tolerance:
    #            print 'Stop rebin from left, stat. unc. = {!s}'.format(stat_unc)
    #            break
    #        index += 1
    #    stop_first_bin = index
    #    # Partition the remaining bins evenly.
    #    if stop_first_bin > 5:
    #        index_remaining = range(stop_first_bin + 1, start_last_bin)
    #        n_bins_remaining = len(index_remaining)
    #        stepsize = n_bins_remaining // (self.norebin_nBins - 2)
    #        index_rebinned = [index_remaining[i] for i in xrange(0, n_bins_remaining, stepsize)]
    #        # Insert the starting index of the first bin.
    #        index_rebinned.insert(0, 1)
    #        # If last two bins are closer than the stepsize, remove the second to last bin.
    #        # Otherwise, append the starting index of the last bin.
    #        if start_last_bin - index_rebinned[-1] < stepsize:
    #            index_rebinned[-1] = start_last_bin
    #        else:
    #            index_rebinned.append(start_last_bin)
    #        # Append the index of the overflow bin, whose low edge determines the maximum x-value.
    #        index_rebinned.append(self.rebin_nBins + 1)
    #    else:
    #        # Remove rebinning from the left.
    #        index_remaining = range(1, start_last_bin)
    #        n_bins_remaining = len(index_remaining)
    #        stepsize = n_bins_remaining // (self.norebin_nBins - 1)
    #        index_rebinned = [index_remaining[i] for i in xrange(0, n_bins_remaining, stepsize)]
    #        if start_last_bin - index_rebinned[-1] < stepsize:
    #            index_rebinned[-1] = start_last_bin
    #        else:
    #            index_rebinned.append(start_last_bin)
    #        index_rebinned.append(self.rebin_nBins + 1)
    #    print 'Rebinned Indices: %s' % index_rebinned
    #    # Use the rebinned indices to create an array of low edges for the rebinned histogram.
    #    low_edges = array('d', [totalBG.GetXaxis().GetBinLowEdge(i) for i in index_rebinned])
    #    print 'Rebinned Low Edges: %s' % low_edges
    #    self.mybinning = Rebinner(self.norebin_nBins, low_edges, True)
    #    # Uncomment for no rebinning
    #    #low_edges = array('d', [totalBG.GetXaxis().GetBinLowEdge(i) for i in xrange(1, self.nBins+2)])
    #    # Uncomment for custom bins
    #    #low_edges = array('d', [-1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0])
    #    #self.mybinning = Rebinner(len(custom_BDT_bins)-1, low_edges, True)
    #    self._rebin = True
    #    print '\t > rebinning is set <\n'

    @staticmethod
    def orderandadd(histo_dicts,setup):
        '''
        Setup is defined in the plot conf file
        histo_dicts contains an array of dictionnary
        '''

        from array import array
        doubleVariable = array('d',[0])
        
        #print "Start orderandadd"
        #print "=================\n"
        #print "Input dict is", histo_dicts

        ordered_histo_dict = {}
        #print "orderandadd-setup",setup
        #print "orderandadd-histo_dicts",histo_dicts
        for sample in setup:
            nSample = 0
            for histo_dict in histo_dicts:
                if histo_dict.has_key(sample):
                    integral = histo_dict[sample].IntegralAndError(0,histo_dict[sample].GetNbinsX(),doubleVariable)
                    error = doubleVariable[0]
                    entries = histo_dict[sample].GetEntries()
                    subsamplename = histo_dict[sample].GetTitle()
                    if nSample == 0:
                        ordered_histo_dict[sample] = histo_dict[sample].Clone()
                    else:
                        ordered_histo_dict[sample].Add(histo_dict[sample])
                    printc('magenta','','\t--> added %s to %s Integral: %s Entries: %s Error: %s'%(subsamplename,sample,integral,entries,error))
                    nSample += 1
        del histo_dicts
        #print "Output dict is", ordered_histo_dict
        return ordered_histo_dict 


class Rebinner:
    def __init__(self,nBins,lowedgearray,active=True):
        self.lowedgearray=lowedgearray
        self.nBins=nBins
        self.active=active
    def rebin(self, histo):
        if not self.active: return histo
        print histo.Integral()
        ROOT.gDirectory.Delete('hnew')
        histo.Rebin(self.nBins,'hnew',self.lowedgearray)
        binhisto=ROOT.gDirectory.Get('hnew')
        print binhisto.Integral()
        newhisto=ROOT.TH1F('new','new',self.nBins,self.lowedgearray[0],self.lowedgearray[-1])
        # For regular rebinning
        newhisto.Sumw2()
        for bin in range(1,self.nBins+1):
            newhisto.SetBinContent(bin,binhisto.GetBinContent(bin))
            newhisto.SetBinError(bin,binhisto.GetBinError(bin))
        newhisto.SetName(binhisto.GetName())
        newhisto.SetTitle(binhisto.GetTitle())
        print newhisto.Integral()
        del histo
        del binhisto
        return copy(newhisto)
        # For custom bins
        #return copy(binhisto)
