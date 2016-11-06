%define debug_package	%{nil}
%define java_ver	1.8.0
%define	java_home	/usr/lib/jvm/java-%{java_ver}
%define data_dir	/var/lib/mesos
%define run_dir		/var/run/mesos
%define log_dir		/var/log/mesos
%define mesos_user	mesos
%define mesos_group	mesos

Name:		mesos
Version:	1.0.1
Release:	1%{?dist}
Summary:	Apache Mesos - A distributed systems kernel
Group:		Software/Clustering
License:	Apache License 2.0
URL:		https://mesos.apache.org
Source0:	mesos-%{version}.tar.gz
Prefix:		/usr

BuildRequires:	apr-devel
BuildRequires:  cyrus-sasl-devel
BuildRequires:  cyrus-sasl-md5
BuildRequires:  java-%{java_ver}-openjdk
BuildRequires:  java-%{java_ver}-openjdk-devel
BuildRequires:  libcurl-devel
BuildRequires:  maven
BuildRequires:  openssl-devel
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-virtualenv
BuildRequires:  subversion-devel
BuildRequires:	systemd
BuildRequires:  zlib-devel


%description
Apache Mesos - A distributed systems kernel


%package devel
Summary:	Apache Mesos - A distributed systems kernel - Devel Package


%description devel
Apache Mesos - A distributed systems kernel - Devel Package


%prep
%setup -q


%build
virtualenv venv
source venv/bin/activate
export JAVA_HOME=%{java_home}
export JAVA=%{java_home}/bin/java
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

# move /etc/mesos/*-env.sh.template -> /etc/sysconfig
mv %{buildroot}%{_sysconfdir}/mesos %{buildroot}%{_sysconfdir}/sysconfig
pushd %{buildroot}%{_sysconfdir}/sysconfig
  mv mesos-agent-env.sh.template  mesos-agent
  mv mesos-deploy-env.sh.template mesos-deploy
  mv mesos-master-env.sh.template mesos-master
  mv mesos-slave-env.sh.template  mesos-slave
popd

mkdir -p %{buildroot}/usr/lib/systemd/system
%{__cat} <<EOF >%{buildroot}/usr/lib/systemd/system/mesos-master.service
[Unit]
Description=Mesos - A distributed systems kernel
After=time-sync.target network.target

[Service]
Type=forking
User=%{mesos_user}
Group=%{mesos_group}
PermissionsStartOnly=true
EnvironmentFile=/etc/sysconfig/mesos-master
ExecStart=/usr/bin/env bash -c "%{_sbindir}/mesos-master --work_dir=%{data_dir}/master --log_dir=%{log_dir} & echo \$! >%{run_dir}/mesos-master.pid; disown \$!"
PIDFile=%{run_dir}/mesos-master.pid

[Install]
WantedBy=multi-user.target
EOF

%{__cat} <<EOF >%{buildroot}/usr/lib/systemd/system/mesos-slave.service
[Unit]
Description=Mesos - A distributed systems kernel
After=time-sync.target network.target

[Service]
Type=forking
User=%{mesos_user}
Group=%{mesos_group}
PermissionsStartOnly=true
EnvironmentFile=/etc/sysconfig/mesos-slave
ExecStart=/usr/bin/env bash -c "%{_sbindir}/mesos-slave --work_dir=%{data_dir}/slave --log_dir=%{log_dir} & echo \$! >%{run_dir}/mesos-slave.pid; disown \$!"
PIDFile=%{run_dir}/mesos-slave.pid

[Install]
WantedBy=multi-user.target
EOF


%pre
getent group %{mesos_group} >/dev/null || groupadd -r %{mesos_group}
getent passwd %{mesos_user} >/dev/null || useradd --comment "Mesos Daemon User" -r -g %{mesos_group} -s /sbin/nologin %{mesos_user}


%post
# install
if [ $1 = 0 ]; then
  for dir in "%{data_dir}" "%{data_dir}/master" "%{data_dir}/slave" "%{log_dir}" "%{run_dir}"; do
    [ ! -e "$dir" ] && mkdir $dir
  done
  chmod 0750 %{data_dir}
  chown -R %{mesos_user}:%{mesos_group} %{data_dir} %{log_dir} %{run_dir}
fi

# upgrade
if [ $1 = 1 ]; then
  for service in "mesos-master" "mesos-slave"; do
    systemctl status $service 2>/dev/null || true
    if [ $? = 0 ]; then
      echo "# Restarting $service..."
      /usr/bin/systemctl restart $service || true
    fi
  done
fi

/usr/bin/systemctl daemon-reload


%preun
# uninstall
if [ $1 = 0 ]; then
  echo "# Stopping/disabling mesos services..."
  for service in "mesos-slave" "mesos-master"; do
    systemctl status $service 2>/dev/null || true
    if [ $? = 0 ]; then
      /usr/bin/systemctl stop $service >/dev/null 2>&1 || true
    fi
    /usr/bin/systemctl disable $service >/dev/null 2>&1 || true
  done
fi


%postun
# uninstall
if [ $1 = 0 ]; then
  /usr/bin/systemctl daemon-reload
fi


%files
%{_sysconfdir}/sysconfig/mesos-*
%{prefix}/bin/*
%{prefix}/lib/*
%{prefix}/lib64/*
%{prefix}/libexec/*
%{prefix}/sbin/*
%{prefix}/share/*


%files devel
%{prefix}/include/*


%changelog

