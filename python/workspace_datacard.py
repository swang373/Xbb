#!/usr/bin/env python
from copy import copy, deepcopy
from math import sqrt
from multiprocessing import Pool
from optparse import OptionParser
import os
import sys
import warnings

import ROOT

from myutils import BetterConfigParser, GlobalFunction, HistoMaker, ParseInfo, printc

ROOT.gROOT.SetBatch(True)

#suppres the EvalInstace conversion warning bug
warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='creating converter.*' )

def useSpacesInDC(fileName):
    file_ = open(fileName,"r+")

    old = file_.read()
    ## get the maximum width of each colum (excluding the first lines)
    lineN = 0
    maxColumnWidth = [0]
    for line in old.split('\n'):
        lineN += 1
        if lineN<10: continue #skip the first 10 lines
        words = line.split('\t')
        for i in range(len(words)):
            if i>=len(maxColumnWidth): maxColumnWidth.append(0)
            if len(words[i])>maxColumnWidth[i]: maxColumnWidth[i]=len(words[i])
    ## replace the tabs with the new formatting (excluding the first lines)
    #newfile = open("newFile.txt","w+")
    lineN = 0
    file_.seek(0)
    for line in old.split('\n'):
        lineN += 1
        if lineN<10: #in the first 10 lines just replace '\t' with ' '
            file_.write(line.replace('\t',' ')+'\n')
            continue
        words = line.split('\t')
        newLine=""
        for i in range(len(words)): #use the new format!
            newLine += words[i].ljust(maxColumnWidth[i]+1)
        file_.write(newLine+'\n')
    file_.close()
    return

print '_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_'
print 'START DATACARD (workspace_datacard)'
print '_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_\n'

#--CONFIGURE---------------------------------------------------------------------

print 'Reading configuration files'
print '===========================\n'

argv = sys.argv
parser = OptionParser()
parser.add_option("-V", "--variable", dest="variable", default="",
                      help="variable for shape analysis")
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                      help="configuration file")
(opts, args) = parser.parse_args(argv)
config = BetterConfigParser()
config.read(opts.config)
var=opts.variable
#-------------------------------------------------------------------------------

#--read variables from config---------------------------------------------------
# 7 or 8TeV Analysis

print "Compile external macros"
print "=======================\n"

# compile external macros to compute variables on the fly
#ROOT.gSystem.CompileMacro("../plugins/PU.C")

print 'Assigne variables from  config'
print '==============================\n'

anaTag = config.get("Analysis","tag")
if not any([anaTag == '7TeV',anaTag == '8TeV',anaTag == '13TeV']):
    raise Exception("anaTag %s unknown. Specify 8TeV or 7TeV or 13TeV in the general config"%anaTag)
# Directories:
Wdir=config.get('Directories','Wdir')
vhbbpath=config.get('Directories','vhbbpath')
samplesinfo=config.get('Directories','samplesinfo')
path = config.get('Directories','dcSamples')
outpath=config.get('Directories','limits')
UseTrainSample = eval(config.get('Analysis','UseTrainSample'))
if UseTrainSample:
    print 'Training events will be used'
try:
    os.stat(outpath)
except:
    os.mkdir(outpath)
# parse histogram config:
treevar = config.get('dc:%s'%var,'var')
name = config.get('dc:%s'%var,'wsVarName')
title = name
# set binning
nBins = int(config.get('dc:%s'%var,'range').split(',')[0])
xMin = float(config.get('dc:%s'%var,'range').split(',')[1])
xMax = float(config.get('dc:%s'%var,'range').split(',')[2])
ROOToutname = config.get('dc:%s'%var,'dcName')
RCut = config.get('dc:%s'%var,'cut')
signals = config.get('dc:%s'%var,'signal').split(' ')
datas = config.get('dc:%s'%var,'dcBin')
Datacardbin=config.get('dc:%s'%var,'dcBin')
anType = config.get('dc:%s'%var,'type')
setup=eval(config.get('LimitGeneral','setup'))

if os.path.exists("$CMSSW_BASE/src/Xbb/interface/DrawFunctions_C.so"):
    print 'ROOT.gROOT.LoadMacro("$CMSSW_BASE/src/Xbb/interface/DrawFunctions_C.so")'
    ROOT.gROOT.LoadMacro("$CMSSW_BASE/src/Xbb/interface/DrawFunctions_C.so")

