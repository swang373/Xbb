import collections
import itertools
import os
import sys

import ROOT
import numpy


SYSTEMATIC_TO_SYSTYPE = {
    'JESUp': 'up_jes',
    'JESDown': 'down_jes',
    'LFUp': 'up_lf',
    'LFDown': 'down_lf',
    'HFUp': 'up_hf',
    'HFDown': 'down_hf',
    'HFStats1Up': 'up_hfstats1',
    'HFStats1Down': 'down_hfstats1',
    'HFStats2Up': 'up_hfstats2',
    'HFStats2Down': 'down_hfstats2',
    'LFStats1Up': 'up_lfstats1',
    'LFStats1Down': 'down_lfstats1',
    'LFStats2Up': 'up_lfstats2',
    'LFStats2Down': 'down_lfstats2',
    'cErr1Up': 'up_cferr1',
    'cErr1Down': 'down_cferr1',
    'cErr2Up': 'up_cferr2',
    'cErr2Down': 'down_cferr2',
}

CALIBRATION = ROOT.BTagCalibration('cmvav2', 'cMVAv2_Moriond17_B_H.csv')

READERS = {'CMVAV2_iterative_central': ROOT.BTagCalibrationReader(3, 'central')}
for systype in SYSTEMATIC_TO_SYSTYPE.values():
    READERS['CMVAV2_iterative_{}'.format(systype)] = ROOT.BTagCalibrationReader(3, systype)
for READER in READERS.itervalues():
    for i in xrange(3):
        READER.load(CALIBRATION, i, 'iterativefit')


Jet = collections.namedtuple('Jet', field_names=['pt', 'eta', 'hadron_flavour', 'btag'])


def jet_scale_factor(pt=30.0, eta=0.0, hadron_flavour=5, btag=0.0, systype='central'):
    if abs(eta) > 2.4 or pt > 1000 or pt < 20:
        return 1.0
    systypes_by_jet_flavor = {
        0: {'up_jes', 'down_jes', 'up_lf', 'down_lf', 'up_hfstats1', 'down_hfstats1', 'up_hfstats2', 'down_hfstats2'},
        1: {'up_cferr1', 'down_cferr1', 'up_cferr2', 'down_cferr2'},
        2: {'up_jes', 'down_jes', 'up_hf', 'down_hf', 'up_lfstats1', 'down_lfstats1', 'up_lfstats2', 'down_lfstats2'},
    }
    # Convert from hadron flavour to jet flavour.
    jet_flavor = {5: 0, 4: 1, 0: 2}[hadron_flavour]
    if systype in systypes_by_jet_flavor[jet_flavor]: 
        return READERS['CMVAV2_iterative_{}'.format(systype)].eval(jet_flavor, eta, pt, btag)
    else:
        return READERS['CMVAV2_iterative_central'].eval(jet_flavor, eta, pt, btag)


def event_scale_factor(jets=[], systype='central', pt_min=20, pt_max=1000, eta_min=0, eta_max=2.4):
    weight = 1.0
    for jet in jets:
        if pt_min < jet.pt < pt_max and eta_min < abs(jet.eta) < eta_max:
            weight *= jet_scale_factor(jet.pt, jet.eta, jet.hadron_flavour, jet.btag, systype)
        else:
            weight *= jet_scale_factor(jet.pt, jet.eta, jet.hadron_flavour, jet.btag)
    return weight


def main():
    ROOT.gROOT.SetBatch(True)
    infile = ROOT.TFile.Open(sys.argv[1])
    outfile = ROOT.TFile.Open(sys.argv[2], 'recreate')
    for key in infile.GetListOfKeys():
        if key.GetName() == 'tree':
            continue
        obj = key.ReadObj()
        obj.Write()
    tree = infile.Get('tree')
    tree.SetBranchStatus('bTagWeightCMVA*', 0)
    tree_new = tree.CloneTree(0)
    branches = {}
    branches['bTagWeightMoriondCMVA'] = numpy.zeros(1, dtype=numpy.float64)
    tree_new.Branch('bTagWeightMoriondCMVA', branches['bTagWeightMoriondCMVA'], 'bTagWeightMoriondCMVA/D')
    for systematic in SYSTEMATIC_TO_SYSTYPE:
        name = 'bTagWeightMoriondCMVA_{}'.format(systematic)
        branches[name] = numpy.zeros(1, dtype=numpy.float64)
        tree_new.Branch(name, branches[name], '{}/D'.format(name))
        for i, j in itertools.product(xrange(5), xrange(3)):
            subname = '{0}_pt{1!s}_eta{2!s}'.format(name, i+1, j+1)
            branches[subname] = numpy.zeros(1, dtype=numpy.float64)
            tree_new.Branch(subname, branches[subname], '{}/D'.format(subname))
    for idx, event in enumerate(tree):
        if idx % 10000 == 0:
            print idx
        jets = [
            Jet(event.Jet_pt[i], event.Jet_eta[i], event.Jet_hadronFlavour[i], event.Jet_btagCMVAV2[i])
            for i in xrange(event.nJet) if event.Jet_pt[i] > 25 and abs(event.Jet_eta[i]) < 2.4
        ]
        branches['bTagWeightMoriondCMVA'][0] = event_scale_factor(jets)
        for systematic, systype in SYSTEMATIC_TO_SYSTYPE.iteritems():
            name = 'bTagWeightMoriondCMVA_{}'.format(systematic)
            branches[name][0] = event_scale_factor(jets, systype)
            for pt_bin, (pt_min, pt_max) in enumerate([(20, 30), (30, 40), (40, 60), (60, 100), (100, 10000)], start=1):
                for eta_bin, (eta_min, eta_max) in enumerate([(0, 0.8), (0.8, 1.6), (1.6, 2.4)], start=1):
                    subname = '{0}_pt{1!s}_eta{2!s}'.format(name, pt_bin, eta_bin)
                    branches[subname][0] = event_scale_factor(jets, systype, pt_min, pt_max, eta_min, eta_max)
        tree_new.Fill()
    tree_new.Write()
    outfile.Close()
    infile.Close()


if __name__ == '__main__':

    status = main()
    sys.exit(status)

