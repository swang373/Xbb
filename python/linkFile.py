def newName (filename):
    temp = (filename.split("-"))[0]
    temp = (temp.split("_"))[0]
    output = temp + filename.split(temp)[2]
    output = output[:-22]+".root"
    return output

from os import listdir, mkdir
from os.path import isfile, join
mypath = '/gpfs/ddn/srm/cms/store/user/arizzi/VHBBHeppyV11/'
output = '/scratch/sdonato/VHbb/ETH/CMSSW_7_4_5_ROOT5/src/Xbb/python/samples'
try:
    mkdir(output)
except:
    pass

onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
print onlyfiles
newNames ={}
for filename in onlyfiles:
    command = "cp -s "+mypath+"/"+filename+" "+output+"/"+newName(filename)
    print command
    os.system(command)

