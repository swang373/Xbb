import ROOT, os


file1 = 'root://t3dcachedb03.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/gaperrin/VHbb/ZllHbb13TeV_V12/prep/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tree_23.root'
file2 = 'root://t3dcachedb03.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/gaperrin/VHbb/ZllHbb13TeV_V12/prep/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/tree_4.root'

t = ROOT.TFileMerger()
t.OutputFile('root://t3dcachedb03.psi.ch:1094//pnfs/psi.ch/cms/trivcat/store/user/gaperrin/VHbb/ZllHbb13TeV_V12/TEST.root')
t.AddFile(file1)
t.AddFile(file2)

t.Merge()




