from ROOT import *
from math import *
import collections

fileName = "../env/MVAout_v0.0.0/ZvvHighPt_V21_ZH_HToBB_ZToNuNu_M125_13TeV_amcatnloFXFX_madspin_pythia8.root"

gStyle.SetOptStat("0000")


def getIntegral(tree, cut="1", weight="1"):
    assert(type(tree) is TTree or type(tree) is TChain)
    tree.Draw("0 >> a(1,0,1)","("+cut+")*"+weight,"goff")
    a = gDirectory.Get("a")
    return a.GetBinContent(1)



#        range(10, 110+1),    # 0-110 (NNPDF30_lo_as_0130)  
#        range(2001, 2100+1), # 2001-2100 (NNPDF30_nlo_nf_5_pdfas)
#        range(2101, 2102+1)  # 2101-2102 (alpha_s variationns) 

LO = range(1, 100+1)
#NLO = range(2001, 2100+1)
#alpha_s = range(2101, 2102+1)


f = TFile(fileName)
tree = f.Get("tree")
CountWeightedLHEWeightPdf = f.Get("CountWeightedLHEWeightPdf")
CountWeighted = f.Get("CountWeighted")

histoLO = TH1F("histoLO","",20,0.9,1.1)
norm = getIntegral(tree,"1","sign(genWeight)")/CountWeighted.GetBinContent(1)
print "norm=",norm
for i in LO:
    val = getIntegral(tree,"1","sign(genWeight)*LHE_weights_pdf_wgt[%s]"%i)/CountWeightedLHEWeightPdf.GetBinContent(i)
    histoLO.Fill(val/norm)
    print i,val

c1 = TCanvas("c1","")

c1.SetGridy()
#c1.SetLogy()

histoLO.GetYaxis().SetTitle("# pdf syst")

#histoLO.SetMaximum(1.05)
#histoLO.SetMinimum(0.001)

histoLO.SetLineColor(kBlue)

histoLO.Draw("ERR")
#histoBkg.Draw("ERR,same")

#leg = TLegend(0.6,0.8,0.9,0.9)
#leg.AddEntry(histoSig,"signal","lep");
#leg.AddEntry(histoBkg,"background","lep");
#leg.Draw("same")

c1.SaveAs("PDF_efficiency.C")
c1.SaveAs("PDF_efficiency.png")
c1.SaveAs("PDF_efficiency.pdf")


#addCut(cuts,    "dPhiHMET",   "abs(TVector2::Phi_mpi_pi(HCSV_reg_phi-met_phi))>0.785")
#addCut(cuts,    "dPhi2JetMET",   "Sum$(Jet_puId>=1 && abs(TVector2::Phi_mpi_pi(Jet_phi-met_phi) )<0.4 && Iteration$<=2)==0 ")
#addCut(cuts,    "ECALcell",   "!(OverAll(Jet_phi[0],Jet_eta[0]) && (abs(TVector2::Phi_mpi_pi ( Jet_phi[0]-met_phi ))>3.1415-0.4)) && Sum$(UnderAll(Jet_phi,Jet_eta) && (Jet_pt>30) && (abs(TVector2::Phi_mpi_pi ( Jet_phi-met_phi ))<0.4))==0")
#addCut(cuts,    "dPhiUnderJetMET",   "Sum$(UnderAll(Jet_phi,Jet_eta) && (Jet_pt>30) && (abs(TVector2::Phi_mpi_pi ( Jet_phi-met_phi ))<0.4))==0")
#addCut(cuts,    "dPhiHJetMET",   "Sum$(Jet_puId[hJCidx]>=1 && abs(TVector2::Phi_mpi_pi(Jet_phi[hJCidx]-met_phi))<0.4 )==0")
#addCut(cuts,    "dPhiJetMETTight",   "Sum$((Jet_pt>30) && (abs(TVector2::Phi_mpi_pi ( Jet_phi-met_phi ))<0.4))==0")

