#
# Conditional build:
%bcond_without	tests		# don't perform "make check"
#
Summary:	Netembryo - tiny network abstraction
Summary(pl.UTF-8):	Netembryo - niewielka warstwa abstrakcji dla sieci
Name:		netembryo
Version:	0.1.1
Release:	3
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://lscube.org/files/downloads/netembryo/%{name}-%{version}.tar.bz2
# Source0-md5:	d5a3c96b37fe3e4fb1c49df1f7a4a16f
Patch0:		%{name}-link.patch
URL:		http://lscube.org/projects/netembryo_network_abstraction_library_feng_and_libnemesi_depend_upon
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	libsctp-devel
BuildRequires:	libtool
BuildRequires:	openssl-devel >= 0.9.8
BuildRequires:	pkgconfig
%if %{with tests}
BuildRequires:	gawk
BuildRequires:	glib2-devel >= 1:2.20
%endif
Requires:	openssl >= 0.9.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Netembryo is a collection of function, ranging from the network
abstraction to the URL string parsing, useful for implementing RTP and
RTSP applications.

Currently the network wrapper (wsocket or wrapped socket) provides
support for TCP, UDP and SCTP.

%description -l pl.UTF-8
Netembryo to zestaw funkcji obejmujących obszar od abstrakcji
sieciowych po przetwarzanie URL-i, przydatnych przy implementowaniu
aplikacji RTP i RTSP.

Obecnie warstwa sieciowa (wsocket - wrapped socket) zapewnia obsługę
TCP, UDP i SCTP.

%package devel
Summary:	Header files for Netembryo library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Netembryo
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libsctp-devel
Requires:	openssl-devel >= 0.9.8

%description devel
Header files for Netembryo library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Netembryo.

%package static
Summary:	Static Netembryo library
Summary(pl.UTF-8):	Statyczna biblioteka Netembryo
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Netembryo library.

%description static -l pl.UTF-8
Statyczna biblioteka Netembryo.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules
%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnetembryo.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_libdir}/libnetembryo.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnetembryo.so.9

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnetembryo.so
%{_includedir}/netembryo
%{_pkgconfigdir}/libnetembryo.pc
%{_pkgconfigdir}/libnetembryo-sctp.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libnetembryo.a
