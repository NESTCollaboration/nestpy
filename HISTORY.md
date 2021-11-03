
History
=======

Patch releases mean (the Z number in X.Y.Z version) that the underlying physics has not changed.  Changes to the NEST version will always trigger a minor or major release.  If this library changes such that end users have to change their code, this may also trigger a minor or major release.

1.4.12 (2021-11-02)
-----------------
Sync with [NEST v2.3.0beta](https://github.com/NESTCollaboration/nest/releases/tag/v2.3.0beta)

  * Beta model updated to work with LUX C-14 (medium E-fields) in addition to XENON1T Rn-220 calibration, < 100 V/cm (Greg Rischbieter, Matthew Szydagis, Vetri Velan, and Quentin Riffard of LZ)
  * Non-beta (L-shell and M-shell) ER data now matched, from the XELDA experiment, with weighting of beta and gamma models (Sophia Farrell, Rice/XENON and Greg R. UAlbany/LZ)
  * Work function of 11.5 eV (EXO-200, Zurich) can now be more accurately reproduced with the "remove quanta" flag set to false, matching the EXO and Baudis (new) data sets (Kirsten McMichael, RPI/nEXO and Matthew Szydagis, UAlbany/LZ)
  * Systematic error taken into account for 3D XYZ position reconstruction with S2, per LUX Mercury paper (Claudio Silva, Coimbra/LZ).
  * Made the default S1 calculation mode hybrid instead of full, for faster simulation of large-energy (e.g., MeV-scale) events
  * Tweaked the default detector example (LUX Run03) to work with the latest models and reproduce D-D and 3H bands perfectly still, while also adding units to this LUX detector header file (Szydagis)
  * Binomial random number generator now uses default C++ library (Robert James, LZ). Code is a bit slower now (only by ~10%) but is more precise, and matches python, Flamedisx
  * The e- ext eff from liquid to gas is now based on both E-field (in liquid) and temperature, not field alone, combining dozen data sets spanning decades, to address concern raised by Sergey Pereverzev, LLNL. So, it's NOT just PIXeY or LLNL, etc.
  
1.4.11 (2021-08-09)
-----------------
Sync with [NEST v2.2.3](https://github.com/NESTCollaboration/nest/releases/tag/v2.2.3)

  * Replaced useTiming variable by an enum and made the GetS1 result a class member. Separated the S1 and S2 calculation modes.
  * Made GetS1 return a ref to avoid vector copy
  * Made the GetS2 results a private member returned by reference, while also making GetS1 and GetS2 results "const"
  * Removed useless, unused variables that caused a lot of memory allocation/deallocation; result of all this and the above: +~1-5% faster
  * Updated the parametric S1 calc to account for the truncated-Gaussian SPE and DPE distributions, making it more consistent with "full"
  * Changed hybrid-mode transition to be 100 keV, ~500 photon hits in modern TPCs, instead of hits directly, creating a smooth transition
  * Efficiency adjustment in the S1 parametric mode that further makes the parametric and full modes (previously useTiming -1,0) closer.
  * Changes driven by Quentin Riffard (LZ/LBNL) & Greg Rischbieter (LZ/UA), with ideas from Matthew (UA) & Luke Kreczko (Bristol)

1.4.10 (2021-07-08)
-----------------
Sync with [NEST v2.2.2](https://github.com/NESTCollaboration/nest/releases/tag/v2.2.2)

Code Quality and/or Misc Bug Fixes:
  * Added default density argument for LXe case, forcing an argument re-ordering (Sophia)
  * Moved position of "delete detector" in execNEST to solve python problem (Albert Baker, Greg R.)
  * Approx eff func for single phe made simpler, for FlameDisx (Robert James, Sophia, Matthew)
  * More robust rule used for when to approximate binomial as Gaussian (Sophia, Greg R.)
  * Warn that you are in a region of too-low time between S1a and S1b for Kr83m only 1x (Sophia)
  * Bad-order if-statements simplified with a min within a max for <0, >1 checks (Luke K., Matthew)
New Physics:
  * Liquid Ar model for ER fits all the data better now, in both energy and dE/dx bases (Kate K.)

Code Quality and/or Miscellaneous Bug Fixes:
  * Deleted unused redundant line in GetS1 that re-calculated the drift time (Quentin Riffard, LBNL/LZ)
  * Only print most error and warning messages if verbosity on (Quentin Riffard, LBNL/LZ)
  * Updated TravisCI link in README and added note about OSX builds (Chris Tunnell, Rice/XENON)
  * Use of abs value func standardized, lines broken up, multi-line string for cerr (Matthew at behest of Luke Kreczko, Bristol/LZ)
New Physics:
  * Liquid Xe model for NR is now better behaved at few hundred keV and few hundred in S1: no odd increase in band width caused by Nex/Ni zeroing out and kinking the recombination probability. Mean yields model unchanged, nor recombination fluctuations / skewness. (Matthew and Greg R., UAlbany/LZ)

1.4.9 (2021-06-01)
-----------------
Sync with [NEST v2.2.1patch2](https://github.com/NESTCollaboration/nest/releases/tag/v2.2.1patch2)

Code Quality and/or Misc Bug Fixes:
  * Added default density argument for LXe case, forcing an argument re-ordering (Sophia)
  * Moved position of "delete detector" in execNEST to solve python problem (Albert Baker, Greg R.)
  * Approx eff func for single phe made simpler, for FlameDisx (Robert James, Sophia, Matthew)
  * More robust rule used for when to approximate binomial as Gaussian (Sophia, Greg R.)
  * Warn that you are in a region of too-low time between S1a and S1b for Kr83m only 1x (Sophia)
  * Bad-order if-statements simplified with a min within a max for <0, >1 checks (Luke K., Matthew)
New Physics:
  * Liquid Ar model for ER fits all the data better now, in both energy and dE/dx bases (Kate K.)

1.4.8 (2021-04-09)
-----------------
Sync with [NEST v2.2.1patch1](https://github.com/NESTCollaboration/nest/releases/tag/v2.2.1patch1)

1.4.7 (2021-03-03)
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
    
1.4.5-1.4.6 (2021-03-01)
-----------------
(Pre-releases, see version 1.4.7 for distributions)
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
