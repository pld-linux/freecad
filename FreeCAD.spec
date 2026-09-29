# Not applicable:
# - BUILD_CLOUD (does not compile, removed upstream: https://github.com/FreeCAD/FreeCAD/pull/30651)
# - BUILD_DRAWING, BUILD_JTREADER, BUILD_VR (modules absent from the tarball)
# - BUILD_MATERIAL_EXTERNAL (API for external material databases; its only backend, the MaterialDB addon, is an unreleased 0.0.1 prototype)
# - FREECAD_USE_EXTERNAL_KDL (lookup commented out upstream, bundled kdl is extended)
# - FREECAD_USE_EXTERNAL_ONDSELSOLVER (FreeCAD-only submodule without releases of its own)
# - FREECAD_USE_EXTERNAL_PYCXX (pkgconfig-only; PLD PyCXX ships no .pc, paths passed directly)
# - OpenMPI (only for med built with MPI)
# - USE_CUDA, USE_OPENCV (no build logic behind them)
#
# Conditional build:
%bcond_without	pcl		# PCL-based reverse engineering features
%bcond_with	system_smesh	# system version of Salome's Mesh
%bcond_with	system_zipios	# system version of zipios++
%bcond_without	tests		# unit tests

Summary:	A general purpose 3D CAD modeler
Summary(pl.UTF-8):	Modeler CAD 3D ogólnego przeznaczenia
Name:		FreeCAD
Version:	1.1.4
Release:	1
License:	LGPL v2
Group:		Applications/Engineering
Source0:	https://github.com/FreeCAD/FreeCAD/releases/download/%{version}/freecad_source_%{version}.tar.gz
# Source0-md5:	59bf65d8df3e999d340483d854cf4333
Patch1:		external-E57Format.patch
Patch2:		FreeCAD-netgen.patch
Patch3:		test-lineformat.patch
Patch4:		cam-offset-occ793.patch
Patch5:		fileinfo-extension.patch
Patch6:		unit-pow-round.patch
Patch7:		fem-glyph-idtype.patch
URL:		https://freecad.org/
BuildRequires:	Coin-devel
# 7.8 cmake exports linked draco, FreeImage, freetype, tk, X11 by path/name; 7.9 exports only OCC and VTK targets
BuildRequires:	OpenCASCADE-devel >= 7.9.3
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-GLU-devel
# 7.1.x uses _Py_PackageContext, gone from Python 3.13 headers
BuildRequires:	PyCXX >= 7.2.0
BuildRequires:	Qt6Concurrent-devel >= 6
BuildRequires:	Qt6Core-devel >= 6
BuildRequires:	Qt6Designer-devel >= 6
BuildRequires:	Qt6Network-devel >= 6
BuildRequires:	Qt6OpenGL-devel >= 6
BuildRequires:	Qt6PrintSupport-devel >= 6
BuildRequires:	Qt6Svg-devel >= 6
%{?with_tests:BuildRequires:	Qt6Test-devel >= 6}
BuildRequires:	Qt6UiTools-devel >= 6
BuildRequires:	Qt6Widgets-devel >= 6
BuildRequires:	Qt6Xml-devel >= 6
BuildRequires:	SoQt-devel
# components: program_options regex thread date_time
BuildRequires:	boost-devel >= 1:1.85.0
BuildRequires:	boost-python-devel-common >= 1:1.85.0
BuildRequires:	boost-python3-devel >= 1:1.85.0
BuildRequires:	cmake >= 3.22.0
BuildRequires:	desktop-file-utils
BuildRequires:	eigen3 >= 3.4.0
BuildRequires:	freetype-devel >= 2
BuildRequires:	gcc-fortran
%{?with_tests:BuildRequires:	gmock-devel}
%{?with_tests:BuildRequires:	gtest-devel}
BuildRequires:	hdf5-devel
BuildRequires:	libE57Format-devel
BuildRequires:	libfmt-devel
# OpenMP >= 4.0
BuildRequires:	libgomp-devel >= 6:5
BuildRequires:	libicu-devel
BuildRequires:	libspnav-devel
BuildRequires:	libstdc++-devel >= 6:11.2
BuildRequires:	med-devel
# FreeCAD-netgen.patch uses Segment::EPGeomInfo() accessors, absent in 6.2.2404
BuildRequires:	netgen-mesher-devel >= 6.2.2607
# not needed at the moment
#BuildRequires:	opencv-devel
# 1.14.1-3 ships Modules/ that PCLConfig.cmake includes
%{?with_pcl:BuildRequires:	pcl-devel >= 1.14.1-3}
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
# 9.3.1-20 -devel pulls in the -devels vtk-config.cmake runs find_package() for
BuildRequires:	vtk-devel >= 9.3.1-20
# 9.3.1-21 fixes the Python 3.13 segfault on import (FEM tests import vtkmodules)
BuildRequires:	vtk-python3-devel >= 9.3.1-21
BuildRequires:	xerces-c-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	yaml-cpp-devel
%{?with_system_zipios:BuildRequires:	zipios++-devel}
BuildRequires:	zlib-devel
Requires:	%{name}-data = %{version}-%{release}
Requires:	glib2 >= 1:2.26.0
Requires:	hicolor-icon-theme
Requires:	python3-PySide6
Requires:	python3-matplotlib
# FEM Netgen mesher runs a python script importing netgen.occ/pyngcore/numpy
Requires:	python3-netgen-mesher
Requires:	python3-numpy
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
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1
%patch -P7 -p1

