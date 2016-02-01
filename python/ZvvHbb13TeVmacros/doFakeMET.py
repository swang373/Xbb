from ROOT import *
from array import *
from math import *

cut = 90
gROOT.SetBatch()

def smartFit(histo,default,formula="gaus(0)+gaus(3)+gaus(6)+gaus(9)"):
    a_=0.25
    b_=1
    c_=5

    function = TF1("function",formula,-c_,c_)
    function.SetParameters(*default)
#    for i in range(function.GetNpar()):
#        if ((i)%3)==0:
#            function.SetParLimits(i,0,1)
#        elif ((i-2)%3)==0:
#            function.SetParLimits(i,0,999999)

    for i in range(function.GetNpar()):
        if not i in [0,1,2]:
            function.FixParameter(i,function.GetParameter(i))
        else:
            function.ReleaseParameter(i)
            if ((i)%3)==0:
                function.SetParLimits(i,0,1)
            elif ((i-2)%3)==0:
                function.SetParLimits(i,0,999999)
            elif ((i-2)%3)==0:
                function.SetParLimits(i,0,999999)
    histo.Fit(function,"","",-a_,a_)

    for i in range(function.GetNpar()):
        if not i in [3,4,5]:
            function.FixParameter(i,function.GetParameter(i))
        else:
            function.ReleaseParameter(i)
            if ((i)%3)==0:
                function.SetParLimits(i,0,1)
            elif ((i-1)%3)==0:
                function.SetParLimits(i,-1,1)
            elif ((i-2)%3)==0:
                function.SetParLimits(i,0,999999)
    histo.Fit(function,"","",-b_,-a_)

    for i in range(function.GetNpar()):
        if not i in [6,7,8]:
            function.FixParameter(i,function.GetParameter(i))
        else:
            function.ReleaseParameter(i)
            if ((i)%3)==0:
                function.SetParLimits(i,0,1)
            elif ((i-1)%3)==0:
                function.SetParLimits(i,-1,1)
            elif ((i-2)%3)==0:
                function.SetParLimits(i,0,999999)
    histo.Fit(function,"","",-c_,-b_)

    for i in range(function.GetNpar()):
        if not i in [9,10,11]:
            function.FixParameter(i,function.GetParameter(i))
        else:
            function.ReleaseParameter(i)
            if ((i)%3)==0:
                function.SetParLimits(i,0,1)
            elif ((i-1)%3)==0:
                function.SetParLimits(i,-1,1)
            elif ((i-2)%3)==0:
                function.SetParLimits(i,0,999999)
    histo.Fit(function,"","",-c_,c_)

    for i in range(function.GetNpar()):
        function.ReleaseParameter(i)
        if ((i)%3)==0:
            function.SetParLimits(i,0,1)
        elif ((i-2)%3)==0:
            function.SetParLimits(i,0,999999)

    histo.Fit(function,"","",-c_,c_)
#    function.Draw("same")
    return function

#def smartFit(histo,formula="(1+[4]*x**[5])*(exp([0]+[1]*x)+exp([2]+[3]*x))",min_=-.,mid_=60.,max_=1000.):
#    function = TF1("function",formula,min_,max_)
#    function.SetParameters(6.58,-0.032,13.32,-0.102,0,0,0)

#    for i in range(function.GetNpar()):
#        if not i in [0,1,2,3]:
#            function.FixParameter(i,function.GetParameter(i))
#        else:
#            function.ReleaseParameter(i)
#
#    histo.Fit(function,"","",mid_,max_)

#    for i in range(function.GetNpar()):
#        if i in [0,1,2,3]:
#            function.FixParameter(i,function.GetParameter(i))
#        else:
#            function.ReleaseParameter(i)

#    histo.Fit(function,"","",min_,mid_)

#    for i in range(function.GetNpar()):
#            function.ReleaseParameter(i)

#    histo.Fit(function,"","",min_+20,max_)
#    histo.Fit(function,"","",min_+10,max_)
#    histo.Fit(function,"","",min_,max_)
#    return function

def getJetIdx(nJets,nGenJets,Jet_pt,Jet_mcIdx,GenJet_wNuPt):
    idx=int(-1)
    diff=-1
    ndiff=0
    for i in range(nJets):
#        if Jet_mcIdx[i]<0 or Jet_mcIdx[i]>=nGenJets: continue
#        if Jet_mcIdx[i]>=nGenJets or Jet_mcIdx[i]<0 : continue
        if Jet_mcIdx[i]>=nGenJets or Jet_mcIdx[i]<0 or abs(tree.GenJet_wNuEta[Jet_mcIdx[i]])>2.6 : continue
        ndiff=abs(GenJet_wNuPt[Jet_mcIdx[i]]-Jet_pt[i])
        if ndiff>diff: idx=i
    return int(idx)

