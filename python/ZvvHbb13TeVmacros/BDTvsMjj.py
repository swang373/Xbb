import ROOT

def makeMjjBDTprofPlot(canvas,inputFile, outputFile="testBins.png", variable1="H.mass", variable2="ZvvBDTNoMjj", cut1=-1, cut2=1, nbins=100,xmin=0,xmax=400):
    file_ = ROOT.TFile.Open(inputFile)
    tree = file_.Get("tree")
    assert type(tree) is ROOT.TTree
    tree.Draw("%s:%s >> Bin1(%s,%s,%s)" %(variable2,variable1,nbins,xmin,xmax),"%s>%s && %s<%s" %(variable2,cut1,variable2,cut2),"prof")
    Bin1 = file_.Get("Bin1")

    Bin1.SetLineColor(ROOT.kBlack)
    Bin1.SetLineWidth(2)

    Bin1.SetMaximum(1)
    Bin1.SetMinimum(-1)
#    maxim = 0
#    maxim = max(maxim,Bin1.GetMaximum())

#    Bin1.SetMaximum(maxim*1.2)

    Bin1.Draw("")

    c1.SaveAs(outputFile)

def makeMjjPlots(canvas,inputFile, outputFile="testBins.png", variable="ZvvBDTNoMjj", cut1=-.2, cut2=.2, cut3=0.6, cut4=1., nbins=100,xmin=0,xmax=400):
    file_ = ROOT.TFile.Open(inputFile)
    tree = file_.Get("tree")
    assert type(tree) is ROOT.TTree
    tree.Draw("HCSV_mass >> Bin1(%s,%s,%s)" %(nbins,xmin,xmax),"%s>%s && %s<%s" %(variable,cut1,variable,cut2),"NORM")
    Bin1 = file_.Get("Bin1")
    tree.Draw("HCSV_mass >> Bin2(%s,%s,%s)" %(nbins,xmin,xmax),"%s>%s && %s<%s" %(variable,cut2,variable,cut3),"NORM")
    Bin2 = file_.Get("Bin2")
    tree.Draw("HCSV_mass >> Bin3(%s,%s,%s)" %(nbins,xmin,xmax),"%s>%s && %s<%s" %(variable,cut3,variable,cut4),"NORM")
    Bin3 = file_.Get("Bin3")

    Bin1.SetLineColor(ROOT.kBlack)
    Bin1.SetLineWidth(2)

    Bin2.SetLineColor(ROOT.kBlue)
    Bin2.SetLineWidth(2)

    Bin3.SetLineColor(ROOT.kRed)
    Bin3.SetLineWidth(2)

    maxim = 0
    maxim = max(maxim,Bin1.GetMaximum())
    maxim = max(maxim,Bin2.GetMaximum())
    maxim = max(maxim,Bin3.GetMaximum())

    Bin1.SetMaximum(maxim*1.2)

    Bin1.Draw("")
    Bin2.Draw("same")
    Bin3.Draw("same")

    c1.SaveAs(outputFile)

ROOT.gROOT.SetBatch()
c1 = ROOT.TCanvas("c1","c1")
c1.SetGridx()
c1.SetGridy()

#../../env/syst/MVAout_v0.0.0/ZvvHighPt_V14_WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root
#../../env/syst/MVAout_v0.0.0/ZvvHighPt_V14_WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root
#../../env/syst/MVAout_v0.0.0/ZvvHighPt_V14_WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root
#../../env/syst/MVAout_v0.0.0/ZvvHighPt_V14_WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root

#../../env/syst/MVAout_v0.0.0/ZvvHighPt_V14_ZJetsToNuNu_HT-100To200_13TeV-madgraph.root
#../../env/syst/MVAout_v0.0.0/ZvvHighPt_V14_ZJetsToNuNu_HT-200To400_13TeV-madgraph.root
#../../env/syst/MVAout_v0.0.0/ZvvHighPt_V14_ZJetsToNuNu_HT-400To600_13TeV-madgraph.root
#../../env/syst/MVAout_v0.0.0/ZvvHighPt_V14_ZJetsToNuNu_HT-600ToInf_13TeV-madgraph.root


WJets_input = "../../env/syst/MVAout_v0.0.0/ZvvHighPt_V14_WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"
makeMjjPlots(canvas=c1,inputFile=WJets_input,outputFile="WJetsHT100.png", nbins=25)
makeMjjBDTprofPlot(canvas=c1,inputFile=WJets_input,outputFile="prof_WJetsHT100.png", nbins=100)

