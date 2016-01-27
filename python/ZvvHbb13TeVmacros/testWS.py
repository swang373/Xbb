import ROOT
file = ROOT.TFile.Open("vhbb_WS_BDT_M125_ZnnHbbHighPt_myDatacard_13TeV.root")
wspace = file.Get("Znn_13TeV")
#objects = wspace.allData()
objects = wspace.allGenericObjects()
for a in objects:
    print a.GetName(),"***",a.GetTitle()

