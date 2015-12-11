TH2F* getGraph2DError(TEfficiency* efficiency,int nx, float xmin, float xmax, int ny=0, float ymin=0, float ymax=0){
    TH2F* output =  (TH2F*) efficiency->CreateHistogram();
    for (int x= 0; x<output->GetNbinsX(); x++){
        for (int y= 0; y<output->GetNbinsX(); y++){
            int bin = efficiency->GetGlobalBin(x,y);
            float value = efficiency->GetEfficiency(bin);
            float value_up = efficiency->GetEfficiencyErrorUp(bin);
            float value_down = efficiency->GetEfficiencyErrorLow(bin);
            float error = (value_up+value_down)*0.5;
            output->SetBinError(bin,error);
//            cout<< output->GetBinContent(bin) <<"\t" << value <<"\t"<<bin<<endl;
        }
    }
    return output;
//    GetGlobalBin
//    FindFixBin
//    SetPointError
}

void doFit(TF1* function,TEfficiency* efficiency,float xmin, float xmax, string fileName, TCanvas* c1){
    function->SetRange(xmin,xmax);
    efficiency->Draw("");
    efficiency->Fit(function);
    c1->SaveAs((fileName+".png").c_str());
//    c1->SaveAs((fileName+".C").c_str());
    c1->SaveAs((fileName+".root").c_str());
}

void doFit(TF2* function,TH2F* efficiency,float xmin, float xmax,float ymin, float ymax, string fileName, TCanvas* c1){
    function->SetRange(xmin,ymin,xmax,ymax);
    efficiency->Draw("COLZ");
    efficiency->Fit(function);
    c1->SaveAs((fileName+".png").c_str());
//    c1->SaveAs((fileName+".C").c_str());
    c1->SaveAs((fileName+".root").c_str());
    function->SetMaximum(1);
    function->SetMinimum(0);
    function->Draw("COLZ");
    c1->SaveAs((fileName+"_function.png").c_str());
}

TEfficiency* getHisto(TTree* tree, string draw, int nx, float xmin, float xmax, string selection, string trigger, string title, string option="", int ny=0, float ymin=0, float ymax=0){
    selection = string("(")+selection+")";
    gStyle->SetOptFit(0);
    gStyle->SetOptStat(0);
    string binning;
    if(ny==0) binning = string("(") + std::to_string(nx) + "," + std::to_string(xmin) + "," +std::to_string(xmax) + ")";
    else binning = string("(") + std::to_string(nx) + "," + std::to_string(xmin) + "," +std::to_string(xmax) + "," + std::to_string(ny) + "," + std::to_string(ymin) + "," +std::to_string(ymax) + ")";
    tree->Draw( (draw + ">> num" + binning).c_str(), (selection + "&&" + trigger).c_str() , option.c_str() );
    tree->Draw( (draw + ">> den" + binning).c_str(), (selection).c_str() , option.c_str() );
    cout << (draw + ">> num" + binning).c_str() <<endl;
    cout << (draw + ">> den" + binning).c_str() <<endl;
    cout << (selection).c_str() <<endl;
    cout << (option).c_str() <<endl;
    if(ny==0){
        TH1F* num = (TH1F*) gDirectory->Get("num");
        TH1F* den = (TH1F*) gDirectory->Get("den");
//        cout << num->GetNbinsX() <<endl;
//        cout << den->GetNbinsX() <<endl;
        TEfficiency* eff = new TEfficiency(*num,*den);
        eff->SetTitle(title.c_str());
        return eff;
    } else {
        TH2F* num = (TH2F*) gDirectory->Get("num");
        TH2F* den = (TH2F*) gDirectory->Get("den");
        TEfficiency* eff = new TEfficiency(*num,*den);
        eff->SetTitle(title.c_str());
        return eff;
    }
}