WJets_input = "../../env/syst/MVAout_v0.0.0/ZvvHighPt_V14_WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"
makeMjjPlots(canvas=c1,inputFile=WJets_input,outputFile="WJetsHT200.png", nbins=25)
makeMjjBDTprofPlot(canvas=c1,inputFile=WJets_input,outputFile="prof_WJetsHT200.png", nbins=100)

WJets_input = "../../env/syst/MVAout_v0.0.0/ZvvHighPt_V14_WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"
makeMjjPlots(canvas=c1,inputFile=WJets_input,outputFile="WJetsHT400.png", nbins=25)
makeMjjBDTprofPlot(canvas=c1,inputFile=WJets_input,outputFile="prof_WJetsHT400.png", nbins=100)

WJets_input = "../../env/syst/MVAout_v0.0.0/ZvvHighPt_V14_WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"
makeMjjPlots(canvas=c1,inputFile=WJets_input,outputFile="WJetsHT600.png", nbins=25)
makeMjjBDTprofPlot(canvas=c1,inputFile=WJets_input,outputFile="prof_WJetsHT600.png", nbins=100)

ZJets_input = "../../env/syst/MVAout_v0.0.0/ZvvHighPt_V14_ZJetsToNuNu_HT-100To200_13TeV-madgraph.root"
makeMjjPlots(canvas=c1,inputFile=ZJets_input,outputFile="ZJetsHT100.png", nbins=25)
makeMjjBDTprofPlot(canvas=c1,inputFile=ZJets_input,outputFile="prof_ZJetsHT100.png", nbins=100)

ZJets_input = "../../env/syst/MVAout_v0.0.0/ZvvHighPt_V14_ZJetsToNuNu_HT-200To400_13TeV-madgraph.root"
makeMjjPlots(canvas=c1,inputFile=ZJets_input,outputFile="ZJetsHT200.png", nbins=25)
makeMjjBDTprofPlot(canvas=c1,inputFile=ZJets_input,outputFile="prof_ZJetsHT200.png", nbins=100)

ZJets_input = "../../env/syst/MVAout_v0.0.0/ZvvHighPt_V14_ZJetsToNuNu_HT-400To600_13TeV-madgraph.root"
makeMjjPlots(canvas=c1,inputFile=ZJets_input,outputFile="ZJetsHT400.png", nbins=25)
makeMjjBDTprofPlot(canvas=c1,inputFile=ZJets_input,outputFile="prof_ZJetsHT400.png", nbins=100)

ZJets_input = "../../env/syst/MVAout_v0.0.0/ZvvHighPt_V14_ZJetsToNuNu_HT-600ToInf_13TeV-madgraph.root"
makeMjjPlots(canvas=c1,inputFile=ZJets_input,outputFile="ZJetsHT600.png", nbins=25)
makeMjjBDTprofPlot(canvas=c1,inputFile=ZJets_input,outputFile="prof_ZJetsHT600.png", nbins=100)

TT_input = "../../env/syst/MVAout_v0.0.0/ZvvHighPt_V14_TT_TuneCUETP8M1_13TeV-powheg-pythia8.root"
makeMjjPlots(canvas=c1,inputFile=TT_input,outputFile="TT.png", nbins=25)
makeMjjBDTprofPlot(canvas=c1,inputFile=TT_input,outputFile="prof_TT.png", nbins=100)

#tree->Draw("H.mass >> bin0","MicheleBDTNoMjj.nominal>-.2 && MicheleBDTNoMjj.nominal<-0.3 && H.mass<500 &&  H.mass>90","NORM")
#tree->Draw("H.mass >> bin1","MicheleBDTNoMjj.nominal>-.3 && MicheleBDTNoMjj.nominal<0. && H.mass<500 &&  H.mass>90","NORM")
#tree->Draw("H.mass >> bin2","MicheleBDTNoMjj.nominal>0 && MicheleBDTNoMjj.nominal<1. && H.mass<500 &&  H.mass>90","NORM")

#bin0->Draw()
#bin1->Draw("same")
#bin2->Draw("same")

#---------------------------------------------

#tree->Draw("ZvvBDT:HCSV_mass","","prof")

#tree->Draw("ZvvBDTNoMjj:HCSV_mass","","prof,same")

#----------------------------

