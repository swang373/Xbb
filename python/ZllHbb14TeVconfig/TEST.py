import os

merged = 'root://t3dcachedb03.psi.ch:1094//pnfs/psi.ch/cms/trivcat/store/user/gaperrin/VHbb/ZllHbb13TeV_V13/prep/ZmmH.BestCSV.heppy.DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root'

print os.path.exists('/pnfs/psi.ch/cms/trivcat/store/user/gaperrin/VHbb/ZllHbb13TeV_V13/prep/ZmmH.BestCSV.heppy.DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root')
print os.path.exists(merged.replace('root://t3dcachedb03.psi.ch:1094/',''))
