Summary:	Script to start and stop PHP FastCGI processes
Name:		php-fcgi-init
Version:	0.1
Release:	1
License:	BSD-like
Group:	Networking/Daemons
Source0:	php-fcgi.init
Source1:	php-fcgi.sysconfig
PreReq:	rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	php-fcgi
Requires:	spawn-fcgi
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Script to start and stop PHP FastCGI processes

%prep

%build

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
%attr(744,root,root) /etc/rc.d/init.d/php-fcgi
%config(noreplace) %attr(600,root,root) /etc/sysconfig/php-fcgi
