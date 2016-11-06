MESOS_VERSION?=1.0.1

all: build

build: clean
	mkdir build build/SOURCES
	wget -O build/SOURCES/mesos-$(MESOS_VERSION).tar.gz https://archive.apache.org/dist/mesos/$(MESOS_VERSION)/mesos-$(MESOS_VERSION).tar.gz
	rpmbuild --define "_topdir $(PWD)/build" -bb SPECS/mesos.spec 2>&1 | tee build.log

clean:
	rm -rf build build.log 2>/dev/null || true
