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
      OtherJets.push_back(Ojet);

    }else{
      
      Ojet.SetPtEtaPhiM( 0, 0, 0, 0);
    }


  }

  return OtherJets;
}

double VHj_Pt(double V_pt, double V_eta, double V_phi, double V_mass, double H_pt, double H_eta, double H_phi, double H_mass, vector<TLorentzVector> O_Jets, double PhiCut, double VHPtCut, bool keep = false){

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

    //Apply phi cut and keep ISR candiate only
    for(unsigned int i = 0; i < O_Jets.size(); ++i){

      // if( abs(O_Jets[i].Phi() - VH.Phi())  < M_PI - PhiCut ) continue;
      if( abs(O_Jets[i].DeltaPhi(VH)) < TMath::Pi() - PhiCut ) continue;
      if( O_Jets[i].Pt() < maxpt ) continue;
      if( O_Jets[i].Pt() == 0 && O_Jets[i].Eta() == 0 && O_Jets[i].Phi() == 0 && O_Jets[i].Phi()) continue;
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

//_*_*
//Main
//_*_*

void VHF_Pt(){
  
  //_*_*_*_*_*
  //Read Input
  //_*_*_*_*_*

  // TString _f_in ="VHBB_HEPPY_U12_ZH_HToBB_ZToLL_M125_13TeV_amcatnloFXFX_madspin_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root";
  TString _f_in ="dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/t3groups/ethz-higgs/run2/V12/VHBB_HEPPY_V12_ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8__RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1.root";
  TString _f_out ="";
  TFile* f = TFile::Open(_f_in);
  TTree* t = (TTree*) f->Get("tree");

  //_*_*_*_*_*_*_*_*_*
  //ISR-tag Parameters
  //_*_*_*_*_*_*_*_*_*
  
  double _PhiCut[11] = { 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5};
  // double _VHPtCut[7] = { 0, 5, 10, 15, 20, 25, 30};
  double _VHPtCut[10] = { 0, 10, 20, 30, 40, 50, 60, 80, 90, 100};
  
  vector<double> PhiCut(_PhiCut, _PhiCut+11);
  vector<double> VHPtCut(_VHPtCut, _VHPtCut+10);
  vector<vector<TH1D*> > hist;
  vector<vector<TCanvas*> > c;

  vector<vector<double> > VHj;//VHj_Pt. To be computed in each event
  vector<vector<Int_t> > nsuccess;//count the # of times vhj_pt is filler to a > 0 value
  vector<vector<Int_t> > noISR;//count the # of times no ISR has been found

  TH1D* h_VH = new TH1D("h_VH","h_VH",200,0,200);

  for(unsigned int i = 0; i < PhiCut.size(); ++i){

    vector<TH1D*>  _hist;
    vector<TCanvas*>  _c;
    vector<double> _VHj;
    vector<Int_t> _nsuccess;
    vector<Int_t> _noISR;

    for(unsigned int k = 0; k < VHPtCut.size(); ++k){

      TH1D* h = new TH1D(Form("h_phi%i_Pt%i",i,k),Form("h_phi%i_Pt%i",i,k),200, 0, 200);
      _hist.push_back(h);
      TCanvas* c1 = new TCanvas(Form("c_phi%i_Pt%i",i,k),Form("c_phi%i_Pt%i",i,k));
      _c.push_back(c1);

      _VHj.push_back(0);
      _nsuccess.push_back(0);
      _noISR.push_back(0);
    }		

    hist.push_back(_hist);
    c.push_back(_c);
    VHj.push_back(_VHj);
    nsuccess.push_back(_nsuccess);
    noISR.push_back(_noISR);

  }

  //_*_*_*_*_*
  //Histograms
  //_*_*_*_*_*
  
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

    if(V_pt > 100) h_VH->Fill(VH.Pt());

    for(unsigned int k = 0; k < PhiCut.size(); ++k){

      for(unsigned int l = 0; l < VHPtCut.size(); ++l){

        double VHj_add = VHj_Pt( V_pt, V_eta, V_phi, V_mass, H_pt, H_eta, H_phi, H_mass, OtherJets( Jet_pt,  Jet_eta,  Jet_phi,  Jet_mass, Jet_puId, Jet_id, Jet_aJCidx, Jet_hJCidx), PhiCut[k], VHPtCut[l], true);
	

        if(V_pt > 100){
          if(VHj_add > 0){ 
            hist[k][l]->Fill(VHj_add);
	    VHj[k][l]+= VHj_add; 
	    ++nsuccess[k][l];
	  }
          else{ ++noISR[k][l];}
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

    }
  }
  fout->Write();
  fout->Close();

}
