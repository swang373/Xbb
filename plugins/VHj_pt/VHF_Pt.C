#include "TString.h"
#include "TBranch.h"
#include "TTree.h"
#include "TFile.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TLorentzVector.h"
#include "TCanvas.h"
#include "TGraph2D.h"
#include "TStyle.h"

#include "tdrstyle.C"

#include <iostream>
#include <vector>

//_*_*_*
//Macros
//_*_*_*

//Create a TLorentzVector of the jets other than the two Higgs candidate b-jets. 
vector<TLorentzVector> OtherJets(Float_t Jet_pt[15], Float_t Jet_eta[15], Float_t Jet_phi[15], Float_t Jet_mass[15], Int_t Jet_puId[15], Int_t Jet_id[15], Int_t aJCidx[8], Int_t hJCidx[2]){
  vector<TLorentzVector> OtherJets;
  for(int i = 0; i < 15; ++i){
    TLorentzVector Ojet;
    if(Jet_pt[i]>30 && abs(Jet_eta[i])<4.5 && Jet_puId[i]>0 && Jet_id[i]>0 && aJCidx[i] != (hJCidx[0]) && (aJCidx[i] != (hJCidx[1]))){
      Ojet.SetPtEtaPhiM( Jet_pt[i], Jet_eta[i], Jet_phi[i], Jet_mass[i]);
    }
    OtherJets.push_back(Ojet);
  }
  return OtherJets;
}

//Create a TLorentzVector of containing all the Higgs sisters
vector<TLorentzVector> Sis(Float_t Sis_pt[3], Float_t Sis_eta[3], Float_t Sis_phi[3], Float_t Sis_mass[3]){
  vector<TLorentzVector> SIS;
  for(int i = 1; i < 3; ++i){//Start at 1 since 0 entrie is always the Z bosons
    TLorentzVector Sis;
    Sis.SetPtEtaPhiM( Sis_pt[i], Sis_eta[i], Sis_phi[i], Sis_mass[i]);
    SIS.push_back(Sis);
  }
  return SIS;
}

int foundISR(double V_pt, double V_eta, double V_phi, double V_mass, double H_pt, double H_eta, double H_phi, double H_mass, vector<TLorentzVector> O_Jets, double PhiCut, double VHPtCut){
  //_*_*_*_*_*_*_*_*
  //Find the ISR jet 
  //_*_*_*_*_*_*_*_*
  //Build the V, H, V+H vector
  TLorentzVector V, H,VH, VHj;
  V.SetPtEtaPhiM(V_pt,V_eta,V_phi,V_mass);
  H.SetPtEtaPhiM(H_pt,H_eta,H_phi,H_mass);
  VH = V+H;
  //Apply VHPt Cut
  if(VH.Pt() < VHPtCut){return 0;}
  //Passes VHPt cut
  double maxpt = 0;
  int ISRidx = -1;
  //Apply phi cut and keep ISR candiate only. Choose the ISR candidate having the higest Pt
  for(unsigned int i = 0; i < O_Jets.size(); ++i){
    if(abs(O_Jets[i].DeltaPhi(VH)) < TMath::Pi() - PhiCut) continue;
    if(O_Jets[i].Pt() < maxpt) continue;
    maxpt = O_Jets[i].Pt();
    ISRidx = i;
  }
  //No ISR Jets found
  if(ISRidx == -1){return 0;}
  else{return 1;}
}

double VHj_Pt(double V_pt, double V_eta, double V_phi, double V_mass, double H_pt, double H_eta, double H_phi, double H_mass, vector<TLorentzVector> O_Jets, double PhiCut, double VHPtCut, bool keep = true){
  //_*_*_*_*_*_*_*_*
  //Find the ISR jet 
  //_*_*_*_*_*_*_*_*
  //Build the V, H, V+H vector
  TLorentzVector V, H,VH, VHj;
  V.SetPtEtaPhiM(V_pt,V_eta,V_phi,V_mass);
  H.SetPtEtaPhiM(H_pt,H_eta,H_phi,H_mass);

  VH = V+H;
  //Apply VHPt Cut
  if(VH.Pt() < VHPtCut && keep == false){
    return -1;
    //Passes VHPt cut
  }else if(VH.Pt() < VHPtCut && keep == true){
    return VH.Pt();
  }else{
    double maxpt = 0;
    int ISRidx = -1;
    //Apply phi cut and keep ISR candiate only. Choose the ISR candidate having the higest Pt
    for(unsigned int i = 0; i < O_Jets.size(); ++i){
      if(abs(O_Jets[i].DeltaPhi(VH)) < TMath::Pi() - PhiCut) continue;
      if(O_Jets[i].Pt() < maxpt) continue;
      maxpt = O_Jets[i].Pt();
      ISRidx = i;
    }
    //No ISR Jets found
    if(ISRidx == -1 && keep == true) return VH.Pt();
    else if(ISRidx == -1 && keep == false) return -1;
    else{
    VHj = VH + O_Jets[ISRidx];
    return VHj.Pt();
    }
  }
}

