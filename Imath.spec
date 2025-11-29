#
# Conditional build:
%bcond_without	python3	# CPython 3.x binding

Summary:	High dynamic-range (HDR) image file format support libraries
Summary(pl.UTF-8):	Biblioteki obsługujące format plików obrazu o wysokiej dynamice (HDR)
Name:		Imath
Version:	3.2.2
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/AcademySoftwareFoundation/Imath/releases
Source0:	https://github.com/AcademySoftwareFoundation/Imath/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e29f25ce926ac53d8e0a52197299f61b
Patch0:		python-install.patch
URL:		https://openexr.com/
BuildRequires:	cmake >= 3.12
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
%if %{with python3}
BuildRequires:	boost-python3-devel
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-numpy-devel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	libPyImath_Python3.*.so.*

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
Requires:	libstdc++-devel >= 6:5
Conflicts:	ilmbase-devel < 3

%description devel
Header files for Imath libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Imath.

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
%patch -P0 -p1

%build
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

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n python3-pyimath -p /sbin/ldconfig
%postun	-n python3-pyimath -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES.md CONTRIBUTORS.md GOVERNANCE.md LICENSE.md README.md SECURITY.md
%{_libdir}/libImath-3_2.so.*.*.*
%ghost %{_libdir}/libImath-3_2.so.30

%files devel
%defattr(644,root,root,755)
%{_libdir}/libImath-3_2.so
%{_libdir}/libImath.so
%dir %{_includedir}/Imath
%{_includedir}/Imath/Imath*.h
%{_includedir}/Imath/half*.h
%{_libdir}/cmake/Imath
%{_pkgconfigdir}/Imath.pc

%if %{with python3}
%files -n python3-pyimath
%defattr(644,root,root,755)
%{_libdir}/libPyImath_Python3_*-3_2.so.*.*.*
%ghost %{_libdir}/libPyImath_Python3_*-3_2.so.30
%attr(755,root,root) %{py3_sitedir}/imath.so
%attr(755,root,root) %{py3_sitedir}/imathnumpy.so

%files -n python3-pyimath-devel
%defattr(644,root,root,755)
%{_libdir}/libPyImath_Python3_*-3_2.so
%{_libdir}/libPyImath.so
%{_includedir}/Imath/PyImath*.h
%{_pkgconfigdir}/PyImath.pc
%endif