def newPt(GenJet_wNuPt,Jet_pt,Jet_phi,met_pt,met_phi,function,cut):
    Jet_ptNew = Jet_pt
    met_ptx = met_pt * cos(met_phi)
    met_pty = met_pt * sin(met_phi)
    Jet_ptx = Jet_pt * cos(Jet_phi)
    Jet_pty = Jet_pt * sin(Jet_phi)
    metNoJet_ptx = met_ptx + Jet_ptx
    metNoJet_pty = met_pty + Jet_pty
#    sign = (Jet_pt-GenJet_wNuPt)/abs(Jet_pt-GenJet_wNuPt)
    i=0
    newMet_pt_squared = met_pt**2
    count=1
    Jet_ptNew_min = Jet_ptNew
    Jet_ptNew_max = Jet_ptNew
    while(newMet_pt_squared < cut**2 and count<1E7):
        count+=1
        Jet_ptNew = GenJet_wNuPt*exp(function.GetRandom());
        if Jet_ptNew<Jet_ptNew_max and Jet_ptNew>Jet_ptNew_min: continue
        Jet_ptNew_min = min(Jet_ptNew_min,Jet_ptNew)
        Jet_ptNew_max = max(Jet_ptNew_max,Jet_ptNew)
        met_ptx = metNoJet_ptx - Jet_ptNew * cos(Jet_phi)
        met_pty = metNoJet_pty - Jet_ptNew * sin(Jet_phi)
        newMet_pt_squared = met_ptx**2+met_pty**2

    if count>1E6: print "count = ",count
    if Jet_ptNew<0: Jet_ptNew=0
    return Jet_ptNew,count

def correctMet(met_pt,met_phi,Jet_pt,Jet_phi,Jet_ptNew):
    met_ptx = met_pt * cos(met_phi)
    met_pty = met_pt * sin(met_phi)
    Jet_ptx = Jet_pt * cos(Jet_phi)
    Jet_pty = Jet_pt * sin(Jet_phi)
    JetNew_ptx = Jet_ptNew * cos(Jet_phi)
    JetNew_pty = Jet_ptNew * sin(Jet_phi)
    met_ptx = met_ptx + Jet_ptx - JetNew_ptx
    met_pty = met_pty + Jet_pty - JetNew_pty
    met_pt  = (met_ptx**2+met_pty**2)**0.5
    if met_ptx==0:
        if met_pty>0: met_phi=pi
        else: met_phi=-pi
    else:
        met_phi = atan(met_pty/met_ptx)
    if met_ptx<0: met_phi+=pi
    if met_phi>pi: met_phi-=2*pi
    if met_phi<-pi: met_phi+=2*pi
    return met_pt,met_phi

#file_ = TFile("tree_100_QCDHT300.root")

def doFile(fileName="tree_100_QCDHT700.root",outName="newTree.root",function=None):

    if function is None:
        c1              = TCanvas()
        chainN          = fileName.split("/tree_")[0]+"/tree_*.root"
        chain           = TChain("tree")
        chain.Add(chainN)
        print "Fitting function in: ",chainN
        chain.Draw(" log(Jet_pt/GenJet_wNuPt[Jet_mcIdx])  >> histo(1000,-3,3)","Jet_mcIdx==0 && GenJet_wNuPt[Jet_mcIdx]>0 && abs(GenJet_wNuEta[Jet_mcIdx])<2.6 && met_pt>0.00","NORM")
        histo = gDirectory.Get("histo")

#        default=(0.015,0.027,0.094,0.0060,-0.050,0.15,0.00015,-0.13,0.44)
#        function = smartFit(histo,default,"gaus(0)+gaus(3)+gaus(6)")

        import copy
        function = copy.deepcopy(histo)

        c1.SetLogy()
        c1.SaveAs(outName.replace(".root","_fit.png"))
        c1.SaveAs(outName.replace(".root","_fit.C"))
        c1.SaveAs(outName.replace(".root","_fit.root"))
#        chain.Delete()

