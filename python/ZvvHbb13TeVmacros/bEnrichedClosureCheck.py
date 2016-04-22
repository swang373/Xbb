from ROOT import *

xsect_WjetHT100 = 1345 *1.23
xsect_WjetHT200 = 359.7 *1.23
xsect_WjetHT400 = 48.91 *1.23
xsect_WjetHT600 = 18.77 *1.23
xsect_Wbjet = 34.2 *1.23
xsect_Wjetbgen = 2.018e+02 *1.23



f_Wjetbgen = TFile("/scratch/sdonato/VHbbRun2/V21_2/CMSSW_7_1_5/src/Xbb/env/ZvvHighPt_V21_WJetsToLNu_BGenFilter_Wpt-40toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root")
tree = f_Wjetbgen.Get("tree")

CountFullWeighted = f_Wjetbgen.Get("CountFullWeighted")
count = CountFullWeighted.GetBinContent(1)

print "count:",count
tree.Draw("lheHT >> Wjetbgen"," ( (lheNb==0 && nGenStatus2bHad>0 && lheV_pt>40 ) && (lheHT>600 && lheHT<1000) && Vtype!=4 )*sign(genWeight)*genWeight * %d / %d"%(xsect_Wjetbgen,count),"ERR")
Wjetbgen = Wjetbgen.Clone("Wjetbgen")

f_Wbjet = TFile("/scratch/sdonato/VHbbRun2/V21_2/CMSSW_7_1_5/src/Xbb/env/ZvvHighPt_V21_WBJetsToLNu_Wpt-40toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root")
tree = f_Wbjet.Get("tree")

CountWeighted = f_Wbjet.Get("CountWeighted")
count = CountWeighted.GetBinContent(1)
print "count:",count
tree.Draw("lheHT >> Wbjet"," ( (lheNb>0  && lheV_pt>40) && (lheHT>600 && lheHT<1000) && Vtype!=4 )*sign(genWeight) * %d / %d"%(xsect_Wbjet,count),"ERR")
Wbjet = Wbjet.Clone("Wbjet")


f_Wjet = TFile("/scratch/sdonato/VHbbRun2/V21/CMSSW_7_1_5/src/Xbb/env/ZvvHighPt_V21_WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root")
tree = f_Wjet.Get("tree")

CountWeighted = f_Wjet.Get("CountWeighted")
count = CountWeighted.GetBinContent(1)
print "count:",count
tree.Draw("lheHT >> Wbjet_check"," ( (lheNb>0  && lheV_pt>40) && (lheHT>600 && lheHT<1000) && Vtype!=4 )*sign(genWeight) * %d / %d"%(xsect_WjetHT600,count),"ERR")
Wbjet_check = Wbjet_check.Clone("Wbjet_check")

tree.Draw("lheHT >> Wjetbgen_check"," ( (lheNb==0 && nGenStatus2bHad>0 && lheV_pt>40 ) && (lheHT>600 && lheHT<1000) && Vtype!=4 )*sign(genWeight) * %d / %d"%(xsect_WjetHT600,count),"ERR")
Wjetbgen_check = Wjetbgen_check.Clone("Wjetbgen_check")

Wbjet_check.SetLineColor(kRed)
Wjetbgen_check.SetLineColor(kRed)

Wbjet.Draw("")
Wbjet_check.Draw("same")
c1.SaveAs("Wbjet.png")

Wjetbgen.Draw("")
Wjetbgen_check.Draw("same")
c1.SaveAs("Wjetbgen.png")



