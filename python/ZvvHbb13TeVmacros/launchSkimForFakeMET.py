import sys
from skimForFakeMET import *
#from doFakeMETStupid import *

try:
  fileNames = sys.argv[1]
  outName   = sys.argv[2]
  print
  print "Launching doFakeMET with:"
  print "fileNames:",   fileNames
  print "outName:",     outName
  print
except:
  print
  print "example:"
  print "python launchFakeMET.py tree_100_*.root newFile.root"
  print sys.argv
  print

print "fileNames: ",fileNames

from os import walk
dirpath_    = ""
dirnames_    = []
files_   = ""
#    filenames = []
inputFiles  = []
folder_prefix = ''

exit = False
for (dirpath_, dirnames_, files_) in walk(fileNames):
    for filename_ in files_:
        print file
        if 'root' in filename_ and 'tree' in filename_ and not 'failed' in dirpath_:
            exit = True
        if exit: break
    if exit: break

print dirpath_
path = dirpath_+'/'+ files_[0]
path = path.split("tree_")[0]
path = path + "tree_*.root"

inputs = []
for file_ in files_:
    inputs.append((dirpath_+'/'+ file_,outName+'/'+file_))

print "First input:",   inputs[0][0]
print "First output:",  inputs[0][1]

quick = False
function = None
expoRatio = None
if quick:
    firstFile = inputs[0][1]
    gROOT.ProcessLine(".x "+firstFile.replace(".root","_fit.C"))
    function = gDirectory.Get("histo")
    function = copy.copy(function)
    gROOT.ProcessLine(".x "+firstFile.replace(".root","_fit4.C"))
    expoRatio = f4.Get("c1").GetPrimitive("expoRatio")
    expoRatio = copy.copy(expoRatio)
for (inpt,outpt) in inputs:
    doFile(inpt,outpt,function,expoRatio)
#    print inpt,outpt