if os.path.exists("$CMSSW_BASE/src/Xbb/interface/VHbbNameSpace_h.so"):
    print 'ROOT.gROOT.LoadMacro("$CMSSW_BASE/src/Xbb/interface/VHbbNameSpace_h.so")'
    ROOT.gROOT.LoadMacro("$CMSSW_BASE/src/Xbb/interface/VHbbNameSpace_h.so")


print "Using",('dc:%s'%var,'var')
print name
print title
print nBins
print xMin
print xMax
print ROOToutname
print RCut
print signals
print datas
print Datacardbin
print anType
print setup

#Systematics:
#find out if BDT or MJJ:
bdt = False
mjj = False
cr = False
if str(anType) == 'BDT':
    bdt = True
    systematics = eval(config.get('LimitGeneral','sys_BDT'))
elif str(anType) == 'Mjj':
    mjj = True
    systematics = eval(config.get('LimitGeneral','sys_Mjj'))
elif str(anType) == 'cr':
    cr = True
    systematics = eval(config.get('LimitGeneral','sys_cr'))
else:
    print 'EXIT: please specify if your datacards are BDT, Mjj or cr.'
    sys.exit()

systematicsnaming = eval(config.get('LimitGeneral','systematicsnaming'))
sys_factor_dict = eval(config.get('LimitGeneral','sys_factor'))
sys_affecting = eval(config.get('LimitGeneral','sys_affecting'))

# weightF:
weightF = config.get('Weights','weightF')
# rescale stat shapes by sqrtN
rescaleSqrtN=eval(config.get('LimitGeneral','rescaleSqrtN'))
# get nominal cutstring:
treecut = config.get('Cuts',RCut)
# Train flag: splitting of samples
TrainFlag = eval(config.get('Analysis','TrainFlag'))
# toy data option:
toy=eval(config.get('LimitGeneral','toy'))
# blind data option:
blind=eval(config.get('LimitGeneral','blind'))
# additional blinding cut:
addBlindingCut = None
if config.has_option('LimitGeneral','addBlindingCut'):
    addBlindingCut = config.get('LimitGeneral','addBlindingCut')
    print 'adding add. blinding cut'
#on control region cr never blind. Overwrite whatever is in the config
if str(anType) == 'cr':
    if blind:
        print '@WARNING: Changing blind to false since you are running for control region.'
    blind = False
if blind:
    printc('red','', 'I AM BLINDED!')
#get List of backgrounds in use:
backgrounds = eval(config.get('LimitGeneral','BKG'))
#Groups for adding samples together
GroupDict = eval(config.get('LimitGeneral','Group'))
#naming for DC
Dict= eval(config.get('LimitGeneral','Dict'))
#treating statistics bin-by-bin:
binstat = eval(config.get('LimitGeneral','binstat'))
# Use the rebinning:
rebin_active=eval(config.get('LimitGeneral','rebin_active'))
#if str(anType) == 'cr':
if not bdt:
    if rebin_active:
        print '@WARNING: Changing rebin_active to false since you are running for control region.'
    rebin_active = False
# ignore stat shapes
ignore_stats = eval(config.get('LimitGeneral','ignore_stats'))
#max_rel = float(config.get('LimitGeneral','rebin_max_rel'))
signal_inject=config.get('LimitGeneral','signal_inject')
#----------------------------------------------------------------------------

#--Setup--------------------------------------------------------------------
#Assign Pt region for sys factors
print 'Assign Pt region for sys factors'
print '================================\n'

if 'HighPtLooseBTag' in ROOToutname:
    pt_region = 'HighPtLooseBTag'
elif 'HighPt' in ROOToutname or 'highPt' in ROOToutname or 'highpt' in ROOToutname:
    pt_region = 'HighPt'
elif 'MedPt' in ROOToutname:
    pt_region = 'MedPt'
elif 'LowPt' in ROOToutname or 'lowPt' in ROOToutname or 'lowpt' in ROOToutname:
    pt_region = 'LowPt'
elif 'ATLAS' in ROOToutname:
    pt_region = 'HighPt'
elif 'MJJ' in ROOToutname:
    pt_region = 'HighPt'
else:
    print "Unknown Pt region"
    pt_region = 'NoSysRegion'
    #sys.exit("Unknown Pt region")
# Set rescale factor of 2 in case of TrainFalg
if TrainFlag:
    MC_rescale_factor=2.
    print 'I RESCALE BY 2.0'
else: MC_rescale_factor = 1.
#systematics up/down
UD = ['Up','Down']

print 'Parse the sample information'
print '============================\n'
#Parse samples configuration
info = ParseInfo(samplesinfo,path)
# get all the treeCut sets
# create different sample Lists

