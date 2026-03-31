%bcond clang 1
%bcond xscreensaver 1

# TDE variables
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif

%define tde_pkg konversation
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Version:	1.1
Release:	%{?tde_version:%{tde_version}_}3
Summary:	User friendly Internet Relay Chat (IRC) client for TDE
Group:		Applications/Utilities
URL:		http://www.trinitydesktop.org/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/internet/%{tarball_name}-%{tde_version}.tar.xz

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DWITH_ALL_OPTIONS=ON -DBUILD_ALL=ON
BuildOption:    -DBUILD_DOC=ON -DBUILD_TRANSLATIONS=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}


BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires:	trinity-tde-cmake >= %{tde_version}

%{!?with_clang:BuildRequires:	gcc-c++}

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

# XSLT support
BuildRequires:  pkgconfig(libxslt)

BuildRequires:	docbook-style-xsl

# LIBXI support
BuildRequires:  pkgconfig(xi)

BuildRequires:  pkgconfig(xrender)

# XSCREENSAVER support
%{?with_xscreensaver:BuildRequires:  pkgconfig(xscrnsaver)}


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


%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"
export PKG_CONFIG_PATH="%{tde_prefix}/%{_lib}/pkgconfig"


%install -a
%find_lang %{tde_pkg}


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{tde_prefix}/bin/konversation
%{tde_prefix}/share/applications/tde/konversation.desktop
%{tde_prefix}/share/apps/tdeconf_update/konversation-0.19-appearance.pl
%{tde_prefix}/share/apps/tdeconf_update/konversation-0.19-colorcodes.pl
%{tde_prefix}/share/apps/tdeconf_update/konversation-0.19-colors.pl
%{tde_prefix}/share/apps/tdeconf_update/konversation-0.19-custombrowser.pl
%{tde_prefix}/share/apps/tdeconf_update/konversation-0.19-notifylists.pl
%{tde_prefix}/share/apps/tdeconf_update/konversation-0.19-sortorder.pl
%{tde_prefix}/share/apps/tdeconf_update/konversation-0.19-tabplacement.pl
%{tde_prefix}/share/apps/tdeconf_update/konversation-0.20-customfonts.pl
%{tde_prefix}/share/apps/tdeconf_update/konversation-0.20-quickbuttons.pl
%{tde_prefix}/share/apps/tdeconf_update/konversation.upd
%{tde_prefix}/share/apps/konversation/
%{tde_prefix}/share/config.kcfg/konversation.kcfg
%{tde_prefix}/share/services/konvirc.protocol
%{tde_prefix}/share/services/konvirc6.protocol
%{tde_prefix}/share/doc/tde/HTML/*/konversation/
%{tde_prefix}/share/icons/crystalsvg/*/actions/tdeimproxyaway.png
%{tde_prefix}/share/icons/crystalsvg/*/actions/tdeimproxyoffline.png
%{tde_prefix}/share/icons/crystalsvg/*/actions/tdeimproxyonline.png
%{tde_prefix}/share/icons/crystalsvg/*/actions/char.png
%{tde_prefix}/share/icons/crystalsvg/*/actions/konv_message.png
%{tde_prefix}/share/icons/crystalsvg/scalable/actions/tdeimproxyaway.svgz
%{tde_prefix}/share/icons/crystalsvg/scalable/actions/tdeimproxyoffline.svgz
%{tde_prefix}/share/icons/crystalsvg/scalable/actions/tdeimproxyonline.svgz
%{tde_prefix}/share/icons/crystalsvg/scalable/actions/konv_message.svgz
%{tde_prefix}/share/icons/hicolor/*/apps/konversation.png
%{tde_prefix}/share/icons/hicolor/scalable/apps/konversation.svgz
%{tde_prefix}/share/man/man1/konversation.1*
%{tde_prefix}/share/man/man1/konversationircprotocolhandler.1*

