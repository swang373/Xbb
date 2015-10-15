void Trigger_TurnOn(){
//gROOT->SetBatch();
//gStyle->SetPadGridX(1);
//gStyle->SetPadGridY(1);
//gStyle->SetLineWidth(2);
gStyle->SetOptStat(0);
gROOT->ForceStyle();
gStyle->SetOptStat(0000);
TCanvas* c1 = new TCanvas("c1","c1");


//L1 cut: Jet_pt[0]>92 && Jet_pt[1]>76 && Jet_pt[2]>64 && abs(Jet_eta)<3
//Calo cut: Jet_pt[0]>80 && Jet_pt[1]>65 && Jet_pt[2]>50 && Jet_pt[3]>15
//Calo CSV 0.74
//PF cut: Jet_pt[0]>92 && Jet_pt[1]>76 && Jet_pt[2]>64 && Jet_pt[3]>15
//PF CSV 0.78 e 0.58

//CaloCut: Mqq_eta>150 && Detaqq_eta>1.5
//PFCut 1-btag: Mqq_1b>460 && Detaqq_1b>4.1 && Dphibb_1b<1.6
//PFCut 2-btag: Mqq_2b>200 && Detaqq_2b>1.2

///////////////////////////////////////////

tree->Draw("HLT_BIT_HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v:Dphibb_1b >> h(8,0,3.2)","json && Detaqq_1b>4.2 && (HLT_BIT_HLT_PFHT750_4JetPt50_v||HLT_BIT_HLT_PFHT450_SixJet40_v||HLT_BIT_HLT_PFHT400_SixJet30_v||HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v||HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v||HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v)","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("#Delta #phi_{bb} ");
h->Draw("COLZ");
c1->SaveAs("data_Dphibb_1b.png");

tree->Draw("HLT_BIT_HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v:Detaqq_1b >> h(16,0,8)","json && Dphibb_1b<1.5 && (HLT_BIT_HLT_PFHT750_4JetPt50_v||HLT_BIT_HLT_PFHT450_SixJet40_v||HLT_BIT_HLT_PFHT400_SixJet30_v||HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v||HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v||HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v)","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("#Delta #eta_{qq} ");
h->Draw("COLZ");
c1->SaveAs("data_Detaqq_1b.png");


//////HLT_BIT_HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v
//PFCut 2-btag: Mqq_2b>200 && Detaqq_2b>1.2

tree->Draw("HLT_BIT_HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v:Detaqq_2b >> h(16,0,4)","json && Mqq_2b>220 && (HLT_BIT_HLT_PFHT750_4JetPt50_v||HLT_BIT_HLT_PFHT450_SixJet40_v||HLT_BIT_HLT_PFHT400_SixJet30_v||HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v||HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v||HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v)","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("#Delta #eta_{qq} ");
h->Draw("COLZ");
c1->SaveAs("data_Detaqq_2b.png");


tree->Draw("HLT_BIT_HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v:Mqq_2b >> h(25,0,500)","json && Detaqq_2b>1.2 && (HLT_BIT_HLT_PFHT750_4JetPt50_v||HLT_BIT_HLT_PFHT450_SixJet40_v||HLT_BIT_HLT_PFHT400_SixJet30_v||HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v||HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v||HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v)","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("#Delta #eta_{qq} ");
h->Draw("COLZ");
c1->SaveAs("data_Mqq_2b.png");

///////////////////////////////////////

tree->Draw("HLT_BIT_HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v:max(0,CSV[1]) >>h(20,0,1)","json && Mqq_2b>220 && Detaqq_2b>1.2 && (HLT_BIT_HLT_PFHT750_4JetPt50_v||HLT_BIT_HLT_PFHT450_SixJet40_v||HLT_BIT_HLT_PFHT400_SixJet30_v)","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("CSV2");
h->Draw("COLZ");
c1->SaveAs("data_CSV2_2b.png");

tree->Draw("HLT_BIT_HLT_QuadPFJet_SingleBTagCSV_VBF_Mqq460_v:max(0,CSV[0]) >>h(20,0,1)","json && Dphibb_1b<1.5 && Detaqq_1b>4.2 && (HLT_BIT_HLT_PFHT750_4JetPt50_v||HLT_BIT_HLT_PFHT450_SixJet40_v||HLT_BIT_HLT_PFHT400_SixJet30_v)","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("CSV1");
h->Draw("COLZ");
c1->SaveAs("data_CSV1_1b.png");







/////////////////////////////////

tree->Draw("(HLT_BIT_HLT_PFHT750_4JetPt50_v||HLT_BIT_HLT_PFHT450_SixJet40_v||HLT_BIT_HLT_PFHT400_SixJet30_v||HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v||HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v||HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v):Dphibb_1b >> h(8,0,3.2)","json && Detaqq_1b>4.2 && (HLT_BIT_HLT_PFHT750_4JetPt50_v||HLT_BIT_HLT_PFHT450_SixJet40_v||HLT_BIT_HLT_PFHT400_SixJet30_v||HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v||HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v||HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v)","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("#Delta #phi_{bb} ");
h->Draw("COLZ");
c1->SaveAs("data_Dphibb_1b.png");

tree->Draw("(HLT_BIT_HLT_PFHT750_4JetPt50_v||HLT_BIT_HLT_PFHT450_SixJet40_v||HLT_BIT_HLT_PFHT400_SixJet30_v||HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v||HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v||HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v):Detaqq_1b >> h(16,0,8)","json && Dphibb_1b<1.5 && (HLT_BIT_HLT_PFHT750_4JetPt50_v||HLT_BIT_HLT_PFHT450_SixJet40_v||HLT_BIT_HLT_PFHT400_SixJet30_v||HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v||HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v||HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v)","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("#Delta #eta_{qq} ");
h->Draw("COLZ");
c1->SaveAs("data_Detaqq_1b.png");

tree->Draw("(HLT_BIT_HLT_PFHT750_4JetPt50_v||HLT_BIT_HLT_PFHT450_SixJet40_v||HLT_BIT_HLT_PFHT400_SixJet30_v||HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v||HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v||HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v):-log(1-CSV[0]) >> h(10,0,5)","json && Dphibb_1b<1.5 && Detaqq_1b>4.2 && (HLT_BIT_HLT_PFHT750_4JetPt50_v||HLT_BIT_HLT_PFHT450_SixJet40_v||HLT_BIT_HLT_PFHT400_SixJet30_v||HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v||HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v||HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v)","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("-log(1-CSV1) ");
h->Draw("COLZ");
c1->SaveAs("data_CSV1_1b.png");


///////////////////////////////////////////
///////////////////////////////////////////
///////////////////////////////////////////


//L1 trigger efficiency: 2D(pt3,eta3) if one of the two leading jets is forward
tree->Draw("HLT_BIT_HLT_L1_TripleJet_VBF_v:Jet_pt[2]:Jet_eta[2] >> h(40,-5,5,30,0,150)","Jet_pt[1]>110 && Sum$(abs(Jet_eta)<3 && Iteration$<=1)==1","prof,COLZ");
h->SetTitle("");
h->GetYaxis()->SetTitle("p^{T}_{3} [GeV]");
h->GetXaxis()->SetTitle("|#eta|_{3} ");
h->Draw("COLZ");
c1->SaveAs("pt3_eta3_otherforward.png");

//L1 trigger efficiency: 2D(pt3,eta3) if the two leading jets are central
tree->Draw("HLT_BIT_HLT_L1_TripleJet_VBF_v:Jet_pt[2]:Jet_eta[2] >> h(40,-5,5,30,0,150)","Jet_pt[1]>110 && Sum$(abs(Jet_eta)<3 && Iteration$<=1)==2","prof,COLZ")
h->SetTitle("");
h->GetYaxis()->SetTitle("p^{T}_{3} [GeV]");
h->GetXaxis()->SetTitle("|#eta|_{3} ");
h->Draw("COLZ");
c1->SaveAs("pt3_eta3_othercentral.png");

//L1 trigger efficiency: 2D(pt2,pt3)
tree->Draw("HLT_BIT_HLT_L1_TripleJet_VBF_v:Jet_pt[1]:Jet_pt[2] >> h(30,0,150,30,0,150)"," Sum$(abs(Jet_eta)<3 && Iteration$<=2)>=2","prof,COLZ")
h->SetTitle("");
h->GetYaxis()->SetTitle("p^{T}_{2} [GeV]");
h->GetXaxis()->SetTitle("p^{T}_{3} [GeV]");
h->Draw("COLZ");
c1->SaveAs("pt2_pt3.png");

//L1 trigger efficiency: 1D(pt3)
tree->Draw("HLT_BIT_HLT_L1_TripleJet_VBF_v:Jet_pt[2] >> h(30,0,150)","Jet_pt[1]>110 && Sum$(abs(Jet_eta)<3 && Iteration$<=2)>=2","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("p^{T}_{3} [GeV]");
h->Draw("");
c1->SaveAs("pt3.png");

//L1 trigger efficiency: 1D(pt2)
tree->Draw("HLT_BIT_HLT_L1_TripleJet_VBF_v:Jet_pt[1] >> h(30,0,150)","abs(Jet_pt[1]-Jet_pt[2])<5 &&  Jet_pt[0]>110 && Sum$(abs(Jet_eta)<3 && Iteration$<=2)>=2","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("p^{T}_{2} [GeV]");
h->Draw("");
c1->SaveAs("pt2.png");


//L1 trigger efficiency: 1D(pt1)
tree->Draw("HLT_BIT_HLT_L1_TripleJet_VBF_v:Jet_pt[0] >> h(30,0,150)","abs(Jet_pt[0]-Jet_pt[1])<5 && abs(Jet_pt[0]-Jet_pt[2])<10 &&  Sum$(abs(Jet_eta)<3 && Iteration$<=2)>=2","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("p^{T}_{1} [GeV]");
h->Draw("");
c1->SaveAs("pt1.png");

//L1 trigger efficiency: 1D(pt1)
tree->Draw("HLT_BIT_HLT_L1_TripleJet_VBF_v:Jet_pt[0] >> h(30,0,150)","abs(Jet_pt[0]-Jet_pt[1])<5 && abs(Jet_pt[0]-Jet_pt[2])<10 &&  Sum$(abs(Jet_eta)<3 && Iteration$<=2)>=2","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("p^{T}_{1} [GeV]");
h->Draw("");
c1->SaveAs("pt1.png");

///////////////////////////////////////////

//HLT trigger efficiency: 2D(pt3,eta3) if one of the two leading jets is forward
tree->Draw("HLT_BIT_HLT_QuadPFJet_VBF_v:Jet_pt[2]:Jet_eta[2] >> h(40,-5,5,30,0,150)","Jet_pt[1]>110 && Sum$(abs(Jet_eta)<3 && Iteration$<=1)==1 && Mqq_eta>200 && Detaqq_eta>1.6","prof,COLZ");
h->SetTitle("");
h->GetYaxis()->SetTitle("p^{T}_{3} [GeV]");
h->GetXaxis()->SetTitle("|#eta|_{3} ");
h->Draw("COLZ");
c1->SaveAs("hlt_pt3_eta3_otherforward_hlt.png");

//HLT trigger efficiency: 2D(pt3,eta3) if the two leading jets are central
tree->Draw("HLT_BIT_HLT_QuadPFJet_VBF_v:Jet_pt[2]:Jet_eta[2] >> h(40,-5,5,30,0,150)","Jet_pt[1]>110 && Sum$(abs(Jet_eta)<3 && Iteration$<=1)==2 && Mqq_eta>200 && Detaqq_eta>1.6","prof,COLZ")
h->SetTitle("");
h->GetYaxis()->SetTitle("p^{T}_{3} [GeV]");
h->GetXaxis()->SetTitle("|#eta|_{3} ");
h->Draw("COLZ");
c1->SaveAs("hlt_pt3_eta3_othercentral.png");

//HLT trigger efficiency: 2D(pt2,pt3)
tree->Draw("HLT_BIT_HLT_QuadPFJet_VBF_v:Jet_pt[1]:Jet_pt[2] >> h(30,0,150,30,0,150)"," Sum$(abs(Jet_eta)<3 && Iteration$<=2)>=2 && Mqq_eta>200 && Detaqq_eta>1.6","prof,COLZ")
h->SetTitle("");
h->GetYaxis()->SetTitle("p^{T}_{2} [GeV]");
h->GetXaxis()->SetTitle("p^{T}_{3} [GeV]");
h->Draw("COLZ");
c1->SaveAs("hlt_pt2_pt3_hlt.png");

//HLT trigger efficiency: 1D(pt3)
tree->Draw("HLT_BIT_HLT_QuadPFJet_VBF_v:Jet_pt[2] >> h(30,0,150)","Jet_pt[1]>110 && Sum$(abs(Jet_eta)<3 && Iteration$<=2)>=2 && Mqq_eta>200 && Detaqq_eta>1.6","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("p^{T}_{3} [GeV]");
h->Draw("");
c1->SaveAs("hlt_pt3_hlt.png");

//HLT trigger efficiency: 1D(pt2)
tree->Draw("HLT_BIT_HLT_QuadPFJet_VBF_v:Jet_pt[1] >> h(30,0,150)","abs(Jet_pt[1]-Jet_pt[2])<5 &&  Jet_pt[0]>110 && Sum$(abs(Jet_eta)<3 && Iteration$<=2)>=2 && Mqq_eta>200 && Detaqq_eta>1.6","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("p^{T}_{2} [GeV]");
h->Draw("");
c1->SaveAs("hlt_pt2_hlt.png");


//HLT trigger efficiency: 1D(pt1)
tree->Draw("HLT_BIT_HLT_QuadPFJet_VBF_v:Jet_pt[0] >> h(30,0,150)","abs(Jet_pt[0]-Jet_pt[1])<5 && abs(Jet_pt[0]-Jet_pt[2])<10 &&  Sum$(abs(Jet_eta)<3 && Iteration$<=2)>=2 && Mqq_eta>200 && Detaqq_eta>1.6","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("p^{T}_{1} [GeV]");
h->Draw("");
c1->SaveAs("hlt_pt1_hlt.png");

//HLT trigger efficiency: 1D(pt4)
tree->Draw("HLT_BIT_HLT_QuadPFJet_VBF_v:Jet_pt[3] >> h(30,0,150)","Jet_pt[0]>95 && Jet_pt[1]>85 && Jet_pt[2]>75  &&  Sum$(abs(Jet_eta)<3 && Iteration$<=2)>=2 && Mqq_eta>200 && Detaqq_eta>1.6","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("p^{T}_{4} [GeV]");
h->Draw("");
c1->SaveAs("hlt_pt1_hlt.png");

//////////////////////////////////////////////////
//HLT EtaSorted trigger efficiency: 2D(Mqq_eta,Detaqq_eta)
tree->Draw("HLT_BIT_HLT_QuadPFJet_VBF_v:Mqq_eta:Detaqq_eta >> h(50,0,5,50,0,1000)","Jet_pt[0]>95 && Jet_pt[1]>85 && Jet_pt[2]>75 && Jet_pt[3]  && HLT_BIT_HLT_L1_TripleJet_VBF_v","prof,COLZ");
h->SetTitle("");
h->GetYaxis()->SetTitle("M_{qq} [GeV]");
h->GetXaxis()->SetTitle("#Delta #eta_{qq}");
h->Draw("COLZ");
c1->SaveAs("Mqq_eta_Detaqq_eta.png");


//HLT EtaSorted trigger efficiency: 1D(Mqq_eta)
tree->Draw("HLT_BIT_HLT_QuadPFJet_VBF_v:Mqq_eta >> h(50,0,500)"," abs(Jet_eta[2])<3 && Jet_pt[0]>95 && Jet_pt[1]>85 && Jet_pt[2]>75 && Jet_pt[3]  && HLT_BIT_HLT_L1_TripleJet_VBF_v && Detaqq_eta>1.6","prof");
h->SetTitle("");
h->GetXaxis()->SetTitle("M_{qq} [GeV]");
h->Draw("");
c1->SaveAs("Mqq_eta.png");

//HLT EtaSorted trigger efficiency: 1D(Mqq_eta)
tree->Draw("HLT_BIT_HLT_QuadPFJet_VBF_v:Detaqq_eta >> h(50,0,2.5)"," abs(Jet_eta[2])<3 && Jet_pt[0]>95 && Jet_pt[1]>85 && Jet_pt[2]>75 && Jet_pt[3]  && HLT_BIT_HLT_L1_TripleJet_VBF_v && Mqq_eta>200","prof");
h->SetTitle("");
h->GetXaxis()->SetTitle("#Delta #eta_{qq}");
h->Draw("");
c1->SaveAs("Detaqq_eta.png");

//////////////////////////////////////////////////
//HLT 1BtagAndEta trigger efficiency: 2D(Dphibb_1b,Detaqq_eta)
tree->Draw("(HLT_BIT_HLT_PFHT750_4JetPt50_v||HLT_BIT_HLT_PFHT450_SixJet40_v||HLT_BIT_HLT_PFHT400_SixJet30_v||HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v||HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v||HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v):Dphibb_1b:Detaqq_1b >> h(160,0,8,32,0,3.2)","HLT_BIT_HLT_QuadPFJet_VBF_v","prof,COLZ")
h->SetTitle("");
h->GetYaxis()->SetTitle("#Delta #phi_{bb}");
h->GetXaxis()->SetTitle("#Delta #eta_{qq}");
h->Draw("COLZ");
c1->SaveAs("Dphibb_1b_Detaqq_1b.png");

//HLT 1BtagAndEta trigger efficiency: 1D(Detaqq_1b)
tree->Draw("(HLT_BIT_HLT_PFHT750_4JetPt50_v||HLT_BIT_HLT_PFHT450_SixJet40_v||HLT_BIT_HLT_PFHT400_SixJet30_v||HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v||HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v||HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v):Detaqq_1b >> h(160,3,5)","HLT_BIT_HLT_QuadPFJet_VBF_v && Dphibb_1b<1.5","prof,COLZ")
h->SetTitle("");
h->GetXaxis()->SetTitle("#Delta #eta_{qq}");
h->Draw("COLZ");
c1->SaveAs("Detaqq_1b.png");


//HLT 1BtagAndEta trigger efficiency: 1D(Dphibb_1b)
tree->Draw("(HLT_BIT_HLT_PFHT750_4JetPt50_v||HLT_BIT_HLT_PFHT450_SixJet40_v||HLT_BIT_HLT_PFHT400_SixJet30_v||HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v||HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v||HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v):Dphibb_1b >> h(160,1,2)","HLT_BIT_HLT_QuadPFJet_VBF_v && Detaqq_1b>4.2","prof,COLZ")
h->SetTitle("");
h->GetXaxis()->SetTitle("#Delta #phi_{bb}");
h->Draw("COLZ");
c1->SaveAs("Dphibb_1b.png");

//HLT 1BtagAndEta trigger efficiency: 1D(Mqq_1b)
tree->Draw("(HLT_BIT_HLT_PFHT750_4JetPt50_v||HLT_BIT_HLT_PFHT450_SixJet40_v||HLT_BIT_HLT_PFHT400_SixJet30_v||HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v||HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v||HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v):Mqq_1b >> h(40,0,2000)","HLT_BIT_HLT_QuadPFJet_VBF_v && Detaqq_1b>4.2 && Dphibb_1b<1.5 && CSV[0]>0.941","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("M_{qq}");
h->Draw("");
c1->SaveAs("Mqq_1b.png");

//HLT 1BtagAndEta trigger efficiency: 1D(-log(1-CSV[0]))
tree->Draw("(HLT_BIT_HLT_PFHT750_4JetPt50_v||HLT_BIT_HLT_PFHT450_SixJet40_v||HLT_BIT_HLT_PFHT400_SixJet30_v||HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v||HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v||HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v):-log(1-CSV[0]) >> h(40,0,8)","HLT_BIT_HLT_QuadPFJet_VBF_v && Detaqq_1b>4.2 && Dphibb_1b<1.5","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("-log(1-CSV1)");
h->Draw("");
c1->SaveAs("CSV1_1b.png");

//HLT 1BtagAndEta trigger efficiency: 2D(Mqq_1b,Detaqq_eta)
tree->Draw("(HLT_BIT_HLT_PFHT750_4JetPt50_v||HLT_BIT_HLT_PFHT450_SixJet40_v||HLT_BIT_HLT_PFHT400_SixJet30_v||HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v||HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v||HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v):Mqq_1b:Detaqq_1b >> h(40,0,8,50,0,5000)","HLT_BIT_HLT_QuadPFJet_VBF_v && Dphibb_1b<1.5 && CSV[0]>0.941","prof,COLZ")
h->SetTitle("");
h->GetYaxis()->SetTitle("M_{qq}");
h->GetXaxis()->SetTitle("#Delta #eta_{qq}");
h->Draw("COLZ");
c1->SaveAs("Mqq_1b_Detaqq_1b.png");


//HLT 1BtagAndEta trigger efficiency: 2D(Mqq_1b,Detaqq_eta)
tree->Draw("(HLT_BIT_HLT_PFHT750_4JetPt50_v||HLT_BIT_HLT_PFHT450_SixJet40_v||HLT_BIT_HLT_PFHT400_SixJet30_v||HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v||HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v||HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v):Mqq_1b:Detaqq_1b >> h(40,0,8,50,0,5000)","HLT_BIT_HLT_QuadPFJet_VBF_v && Dphibb_1b<1.5 && CSV[0]>0.941","prof,COLZ")
h->SetTitle("");
h->GetYaxis()->SetTitle("M_{qq}");
h->GetXaxis()->SetTitle("#Delta #eta_{qq}");
h->Draw("COLZ");
c1->SaveAs("Mqq_1b_Detaqq_1b.png");

//////////////////////////////////////////////////

//CSVL: 0.423 -> 0.549913012
//CSVM: 0.814 -> 1.682008605
//CSVT: 0.941 -> 2.830217835

//HLT 2BtagAndPt trigger efficiency: 2D(Mqq_1b,Detaqq_eta)
tree->Draw("HLT_BIT_HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v:Mqq_2b:Detaqq_2b >> h(30,0,6,25,0,1000)","HLT_BIT_HLT_QuadPFJet_VBF_v && CSV[1]>0.941","prof,COLZ")
h->SetTitle("");
h->GetYaxis()->SetTitle("M_{qq}");
h->GetXaxis()->SetTitle("#Delta #eta_{qq}");
h->Draw("COLZ");
c1->SaveAs("Mqq_2b_Detaqq_2b.png");


//HLT 2BtagAndPt trigger efficiency: 1D(Mqq_1b)
tree->Draw("HLT_BIT_HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v:Mqq_2b >> h(25,0,500)","HLT_BIT_HLT_QuadPFJet_VBF_v && CSV[1]>0.941 && Detaqq_2b>1.3","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("M_{qq}");
h->Draw("");
c1->SaveAs("Mqq_2b.png");


//HLT 2BtagAndPt trigger efficiency: 1D(Detaqq_eta)
tree->Draw("HLT_BIT_HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v:Detaqq_2b >> h(30,0,3)","HLT_BIT_HLT_QuadPFJet_VBF_v && CSV[1]>0.941 && Mqq_2b>200","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("#Delta #eta_{qq}");
h->Draw("");
c1->SaveAs("Detaqq_2b.png");

//HLT 2BtagAndPt trigger efficiency: 1D(Detaqq_eta)
tree->Draw("HLT_BIT_HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v:-log(1-CSV[0]):-log(1-CSV[1]) >> h(20,0,5,20,0.001,5)","HLT_BIT_HLT_QuadPFJet_VBF_v && Mqq_2b>200 && Detaqq_2b>1.2","prof,COLZ")
h->SetTitle("");
h->GetYaxis()->SetTitle("-log(1-CSV1)");
h->GetXaxis()->SetTitle("-log(1-CSV2)");
h->Draw("COLZ");
c1->SaveAs("CSV1_CSV2_2b.png");

//HLT 2BtagAndPt trigger efficiency: 1D(Detaqq_eta)
tree->Draw("HLT_BIT_HLT_QuadPFJet_DoubleBTagCSV_VBF_Mqq200_v:-log(1-CSV[1]) >> h(24,0,6)","HLT_BIT_HLT_QuadPFJet_VBF_v && Mqq_2b>200 && Detaqq_2b>1.2 && CSV[0]>0.999","prof")
h->SetTitle("");
h->GetXaxis()->SetTitle("-log(1-CSV2)");
h->Draw("COLZ");
c1->SaveAs("CSV2_2b.png");

//HLT EtaSorted trigger efficiency: 1D(CSV1)
//tree->Draw("-log(1-CSV[0]) >> h(50,0,8)","HLT_BIT_HLT_QuadPFJet_VBF_v && Detaqq_1b>4.2 && Dphibb_1b<1.5 && Mqq_1b>650","")
//tree->Draw("-log(1-CSV[0]) >> h2(50,0,8)", "HLT_BIT_HLT_QuadPFJet_VBF_v && Detaqq_1b>4.2 && Dphibb_1b<1.5 && Mqq_1b>650 && (HLT_BIT_HLT_PFHT750_4JetPt50_v||HLT_BIT_HLT_PFHT450_SixJet40_v||HLT_BIT_HLT_PFHT400_SixJet30_v||HLT_BIT_HLT_PFHT400_SixJet30_BTagCSV0p55_2PFBTagCSV0p72_v||HLT_BIT_HLT_QuadJet45_DoubleBTagCSV0p67_v||HLT_BIT_HLT_DoubleJet90_Double30_DoubleBTagCSV0p67_v)")
//h->SetLineColor(kBlue);
//h->SetFillColor(kBlue);
//h2->SetLineColor(kRed);
//h2->SetFillColor(kRed);
//h->SetTitle("");
//h->GetXaxis()->SetTitle("CSV1");
////h->GetXaxis()->SetTitle("M_{qq}");
//h->Draw("");
//h2->Draw("same");
//c1->SaveAs("CSV1_1b.png");

}
