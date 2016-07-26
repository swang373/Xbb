#!/usr/bin/env python
import pickle
import ROOT 
from array import array
import sys, os
from optparse import OptionParser
from copy import copy,deepcopy
from math import sqrt
ROOT.gROOT.SetBatch(True)

#CONFIGURE
argv = sys.argv
parser = OptionParser()
parser.add_option("-R", "--region", dest="region", default="",
                      help="region to plot")
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                      help="configuration file")
(opts, args) = parser.parse_args(argv)
if opts.config =="":
        opts.config = "config"
        
from myutils import BetterConfigParser, printc, ParseInfo, mvainfo, StackMaker, HistoMaker


print 'opts.config',opts.config

vhbbPlotDef=opts.config[0].split('/')[0]+'/vhbbPlotDef.ini'
# print 'vhbbPlotDef',vhbbPlotDef
# sys.exit()
opts.config.append(vhbbPlotDef)
# opts.config.append('8TeVconfig/vhbbPlotDef.ini')

config = BetterConfigParser()
config.read(opts.config)

#path = opts.path
region = opts.region

# additional blinding cut:
addBlindingCut = None
if config.has_option('Plot_general','addBlindingCut'):
    addBlindingCut = config.get('Plot_general','addBlindingCut')
    print 'adding add. blinding cut'

#get locations:
Wdir=config.get('Directories','Wdir')
samplesinfo=config.get('Directories','samplesinfo')

path = config.get('Directories','plottingSamples')

section='Plot:%s'%region

info = ParseInfo(samplesinfo,path)

#----------Histo from trees------------
def doPlot():
    vars = (config.get(section, 'vars')).split(',')
    # print 'vars',vars
    data = config.get(section,'Datas')
    mc = eval(config.get('Plot_general','samples'))

    SignalRegion = False
    if config.has_option(section,'Signal'):
        mc.append(config.get(section,'Signal'))
        SignalRegion = True
            
    datasamples = info.get_samples(data)
    mcsamples = info.get_samples(mc)

    GroupDict = eval(config.get('Plot_general','Group'))

    #GETALL AT ONCE
    options = []
    Stacks = []
    for i in range(len(vars)):
        Stacks.append(StackMaker(config,vars[i],region,SignalRegion))
        options.append(Stacks[i].options)
        print 'loop options',options
    # print 'options',options

    Plotter=HistoMaker(mcsamples+datasamples,path,config,options,GroupDict)

    #print '\nProducing Plot of %s\n'%vars[v]
    Lhistos = [[] for _ in range(0,len(vars))]
    Ltyps = [[] for _ in range(0,len(vars))]
    Ldatas = [[] for _ in range(0,len(vars))]
    Ldatatyps = [[] for _ in range(0,len(vars))]
    Ldatanames = [[] for _ in range(0,len(vars))]
    Ljobnames = [[] for _ in range(0,len(vars))]

    #Find out Lumi:
    lumicounter=0.
    lumi=0.
    for job in datasamples:
        lumi+=float(job.lumi)
        lumicounter+=1.

    if lumicounter > 0:
        lumi=lumi/lumicounter

    Plotter.lumi=lumi
    mass = Stacks[0].mass

#        multiprocess=16
#        if multiprocess>0:
#            from multiprocessing import Pool
#            p = Pool(multiprocess)
##            import pathos.multiprocessing as mp
##            p = mp.ProcessingPool(multiprocess)
#            myinputs = []
#            for job in self.__sampleList:
#                myoptions = self.putOptions()
#                myinputs.append((myoptions,job))
#                
#            outputs = p.map(trim_treeMT, myinputs)

    print 'mcsamples',mcsamples
    inputs=[]
    for job in mcsamples:
#        print 'job.name'
        cutOverWrite = None
        if addBlindingCut:
            cutOverWrite = config.get('Cuts',region)+' & ' + addBlindingCut
        inputs.append((Plotter,"get_histos_from_tree",(job,cutOverWrite)))
    
    multiprocess=0#64
    outputs = []
    if multiprocess>0:
        from multiprocessing import Pool
        from myutils import GlobalFunction
        p = Pool(multiprocess)
        print 'launching get_histos_from_tree with ',multiprocess,' processes'
        outputs = p.map(GlobalFunction, inputs)
    else:
        print 'launching get_histos_from_tree with ',multiprocess,' processes'
        for input_ in inputs:
            outputs.append(getattr(input_[0],input_[1])(*input_[2])) #ie. Plotter.get_histos_from_tree(job,cutOverWrite)
    print 'get_histos_from_tree DONE'
    Overlaylist = []
    for i,job in enumerate(mcsamples):
        print 'job.name',job.name,"mass==",mass
        #hTempList, typList = Plotter.get_histos_from_tree(job)
        hDictList = outputs[i]
        if job.name in mass:
            print 'job.name == mass'
            histoList = []
            for v in range(0,len(vars)):
                histoCopy = deepcopy(hDictList[v].values()[0])
                histoCopy.SetTitle(job.name)
                histoList.append(histoCopy)
            Overlaylist.append(histoList)
