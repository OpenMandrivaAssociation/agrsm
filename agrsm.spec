%define module agrsm
%define version 2.1.80
%define card Agere Systems Soft Modem

%define extra ONE_A1XX
%define date 20080527
%define distname %{module}-%{version}-%{extra}-%{date}

Summary: %{module} driver
Name: %{module}
Version: %{version}
Release: %mkrel 3
# http://service.one.de/download/index.php?&direction=0&order=&directory=NOTEBOOKS/ONE_A1xx/Linux%20Drivers/Source-code
Source0: %{distname}.tar.gz
Source1: /usr/src/linux-2.6.24.5-1mnb/sound/pci/hda/hda_codec.h
Patch0: modem-update-device_interrupt-definition.patch
Patch1: modem-update-for-serial-changes.patch
Patch2: modem-update-irq-flags.patch
Patch3: modem-update-hda-structs.patch
Patch4: modem-fix-ptr-warnings.patch
Patch5: modem-drvname.patch
Patch6: agrsm-2.1.80-ONE_A1XX-20080527-modprobe.patch
Patch7: agrsm-2.1.80-ONE_A1XX-20080527-hda_codec.patch
Patch8: agrsm-2.1.80-ONE_A1XX-20080527-LSB.patch
License: Commercial
Group: System/Kernel and hardware
URL: http://www.lsi.com/
BuildRoot: %{_tmppath}/%{name}-buildroot
ExclusiveArch: %{ix86}

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
cp %{SOURCE1} .
%patch0 -p1 -b .device-interrupt
%patch1 -p1 -b .for-serial-changes
%patch2 -p1 -b .irq-flags
%patch3 -p1 -b .hda-structs
%patch4 -p1 -b .warnings
%patch5 -p1 -b .drvname
%patch6 -p1 -b .modprobe
%patch7 -p1 -b .hda_codec
%patch8 -p1 -b .LSB

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/src/%{module}-%{version}-%{release}/
cat > %{buildroot}/usr/src/%{module}-%{version}-%{release}/dkms.conf <<EOF
PACKAGE_NAME=%{module}
PACKAGE_VERSION=%{version}-%{release}
DEST_MODULE_LOCATION[0]=/kernel/drivers/char
DEST_MODULE_LOCATION[1]=/kernel/drivers/char
BUILT_MODULE_NAME[0]=agrmodem
BUILT_MODULE_NAME[1]=agrserial
CLEAN="make clean"
AUTOINSTALL="yes"
EOF

tar c . | tar x -C %{buildroot}/usr/src/%{module}-%{version}-%{release}/

install -d %{buildroot}%{_initrddir}
install -m755 agr_softmodem %{buildroot}%{_initrddir}
install -d %{buildroot}%{_prefix}/lib/AgereSoftModem
install -m755 AgereMdmDaemon %{buildroot}%{_prefix}/lib/AgereSoftModem

%clean
rm -rf %{buildroot}

%post
%_post_service agr_softmodem

%preun
%_preun_service agr_softmodem

%files
%defattr(-,root,root)
%{_initrddir}/agr_softmodem
%dir %{_prefix}/lib/AgereSoftModem
%{_prefix}/lib/AgereSoftModem/AgereMdmDaemon

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
