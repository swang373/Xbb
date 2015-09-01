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

  //_*_*_*_*_*
  //Read Input
  //_*_*_*_*_*

  TString _f_in ="dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/ethz-higgs/run2/V12/VHBB_HEPPY_V12_ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root";
  TString _f_out ="";
  TFile* f = TFile::Open(_f_in);
  TTree* t = (TTree*) f->Get("tree");

  //_*_*_*_*_*_*_*_*_*
  //ISR-tag Parameters
  //_*_*_*_*_*_*_*_*_*

  double _PhiCut[14] = { 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5};
  double _VHPtCut[9] = {10, 20, 30, 40, 50, 60, 80, 90, 100};
  double _PhiCut2[15] = {0, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 1.05, 1.15, 1.25, 1.35, 1.45, 1.55};
  double _VHPtCut2[10] = { 0, 15, 25, 35, 45, 55, 65, 85, 95, 105};
  bool keep = true;

  vector<double> PhiCut(_PhiCut, _PhiCut+14);
  vector<double> VHPtCut(_VHPtCut, _VHPtCut+9);
  vector<vector<TH1D*> > hist;
  vector<vector<TCanvas*> > c;
  TCanvas* cVHj = new TCanvas("cVHj","cVHj");
  TCanvas* cpur = new TCanvas("cpur","cpur");
  TCanvas* ceff = new TCanvas("ceff","ceff");
  TCanvas* ceffxpur = new TCanvas("ceffxpur","ceffxpur");

  vector<vector<double> > VHj;//VHj_Pt. To be computed in each event
  vector<vector<double> > eff;//Sister-ISR efficiency. To be computed at each event
  vector<vector<Int_t> > nbinentries;//#entries per PhixPt bins
  vector<vector<Int_t> > nisrtag;//#ISR jets found per PhixPt bins
  vector<vector<Int_t> > isreff;//#efficiency to be ISR tagged
  vector<vector<Int_t> > noISR;//count the # of times no ISR has been found

  TH2D* hVHj = new TH2D("hVHj", "h_VHj", 14, _PhiCut2, 9, _VHPtCut2);
  TH2D* hpur = new TH2D("hpur", "hpur",  14, _PhiCut2, 9, _VHPtCut2);
  TH2D* heff = new TH2D("heff", "heff",  14, _PhiCut2, 9, _VHPtCut2);
  TH2D* heffxpur = new TH2D("heffxpur", "heffxpur",  14, _PhiCut2, 9, _VHPtCut2);

  //Simple h_VH histogram without the ISR jet 
  TH1D* h_VH = new TH1D("h_VH","h_VH",200,0,200);

  //_*_*_*_*_*_*_*_*_*_*_*_*_*
  //Prepar all the histograms
  //_*_*_*_*_*_*_*_*_*_*_*_*_*

  for(unsigned int i = 0; i < PhiCut.size(); ++i){

    vector<TH1D*>  _hist;
    vector<TCanvas*>  _c;
    vector<double> _VHj;
    vector<double> _eff;
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
      _eff.push_back(0);
      _nbinentries.push_back(0);
      _nisrtag.push_back(0);
      _isreff.push_back(0);
      _noISR.push_back(0);
    }		

    hist.push_back(_hist);
    c.push_back(_c);
    VHj.push_back(_VHj);
    eff.push_back(_eff);
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

  //_*_*_*_*_*_*_*_*
  //Perform the loop
  //_*_*_*_*_*_*_*_*

  // double nentries = t->GetEntries();
  double nentries = 1e3;
  for(Int_t i = 0; i < nentries; ++i){
    if(i%10000==0) cout << "event " << i << "/" << nentries << endl;
    t->GetEntry(i);
    //Build the V+H to cross-check
    TLorentzVector V, H, VH;
    V.SetPtEtaPhiM(V_pt,V_eta,V_phi,V_mass);
    H.SetPtEtaPhiM(H_pt,H_eta,H_phi,H_mass);
    VH = V+H;
    if(V_pt > 100){
      for(unsigned int k = 0; k < PhiCut.size(); ++k){
	for(unsigned int l = 0; l < VHPtCut.size(); ++l){
	  h_VH->Fill(VH.Pt());
	  //Count #ISR tags
	  nisrtag[k][l] +=  foundISR( V_pt,  V_eta,  V_phi,  V_mass,  H_pt,  H_eta,  H_phi,  H_mass, OtherJets( Jet_pt,  Jet_eta,  Jet_phi,  Jet_mass, Jet_puId, Jet_id, Jet_aJCidx, Jet_hJCidx),  PhiCut[k],  VHPtCut[l]);
	  ++nbinentries[k][l];
	  //Fill TH2D
	  isreff[k][l] = nisrtag[k][l]/nbinentries[k][l];
	    //VHj minimisation
	  double VHj_add = VHj_Pt(V_pt, V_eta, V_phi, V_mass, H_pt, H_eta, H_phi, H_mass, OtherJets( Jet_pt,  Jet_eta,  Jet_phi,  Jet_mass, Jet_puId, Jet_id, Jet_aJCidx, Jet_hJCidx), PhiCut[k], VHPtCut[l], keep);
	  //if(keep){ 
	  hist[k][l]->Fill(VHj_add);
	  VHj[k][l]+= VHj_add; 
	  //}else if(VHj_add != -1 && (!keep)){ 
	  //  hist[k][l]->Fill(VHj_add);
	  //  VHj[k][l]+= VHj_add; 
	  //  ++nbinentries[k][l];
	  //}else if(VHj_add == -1 && (!keep)){ ++noISR[k][l];}
	  //Sister optimisation
	  eff[k][l] +=  PurSisISR(V_pt, V_eta, V_phi, V_mass, H_pt, H_eta, H_phi, H_mass, OtherJets( Jet_pt,  Jet_eta,  Jet_phi,  Jet_mass, Jet_puId, Jet_id, Jet_aJCidx, Jet_hJCidx), Sis(Sis_pt, Sis_eta, Sis_phi, Sis_mass), PhiCut[k], VHPtCut[l]);
	}
      }
    }
  }



  //_*_*_*_*_*_*_*_
  //Save the histos
  //_*_*_*_*_*_*_*_
  h_VH->Scale(1./h_VH->Integral(h_VH->FindBin(1.5),h_VH->FindBin(199.5)));
  TFile *fout = new TFile("results_keep.root","RECREATE");
  for(unsigned int k = 0; k < PhiCut.size(); ++k){
    for(unsigned int l = 0; l < VHPtCut.size(); ++l){
      //compute isreff
      hist[k][l]->Scale(1./hist[k][l]->Integral(hist[k][l]->FindBin(0.5),hist[k][l]->FindBin(199.5)));
      c[k][l]->cd();
      hist[k][l]->SetLineColor(2);
      hist[k][l]->Draw();
      h_VH->Draw("same");
      // c[k][l]->SaveAs(Form("ISR_phi%i_Pt%i.pdf",k,l));
      c[k][l]->Write();
      //cout<<"The VHj_Pt mean for PhiCut: "<<k<<" and VHPtCut "<<l<<" is "<<VHj[k][l]/nbinentries[k][l]<<endl;
      //cout<<"The Sister-ISR efficiency for PhiCut: "<<k<<" and VHPtCut "<<l<<" is "<<eff[k][l]/nisrtag[k][l]<<endl;
      //cout<<"The efficiency for PhiCut: "<<k<<" and VHPtCut "<<l<<" is "<<nisrtag[k][l]/nbinentries[k][l]<<endl;
    }
  }
  for(unsigned int k = 0; k < 14; ++k){
    for(unsigned int l = 0; l < 9; ++l){
      ceff->cd();
      heff->Fill(PhiCut[k], VHPtCut[l], (double)nisrtag[k][l]/(double)nbinentries[k][l]);
      heff->Draw("colz text");
      //cout<<"Debug1blabla"<<endl;
      //cout<<"k is"<<k<<endl;
      //cout<<"l is"<<l<<endl;
      cVHj->cd();
      //cout<<"The x bin is"<<(PhiCut[k]+PhiCut[k+1])/2.0<<endl;
      hVHj->Fill(PhiCut[k], VHPtCut[l], VHj[k][l]/nbinentries[k][l]);
      hVHj->Draw("colz text");
      cpur->cd();
      hpur->Fill(PhiCut[k], VHPtCut[l], eff[k][l]/nisrtag[k][l]);
      hpur->Draw("colz text");
      ceffxpur->cd();
      heffxpur->Fill(PhiCut[k], VHPtCut[l], ((double)nisrtag[k][l]*eff[k][l])/((double)nisrtag[k][l]*nbinentries[k][l]));
      heffxpur->Draw("colz text");
    }
  }
  cVHj->Write();
  cpur->Write();
  ceff->Write();
  fout->Write();
  ceffxpur->Write();
  fout->Close();
}
