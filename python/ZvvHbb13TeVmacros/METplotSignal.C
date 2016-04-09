{
    TChain* tree = new TChain("tree");
    tree->Add("../MCAndDataLinks/ZH_HToBB_ZToNuNu_M125_13TeV_amcatnloFXFX_madspin_pythia8/VHBB_HEPPY_V21_ZH_HToBB_ZToNuNu_M125_13TeV_amcatnloFXFX_madspin_Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160316_150722/0000/tree_*");
    tree->Draw("min(met_pt,mhtJet30) >> h1(100,90,290)","puWeight * sign(genWeight) * bTagWeight","ERR,goff");
    float total = h1->GetMaximum();
    h1->Scale(1./total);
    tree->Draw("min(met_pt,mhtJet30) >> h2(100,90,290)","puWeight * sign(genWeight) * bTagWeight * (HLT_BIT_HLT_PFMET90_PFMHT90_IDTight_v||HLT_BIT_HLT_PFMET170_NoiseCleaned_v)","ERR,goff");
    h2->Scale(1./total);

//    TCanvas* c1 = new TCanvas("");
    h1->SetLineWidth(2);
    h2->SetLineWidth(2);

    h2->SetLineColor(kRed);

//    c1->SetTitle("");
    h1->SetTitle("");
    h1->GetXaxis()->SetTitle("min(MET,MHT)");
    h1->GetYaxis()->SetTitle("A.U.");

    h1->Draw();
    h2->Draw("same");

    c1->SetGridx();
    c1->SetGridy();
    c1->SaveAs("METSignalPlot.png");
    c1->SaveAs("METSignalPlot.pdf");

}


