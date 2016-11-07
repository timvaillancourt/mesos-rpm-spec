# mesos-rpm-spec
RPM spec file(s) for Apache Mesos

## Building
```
git clone https://github.com/timvaillancourt/mesos-rpm-spec
cd mesos-rpm-spec
make MESOS_VERSION=1.0.1
# or, for a specific java:
make MESOS_VERSION=1.0.1 JAVA_HOME=/path/to/java
```

### Build Dependencies
1. 'rpmbuild' command (*provided by 'rpm-build' package*).
2. The dependencies listed as 'BuildRequires:' lines in SPECS/mesos.spec.
3. 'java-1.8.0-openjdk' package or custom Java path specified via *"make JAVA_HOME="*.

## Contact
- Tim Vaillancourt - [Github](https://github.com/timvaillancourt), [Email](mailto:tim.vaillancourt@percona.com)
