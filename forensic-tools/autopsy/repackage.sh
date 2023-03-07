#!/usr/bin/bash

WORKSPACE=~/rpmbuild
DRY_RUN=false
CLEAN=false
INFO=false
# info from manual lookup
LICENSE="Apache-2.0" 
RELEASE="1"

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

gen_spec() {
  printf "Name:           autopsy-core\n" >  $SPEC_FILE
  printf "Version:        "$VERSION"\n" >> $SPEC_FILE
  printf "Release:        "$RELEASE"\n" >> $SPEC_FILE
  printf "ExclusiveArch:  %%{java_arches} x86_64\n" >> $SPEC_FILE
  printf "Summary:        Autopsy repackaged for RPM based systems\n\n" >> $SPEC_FILE
  printf "License:        "$LICENSE"\n" >> $SPEC_FILE
  printf "URL:            https://www.sleuthkit.org/autopsy/\n" >> $SPEC_FILE
  printf "Source0:        %%{name}-%%{version}.tar.xz\n\n" >> $SPEC_FILE
  printf "AutoReqProv: no\n" >> $SPEC_FILE
  printf "Requires:       testdisk\n" >> $SPEC_FILE
  printf "Requires:       java-1.8.0-openjdk\n" >> $SPEC_FILE
  printf "Requires:       sleuthkit-java-bindings\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "%%description\n" >> $SPEC_FILE
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
  printf "# copy files to target\n" >> $SPEC_FILE
  printf "pushd  %%{_builddir}/%%{name}-%%{version}\n" >> $SPEC_FILE
  printf "mkdir -p %%{buildroot}%%{_bindir}/\n" >> $SPEC_FILE
  printf "cp -n  bin/autopsy                    %%{buildroot}%%{_bindir}/\n" >> $SPEC_FILE
  printf "mkdir -p %%{buildroot}%%{_sysconfdir}/\n" >> $SPEC_FILE
  printf "cp -nr etc/*                          %%{buildroot}%%{_sysconfdir}/\n" >> $SPEC_FILE
  printf "mkdir -p %%{buildroot}%%{_libdir}/autopsy/\n" >> $SPEC_FILE
  printf "cp -n  README.txt                     %%{buildroot}%%{_libdir}/autopsy/\n" >> $SPEC_FILE
  printf "cp -n  CHANGELOG.txt                  %%{buildroot}%%{_libdir}/autopsy/\n" >> $SPEC_FILE
  printf "cp -n  LICENSE-2.0.txt                %%{buildroot}%%{_libdir}/autopsy/\n" >> $SPEC_FILE
  printf "cp -nr autopsy/                       %%{buildroot}%%{_libdir}/autopsy/\n" >> $SPEC_FILE
  printf "cp -nr java/                          %%{buildroot}%%{_libdir}/autopsy/\n" >> $SPEC_FILE
  printf "cp -nr platform/                      %%{buildroot}%%{_libdir}/autopsy/\n" >> $SPEC_FILE
## for some reason it already contains TSK
#  printf "mkdir -p %%{buildroot}%%{_libdir}/autopsy/autopsy/modules/ext/\n" >> $SPEC_FILE
#  printf "ln -s  %%{_libdir}/sleuthkit.jar      %%{buildroot}%%{_libdir}/autopsy/autopsy/modules/ext/sleuthkit.jar\n" >> $SPEC_FILE
  printf "mkdir -p %%{buildroot}%%{_datadir}/applications/\n" >> $SPEC_FILE
  printf "cp -n  org.sleuthkit.autopsy.desktop  %%{buildroot}%%{_datadir}/applications/\n" >> $SPEC_FILE
  printf "mkdir -p %%{buildroot}%%{_datadir}/icons/autopsy/\n" >> $SPEC_FILE
  printf "cp -n  autopsy.png                    %%{buildroot}%%{_datadir}/icons/autopsy/\n" >> $SPEC_FILE
  printf "mkdir -p %%{buildroot}%%{_docdir}/autopsy/\n" >> $SPEC_FILE
  printf "cp -nr docs/*                         %%{buildroot}%%{_docdir}/autopsy/\n" >> $SPEC_FILE
  printf "popd\n" >> $SPEC_FILE
  printf "# update jdkhome\n" >> $SPEC_FILE
  printf "awk '!/^\s*#?\s*jdkhome=.*$/' %%{name}-%%{version}/etc/autopsy.conf > %%{buildroot}%%{_sysconfdir}/autopsy.conf\n" >> $SPEC_FILE
  printf "printf \"jdkhome=/usr/lib/jvm/java-1.8.0-openjdk\\" >> $SPEC_FILE
  printf "n\" >> %%{buildroot}%%{_sysconfdir}/autopsy.conf\n" >> $SPEC_FILE
  printf "# make sure thirdparty files are executable\n" >> $SPEC_FILE
  printf "chmod +x %%{buildroot}%%{_libdir}/autopsy/autopsy/markmckinnon/Export*\n" >> $SPEC_FILE
  printf "chmod +x %%{buildroot}%%{_libdir}/autopsy/autopsy/markmckinnon/parse*\n" >> $SPEC_FILE
  printf "# allow solr dependencies to execute\n" >> $SPEC_FILE
  printf "chmod -R +x %%{buildroot}%%{_libdir}/autopsy/autopsy/solr/bin\n" >> $SPEC_FILE
  printf "# make sure the start script is executable\n" >> $SPEC_FILE
  printf "chmod +x %%{buildroot}%%{_bindir}/autopsy\n" >> $SPEC_FILE
  printf "# stop the toolkit from doing other stuff\n" >> $SPEC_FILE
  printf "exit 0\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "%%clean\n" >> $SPEC_FILE
  printf "rm -rf %%{buildroot}\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
  printf "%%files\n" >> $SPEC_FILE
  printf "%%{_datadir}/applications/org.sleuthkit.autopsy.desktop\n" >> $SPEC_FILE
  printf "%%{_bindir}/autopsy\n" >> $SPEC_FILE
  printf "%%{_libdir}/autopsy/\n" >> $SPEC_FILE
  printf "%%{_datadir}/icons/autopsy/\n" >> $SPEC_FILE
  printf "%%{_docdir}/autopsy/\n" >> $SPEC_FILE
  printf "%%config(noreplace) %%{_sysconfdir}/autopsy.clusters\n" >> $SPEC_FILE
  printf "%%config(noreplace) %%{_sysconfdir}/autopsy.conf\n" >> $SPEC_FILE
  printf "%%docdir            %%{_docdir}/autopsy/\n" >> $SPEC_FILE
  printf "%%license           %%{_libdir}/autopsy/LICENSE-2.0.txt\n" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
# changelog redacted - file structure mismatch
#  printf "%%changelog\n" >> $SPEC_FILE
#  cat $WORKSPACE"/REPACK/autopsy-"$VERSION"/NEWS.txt" >> $SPEC_FILE
#  printf "\n" >> $SPEC_FILE
}

