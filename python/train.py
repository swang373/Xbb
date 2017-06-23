#!/usr/bin/env python
from optparse import OptionParser
import sys
import pickle
import ROOT 
ROOT.gROOT.SetBatch(True)
from array import array
#warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='creating converter.*' )
#usage: ./train run gui

#CONFIGURE
argv = sys.argv
parser = OptionParser()
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
                          help="Verbose mode.")
parser.add_option("-T", "--training", dest="training", default="",
                      help="Training")
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                      help="configuration file")
parser.add_option("-S","--setting", dest="MVAsettings", default='',
                      help="Parameter setting string")
parser.add_option("-N","--name", dest="set_name", default='',
                      help="Parameter setting name. Output files will have this name")
parser.add_option("-L","--local",dest="local", default=True,
                      help="True to run it locally. False to run on batch system using config")

(opts, args) = parser.parse_args(argv)
if opts.config =="":
        opts.config = "config"

#Import after configure to get help message
from myutils import BetterConfigParser, mvainfo, ParseInfo, TreeCache

import os
if os.path.exists("../interface/DrawFunctions_C.so"):
    print 'ROOT.gROOT.LoadMacro("../interface/DrawFunctions_C.so")'
    ROOT.gROOT.LoadMacro("../interface/DrawFunctions_C.so")

#load config
config = BetterConfigParser()
config.read(opts.config)
anaTag = config.get("Analysis","tag")
run=opts.training
gui=opts.verbose


#print "Compile external macros"
#print "=======================\n"

## compile external macros to compute variables on the fly
#ROOT.gSystem.CompileMacro("../plugins/PU.C")

#GLOABAL rescale from Train/Test Spliiting:
global_rescale=2.

#get locations:
MVAdir=config.get('Directories','vhbbpath')+'/python/weights/'
samplesinfo=config.get('Directories','samplesinfo')

#systematics
systematics=config.get('systematics','systematics')
systematics=systematics.split(' ')

weightF=config.get('Weights','weightF')

VHbbNameSpace=config.get('VHbbNameSpace','library')
ROOT.gSystem.Load(VHbbNameSpace)

#CONFIG
#factory
factoryname=config.get('factory','factoryname')
factorysettings=config.get('factory','factorysettings')
#MVA
MVAtype=config.get(run,'MVAtype')
#MVA name and settings. From local running or batch running different option
print opts.local
optimisation_training = False
if not  opts.MVAsettings == '':
    print 'This is an optimisation training'
    opt_MVAsettings = opts.MVAsettings
    optimisation_training = True

if(eval(opts.local)):
  print 'Local run'
  MVAname=run
  MVAsettings=config.get(run,'MVAsettings')
  if optimisation_training:
      MVAname=opts.set_name
      if not opt_MVAsettings == 'main_par':
          opt_Dict = dict(item.split("=") for item in opt_MVAsettings.split(","))
          for key in opt_Dict:
              for par in MVAsettings.split(':'):
                  if not key in par: continue
                  par_new = par[:par.find('=')+1]
                  par_new += opt_Dict[key]
                  MVAsettings = MVAsettings.replace(par,par_new)

elif(opts.set_name!='' and opts.MVAsettings!=''):
  print 'Batch run'
  MVAname=opts.set_name
  MVAsettings=opts.MVAsettings
else :
  print 'Problem in configuration. Missing or inconsitent information Check input options'
  sys.exit()  
print '@DEBUG: MVAname'
print 'input : ' + opts.set_name
print 'used : ' + MVAname

fnameOutput = MVAdir+factoryname+'_'+MVAname+'.root'
print '@DEBUG: output file name : ' + fnameOutput


#sys.exit()

#locations
path=config.get('Directories','MVAin')

TCutname=config.get(run, 'treeCut')
TCut=config.get('Cuts',TCutname)
#print TCut

