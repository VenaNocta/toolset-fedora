Name:           sleuthkit-bundle
Version:        4.12.0
Release:        1
Conflicts:      sleuthkit
ExclusiveArch:  %{java_arches} x86_64
Summary:        The Sleuth Kit (TSK) Bundle

License:        CPL and IBM and GPLv2+
URL:            https://www.sleuthkit.org/sleuthkit/
Source0:        sleuthkit-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  libtool
BuildRequires:  gcc
Requires:       sleuthkit-core          = %{version}-%{release}
Requires:       sleuthkit-java-bindings = %{version}-%{release}

# https://src.fedoraproject.org/rpms/sleuthkit/blob/rawhide/f/sleuthkit.spec

%description
The Sleuth Kit is a collection of UNIX-based command line file and volume system forensic analysis tools. The file system tools allow you to examine file systems of a suspect computer in a non-intrusive fashion. Because the tools do not rely on the operating system to process the file systems, deleted and hidden content is shown.

The volume system (media management) tools allow you to examine the layout of disks and other media. The Sleuth Kit supports DOS partitions, BSD partitions (disk labels), Mac partitions, Sun slices (Volume Table of Contents), and GPT disks. With these tools, you can identify where partitions are located and extract them so that they can be analyzed with file system analysis tools.

## sleuthkit-core
%package        sleuthkit-core
Summary:        The Sleuth Kit (TSK) - Core
Requires:       mac-robber

%description    sleuthkit-core
The core binaries provided by TSK

## sleuthkit-java-bindings
%package        sleuthkit-java-bindings
Summary:        The Sleuth Kit (TSK) - Java Bindings
BuildRequires:  ant
Requires:       java-1.8.0-openjdk
Requires:       sleuthkit-core = %{version}-%{release}

%description    sleuthkit-java-bindings
The java bindings provided by TSK

%prep
rm -rf %{_builddir}/%{name}-%{version}/
mkdir -p %{_builddir}/%{name}-%{version}
pushd %{_builddir}/%{name}-%{version}
tar -xf %{_sourcedir}/sleuthkit-%{version}.tar.gz
popd

%build
pushd %{_builddir}/%{name}-%{version}/sleuthkit-%{version}/
JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk ./configure --disable-cppunit --enable-java --prefix %{_builddir}/%{name}-%{version}/target/ --exec-prefix=%{_builddir}/%{name}-%{version}/target/
make
make install
find %{_builddir}/%{name}-%{version}/target/ -name '*.la' -exec rm -f {} ';'
rm -rf %{_builddir}/%{name}-%{version}/target/lib/pkgconfig/
popd

%install
rm -rf %{buildroot}
# copy source files to target
pushd %{_builddir}/%{name}-%{version}/sleuthkit-%{version}/
mkdir -p %{buildroot}%{_docdir}/sleuthkit/
cp -nr docs/*                              %{buildroot}%{_docdir}/sleuthkit/
mkdir -p %{buildroot}%{_datadir}/licenses/sleuthkit/
cp -nr licenses/*                          %{buildroot}%{_datadir}/licenses/sleuthkit/
popd
# copy target files to target
pushd %{_builddir}/%{name}-%{version}/target/
mkdir -p %{buildroot}%{_bindir}/
cp -nr bin/                                %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_libdir}/
cp -nr lib/                                %{buildroot}%{_libdir}/
mkdir -p %{buildroot}%{_datadir}/java/sleuthkit/
cp -n  share/java/sleuthkit-%{version}.jar %{buildroot}%{_datadir}/java/sleuthkit/
ln -s  sleuthkit/sleuthkit-%{version}.jar  %{buildroot}%{_datadir}/java/sleuthkit.jar
mkdir -p %{buildroot}%{_mandir}/
cp -nr man/man1/                           %{buildroot}%{_mandir}/
popd
exit 0

%clean
#rm -rf %{buildroot}

## sleuthkit-core
%files sleuthkit-core

## sleuthkit-java-bindings
%files sleuthkit-java-bindings

