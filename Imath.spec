Summary:	High dynamic-range (HDR) image file format support libraries
Summary(pl.UTF-8):	Biblioteki obsługujące format plików obrazu o wysokiej dynamice (HDR)
Name:		Imath
Version:	3.1.7
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/AcademySoftwareFoundation/imath/releases
Source0:	https://github.com/AcademySoftwareFoundation/imath/archive/v%{version}/imath-%{version}.tar.gz
# Source0-md5:	5cedab446ab296c080957c3037c6d097
URL:		https://openexr.com/
BuildRequires:	cmake >= 3.12
BuildRequires:	libstdc++-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
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

%description devel
Header files for Imath libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Imath.

%prep
%setup -q

%build
install -d build
cd build
%cmake -G Ninja \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..

%ninja_build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES.md CONTRIBUTORS.md GOVERNANCE.md LICENSE.md README.md SECURITY.md
%attr(755,root,root) %{_libdir}/libImath-3_1.so.30.*.*
%ghost %{_libdir}/libImath-3_1.so.30

%files devel
%defattr(644,root,root,755)
%{_libdir}/libImath-3_1.so
%{_libdir}/libImath.so
%{_includedir}/Imath
%{_libdir}/cmake/Imath
%{_pkgconfigdir}/Imath.pc
