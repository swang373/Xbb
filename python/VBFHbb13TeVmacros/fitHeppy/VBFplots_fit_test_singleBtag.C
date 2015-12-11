#include"fittedFunctions.h"
//#include"fittedFunctions.h.GoodOld"

void VBFplots_fit_test_singleBtag(){
    gStyle->SetOptStat(0);
//    gROOT->SetBatch();

    TCanvas* c1 = new TCanvas("c1","c1");
    c1->SetGridx();
    c1->SetGridy();

//    TFile *_file0 = TFile::Open("SingleElectronVBF.root");
    TFile *_file0 = TFile::Open("JetHTVBF.root");
    TTree* tree = (TTree*) _file0->Get("tree");

    //////////////////////////////////////////////////
    // plots for the single b-tag trigger, starting from (HLT_BIT_HLT_DiPFJetAve60_v && Alt$(Jet_pt[3],0)>30)
    //////////////////////////////////////////////////

    tree->Draw("Mqq_1b  >> h(25,0,2000)"," SingleBtagVBFTriggerWeight(Jet_pt[0], Jet_pt[1], Jet_pt[2], Jet_pt[3], min(CSV[0],1-1.e-7), Detaqq_eta,Mqq_eta, Dphibb_1b, Detaqq_1b)*(HLT_BIT_HLT_DiPFJetAve60_v && Alt$(Jet_pt[3],0)>30)","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);h->SetMaximum(2.0*h->GetMaximum());
    tree->Draw("Mqq_1b"," 1.0001*(HLT_BIT_HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v && (HLT_BIT_HLT_DiPFJetAve60_v && Alt$(Jet_pt[3],0)>30))","same");

    c1->SaveAs("check_full_Mqq_single.png");
    c1->SaveAs("check_full_Mqq_single.C");

    tree->Draw("Mbb_1b  >> h(50,0,500)"," SingleBtagVBFTriggerWeight(Jet_pt[0], Jet_pt[1], Jet_pt[2], Jet_pt[3], min(CSV[0],1-1.e-7), Detaqq_eta,Mqq_eta, Dphibb_1b, Detaqq_1b)*(HLT_BIT_HLT_DiPFJetAve60_v && Alt$(Jet_pt[3],0)>30)","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);h->SetMaximum(2.0*h->GetMaximum());
    tree->Draw("Mbb_1b"," 1.0001*(HLT_BIT_HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v && (HLT_BIT_HLT_DiPFJetAve60_v && Alt$(Jet_pt[3],0)>30))","same");

    c1->SaveAs("check_full_Mbb_1b.png");
    c1->SaveAs("check_full_Mbb_1b.C");

    tree->Draw("Detaqq_1b  >> h(50,0,10)"," SingleBtagVBFTriggerWeight(Jet_pt[0], Jet_pt[1], Jet_pt[2], Jet_pt[3], min(CSV[0],1-1.e-7), Detaqq_eta,Mqq_eta, Dphibb_1b, Detaqq_1b)*(HLT_BIT_HLT_DiPFJetAve60_v && Alt$(Jet_pt[3],0)>30)","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);h->SetMaximum(2.0*h->GetMaximum());
    tree->Draw("Detaqq_1b"," 1.0001*(HLT_BIT_HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v && (HLT_BIT_HLT_DiPFJetAve60_v && Alt$(Jet_pt[3],0)>30))","same");

    c1->SaveAs("check_full_Detaqq_1b.png");
    c1->SaveAs("check_full_Detaqq_1b.C");

    tree->Draw("Dphibb_1b  >> h(32,0,3.2)"," SingleBtagVBFTriggerWeight(Jet_pt[0], Jet_pt[1], Jet_pt[2], Jet_pt[3], min(CSV[0],1-1.e-7), Detaqq_eta,Mqq_eta, Dphibb_1b, Detaqq_1b)*(HLT_BIT_HLT_DiPFJetAve60_v && Alt$(Jet_pt[3],0)>30)","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);h->SetMaximum(2.0*h->GetMaximum());
    tree->Draw("Dphibb_1b"," 1.0001*(HLT_BIT_HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v && (HLT_BIT_HLT_DiPFJetAve60_v && Alt$(Jet_pt[3],0)>30))","same");

    c1->SaveAs("check_full_Dphibb_1b.png");
    c1->SaveAs("check_full_Dphibb_1b.C");

    tree->Draw("Max$(Jet_btagCSV)  >> h(40,0,1)"," SingleBtagVBFTriggerWeight(Jet_pt[0], Jet_pt[1], Jet_pt[2], Jet_pt[3], min(CSV[0],1-1.e-7), Detaqq_eta,Mqq_eta, Dphibb_1b, Detaqq_1b)*(HLT_BIT_HLT_DiPFJetAve60_v && Alt$(Jet_pt[3],0)>30)","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);h->SetMaximum(2.0*h->GetMaximum());
    tree->Draw("Max$(Jet_btagCSV)"," 1.0001*(HLT_BIT_HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v && (HLT_BIT_HLT_DiPFJetAve60_v && Alt$(Jet_pt[3],0)>30))","same");
    c1->SaveAs("check_full_CSV1_single.png");
    c1->SaveAs("check_full_CSV1_single.C");

    tree->Draw("MaxIf$(Jet_btagCSV,Jet_btagCSV!=Max$(Jet_btagCSV))  >> h(40,0,1)"," SingleBtagVBFTriggerWeight(Jet_pt[0], Jet_pt[1], Jet_pt[2], Jet_pt[3], min(CSV[0],1-1.e-7), Detaqq_eta,Mqq_eta, Dphibb_1b, Detaqq_1b)*(HLT_BIT_HLT_DiPFJetAve60_v && Alt$(Jet_pt[3],0)>30)","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);h->SetMaximum(2.0*h->GetMaximum());
    tree->Draw("MaxIf$(Jet_btagCSV,Jet_btagCSV!=Max$(Jet_btagCSV))"," 1.0001*(HLT_BIT_HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v && (HLT_BIT_HLT_DiPFJetAve60_v && Alt$(Jet_pt[3],0)>30))","same");
    c1->SaveAs("check_full_CSV2_single.png");
    c1->SaveAs("check_full_CSV2_single.C");

}

//SingleBtagVBFTriggerWeight(pt1,pt2,pt3,pt4,CSV1,DeltaEtaqq_eta, Mqq_eta, DeltaPhibb_single, DeltaEtaqq_single)

//(HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1)
//HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v3
//HLT_BIT_HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v
//HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v3

