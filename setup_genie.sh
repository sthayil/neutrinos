#!/bin/bash

export GENIE=$PWD/GENIE-Generator_v2.12.10
export ROOTSYS=/afs/cern.ch/work/s/sthayil/neutrinos/root 
export LHAPATH=/afs/cern.ch/work/s/sthayil/neutrinos/lhapdf-5.9.1_install/data 

export PATH=$PATH:\
$ROOTSYS/bin:\
$GENIE/bin:\

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:\
/afs/cern.ch/work/s/sthayil/neutrinos/log4cpp_install/lib:\
/usr/lib:\
/afs/cern.ch/work/s/sthayil/neutrinos/lhapdf-5.9.1_install/lib:\
/afs/cern.ch/sw/lcg/external/lhapdfsets/current:\
/afs/cern.ch/work/s/sthayil/neutrinos/root_install/lib/root:\
$ROOTSYS/lib:\
$GENIE/lib

source $ROOTSYS/bin/thisroot.sh 