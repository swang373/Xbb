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
#Read the configuration file. region corresponds to the sample and --configs lists the conf. files for a given energy
#opts.config = ['8TeVconfig/paths', '8TeVconfig/general', '8TeVconfig/cuts', '8TeVconfig/training', '8TeVconfig/datacards', '8TeVconfig/plots', '8TeVconfig/lhe_weights']

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

vhbbPlotDef=opts.config[0].split('/')[0]+'/vhbbPlotDef.ini'#Takes the name 8TeVconfig/vhbbPlotDef.ini
# print 'vhbbPlotDef',vhbbPlotDef
# sys.exit()
opts.config.append(vhbbPlotDef)#adds it to the config list
# opts.config.append('8TeVconfig/vhbbPlotDef.ini')

config = BetterConfigParser()
config.read(opts.config)

#path = opts.path
region = opts.region
print 'The region is ', region#TTbar_fit_EE

# additional blinding cut:
addBlindingCut = None
if config.has_option('Plot_general','addBlindingCut'):#contained in plots, cut on the event number
    addBlindingCut = config.get('Plot_general','addBlindingCut')
    print 'adding add. blinding cut'


#get locations:
print "DEBUG 1"
Wdir=config.get('Directories','Wdir')
samplesinfo=config.get('Directories','samplesinfo')

path = config.get('Directories','plottingSamples')

section='Plot:%s'%region#Plot:TTbar_fit_EE
print 'section is ', section #Plot:TTbar_fit_EE, correspond to the CR


info = ParseInfo(samplesinfo,path)#root://t3dcachedb03.psi.ch:1094//pnfs/psi.ch/cms/trivcat/store/user/gaperrin/VHbb_test/

print 'samplesinfo is ', samplesinfo
print 'path is ', path
print 'info = ParseInfo(samplesinfo,path) is ', path

#----------Histo from trees------------
print "DEBUG 2"
#Get the selections and the samples
def doPlot():
    vars = (config.get(section, 'vars')).split(',')#get the variables vars in the control region
    print 'vars',vars
    data = config.get(section,'Datas')#Datas: Zee
    mc = eval(config.get('Plot_general','samples'))#Loads all the bkg. see plots and general files

    SignalRegion = False
    if config.has_option(section,'Signal'):#Signal: <!Plot_general|plot_mass!>
        mc.append(config.get(section,'Signal'))
        SignalRegion = True
            
    datasamples = info.get_samples(data)
    mcsamples = info.get_samples(mc)

    GroupDict = eval(config.get('Plot_general','Group'))#lots of variables there

    #GETALL AT ONCE
    print "DEBUG 3"
    options = []
    Stacks = []
    for i in range(len(vars)):
        Stacks.append(StackMaker(config,vars[i],region,SignalRegion))
        options.append(Stacks[i].options)
        #print 'loop options',options
    #print 'options',options

    print "DEBUG 4"
    Plotter=HistoMaker(mcsamples+datasamples,path,config,options,GroupDict)

    #print '\nProducing Plot of %s\n'%vars[v]
    Lhistos = [[] for _ in range(0,len(vars))]
    print "DEBUG 4.5"
    Ltyps = [[] for _ in range(0,len(vars))]
    Ldatas = [[] for _ in range(0,len(vars))]
    Ldatatyps = [[] for _ in range(0,len(vars))]
    Ldatanames = [[] for _ in range(0,len(vars))]

    #Find out Lumi:
    print "DEBUG 5"
    lumicounter=0.
    lumi=0.
    for job in datasamples:
        lumi+=float(job.lumi)
        lumicounter+=1.

    if lumicounter > 0:
        lumi=lumi/lumicounter

    Plotter.lumi=lumi
    mass = Stacks[0].mass

    print 'mcsamples',mcsamples
    for job in mcsamples:
        print 'job.name',job.name
        #hTempList, typList = Plotter.get_histos_from_tree(job)
        if addBlindingCut:
            hDictList = Plotter.get_histos_from_tree(job,config.get('Cuts',region)+' & ' + addBlindingCut)
        else:
            print 'going to get_histos_from_tree'
            hDictList = Plotter.get_histos_from_tree(job)
        if job.name == mass:
            print 'job.name', job.name
            Overlaylist= deepcopy([hDictList[v].values()[0] for v in range(0,len(vars))])
        for v in range(0,len(vars)):
            Lhistos[v].append(hDictList[v].values()[0])
            Ltyps[v].append(hDictList[v].keys()[0])

    print 'datasamples',datasamples
    print "DEBUG 6"
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

        histos = Lhistos[v]
        typs = Ltyps[v]
        Stacks[v].histos = Lhistos[v]
        Stacks[v].typs = Ltyps[v]
        Stacks[v].datas = Ldatas[v]
        Stacks[v].datatyps = Ldatatyps[v]
        Stacks[v].datanames= Ldatanames[v]
        #if SignalRegion:
        #    Stacks[v].overlay = Overlaylist[v]
        Stacks[v].lumi = lumi
        Stacks[v].doPlot()
        Stacks[v].histos = Lhistos[v]
        Stacks[v].typs = Ltyps[v]
        Stacks[v].datas = Ldatas[v]
        Stacks[v].datatyps = Ldatatyps[v]
        Stacks[v].datanames= Ldatanames[v]
        Stacks[v].normalize = True
        Stacks[v].options['pdfName'] = Stacks[v].options['pdfName'].replace('.pdf','_norm.pdf')
        Stacks[v].doPlot()
        print 'i am done!\n'
#----------------------------------------------------
doPlot()
sys.exit(0)
