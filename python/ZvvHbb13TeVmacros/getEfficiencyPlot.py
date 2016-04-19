from ROOT import *
from math import *
import collections
prefix = "/scratch/sdonato/VHbbRun2/V21_2/CMSSW_7_1_5/src/Xbb/env/ZvvHighPt_V21_"

gStyle.SetOptStat("0000")
import os
if os.path.exists("../interface/DrawFunctions.C"):
    print 'gROOT.LoadMacro("../interface/DrawFunctions.C")'
    gROOT.LoadMacro("../interface/DrawFunctions.C")
    print "."


def getIntegral(tree, cut="1", weight="1"):
    assert(type(tree) is TTree or type(tree) is TChain)
    tree.Draw("0 >> a(1,0,1)","("+cut+")*"+weight,"goff")
    a = gDirectory.Get("a")
    return a.GetBinContent(1)

def addCut(cuts,name,cut):
    lastcut = cuts[cuts.keys()[len(cuts)-1]]
    cuts[name] = lastcut + "&&" + "("+cut+")"
    return

cuts = collections.OrderedDict()
cuts["incl."]   = "HLT_BIT_HLT_PFMET90_PFMHT90_IDTight_v && Vtype==4 && json"

addCut(cuts,    "MET flags",   "Flag_HBHENoiseIsoFilter && Flag_HBHENoiseFilter && Flag_CSCTightHalo2015Filter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_goodVertices && Flag_eeBadScFilter")
addCut(cuts,    "#Higgs jets#geq2",  "nhJCidx>=2")
addCut(cuts,    "CSV_{min}>CSVL",   "Jet_btagCSV[hJCidx[1]]>0.460")
addCut(cuts,    "CSV_{max}>CSVM",   "Jet_btagCSV[hJCidx[0]]>0.800")
addCut(cuts,    "50<m(jj)<500",   "HCSV_reg_mass<500 && HCSV_reg_mass>50")
addCut(cuts,    "MHT>120",   "mhtJet30>120")
addCut(cuts,    "MET>120",   "met_pt>120")
addCut(cuts,    "H p_{T}>120",   "H_reg_pt>120")
addCut(cuts,    "H jets quality",   "abs(Jet_eta[hJCidx[0]])<2.4 && abs(Jet_eta[hJCidx[1]])<2.4 && abs(Jet_eta[0])<2.4 && Jet_pt_reg[hJCidx[0]]>20 && Jet_pt_reg[hJCidx[1]]>20 && Jet_pt_reg[0]>20  && Jet_id[hJCidx[1]]>=4 && Jet_id[hJCidx[0]]>=4 && Jet_id[0]>=4 && Jet_puId[hJCidx[1]]>=1 && Jet_puId[hJCidx[0]]>=1 && Jet_puId[0]>=1")
addCut(cuts,    "#Delta#phi(H,MET)>#pi/2",   "abs(TVector2::Phi_mpi_pi(HCSV_reg_phi-met_phi))>1.58")
addCut(cuts,    "anti-QCD loose",   "Sum$(Jet_puId>=1 && abs(TVector2::Phi_mpi_pi(Jet_phi-met_phi) )<0.4 && Iteration$<=2)==0 && \
    Sum$(Jet_puId[hJCidx]>=1 && abs(TVector2::Phi_mpi_pi(Jet_phi[hJCidx]-met_phi))<0.4 )==0 &&\
    !(OverAll(Jet_phi[0],Jet_eta[0]) && (abs(TVector2::Phi_mpi_pi ( Jet_phi[0]-met_phi ))>3.1415-0.4)) &&\
    Sum$(UnderAll(Jet_phi,Jet_eta) && (Jet_pt>30) && (abs(TVector2::Phi_mpi_pi ( Jet_phi-met_phi ))<0.4))==0 ")
addCut(cuts,    "90<m(jj)<150",   "HCSV_reg_mass<150 && HCSV_reg_mass>90")

#sigFile     = "/scratch/sdonato/VHbbRun2/V21_2/CMSSW_7_1_5/src/Xbb/env/ZvvHighPt_V21_ZH_HToBB_ZToNuNu_M125_13TeV_amcatnloFXFX_madspin_pythia8.root"
#bkgFile     = "/scratch/sdonato/VHbbRun2/V21_2/CMSSW_7_1_5/src/Xbb/env/ZvvHighPt_V21_MET.root"

