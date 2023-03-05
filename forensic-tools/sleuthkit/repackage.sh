#!/usr/bin/bash

WORKSPACE=~/rpmbuild
DRY_RUN=false
CLEAN=false
INFO=false
# info from manual lookup
LICENSE="Apache-2.0" 

print_help() {
  printf ">>> REPACKAGE AUTOPSY\n\n";
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

gen_core_spec() {
  printf "Name:           sleuthkit-java-bindings\n" >  $SPEC_FILE
  printf "Version:        "$VERSION"\n" >> $SPEC_FILE
  printf "Release:        1\n" >> $SPEC_FILE
  printf "#Conflicts:      sleuthkit\n" >> $SPEC_FILE
  printf "ExclusiveArch:  %%{java_arches} x86_64\n" >> $SPEC_FILE
  printf "Summary:        Sleuthkit Java Bindings repackaged for RPM based systems\n\n" >> $SPEC_FILE
  printf "License:        "$LICENSE"\n" >> $SPEC_FILE
  printf "URL:            https://www.sleuthkit.org/sleuthkit/\n" >> $SPEC_FILE
  printf "Source0:        %%{name}-%%{version}.tar.xz\n\n" >> $SPEC_FILE
  printf "BuildRequires:  make\n" >> $SPEC_FILE
  printf "BuildRequires:  libtool\n" >> $SPEC_FILE
  printf "BuildRequires:  gcc-c++\n" >> $SPEC_FILE
  printf "BuildRequires:  ant\n" >> $SPEC_FILE
  printf "BuildRequires:  ant-antunit\n" >> $SPEC_FILE
  printf "BuildRequires:  sqlite-devel\n" >> $SPEC_FILE
  printf "Requires:       java-1.8.0-openjdk\n" >> $SPEC_FILE
  printf "Requires:       mac-robber\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "%%description\n" >> $SPEC_FILE
  printf "The Sleuth Kit (TSK) is a collection of UNIX-based command line tools that\n" >> $SPEC_FILE
  printf "allow you to investigate a computer. The current focus of the tools is the\n" >> $SPEC_FILE
  printf "file and volume systems and TSK supports FAT, Ext2/3, NTFS, UFS,\n" >> $SPEC_FILE
  printf "and ISO 9660 file systems\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "%%prep\n" >> $SPEC_FILE
  printf "rm -rf %%{_builddir}/%%{name}-%%{version}/\n" >> $SPEC_FILE
  printf "mkdir -p %%{_builddir}/%%{name}-%%{version}\n" >> $SPEC_FILE
  printf "pushd %%{_builddir}/%%{name}-%%{version}\n" >> $SPEC_FILE
  printf "tar -xf %%{_sourcedir}/%%{name}-%%{version}.tar.xz\n" >> $SPEC_FILE
  printf "popd\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE

  printf "%%install\n" >> $SPEC_FILE
  printf "rm -rf %%{buildroot}\n" >> $SPEC_FILE
  printf "mkdir -p %%{buildroot}/\n" >> $SPEC_FILE

  printf "\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE

  printf "pushd  %%{_builddir}/%%{name}-%%{version}\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE

#  printf "mkdir -p %%{buildroot}%%{_docdir}/autopsy/\n" >> $SPEC_FILE
#  printf "cp -nr docs/*                         %%{buildroot}%%{_docdir}/autopsy/\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "# copy files to target\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "popd\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "exit 0\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "%%clean\n" >> $SPEC_FILE
  printf "rm -rf %%{buildroot}\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "%%files\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
# changelog redacted
#  printf "%%changelog\n" >> $SPEC_FILE
#  printf "\n" >> $SPEC_FILE
}

patch_sleuthkit() {
  printf ">>    (3.1)                    » patching bin/autopsy\n"
  SRC_DIR=$WORKSPACE"/REPACK/sleuthkit-"$VERSION"/src/"
  TARGET_DIR=$WORKSPACE"/REPACK/sleuthkit-"$VERSION"/target/"
  mkdir -p $TARGET_DIR
  pushd $SRC_DIR
  JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk ./configure --disable-cppunit --enable-java --prefix $TARGET_DIR --exec-prefix=$TARGET_DIR"usr/"
  make install
  find $TARGET_DIR -name '*.la' -exec rm -f {} ';'
  rm -rf $TARGET_DIR"/pkgconfig/"
  popd
}

pack_sleuthkit-java-bindings() {
  pushd $WORKSPACE"/REPACK/sleuthkit-"$VERSION"/src/"
  tar -I "pxz -9" -cf $WORKSPACE"/SOURCES/sleuthkit-java-bindings-"$VERSION".tar.xz" \
      *
  popd
}

while [ True ]; do
if [ "$1" = "--help" -o "$1" = "-h" ]; then
  print_help
  exit 0
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

GIT_TAG=$(git ls-remote --refs --sort='version:refname' --tags https://github.com/sleuthkit/sleuthkit.git 'sleuthkit-*.*.*' | tail --lines=1 | cut --delimiter='/' --fields=3)
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

URL="https://github.com/sleuthkit/sleuthkit/releases/download/"$GIT_TAG"/sleuthkit-"$VERSION".tar.gz"
ORIG_PACKAGE="sleuthkit-"$VERSION".tar.gz"

printf ">>>  [Repackage Sleuthkit Java Bindings as RPMs]\n"
printf ">>    URL                      = "$URL"\n"
printf ">>    FILE                     = "$WORKSPACE"/BUILD/"$ORIG_PACKAGE"\n"
printf "  ____________________________________________________________________________\n"
mkdir -p $WORKSPACE"/REPACK/"
if [ -f $WORKSPACE"/REPACK/"$ORIG_PACKAGE ]; then
  printf ">>    (1) tar archive located  » skipping download\n"
else
  printf ">>    (1) tar archive missing  » download from GitHub Releases\n\n"
  curl -L -o $WORKSPACE"/REPACK/"$ORIG_PACKAGE $URL
fi

# unpack
if [ -d $WORKSPACE"/REPACK/sleuthkit-"$VERSION ]; then
  printf ">>    (2) data located         » skipping decompression\n"
else
  printf ">>    (2) data missing         » unpacking archive\n"
  mkdir -p $WORKSPACE"/REPACK/sleuthkit-"$VERSION"/"
  tar -xf $WORKSPACE"/REPACK/"$ORIG_PACKAGE -C $WORKSPACE"/REPACK/sleuthkit-"$VERSION"/"
  mv $WORKSPACE"/REPACK/sleuthkit-"$VERSION"/sleuthkit-"$VERSION"/" $WORKSPACE"/REPACK/sleuthkit-"$VERSION"/src/"
fi

# patch
printf ">>    (3)                      » patching data\n"
patch_sleuthkit

# repackage with just the required files!!!
printf ">>    (4)                      » building compressed archives\n"
if [ -f $WORKSPACE"/SOURCES/sleuthkit-java-bindings-"$VERSION".tar.xz" ]; then
  printf ">>    (4.1)                    » found sleuthkit-java-bindings-"$VERSION".tar.xz\n"
else
  printf ">>    (4.1)                    » building sleuthkit-java-bindings-"$VERSION".tar.xz\n"
  pack_sleuthkit-java-bindings
fi


SPEC_FILE=$WORKSPACE/SPECS/sleuthkit-java-bindings.spec
printf "=== BUILDING RPM \n"
printf ">>    SPEC FILE                = "$SPEC_FILE"\n"
printf ">>    RPM                      = sleuthkit-java-bindings-"$VERSION"-1.x86_64.rpm\n"
printf "  ____________________________________________________________________________\n"
printf ">>    (1)                      » compiling autopsy.spec file\n"
gen_core_spec
printf ">>    (2)                      » building sleuthkit-java-bindings-"$VERSION"-1.src.rpm\n"
#rpmbuild -bs $SPEC_FILE
printf ">>    (3)                      » building sleuthkit-java-bindings-"$VERSION"-1.rpm\n"
#rpmbuild -bb $SPEC_FILE

