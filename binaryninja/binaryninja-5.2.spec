Name:           binaryninja
Version:        5.2
Release:        1
Summary:        BinaryNinja repackaged for RPM based systems

License:        «proprietary»
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
Provides binaryninja


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

