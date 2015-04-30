# Maintainers:  keep this list of plugins up to date
# List plugins in %%{_libdir}/freecad/lib, less '.so' and 'Gui.so', here
%global plugins Assembly Complete Drawing Fem FreeCAD Image Import Inspection Mesh MeshPart Part Points QtUnit Raytracing ReverseEngineering Robot Sketcher Start Web PartDesignGui _PartDesign

# Some plugins go in the Mod folder instead of lib. Deal with those here:
%global mod_plugins Mod/PartDesign

# This revision is 0.13 final.
%global rev 3702

# Temporary workaround for cmake/boost bug:
# http://public.kitware.com/Bug/view.php?id=13446
%if 0%{?rhel} && 0%{?rhel} <= 6
%global cmake %cmake -DBoost_NO_BOOST_CMAKE=ON
%endif

# Some configuration options for other environments
# rpmbuild --with=occ:  Compile using OpenCASCADE instead of OCE
%global occ %{?_with_occ:1} %{?!_with_occ: 0}
# rpmbuild --with=bundled_zipios:  use bundled version of zipios++
%global bundled_zipios %{?_with_bundled_zipios:1} %{?!_with_bundled_zipios: 0}
# rpmbuild --with=bundled_pycxx:  use bundled version of pycxx
%global bundled_pycxx %{?_with_bundled_pycxx:1} %{?!_with_bundled_pycxx: 0}
# rpmbuild --with=bundled_smesh:  use bundled version of Salome's Mesh
%global bundled_smesh %{?_with_bundled_smesh:1} %{?!_with_bundled_smesh: 0}


Summary:	A general purpose 3D CAD modeler
Name:		freecad
Version:	0.14
Release:	0.1
Group:		Applications/Engineering

License:	GPL v2+
URL:		http://sourceforge.net/apps/mediawiki/free-cad/
Source0:	http://downloads.sourceforge.net/free-cad/%{name}-%{version}.%{rev}.tar.gz
# Source0-md5:	234747bdff47a62fd10cb902f3dd772b
Source101:	%{name}.desktop
Source102:	%{name}.1
Source103:	%{name}.appdata.xml
Source104:	%{name}.sharedmimeinfo

Patch0:		%{name}-3rdParty.patch
Patch1:		%{name}-0.14-Xlib_h.patch
Patch2:		%{name}-0.14-smesh.patch
# http://www.freecadweb.org/tracker/view.php?id=1757
Patch3:		%{name}-0.14-DraftSnap.patch
#Patch4: %{name}-0.14-disable_auto_dxf_dl.patch


# Utilities
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	dos2unix
BuildRequires:	doxygen
BuildRequires:	gcc-gfortran
BuildRequires:	gettext
BuildRequires:	graphviz
BuildRequires:	swig
%ifnarch ppc64
BuildRequires:	tbb-devel
%endif
# Development Libraries
BuildRequires:	freeimage-devel
BuildRequires:	mesa-libGLU-devel
BuildRequires:	xorg-lib-libXmu-devel
%if %{occ}
BuildRequires:	OpenCASCADE-devel
%else
BuildRequires:	OCE-devel
%endif
# Not yet in Fedora
# https://bugzilla.redhat.com/show_bug.cgi?id=665733
BuildRequires:	Coin2-devel
#BuildRequires:  Coin3-devel
BuildRequires:	SoQt-devel
BuildRequires:	boost-devel
BuildRequires:	eigen3-devel
BuildRequires:	python-devel
BuildRequires:	qt-devel
BuildRequires:	qt-webkit-devel
# Not used yet.
BuildRequires:	libspnav-devel
#BuildRequires:  ode-devel
#BuildRequires:  opencv-devel
BuildRequires:	python-pyside-devel
BuildRequires:	shiboken-devel
BuildRequires:	xerces-c
BuildRequires:	xerces-c-devel
%if ! %{bundled_smesh}
BuildRequires:	smesh-devel
%endif
BuildRequires:	netgen-mesher-devel
%if ! %{bundled_zipios}
BuildRequires:	zipios++-devel
%endif
%if ! %{bundled_pycxx}
BuildRequires:	python-pycxx-devel
%endif
BuildRequires:	libicu-devel
BuildRequires:	python-matplotlib

