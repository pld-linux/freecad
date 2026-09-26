# TODO:
# - OpenMPI (ompi-cxx)?
# - BUILD_CLOUD?
# - BUILD_DRAWING?
# - BUILD_JTREADER?
# - BUILD_MATERIAL_EXTERNAL?
# - BUILD_VR? (BR: OCULUS/Rift SDK 4.x)
# - FREECAD_USE_EXTERNAL_KDL? (BR: pkgconfig(orocos-kdl) >= 1.4.0, pkgconfig(orocos-kdltk-*) >= 1.4.0)
# - FREECAD_USE_EXTERNAL_ONDSELSOLVER? (BR: OndselSolver)
# - FREECAD_USE_EXTERNAL_PYCXX?
# - FREECAD_USE_PCL? (BR: pcl-devel components: common kdtree features surface io filters segmentation sample_consensus)
# - USE_CUDA on bcond?
# - USE_OPENCV?
#
# Conditional build:
%bcond_with	system_smesh	# system version of Salome's Mesh
%bcond_with	system_zipios	# system version of zipios++

Summary:	A general purpose 3D CAD modeler
Summary(pl.UTF-8):	Modeler CAD 3D ogólnego przeznaczenia
Name:		FreeCAD
Version:	1.1.3
Release:	3
License:	LGPL v2
Group:		Applications/Engineering
Source0:	https://github.com/FreeCAD/FreeCAD/releases/download/%{version}/freecad_source_%{version}.tar.gz
# Source0-md5:	355c28ccdabc1afedc9adbc247c490bf
Patch0:		apphome.patch
Patch1:		external-E57Format.patch
Patch2:		FreeCAD-netgen.patch
URL:		https://freecad.org/
BuildRequires:	Coin-devel
BuildRequires:	FreeImage-devel
BuildRequires:	OpenCASCADE-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	PyCXX
BuildRequires:	Qt6Concurrent-devel >= 6
BuildRequires:	Qt6Core-devel >= 6
BuildRequires:	Qt6Designer-devel >= 6
BuildRequires:	Qt6Network-devel >= 6
BuildRequires:	Qt6OpenGL-devel >= 6
BuildRequires:	Qt6PrintSupport-devel >= 6
BuildRequires:	Qt6Svg-devel >= 6
BuildRequires:	Qt6UiTools-devel >= 6
BuildRequires:	Qt6Widgets-devel >= 6
BuildRequires:	Qt6Xml-devel >= 6
BuildRequires:	SoQt-devel
# components: program_options regex thread date_time
BuildRequires:	boost-devel >= 1:1.85.0
BuildRequires:	boost-python-devel-common >= 1:1.85.0
BuildRequires:	boost-python3-devel >= 1:1.85.0
BuildRequires:	cmake >= 3.22.0
BuildRequires:	cups-devel
BuildRequires:	desktop-file-utils
BuildRequires:	dos2unix
BuildRequires:	double-conversion-devel
BuildRequires:	doxygen
BuildRequires:	draco-devel
BuildRequires:	eigen3 >= 3.4.0
BuildRequires:	expat-devel >= 1.95
BuildRequires:	ffmpeg-devel >= 6.0
BuildRequires:	freetype-devel >= 2
BuildRequires:	gcc-fortran
BuildRequires:	gettext-tools
BuildRequires:	glew-devel
BuildRequires:	graphviz
BuildRequires:	hdf5-devel
BuildRequires:	hdf5-c++-devel
BuildRequires:	libE57Format-devel
BuildRequires:	libfmt-devel
# OpenMP >= 4.0
BuildRequires:	libgomp-devel >= 6:5
BuildRequires:	libicu-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libspnav-devel
BuildRequires:	libstdc++-devel >= 6:11.2
BuildRequires:	libtiff-devel
BuildRequires:	lz4-devel
BuildRequires:	med-devel
BuildRequires:	netcdf-cxx4-devel
BuildRequires:	netgen-mesher-devel >= 6.2
# not needed at the moment
#BuildRequires:	opencv-devel
BuildRequires:	pkgconfig
BuildRequires:	python3-PySide6 >= 6
BuildRequires:	python3-devel >= 1:3.10
BuildRequires:	python3-matplotlib
BuildRequires:	python3-pivy
BuildRequires:	python3-pivy-gui
BuildRequires:	python3-pybind11
BuildRequires:	qt6-build >= 6
BuildRequires:	qt6-linguist >= 6
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.047
BuildRequires:	shiboken6 >= 6
%{?with_system_smesh:BuildRequires:  smesh-devel >= 7.7.1}
BuildRequires:	swig
BuildRequires:	tbb-devel
BuildRequires:	vtk-devel >= 6.2
BuildRequires:	vtk-python3-devel >= 6.2
BuildRequires:	xerces-c-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz-devel
BuildRequires:	yaml-cpp-devel
%{?with_system_zipios:BuildRequires:	zipios++-devel}
BuildRequires:	zlib-devel
Requires:	%{name}-data = %{version}-%{release}
Requires:	glib2 >= 1:2.26.0
Requires:	hicolor-icon-theme
Requires:	python3-PySide6
Requires:	python3-matplotlib
Requires:	python3-pivy
Requires:	python3-pivy-gui
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FreeCAD is a general purpose Open Source 3D CAD/MCAD/CAx/CAE/PLM
modeler, aimed directly at mechanical engineering and product design
but also fits a wider range of uses in engineering, such as
architecture or other engineering specialties. It is a feature-based
parametric modeler with a modular software architecture which makes it
easy to provide additional functionality without modifying the core
system.

