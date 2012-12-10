%define major 0
%define libbase %mklibname %name-base %major
%define libclient %mklibname %name-client %major
%define libserver %mklibname %name-server %major
%define mainver %(echo %{version} | sed -e "s/\\([0-9]*\\.[0-9]*\\).[0-9]*/\\1/")

Summary:	Extremely fast and flexible web server
Name:		cherokee
Version:	1.2.101
Release:	1
License:	GPLv2
Group:		System/Servers
Source0:	http://www.cherokee-project.com/download/%{mainver}/%{version}/%{name}-%{version}.tar.gz
Source1:	cherokee.init
Source2:	cherokee.logrotate
Patch0:		cherokee-1.2.101-rosa-linkage.patch
URL:		http://www.cherokee-project.com/
BuildRequires:	ffmpeg0.7-devel
BuildRequires:	php-devel
BuildRequires:	php-fpm
Requires:	php-fpm
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	GeoIP-devel
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Provides:	webserver
Provides:	%mklibname %name-config %major
Obsoletes:	%mklibname %name-config 0

%description
Cherokee is an extremely flexible and fast web server. It's embedable,
extensible with plug-ins. It has handler-to-path, virtual servers, gzip
encoding, modular loggers, CGI support, and can run in a chroot
environment, among other features.

%files -f %{name}.lang
%_initrddir/%{name}
%dir %_sysconfdir/cherokee
%config(noreplace) %_sysconfdir/cherokee/cherokee.conf
%_sysconfdir/cherokee/cherokee.conf.perf_sample
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%_bindir/cherokee-admin-launcher
%_bindir/cherokee-macos-askpass
%_bindir/cherokee-panic
%_bindir/cherokee-tweak
%_bindir/CTK-run
%dir %_libdir/%name
%_libdir/%name/*.so
%_sbindir/*
%_datadir/%name
%doc %_datadir/doc/%name
%_mandir/man1/cherokee-admin.*
%_mandir/man1/cherokee-admin-launcher.*
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
%_libdir/*.so
%_includedir/%name
%_libdir/pkgconfig/*.pc
%_datadir/aclocal/*.m4
%_mandir/man1/%name-config.*

#----------------------------------------------------------------------
%prep
%setup -q -n %name-%version
%patch0 -p1
touch ./INSTALL

%build
autoreconf
%serverbuild
%configure2_5x --disable-static
%make

%install
%makeinstall_std

mv %{buildroot}%{_datadir}/locale/jp %{buildroot}%{_datadir}/locale/ja
%find_lang %name

%{__install} -D -m 0644 pam.d_cherokee %{buildroot}%{_sysconfdir}/pam.d/%{name}
%{__install} -D -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%{__install} -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%{buildroot}%{_datadir}/%{name}/admin/upgrade_config.py %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
rm -f %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf.backup

%check
# broken in 0.99.39
#%make test

%post
[[ -e %{_sysconfdir}/%{name}/%{name}.conf ]] && %{_datadir}/%{name}/admin/upgrade_config.py %{_sysconfdir}/%{name}/%{name}.conf

%_post_service

%preun
%_preun_service


%changelog
* Thu May 26 2011 Lonyai Gergely <aleph@mandriva.org> 1.2.98-1mdv2011.0
+ Revision: 679155
- 1.2.98

* Mon Mar 21 2011 Lonyai Gergely <aleph@mandriva.org> 1.2.2-1
+ Revision: 647389
- 1.2.2

* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2.1-3
+ Revision: 645778
- relink against libmysqlclient.so.18

* Sun Mar 13 2011 Funda Wang <fwang@mandriva.org> 1.2.1-2
+ Revision: 644116
- prefer php-fpm over php-cgi

* Thu Feb 24 2011 Lonyai Gergely <aleph@mandriva.org> 1.2.1-1
+ Revision: 639623
- 1.2.1

* Tue Feb 22 2011 Lonyai Gergely <aleph@mandriva.org> 1.2.0-1
+ Revision: 639302
- 1.2.0

* Thu Feb 03 2011 Lonyai Gergely <aleph@mandriva.org> 1.0.20-1
+ Revision: 635446
- 1.0.20

* Mon Jan 31 2011 Lonyai Gergely <aleph@mandriva.org> 1.0.19-1
+ Revision: 634579
- 1.0.19

* Thu Jan 20 2011 Lonyai Gergely <aleph@mandriva.org> 1.0.18-1
+ Revision: 631868
- 1.0.18

* Wed Jan 12 2011 Lonyai Gergely <aleph@mandriva.org> 1.0.16-1
+ Revision: 630959
- 1.0.16

* Sat Jan 01 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.15-4mdv2011.0
+ Revision: 627216
- rebuilt against mysql-5.5.8 libs, again

* Thu Dec 30 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.15-3mdv2011.0
+ Revision: 626510
- rebuilt against mysql-5.5.8 libs

* Thu Dec 30 2010 Funda Wang <fwang@mandriva.org> 1.0.15-1mdv2011.0
+ Revision: 626270
- new version 1.0.15

* Tue Dec 14 2010 Funda Wang <fwang@mandriva.org> 1.0.14-1mdv2011.0
+ Revision: 621747
- update file list
- new version 1.0.14

* Fri Dec 10 2010 Lonyai Gergely <aleph@mandriva.org> 1.0.13-1mdv2011.0
+ Revision: 620436
- 1.0.13

* Wed Dec 01 2010 Lonyai Gergely <aleph@mandriva.org> 1.0.12-1mdv2011.0
+ Revision: 604627
- 1.0.12

* Thu Nov 25 2010 Lonyai Gergely <aleph@mandriva.org> 1.0.10-1mdv2011.0
+ Revision: 601168
- New file: CTK-run
- 1.0.10

* Thu Nov 11 2010 Lonyai Gergely <aleph@mandriva.org> 1.0.9-2mdv2011.0
+ Revision: 595948
- Provide libcherokee-config
- Drop package: libcherokee-config
- 1.0.9

* Tue Nov 02 2010 Rémy Clouard <shikamaru@mandriva.org> 1.0.8-2mdv2011.0
+ Revision: 592563
- make cherokee provide webserver

* Thu Aug 12 2010 Lonyai Gergely <aleph@mandriva.org> 1.0.8-1mdv2011.0
+ Revision: 569211
- 1.0.8

* Mon Aug 09 2010 Funda Wang <fwang@mandriva.org> 1.0.7-1mdv2011.0
+ Revision: 568058
- new version 1.0.7

* Wed Aug 04 2010 Lonyai Gergely <aleph@mandriva.org> 1.0.6-1mdv2011.0
+ Revision: 565879
- 1.0.6

* Wed Jul 07 2010 Lonyai Gergely <aleph@mandriva.org> 1.0.5-1mdv2011.0
+ Revision: 549843
- 1.0.5
- 1.0.4
- 1.0.2
- 1.0.1

* Tue May 18 2010 Funda Wang <fwang@mandriva.org> 1.0.0-1mdv2010.1
+ Revision: 545086
- New version 1.0.0 stable

  + Lonyai Gergely <aleph@mandriva.org>
    - 0.99.48

* Tue May 04 2010 Funda Wang <fwang@mandriva.org> 0.99.45-2mdv2010.1
+ Revision: 541909
- sync with fedora initfile (suppress confusing output)

* Mon Apr 26 2010 Funda Wang <fwang@mandriva.org> 0.99.45-1mdv2010.1
+ Revision: 538916
- update to new version 0.99.45

* Tue Apr 13 2010 Funda Wang <fwang@mandriva.org> 0.99.44-2mdv2010.1
+ Revision: 534175
- rebuild

* Sun Mar 28 2010 Sandro Cazzaniga <kharec@mandriva.org> 0.99.44-1mdv2010.1
+ Revision: 528476
- update to 0.99.44

* Thu Feb 18 2010 Oden Eriksson <oeriksson@mandriva.com> 0.99.43-2mdv2010.1
+ Revision: 507479
- rebuild

* Thu Feb 18 2010 Funda Wang <fwang@mandriva.org> 0.99.43-1mdv2010.1
+ Revision: 507368
- update to new version 0.99.43

* Thu Jan 28 2010 Frederik Himpe <fhimpe@mandriva.org> 0.99.42-1mdv2010.1
+ Revision: 497853
- update to new version 0.99.42

* Wed Jan 27 2010 Funda Wang <fwang@mandriva.org> 0.99.41-1mdv2010.1
+ Revision: 497174
- new version 0.99.41

* Tue Dec 29 2009 Frederik Himpe <fhimpe@mandriva.org> 0.99.39-1mdv2010.1
+ Revision: 483297
- Update to new version 0.99.39

* Thu Dec 24 2009 Funda Wang <fwang@mandriva.org> 0.99.38-1mdv2010.1
+ Revision: 482038
- new version 0.99.38

* Thu Dec 17 2009 Funda Wang <fwang@mandriva.org> 0.99.37-1mdv2010.1
+ Revision: 479620
- new verison 0.99.37

* Sun Dec 13 2009 Funda Wang <fwang@mandriva.org> 0.99.35-1mdv2010.1
+ Revision: 478132
- new version 0.99.35

* Sat Dec 12 2009 Funda Wang <fwang@mandriva.org> 0.99.34-1mdv2010.1
+ Revision: 477741
- new version 0.99.34

* Thu Dec 10 2009 Frederik Himpe <fhimpe@mandriva.org> 0.99.32-1mdv2010.1
+ Revision: 476113
- update to new version 0.99.32

* Thu Dec 03 2009 Funda Wang <fwang@mandriva.org> 0.99.31-1mdv2010.1
+ Revision: 472870
- new version 0.99.31

* Mon Nov 30 2009 Funda Wang <fwang@mandriva.org> 0.99.30-1mdv2010.1
+ Revision: 471782
- new version 0.99.30
- add ifarg

* Sun Nov 29 2009 Funda Wang <fwang@mandriva.org> 0.99.29-2mdv2010.1
+ Revision: 471453
- fcgi has been merged in cgi since php 5.3.1 (>= 2010)
- use fastcgi support

* Fri Nov 20 2009 Frederik Himpe <fhimpe@mandriva.org> 0.99.29-1mdv2010.1
+ Revision: 467674
- update to new version 0.99.29

* Tue Nov 17 2009 Frederik Himpe <fhimpe@mandriva.org> 0.99.28-1mdv2010.1
+ Revision: 467024
- update to new version 0.99.28

* Fri Nov 06 2009 Frederik Himpe <fhimpe@mandriva.org> 0.99.27-1mdv2010.1
+ Revision: 462038
- update to new version 0.99.27

* Tue Sep 01 2009 Frederik Himpe <fhimpe@mandriva.org> 0.99.24-1mdv2010.0
+ Revision: 423675
- update to new version 0.99.24

* Wed Aug 05 2009 Frederik Himpe <fhimpe@mandriva.org> 0.99.22-1mdv2010.0
+ Revision: 410298
- update to new version 0.99.22

* Wed Jul 01 2009 Frederik Himpe <fhimpe@mandriva.org> 0.99.20-1mdv2010.0
+ Revision: 391357
- update to new version 0.99.20

* Thu Jun 25 2009 Frederik Himpe <fhimpe@mandriva.org> 0.99.19-1mdv2010.0
+ Revision: 389196
- update to new version 0.99.19

* Mon Jun 22 2009 Frederik Himpe <fhimpe@mandriva.org> 0.99.18-1mdv2010.0
+ Revision: 388053
- update to new version 0.99.18

* Sun Jun 14 2009 Frederik Himpe <fhimpe@mandriva.org> 0.99.17-1mdv2010.0
+ Revision: 385846
- update to new version 0.99.17

* Wed Jun 10 2009 Frederik Himpe <fhimpe@mandriva.org> 0.99.16-1mdv2010.0
+ Revision: 384902
- update to new version 0.99.16

* Wed May 13 2009 Frederik Himpe <fhimpe@mandriva.org> 0.99.15-1mdv2010.0
+ Revision: 375515
- Update to new version 0.99.15

* Wed May 06 2009 Frederik Himpe <fhimpe@mandriva.org> 0.99.14-1mdv2010.0
+ Revision: 372658
- Update to new version 0.99.14
- Fix source URL

* Fri May 01 2009 Funda Wang <fwang@mandriva.org> 0.99.13-1mdv2010.0
+ Revision: 369395
- New version 0.99.13

* Fri May 01 2009 Funda Wang <fwang@mandriva.org> 0.99.11-1mdv2010.0
+ Revision: 369353
- New version 0.99.11

* Mon Mar 30 2009 Funda Wang <fwang@mandriva.org> 0.99.4-2mdv2009.1
+ Revision: 362425
- fix initscript typo

* Fri Mar 13 2009 Frederik Himpe <fhimpe@mandriva.org> 0.99.4-1mdv2009.1
+ Revision: 354689
- Update to new version 0.99.4
- Use %%serverbuild macro

* Tue Jan 27 2009 Funda Wang <fwang@mandriva.org> 0.98.1-1mdv2009.1
+ Revision: 334167
- new version 0.98.1

* Sat Jan 24 2009 Funda Wang <fwang@mandriva.org> 0.98.0-1mdv2009.1
+ Revision: 333183
- 0.98.0
- New version 0.11.5
- there is no server subpackage
- add init and logrotate
- add manpages
- add cget
- import cherokee


