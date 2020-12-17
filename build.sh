#!/usr/bin/env bash

proj="cli gui"
if [ "$1" != "" ]; then
  proj="$1"
fi

rpmdev-setuptree

set -e
for prj in $proj; do 
  rm -rf ~/rpmbuild/SOURCES/*
  rm -rf ~/rpmbuild/BUILD/*
  cp -rf simulationcraft-${proj}/* ~/rpmbuild/SOURCES/
  rpmbuild -ba simulationcraft-${proj}/simulationcraft-${proj}-nightly.spec
done