#            Overlaylist.append(deepcopy([hDictList[v].values()[0] for v in range(0,len(vars))]))
        for v in range(0,len(vars)):
            Lhistos[v].append(hDictList[v].values()[0])
            Ltyps[v].append(hDictList[v].keys()[0])
            Ljobnames[v].append(job.name)
    
    print "len(vars)=",len(vars)
    ##invert Overlaylist[variable][job] -> Overlaylist[job][variable]
    print "len(Overlaylist) before: ",len(Overlaylist)
    print "Overlaylist",Overlaylist
#    newOverlaylist = [[None]*len(Overlaylist)]*len(vars)
#    for i,OverlaySameSample in enumerate(Overlaylist):
#            for j,Overlay in enumerate(OverlaySameSample):
#                newOverlaylist[j][i] = Overlay    
#    Overlaylist = newOverlaylist
    Overlaylist = [list(a) for a in zip(*Overlaylist)]
    print "len(Overlaylist) after: ",len(Overlaylist)
    print "Overlaylist",Overlaylist
    
    ##merge overlays in groups 
    for i in range(len(Overlaylist)):
        newhistos = {}
        print "len(Overlaylist[i]):",Overlaylist[i]
        for histo in Overlaylist[i]:
            print "histo.GetName()",histo.GetName(),
            print "histo.GetTitle()",histo.GetTitle(),
            group = GroupDict[histo.GetTitle()]
            if not group in newhistos.keys():
                histo.SetTitle(group)
                newhistos[group]=histo
            else:
                print "Before newhistos[group].Integral()",newhistos[group].Integral(),
                newhistos[group].Add(histo)
                print "After newhistos[group].Integral()",newhistos[group].Integral()
        Overlaylist[i] = newhistos.values()
        


#   ### ORIGINAL ###
#    print 'mcsamples',mcsamples
#    for job in mcsamples:
#        print 'job.name',job.name
#        #hTempList, typList = Plotter.get_histos_from_tree(job)
#        if addBlindingCut:
#            hDictList = Plotter.get_histos_from_tree(job,config.get('Cuts',region)+' & ' + addBlindingCut)
#        else:
#            print 'going to get_histos_from_tree'
#            hDictList = Plotter.get_histos_from_tree(job)
#        if job.name == mass:
#            print 'job.name', job.name
#            Overlaylist= deepcopy([hDictList[v].values()[0] for v in range(0,len(vars))])
#        for v in range(0,len(vars)):
#            Lhistos[v].append(hDictList[v].values()[0])
#            Ltyps[v].append(hDictList[v].keys()[0])
#            Ljobnames[v].append(job.name)


    print 'datasamples',datasamples
    for job in datasamples:
        #hTemp, typ = Plotter.get_histos_from_tree(job)
        if addBlindingCut:
            dDictList = Plotter.get_histos_from_tree(job,config.get('Cuts',region)+' & ' + addBlindingCut)
        else:
            dDictList = Plotter.get_histos_from_tree(job)
        for v in range(0,len(vars)):
            Ldatas[v].append(dDictList[v].values()[0])
            Ldatatyps[v].append(dDictList[v].keys()[0])
            Ldatanames[v].append(job.name)

    for v in range(0,len(vars)):

        print "Ltyps[v]:",Ltyps[v]
        print "Lhistos[v]:",Lhistos[v]
        print "Ldatas[v]:",Ldatas[v]
        print "Ldatatyps[v]:",Ldatatyps[v]
        print "Ldatanames[v]:",Ldatanames[v]
        print "lumi:",lumi

        histos = Lhistos[v]
        typs = Ltyps[v]
        Stacks[v].histos = Lhistos[v]
        Stacks[v].typs = Ltyps[v]
        Stacks[v].datas = Ldatas[v]
        Stacks[v].datatyps = Ldatatyps[v]
        Stacks[v].datanames= Ldatanames[v]
        #if SignalRegion:
        #Stacks[v].overlay = Overlaylist[v] ## from 
        Stacks[v].lumi = lumi
        Stacks[v].normalize = eval(config.get(section,'Normalize'))
        Stacks[v].jobnames= Ljobnames[v]
        Stacks[v].doPlot()
        ##FIXME##
#        Stacks[v].histos = Lhistos[v]
#        Stacks[v].typs = Ltyps[v]
#        Stacks[v].datas = Ldatas[v]
#        Stacks[v].datatyps = Ldatatyps[v]
#        Stacks[v].datanames= Ldatanames[v]
#        Stacks[v].normalize = True
#        Stacks[v].options['pdfName'] = Stacks[v].options['pdfName'].replace('.pdf','_norm.pdf')
#        Stacks[v].doPlot()
        print 'i am done!\n'
#----------------------------------------------------
doPlot()
sys.exit(0)
