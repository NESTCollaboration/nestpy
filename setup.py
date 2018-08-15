import os
import re
import sys
import sysconfig
import platform
import subprocess

from distutils.version import LooseVersion
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext

CMAKE_BINARY = 'cmake'

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output([CMAKE_BINARY, '--version'])
        except OSError:
            try:
                import cmake
                CMAKE_BINARY = os.path.join(cmake.CMAKE_BIN_DIR, 'cmake')
                out = subprocess.check_output([CMAKE_BINARY, '--version'])
            except ImportError:
                raise RuntimeError(
                     "CMake must be installed to build the following extensions: " +
                      ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)',
                                         out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(
            os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(
                cfg.upper(),
                extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            build_args += ['--', '-j2']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(
            env.get('CXXFLAGS', ''),
            self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call([CMAKE_BINARY, ext.sourcedir] + cmake_args,
                              cwd=self.build_temp, env=env)
        subprocess.check_call([CMAKE_BINARY, '--build', '.'] + build_args,
                              cwd=self.build_temp)
        print()  # Add an empty line for cleaner output

readme = open('README.md').read()
history = open('HISTORY.md').read().replace('.. :changelog:', '')

# Fetch requirements, but remove explicit version pins.
# Use pip install -r requirements.txt for repeatable installations
requirements = open('requirements.txt').read().splitlines()
requirements = [x.split('=')[0] for x in requirements]

setup(
    name='nestpy',
    version='2.0.0',
    author='Christopher Tunnell',
    author_email='tunnell@rice.edu',
    description='Python bindings for the NEST noble element simulations',
    long_description=readme + '\n\n' + history,
    packages=find_packages('src'),
    package_dir={'':'src'},
    ext_modules=[CMakeExtension('nestpy/nestpy')],
    install_requires=requirements,
    cmdclass=dict(build_ext=CMakeBuild),
    test_suite='tests',
    zip_safe=False,
    include_package_data=True
)
