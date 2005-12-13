Summary:	Script to start and stop PHP FastCGI processes
Summary(pl):	Skrypt do uruchamiania i zatrzymywania procesów FastCGI PHP
Name:		php-fcgi-init
Version:	0.1
Release:	1
License:	BSD-like
Group:		Networking/Daemons
Source0:	php-fcgi.init
Source1:	php-fcgi.sysconfig
Requires(post,preun):	/sbin/chkconfig
Requires:	php-fcgi
Requires:	rc-scripts
Requires:	spawn-fcgi
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Script to start and stop PHP FastCGI processes.

%description -l pl
Skrypt do uruchamiania i zatrzymywania procesów FastCGI PHP

%prep

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

install %{SOURCE0} $RPM_BUILD_ROOT/etc/rc.d/init.d/php-fcgi
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/php-fcgi

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add php-fcgi
if [ -f /var/lock/subsys/php-fcgi ]; then
	/etc/rc.d/init.d/php-fcgi restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/php-fcgi start\" to start PHP FastCGI."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/php-fcgi ]; then
		/etc/rc.d/init.d/php-fcgi stop 1>&2
	fi
	/sbin/chkconfig --del php-fcgi
fi

%files
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/php-fcgi
%config(noreplace) %verify(not md5 mtime size) %attr(600,root,root) /etc/sysconfig/php-fcgi
