%global sname   skindesigner
# https://gitlab.com/kamel5/skindesigner/-/archive/71b3e514c6c7f8eb76751ce04f1e3dd8f3037b25
%global commit0 71b3e514c6c7f8eb76751ce04f1e3dd8f3037b25
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gitdate 20240104

# Set vdr_version based on Fedora version
%if 0%{?fedora} >= 43
%global vdr_version 2.7.6
%elif 0%{?fedora} == 42
%global vdr_version 2.7.4
%else
%global vdr_version 2.6.9
%endif

Name:           vdr-skindesigner
Version:        1.2.25
Release:        5%{?dist}
# Release:        0.6.%%{gitdate}git%%{shortcommit0}%%{?dist}
Summary:        A VDR skinning engine that displays XML based Skins
License:        GPL-2.0-or-later
Epoch:          1
URL:            https://gitlab.com/kamel5/skindesigner
Source0:        %url/-/archive/%{version}/%{sname}-%{version}.tar.bz2
# Source0:        %%url/-/archive/%%{commit0}/%%{name}-%%{shortcommit0}.tar.gz
# Configuration files for plugin parameters. These are Fedora specific and not in upstream.
Source1:        %{name}.conf

BuildRequires:  gcc-c++
BuildRequires:  vdr-devel >= %{vdr_version}
BuildRequires:  gettext
BuildRequires:  libcurl-devel
BuildRequires:  libxml2-devel
BuildRequires:  freetype-devel
BuildRequires:  fontconfig-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  cairo-devel
BuildRequires:  librsvg2-devel
Requires:       vdr(abi)%{?_isa} = %{vdr_apiversion}
Requires:       vdr-softhddevice
Requires:       vdr-epgsearch

%description
SkinDesigner is a powerful tool to create VDR Skins based on Skindesigner
specific XML Code. The following documentation shows the SkinDesigner
"internals" so that new Skinners get easily an overview how Skindesigner works.
Hopefully all your open questions are answered, if not, feel free to ask in
VDR Portal.

%package data
Summary:       Icons xml files for %{name}
Group:         Applications/Multimedia
BuildArch:     noarch
Requires:      %{name} = %{epoch}:%{version}-%{release}

%description data
This package contains icons and xml files.

%package -n libskindesignerapi
Summary:        Library files for %{name}

%description -n libskindesignerapi
Library which provides the Skindesigner API to other VDR Plugins.
VDR Plugins using this API are able to use all Skindesigner
facilities to display their OSD representation.

%package -n libskindesignerapi-devel
Summary:        Development files for libskindesignerapi
Requires:       libskindesignerapi%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       vdr-devel >= 2.0.0

%description -n libskindesignerapi-devel
Development files for libskindesignerapi.

%prep
%autosetup -p1 -n skindesigner-%{version}

sed -i -e 's|PREFIX ?= /usr/local|PREFIX ?= /usr|g' libskindesignerapi/Makefile
sed -i -e 's|LIBDIR ?= $(PREFIX)/lib|LIBDIR ?= %{_libdir}/|g' libskindesignerapi/Makefile
sed -i -e 's|PCDIR  ?= $(PREFIX)/lib/pkgconfig|PCDIR  ?= %{_libdir}/pkgconfig|g' libskindesignerapi/Makefile

# changed permission due rpmlint warning E: non-executable-script
chmod a+x scripts/{temperatures.g2v,vdrstats.default}

%build
%{set_build_flags}
%make_build

