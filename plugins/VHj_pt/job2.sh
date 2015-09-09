#!/bin/bash

#$ -q all.q
#$ -cwd

source $VO_CMS_SW_DIR/cmsset_default.sh
source /swshare/psit3/etc/profile.d/cms_ui_env.sh  # for bash
cd /shome/gaperrin/VHbb/CMSSW_7_4_3/src
eval `scramv1 ru -sh`

#roofit
cmsenv
. /swshare/ROOT/root_v5.34.18_slc6_amd64/bin/thisroot.sh

cd /shome/gaperrin/VHbb/CMSSW_7_4_3/src/Xbb/plugins/VHj_pt 
#$ -N job_V1
#$ -o /shome/gaperrin/VHbb/CMSSW_7_4_3/src/Xbb/plugins/VHj_pt/Log
#$ -e /shome/gaperrin/VHbb/CMSSW_7_4_3/src/Xbb/plugins/VHj_pt/Log

root -b VHF_Pt.C++
