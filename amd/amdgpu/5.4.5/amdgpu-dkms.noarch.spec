Name:			amdgpu-dkms
Summary:		The amdgpu Linux kernel driver
Version:		5.18.13.50405
Release:		1577590%{?dist}
License:		GPLv2 and Redistributable, no modification permitted
Group:			System Environment/Kernel
ExclusiveArch:	noarch

Requires:		amdgpu-dkms-firmware            =  1:%{version}-%{release}
Requires:		config(amdgpu-dkms)             =  1:%{version}-%{release}
Requires:		dkms                            >= 1.95

Requires:		autoconf
Requires:		automake
Requires:		gcc
Requires:		kernel-devel
Requires:		make
Requires:		rpmlib(CompressedFileNames)     <= 3.0.4-1
Requires:		rpmlib(FileDigests)             <= 4.6.0-1
Requires:		rpmlib(PayloadFilesHavePrefix)  <= 4.0-1
Requires:		rpmlib(PayloadIsXz)             <= 5.2-1

%description
The AMD display driver kernel module in DKMS format for AMD graphics S/W

%package firmware
Summary:		Firmware for amdgpu-dkms

%description firmware
The AMD display driver firmware blobs used by kernel module in DKMS format

%package headers
Summary:		Header files for the AMD display driver kernel module
Group:			Development/Libraries

%description headers
amdgpu-dkms-headers includes a subset of the C header files that specify the
interface between the Linux kernel and userspace libraries and programs. This
package only contains amdgpu-dkms headers that may differ from the files from
the kernel-headers package.

%post
rc=0
postinst=/usr/libexec/dkms/common.postinst

if [ ! -x $postinst ]; then
	postinst=/usr/lib/dkms/common.postinst
fi

if /usr/bin/mokutil --sb-state | grep -iq enabled && \
    ! grep -q "^[[:blank:]]*sign_tool=" /etc/dkms/framework.conf; then
  if [ ! -f "/root/mok.priv" ]; then
    mkdir -p /root
    /usr/bin/openssl req -new -x509 -newkey rsa:2048 \
      -keyout /root/mok.priv -out /root/mok.der -nodes \
      -days 36500 -subj "/CN=root/" -outform DER
    if [ $? -ne 0 ]; then
      echo "ERROR: Failed to generate mok/dkms signing key" >&2
      exit 1
    fi
  fi
  ln -s /root/mok.priv /root/dkms.key
  ln -s /root/mok.der /root/dkms.der
  echo 'sign_tool="/etc/dkms/sign_helper.sh"' >> /etc/dkms/framework.conf
fi

if [ -x $postinst ]; then
  #
  # Prevent modprobe amdgpu by DKMS that may cause black screen during
  # installation:
  #    1. Blacklist amdgpu
  #    2. Build and install amdgpu kernel module
  #    3. Remove amdgpu from blacklist
  #    4. Generate new initramfs
  #
  echo "blacklist amdgpu" >/etc/modprobe.d/blacklist-amdgpu.conf
  $postinst amdgpu %{version}-%{release}
  rc=$?
  rm -f /etc/modprobe.d/blacklist-amdgpu.conf
  if [ $rc -eq 0 ]; then
    #
    # Different versions of dkms may format output of the status differently,
    # for example:
    #
    #  amdgpu, <version>, <kernel version>, x86_64: installed
    #  amdgpu/<version>, <kernel version>, x86_64: installed (<comments>)
    #
    # To handle it correctly we use a multi-separator for `read' function to
    # make sure the kernel version is always in the field #3. The rest of the
    # output appears in `status' variable that has to contain `installed'
    # sub-string.
    #
    # Collect all kernel versions in /var/tmp/amdgpu-dkms-kernels file to be
    # used by %postun scriptlet to re-generate initramfs images.
    #
    echo -n >/var/tmp/amdgpu-dkms-kernels
    while IFS=" /," read name mver kver status; do
      if [ -z "${status##*installed*}" ]; then
        /usr/bin/dracut -f --kver $kver
	echo "$kver" >>/var/tmp/amdgpu-dkms-kernels
      fi
    done<<<$(/usr/sbin/dkms status amdgpu/%{version}-%{release})
  fi
else
  echo "WARNING: $postinst does not exist."
fi

if [ ! $rc ]; then
  echo -e "ERROR: DKMS version is too old and amdgpu was not"
  echo -e "built with legacy DKMS support."
  echo -e "You must either rebuild amdgpu with legacy postinst"
  echo -e "support or upgrade DKMS to a more current version."
fi

exit $rc

%preun
dkms remove -m amdgpu -v %{version}-%{release} --all --rpm_safe_upgrade
exit $?

%postun
while read kver; do
  /usr/bin/dracut -f --kver $kver
done < /var/tmp/amdgpu-dkms-kernels

if [ $1 -eq 0 ]; then
  rm -f /var/tmp/amdgpu-dkms-kernels
fi

