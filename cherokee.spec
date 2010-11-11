%define major 0
%define libbase %mklibname %name-base %major
%define libclient %mklibname %name-client %major
%define libserver %mklibname %name-server %major
%define mainver %(echo %{version} | sed -e "s/\\([0-9]*\\.[0-9]*\\).[0-9]*/\\1/")

Summary:	Extremely fast and flexible web server
Name:		cherokee
Version:	1.0.9
Release:	%mkrel 1
License:	GPLv2
Group:		System/Servers
Source0:	http://www.cherokee-project.com/download/%{mainver}/%{version}/%{name}-%{version}.tar.gz
Source1:	cherokee.init
Source2:	cherokee.logrotate
URL:		http://www.cherokee-project.com/
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	ffmpeg-devel
BuildRequires:	php-devel
%if %mdkversion >= 201000
Buildrequires:	php-cgi
%else
BuildRequires:	php-fcgi
%endif
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	GeoIP-devel
%if %mdkversion >= 201000
Requires:	php-cgi
%else
Requires:	php-fcgi
%endif
Provides:	webserver

%description
Cherokee is an extremely flexible and fast web server. It's embedable,
extensible with plug-ins. It has handler-to-path, virtual servers, gzip
encoding, modular loggers, CGI support, and can run in a chroot
environment, among other features.

%files -f %{name}.lang
%defattr(-, root, root)
%_initrddir/%{name}
%dir %_sysconfdir/cherokee
%config(noreplace) %_sysconfdir/cherokee/cherokee.conf
%_sysconfdir/cherokee/cherokee.conf.perf_sample
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%_bindir/cherokee-tweak
%_bindir/cherokee-panic
%dir %_libdir/%name
%_libdir/%name/*.so
%_sbindir/*
%_datadir/%name
%doc %_datadir/doc/%name
%_mandir/man1/cherokee-admin.*
%_mandir/man1/cherokee-tweak.*
%_mandir/man1/cherokee-worker.*
%_mandir/man1/cherokee.*
%_var/www

#----------------------------------------------------------------------

%package -n cget
Group:		System/Servers
Summary:	Web page downloader

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
%serverbuild
%if %mdkversion < 201000
export PHPCGI=%{_bindir}/php-fcgi
%endif
%configure2_5x --disable-static
%make

%install
rm -rf %buildroot
%makeinstall_std

%find_lang %name

rm -f %buildroot%_libdir/%name/*.la

%{__install} -D -m 0644 pam.d_cherokee %{buildroot}%{_sysconfdir}/pam.d/%{name}
%{__install} -D -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%{__install} -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%clean
rm -rf %buildroot

%check
# broken in 0.99.39
#%make test
