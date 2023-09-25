#!/usr/bin/bash

WORKSPACE=~/rpmbuild
CLEAN=false
INFO=false
# info from manual lookup
LICENSE="TeamSpeak License"
VERSION="3.6.2"
RELEASE="1"
# paths
REPACK_PATH=$WORKSPACE/REPACK/teamspeak-${VERSION%%.*}-client-bundled-${VERSION}
BUILD_PATH=$WORKSPACE/BUILD/teamspeak-${VERSION%%.*}-client-bundled-${VERSION}
BUILDROOT_PATH=$WORKSPACE/BUILDROOT/teamspeak-${VERSION%%.*}-client-bundled-${VERSION}
SOURCES_PATH=$WORKSPACE/SOURCES/teamspeak-${VERSION%%.*}-client-bundled-${VERSION}

print_help() {
  printf ">>> REPACKAGE TEAMSPEAK\n\n";
  printf "  -c | --clean               ... clean build path\n"
  printf "  -i | --info                ... show info\n"teamspeak
  printf "  ____________________________________________________________________________\n"
  printf "  -h | --help                ... show this help page\n\n";
}

print_info() {
  printf ">>>  [INFO]\n"
  printf "==  Environment\n"
  printf ">>    WORKSPACE                = "$WORKSPACE"\n"
  printf ">>    SOURCE                   = https://files.teamspeak-services.com/releases/client/\n"
  printf ">>    VERSION                  = "$VERSION"\n"
  printf "  ____________________________________________________________________________\n"
  printf "==  Tools\n"
  printf "  ____________________________________________________________________________\n\n"
}

gen_spec() {
  printf "Name:           teamspeak-"${VERSION%%.*}"-client-bundled\n"         >  $SPEC_FILE
  printf "Version:        $VERSION\n"                                          >> $SPEC_FILE
  printf "Release:        $RELEASE\n"                                          >> $SPEC_FILE
  printf "ExclusiveArch:  x86_64\n"                                            >> $SPEC_FILE
  printf "Obsoletes:      %%{name} <= %%{version}\n"                           >> $SPEC_FILE
  printf "Summary:        TeamSpeak repackaged for RPM based systems\n\n"      >> $SPEC_FILE
  printf "License:        $LICENSE\n"                                          >> $SPEC_FILE
  printf "URL:            https://teamspeak.com/en/downloads/#client\n"        >> $SPEC_FILE
  printf "Source0:        %%{name}-%%{version}.tar.xz\n\n"                     >> $SPEC_FILE
  printf "AutoReqProv:    no\n"                                                >> $SPEC_FILE
  printf "BuildRequires:  pxz\n"                                               >> $SPEC_FILE
  printf "BuildRequires:  sed\n"                                               >> $SPEC_FILE
#  printf "#Requires:       <requirement>\n"                                    >> $SPEC_FILE
  printf "\n"                                                                  >> $SPEC_FILE
  printf "%%description\n"                                                     >> $SPEC_FILE
  printf "\n"                                                                  >> $SPEC_FILE
  printf "%%prep\n"                                                            >> $SPEC_FILE
  printf "rm -rf %%{_builddir}/%%{name}-%%{version}/\n"                        >> $SPEC_FILE
  printf "mkdir -p %%{_builddir}/%%{name}-%%{version}\n"                       >> $SPEC_FILE
  printf "pushd %%{_builddir}/%%{name}-%%{version}\n"                          >> $SPEC_FILE
  printf "tar -xf %%{_sourcedir}/%%{name}-%%{version}.tar.xz\n"                >> $SPEC_FILE
  printf "popd\n"                                                              >> $SPEC_FILE
  printf "\n"                                                                  >> $SPEC_FILE
  printf "%%define _ts_path /teamspeak/client-v"${VERSION%%.*}"\n"             >> $SPEC_FILE
  printf "%%install\n"                                                         >> $SPEC_FILE
  printf "rm -rf %%{buildroot}\n"                                              >> $SPEC_FILE
  printf "# copy files to target\n"                                            >> $SPEC_FILE
  printf "pushd  %%{_builddir}/%%{name}-%%{version}\n"                         >> $SPEC_FILE
  printf "mkdir -p %%{buildroot}%%{_bindir}/\n"                                >> $SPEC_FILE
  printf "# update install location\n"                                         >> $SPEC_FILE
# sed -i -r 'h;s/[^#]*//1;x;s/#.*//;s/"\$\(dirname "\$\(readlink -f "\$\{BASH_SOURCE\[0\]\}"\)"\)"/\/usr\/lib64\/teamspeak\/client-v3\//g;G;s/(.*)\n/\1/' ts3client
  printf "sed -i -r 'h;s/[^#]*//1;x;s/#.*//;s/\"\\$\(dirname \"\\$\\(readlink -f \"\\$\\{BASH_SOURCE\\[0\\]\\}\"\\)\"\\)\"/\\/usr\\/lib64\\/teamspeak\\/client-v"${VERSION%%.*}"\\//g;G;s/(.*)\\\\n/\\\\1/' ts3client\n" >> $SPEC_FILE
  printf "cp -n  ts3client                         %%{buildroot}%%{_bindir}/\n"   >> $SPEC_FILE
  printf "mkdir -p %%{buildroot}%%{_libdir}%%{_ts_path}/\n"                       >> $SPEC_FILE
  printf "cp -n  LICENSE.txt                       %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -n  CHANGELOG                         %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -n  error_report                      %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -n  *.so*                             %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -n  openglblacklist.json              %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -n  package_inst                      %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -n  qt.conf                           %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -n  QtWebEngineProcess                %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -n  ts3client_linux_amd64             %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -n  update                            %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -nr gfx/                              %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -nr html/                             %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -nr iconengines/                      %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -nr imageformats/                     %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -nr platforms/                        %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -nr qtwebengine_locales/              %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -nr resources/                        %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -nr sound/                            %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -nr soundbackends/                    %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -nr sqldrivers/                       %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -nr styles/                           %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -nr translations/                     %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "cp -nr xcbglintegrations/                %%{buildroot}%%{_libdir}%%{_ts_path}/\n" >> $SPEC_FILE
  printf "mkdir -p %%{buildroot}%%{_datadir}/applications/\n"                  >> $SPEC_FILE
  printf "cp -n  com.teamspeak.client-v"${VERSION%%.*}".desktop %%{buildroot}%%{_datadir}/applications/\n" >> $SPEC_FILE
  printf "popd\n"                                                              >> $SPEC_FILE
  printf "# stop the toolkit from doing other stuff\n"                         >> $SPEC_FILE
  printf "exit 0\n"                                                            >> $SPEC_FILE
  printf "\n"                                                                  >> $SPEC_FILE
  printf "%%clean\n"                                                           >> $SPEC_FILE
  printf "rm -rf %%{buildroot}\n"                                              >> $SPEC_FILE
  printf "\n"                                                                  >> $SPEC_FILE
  printf "%%files\n"                                                           >> $SPEC_FILE
  printf "%%{_datadir}/applications/com.teamspeak.client-v"${VERSION%%.*}".desktop\n" >> $SPEC_FILE
  printf "%%{_bindir}/ts3client\n"                                             >> $SPEC_FILE
  printf "%%{_libdir}/%%{_ts_path}/\n"                                         >> $SPEC_FILE
#  printf "%%license           %%{_libdir}/%%{_ts_path}/LICENSE.txt\n"          >> $SPEC_FILE
  printf "\n"                                                                  >> $SPEC_FILE
  printf "%%changelog\n" >> $SPEC_FILE
  cat    $REPACK_PATH"/CHANGELOG" >> $SPEC_FILE
  printf "\n" >> $SPEC_FILE
}

