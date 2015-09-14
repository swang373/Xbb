#!/bin/bash

#$ -q all.q
#$ -cwd

# source $VO_CMS_SW_DIR/cmsset_default.sh
# source /swshare/psit3/etc/profile.d/cms_ui_env.sh  # for bash
cd /shome/perrozzi/for_gael/CMSSW_7_4_3/src/Xbb/macros
eval `scramv1 ru -sh`

#roofit
# cmsenv
# ./swshare/ROOT/root_v5.34.18_slc6_amd64/bin/thisroot.sh

cd /shome/perrozzi/for_gael/CMSSW_7_4_3/src/Xbb/macros/VHj_pt 
#$ -N job_V1
#$ -o /shome/gaperrin/VHbb/CMSSW_7_4_3/src/Xbb/plugins/VHj_pt/Log
#$ -e /shome/gaperrin/VHbb/CMSSW_7_4_3/src/Xbb/plugins/VHj_pt/Log

root -l -b 'VHF_Pt.C++(0)'
