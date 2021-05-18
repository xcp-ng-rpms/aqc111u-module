%define vendor_name Marvell
%define vendor_label marvell
%define driver_name aqc111u

%if %undefined module_dir
%define module_dir extra
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{driver_name}-module
Version: 1.3.3.0
Release: 1%{?dist}
License: GPL

#Source taken from https://www.marvell.com/content/dam/marvell/en/drivers/AQ_USBDongle_LinuxDriver_1.3.3.0.zip
Source0: %{driver_name}-%{version}.tar.gz

Patch0: %{driver_name}-%{version}.patch

BuildRequires: gcc
BuildRequires: kernel-devel
Provides: %{driver_name}-module
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -n %{driver_name}-%{version}

%build
%{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# remove extra files modules_install copies in
rm -f %{buildroot}/lib/modules/%{kernel_version}/modules.*

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Sun May 09 2021 Simone Conti <s.conti@itnok.com> - 1.3.3.0-1
- Adding patch to rename kernel module from `aqc111` to `aqc111u`
- Re-packing for XCP-ng of Marvell AQC111U driver
