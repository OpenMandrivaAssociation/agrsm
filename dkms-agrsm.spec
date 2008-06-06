%define module agrsm
%define version 2.1.80
%define card Agere Systems Soft Modem

%define extra ONE_A1XX
%define date 20080527
%define distname %{module}-%{version}-%{extra}-%{date}

Summary: %{module} driver
Name: %{module}
Version: %{version}
Release: %mkrel 1
# http://service.one.de/download/index.php?&direction=0&order=&directory=NOTEBOOKS/ONE_A1xx/Linux%20Drivers/Source-code
Source0: %{distname}.tar.gz
License: Commercial
Group: System/Kernel and hardware
URL: http://www.lsi.com/
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildArch: noarch

%description
This package contains the %{module} driver for %{card}.

%package -n dkms-%{name}
Summary: dkms package for %{module} driver
Group: System/Kernel and hardware
Requires(preun): dkms
Requires(post): dkms

%description -n dkms-%{module}
This package contains the %{module} driver for %{card}.

%prep
%setup -q -n %{distname}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/src/%{module}-%{version}-%{release}/
cat > %{buildroot}/usr/src/%{module}-%{version}-%{release}/dkms.conf <<EOF
PACKAGE_NAME=%{module}
PACKAGE_VERSION=%{version}-%{release}
DEST_MODULE_LOCATION[0]=/kernel/drivers/char
BUILT_MODULE_NAME[0]=%{module}
AUTOINSTALL="yes"
EOF

tar c . | tar x -C %{buildroot}/usr/src/%{module}-%{version}-%{release}/

%clean
rm -rf %{buildroot}

%files -n dkms-%{module}
%defattr(0644,root,root,0755)
/usr/src/%{module}-%{version}-%{release}/

%post -n dkms-%{module}
/usr/sbin/dkms --rpm_safe_upgrade add -m %{module} -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade build -m %{module} -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade install -m %{module} -v %{version}-%{release}
exit 0

%preun -n dkms-%{module}
/usr/sbin/dkms --rpm_safe_upgrade remove -m %{module} -v %{version}-%{release} --all
exit 0
