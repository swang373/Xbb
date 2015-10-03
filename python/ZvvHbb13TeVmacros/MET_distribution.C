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

tree->Draw("met_pt >> metDistr","met_pt<500 && met_genPt>170 && met_genPt<180");
tree->Draw("metPuppi_pt  >> metPuppiDistr","met_genPt>170 && met_genPt<180","same");
tree->Draw("mhtJet30  >> mhtDistr","met_genPt>170 && met_genPt<180","same");
tree->Draw("metType1p2_pt  >> metType1p2Distr","met_genPt>170 && met_genPt<180","same");

metDistr = (TH1F*) gDirectory->Get("metDistr");
metPuppiDistr = (TH1F*) gDirectory->Get("metPuppiDistr");
mhtDistr = (TH1F*) gDirectory->Get("mhtDistr");
metType1p2Distr = (TH1F*) gDirectory->Get("metType1p2Distr");


metDistr->SetLineWidth(2);
metPuppiDistr->SetLineWidth(2);
mhtDistr->SetLineWidth(2);
metType1p2Distr->SetLineWidth(2);


metDistr->SetLineColor(kBlack);
metPuppiDistr->SetLineColor(kRed);
mhtDistr->SetLineColor(kBlue);
metType1p2Distr->SetLineColor(kGreen);

maxim = max(max(metDistr->GetMaximum(),mhtDistr->GetMaximum()),max(metPuppiDistr->GetMaximum(),metType1p2Distr->GetMaximum()));

metDistr->SetMaximum(maxim*1.1);
metDistr->SetTitle("MET/MHT distribution for events with 170 GeV < genMET < 180 GeV");
metDistr->GetXaxis()->SetTitle("MET/MHT [GeV]");
metDistr->GetYaxis()->SetTitle("Events");


metDistr->Draw("");
metPuppiDistr->Draw("same");
mhtDistr->Draw("same");
metType1p2Distr->Draw("same");

TLegend* leg = new TLegend(0.52,0.7,0.9,0.9);
//leg->SetHeader("The Legend Title");
leg->AddEntry(metDistr,"MET","l");
leg->AddEntry(metType1p2Distr,"MET type 1.2","l");
leg->AddEntry(metPuppiDistr,"MET PUPPI","l");
leg->AddEntry(mhtDistr,"MHT (jet30)","l");
leg->Draw();
   
c1->SaveAs("met_distributions.png");
c1->SaveAs("met_distributions.C");
}

