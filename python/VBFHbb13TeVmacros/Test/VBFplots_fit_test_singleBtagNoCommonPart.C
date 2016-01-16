#include"fittedFunctions.h"

void VBFplots_fit_test_singleBtagNoCommonPart(){
    gStyle->SetOptStat(0);
//    gROOT->SetBatch();

    TCanvas* c1 = new TCanvas("c1","c1");
    c1->SetGridx();
    c1->SetGridy();

    TFile *_file0 = TFile::Open("newTree5.root");
    TTree* tree = (TTree*) _file0->Get("tree");

//    ////////////////////////////////////////////////// ()
//    // plots for the single b-tag trigger, starting from (HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1)
//    //////////////////////////////////////////////////

    tree->Draw("bMqq_single  >> h(25,0,2000)"," SingleBtagVBFTriggerWeightNoCommonPart(Max$(min(offJet_csv,1)), bDphibb_single, bDetaqq_single)*((HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);h->SetMaximum(2.0*h->GetMaximum());
    tree->Draw("bMqq_single"," 1.0001*(HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v3 && (HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","same");

    c1->SaveAs("check_Mqq_single.png");
    c1->SaveAs("check_Mqq_single.C");

    tree->Draw("Mbb_single  >> h(50,0,500)"," SingleBtagVBFTriggerWeightNoCommonPart(Max$(min(offJet_csv,1)), bDphibb_single, bDetaqq_single)*((HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);h->SetMaximum(2.0*h->GetMaximum());
    tree->Draw("Mbb_single"," 1.0001*(HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v3 && (HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","same");

    c1->SaveAs("check_Mbb_single.png");
    c1->SaveAs("check_Mbb_single.C");

    tree->Draw("bDetaqq_single  >> h(50,0,10)"," SingleBtagVBFTriggerWeightNoCommonPart(Max$(min(offJet_csv,1)), bDphibb_single, bDetaqq_single)*((HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);h->SetMaximum(2.0*h->GetMaximum());
    tree->Draw("bDetaqq_single"," 1.0001*(HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v3 && (HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","same");

    c1->SaveAs("check_bDetaqq_single.png");
    c1->SaveAs("check_bDetaqq_single.C");

    tree->Draw("bDphibb_single  >> h(32,0,3.2)"," SingleBtagVBFTriggerWeightNoCommonPart(Max$(min(offJet_csv,1)), bDphibb_single, bDetaqq_single)*((HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);h->SetMaximum(2.0*h->GetMaximum());
    tree->Draw("bDphibb_single"," 1.0001*(HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v3 && (HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","same");

    c1->SaveAs("check_bDphibb_single.png");
    c1->SaveAs("check_bDphibb_single.C");

    tree->Draw("Max$(offJet_csv)  >> h(40,0,1)"," SingleBtagVBFTriggerWeightNoCommonPart(Max$(min(offJet_csv,1)), bDphibb_single, bDetaqq_single)*((HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);h->SetMaximum(2.0*h->GetMaximum());
    tree->Draw("Max$(offJet_csv)"," 1.0001*(HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v3 && (HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","same");
    c1->SaveAs("check_CSV1_single.png");
    c1->SaveAs("check_CSV1_single.C");

    tree->Draw("MaxIf$(offJet_csv,offJet_csv!=Max$(offJet_csv))  >> h(40,0,1)"," SingleBtagVBFTriggerWeightNoCommonPart(Max$(min(offJet_csv,1)), bDphibb_single, bDetaqq_single)*((HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);h->SetMaximum(2.0*h->GetMaximum());
    tree->Draw("MaxIf$(offJet_csv,offJet_csv!=Max$(offJet_csv))"," 1.0001*(HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v3 && (HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","same");
    c1->SaveAs("check_CSV2_single.png");
    c1->SaveAs("check_CSV2_single.C");


}

