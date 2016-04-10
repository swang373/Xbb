#! /usr/bin/env python
import ROOT,sys,os,subprocess,random,string,hashlib
ROOT.gROOT.SetBatch(True)
from printcolor import printc
import pickle
from optparse import OptionParser
from BetterConfigParser import BetterConfigParser
from sample_parser import ParseInfo

print 'start mergetreePSI.py'

argv = sys.argv

#get files info from config
parser = OptionParser()
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                      help="directory config")
parser.add_option("-S", "--samples", dest="names", default="",
                              help="samples you want to run on")
parser.add_option("-f", "--filelist", dest="filelist", default="",
                              help="list of files you want to run on")
parser.add_option("-s", "--mergesys", dest="mergesys", default="False",
                              help="merge sys step, otherwise")

(opts, args) = parser.parse_args(argv)

config = BetterConfigParser()
config.read(opts.config)

namelist=opts.names.split(',')
filelist=opts.filelist.split(';')
print "namelist:",namelist
# print "opts.filelist:",opts.filelist
print "len(filelist)",len(filelist),"filelist[0]:",filelist[0]

if opts.mergesys == 'True':
    pathIN = config.get('Directories','SYSin')
    pathOUT = config.get('Directories','SYSout')
else:
    pathIN = config.get('Directories','PREPin')
    pathOUT = config.get('Directories','PREPout')
samplesinfo=config.get('Directories','samplesinfo')
sampleconf = BetterConfigParser()
sampleconf.read(samplesinfo)

whereToLaunch = config.get('Configuration','whereToLaunch') # USEFUL IN CASE OF SITE BY SITE OPTIONS
prefix=sampleconf.get('General','prefix')
info = ParseInfo(samplesinfo,pathIN)
print "samplesinfo:",samplesinfo


def mergetreePSI(pathIN,pathOUT,prefix,newprefix,folderName,Aprefix,Acut,config):
    '''
    List of variables
    pathIN: path of the input file containing the data
    pathOUT: path of the output files
    prefix: "prefix" variable from "samples_nosplit.cfg"
    newprefix: "newprefix" variable from "samples_nosplit.cfg"
    file: sample header (as DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball)
    Aprefix: empty string ''
    Acut: the sample cut as defined in "samples_nosplit.cfg"
    '''
    print 'start mergetreePSI.py'
    print (pathIN,pathOUT,prefix,newprefix,folderName,Aprefix,Acut)
    print "##### MERGE TREE - BEGIN ######"

    merged = pathOUT+'/'+newprefix+folderName+".root "

    t = ROOT.TFileMerger(ROOT.kFALSE)
    __tmpPath = os.environ["TMPDIR"]
    tmp_filename = __tmpPath+'/'+newprefix+folderName+".root "
    print 't.OutputFile('+tmp_filename+',"RECREATE")'
    t.OutputFile(tmp_filename, "RECREATE")
    outputFolder = "%s/%s/" %(pathOUT,folderName)
    print 'outputFolder is', outputFolder
    for file in os.listdir(outputFolder.replace('root://t3dcachedb03.psi.ch:1094','').replace('gsidcap://t3se01.psi.ch:22128/','').replace('dcap://t3se01.psi.ch:22125/','')):
        if file.startswith('tree'):
            print 't.AddFile('+outputFolder+file+')'
            t.AddFile(outputFolder+file)
    t.Merge()

    # DUMMY WAYS TO COPE WITH FILE COMMAND PROTOCOLS @T2-PSI...
    del_merged = merged.replace('gsidcap://t3se01.psi.ch:22128/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=').replace('dcap://t3se01.psi.ch:22125/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=').replace('root://t3dcachedb03.psi.ch:1094/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')
    command = 'srmrm %s' %(del_merged)
    print command
    subprocess.call([command], shell = True)
    srmpathOUT = pathOUT.replace('gsidcap://t3se01.psi.ch:22128/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=').replace('dcap://t3se01.psi.ch:22125/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=').replace('root://t3dcachedb03.psi.ch:1094/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')
    command = 'srmcp -2 -globus_tcp_port_range 20000,25000 file:///'+__tmpPath+'/'+newprefix+folderName+".root"+' '+srmpathOUT+'/'+newprefix+folderName+".root"
    print command
    subprocess.call([command], shell=True)

    print 'checking output file',pathOUT+'/'+newprefix+folderName+".root"
    f = ROOT.TFile.Open(pathOUT+'/'+newprefix+folderName+".root",'read')
    if not f or f.GetNkeys() == 0 or f.TestBit(ROOT.TFile.kRecovered) or f.IsZombie():
        print 'TERREMOTO AND TRAGEDIA: THE MERGED FILE IS CORRUPTED!!! ERROR: exiting'
        sys.exit(1)

    command = 'rm '+__tmpPath+'/'+newprefix+folderName+'.root'
    print command
    subprocess.call([command], shell=True)

    print "##### MERGE TREE - END ######"


print "info:",info
for job in info:
    if not job.name in namelist and not job.identifier in namelist:
        continue
    if job.subsample:
        continue
    samplefiles = config.get('Directories','samplefiles')
    mergetreePSI(samplefiles,pathOUT,prefix,job.prefix,job.identifier,'',job.addtreecut, config)

print 'end mergetreePSI.py'