# don't force color diagnostics if output is not terminal
%{__sed} -i -e 's/-fdiagnostics-color //' cMake/FreeCAD_Helpers/CompilerChecksAndSetups.cmake

%build
#	-DFREECAD_USE_EXTERNAL_PIVY=TRUE \
# install dirs relative to AppHomePath (the binary location), so data and libs are found from the build tree too
%cmake -B build \
	-DCMAKE_INSTALL_PREFIX=%{_libdir}/%{name} \
	-DCMAKE_INSTALL_BINDIR=bin \
	-DCMAKE_INSTALL_DATADIR=../../share/%{name} \
	-DCMAKE_INSTALL_DOCDIR=%{_docdir}/%{name} \
	-DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
	-DCMAKE_INSTALL_LIBDIR=lib \
	-DBUILD_DESIGNER_PLUGIN=ON \
	-DBUILD_FEM_NETGEN=ON \
	-DENABLE_DEVELOPER_TESTS=%{__ON_OFF tests} \
	-DFREECAD_QT_MAJOR_VERSION=6 \
	-DFREECAD_USE_EXTERNAL_E57FORMAT=ON \
	-DFREECAD_USE_EXTERNAL_GTEST=ON \
	-DFREECAD_USE_EXTERNAL_ZIPIOS=%{__ON_OFF system_zipios} \
	-DFREECAD_USE_PCL=%{__ON_OFF pcl} \
	-DPYCXX_INCLUDE_DIRS=%{py3_incdir} \
	-DPYCXX_SOURCE_DIR=%{_datadir}/python%{py3_ver}/CXX \
	-DQT_DEFAULT_MAJOR_VERSION=6 \
%if %{with system_smesh}
	-DFREECAD_USE_EXTERNAL_SMESH=ON \
	-DSMESH_INCLUDE_DIR=%{_includedir}/smesh \
%endif

%{__make} -C build

%if %{with tests}
# user config and caches go to $HOME
export HOME=$(pwd)/build/tests-home
export QT_QPA_PLATFORM=offscreen
# FileInfoTest cases share one scratch dir, https://github.com/FreeCAD/FreeCAD/issues/28737
ctest_exclude='FileInfoTest'
%ifarch %{ix86}
# exact floating point comparisons that x87 excess precision does not meet
ctest_exclude="$ctest_exclude|^BaseQuantityLoc\.psi_|^Vector\.TestIsNormal$|^SMesh\.testMefisto$"
%endif
%ifarch x32
# shiboken6 segfaults in PyStaticMethod_New when these tests start PySide
ctest_exclude="$ctest_exclude|^(Assistant|CameraPrecalculatedQuaternions|CameraRotation|StyleParametersApplicationTest)\.|^(DlgVersionMigrator|QuantitySpinBox)_Tests_run$"
%endif
ctest --test-dir build --output-on-failure %{?_smp_mflags} -E "$ctest_exclude"
ctest --test-dir build --output-on-failure -R FileInfoTest
%ifnarch %{ix86}
# CAM Adaptive does not converge with x87 math, TestPathAdaptive loops for hours
build/bin/FreeCADCmd -t 0
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# AppHomePath is derived from the real path of the binary
install -d $RPM_BUILD_ROOT%{_bindir}
for f in FreeCAD FreeCADCmd freecad-thumbnailer; do
	ln -s ../%{_lib}/%{name}/bin/$f $RPM_BUILD_ROOT%{_bindir}/$f
done

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
%{_bindir}/FreeCAD
%{_bindir}/FreeCADCmd
%{_bindir}/freecad-thumbnailer
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/bin
%attr(755,root,root) %{_libdir}/%{name}/bin/FreeCAD
%attr(755,root,root) %{_libdir}/%{name}/bin/FreeCADCmd
%attr(755,root,root) %{_libdir}/%{name}/bin/freecad-thumbnailer
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
