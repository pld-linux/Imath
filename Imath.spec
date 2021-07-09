Summary:	High dynamic-range (HDR) image file format support libraries
Summary(pl.UTF-8):	Biblioteki obsługujące format plików obrazu o wysokiej dynamice (HDR)
Name:		Imath
Version:	3.0.5
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://github.com/AcademySoftwareFoundation/imath/archive/v%{version}/imath-%{version}.tar.gz
# Source0-md5:	d2d5415f177f6bec9c2f3c3180741179
URL:		http://www.openexr.com/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1.6.3
BuildRequires:	cmake
BuildRequires:	ilmbase-devel >= 2.2.1
BuildRequires:	libstdc++-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
Requires:	ilmbase >= 2.2.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Imath is a basic, light-weight, and efficient C++ representation of 2D
and 3D vectors and matrices and other simple but useful mathematical
objects, functions, and data types common in computer graphics
applications, including the “half” 16-bit floating-point type.

%description -l pl.UTF-8
Imath to prosta, lekka i wydajna reprezentacja C++ dwu- i
trójwymiarowych wektorów i macierzy i inne proste, ale użyteczne
matematyczne obiekty, funkcje i typy danych zwykle występujące w
programach graficznych, w tym "półówkowy" 16 bitowy typ
zmiennoprzecinkowy.

%package devel
Summary:	Header files for Imath libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Imath
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ilmbase-devel >= 2.2.1
Requires:	libstdc++-devel
Requires:	zlib-devel

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
%ninja_install -C build install

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%ghost %{_libdir}/libImath-3_0.so.28
%attr(755,root,root) %{_libdir}/libImath-3_0.so.28.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/Imath
%{_libdir}/cmake/Imath
%{_libdir}/libImath-3_0.so
%{_libdir}/libImath.so
%{_pkgconfigdir}/Imath.pc
