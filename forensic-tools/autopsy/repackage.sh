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
  printf "Version:        "$VERSION"\n" >> $SPEC_FILE
  printf "Release:        1\n" >> $SPEC_FILE
  printf "BuildArch:      noarch\n" >> $SPEC_FILE
  printf "Summary:        Autopsy repackaged for RPM based systems\n\n" >> $SPEC_FILE
  printf "License:        "$LICENSE"\n" >> $SPEC_FILE
  printf "URL:            https://www.sleuthkit.org/autopsy/\n" >> $SPEC_FILE
  printf "Source0:        %%{name}-%%{version}.zip\n\n" >> $SPEC_FILE
  printf "Requires:       testdisk\n" >> $SPEC_FILE
  printf "Requires:       java-1.8.0-openjdk\n" >> $SPEC_FILE
  printf "Requires:       sleuthkit\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "%%description\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "%%prep\n" >> $SPEC_FILE
  printf "rm -rf %%{_builddir}/%%{name}-%%{version}/\n" >> $SPEC_FILE
  printf "unzip -d %%{_builddir} %%{_sourcedir}/%%{name}-%%{version}.zip\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "%%install\n" >> $SPEC_FILE
  printf "rm -rf \$RPM_BUILD_ROOT\n" >> $SPEC_FILE
  printf "mkdir -p \$RPM_BUILD_ROOT/%%{_bindir}\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
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
mkdir -p $WORKSPACE/BUILD

# info
if $INFO; then
  print_info
fi

URL="https://github.com/sleuthkit/autopsy/releases/download/"$GIT_TAG"/autopsy-"$VERSION".zip"
ORIG_PACKAGE="autopsy-"$VERSION".zip"

printf "=== SOURCES\n"
printf ">>    URL                   = "$URL"\n"
printf ">>    FILE                  = "$WORKSPACE"/BUILD/"$ORIG_PACKAGE"\n"
printf "  ____________________________________________________________________________\n"
if [ -f $WORKSPACE"/SOURCES/"$ORIG_PACKAGE ]; then
  printf ">>    file located          » skipping download\n"
else
  printf ">>    file missing          » download from GitHub Releases\n\n"
  curl -L -o $WORKSPACE"/SOURCES/"$ORIG_PACKAGE $URL
fi

# repackage with just the required files!!!


SPEC_FILE=$WORKSPACE/SPECS/autopsy.spec
printf "=== BUILDING RPM \n"
printf ">>    SPEC FILE             = "$SPEC_FILE"\n"
printf ">>    RPM                   = ???\n"
printf "  ____________________________________________________________________________\n"
printf ">>    (1)                   » compiling autopsy.spec file\n"
gen_spec
printf ">>    (2)                   » building autopsy-"$VERSION"-1.src.rpm\n"
rpmbuild -bs $SPEC_FILE
printf ">>    (3)                   » building autopsy-"$VERSION"-1.rpm\n"
rpmbuild -bb $SPEC_FILE









