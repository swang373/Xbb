from ROOT import *


xsect_ZjetHT100 = 280.35 *1.23
xsect_ZjetHT200 = 77.67 *1.23
xsect_ZjetHT400 = 10.73 *1.23
xsect_ZjetHT600 = 4.116 *1.23
xsect_Zbjet = 48.6 *1.23


f_Zbjet = TFile("/scratch/sdonato/VHbbRun2/V21_2/CMSSW_7_1_5/src/Xbb/env/ZvvHighPt_V21_DYBJetsToNuNu_Zpt-40toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root")
tree = f_Zbjet.Get("tree")
CountWeighted = f_Zbjet.Get("CountWeighted")
count = CountWeighted.GetBinContent(1)
print "count:",count

tree.Draw("lheHT >> Zbjet(100)"," ( (lheNb>0  ) && lheHT>600 && lheHT<1000 )*sign(genWeight) * %d/ %d"%(xsect_Zbjet,count),"ERR")
Zbjet = Zbjet.Clone("Zbjet")

f_Zjet = TFile("/scratch/sdonato/VHbbRun2/V21/CMSSW_7_1_5/src/Xbb/env/ZvvHighPt_V21_ZJetsToNuNu_HT-600ToInf_13TeV-madgraph.root")
tree = f_Zjet.Get("tree")
CountWeighted = f_Zjet.Get("CountWeighted")
count = CountWeighted.GetBinContent(1)
print "count:",count

tree.Draw("lheHT >> Zbjet_check(100)"," ( (lheNb>0  ) && lheHT>600  && lheHT<1000  )*sign(genWeight) * %d/ %d"%(xsect_ZjetHT600,count),"ERR")
Zbjet_check = Zbjet_check.Clone("Zbjet_check")

Zbjet_check.SetLineColor(kRed)


Zbjet.Draw("")
Zbjet_check.Draw("same")

c1.SaveAs("Zbjet.png")

