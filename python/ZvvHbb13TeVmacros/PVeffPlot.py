import sys
from ROOT import *
from DataFormats.FWLite import Handle, Events

#filesInput = "/scratch/sdonato/ZvvHbb_AOD76X.root"
#filesInput = "/scratch/sdonato/ZvvHbb_AOD76X.root"
#filesInput = "/scratch/sdonato/ZvvHbb_AOD76X_PU40.root"

filesInput = [
      'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/080FC889-C9D6-E511-B8E8-002590D6004A.root',
       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/0C84F5FD-ADD7-E511-92DC-0CC47A57CDD2.root',
       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/0E683AA5-B4D6-E511-9A5C-24BE05CE4D91.root',
       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/1297447A-EDD6-E511-AC4F-0025907B4F64.root',
       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/16163D14-E7D6-E511-B4D0-901B0E6459CA.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/18428181-E4D6-E511-98B0-002590D0AFD0.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/1EE9DDC8-B6D6-E511-A2B4-0025905B85B8.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/2A05467B-C9D6-E511-B0F7-000F530E47CC.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/36D4387B-F1D6-E511-9C0D-90B11C04FE38.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/38579AC5-B6D6-E511-99AF-0CC47A4D765E.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/402A4D8D-B6D6-E511-92F1-5065F38142E1.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/40EBC8BB-C8D6-E511-816D-00259021A262.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/4A6A9845-AED7-E511-AC15-3417EBE53662.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/544F54AC-B6D6-E511-8A62-0CC47A4D7644.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/58983777-B6D6-E511-86C0-0CC47A745282.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/5E6DEEED-51D8-E511-9F77-90B11C05037D.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/6012E374-8BD6-E511-AA0A-842B2B2B0DAD.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/684D808B-89D7-E511-96E9-0CC47A78A32E.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/6A6C81DD-B0D7-E511-B963-00259021A14E.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/6ED515BB-B4D6-E511-A8A7-000F53273500.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/72357791-BED6-E511-907D-782BCB27B958.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/74380F56-C1D6-E511-A36B-000F53273728.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/780ED172-8BD6-E511-856D-842B2B2922E2.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/78C30C2A-BBD6-E511-BEAD-842B2B29FE8C.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/7E4EED76-BBD6-E511-9519-000F530E4644.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/86564999-E1D6-E511-9A60-001E67504645.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/88BEBAA4-EBD6-E511-93BA-20CF307C98DC.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/8A740862-8CD7-E511-BDC3-0002C94CD0D8.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/8C5B2216-BDD6-E511-BBFF-000F53273728.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/8C664F58-BBD6-E511-9BA0-AC853D9DAC21.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/904FB573-BBD6-E511-B2EF-B083FED76508.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/941D5093-BBD6-E511-A0FD-AC853D9DAC2B.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/9436EB3D-C1D6-E511-94F4-001E67504645.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/94874E76-BBD6-E511-83B9-782BCB407BCB.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/9CFE22E1-B6D6-E511-BA2C-0025905A60A8.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/A01F8E8A-BED6-E511-9F0C-001E675050F5.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/A027BD80-BED6-E511-B8FF-0CC47A4D9A42.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/A2CD9241-C1D6-E511-8E4B-3417EBE8862E.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/A6BFF7B0-BAD6-E511-92B1-0002C92F34E8.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/A80D3866-B6D6-E511-B1CB-0CC47A4C8F30.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/A82949FB-51D8-E511-AA83-BCAEC5097201.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/A8D42CDF-B7D7-E511-94FE-44A842434705.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/AE423A09-E5D6-E511-B32E-001E67A3E872.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/B08113AF-B6D6-E511-92CD-0CC47A4C8E20.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/B2D4EFF4-A7D7-E511-95FC-AC853D9DACD3.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/B63B26AA-B6D6-E511-8D47-001E6750507D.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/C450A661-93D6-E511-BA0F-A0000420FE80.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/C6E1D425-AED6-E511-85E4-0025905964C2.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/CE8A595D-BED6-E511-AA93-0CC47A4C8E28.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/D416BE78-BBD6-E511-B1DC-000F53273728.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/DAF31EBC-B6D6-E511-AA45-0025905A6082.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/F2571EBB-B4D6-E511-8D3A-B083FED7685B.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/F4AB2592-DFD6-E511-9324-001E67504255.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/F6B5732A-BBD6-E511-A1E8-842B2B29FE8C.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/FA0F0978-BBD6-E511-8C20-AC853D9DAC1F.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/00000/FED45891-B6D6-E511-A870-A0000420FE80.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/10000/10CDC645-8AD6-E511-902D-20CF3027A61A.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/10000/14B13FAA-05D7-E511-8170-001E6757F1D4.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/10000/1852A4B4-05D7-E511-8C20-0025907277CE.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/10000/18A1D39F-05D7-E511-A174-002590D9D8BA.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/10000/2C5F23A1-05D7-E511-B4EA-0002C94CD2A6.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/10000/569A7F7B-92D6-E511-B416-0CC47A13D2BE.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/10000/56D61383-05D7-E511-9EE8-0025905A6118.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/10000/5A412F7C-91D6-E511-B10C-A0000420FE80.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/10000/7212470A-8AD6-E511-9643-0CC47A6C1864.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/10000/72A03901-8BD6-E511-99A1-5065F381E251.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/10000/7E02F88C-91D6-E511-A4DB-24BE05C48821.root',
#       'root://cms-xrd-global.cern.ch//store/mc/RunIIFall15DR76/ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/10000/7EED318F-05D7-E511-B2C9-90B11C094A7E.root',
]


