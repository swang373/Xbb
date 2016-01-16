#include"fittedFunctions.h"

void VBFplots_fit_test_doubleBtagNoCommonPart(){
    gStyle->SetOptStat(0);
//    gROOT->SetBatch();

    TCanvas* c1 = new TCanvas("c1","c1");
    c1->SetGridx();
    c1->SetGridy();

    TFile *_file0 = TFile::Open("newTree5.root");
    TTree* tree = (TTree*) _file0->Get("tree");

//    //////////////////////////////////////////////////
//    // plots for the double b-tag trigger, starting from (HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1)
//    //////////////////////////////////////////////////

    tree->Draw("bMqq_double  >> h(25,0,2000)"," DoubleBtagVBFTriggerWeightNoCommonPart(Max$(min(offJet_csv,1)), MaxIf$(min(offJet_csv,1),min(offJet_csv,1)!=Max$(min(offJet_csv,1))), bDetaqq_double, Mqq_double)*((HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);h->SetMaximum(2.0*h->GetMaximum());
    tree->Draw("bMqq_double"," 1.0001*(HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v3 && (HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","same");

    c1->SaveAs("check_Mqq_double.png");
    c1->SaveAs("check_Mqq_double.C");

    tree->Draw("Mbb_double  >> h(50,0,500)"," DoubleBtagVBFTriggerWeightNoCommonPart(Max$(min(offJet_csv,1)), MaxIf$(min(offJet_csv,1),min(offJet_csv,1)!=Max$(min(offJet_csv,1))), bDetaqq_double, Mqq_double)*((HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);h->SetMaximum(2.0*h->GetMaximum());
    tree->Draw("Mbb_double"," 1.0001*(HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v3 && (HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","same");

    c1->SaveAs("check_Mbb_double.png");
    c1->SaveAs("check_Mbb_double.C");

    tree->Draw("bDetaqq_double  >> h(50,0,10)"," DoubleBtagVBFTriggerWeightNoCommonPart(Max$(min(offJet_csv,1)), MaxIf$(min(offJet_csv,1),min(offJet_csv,1)!=Max$(min(offJet_csv,1))), bDetaqq_double, Mqq_double)*((HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);h->SetMaximum(2.0*h->GetMaximum());
    tree->Draw("bDetaqq_double"," 1.0001*(HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v3 && (HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","same");

    c1->SaveAs("check_bDetaqq_double.png");
    c1->SaveAs("check_bDetaqq_double.C");

    tree->Draw("bDphibb_double  >> h(32,0,3.2)"," DoubleBtagVBFTriggerWeightNoCommonPart(Max$(min(offJet_csv,1)), MaxIf$(min(offJet_csv,1),min(offJet_csv,1)!=Max$(min(offJet_csv,1))), bDetaqq_double, Mqq_double)*((HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);h->SetMaximum(2.0*h->GetMaximum());
    tree->Draw("bDphibb_double"," 1.0001*(HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v3 && (HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","same");

    c1->SaveAs("check_bDphibb_double.png");
    c1->SaveAs("check_bDphibb_double.C");

    tree->Draw("Max$(offJet_csv)  >> h(40,0,1)"," DoubleBtagVBFTriggerWeightNoCommonPart(Max$(min(offJet_csv,1)), MaxIf$(min(offJet_csv,1),min(offJet_csv,1)!=Max$(min(offJet_csv,1))), bDetaqq_double, Mqq_double)*((HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);h->SetMaximum(2.0*h->GetMaximum());
    tree->Draw("Max$(offJet_csv)"," 1.0001*(HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v3 && (HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","same");
    c1->SaveAs("check_CSV1_double.png");
    c1->SaveAs("check_CSV1_double.C");

    tree->Draw("MaxIf$(offJet_csv,offJet_csv!=Max$(offJet_csv))  >> h(40,0,1)"," DoubleBtagVBFTriggerWeightNoCommonPart(Max$(min(offJet_csv,1)), MaxIf$(min(offJet_csv,1),min(offJet_csv,1)!=Max$(min(offJet_csv,1))), bDetaqq_double, Mqq_double)*((HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","");
    h = (TProfile*) gDirectory->Get("h");h->SetLineColor(kBlack);h->SetMaximum(2.0*h->GetMaximum());
    tree->Draw("MaxIf$(offJet_csv,offJet_csv!=Max$(offJet_csv))"," 1.0001*(HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v3 && (HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1))","same");
    c1->SaveAs("check_CSV2_double.png");
    c1->SaveAs("check_CSV2_double.C");


}

//SingleBtagVBFTriggerWeight(pt1,pt2,pt3,pt4,CSV1,DeltaEtaqq_eta, Mqq_eta, DeltaPhibb_single, DeltaEtaqq_single)

//(HLT_QuadPFJet_VBF_v3 && hltCSVL30p74>=1)
//HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v3
//HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v3
//HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v3

