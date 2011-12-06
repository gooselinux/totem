%define gstreamer_version 0.10.22
%define gstreamer_plugins_base_version 0.10.22.4
%define gstreamer_plugins_good_version 0.10.0
%define gstreamer_plugins_bad_version 0.10.17

Summary: Movie player for GNOME
Name: totem
Version: 2.28.6
Release: 2%{?dist}
License: GPLv2+ with exceptions
Group: Applications/Multimedia
URL: http://projects.gnome.org/totem/
Source0: http://download.gnome.org/sources/totem/2.28/totem-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(pre): GConf2 >= 2.14
Requires(preun): GConf2 >= 2.14
Requires(post): GConf2 >= 2.14
Requires(post): desktop-file-utils
Requires(post): scrollkeeper
Requires(postun): desktop-file-utils
Requires(postun): scrollkeeper

Requires: iso-codes
Requires: gnome-icon-theme
# For all the Python plugins
Requires: pygtk2

Requires: gstreamer >= %gstreamer_version
Requires: gstreamer-plugins-base >= %gstreamer_plugins_base_version
Requires: gstreamer-plugins-good >= %gstreamer_plugins_good_version
Requires: gstreamer-plugins-bad-free >= %gstreamer_plugins_bad_version
Requires: gvfs-fuse

BuildRequires: gstreamer-devel >= %gstreamer_version
BuildRequires: gstreamer-plugins-base-devel >= %gstreamer_plugins_base_version
BuildRequires: gstreamer-plugins-good >= %gstreamer_plugins_good_version
BuildRequires: liboil >= 0.3.13-5

BuildRequires: gcc-c++, pkgconfig, gettext
BuildRequires: perl(XML::Parser) intltool
BuildRequires: iso-codes-devel
BuildRequires: gnome-icon-theme
BuildRequires: libXtst-devel
BuildRequires: libXi-devel
BuildRequires: libXxf86vm-devel
BuildRequires: libXt-devel
BuildRequires: gnome-doc-utils
BuildRequires: python-devel pygtk2-devel
BuildRequires: totem-pl-parser-devel
BuildRequires: unique-devel
BuildRequires: GConf2-devel

# For the nautilus extension
BuildRequires: nautilus-devel

# Screensaver, mozilla and mmkeys plugin
BuildRequires: dbus-devel

# Work-around for fontconfig bug https://bugzilla.redhat.com/show_bug.cgi?id=480928
BuildRequires: liberation-sans-fonts

# For plugins
BuildRequires: libgdata-devel

Obsoletes: nautilus-media < 0.8.2
Provides: nautilus-media = %{version}-%{release}
Obsoletes: totem-gstreamer < 2.27.1
Provides: totem-gstreamer = %{version}-%{release}
Obsoletes: totem-xine < 2.27.1
Provides: totem-xine = %{version}-%{release}

# https://bugzilla.redhat.com/show_bug.cgi?id=564363
Patch0: add-fullscreen-button.patch

# update translations
# https://bugzilla.redhat.com/show_bug.cgi?id=588728
Patch1: totem-translations.patch

%description
Totem is simple movie player for the GNOME desktop. It features a
simple playlist, a full-screen mode, seek and volume controls, as well as
a pretty complete keyboard navigation.

Totem is extensible through a plugin system.

%package mozplugin
Summary: Mozilla plugin for Totem
Group: Applications/Internet

%description mozplugin
Totem is simple movie player for the GNOME desktop.
The mozilla plugin for Totem allows it to be embedded into a web browser.

%package youtube
Summary: YouTube plugin for Totem
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}

%description youtube
This package provides a plugin to allow browsing YouTube videos in Totem,
and watching them.

To play back the videos however, you will need codecs that are not
available in the Fedora repositories.

%package jamendo
Summary: Jamendo plugin for Totem
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}

%description jamendo
This package provides a plugin to allow browsing the Jamendo music store
in Totem, and listening to them.

%package upnp
Summary: UPNP/DLNA plugin for Totem
Group: Applications/Multimedia
Requires: python-Coherence
Requires: %{name} = %{version}-%{release}

%description upnp
This package provides a plugin to allow browsing UPNP/DLNA shares,
and watching videos from those.

%package devel
Summary: Plugin writer's documentation for totem
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains API documentation for
developing developing plugins for %{name}.

