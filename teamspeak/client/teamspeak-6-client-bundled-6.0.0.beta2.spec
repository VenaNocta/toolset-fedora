Name:           teamspeak-6-client-bundled
Version:        6.0.0.beta2
Release:        1
Summary:        TeamSpeak 6 Client repackaged for RPM based systems

License:        «proprietary»
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
Provides TeamSpeak 6 Client


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

