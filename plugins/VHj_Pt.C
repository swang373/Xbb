#include <math.h>
#include <vector>

#include "TLorentzVector.h"

double VHj_Pt(double V_pt, double V_eta, double V_phi, double V_mass,
              double H_pt, double H_eta, double H_phi, double H_mass,
              vector<TLorentzVector> O_Jets, double PhiCut, double VHPtCut) {

  // Build the V, H, and V+H vectors.
  TLorentzVector V, H, VH, VHj;
  V.SetPtEtaPhiM(V_pt, V_eta, V_phi, V_mass);
  H.SetPtEtaPhiM(H_pt, H_eta, H_phi, H_mass);
  VH = V + H;

  // Apply VHPt cut.
  if (VH.Pt() < VHPtCut) return -1;

  double maxpt = 0;
  int ISRidx = -1;

  // Apply phi cut and keep ISR candiate only.
  for (unsigned int i = 0; i < O_Jets.size(); ++i) {
    if ((abs(O_Jets[i].Phi() - VH.Phi()) < M_PI - PhiCut) || O_Jets[i].Pt() < maxpt) continue;
    maxpt = O_Jets[i].Pt();
    ISRidx = i;
  }

  // No ISR jets found.
  if (ISRidx == -1) return -1;

  VHj = VH + O_Jets[ISRidx];

  return VHj.Pt();
}