# For appdata
%if 0%{?fedora}
BuildRequires:	libappstream-glib
%endif

# Packages separated because they are noarch, but not optional so require them
# here.
Requires:	%{name}-data = %{version}-%{release}
# Obsolete old doc package since it's required for functionality.
Obsoletes:	freecad-doc < 0.13-5

# Needed for plugin support and is not a soname dependency.
%if ! 0%{?rhel} <= 6 && "%{_arch}" != "ppc64"
# python-pivy does not build on EPEL 6 ppc64.
Requires:	python-pivy
%endif
Requires:	hicolor-icon-theme
Requires:	python-collada
Requires:	python-matplotlib
Requires:	python-pyside

# plugins and private shared libs in %%{_libdir}/freecad/lib are private;
# prevent private capabilities being advertised in Provides/Requires
%define plugin_regexp /^\\\(libFreeCAD.*%(for i in %{plugins}; do echo -n "\\\|$i\\\|$iGui"; done)\\\)\\\(\\\|Gui\\\)\\.so/d
%{?filter_setup:
%filter_provides_in %{_libdir}/%{name}/lib
%filter_from_requires %{plugin_regexp}
%filter_from_provides %{plugin_regexp}
%filter_provides_in %{_libdir}/%{name}/Mod
%filter_requires_in %{_libdir}/%{name}/Mod
%filter_setup
}


%description
FreeCAD is a general purpose Open Source 3D CAD/MCAD/CAx/CAE/PLM
modeler, aimed directly at mechanical engineering and product design
but also fits a wider range of uses in engineering, such as
architecture or other engineering specialties. It is a feature-based
parametric modeler with a modular software architecture which makes it
easy to provide additional functionality without modifying the core
system.


%package data
Summary:	Data files for FreeCAD
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description data
Data files for FreeCAD


%prep
%setup -q -n %{name}-%{version}.%{rev}
%patch0 -p1 -b .3rdparty
# Remove bundled pycxx if we're not using it
%if ! %{bundled_pycxx}
rm -rf src/CXX
%endif
%patch1 -p1 -b .Xlib_h
%patch2 -p1 -b .smesh
%patch3 -p1 -b .draftsnap
# Patch comes from upstream/master, doesn't apply cleanly to 0.14.
#patch4 -p1 -b .no_dxf_dl

%if ! %{bundled_zipios}
rm -rf src/zipios++
%endif

# Fix encodings
dos2unix -k src/Mod/Test/unittestgui.py \
            ChangeLog.txt \
            copying.lib \
            data/License.txt

# Removed bundled libraries
rm -rf src/3rdParty


%build
rm -rf build && mkdir build && pushd build

# Deal with cmake projects that tend to link excessively.
LDFLAGS='-Wl,--as-needed -Wl,--no-undefined'; export LDFLAGS"

%cmake -DCMAKE_INSTALL_PREFIX=%{_libdir}/%{name} \
	   -DCMAKE_INSTALL_DATADIR=%{_datadir}/%{name} \
	   -DCMAKE_INSTALL_DOCDIR=%{_docdir}/%{name} \
	   -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
	   -DRESOURCEDIR=%{_datadir}/%{name} \
	   -DCOIN3D_INCLUDE_DIR=%{_includedir}/Coin2 \
	   -DCOIN3D_DOC_PATH=%{_datadir}/Coin2/Coin \
	   -DFREECAD_USE_EXTERNAL_PIVY=TRUE \
%if %{occ}
	   -DUSE_OCC=TRUE \
%endif
%if ! %{bundled_smesh}
	   -DFREECAD_USE_EXTERNAL_SMESH=TRUE \
	   -DSMESH_INCLUDE_DIR=%{_includedir}/smesh \
%endif
%if ! %{bundled_zipios}
	   -DFREECAD_USE_EXTERNAL_ZIPIOS=TRUE \
%endif
%if ! %{bundled_pycxx}
	   -DPYCXX_INCLUDE_DIR=$(pkg-config --variable=includedir PyCXX) \
	   -DPYCXX_SOURCE_DIR=$(pkg-config --variable=srcdir PyCXX) \
