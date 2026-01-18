#!/usr/bin/bash

CLEAN=false
INFO=false
BUILD=false

# info from manual lookup
PROJECT_NAME="BinaryNinja"
ARTIFACT_NAME="binaryninja"
GITHUB_REPO="<org>/<repo>"
# https://cdn.binary.ninja/installers/binaryninja_free_linux.zip
LICENSE="«proprietary»"
VERSION="5.2"
RELEASE="1"

# paths & files
set_paths(){
  WORKSPACE=~/rpmbuild
  SPEC_FILE_NAME=${ARTIFACT_NAME}-${VERSION}.spec
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
  printf ">>    SOURCE                   = https://cdn.binary.ninja/installers/binaryninja_free_linux.zip\n"
  printf ">>    VERSION                  = "$VERSION"\n"
  printf ">>    LICENSE                  = "$LICENSE"\n"
  printf "  ____________________________________________________________________________\n"
  printf "==  Tools\n"
  printf "  ____________________________________________________________________________\n\n"
}

gen_spec() {
  cat << EOF > $SPEC_FILE
Name:           $ARTIFACT_NAME
Version:        $VERSION
Release:        $RELEASE
Summary:        $PROJECT_NAME repackaged for RPM based systems

License:        $LICENSE
URL:            https://binary.ninja/
Source0:        %{name}-%{version}.tar.xz
BuildRequires:  ( coreutils or coreutils-single )
AutoReqProv:    no

# disable rpmbuild features
%global debug_package %{nil}
%define __arch_install_post %{nil}
%define __os_install_post %{nil}
%define _build_id_links none

%description
Provides $ARTIFACT_NAME


%define builddir_extract %{_builddir}/%{name}-%{version}/
%define libdir %{_libdir}/binaryninja


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
mkdir -p           %{buildroot}%{_bindir}/
cp -r              bin/*                                   %{buildroot}%{_bindir}/
mkdir -p           %{buildroot}%{libdir}
cp -r              binaryninja                          -T %{buildroot}%{libdir}
mkdir -p           %{buildroot}%{_datadir}/applications/
cp -u              com.vector35.%{name}.desktop            %{buildroot}%{_datadir}/applications/
popd

# modify files
chmod +x           %{buildroot}%{_bindir}/*

%clean
rm -rf             %{buildroot}


%files
%{_bindir}/%{name}
%{_datadir}/applications/com.vector35.%{name}.desktop
%{libdir}/


%changelog
* Sun Jan 18 2026 VenaNocta <venanocta@gmail.com> - 20260118
- patched for Fedora deploy

EOF
}

gen_patch_files() {
  mkdir -p $PATCH_PATH/
  pushd $PATCH_PATH/ > /dev/null
  # create .patch files
  ## currently no patchfiles required...
  popd > /dev/null
}

patch_unpacked() {
  printf ">>    (3.1)                    » patching bin/"$ARTIFACT_NAME"\n"
  mkdir -p $REPACK_PATH/bin/
  cat << EOF > $REPACK_PATH/bin/$ARTIFACT_NAME
#!/usr/bin/sh

#  set environment overrides

#  launch binaryninja
exec /usr/lib64/binaryninja/binaryninja \$@
EOF
  printf ">>    (3.2)                    » patching com.vector35."$ARTIFACT_NAME".desktop\n"
  cat << EOF > $REPACK_PATH"/com.vector35."$ARTIFACT_NAME".desktop"
[Desktop Entry]
Name=BinaryNinja Free
GenericName=BinaryNinja IDE
Exec=$ARTIFACT_NAME %u
Terminal=false
Version=$VERSION
Icon=$ARTIFACT_NAME
Type=Application
Categories=Development;IDE;
StartupWMClass=binaryninja
StartupNotify=true
MimeType=;
EOF
  printf ">>    (3.3)                    » patches applied > removing patches\n"
  rm -r $PATCH_PATH
#  printf ">>    (3.1)                    » no patches to be applied > skipped\n"
}

pack_xz() {
  pushd $REPACK_PATH > /dev/null
  tar -I "pxz -9" -cf $WORKSPACE"/SOURCES/"$ARTIFACT_NAME"-"$VERSION".tar.xz" \
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
  rm -rf $WORKSPACE/BUILD/${ARTIFACT_NAME}-${VERSION}*
  rm -rf $WORKSPACE/BUILDROOT/${ARTIFACT_NAME}-${VERSION}*
  rm -rf $WORKSPACE/SOURCES/${ARTIFACT_NAME}-${VERSION}*
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
URL="https://cdn.binary.ninja/installers/binaryninja_free_linux.zip"
ORIG_PACKAGE=$ARTIFACT_NAME"-"$VERSION".zip"

printf ">>>  [Repackage "${PROJECT_NAME}" as RPMs]\n"
printf ">>    URL                      = "$URL"\n"
printf ">>    FILE                     = "$WORKSPACE"/BUILD/"$ORIG_PACKAGE"\n"
printf "  ____________________________________________________________________________\n"
mkdir -p $WORKSPACE"/REPACK/"
if [ -f $WORKSPACE"/REPACK/"$ORIG_PACKAGE ]; then
  printf ">>    (1) zip archive located  » skipping download\n"
else
  printf ">>    (1) zip archive missing  » download from BinaryNinja CDN\n\n"
  curl -L -o $WORKSPACE"/REPACK/"$ORIG_PACKAGE $URL
fi

# unpack
if [ -d $REPACK_PATH ]; then
  printf ">>    (2) data located         » skipping decompression\n"
else
  printf ">>    (2) data missing         » unpacking archive\n"
  mkdir -p $REPACK_PATH
  pushd $REPACK_PATH > /dev/null
    unzip $WORKSPACE"/REPACK/"$ORIG_PACKAGE
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
if [ -f $WORKSPACE"/SOURCES/"$ARTIFACT_NAME"-"$VERSION".tar.xz" ]; then
  printf ">>    (4.1)                    » found "$ARTIFACT_NAME"-"$VERSION".tar.xz\n"
else
  printf ">>    (4.1)                    » building "$ARTIFACT_NAME"-"$VERSION".tar.xz\n"
  pack_xz
fi


printf "=== BUILDING RPM \n"
printf ">>    SPEC FILE                = "$SPEC_FILE"\n"
printf ">>    SRPM                     = "$ARTIFACT_NAME"-"$VERSION"-"$RELEASE".src.rpm\n"
printf ">>    RPM FILES                = "$ARTIFACT_NAME"-*-"$VERSION"-"$RELEASE".x86_64.rpm\n"
printf "  ____________________________________________________________________________\n"
printf ">>    (1)                      » compiling "$SPEC_FILE_NAME" file\n"
gen_spec
printf ">>    (2)                      » building "$ARTIFACT_NAME"-"$VERSION"-"$RELEASE".src.rpm\n"
rpmbuild -bs $SPEC_FILE
printf ">>    (3)                      » building packages "$ARTIFACT_NAME"-*-"$VERSION"-"$RELEASE".rpm\n"
rpmbuild -bb $SPEC_FILE