void VBFplots_fit_new(){
    gEnv->SetValue("Hist.Binning.2D.Prof",10);
    gEnv->SetValue("Hist.Binning.3D.Profx",10);
    gEnv->SetValue("Hist.Binning.3D.Profy",10);
    gEnv->SetValue("Hist.Binning.2D.x",10);
    gEnv->SetValue("Hist.Binning.2D.y",10);

    TCanvas* c1 = new TCanvas("c1","c1");
    c1->SetGridx();
    c1->SetGridy();


    gStyle->SetOptFit(0);
    gStyle->SetOptStat(0);
//    gROOT->SetBatch();

    TFile *_file0 = TFile::Open("SingleElectronVBF.root");
    TTree* tree = (TTree*) _file0->Get("tree");

    TFile* file = new TFile("test.root","recreate");

    //L1 cut: Jet_pt[0]>92 && Jet_pt[1]>76 && Jet_pt[2]>64 && abs(Jet_eta)<3
    //Calo cut: Jet_pt[0]>80 && Jet_pt[1]>65 && Jet_pt[2]>50 && Jet_pt[3]>15
    //Calo CSV 0.74
    //PF cut: Jet_pt[0]>92 && Jet_pt[1]>76 && Jet_pt[2]>64 && Jet_pt[3]>15
    //PF CSV 0.78 e 0.58

    //CaloCut: Mqq_eta>150 && Detaqq_eta>1.5
    //PFCut 1-btag: Mqq_1b>460 && Detaqq_1b>4.1 && Dphibb_1b<1.6
    //PFCut 2-btag: Mqq_2b>200 && Detaqq_2b>1.2


    //TF1* turnonPt = new TF1("turnonPt","  [2]/(1+exp(-[1]*(x-[0]))) +[3] ");
    //turnonPt->SetParameters(40,0.01,1,-0.01);
    //TF1* turnonPt = new TF1("turnonPt","(0.5+0.5*erf((x-[0])*(x-[3]>[0])/[1] + (x-[0])*(x-[3]<=[0])/[2] ))*[5]+[4]");
    //TF1* turnonPt = new TF1("turnonPt","(0.5+0.5*erf((x-[0])*(x-[0]>[5])/[1] + (x-[0])*(x-[0]<=[5])/[2] ))*[4]+[3]");
    TF1* turnonPt = new TF1("turnonPt","(0.5+0.5*erf( (x-[0])*(x-[0]>[5])/[1] + (x-[0])*(x-[0]<[5])/[2] + [5]*(1/[1]-1/[2])*(x-[0]<[5]) ))*[4]+[3] ");
    turnonPt->SetRange(-1000,10000);
    turnonPt->SetParameters(70,20,100,0.1,0.9,5);
//    turnonPt->SetParLimits(0,0,10000);
//    turnonPt->SetParLimits(1,0,100);
//    turnonPt->SetParLimits(2,0,100);
//    turnonPt->SetParLimits(3,-0.5,0.5);
//    turnonPt->SetParLimits(4,0,1);
//    turnonPt->SetParLimits(5,-100,100);


    TF2* turnon2D = new TF2("turnonPt","((0.5+0.5*erf((x-[0])/[1]))*[2]+[3])*((0.5+0.5*erf((y-[4])/[5]))*[6]+[7])");
    turnon2D->SetParameters(40,10,1,0,40,10,1,0);
    turnon2D->SetParLimits(2,0,1);
    turnon2D->SetParLimits(3,-1,1);
    turnon2D->SetParLimits(6,0,1);
    turnon2D->SetParLimits(7,-1,1);

    //turnonPt->SetParLimits(0,0,10000);
    //turnonPt->SetParLimits(1,0,100);
    //turnonPt->SetParLimits(2,0,100);
    //turnonPt->SetParLimits(3,-100,100);
    //turnonPt->SetParLimits(4,-0.5,0);
    //turnonPt->SetParLimits(5,0,1);

    //TF1* turnonCSV = new TF1("turnonCSV","[0]+x*[1]+x*x*[2]+x*x*x*[3]");
    //turnonCSV->SetParameters(0,0.5,0.5,0);

    //TF1* turnonCSV = new TF1("turnonCSV","0.5+0.5*erf(((-log(1.00001-x))-[0])/[1])+[2]");
    TF1* turnonCSV = (TF1*) turnonPt->Clone("turnonCSV");
    turnonCSV->SetParameters(2,2,2,0,1,0);

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
    //TTree* tree = (TTree*) tree->CopyTree("(HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30)");
//    /*

    int nx=0, ny=0;
    float xmax=0, xmin=0, ymax=0, ymin=0;
    string filter="", preselection ="", variable="",title="", fileName="";
    TEfficiency* efficiency;

    gStyle->SetOptFit(0);
    gStyle->SetOptStat(0);

///////////////////////////////////////////////////////



    nx=100, xmin=0, xmax=400;
    variable="Jet_pt[0]+Jet_pt[1]+Jet_pt[2]";
    filter="ntrgObjects_hltQuadJet15>=1";
    preselection="HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30";
    title= "L1 trigger turn-on; p^{T}_{1}+p^{T}_{2}+p^{T}_{3} ; Efficiency";
    fileName= "L1Pt1PtPt3";
    TH2F* graph2D;
    efficiency = getHisto(tree,variable,nx,xmin,xmax,preselection,filter,title);
    TF1* tnL1Pt1PtPt3 = (TF1*) turnonPt->Clone("tnL1Pt1PtPt3");
    tnL1Pt1PtPt3->SetParameters(110,75,165,-1,2,30);
    doFit(tnL1Pt1PtPt3,efficiency,xmin,xmax, fileName, c1);

///////////////////////////////////////////////////////
    turnonPt->SetParameters(50,20,12,0,1,12);

    nx=100, xmin=0, xmax=100;
    variable="Jet_pt[3]";
    preselection=preselection+"&&"+filter;
    filter="(ntrgObjects_hltQuadJet15>=4)";
    title= "Calo p^{T}_{4} turn-on; p^{T}_{4} ; Efficiency";
    fileName= "CaloPt4";
    efficiency = getHisto(tree,variable,nx,xmin,xmax,preselection,filter,title);
    TF1* tnCaloPt4 = (TF1*) turnonPt->Clone("tnCaloPt4");
    tnCaloPt4->SetParameters(4,20,160,0,1,2);
    doFit(tnCaloPt4,efficiency,xmin,xmax, fileName, c1);

    nx=100, xmin=0, xmax=200;
    variable="Jet_pt[2]";
    preselection=preselection+"&&"+filter;
    filter="(ntrgObjects_hltTripleJet50>=3)";
    title= "Calo p^{T}_{3} turn-on; p^{T}_{3} ; Efficiency";
    fileName= "CaloPt3";
    efficiency = getHisto(tree,variable,nx,xmin,xmax,preselection,filter,title);
    TF1* tnCaloPt3 = (TF1*) turnonPt->Clone("tnCaloPt3");
    doFit(tnCaloPt3,efficiency,xmin,xmax, fileName, c1);

    nx=50, xmin=60, xmax=160;
    variable="Jet_pt[1]";
    preselection=preselection+"&&"+filter;
    filter="(ntrgObjects_hltDoubleJet65>=2)";
    title= "Calo p^{T}_{2} turn-on; p^{T}_{2} ; Efficiency";
    fileName= "CaloPt2";
    efficiency = getHisto(tree,variable,nx,xmin,xmax,preselection,filter,title);
    TF1* tnCaloPt2 = (TF1*) turnonPt->Clone("tnCaloPt2");
    doFit(tnCaloPt2,efficiency,xmin,xmax, fileName, c1);

    nx=50, xmin=70, xmax=170;
    variable="Jet_pt[0]";
    preselection=preselection+"&&"+filter;
    filter="(ntrgObjects_hltSingleJet80>=1)";
    title= "Calo p^{T}_{1} turn-on; p^{T}_{1} ; Efficiency";
    fileName= "CaloPt1";
    efficiency = getHisto(tree,variable,nx,xmin,xmax,preselection,filter,title);
    TF1* tnCaloPt1 = (TF1*) turnonPt->Clone("tnCaloPt1");
    tnCaloPt1->SetParameters(80,20,160,0,1,2);
    doFit(tnCaloPt1,efficiency,xmin,xmax, fileName, c1);

/////////////////////////////////////////////////////

    nx=50, xmin=100, xmax=600;
    ny=40, ymin=0, ymax=4;
    variable="Detaqq_eta:Mqq_eta";
    preselection=preselection+"&&"+filter;
    filter="ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4";
    title= "Calo VBF cut turn-on; M (qq) ; #Delta#eta (qq)";
    fileName= "2D_eta";
    efficiency = getHisto(tree,variable,nx,xmin,xmax,preselection,filter,title,"",ny,ymin,ymax);
    TF2* tn2D_eta = (TF2*) turnon2D->Clone("tn2D_eta");
    tn2D_eta->SetParameters(150,30,1,0,1.5,0.1,1,0);
    graph2D = getGraph2DError(efficiency,nx,xmin,xmax,ny,ymin,ymax);
    doFit(tn2D_eta,graph2D,xmin,xmax ,ymin,ymax, fileName, c1);

/////////////////////////////////////////////////////

    nx=80, xmin=0, xmax=8;
    ny=0, ymin=0, ymax=0;
    variable="-log(1-CSV[0]+1.e-7)";
    preselection=preselection+"&&"+filter;
    filter="(ntrgObjects_hltCSVL30p74>=1)";
    title= "Calo CSV_{1} turn-on; -Log(1-CSV_{1}) ; Efficiency";
    fileName= "CaloCSV1";
    efficiency = getHisto(tree,variable,nx,xmin,xmax,preselection,filter,title);
    TF1* tnCaloCSV1 = (TF1*) turnonPt->Clone("tnCaloCSV1");
    tnCaloCSV1->SetParameters(-0.4,2.8,10,-2.7,3.7,1.8);
    doFit(tnCaloCSV1,efficiency,xmin,xmax, fileName, c1);

///////////////////////////////////////////////////////


    nx=50, xmin=20, xmax=120;
    variable="Jet_pt[3]";
    preselection=preselection+"&&"+filter;
    filter="(ntrgObjects_hltPFQuadJetLooseID15>=4)";
    title= "PF p^{T}_{4} turn-on; p^{T}_{4} ; Efficiency";
    fileName= "PFPt4";
    efficiency = getHisto(tree,variable,nx,xmin,xmax,preselection,filter,title);
//    TF1* tnPFPt4 = (TF1*) tnPFPt4->Clone("tnPFPt4");
    TF1* tnPFPt4 = (TF1*) tnCaloPt4->Clone("tnPFPt4");
//    tnPFPt4->SetParameters(133,1.7,90,0.1,0.9,5);
    doFit(tnPFPt4,efficiency,xmin,xmax, fileName, c1);

    nx=50, xmin=60, xmax=160;
    variable="Jet_pt[2]";
    preselection=preselection+"&&"+filter;
    filter="(ntrgObjects_hltPFTripleJetLooseID64>=3)";
    title= "PF p^{T}_{3} turn-on; p^{T}_{3} ; Efficiency";
    fileName= "PFPt3";
    efficiency = getHisto(tree,variable,nx,xmin,xmax,preselection,filter,title);
    TF1* tnPFPt3 = (TF1*) turnonPt->Clone("tnPFPt3");
    doFit(tnPFPt3,efficiency,xmin,xmax, fileName, c1);

    nx=50, xmin=70, xmax=170;
    variable="Jet_pt[1]";
    preselection=preselection+"&&"+filter;
    filter="(ntrgObjects_hltPFDoubleJetLooseID76>=2)";
    title= "PF p^{T}_{2} turn-on; p^{T}_{2} ; Efficiency";
    fileName= "PFPt2";
    efficiency = getHisto(tree,variable,nx,xmin,xmax,preselection,filter,title);
    TF1* tnPFPt2 = (TF1*) turnonPt->Clone("tnPFPt2");
    tnPFPt2->SetParameters(73,20,80,0.1,0.9,6.5);
    doFit(tnPFPt2,efficiency,xmin,xmax, fileName, c1);

    nx=50, xmin=80, xmax=180;
    variable="Jet_pt[0]";
    preselection=preselection+"&&"+filter;
    filter="(ntrgObjects_hltPFSingleJetLooseID92>=1)";
    title= "PF p^{T}_{1} turn-on; p^{T}_{1} ; Efficiency";
    fileName= "PFPt1";
    efficiency = getHisto(tree,variable,nx,xmin,xmax,preselection,filter,title);
    TF1* tnPFPt1 = (TF1*) turnonPt->Clone("tnPFPt1");
    tnPFPt1->SetParameters(100,16,100,0.4,0.5,-9);
    doFit(tnPFPt1,efficiency,xmin,xmax, fileName, c1);

//////////////////////////////////////////////////

    string preselectionCommon=preselection+"&&"+filter;
    _file0 = TFile::Open("JetHTVBF.root");
    tree = (TTree*) _file0->Get("tree");

    string old("HLT_BIT_HLT_Ele23_WPLoose_Gsf_v");
    string new_("HLT_BIT_HLT_QuadPFJet_VBF_v");
    preselectionCommon.find(old);
    preselectionCommon.replace(preselectionCommon.find(old),preselectionCommon.find(old)+old.length(),new_);
///////////////////////////////////////////////////////

    nx=80, xmin=0, xmax=8;
    ny=0, ymin=0, ymax=0;
    variable="-log(1-CSV[1]+1.e-7)";
    preselection=preselectionCommon;
    filter="(ntrgObjects_hltDoubleCSVPF0p58>=2)";
    title= "PF CSV_{2} turn-on; -Log(1-CSV_{2}) ; Efficiency";
    fileName= "PFCSV2_double";
    efficiency = getHisto(tree,variable,nx,xmin,xmax,preselection,filter,title);
    TF1* tnPFCSV2_double = (TF1*) turnonPt->Clone("tnPFCSV2_double");
    tnPFCSV2_double->SetParameters(3,1.5,1.5,0.1,1,10);
    doFit(tnPFCSV2_double,efficiency,xmin,xmax, fileName, c1);

    nx=80, xmin=0, xmax=8;
    ny=0, ymin=0, ymax=0;
    variable="-log(1-CSV[0]+1.e-7)";
    preselection=preselection+"&&"+filter;
    filter="(ntrgObjects_hltCSVPF0p78>=1)";
    title= "PF CSV_{1} turn-on; -Log(1-CSV_{1}) ; Efficiency";
    fileName= "PFCSV1_double";
    efficiency = getHisto(tree,variable,nx,xmin,xmax,preselection,filter,title);
    TF1* tnPFCSV1_double = (TF1*) turnonPt->Clone("tnPFCSV1_double");
    tnPFCSV1_double->SetParameters(1.3,1.4,5,0.5,0.4,0.001);
    doFit(tnPFCSV1_double,efficiency,xmin,xmax, fileName, c1);

    nx=40, xmin=0, xmax=4;
    ny=50, ymin=100, ymax=600;
    variable="Mqq_2b:Detaqq_2b";
    preselection=preselection+"&&"+filter;
    filter="ntrgObjects_hltVBFPFJetCSVSortedMqq200Detaqq1p2>=4";
    title= "PF VBF cut turn-on (double b-tag path); #Delta#eta (qq) ; M (qq)";
    fileName= "2D_double";
    efficiency = getHisto(tree,variable,nx,xmin,xmax,preselection,filter,title,"",ny,ymin,ymax);
    TF2* tn2D_double = (TF2*) turnon2D->Clone("tn2D_double");
    tn2D_double->SetParameters(1.2,0.1,0.6,0.3,200,10,0.6,0.3);
    graph2D = getGraph2DError(efficiency,nx,xmin,xmax,ny,ymin,ymax);
    doFit(tn2D_double,graph2D,xmin,xmax ,ymin,ymax, fileName, c1);

///////////////////////////////////////////////////////

    nx=80, xmin=0, xmax=8;
    ny=0, ymin=0, ymax=0;
    variable="-log(1-CSV[0]+1.e-7)";
    preselection=preselectionCommon;
    filter="(ntrgObjects_hltCSVPF0p78>=1)";
    title= "PF CSV_{1} turn-on; -Log(1-CSV_{1}) ; Efficiency";
    fileName= "PFCSV1_single";
    efficiency = getHisto(tree,variable,nx,xmin,xmax,preselection,filter,title);
    TF1* tnPFCSV1_single = (TF1*) turnonPt->Clone("tnPFCSV1_single");
    tnPFCSV1_single->SetParameters(1.7,1.5,0.8,0.5,0.5,0.2);
    doFit(tnPFCSV1_single,efficiency,xmin,xmax, fileName, c1);

    nx=48, xmin=0, xmax=3.2;
    ny=24, ymin=0, ymax=6;
    variable="Detaqq_1b:Dphibb_1b";
    preselection=preselection+"&&"+filter;
    filter="ntrgObjects_hltVBFPFJetCSVSortedMqq460Detaqq4p1>=4";
    title= "PF VBF cut turn-on (single b-tag path); #Delta#phi (bb) ; #Delta#eta (qq)";
    fileName= "2D_single";
    efficiency = getHisto(tree,variable,nx,xmin,xmax,preselection,filter,title,"",ny,ymin,ymax);
    TF2* tn2D_single = (TF2*) turnon2D->Clone("tn2D_single");
    tn2D_single->SetParameters(1.55,-0.02,0.67,0.06,4.15,0.27,73,0.001);
    graph2D = getGraph2DError(efficiency,nx,xmin,xmax,ny,ymin,ymax);
    doFit(tn2D_single,graph2D,xmin,xmax ,ymin,ymax, fileName, c1);

////////////////////////////////////////////////

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

////////////////////////////////////////////////

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
    myfile << "float tn2D_eta(float x, float y){\n\treturn "<< tn2D_eta->GetExpFormula("P") <<" ; }\n\n";

    myfile << "float tnPFCSV2_double(float x){\n\treturn "<< tnPFCSV2_double->GetExpFormula("P") <<" ; }\n\n";
    myfile << "float tnPFCSV1_double(float x){\n\treturn "<< tnPFCSV1_double->GetExpFormula("P") <<" ; }\n\n";
    myfile << "float tn2D_double(float x, float y){\n\treturn "<< tn2D_double->GetExpFormula("P") <<" ; }\n\n";

    myfile << "float tnPFCSV1_single(float x){\n\treturn "<< tnPFCSV1_single->GetExpFormula("P") <<" ; }\n\n";
    myfile << "float tn2D_single(float x, float y){\n\treturn "<< tn2D_single->GetExpFormula("P") <<" ; }\n\n";

    myfile << "float SingleBtagVBFTriggerWeight(float pt1, float pt2, float pt3, float pt4 , float CSV1, float DeltaEtaqq_eta, float Mqq_eta, float DeltaPhibb_single, float DeltaEtaqq_single){\n\tif(isnan(CSV1)) CSV1=0;\n\tCSV1=CSV1>1?1:CSV1;CSV1=CSV1<0?0:CSV1;\n\treturn tnL1Pt1PtPt3(pt1+pt2+pt3)*tnCaloPt4(pt4)*tnPFPt4(pt4)*tnCaloPt3(pt3)*tnPFPt3(pt3)*tnCaloPt2(pt2)*tnPFPt2(pt2)*tnCaloPt1(pt1)*tnPFPt1(pt1)*tnCaloCSV1(-log(1-CSV1+1.e-7))*tn2D_eta(Mqq_eta,DeltaEtaqq_eta)*tnPFCSV1_single(-log(1-CSV1+1.e-7))*tn2D_single(DeltaPhibb_single,DeltaEtaqq_single) ; }\n\n";

    myfile << "float DoubleBtagVBFTriggerWeightBeta(float pt1, float pt2, float pt3, float CSV1, float CSV2 , float DeltaEtaqq_eta, float Mqq_eta, float DeltaEtaqq_double, float Mqq_double){\n\tif(isnan(CSV2)) CSV2=0;\n\tCSV2=CSV2>1?1:CSV2;CSV2=CSV2<0?0:CSV2;\n\tif(isnan(CSV1)) CSV1=0;\n\tCSV1=CSV1>1?1:CSV1;CSV1=CSV1<0?0:CSV1;\n\treturn tnL1Pt1PtPt3(pt1+pt2+pt3)*tnCaloPt3(pt3)*tnPFPt3(pt3)*tnCaloPt2(pt2)*tnPFPt2(pt2)*tnCaloPt1(pt1)*tnPFPt1(pt1)*tnCaloCSV1(-log(1-CSV1+1.e-7))*tn2D_eta(Mqq_eta,DeltaEtaqq_eta)*tnPFCSV1_double(-log(1-CSV1+1.e-7))*tnPFCSV2_double(-log(1-CSV2))*tn2D_double(DeltaEtaqq_double,Mqq_double) ; }\n\n";

    myfile << "float DoubleBtagVBFTriggerWeight(float pt1, float pt2, float pt3, float pt4 , float CSV1, float CSV2 , float DeltaEtaqq_eta, float Mqq_eta, float DeltaEtaqq_double, float Mqq_double){\n\tif(isnan(CSV2)) CSV2=0;\n\tCSV2=CSV2>1?1:CSV2;CSV2=CSV2<0?0:CSV2;\n\tif(isnan(CSV1)) CSV1=0;\n\tCSV1=CSV1>1?1:CSV1;CSV1=CSV1<0?0:CSV1;\n\treturn tnL1Pt1PtPt3(pt1+pt2+pt3)*tnCaloPt4(pt4)*tnPFPt4(pt4)*tnCaloPt3(pt3)*tnPFPt3(pt3)*tnCaloPt2(pt2)*tnPFPt2(pt2)*tnCaloPt1(pt1)*tnPFPt1(pt1)*tnCaloCSV1(-log(1-CSV1+1.e-7))*tn2D_eta(Mqq_eta,DeltaEtaqq_eta)*tnPFCSV1_double(-log(1-CSV1+1.e-7))*tnPFCSV2_double(-log(1-CSV2))*tn2D_double(DeltaEtaqq_double,Mqq_double) ; }\n\n";

    myfile << "float PrescaledBtagVBFTriggerWeight(float pt1, float pt2, float pt3, float pt4 ,float DeltaEtaqq_eta, float Mqq_eta){\n\treturn tnL1Pt1PtPt3(pt1+pt2+pt3)*tnCaloPt4(pt4)*tnPFPt4(pt4)*tnCaloPt3(pt3)*tnPFPt3(pt3)*tnCaloPt2(pt2)*tnPFPt2(pt2)*tnCaloPt1(pt1)*tnPFPt1(pt1)*tn2D_eta(Mqq_eta,DeltaEtaqq_eta) ; }\n\n";

    myfile << "float DoubleBtagVBFTriggerWeightNoCommonPart(float CSV1, float CSV2 , float DeltaEtaqq_double, float Mqq_double){\n\treturn tnPFCSV1_double(-log(1-CSV1+1.e-7))*tnPFCSV2_double(-log(1-CSV2))*tn2D_double(DeltaEtaqq_double,Mqq_double) ; }\n\n";

    myfile << "float SingleBtagVBFTriggerWeightNoCommonPart(float CSV1, float DeltaPhibb_single, float DeltaEtaqq_single){\n\treturn tnPFCSV1_single(-log(1-CSV1+1.e-7))*tn2D_single(DeltaPhibb_single,DeltaEtaqq_single) ; }\n\n";

    myfile.close();
}


