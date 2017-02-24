%define kmod_name igbvf
Name: kmod-%{kmod_name}
Summary: Intel(R) 82576 Virtual Function
Version: 2.3.8.2
Release: 3%{?kpkgversion:%(echo .%{kpkgversion} | tr - _)}
Source: %{name}-%{version}.tar.gz
Vendor: Intel Corporation
License: GPL
ExclusiveOS: linux
Group: System Environment/Kernel
Provides: %{name}
URL: http://support.intel.com/support/go/linux/igbvf.htm
BuildRoot: %{_tmppath}/%{name}-%{version}-root

# do not generate debugging packages by default - older versions of rpmbuild
# may instead need:
%define debug_package %{nil}
%debug_package %{nil}

Requires: kernel, fileutils, findutils, gawk, bash

%if %{?kpkgversion:1}%{?!kpkgversion:0}
Requires: kernel = %{kpkgversion}
BuildRequires: kernel-devel = %{kpkgversion}
%endif

%description
This package contains the Linux driver for the Intel(R) 82576 Virtual Function.

%prep
%setup
%if "%{?kversion:1}%{?!kversion:0}%{?kpkgversion:1}%{?!kpkgversion:0}" != "11"
echo 'kversion (path to kernel src) and kpkgversion (version of kernel pkg) must be defined externally!'
exit 1
%endif

%build
make -C src KERNEL_SRC=%{_usrsrc}/kernels/%{kversion}

%install
%{__install} -d %{buildroot}/lib/modules/%{kversion}/drivers/net/ethernet/intel/%{kmod_name}/
%{__install} src/%{kmod_name}.ko %{buildroot}/lib/modules/%{kversion}/drivers/net/ethernet/intel/%{kmod_name}/

# Sign the modules(s).
%if %{?_with_modsign:1}%{!?_with_modsign:0}
# If the module signing keys are not defined, define them here.
%{!?privkey: %define privkey %{_sysconfdir}/pki/SECURE-BOOT-KEY.priv}
%{!?pubkey: %define pubkey %{_sysconfdir}/pki/SECURE-BOOT-KEY.der}
for module in $(find %{buildroot} -type f -name \*.ko);
do %{__perl} /usr/src/kernels/%{kversion}/scripts/sign-file \
    sha256 %{privkey} %{pubkey} $module;
done
%endif


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0755,root,root) /lib/modules/%(echo %{kversion})/drivers/net/ethernet/intel/%{kmod_name}/%{kmod_name}.ko

%changelog
* Fri Feb 24 2017 Michal Gawlik <michal.gawlik@thalesgroup.com> 2.3.8.2-3
- spec: remove old method of module autoloading (michal.gawlik@thalesgroup.com)
- spec: add used kernel version (michal.gawlik@thalesgroup.com)

* Fri Sep 09 2016 Michal Gawlik <michal.gawlik@thalesgroup.com> 2.3.8.2-2
- tito: switch to release tagger (3rd-party project)
  (michal.gawlik@thalesgroup.com)
- Compilation fix for kernel 4.7 (michal.gawlik@thalesgroup.com)

* Wed Jul 20 2016 Tomasz Rostanski <tomasz.rostanski@thalesgroup.com> 2.3.8.2-1
- new package built with tito