print 'Get the sample list'
print '===================\n'
all_samples = info.get_samples(signals+backgrounds)
print 'workspace_datacard-all_samples:',[job.name for job in all_samples]

signal_samples = info.get_samples(signals)
print 'signal samples:',[job.name for job in signal_samples]

background_samples = info.get_samples(backgrounds)
data_sample_names = config.get('dc:%s'%var,'data').split(' ')
data_samples = info.get_samples(data_sample_names)

print 'The signal sample list is\n'
for samp in signal_samples:
    print samp
print 'The background sample list is\n'
for samp in background_samples:
    print samp
print 'The data samples are'
for samp in data_samples:
    print samp
#-------------------------------------------------------------------------------------------------

optionsList=[]

def appendList():
    optionsList.append({
        'cut': copy(_cut),
        'var': copy(_treevar),
        'name': copy(_name),
        'nBins': nBins,
        'xMin': xMin,
        'xMax': xMax,
        'weight': copy(_weight),
        'blind': blind,
        'sys_cut': copy(_sys_cut),
    })

#nominal
_cut = treecut
_treevar = treevar
_name = title
_weight = weightF
#ie. take count from 'CountWeighted->GetBinContent(1)'
_sys_cut = treecut
appendList()

print "Using weightF:",weightF
print 'Assign the systematics'
print '======================\n'

# Shape Systematics

JER_or_JES = {
    'JER',
    'PileUpDataMC',
    'PileUpPtRef',
    'PileUpPtBB',
    'PileUpPtEC1',
    'RelativeJEREC1',
    'RelativeFSR',
    'RelativeStatFSR',
    'RelativeStatEC',
    'RelativePtBB',
    'RelativePtEC1',
    'AbsoluteScale',
    'AbsoluteMPFBias',
    'AbsoluteStat',
    'SinglePionECAL',
    'SinglePionHCAL',
    'Fragmentation',
    'TimePtEta',
    'FlavorQCD',
}

