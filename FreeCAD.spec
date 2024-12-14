#
# Conditional build:
%bcond_with	system_smesh	# use system version of Salome's Mesh
%bcond_with	system_zipios	# use system version of zipios++

Summary:	A general purpose 3D CAD modeler
Name:		FreeCAD
Version:	1.0.0
Release:	0.1
License:	LGPL v2
Group:		Applications/Engineering
Source0:	https://github.com/FreeCAD/FreeCAD/releases/download/%{version}/freecad_source.tar.gz
# Source0-md5:	6f0d75711b1d3b3ba35cb4e79c200c2d
URL:		http://freecadweb.org/
# Utilities
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	dos2unix
BuildRequires:	doxygen
BuildRequires:	gcc-fortran
BuildRequires:	gettext
BuildRequires:	graphviz
%{?with_system_smesh:BuildRequires:  smesh-devel}
BuildRequires:	swig
BuildRequires:	tbb-devel
# Development Libraries
BuildRequires:	FreeImage-devel
BuildRequires:	Mesa-libGLU-devel
BuildRequires:	PyCXX
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	OpenCASCADE-devel
BuildRequires:	Coin-devel
BuildRequires:	Qt5Concurrent-devel
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Network-devel
BuildRequires:	Qt5OpenGL-devel
BuildRequires:	Qt5PrintSupport-devel
BuildRequires:	Qt5Svg-devel
BuildRequires:	Qt5Test-devel
BuildRequires:	Qt5UiTools-devel
BuildRequires:	Qt5WebKit-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	Qt5Xml-devel
BuildRequires:	SoQt-devel
BuildRequires:	appstream-glib-devel
BuildRequires:	boost-devel
BuildRequires:	eigen3
BuildRequires:	ffmpeg-devel >= 6.0
BuildRequires:	hdf5-c++-devel
BuildRequires:	libicu-devel
BuildRequires:	libspnav-devel
BuildRequires:	med-devel
BuildRequires:	netcdf-cxx4-devel
#BuildRequires:	netgen-mesher-devel
#BuildRequires:  ode-devel
#BuildRequires:  opencv-devel
#BuildRequires:	pyside-tools
#BuildRequires:	python-PySide2-devel
BuildRequires:	python3-devel
BuildRequires:	python3-matplotlib
#BuildRequires:	shiboken
BuildRequires:	vtk-devel
BuildRequires:	xerces-c
BuildRequires:	xerces-c-devel
%{?with_system_zipios:BuildRequires:	zipios++-devel}
Requires:	%{name}-data = %{version}-%{release}
Requires:	glib2 >= 1:2.26.0
# Needed for plugin support and is not a soname dependency.
Requires:	hicolor-icon-theme
Requires:	python3-collada
Requires:	python3-matplotlib
Requires:	python3-Pivy
Requires:	python3-PySide2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Maintainers:  keep this list of plugins up to date
# List plugins in %%{_libdir}/freecad/lib, less '.so' and 'Gui.so', here
%define	plugins Complete Drawing Fem FreeCAD Image Import Inspection Mesh MeshPart Part Points QtUnit Raytracing ReverseEngineering Robot Sketcher Start Web PartDesignGui _PartDesign Spreadsheet SpreadsheetGui

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
BuildArch:	noarch

%description data
Data files for FreeCAD.

%prep
%setup -q -c

%build
#	-DCMAKE_INSTALL_PREFIX=%{_libdir}/%{name} \
#	-DCMAKE_INSTALL_DATADIR=%{_datadir}/%{name} \
#	-DCMAKE_INSTALL_DOCDIR=%{_docdir}/%{name} \
#	-DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
#	-DCMAKE_INSTALL_LIBDIR=%{_libdir}/%{name}/lib \
#	-DRESOURCEDIR=%{_datadir}/%{name} \
#	-DCOIN3D_INCLUDE_DIR=%{_includedir}/Coin2 \
#	-DCOIN3D_DOC_PATH=%{_datadir}/Coin2/Coin \
#	-DFREECAD_USE_EXTERNAL_PIVY=TRUE \
install -d build
cd build
%cmake ../ \
%if %{with system_smesh}
	-DFREECAD_USE_EXTERNAL_SMESH=TRUE \
	-DSMESH_INCLUDE_DIR=%{_includedir}/smesh \
%endif
	%{cmake_on_off system_zipios FREECAD_USE_EXTERNAL_ZIPIOS} \
	-DPYCXX_INCLUDE_DIR=%{_includedir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

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
%update_icon_cache hicolor
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
%attr(755,root,root) %{_bindir}/FreeCAD
%attr(755,root,root) %{_bindir}/FreeCADCmd
%{_mandir}/man1/*.1*
%{_datadir}/appdata/*.appdata.xml
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%{_datadir}/mime/packages/%{name}.xml
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/bin
%attr(755,root,root) %{_libdir}/%{name}/bin/*
%dir %{_libdir}/%{name}/lib
%attr(755,root,root) %{_libdir}/%{name}/lib/*.so
%{_libdir}/%{name}/Mod

%files data
%defattr(644,root,root,755)
%{_datadir}/%{name}/
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/freecad.q*