double PurSisISR(double V_pt, double V_eta, double V_phi, double V_mass, double H_pt, double H_eta, double H_phi, double H_mass, vector<TLorentzVector> O_Jets, vector<TLorentzVector> Sis, double PhiCut, double VHPtCut){
  //_*_*_*_*_*_*_*_*
  //Find the ISR jet 
  //_*_*_*_*_*_*_*_*
  //Returns the efficiency for a ISR-tagged jet to be matched to a syster jet
  TLorentzVector V, H,VH, VHj;
  V.SetPtEtaPhiM(V_pt,V_eta,V_phi,V_mass);
  H.SetPtEtaPhiM(H_pt,H_eta,H_phi,H_mass);
  VH = V+H;
  //Apply VHPt Cut
  if(VH.Pt() < VHPtCut){
    return 0;
    //Passes VHPt cut
  }else{
    double maxpt = 0;
    int ISRidx = -1;
    //Apply phi cut and keep ISR candiate only. Choose the ISR candidate having the higest Pt
    for(unsigned int i = 0; i < O_Jets.size(); ++i){
      if( abs(O_Jets[i].DeltaPhi(VH)) < TMath::Pi() - PhiCut ) continue;
      if( O_Jets[i].Pt() < maxpt ) continue;
      maxpt = O_Jets[i].Pt();
      ISRidx = i;
    }
    if(ISRidx == -1) {return 0;}
    else{
      double dR = 99999;
      for(unsigned int i = 0; i < Sis.size(); ++i){
	//if(Sis[i].Pt() == 0 && Sis[i].Eta() == 0 && Sis[i].Phi() == 0) continue;
	if(Sis[i].DeltaR(O_Jets[ISRidx]) > dR) continue;
	dR = Sis[i].DeltaR(O_Jets[ISRidx]);
      }
      if(dR < 0.3){
	return 1;
      }else{
	return 0;
      }
    }
  }
}

//_*_*
//Main
//_*_*