//    gEnv->SetValue("Hist.Binning.2D.y",32);
//    gEnv->SetValue("Hist.Binning.2D.x",15);
//    tree->Draw("(ntrgObjects_hltVBFPFJetCSVSortedMqq460Detaqq4p1>=4):Detaqq_1b:Dphibb_1b >> h(,0,3.2,,0,6)"," (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=1) && (ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (ntrgObjects_hltCSVL30p74>=1) && (ntrgObjects_hltPFQuadJetLooseID15>=4) && (ntrgObjects_hltPFTripleJetLooseID64>=3) && (ntrgObjects_hltPFDoubleJetLooseID76>=2) && (ntrgObjects_hltPFSingleJetLooseID92>=1) && (ntrgObjects_hltCSVPF0p78>=1) && (ntrgObjects_hltVBFPFJetCSVSortedMqq460Detaqq4p1>=0)","prof,COLZ");
//    h->GetYaxis()->SetTitle("#Delta#eta (qq)");h->SetTitle("PF VBF cut turn-on (single b-tag path)");
//    h->GetXaxis()->SetTitle("#Delta#phi (bb)");
//    TF2* tn2D_single = (TF2*) turnon2D->Clone("tn2D_single");
//    tn2D_single->SetRange(0,0,3.2,6);
//    tn2D_single->SetParameters(1.6,-0.005,0.95,0.11,4.0,0.003,0.85,0.001);
//    //tn2D_double->SetParameters(200,30,30,0,0);
//    h->Fit(tn2D_single);
//    c1->SaveAs("tn2D_single.png");
//    c1->SaveAs("tn2D_single.C");

