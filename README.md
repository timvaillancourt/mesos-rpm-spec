# mesos-rpm-spec
RPM spec file(s) for Apache Mesos

## Building
```
git clone https://github.com/timvaillancourt/mesos-rpm-spec
cd mesos-rpm-spec
make
# or, for a specific mesos version:
make MESOS_VERSION=0.28.0
# or, for a specific java:
make JAVA_HOME=/path/to/java
```

### Build Dependencies
1. 'rpmbuild' command (*provided by 'rpm-build' package*)
2.  The dependencies listed as 'BuildRequires:' lines in SPECS/mesos.spec.

## Contact
- Tim Vaillancourt - [Github](https://github.com/timvaillancourt), [Email](mailto:tim.vaillancourt@percona.com)