patch_autopsy() {
  printf ">>    (3.1)                    » patching bin/autopsy\n"
  cp $(dirname $0)"/patches/bin/autopsy" $WORKSPACE"/REPACK/autopsy-"$VERSION"/bin/autopsy"

  printf ">>    (3.2)                    » patching CHANGELOG.txt\n"
  [ -f $WORKSPACE"/REPACK/autopsy-"$VERSION"/NEWS.txt" ] && mv $WORKSPACE"/REPACK/autopsy-"$VERSION"/NEWS.txt" $WORKSPACE"/REPACK/autopsy-"$VERSION"/CHANGELOG.txt"

  printf ">>    (3.3)                    » patching autopsy.png\n"
  curl -L -o $WORKSPACE"/REPACK/autopsy-"$VERSION"/autopsy.png" "https://raw.githubusercontent.com/sleuthkit/autopsy/develop/unix/autopsy.png"

  DESKTOP_FILE=$WORKSPACE"/REPACK/autopsy-"$VERSION"/org.sleuthkit.autopsy.desktop"
  printf ">>    (3.4)                    » patching org.sleuthkit.autopsy.desktop\n"
  printf "[Desktop Entry]\n"                                   >  $DESKTOP_FILE
  printf "Version="$VERSION"\n"                                >> $DESKTOP_FILE
  printf "Name=Autopsy\n"                                      >> $DESKTOP_FILE
  printf "Comment=Complete Digital forensics analysis suite\n" >> $DESKTOP_FILE
  printf "Exec=/usr/bin/autopsy\n"                             >> $DESKTOP_FILE
  printf "Icon=/usr/share/icons/autopsy/autopsy.png\n"         >> $DESKTOP_FILE
  printf "Terminal=false\n"                                    >> $DESKTOP_FILE
  printf "Type=Application\n"                                  >> $DESKTOP_FILE
  printf "Categories=Utility;System;\n"                        >> $DESKTOP_FILE
}

