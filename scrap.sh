#!/bin/bash

#TODO rename to scrap

scrap_dir=$(pwd)
scrap=/tmp/scrap.tar.gz

if [ $# -gt 2 ]; then
    scrap_dir=$1
fi

# to be able to transfer any bytes through python3,
# i need the array to be translated to hex,
# in order to be able to encode it in utf-8.

tar -czvf $scrap_tar $scrap_dir 2>/dev/null