//    tn2D_single->SetMaximum(1);
//    tn2D_single->SetMinimum(0);
//    tn2D_single->Draw("COLZ");
//    c1->SaveAs("tn2D_single_funct.png");
//    c1->SaveAs("tn2D_single_funct.C");


//    tnL1Pt1PtPt3->SetRange(xmin,xmax);
//    efficiency->Draw();
//    efficiency->Fit(tnL1Pt1PtPt3);
//    c1->SaveAs((fileName+".png").c_str());
//    c1->SaveAs((fileName+".C").c_str());


        //    tree->Draw("(ntrgObjects_hltQuadJet15>=4):Jet_pt[3] >> h(160,0,160)"," (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30) && (ntrgObjects_hltQuadJet15>=0)","prof");
//    h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("Calo p^{T}_{4} turn-on");
//    h->GetXaxis()->SetTitle("p^{T}_{4}");
//    TF1* tnCaloPt4 = (TF1*) turnonPt->Clone("tnCaloPt4");
//    h->Fit(tnCaloPt4,"","",20,2000);
//    c1->SaveAs("CaloPt4.png");
//    c1->SaveAs("CaloPt4.C");

//    tree->Draw("(ntrgObjects_hltTripleJet50>=3):Jet_pt[2] >> h(160,0,160)"," (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=0) ","prof");
//    h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("");
//    h->GetXaxis()->SetTitle("p^{T}_{3}");
//    TF1* tnCaloPt3 = (TF1*) turnonPt->Clone("Calo p^{T}_{3} turn-on");
//    tnCaloPt3->SetParameters(50,20,12,0,1,12);
//    h->Fit(tnCaloPt3,"","",30,2000);
//    c1->SaveAs("CaloPt3.png");
//    c1->SaveAs("CaloPt3.C");

