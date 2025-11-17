#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg konversation
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	1.1
Release:	%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	User friendly Internet Relay Chat (IRC) client for TDE
Group:		Applications/Utilities
URL:		http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/internet/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires:	trinity-tde-cmake >= %{tde_version}
%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif
BuildRequires:	pkgconfig

# ACL support
BuildRequires:  pkgconfig(libacl)

# IDN support
BuildRequires:	pkgconfig(libidn)

# OPENSSL support
BuildRequires:  pkgconfig(openssl)

# PYTHON support
%global python python3
%global __python %__python3
%global python_sitearch %{python3_sitearch}
%{!?python_sitearch:%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
BuildRequires:	%{python}
BuildRequires:	%{python}-devel

# SUSE desktop files utility
%if 0%{?suse_version}
BuildRequires:	update-desktop-files
%endif

%if 0%{?opensuse_bs} && 0%{?suse_version}
# for xdg-menu script
BuildRequires:	brp-check-trinity
%endif

# XSLT support
BuildRequires:  pkgconfig(libxslt)

%if 0%{?suse_version}
BuildRequires:	docbook-xsl-stylesheets
%else
BuildRequires:	docbook-style-xsl
%endif

# LIBXI support
BuildRequires:  pkgconfig(xi)

BuildRequires:  pkgconfig(xrender)

# XSCREENSAVER support
#  RHEL 4: disabled
#  RHEL 5: available in centos-extras
#  RHEL 6: available in EPEL
#  RHEL 7: available in NUX
#  RHEL 8: available in EPEL
#  RHEL 9: available in EPEL
%if 0%{?fedora} || 0%{?mgaversion} || 0%{?mdkversion} || 0%{?rhel} >= 5 || 0%{?suse_version}
%define with_xscreensaver 1
BuildRequires:  pkgconfig(xscrnsaver)
%endif


%description
Konversation is a client for the Internet Relay Chat (IRC) protocol.
It is easy to use and well-suited for novice IRC users, but novice
and experienced users alike will appreciate its many features:

 * Standard IRC features
 * Easy to use graphical interface
 * Multiple server and channel tabs in a single window
 * IRC color support
 * Pattern-based message highlighting and OnScreen Display
 * Multiple identities for different servers
 * Multi-language scripting support (with DCOP)
 * Customizable command aliases
 * NickServ-aware log-on (for registered nicknames)
 * Smart logging
 * Traditional or enhanced-shell-style nick completion
 * DCC file transfer with resume support


##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########


%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 8 || 0%{?mgaversion} >= 8
%__sed -i "konversation/scripts/media" \
          "konversation/scripts/weather" \
  -e "s|/usr/bin/env python|/usr/bin/env %{python}|"
%endif


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DCMAKE_INSTALL_PREFIX="%{tde_prefix}" \
  -DSHARE_INSTALL_PREFIX="%{tde_datadir}" \
  -DLIB_INSTALL_DIR="%{tde_libdir}" \
  \
  -DWITH_ALL_OPTIONS=ON \
  -DWITH_GCC_VISIBILITY=ON \
  \
  -DBUILD_ALL=ON \
  -DBUILD_DOC=ON \
  -DBUILD_TRANSLATIONS=ON \
  ..

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__make install DESTDIR=%{buildroot} -C build

%find_lang %{tde_pkg}


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{tde_bindir}/konversation
%{tde_tdeappdir}/konversation.desktop
%{tde_datadir}/apps/tdeconf_update/konversation-0.19-appearance.pl
%{tde_datadir}/apps/tdeconf_update/konversation-0.19-colorcodes.pl
%{tde_datadir}/apps/tdeconf_update/konversation-0.19-colors.pl
%{tde_datadir}/apps/tdeconf_update/konversation-0.19-custombrowser.pl
%{tde_datadir}/apps/tdeconf_update/konversation-0.19-notifylists.pl
%{tde_datadir}/apps/tdeconf_update/konversation-0.19-sortorder.pl
%{tde_datadir}/apps/tdeconf_update/konversation-0.19-tabplacement.pl
%{tde_datadir}/apps/tdeconf_update/konversation-0.20-customfonts.pl
%{tde_datadir}/apps/tdeconf_update/konversation-0.20-quickbuttons.pl
%{tde_datadir}/apps/tdeconf_update/konversation.upd
%{tde_datadir}/apps/konversation/
%{tde_datadir}/config.kcfg/konversation.kcfg
%{tde_datadir}/services/konvirc.protocol
%{tde_datadir}/services/konvirc6.protocol
%{tde_tdedocdir}/HTML/*/konversation/
%{tde_datadir}/icons/crystalsvg/*/actions/tdeimproxyaway.png
%{tde_datadir}/icons/crystalsvg/*/actions/tdeimproxyoffline.png
%{tde_datadir}/icons/crystalsvg/*/actions/tdeimproxyonline.png
%{tde_datadir}/icons/crystalsvg/*/actions/char.png
%{tde_datadir}/icons/crystalsvg/*/actions/konv_message.png
%{tde_datadir}/icons/crystalsvg/scalable/actions/tdeimproxyaway.svgz
%{tde_datadir}/icons/crystalsvg/scalable/actions/tdeimproxyoffline.svgz
%{tde_datadir}/icons/crystalsvg/scalable/actions/tdeimproxyonline.svgz
%{tde_datadir}/icons/crystalsvg/scalable/actions/konv_message.svgz
%{tde_datadir}/icons/hicolor/*/apps/konversation.png
%{tde_datadir}/icons/hicolor/scalable/apps/konversation.svgz
%{tde_mandir}/man1/konversation.1*
%{tde_mandir}/man1/konversationircprotocolhandler.1*

