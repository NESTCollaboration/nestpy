#!/bin/bash
set -e -x

# Install a system package required by our library
yum install -y atlas-devel

# Manual install cmake since Centos5 old and pip somehow didn't work
ls
pwd
wget https://cmake.org/files/v3.12/cmake-3.12.1-Linux-x86_64.sh
chmod +x cmake-3.12.1-Linux-x86_64.sh
./cmake-3.12.1-Linux-x86_64.sh --skip-license
export PATH=$PATH:`pwd`/bin

# Compile wheels
for PYBIN in /opt/python/*/bin; do
    "${PYBIN}/pip" install -r /io/requirements_dev.txt
    "${PYBIN}/pip" wheel /io/ -w wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" -w /io/wheelhouse/
done

# Install packages and test
for PYBIN in /opt/python/*/bin/; do
    "${PYBIN}/pip" install python-manylinux-demo --no-index -f /io/wheelhouse
    (cd "$HOME"; "${PYBIN}/nosetests" pymanylinuxdemo)
done
