#bash runAll.sh ZvvBDT ZvvHbb13TeV train >& log/logTrainZH;
#bash runAll.sh ZvvBDTTight ZvvHbb13TeV train >& log/logTrainZHTight;
#bash runAll.sh ZvvBDTNoMjj ZvvHbb13TeV train >& log/logTrainZHNoMjj;

#bash runAll.sh ZvvBDTOnlyPositiveWeights ZvvHbb13TeV train >& log/logTrainZHOnlyPositiveWeights;
#bash runAll.sh ZvvBDTNoMjjOnlyPositiveWeights ZvvHbb13TeV train >& log/logTrainZHNoMjjOnlyPositiveWeights;

bash runAll.sh ZvvBDTHighPt SeanZvvHbb13TeV train >& log/Train_HighPt;
bash runAll.sh ZvvBDTLowPt SeanZvvHbb13TeV train >& log/Train_LowPt;
bash runAll.sh ZvvBDTTightHighPt SeanZvvHbb13TeV train >& log/Train_HighPt_Tight;
bash runAll.sh ZvvBDTTightLowPt SeanZvvHbb13TeV train >& log/Train_LowPt_Tight;