%description -l pl.UTF-8
FreeCAD to mający otwarte źródła modeler CAD/MCAD/CAx/CAE/PLM 3D
ogólnego przeznaczenia, przeznaczony bezpośrednio do inżynierii
mechanicznej oraz projektowania wyrobów, ale nadający się także do
szerszego zakresu prac inżynierskich, takich jak architektura czy
inne specjalizacje. Jest to modeler parametryczny o modularnej
architekturze programowej, ułatwiający dodawanie nowej funkcjonalności
bez modyfikowania podstawowego systemu.

%package data
Summary:	Data files for FreeCAD
Summary(pl.UTF-8):	Pliki danych FreeCAD-a
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description data
Data files for FreeCAD.

%description data -l pl.UTF-8
Pliki danych FreeCAD-a.

%package -n Qt6Designer-plugin-%{name}
Summary:	FreeCAD plugin for Qt Designer
Summary(pl.UTF-8):	Wtyczka FreeCAD do Qt Designera
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Designer >= 6

%description -n Qt6Designer-plugin-%{name}
FreeCAD plugin for Qt Designer that allows FreeCAD instances to
be included in GUI designs just like any other Qt widget.

%description -n Qt6Designer-plugin-%{name} -l pl.UTF-8
Wtyczka FreeCAD do Qt Designera, pozwalająca na włączanie w projektach
GUI instancji FreeCAD-a tak, jak innych widżetów Qt.

%prep
%setup -q -c
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

# don't force color diagnostics if output is not terminal
%{__sed} -i -e 's/-fdiagnostics-color //' cMake/FreeCAD_Helpers/CompilerChecksAndSetups.cmake

%build
#	-DFREECAD_USE_EXTERNAL_PIVY=TRUE \
%cmake -B build \
	-DCMAKE_INSTALL_PREFIX=%{_libdir}/%{name} \
	-DCMAKE_INSTALL_DATADIR=%{_datadir}/%{name} \
	-DCMAKE_INSTALL_DOCDIR=%{_docdir}/%{name} \
	-DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
	-DCMAKE_INSTALL_LIBDIR=%{_libdir}/%{name}/lib \
	-DAPPHOMEPATH=%{_libdir}/%{name} \
	-DLIBRARYDIR=%{_libdir}/%{name}/lib \
	-DRESOURCEDIR=%{_datadir}/%{name} \
	-DBUILD_DESIGNER_PLUGIN=ON \
	-DBUILD_FEM_NETGEN=ON \
	-DENABLE_DEVELOPER_TESTS=OFF \
	-DFREECAD_QT_MAJOR_VERSION=6 \
	-DFREECAD_USE_EXTERNAL_E57FORMAT=ON \
	-DFREECAD_USE_EXTERNAL_ZIPIOS=%{__ON_OFF system_zipios} \
	-DQT_DEFAULT_MAJOR_VERSION=6 \
%if %{with system_smesh}
	-DFREECAD_USE_EXTERNAL_SMESH=ON \
	-DSMESH_INCLUDE_DIR=%{_includedir}/smesh \
%endif

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%py3_ocomp $RPM_BUILD_ROOT%{py3_sitescriptdir}

%{__rm} -r $RPM_BUILD_ROOT{%{_includedir},%{_npkgconfigdir}}
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/FreeCAD

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
%doc README.md SECURITY.md
%doc build/usr/share/doc/FreeCAD/LICENSE.html
%doc build/usr/share/doc/FreeCAD/ThirdPartyLibraries.html
%attr(755,root,root) %{_bindir}/FreeCAD
%attr(755,root,root) %{_bindir}/FreeCADCmd
%attr(755,root,root) %{_bindir}/freecad-thumbnailer
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/Ext
%{_libdir}/%{name}/Mod
%dir %{_libdir}/%{name}/lib
%{_libdir}/%{name}/lib/*.so
%{_libdir}/%{name}/lib/libOndselSolver.so.*
%{py3_sitescriptdir}/freecad
%{_datadir}/metainfo/org.freecad.FreeCAD.metainfo.xml
%{_datadir}/mime/packages/org.freecad.FreeCAD.xml
%{_datadir}/thumbnailers/FreeCAD.thumbnailer
%{_desktopdir}/org.freecad.FreeCAD.desktop
%{_iconsdir}/hicolor/*x*/apps/org.freecad.FreeCAD.png
%{_iconsdir}/hicolor/scalable/apps/org.freecad.FreeCAD.svg
%{_iconsdir}/hicolor/scalable/mimetypes/application-x-extension-fcstd.svg
%{_pixmapsdir}/freecad.svg

%files data
%defattr(644,root,root,755)
%{_datadir}/%{name}

%files -n Qt6Designer-plugin-%{name}
%defattr(644,root,root,755)
%{_libdir}/qt6/plugins/designer/libFreeCAD_widgets.so
