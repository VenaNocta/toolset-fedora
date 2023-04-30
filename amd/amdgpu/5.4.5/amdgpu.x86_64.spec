Name:			amdgpu
Version:		5.4.50405
Release:		1577590%{?dist}
License:		MIT
ExclusiveArch:	x86_64

Requires:		amdgpu-core
Requires:		amdgpu-dkms
Requires:		amdgpu-lib                      =  %{version}-%{release}

Requires:		rpmlib(CompressedFileNames)     <= 3.0.4-1
Requires:		rpmlib(FileDigests)             <= 4.6.0-1
Requires:		rpmlib(PayloadFilesHavePrefix)  <= 4.0-1
Requires:		rpmlib(PayloadIsXz)             <= 5.2-1

