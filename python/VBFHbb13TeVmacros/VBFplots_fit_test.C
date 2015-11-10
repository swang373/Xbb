#include"fittedFunctions.h"

void VBFplots_fit_test(){
    gStyle->SetOptStat(0);
//    gROOT->SetBatch();

    TCanvas* c1 = new TCanvas("c1","c1");
    c1->SetGridx();
    c1->SetGridy();

    TFile *_file0 = TFile::Open("newTree2.root");
    TTree* tree = (TTree*) _file0->Get("tree");

    tree->Draw("Mqq_single  >> h(25,0,2000)"," SingleBtagVBFTriggerWeightNoCommonPart(Max$(min(offJet_csv,1)), bDphibb_single, bDetaqq_single)*(HLT_QuadPFJet_VBF_v3)","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);
    tree->Draw("Mqq_single"," 1.0001*(HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v3 && HLT_QuadPFJet_VBF_v3)","same");

    c1->SaveAs("check_Mqq_single.png");
    c1->SaveAs("check_Mqq_single.C");

    tree->Draw("Mbb_single  >> h(50,0,500)"," SingleBtagVBFTriggerWeightNoCommonPart(Max$(min(offJet_csv,1)), bDphibb_single, bDetaqq_single)*(HLT_QuadPFJet_VBF_v3)","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);
    tree->Draw("Mbb_single"," 1.0001*(HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v3 && HLT_QuadPFJet_VBF_v3)","same");

    c1->SaveAs("check_Mbb_single.png");
    c1->SaveAs("check_Mbb_single.C");

    tree->Draw("bDetaqq_single  >> h(50,0,10)"," SingleBtagVBFTriggerWeightNoCommonPart(Max$(min(offJet_csv,1)), bDphibb_single, bDetaqq_single)*(HLT_QuadPFJet_VBF_v3)","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);
    tree->Draw("bDetaqq_single"," 1.0001*(HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v3 && HLT_QuadPFJet_VBF_v3)","same");

    c1->SaveAs("check_bDetaqq_single.png");
    c1->SaveAs("check_bDetaqq_single.C");

    tree->Draw("bDphibb_single  >> h(32,0,3.2)"," SingleBtagVBFTriggerWeightNoCommonPart(Max$(min(offJet_csv,1)), bDphibb_single, bDetaqq_single)*(HLT_QuadPFJet_VBF_v3)","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);
    tree->Draw("bDphibb_single"," 1.0001*(HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v3 && HLT_QuadPFJet_VBF_v3)","same");

    c1->SaveAs("check_bDphibb_single.png");
    c1->SaveAs("check_bDphibb_single.C");

    tree->Draw("Max$(offJet_csv)  >> h(40,0,1)"," SingleBtagVBFTriggerWeightNoCommonPart(Max$(min(offJet_csv,1)), bDphibb_single, bDetaqq_single)*(HLT_QuadPFJet_VBF_v3)","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);
    tree->Draw("Max$(offJet_csv)"," 1.0001*(HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v3 && HLT_QuadPFJet_VBF_v3)","same");
    c1->SaveAs("check_CSV1_single.png");
    c1->SaveAs("check_CSV1_single.C");

    tree->Draw("MaxIf$(offJet_csv,offJet_csv!=Max$(offJet_csv))  >> h(40,0,1)"," SingleBtagVBFTriggerWeightNoCommonPart(Max$(min(offJet_csv,1)), bDphibb_single, bDetaqq_single)*(HLT_QuadPFJet_VBF_v3)","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);
    tree->Draw("MaxIf$(offJet_csv,offJet_csv!=Max$(offJet_csv))"," 1.0001*(HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v3 && HLT_QuadPFJet_VBF_v3)","same");
    c1->SaveAs("check_CSV2_single.png");
    c1->SaveAs("check_CSV2_single.C");

}

//SingleBtagVBFTriggerWeight(pt1,pt2,pt3,pt4,CSV1,DeltaEtaqq_eta, Mqq_eta, DeltaPhibb_single, DeltaEtaqq_single)

//HLT_QuadPFJet_VBF_v3
//HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v3
//HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v3
//HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v3