for syst in systematics:
    for Q in UD:

        _cut = treecut
        _name = title
        _weight = weightF
        _treevar = treevar
        _sys_cut = treecut

        # Pileup Weight Variations
        if 'pileUp' in syst:
            _weight = _weight.replace('puWeight', 'puWeight{}'.format(Q))
        # TTbar nCentralJet Weight Variations
        elif 'TT_nJetCentral' in syst:
            _weight = _weight.replace('VHbb::weight_TTbar_nJetCentral', 'VHbb::weight_TTbar_nJetCentral_{}'.format(Q))
        # LHE Scale Variations(muF, muR)
        elif 'muF' in syst:
            if Q is 'Up':
                _weight += '*(LHE_weights_scale_wgt[0])'
            if Q is 'Down':
                _weight += '*(LHE_weights_scale_wgt[1])'
        elif 'muR' in syst:
            if Q is 'Up':
                _weight += '*(LHE_weights_scale_wgt[2])'
            if Q is 'Down':
                _weight += '*(LHE_weights_scale_wgt[3])'
        # Moriond2017 bTag Weights
        elif 'bTagWeight' in syst:
            if 'JES' in syst:
                if 'HighCentral' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_JESHighCentral{}'.format(Q))
                elif 'LowCentral' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_JESLowCentral{}'.format(Q))
                elif 'HighForward' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_JESHighForward{}'.format(Q))
                elif 'LowForward' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_JESLowForward{}'.format(Q))
            elif 'LF' in syst and 'Stats' not in syst:
                if 'HighCentral' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_LFHighCentral{}'.format(Q))
                elif 'LowCentral' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_LFLowCentral{}'.format(Q))
                elif 'HighForward' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_LFHighForward{}'.format(Q))
                elif 'LowForward' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_LFLowForward{}'.format(Q))
            elif 'HF' in syst and 'Stats' not in syst:
                if 'HighCentral' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_HFHighCentral{}'.format(Q))
                elif 'LowCentral' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_HFLowCentral{}'.format(Q))
                elif 'HighForward' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_HFHighForward{}'.format(Q))
                elif 'LowForward' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_HFLowForward{}'.format(Q))
            elif 'LFStats1' in syst:
                if 'HighCentral' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_LFStats1HighCentral{}'.format(Q))
                elif 'LowCentral' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_LFStats1LowCentral{}'.format(Q))
                elif 'HighForward' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_LFStats1HighForward{}'.format(Q))
                elif 'LowForward' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_LFStats1LowForward{}'.format(Q))
            elif 'LFStats2' in syst:
                if 'HighCentral' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_LFStats2HighCentral{}'.format(Q))
                elif 'LowCentral' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_LFStats2LowCentral{}'.format(Q))
                elif 'HighForward' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_LFStats2HighForward{}'.format(Q))
                elif 'LowForward' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_LFStats2LowForward{}'.format(Q))
            elif 'HFStats1' in syst:
                if 'HighCentral' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_HFStats1HighCentral{}'.format(Q))
                elif 'LowCentral' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_HFStats1LowCentral{}'.format(Q))
                elif 'HighForward' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_HFStats1HighForward{}'.format(Q))
                elif 'LowForward' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_HFStats1LowForward{}'.format(Q))
            elif 'HFStats2' in syst:
                if 'HighCentral' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_HFStats2HighCentral{}'.format(Q))
                elif 'LowCentral' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_HFStats2LowCentral{}'.format(Q))
                elif 'HighForward' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_HFStats2HighForward{}'.format(Q))
                elif 'LowForward' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_HFStats2LowForward{}'.format(Q))
            elif 'cErr1' in syst:
                if 'HighCentral' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_cErr1HighCentral{}'.format(Q))
                elif 'LowCentral' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_cErr1LowCentral{}'.format(Q))
                elif 'HighForward' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_cErr1HighForward{}'.format(Q))
                elif 'LowForward' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_cErr1LowForward{}'.format(Q))
            elif 'cErr2' in syst:
                if 'HighCentral' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_cErr2HighCentral{}'.format(Q))
                elif 'LowCentral' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_cErr2LowCentral{}'.format(Q))
                elif 'HighForward' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_cErr2HighForward{}'.format(Q))
                elif 'LowForward' in syst:
                    _weight = _weight.replace('bTagWeightCMVAv2_Moriond', 'bTagWeightCMVAV2_Moriond_cErr2LowForward{}'.format(Q))
        # JER and Factorized JEC Systematics
        elif syst in JER_or_JES:
            mass_cut = (
                '(HCMVAV2_reg_mass{0}'
                '||HCMVAV2_reg_mass_corrJERUp{0}||HCMVAV2_reg_mass_corrJERDown{0}'
                '||HCMVAV2_reg_mass_corrPileUpDataMCUp{0}||HCMVAV2_reg_mass_corrPileUpDataMCDown{0}'
                '||HCMVAV2_reg_mass_corrPileUpPtRefUp{0}||HCMVAV2_reg_mass_corrPileUpPtRefDown{0}'
                '||HCMVAV2_reg_mass_corrPileUpPtBBUp{0}||HCMVAV2_reg_mass_corrPileUpPtBBDown{0}'
                '||HCMVAV2_reg_mass_corrPileUpPtEC1Up{0}||HCMVAV2_reg_mass_corrPileUpPtEC1Down{0}'
                '||HCMVAV2_reg_mass_corrRelativeJEREC1Up{0}||HCMVAV2_reg_mass_corrRelativeJEREC1Down{0}'
                '||HCMVAV2_reg_mass_corrRelativeFSRUp{0}||HCMVAV2_reg_mass_corrRelativeFSRDown{0}'
                '||HCMVAV2_reg_mass_corrRelativeStatFSRUp{0}||HCMVAV2_reg_mass_corrRelativeStatFSRDown{0}'
                '||HCMVAV2_reg_mass_corrRelativeStatECUp{0}||HCMVAV2_reg_mass_corrRelativeStatECDown{0}'
                '||HCMVAV2_reg_mass_corrRelativePtBBUp{0}||HCMVAV2_reg_mass_corrRelativePtBBDown{0}'
                '||HCMVAV2_reg_mass_corrRelativePtEC1Up{0}||HCMVAV2_reg_mass_corrRelativePtEC1Down{0}'
                '||HCMVAV2_reg_mass_corrAbsoluteScaleUp{0}||HCMVAV2_reg_mass_corrAbsoluteScaleDown{0}'
                '||HCMVAV2_reg_mass_corrAbsoluteMPFBiasUp{0}||HCMVAV2_reg_mass_corrAbsoluteMPFBiasDown{0}'
                '||HCMVAV2_reg_mass_corrAbsoluteStatUp{0}||HCMVAV2_reg_mass_corrAbsoluteStatDown{0}'
                '||HCMVAV2_reg_mass_corrSinglePionECALUp{0}||HCMVAV2_reg_mass_corrSinglePionECALDown{0}'
                '||HCMVAV2_reg_mass_corrSinglePionHCALUp{0}||HCMVAV2_reg_mass_corrSinglePionHCALDown{0}'
                '||HCMVAV2_reg_mass_corrFragmentationUp{0}||HCMVAV2_reg_mass_corrFragmentationDown{0}'
                '||HCMVAV2_reg_mass_corrTimePtEtaUp{0}||HCMVAV2_reg_mass_corrTimePtEtaDown{0}'
                '||HCMVAV2_reg_mass_corrFlavorQCDUp{0}||HCMVAV2_reg_mass_corrFlavorQCDDown{0})'
            )

            if bdt:
                _cut = _cut.replace('HCMVAV2_reg_mass>60', mass_cut.format('>60'))
                _cut = _cut.replace('HCMVAV2_reg_mass<160', mass_cut.format('<160'))
                _treevar = treevar.replace('.nominal', '.{0}_{1}'.format(syst, Q))
                _sys_cut = _sys_cut.replace('HCMVAV2_reg_mass', 'HCMVAV2_reg_mass_corr{0}{1}'.format(syst, Q))
            else:
                if 'Zbb' in name or 'Wbb' in name:
                    _cut = _cut.replace('HCMVAV2_reg_mass<60', mass_cut.format('<60'))
                    _cut = _cut.replace('HCMVAV2_reg_mass>160', mass_cut.format('>160'))
                _sys_cut = _sys_cut.replace('HCMVAV2_reg_mass', 'HCMVAV2_reg_mass_corr{0}{1}'.format(syst, Q))
        else:
            _treevar = treevar

        print '----> New Weights       :',syst, ' : ', _weight
        print '--->  New tree variable : ', _treevar
        print '----> New tree cut      : ', _cut
        print '----> New SYS cut      : ', _sys_cut
        #append
        appendList()

