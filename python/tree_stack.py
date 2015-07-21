#!/usr/bin/env python
import pickle
import ROOT 
from array import array
import sys, os
from optparse import OptionParser
from copy import copy,deepcopy
from math import sqrt
ROOT.gROOT.SetBatch(True)

argv = sys.argv

#Read the arguments. --region corresponds to the region to plot --configs to the lists of the config files for a given energy.
#i.e. opts.config = ['8TeVconfig/paths', '8TeVconfig/general', '8TeVconfig/cuts', '8TeVconfig/training', '8TeVconfig/datacards', '8TeVconfig/plots', '8TeVconfig/lhe_weights'] when --config is 8TeV in runAll

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

print 'tree_stack_1'

#adds the file vhbbPlotDef.ini to the config list
vhbbPlotDef=opts.config[0].split('/')[0]+'/vhbbPlotDef.ini'
opts.config.append(vhbbPlotDef)#adds it to the config list

config = BetterConfigParser()
config.read(opts.config)

#path = opts.path
region = opts.region
print 'The region is ', region

# additional blinding cut:
addBlindingCut = None
if config.has_option('Plot_general','addBlindingCut'):#contained in plots, cut on the event number
    addBlindingCut = config.get('Plot_general','addBlindingCut')
    print 'adding add. blinding cut'

# compile external macros to compute variables on the fly
print('current directory while compiling external macro',os.getcwd())
ROOT.gSystem.CompileMacro("../plugins/VH_pt.C")
ROOT.gSystem.CompileMacro("../plugins/SimpleDeltaR.C")
ROOT.gSystem.CompileMacro("../plugins/HJetPt.C")

#get locations:
print 'tree_stack_2'
Wdir=config.get('Directories','Wdir')# working direcoty containing the ouput
samplesinfo=config.get('Directories','samplesinfo')# samples_nosplit.cfg

path = config.get('Directories','plottingSamples')# from which samples to plot

section='Plot:%s'%region
print 'section is ', section 

info = ParseInfo(samplesinfo,path) #creates a list of Samples by reading the info in samples_nosplit.cfg and the conentent of the path.
print 'tree_stack3'

#----------Histo from trees------------
#Get the selections and the samples
def doPlot():
    print 'DOPLOT1'

    vars = (config.get(section, 'vars')).split(',')# get the variables to be ploted for all the regions
    # print 'vars',vars
    data = config.get(section,'Datas')# read the data corresponding to each CR (section)
    mc = eval(config.get('Plot_general','samples'))# read the list of mc samples

    print 'mc is', mc

    SignalRegion = False
    if config.has_option(section,'Signal'):#Signal: <!Plot_general|plot_mass!>
        mc.append(config.get(section,'Signal'))# ?
        SignalRegion = True
            
    datasamples = info.get_samples(data)#get the Sample "Data"
    mcsamples = info.get_samples(mc)#get the Samples "sample"

    GroupDict = eval(config.get('Plot_general','Group'))#Contained in plots. Listed in general, under Group [Samples] group. This is a dictionnary that descriebes what samples should share the same color under the stack plot.

    #GETALL AT ONCE
    print 'DOPLOT2'
    options = []
    Stacks = []
    for i in range(len(vars)):# loop over the list of variables to be ploted in each reagion
        Stacks.append(StackMaker(config,vars[i],region,SignalRegion))# defined in myutils DoubleStackMaker. The StackMaker merge together all the informations necessary to perform the plot (plot region, variables, samples and signal region ). "options" contains the variables information, including the cuts. 
        options.append(Stacks[i].options)

    #Prepare cached files in the temporary (tmpSamples) folder.
    Plotter=HistoMaker(mcsamples+datasamples,path,config,options,GroupDict)

    #print '\nProducing Plot of %s\n'%vars[v]
    print 'DOPLOT3'
    #! Create lists of the histos for each Sample (each Sample containing one histogram for each variable )
    Lhistos = [[] for _ in range(0,len(vars))]
    Ltyps = [[] for _ in range(0,len(vars))]
    Ldatas = [[] for _ in range(0,len(vars))]
    Ldatatyps = [[] for _ in range(0,len(vars))]
    Ldatanames = [[] for _ in range(0,len(vars))]

    #! Sums up the luminosity of the data:
    print 'DOPLOT4'
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

    #! Get the histogram from Plotter
    #! Get the mc histograms
    print 'DOPLOT5'
    for job in mcsamples:
        print 'job.name',job.name
        #hTempList, typList = Plotter.get_histos_from_tree(job)
        if addBlindingCut:
	    print 'there is a blinding cut'
            hDictList = Plotter.get_histos_from_tree(job,config.get('Cuts',region)+' & ' + addBlindingCut)
        else:
            print 'going to get_histos_from_tree'
            hDictList = Plotter.get_histos_from_tree(job)
        if job.name == mass:
            print 'job.name', job.name
            Overlaylist= deepcopy([hDictList[v].values()[0] for v in range(0,len(vars))])
	    #! add the variables list for each job (Samples)
        for v in range(0,len(vars)):
            Lhistos[v].append(hDictList[v].values()[0])
            Ltyps[v].append(hDictList[v].keys()[0])

    print 'datasamples',datasamples
    #! Get the data histograms
    print 'DOPLOT6'
    for job in datasamples:
        print 'DOPLOT6.0'
        if addBlindingCut:
            print 'DOPLOT6.05'
            dDictList = Plotter.get_histos_from_tree(job,config.get('Cuts',region)+' & ' + addBlindingCut)
            print 'DOPLOT6.1'
        else:
            print 'DOPLOT6.15'
            dDictList = Plotter.get_histos_from_tree(job)
            print 'DOPLOT6.2'
	    #! add the variables list for each job (Samples)
        for v in range(0,len(vars)):
            print 'DOPLOT6.3'
            Ldatas[v].append(dDictList[v].values()[0])
            Ldatatyps[v].append(dDictList[v].keys()[0])
            Ldatanames[v].append(job.name)

    print 'DOPLOT7'
    for v in range(0,len(vars)):

        print "The number of variables is ", len(vars)
        histos = Lhistos[v]
        typs = Ltyps[v]
        Stacks[v].histos = Lhistos[v]
	print 'The number of histogram is', len(Stacks[v].histos)
        Stacks[v].typs = Ltyps[v]
        Stacks[v].datas = Ldatas[v]
        Stacks[v].datatyps = Ldatatyps[v]
        Stacks[v].datanames= Ldatanames[v]
        #if SignalRegion:
        #    Stacks[v].overlay = Overlaylist[v]
        Stacks[v].lumi = lumi
        Stacks[v].doPlot()#bug here
        Stacks[v].histos = Lhistos[v]
        Stacks[v].typs = Ltyps[v]
        Stacks[v].datas = Ldatas[v]
        Stacks[v].datatyps = Ldatatyps[v]
        Stacks[v].datanames= Ldatanames[v]
        Stacks[v].normalize = True
        Stacks[v].options['pdfName'] = Stacks[v].options['pdfName'].replace('.pdf','_norm.pdf')
        Stacks[v].doPlot()
        print 'i am done!\n'
    print 'DOPLOT END'
#----------------------------------------------------
doPlot()
print 'tree_stack4'
sys.exit(0)
