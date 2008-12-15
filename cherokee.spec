%define major 0
%define libbase %mklibname %name-base %major
%define libclient %mklibname %name-client %major
%define libconfig %mklibname %name-config %major
%define libserver %mklibname %name-server %major

Summary:	Extremely fast and flexible web server
Name:     	cherokee
Version:	0.11.3
Release:	%mkrel 1
License:	GPLv2
Group:		System/Servers
Source0: 	http://www.cherokee-project.com/download/0.11/%version/%name-%version.tar.gz
Source1:	cherokee.init
Source2:	cherokee.logrotate
URL:		http://www.cherokee-project.com/
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	php-devel
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	GeoIP-devel
Suggests:	%name-server = %version

%description
Cherokee is an extremely flexible and fast web server. It's embedable,
extensible with plug-ins. It has handler-to-path, virtual servers, gzip
encoding, modular loggers, CGI support, and can run in a chroot
environment, among other features.

%files
%defattr(-, root, root)
%_initrddir/%{name}
%_sysconfdir/cherokee
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%_bindir/cherokee-tweak
%_bindir/cherokee-panic
%_bindir/spawn-fcgi
%dir %_libdir/%name
%_libdir/%name/*.so
%_sbindir/*
%_datadir/%name
%doc %_datadir/doc/%name
%_libdir/%name/*.so
%_mandir/man1/cherokee-admin.*
%_mandir/man1/cherokee-tweak.*
%_mandir/man1/cherokee-worker.*
%_mandir/man1/cherokee.*
%_mandir/man1/spawn-fcgi.*
%_var/www

#----------------------------------------------------------------------

%package -n cget
Group:          System/Servers
Summary:        Web page downloader

%description -n cget
CGet is a small downloader based in the Cherokee client library.

%files -n cget
%defattr(-, root, root)
%{_bindir}/cget
%{_mandir}/man1/cget.*

#----------------------------------------------------------------------

%package -n %libbase
Group:		System/Servers
Summary:	Extremely fast and flexible web server - libraries

%description -n %libbase
Cherokee is an extremely flexible and fast web server. It's embedable,
extensible with plug-ins. It has handler-to-path, virtual servers, gzip
encoding, modular loggers, CGI support, and can run in a chroot
environment, among other features.

This is the runtime library.

%files -n %libbase
%defattr(-, root, root)
%{_libdir}/libcherokee-base.so.%{major}*

#----------------------------------------------------------------------

%package -n %libclient
Group:		System/Servers
Summary:	Extremely fast and flexible web server - libraries

%description -n %libclient
Cherokee is an extremely flexible and fast web server. It's embedable,
extensible with plug-ins. It has handler-to-path, virtual servers, gzip
encoding, modular loggers, CGI support, and can run in a chroot
environment, among other features.

This is the client runtime library.

%files -n %libclient
%defattr(-, root, root)
%{_libdir}/libcherokee-client.so.%{major}*

#----------------------------------------------------------------------

%package -n %libconfig
Group:		System/Servers
Summary:	Extremely fast and flexible web server - libraries

%description -n %libconfig
Cherokee is an extremely flexible and fast web server. It's embedable,
extensible with plug-ins. It has handler-to-path, virtual servers, gzip
encoding, modular loggers, CGI support, and can run in a chroot
environment, among other features.

This is the configuration handler's runtime library.

%files -n %libconfig
%defattr(-, root, root)
%{_libdir}/libcherokee-config.so.%{major}*

#----------------------------------------------------------------------

%package -n %libserver
Group:		System/Servers
Summary:	Extremely fast and flexible web server - libraries

%description -n %libserver
Cherokee is an extremely flexible and fast web server. It's embedable,
extensible with plug-ins. It has handler-to-path, virtual servers, gzip
encoding, modular loggers, CGI support, and can run in a chroot
environment, among other features.

This is the server runtime library.

%files -n %libserver
%defattr(-, root, root)
%{_libdir}/libcherokee-server.so.%{major}*

#----------------------------------------------------------------------

%package devel
Group:		System/Servers
Requires:	%libbase = %version
Requires:	%libclient = %version
Requires:	%libconfig = %version
Requires:	%libserver = %version
Summary:	Extremely fast and flexible web server - development files

%description devel
Cherokee is an extremely flexible and fast web server. It's embedable,
extensible with plug-ins. It has handler-to-path, virtual servers, gzip
encoding, modular loggers, CGI support, and can run in a chroot
environment, among other features.

This package contains the server development files - headers, .so and .a files.

%files devel
%defattr(-, root, root)
%_bindir/%name-config
%_libdir/*.la
%_libdir/*.so
%_includedir/%name
%_libdir/pkgconfig/*.pc
%_datadir/aclocal/*.m4
%_mandir/man1/%name-config.*

#----------------------------------------------------------------------
%prep
%setup -q -n %name-%version

%build
%configure2_5x --disable-static
%make

%install
rm -rf %buildroot
%makeinstall_std

rm -f %buildroot%_libdir/%name/*.la

%{__install} -D -m 0644 pam.d_cherokee %{buildroot}%{_sysconfdir}/pam.d/%{name}
%{__install} -D -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%{__install} -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%clean
rm -rf %buildroot
