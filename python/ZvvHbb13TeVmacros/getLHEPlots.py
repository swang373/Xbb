from ROOT import *
from math import *
import collections

fileName = "../env/MVAout_v0.0.0/ZvvHighPt_V21_ZH_HToBB_ZToNuNu_M125_13TeV_amcatnloFXFX_madspin_pythia8.root"
#fileName = "../env/MVAout_v0.0.0/ZvvHighPt_V21_ZJetsToNuNu_HT-400To600_13TeV-madgraph.root"


gStyle.SetOptStat("0000")


def getIntegral(tree, cut="1", weight="1"):
    assert(type(tree) is TTree or type(tree) is TChain)
    tree.Draw("0 >> a(1,0,1)","("+cut+")*"+weight,"goff")
    a = gDirectory.Get("a")
    return a.GetBinContent(1)

LO = range(0, 6)
#NLO = range(2001, 2100+1)
#alpha_s = range(2101, 2102+1)


f = TFile(fileName)
tree = f.Get("tree")
CountWeightedLHEWeightScale = f.Get("CountWeightedLHEWeightScale")
CountWeighted = f.Get("CountWeighted")

histos = []
norm = 1.*CountWeighted.GetBinContent(1)
print "norm=",norm
for i in LO:
    count = 1.*CountWeightedLHEWeightScale.GetBinContent(CountWeightedLHEWeightScale.FindBin(i))
    tree.Draw("ZvvBDT >> histo%s (40,-1,1)"%i,"sign(genWeight)*LHE_weights_scale_wgt[%s]*1./%s"%(i,count),"goff")
    histos.append(gDirectory.Get("histo%s"%i))

count = 1.*CountWeighted.GetBinContent(1)
tree.Draw("ZvvBDT >> histo (40,-1,1)","sign(genWeight)*1./%s"%(count),"goff")
histo = gDirectory.Get("histo")
c1 = TCanvas("c1","")

c1.SetGridy()
#c1.SetLogy()

histo.GetYaxis().SetTitle("# LHE syst")

max_ = histo.GetMaximum()
#histo.SetMaximum(1.1*histo.GetMaximum())
#histos.SetMaximum(1.05)
#histos.SetMinimum(0.001)

#histos.SetLineColor(kBlue)

histo.SetLineWidth(2)
histo.SetLineColor(kYellow+1)


minInt = 1E9
minHist = 0
maxInt = -1E9
maxHist = 0

for h in histos:
    integ = h.Integral()
    if histos.index(h)==4:
        minInt = integ
        minHist = h
    if histos.index(h)==5:
        maxInt = integ
        maxHist = h
    max_ = max(max_, h.GetMaximum())

histo.SetMaximum(1.05*max_)
histo.Draw("")

for h in histos:
    h.Draw("same")


maxHist.SetLineWidth(2)
maxHist.SetLineColor(kRed)

minHist.SetLineWidth(2)
minHist.SetLineColor(kGreen+2)

histo.Draw("same")
minHist.Draw("same")
maxHist.Draw("same")

#histoBkg.Draw("same")

#leg = TLegend(0.6,0.8,0.9,0.9)
#leg.AddEntry(histoSig,"signal","lep");
#leg.AddEntry(histoBkg,"background","lep");
#leg.Draw("same")

c1.SaveAs("LHE_efficiency.C")
c1.SaveAs("LHE_efficiency.png")
c1.SaveAs("LHE_efficiency.pdf")


#addCut(cuts,    "dPhiHMET",   "abs(TVector2::Phi_mpi_pi(HCSV_reg_phi-met_phi))>0.785")
#addCut(cuts,    "dPhi2JetMET",   "Sum$(Jet_puId>=1 && abs(TVector2::Phi_mpi_pi(Jet_phi-met_phi) )<0.4 && Iteration$<=2)==0 ")
#addCut(cuts,    "ECALcell",   "!(OverAll(Jet_phi[0],Jet_eta[0]) && (abs(TVector2::Phi_mpi_pi ( Jet_phi[0]-met_phi ))>3.1415-0.4)) && Sum$(UnderAll(Jet_phi,Jet_eta) && (Jet_pt>30) && (abs(TVector2::Phi_mpi_pi ( Jet_phi-met_phi ))<0.4))==0")
#addCut(cuts,    "dPhiUnderJetMET",   "Sum$(UnderAll(Jet_phi,Jet_eta) && (Jet_pt>30) && (abs(TVector2::Phi_mpi_pi ( Jet_phi-met_phi ))<0.4))==0")
#addCut(cuts,    "dPhiHJetMET",   "Sum$(Jet_puId[hJCidx]>=1 && abs(TVector2::Phi_mpi_pi(Jet_phi[hJCidx]-met_phi))<0.4 )==0")
#addCut(cuts,    "dPhiJetMETTight",   "Sum$((Jet_pt>30) && (abs(TVector2::Phi_mpi_pi ( Jet_phi-met_phi ))<0.4))==0")

