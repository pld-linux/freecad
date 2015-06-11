#
# Conditional build:
%bcond_with	occ		# Compile using OpenCASCADE instead of OCE
%bcond_with	bundled_zipios 		# use bundled version of zipios++
%bcond_with	bundled_pycxx	# use bundled version of pycxx
%bcond_with	bundled_smesh	# use bundled version of Salome's Mesh

# This revision is 0.15 final.
%define	rev 4671
Summary:	A general purpose 3D CAD modeler
Name:		freecad
Version:	0.15
Release:	0.1
License:	GPL v2+
Group:		Applications/Engineering
Source0:	http://downloads.sourceforge.net/free-cad/%{name}_%{version}.%{rev}.tar.gz
# Source0-md5:	7afa95d3e8cd845bef83202e76db7f24
Source101:	%{name}.desktop
Source102:	%{name}.1
Source103:	%{name}.appdata.xml
Source104:	%{name}.sharedmimeinfo
Patch0:		%{name}-3rdParty.patch
Patch1:		%{name}-0.14-Xlib_h.patch
Patch2:		%{name}-0.14-smesh.patch
Patch3:		%{name}-0.14-DraftSnap.patch
#Patch4: %{name}-0.14-disable_auto_dxf_dl.patch
URL:		http://freecadweb.org/
# Utilities
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	dos2unix
BuildRequires:	doxygen
BuildRequires:	gcc-fortran
BuildRequires:	gettext
BuildRequires:	graphviz
BuildRequires:	swig
BuildRequires:	tbb-devel
# Development Libraries
BuildRequires:	FreeImage-devel
BuildRequires:	Mesa-libGLU-devel
BuildRequires:	xorg-lib-libXmu-devel
%if %{with occ}
BuildRequires:	OpenCASCADE-devel
%else
BuildRequires:	OCE-devel
%endif
BuildRequires:	Coin-devel
BuildRequires:	SoQt-devel
BuildRequires:	appstream-glib-devel
BuildRequires:	boost-devel
BuildRequires:	eigen3
BuildRequires:	libicu-devel
BuildRequires:	libspnav-devel
BuildRequires:	netgen-mesher-devel
#BuildRequires:  ode-devel
#BuildRequires:  opencv-devel
BuildRequires:	python-devel
BuildRequires:	python-matplotlib
%{!?with_bundled_pycxx:BuildRequires:	python-pycxx-devel}
BuildRequires:	python-pyside-devel
BuildRequires:	qt-devel
BuildRequires:	qt-webkit-devel
BuildRequires:	shiboken
%{!?with_bundled_smesh:BuildRequires:	smesh-devel}
BuildRequires:	xerces-c
BuildRequires:	xerces-c-devel
%{!?with_bundled_zipios:BuildRequires:	zipios++-devel}
Requires:	%{name}-data = %{version}-%{release}
Requires:	glib2 >= 1:2.26.0
# Obsolete old doc package since it's required for functionality.
Obsoletes:	freecad-doc < 0.13-5
# Needed for plugin support and is not a soname dependency.
Requires:	hicolor-icon-theme
Requires:	python-collada
Requires:	python-matplotlib
Requires:	python-pivy
Requires:	python-pyside
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Maintainers:  keep this list of plugins up to date
# List plugins in %%{_libdir}/freecad/lib, less '.so' and 'Gui.so', here
%define	plugins Assembly Complete Drawing Fem FreeCAD Image Import Inspection Mesh MeshPart Part Points QtUnit Raytracing ReverseEngineering Robot Sketcher Start Web PartDesignGui _PartDesign

# Some plugins go in the Mod folder instead of lib. Deal with those here:
%define	mod_plugins Mod/PartDesign

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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description data
Data files for FreeCAD.

%prep
%setup -q -n %{name}-%{version}.%{rev}
%patch0 -p1
%if %{without bundled_pycxx}
rm -r src/CXX
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1
# Patch comes from upstream/master, doesn't apply cleanly to 0.14.
#patch4 -p1

%if %{without bundled_zipios}
rm -r src/zipios++
%endif

# Fix encodings
dos2unix -k src/Mod/Test/unittestgui.py \
	ChangeLog.txt \
	copying.lib \
	data/License.txt

# Removed bundled libraries
rm -r src/3rdParty

%build
install -d build
cd build

# Deal with cmake projects that tend to link excessively.
export LDFLAGS="%{rpmcflags} -Wl,--as-needed -Wl,--no-undefined"

