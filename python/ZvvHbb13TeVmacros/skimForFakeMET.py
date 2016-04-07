from doFakeMET import getJetIdx
from ROOT import *
from array import *
from math import *
import copy

maxEvents = -1
precut  = 80
cut     = 120
gROOT.SetBatch()

range_ = 500

newHCSV = TLorentzVector()
j1 = TLorentzVector()
j2 = TLorentzVector()

def doFile(fileName="tree_100_QCDHT700.root",outName="newTree.root",function=None,expoRatio=None):

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

    FakeMET_jetIdx = array('i',[0])
    tree.Branch('FakeMET_jetIdx',FakeMET_jetIdx,'FakeMET_jetIdx/I')

    nEntries = old_tree.GetEntries()
    print "nEntries:",nEntries

    random = TRandom3()
    formCut = TTreeFormula("formCut","(met_pt > %d) && nhJCidx>=2"%(precut),old_tree)
    entry=0
    for entry in range(0,nEntries):
        if entry%1000==0: print "entry: ",entry
        if maxEvents>0 and entry>maxEvents: break
        old_tree.GetEntry(entry)

        formCut.GetNdata()
        bit = formCut.EvalInstance()

        if not bit: continue
        if type(old_tree)!=TTree: continue
        idx = 0
        idx                     = getJetIdx(old_tree.nJet,old_tree.nGenJet,old_tree.Jet_pt,old_tree.Jet_mcIdx,old_tree.GenJet_wNuPt,old_tree.GenJet_wNuEta)
        if idx>=old_tree.nJet or idx<0 or old_tree.Jet_mcIdx[idx]<0 or old_tree.Jet_mcIdx[idx]>=old_tree.nGenJet:
            print
            print idx
            print old_tree.nJet
            continue
        FakeMET_jetIdx[0]       = idx

        tree.Fill()

    print "Done:",entry
    tree.Write()
    Count.Write()
    CountWeighted.Write()
    CountPosWeight.Write()
    CountNegWeight.Write()
#    FakeMET_jetIdx.Write()
    fileNew.Close()

if __name__ == "__main__":
    fileName="../../env/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tree_VHBB_HEPPY_V21_QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1_19.root"

    outName="newTree.root"
    maxEvents = 1000
    doFile(fileName,outName)


