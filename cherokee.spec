%define major 0
%define libbase %mklibname %{name}-base %{major}
%define libclient %mklibname %{name}-client %{major}
%define libserver %mklibname %{name}-server %{major}
%define mainver %(echo %{version} | sed -e "s/\\([0-9]*\\.[0-9]*\\).[0-9]*/\\1/")

Summary:	Extremely fast and flexible web server
Name:		cherokee
Version:	1.2.101
Release:	8
License:	GPLv2
Group:		System/Servers
Source0:	http://www.cherokee-project.com/download/%{mainver}/%{version}/%{name}-%{version}.tar.gz
Source1:	cherokee.service
Source2:	cherokee.logrotate
Patch0:		cherokee-1.2.101-rosa-linkage.patch
Patch1:		cherokee-1.2.101-ffmpeg0.11.patch
URL:		https://www.cherokee-project.com/
BuildRequires:	ffmpeg-devel
BuildRequires:	php-devel
BuildRequires:	php-fpm
Requires:	php-fpm
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig(geoip)
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Provides:	webserver
Provides:	%mklibname %{name}-config %{major}
Obsoletes:	%mklibname %{name}-config 0

%description
Cherokee is an extremely flexible and fast web server. It's embedable,
extensible with plug-ins. It has handler-to-path, virtual servers, gzip
encoding, modular loggers, CGI support, and can run in a chroot
environment, among other features.

%files -f %{name}.lang
%{_unitdir}/%{name}*
%dir %{_sysconfdir}/cherokee
%config(noreplace) %{_sysconfdir}/cherokee/cherokee.conf
%{_sysconfdir}/cherokee/cherokee.conf.perf_sample
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_bindir}/cherokee-admin-launcher
%{_bindir}/cherokee-macos-askpass
%{_bindir}/cherokee-panic
%{_bindir}/cherokee-tweak
%{_bindir}/CTK-run
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%{_sbindir}/*
%{_datadir}/%{name}
%doc %{_datadir}/doc/%{name}
%{_mandir}/man1/cherokee-admin.*
%{_mandir}/man1/cherokee-admin-launcher.*
%{_mandir}/man1/cherokee-tweak.*
%{_mandir}/man1/cherokee-worker.*
%{_mandir}/man1/cherokee.*
%_var/www

#----------------------------------------------------------------------

%package -n cget
Group:		System/Servers
Summary:	Web page downloader

%description -n cget
CGet is a small downloader based in the Cherokee client library.

%files -n cget
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
%{_libdir}/libcherokee-server.so.%{major}*

#----------------------------------------------------------------------

%package devel
Group:		System/Servers
Requires:	%libbase = %{version}
Requires:	%libclient = %{version}
Requires:	%libserver = %{version}
Summary:	Extremely fast and flexible web server - development files

%description devel
Cherokee is an extremely flexible and fast web server. It's embedable,
extensible with plug-ins. It has handler-to-path, virtual servers, gzip
encoding, modular loggers, CGI support, and can run in a chroot
environment, among other features.

This package contains the server development files - headers, .so and .a files.

%files devel
%{_bindir}/%{name}-config
%{_libdir}/*.so
%{_includedir}/%{name}
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/*.m4
%{_mandir}/man1/%{name}-config.*

#----------------------------------------------------------------------
%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p0
touch ./INSTALL

%build
autoreconf -i
%serverbuild
%configure2_5x --disable-static
%make

%install
%makeinstall_std

mv %{buildroot}%{_datadir}/locale/jp %{buildroot}%{_datadir}/locale/ja
%find_lang %{name}

%{__install} -D -m 0644 pam.d_cherokee %{buildroot}%{_sysconfdir}/pam.d/%{name}
%{__install} -D -m 0755 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
%{__install} -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%{buildroot}%{_datadir}/%{name}/admin/upgrade_config.py %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
rm -f %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf.backup

%check
# broken in 0.99.39
#%make test

%post
[[ -e %{_sysconfdir}/%{name}/%{name}.conf ]] && %{_datadir}/%{name}/admin/upgrade_config.py %{_sysconfdir}/%{name}/%{name}.conf
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