histoOld = TH1F("histoOld","",50,0,500)
histoNew = histoOld.Clone("histoNew")
histoDen = histoOld.Clone("histoDen")

histoDen.SetLineColor(kBlack)
histoNew.SetLineColor(kRed)
histoOld.SetLineColor(kBlue)

effNew =  TGraphAsymmErrors(histoNew)
effOld =  TGraphAsymmErrors(histoDen)

effNew.SetLineColor(kRed)
effNew.SetMarkerColor(kRed)

effOld.SetLineColor(kBlue)
effOld.SetMarkerColor(kBlue)

print
print "Opening ",filesInput
print
events = Events (filesInput)
genParticles_source, genParticles_label = Handle("vector<reco::GenParticle>"), ("genParticles")
offVtx_source, offVtx_label = Handle("vector<reco::Vertex>"), ("offlinePrimaryVertices")
genMET_source, genMET_label = Handle("vector<reco::GenMET>"), ("genMetTrue")
for iev,event in enumerate(events): 
    event.getByLabel(offVtx_label, offVtx_source)
    sumPt2 = 0
    sumPt2 = 0
    iVtx = -1
    VtxMax = -1
    for idx,vtx in  enumerate(offVtx_source.product()):
        sumPt2 = 0
        trk = vtx.tracks_begin()
        for i in range(vtx.tracksSize()):
            sumPt2 += trk.get().pt()**2
            trk +=1
        if sumPt2>VtxMax:
            VtxMax = sumPt2
            iVtx = idx
    
    event.getByLabel(genMET_label, genMET_source)
    event.getByLabel(genParticles_label, genParticles_source)
    
    genMET = genMET_source.product()[0].pt()
    genZVtx = genParticles_source.product()[2].vz()
    
    newZVtx = offVtx_source.product()[0].z()
    oldZVtx = offVtx_source.product()[iVtx].z()
    
    histoDen.Fill(genMET)
    if abs(oldZVtx-genZVtx)<0.5:
        histoOld.Fill(genMET)
    if abs(newZVtx-genZVtx)<0.5:
        histoNew.Fill(genMET)
#    if iev>1000: break

c1 = TCanvas("c1")


histoDen.Draw()
histoOld.Draw("same")
histoNew.Draw("same")

c1.SaveAs("histosPV.C")

effNew.Divide(histoNew,histoDen,"cl=0.683 b(1,1) mode")
effOld.Divide(histoOld,histoDen,"cl=0.683 b(1,1) mode")

effOld.Draw("AP")
effNew.Draw("P")

c1.SaveAs("efficiencyPV.C")