%endif
	   ../

%{__make} %{?_smp_mflags}

%{__make} doc


%install
rm -rf $RPM_BUILD_ROOT
pushd build
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
popd

# Symlink binaries to %{_bindir}
install -d $RPM_BUILD_ROOT%{_bindir}
pushd $RPM_BUILD_ROOT%{_bindir}
ln -s ../%{_lib}/freecad/bin/FreeCAD .
ln -s ../%{_lib}/freecad/bin/FreeCADCmd .
popd

# Fix problems with unittestgui.py
#chmod +x $RPM_BUILD_ROOT%{_libdir}/%{name}/Mod/Test/unittestgui.py

# Install desktop file
desktop-file-install                                   \
    --dir=$RPM_BUILD_ROOT%{_desktopdir}         \
    %{SOURCE101}
sed -i 's,@lib@,%{_lib},g' $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

# Install desktop icon
install -pD src/Gui/Icons/%{name}.svg \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

# Install man page
install -pD %{SOURCE102} \
    $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1

# Symlink manpage to other binary names
pushd $RPM_BUILD_ROOT%{_mandir}/man1
ln -sf %{name}.1.gz FreeCAD.1.gz
ln -sf %{name}.1.gz FreeCADCmd.1.gz
popd

# Remove obsolete Start_Page.html
rm -f $RPM_BUILD_ROOT%{_docdir}/%{name}/Start_Page.html

# Install MimeType file
install -d $RPM_BUILD_ROOT%{_datadir}/mime/packages
install -pm 0644 %{SOURCE104} $RPM_BUILD_ROOT%{_datadir}/mime/packages/%{name}.xml

# Install appdata file
install -d $RPM_BUILD_ROOT%{_datadir}/appdata
install -pm 0644 %{SOURCE103} $RPM_BUILD_ROOT%{_datadir}/appdata/

# Bug maintainers to keep %%{plugins} macro up to date.
#
# Make sure there are no plugins that need to be added to plugins macro
new_plugins=`ls $RPM_BUILD_ROOT%{_libdir}/freecad/lib | sed -e  '%{plugin_regexp}'`
if [ -n "$new_plugins" ]; then
    echo -e "\n\n\n**** ERROR:\n" \
        "\nPlugins not caught by regexp:  " $new_plugins \
        "\n\nPlugins in %{_libdir}/freecad/lib do not exist in" \
         "\nspecfile %%{plugins} macro.  Please add these to" \
         "\n%%{plugins} macro at top of specfile and rebuild.\n****\n" 1>&2
    exit 1
fi
# Make sure there are no entries in the plugins macro that don't match plugins
for p in %{plugins}; do
    if [ -z "`ls $RPM_BUILD_ROOT%{_libdir}/freecad/lib/$p*.so`" ]; then
        set +x
        echo -e "\n\n\n**** ERROR:\n" \
             "\nExtra entry in %%{plugins} macro with no matching plugin:" \
             "'$p'.\n\nPlease remove from %%{plugins} macro at top of" \
             "\nspecfile and rebuild.\n****\n" 1>&2
        exit 1
    fi
done



%check
%{?fedora:appstream-util validate-relax --nonet \
    %{buildroot}/%{_datadir}/appdata/*.appdata.xml}


%post
/bin/%update_icon_cache_post hicolor &>/dev/null || :
%{_bindir}/%update_desktop_database
%{_bindir}/update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/%update_icon_cache_post hicolor &>/dev/null
    %{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
%{_bindir}/%update_desktop_database
%{_bindir}/update-mime-database %{_datadir}/mime &> /dev/null || :

%posttrans
%{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog.txt copying.lib data/License.txt
%exclude %{_docdir}/freecad/freecad.*
%attr(755,root,root) %{_bindir}/*
%{_datadir}/appdata/*.appdata.xml
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%{_datadir}/mime/packages/%{name}.xml
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/bin/
%{_libdir}/%{name}/lib/
%{_libdir}/%{name}/Mod/
%{_mandir}/man1/*.1*

%files data
%defattr(644,root,root,755)
%{_datadir}/%{name}/
%{_docdir}/%{name}/freecad.q*
