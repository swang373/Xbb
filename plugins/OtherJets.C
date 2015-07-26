#include "TLorentzVector.h"

#include <vector>

//vector<TLorentzVector> OtherJets(Float_t Jet_pt[15], Float_t Jet_eta[15], Float_t Jet_phi[15], Float_t Jet_mass[15], Int_t Jet_puId[15], Int_t Jet_id[15], Int_t aJCidx[8], Int_t hJCidx[2]){
//double OtherJets(Float_t Jet_pt[15], Float_t Jet_eta[15], Float_t Jet_phi[15], Float_t Jet_mass[15], Int_t Jet_puId[15], Int_t Jet_id[15], Int_t aJCidx[8], Int_t hJCidx[2]){
Float_t OtherJets(Float_t Jet_pt[]){

  //Create a TLorentzVector of the jets other than the two b-jets. 

  //vector<TLorentzVector> OtherJets;

  /*for(int i = 0; i < 15; ++i){

    if(Jet_pt[i]>30 && abs(Jet_eta[i])<4.5 && Jet_puId[i]>0 && Jet_id[i]>0 && aJCidx[i] != (hJCidx[0]) && (aJCidx[i] != (hJCidx[1]))){

      TLorentzVector Ojet;
      Ojet.SetPtEtaPhiM( Jet_pt[i], Jet_eta[i], Jet_phi[i], Jet_mass[i]);
      OtherJets.push_back(Ojet);

    }else{}


  }*/

  //return OtherJets;
  return Jet_pt[0];

}

