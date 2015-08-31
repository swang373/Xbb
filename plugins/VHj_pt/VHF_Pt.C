#include "TString.h"
#include "TBranch.h"
#include "TTree.h"
#include "TFile.h"
#include "TH1D.h"
#include "TLorentzVector.h"
#include "TCanvas.h"

#include <iostream>
#include <vector>

//_*_*_*
//Macros
//_*_*_*

vector<TLorentzVector> OtherJets(Float_t Jet_pt[15], Float_t Jet_eta[15], Float_t Jet_phi[15], Float_t Jet_mass[15], Int_t Jet_puId[15], Int_t Jet_id[15], Int_t aJCidx[8], Int_t hJCidx[2]){
  //Create a TLorentzVector of the jets other than the two Higgs candidate b-jets. 
  vector<TLorentzVector> OtherJets;
  for(int i = 0; i < 15; ++i){
    TLorentzVector Ojet;
    if(Jet_pt[i]>30 && abs(Jet_eta[i])<4.5 && Jet_puId[i]>0 && Jet_id[i]>0 && aJCidx[i] != (hJCidx[0]) && (aJCidx[i] != (hJCidx[1]))){
      Ojet.SetPtEtaPhiM( Jet_pt[i], Jet_eta[i], Jet_phi[i], Jet_mass[i]);
    }else{
      Ojet.SetPtEtaPhiM( 0, 0, 0, 0);
    }
    OtherJets.push_back(Ojet);
  }
  return OtherJets;
}

vector<TLorentzVector> Sis(Float_t Sis_pt[3], Float_t Sis_eta[3], Float_t Sis_phi[3], Float_t Sis_mass[3]){
  //Create a TLorentzVector of containing all the sisters
  vector<TLorentzVector> SIS;
  for(int i = 1; i < 3; ++i){//Start at 1 since 0 entrie is always Z bosons
    TLorentzVector Sis;
    Sis.SetPtEtaPhiM( Sis_pt[i], Sis_eta[i], Sis_phi[i], Sis_mass[i]);
    SIS.push_back(Sis);
  }
  return SIS;
}

double VHj_Pt(double V_pt, double V_eta, double V_phi, double V_mass, double H_pt, double H_eta, double H_phi, double H_mass, vector<TLorentzVector> O_Jets, double PhiCut, double VHPtCut, bool keep = false){

  //Calculates the VHj_Pt taking as parameter the Phi and Pt cut. If keep == false, -1 is returned when no V_pt value is found. Otherwise VH.Pt() without the ISR jet is returned
  //Build the V, H, V+H vector
  TLorentzVector V, H,VH, VHj;
  V.SetPtEtaPhiM(V_pt,V_eta,V_phi,V_mass);
  H.SetPtEtaPhiM(H_pt,H_eta,H_phi,H_mass);
  VH = V+H;
  //Apply VHPt Cut
  if(VH.Pt() < VHPtCut && keep == false){
    //cout<<"smaller1"<<endl;
    return -1;
    //Passes VHPt cut
  }else if(VH.Pt() < VHPtCut && keep == true){
    //cout<<"smaller1"<<endl;
    return VH.Pt();
  }else{
    double maxpt = 0;
    int ISRidx = -1;
    //Apply phi cut and keep ISR candiate only. Choose the ISR candidate having the higest Pt
    for(unsigned int i = 0; i < O_Jets.size(); ++i){
      if( abs(O_Jets[i].DeltaPhi(VH)) < TMath::Pi() - PhiCut ) continue;
      if( O_Jets[i].Pt() < maxpt ) continue;
      if( O_Jets[i].Pt() == 0 && O_Jets[i].Eta() == 0 && O_Jets[i].Phi() == 0) continue;//In case the jet haven't passed the "no Higgs candidtate" selection
      maxpt = O_Jets[i].Pt();
      ISRidx = i;
    }
    //No ISR Jets found
    if(ISRidx == -1 && keep == true) return VH.Pt();
    else if(ISRidx == -1 && keep == false) return -1;
    VHj = VH + O_Jets[ISRidx];
    return VHj.Pt();
  }
}

