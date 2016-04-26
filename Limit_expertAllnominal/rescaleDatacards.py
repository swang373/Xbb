import os
from ROOT import *

#WARNING: changed value to 2.29. Was 2.32 presiously
oldLumi = 2.29
#oldLumi = 2.32
newLumi = 5.0
dirName = "5fb"
#channel = "Znn"
channel = "Zll"

if channel == "Zvv":
    oldFileNames = [
        "vhbb_TH_Znn_13TeVTightLowPt_Wbb.root",
        "vhbb_TH_Znn_13TeVTightHighPt_QCD.root",
        "vhbb_TH_Znn_13TeVTightHighPt_Signal.root",
        "vhbb_TH_Znn_13TeVTightHighPt_TTbarTight.root",
        "vhbb_TH_Znn_13TeVTightHighPt_WLight.root",
        "vhbb_TH_Znn_13TeVTightHighPt_Wbb.root",
        "vhbb_TH_Znn_13TeVTightHighPt_ZLight.root",
        "vhbb_TH_Znn_13TeVTightHighPt_Zbb.root",
        "vhbb_TH_Znn_13TeVTightLowPt_QCD.root",
        "vhbb_TH_Znn_13TeVTightLowPt_Signal.root",
        "vhbb_TH_Znn_13TeVTightLowPt_TTbarTight.root",
        "vhbb_TH_Znn_13TeVTightLowPt_WLight.root",
        "vhbb_TH_Znn_13TeVTightLowPt_Wbb.root",
        "vhbb_TH_Znn_13TeVTightLowPt_ZLight.root",
        "vhbb_TH_Znn_13TeVTightLowPt_Zbb.root"
    ]
elif channel == "Zll":
    oldFileNames = [
        "vhbb_TH_First_dc_highpt.root",
        "vhbb_TH_First_dc_lowpt.root",
    ]


def scaleDC(oldFileName, newFileName, scale):
    print "DC - Opening: ",oldFileName+" . Writing:",newFileName
    fOld = open(oldFileName)
    fNew = open(newFileName, 'w')

    for line in fOld.readlines():
        if 'rate' == line[:4] or 'observation' == line[:11]:
            newLine = ""
            for word in line.split(" "):
                try:
                    num = eval(word)
                except:
                    num = 0.0
                if num>0:
                    word = str(num*scale)
                newLine = newLine + word + " "
            line = newLine
        fNew.write(line)

    fOld.close()
    fNew.close()

def scaleHistos(oldFileName, newFileName, scale):
    print "Opening: ",oldFileName+" . Writing:",newFileName
    fileOld = TFile(oldFileName)
    fileOld.ls()
    if channel == "Zvv": Dir = fileOld.Get(channel+"_13TeV")
    elif channel == "Zll": Dir = fileOld.Get("Vpt1")
    assert(type(Dir)==TDirectoryFile)
    fileNew = TFile(newFileName,"recreate")
    if channel == "Zvv": newDir = fileNew.mkdir(channel+"_13TeV")
    elif channel == "Zll": newDir = fileNew.mkdir("Vpt1")
    newDir.cd()
    for i in Dir.GetListOfKeys():
        obj = i.ReadObj()
        obj = obj.Clone(obj.GetName())
        obj.Scale(scale)
        if obj.GetName()=="TTCMS_vhbb_bTagHFWeightHFStats1Up":
            print obj.GetName(), obj.GetMaximum() 
        obj.Write()
    fileNew.Close()
    return

scale = newLumi/oldLumi

oldFileName = oldFileNames[0]
try:
    os.mkdir(oldFileName.split("vhbb_")[0]+dirName)
except:
    pass

for oldFileName in oldFileNames:
    newFileName = oldFileName.replace("vhbb_",dirName+"/vhbb_")
    oldFileNameDC = (oldFileName.replace("vhbb_TH","vhbb_DC_TH")).replace(".root",".txt")
    newFileNameDC = (newFileName.replace("vhbb_TH","vhbb_DC_TH")).replace(".root",".txt")
    
    scaleHistos(oldFileName, newFileName, scale)
    scaleDC(oldFileNameDC, newFileNameDC, scale)

