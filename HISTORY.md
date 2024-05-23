
History
=======

Patch releases mean (the Z number in X.Y.Z version) that the underlying physics has not changed.  Changes to the NEST version will always trigger a minor or major release.  If this library changes such that end users have to change their code, this may also trigger a minor or major release.

2.0.3 (2024-05-23)
-----------------
Minor Changes:
  * Added the ability to lock and unlock the random seed
  * Removed Constraints in helpers.py that prevented vectorized yield equations from return high-energy yields. 

2.0.2 (2024-01-29)
-----------------
Synced with NEST v2.4.0

2.0.1 (2023-01-18)
-----------------
Updated python bindings to sync with NEST v2.3.12
  * GetYields has been updated to allow for the beta ER model parameters to be user-controllable parameters
  ** Introduced the new default vector `ERYieldsParam` for use with GetYields
  
  * Default parameter vectors have been moved from NESTcalc declarations to globally available vectors from NEST.hh

2.0.0 (2022-09-08)
-----------------
Update to nestpy internals, adding in basic LArNEST bindings
  * The copy/paste method for the NEST bindings have been replaced with adding NEST and other modules (such as gcem and pybind11) as git submodules which are downloaded at compile time. LXe notebooks and python scripts have been moved to tutorials/arxiv, and new notebooks will be placed in the tutorials folder as they are created in the future. LAr functionality through LArNEST has been added and will be expanded upon in future releases.

  * Suggestions/issues/errors should be added as github issues.

  * Users may have to do before installing:
  ** `pip uninstall nestpy`


1.5.5 (2022-07-08)
-----------------
Synced with NEST v2.3.9
  * New Physics Modeling:
  ** Skewness can be turned off and on now for ER just like for NR. For on -> old model or fixed (Quentin Riffard, LZ/LBNL)
  ** Older beta model is default for gaseous Xenon, a better fit to old world data at the keV scale (Eric Church, DUNE/PNNL)
  ** New dark matter halo model defaults, bringing NEST up to date on WIMP and Sun v (Baxter et al., arXiv:2105.00599)

  * Miscellaneous Bug Fixes:
  ** Fluctuations adjust for difference in width from truncated Gaussians for PE not just mean
  ** Complaint that position resolution too poor does not activate until above S2 (top) of 40 PE
  ** In the dE/dx-based model the minimum LET is now 1.0 MeV/cm not 0 to avoid weirdness

  * Updated binding for GetQuanta to allow for nestpy control over ER skewness. 


1.5.4 (2022-04-16)
-----------------
nestpy specific code quality:
  * Thanks to the great help of Joran  Angevaare, we now use GitHub workflows and no longer use Travis for releases and testing. 
  * `pip install nestpy` works again.
  * Should one want to recompile from source, you will still need to use `git clone` (for now).  


1.5.3 (2022-04-15)
-----------------
**Development version, not installable**
  * No new physics or implementation beyond developing a stable release workflow. 
  * There will not be a release associated with this version since we wanted to test the entire workflow. The stable release one should use to incorporate changes from 2022-02-09 (`NEST v2.3.5`) is `nestpy v1.5.4.` 

1.5.2 (2022-04-11)
-----------------
New Physics:
  * Perfectly vertical MIP tracks now work, and use latest beta model (Greg Rischbieter, LZ/UAlbany)
  * Field in G4 in any direction not just vertical but e.g. radial OK, ala (n)EXO and PETALO (Paola Ferrario)

Code Quality:
  * NEST: Geant4.9.11 & C++17 compatibility achieved (Paola Ferrario, PETALO/Basque Foundation for Science)
  * Multiple scatter code warning addressed: unused variable (Greg Rischbieter, LZ/UAlbany)

nestpy Specific: 
  * N/A

1.5.1 (2022-02-09)
-----------------
New Physics:
  * dE/dx-based yield code moved (execNEST->NEST.cpp) for accessibility. Muons, MIPs, LIPs; random positions
  * Initial or average dE/dx allowed, and use of ESTAR or custom power law, with variation around a mean dE/dx 
  * loopNEST for ER restored, with 1st-principles mod TIB model of recombination parameters for sustainability
  * New multiple scatter tool allows for creation of 2+ ER-like/NR-like scatters, or mixed for inelastic, Migdal, etc.

Code Quality and/or Miscellaneous Bug Fixes:
  * random exponential smarter sampling for small ranges especially for Kr83m times (Scott Kravitz, LZ/LBNL)
  * D-D energy spectrum user-settable, serving as example for any NR calibrations (Greg Rischbieter, LZ/UAlbany)
  * New truncated Gauss option, w/ truncation at 0 in 1st usage to solve S2 corner case (Scott Kravitz, LZ/LBNL)

nestpy Specific:
  * N/A 

1.5.0 (2021-11-11)
-----------------
New Physics:
  * Carried over from v2.3 beta: A new binomial random number generator (C++ default library), e- EE models, beta model with new yields and fluctuations, non-beta-ER (XELDA).
  * New beta model is default regardless of E-field, but old one is still accessible
  * ER model (betas and gammas weighted) is its own function, callable
  * Pb-206 ion coming off wall from alpha decay has correct Ly and Qy versus field (Thomas-Imel box model for recomb)
  * The electron extraction efficiency model now includes “optimistic” high e- EE Aprile/PandaX fits (activatable with EPS_GAS negative)

Code Quality and/or Miscellaneous Bug Fixes:
  * C++11 -> 17 default, README updated with all new versioning requirements, but old gcc and cmake versions requested to allow backwards-compatibility with nestpy. std::clamp still doesn’t work, so similar function written by hand
  * 1.1 -> 1.08 for increasing Qy to match new Zurich W-value measurement, but with new more logical variable names both deep in code and in detector file for user, and with one factor universal in NEST.cpp; general variable renaming for greater clarity
  * Numerous cosmetic and aesthetic changes to code, including unused variable removal, while spacing and tabbing made Google clang-format (with shell script for that now included with NEST), if/else Mac dangle warning addressed
  * Kr83m yields same but code overhauled to allow min versus max time separation flexibility and easier data comparison, with bug squashed where wrong error message got replayed
  * NEST is now 30% faster, cf. v2.2.4, at least when using gcc 7+, despite the new binomial fluctuation function!

nestpy Specific:
  * Bindings to energy spectra generators from TestSpectra.cpp, including: tritium and C14 beta sources; AmBe, DD, Cf252 neutron sources; Spin-Independent WIMP Generators. 

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