//    tree->Draw("(ntrgObjects_hltDoubleJet65>=2):Jet_pt[1] >> h(160,0,160)"," (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=0) ","prof");
//    h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("Calo p^{T}_{2} turn-on");
//    h->GetXaxis()->SetTitle("p^{T}_{2}");
//    TF1* tnCaloPt2 = (TF1*) turnonPt->Clone("tnCaloPt2");
//    h->Fit(tnCaloPt2,"","",50,2000);
//    c1->SaveAs("CaloPt2.png");
//    c1->SaveAs("CaloPt2.C");

//    tree->Draw("(ntrgObjects_hltSingleJet80>=1):Jet_pt[0] >> h(160,0,160)"," (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=0) ","prof");
//    h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("Calo p^{T}_{1} turn-on");
//    h->GetXaxis()->SetTitle("p^{T}_{1}");
//    TF1* tnCaloPt1 = (TF1*) turnonPt->Clone("tnCaloPt1");
//    h->Fit(tnCaloPt1,"","",60,2000);
//    c1->SaveAs("CaloPt1.png");
//    c1->SaveAs("CaloPt1.C");

//    //tree->Draw("(ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4):MaxIf$(offJet_eta,Jet_pt>30)-MinIf$(offJet_eta,Jet_pt>30) >> h(100,0,5)"," (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=1) && (ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=0) && Mqq_single>250","prof");
//    //h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("");
//    //h->GetXaxis()->SetTitle("#Delta #eta (qq)");
//    //TF1* tnDeltaEtaCalo = (TF1*) turnonPt->Clone("tnDeltaEtaCalo");
//    //tnDeltaEtaCalo->SetParameters(1.5,0.05,0.05,0,0);
//    //h->Fit(tnDeltaEtaCalo);
//    //c1->SaveAs("DeltaEtaCalo.png");
//    //c1->SaveAs("DeltaEtaCalo.C");

