setenv TMPDIR /scratch/sdonato/VHbbRun2/CMSSW_7_4_12_patch4/src/Xbb/tmp

bash runAll.sh Nothing ZvvHbb13TeV plot >& log/logPlotNothing &
bash runAll.sh NoQCD1 ZvvHbb13TeV plot >& log/logPlotNoQCD1 &
bash runAll.sh NoQCD2 ZvvHbb13TeV plot >& log/logPlotNoQCD2 &
bash runAll.sh NoQCD3 ZvvHbb13TeV plot >& log/logPlotNoQCD3 &
bash runAll.sh CutAndCount ZvvHbb13TeV plot >& log/logPlotCutAndCount &
bash runAll.sh AllBDT ZvvHbb13TeV plot >& log/logPlotAllBDT &


