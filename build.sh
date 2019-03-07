#!/bin/bash
SCRIPT=`realpath -s $0`
SCRIPTPATH=`dirname $SCRIPT`
cd $SCRIPTPATH

if [ ! -f external/CmakeStuff/GBA.cmake ]; then
    git submodule update --init -- external/CmakeStuff
fi

if [ ! -d build ]; then
    mkdir build
    cd build
    cmake --DCMAKE_TOOLCHAIN_FILE=external/CmakeStuff/GBA.cmake -GNinja ..
else
    cd build
fi

ninja