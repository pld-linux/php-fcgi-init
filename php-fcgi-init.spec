Summary:	Script to start and stop PHP FastCGI processes
Summary(pl.UTF-8):	Skrypt do uruchamiania i zatrzymywania procesów FastCGI PHP
Name:		php-fcgi-init
Version:	0.6
Release:	2
License:	BSD-like
Group:		Networking/Daemons
Source0:	php-fcgi.init
Source1:	php-fcgi.sysconfig
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires:	php(fcgi)
Requires:	rc-scripts
Requires:	spawn-fcgi >= 1.4.19-9
Provides:	user(http)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Script to start and stop PHP FastCGI processes.

%description -l pl.UTF-8
Skrypt do uruchamiania i zatrzymywania procesów FastCGI PHP

%prep

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}
install -p %{SOURCE0} $RPM_BUILD_ROOT/etc/rc.d/init.d/php-fcgi
cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/php-fcgi

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd -u 51 -r -s /bin/false -c "HTTP User" -g http http

%post
/sbin/chkconfig --add php-fcgi
# there's no point of restarting php-fcgi as this package contains only scripts
# therefore nothing has changed in memory and restart would be pointless

%preun
if [ "$1" = "0" ]; then
	%service php-fcgi stop
	/sbin/chkconfig --del php-fcgi
fi

%postun
if [ "$1" = "0" ]; then
	%userremove http
fi

%files
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/php-fcgi
%config(noreplace) %verify(not md5 mtime size) %attr(600,root,root) /etc/sysconfig/php-fcgi
