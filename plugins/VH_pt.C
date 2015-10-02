#include "TLorentzVector.h"

double VH_pt(double V_pt,double V_eta,double V_phi,double V_mass, double H_pt,double H_eta,double H_phi,double H_mass){
  
  TLorentzVector V,H,VH;
  V.SetPtEtaPhiM(V_pt,V_eta,V_phi,V_mass);
  H.SetPtEtaPhiM(H_pt,H_eta,H_phi,H_mass);
  VH = V+H;
  return VH.Pt();
  
}