%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_libdir}/%{name} \
	-DCMAKE_INSTALL_DATADIR=%{_datadir}/%{name} \
	-DCMAKE_INSTALL_DOCDIR=%{_docdir}/%{name} \
	-DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
	-DRESOURCEDIR=%{_datadir}/%{name} \
	-DCOIN3D_INCLUDE_DIR=%{_includedir}/Coin2 \
	-DCOIN3D_DOC_PATH=%{_datadir}/Coin2/Coin \
	-DFREECAD_USE_EXTERNAL_PIVY=TRUE \
%if %{with occ}
	-DUSE_OCC=TRUE \
%endif
%if %{without bundled_smesh}
	-DFREECAD_USE_EXTERNAL_SMESH=TRUE \
	-DSMESH_INCLUDE_DIR=%{_includedir}/smesh \
%endif
%if %{without bundled_zipios}
	-DFREECAD_USE_EXTERNAL_ZIPIOS=TRUE \
%endif
%if %{without bundled_pycxx}
	-DPYCXX_INCLUDE_DIR=$(pkg-config --variable=includedir PyCXX) \
	-DPYCXX_SOURCE_DIR=$(pkg-config --variable=srcdir PyCXX) \
%endif
	..

%{__make}
%{__make} doc

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# Symlink binaries to %{_bindir}
install -d $RPM_BUILD_ROOT%{_bindir}
ln -s ../%{_lib}/freecad/bin/FreeCAD $RPM_BUILD_ROOT%{_bindir}
ln -s ../%{_lib}/freecad/bin/FreeCADCmd $RPM_BUILD_ROOT%{_bindir}

# Fix problems with unittestgui.py
#chmod +x $RPM_BUILD_ROOT%{_libdir}/%{name}/Mod/Test/unittestgui.py

# Install desktop file
desktop-file-install --dir=$RPM_BUILD_ROOT%{_desktopdir} %{SOURCE101}
sed -i 's,@lib@,%{_lib},g' $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

# Install desktop icon
install -pD src/Gui/Icons/%{name}.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

# Install man page
install -pD %{SOURCE102} $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1

# Symlink manpage to other binary names
ln -s %{name}.1 $RPM_BUILD_ROOT%{_mandir}/man1/FreeCAD.1
ln -s %{name}.1 $RPM_BUILD_ROOT%{_mandir}/man1/FreeCADCmd.1

# Remove obsolete Start_Page.html
rm $RPM_BUILD_ROOT%{_docdir}/%{name}/Start_Page.html

# Install MimeType file
install -d $RPM_BUILD_ROOT%{_datadir}/mime/packages
cp -p %{SOURCE104} $RPM_BUILD_ROOT%{_datadir}/mime/packages/%{name}.xml

# Install appdata file
install -d $RPM_BUILD_ROOT%{_datadir}/appdata
cp -p %{SOURCE103} $RPM_BUILD_ROOT%{_datadir}/appdata/

# Bug maintainers to keep %%{plugins} macro up to date.
#
# Make sure there are no plugins that need to be added to plugins macro
new_plugins=$(ls $RPM_BUILD_ROOT%{_libdir}/freecad/lib | sed -e '%{plugin_regexp}')
if [ -n "$new_plugins" ]; then
	cat >&2 <<-EOF
	**** ERROR:

	Plugins not caught by regexp: $new_plugins

	Plugins in %{_libdir}/freecad/lib do not exist in
	specfile %%{plugins} macro. Please add these to
	%%{plugins} macro at top of specfile and rebuild.

	****
	EOF
	exit 1
fi

# Make sure there are no entries in the plugins macro that don't match plugins
for p in %{plugins}; do
	if [ -z "$(ls $RPM_BUILD_ROOT%{_libdir}/freecad/lib/$p*.so)" ]; then
		set +x
		cat >&2 <<-EOF
			**** ERROR:

			Extra entry in %%{plugins} macro with no matching plugin:
			'$p'

			Please remove from %%{plugins} macro at top of specfile and rebuild.

			****
		EOF
		exit 1
	fi
done

appstream-util validate-relax --nonet $RPM_BUILD_ROOT/%{_datadir}/appdata/*.appdata.xml

%post
%update_icon_cache_post hicolor
%update_desktop_database
%update_mime_database

%postun
if [ $1 -eq 0 ] ; then
	%update_icon_cache hicolor
fi
%update_desktop_database
%update_mime_database

%posttrans
%update_icon_cache hicolor

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog.txt copying.lib data/License.txt
%exclude %{_docdir}/freecad/freecad.*
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*.1*
%{_datadir}/appdata/*.appdata.xml
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%{_datadir}/mime/packages/%{name}.xml
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/bin
%{_libdir}/%{name}/lib
%{_libdir}/%{name}/Mod

%files data
%defattr(644,root,root,755)
%{_datadir}/%{name}/
%{_docdir}/%{name}/freecad.q*