#print '===================\n'
#print 'The option list is', optionsList


print 'Preparations for Histograms (HistoMakeri)'
print '=========================================\n'

mc_hMaker = HistoMaker(all_samples,path,config,optionsList,GroupDict)
data_hMaker = HistoMaker(data_samples,path,config,[optionsList[0]])

print 'Calculate luminosity'
print '====================\n'
#Calculate lumi
lumi = 0.
nData = 0
for job in data_samples:
    nData += 1
    lumi += float(job.lumi)

if nData > 1:
    lumi = lumi/float(nData)

mc_hMaker.lumi = lumi
data_hMaker.lumi = lumi

if addBlindingCut:
    for i in range(len(mc_hMaker.optionsList)):
        mc_hMaker.optionsList[i]['cut'] += ' & %s' %addBlindingCut
    for i in range(len(data_hMaker.optionsList)):
        data_hMaker.optionsList[i]['cut'] += ' & %s' %addBlindingCut


if rebin_active:
    print "background_samples: ",background_samples
    mc_hMaker.calc_rebin(background_samples)
    #transfer rebinning info to data maker
    data_hMaker.norebin_nBins = copy(mc_hMaker.norebin_nBins)
    data_hMaker.rebin_nBins = copy(mc_hMaker.rebin_nBins)
    data_hMaker.nBins = copy(mc_hMaker.nBins)
    data_hMaker._rebin = copy(mc_hMaker._rebin)
    data_hMaker.mybinning = deepcopy(mc_hMaker.mybinning)

all_histos = {}
data_histos = {}

print '\n\t...fetching histos...\n'


inputs=[]
for job in all_samples:
    inputs.append((mc_hMaker,"get_histos_from_tree",(job,True)))

multiprocess=int(config.get('Configuration','nprocesses'))
outputs = []
if multiprocess>1:
    p = Pool(multiprocess)
    print 'launching get_histos_from_tree with ',multiprocess,' processes'
    outputs = p.map(GlobalFunction, inputs)
else:
    print 'launching get_histos_from_tree with ',multiprocess,' processes'
    for input_ in inputs:
        outputs.append(getattr(input_[0],input_[1])(*input_[2])) #ie. mc_hMaker.get_histos_from_tree(job)

print "job.name and all_histos[job.name]:"
for i,job in enumerate(all_samples):
    all_histos[job.name] = outputs[i]


for job in data_samples:
    print '\t- %s'%job
    data_histos[job.name] = data_hMaker.get_histos_from_tree(job)[0]['DATA']

print '\t> done <\n'

