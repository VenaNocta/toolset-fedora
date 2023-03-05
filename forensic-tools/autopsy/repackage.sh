#!/usr/bin/bash

WORKSPACE=~/rpmbuild
DRY_RUN=false
CLEAN=false
INFO=false
# info from manual lookup
LICENSE="Apache-2.0" 

print_help() {
  printf ">>> REPACKAGE AUTOPSY\n\n";
  printf "  -d | --dry-run             ... dont execute commands\n\n"
  printf "  -c | --clean               ... clean build path\n"
  printf "  -i | --info                ... show info\n"
  printf "  ____________________________________________________________________________\n"
  printf "  -h | --help                ... show this help page\n\n";
}

print_info() {
  printf ">>>  [INFO]\n"
  printf "==  Environment\n"
  printf ">>    WORKSPACE                = "$WORKSPACE"\n"
  printf ">>    SOURCE                   = https://github.com/sleuthkit/autopsy/releases/\n"
  printf ">>    LATEST GIT RELEASE       = "$GIT_TAG"\n"
  printf ">>    VERSION                  = "$VERSION"\n"
  printf ">>    LICENSE                  = "$LICENSE"\n"
  printf "  ____________________________________________________________________________\n"
  printf "==  Tools\n"
  printf "  ____________________________________________________________________________\n\n"
}

gen_spec() {
  printf "# SPEC FILE IS JUST A BLUEPRINT AT THIS POINT!!!\n\n" >  $SPEC_FILE
  printf "Name:           autopsy-core\n" >>  $SPEC_FILE
  printf "Version:        "$VERSION"\n" >> $SPEC_FILE
  printf "Release:        1\n" >> $SPEC_FILE
  printf "BuildArch:      noarch\n" >> $SPEC_FILE
  printf "Summary:        Autopsy repackaged for RPM based systems\n\n" >> $SPEC_FILE
  printf "License:        "$LICENSE"\n" >> $SPEC_FILE
  printf "URL:            https://www.sleuthkit.org/autopsy/\n" >> $SPEC_FILE
  printf "Source0:        %%{name}-%%{version}.tar.xz\n\n" >> $SPEC_FILE
  printf "Requires:       testdisk\n" >> $SPEC_FILE
  printf "Requires:       java-1.8.0-openjdk\n" >> $SPEC_FILE
  printf "Requires:       sleuthkit\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "%%description\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "%%prep\n" >> $SPEC_FILE
  printf "rm -rf %%{_builddir}/%%{name}-%%{version}/\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "%%install\n" >> $SPEC_FILE
  printf "rm -rf \$RPM_BUILD_ROOT\n" >> $SPEC_FILE
  printf "mkdir -p \$RPM_BUILD_ROOT/%%{_bindir}\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
#        awk '!/^\s*#?\s*jdkhome=.*$/' etc/$APPLICATION_NAME.conf > etc/$APPLICATION_NAME.conf.tmp && \
#        mv etc/$APPLICATION_NAME.conf.tmp etc/$APPLICATION_NAME.conf && \
#        echo "jdkhome=$JAVA_PATH" >> etc/$APPLICATION_NAME.conf
# make sure thirdparty files are executable
#chmod u+x autopsy/markmckinnon/Export*
#chmod u+x autopsy/markmckinnon/parse*
#
# allow solr dependencies to execute
#chmod -R u+x autopsy/solr/bin
#
# make sure it is executable
#chmod u+x bin/$APPLICATION_NAME
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
  cat $WORKSPACE"/REPACK/autopsy-"$VERSION"/NEWS.txt" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
}

patch_autopsy() {
  printf ">>    (3.1)                    » patching bin/autopsy\n"
  cp $(dirname $0)"/patches/bin/autopsy" $WORKSPACE"/REPACK/autopsy-"$VERSION"/bin/autopsy"
}

pack_autopsy_core() {
  printf ">>    (4.1)                    » building autopsy-core-"$VERSION".tar.xz\n"
  pushd $WORKSPACE"/REPACK/autopsy-"$VERSION
  tar -I "pxz -9" -cvf $WORKSPACE"/SOURCES/autopsy-core-"$VERSION".tar.xz" \
      icon.ico LICENSE-2.0.txt README.txt \
      bin/autopsy \
      etc platform java docs
  popd
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

printf ">>>  [Repackage Autopsy as RPMs]\n"
printf ">>    URL                      = "$URL"\n"
printf ">>    FILE                     = "$WORKSPACE"/BUILD/"$ORIG_PACKAGE"\n"
printf "  ____________________________________________________________________________\n"
mkdir -p $WORKSPACE"/REPACK/"
if [ -f $WORKSPACE"/REPACK/"$ORIG_PACKAGE ]; then
  printf ">>    (1) zip archive located  » skipping download\n"
else
  printf ">>    (1) zip archive missing  » download from GitHub Releases\n\n"
  curl -L -o $WORKSPACE"/REPACK/"$ORIG_PACKAGE $URL
fi
if [ -d $WORKSPACE"/REPACK/autopsy-"$VERSION ]; then
  printf ">>    (2) data located         » skipping decompression\n"
else
  printf ">>    (2) data missing         » unpacking archive\n"
  unzip -qod $WORKSPACE"/REPACK/" $WORKSPACE"/REPACK/"$ORIG_PACKAGE
fi
printf ">>    (3)                      » patching data\n"
patch_autopsy
printf ">>    (4)                      » building compressed archives\n"
#pack_autopsy_core

# repackage with just the required files!!!


SPEC_FILE=$WORKSPACE/SPECS/autopsy-core.spec
printf "=== BUILDING RPM \n"
printf ">>    SPEC FILE                = "$SPEC_FILE"\n"
printf ">>    RPM                      = ???\n"
printf "  ____________________________________________________________________________\n"
printf ">>    (1)                      » compiling autopsy.spec file\n"
gen_spec
printf ">>    (2)                      » building autopsy-core-"$VERSION"-1.src.rpm\n"
#rpmbuild -bs $SPEC_FILE
printf ">>    (3)                      » building autopsy-core-"$VERSION"-1.rpm\n"
#rpmbuild -bb $SPEC_FILE









