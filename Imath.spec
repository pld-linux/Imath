#
# Conditional build:
%bcond_without	python2	# CPython 2.x binding
%bcond_without	python3	# CPython 3.x binding

Summary:	High dynamic-range (HDR) image file format support libraries
Summary(pl.UTF-8):	Biblioteki obsługujące format plików obrazu o wysokiej dynamice (HDR)
Name:		Imath
Version:	3.1.11
Release:	3
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/AcademySoftwareFoundation/Imath/releases
Source0:	https://github.com/AcademySoftwareFoundation/Imath/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	28c0e9971a8e6720112a8037837ff8e4
URL:		https://openexr.com/
BuildRequires:	cmake >= 3.12
BuildRequires:	libstdc++-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
%if %{with python2}
BuildRequires:	boost-python-devel
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	python-numpy-devel
%endif
%if %{with python3}
BuildRequires:	boost-python3-devel
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-numpy-devel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Imath is a basic, light-weight, and efficient C++ representation of 2D
and 3D vectors and matrices and other simple but useful mathematical
objects, functions, and data types common in computer graphics
applications, including the "half" 16-bit floating-point type.

%description -l pl.UTF-8
Imath to prosta, lekka i wydajna reprezentacja C++ dwu- i
trójwymiarowych wektorów i macierzy i inne proste, ale użyteczne
matematyczne obiekty, funkcje i typy danych zwykle występujące w
programach graficznych, w tym "połówkowy" 16 bitowy typ
zmiennoprzecinkowy.

%package devel
Summary:	Header files for Imath libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Imath
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Conflicts:	ilmbase-devel < 3

%description devel
Header files for Imath libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Imath.

%package -n python-pyimath
Summary:	Python 2 bindings for the Imath library
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki Imath
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Obsoletes:	python-pyilmbase < 3

%description -n python-pyimath
The PyImath package provides Python bindings for the Imath library.

%description -n python-pyimath -l pl.UTF-8
Pakiet PyImath dostarcza wiązania Pythona do bibliotek Imath.

%package -n python-pyimath-devel
Summary:	Header files for Python 2 bindings for the Imath library
Summary(pl.UTF-8):	Pliki nagłówkowe wiązań Pythona 2 do biblioteki Imath
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	python-devel >= 1:2.5
Requires:	python-pyimath = %{version}-%{release}
Obsoletes:	pyilmbase-devel < 3
Obsoletes:	python-pyilmbase-devel < 3

%description -n python-pyimath-devel
Header files for Python bindings for the Imath library.

%description -n python-pyimath-devel -l pl.UTF-8
Pliki nagłówkowe wiązań Pythona do biblioteki Imath.

%package -n python3-pyimath
Summary:	Python 3 bindings for the Imath library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki Imath
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Obsoletes:	python3-pyilmbase < 3

%description -n python3-pyimath
The PyImath package provides Python bindings for the Imath library.

%description -n python3-pyimath -l pl.UTF-8
Pakiet PyImath dostarcza wiązania Pythona do bibliotek Imath.

%package -n python3-pyimath-devel
Summary:	Header files for Python 3 bindings for the Imath library
Summary(pl.UTF-8):	Pliki nagłówkowe wiązań Pythona 3 do biblioteki Imath
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	python3-devel >= 1:3.2
Requires:	python3-pyimath = %{version}-%{release}
Obsoletes:	pyilmbase-devel < 3
Obsoletes:	python3-pyilmbase-devel < 3

%description -n python3-pyimath-devel
Header files for Python bindings for the Imath library.

%description -n python3-pyimath-devel -l pl.UTF-8
Pliki nagłówkowe wiązań Pythona do biblioteki Imath.

%prep
%setup -q

%build
%if %{with python2}
install -d build-py2
cd build-py2
%cmake -G Ninja \
	-DCMAKE_INSTALL_INSTALLDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DPYIMATH_OVERRIDE_PYTHON_INSTALL_DIR=%{py_sitedir} \
	-DPYTHON=ON \
	-DUSE_PYTHON2=ON \
	..

%ninja_build
cd ..
%endif

install -d build
cd build
%cmake -G Ninja \
	-DCMAKE_INSTALL_INSTALLDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DPYIMATH_OVERRIDE_PYTHON_INSTALL_DIR=%{py3_sitedir} \
	%{?with_python3:-DPYTHON=ON} \
	..

%ninja_build

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%ninja_install -C build-py2

%{__mv} $RPM_BUILD_ROOT%{_pkgconfigdir}/Py{,2}Imath.pc
%endif

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n python-pyimath -p /sbin/ldconfig
%postun	-n python-pyimath -p /sbin/ldconfig

%post	-n python3-pyimath -p /sbin/ldconfig
%postun	-n python3-pyimath -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES.md CONTRIBUTORS.md GOVERNANCE.md LICENSE.md README.md SECURITY.md
%attr(755,root,root) %{_libdir}/libImath-3_1.so.*.*.*
%ghost %{_libdir}/libImath-3_1.so.29

%files devel
%defattr(644,root,root,755)
%{_libdir}/libImath-3_1.so
%{_libdir}/libImath.so
%dir %{_includedir}/Imath
%{_includedir}/Imath/Imath*.h
%{_includedir}/Imath/half*.h
%{_libdir}/cmake/Imath
%{_pkgconfigdir}/Imath.pc

%if %{with python2}
%files -n python-pyimath
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libPyImath_Python2_*-3_1.so.*.*.*
%ghost %{_libdir}/libPyImath_Python2_*-3_1.so.29
%attr(755,root,root) %{py_sitedir}/imath.so
%attr(755,root,root) %{py_sitedir}/imathnumpy.so

%files -n python-pyimath-devel
%defattr(644,root,root,755)
%{_libdir}/libPyImath_Python2_*-3_1.so
%{_includedir}/Imath/PyImath*.h
%{_pkgconfigdir}/Py2Imath.pc
%endif

%if %{with python3}
%files -n python3-pyimath
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libPyImath_Python3_*-3_1.so.*.*.*
%ghost %{_libdir}/libPyImath_Python3_*-3_1.so.29
%attr(755,root,root) %{py3_sitedir}/imath.so
%attr(755,root,root) %{py3_sitedir}/imathnumpy.so

%files -n python3-pyimath-devel
%defattr(644,root,root,755)
%{_libdir}/libPyImath_Python3_*-3_1.so
%{_includedir}/Imath/PyImath*.h
%{_pkgconfigdir}/PyImath.pc
%endif
