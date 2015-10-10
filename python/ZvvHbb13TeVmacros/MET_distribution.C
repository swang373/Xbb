void MET_distribution(){
gROOT->SetBatch();
gStyle->SetPadGridX(1);
gStyle->SetPadGridY(1);
gStyle->SetOptStat(0);
gStyle->SetLineWidth(2);
gROOT->ForceStyle();

TChain* tree = new TChain("tree");
tree->Add("/gpfs/ddn/srm/cms/store/user/arizzi/VHBBHeppyV13/ZH_HToBB_ZToNuNu_M125_13TeV_amcatnloFXFX_madspin_pythia8/VHBB_HEPPY_V13_ZH_HToBB_ZToNuNu_M125_13TeV_amcatnloFXFX_madspin_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/151002_084016/0000/tree_*.root");
//TFile *_file0 = TFile::Open("../../env/ZvvHighPt_V12_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root");
//tree = (TTree*) _file0->Get("tree");

//TFile *_file0 = TFile::Open("../../env/ZvvHighPt_V12_ZH_HToBB_ZToNuNu_M125_13TeV_amcatnloFXFX_madspin_pythia8.root");
//tree = (TTree*) _file0->Get("tree");

TCanvas* c1 = new TCanvas("c1","c1",1280,768);

tree->Draw("met_pt >> metDistr(100,0,500)","met_genPt>150 && met_genPt<170");
tree->Draw("metPuppi_pt  >> metPuppiRes","met_genPt>150 && met_genPt<170","same");
tree->Draw("mhtJet30  >> mhtRes","met_genPt>150 && met_genPt<170","same");
tree->Draw("metType1p2_pt  >> metType1p2Res","met_genPt>150 && met_genPt<170","same");

metDistr = (TH1F*) gDirectory->Get("metDistr");
metPuppiRes = (TH1F*) gDirectory->Get("metPuppiRes");
mhtRes = (TH1F*) gDirectory->Get("mhtRes");
metType1p2Res = (TH1F*) gDirectory->Get("metType1p2Res");


metDistr->SetLineWidth(2);
metPuppiRes->SetLineWidth(2);
mhtRes->SetLineWidth(2);
metType1p2Res->SetLineWidth(2);


metDistr->SetLineColor(kBlack);
metPuppiRes->SetLineColor(kRed);
mhtRes->SetLineColor(kBlue);
metType1p2Res->SetLineColor(kGreen);

maxim = max(max(metDistr->GetMaximum(),mhtRes->GetMaximum()),max(metPuppiRes->GetMaximum(),metType1p2Res->GetMaximum()));

metDistr->SetMaximum(maxim*1.1);
metDistr->SetTitle("MET/MHT distribution for events with 150 GeV < genMET < 170 GeV");
metDistr->GetXaxis()->SetTitle("MET/MHT [GeV]");
metDistr->GetYaxis()->SetTitle("Events");


metDistr->Draw("");
metPuppiRes->Draw("same");
mhtRes->Draw("same");
metType1p2Res->Draw("same");

TLegend* leg = new TLegend(0.52,0.7,0.9,0.9);
//leg->SetHeader("The Legend Title");
leg->AddEntry(metDistr,"MET","l");
leg->AddEntry(metType1p2Res,"MET type 1.2","l");
leg->AddEntry(metPuppiRes,"MET PUPPI","l");
leg->AddEntry(mhtRes,"MHT (jet30)","l");
leg->Draw();

TF1* gaus1 = new TF1("gaus1","gaus");
TF1* gaus2 = new TF1("gaus2","gaus");
TF1* gaus3 = new TF1("gaus3","gaus");
TF1* gaus4 = new TF1("gaus4","gaus");

gaus1->SetLineColor(metDistr->GetLineColor());
gaus2->SetLineColor(metPuppiRes->GetLineColor());
gaus3->SetLineColor(mhtRes->GetLineColor());
gaus4->SetLineColor(metType1p2Res->GetLineColor());
    
metDistr->Fit(gaus1);
metPuppiRes->Fit(gaus2);
mhtRes->Fit(gaus3);
metType1p2Res->Fit(gaus4);

gaus1->SetRange(gaus1->GetParameter(1)-gaus1->GetParameter(2),gaus1->GetParameter(1)+gaus1->GetParameter(3));
gaus2->SetRange(gaus2->GetParameter(1)-gaus2->GetParameter(2),gaus2->GetParameter(1)+gaus2->GetParameter(3));
gaus3->SetRange(gaus3->GetParameter(1)-gaus3->GetParameter(2),gaus3->GetParameter(1)+gaus3->GetParameter(3));
gaus4->SetRange(gaus4->GetParameter(1)-gaus4->GetParameter(2),gaus4->GetParameter(1)+gaus4->GetParameter(3));
const float sigmap = 2;
const float sigmam = 1;

cout<<endl<< "Fitting metDistr"<<endl;
metDistr->Fit(gaus1,"","",sigmam*gaus1->GetParameter(1)-gaus1->GetParameter(2),gaus1->GetParameter(1)+sigmap*gaus1->GetParameter(2));
cout<<endl<< "Fitting metPuppiRes"<<endl;
metPuppiRes->Fit(gaus2,"","",sigmam*gaus2->GetParameter(1)-gaus2->GetParameter(2),gaus2->GetParameter(1)+sigmap*gaus2->GetParameter(2));
cout<<endl<< "Fitting mhtRes"<<endl;
mhtRes->Fit(gaus3,"","",sigmam*gaus3->GetParameter(1)-gaus3->GetParameter(2),gaus3->GetParameter(1)+sigmap*gaus3->GetParameter(2));
cout<<endl<< "Fitting metType1p2Res"<<endl;
metType1p2Res->Fit(gaus4,"","",sigmam*gaus4->GetParameter(1)-gaus4->GetParameter(2),gaus4->GetParameter(1)+sigmap*gaus4->GetParameter(2));   
   
c1->SaveAs("met_distributions.png");
c1->SaveAs("met_distributions.C");
}

