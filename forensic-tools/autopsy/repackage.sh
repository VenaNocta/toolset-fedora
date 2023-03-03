#!/usr/bin/bash

WORKSPACE=~/rpmbuild
DRY_RUN=false
CLEAN=false
INFO=false
# info from manual lookup
LICENSE="Apache-2.0" 

print_help() {
  printf ">>> REPACKAGE AUTOPSY\n\n";
  printf "  -d | --dry-run         ... dont execute commands\n\n"
  printf "  -c | --clean           ... clean build path\n"
  printf "  -i | --info            ... show info\n"
  printf "  ____________________________________________________________________________\n"
  printf "  -h | --help            ... show this help page\n\n";
}

print_info() {
  printf ">>>  [INFO]\n"
  printf "==  Environment\n"
  printf ">>    WORKSPACE             = "$WORKSPACE"\n"
  printf ">>    SOURCE                = https://github.com/sleuthkit/autopsy/releases/\n"
  printf ">>    LATEST GIT RELEASE    = "$GIT_TAG"\n"
  printf ">>    VERSION               = "$VERSION"\n"
  printf ">>    LICENSE               = "$LICENSE"\n"
  printf "  ____________________________________________________________________________\n"
  printf "==  Tools\n"
  printf "  ____________________________________________________________________________\n\n"
}

gen_spec() {
  printf "# SPEC FILE IS JUST A BLUEPRINT AT THIS POINT!!!\n\n" >  $SPEC_FILE
  printf "Name:           autopsy\n" >>  $SPEC_FILE
  printf "Version:        4.20.0\n" >> $SPEC_FILE
  printf "Release:        1%%{?dist} \n" >> $SPEC_FILE
  printf "Summary:        \n\n" >> $SPEC_FILE
  printf "License:        "$LICENSE"\n" >> $SPEC_FILE
  printf "URL:            https://www.sleuthkit.org/autopsy/\n" >> $SPEC_FILE
  printf "Source0:        \n\n" >> $SPEC_FILE
  printf "Requires:       testdisk\n" >> $SPEC_FILE
  printf "Requires:       java-1.8.0-openjdk\n" >> $SPEC_FILE
  printf "Requires:       sleuthkit\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "%%description\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "%%prep\n" >> $SPEC_FILE
  printf "%%autosetup\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "%%build\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "%%install\n" >> $SPEC_FILE
  printf "%%make_install\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "%%files\n" >> $SPEC_FILE
  printf "%%license LICENSE-2.0.txt\n" >> $SPEC_FILE
  printf "%%doc add-docs-here\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "%%changelog\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
}

while [ True ]; do
if [ "$1" = "--help" -o "$1" = "-h" ]; then
  print_help
  exit 0
elif [ "$1" = "--dry-run" -o "$1" = "-d" ]; then
  DRY_RUN=true
  shift 1
elif [ "$1" = "--clean" -o "$1" = "-c" ]; then
  CLEAN=true
  shift 1
elif [ "$1" = "--info" -o "$1" = "-i" ]; then
  INFO=true
  shift 1
else
  break
fi
done

GIT_TAG=$(git ls-remote --refs --sort='version:refname' --tags https://github.com/sleuthkit/autopsy.git 'autopsy-*.*.*' | tail --lines=1 | cut --delimiter='/' --fields=3)
VERSION=$(printf $GIT_TAG | cut --delimiter='-' --fields=2)

# clear
if $CLEAN; then
  printf "=== CLEAN $WORKSPACE/*\n\n"
  rm -rf $WORKSPACE/*
fi

rpmdev-setuptree
mkdir -p $WORKSPACE/REPACK

# info
if $INFO; then
  print_info
fi

URL="https://github.com/sleuthkit/autopsy/releases/download/"$GIT_TAG"/autopsy-"$VERSION".zip"
ORIG_PACKAGE="autopsy-"$VERSION".zip"

printf "=== SOURCES\n"
printf ">>    URL                   = "$URL"\n"
printf ">>    FILE                  = "$WORKSPACE"/REPACK/"$ORIG_PACKAGE"\n"
printf "  ____________________________________________________________________________\n"
if [ -f $WORKSPACE"/REPACK/"$ORIG_PACKAGE ]; then
  printf ">>    file located          » skipping download\n"
else
  printf ">>    file missing          » download from GitHub Releases\n\n"
  curl -L -o $WORKSPACE"/REPACK/"$ORIG_PACKAGE $URL
fi

TAR_GZ_PACKAGE="autopsy-"$VERSION".tar.gz"
printf "=== REBUILDING \n"
printf ">>    URL                   = "$URL"\n"
printf ">>    ORIGINAL              = "$WORKSPACE"/REPACK/"$ORIG_PACKAGE"\n"
printf ">>    TARGET                = "$WORKSPACE"/REPACK/"$TAR_GZ_PACKAGE"\n"
printf "  ____________________________________________________________________________\n"

if [ -d $WORKSPACE"/REPACK/autopsy-"$VERSION ]; then
  printf ">>    extracting            » folder exists\n"
else
  printf ">>    extracting            » unzipping original\n"
  unzip -d $WORKSPACE"/REPACK/" $WORKSPACE"/REPACK/"$ORIG_PACKAGE
fi

# repackage with just the required files!!!


SPEC_FILE=$WORKSPACE/SPECS/autopsy.spec
printf "=== BUILDING RPM \n"
printf ">>    SPEC FILE             = "$SPEC_FILE"\n"
printf ">>    RPM                   = ???\n"
printf "  ____________________________________________________________________________\n"
printf ">>    (1)                   » compiling spec file\n"
gen_spec












