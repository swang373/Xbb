#include"fittedFunctions.h"

void VBFplots_fit_test_test(){
    gStyle->SetOptStat(0);
//    gROOT->SetBatch();

    TCanvas* c1 = new TCanvas("c1","c1");
    c1->SetGridx();
    c1->SetGridy();

    TFile *_file0 = TFile::Open("newTreeSilvio2.root");
    TTree* tree = (TTree*) _file0->Get("tree");

//    //////////////////////////////////////////////////
//    // plots for the double b-tag trigger, starting from (HLT_Ele23_WPLoose_Gsf_v2)
//    //////////////////////////////////////////////////

//    tree->Draw("2"," DoubleBtagVBFTriggerWeight(30, 30, 30, 30, 0.9, 0.9, 3000,30, 30, 3000)*(1)","");
    tree->Draw("bMqq_eta  >> h(25,0,2000)"," test(offJet_pt[0], offJet_pt[1], offJet_pt[2], Max$(min(offJet_csv,1)), MaxIf$(min(offJet_csv,1),min(offJet_csv,1)!=Max$(min(offJet_csv,1))), bMqq_eta,bDetaqq_eta, bDetaqq_double, Mqq_double)*((HLT_Ele23_WPLoose_Gsf_v2))","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);h->SetMaximum(2.0*h->GetMaximum());
    tree->Draw("bMqq_eta"," 1.0001*((HLT_Ele23_WPLoose_Gsf_v2)&& (hltQuadJet15>=0) )","same");

    c1->SaveAs("check_full_Mqq_test.png");
    c1->SaveAs("check_full_Mqq_test.C");

    tree->Draw("bDetaqq_eta  >> h(50,0,10)"," test(offJet_pt[0], offJet_pt[1], offJet_pt[2], Max$(min(offJet_csv,1)), MaxIf$(min(offJet_csv,1),min(offJet_csv,1)!=Max$(min(offJet_csv,1))), bMqq_eta,bDetaqq_eta, bDetaqq_double, Mqq_double)*((HLT_Ele23_WPLoose_Gsf_v2))","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);h->SetMaximum(2.0*h->GetMaximum());
    tree->Draw("bDetaqq_eta"," 1.0001*((HLT_Ele23_WPLoose_Gsf_v2)&& (hltQuadJet15>=0) )","same");

    c1->SaveAs("check_full_bDetaqq_test.png");
    c1->SaveAs("check_full_bDetaqq_test.C");


}

//SingleBtagVBFTriggerWeight(pt1,pt2,pt3,pt4,CSV1,DeltaEtaqq_eta, Mqq_eta, DeltaPhibb_single, DeltaEtaqq_single)

//(HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1)
//HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v3
//HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v3
//HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v3

