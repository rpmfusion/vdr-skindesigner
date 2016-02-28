Name:           vdr-skindesigner
Version:        0.8.7
Release:        1%{?dist}
Summary:        A VDR skinning engine that displays XML based Skins

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://projects.vdr-developer.org/projects/plg-skindesigner
Source0:        http://projects.vdr-developer.org/git/vdr-plugin-skindesigner.git/snapshot/vdr-plugin-skindesigner-%{version}.tar.bz2
# Configuration files for plugin parameters. These are Fedora specific and not in upstream.
Source1:        %{name}.conf

BuildRequires:  vdr-devel >= 2.0.0
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
Requires:      %{name} = %{version}-%{release}

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
Requires:       libskindesignerapi%{?_isa} = %{version}-%{release}
Requires:       vdr-devel >= 2.0.0

%description -n libskindesignerapi-devel
Development files for libskindesignerapi.

%prep
%setup -q -n vdr-plugin-skindesigner-%{version}

sed -i -e 's|PREFIX ?= /usr/local|PREFIX ?= /usr|g' libskindesignerapi/Makefile
sed -i -e 's|LIBDIR ?= $(PREFIX)/lib|LIBDIR ?= %{_libdir}/|g' libskindesignerapi/Makefile
sed -i -e 's|PCDIR  ?= $(PREFIX)/lib/pkgconfig|PCDIR  ?= %{_libdir}/pkgconfig|g' libskindesignerapi/Makefile

# changed permission due rpmlint warning E: non-executable-script
chmod a+x scripts/{temperatures.g2v,vdrstats.default}

%build
make CFLAGS="%{optflags} -fPIC" CXXFLAGS="%{optflags} -fPIC" %{?_smp_mflags} all

%install
# make install would install the themes under /etc, let's not use that
make install-subprojects install-lib install-i18n DESTDIR=%{buildroot} INSTALL="install -p"
# install the themes to the custom location used in Fedora
install -dm 755 %{buildroot}%{vdr_vardir}/themes
install -pm 644 themes/*.theme %{buildroot}%{vdr_vardir}/themes/
# install the skins to the custom location used in Fedora
install -dm 755 %{buildroot}%{vdr_resdir}/plugins/skindesigner/skins
cp -pR skins/* %{buildroot}%{vdr_resdir}/plugins/skindesigner/skins
# install the scripts to the custom location used in Fedora
install -dm 755 %{buildroot}%{vdr_resdir}/plugins/skindesigner/scripts
cp -pR scripts/* %{buildroot}%{vdr_resdir}/plugins/skindesigner/scripts

# skindesigner.conf
install -Dpm 644 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/sysconfig/vdr-plugins.d/skindesigner.conf

# install missing symlink (was giving no-ldconfig-symlink rpmlint errors)
ldconfig -n %{buildroot}%{_libdir}

%find_lang %{name}

%post -n libskindesignerapi -p /sbin/ldconfig

%postun -n libskindesignerapi -p /sbin/ldconfig

%files -f %{name}.lang
%doc HISTORY README
%license COPYING
%config(noreplace) %{_sysconfdir}/sysconfig/vdr-plugins.d/skindesigner.conf
%{vdr_plugindir}/libvdr-*.so.%{vdr_apiversion}
%{vdr_vardir}/themes/*.theme

%files data
%{vdr_resdir}/plugins/skindesigner/

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

