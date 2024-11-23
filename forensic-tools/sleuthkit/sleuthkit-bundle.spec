Name:           sleuthkit
Version:        4.12.1
Release:        1
Conflicts:      sleuthkit
ExclusiveArch:  %{java_arches}
Summary:        The Sleuth Kit (TSK) Bundle

License:        CPL and IBM and GPLv2+
URL:            https://www.sleuthkit.org/sleuthkit/
Source0:        sleuthkit-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  libtool
BuildRequires:  gcc-c++
BuildRequires:  gzip

# https://src.fedoraproject.org/rpms/sleuthkit/blob/rawhide/f/sleuthkit.spec

%description
The Sleuth Kit is a collection of UNIX-based command line file and volume system forensic analysis tools. The file system tools allow you to examine file systems of a suspect computer in a non-intrusive fashion. Because the tools do not rely on the operating system to process the file systems, deleted and hidden content is shown.

The volume system (media management) tools allow you to examine the layout of disks and other media. The Sleuth Kit supports DOS partitions, BSD partitions (disk labels), Mac partitions, Sun slices (Volume Table of Contents), and GPT disks. With these tools, you can identify where partitions are located and extract them so that they can be analyzed with file system analysis tools.

## sleuthkit-core
%package        core
Summary:        The Sleuth Kit (TSK) - Core
Conflicts:      sleuthkit
Requires:       mac-robber

%description    core
The core binaries provided by TSK

## sleuthkit-java-bindings
%package        java-bindings
Summary:        The Sleuth Kit (TSK) - Java Bindings
BuildRequires:  ant
BuildRequires:  ant-junit
Requires:       javapackages-filesystem
%define java_version      17
%define jdk java-%{java_version}-openjdk
BuildRequires:  %{jdk}
#Requires:       java-%{java_version}
Requires:       (sleuthkit-core = %{version}-%{release} or sleuthkit = %{version})

%description    java-bindings
The java bindings provided by TSK

%prep
rm -rf %{_builddir}/%{name}-%{version}/
mkdir -p %{_builddir}/%{name}-%{version}
pushd %{_builddir}/%{name}-%{version}
tar -xf %{_sourcedir}/sleuthkit-%{version}.tar.gz
popd

%build
%define builddir_extract %{_builddir}/%{name}-%{version}/sleuthkit-%{version}/ 
pushd %{builddir_extract}
JAVA_HOME=/usr/lib/jvm/%{jdk} ./configure --prefix=/usr --exec-prefix=/usr --disable-cppunit --enable-java
popd

%install
pushd %{builddir_extract}
%make_install
popd

# copy source files to buildroot
pushd %{builddir_extract}/
mkdir -p %{buildroot}%{_docdir}/sleuthkit/
cp -nr docs/*                                           %{buildroot}%{_docdir}/sleuthkit/
mkdir -p %{buildroot}%{_datadir}/licenses/sleuthkit/
cp -nr licenses/*                                       %{buildroot}%{_datadir}/licenses/sleuthkit/
popd

pushd %{buildroot}
gzip -r usr/share/man/man1/
rm -rf  usr/lib/pkgconfig/

## https://docs.fedoraproject.org/en-US/packaging-guidelines/Java/#JNI
mkdir -p %{buildroot}%{_jnidir}/
mv usr/share/java/sleuthkit-%{version}.jar              %{buildroot}%{_jnidir}
popd


%clean
rm -rf %{buildroot}

## sleuthkit-core
%files core
%{_bindir}/blkcalc
%{_bindir}/blkcat
%{_bindir}/blkls
%{_bindir}/blkstat
%{_bindir}/fcat
%{_bindir}/ffind
%{_bindir}/fiwalk
%{_bindir}/fls
%{_bindir}/fsstat
%{_bindir}/hfind
%{_bindir}/icat
%{_bindir}/ifind
%{_bindir}/ils
%{_bindir}/img_cat
%{_bindir}/img_stat
%{_bindir}/istat
%{_bindir}/jcat
%{_bindir}/jls
%{_bindir}/jpeg_extract
%{_bindir}/mactime
%{_bindir}/mmcat
%{_bindir}/mmls
%{_bindir}/mmstat
%{_bindir}/pstat
%{_bindir}/sigfind
%{_bindir}/sorter
%{_bindir}/srch_strings
%{_bindir}/tsk_comparedir
%{_bindir}/tsk_gettimes
%{_bindir}/tsk_imageinfo
%{_bindir}/tsk_loaddb
%{_bindir}/tsk_recover
%{_bindir}/usnjls
%{_includedir}/tsk/
%docdir %{_docdir}/sleuthkit/
%{_docdir}/sleuthkit/README.txt
%license %{_datadir}/licenses/sleuthkit/
%{_mandir}/man1/blkcalc.1.gz
%{_mandir}/man1/blkcat.1.gz
%{_mandir}/man1/blkls.1.gz
%{_mandir}/man1/blkstat.1.gz
%{_mandir}/man1/fcat.1.gz
%{_mandir}/man1/ffind.1.gz
%{_mandir}/man1/fls.1.gz
%{_mandir}/man1/fsstat.1.gz
%{_mandir}/man1/hfind.1.gz
%{_mandir}/man1/icat.1.gz
%{_mandir}/man1/ifind.1.gz
%{_mandir}/man1/ils.1.gz
%{_mandir}/man1/img_cat.1.gz
%{_mandir}/man1/img_stat.1.gz
%{_mandir}/man1/istat.1.gz
%{_mandir}/man1/jcat.1.gz
%{_mandir}/man1/jls.1.gz
%{_mandir}/man1/mactime.1.gz
%{_mandir}/man1/mmcat.1.gz
%{_mandir}/man1/mmls.1.gz
%{_mandir}/man1/mmstat.1.gz
%{_mandir}/man1/sigfind.1.gz
%{_mandir}/man1/sorter.1.gz
%{_mandir}/man1/tsk_comparedir.1.gz
%{_mandir}/man1/tsk_gettimes.1.gz
%{_mandir}/man1/tsk_loaddb.1.gz
%{_mandir}/man1/tsk_recover.1.gz
%{_mandir}/man1/usnjls.1.gz
%{_datadir}/tsk/sorter/default.sort
%{_datadir}/tsk/sorter/freebsd.sort
%{_datadir}/tsk/sorter/images.sort
%{_datadir}/tsk/sorter/linux.sort
%{_datadir}/tsk/sorter/openbsd.sort
%{_datadir}/tsk/sorter/solaris.sort
%{_datadir}/tsk/sorter/windows.sort

## sleuthkit-java-bindings
%files java-bindings
/usr/lib/libtsk.a
/usr/lib/libtsk.so*
/usr/lib/libtsk_jni.a
/usr/lib/libtsk_jni.so*
%{_jnidir}/sleuthkit-%{version}.jar
%{_javadir}/sleuthkit-caseuco-%{version}.jar
