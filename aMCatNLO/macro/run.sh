#/bin/bash

nevt=${1}

#source /afs/cern.ch/cms/cmsset_default.sh
#export SCRAM_ARCH=slc6_amd64_gcc472

#cd /afs/cern.ch/work/y/youngjo/slc6/cmssw/CMSSW_5_3_19/src
#eval `scramv1 runtime -s`

#cd /afs/cern.ch/work/y/youngjo/public/For8Tev/aMCatNLO/ttbb/lhe2

python LHEploter.py $nevt #| grep eff > log_${nevt}.txt

