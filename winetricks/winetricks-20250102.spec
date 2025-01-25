Name:           winetricks
Version:        20250102
Release:        1
Summary:        Winetricks repackaged for RPM based systems

License:        LGPL-2.1
URL:            https://github.com/Winetricks/winetricks
Source0:        %{name}-%{version}.tar.xz
BuildArch:      noarch

AutoReqProv:    no

%description
Provides winetricks


## winetricks-bash-completion
%package        bash-completion
Summary:        Winetricks - bash-completion
Requires:       %{name} = %{version}-%{release}
Requires:       bash-completion

%description    bash-completion
Provides bash-completion for Winetricks


## winetricks-gui
%package        gui
Summary:        Winetricks - gui
Requires:       %{name} = %{version}-%{release}

%description    gui
Provides gui & .desktop file for Winetricks


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

