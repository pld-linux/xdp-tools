Summary:	Utilities for use with XDP
Summary(pl.UTF-8):	Narzędzia do używania z XDP
Name:		xdp-tools
Version:	1.4.1
Release:	1
License:	GPL v2, LGPL v2.1, BSD
Group:		Applications/System
#Source0Download: https://github.com/xdp-project/xdp-tools/releases
Source0:	https://github.com/xdp-project/xdp-tools/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	853214d0219f64eee3373e1f1ec69148
Patch0:		%{name}-sh.patch
URL:		https://github.com/xdp-project/xdp-tools
BuildRequires:	clang >= 11
# llc
BuildRequires:	llvm >= 11
BuildRequires:	elfutils-devel
# bpftool
BuildRequires:	kernel-tools >= 4.15
BuildRequires:	libbpf-devel
BuildRequires:	libcap-ng-devel
BuildRequires:	libpcap-devel
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
Requires:	libxdp = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Collection of utilties using libxdp library for working with the
eXpress Data Path facility of the Linux kernel.

%description -l pl.UTF-8
Zestaw narzędzi wykorzystujących bibliotekę libxdp do pracy z funkcją
XDP (eXpress Data Path) jądra Linuksa.

%package -n libxdp
Summary:	Library for use with XDP
Summary(pl.UTF-8):	Biblioteka do używania z XDP
Group:		Libraries

%description -n libxdp
libxdp library for working with the eXpress Data Path facility of the
Linux kernel.

%description -n libxdp -l pl.UTF-8
Biblioteka libxdp do pracy z funkcją XDP (eXpress Data Path) jądra
Linuksa.

%package -n libxdp-devel
Summary:	Header files for libxdp library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libxdp
Group:		Development/Libraries
Requires:	libxdp = %{version}-%{release}

%description -n libxdp-devel
Header files for libxdp library.

%description -n libxdp-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libxdp.

%package -n libxdp-static
Summary:	Static libxdp library
Summary(pl.UTF-8):	Statyczna biblioteka libxdp
Group:		Development/Libraries
Requires:	libxdp-devel = %{version}-%{release}

%description -n libxdp-static
Static libxdp library.

%description -n libxdp-static -l pl.UTF-8
Statyczna biblioteka libxdp.

%prep
%setup -q
%patch0 -p1

%build
BPFTOOL=/usr/sbin/bpftool \
CC="%{__cc}" \
./configure

CFLAGS="%{rpmcflags} %{rpmcppflags}" \
LDFLAGS="%{rpmldflags} %{rpmcflags}" \
%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir}

# tests
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/xdp-tools

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libxdp -p /sbin/ldconfig
%postun	-n libxdp -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE LICENSES/BSD-2-Clause README.org
%attr(755,root,root) %{_sbindir}/xdp-bench
%attr(755,root,root) %{_sbindir}/xdp-filter
%attr(755,root,root) %{_sbindir}/xdp-loader
%attr(755,root,root) %{_sbindir}/xdp-monitor
%attr(755,root,root) %{_sbindir}/xdp-trafficgen
%attr(755,root,root) %{_sbindir}/xdpdump
%{_mandir}/man8/xdp-bench.8*
%{_mandir}/man8/xdp-filter.8*
%{_mandir}/man8/xdp-loader.8*
%{_mandir}/man8/xdp-monitor.8*
%{_mandir}/man8/xdp-trafficgen.8*
%{_mandir}/man8/xdpdump.8*

%files -n libxdp
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxdp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxdp.so.1
%dir %{_libdir}/bpf
%{_libdir}/bpf/xdp-dispatcher.o
%{_libdir}/bpf/xdpdump_*.o
%{_libdir}/bpf/xdpfilt_*.o
%{_libdir}/bpf/xsk_def_xdp_prog*.o

%files -n libxdp-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxdp.so
%{_includedir}/xdp
%{_pkgconfigdir}/libxdp.pc
%{_mandir}/man3/libxdp.3*

%files -n libxdp-static
%defattr(644,root,root,755)
%{_libdir}/libxdp.a
