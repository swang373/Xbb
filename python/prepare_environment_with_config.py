#! /usr/bin/env python
import os, pickle, sys, ROOT
ROOT.gROOT.SetBatch(True)
from optparse import OptionParser
from myutils import BetterConfigParser, copytree, ParseInfo

print 'start prepare_environment_with_config.py'

argv = sys.argv

#get files info from config
parser = OptionParser()
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                      help="directory config")
parser.add_option("-S", "--samples", dest="names", default="",
                              help="samples you want to run on")

(opts, args) = parser.parse_args(argv)

config = BetterConfigParser()
config.read(opts.config)

namelist=opts.names.split(',')
print "namelist:",namelist

pathIN = config.get('Directories','PREPin')
pathOUT = config.get('Directories','PREPout')
samplesinfo=config.get('Directories','samplesinfo')
sampleconf = BetterConfigParser()
sampleconf.read(samplesinfo)

prefix=sampleconf.get('General','prefix')

info = ParseInfo(samplesinfo,pathIN)
print "samplesinfo:",samplesinfo
print "info:",info
for job in info:
    print "job.name:",job.name
    if not job.name in namelist: 
        continue
    if job.subsample:
        continue
    copytree(pathIN,pathOUT,prefix,job.prefix,job.identifier,'',job.addtreecut)
print 'end prepare_environment_with_config.py'
