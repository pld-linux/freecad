#
# Conditional build:
%bcond_with	system_smesh	# use system version of Salome's Mesh
%bcond_with	system_zipios	# use system version of zipios++

Summary:	A general purpose 3D CAD modeler
Name:		FreeCAD
Version:	1.0.0
Release:	3
License:	LGPL v2
Group:		Applications/Engineering
Source0:	https://github.com/FreeCAD/FreeCAD/releases/download/%{version}/freecad_source.tar.gz
# Source0-md5:	6f0d75711b1d3b3ba35cb4e79c200c2d
Patch0:		apphome.patch
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
BuildRequires:	Coin-devel
BuildRequires:	FreeImage-devel
BuildRequires:	Mesa-libGLU-devel
BuildRequires:	OpenCASCADE-devel
BuildRequires:	PyCXX
BuildRequires:	Qt6Concurrent-devel
BuildRequires:	Qt6Core-devel
BuildRequires:	Qt6Designer-devel
BuildRequires:	Qt6Network-devel
BuildRequires:	Qt6OpenGL-devel
BuildRequires:	Qt6PrintSupport-devel
BuildRequires:	Qt6Svg-devel
BuildRequires:	Qt6Test-devel
BuildRequires:	Qt6UiTools-devel
BuildRequires:	Qt6WebEngine-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	Qt6Xml-devel
BuildRequires:	SoQt-devel
BuildRequires:	appstream-glib-devel
BuildRequires:	boost-devel >= 1:1.85.0
BuildRequires:	eigen3
BuildRequires:	ffmpeg-devel >= 6.0
BuildRequires:	hdf5-c++-devel
BuildRequires:	libicu-devel
BuildRequires:	libspnav-devel
BuildRequires:	med-devel
BuildRequires:	netcdf-cxx4-devel
BuildRequires:	netgen-mesher-devel
# not needed at the moment
#BuildRequires:  opencv-devel
BuildRequires:	python3-PySide6
BuildRequires:	python3-devel
BuildRequires:	python3-matplotlib
BuildRequires:	python3-pivy
BuildRequires:	python3-pivy-gui
BuildRequires:	shiboken6
BuildRequires:	vtk-devel
BuildRequires:	xerces-c
BuildRequires:	xerces-c-devel
BuildRequires:	xorg-lib-libXmu-devel
%{?with_system_zipios:BuildRequires:	zipios++-devel}
Requires:	%{name}-data = %{version}-%{release}
Requires:	glib2 >= 1:2.26.0
# Needed for plugin support and is not a soname dependency.
Requires:	hicolor-icon-theme
Requires:	python3-PySide6
Requires:	python3-matplotlib
Requires:	python3-pivy
Requires:	python3-pivy-gui
ExcludeArch:	%{ix86} x32
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%patch -P 0 -p1

%build
#	-DFREECAD_USE_EXTERNAL_PIVY=TRUE \
install -d build
cd build
%cmake ../ \
	-DCMAKE_INSTALL_PREFIX=%{_libdir}/%{name} \
	-DCMAKE_INSTALL_DATADIR=%{_datadir}/%{name} \
	-DCMAKE_INSTALL_DOCDIR=%{_docdir}/%{name} \
	-DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
	-DCMAKE_INSTALL_LIBDIR=%{_libdir}/%{name}/lib \
	-DAPPHOMEPATH=%{_libdir}/%{name} \
	-DLIBRARYDIR=%{_libdir}/%{name}/lib \
	-DRESOURCEDIR=%{_datadir}/%{name} \
	-DENABLE_DEVELOPER_TESTS=OFF \
	-DBUILD_DESIGNER_PLUGIN=ON \
	-DBUILD_FEM_NETGEN=ON \
	-DFREECAD_QT_MAJOR_VERSION=6 \
	-DQT_DEFAULT_MAJOR_VERSION=6 \
%if %{with system_smesh}
	-DFREECAD_USE_EXTERNAL_SMESH=ON \
	-DSMESH_INCLUDE_DIR=%{_includedir}/smesh \
%endif
	%{cmake_on_off system_zipios FREECAD_USE_EXTERNAL_ZIPIOS}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%py3_ocomp $RPM_BUILD_ROOT{py3_sitescriptdir}

%{__rm} -r $RPM_BUILD_ROOT{%{_includedir},%{_npkgconfigdir}}
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/FreeCAD/include
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
%{_datadir}/metainfo/*.xml
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*x*/apps/org.freecad.FreeCAD.png
%{_iconsdir}/hicolor/scalable/apps/org.freecad.FreeCAD.svg
%{_iconsdir}/hicolor/scalable/mimetypes/application-x-extension-fcstd.svg
%{_pixmapsdir}/freecad.xpm
%{_datadir}/mime/packages/*.xml
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/Ext
%{_libdir}/%{name}/Mod
%dir %{_libdir}/%{name}/lib
%attr(755,root,root) %{_libdir}/%{name}/lib/*.so
%attr(755,root,root) %{_libdir}/%{name}/lib/libOndselSolver.so.*
%{py3_sitescriptdir}/freecad
%{_datadir}/thumbnailers/FreeCAD.thumbnailer

%files data
%defattr(644,root,root,755)
%{_datadir}/%{name}