#signals
signals=config.get(run,'signals')
signals=eval(signals)
print 'signals are', signals
#backgrounds
backgrounds=config.get(run,'backgrounds')
backgrounds=eval(backgrounds)
treeVarSet=config.get(run,'treeVarSet')
        
#variables
#TreeVar Array
MVA_Vars={}
MVA_Vars['Nominal']=config.get(treeVarSet,'Nominal')
MVA_Vars['Nominal']=MVA_Vars['Nominal'].split(' ')    

#Infofile
info = ParseInfo(samplesinfo,path)

#Workdir
workdir=ROOT.gDirectory.GetPath()


#Remove EventForTraining in order to run the MVA directly from the PREP step
TrainCut='%s & !((evt%s)==0 || isData)'%(TCut,'%2')
EvalCut= '%s & ((evt%s)==0 || isData)'%(TCut,'%2')
#TrainCut='%s & EventForTraining==1'%TCut
#EvalCut='%s & EventForTraining==0'%TCut

print "TrainCut:",TrainCut
print "EvalCut:",EvalCut
cuts = [TrainCut,EvalCut] 


samples = []
print 'agains, signals is', signals
samples = info.get_samples(signals+backgrounds)

print "XXXXXXXXXXXXXXXX"

tc = TreeCache(cuts,samples,path,config)

output = ROOT.TFile.Open(fnameOutput, "RECREATE")

print '\n\t>>> READING EVENTS <<<\n'

signal_samples = info.get_samples(signals)
background_samples = info.get_samples(backgrounds)

#TRAIN trees
Tbackgrounds = []
TbScales = []
Tsignals = []
TsScales = []
#EVAL trees
Ebackgrounds = []
EbScales = []
Esignals = []
EsScales = []

#load trees
for job in signal_samples:
    print '\tREADING IN %s AS SIG'%job.name
    Tsignal = tc.get_tree(job,TrainCut)
    ROOT.gDirectory.Cd(workdir)
    TsScale = tc.get_scale(job,config)*global_rescale    
    Tsignals.append(Tsignal)
    TsScales.append(TsScale)
    Esignal = tc.get_tree(job,EvalCut)
    Esignals.append(Esignal)
    EsScales.append(TsScale)
    print '\t\t\tTraining %s events'%Tsignal.GetEntries()
    print '\t\t\tEval %s events'%Esignal.GetEntries()
for job in background_samples:
    print '\tREADING IN %s AS BKG'%job.name
    Tbackground = tc.get_tree(job,TrainCut)
    ROOT.gDirectory.Cd(workdir)
    TbScale = tc.get_scale(job,config)*global_rescale
    Tbackgrounds.append(Tbackground)
    TbScales.append(TbScale)
    Ebackground = tc.get_tree(job,EvalCut)
    ROOT.gDirectory.Cd(workdir)
    Ebackgrounds.append(Ebackground)
    EbScales.append(TbScale)
    print '\t\t\tTraining %s events'%Tbackground.GetEntries()
    print '\t\t\tEval %s events'%Ebackground.GetEntries()


# print 'creating TMVA.Factory object'
factory = ROOT.TMVA.Factory(factoryname, output, factorysettings)

#set input trees
# print 'set signal input trees'
for i in range(len(Tsignals)):
    factory.AddSignalTree(Tsignals[i], TsScales[i], ROOT.TMVA.Types.kTraining)
    factory.AddSignalTree(Esignals[i], EsScales[i], ROOT.TMVA.Types.kTesting)

# print 'set background input trees'
for i in range(len(Tbackgrounds)):
    if (Tbackgrounds[i].GetEntries()>0):
        factory.AddBackgroundTree(Tbackgrounds[i], TbScales[i], ROOT.TMVA.Types.kTraining)

    if (Ebackgrounds[i].GetEntries()>0):
        factory.AddBackgroundTree(Ebackgrounds[i], EbScales[i], ROOT.TMVA.Types.kTesting)
        
# print 'add the variables'
for var in MVA_Vars['Nominal']:
    factory.AddVariable(var,'D') # add the variables

