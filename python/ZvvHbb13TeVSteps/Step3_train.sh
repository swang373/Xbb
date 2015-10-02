bash runAll.sh ZvvBDT ZvvHbb13TeV train >& log/logTrainZH &
bash runAll.sh ZvvBDTNoMjj ZvvHbb13TeV train >& log/logTrainZHNoMjj &

bash runAll.sh ZvvBDTOnlyPositiveWeights ZvvHbb13TeV train >& log/logTrainZHOnlyPositiveWeights &
bash runAll.sh ZvvBDTNoMjjOnlyPositiveWeights ZvvHbb13TeV train >& log/logTrainZHNoMjjOnlyPositiveWeights &

