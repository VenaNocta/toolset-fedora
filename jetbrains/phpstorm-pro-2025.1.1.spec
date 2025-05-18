Name:           phpstorm-pro
Version:        2025.1.1
Release:        1
Summary:        PhpStorm Professional repackaged for RPM based systems

License:        «proprietary»
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
Provides phpstorm-pro


## phpstorm-pro-jbr
%package        jbr
Summary:        PhpStorm Professional - Java Runtime
Requires:       %{name} = %{version}-%{release}
AutoReqProv:    no

%description    jbr
Provides JetBrain's Java Runtime for PhpStorm Professional


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

