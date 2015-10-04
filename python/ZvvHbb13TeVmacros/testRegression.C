{
    TFile *_file0 = TFile::Open("../env/syst/ZvvHighPt_V12_ZH_HToBB_ZToNuNu_M125_13TeV_amcatnloFXFX_madspin_pythia8_mini.root")
    gStyle->SetOptStat(0);

    tree->Draw("HNoReg.mass>>BeforeReg(100,50,250)","Sum$(Jet_mcMatchId[hJCidx]==25)==2");
    BeforeReg->SetLineWidth(2);
    BeforeReg->SetLineColor(kBlack);
    TF1* fit1 = new TF1("fit1","gaus");
    fit1->SetLineColor(kBlack);
    BeforeReg->Fit(fit1,"","",100,140);

    tree->Draw("H.mass>>AfterReg","Sum$(Jet_mcMatchId[hJCidx]==25)==2","same");
    AfterReg->SetLineWidth(2);
    AfterReg->SetLineColor(kRed);
    TF1* fit2 = new TF1("fit2","gaus");
    fit2->SetLineColor(kRed);
    AfterReg->Fit(fit2,"","",100,150);
    
   TLegend* leg = new TLegend(0.52,0.7,0.9,0.9);
   leg->AddEntry(BeforeReg,"Before regression","l");
   leg->AddEntry(AfterReg,"After regression","l");
   leg->Draw();
}