print 'Get the bkg histo'
print '=================\n'
i=0
for job in background_samples:
    print job.name
    htree = all_histos[job.name][0].values()[0]
    if not i:
        hDummy = copy(htree)
    else:
        hDummy.Add(htree,1)
    del htree
    i+=1
#?
if signal_inject:
    signal_inject = info.get_samples([signal_inject])
    sig_hMaker = HistoMaker(signal_inject,path,config,optionsList,GroupDict)
    sig_hMaker.lumi = lumi
    if rebin_active:
        sig_hMaker.norebin_nBins = copy(mc_hMaker.norebin_nBins)
        sig_hMaker.rebin_nBins = copy(mc_hMaker.rebin_nBins)
        sig_hMaker.nBins = copy(mc_hMaker.nBins)
        sig_hMaker._rebin = copy(mc_hMaker._rebin)
        sig_hMaker.mybinning = deepcopy(mc_hMaker.mybinning)

print 'Get the signal histo'
print '====================\n'
for job in signal_inject:
    htree = sig_hMaker.get_histos_from_tree(job)
    hDummy.Add(htree[0].values()[0],1)
    del htree

print 'Get the data histo'
print '==================\n'
nData = 0
for job in data_histos:
    if nData == 0:
        theData = data_histos[job]
        nData = 1
    else:
        theData.Add(data_histos[job])


print 'END DEBUG'


#-- Write Files-----------------------------------------------------------------------------------
# generate the TH outfile:
print 'Start writing the files'
print '=======================\n'

print 'Creating output file'
print '====================\n'
outfile = ROOT.TFile(outpath+'vhbb_TH_'+ROOToutname+'.root', 'RECREATE')
outfile.mkdir(Datacardbin,Datacardbin)
outfile.cd(Datacardbin)
# generate the Workspace:
WS = ROOT.RooWorkspace('%s'%Datacardbin,'%s'%Datacardbin) #Zee
print 'WS initialized'
disc= ROOT.RooRealVar(name,name,xMin,xMax)
obs = ROOT.RooArgList(disc)
#
ROOT.gROOT.SetStyle("Plain")

#order and add all together
final_histos = {}

print '\n\t--> Ordering and Adding Histos\n'

print 'workspace_datacard-all_samples:',[all_histos['%s'%job][0] for job in all_samples]

jobnames = [job.name for job in all_samples]

#NOMINAL:
final_histos['nominal'] = HistoMaker.orderandadd([all_histos['%s'%job][0] for job in all_samples],setup)

#SYSTEMATICS:
ind = 1
#print 'systematics is', systematics

print 'all_histos[job.name]',all_histos[job.name]
print 'len(all_histos[job.name])',len(all_histos[job.name])

print 'add UD sys'
print '==========\n'
for syst in systematics:
    for Q in UD:
        final_histos['%s_%s'%(systematicsnaming[syst],Q)] = HistoMaker.orderandadd([all_histos[job.name][ind] for job in all_samples],setup)
        ind+=1

