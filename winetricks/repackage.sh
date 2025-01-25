#!/usr/bin/bash

CLEAN=false
INFO=false
BUILD=false

# info from manual lookup
PROJECT_NAME="Winetricks"
ARTIFACT_NAME="winetricks"
GITHUB_REPO="Winetricks/winetricks"
LICENSE="LGPL-2.1" 
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
  printf ">>    SOURCE                   = https://github.com/"$GITHUB_REPO"/releases/\n"
  printf ">>    LATEST GIT RELEASE       = "$GIT_TAG"\n"
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
URL:            https://github.com/Winetricks/winetricks
Source0:        %{name}-%{version}.tar.xz
BuildArch:      noarch

AutoReqProv:    no

%description
Provides $ARTIFACT_NAME


## $ARTIFACT_NAME-bash-completion
%package        bash-completion
Summary:        $PROJECT_NAME - bash-completion
Requires:       %{name} = %{version}-%{release}
Requires:       bash-completion

%description    bash-completion
Provides bash-completion for $PROJECT_NAME


## $ARTIFACT_NAME-gui
%package        gui
Summary:        $PROJECT_NAME - gui
Requires:       %{name} = %{version}-%{release}

%description    gui
Provides gui & .desktop file for $PROJECT_NAME


%prep
%define builddir_extract %{_builddir}/%{name}-%{version}/
rm -rf             %{_builddir}/%{name}-%{version}/
mkdir -p           %{_builddir}/%{name}-%{version}
pushd        %{_builddir}/%{name}-%{version}
tar -xf            %{_sourcedir}/%{name}-%{version}.tar.xz
popd


%install
rm -rf             %{buildroot}
pushd %{builddir_extract}
%make_install
popd


%clean
rm -rf             %{buildroot}


%files
%{_bindir}/winetricks
%{_mandir}/man1/winetricks.1.gz

%files bash-completion
%{_datadir}/bash-completion/completions/winetricks

%files gui
%{_datadir}/applications/winetricks.desktop
%{_datadir}/icons/hicolor/scalable/apps/winetricks.svg
%{_datadir}/metainfo/io.github.winetricks.Winetricks.metainfo.xml


%changelog
* Fri Nov 29 2024 VenaNocta <venanocta@gmail.com> - 20240105
- updated for Fedora deploy

EOF
}

gen_patch_files() {
mkdir -p $PATCH_PATH/
pushd $PATCH_PATH/ > /dev/null
  # create .patch files
popd > /dev/null
}

patch_unpacked() {
#  printf ">>    (3.1)                    » patching bin/<file>\n"
#  printf ">>    (3.1)                    » patches applied > removing patches\n"
  printf ">>    (3.1)                    » no patches to be applied > skipped\n"
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

GIT_TAG=$(git ls-remote --refs --sort='version:refname' --tags https://github.com/${GITHUB_REPO}.git | tail --lines=1 | cut --delimiter='/' --fields=3)
#VERSION=$(printf $GIT_TAG | cut --delimiter='-' --fields=2)
VERSION=$(printf $GIT_TAG)

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
URL="https://codeload.github.com/$GITHUB_REPO/tar.gz/refs/tags/"$GIT_TAG
ORIG_PACKAGE=$ARTIFACT_NAME"-"$VERSION".tar.gz"

printf ">>>  [Repackage "$PROJECT_NAME" as RPMs]\n"
printf ">>    URL                      = "$URL"\n"
printf ">>    FILE                     = "$WORKSPACE"/BUILD/"$ORIG_PACKAGE"\n"
printf "  ____________________________________________________________________________\n"
mkdir -p $WORKSPACE"/REPACK/"
if [ -f $WORKSPACE"/REPACK/"$ORIG_PACKAGE ]; then
  printf ">>    (1) tar.gz archive located  » skipping download\n"
else
  printf ">>    (1) tar.gz archive missing  » download from GitHub Releases\n\n"
  curl -L -o $WORKSPACE"/REPACK/"$ORIG_PACKAGE $URL
fi

# unpack
if [ -d $REPACK_PATH ]; then
  printf ">>    (2) data located         » skipping decompression\n"
else
  printf ">>    (2) data missing         » unpacking archive\n"
#  unzip -qod $WORKSPACE"/REPACK/" $WORKSPACE"/REPACK/"$ORIG_PACKAGE
  pushd $WORKSPACE"/REPACK/" > /dev/null
    tar -xf $WORKSPACE"/REPACK/"$ORIG_PACKAGE
  popd > /dev/null
  gen_patch_files
fi

# patch
printf ">>    (3)                      » patching data\n"
if [ -d $PATCH_PATH ]; then
  patch_unpacked
  rm -r $PATCH_PATH
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

