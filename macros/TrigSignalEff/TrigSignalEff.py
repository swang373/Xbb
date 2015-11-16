#USAGE:         python TrigSignalEff.py ZmmH.BestCSV.heppy.ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8.root

import ROOT as r
import sys

_tree = ''
_tree = sys.argv[1]
print 'the tree path is', _tree
f = r.TFile(_tree, 'read')
t = f.Get('tree')

BRANCH = t.GetListOfBranches()
HLT = []
for branch in BRANCH:
    if branch.GetName().find("HLT") == -1: continue
    else: HLT.append(branch.GetName())

print '========================='
print 'The list of HLT branch is'
print '=========================\n'
print HLT

HLT_val = [0]*len(HLT)
t.SetBranchStatus("*",0)
for hlt in HLT:
    t.SetBranchStatus(hlt,1)

#for n in  xrange (t.GetEntries()):
for n in  xrange (1000):
    if n % 1000 == 0:
        print "Event number %d out of %d " % (n, t.GetEntries())
        print 'hlt val is', HLT_val
    t.GetEntry(n)
    for hlt, index, hlt_val in zip(HLT, range(len(HLT)), HLT_val):
        exec ('hlt_val += t.%s' % (hlt))
        HLT_val[index] = hlt_val


print 'hlt val is', HLT_val
print 'HLT', HLT

for hlt_val, hlt in zip(HLT_val, HLT):
    print hlt, hlt_val