if not ignore_stats:
    #make statistical shapes:
    print 'Make the statistical shapes'
    print '===========================\n'
    if not binstat:
        for Q in UD:
            final_histos['%s_%s'%(systematicsnaming['stats'],Q)] = {}
        for job,hist in final_histos['nominal'].items():
            errorsum=0
            for j in range(hist.GetNbinsX()+1):
                errorsum=errorsum+(hist.GetBinError(j))**2
            errorsum=sqrt(errorsum)
            total=hist.Integral()
            for Q in UD:
                final_histos['%s_%s'%(systematicsnaming['stats'],Q)][job] = hist.Clone()
                for j in range(hist.GetNbinsX()+1):
                    if Q == 'Up':
                        if rescaleSqrtN and total:
                            final_histos['%s_%s'%(systematicsnaming['stats'],Q)][job].SetBinContent(j,max(1.E-6,hist.GetBinContent(j)+hist.GetBinError(j)/total*errorsum))
                        else:
                            final_histos['%s_%s'%(systematicsnaming['stats'],Q)][job].SetBinContent(j,max(1.E-6,hist.GetBinContent(j)+hist.GetBinError(j)))
                    if Q == 'Down':
                        if rescaleSqrtN and total:
                            final_histos['%s_%s'%(systematicsnaming['stats'],Q)][job].SetBinContent(j,max(1.E-6,hist.GetBinContent(j)-hist.GetBinError(j)/total*errorsum))
                        else:
                            final_histos['%s_%s'%(systematicsnaming['stats'],Q)][job].SetBinContent(j,max(1.E-6,hist.GetBinContent(j)-hist.GetBinError(j)))
    else:
        print "Running Statistical uncertainty"
        threshold =  1 #stat error / sqrt(value). It was 0.5
        print "threshold",threshold
        binsBelowThreshold = {}
        for bin in range(1,nBins+1):
            for Q in UD:
                final_histos['%s_bin%s_%s'%(systematicsnaming['stats'],bin,Q)] = {}
            for job,hist in final_histos['nominal'].items():
                if not job in binsBelowThreshold.keys(): binsBelowThreshold[job] = []
                print "binsBelowThreshold",binsBelowThreshold
                print "hist.GetBinContent(bin)",hist.GetBinContent(bin)
                print "hist.GetBinError(bin)",hist.GetBinError(bin)
                if hist.GetBinContent(bin) > 0.:
                    if hist.GetBinError(bin)/sqrt(hist.GetBinContent(bin)) > threshold and hist.GetBinContent(bin) >= 1.:
                        binsBelowThreshold[job].append(bin)
                    elif hist.GetBinError(bin)/(hist.GetBinContent(bin)) > threshold and hist.GetBinContent(bin) < 1.:
                        binsBelowThreshold[job].append(bin)
                for Q in UD:
                    final_histos['%s_bin%s_%s'%(systematicsnaming['stats'],bin,Q)][job] = hist.Clone()
                    if Q == 'Up':
                        final_histos['%s_bin%s_%s'%(systematicsnaming['stats'],bin,Q)][job].SetBinContent(bin,max(1.E-6,hist.GetBinContent(bin)+hist.GetBinError(bin)))
                    if Q == 'Down':
                        final_histos['%s_bin%s_%s'%(systematicsnaming['stats'],bin,Q)][job].SetBinContent(bin,max(1.E-6,hist.GetBinContent(bin)-hist.GetBinError(bin)))


#print "binsBelowThreshold:",binsBelowThreshold
print 'Start writing shapes in WS'
print '==========================\n'
print 'final_histos:',final_histos
#write shapes in WS:
for key in final_histos:
    for job, hist in final_histos[key].items():
        if 'nominal' == key:
            hist.SetName('%s'%(Dict[job]))
            hist.Write()
            rooDataHist = ROOT.RooDataHist('%s' %(Dict[job]),'%s'%(Dict[job]),obs, hist)
            getattr(WS,'import')(rooDataHist)
        for Q in UD:
            if Q in key:
                theSyst = key.replace('_%s'%Q,'')
            else:
                continue
            if systematicsnaming['stats'] in key:
                nameSyst = '%s_%s_%s' %(theSyst,Dict[job],Datacardbin)
            elif systematicsnaming['model'] in key:
                nameSyst = '%s_%s' %(theSyst,Dict[job])
            else:
                nameSyst = theSyst
            hist.SetName('%s%s%s' %(Dict[job],nameSyst,Q))
            hist.Write()
            rooDataHist = ROOT.RooDataHist('%s%s%s' %(Dict[job],nameSyst,Q),'%s%s%s'%(Dict[job],nameSyst,Q),obs, hist)
            getattr(WS,'import')(rooDataHist)

if toy or signal_inject:
    hDummy.SetName('data_obs')
    hDummy.Write()
    rooDataHist = ROOT.RooDataHist('data_obs','data_obs',obs, hDummy)
else:
    theData.SetName('data_obs')
    theData.Write()
    rooDataHist = ROOT.RooDataHist('data_obs','data_obs',obs, theData)

getattr(WS,'import')(rooDataHist)

WS.writeToFile(outpath+'vhbb_WS_'+ROOToutname+'.root')

# now we have a Dict final_histos with sets of all grouped MCs for all systematics:
# nominal, ($SYS_Up/Down)*4, weightF_sys_Up/Down, stats_Up/Down

print '\n\t >>> PRINTOUT PRETTY TABLE <<<\n'
#header
printout = ''
printout += '%-25s'%'Process'
printout += ':'
for item, val in final_histos['nominal'].items():
    printout += '%-12s'%item
print printout+'\n'
for key in final_histos:
    printout = ''
    printout += '%-25s'%key
    printout += ':'
    for item, val in final_histos[key].items():
        printout += '%-12s'%str('%0.5f'%val.Integral())
    print printout

#-----------------------------------------------------------------------------------------------------------