%install
# make install would install the themes under /etc, let's not use that
make install-subprojects install-lib install-i18n DESTDIR=%{buildroot} INSTALL="install -p"
# install the themes to the custom location used in Fedora
install -dm 755 %{buildroot}%{vdr_vardir}/themes
install -pm 644 themes/*.theme %{buildroot}%{vdr_vardir}/themes/
# install the skins to the custom location used in Fedora
install -dm 755 %{buildroot}%{vdr_resdir}/plugins/%{sname}/skins
cp -pR skins/* %{buildroot}%{vdr_resdir}/plugins/%{sname}/skins
# install the dtd to the custom location used in Fedora
install -dm 755 %{buildroot}%{vdr_resdir}/plugins/%{sname}/dtd
cp -pR dtd/* %{buildroot}%{vdr_resdir}/plugins/%{sname}/dtd
# install the scripts to the custom location used in Fedora
install -dm 755 %{buildroot}%{vdr_resdir}/plugins/%{sname}/scripts
cp -pR scripts/* %{buildroot}%{vdr_resdir}/plugins/%{sname}/scripts
# create path where XML skins are installed by the Skindesigner Installer
install -dm 755 %{buildroot}%{vdr_resdir}/plugins/%{sname}/installerskins/

# skindesigner.conf
install -Dpm 644 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/sysconfig/vdr-plugins.d/%{sname}.conf

# install missing symlink (was giving no-ldconfig-symlink rpmlint errors)
ldconfig -n %{buildroot}%{_libdir}

#
mkdir -p %{buildroot}/etc/vdr/plugins/skindesigner/
ln -s %{vdr_resdir}/plugins/skindesigner/dtd %{buildroot}/%{vdr_configdir}/plugins/skindesigner/

%find_lang %{name}

%post -n libskindesignerapi -p /sbin/ldconfig

%postun -n libskindesignerapi -p /sbin/ldconfig

%files -f %{name}.lang
%doc HISTORY README
%license COPYING
%config(noreplace) %{_sysconfdir}/sysconfig/vdr-plugins.d/%{sname}.conf
%{vdr_plugindir}/libvdr-*.so.%{vdr_apiversion}
%dir %{vdr_resdir}/plugins/%{sname}/dtd
%{vdr_resdir}/plugins/%{sname}/dtd/*
%dir %{vdr_resdir}/plugins/%{sname}/scripts
%{vdr_resdir}/plugins/%{sname}/scripts/*
%{vdr_configdir}/plugins/skindesigner/dtd
# to be able to install skin repos without the data package
%dir %{vdr_resdir}/plugins/%{sname}/
%dir %{vdr_resdir}/plugins/%{sname}/installerskins/

%files data
%dir %{vdr_resdir}/plugins/%{sname}/skins
%{vdr_resdir}/plugins/%{sname}/skins/*
%{vdr_vardir}/themes/*.theme

%files -n libskindesignerapi
%doc libskindesignerapi/README
%license libskindesignerapi/COPYING
%{_libdir}/libskindesignerapi.so.*

%files -n libskindesignerapi-devel
%{_libdir}/pkgconfig/libskindesignerapi.pc
%{_libdir}/libskindesignerapi.so
%dir %{_includedir}/libskindesignerapi
%{_includedir}/libskindesignerapi/*

%changelog
* Sat Jun 21 2025 Martin Gansser <martinkg@fedoraproject.org> - 1:1.2.25-5
- Rebuilt for new VDR API version 2.7.6

* Tue May 27 2025 Martin Gansser <martinkg@fedoraproject.org> - 1:1.2.25-4
- Rebuilt for new VDR API version 2.7.5

* Sun Mar 16 2025 Martin Gansser <martinkg@fedoraproject.org> - 1:1.2.25-3
- Rebuilt for new VDR API version 2.7.4

* Wed Jan 29 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1:1.2.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Nov 11 2024 Martin Gansser <martinkg@fedoraproject.org> - 1:1.2.25-1
- Update to 1:1.2.25

* Sun Nov 10 2024 Martin Gansser <martinkg@fedoraproject.org> - 1:1.2.24-1
- Update to 1:1.2.24

* Mon Oct 21 2024 Martin Gansser <martinkg@fedoraproject.org> - 1:1.2.23-2
- Rebuilt for new VDR API version 2.7.3

* Tue Oct 01 2024 Martin Gansser <martinkg@fedoraproject.org> - 1:1.2.23-1
- Update to 1:1.2.23
- Add epoch to allow upgrade to older release

* Fri Jul 26 2024 Martin Gansser <martinkg@fedoraproject.org> - 2.12-0.5.20240104git71b3e51
- Rebuilt for new VDR API version 2.6.9

* Sun Apr 21 2024 Martin Gansser <martinkg@fedoraproject.org> - 2.12-0.4.20240104git71b3e51
- Rebuilt for new VDR API version

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.12-0.3.20240104git71b3e51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 26 2024 Martin Gansser <martinkg@fedoraproject.org> - 2.12-0.2.20240104git71b3e51
- Rebuilt for new VDR API version

* Tue Jan 09 2024 Martin Gansser <martinkg@fedoraproject.org> - 2.12-0.1.20240104git71b3e51
- Rebuilt for new VDR API version
- Update to 2.12

* Sat Oct 14 2023 Martin Gansser <martinkg@fedoraproject.org> - 1.2.22-1
- Update to 1.2.22

* Wed Sep 06 2023 Martin Gansser <martinkg@fedoraproject.org> - 1.2.21-1
- Update to 1.2.21

* Sat Aug 19 2023 Martin Gansser <martinkg@fedoraproject.org> - 1.2.20-1
- Update to 1.2.20

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.2.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Dec 18 2022 Martin Gansser <martinkg@fedoraproject.org> - 1.2.19-3
- Rebuilt for new VDR API version

* Sat Dec 03 2022 Martin Gansser <martinkg@fedoraproject.org> - 1.2.19-2
- Rebuilt for new VDR API version

* Thu Nov 10 2022 Martin Gansser <martinkg@fedoraproject.org> - 1.2.19-1
- Update to 1.2.19
- Add missing algorithm include for std::min_element

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.2.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Aug 04 2022 Martin Gansser <martinkg@fedoraproject.org> - 1.2.18-3
- Update to new github address

* Mon Apr 11 2022 Sérgio Basto <sergio@serjux.com> - 1.2.18-2
- Rebuilt for VDR 2.6.1

* Fri Feb 11 2022 Martin Gansser <martinkg@fedoraproject.org> - 1.2.18-1
- Update to 1.2.18

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.2.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Feb 04 2022 Martin Gansser <martinkg@fedoraproject.org> - 1.2.17-4
- Rebuilt for new VDR API version

* Thu Dec 30 2021 Martin Gansser <martinkg@fedoraproject.org> - 1.2.17-3
- Rebuilt for new VDR API version

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 31 2021 Martin Gansser <martinkg@fedoraproject.org> - 1.2.17-1
- Update to 1.2.17

* Fri May 21 2021 Martin Gansser <martinkg@fedoraproject.org> - 1.2.16-1
- Update to 1.2.16

* Mon Apr 26 2021 Martin Gansser <martinkg@fedoraproject.org> - 1.2.15-2
- Rebuilt for new VDR API version

* Mon Mar 15 2021 Martin Gansser <martinkg@fedoraproject.org> - 1.2.15-1
- Update to 1.2.15

* Fri Mar 05 2021 Martin Gansser <martinkg@fedoraproject.org> - 1.2.14-1
- Update to 1.2.14

* Mon Feb 15 2021 Martin Gansser <martinkg@fedoraproject.org> - 1.2.13-1
- Update to 1.2.13

* Sun Feb 07 2021 Martin Gansser <martinkg@fedoraproject.org> - 1.2.12-1
- Update to 1.2.12

* Wed Feb 03 2021 Martin Gansser <martinkg@fedoraproject.org> - 1.2.11-1
- Update to 1.2.11

* Mon Jan 25 2021 Martin Gansser <martinkg@fedoraproject.org> - 1.2.10-1
- Update to 1.2.10

* Thu Jan 21 2021 Martin Gansser <martinkg@fedoraproject.org> - 1.2.9-1
- Update to 1.2.9

* Mon Jan 04 2021 Martin Gansser <martinkg@fedoraproject.org> - 1.2.8.6-3
- Rebuilt for new VDR API version

* Tue Dec 29 2020 Martin Gansser <martinkg@fedoraproject.org> - 1.2.8.6-2
- Move dtd and script files into base package
- Create softlink dtd files are expected in /etc/vdr/plugins/skindesigner
- Move themes into data package
- Move the two "builtin" skins into vdr-skindesigner-data
- fixes (rfbz#5881)

* Thu Dec 17 2020 Martin Gansser <martinkg@fedoraproject.org> - 1.2.8.6-1
- Update to 1.2.8.6

* Wed Oct 21 2020 Martin Gansser <martinkg@fedoraproject.org> - 1.2.8.5-2
- Rebuilt for new VDR API version

* Thu Sep 24 2020 Martin Gansser <martinkg@fedoraproject.org> - 1.2.8.5-1
- Update to 1.2.8.5

* Thu Aug 27 2020 Martin Gansser <martinkg@fedoraproject.org> - 1.2.8.4-3
- Rebuilt for new VDR API version

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Martin Gansser <martinkg@fedoraproject.org> - 1.2.8.4-1
- Update to 1.2.8.4

* Mon Feb 10 2020 Martin Gansser <martinkg@fedoraproject.org> - 1.2.8.2-1
- Update to 1.2.8.2

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 14 2019 Martin Gansser <martinkg@fedoraproject.org> - 1.2.8.1-1
- Update to 1.2.8.1

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 01 2019 Martin Gansser <martinkg@fedoraproject.org> - 1.2.8-3
- Rebuilt for new VDR API version 2.4.1

* Sun Jun 30 2019 Martin Gansser <martinkg@fedoraproject.org> - 1.2.8-2
- Rebuilt for new VDR API version

* Sat Jun 22 2019 Martin Gansser <martinkg@fedoraproject.org> - 1.2.8-1
- Update to 1.2.8
- Dropped skindesigner.diff.gz

* Tue Jun 18 2019 Martin Gansser <martinkg@fedoraproject.org> - 1.2.7-9
- Rebuilt for new VDR API version
- Add skindesigner.diff.gz to fix invalid lock sequence report

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 13 2018 Martin Gansser <martinkg@fedoraproject.org> - 1.2.7-7
- Create path where XML skins are installed by the Skindesigner Installer

* Tue Oct 30 2018 Martin Gansser <martinkg@fedoraproject.org> - 1.2.7-6
- Add dtd setup files

* Thu Oct 11 2018 Martin Gansser <martinkg@fedoraproject.org> - 1.2.7-5
- Add BR gcc-c++

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2.7-4
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 17 2018 Martin Gansser <martinkg@fedoraproject.org> - 1.2.7-2
- Rebuilt for vdr-2.4.0

* Mon Mar 05 2018 Martin Gansser <martinkg@fedoraproject.org> - 1.2.7-1
- Update to 1.2.7

* Fri Feb 23 2018 Martin Gansser <martinkg@fedoraproject.org> - 1.2.6-1
- Update to 1.2.6

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 03 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3

* Sat Sep 24 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2

* Sun Jul 31 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1

* Sat Jun 25 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.1.5-1
- Update to 1.1.5

* Fri Jun 24 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.1.4-1
- Update to 1.1.4

* Mon Jun 13 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3

* Mon May 30 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2

* Fri May 27 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0

* Sat May 14 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Mon May 02 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2

* Sun Apr 17 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0

* Thu Mar 31 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.9.5-1
- Update to 0.9.5

* Tue Mar 29 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.9.4-1
- Update to 0.9.4

* Wed Mar 23 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.9.3-1
- Update to 0.9.3

* Sun Mar 20 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.9.1-1
- Update to 0.9.1

* Mon Mar 14 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.9.0-1
- Update to 0.9.0

* Tue Mar 08 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.8-1
- Update to 0.8.8

* Sun Feb 28 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.7-1
- Update to 0.8.7

* Sun Feb 21 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.6-1
- Update to 0.8.6

* Sun Feb 14 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.5-1
- Update to 0.8.5

* Sat Feb 13 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.4-1
- Update to 0.8.4
- Corrected spelling-error

* Wed Feb 10 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.3-1
- Update to 0.8.3

* Sat Feb 06 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.2-1
- Update to 0.8.2

* Mon Feb 01 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.1-1
- Update to 0.8.1
- Cleanup

* Sun Jan 31 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.8.0-1
- Update to 0.8.0
- Added vdr-skindesigner-0.8.0-makefile.patch
- Added vdr-skindesigner-0.8.0-svdrp.patch

* Fri Aug 14 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.7.2-1
- Update to 0.7.2

* Fri Aug 14 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.7.1-1
- Update to 0.7.1

* Sun Aug 09 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.7.0-1
- Update to 0.7.0
- added Patch that fixed compiling for unpatched VDR

* Thu Jul 30 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.6.3-1
- Update to 0.6.3

* Sat Jul 18 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.6.2-1
- Update to 0.6.2

* Fri Jul 10 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.6.1-1
- Update to 0.6.1

* Mon Jun 15 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.5.3-1
- Update to 0.5.3

* Thu Jun 04 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.5.2-1
- Update to 0.5.2

* Mon Jun 01 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.5.1-1
- Update to 0.5.1

* Sat May 30 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.5.0-1
- Update to 0.5.0

* Fri May 22 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.4.8-1
- Update to 0.4.8

* Sat May 16 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.4.7-1
- Update to 0.4.7

* Thu May 14 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.4.6-1
- Update to 0.4.6

* Sun May 10 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.4.5-1
- Update to 0.4.5

* Fri May 01 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.4.4-1
- Update to 0.4.4

* Sun Apr 12 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.4.3-1
- Update to 0.4.3

* Wed Apr 08 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.4.2-2
- corrected /sbin/ldconfig calls in %%post and %%postun
- corrected unversioned libskindesignerapi.so.* name
- dropped Requires: pkgconfig from libskindesignerapi-devel
- dropped unversioned-explicit-provides libskindesignerapi.so.0
- corrected description for libskindesignerapi-devel package
- added Requires: libskindesignerapi%%{?_isa} = %%{version}-%%{release}

* Tue Apr 07 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.4.2-1
- Update to 0.4.2
- added libskindesignerapi subpackage

* Sat Mar 28 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.3.3-1
- Update to 0.3.3

* Fri Mar 20 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.3.2-1
- Update to 0.3.2

* Fri Mar 20 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.3.1-1
- Update to 0.3.1

* Fri Mar 13 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.3.0-1
- mark license files as %%license where available
- Update to 0.3.0

* Sat Jan 31 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.2.2-1
- Update to 0.2.2

* Tue Jan 27 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.2.1-1
- Update to 0.2.1

* Sun Jan 25 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0

* Thu Jan 22 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.1.6-1
- Update to 0.1.6

* Tue Jan 20 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.1.5-1
- Update to 0.1.5

* Sun Jan 18 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.1.4-1
- Update to 0.1.4

* Thu Jan 15 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.1.3-1
- Update to 0.1.3

* Tue Jan 06 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.1.2-1
- Update to 0.1.2

* Sat Dec 20 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.1.1-2
- rebuild

* Fri Dec 19 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.1.1-1
- Update to 0.1.1

* Sat Dec 06 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.1.0-1
- Update to 0.1.0

* Sun Nov 30 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.0.8-1
- Update to 0.0.8

* Mon Nov 24 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.0.6-2
- Rebuild
- removed BR GraphicsMagick-c++-devel

* Sat Nov 22 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.0.6-1
- Update to 0.0.6

* Sat Nov 15 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.0.5-4
- added BR libjpeg-turbo-devel

* Sat Nov 15 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.0.5-3
- added BR librsvg2-devel

* Sat Nov 15 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.0.5-2
- added BR cairo-devel

* Sat Nov 15 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.0.5-1
- Update to 0.0.5

* Sun Oct 26 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.0.3-1
- Update to 0.0.3

* Sat Oct 25 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.0.1-12.20141025gitee39eb8
- rebuild for new git release

* Sat Oct 25 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.0.1-11.20141023git69af1d5
- rebuild for new git release

* Mon Oct 20 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.0.1-10.20141020git1809656
- rebuild for new git release

* Sun Oct 19 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.0.1-9.20141019git49c6ef5
- rebuild for new git release

* Sun Oct 19 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.0.1-8.20141019git4d0e2e7
- rebuild for new git release

* Sat Oct 18 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.0.1-7.20141018git762115b
- rebuild for new git release

* Wed Oct 15 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.0.1-6.20141015git6b16f46
- rebuild for new git release

* Sat Oct 11 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.0.1-5.20141011git71aed6f
- rebuild for new git release

* Tue Oct 07 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.0.1-4.20141007giteebe8ac
- rebuild for new git release

* Sun Oct 05 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.0.1-3.20141004gite14982a
- make install preserve timestamps
- added main directory in section %%files data in order to own all its sub-directories and files.

* Sat Oct 04 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.0.1-2.20141004gite14982a
- rebuild for new git release

* Sat Oct 04 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.0.1-1.20141004gite688ad96
- Initial build

