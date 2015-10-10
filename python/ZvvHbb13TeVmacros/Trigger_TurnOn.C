void Trigger_TurnOn(){
gROOT->SetBatch();
gStyle->SetPadGridX(1);
gStyle->SetPadGridY(1);
gStyle->SetOptStat(0);
gStyle->SetLineWidth(2);
gROOT->ForceStyle();

TChain* tree = new TChain("tree");
tree->Add("/gpfs/ddn/srm/cms/store/user/arizzi/VHBBHeppyV13/ZH_HToBB_ZToNuNu_M125_13TeV_amcatnloFXFX_madspin_pythia8/VHBB_HEPPY_V13_ZH_HToBB_ZToNuNu_M125_13TeV_amcatnloFXFX_madspin_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/151002_084016/0000/tree_*.root");

TCanvas* c1 = new TCanvas("c1","c1",1280,768);

const char* preselection = "Vtype>=0 && Jet_btagCSV[hJCidx[0]]>0.941 && Jet_btagCSV[hJCidx[1]]>0.814";
tree->Draw("HLT_BIT_HLT_PFMET90_PFMHT90_IDLoose_v :met_genPt >> PFMET90(100,0,400)",preselection,"prof");
tree->Draw("HLT_BIT_HLT_PFMET120_PFMHT120_IDLoose_v :met_genPt >> PFMET120(100,0,400)",preselection,"prof");
tree->Draw("HLT_BIT_HLT_PFMET170_NoiseCleaned_v :met_genPt >> MET170(100,0,400)",preselection,"prof");
tree->Draw("HLT_BIT_HLT_CaloMHTNoPU90_PFMET90_PFMHT90_IDLoose_BTagCSV0p7_v :met_genPt >> CaloMHT90Btag(100,0,400)",preselection,"prof");

PFMET90 = (TH1F*) gDirectory->Get("PFMET90");
PFMET120 = (TH1F*) gDirectory->Get("PFMET120");
MET170 = (TH1F*) gDirectory->Get("MET170");
CaloMHT90Btag = (TH1F*) gDirectory->Get("CaloMHT90Btag");


PFMET90->SetLineWidth(2);
PFMET120->SetLineWidth(2);
MET170->SetLineWidth(2);
CaloMHT90Btag->SetLineWidth(2);


PFMET90->SetLineColor(kBlack);
PFMET120->SetLineColor(kRed);
MET170->SetLineColor(kBlue);
CaloMHT90Btag->SetLineColor(kGreen);

maxim = max(max(PFMET90->GetMaximum(),MET170->GetMaximum()),max(PFMET120->GetMaximum(),CaloMHT90Btag->GetMaximum()));

PFMET90->SetMaximum(maxim*1.1);
PFMET90->SetTitle("Trigger efficiency");
PFMET90->GetXaxis()->SetTitle("genMET [GeV]");
PFMET90->GetYaxis()->SetTitle("Efficiency");


PFMET90->Draw("");
PFMET120->Draw("same");
MET170->Draw("same");
CaloMHT90Btag->Draw("same");

TLegend* leg = new TLegend(0.45,0.1,0.9,0.3);
//leg->SetHeader("The Legend Title");
leg->AddEntry(PFMET90,"HLT_PFMET90_PFMHT90_IDLoose","l");
leg->AddEntry(PFMET120,"HLT_PFMET120_PFMHT120_IDLoose","l");
leg->AddEntry(CaloMHT90Btag,"HLT_CaloMHTNoPU90_PFMET90_PFMHT90_IDLoose_BTagCSV0p7_v","l");
leg->AddEntry(MET170,"HLT_PFMET170_NoiseCleaned_v","l");
leg->Draw();

const char* function = "  [2]/(1+exp(-[1]*(x-[0])))  ";
TF1* turnon1 = new TF1("turnon1",function);
TF1* turnon2 = new TF1("turnon2",function);
TF1* turnon3 = new TF1("turnon3",function);
TF1* turnon4 = new TF1("turnon4",function);

turnon1->SetParameters(100,0.01,1);
turnon2->SetParameters(100,0.01,1);
turnon3->SetParameters(100,0.01,1);
turnon4->SetParameters(100,0.01,1);

turnon1->SetLineColor(PFMET90->GetLineColor());
turnon2->SetLineColor(PFMET120->GetLineColor());
turnon3->SetLineColor(MET170->GetLineColor());
turnon4->SetLineColor(CaloMHT90Btag->GetLineColor());
    
PFMET90->Fit(turnon1);
PFMET120->Fit(turnon2);
MET170->Fit(turnon3);
CaloMHT90Btag->Fit(turnon4);

turnon1->SetRange(turnon1->GetParameter(1)-turnon1->GetParameter(2),turnon1->GetParameter(1)+turnon1->GetParameter(3));
turnon2->SetRange(turnon2->GetParameter(1)-turnon2->GetParameter(2),turnon2->GetParameter(1)+turnon2->GetParameter(3));
turnon3->SetRange(turnon3->GetParameter(1)-turnon3->GetParameter(2),turnon3->GetParameter(1)+turnon3->GetParameter(3));
turnon4->SetRange(turnon4->GetParameter(1)-turnon4->GetParameter(2),turnon4->GetParameter(1)+turnon4->GetParameter(3));
const float sigmap = 2;
const float sigmam = 1;

cout<<endl<< "Fitting PFMET90"<<endl;
PFMET90->Fit(turnon1,"","",sigmam*turnon1->GetParameter(1)-turnon1->GetParameter(2),turnon1->GetParameter(1)+sigmap*turnon1->GetParameter(2));
cout<<endl<< "Fitting PFMET120"<<endl;
PFMET120->Fit(turnon2,"","",sigmam*turnon2->GetParameter(1)-turnon2->GetParameter(2),turnon2->GetParameter(1)+sigmap*turnon2->GetParameter(2));
cout<<endl<< "Fitting MET170"<<endl;
MET170->Fit(turnon3,"","",sigmam*turnon3->GetParameter(1)-turnon3->GetParameter(2),turnon3->GetParameter(1)+sigmap*turnon3->GetParameter(2));
cout<<endl<< "Fitting CaloMHT90Btag"<<endl;
CaloMHT90Btag->Fit(turnon4,"","",sigmam*turnon4->GetParameter(1)-turnon4->GetParameter(2),turnon4->GetParameter(1)+sigmap*turnon4->GetParameter(2));   
   
c1->SaveAs("trigger_turnon.png");
c1->SaveAs("trigger_turnon.C");
}

