#!/bin/bash

#TODO rename to scrap

scrap_dir=$(pwd)
scrap_tar=/tmp/scrap.tar
scrap_zip=/tmp/scrap.zip
if $# -gt 2; then
    scrab_dir=$1
fi
tar cvf $scrap_tar $scrap_dir 2>/dev/null 
zip $scrap_zip $scrap_tar 2>/dev/null
