#!/usr/bin/bash

CLEAN=false
INFO=false
BUILD=false

# info from manual lookup
PROJECT_NAME="PhpStorm Professional"
ARTIFACT_NAME="phpstorm-pro"
GITHUB_REPO="<org>/<repo>"
# https://download-cdn.jetbrains.com/webide/PhpStorm-2024.3.5.tar.gz
LICENSE="«proprietary»"
VERSION="2024.3.5"
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
  printf ">>    SOURCE                   = https://download-cdn.jetbrains.com/webide/PhpStorm-*.tar.gz\n"
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
URL:            https://www.jetbrains.com/phpstorm/
Source0:        %{name}-%{version}.tar.xz
BuildRequires:  ( coreutils or coreutils-single )
Requires:       ( coreutils or coreutils-single )
Requires:       grep
AutoReqProv:    no

# disable rpmbuild features
%global debug_package %{nil}
%define __arch_install_post %{nil}
%define __os_install_post %{nil}
%define _build_id_links none

%description
Provides $ARTIFACT_NAME


## $ARTIFACT_NAME-jbr
%package        jbr
Summary:        $PROJECT_NAME - Java Runtime
Requires:       %{name} = %{version}-%{release}
AutoReqProv:    no

%description    jbr
Provides JetBrain's Java Runtime for $PROJECT_NAME


%define builddir_extract %{_builddir}/%{name}-%{version}/
%define libdir %{_libdir}/jetbrains/%{name}-%{version}


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
cp -n              Install-Linux-tar.txt                   %{buildroot}%{libdir}/
cp -n              product-info.json                       %{buildroot}%{libdir}/
cp -n              build.txt                               %{buildroot}%{libdir}/
mkdir -p           %{buildroot}%{_datadir}/applications/
cp -n              com.jetbrains.%{name}.desktop           %{buildroot}%{_datadir}/applications/
cp -nr             bin/                                    %{buildroot}%{libdir}/
cp -nr             help/                                   %{buildroot}%{libdir}/
cp -nr             jbr/                                    %{buildroot}%{libdir}/
cp -nr             lib/                                    %{buildroot}%{libdir}/
cp -nr             license/                                %{buildroot}%{libdir}/
cp -nr             modules/                                %{buildroot}%{libdir}/
cp -nr             plugins/                                %{buildroot}%{libdir}/
popd

# move files
mkdir -p           %{buildroot}%{_bindir}/
mv                 %{buildroot}%{libdir}/bin/%{name}       %{buildroot}%{_bindir}/
chmod +x           %{buildroot}%{_bindir}/%{name}
mkdir -p           %{buildroot}%{_sysconfdir}/jetbrains/
mv                 %{buildroot}%{libdir}/bin/phpstorm64.vmoptions  %{buildroot}%{_sysconfdir}/jetbrains/
mkdir -p           %{buildroot}%{_datadir}/icons/jetbrains/
mkdir -p           %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/
mv                 %{buildroot}%{libdir}/bin/phpstorm.png  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
mkdir -p           %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
mv                 %{buildroot}%{libdir}/bin/phpstorm.svg   %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg


%clean
rm -rf             %{buildroot}


%files
%{_bindir}/%{name}
%{_datadir}/applications/com.jetbrains.%{name}.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%config(noreplace) %{_sysconfdir}/jetbrains/phpstorm64.vmoptions
%{libdir}/Install-Linux-tar.txt
%{libdir}/product-info.json
%{libdir}/build.txt
%{libdir}/bin/
%{libdir}/help/
%{libdir}/lib/
%{libdir}/license/
%{libdir}/modules/
%{libdir}/plugins/


%files jbr
%{libdir}/jbr/


%changelog
* Sun Apr 13 2025 VenaNocta <venanocta@gmail.com> - 20250413
- patched for Fedora deploy

EOF
}

gen_patch_files() {
  mkdir -p $PATCH_PATH/
  pushd $PATCH_PATH/ > /dev/null
  # create .patch files
  cat << EOF > $PATCH_PATH/bin_phpstorm.sh.patch
42a43,44
> # patch | provide \$IDE_HOME as env override
> if [ -z "\$IDE_HOME" ]; then
43a46
> fi
102c105,106
< 
---
> # patch | provide \$VM_OPTIONS_FILE as env override
> if [ -z "\$VM_OPTIONS_FILE" ]; then
111a116
> fi
EOF
  popd > /dev/null
}

patch_unpacked() {
  printf ">>    (3.1)                    » patching bin/phpstorm.sh\n"
  patch  $REPACK_PATH/bin/phpstorm.sh < $PATCH_PATH/bin_phpstorm.sh.patch
  printf ">>    (3.2)                    » patching bin/"$ARTIFACT_NAME"\n"
  cat << EOF > $REPACK_PATH/bin/$ARTIFACT_NAME
#!/usr/bin/bash

#  set environment overrides
# export PHPSTORM_JDK=/usr/lib/jvm/java-21/
export IDE_HOME=/usr/lib64/jetbrains/$ARTIFACT_NAME-$VERSION
export VM_OPTIONS_FILE=/etc/jetbrains/phpstorm64.vmoptions

#  launch phpstorm
exec /usr/lib64/jetbrains/$ARTIFACT_NAME-$VERSION/bin/phpstorm.sh \$@
EOF
  printf ">>    (3.3)                    » patching com.jetbrains."$ARTIFACT_NAME".desktop\n"
  cat << EOF > $REPACK_PATH"/com.jetbrains."$ARTIFACT_NAME".desktop"
[Desktop Entry]
Name=PhpStorm Pro Edition
GenericName=The intelligent PHP IDE
Exec=$ARTIFACT_NAME %u
Terminal=false
Version=$VERSION
Icon=$ARTIFACT_NAME
Type=Application
Categories=Development;IDE;
StartupWMClass=jetbrains-phpstorm
StartupNotify=true
MimeType=application/x-php-code;text/x-php;
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
URL="https://download-cdn.jetbrains.com/webide/PhpStorm-"$VERSION".tar.gz"
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
    mv PhpStorm-*/* .
    rm -rf PhpStorm-*
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

