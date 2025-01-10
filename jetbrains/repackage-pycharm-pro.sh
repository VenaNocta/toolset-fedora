#!/usr/bin/bash

CLEAN=false
INFO=false
BUILD=false

# info from manual lookup
PROJECT_NAME="PyCharm Professional"
ARTIFACT_NAME="pycharm-pro"
GITHUB_REPO="Winetricks/winetricks"
# https://download-cdn.jetbrains.com/python/pycharm-professional-2024.3.1.1.tar.gz
LICENSE="«proprietary»"
VERSION="2024.3.1.1"
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
  printf ">>    SOURCE                   = https://download-cdn.jetbrains.com/python/\n"
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
URL:            https://www.jetbrains.com/pycharm/
Source0:        %{name}-%{version}.tar.xz

AutoReqProv:    no

# disable rpmbuild features
%define __arch_install_post %{nil}
%define __os_install_post %{nil}
%define __find_provides %{nil}
%define __find_requires %{nil}
%define _use_internal_dependency_generator 0

%description
Provides $ARTIFACT_NAME


## $ARTIFACT_NAME-jbr
%package        jbr
Summary:        $PROJECT_NAME - Java Runtime
Requires:       %{name} = %{version}-%{release}

%description    jbr
Provides JetBrain's Java Runtime for $PROJECT_NAME


%define builddir_extract %{_builddir}/%{name}-%{version}/

%prep
rm -rf             %{_builddir}/%{name}-%{version}/
mkdir -p           %{_builddir}/%{name}-%{version}
pushd        %{_builddir}/%{name}-%{version}
tar -xf            %{_sourcedir}/%{name}-%{version}.tar.xz
popd


%define libdir %{_libdir}/jetbrains/%{name}-%{version}
%install
rm -rf             %{buildroot}
pushd %{builddir_extract}

# copy files to target
mkdir -p           %{buildroot}%{libdir}/
cp -n              Install-Linux-tar.txt                   %{buildroot}%{libdir}/
mkdir -p           %{buildroot}%{_datadir}/applications/
cp -n              com.jetbrains.pycharm-pro.desktop       %{buildroot}%{_datadir}/applications/
cp -nr             bin/                                    %{buildroot}%{libdir}/
cp -nr             debug-eggs/                             %{buildroot}%{libdir}/
cp -nr             help/                                   %{buildroot}%{libdir}/
cp -nr             jbr/                                    %{buildroot}%{libdir}/
cp -nr             lib/                                    %{buildroot}%{libdir}/
cp -nr             license/                                %{buildroot}%{libdir}/
cp -nr             modules/                                %{buildroot}%{libdir}/
cp -nr             plugins/                                %{buildroot}%{libdir}/
popd

# move files
mkdir -p           %{buildroot}%{_bindir}/
mv                 %{buildroot}%{libdir}/bin/pycharm-pro   %{buildroot}%{_bindir}/
mkdir -p           %{buildroot}%{_sysconfdir}/jetbrains/
mv                 %{buildroot}%{libdir}/bin/pycharm64.vmoptions  %{buildroot}%{_sysconfdir}/jetbrains/
mkdir -p           %{buildroot}%{_datadir}/icons/jetbrains/
mv                 %{buildroot}%{libdir}/bin/pycharm.png   %{buildroot}%{_datadir}/icons/jetbrains/pycharm-pro.png
mkdir -p           %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
mv                 %{buildroot}%{libdir}/bin/pycharm.svg   %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/pycharm-pro.svg


%clean
rm -rf             %{buildroot}


%files
%{_bindir}/pycharm-pro
%{_datadir}/applications/com.jetbrains.pycharm-pro.desktop
%{_datadir}/icons/jetbrains/pycharm-pro.png
%{_datadir}/icons/hicolor/scalable/apps/pycharm-pro.svg
%config(noreplace) %{_sysconfdir}/jetbrains/pycharm64.vmoptions
%{libdir}/Install-Linux-tar.txt
%{libdir}/bin/
%{libdir}/debug-eggs/
%{libdir}/help/
%{libdir}/lib/
%{libdir}/license/
%{libdir}/modules/
%{libdir}/plugins/


%files jbr
%{libdir}/jbr/


%changelog
* Thu Jan 09 2025 VenaNocta <venanocta@gmail.com> - 20250109
- patched for Fedora deploy

EOF
}

gen_patch_files() {
  mkdir -p $PATCH_PATH/
  pushd $PATCH_PATH/ > /dev/null
  # create .patch files
  cat << EOF > $PATCH_PATH/bin_pycharm.sh.patch
42a43,44
> # patch | provide $IDE_HOME as env override
> if [ -z "$IDE_HOME" ]
43a46
> fi
54a58
> fi
101a106,107
> # patch | provide $VM_OPTIONS_FILE as env override
> if [ -z "$VM_OPTIONS_FILE" ]
111a118
> fi
120a128
> fi
EOF
  popd > /dev/null
}

patch_unpacked() {
  printf ">>    (3.1)                    » patching bin/pycharm.sh\n"
  patch  $REPACK_PATH/bin/pycharm.sh < $PATCH_PATH/bin_pycharm.sh.patch
  printf ">>    (3.2)                    » patching bin/pycharm-pro\n"
  cat << EOF > $REPACK_PATH/bin/pycharm-pro
#!/usr/bin/bash

#  set environment overrides
# export PYCHARM_JDK=/usr/lib/jvm/java-21/
export IDE_HOME=/usr/lib64/jetbrains/pycharm-pro-$VERSION
export VM_OPTIONS_FILE=/etc/jetbrains/pycharm64.vmoptions

#  launch pycharm
exec /usr/lib64/jetbrains/pycharm-pro-$VERSION/bin/pycharm.sh \$@
EOF
  printf ">>    (3.3)                    » patching com.jetbrains.pycharm-pro.desktop\n"
  cat << EOF > $REPACK_PATH"/com.jetbrains.pycharm-pro.desktop"
[Desktop Entry]
Name=PyCharm Pro Edition
GenericName=The intelligent Python IDE
Exec=pycharm-pro
Terminal=false
Icon=pycharm-pro
Type=Application
Categories=Development;IDE;
StartupWMClass=jetbrains-pycharm
MimeType=text/plain;application/x-python-code;text/x-python;application/xml;text/markdown;
EOF
  printf ">>    (3.4)                    » patches applied > removing patches\n"
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
URL="https://download-cdn.jetbrains.com/python/pycharm-professional-"$VERSION".tar.gz"
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
    mv "pycharm-"$VERSION/* .
    rm -rf "pycharm-"$VERSION
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

