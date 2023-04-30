Name:			amdgpu-core
Version:		5.4.50405
Release:		1577590%{?dist}
License:		MIT
ExclusiveArch:	noarch

Requires:		rpmlib(CompressedFileNames)     <= 3.0.4-1
Requires:		rpmlib(FileDigests)             <= 4.6.0-1
Requires:		rpmlib(PayloadFilesHavePrefix)  <= 4.0-1
Requires:		rpmlib(PayloadIsXz)             <= 5.2-1

%post
prefix=/opt/amdgpu
conf=/etc/ld.so.conf.d/20-amdgpu.conf

echo "${prefix}/$(rpm --eval %{_lib})" >$conf
if [ "$(rpm --eval %{_arch})" = "x86_64" ]; then
  echo "${prefix}/lib" >>$conf
fi

%postun
if [ $1 -eq 0 ]; then
  rm -f /etc/ld.so.conf.d/20-amdgpu.conf
  /sbin/ldconfig
fi

