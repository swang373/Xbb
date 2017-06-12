#!/usr/bin/env python
import ROOT 
ROOT.gROOT.SetBatch(True)
from ROOT import TFile
from optparse import OptionParser
import sys
from myutils import BetterConfigParser, TdrStyles, getRatio
import os


argv = sys.argv
parser = OptionParser()
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                      help="configuration file")
(opts, args) = parser.parse_args(argv)
config = BetterConfigParser()
config.read(opts.config)

print config


#---------- yes, this is not in the config yet---------
 
mode = 'BDT'
xMin=-1
xMax=1
masses = ['125']
Abins = ['Signal']#,'HighPt']
channels = ['Znn_13TeV']#, 'Zee']

#------------------------------------------------------

#---------- Control Regions ---------------------------------------
'''
mode = 'CR'
xMin=0
xMax=1
masses = ['125']
Abins = ['ttbar', 'Zlf', 'Zhf']
channels= ['Zll']
'''
#------------------------------------------------------

path = '/afs/cern.ch/work/s/swang373/private/Xbb_ICHEP/src/Xbb/Nominal_nBins40/'

outpath = '/afs/cern.ch/user/s/swang373/www/V25_ZnnHbb_ShapeSystematics_Nominal_nBins40/'

# Make the dir and copy the website ini files
try:
    os.system('mkdir '+outpath)
except:
     print outpath+' already exists...'

temp_string2 = 'cp /afs/cern.ch/user/s/swang373/www/index.php '+outpath

os.system(temp_string2)

setup = eval(config.get('LimitGeneral','setup'))
Dict = eval(config.get('LimitGeneral','Dict'))
MCs = [Dict[s] for s in setup]

sys_BDT= eval(config.get('LimitGeneral','sys_BDT'))
systematicsnaming = eval(config.get('LimitGeneral','systematicsnaming'))
print systematicsnaming
systs=[systematicsnaming[s] for s in sys_BDT]

#if eval(config.get('LimitGeneral','weightF_sys')): systs.append('UEPS')

def myText(txt="CMS Preliminary",ndcX=0,ndcY=0,size=0.8):
    ROOT.gPad.Update()
    text = ROOT.TLatex()
    text.SetNDC()
    text.SetTextColor(ROOT.kBlack)
    text.SetTextSize(text.GetTextSize()*size)
    text.DrawLatex(ndcX,ndcY,txt)
    return text


print '\n\n\t\tMaking Plots for Systematics: ', systs

print '\n\t ---> Output: ', outpath

