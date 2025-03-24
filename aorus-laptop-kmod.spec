%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%global tag master
%global ref heads
%endif

Name:     aorus-laptop-kmod
Version:  {{{ git_dir_version }}}
Release:  1%{?dist}
Summary:  Experimental kernel driver for Gigabyte Aero/AORUS laptops to interact with the embedded controller.
License:  GPLv2
URL:      https://github.com/tangalbert919/gigabyte-laptop-wmi

Source:   %{url}/archive/refs/%{ref}/%{tag}.tar.gz

BuildRequires: kmodtool

%description
Experimental kernel driver for Gigabyte Aero/AORUS laptops to interact with the embedded controller.

Gigabyte Gaming series laptops are not supported. Since they are rebadged Clevo laptops (NP5x/NP7x series), you can use existing Clevo drivers instead.

%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%prep
%setup -c gigabyte-laptop-wmi-${tag}

for kernel_version in %{?kernel_versions}; do
  mkdir -p _kmod_build_${kernel_version%%___*}
  cp -a gigabyte-laptop-wmi-master/*.c gigabyte-laptop-wmi-master/Makefile _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} VERSION=v%{version} modules
done

%install
for kernel_version in %{?kernel_versions}; do
  mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
  install -D -m 755 _kmod_build_${kernel_version%%___*}/aorus-laptop.ko \
    %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
  chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/aorus-laptop.ko
done
%{?akmod_install}

%changelog
{{{ git_dir_changelog }}}
