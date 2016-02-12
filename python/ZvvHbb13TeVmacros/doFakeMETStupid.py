from ROOT import *
from array import *
from math import *
import copy

precut  = 90
cut     = 130
gROOT.SetBatch()

def doFile(fileName="tree_100_QCDHT700.root",outName="newTree.root",function=None):

    file_               = TFile(fileName)
    old_tree            = file_.Get("tree")
    old_Count           = file_.Get("Count")
    old_CountWeighted   = file_.Get("CountWeighted")
    old_CountPosWeight  = file_.Get("CountPosWeight")
    old_CountNegWeight  = file_.Get("CountNegWeight")


    fileNew = TFile(outName,"recreate")
    fileNew.cd()

    tree            = old_tree.CloneTree(0)
    Count           = old_Count.Clone("Count")
    CountWeighted   = old_CountWeighted.Clone("CountWeighted")
    CountPosWeight  = old_CountPosWeight.Clone("CountPosWeight")
    CountNegWeight  = old_CountNegWeight.Clone("CountNegWeight")
    FakeMET_count   = old_CountNegWeight.Clone("FakeMET_count")
    FakeMET_count.SetBinContent(0,0)

    Vtype = array('f',[0])
    tree.SetBranchAddress("Vtype",Vtype)

    HLT_BIT_HLT_PFMET90_PFMHT90_IDLoose_v = array('f',[0])
    tree.SetBranchAddress("HLT_BIT_HLT_PFMET90_PFMHT90_IDLoose_v",HLT_BIT_HLT_PFMET90_PFMHT90_IDLoose_v)

    FakeMET_met = array('f',[0])
    tree.Branch('FakeMET_met',FakeMET_met,'FakeMET_met/F')

    met_pt = array('f',[0])
    tree.SetBranchAddress("met_pt",met_pt)

    mhtJet30 = array('f',[0])
    tree.SetBranchAddress("mhtJet30",mhtJet30)

    nEntries = old_tree.GetEntries()

    for entry in range(0,nEntries):
        old_tree.GetEntry(entry)
        if old_tree.met_pt<90:  continue

        FakeMET_met[0]  = old_tree.met_pt

        met_pt[0]       = old_tree.met_pt   + 40.
        mhtJet30[0]     = old_tree.mhtJet30 + 40.

        Vtype[0]                   = 4
        HLT_BIT_HLT_PFMET90_PFMHT90_IDLoose_v[0] = 1

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
    f       = TFile("newTree_fit.root")
    function = f.Get("c1").GetPrimitive("histo")
#    function = copy.copy(function)
    fileName="/scratch/sdonato/VHbbRun2/V14_forPreApproval/CMSSW_7_1_5/src/Xbb/env/ZvvHighPt_V15_QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"
#    fileName="/gpfs/ddn/srm/cms/store/user/arizzi/VHBBHeppyV14//QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V14_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151024_181957/0000/tree_1.root"
#    fileName="/scratch/sdonato/VHbbRun2/V14_forPreApproval/CMSSW_7_1_5/src/Xbb/env/ZvvHighPt_V15_QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"
#    fileName="/scratch/sdonato/VHbbRun2/V14_forPreApproval/CMSSW_7_1_5/src/Xbb/env/ZvvHighPt_V15_QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"
#    fileName="/scratch/sdonato/VHbbRun2/V14_forPreApproval/CMSSW_7_1_5/src/Xbb/env/ZvvHighPt_V15_QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root"
#    fileName="/gpfs/ddn/srm/cms/store/user/arizzi/VHBBHeppyV14//QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V14_QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151025_083609/0000/tree_1.root"
    outName="newTree.root"
    doFile(fileName,outName)


