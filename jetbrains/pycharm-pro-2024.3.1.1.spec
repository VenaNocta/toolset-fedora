Name:           pycharm-pro
Version:        2024.3.1.1
Release:        1
Summary:        PyCharm Professional repackaged for RPM based systems

License:        «proprietary»
URL:            https://www.jetbrains.com/pycharm/
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
Provides pycharm-pro


## pycharm-pro-jbr
%package        jbr
Summary:        PyCharm Professional - Java Runtime
Requires:       %{name} = %{version}-%{release}
AutoReqProv:    no

%description    jbr
Provides JetBrain's Java Runtime for PyCharm Professional


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
chmod +x           %{buildroot}%{_bindir}/pycharm-pro
mkdir -p           %{buildroot}%{_sysconfdir}/jetbrains/
mv                 %{buildroot}%{libdir}/bin/pycharm64.vmoptions  %{buildroot}%{_sysconfdir}/jetbrains/
mkdir -p           %{buildroot}%{_datadir}/icons/jetbrains/
mkdir -p           %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/
mv                 %{buildroot}%{libdir}/bin/pycharm.png   %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/pycharm-pro.png
mkdir -p           %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
mv                 %{buildroot}%{libdir}/bin/pycharm.svg   %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/pycharm-pro.svg


%clean
rm -rf             %{buildroot}


%files
%{_bindir}/pycharm-pro
%{_datadir}/applications/com.jetbrains.pycharm-pro.desktop
%{_datadir}/icons/hicolor/128x128/apps/pycharm-pro.png
%{_datadir}/icons/hicolor/scalable/apps/pycharm-pro.svg
%config(noreplace) %{_sysconfdir}/jetbrains/pycharm64.vmoptions
%{libdir}/Install-Linux-tar.txt
%{libdir}/product-info.json
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
* Thu Jan 13 2025 VenaNocta <venanocta@gmail.com> - 20250113
- patched for Fedora deploy