void VHF_Pt(){

  //setTDRStyle();
  //gStyle->SetPaintTextFormat("4.2f");
  //gStyle->SetOptStat(0);


  //_*_*_*_*_*
  //Read Input
  //_*_*_*_*_*

  //TString _sample = "ZH_HToBB_powheg_pythia";
  //TString _sample = "ZH_HToBB_amcanlo_pythia";
  //TString _sample = "ggZH_powheg_pythia";
  //TString _sample = "ttjets_amcanlo_pythia";
  //TString _sample = "ttjets_madgraph_pythia";


  //ZHbb
  //TString _f_in ="dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/ethz-higgs/run2/V12/VHBB_HEPPY_V12_ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root";
  //TString _f_in ="dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/ethz-higgs/run2/V12/VHBB_HEPPY_V12_ZH_HToBB_ZToLL_M125_13TeV_amcatnloFXFX_madspin_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root";
  //ggZH
  //TString _f_in ="dcap://t3se01.psi.ch:22125/pnfs/psi.ch/cms/trivcat/store/t3groups/ethz-higgs/run2/V12/VHBB_HEPPY_V12_ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root";
  //ttH
  //TString _f_in ="dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/ethz-higgs/run2/V12/VHBB_HEPPY_V12_TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root";
  //TString _f_in ="dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/ethz-higgs/run2/V12/VHBB_HEPPY_V12_TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2.root";


  TString _f_out ="";
  TFile* f = TFile::Open(_f_in);
  TTree* t = (TTree*) f->Get("tree");

  //_*_*_*_*_*_*_*_*_*
  //ISR-tag Parameters
  //_*_*_*_*_*_*_*_*_*

  double _PhiCut[16] = { 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2., 2.2, 2.4, 2.6, 2.8, 3., 3.2};
  double _VHPtCut[9] = {10, 20, 30, 40, 50, 60, 80, 90, 100};
  bool keep = true;

  vector<double> PhiCut(_PhiCut, _PhiCut+16);
  vector<double> VHPtCut(_VHPtCut, _VHPtCut+9);
  vector<vector<TH1D*> > hist;
  vector<vector<TCanvas*> > c;
  TCanvas* cVHj = new TCanvas("cVHj","cVHj");
  TCanvas* cpur = new TCanvas("cpur","cpur");
  TCanvas* ceff = new TCanvas("ceff","ceff");
  TCanvas* ceffxpur = new TCanvas("ceffxpur","ceffxpur");

  vector<vector<double> > VHj;//VHj_Pt. To be computed in each event
  vector<vector<double> > pur;//Sister-ISR efficiency. To be computed at each event
  vector<vector<Int_t> > nbinentries;//#entries per PhixPt bins
  vector<vector<Int_t> > nisrtag;//#ISR jets found per PhixPt bins
  vector<vector<Int_t> > isreff;//#efficiency to be ISR tagged
  vector<vector<Int_t> > noISR;//count the # of times no ISR has been found

  TH2D* hVHj = new TH2D("hVHj", "h_VHj", 15, _PhiCut, 8, _VHPtCut);
  TH2D* hpur = new TH2D("hpur", "hpur",  15, _PhiCut, 8, _VHPtCut);
  TH2D* heff = new TH2D("heff", "heff",  15, _PhiCut, 8, _VHPtCut);
  TH2D* heffxpur = new TH2D("heffxpur", "heffxpur",  15, _PhiCut, 8, _VHPtCut);

  //Simple h_VH histogram without the ISR jet 
  TH1D* h_VH = new TH1D("h_VH","h_VH",200,0,200);

  //_*_*_*_*_*_*_*_*_*_*_*_*_*
  //Prepar all the histograms
  //_*_*_*_*_*_*_*_*_*_*_*_*_*

  for(unsigned int i = 0; i < PhiCut.size(); ++i){

    vector<TH1D*>  _hist;
    vector<TCanvas*>  _c;
    vector<double> _VHj;
    vector<double> _pur;
    vector<Int_t> _nbinentries;
    vector<Int_t> _nisrtag;
    vector<Int_t> _isreff;
    vector<Int_t> _noISR;

    for(unsigned int k = 0; k < VHPtCut.size(); ++k){

      TH1D* h = new TH1D(Form("h_phi%i_Pt%i",i,k),Form("h_phi%i_Pt%i",i,k),200, 0, 200);
      _hist.push_back(h);
      TCanvas* c1 = new TCanvas(Form("c_phi%i_Pt%i",i,k),Form("c_phi%i_Pt%i",i,k));
      _c.push_back(c1);

      _VHj.push_back(0);
      _pur.push_back(0);
      _nbinentries.push_back(0);
      _nisrtag.push_back(0);
      _isreff.push_back(0);
      _noISR.push_back(0);
    }		

    hist.push_back(_hist);
    c.push_back(_c);
    VHj.push_back(_VHj);
    pur.push_back(_pur);
    nbinentries.push_back(_nbinentries);
    nisrtag.push_back(_nisrtag);
    isreff.push_back(_isreff);
    noISR.push_back(_noISR);

  }

  //_*_*_*_*_*_*_*_*_*_*
  //Get Branch Variables
  //_*_*_*_*_*_*_*_*_*_*

  Float_t Jet_pt[15];
  Float_t Jet_eta[15];
  Float_t Jet_phi[15];
  Float_t Jet_mass[15];
  Int_t Jet_puId[15];
  Int_t Jet_id[15];
  Int_t Jet_aJCidx[8];
  Int_t Jet_hJCidx[2];
  Float_t V_pt;
  Float_t V_eta;
  Float_t V_phi;
  Float_t V_mass;
  Float_t H_pt;
  Float_t H_eta;
  Float_t H_phi;
  Float_t H_mass;
  Float_t Sis_pt[3];
  Float_t Sis_eta[3];
  Float_t Sis_phi[3];
  Float_t Sis_mass[3];
  Float_t weight;

  t->SetBranchAddress("Jet_pt", &Jet_pt);
  t->SetBranchAddress("Jet_eta", &Jet_eta);
  t->SetBranchAddress("Jet_phi", &Jet_phi);
  t->SetBranchAddress("Jet_mass", &Jet_mass);
  t->SetBranchAddress("Jet_puId", &Jet_puId);
  t->SetBranchAddress("Jet_id", &Jet_id);
  t->SetBranchAddress("aJCidx", &Jet_aJCidx);
  t->SetBranchAddress("hJCidx", &Jet_hJCidx);
  t->SetBranchAddress("V_pt", &V_pt);
  t->SetBranchAddress("V_eta", &V_eta);
  t->SetBranchAddress("V_phi", &V_phi);
  t->SetBranchAddress("V_mass", &V_mass);
  t->SetBranchAddress("H_pt", &H_pt);
  t->SetBranchAddress("H_eta", &H_eta);
  t->SetBranchAddress("H_phi", &H_phi);
  t->SetBranchAddress("H_mass", &H_mass);
  t->SetBranchAddress("GenHiggsSisters_pt", &Sis_pt);
  t->SetBranchAddress("GenHiggsSisters_eta", &Sis_eta);
  t->SetBranchAddress("GenHiggsSisters_phi", &Sis_phi);
  t->SetBranchAddress("GenHiggsSisters_mass", &Sis_mass);
  t->SetBranchAddress("genWeight", &weight);

  //_*_*_*_*_*_*_*_*
  //Perform the loop
  //_*_*_*_*_*_*_*_*

  // double nentries = t->GetEntries();
  double nentries = 1e5;
  for(Int_t i = 0; i < nentries; ++i){
    if(i%10000==0) cout << "event " << i << "/" << nentries << endl;
    t->GetEntry(i);
    //Build the V+H to cross-check
    TLorentzVector V, H, VH;
    V.SetPtEtaPhiM(V_pt,V_eta,V_phi,V_mass);
    H.SetPtEtaPhiM(H_pt,H_eta,H_phi,H_mass);
    VH = V+H;
    if(weight < 0){weight = -1;}
    else if(weight > 0){weight = 1;}
    //weight = 1;
    if(V_pt > 100){
      for(unsigned int k = 0; k < PhiCut.size(); ++k){
	for(unsigned int l = 0; l < VHPtCut.size(); ++l){
	  //Count n events
	  nbinentries[k][l] += weight;
	  //Count #ISR tags
	  nisrtag[k][l] +=  weight*foundISR( V_pt,  V_eta,  V_phi,  V_mass,  H_pt,  H_eta,  H_phi,  H_mass, OtherJets( Jet_pt,  Jet_eta,  Jet_phi,  Jet_mass, Jet_puId, Jet_id, Jet_aJCidx, Jet_hJCidx),  PhiCut[k],  VHPtCut[l]);
	  isreff[k][l] = nisrtag[k][l];
	  //VHj minimisation
	  double VHj_add = VHj_Pt(V_pt, V_eta, V_phi, V_mass, H_pt, H_eta, H_phi, H_mass, OtherJets( Jet_pt,  Jet_eta,  Jet_phi,  Jet_mass, Jet_puId, Jet_id, Jet_aJCidx, Jet_hJCidx), PhiCut[k], VHPtCut[l], keep);
	  hist[k][l]->Fill(weight*VHj_add);
	  VHj[k][l]+= weight*VHj_add; 
	  //Sister optimisation
	  pur[k][l] +=  weight*PurSisISR(V_pt, V_eta, V_phi, V_mass, H_pt, H_eta, H_phi, H_mass, OtherJets( Jet_pt,  Jet_eta,  Jet_phi,  Jet_mass, Jet_puId, Jet_id, Jet_aJCidx, Jet_hJCidx), Sis(Sis_pt, Sis_eta, Sis_phi, Sis_mass), PhiCut[k], VHPtCut[l]);
	  //Fill VH histogram
	  h_VH->Fill(VH.Pt());
	}
      }
    }
  }

  //_*_*_*_*_*_*_*_
  //Save the histos
  //_*_*_*_*_*_*_*_
  h_VH->Scale(1./h_VH->Integral(h_VH->FindBin(1.5),h_VH->FindBin(199.5)));
  TFile *fout = new TFile("results"+_sample+".root","RECREATE");
  for(unsigned int k = 0; k < PhiCut.size(); ++k){
    for(unsigned int l = 0; l < VHPtCut.size(); ++l){
      //compute isreff
      hist[k][l]->Scale(1./hist[k][l]->Integral(hist[k][l]->FindBin(0.5),hist[k][l]->FindBin(199.5)));
      c[k][l]->cd();
      hist[k][l]->SetLineColor(2);
      hist[k][l]->Draw();
      h_VH->Draw("same");
      c[k][l]->Write();
      //cout<<"The VHj_Pt mean for PhiCut: "<<k<<" and VHPtCut "<<l<<" is "<<VHj[k][l]/nbinentries[k][l]<<endl;
      //cout<<"The Sister-ISR efficiency for PhiCut: "<<k<<" and VHPtCut "<<l<<" is "<<eff[k][l]/nisrtag[k][l]<<endl;
      //cout<<"The efficiency for PhiCut: "<<k<<" and VHPtCut "<<l<<" is "<<nisrtag[k][l]/nbinentries[k][l]<<endl;
    }
  }
  for(unsigned int k = 0; k < 15; ++k){
    for(unsigned int l = 0; l < 8; ++l){
      ceff->cd();
      heff->Fill((PhiCut[k]+PhiCut[k+1])/2., (VHPtCut[l]+VHPtCut[l+1])/2., isreff[k][l]/(double)nbinentries[k][l]);
      heff->SetTitle("ISR-finder efficiency");
      heff->GetXaxis()->SetTitle("#alpha");
      heff->GetXaxis()->SetLabelSize(20);
      heff->GetXaxis()->SetLabelFont(43);
      heff->GetXaxis()->SetTitleFont(63);
      heff->GetXaxis()->SetTitleSize(20);
      heff->GetYaxis()->SetTitle("P_{T}(VH) Cut");
      heff->GetYaxis()->SetLabelSize(20);
      heff->GetYaxis()->SetLabelFont(43);
      heff->GetYaxis()->SetTitleFont(63);
      heff->GetYaxis()->SetTitleSize(20);
      heff->Draw("colz text");
      cVHj->cd();
      hVHj->Fill((PhiCut[k]+PhiCut[k+1])/2., (VHPtCut[l]+VHPtCut[l+1])/2., VHj[k][l]/nbinentries[k][l]);
      hVHj->SetTitle("P_{T}(VH + ISR Jets)");
      hVHj->GetXaxis()->SetTitle("#alpha");
      hVHj->GetXaxis()->SetLabelSize(20);
      hVHj->GetXaxis()->SetLabelFont(43);
      hVHj->GetXaxis()->SetTitleFont(63);
      hVHj->GetXaxis()->SetTitleSize(20);
      hVHj->GetYaxis()->SetTitle("P_{t}(VH) Cut");
      hVHj->GetYaxis()->SetLabelSize(20);
      hVHj->GetYaxis()->SetLabelFont(43);
      hVHj->GetYaxis()->SetTitleFont(63);
      hVHj->GetYaxis()->SetTitleSize(20);
      hVHj->Draw("colz text");
      cpur->cd();
      hpur->Fill((PhiCut[k]+PhiCut[k+1])/2., (VHPtCut[l]+VHPtCut[l+1])/2., pur[k][l]/nisrtag[k][l]);
      hpur->SetTitle("ISR-finder purity");
      hpur->GetXaxis()->SetTitle("#alpha");
      hpur->GetXaxis()->SetLabelSize(20);
      hpur->GetXaxis()->SetLabelFont(43);
      hpur->GetXaxis()->SetTitleFont(63);
      hpur->GetXaxis()->SetTitleSize(20);
      hpur->GetYaxis()->SetTitle("P_{t}(VH) Cut");
      hpur->GetYaxis()->SetLabelSize(20);
      hpur->GetYaxis()->SetLabelFont(43);
      hpur->GetYaxis()->SetTitleFont(63);
      hpur->GetYaxis()->SetTitleSize(20);
      hpur->Draw("colz text");
      ceffxpur->cd();
      heffxpur->Fill((PhiCut[k]+PhiCut[k+1])/2., (VHPtCut[l]+VHPtCut[l+1])/2., ((double)nisrtag[k][l]*pur[k][l])/((double)nisrtag[k][l]*nbinentries[k][l]));
      heffxpur->SetTitle("ISR-finder purity x efficiency");
      heffxpur->GetXaxis()->SetTitle("#alpha");
      heffxpur->GetXaxis()->SetLabelSize(20);
      heffxpur->GetXaxis()->SetLabelFont(43);
      heffxpur->GetXaxis()->SetTitleFont(63);
      heffxpur->GetXaxis()->SetTitleSize(20);
      heffxpur->GetYaxis()->SetTitle("P_{t}(VH) Cut");
      heffxpur->GetYaxis()->SetLabelSize(20);
      heffxpur->GetYaxis()->SetLabelFont(43);
      heffxpur->GetYaxis()->SetTitleFont(63);
      heffxpur->GetYaxis()->SetTitleSize(20);
      heffxpur->Draw("colz text");
    }
  }

  gStyle->SetPaintTextFormat("4.2f");
  gStyle->SetOptStat(0);

  cVHj->Write();
  cVHj->SaveAs("optimisation/VHj"+_sample+".pdf");
  cpur->Write();
  cpur->SaveAs("optimisation/pur"+_sample+".pdf");
  ceff->Write();
  ceff->SaveAs("optimisation/eff"+_sample+".pdf");
  ceffxpur->Write();
  ceffxpur->SaveAs("optimisation/effxpur"+_sample+".pdf");
  fout->Write();
  fout->Close();
}