//    //FIXME: we should use as variables Mqq_eta:Detaqq_eta !!
//    tree->Draw("(ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4):Detaqq_eta:Mqq_eta >> h(50,100,600,40,0,4)"," (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30 ) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=1) && (ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=0)","prof,COLZ");
//    //tree->Draw("(ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4):Detaqq_eta:Mqq_eta >> h(20,0,800,60,0,6)"," (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30 ) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=1) && (ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=0)","prof,COLZ");
//    h->GetYaxis()->SetTitle("#Delta#eta (qq)");h->SetTitle("Calo VBF cut turn-on");
//    h->GetXaxis()->SetTitle("M (qq)");
//    TF2* tn2D_eta = (TF2*) turnon2D->Clone("tn2D_eta");
//    tn2D_eta->SetRange(100,0,600,4);
//    tn2D_eta->SetParameters(150,30,1,0,1.5,0.1,1,0);
//    h->Fit(tn2D_eta);
//    c1->SaveAs("tn2D_eta.png");
//    c1->SaveAs("tn2D_eta.C");

//    tn2D_eta->SetMaximum(1);
//    tn2D_eta->SetMinimum(0);
//    tn2D_eta->Draw("COLZ");
//    c1->SaveAs("tn2D_eta_funct.png");
//    c1->SaveAs("tn2D_eta_funct.C");


//    //tree->Draw("(ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4):Mqq_eta >> h(20,0,800)"," (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30 ) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=1) && (ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=0) && Detaqq_eta>1.6","prof,COLZ");
//    //h->GetYaxis()->SetTitle("#Delta#eta (qq)");h->SetTitle("Calo VBF cut turn-on");
//    //h->GetXaxis()->SetTitle("M (qq)");
//    ////TF2* tn2D_eta = (TF2*) turnon2D->Clone("tn2D_eta");
//    ////tn2D_eta->SetRange(0,0,4,400);
//    ////tn2D_eta->SetParameters(1.2,0.1,0.6,0.3,200,10,0.6,0.3);
//    ////h->Fit(tn2D_eta);
//    //c1->SaveAs("tnMqq_eta.png");
//    //c1->SaveAs("tnMqq_eta.C");

//    //tree->Draw("(ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4):Detaqq_eta >> h(80,0,8)"," (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30 ) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=1) && (ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=0) && Mqq_eta>1.6","prof,COLZ");
//    //h->GetYaxis()->SetTitle("#Delta#eta (qq)");h->SetTitle("Calo VBF cut turn-on");
//    //h->GetXaxis()->SetTitle("M (qq)");
//    ////TF2* tn2D_eta = (TF2*) turnon2D->Clone("tn2D_eta");
//    ////tn2D_eta->SetRange(0,0,4,400);
//    ////tn2D_eta->SetParameters(1.2,0.1,0.6,0.3,200,10,0.6,0.3);
//    ////h->Fit(tn2D_eta);
//    //c1->SaveAs("tnDetaqq_eta.png");
//    //c1->SaveAs("tnDetaqq_eta.C");

//    tree->Draw("ntrgObjects_hltCSVL30p74>0:-log(1-CSV[0]) >> h(80,0,8)","(HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=1) && (ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (ntrgObjects_hltCSVL30p74>=0) ","prof");
//    h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("Calo CSV1 turn-on");
//    h->GetXaxis()->SetTitle("CSV");
//    TF1* tnCaloCSV1 = (TF1*) turnonCSV->Clone("tnCaloCSV1");
//    //tnCaloCSV1->SetParameters(1.5,0.05,0.05,0,0);
//    h->Fit(tnCaloCSV1,"","",0.2,2000);
//    c1->SaveAs("CaloCSV1.png");
//    c1->SaveAs("CaloCSV1.C");

//    tree->Draw("(ntrgObjects_hltPFQuadJetLooseID15>=4):Jet_pt[3] >> h(160,0,160)"," (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=1) && (ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (ntrgObjects_hltCSVL30p74>=1) && (ntrgObjects_hltPFQuadJetLooseID15>=0) ","prof");
//    h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("PF p^{T}_{4} turn-on");
//    h->GetXaxis()->SetTitle("p^{T}_{4}");
//    TF1* tnPFPt4 = (TF1*) turnonPt->Clone("tnPFPt4");
//    tnPFPt4->SetParameters(20,10,10,0,1,0);
//    h->Fit(tnPFPt4,"","",20,2000);
//    c1->SaveAs("PFPt4.png");
//    c1->SaveAs("PFPt4.C");

//    tree->Draw("(ntrgObjects_hltPFTripleJetLooseID64>=3):Jet_pt[2] >> h(160,0,160)"," (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=1) && (ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (ntrgObjects_hltCSVL30p74>=1) && (ntrgObjects_hltPFQuadJetLooseID15>=4) && (ntrgObjects_hltPFTripleJetLooseID64>=0)","prof");
//    h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("PF p^{T}_{3} turn-on");
//    h->GetXaxis()->SetTitle("p^{T}_{3}");
//    TF1* tnPFPt3 = (TF1*) turnonPt->Clone("tnPFPt3");
//    h->Fit(tnPFPt3,"","",45,2000);
//    c1->SaveAs("PFPt3.png");
//    c1->SaveAs("PFPt3.C");

//    tree->Draw("(ntrgObjects_hltPFDoubleJetLooseID76>=2):Jet_pt[1] >> h(160,0,160)"," (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=1) && (ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (ntrgObjects_hltCSVL30p74>=1) && (ntrgObjects_hltPFQuadJetLooseID15>=4) && (ntrgObjects_hltPFTripleJetLooseID64>=3) && (ntrgObjects_hltPFDoubleJetLooseID76>=0)","prof");
//    h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("PF p^{T}_{2} turn-on");
//    h->GetXaxis()->SetTitle("p^{T}_{2}");
//    TF1* tnPFPt2 = (TF1*) turnonPt->Clone("tnPFPt2");
//    h->Fit(tnPFPt2,"","",65,2000);
//    c1->SaveAs("PFPt2.png");
//    c1->SaveAs("PFPt2.C");

//    tree->Draw("(ntrgObjects_hltPFSingleJetLooseID92>=1):Jet_pt[0] >> h(160,0,160)"," (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=1) && (ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (ntrgObjects_hltCSVL30p74>=1) && (ntrgObjects_hltPFQuadJetLooseID15>=4) && (ntrgObjects_hltPFTripleJetLooseID64>=3) && (ntrgObjects_hltPFDoubleJetLooseID76>=2) && (ntrgObjects_hltPFSingleJetLooseID92>=0) ","prof");
//    h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("PF p^{T}_{1} turn-on");
//    h->GetXaxis()->SetTitle("p^{T}_{1}");
//    TF1* tnPFPt1 = (TF1*) turnonPt->Clone("tnPFPt1");
//    h->Fit(tnPFPt1,"","",80,2000);
//    c1->SaveAs("PFPt1.png");
//    c1->SaveAs("PFPt1.C");

