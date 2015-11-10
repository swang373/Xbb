{
gStyle->SetOptStat(0);
gROOT->SetBatch();

TCanvas* c1 = new TCanvas("c1","c1");
c1->SetGridx();
c1->SetGridy();

TFile *_file0 = TFile::Open("newTree2.root");
TTree* tree = (TTree*) _file0->Get("tree");

TFile* file = new TFile("test.root","recreate");

//L1 cut: Jet_pt[0]>92 && Jet_pt[1]>76 && Jet_pt[2]>64 && abs(Jet_eta)<3
//Calo cut: Jet_pt[0]>80 && Jet_pt[1]>65 && Jet_pt[2]>50 && Jet_pt[3]>15
//Calo CSV 0.74
//PF cut: Jet_pt[0]>92 && Jet_pt[1]>76 && Jet_pt[2]>64 && Jet_pt[3]>15
//PF CSV 0.78 e 0.58

//CaloCut: Mqq_eta>150 && Detaqq_eta>1.5
//PFCut 1-btag: Mqq_1b>460 && bDetaqq_single>4.1 && Dphibb_1b<1.6
//PFCut 2-btag: Mqq_2b>200 && bDetaqq_double>1.2


//TF1* turnonPt = new TF1("turnonPt","  [2]/(1+exp(-[1]*(x-[0]))) +[3] ");
//turnonPt->SetParameters(40,0.01,1,-0.01);
//TF1* turnonPt = new TF1("turnonPt","(0.5+0.5*erf((x-[0])*(x-[3]>[0])/[1] + (x-[0])*(x-[3]<=[0])/[2] ))*[5]+[4]");
//TF1* turnonPt = new TF1("turnonPt","(0.5+0.5*erf((x-[0])*(x-[0]>[5])/[1] + (x-[0])*(x-[0]<=[5])/[2] ))*[4]+[3]");
TF1* turnonPt = new TF1("turnonPt","(0.5+0.5*erf( (x-[0])*(x-[0]>[5])/[1] + (x-[0])*(x-[0]<[5])/[2] + [5]*(1/[1]-1/[2])*(x-[0]<[5]) ))*[4]+[3] ");
turnonPt->SetParameters(40,10,10,0,1);
turnonPt->SetParLimits(0,0,10000);
turnonPt->SetParLimits(1,0,100);
turnonPt->SetParLimits(2,0,100);
turnonPt->SetParLimits(3,-0.5,0);
turnonPt->SetParLimits(4,0,1);
turnonPt->SetParLimits(5,-100,100);


TF2* turnon2D = new TF2("turnonPt","((0.5+0.5*erf((x-[0])/[1]))*[2]+[3])*((0.5+0.5*erf((y-[4])/[5]))*[6]+[7])");
turnon2D->SetParameters(40,10,1,0,40,10,1,0);
//turnonPt->SetParLimits(0,0,10000);
//turnonPt->SetParLimits(1,0,100);
//turnonPt->SetParLimits(2,0,100);
//turnonPt->SetParLimits(3,-100,100);
//turnonPt->SetParLimits(4,-0.5,0);
//turnonPt->SetParLimits(5,0,1);

//TF1* turnonCSV = new TF1("turnonCSV","[0]+x*[1]+x*x*[2]+x*x*x*[3]");
//turnonCSV->SetParameters(0,0.5,0.5,0);

TF1* turnonCSV = new TF1("turnonCSV","0.5+0.5*erf(((-log(1.00001-x))-[0])/[1])+[2]");
turnonCSV->SetParameters(2,2,-0.05);


TF1* turnonDphi = new TF1("turnonDphi"," [2]/(1+exp([1]*(x-[0]))) +[3]");
turnonDphi->SetParameters(1.6,0.01,1,-0.01);

//tree->SetBranchStatus("*",0);
//tree->SetBranchStatus("*Jet*",1);
//tree->SetBranchStatus("*l1Jet*",0);
//tree->SetBranchStatus("*PUPPI*",0);
//tree->SetBranchStatus("*CSV*",1);
//tree->SetBranchStatus("1==1",1);
//tree->SetBranchStatus("HLT_DiPFJetAve60_v2",1);
//tree->SetBranchStatus("HLT_DiPFJetAve40_v2",1);


//TFile *_tmpFile = TFile::Open("tmp.root","recreate");
//TTree* tree = (TTree*) tree->CopyTree("(HLT_DiPFJetAve60_v2 || HLT_DiPFJetAve40_v2)");

tree->Draw("(hltQuadJet15>=0):offJet_pt[0]+offJet_pt[1]+offJet_pt[2]  >> h(100,0,500)"," ( HLT_PFJet40_v3)  ","prof,B");
h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("L1 trigger turn-on");
h->GetXaxis()->SetTitle("p^{T}_{1}+p^{T}_{2}+p^{T}_{3}");
TF1* tnL1Pt1PtPt3 = (TF1*) turnonPt->Clone("tnL1Pt1PtPt3");
h->Fit(tnL1Pt1PtPt3,"","",20,2000);
c1->SaveAs("L1Pt1PtPt3.png");
c1->SaveAs("L1Pt1PtPt3.C");


tree->Draw("(hltQuadJet15>=4):offJet_pt[3] >> h(50,0,200)"," (HLT_PFJet40_v3) && (hltQuadJet15>=0)","prof");
h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("Calo p^{T}_{4} turn-on");
h->GetXaxis()->SetTitle("p^{T}_{4}");
TF1* tnCaloPt4 = (TF1*) turnonPt->Clone("tnCaloPt4");
h->Fit(tnCaloPt4,"","",20,2000);
c1->SaveAs("CaloPt4.png");
c1->SaveAs("CaloPt4.C");

tree->Draw("(hltTripleJet50>=3):offJet_pt[2] >> h(50,0,200)"," (HLT_PFJet60_v3) && (hltQuadJet15>=4) && (hltTripleJet50>=0) ","prof");
h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("");
h->GetXaxis()->SetTitle("p^{T}_{3}");
TF1* tnCaloPt3 = (TF1*) turnonPt->Clone("Calo p^{T}_{3} turn-on");
h->Fit(tnCaloPt3,"","",20,2000);
c1->SaveAs("CaloPt3.png");
c1->SaveAs("CaloPt3.C");

tree->Draw("(hltDoubleJet65>=2):offJet_pt[1] >> h(50,0,200)"," (HLT_DiPFJetAve60_v2 || HLT_DiPFJetAve40_v2) && (hltQuadJet15>=4) && (hltTripleJet50>=3) && (hltDoubleJet65>=0) ","prof");
h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("Calo p^{T}_{2} turn-on");
h->GetXaxis()->SetTitle("p^{T}_{2}");
TF1* tnCaloPt2 = (TF1*) turnonPt->Clone("tnCaloPt2");
h->Fit(tnCaloPt2,"","",20,2000);
c1->SaveAs("CaloPt2.png");
c1->SaveAs("CaloPt2.C");

tree->Draw("(hltSingleJet80>=1):offJet_pt[0] >> h(50,0,200)"," (HLT_DiPFJetAve60_v2 || HLT_DiPFJetAve40_v2) && (hltQuadJet15>=4) && (hltTripleJet50>=3) && (hltDoubleJet65>=2) && (hltSingleJet80>=0) ","prof");
h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("Calo p^{T}_{1} turn-on");
h->GetXaxis()->SetTitle("p^{T}_{1}");
TF1* tnCaloPt1 = (TF1*) turnonPt->Clone("tnCaloPt1");
h->Fit(tnCaloPt1,"","",20,2000);
c1->SaveAs("CaloPt1.png");
c1->SaveAs("CaloPt1.C");

//tree->Draw("(hltVBFCaloJetEtaSortedMqq150Deta1p5>=4):MaxIf$(offJet_eta,offJet_pt>30)-MinIf$(offJet_eta,offJet_pt>30) >> h(100,0,5)"," (HLT_DiPFJetAve60_v2 || HLT_DiPFJetAve40_v2) && (hltQuadJet15>=4) && (hltTripleJet50>=3) && (hltDoubleJet65>=2) && (hltSingleJet80>=1) && (hltVBFCaloJetEtaSortedMqq150Deta1p5>=0) && Mqq_single>250","prof");
//h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("");
//h->GetXaxis()->SetTitle("#Delta #eta (qq)");
//TF1* tnDeltaEtaCalo = (TF1*) turnonPt->Clone("tnDeltaEtaCalo");
//tnDeltaEtaCalo->SetParameters(1.5,0.05,0.05,0,0);
//h->Fit(tnDeltaEtaCalo);
//c1->SaveAs("DeltaEtaCalo.png");
//c1->SaveAs("DeltaEtaCalo.C");

//FIXME: we should use as variables Mqq_eta:bDetaqq_eta !!
tree->Draw("(hltVBFCaloJetEtaSortedMqq150Deta1p5>=4):Mqq_single:MaxIf$(offJet_eta,offJet_pt>30)-MinIf$(offJet_eta,offJet_pt>30) >> h(20,0,4,20,0,400)"," (HLT_DiPFJetAve60_v2 || HLT_DiPFJetAve40_v2 || HLT_DiPFJetAve60_v2 || HLT_QuadPFJet_VBF_v3) && (hltQuadJet15>=4) && (hltTripleJet50>=3) && (hltDoubleJet65>=2) && (hltSingleJet80>=0) && (hltVBFCaloJetEtaSortedMqq150Deta1p5>=0)","prof,COLZ");
h->GetYaxis()->SetTitle("#Delta#eta (qq)");h->SetTitle("Calo VBF cut turn-on");
h->GetXaxis()->SetTitle("M (qq)");
TF2* tn2D_eta = (TF2*) turnon2D->Clone("tn2D_eta");
tn2D_eta->SetRange(0,0,4,400);
tn2D_eta->SetParameters(1.2,0.1,0.6,0.3,200,10,0.6,0.3);
h->Fit(tn2D_eta);
c1->SaveAs("2D_eta.png");
c1->SaveAs("2D_eta.C");

tree->Draw("hltCSVL30p74>0:Max$(offJet_csv) >> h(100,0,1)","(HLT_DiPFJetAve60_v2 || HLT_DiPFJetAve40_v2) && (hltQuadJet15>=4) && (hltTripleJet50>=3) && (hltDoubleJet65>=2) && (hltSingleJet80>=1) && (hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (hltCSVL30p74>=0) ","prof");
h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("Calo CSV1 turn-on");
h->GetXaxis()->SetTitle("CSV");
TF1* tnCaloCSV1 = (TF1*) turnonCSV->Clone("tnCaloCSV1");
tnCaloCSV1->SetParameters(1.5,0.05,0.05,0,0);
h->Fit(tnCaloCSV1);
c1->SaveAs("CaloCSV1.png");
c1->SaveAs("CaloCSV1.C");

tree->Draw("(hltPFQuadJetLooseID15>=4):offJet_pt[3] >> h(50,0,200)"," (HLT_DiPFJetAve60_v2 || HLT_DiPFJetAve40_v2) && (hltQuadJet15>=4) && (hltTripleJet50>=3) && (hltDoubleJet65>=2) && (hltSingleJet80>=0) && (hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (hltCSVL30p74>=1) && (hltPFQuadJetLooseID15>=0) ","prof");
h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("PF p^{T}_{4} turn-on");
h->GetXaxis()->SetTitle("p^{T}_{4}");
TF1* tnPFPt4 = (TF1*) turnonPt->Clone("tnPFPt4");
tnPFPt4->SetParameters(6.7,14,0,0,0);
h->Fit(tnPFPt4,"","",20,2000);
c1->SaveAs("PFPt4.png");
c1->SaveAs("PFPt4.C");

tree->Draw("(hltPFTripleJetLooseID64>=3):offJet_pt[2] >> h(50,0,200)"," (HLT_DiPFJetAve60_v2 || HLT_DiPFJetAve40_v2) && (hltQuadJet15>=4) && (hltTripleJet50>=3) && (hltDoubleJet65>=2) && (hltSingleJet80>=0) && (hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (hltCSVL30p74>=1) && (hltPFQuadJetLooseID15>=4) && (hltPFTripleJetLooseID64>=0)","prof");
h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("PF p^{T}_{3} turn-on");
h->GetXaxis()->SetTitle("p^{T}_{3}");
TF1* tnPFPt3 = (TF1*) turnonPt->Clone("tnPFPt3");
h->Fit(tnPFPt3,"","",20,2000);
c1->SaveAs("PFPt3.png");
c1->SaveAs("PFPt3.C");

tree->Draw("(hltPFDoubleJetLooseID76>=2):offJet_pt[1] >> h(50,0,200)"," (HLT_DiPFJetAve60_v2 || HLT_DiPFJetAve40_v2) && (hltQuadJet15>=4) && (hltTripleJet50>=3) && (hltDoubleJet65>=2) && (hltSingleJet80>=0) && (hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (hltCSVL30p74>=1) && (hltPFQuadJetLooseID15>=4) && (hltPFTripleJetLooseID64>=3) && (hltPFDoubleJetLooseID76>=0)","prof");
h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("PF p^{T}_{2} turn-on");
h->GetXaxis()->SetTitle("p^{T}_{2}");
TF1* tnPFPt2 = (TF1*) turnonPt->Clone("tnPFPt2");
h->Fit(tnPFPt2,"","",20,2000);
c1->SaveAs("PFPt2.png");
c1->SaveAs("PFPt2.C");

tree->Draw("(hltPFSingleJetLooseID92>=1):offJet_pt[0] >> h(50,0,200)"," (HLT_DiPFJetAve60_v2 || HLT_DiPFJetAve40_v2) && (hltQuadJet15>=4) && (hltTripleJet50>=3) && (hltDoubleJet65>=2) && (hltSingleJet80>=0) && (hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (hltCSVL30p74>=1) && (hltPFQuadJetLooseID15>=4) && (hltPFTripleJetLooseID64>=3) && (hltPFDoubleJetLooseID76>=2) && (hltPFSingleJetLooseID92>=0) ","prof");
h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("PF p^{T}_{1} turn-on");
h->GetXaxis()->SetTitle("p^{T}_{1}");
TF1* tnPFPt1 = (TF1*) turnonPt->Clone("tnPFPt1");
h->Fit(tnPFPt1,"","",20,2000);
c1->SaveAs("PFPt1.png");
c1->SaveAs("PFPt1.C");

//tree->Draw("pfJet_hltCSVPF0p78>0:offJet_csv[pfJet_offmatch] >> h(100,0,1)","pfJet_offmatch>=0 && (HLT_DiPFJetAve60_v2 || HLT_DiPFJetAve40_v2) && (hltQuadJet15>=4) && (hltTripleJet50>=3) && (hltDoubleJet65>=2) && (hltSingleJet80>=0) && (hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (hltCSVL30p74>=1) && (hltPFQuadJetLooseID15>=4) && (hltPFTripleJetLooseID64>=3) && (hltPFDoubleJetLooseID76>=2) && (hltPFSingleJetLooseID92>=1) ","prof");
//h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("");
//h->GetXaxis()->SetTitle("CSV");
//c1->SaveAs("PFCSV1.png");
//c1->SaveAs("PFCSV1.C");

//tree->Draw("pfJet_hltDoubleCSVPF0p58>0:offJet_csv[pfJet_offmatch] >> h(100,0,1)","pfJet_offmatch>=0 && (HLT_DiPFJetAve60_v2 || HLT_DiPFJetAve40_v2) && (hltQuadJet15>=4) && (hltTripleJet50>=3) && (hltDoubleJet65>=2) && (hltSingleJet80>=0) && (hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (hltCSVL30p74>=1) && (hltPFQuadJetLooseID15>=4) && (hltPFTripleJetLooseID64>=3) && (hltPFDoubleJetLooseID76>=2) && (hltPFSingleJetLooseID92>=1) ","prof");
//h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("");
//h->GetXaxis()->SetTitle("CSV");
//c1->SaveAs("PFCSV2.png");
//c1->SaveAs("PFCSV2.C");

//Double CSV path hltDoubleCSVPF0p58, hltCSVPF0p78, hltVBFPFJetCSVSortedMqq200Detaqq1p2

tree->Draw("hltDoubleCSVPF0p58>=2:MaxIf$(offJet_csv,offJet_csv!=Max$(offJet_csv)) >> h(50,0,1)","(HLT_DiPFJetAve60_v2 || HLT_DiPFJetAve40_v2 || HLT_DiPFJetAve60_v2 || HLT_QuadPFJet_VBF_v3) && (hltQuadJet15>=4) && (hltTripleJet50>=3) && (hltDoubleJet65>=2) && (hltSingleJet80>=0) && (hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (hltCSVL30p74>=1) && (hltPFQuadJetLooseID15>=4) && (hltPFTripleJetLooseID64>=3) && (hltPFDoubleJetLooseID76>=2) && (hltPFSingleJetLooseID92>=1) && (hltDoubleCSVPF0p58>=0) ","prof");
h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("PF CSV2 turn-on (double b-tag path)");
h->GetXaxis()->SetTitle("CSV");
TF1* tnPFCSV2_double = (TF1*) turnonCSV->Clone("tnPFCSV2_double");
tnPFCSV2_double->SetParameters(1.5,0.05,0.05,0,0);
h->Fit(tnPFCSV2_double);
c1->SaveAs("PFCSV2_double.png");
c1->SaveAs("PFCSV2_double.C");

tree->Draw("hltCSVPF0p78>=1:Max$(offJet_csv) >> h(50,0,1)","(HLT_DiPFJetAve60_v2 || HLT_DiPFJetAve40_v2 || HLT_DiPFJetAve60_v2 || HLT_QuadPFJet_VBF_v3) && (hltQuadJet15>=4) && (hltTripleJet50>=3) && (hltDoubleJet65>=2) && (hltSingleJet80>=0) && (hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (hltCSVL30p74>=1) && (hltPFQuadJetLooseID15>=4) && (hltPFTripleJetLooseID64>=3) && (hltPFDoubleJetLooseID76>=2) && (hltPFSingleJetLooseID92>=1) && (hltDoubleCSVPF0p58>=2) && (hltCSVPF0p78>=0)","prof");
h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("PF CSV1 turn-on (double b-tag path)");
h->GetXaxis()->SetTitle("CSV");
TF1* tnPFCSV1_double = (TF1*) turnonCSV->Clone("tnPFCSV1_double");
tnPFCSV1_double->SetParameters(1.5,0.05,0.05,0,0);
h->Fit(tnPFCSV1_double);
c1->SaveAs("PFCSV1_double.png");
c1->SaveAs("PFCSV1_double.C");

tree->Draw("(hltVBFPFJetCSVSortedMqq200Detaqq1p2>=4):Mqq_double:bDetaqq_double >> h(20,0,4,20,0,400)"," (HLT_DiPFJetAve60_v2 || HLT_DiPFJetAve40_v2 || HLT_DiPFJetAve60_v2 || HLT_QuadPFJet_VBF_v3) && (hltQuadJet15>=4) && (hltTripleJet50>=3) && (hltDoubleJet65>=2) && (hltSingleJet80>=0) && (hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (hltCSVL30p74>=1) && (hltPFQuadJetLooseID15>=4) && (hltPFTripleJetLooseID64>=3) && (hltPFDoubleJetLooseID76>=2) && (hltPFSingleJetLooseID92>=1) && (hltDoubleCSVPF0p58>=2) && (hltCSVPF0p78>=1) && (hltVBFPFJetCSVSortedMqq200Detaqq1p2>=0)","prof,COLZ");
h->GetYaxis()->SetTitle("#Delta#eta (qq)");h->SetTitle("PF VBF cut turn-on (double b-tag path)");
h->GetXaxis()->SetTitle("M (qq)");
TF2* tn2D_double = (TF2*) turnon2D->Clone("tn2D_double");
tn2D_double->SetRange(0,0,4,400);
tn2D_double->SetParameters(1.2,0.1,0.6,0.3,200,10,0.6,0.3);
h->Fit(tn2D_double);
c1->SaveAs("2D_double.png");
c1->SaveAs("2D_double.C");

tn2D_double->SetMaximum(1);
tn2D_double->Draw("COLZ");
c1->SaveAs("2D_double_funct.png");
c1->SaveAs("2D_double_funct.C");


//tree->Draw("(hltVBFPFJetCSVSortedMqq200Detaqq1p2>=4):Mqq_double >> h(20,0,400)"," (HLT_DiPFJetAve60_v2 || HLT_DiPFJetAve40_v2 || HLT_DiPFJetAve60_v2 || HLT_QuadPFJet_VBF_v3) && (hltQuadJet15>=4) && (hltTripleJet50>=3) && (hltDoubleJet65>=2) && (hltSingleJet80>=0) && (hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (hltCSVL30p74>=1) && (hltPFQuadJetLooseID15>=4) && (hltPFTripleJetLooseID64>=3) && (hltPFDoubleJetLooseID76>=2) && (hltPFSingleJetLooseID92>=1) && (hltDoubleCSVPF0p58>=2) && (hltCSVPF0p78>=1) && (hltVBFPFJetCSVSortedMqq200Detaqq1p2>=0) && bDetaqq_double>1.3","prof");
//h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("");
//h->GetXaxis()->SetTitle("M (qq)");
//TF1* tnMqqdouble = (TF1*) turnonPt->Clone("tnMqqdouble");
//tnMqqdouble->SetParameters(200,30,30,0,0);
//h->Fit(tnMqqdouble);
//c1->SaveAs("MqqPF200_double.png");
//c1->SaveAs("MqqPF200_double.C");

//tree->Draw("(hltVBFPFJetCSVSortedMqq200Detaqq1p2>=4):bDetaqq_double >> h(20,0,4)"," (HLT_DiPFJetAve60_v2 || HLT_DiPFJetAve40_v2 || HLT_DiPFJetAve60_v2 || HLT_QuadPFJet_VBF_v3) && (hltQuadJet15>=4) && (hltTripleJet50>=3) && (hltDoubleJet65>=2) && (hltSingleJet80>=0) && (hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (hltCSVL30p74>=1) && (hltPFQuadJetLooseID15>=4) && (hltPFTripleJetLooseID64>=3) && (hltPFDoubleJetLooseID76>=2) && (hltPFSingleJetLooseID92>=1) && (hltDoubleCSVPF0p58>=2) && (hltCSVPF0p78>=1) && (hltVBFPFJetCSVSortedMqq200Detaqq1p2>=0) && Mqq_double>220","prof");
//h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("");
//h->GetXaxis()->SetTitle("#Delta #eta (qq)");
//TF1* tnDeltaEtadouble = (TF1*) turnonPt->Clone("tnDeltaEtadouble");
//tnDeltaEtadouble->SetParameters(1.5,0.05,0.05,0,0);
//h->Fit(tnDeltaEtadouble);
//c1->SaveAs("DeltaEtaPF200_double.png");
//c1->SaveAs("DeltaEtaPF200_double.C");

//Single CSV path hltDoubleCSVPF0p58, hltCSVPF0p78, hltVBFPFJetCSVSortedMqq200Detaqq1p2

tree->Draw("hltCSVPF0p78>=1:Max$(offJet_csv) >> h(50,0,1)","(HLT_DiPFJetAve60_v2 || HLT_DiPFJetAve40_v2 || HLT_DiPFJetAve60_v2 || HLT_QuadPFJet_VBF_v3) && (hltQuadJet15>=4) && (hltTripleJet50>=3) && (hltDoubleJet65>=2) && (hltSingleJet80>=0) && (hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (hltCSVL30p74>=1) && (hltPFQuadJetLooseID15>=4) && (hltPFTripleJetLooseID64>=3) && (hltPFDoubleJetLooseID76>=2) && (hltPFSingleJetLooseID92>=1) && (hltCSVPF0p78>=0)","prof");
h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("PF CSV1 turn-on (single b-tag path)");
h->GetXaxis()->SetTitle("CSV");
TF1* tnPFCSV1_single = (TF1*) turnonCSV->Clone("tnPFCSV1_single");
tnPFCSV1_single->SetParameters(1.5,0.05,0.05,0,0);
h->Fit(tnPFCSV1_single);
c1->SaveAs("PFCSV1_single.png");
c1->SaveAs("PFCSV1_single.C");

tree->Draw("(hltVBFPFJetCSVSortedMqq460Detaqq4p1>=4):bDetaqq_single:bDphibb_single >> h(32,0,3.2,20,0,6)"," (HLT_DiPFJetAve60_v2 || HLT_DiPFJetAve40_v2 || HLT_DiPFJetAve60_v2 || HLT_QuadPFJet_VBF_v3) && (hltQuadJet15>=4) && (hltTripleJet50>=3) && (hltDoubleJet65>=2) && (hltSingleJet80>=0) && (hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (hltCSVL30p74>=1) && (hltPFQuadJetLooseID15>=4) && (hltPFTripleJetLooseID64>=3) && (hltPFDoubleJetLooseID76>=2) && (hltPFSingleJetLooseID92>=1) && (hltCSVPF0p78>=1) && (hltVBFPFJetCSVSortedMqq460Detaqq4p1>=0)","prof,COLZ");
h->GetYaxis()->SetTitle("#Delta#eta (qq)");h->SetTitle("PF VBF cut turn-on (single b-tag path)");
h->GetXaxis()->SetTitle("#Delta#phi (bb)");
TF2* tn2D_single = (TF2*) turnon2D->Clone("tn2D_single");
tn2D_single->SetRange(0,0,3.2,6);
tn2D_single->SetParameters(1.6,-0.06,0.8,0.15,4.1,0.17,0.68,0.06);
//tn2D_double->SetParameters(200,30,30,0,0);
h->Fit(tn2D_single);
c1->SaveAs("2D_single.png");
c1->SaveAs("2D_single.C");

tn2D_single->SetMaximum(1);
tn2D_single->Draw("COLZ");
c1->SaveAs("2D_single_funct.png");
c1->SaveAs("2D_single_funct.C");

//tree->Draw("(hltVBFPFJetCSVSortedMqq460Detaqq4p1>=4):bDphibb_single >> h(16,0,3.2)"," (HLT_DiPFJetAve60_v2 || HLT_DiPFJetAve40_v2 || HLT_DiPFJetAve60_v2 || HLT_QuadPFJet_VBF_v3) && (hltQuadJet15>=4) && (hltTripleJet50>=3) && (hltDoubleJet65>=2) && (hltSingleJet80>=0) && (hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (hltCSVL30p74>=1) && (hltPFQuadJetLooseID15>=4) && (hltPFTripleJetLooseID64>=3) && (hltPFDoubleJetLooseID76>=2) && (hltPFSingleJetLooseID92>=1) && (hltCSVPF0p78>=1) && (hltVBFPFJetCSVSortedMqq460Detaqq4p1>=0) && bDetaqq_single>4.2 ","prof");
//h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("");
//h->GetXaxis()->SetTitle("#Delta #eta (qq)");
//TF1* tnDeltaEta_single = (TF1*) turnonPt->Clone("tnDeltaEta_single");
//tnDeltaEta_single->SetParameters(1.5,0.05,0.05,0,0);
//h->Fit(tnDeltaEta_single);
//c1->SaveAs("DeltaEtaPF460_single.png");
//c1->SaveAs("DeltaEtaPF460_single.C");

//tree->Draw("(hltVBFPFJetCSVSortedMqq460Detaqq4p1>=4):bDetaqq_single >> h(50,0,10)"," (HLT_DiPFJetAve60_v2 || HLT_DiPFJetAve40_v2 || HLT_DiPFJetAve60_v2 || HLT_QuadPFJet_VBF_v3) && (hltQuadJet15>=4) && (hltTripleJet50>=3) && (hltDoubleJet65>=2) && (hltSingleJet80>=0) && (hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (hltCSVL30p74>=1) && (hltPFQuadJetLooseID15>=4) && (hltPFTripleJetLooseID64>=3) && (hltPFDoubleJetLooseID76>=2) && (hltPFSingleJetLooseID92>=1) && (hltCSVPF0p78>=1) && (hltVBFPFJetCSVSortedMqq460Detaqq4p1>=0) && bDphibb_single<1.5 ","prof");
//h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("");
//h->GetXaxis()->SetTitle("#Delta #phi (bb)");
//TF1* tnDeltaPhi_single = (TF1*) turnonDphi->Clone("tnDeltaPhi_single");
//tnDeltaPhi_single->SetParameters(1.5,0.05,0.05,0,0);
//h->Fit(tnDeltaPhi_single);
//c1->SaveAs("DeltaPhiPF460_single.png");
//c1->SaveAs("DeltaPhiPF460_single.C");

tnCaloPt4->Write();
tnCaloPt3->Write();
tnCaloPt2->Write();
tnCaloPt1->Write();
tn2D_eta->Write();
tnPFPt4->Write();
tnPFPt3->Write();
tnPFPt2->Write();
tnPFPt1->Write();
tnCaloCSV1->Write();

tnPFCSV2_double->Write();
tnPFCSV1_double->Write();
tn2D_double->Write();

tnPFCSV1_single->Write();
tn2D_single->Write();

file->Write();
file->Close();

ofstream myfile;
myfile.open ("fittedFunctions.h");

myfile << "float tnL1Pt1PtPt3(float x){\n\treturn "<< tnL1Pt1PtPt3->GetExpFormula("P") <<" ; }\n\n";

myfile << "float tnCaloPt4(float x){\n\treturn "<< tnCaloPt4->GetExpFormula("P") <<" ; }\n\n";
myfile << "float tnCaloPt3(float x){\n\treturn "<< tnCaloPt3->GetExpFormula("P") <<" ; }\n\n";
myfile << "float tnCaloPt2(float x){\n\treturn "<< tnCaloPt2->GetExpFormula("P") <<" ; }\n\n";
myfile << "float tnCaloPt1(float x){\n\treturn "<< tnCaloPt1->GetExpFormula("P") <<" ; }\n\n";

myfile << "float tnCaloCSV1(float x){\n\treturn "<< tnCaloCSV1->GetExpFormula("P") <<" ; }\n\n";

myfile << "float tnPFPt4(float x){\n\treturn "<< tnPFPt4->GetExpFormula("P") <<" ; }\n\n";
myfile << "float tnPFPt3(float x){\n\treturn "<< tnPFPt3->GetExpFormula("P") <<" ; }\n\n";
myfile << "float tnPFPt2(float x){\n\treturn "<< tnPFPt2->GetExpFormula("P") <<" ; }\n\n";
myfile << "float tnPFPt1(float x){\n\treturn "<< tnPFPt1->GetExpFormula("P") <<" ; }\n\n";

//myfile << "float tnDeltaEtaCalo(float x){\n\treturn "<< tnDeltaEtaCalo->GetExpFormula("P") <<" ; }\n\n";
myfile << "float tn2D_eta(float x, float y){\n\treturn "<< tn2D_double->GetExpFormula("P") <<" ; }\n\n";


myfile << "float tnPFCSV2_double(float x){\n\treturn "<< tnPFCSV2_double->GetExpFormula("P") <<" ; }\n\n";
myfile << "float tnPFCSV1_double(float x){\n\treturn "<< tnPFCSV1_double->GetExpFormula("P") <<" ; }\n\n";
myfile << "float tn2D_double(float x, float y){\n\treturn "<< tn2D_double->GetExpFormula("P") <<" ; }\n\n";

myfile << "float tnPFCSV1_single(float x){\n\treturn "<< tnPFCSV1_single->GetExpFormula("P") <<" ; }\n\n";
myfile << "float tn2D_single(float x, float y){\n\treturn "<< tn2D_single->GetExpFormula("P") <<" ; }\n\n";

myfile << "float SingleBtagVBFTriggerWeight(float pt1, float pt2, float pt3, float pt4 , float CSV1, float DeltaEtaqq_eta, float Mqq_eta, float DeltaPhibb_single, float DeltaEtaqq_single){\n\treturn tnL1Pt1PtPt3(pt1+pt2+pt3)*tnCaloPt4(pt4)*tnPFPt4(pt4)*tnCaloPt3(pt3)*tnPFPt3(pt3)*tnCaloPt2(pt2)*tnPFPt2(pt2)*tnCaloPt1(pt1)*tnCaloCSV1(CSV1)*tn2D_eta(DeltaEtaqq_eta,Mqq_eta)*tnPFCSV1_single(CSV1)*tn2D_single(DeltaPhibb_single,DeltaEtaqq_single) ; }\n\n";

myfile << "float DoubleBtagVBFTriggerWeight(float pt1, float pt2, float pt3, float pt4 , float CSV1, float CSV2 , float DeltaEtaqq_eta, float Mqq_eta, float DeltaEtaqq_double, float Mqq_double){\n\treturn tnL1Pt1PtPt3(pt1+pt2+pt3)*tnCaloPt4(pt4)*tnPFPt4(pt4)*tnCaloPt3(pt3)*tnPFPt3(pt3)*tnCaloPt2(pt2)*tnPFPt2(pt2)*tnCaloPt1(pt1)*tnCaloCSV1(CSV1)*tn2D_eta(DeltaEtaqq_eta,Mqq_eta)*tnPFCSV1_double(CSV1)*tnPFCSV2_double(CSV2)*tn2D_double(DeltaEtaqq_double,Mqq_double) ; }\n\n";

myfile << "float PrescaledBtagVBFTriggerWeight(float pt1, float pt2, float pt3, float pt4 ,float DeltaEtaqq_eta, float Mqq_eta){\n\treturn tnL1Pt1PtPt3(pt1+pt2+pt3)*tnCaloPt4(pt4)*tnPFPt4(pt4)*tnCaloPt3(pt3)*tnPFPt3(pt3)*tnCaloPt2(pt2)*tnPFPt2(pt2)*tnCaloPt1(pt1)*tn2D_eta(DeltaEtaqq_eta,Mqq_eta) ; }\n\n";

myfile << "float DoubleBtagVBFTriggerWeightNoCommonPart(float CSV1, float CSV2 , float DeltaEtaqq_double, float Mqq_double){\n\treturn tnCaloCSV1(CSV1)*tnPFCSV1_double(CSV1)*tnPFCSV2_double(CSV2)*tn2D_double(DeltaEtaqq_double,Mqq_double) ; }\n\n";

myfile << "float SingleBtagVBFTriggerWeightNoCommonPart(float CSV1, float DeltaPhibb_single, float DeltaEtaqq_single){\n\treturn tnCaloCSV1(CSV1)*tnPFCSV1_single(CSV1)*tn2D_single(DeltaPhibb_single,DeltaEtaqq_single) ; }\n\n";

myfile.close();


}

