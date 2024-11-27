#!/usr/bin/bash

WORKSPACE=~/rpmbuild
DRY_RUN=false
CLEAN=false
INFO=false
# info from manual lookup
LICENSE="Apache-2.0" 
RELEASE="1"
JAVA_VERSION=17

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
  cat << EOF > $SPEC_FILE
Name:           autopsy-core
Version:        $VERSION
Release:        $RELEASE
ExclusiveArch:  %{java_arches} x86_64
Summary:        Autopsy repackaged for RPM based systems

License:        $LICENSE
URL:            https://www.sleuthkit.org/autopsy/
Source0:        %{name}-%{version}.tar.xz

AutoReqProv:    no
Requires:       testdisk
Requires:       java-$JAVA_VERSION
## needs openjfx but freezes with it
#Requires:      java-$JAVA_VERSION-openjdk-openjfx
Requires:       sleuthkit-java-bindings = $TSK_VERSION
#Requires:      opencv-java

%description

%prep
rm -rf             %{_builddir}/%{name}-%{version}/
mkdir -p           %{_builddir}/%{name}-%{version}
pushd        %{_builddir}/%{name}-%{version}
tar -xf            %{_sourcedir}/%{name}-%{version}.tar.xz
popd

%install
rm -rf             %{buildroot}
# copy files to target
pushd        %{_builddir}/%{name}-%{version}
mkdir -p           %{buildroot}%{_bindir}/
cp -n              bin/autopsy                             %{buildroot}%{_bindir}/
mkdir -p           %{buildroot}%{_sysconfdir}/
cp -nr             etc/*                                   %{buildroot}%{_sysconfdir}/
mkdir -p           %{buildroot}%{_libdir}/autopsy/
cp -n              README.txt                              %{buildroot}%{_libdir}/autopsy/
cp -n              CHANGELOG.txt                           %{buildroot}%{_libdir}/autopsy/
cp -n              LICENSE-2.0.txt                         %{buildroot}%{_libdir}/autopsy/
cp -nr             autopsy/                                %{buildroot}%{_libdir}/autopsy/
cp -nr             java/                                   %{buildroot}%{_libdir}/autopsy/
cp -nr             platform/                               %{buildroot}%{_libdir}/autopsy/
cp -nr             CoreTestLibs/                           %{buildroot}%{_libdir}/autopsy/
cp -nr             harness/                                %{buildroot}%{_libdir}/autopsy/
## for some reason autopsy already contains TSK -> which are missing their native files!!!
mkdir -p           %{buildroot}%{_libdir}/autopsy/autopsy/modules/ext/
## in the future we'll link the jars version independent
ln -sf             /usr/lib/java/sleuthkit-$TSK_VERSION.jar  %{buildroot}%{_libdir}/autopsy/autopsy/modules/ext/sleuthkit-$TSK_VERSION.jar
#ln -s              %{_javadir}/sleuthkit-caseuco.jar       %{buildroot}%{_libdir}/autopsy/autopsy/modules/ext/sleuthkit-caseuco-$TSK_VERSION.jar
mkdir -p           %{buildroot}%{_datadir}/applications/
cp -n              org.sleuthkit.autopsy.desktop           %{buildroot}%{_datadir}/applications/
mkdir -p           %{buildroot}%{_datadir}/icons/autopsy/
cp -n              autopsy.png                             %{buildroot}%{_datadir}/icons/autopsy/
mkdir -p           %{buildroot}%{_docdir}/autopsy/
cp -nr             docs/*                                  %{buildroot}%{_docdir}/autopsy/
popd

# update jdkhome
awk    '!/^\s*#?\s*jdkhome=.*$/' %{name}-%{version}/etc/autopsy.conf > %{buildroot}%{_sysconfdir}/autopsy.conf
printf "jdkhome=/usr/lib/jvm/jre-$JAVA_VERSION\n" >> %{buildroot}%{_sysconfdir}/autopsy.conf

# move license file
mkdir -p           %{buildroot}%{_datadir}/licenses/autopsy/
mv                 %{buildroot}%{_libdir}/autopsy/LICENSE-2.0.txt  %{buildroot}%{_datadir}/licenses/autopsy/

# make sure thirdparty files are executable
chmod +x           %{buildroot}%{_libdir}/autopsy/autopsy/markmckinnon/Export*
chmod +x           %{buildroot}%{_libdir}/autopsy/autopsy/markmckinnon/parse*
# allow solr dependencies to execute
chmod -R +x        %{buildroot}%{_libdir}/autopsy/autopsy/solr/bin
# make sure the start script is executable
chmod +x           %{buildroot}%{_bindir}/autopsy
# stop the toolkit from doing other stuff
exit 0

%clean
rm -rf             %{buildroot}

%files
%{_datadir}/applications/org.sleuthkit.autopsy.desktop
%{_bindir}/autopsy
%{_libdir}/autopsy/
%{_datadir}/icons/autopsy/
%{_docdir}/autopsy/
%config(noreplace) %{_sysconfdir}/autopsy.clusters
%config(noreplace) %{_sysconfdir}/autopsy.conf
%docdir            %{_docdir}/autopsy/
%license           %{_datadir}/licenses/autopsy/

# changelog redacted - file structure mismatch

%changelog
* Wed Nov 27 2024 VenaNocta <venanocta@gmail.com> - 4.21.0-1
- updated for Fedora deploy

EOF
}

gen_patch_files() {
mkdir -p $PATCH_PATH/
cat << EOF > $PATCH_PATH/bin_autopsy.patch
24,37c24,25
< PRG=\$0
< 
< while [ -h "\$PRG" ]; do
<     ls=\`ls -ld "\$PRG"\`
<     link=\`expr "\$ls" : '^.*-> \(.*\)$' 2>/dev/null\`
<     if expr "\$link" : '^/' 2> /dev/null >/dev/null; then
< 	PRG="\$link"
<     else
< 	PRG="\`dirname "\$PRG"\`/\$link"
<     fi
< done
< 
< progdir=\`dirname "\$PRG"\`
< APPNAME=\`basename "\$PRG"\`
---
> progdir=/
> APPNAME=autopsy
124c112
< nbexec=\`echo "\$progdir"/../platform*/lib/nbexec\`
---
> nbexec=/usr/lib64/autopsy/platform*/lib/nbexec
EOF
}

patch_autopsy() {
  printf ">>    (3.1)                    » patching bin/autopsy\n"
printf "!! patch  $WORKSPACE/REPACK/autopsy-$VERSION/bin/autopsy < $PATCH_PATH/bin_autopsy.patch\n" 
  patch  $WORKSPACE/REPACK/autopsy-$VERSION/bin/autopsy < $PATCH_PATH/bin_autopsy.patch

  printf ">>    (3.2)                    » patching CHANGELOG.txt\n"
  [ -f $WORKSPACE"/REPACK/autopsy-"$VERSION"/NEWS.txt" ] && mv $WORKSPACE"/REPACK/autopsy-"$VERSION"/NEWS.txt" $WORKSPACE"/REPACK/autopsy-"$VERSION"/CHANGELOG.txt"

  printf ">>    (3.3)                    » patching autopsy.png\n"
  curl -L -o $WORKSPACE"/REPACK/autopsy-"$VERSION"/autopsy.png" "https://raw.githubusercontent.com/sleuthkit/autopsy/develop/unix/autopsy.png"

  DESKTOP_FILE=$WORKSPACE"/REPACK/autopsy-"$VERSION"/org.sleuthkit.autopsy.desktop"
  printf ">>    (3.4)                    » patching org.sleuthkit.autopsy.desktop\n"
  cat << EOF > $DESKTOP_FILE
[Desktop Entry]
Version=$VERSION
Name=Autopsy
Comment=Complete Digital forensics analysis suite
Exec=/usr/bin/autopsy
Icon=/usr/share/icons/autopsy/autopsy.png
Terminal=false
Type=Application
Categories=Utility;System;Analysis;
EOF
}

pack_autopsy() {
  pushd $WORKSPACE"/REPACK/autopsy-"$VERSION
  tar -I "pxz -9" -cf $WORKSPACE"/SOURCES/autopsy-core-"$VERSION".tar.xz" \
      icon.ico LICENSE-2.0.txt README.txt CHANGELOG.txt \
      bin/autopsy autopsy.png org.sleuthkit.autopsy.desktop \
      etc autopsy platform java docs CoreTestLibs harness
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
PATCH_PATH=$WORKSPACE/REPACK/autopsy-$VERSION/patches
if [ -d $WORKSPACE"/REPACK/autopsy-"$VERSION ]; then
  printf ">>    (2) data located         » skipping decompression\n"
else
  printf ">>    (2) data missing         » unpacking archive\n"
  unzip -qod $WORKSPACE"/REPACK/" $WORKSPACE"/REPACK/"$ORIG_PACKAGE
  gen_patch_files
fi

# patch
printf ">>    (3)                      » patching data\n"
if [ -d $PATCH_PATH ]; then
  patch_autopsy
  printf ">>    (3.5)                    » patches applied > removing patches\n"
  rm -r $PATCH_PATH
else
  printf ">>    (3.1)                    » patches already applied > skipping!\n"
fi
printf ">>    (4)                      » parsing sleuthkit (TSK) version\n"
TSK_VERSION=$(cat $WORKSPACE"/REPACK/autopsy-"$VERSION"/unix_setup.sh" | grep TSK_VERSION= | cut --delimiter='=' --fields=2)
printf ">>                             » version: "$TSK_VERSION"\n"

# repackage with just the required files!!!
printf ">>    (5)                      » building compressed archives\n"
if [ -f $WORKSPACE"/SOURCES/autopsy-core-"$VERSION".tar.xz" ]; then
  printf ">>    (5.1)                    » found autopsy-core-"$VERSION".tar.xz\n"
else
  printf ">>    (5.1)                    » building autopsy-core-"$VERSION".tar.xz\n"
  pack_autopsy
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

