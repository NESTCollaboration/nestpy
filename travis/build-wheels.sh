#!/bin/bash
set -e -x

# Install a system package required by our library
yum install -y atlas-devel wget

# Have to manually build and install CMake since libc old but
# at least 2.8.12 is required for pybind11.
cd /root
wget --no-check-certificate https://github.com/Kitware/CMake/archive/v2.8.12.tar.gz
tar xfz v2.8.12.tar.gz
cd CMake-2.8.12
./bootstrap > quiet_bootstrap
make  > quiet_make
make install > quiet_make_install
export PATH=$PATH:/usr/local/bin

# Compile wheels
for PYBIN in /opt/python/*/bin; do
    "${PYBIN}/pip" wheel /io/ -w wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" -w /io/wheelhouse/
done

# Install packages and test
for PYBIN in /opt/python/*/bin/; do
    "${PYBIN}/pip" install nestpy --no-index -f /io/wheelhouse
#    (cd "$HOME"; "${PYBIN}/nosetests" -w /io/tests)
done