patch_files() {
  printf ">>    (3.1)                    » patching LICENSE.txt\n"
  printf "  PLEASE UNDERSTAND WE FAILED TO EXTRACT THE LICENSE FILE\n"         >  $REPACK_PATH"/LICENSE.txt"
  printf "FROM THE OFFICIAL INSTALLER WHICH YOU CAN FIND HERE:\n"              >> $REPACK_PATH"/LICENSE.txt"
  printf "https://files.teamspeak-services.com/releases/client/"$VERSION"/TeamSpeak"${VERSION%%.*}"-Client-linux_amd64-"$VERSION".run\n" >> $REPACK_PATH"/LICENSE.txt"
  printf " --- TeamSpeak License ---\n"                                        >> $REPACK_PATH"/LICENSE.txt"
  printf "\n"                                                                  >> $REPACK_PATH"/LICENSE.txt"

  DESKTOP_FILE=$REPACK_PATH"/com.teamspeak.client-v"${VERSION%%.*}".desktop"
  printf ">>    (3.2)                    » patching com.teamspeak.client-v"${VERSION%%.*}".desktop\n"
  printf "[Desktop Entry]\n"                                                   >  $DESKTOP_FILE
  printf "Version="$VERSION"\n"                                                >> $DESKTOP_FILE
  printf "Type=Application\n"                                                  >> $DESKTOP_FILE
  printf "Name=TeamSpeak "${VERSION%%.*}"\n"                                   >> $DESKTOP_FILE
  printf "Comment=TeamSpeak Voice Communication Client\n"                      >> $DESKTOP_FILE
  printf "Exec=/usr/bin/ts3client\n"                                           >> $DESKTOP_FILE
  printf "Icon=teamspeak-client\n"                                             >> $DESKTOP_FILE
  printf "StartupNotify=false\n"                                               >> $DESKTOP_FILE
  printf "StartupWMClass=TeamSpeak\n"                                          >> $DESKTOP_FILE
  printf "Terminal=false\n"                                                    >> $DESKTOP_FILE
  printf "MimeType=x-scheme-handler/ts3server;x-scheme-handler/teamspeak\n"    >> $DESKTOP_FILE
  printf "Categories=AudioVideo;Audio;Chat;Network;\n"                         >> $DESKTOP_FILE
}

