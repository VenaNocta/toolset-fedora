Name:           sleuthkit
Version:        4.12.0
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
Requires:       java-1.8.0-openjdk
Requires:       sleuthkit-core = %{version}-%{release}

%description    java-bindings
The java bindings provided by TSK

%prep
%define version1 %(printf %{version} | cut --delimiter='.' --fields=1)
%define version2 %(printf %{version} | cut --delimiter='.' --fields=1,2)
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
popd
pushd %{_builddir}/%{name}-%{version}/target/
gzip -r share/man/man1/
find    lib/ -type l -exec rm {} ';'
find    lib/ -name '*.la' -exec rm -f {} ';'
rm -rf  lib/pkgconfig/
mv      lib/libtsk.so.*     lib/libtsk.so.%{version}
mv      lib/libtsk_jni.so.* lib/libtsk_jni.so.%{version}
popd

%install
rm -rf %{buildroot}
# copy source files to target
pushd %{_builddir}/%{name}-%{version}/sleuthkit-%{version}/
mkdir -p %{buildroot}%{_docdir}/sleuthkit/
cp -nr docs/*                                      %{buildroot}%{_docdir}/sleuthkit/
mkdir -p %{buildroot}%{_datadir}/licenses/sleuthkit/
cp -nr licenses/*                                  %{buildroot}%{_datadir}/licenses/sleuthkit/
popd
# copy target files to target
pushd %{_builddir}/%{name}-%{version}/target/
mkdir -p %{buildroot}%{_bindir}/
cp -nr bin/*                                         %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_libdir}/
cp -n  lib/libtsk.a                                  %{buildroot}%{_libdir}/
cp -n  lib/libtsk.so.%{version}                      %{buildroot}%{_libdir}/
ln -s  libtsk.so.%{version}                          %{buildroot}%{_libdir}/libtsk.so
ln -s  libtsk.so.%{version}                          %{buildroot}%{_libdir}/libtsk.so.%{version1}
ln -s  libtsk.so.%{version}                          %{buildroot}%{_libdir}/libtsk.so.%{version2}
cp -n  lib/libtsk_jni.a                              %{buildroot}%{_libdir}/
cp -n  lib/libtsk_jni.so.%{version}                  %{buildroot}%{_libdir}/
ln -s  libtsk_jni.so.%{version}                      %{buildroot}%{_libdir}/libtsk_jni.so
ln -s  libtsk_jni.so.%{version}                      %{buildroot}%{_libdir}/libtsk_jni.so.%{version1}
ln -s  libtsk_jni.so.%{version}                      %{buildroot}%{_libdir}/libtsk_jni.so.%{version2}
mkdir -p %{buildroot}%{_datadir}/tsk/
cp -nr share/tsk/*                                   %{buildroot}%{_datadir}/tsk/
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Java/#JNI
mkdir -p %{buildroot}%{_jnidir}/sleuthkit/
cp -n  share/java/sleuthkit-%{version}.jar           %{buildroot}%{_jnidir}/sleuthkit/
ln -s  %{_jnidir}/sleuthkit/sleuthkit-%{version}.jar %{buildroot}%{_libdir}/sleuthkit.jar
mkdir -p %{buildroot}%{_javadir}/sleuthkit/
cp -n  share/java/sleuthkit-caseuco-%{version}.jar   %{buildroot}%{_javadir}/sleuthkit/
ln -s  sleuthkit/sleuthkit-caseuco-%{version}.jar    %{buildroot}%{_javadir}/sleuthkit-caseuco.jar
mkdir -p %{buildroot}%{_mandir}/
cp -nr share/man/man1/                               %{buildroot}%{_mandir}/
popd
exit 0

%clean
#rm -rf %{buildroot}

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
%{_libdir}/libtsk.a
%{_libdir}/libtsk.so
%{_libdir}/libtsk.so.%{version1}
%{_libdir}/libtsk.so.%{version2}
%{_libdir}/libtsk.so.%{version}
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

## sleuthkit-java-bindings
%files java-bindings
%{_libdir}/libtsk_jni.a
%{_libdir}/libtsk_jni.so
%{_libdir}/libtsk_jni.so.%{version1}
%{_libdir}/libtsk_jni.so.%{version2}
%{_libdir}/libtsk_jni.so.%{version}
%{_jnidir}/sleuthkit/sleuthkit-%{version}.jar
%{_libdir}/sleuthkit.jar
%{_javadir}/sleuthkit/sleuthkit-caseuco-%{version}.jar
%{_javadir}/sleuthkit-caseuco.jar
%{_datadir}/tsk/sorter/default.sort
%{_datadir}/tsk/sorter/freebsd.sort
%{_datadir}/tsk/sorter/images.sort
%{_datadir}/tsk/sorter/linux.sort
%{_datadir}/tsk/sorter/openbsd.sort
%{_datadir}/tsk/sorter/solaris.sort
%{_datadir}/tsk/sorter/windows.sort

