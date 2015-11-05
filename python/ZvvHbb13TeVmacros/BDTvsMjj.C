tree->Draw("H.mass >> bin0","MicheleBDTNoMjj.nominal>-.2 && MicheleBDTNoMjj.nominal<-0.3 && H.mass<500 &&  H.mass>90","NORM")
tree->Draw("H.mass >> bin1","MicheleBDTNoMjj.nominal>-.3 && MicheleBDTNoMjj.nominal<0. && H.mass<500 &&  H.mass>90","NORM")
tree->Draw("H.mass >> bin2","MicheleBDTNoMjj.nominal>0 && MicheleBDTNoMjj.nominal<1. && H.mass<500 &&  H.mass>90","NORM")

bin0->Draw()
bin1->Draw("same")
bin2->Draw("same")

---------------------------------------------

tree->Draw("ZvvBDT:HCSV_mass","","prof")

tree->Draw("ZvvBDTNoMjj:HCSV_mass","","prof,same")

----------------------------


tree->Draw("HCSV_mass >> Bin1(100,0,350)","-0.2<ZvvBDTNoMjj<0.2","NORM");
tree->Draw("HCSV_mass >> Bin2(100,0,350)","-0.2<ZvvBDTNoMjj<0.2","NORM");
tree->Draw("HCSV_mass >> Bin3(100,0,350)","-0.2<ZvvBDTNoMjj<0.2","NORM");

Bin1->SetLineColor(kBlack);
Bin1->SetLineWidth(2);

Bin2->SetLineColor(kBlue);
Bin2->SetLineWidth(2);

Bin3->SetLineColor(kRed);
Bin3->SetLineWidth(2);

Bin1->Draw();
Bin2->Draw("same");
Bin3->Draw("same");

c1->SaveAs("TTbarBins.png")

