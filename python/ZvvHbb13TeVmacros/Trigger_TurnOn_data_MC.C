void Trigger_TurnOn_data_MC(){
gROOT->SetBatch();
gStyle->SetPadGridX(1);
gStyle->SetPadGridY(1);
gStyle->SetOptStat(0);
gStyle->SetLineWidth(2);
gROOT->ForceStyle();

TChain* tree = new TChain("tree");

TCanvas* c1 = new TCanvas("c1","c1",1280,768);

//const char* preselection = "HLT_BIT_HLT_IsoMu20_v && json && max(Max$(vLeptons_pt),Max$(aLeptons_pt))<60 && max(Max$(vLeptons_pt),Max$(aLeptons_pt))>30 && Flag_hbheFilterNew &&Flag_hbheIsoFilter && Flag_goodVertices &&Flag_eeBadScFilter &&Flag_CSCTightHaloFilter && MinIf$(abs(TVector2::Phi_mpi_pi(Jet_phi-met_phi)),Jet_pt>30 && Jet_eta<5.2)>0.5 ";
//const char* preselection_data = preselection;
const char* preselection = "HLT_BIT_HLT_Ele27_WP85_Gsf_v         && json && max(Max$(vLeptons_pt),Max$(aLeptons_pt))<60 && max(Max$(vLeptons_pt),Max$(aLeptons_pt))>30 && Flag_hbheFilterNew &&Flag_hbheIsoFilter && Flag_goodVertices &&Flag_eeBadScFilter &&Flag_CSCTightHaloFilter && MinIf$(abs(TVector2::Phi_mpi_pi(Jet_phi-met_phi)),Jet_pt>30 && Jet_eta<5.2)>0.5 ";
const char* preselection_data = "HLT_BIT_HLT_Ele27_WPLoose_Gsf_v && json && max(Max$(vLeptons_pt),Max$(aLeptons_pt))<60 && max(Max$(vLeptons_pt),Max$(aLeptons_pt))>30 && Flag_hbheFilterNew &&Flag_hbheIsoFilter && Flag_goodVertices &&Flag_eeBadScFilter &&Flag_CSCTightHaloFilter && MinIf$(abs(TVector2::Phi_mpi_pi(Jet_phi-met_phi)),Jet_pt>30 && Jet_eta<5.2)>0.5 ";

tree->Reset();
//tree->Add("../../env/ZvvHighPt_V14_SingleElectron.root");
tree->Add("/gpfs/ddn/srm/cms/store/user/arizzi/VHBBHeppyV15/SingleElectron/VHBB_HEPPY_V15_SingleElectron__Run2015D-05Oct2015-v1/151027_145709/0000/tree_**.root");
//tree->Add("../../env/ZvvHighPt_V14_SingleMuon.root");
//tree->Add("/gpfs/ddn/srm/cms/store/user/arizzi/VHBBHeppyV15/SingleMuon/VHBB_HEPPY_V15_SingleMuon__Run2015D-05Oct2015-v1/151027_145808/0000/tree_99*");
tree->Draw("HLT_BIT_HLT_PFMET90_PFMHT90_IDTight_v :min(met_pt,mhtJet30) >> PFMET90_data(100,0,400)",preselection_data,"prof");
PFMET90_data = (TProfile*) gDirectory->Get("PFMET90_data");

tree->Reset();
//tree->Add("../../env/ZvvHighPt_V14_WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root");
tree->Add("/gpfs/ddn/srm/cms/store/user/arizzi/VHBBHeppyV14/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V14_WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151024_220138/0000/tree_**.root");
//tree->Add("/gpfs/ddn/srm/cms/store/user/arizzi/VHBBHeppyV14/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V14_WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151024_220559/0000/tree_1*");
tree->Draw("HLT_BIT_HLT_PFMET90_PFMHT90_IDLoose_v :min(met_pt,mhtJet30) >> PFMET90_WjetsHT100(100,0,400)",preselection,"prof");
PFMET90_WjetsHT100 = (TProfile*) gDirectory->Get("PFMET90_WjetsHT100");

tree->Reset();
tree->Add("/gpfs/ddn/srm/cms/store/user/arizzi/VHBBHeppyV14/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V14_WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151024_220559/0000/tree_**.root");
//tree->Add("/gpfs/ddn/srm/cms/store/user/arizzi/VHBBHeppyV14/TT_TuneCUETP8M1_13TeV-powheg-pythia8/VHBB_HEPPY_V14_TT_TuneCUETP8M1_13TeV-powheg-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151024_212301/0000/tree_99*");
tree->Draw("HLT_BIT_HLT_PFMET90_PFMHT90_IDLoose_v :min(met_pt,mhtJet30) >> PFMET90_WjetsHT200(100,0,400)",preselection,"prof");
PFMET90_WjetsHT200 = (TProfile*) gDirectory->Get("PFMET90_WjetsHT200");

tree->Reset();
//tree->Add("../../env/ZvvHighPt_V14_WH_HToBB_WToLNu_M125_13TeV_amcatnloFXFX_madspin_pythia8.root");
tree->Add("/gpfs/ddn/srm/cms/store/user/arizzi/VHBBHeppyV14/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V14_WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151025_084451/0000/tree_**.root");

//tree->Add("/gpfs/ddn/srm/cms/store/user/arizzi/VHBBHeppyV14/WH_HToBB_WToLNu_M125_13TeV_amcatnloFXFX_madspin_pythia8/VHBB_HEPPY_V14_WH_HToBB_WToLNu_M125_13TeV_amcatnloFXFX_madspin_pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151024_220043/0000/tree_**");
tree->Draw("HLT_BIT_HLT_PFMET90_PFMHT90_IDLoose_v :min(met_pt,mhtJet30) >> PFMET90_WjetsHT400(100,0,400)",preselection,"prof");
PFMET90_WjetsHT400 = (TProfile*) gDirectory->Get("PFMET90_WjetsHT400");



PFMET90_data->SetLineWidth(2);
PFMET90_WjetsHT100->SetLineWidth(2);
PFMET90_WjetsHT200->SetLineWidth(2);
PFMET90_WjetsHT400->SetLineWidth(2);


PFMET90_data->SetLineColor(kBlack);
PFMET90_WjetsHT100->SetLineColor(kRed);
PFMET90_WjetsHT200->SetLineColor(kBlue);
PFMET90_WjetsHT400->SetLineColor(kGreen);

maxim = max(max(PFMET90_data->GetMaximum(),PFMET90_WjetsHT200->GetMaximum()),max(PFMET90_WjetsHT100->GetMaximum(),PFMET90_WjetsHT400->GetMaximum()));

PFMET90_data->SetMaximum(maxim*1.1);
PFMET90_data->SetTitle("Trigger efficiency");
PFMET90_data->GetXaxis()->SetTitle("min(MET,MHT) [GeV]");
PFMET90_data->GetYaxis()->SetTitle("Efficiency");


PFMET90_data->Draw("");
PFMET90_WjetsHT100->Draw("same");
PFMET90_WjetsHT200->Draw("same");
PFMET90_WjetsHT400->Draw("same");

TLegend* leg = new TLegend(0.45,0.1,0.9,0.3);
//leg->SetHeader("The Legend Title");
leg->AddEntry(PFMET90_data,"HLT_PFMET90_PFMHT90 in data","l");
leg->AddEntry(PFMET90_WjetsHT100,"HLT_PFMET90_PFMHT90 in WjetsHT100","l");
leg->AddEntry(PFMET90_WjetsHT200,"HLT_PFMET90_PFMHT90 in WjetsHT200","l");
leg->AddEntry(PFMET90_WjetsHT400,"HLT_PFMET90_PFMHT90 in WjetsHT400","l");
leg->Draw();

//const char* function = "  [2]/(1+exp(-[1]*(x-[0])))  ";
const char* function_string = "  (0.5+0.5*erf( (x-[0])*(x-[0]>[5])/[1] + (x-[0])*(x-[0]<[5])/[2] + [5]*(1/[1]-1/[2])*(x-[0]<[5]) ))*[4]+[3]  ";

TF1* turnon1 = new TF1("turnon1",function_string);
turnon1->SetParameters(110,35,35,0,1,0);
TF1* turnon2 = (TF1*) turnon1->Clone("turnon1");
TF1* turnon3 = (TF1*) turnon1->Clone("turnon1");
TF1* turnon4 = (TF1*) turnon1->Clone("turnon1");

turnon1->SetParameters(100,0.01,1);
turnon2->SetParameters(100,0.01,1);
turnon3->SetParameters(100,0.01,1);
turnon4->SetParameters(100,0.01,1);

turnon1->SetLineColor(PFMET90_data->GetLineColor());
turnon2->SetLineColor(PFMET90_WjetsHT100->GetLineColor());
turnon3->SetLineColor(PFMET90_WjetsHT200->GetLineColor());
turnon4->SetLineColor(PFMET90_WjetsHT400->GetLineColor());

PFMET90_data->Fit(turnon1);
PFMET90_WjetsHT100->Fit(turnon2);
PFMET90_WjetsHT200->Fit(turnon3);
PFMET90_WjetsHT400->Fit(turnon4);

turnon1->SetRange(turnon1->GetParameter(1)-turnon1->GetParameter(2),turnon1->GetParameter(1)+turnon1->GetParameter(3));
turnon2->SetRange(turnon2->GetParameter(1)-turnon2->GetParameter(2),turnon2->GetParameter(1)+turnon2->GetParameter(3));
turnon3->SetRange(turnon3->GetParameter(1)-turnon3->GetParameter(2),turnon3->GetParameter(1)+turnon3->GetParameter(3));
turnon4->SetRange(turnon4->GetParameter(1)-turnon4->GetParameter(2),turnon4->GetParameter(1)+turnon4->GetParameter(3));
const float sigmap = 2;
const float sigmam = 1;

cout<<endl<< "Fitting PFMET90_data"<<endl;
PFMET90_data->Fit(turnon1,"","",sigmam*turnon1->GetParameter(1)-turnon1->GetParameter(2),turnon1->GetParameter(1)+sigmap*turnon1->GetParameter(2));
cout<<endl<< "Fitting PFMET90_WjetsHT100"<<endl;
PFMET90_WjetsHT100->Fit(turnon2,"","",sigmam*turnon2->GetParameter(1)-turnon2->GetParameter(2),turnon2->GetParameter(1)+sigmap*turnon2->GetParameter(2));
cout<<endl<< "Fitting PFMET90_WjetsHT200"<<endl;
PFMET90_WjetsHT200->Fit(turnon3,"","",sigmam*turnon3->GetParameter(1)-turnon3->GetParameter(2),turnon3->GetParameter(1)+sigmap*turnon3->GetParameter(2));
cout<<endl<< "Fitting PFMET90_WjetsHT400"<<endl;
PFMET90_WjetsHT400->Fit(turnon4,"","",sigmam*turnon4->GetParameter(1)-turnon4->GetParameter(2),turnon4->GetParameter(1)+sigmap*turnon4->GetParameter(2));

c1->SaveAs("trigger_turnon_data_MC.png");
c1->SaveAs("trigger_turnon_data_MC.C");
}