#Execute TMVA
# print 'Execute TMVA: SetSignalWeightExpression'
factory.SetSignalWeightExpression(weightF)
# print 'Execute TMVA: SetBackgroundWeightExpression'
factory.SetBackgroundWeightExpression(weightF)
factory.Verbose()
# print 'Execute TMVA: factory.BookMethod'
my_methodBase_bdt = factory.BookMethod(MVAtype,MVAname,MVAsettings)
# print 'Execute TMVA: TrainMethod'
my_methodBase_bdt.TrainMethod()
#factory.TrainAllMethods()
# print 'Execute TMVA: TestAllMethods'
factory.TestAllMethods()
# print 'Execute TMVA: EvaluateAllMethods'
factory.EvaluateAllMethods()
# print 'Execute TMVA: output.Write'
output.Write()


#training performance parameters

#output.ls()
output.cd('Method_%s'%MVAtype)
#ROOT.gDirectory.ls()
ROOT.gDirectory.cd(MVAname)

# print 'Get ROCs'
rocIntegral_default=my_methodBase_bdt.GetROCIntegral()
roc_integral_test = my_methodBase_bdt.GetROCIntegral(ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_S'),ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_B'))
roc_integral_train = my_methodBase_bdt.GetROCIntegral(ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_Train_S'),ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_Train_B'))
# print 'Get significances'
significance = my_methodBase_bdt.GetSignificance()
separation_test = my_methodBase_bdt.GetSeparation(ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_S'),ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_B'))
separation_train = my_methodBase_bdt.GetSeparation(ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_Train_S'),ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_Train_B'))
ks_signal = (ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_S')).KolmogorovTest(ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_Train_S'))
ks_bkg= (ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_B')).KolmogorovTest(ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_Train_B'))


print '@DEBUG: Test Integral'
print ROOT.gDirectory.Get(factoryname+'_'+MVAname+'_S').Integral()
print '@LOG: ROC integral (default)'
print rocIntegral_default
print '@LOG: ROC integral using signal and background'
print roc_integral_test
print '@LOG: ROC integral using train signal and background'
print roc_integral_train
print '@LOG: ROC integral ratio (Test/Train)'
print roc_integral_test/roc_integral_train
print '@LOG: Significance'
print significance
print '@LOG: Separation for test sample'
print separation_test
print '@LOG: Separation for test train'
print separation_train
print '@LOG: Kolmogorov test on signal'
print ks_signal
print '@LOG: Kolmogorov test on background'
print ks_bkg

#!! update the database
import sqlite3 as lite
con = lite.connect(MVAdir+'Trainings.db',timeout=10000) #timeout in milliseconds. default 5 sec
with con: # here DB is locked
    cur = con.cursor()
    cur.execute("create table if not exists trainings (Roc_integral real, Separation real, Significance real, Ks_signal real, Ks_background real, Roc_integral_train real, Separation_train real, MVASettings text)");
    cur.execute("insert into trainings values(?,?,?,?,?,?,?,?)",(roc_integral_test,separation_test,significance,ks_signal,ks_bkg,roc_integral_train,separation_train,MVAsettings));
#!! here is unlocked

#!! Close the output file to avoid memory leak
output.Close()


#WRITE INFOFILE
infofile = open(MVAdir+factoryname+'_'+MVAname+'.info','w')
print '@DEBUG: output infofile name'
print infofile

info=mvainfo(MVAname)
info.factoryname=factoryname
info.factorysettings=factorysettings
info.MVAtype=MVAtype
info.MVAsettings=MVAsettings
info.weightfilepath=MVAdir
info.path=path
info.varset=treeVarSet
info.vars=MVA_Vars['Nominal']
pickle.dump(info,infofile)
infofile.close()

# open the TMVA Gui 
if gui == True: 
    ROOT.gROOT.ProcessLine( ".L myutils/TMVAGui.C")
    ROOT.gROOT.ProcessLine( "TMVAGui(\"%s\")" % fnameOutput )
    ROOT.gApplication.Run() 


