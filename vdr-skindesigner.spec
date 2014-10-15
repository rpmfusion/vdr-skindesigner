%global commit  6b16f46272ad44d9fbf737ed43e696b95e972f34
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitdate 20141015

Name:           vdr-skindesigner
Version:        0.0.1
Release:        6.%{gitdate}git%{shortcommit}%{?dist}
Summary:        A VDR skinning engine that displays XML based Skins

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://projects.vdr-developer.org/projects/plg-skindesigner
Source0:        http://projects.vdr-developer.org/git/vdr-plugin-skindesigner.git/snapshot/vdr-plugin-skindesigner-%{commit}.tar.bz2
# Configuration files for plugin parameters. These are Fedora specific and not in upstream.
Source1:        %{name}.conf

BuildRequires:  vdr-devel >= 2.0.0
BuildRequires:  gettext
BuildRequires:  libcurl-devel
BuildRequires:  libxml2-devel
BuildRequires:  freetype-devel
BuildRequires:  fontconfig-devel
BuildRequires:  GraphicsMagick-c++-devel
Requires:       vdr(abi)%{?_isa} = %{vdr_apiversion}
Requires:       vdr-softhddevice
Requires:       vdr-epgsearch

%description
SkinDesigner is a powerfull tool to create VDR Skins based on Skindesigner
specific XML Code. The following documentation shows the SkinDesigner
"internals" so that new Skinners get easily an overview how Skindesigner works.
Hopefully all your open questions are answerd, if not, feel free to ask in
VDR Portal.

%package data
Summary:       Icons xml files for %{name}
Group:         Applications/Multimedia
BuildArch:     noarch
Requires:      %{name} = %{version}-%{release}

%description data
This package contains icons and xml files.

%prep
%setup -q -n vdr-plugin-skindesigner-%{commit}

%build
make CFLAGS="%{optflags} -fPIC" CXXFLAGS="%{optflags} -fPIC" IMAGELIB=graphicsmagick %{?_smp_mflags} all

%install
# make install would install the themes under /etc, let's not use that
make install-lib install-i18n DESTDIR=%{buildroot} INSTALL="install -p"
# install the themes to the custom location used in Fedora
install -dm 755 %{buildroot}%{vdr_vardir}/themes
install -pm 644 themes/*.theme %{buildroot}%{vdr_vardir}/themes/

install -dm 755 %{buildroot}%{vdr_resdir}/plugins/skindesigner/skins
cp -pR skins/* %{buildroot}%{vdr_resdir}/plugins/skindesigner/skins

# tvguide.conf
install -Dpm 644 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/sysconfig/vdr-plugins.d/skindesigner.conf


%find_lang %{name}

%files -f %{name}.lang
%doc COPYING HISTORY README
%config(noreplace) %{_sysconfdir}/sysconfig/vdr-plugins.d/skindesigner.conf
%{vdr_plugindir}/libvdr-*.so.%{vdr_apiversion}
%{vdr_vardir}/themes/nopacity-*.theme

%files data
%{vdr_resdir}/plugins/skindesigner/


%changelog
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

