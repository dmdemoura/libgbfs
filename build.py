#!/usr/bin/python3
import subprocess
import pathlib
import os
import sys

##############
#CONFIG START#
##############

cmakePrefixPath = [
]
cmakeToolchainFile = 'buildsystem/GBA.cmake'
buildsystemRoot = 'buildsystem'
buildFolder = 'build'
generator = 'Ninja'

##############
# END CONFIG #
##############

def asFullPathStr(path):
    return str(pathlib.Path(path).absolute())

def asCollonSeparatedPathList(pathList):
    pathListStr = ""
    
    for path in pathList:
        pathListStr += path + ";"

    return pathListStr

cmd = [
    'cmake',
    '-G' + generator + '',
    '-DBUILDSYSTEM_ROOT=' + asFullPathStr(buildsystemRoot),
    '-DCMAKE_MODULE_PATH=' + asFullPathStr(buildsystemRoot),
    '-DCMAKE_PREFIX_PATH=' + asCollonSeparatedPathList(cmakePrefixPath),
    '-DCMAKE_TOOLCHAIN_FILE=' + asFullPathStr(cmakeToolchainFile),
    str(pathlib.Path('.').absolute())
]

if not pathlib.Path(buildFolder).exists():
    pathlib.Path(buildFolder).mkdir()
elif not pathlib.Path(buildFolder).is_dir():
    print("Error: Can't create build folder, file with same name exists")
    sys.exit()

subprocess.run(cmd, cwd=buildFolder)