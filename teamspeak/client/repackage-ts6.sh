#!/usr/bin/bash

CLEAN=false
INFO=false
BUILD=false

# info from manual lookup
PROJECT_NAME="TeamSpeak 6 Client"
ARTIFACT_NAME="teamspeak-6-client-bundled"
GITHUB_REPO="<org>/<repo>"
# https://files.teamspeak-services.com/pre_releases/client/6.0.0-beta2/teamspeak-client.tar.gz
LICENSE="«proprietary»"
VERSION="6.0.0-beta2"
RELEASE="1"

# paths & files
set_paths(){
  WORKSPACE=~/rpmbuild
  SPEC_FILE_NAME=${ARTIFACT_NAME}-${VERSION//-/.}.spec
  SPEC_FILE=$WORKSPACE/SPECS/$SPEC_FILE_NAME
  REPACK_PATH=$WORKSPACE/REPACK/${ARTIFACT_NAME}-${VERSION}
  PATCH_PATH=$WORKSPACE/REPACK/${ARTIFACT_NAME}-${VERSION}/patches
}

print_help() {
  printf ">>> REPACKAGE "$PROJECT_NAME"\n\n";
  printf "  -c | --clean               ... clean build path\n"
  printf "  -i | --info                ... show info\n"
  printf "  -b | --build               ... build the package\n"
  printf "  ____________________________________________________________________________\n"
  printf "  -h | --help                ... show this help page\n\n";
}

print_info() {
  printf ">>>  [INFO]\n"
  printf "==  Environment\n"
  printf ">>    WORKSPACE                = "$WORKSPACE"\n"
  printf ">>    SOURCE                   = files.teamspeak-services.com/pre_releases/client/*/teamspeak-client.tar.gz\n"
  printf ">>    VERSION                  = "$VERSION"\n"
  printf ">>    LICENSE                  = "$LICENSE"\n"
  printf "  ____________________________________________________________________________\n"
  printf "==  Tools\n"
  printf "  ____________________________________________________________________________\n\n"
}

gen_spec() {
  cat << EOF > $SPEC_FILE
Name:           $ARTIFACT_NAME
Version:        ${VERSION//-/.}
Release:        $RELEASE
Summary:        $PROJECT_NAME repackaged for RPM based systems

License:        $LICENSE
URL:            https://www.teamspeak.com
Source0:        %{name}-%{version}.tar.xz
Obsoletes:      %{name} < %{version}
BuildRequires:  ( coreutils or coreutils-single )
AutoReqProv:    no

# disable rpmbuild features
%global debug_package %{nil}
%define __arch_install_post %{nil}
%define __os_install_post %{nil}
%define _build_id_links none

%description
Provides $PROJECT_NAME


%define builddir_extract %{_builddir}/%{name}-%{version}/
%define libdir %{_libdir}/teamspeak/client-v6


%prep
rm -rf             %{builddir_extract}/
mkdir -p           %{builddir_extract}
pushd        %{builddir_extract}
tar -xf            %{_sourcedir}/%{name}-%{version}.tar.xz
popd


%install
rm -rf             %{buildroot}
pushd %{builddir_extract}

# copy files to target
mkdir -p           %{buildroot}%{libdir}/
cp -nr             *                                       %{buildroot}%{libdir}/
popd

# move files
mkdir -p           %{buildroot}%{_bindir}/
mv                 %{buildroot}%{libdir}/ts6client         %{buildroot}%{_bindir}/
chmod +x           %{buildroot}%{_bindir}/ts6client
mkdir -p           %{buildroot}%{_datadir}/applications/
mv                 %{buildroot}%{libdir}/com.teamspeak.client-v6.desktop  %{buildroot}%{_datadir}/applications/
mkdir -p           %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/
mv                 %{buildroot}%{libdir}/logo-48.png       %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/ts6client.png
mkdir -p           %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/
mv                 %{buildroot}%{libdir}/logo-128.png      %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/ts6client.png
mkdir -p           %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/
mv                 %{buildroot}%{libdir}/logo-256.png      %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/ts6client.png


%clean
rm -rf             %{buildroot}


%files
%{_bindir}/ts6client
%{_datadir}/applications/com.teamspeak.client-v6.desktop
%{_datadir}/icons/hicolor/48x48/apps/ts6client.png
%{_datadir}/icons/hicolor/128x128/apps/ts6client.png
%{_datadir}/icons/hicolor/256x256/apps/ts6client.png
%{libdir}/


%changelog
* Mon Apr 14 2025 VenaNocta <venanocta@gmail.com> - 20250414
- patched for Fedora deploy

EOF
}

gen_patch_files() {
  mkdir -p $PATCH_PATH/
  pushd $PATCH_PATH/ > /dev/null
  # create .patch files
  popd > /dev/null
}

patch_unpacked() {
  printf ">>    (3.1)                    » patching bin/ts6client\n"
  cat << EOF > $REPACK_PATH/ts6client
#!/bin/bash

#  set environment overrides

#  launch teamspeak 6 client
exec /usr/lib64/teamspeak/client-v6/TeamSpeak \$@
EOF
  printf ">>    (3.2)                    » patching com.teamspeak.client-v6.desktop\n"
  cat << EOF > $REPACK_PATH"/com.teamspeak.client-v6.desktop"
[Desktop Entry]
Name=TeamSpeak 6
Comment=TeamSpeak Voice Communication Client
Exec=ts6client %u
Terminal=false
Version=$VERSION
Icon=ts6client
Type=Application
Categories=AudioVideo;Audio;Chat;Network
StartupWMClass=TeamSpeak
StartupNotify=false
MimeType=x-scheme-handler/ts6server
EOF
  printf ">>    (3.4)                    » patches applied > removing patches\n"
  rm -r $PATCH_PATH
#  printf ">>    (3.1)                    » no patches to be applied > skipped\n"
}

pack_xz() {
  pushd $REPACK_PATH > /dev/null
  tar -I "pxz -9" -cf $WORKSPACE"/SOURCES/"$ARTIFACT_NAME"-"${VERSION//-/.}".tar.xz" \
      *
  popd > /dev/null
}

#------------------------------------------------------------------------------
# START EXEC
#------------------------------------------------------------------------------

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
elif [ "$1" = "--build" -o "$1" = "-b" ]; then
  BUILD=true
  shift 1
else
  break
fi
done

# VERSION is not computed but predefined at file start!

set_paths

# clear
if $CLEAN; then
  printf "=== CLEAN $WORKSPACE/...\n\n"
  rm -rf $REPACK_PATH
  rm -rf $WORKSPACE/BUILD/${ARTIFACT_NAME}-${VERSION//-/.}*
  rm -rf $WORKSPACE/BUILDROOT/${ARTIFACT_NAME}-${VERSION//-/.}*
  rm -rf $WORKSPACE/SOURCES/${ARTIFACT_NAME}-${VERSION//-/.}*
  rm -f  $SPEC_FILE
fi

# build
if $BUILD; then
  rpmdev-setuptree
  mkdir -p $WORKSPACE/BUILD
fi

# info
if $INFO; then
  print_info
fi

# stop exec
if ! $BUILD; then
  exit 0
fi

#URL="https://github.com/"$GITHUB_REPO"/releases/download/"$GIT_TAG"/<package-name>-"$VERSION".zip"
URL="https://files.teamspeak-services.com/pre_releases/client/"$VERSION"/teamspeak-client.tar.gz"
ORIG_PACKAGE=$ARTIFACT_NAME"-"$VERSION".tar.gz"

printf ">>>  [Repackage "${PROJECT_NAME}" as RPMs]\n"
printf ">>    URL                      = "$URL"\n"
printf ">>    FILE                     = "$WORKSPACE"/BUILD/"$ORIG_PACKAGE"\n"
printf "  ____________________________________________________________________________\n"
mkdir -p $WORKSPACE"/REPACK/"
if [ -f $WORKSPACE"/REPACK/"$ORIG_PACKAGE ]; then
  printf ">>    (1) tar.gz archive located  » skipping download\n"
else
  printf ">>    (1) tar.gz archive missing  » download from JetBrains CDN\n\n"
  curl -L -o $WORKSPACE"/REPACK/"$ORIG_PACKAGE $URL
fi

# unpack
if [ -d $REPACK_PATH ]; then
  printf ">>    (2) data located         » skipping decompression\n"
else
  printf ">>    (2) data missing         » unpacking archive\n"
  mkdir -p $REPACK_PATH
  pushd $REPACK_PATH > /dev/null
    tar -xf $WORKSPACE"/REPACK/"$ORIG_PACKAGE
  popd > /dev/null
  gen_patch_files
fi

# patch
printf ">>    (3)                      » patching data\n"
if [ -d $PATCH_PATH ]; then
  patch_unpacked
else
  printf ">>    (3.1)                    » patches already applied > skipping!\n"
fi

# repackage with just the required files!!!
printf ">>    (4)                      » building compressed archives\n"
if [ -f $WORKSPACE"/SOURCES/"$ARTIFACT_NAME"-"${VERSION//-/.}".tar.xz" ]; then
  printf ">>    (4.1)                    » found "$ARTIFACT_NAME"-"${VERSION//-/.}".tar.xz\n"
else
  printf ">>    (4.1)                    » building "$ARTIFACT_NAME"-"${VERSION//-/.}".tar.xz\n"
  pack_xz
fi


printf "=== BUILDING RPM \n"
printf ">>    SPEC FILE                = "$SPEC_FILE"\n"
printf ">>    SRPM                     = "$ARTIFACT_NAME"-"${VERSION//-/.}"-"$RELEASE".src.rpm\n"
printf ">>    RPM FILES                = "$ARTIFACT_NAME"-*-"${VERSION//-/.}"-"$RELEASE".x86_64.rpm\n"
printf "  ____________________________________________________________________________\n"
printf ">>    (1)                      » compiling "$SPEC_FILE_NAME" file\n"
gen_spec
printf ">>    (2)                      » building "$ARTIFACT_NAME"-"${VERSION//-/.}"-"$RELEASE".src.rpm\n"
rpmbuild -bs $SPEC_FILE
printf ">>    (3)                      » building packages "$ARTIFACT_NAME"-*-"${VERSION//-/.}"-"$RELEASE".rpm\n"
rpmbuild -bb $SPEC_FILE

