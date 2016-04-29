double HJetPt(double CSVj1, double Ptj1, double CSVj2, double Ptj2) {
  return (CSVj1 > CSVj2) ? Ptj1 : Ptj2;
}