#for mass in ['110','115','120','125','130','135']:
for mass in masses:
    for Abin in Abins:

        systematicsnaming = eval(config.get('LimitGeneral','systematicsnaming'))
        systs=[systematicsnaming[s] for s in sys_BDT]

        for channel in channels:

            if mode == 'BDT':
                input = TFile.Open(path+'/vhbb_TH_'+channel+'_'+Abin+'.root','read')

            if mode == 'CR':
                input = TFile.Open(path+'/vhbb_TH_'+Abin+'.root','read')


            print '\n-----> Input: ', input     

            for MC in MCs:

                print 'MC sample: ',MC

                #if MC == 's_Top':
                #    continue
                if MC == 'QCD':
                    continue

                for syst in systs:
                    print '\n\t Plotting Systematic: ', syst
                #['CMS_res_j','CMS_scale_j','CMS_eff_b','CMS_fake_b_8TeV','UEPS']:
                #for syst in ['CMS_vhbb_stats_']:

                    if '_eff_' in syst:
                        if 'Zuu' in channels and '_e_' in syst: continue
                        if 'Zee' in channels and '_m_' in syst:continue

                    TdrStyles.tdrStyle()

                    c = ROOT.TCanvas('','', 600, 600)
                    c.SetFillStyle(4000)
                    c.SetFrameFillStyle(1000)
                    c.SetFrameFillColor(0)
                    oben = ROOT.TPad('oben','oben',0,0.3 ,1.0,1.0)
                    oben.SetBottomMargin(0)
                    oben.SetFillStyle(4000)
                    oben.SetFrameFillStyle(1000)
                    oben.SetFrameFillColor(0)
                    unten = ROOT.TPad('unten','unten',0,0.0,1.0,0.3)
                    unten.SetTopMargin(0.)
                    unten.SetBottomMargin(0.35)
                    unten.SetFillStyle(4000)
                    unten.SetFrameFillStyle(1000)
                    unten.SetFrameFillColor(0)
                    oben.Draw()
                    unten.Draw()
                    oben.cd()

                    ROOT.gPad.SetTicks(1,1)
                    
                    if mode == 'BDT':
                        input.cd(channel+'_'+Abin)
                    if mode == 'CR':
                        input.cd(Abin)

                    Ntotal=ROOT.gDirectory.Get(MC)

                    #if 'pu' not in syst and '_eff_' not in syst:
                    #if '_j_' in syst:
                    #    if 'High' in Abin:
                    #        Utotal=ROOT.gDirectory.Get(MC+syst+'_highVptUp')
                    #        Dtotal=ROOT.gDirectory.Get(MC+syst+'_highVptDown')
                    #    if 'Low' in Abin:
                    #        Utotal=ROOT.gDirectory.Get(MC+syst+'_lowVptUp')
                    #        Dtotal=ROOT.gDirectory.Get(MC+syst+'_lowVptDown')

                    #else:
                    Utotal=ROOT.gDirectory.Get(MC+syst+'Up')
                    Dtotal=ROOT.gDirectory.Get(MC+syst+'Down')

                    print '\n\t Input: ', channel+'_'+Abin
                    print input
                    print '\n\t NOM : ', MC
                    print Ntotal
                    print '\n\t UP  : ', MC+syst+'Up'
                    print Utotal
                    print '\n\t DOWN: ', MC+syst+'Down'
                    print Dtotal


                    l = ROOT.TLegend(0.17, 0.8, 0.37, 0.65)
                    
                    l.SetLineWidth(2)
                    l.SetBorderSize(0)
                    l.SetFillColor(0)
                    l.SetFillStyle(4000)
                    l.SetTextFont(62)
                    l.SetTextSize(0.035)
                    
                    l.AddEntry(Ntotal,'nominal(%s)'%round(Ntotal.Integral(),3),'PL')
                    l.AddEntry(Utotal,'up(%s)'%round(Utotal.Integral(),3),'PL')
                    l.AddEntry(Dtotal,'down(%s)'%round(Dtotal.Integral(),3),'PL')
                    Ntotal.GetYaxis().SetRangeUser(0,1.5*Ntotal.GetBinContent(Ntotal.GetMaximumBin()))
                    Ntotal.SetMarkerStyle(8)
                    Ntotal.SetLineColor(1)
                    Ntotal.SetStats(0)
                    Ntotal.SetTitle(MC +' '+syst)
                    Ntotal.Draw("P0")
                    Ntotal.Draw("same")
                    Utotal.SetLineColor(4)    
                    Utotal.SetLineStyle(4)
                    Utotal.SetLineWidth(2)        
                    Utotal.Draw("same hist")
                    Dtotal.SetLineColor(2)
                    Dtotal.SetLineStyle(3)
                    Dtotal.SetLineWidth(2)  
                    Dtotal.Draw("same hist")
                    l.SetFillColor(0)
                    l.SetBorderSize(0)
                    l.Draw()
                    
                    if 'High' in Abin:
                        title=myText('%s in %s'%(syst,MC+'_'+channel+'_highZpt'),0.17,0.85)
                    if 'Low' in Abin:
                        title=myText('%s in %s'%(syst,MC+'_'+channel+'_lowZpt'),0.17,0.85)
                        

                    print 'Shape Systematic %s in %s'%(syst,MC)
                    print 'Up:     \t%s'%Utotal.Integral()
                    print 'Nominal:\t%s'%Ntotal.Integral()
                    print 'Down:   \t%s'%Dtotal.Integral()
                    
                    unten.cd()
                    ROOT.gPad.SetTicks(1,1)

                    ratioU, errorU  = getRatio(Utotal,Ntotal,xMin,xMax)
                    ratioD, errorD  = getRatio(Dtotal,Ntotal,xMin,xMax)

                    ksScoreU = Ntotal.KolmogorovTest( Utotal )
                    chiScoreU = Ntotal.Chi2Test( Utotal , "WWCHI2/NDF")
                    ksScoreD = Ntotal.KolmogorovTest( Dtotal )
                    chiScoreD = Ntotal.Chi2Test( Dtotal , "WWCHI2/NDF")

                    yUp   = 1.1
                    yDown = 0.9


                    ratioU.SetStats(0)
                    ratioU.GetYaxis().SetRangeUser(yDown, yUp)
                    ratioU.GetYaxis().SetNdivisions(502,0)
                    ratioD.SetStats(0)
                    ratioD.GetYaxis().SetRangeUser(yDown, yUp)
                    ratioD.GetYaxis().SetNdivisions(502,0)
                    ratioD.GetYaxis().SetLabelSize(0.05)
                    ratioD.SetLineColor(2)
                    ratioD.SetLineStyle(3)
                    ratioD.SetLineWidth(2)  
                    ratioU.SetLineColor(4)    
                    ratioU.SetLineStyle(4)
                    ratioU.SetLineWidth(2)

                    fitRatioU = ratioU.Fit("pol2","S")
                    ratioU.GetFunction("pol2").SetLineColor(4)
                    fitRatioD = ratioD.Fit("pol2","S")
                    ratioU.Draw("APSAME")
                    ratioD.GetXaxis().SetTitle('BDT Output')
                    ratioD.GetYaxis().SetTitle('Ratio')
                    ratioD.GetYaxis().SetTitleSize(0.1)
                    ratioD.GetYaxis().SetTitleOffset(0.2)
                    fitRatioU.Draw("SAME")
                    fitRatioD.Draw("SAME")
                    
                    ratioD.Draw("SAME")

                    #ratioU.GetYaxis().SetTitleSize(0.2)
                    #ratioU.GetYaxis().SetTitleOffset(0.2)
                    #ratioU.GetXaxis().SetLabelColor(10)
                    
                    #fitRatioU = ratioU.Fit("pol2","S")
                    #fitRatioU.Draw("SAME")

                    #ratioD.GetYaxis().SetTitleSize(0.2)
                    #ratioD.GetYaxis().SetTitleOffset(0.2)
                    #ratioD.GetXaxis().SetLabelColor(10)
                    
                    #fitRatioD = ratioD.Fit("pol2","S")
                    #fitRatioD.Draw("SAME")

                    m_one_line = ROOT.TLine(xMin,1,xMax,1)
                    m_one_line.SetLineStyle(7)
                    m_one_line.SetLineColor(1)
                    m_one_line.Draw("Same")


                    #name = outpath+Abin+'_M'+mass+'_'+channel+'_'+MC+syst+'.png'
                    #c.Print(name)

                    if mode == 'CR':
                        name = outpath+'systPlot_'+Abin+'_'+channel+'_'+MC+'_'+syst+'.pdf'
                        c.Print(name)
                        name2 = outpath+'systPlot_'+Abin+'_'+channel+'_'+MC+'_'+syst+'.png'
                        c.Print(name2)
                        
                    else:
                        name = outpath+'systPlot_'+Abin+'_M'+mass+'_'+channel+'_'+MC+syst+'.pdf'
                        c.Print(name)
                        name2 = outpath+'systPlot_'+Abin+'_M'+mass+'_'+channel+'_'+MC+syst+'.png'
                        c.Print(name2)


            input.Close()