sigFile     = "MCAndDataLinks/ZH_HToBB_ZToNuNu_M125_13TeV_amcatnloFXFX_madspin_pythia8/VHBB_HEPPY_V21_ZH_HToBB_ZToNuNu_M125_13TeV_amcatnloFXFX_madspin_Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160316_150722/0000/tree_1.root"
bkgFile     = "MCAndDataLinks/MET/VHBB_HEPPY_V21_MET__Run2015D-16Dec2015-v1/160317_131113/0000/tree_?.root"

#sigFile = TFile(sigFile)
#sigTree = sigFile.Get("tree")

sigTree = TChain("tree")
sigTree.Add(sigFile)

bkgTree = TChain("tree")
bkgTree.Add(bkgFile)

weight = "sign(genWeight) * ((1-((0.5-(0.5*TMath::Erf((min(met_pt,mhtJet30)+1.01 )/60.2)))*13.9))-0.00245) * puWeight * bTagWeight"


firstCut = cuts[cuts.keys()[0]]
normBkg = getIntegral(bkgTree,firstCut)
normSig = getIntegral(sigTree,firstCut,weight)

histoSig = TH1F("histoSig","Efficiency",len(cuts),0.,1.*len(cuts))
histoBkg = TH1F("histoBkg","Efficiency",len(cuts),0.,1.*len(cuts))

for i,cut in enumerate(cuts.keys()):
    effBkg = getIntegral(bkgTree,cuts[cut]) / normBkg
    effSig = getIntegral(sigTree,cuts[cut],weight) / normSig

    histoSig.SetBinContent(i+1,effSig)
    histoSig.SetBinError(i+1,sqrt(effSig*(1-effSig)/normSig))
    histoSig.GetXaxis().SetBinLabel(i+1,cut)

    histoBkg.SetBinContent(i+1,effBkg)
    histoBkg.SetBinError(i+1,sqrt(effBkg*(1-effBkg)/normBkg))
    histoBkg.GetXaxis().SetBinLabel(i+1,cut)

    print cut
    print cuts[cut]

c1 = TCanvas("c1","")

c1.SetGridy()
c1.SetLogy()

histoSig.GetYaxis().SetTitle("Efficiency")

histoSig.SetMaximum(1.05)
histoSig.SetMinimum(0.001)

histoSig.SetLineColor(kRed)
histoBkg.SetLineColor(kBlue)

histoSig.Draw("ERR")
histoBkg.Draw("ERR,same")

leg = TLegend(0.6,0.8,0.9,0.9)
leg.AddEntry(histoSig,"signal","lep");
leg.AddEntry(histoBkg,"background","lep");
leg.Draw("same")

c1.SaveAs("cut_efficiency.C")
c1.SaveAs("cut_efficiency.png")
c1.SaveAs("cut_efficiency.pdf")


#addCut(cuts,    "dPhiHMET",   "abs(TVector2::Phi_mpi_pi(HCSV_reg_phi-met_phi))>0.785")
#addCut(cuts,    "dPhi2JetMET",   "Sum$(Jet_puId>=1 && abs(TVector2::Phi_mpi_pi(Jet_phi-met_phi) )<0.4 && Iteration$<=2)==0 ")
#addCut(cuts,    "ECALcell",   "!(OverAll(Jet_phi[0],Jet_eta[0]) && (abs(TVector2::Phi_mpi_pi ( Jet_phi[0]-met_phi ))>3.1415-0.4)) && Sum$(UnderAll(Jet_phi,Jet_eta) && (Jet_pt>30) && (abs(TVector2::Phi_mpi_pi ( Jet_phi-met_phi ))<0.4))==0")
#addCut(cuts,    "dPhiUnderJetMET",   "Sum$(UnderAll(Jet_phi,Jet_eta) && (Jet_pt>30) && (abs(TVector2::Phi_mpi_pi ( Jet_phi-met_phi ))<0.4))==0")
#addCut(cuts,    "dPhiHJetMET",   "Sum$(Jet_puId[hJCidx]>=1 && abs(TVector2::Phi_mpi_pi(Jet_phi[hJCidx]-met_phi))<0.4 )==0")
#addCut(cuts,    "dPhiJetMETTight",   "Sum$((Jet_pt>30) && (abs(TVector2::Phi_mpi_pi ( Jet_phi-met_phi ))<0.4))==0")

