MESOS_VERSION?=1.0.1
JAVA_VERSION?=1.8.0
JAVA_HOME?=/usr/lib/jvm/java-$(JAVA_VERSION)

all: build

build: clean
	mkdir build build/SOURCES
	wget -O build/SOURCES/mesos-$(MESOS_VERSION).tar.gz https://archive.apache.org/dist/mesos/$(MESOS_VERSION)/mesos-$(MESOS_VERSION).tar.gz
	rpmbuild --define "_topdir $(PWD)/build" --define "version $(MESOS_VERSION)" --define "java_home $(JAVA_HOME)" -bb SPECS/mesos.spec 2>&1 | tee build.log

clean:
	rm -rf build build.log 2>/dev/null || true
