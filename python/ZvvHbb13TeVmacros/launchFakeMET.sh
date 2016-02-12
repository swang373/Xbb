#source /afs/pi.infn.it/grid_exp_sw/cms/scripts/setcms.sh
#setenv SCRAM_ARCH="slc5_amd64_gcc462"
#source $VO_CMS_SW_DIR/cmsset_default.sh
#eval `scramv1 runtime -sh`
##eval `cmsenv`

setenv envFolder=/scratch/sdonato/VHbbRun2/V14_forPreApproval/CMSSW_7_1_5/src/Xbb/env/
setenv source=/gpfs/ddn/srm/cms/store/user/arizzi/VHBBHeppyV14/

#/gpfs/ddn/srm/cms/store/user/arizzi/VHBBHeppyV14/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*/tree*.root

setenv QCDHT100     QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
setenv QCDHT200     QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
setenv QCDHT300     QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
setenv QCDHT500     QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
setenv QCDHT700     QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
setenv QCDHT1000    QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
setenv QCDHT1500    QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
setenv QCDHT2000    QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8

#mkdir $envFolder'/Fake'$QCDHT100
#mkdir $envFolder'/Fake'$QCDHT200
#mkdir $envFolder'/Fake'$QCDHT300
#mkdir $envFolder'/Fake'$QCDHT500
#mkdir $envFolder'/Fake'$QCDHT700
#mkdir $envFolder'/Fake'$QCDHT1000
#mkdir $envFolder'/Fake'$QCDHT1500
#mkdir $envFolder'/Fake'$QCDHT2000

python launchFakeMET.py $source/$QCDHT100'/*/*/*/tree*.root'  $envFolder/'ZvvHighPt_V15_Fake'$QCDHT100'.root'     >& logFakeQCDHT100 &
python launchFakeMET.py $source/$QCDHT200'/*/*/*/tree*.root'  $envFolder/'ZvvHighPt_V15_Fake'$QCDHT200'.root'     >& logFakeQCDHT200 &
python launchFakeMET.py $source/$QCDHT300'/*/*/*/tree*.root'  $envFolder/'ZvvHighPt_V15_Fake'$QCDHT300'.root'     >& logFakeQCDHT300 &
python launchFakeMET.py $source/$QCDHT500'/*/*/*/tree*.root'  $envFolder/'ZvvHighPt_V15_Fake'$QCDHT500'.root'     >& logFakeQCDHT500 &
python launchFakeMET.py $source/$QCDHT700'/*/*/*/tree*.root'  $envFolder/'ZvvHighPt_V15_Fake'$QCDHT700'.root'     >& logFakeQCDHT700 &
python launchFakeMET.py $source/$QCDHT1000'/*/*/*/tree*.root' $envFolder/'ZvvHighPt_V15_Fake'$QCDHT1000'.root'   >& logFakeQCDHT1000 &
python launchFakeMET.py $source/$QCDHT1500'/*/*/*/tree*.root' $envFolder/'ZvvHighPt_V15_Fake'$QCDHT1500'.root'   >& logFakeQCDHT1500 &
python launchFakeMET.py $source/$QCDHT2000'/*/*/*/tree*.root' $envFolder/'ZvvHighPt_V15_Fake'$QCDHT2000'.root'   >& logFakeQCDHT2000 &



