%if 0%{?fedora}
%global debug_package %{nil}
%endif

Name:     aorus-laptop
Version:  {{{ git_dir_version }}}
Release:  1%{?dist}
Summary:  Kernel module for Gigabyte Aero/AORUS laptops to interact with the embedded controller.
License:  GPLv2
URL:      https://github.com/Ethernium/aorus-akmod

Source:   %{url}/archive/refs/heads/main.tar.gz

Provides: %{name}-kmod-common = %{version}
Requires: %{name}-kmod >= %{version}

BuildRequires: systemd-rpm-macros

%description
Kernel module for Gigabyte Aero/AORUS laptops to interact with the embedded controller.

Gigabyte Gaming series laptops are not supported. Since they are rebadged Clevo laptops (NP5x/NP7x series), you can use existing Clevo drivers instead.

%prep
%setup -q -c aorus-akmod-main

%build
install -D -m 0644 aorus-akmod-main/%{name}.conf %{buildroot}%{_modulesloaddir}/%{name}.conf

%files
%doc aorus-akmod-main/README.md
%license aorus-akmod-main/LICENSE
%{_modulesloaddir}/%{name}.conf

%changelog
{{{ git_dir_changelog }}}
