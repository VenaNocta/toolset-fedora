Name:           autopsy-core
Version:        4.21.0
Release:        1
ExclusiveArch:  %{java_arches} x86_64
Summary:        Autopsy repackaged for RPM based systems

License:        Apache-2.0
URL:            https://www.sleuthkit.org/autopsy/
Source0:        %{name}-%{version}.tar.xz

AutoReqProv:    no
Requires:       testdisk
Requires:       java-17
## needs openjfx but freezes with it
#Requires:      java-17-openjdk-openjfx
Requires:       sleuthkit-java-bindings = 4.12.1
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
ln -sf             /usr/lib/java/sleuthkit-4.12.1.jar  %{buildroot}%{_libdir}/autopsy/autopsy/modules/ext/sleuthkit-4.12.1.jar
#ln -s              %{_javadir}/sleuthkit-caseuco.jar       %{buildroot}%{_libdir}/autopsy/autopsy/modules/ext/sleuthkit-caseuco-4.12.1.jar
mkdir -p           %{buildroot}%{_datadir}/applications/
cp -n              org.sleuthkit.autopsy.desktop           %{buildroot}%{_datadir}/applications/
mkdir -p           %{buildroot}%{_datadir}/icons/autopsy/
cp -n              autopsy.png                             %{buildroot}%{_datadir}/icons/autopsy/
mkdir -p           %{buildroot}%{_docdir}/autopsy/
cp -nr             docs/*                                  %{buildroot}%{_docdir}/autopsy/
popd

# update jdkhome
awk    '!/^\s*#?\s*jdkhome=.*$/' %{name}-%{version}/etc/autopsy.conf > %{buildroot}%{_sysconfdir}/autopsy.conf
printf "jdkhome=/usr/lib/jvm/jre-17\n" >> %{buildroot}%{_sysconfdir}/autopsy.conf

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