//    ////////////////////////////////////////////
//    //// Load JetHT dataset ////////////////////
//    ////////////////////////////////////////////

//    //_file0 = TFile::Open("JetHTVBF.root");
//    //tree = (TTree*) _file0->Get("tree");


//    //tree->Draw("pfJet_ntrgObjects_hltCSVPF0p78>0:Jet_btagCSV[pfJet_offmatch] >> h(100,0,1)","pfJet_offmatch>=0 && (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=1) && (ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (ntrgObjects_hltCSVL30p74>=1) && (ntrgObjects_hltPFQuadJetLooseID15>=4) && (ntrgObjects_hltPFTripleJetLooseID64>=3) && (ntrgObjects_hltPFDoubleJetLooseID76>=2) && (ntrgObjects_hltPFSingleJetLooseID92>=1) ","prof");
//    //h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("");
//    //h->GetXaxis()->SetTitle("CSV");
//    //c1->SaveAs("PFCSV1.png");
//    //c1->SaveAs("PFCSV1.C");

//    //tree->Draw("pfJet_ntrgObjects_hltDoubleCSVPF0p58>0:Jet_btagCSV[pfJet_offmatch] >> h(100,0,1)","pfJet_offmatch>=0 && (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=1) && (ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (ntrgObjects_hltCSVL30p74>=1) && (ntrgObjects_hltPFQuadJetLooseID15>=4) && (ntrgObjects_hltPFTripleJetLooseID64>=3) && (ntrgObjects_hltPFDoubleJetLooseID76>=2) && (ntrgObjects_hltPFSingleJetLooseID92>=1) ","prof");
//    //h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("");
//    //h->GetXaxis()->SetTitle("CSV");
//    //c1->SaveAs("PFCSV2.png");
//    //c1->SaveAs("PFCSV2.C");

//    //Double CSV path ntrgObjects_hltDoubleCSVPF0p58, ntrgObjects_hltCSVPF0p78, ntrgObjects_hltVBFPFJetCSVSortedMqq200Detaqq1p2

//    tree->Draw("ntrgObjects_hltDoubleCSVPF0p58>=2:-log(1-CSV[1]) >> h(40,0,8)","(HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=1) && (ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (ntrgObjects_hltCSVL30p74>=1) && (ntrgObjects_hltPFQuadJetLooseID15>=4) && (ntrgObjects_hltPFTripleJetLooseID64>=3) && (ntrgObjects_hltPFDoubleJetLooseID76>=2) && (ntrgObjects_hltPFSingleJetLooseID92>=1) && (ntrgObjects_hltDoubleCSVPF0p58>=0) ","prof");
//    h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("PF CSV2 turn-on (double b-tag path)");
//    h->GetXaxis()->SetTitle("CSV");
//    TF1* tnPFCSV2_double = (TF1*) turnonCSV->Clone("tnPFCSV2_double");
//    //tnPFCSV2_double->SetParameters(1.5,0.05,0.05,0,0);
//    h->Fit(tnPFCSV2_double,"","",0.2,2000);
//    c1->SaveAs("PFCSV2_double.png");
//    c1->SaveAs("PFCSV2_double.C");

//    tree->Draw("ntrgObjects_hltCSVPF0p78>=1:-log(1-CSV[0]) >> h(80,0,8)","(HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=1) && (ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (ntrgObjects_hltCSVL30p74>=1) && (ntrgObjects_hltPFQuadJetLooseID15>=4) && (ntrgObjects_hltPFTripleJetLooseID64>=3) && (ntrgObjects_hltPFDoubleJetLooseID76>=2) && (ntrgObjects_hltPFSingleJetLooseID92>=1) && (ntrgObjects_hltDoubleCSVPF0p58>=2) && (ntrgObjects_hltCSVPF0p78>=0)","prof");
//    h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("PF CSV1 turn-on (double b-tag path)");
//    h->GetXaxis()->SetTitle("CSV");
//    TF1* tnPFCSV1_double = (TF1*) turnonCSV->Clone("tnPFCSV1_double");
//    //tnPFCSV1_double->SetParameters(1.5,0.05,0.05,0,0);
//    h->Fit(tnPFCSV1_double,"","",0.2,2000);
//    c1->SaveAs("PFCSV1_double.png");
//    c1->SaveAs("PFCSV1_double.C");
//    //*/
//    gEnv->SetValue("Hist.Binning.2D.x",20);
//    tree->Draw("(ntrgObjects_hltVBFPFJetCSVSortedMqq200Detaqq1p2>=4):Mqq_2b:Detaqq_2b >> h(50,0,5,48,0,600)"," (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=1) && (ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (ntrgObjects_hltCSVL30p74>=1) && (ntrgObjects_hltPFQuadJetLooseID15>=4) && (ntrgObjects_hltPFTripleJetLooseID64>=3) && (ntrgObjects_hltPFDoubleJetLooseID76>=2) && (ntrgObjects_hltPFSingleJetLooseID92>=1) && (ntrgObjects_hltDoubleCSVPF0p58>=2) && (ntrgObjects_hltCSVPF0p78>=1) && (ntrgObjects_hltVBFPFJetCSVSortedMqq200Detaqq1p2>=0)","prof,COLZ");
//    h->GetYaxis()->SetTitle("M (qq)");h->SetTitle("PF VBF cut turn-on (double b-tag path)");
//    h->GetXaxis()->SetTitle("#Delta#eta (qq)");
//    TF2* tn2D_double = (TF2*) turnon2D->Clone("tn2D_double");
//    tn2D_double->SetRange(0,0,5,600);
//    tn2D_double->SetParameters(1.2,0.1,0.6,0.3,200,10,0.6,0.3);
//    h->Fit(tn2D_double);
//    c1->SaveAs("tn2D_double.png");
//    c1->SaveAs("tn2D_double.C");

//    tn2D_double->SetMaximum(1);
//    tn2D_double->SetMinimum(0);
//    tn2D_double->Draw("COLZ");
//    c1->SaveAs("tn2D_double_funct.png");
//    c1->SaveAs("tn2D_double_funct.C");