package() {
  pushd $REPACK_PATH
  tar -I "pxz -9" -cf $WORKSPACE"/SOURCES/teamspeak-"${VERSION%%.*}"-client-bundled-"$VERSION".tar.xz" *
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

# clear
if $CLEAN; then
  printf "=== CLEAN $WORKSPACE/...\n\n"
  rm -rf $REPACK_PATH*
  rm -rf $BUILD_PATH*
  rm -rf $BUILDROOT_PATH*
  rm -rf $SOURCES_PATH*
  rm -f  $WORKSPACE/SPECS/teamspeak-${VERSION%%.*}-client-bundled-${VERSION}.spec
fi

rpmdev-setuptree
mkdir -p $WORKSPACE/BUILD

# info
if $INFO; then
  print_info
fi

URL="https://files.teamspeak-services.com/releases/client/"$VERSION"/TeamSpeak"${VERSION%%.*}"-Client-linux_amd64-"$VERSION".run"
ORIG_PACKAGE="teamspeak"${VERSION%%.*}"-client-linux_amd64-"$VERSION".run"

printf ">>>  [Repackage TeamSpeak as RPMs]\n"
printf ">>    URL                      = "$URL"\n"
printf ">>    FILE                     = "$WORKSPACE"/BUILD/"$ORIG_PACKAGE"\n"
printf "  ____________________________________________________________________________\n"
mkdir -p $WORKSPACE"/REPACK/"
if [ -f $WORKSPACE"/REPACK/"$ORIG_PACKAGE ]; then
  printf ">>    (1) archive located  » skipping download\n"
else
  printf ">>    (1) archive missing  » download from TeamSpeak Releases\n\n"
  curl -L -o $WORKSPACE"/REPACK/"$ORIG_PACKAGE $URL
fi

# unpack
if [ -d $REPACK_PATH ]; then
  printf ">>    (2) data located         » skipping decompression\n"
else
  printf ">>    (2) data missing         » unpacking archive\n"
  mkdir -p $REPACK_PATH
  chmod +x $WORKSPACE"/REPACK/"$ORIG_PACKAGE
  $($WORKSPACE"/REPACK/"$ORIG_PACKAGE --tar x -C $REPACK_PATH .)
  find $REPACK_PATH -type d -exec chmod 755 {} \;
  find $REPACK_PATH -type f -exec chmod 644 {} \;
  pushd $REPACK_PATH
  mv ts3client_runscript.sh ts3client
  chmod +x error_report package_inst QtWebEngineProcess ts3client_linux_amd64 ts3client update
  popd
fi

# patch
printf ">>    (3)                      » patching data\n"
patch_files

# repackage with just the required files!!!
printf ">>    (4)                      » building compressed archives\n"
if [ -f $WORKSPACE"/SOURCES/teamspeak-"${VERSION%%.*}"-client-bundled-"$VERSION".tar.xz" ]; then
  printf ">>    (4.1)                    » found teamspeak-"${VERSION%%.*}"-client-bundled-"$VERSION".tar.xz\n"
else
  printf ">>    (4.1)                    » building teamspeak-"${VERSION%%.*}"-client-bundled-"$VERSION".tar.xz\n"
  package
fi

SPEC_FILE=$WORKSPACE/SPECS/teamspeak-${VERSION%%.*}-client-bundled-${VERSION}.spec
printf "=== BUILDING RPM \n"
printf ">>    SPEC FILE                  = "$SPEC_FILE"\n"
printf ">>    SRPM                       = teamspeak-"${VERSION%%.*}"-client-bundled-"$VERSION"-"$RELEASE".src.rpm\n"
printf ">>    RPM                        = teamspeak-"${VERSION%%.*}"-client-bundled-"$VERSION"-"$RELEASE".x86_64.rpm\n"
printf "  ____________________________________________________________________________\n"
printf ">>    (1)                        » compiling teamspeak-"${VERSION%%.*}"-client-bundled-"$VERSION".spec file\n"
gen_spec
printf ">>    (2)                        » building teamspeak-"${VERSION%%.*}"-client-bundled-"$VERSION"-"$RELEASE".src.rpm\n"
rpmbuild -bs $SPEC_FILE
printf ">>    (3)                        » building teamspeak-"${VERSION%%.*}"-client-bundled-"$VERSION"-"$RELEASE".rpm\n"
rpmbuild -bb $SPEC_FILE

