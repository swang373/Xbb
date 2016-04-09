#source /afs/pi.infn.it/grid_exp_sw/cms/scripts/setcms.sh
#setenv SCRAM_ARCH="slc5_amd64_gcc462"
#source $VO_CMS_SW_DIR/cmsset_default.sh
#eval `scramv1 runtime -sh`
##eval `cmsenv`

setenv envFolder    ../MCAndDataLinks/
setenv source_      ../MCAndDataLinks/

#/gpfs/ddn/srm/cms/store/user/arizzi/VHBBHeppyV14/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/*/*/*/tree*.root

setenv QCDHT100     QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
setenv QCDHT200     QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
setenv QCDHT300     QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
setenv QCDHT500     QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
setenv QCDHT700     QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
setenv QCDHT1000    QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
setenv QCDHT1500    QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
setenv QCDHT2000    QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8

mkdir $envFolder'/Skim'$QCDHT100
mkdir $envFolder'/Skim'$QCDHT200
mkdir $envFolder'/Skim'$QCDHT300
mkdir $envFolder'/Skim'$QCDHT500
mkdir $envFolder'/Skim'$QCDHT700
mkdir $envFolder'/Skim'$QCDHT1000
mkdir $envFolder'/Skim'$QCDHT1500
mkdir $envFolder'/Skim'$QCDHT2000

python launchSkimForFakeMET.py $source_/$QCDHT100  $envFolder'/Skim'$QCDHT100'/'     >& logSkimQCDHT100 &
python launchSkimForFakeMET.py $source_/$QCDHT200  $envFolder'/Skim'$QCDHT200'/'     >& logSkimQCDHT200 &
python launchSkimForFakeMET.py $source_/$QCDHT300  $envFolder'/Skim'$QCDHT300'/'     >& logSkimQCDHT300 &
python launchSkimForFakeMET.py $source_/$QCDHT500  $envFolder'/Skim'$QCDHT500'/'     >& logSkimQCDHT500 &
python launchSkimForFakeMET.py $source_/$QCDHT700  $envFolder'/Skim'$QCDHT700'/'     >& logSkimQCDHT700 &
python launchSkimForFakeMET.py $source_/$QCDHT1000 $envFolder'/Skim'$QCDHT1000'/'    >& logSkimQCDHT1000 &
python launchSkimForFakeMET.py $source_/$QCDHT1500 $envFolder'/Skim'$QCDHT1500'/'    >& logSkimQCDHT1500 &
python launchSkimForFakeMET.py $source_/$QCDHT2000 $envFolder'/Skim'$QCDHT2000'/'    >& logSkimQCDHT2000 &