# -------------------- write DATAcard: ----------------------------------------------------------------------
DCprocessseparatordict = {'WS':':','TH':'/'}
# create two datacards: for TH an WS
for DCtype in ['WS','TH']:
    columns=len(setup)
    fileName = outpath+'vhbb_DC_%s_%s.txt'%(DCtype,ROOToutname)
    f = open(fileName,'w')
    f.write('imax\t1\tnumber of channels\n')
    f.write('jmax\t%s\tnumber of backgrounds (\'*\' = automatic)\n'%(columns-1))
    f.write('kmax\t*\tnumber of nuisance parameters (sources of systematical uncertainties)\n\n')
    f.write('shapes * * vhbb_%s_%s.root $CHANNEL%s$PROCESS $CHANNEL%s$PROCESS$SYSTEMATIC\n\n'%(DCtype,ROOToutname,DCprocessseparatordict[DCtype],DCprocessseparatordict[DCtype]))
    f.write('bin\t%s\n\n'%Datacardbin)
    if toy or signal_inject:
        f.write('observation\t%s\n\n'%(hDummy.Integral()))
    else:
        f.write('observation\t%s\n\n'%(theData.Integral()))
    # datacard bin
    f.write('bin\t')
    for c in range(0,columns): f.write('\t%s'%Datacardbin)
    f.write('\n')
    # datacard process
    f.write('process\t')
    for c in setup: f.write('\t%s'%Dict[c])
    f.write('\n')
    f.write('process\t')
    for c in range(0,columns): f.write('\t%s'%(c-len(signals)+2))
    f.write('\n')
    # datacard yields
    f.write('rate\t')
    print "workspace_datacard-setup: ", setup
    print "workspace_datacard-final_histos: ", final_histos
    for c in setup:
        f.write('\t%s'%final_histos['nominal'][c].Integral())
    f.write('\n')
    # get list of systematics in use
    InUse=eval(config.get('Datacard','InUse_%s_%s'%(str(anType), pt_region)))
    # write non-shape systematics
    for item in InUse:
        f.write(item)
        what=eval(config.get('Datacard',item))
        f.write('\t%s'%what['type'])
        for c in setup:
            if c in what:
                if '_eff_e' in item and 'Zmm' in data_sample_names: f.write('\t-')
                elif '_eff_m' in item and 'Zee' in data_sample_names: f.write('\t-')
                elif '_trigger_e' in item and 'Zmm' in data_sample_names: f.write('\t-')
                elif '_trigger_m' in item and 'Zee' in data_sample_names: f.write('\t-')
                else:
                    f.write('\t%s'%what[c])
            else:
                f.write('\t-')
        f.write('\n')
    if not ignore_stats:
    # Write statistical shape variations
        if binstat:
            for c in setup:
                for bin in range(0,nBins):
                    if bin in binsBelowThreshold[c]:
                        f.write('%s_bin%s_%s_%s\tshape'%(systematicsnaming['stats'],bin,Dict[c],Datacardbin))
                        for it in range(0,columns):
                            if it == setup.index(c):
                                f.write('\t1.0')
                            else:
                                f.write('\t-')
                        f.write('\n')
        else:
            for c in setup:
                f.write('%s_%s_%s\tshape'%(systematicsnaming['stats'],Dict[c],Datacardbin))
                for it in range(0,columns):
                    if it == setup.index(c):
                        f.write('\t1.0')
                    else:
                        f.write('\t-')
                f.write('\n')
    # regular systematics
    for sys in systematics:
        sys_factor=sys_factor_dict[sys]
        f.write('%s\tshape'%systematicsnaming[sys])
        for c in setup:
            if c in sys_affecting[sys] or 'all' in sys_affecting[sys]:
                f.write('\t%s'%sys_factor)
            else:
                f.write('\t-')
        f.write('\n')

    # write rateParams systematics (free parameters)
    rateParams=eval(config.get('Datacard','rateParams_%s_%s'%(str(anType), pt_region)))
    try:
        rateParamRange=eval(config.get('Datacard','rateParamRange'))
    except:
        rateParamRange=[0,10]
    assert len(rateParamRange) is 2, 'rateParamRange is not 2! rateParamRange:'+ len(rateParamRange)
    for rateParam in rateParams:
        dictProcs=eval(config.get('Datacard',rateParam))
        for proc in dictProcs.keys():
            f.write(rateParam+'\trateParam\t'+Datacardbin+'\t'+proc+'\t'+str(dictProcs[proc])+' ['+str(rateParamRange[0])+','+str(rateParamRange[1])+']\n')
    f.close()
    useSpacesInDC(fileName)

# --------------------------------------------------------------------------

WS.IsA().Destructor(WS)
outfile.Close()