pack_autopsy_core() {
  pushd $WORKSPACE"/REPACK/autopsy-"$VERSION
  tar -I "pxz -9" -cf $WORKSPACE"/SOURCES/autopsy-core-"$VERSION".tar.xz" \
      icon.ico LICENSE-2.0.txt README.txt CHANGELOG.txt \
      bin/autopsy autopsy.png org.sleuthkit.autopsy.desktop \
      etc autopsy platform java docs
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

GIT_TAG=$(git ls-remote --refs --sort='version:refname' --tags https://github.com/sleuthkit/autopsy.git 'autopsy-*.*.*' | tail --lines=1 | cut --delimiter='/' --fields=3)
VERSION=$(printf $GIT_TAG | cut --delimiter='-' --fields=2)

# clear
if $CLEAN; then
  printf "=== CLEAN $WORKSPACE/...\n\n"
  rm -rf $WORKSPACE/REPACK/autopsy-${VERSION}*
  rm -rf $WORKSPACE/BUILD/autopsy-core-${VERSION}*
  rm -rf $WORKSPACE/BUILDROOT/autopsy-core-${VERSION}*
  rm -rf $WORKSPACE/SOURCES/autopsy-core-${VERSION}*
  rm -f  $WORKSPACE/SPECS/autopsy-core-${VERSION}.spec
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

# unpack
if [ -d $WORKSPACE"/REPACK/autopsy-"$VERSION ]; then
  printf ">>    (2) data located         » skipping decompression\n"
else
  printf ">>    (2) data missing         » unpacking archive\n"
  unzip -qod $WORKSPACE"/REPACK/" $WORKSPACE"/REPACK/"$ORIG_PACKAGE
fi

# patch
printf ">>    (3)                      » patching data\n"
patch_autopsy

# repackage with just the required files!!!
printf ">>    (4)                      » building compressed archives\n"
if [ -f $WORKSPACE"/SOURCES/autopsy-core-"$VERSION".tar.xz" ]; then
  printf ">>    (4.1)                    » found autopsy-core-"$VERSION".tar.xz\n"
else
  printf ">>    (4.1)                    » building autopsy-core-"$VERSION".tar.xz\n"
  pack_autopsy_core
fi

SPEC_FILE=$WORKSPACE/SPECS/autopsy-core-${VERSION}.spec
printf "=== BUILDING RPM \n"
printf ">>    SPEC FILE                = "$SPEC_FILE"\n"
printf ">>    SRPM                     = autopsy-core-"$VERSION"-"$RELEASE".src.rpm\n"
printf ">>    RPM                      = autopsy-core-"$VERSION"-"$RELEASE".x86_64.rpm\n"
printf "  ____________________________________________________________________________\n"
printf ">>    (1)                      » compiling autopsy.spec file\n"
gen_spec
printf ">>    (2)                      » building autopsy-core-"$VERSION"-1.src.rpm\n"
rpmbuild -bs $SPEC_FILE
printf ">>    (3)                      » building autopsy-core-"$VERSION"-1.rpm\n"
rpmbuild -bb $SPEC_FILE

