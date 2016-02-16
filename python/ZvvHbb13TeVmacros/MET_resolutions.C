#include <algorithm>
void MET_resolutions(){
gROOT->SetBatch();
gStyle->SetPadGridX(1);
gStyle->SetPadGridY(1);
gStyle->SetOptStat(0);
gStyle->SetLineWidth(2);
//gStyle->SetOptFit();
gROOT->ForceStyle();

TChain* tree = new TChain("tree");
tree->Add("../MCAndDataLinks/ZH_HToBB_ZToNuNu_M125_13TeV_amcatnloFXFX_madspin_pythia8/VHBB_HEPPY_V20_ZH_HToBB_ZToNuNu_M125_13TeV_amcatnloFXFX_madspin_Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160209_172306/0000/tree_*.root");
//TFile *_file0 = TFile::Open("../../env/ZvvHighPt_V12_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root");
//tree = (TTree*) _file0->Get("tree");

//TFile *_file0 = TFile::Open("../../env/ZvvHighPt_V12_ZH_HToBB_ZToNuNu_M125_13TeV_amcatnloFXFX_madspin_pythia8.root");
//tree = (TTree*) _file0->Get("tree");

TCanvas* c1 = new TCanvas("c1","c1",1280,768);

tree->Draw("(met_pt-met_genPt)/met_pt >> metRes(200,-1,1)","met_genPt>150");
tree->Draw("(metPuppi_pt-met_genPt)/met_pt  >> metPuppiRes","met_genPt>150","+sames");
tree->Draw("(mhtJet30-met_genPt)/met_pt  >> mhtRes","met_genPt>150","+sames");
tree->Draw("(metType1p2_pt-met_genPt)/met_pt  >> metType1p2Res","met_genPt>150","+sames");

metRes = (TH1F*) gDirectory->Get("metRes");
metPuppiRes = (TH1F*) gDirectory->Get("metPuppiRes");
mhtRes = (TH1F*) gDirectory->Get("mhtRes");
metType1p2Res = (TH1F*) gDirectory->Get("metType1p2Res");


metRes->SetLineWidth(2);
metPuppiRes->SetLineWidth(2);
mhtRes->SetLineWidth(2);
metType1p2Res->SetLineWidth(2);


metRes->SetLineColor(kBlack);
metPuppiRes->SetLineColor(kRed);
mhtRes->SetLineColor(kBlue);
metType1p2Res->SetLineColor(kGreen);

float maxim = max(max(metRes->GetMaximum(),mhtRes->GetMaximum()),max(metPuppiRes->GetMaximum(),metType1p2Res->GetMaximum()));

metRes->SetMaximum(maxim*1.1);
metRes->SetTitle("(MET-genMET)/MET for events with genMET > 150 GeV");
metRes->GetXaxis()->SetTitle("(MET-genMET)/MET [GeV]");
metRes->GetYaxis()->SetTitle("Events");

TLegend* leg = new TLegend(0.1,0.7,0.25,0.9);
//leg->SetHeader("The Legend Title");
leg->AddEntry(metRes,"MET","l");
leg->AddEntry(metType1p2Res,"MET type 1.2","l");
leg->AddEntry(metPuppiRes,"MET PUPPI","l");
leg->AddEntry(mhtRes,"MHT (jet30)","l");

TF1* gaus1 = new TF1("gaus1","gaus");
TF1* gaus2 = new TF1("gaus2","gaus");
TF1* gaus3 = new TF1("gaus3","gaus");
TF1* gaus4 = new TF1("gaus4","gaus");

gaus1->SetLineColor(metRes->GetLineColor());
gaus2->SetLineColor(metPuppiRes->GetLineColor());
gaus3->SetLineColor(mhtRes->GetLineColor());
gaus4->SetLineColor(metType1p2Res->GetLineColor());
    
metRes->Fit(gaus1);
metPuppiRes->Fit(gaus2);
mhtRes->Fit(gaus3);
metType1p2Res->Fit(gaus4);

gaus1->SetRange(gaus1->GetParameter(1)-gaus1->GetParameter(2),gaus1->GetParameter(1)+gaus1->GetParameter(3));
gaus2->SetRange(gaus2->GetParameter(1)-gaus2->GetParameter(2),gaus2->GetParameter(1)+gaus2->GetParameter(3));
gaus3->SetRange(gaus3->GetParameter(1)-gaus3->GetParameter(2),gaus3->GetParameter(1)+gaus3->GetParameter(3));
gaus4->SetRange(gaus4->GetParameter(1)-gaus4->GetParameter(2),gaus4->GetParameter(1)+gaus4->GetParameter(3));

const float sigmap = 2;
const float sigmam = 1;

cout<<endl<< "Fitting metRes"<<endl;
metRes->Fit(gaus1,"","",sigmam*gaus1->GetParameter(1)-gaus1->GetParameter(2),gaus1->GetParameter(1)+sigmap*gaus1->GetParameter(2));
cout<<endl<< "Fitting metPuppiRes"<<endl;
metPuppiRes->Fit(gaus2,"","",sigmam*gaus2->GetParameter(1)-gaus2->GetParameter(2),gaus2->GetParameter(1)+sigmap*gaus2->GetParameter(2));
cout<<endl<< "Fitting mhtRes"<<endl;
mhtRes->Fit(gaus3,"","",sigmam*gaus3->GetParameter(1)-gaus3->GetParameter(2),gaus3->GetParameter(1)+sigmap*gaus3->GetParameter(2));
cout<<endl<< "Fitting metType1p2Res"<<endl;
metType1p2Res->Fit(gaus4,"","",sigmam*gaus4->GetParameter(1)-gaus4->GetParameter(2),gaus4->GetParameter(1)+sigmap*gaus4->GetParameter(2));   

metRes->Draw("");
metPuppiRes->Draw("same");
mhtRes->Draw("same");
metType1p2Res->Draw("same");
leg->Draw();

c1->SaveAs("met_resolutions.png");
c1->SaveAs("met_resolutions.C");
}

