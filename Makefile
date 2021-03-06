## makefile for debian packaging

PYTHON=`which python`
DESTDIR=/
BUILDIR=$(CURDIR)/debian/splitsingleflac
PROJECT=splitsingleflac
VERSION=0.4
PREFIX=/usr

all:
	@echo 'make builddeb - Generate a deb package'
	@echo 'make source - Create source package'
	@echo 'make clean - Get rid of scratch and byte files'

source:
	$(PYTHON) setup.py sdist $(COMPILE)

install:
	$(PYTHON) setup.py install --root $(DESTDIR) \
	--single-version-externally-managed \
	--prefix=$(PREFIX) \
        --no-compile
	# install the desktop file
	desktop-file-install --dir=$(DESTDIR)$(PREFIX)/share/applications splitsingleflac.desktop

builddeb:
	# build the source package in the parent directory
        # then rename it to project_version.orig.tar.gz
	$(PYTHON) setup.py sdist --dist-dir=../
	rename -f 's/$(PROJECT)-(.*)\.tar\.gz/$(PROJECT)_$$1\.orig\.tar\.gz/' ../*
	# build the package
	dpkg-buildpackage -i -I -rfakeroot


clean:
	$(PYTHON) setup.py clean
	rm -rf build/ MANIFEST
	rm -r src/splitsingleflac.egg-info
	find . -name '*.pyc' -delete
