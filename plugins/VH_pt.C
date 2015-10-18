#include "TLorentzVector.h"

double VH_pt(Float_t V_pt,Float_t V_eta,Float_t V_phi,Float_t V_mass,Float_t H_pt,Float_t H_eta,Float_t H_phi,Float_t H_mass){
  
  TLorentzVector V,H,VH;
  V.SetPtEtaPhiM(V_pt,V_eta,V_phi,V_mass);
  H.SetPtEtaPhiM(H_pt,H_eta,H_phi,H_mass);
  VH = V+H;
  return VH.Pt();
  
}

