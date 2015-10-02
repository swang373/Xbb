setenv TMPDIR /scratch/sdonato/VHbbRun2/CMSSW_7_4_12_patch4/src/Xbb/tmp

bash runAll.sh ZvvBDT ZvvHbb13TeV train >& log/logTrainZH &
bash runAll.sh ZvvBDTNoMjj ZvvHbb13TeV train >& log/logTrainZHNoMjj &

bash runAll.sh ZvvBDTOnlyPositiveWeights ZvvHbb13TeV train >& log/logTrainZHOnlyPositiveWeights &
bash runAll.sh ZvvBDTNoMjjOnlyPositiveWeights ZvvHbb13TeV train >& log/logTrainZHNoMjjOnlyPositiveWeights &

bash runAll.sh ZvvBDTWithWeights ZvvHbb13TeV train >& log/logTrainZHWithWeights &
bash runAll.sh ZvvBDTNoMjjWithWeights ZvvHbb13TeV train >& log/logTrainZHNoMjjWithWeights &