#    old_tree            = TChain("tree")
#    old_tree.Add(fileNames)
#    file_               = old_tree.GetFile()


    file_               = TFile(fileName)
    old_tree            = file_.Get("tree")
    old_Count           = file_.Get("Count")
    old_CountWeighted   = file_.Get("CountWeighted")
    old_CountPosWeight  = file_.Get("CountPosWeight")
    old_CountNegWeight  = file_.Get("CountNegWeight")


    fileNew = TFile(outName,"recreate")
    fileNew.cd()
    #tree.Write()

    #old_tree.Draw("(MaxIf$(abs(GenJet_wNuPt[Jet_mcIdx] - Jet_pt),Jet_mcIdx>=0 && GenJet_wNuPt[Jet_mcIdx]>0 && abs(GenJet_wNuEta[Jet_mcIdx])<2.6)) >> histo(1000,0,1000)","")
    #function = smartFit(histo,"(1+[4]+[5]*x**2)*(exp([0]+[1]*x)+exp([2]+[3]*x))")
    #1/0
    #tree = old_tree
    #return

    tree            = old_tree.CloneTree(0)
    #tree            = old_tree.CopyTree(1000,0)
    Count           = old_Count.Clone("Count")
    CountWeighted   = old_CountWeighted.Clone("CountWeighted")
    CountPosWeight  = old_CountPosWeight.Clone("CountPosWeight")
    CountNegWeight  = old_CountNegWeight.Clone("CountNegWeight")
    FakeMET_count   = old_CountNegWeight.Clone("FakeMET_count")
    FakeMET_count.SetBinContent(0,0)
    #file_.Close()

    met_pt = array('f',[0])
    tree.SetBranchAddress("met_pt",met_pt)

    met_phi = array('f',[0])
    tree.SetBranchAddress("met_phi",met_phi)

    mhtJet30 = array('f',[0])
    tree.SetBranchAddress("mhtJet30",mhtJet30)

    mhtPhiJet30 = array('f',[0])
    tree.SetBranchAddress("mhtPhiJet30",mhtPhiJet30)

    FakeMET_met = array('f',[0])
    tree.Branch('FakeMET_met',FakeMET_met,'FakeMET_met/F')

    FakeMET_metPhi = array('f',[0])
    tree.Branch('FakeMET_metPhi',FakeMET_metPhi,'FakeMET_metPhi/F')

    FakeMET_jetPt = array('f',[0])
    tree.Branch('FakeMET_jetPt',FakeMET_jetPt,'FakeMET_jetPt/F')

    FakeMET_jetIdx = array('i',[0])
    tree.Branch('FakeMET_jetIdx',FakeMET_jetIdx,'FakeMET_jetIdx/I')

    nEntries = old_tree.GetEntries()
    for entry in range(0,nEntries):
        old_tree.GetEntry(entry)
        if not old_tree.met_pt>0.00: continue
    #    if entry>1000: break
    #    idx                     = getJetIdx(old_tree.nJet,old_tree.nGenJet,old_tree.Jet_pt,old_tree.Jet_mcIdx,old_tree.GenJet_wNuPt)
        idx = 0
        if idx>=old_tree.nJet or idx<0 or old_tree.Jet_mcIdx[idx]<0 or old_tree.Jet_mcIdx[idx]>=old_tree.nGenJet:
            print
            print idx
            print old_tree.nJet
            continue
        FakeMET_met[0]          = old_tree.met_pt
        FakeMET_metPhi[0]       = old_tree.met_phi
        FakeMET_jetPt[0]        = old_tree.Jet_pt[idx]
        FakeMET_jetIdx[0]       = idx
        newPt_,count            = newPt(old_tree.GenJet_wNuPt[old_tree.Jet_mcIdx[idx]],old_tree.Jet_pt[idx],old_tree.Jet_phi[idx],old_tree.met_pt,old_tree.met_phi,function,cut)
        newPt_15                = newPt_
        newPt_30                = newPt_
        if newPt_15<15: newPt_15=0
        if newPt_30<30: newPt_30=0
    #    print count,FakeMET_count.GetBinContent(1)
        (met_pt[0],met_phi[0])  = correctMet(old_tree.met_pt,old_tree.met_phi,old_tree.Jet_pt[idx],old_tree.Jet_phi[idx],newPt_)
        (mhtJet30[0],mhtPhiJet30[0]) = correctMet(old_tree.mhtJet30,old_tree.mhtPhiJet30,old_tree.Jet_pt[idx],old_tree.Jet_phi[idx],newPt_30)
        old_tree.Jet_pt[idx]    = newPt_15
        tree.Fill()

    FakeMET_count.SetBinContent(1,CountWeighted.GetBinContent(1))
    ratio = 1.*tree.Draw("","met_pt>%d"%cut)/(1E-9+tree.Draw("","FakeMET_met>%d"%cut))
    tree.AutoSave()

    Count.SetBinContent(1,ratio*Count.GetBinContent(1))
    CountWeighted.SetBinContent(1,ratio*CountWeighted.GetBinContent(1))
    CountPosWeight.SetBinContent(1,ratio*CountPosWeight.GetBinContent(1))
    CountNegWeight.SetBinContent(1,ratio*CountNegWeight.GetBinContent(1))

    Count.Write()
    CountWeighted.Write()
    CountPosWeight.Write()
    CountNegWeight.Write()
    FakeMET_count.Write()
    fileNew.Close()
    return function

if __name__ == "__main__":

    fileName="/gpfs/ddn/srm/cms/store/user/arizzi/VHBBHeppyV14//QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V14_QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151025_083726/0000/tree_99.root"
    outName="newTree.root"
    doFile(fileName,outName)

