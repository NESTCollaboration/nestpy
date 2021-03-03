
History
=======

Patch releases mean (the Z number in X.Y.Z version) that the underlying physics has not changed.  Changes to the NEST version will always trigger a minor or major release.  If this library changes such that end users have to change their code, this may also trigger a minor or major release.

1.4.6 (2021-03-03)
-----------------
Sync with [NEST v2.2.1](https://github.com/NESTCollaboration/nest/releases/tag/v2.2.1)
  * Cleaned up MANIFEST so pypi dist packages are less bulky
    [#56](https://github.com/NESTCollaboration/nestpy/pull/56)
  * Added floating point comparison method for equality checks
    [#54](https://github.com/NESTCollaboration/nestpy/pull/54)
  * Random Number Generation in bindings.cpp to ensure quanta are truly randomized.
    [#54](https://github.com/NESTCollaboration/nestpy/pull/54)
  * Binding to Kr83m yields model directly so users can specify explicity deltaT_ns between decay modes.
    [#55](https://github.com/NESTCollaboration/nestpy/pull/55)
    
1.4.5 (2021-03-01)
-----------------
(Pre-release, see version 1.4.6 for distributions)
<br>
Sync with [NEST v2.2.1](https://github.com/NESTCollaboration/nest/releases/tag/v2.2.1)

1.4.4 (2021-02-10)
-----------------
NEST v2.2.0 (no NEST changes)
  * PyPi calls improved to compile for linux

1.4.3 (2021-02-08)
-----------------
NEST v2.2.0 (no NEST changes)
  * Attempted bug fix (fixed properly in 1.4.4)
  * New tutorials directory

1.4.2 (2021-02-01)
-----------------
  * Bind with LUX detector file 
  * Fix interaction key interpretation in helpers

1.4.1 (2020-12-15)
-----------------
Sync with v2.2.0 NEST. 
Includes all files in MANIFEST.in, so that pip install will work.

1.4.0 (2020-11-19)
-----------------
Minor changes all are to fix software bugs, no physics changes. 

  * MANIFEST.in include requirements
  * Make sure to include all dependencies. 
  * Fix travis builds. 

1.4.0beta (2020-11-14)
-----------------

NESTv2.2.0beta

1.3.2 (2020-11-11)
-----------------

NESTv2.1.2
  * New free parameters registered
  * Cases of void initialization in tests fixed
  * Introduced files for debugging tests as we improve code
  * Prepared for NEST v.2.2 which is imminent
  * Solved half of GetS1 and GetS2 issues opened in #37


1.3.1 (2020-08-26)
-----------------

NESTv2.1.1

1.3.0 (2020-07-06)
------------------

NESTv2.1.0

1.2.1 (2020-06-20)
------------------

NESTv2.1.0beta

1.1.4 (2020-06-20)
------------------

* Update pybind11 2.5.0
* Fix manylinux build 
* Add Python 3.8 support

1.1.3 (2019-08-05)
------------------

Default arguments for GetYields and GetQuanta (see PR #25)


1.1.2 (2019-08-02)
------------------

NESTv2.0.1

* execNEST included in nestpy
* Extensive bug fixes and testing improvements

1.1.1 (2018-08-29)
------------------

NESTv2.0.0

* Fix source installation (See #16).

1.1.0 (2018-08-18)
------------------

NESTv2.0.0

* Release to world.
* Cleanup (#15)

1.0.3 (2018-08-18)
------------------

NESTv2.0.0

* README broken links fixed

1.0.2 (2018-08-18)
------------------

NESTv2.0.0

* Metadata (classifier in setup.py, badges, chat) (#14)

1.0.1 (2018-08-18)
------------------

NESTv2.0.0

* Retrigger release for PyPI deployment

1.0.0 (2018-08-18)
------------------

NESTv2.0.0

* First release intended for general public.
* Mac OSX support (#10)
* Complete tests and various bug fixes (#13)
* Documentation, citation, and technical detail writing


0.2.3 (2018-08-14)
------------------

NESTv2.0.0

* Still working on PyPI

0.2.2 (2018-08-14)
------------------

NESTv2.0.0

* Fix lack of deploy of release to PyPI

0.2.1 (2018-08-14)
------------------

NESTv2.0.0

* Fix tests that were breaking only in deploys

0.2.0 (2018-08-14)
------------------

NESTv2.0.0

* Fully wrapped NEST (PR #5)

0.1.1 (2018-08-14)
------------------

NESTv2.0.0

* First release that deploys on PyPI. Limited functionality. (PR #2)

0.1.0 (2018-08-14)
------------------

NESTv2.0.0

* Initial release
