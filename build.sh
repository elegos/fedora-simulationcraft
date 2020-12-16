#!/usr/bin/env bash

proj="cli gui"
if [ "$1" != "" ]; then
  proj="$1"
fi

rpmdev-setuptree
rm -rf ~/rpmbuild/SOURCES/*
cp spec/*.patch ~/rpmbuild/SOURCES/

set -e

for prj in $proj; do 
  rpmbuild -ba spec/simulationcraft-${proj}-nightly.spec
done