%package nautilus
Summary: Video and Audio Properties tab for Nautilus
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}
Provides: totem-nautilus-xine = %{version}-%{release}
Provides: totem-nautilus-gstreamer = %{version}-%{release}
Obsoletes: totem-nautilus-xine < 2.23.0
Obsoletes: totem-nautilus-gstreamer < 2.23.0

%description nautilus
This package provides a Nautilus extension that shows the properties of
audio and video files in the properties dialog.

%prep
%setup -q
%patch0 -p1 -b .fullscreen
%patch1 -p2 -b .translations

%build

# try to work around a problem where gst-inspect does
# not find playbin the first time around
DBUS_FATAL_WARNINGS=0 /usr/bin/gst-inspect-0.10 --print-all > /dev/null
export MOZILLA_PLUGINDIR=%{_libdir}/mozilla/plugins
%configure \
  --enable-gstreamer \
  --enable-mozilla \
  --enable-nautilus \
  --disable-scrollkeeper \
  --disable-nvtv \
  --disable-vala

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name} --with-gnome

rm -rf $RPM_BUILD_ROOT%{_libdir}/totem/plugins/*/*.{a,la} \
 $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins/*.{a,la} \
 $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-2.0/*.{a,la} \
 $RPM_BUILD_ROOT%{_libdir}/libbaconvideowidget*.{a,la} \
 $RPM_BUILD_ROOT%{_libdir}/libbaconvideowidget.so \
 $RPM_BUILD_ROOT%{_libdir}/totem/plugins/bemused/ \
 $RPM_BUILD_ROOT%{_libdir}/totem/plugins/gromit/ \
 $RPM_BUILD_ROOT%{_libdir}/totem/plugins/opensubtitles/ \
 $RPM_BUILD_ROOT%{_libdir}/totem/plugins/iplayer/

%find_lang %{name} --with-gnome

# save space by linking identical images in translated docs
helpdir=$RPM_BUILD_ROOT%{_datadir}/gnome/help/%{name}
for f in $helpdir/C/figures/*.png; do
  b="$(basename $f)"
  for d in $helpdir/*; do
    if [ -d "$d" -a "$d" != "$helpdir/C" ]; then
      g="$d/figures/$b"
      if [ -f "$g" ]; then
        if cmp -s $f $g; then
          rm "$g"; ln -s "../../C/figures/$b" "$g"
        fi
      fi
    fi
  done
done


%clean
rm -rf $RPM_BUILD_ROOT

%post
scrollkeeper-update -q
update-desktop-database -q
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
        %{_sysconfdir}/gconf/schemas/totem.schemas \
        %{_sysconfdir}/gconf/schemas/totem-handlers.schemas \
        %{_sysconfdir}/gconf/schemas/totem-video-thumbnail.schemas \
 >& /dev/null || :
touch %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  /usr/bin/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

%pre
if [ "$1" -gt 1 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
        %{_sysconfdir}/gconf/schemas/totem.schemas \
        %{_sysconfdir}/gconf/schemas/totem-handlers.schemas \
        %{_sysconfdir}/gconf/schemas/totem-video-thumbnail.schemas \
 >& /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
        %{_sysconfdir}/gconf/schemas/totem.schemas \
        %{_sysconfdir}/gconf/schemas/totem-handlers.schemas \
        %{_sysconfdir}/gconf/schemas/totem-video-thumbnail.schemas \
 >& /dev/null || :
fi

%postun
scrollkeeper-update -q
update-desktop-database -q
touch %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  /usr/bin/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README TODO
%config %{_sysconfdir}/gconf/schemas/totem.schemas
%config %{_sysconfdir}/gconf/schemas/totem-handlers.schemas
%config %{_sysconfdir}/gconf/schemas/totem-video-thumbnail.schemas
%{_bindir}/%{name}
%{_bindir}/%{name}-video-thumbnailer
%{_bindir}/%{name}-video-indexer
%{_bindir}/%{name}-audio-preview
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/
%dir %{_libexecdir}/totem
%{_libexecdir}/totem/totem-bugreport.py
%exclude %{_libexecdir}/totem/totem-bugreport.py[co]
%dir %{_libdir}/totem
%dir %{_libdir}/totem/plugins
%{_libdir}/totem/plugins/brasero-disc-recorder
%{_libdir}/totem/plugins/dbus
%{_libdir}/totem/plugins/ontop
%{_libdir}/totem/plugins/screensaver
%{_libdir}/totem/plugins/skipto
%{_libdir}/totem/plugins/properties
%{_libdir}/totem/plugins/media-player-keys
%{_libdir}/totem/plugins/totem
%{_libdir}/totem/plugins/thumbnail
%{_libdir}/totem/plugins/pythonconsole
%{_libdir}/totem/plugins/screenshot
#%{_libdir}/totem/plugins/bemused
%{_datadir}/icons/hicolor/*/apps/totem.png
%{_datadir}/icons/hicolor/*/devices/totem-tv.png
%{_datadir}/icons/hicolor/scalable/apps/totem.svg
%{_datadir}/icons/hicolor/scalable/devices/totem-tv.svg
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/totem-video-thumbnailer.1.gz

%files nautilus
%defattr(-, root, root)
%{_libdir}/nautilus/extensions-2.0/*.so*

%files youtube
%defattr(-, root, root)
%{_libdir}/totem/plugins/youtube

%files jamendo
%defattr(-, root, root)
%{_libdir}/totem/plugins/jamendo

%files upnp
%defattr(-, root, root)
%{_libdir}/totem/plugins/coherence_upnp

%files devel
%defattr(-, root, root)
%{_datadir}/gtk-doc/html/totem

%files mozplugin
%defattr(-, root, root)
%{_libdir}/mozilla/plugins/*
%{_libexecdir}/totem-plugin-viewer

%changelog
* Thu Jul 22 2010 Bastien Nocera <bnocera@redhat.com> 2.28.6-2
- Update translations
Resolves: #588728

* Tue Jun 01 2010 Bastien Nocera <bnocera@redhat.com> 2.28.6-1
- Rebase to 2.28.6
- Fix bugs from review
Related: rhbz#592301

* Wed May  5 2010 Matthias Clasen <mclasen@redhat.com> 2.28.5-6
- Update translations
Resolves: #588728

* Thu Feb 18 2010 Benjamin Otte <otte@redhat.com> 2.28.5-5
- Require gstreamer-plugins-bad-free, not gstreamer-plugins-bad
Related: rhbz#566450

* Wed Feb 17 2010 Bastien Nocera <bnocera@redhat.com> 2.28.5-4
- Add fullscreen button
Related: rhbz#564363

* Tue Feb 16 2010 Benjamin Otte <otte@redhat.com> 2.28.5-3
- Update gstreamer plugin dependencies
Related: rhbz#561913

* Tue Jan 12 2010 Bastien Nocera <bnocera@redhat.com> 2.28.5-2
- Remove python-gdata requirement for the Jamendo plugin
Related: rhbz#543948

* Tue Dec 22 2009 Bastien Nocera <bnocera@redhat.com> 2.28.5-1
- Update to 2.28.5
Related: rhbz#543948

* Thu Dec 17 2009 Bastien Nocera <bnocera@redhat.com> 2.28.3-2
- Remove plugins we don't want to ship
Related: rhbz#543948

* Thu Dec  3 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.28.3-1.1
- Don't build myth and lirc subpackages on RHEL

* Fri Nov 13 2009 Bastien Nocera <bnocera@redhat.com> 2.28.3-1
- Update to 2.28.3
- Fixes tag confusion in playlist (#536896)

* Tue Nov 03 2009 Bastien Nocera <bnocera@redhat.com> 2.28.2-2
- Fix YouTube URLs regexp again

* Mon Oct 26 2009 Bastien Nocera <bnocera@redhat.com> 2.28.2-1
- Update to 2.28.2

* Tue Oct 20 2009 Bastien Nocera <bnocera@redhat.com> 2.28.1-4
- Add missing dependency (#529845)

* Wed Oct 07 2009 Bastien Nocera <bnocera@redhat.com> 2.28.1-3
- Remove work-around for brasero bug

* Tue Oct  6 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.1-2
- Make video burning work again

* Tue Sep 29 2009 Bastien Nocera <bnocera@redhat.com> 2.28.1-1
- Update to 2.28.1

* Fri Sep 25 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-4
- More requires

* Fri Sep 25 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-3
- Add requires for iplayer plugin (#522068)

* Thu Sep 24 2009 Bastien Nocera <bnocera@redhat.com> 2.28.0-2
- Rebuild for new libgdata

* Mon Sep 21 2009 Bastien Nocera <bnocera@redhat.com> 2.28.0-1
- Update to 2.28.0

* Tue Sep 15 2009 Bill Nottingham <notting@redhat.com> 2.27.92-3
- youtube plugin is now in C, remove python requires

* Tue Sep 15 2009 Bastien Nocera <bnocera@redhat.com> 2.27.92-2
- Use PA to set the stream volume

* Tue Sep 08 2009 Bastien Nocera <bnocera@redhat.com> 2.27.92-1
- Update to 2.27.92

* Sat Aug 29 2009 Caolán McNamara <caolanm@redhat.com> - 2.27.2-8
- rebuilt with new openssl

* Thu Aug 27 2009 Tomas Mraz <tmraz@redhat.com> - 2.27.2-7
- rebuilt with new openssl

* Sat Aug 22 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.2-6
- Respect the button-images setting better

* Tue Aug 11 2009 Bastien Nocera <bnocera@redhat.com> 2.27.2-4
- Fix source URL

* Tue Aug 04 2009 Bastien Nocera <bnocera@redhat.com> 2.27.2-3
- Remove gnome-themes dependency, use gnome-icon-theme instead

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Bastien Nocera <bnocera@redhat.com> 2.27.2-1
- Update to 2.27.2

* Tue Jul 21 2009 Bastien Nocera <bnocera@redhat.com> 2.27.1-3
- Rebuild for new libgdata

* Mon Jun 08 2009 Bastien Nocera <bnocera@redhat.com> 2.27.1-2
- Rebuild against newer libgdata

* Wed May 06 2009 Bastien Nocera <bnocera@redhat.com> 2.27.1-1
- Update to 2.27.1
- Remove xine-lib backend

* Tue Apr 28 2009 Bastien Nocera <bnocera@redhat.com> 2.26.1-3
- Add missing pyxdg requires for the OpenSubtitles plugin (#497787)

* Thu Apr 23 2009 Bastien Nocera <bnocera@redhat.com> 2.26.1-4
- Add missing gnome-python2-gconf req (#483265)

* Thu Apr 02 2009 - Bastien Nocera <bnocera@redhat.com> - 2.26.1-2
- Update patch to set the PA stream volume, avoids setting the 
  volume when pulsesink isn't in a state where it has a stream
  (#488532)

* Wed Apr 01 2009 - Bastien Nocera <bnocera@redhat.com> - 2.26.1-1
- Update to 2.26.1

* Mon Mar 16 2009 - Bastien Nocera <bnocera@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Tue Mar 03 2009 - Bastien Nocera <bnocera@redhat.com> -2.25.92-1
- Update to 2.25.92

* Thu Feb 26 2009 - Bastien Nocera <bnocera@redhat.com> - 2.25.91-4
- Kill galago plugin

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 - Bastien Nocera <bnocera@redhat.com> - 2.25.91-2
- Add patch to set the PulseAudio application role

* Tue Feb 17 2009 - Bastien Nocera <bnocera@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Thu Feb 12 2009 - Bastien Nocera <bnocera@redhat.com> - 2.25.90-3
- Add patch to set the PA stream volume from Totem, instead
  of having a separate one

* Wed Feb 04 2009 - Peter Robinson <pbrobinson@gmail.com> - 2.25.90-2
- Fix logic in spec file for xine disable

* Tue Feb 03 2009 - Bastien Nocera <bnocera@redhat.com> - 2.25.90-1
- Update to 2.25.90
- Add separate UPNP plugin package

* Wed Jan 28 2009 - Bastien Nocera <bnocera@redhat.com> - 2.25.3-9
- Remove gnome-desktop requires, it's not needed

* Fri Jan 23 2009 - Bastien Nocera <bnocera@redhat.com> - 2.25.3-8
- Rebuild for new MySQL libraries

* Fri Jan 16 2009  Matthias Clasen <mclasen@redhat.com> - 2.25.3-7
- Own /usr/lib/totem

* Mon Jan 05 2009 - Bastien Nocera <bnocera@redhat.com> - 2.25.3-6
- Remove compiled bits for the bug report scripts (#478889)

* Wed Dec 17 2008 - Bastien Nocera <bnocera@redhat.com> - 2.25.3-5
- Whatever

* Wed Dec 17 2008 - Bastien Nocera <bnocera@redhat.com> - 2.25.3-4
- Add totem-tv icons, and jamendo plugin

* Wed Dec 17 2008 - Bastien Nocera <bnocera@redhat.com> - 2.25.3-3
- Add missing, but temporary, startup-notification BR

* Wed Dec 17 2008 - Bastien Nocera <bnocera@redhat.com> - 2.25.3-2
- Disable tracker plugin until tracker is fixed

* Mon Dec 15 2008 - Bastien Nocera <bnocera@redhat.com> - 2.25.3-1
- Update to 2.25.3

* Wed Dec 10 2008 - Bastien Nocera <bnocera@redhat.com> - 2.24.3-4
- Remove hal, glade, gnome-desktop and control-center BRs, not needed anymore

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.24.3-3
- Rebuild for Python 2.6

* Sat Nov 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.3-2
- Tweak %%descriptions

* Sun Oct 26 2008 - Bastien Nocera <bnocera@redhat.com> - 2.24.3-1
- Update to 2.24.3
- Fixes for recent YouTube website changes (#468578)

* Fri Oct 24 2008 Brian Pepple <bpepple@fedoraproject.org> - 2.24.2-3
- rebuild for new libepc.

* Thu Oct  9 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.2-2
- Save some space

* Tue Oct 07 2008 - Bastien Nocera <bnocera@redhat.com> - 2.24.2-1
- Update to 2.24.2

* Wed Oct 01 2008 - Bastien Nocera <bnocera@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Sun Sep 21 2008 - Bastien Nocera <bnocera@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Mon Sep  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.23.91-3
- fix license tag

* Mon Sep 01 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.91-2
- Remove unneeded scrollkeeper BR (#460344)

* Fri Aug 29 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Wed Jun 11 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.4-1
- Update to 2.23.4
- Remove gnome-vfs BRs
- Remove xulrunner patches and requires, we don't need them anymore

* Sat May 17 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.3-2
- Rebuild

* Wed May 14 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.3-1
- Update to 2.23.3

* Tue May 13 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.2-4
- Rebuild

* Wed May 07 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.2-3
- Require gstreamer-plugins-flumpegdemux as used by the DVB and DVD
  playback bits

* Mon Apr 21 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.2-1
- Update to 2.23.2
- Fix scriptlets removing the alternatives on upgrade (#442895)

* Tue Apr 08 2008 Stewart Adam <s.adam@diffingo.com> - 2.23.1-2
- Fix error when only a single backend has been installed (#439634)

* Tue Apr 08 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.1-1
- Update to 2.23.1

* Wed Mar 19 2008 Stewart Adam <s.adam@diffingo.com> - 2.23.0-6
- Use alternatives to switch the backend
- Update totem-backend script accordingly
- Remove ldconfig from %%postun, do that in individual the backends instead
- Do not restore a default backend, ldconfig in backends does this
- Fix Source0 URL

* Mon Mar 17 2008 Jesse Keating <jkeating@redhat.com> - 2.23.0-5
- Fix some Provides to prevent cross arch obsoletions.

* Mon Mar 10 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.0-4
- Try to build with a liboil with Altivec disabled

* Sun Mar 09 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.0-3
- Remove PPC/PPC64 ExcludeArch

* Fri Mar 07 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.0-2
- Re-add missing nautilus files section
- Fix obsoletes and provides to upgrade from the broken 2.21.96
  packages

* Tue Mar 04 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.0-1
- Update to 2.23.0, rework the -gstreamer/-xine backend split to
  switch libraries instead of having replacements for all the
  binaries

* Mon Mar 03 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.96-1
- Update to 2.21.96
- Add ppc and ppc64 to ExcludeArch as liboil is crashing on us (#435771)
- Add big patch from Stewart Adam <s.adam@diffingo.com> to allow
  switching between the GStreamer and the xine-lib backends at
  run-time, see #327211 for details

* Tue Feb 26 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.95-1
- Update to 2.21.95

* Sun Feb 24 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.94-1
- Update to 2.21.94

* Sun Feb 17 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.93-2
- Rebuild for dependencies

* Tue Feb 12 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.93-1
- Update to 2.21.93

* Tue Feb 05 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.92-2
- Remove unnecessary patch to the GMP plugin

* Mon Feb 04 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.92-1
- Update to 2.21.92

* Fri Jan 25 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.91-1
- Update to 2.21.91
- Split out the nautilus extension (#427832)
- Remove .a and .la files (#430328)

* Fri Jan 18 2008  Matthias Clasen <mclasen@redhat.com> - 2.21.90-2
- Add content-type support

* Mon Jan 07 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.90-1
- Update to 2.21.90
- Add patch to allow building against xulrunner

* Mon Dec 10 2007 - Bastien Nocera <bnocera@redhat.com> - 2.21.5-4
- Add the (non-working yet, missing files in the tarball) publish plugin

* Mon Dec 10 2007 - Bastien Nocera <bnocera@redhat.com> - 2.21.5-3
- Add the mythtv schemas to the mythtv subpackage (#410451)

* Sun Dec  9 2007  Matthias Clasen  <mclasen@redhat.com> - 2.21.5-2
- Make it build

* Sun Dec 09 2007 - Bastien Nocera <bnocera@redhat.com> - 2.21.5-1
- Update to 2.21.5
- Remove -devel and -plparser subpackages, they're in totem-pl-parser now

* Thu Dec 06 2007 - Bastien Nocera <bnocera@redhat.com> - 2.21.3-3
- The mozilla plugin only need gecko-libs, not devel
  Thanks to Jeremy Katz for noticing

* Thu Dec 06 2007 Release Engineering <rel-eng at fedoraproject dot org> - 2.21.3-2
- Rebuild for deps

* Mon Dec 03 2007 - Bastien Nocera <bnocera@redhat.com> - 2.21.3-1
- Update to 2.21.3
- Add tracker video search sub-package

* Wed Nov 21 2007 - Bastien Nocera <bnocera@redhat.com> - 2.21.2-2
- Try to build against xulrunner

* Mon Nov 12 2007 - Bastien Nocera <bnocera@redhat.com> - 2.21.2-1
- Update to 2.21.2

* Wed Oct 31 2007 - Bastien Nocera <bnocera@redhat.com> - 2.21.1-1
- Update to 2.21.1

* Wed Oct 24 2007 - Bastien Nocera <bnocera@redhat.com> - 2.21.0-3
- Add python BRs so we have Python support for the YouTube plugin

* Mon Oct 22 2007  Matthias Clasen <mclasen@redhat.com> - 2.21.0-2
- Rebuild against new dbus-glib

* Sun Oct 21 2007 - Bastien Nocera <bnocera@redhat.com> - 2.21.0-1
- Update to 2.21.0

* Wed Oct 17 2007 - Bastien Nocera <bnocera@redhat.com> - 2.20.1-1
- Update to 2.20.1
- Require GTK+ 2.12.1

* Sun Sep 16 2007 - Bastien Nocera <bnocera@redhat.com> - 2.20.0-1
- Update for 2.20.0

* Fri Aug 17 2007 - Bastien Nocera <bnocera@redhat.com> - 2.19.90-1
- Update for 2.19.90

* Wed Aug 15 2007 - Bastien Nocera <bnocera@redhat.com> - 2.19.6-5
- Up the gstreamer-plugins-base requirements so we get a newer liboil
  and PPC(64) builds work again (#252179)

* Tue Aug 14 2007 - Bastien Nocera <bnocera@redhat.com> - 2.19.6-4
- Disable ppc and ppc64 to work around a liboil bug (#252179)

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-3
- Update license fields
- Use %%find_lang for help files

* Sat Aug 04 2007 - Bastien Nocera <bnocera@redhat.com> - 2.19.6-2
- Don't package the bemused plugin, it's not ready yet

* Mon Jul 30 2007 - Bastien Nocera <bnocera@redhat.com> - 2.19.6-1
- Update to 2.19.6
- Fix location of the browser plugins
- Avoid gst-inspect failing stopping the build

* Mon Jun 04 2007 - Bastien Nocera <bnocera@redhat.com> - 2.19.4-2.1
- Another rebuild with the liboil fixes

* Mon Jun 04 2007 - Bastien Nocera <bnocera@redhat.com> - 2.19.4-2
- Update to 2.19.4

* Mon May 21 2007 - Bastien Nocera <bnocera@redhat.com> - 2.19.3-2
- Don't forget the media-player-keys plugin

* Mon May 21 2007 - Bastien Nocera <bnocera@redhat.com> - 2.19.3-1
- Update to 2.19.3, fix build

* Mon May 21 2007 - Bastien Nocera <bnocera@redhat.com> - 2.19.2-3
- Fix unclosed curly brace

* Fri May 21 2007 - Bastien Nocera <bnocera@redhat.com> - 2.19.2-2
- Add lirc, and galago sub-packages

* Sun May 20 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.2-1
- Update to 2.19.2

* Mon Apr 23 2007 - Bastien Nocera <bnocera@redhat.com> - 2.18.2-3
- Add missing control-center-devel BuildRequires, to use the new
  playback key infrastructure in gnome-settings-daemon (#237484)

* Wed Apr 11 2007 - Bastien Nocera <bnocera@redhat.com> - 2.18.1-2
- Add requires for gnome-themes, spotted by Nigel Jones (#235819)

* Wed Apr 04 2007 - Bastien Nocera <bnocera@redhat.com> - 2.18.1-1
- New upstream version with plenty of bug fixes

* Fri Mar 09 2007 - Bastien Nocera <bnocera@redhat.com> - 2.18.0-1
- Update to 2.18.0
- Update GStreamer base plugins requirements to get some "codec-buddy"
  support

* Wed Feb 21 2007 - Bastien Nocera <bnocera@redhat.com> - 2.17.92-2
- Add gstreamer-plugins-good as a builddep so that gconfaudiosink
  can be found during configure

* Wed Feb 21 2007 - Bastien Nocera <bnocera@redhat.com> - 2.17.92-1
- Update to 2.17.92

* Thu Feb 08 2007 - Bastien Nocera <bnocera@redhat.com> - 2.17.91-1
- Update to 2.17.91
- Resolves: #227661

* Mon Jan 29 2007 - Bastien Nocera <bnocera@redhat.com> - 2.17.90-1
- Make the -devel package own $includedir/totem and below
- Resolves: #212093
- Update homepage, and download URLs
- Update to 2.17.90, remove obsolete patch

* Tue Jan 16 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.5-1
- Update to 2.17.5

* Mon Nov 20 2006 Alexander Larsson <alexl@redhat.com> - 2.17.3-2
- Remove libtotem-plparser.so from totem package
- Split out totem-plparser into subpackage
- Resolves: #203640

* Wed Nov 15 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.3-1
- Update to 2.17.3
 
* Sat Nov  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.2-1 
- Update to 2.17.2

* Sun Oct 22 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.1-1 
- Update to 2.17.1

* Sat Oct 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.0-1
- Update to 2.17.0

* Wed Oct 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.1-2
- Fix scripts to follow packaging guidelines

* Thu Sep  7 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.1-1.fc6
- Update to 2.16.1, including several improvements to 
  the mozilla plugin

* Sun Sep  3 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1.fc6
- Update to 2.16.0

* Tue Aug 22 2006 Matthias Clasen <mclasen@redhat.com> - 1.5.92-1.fc6
- Update to 1.5.92
- Require pkgconfig in the -devel package

* Mon Aug 14 2006 Matthias Clasen <mclasen@redhat.com> - 1.5.91-2.fc6
- Make translations work again

* Sun Aug 13 2006 Matthias Clasen <mclasen@redhat.com> - 1.5.91-1.fc6
- Update to 1.5.91

* Thu Aug  3 2006 Matthias Clasen <mclasen@redhat.com> - 1.5.90-1.fc6
- Update to 1.5.90

* Mon Jul 31 2006 Matthias Clasen <mclasen@redhat.com> - 1.5.4-4
- Rebuild against firefox-devel

* Wed Jul 19 2006 Matthias Clasen <mclasen@redhat.com> - 1.5.4-3
- Don't use deprecated dbus api

* Wed Jul 19 2006 Matthias Clasen <mclasen@redhat.com> - 1.5.4-2
- Rebuild against dbus

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 1.5.4-1
- Update to 1.5.4

* Wed Jun 14 2006 Matthias Clasen <mclasen@redhat.com> - 1.5.2-2
- Work around a gstreamer problem

* Tue Jun 13 2006 Matthias Clasen <mclasen@redhat.com> - 1.5.2-1
- Update to 1.5.2
- BuildRequire hal
- Update icon themes

* Wed May 17 2006 Matthias Clasen <mclasen@redhat.com> - 1.5.1-1
- Update to 1.5.1

* Wed Apr 19 2006 Matthias Clasen <mclasen@redhat.com> - 1.4.0-3
- Add missing BuildRequires (#181304)

* Tue Mar 14 2006 Ray Strode <rstrode@redhat.com> - 1.4.0-2
- Update to 1.4.0

* Mon Mar 13 2006 Matthias Clasen <mclasen@redhat.com> - 1.4.0-1
- Update to 1.4.0

* Tue Feb 28 2006 Matthias Clasen <mclasen@redhat.com> - 1.3.92-1
- Update to 1.3.92

* Mon Feb 13 2006 Matthias Clasen <mclasen@redhat.com> - 1.3.91-1
- Update to 1.3.91

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.3.90-2.1
- bump again for double-long bug on ppc(64)

* Thu Feb  9 2006 Matthias Clasen <mclasen@redhat.com> - 1.3.90-2
- Rebuild

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.3.90-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 30 2006 Matthias Clasen <mclasen@redhat.com> - 1.3.90-1
- Update to 1.3.90

* Fri Jan 20 2006 Matthias Clasen <mclasen@redhat.com> - 1.3.1-1
- Update to 1.3.1

* Fri Jan 06 2006 John (J5) Palmieri <johnp@redhat.com> 1.3.0-3
- Build with gstreamer 0.10
- Enable the mozilla plugin

* Thu Jan 05 2006 John (J5) Palmieri <johnp@redhat.com> 1.3.0-2
- GStreamer has been split into gstreamer08 and gstreamer (0.10) packages
  we need gstreamer08 for now

* Thu Dec 20 2005 Matthias Clasen <mclasen@redhat.com> 1.3.0-1
- Update to 1.3.0

* Thu Dec 15 2005 Matthias Clasen <mclasen@redhat.com> 1.2.1-1
- Update to 1.2.1

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Oct 26 2005 John (J5) Palmieri <johnp@redhat.com> - 1.2.0-1
- Update to 1.2.0

* Tue Oct 25 2005 Matthias Clasen <mclasen@redhat.com> - 1.1.5-1
- Update to 1.1.5

* Tue Aug 18 2005 John (J5) Palmieri <johnp@redhat.com> - 1.1.4-1
- Update to upstream version 1.1.4 and rebuild
- Don't build with nautilus-cd-burner on s390 platforms

* Fri Jul 22 2005 Colin Walters <walters@redhat.com> - 1.1.3-1
- Update to upstream version 1.1.2

* Wed Jun 29 2005 John (J5) Palmieri <johnp@redhat.com> - 1.1.2-1
- Update to upstream version 1.1.2

* Tue May 17 2005 John (J5) Palmieri <johnp@redhat.com> - 1.0.2-1
- Update to upstream version 1.0.2 to fix minor bugs
- Register the thumbnail and handlers schemas

* Tue Feb 29 2005 John (J5) Palmieri <johnp@redhat.com> - 1.0.1-1
- Update to upstream version 1.0.1
- Break out devel package

* Mon Feb 21 2005 Bill Nottingham <notting@redhat.com> - 0.101-4
- fix %%post

* Wed Feb  2 2005 Matthias Clasen <mclasen@redhat.com> - 0.101-3
- Obsolete nautilus-media
- Install property page and thumbnailer

* Wed Feb  2 2005 Matthias Clasen <mclasen@redhat.com> - 0.101-2
- Update to 0.101
 
* Mon Jan 03 2005 Colin Walters <walters@redhat.com> - 0.100-2
- Grab patch totem-0.100-desktopfile.patch from CVS to fix
  missing menu entry (144088)
- Remove workaround for desktop file being misinstalled, fixed
  by above patch

* Mon Jan 03 2005 Colin Walters <walters@redhat.com> - 0.100-1
- New upstream version 0.100

* Sun Dec  5 2004 Bill Nottingham <notting@redhat.com> - 0.99.22-1
- update to 0.99.22

* Thu Oct 28 2004 Colin Walters <walters@redhat.com> - 0.99.19-2
- Add patch to remove removed items from package from help

* Thu Oct 14 2004 Colin Walters <walters@redhat.com> - 0.99.19-1
- New upstream 0.99.19
  - Fixes crasher with CD playback (see NEWS)

* Tue Oct 12 2004 Alexander Larsson <alexl@redhat.com> - 0.99.18-2
- Call update-desktop-database in post

* Tue Oct 12 2004 Alexander Larsson <alexl@redhat.com> - 0.99.18-1
- update to 0.99.18

* Wed Oct  6 2004 Alexander Larsson <alexl@redhat.com> - 
- Initial version, based on specfile by Matthias Saou <http://freshrpms.net/>

