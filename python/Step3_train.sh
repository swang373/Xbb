setenv TMPDIR /scratch/sdonato/VHbbRun2/CMSSW_7_4_12_patch4/src/Xbb/tmp

bash runAll.sh MicheleBDT ZvvHbb13TeV train >& log/logTrainZH &
bash runAll.sh MicheleBDTNoMjj ZvvHbb13TeV train >& log/logTrainZHNoMjj &