//    //tree->Draw("(ntrgObjects_hltVBFPFJetCSVSortedMqq200Detaqq1p2>=4):Mqq_2b >> h(20,0,400)"," (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=1) && (ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (ntrgObjects_hltCSVL30p74>=1) && (ntrgObjects_hltPFQuadJetLooseID15>=4) && (ntrgObjects_hltPFTripleJetLooseID64>=3) && (ntrgObjects_hltPFDoubleJetLooseID76>=2) && (ntrgObjects_hltPFSingleJetLooseID92>=1) && (ntrgObjects_hltDoubleCSVPF0p58>=2) && (ntrgObjects_hltCSVPF0p78>=1) && (ntrgObjects_hltVBFPFJetCSVSortedMqq200Detaqq1p2>=0) && Detaqq_2b>1.3","prof");
//    //h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("");
//    //h->GetXaxis()->SetTitle("M (qq)");
//    //TF1* tnMqqdouble = (TF1*) turnonPt->Clone("tnMqqdouble");
//    //tnMqqdouble->SetParameters(200,30,30,0,0);
//    //h->Fit(tnMqqdouble);
//    //c1->SaveAs("MqqPF200_double.png");
//    //c1->SaveAs("MqqPF200_double.C");

//    //tree->Draw("(ntrgObjects_hltVBFPFJetCSVSortedMqq200Detaqq1p2>=4):Detaqq_2b >> h(20,0,4)"," (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=1) && (ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (ntrgObjects_hltCSVL30p74>=1) && (ntrgObjects_hltPFQuadJetLooseID15>=4) && (ntrgObjects_hltPFTripleJetLooseID64>=3) && (ntrgObjects_hltPFDoubleJetLooseID76>=2) && (ntrgObjects_hltPFSingleJetLooseID92>=1) && (ntrgObjects_hltDoubleCSVPF0p58>=2) && (ntrgObjects_hltCSVPF0p78>=1) && (ntrgObjects_hltVBFPFJetCSVSortedMqq200Detaqq1p2>=0) && Mqq_double>220","prof");
//    //h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("");
//    //h->GetXaxis()->SetTitle("#Delta #eta (qq)");
//    //TF1* tnDeltaEtadouble = (TF1*) turnonPt->Clone("tnDeltaEtadouble");
//    //tnDeltaEtadouble->SetParameters(1.5,0.05,0.05,0,0);
//    //h->Fit(tnDeltaEtadouble);
//    //c1->SaveAs("DeltaEtaPF200_double.png");
//    //c1->SaveAs("DeltaEtaPF200_double.C");

//    //Single CSV path ntrgObjects_hltDoubleCSVPF0p58, ntrgObjects_hltCSVPF0p78, ntrgObjects_hltVBFPFJetCSVSortedMqq200Detaqq1p2

//    tree->Draw("ntrgObjects_hltCSVPF0p78>=1:-log(1-CSV[0]) >> h(80,0,8)","(HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=1) && (ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (ntrgObjects_hltCSVL30p74>=1) && (ntrgObjects_hltPFQuadJetLooseID15>=4) && (ntrgObjects_hltPFTripleJetLooseID64>=3) && (ntrgObjects_hltPFDoubleJetLooseID76>=2) && (ntrgObjects_hltPFSingleJetLooseID92>=1) && (ntrgObjects_hltCSVPF0p78>=0)","prof");
//    h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("PF CSV1 turn-on (single b-tag path)");
//    h->GetXaxis()->SetTitle("CSV");
//    TF1* tnPFCSV1_single = (TF1*) turnonCSV->Clone("tnPFCSV1_single");
//    //tnPFCSV1_single->SetParameters(1.5,0.05,0.05,0,0);
//    h->Fit(tnPFCSV1_single,"","",0.2,2000);
//    c1->SaveAs("PFCSV1_single.png");
//    c1->SaveAs("PFCSV1_single.C");


//    //tree->Draw("(ntrgObjects_hltVBFPFJetCSVSortedMqq460Detaqq4p1>=4):Dphibb_1b >> h(16,0,3.2)"," (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=1) && (ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (ntrgObjects_hltCSVL30p74>=1) && (ntrgObjects_hltPFQuadJetLooseID15>=4) && (ntrgObjects_hltPFTripleJetLooseID64>=3) && (ntrgObjects_hltPFDoubleJetLooseID76>=2) && (ntrgObjects_hltPFSingleJetLooseID92>=1) && (ntrgObjects_hltCSVPF0p78>=1) && (ntrgObjects_hltVBFPFJetCSVSortedMqq460Detaqq4p1>=0) && Detaqq_1b>4.2 ","prof");
//    //h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("");
//    //h->GetXaxis()->SetTitle("#Delta #eta (qq)");
//    //TF1* tnDeltaEta_single = (TF1*) turnonPt->Clone("tnDeltaEta_single");
//    //tnDeltaEta_single->SetParameters(1.5,0.05,0.05,0,0);
//    //h->Fit(tnDeltaEta_single);
//    //c1->SaveAs("DeltaEtaPF460_single.png");
//    //c1->SaveAs("DeltaEtaPF460_single.C");

//    //tree->Draw("(ntrgObjects_hltVBFPFJetCSVSortedMqq460Detaqq4p1>=4):Detaqq_1b >> h(50,0,10)"," (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v && Alt$(Jet_pt[3],0)>30) && (ntrgObjects_hltQuadJet15>=4) && (ntrgObjects_hltTripleJet50>=3) && (ntrgObjects_hltDoubleJet65>=2) && (ntrgObjects_hltSingleJet80>=1) && (ntrgObjects_hltVBFCaloJetEtaSortedMqq150Deta1p5>=4) && (ntrgObjects_hltCSVL30p74>=1) && (ntrgObjects_hltPFQuadJetLooseID15>=4) && (ntrgObjects_hltPFTripleJetLooseID64>=3) && (ntrgObjects_hltPFDoubleJetLooseID76>=2) && (ntrgObjects_hltPFSingleJetLooseID92>=1) && (ntrgObjects_hltCSVPF0p78>=1) && (ntrgObjects_hltVBFPFJetCSVSortedMqq460Detaqq4p1>=0) && Dphibb_1b<1.5 ","prof");
//    //h->GetYaxis()->SetTitle("Efficiency");h->SetTitle("");
//    //h->GetXaxis()->SetTitle("#Delta #phi (bb)");
//    //TF1* tnDeltaPhi_single = (TF1*) turnonDphi->Clone("tnDeltaPhi_single");
//    //tnDeltaPhi_single->SetParameters(1.5,0.05,0.05,0,0);
//    //h->Fit(tnDeltaPhi_single);
//    //c1->SaveAs("DeltaPhiPF460_single.png");
//    //c1->SaveAs("DeltaPhiPF460_single.C");