double EffSisISR(double V_pt, double V_eta, double V_phi, double V_mass, double H_pt, double H_eta, double H_phi, double H_mass, vector<TLorentzVector> O_Jets, vector<TLorentzVector> Sis, double PhiCut, double VHPtCut){
  //Returns the efficiency for a ISR-tagged jet to be matched to a syster jet
  TLorentzVector V, H,VH, VHj;
  V.SetPtEtaPhiM(V_pt,V_eta,V_phi,V_mass);
  H.SetPtEtaPhiM(H_pt,H_eta,H_phi,H_mass);
  VH = V+H;
  //Apply VHPt Cut
  if(VH.Pt() < VHPtCut){
    //cout<<"smaller2"<<endl;
    return -1;
    //Passes VHPt cut
  }else{
    double maxpt = 0;
    int ISRidx = -1;
    //Apply phi cut and keep ISR candiate only. Choose the ISR candidate having the higest Pt
    for(unsigned int i = 0; i < O_Jets.size(); ++i){
      if( abs(O_Jets[i].DeltaPhi(VH)) < TMath::Pi() - PhiCut ) continue;
      if( O_Jets[i].Pt() < maxpt ) continue;
      if( O_Jets[i].Pt() == 0 && O_Jets[i].Eta() == 0 && O_Jets[i].Phi() == 0) continue;//In case the jet haven't passed the "no Higgs candidtate" selection
      maxpt = O_Jets[i].Pt();
      ISRidx = i;
    }
    //cout<<"ISRidx is"<<ISRidx<<endl;
    if(ISRidx == -1) {return -1;}
    else{
      double dR = 99999;
	for(unsigned int i = 0; i < Sis.size(); ++i){
	  if(Sis[i].Pt() == 0 && Sis[i].Eta() == 0 && Sis[i].Phi() == 0) continue;
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
  double _VHPtCut[10] = { 0, 10, 20, 30, 40, 50, 60, 80, 90, 100};
  
  vector<double> PhiCut(_PhiCut, _PhiCut+14);
  vector<double> VHPtCut(_VHPtCut, _VHPtCut+10);
  vector<vector<TH1D*> > hist;
  vector<vector<TCanvas*> > c;

  vector<vector<double> > VHj;//VHj_Pt. To be computed in each event
  vector<vector<double> > eff;//Sister-ISR efficiency. To be computed at each event
  vector<vector<Int_t> > nsuccess;//count the # of times vhj_pt is filler to a > 0 value
  vector<vector<Int_t> > nsuccess2;
  vector<vector<Int_t> > noISR;//count the # of times no ISR has been found

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
    vector<Int_t> _nsuccess;
    vector<Int_t> _nsuccess2;
    vector<Int_t> _noISR;

    for(unsigned int k = 0; k < VHPtCut.size(); ++k){

      TH1D* h = new TH1D(Form("h_phi%i_Pt%i",i,k),Form("h_phi%i_Pt%i",i,k),200, 0, 200);
      _hist.push_back(h);
      TCanvas* c1 = new TCanvas(Form("c_phi%i_Pt%i",i,k),Form("c_phi%i_Pt%i",i,k));
      _c.push_back(c1);

      _VHj.push_back(0);
      _eff.push_back(0);
      _nsuccess.push_back(0);
      _nsuccess2.push_back(0);
      _noISR.push_back(0);
    }		

    hist.push_back(_hist);
    c.push_back(_c);
    VHj.push_back(_VHj);
    eff.push_back(_eff);
    nsuccess.push_back(_nsuccess);
    nsuccess2.push_back(_nsuccess2);
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
  double nentries = 1e4;
  for(Int_t i = 0; i < nentries; ++i){
    if(i%10000==0) cout << "event " << i << "/" << nentries << endl;
    t->GetEntry(i);
    //Build the V+H to cross-check
    TLorentzVector V, H, VH;
    V.SetPtEtaPhiM(V_pt,V_eta,V_phi,V_mass);
    H.SetPtEtaPhiM(H_pt,H_eta,H_phi,H_mass);
    VH = V+H;
    if(V_pt > 100) h_VH->Fill(VH.Pt());
    for(unsigned int k = 0; k < PhiCut.size(); ++k){
      for(unsigned int l = 0; l < VHPtCut.size(); ++l){
	if(V_pt > 100){
	//VHj minimisation
	double VHj_add = VHj_Pt(V_pt, V_eta, V_phi, V_mass, H_pt, H_eta, H_phi, H_mass, OtherJets( Jet_pt,  Jet_eta,  Jet_phi,  Jet_mass, Jet_puId, Jet_id, Jet_aJCidx, Jet_hJCidx), PhiCut[k], VHPtCut[l], true);
	  if(VHj_add > 0){ 
	    hist[k][l]->Fill(VHj_add);
	    VHj[k][l]+= VHj_add; 
	    ++nsuccess[k][l];
	  }
	  else{ ++noISR[k][l];}
	  //Sister optimisation
	  double num =  EffSisISR(V_pt, V_eta, V_phi, V_mass, H_pt, H_eta, H_phi, H_mass, OtherJets( Jet_pt,  Jet_eta,  Jet_phi,  Jet_mass, Jet_puId, Jet_id, Jet_aJCidx, Jet_hJCidx), Sis(Sis_pt, Sis_eta, Sis_phi, Sis_mass), PhiCut[k], VHPtCut[l]);
	  //cout<<"num is"<<num<<endl;
	  if(num != -1) {
	    ++nsuccess2[k][l];
	    eff[k][l] += num;
	  }
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
      hist[k][l]->Scale(1./hist[k][l]->Integral(hist[k][l]->FindBin(0.5),hist[k][l]->FindBin(199.5)));
      c[k][l]->cd();
      hist[k][l]->SetLineColor(2);
      hist[k][l]->Draw();
      h_VH->Draw("same");
      // c[k][l]->SaveAs(Form("ISR_phi%i_Pt%i.pdf",k,l));
      c[k][l]->Write();
      cout<<"(keep) The VHj_Pt mean for PhiCut: "<<k<<" and VHPtCut "<<l<<" is "<<VHj[k][l]/nsuccess[k][l]<<endl;
      cout<<"The Sister-ISR efficiency for PhiCut: "<<k<<" and VHPtCut "<<l<<" is "<<eff[k][l]/nsuccess2[k][l]<<endl;
    }
  }
  fout->Write();
  fout->Close();
}
