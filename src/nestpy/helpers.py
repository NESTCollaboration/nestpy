"""
vectorized_yields.py
Makes plots of nestpy.

This contains all of the functions that are used to make the plots
which will be called via flask on main.py

The main components are:
1. Getting the yields for the interaction types of interest (done via numpy vectorized, rather than a loop)

Main ingredients for the above steps:
1. np.vectorize, dictionary with yields, field array and energy array.
    - Note: some of the yields will crash the plots at too high of energies (way above physical meaning)
    so np.nan is returned to keep things running.
"""

import numpy as np

from .nestpy import DetectorExample_XENON10, NESTcalc, INTERACTION_TYPE # This is C++ library

# Detector identification for default
# Performing NEST calculations according to the given detector example.
# Yields are ambivalent to detector.
DETECTOR = DetectorExample_XENON10()
NC = NESTcalc(DETECTOR)

NEST_INTERACTION_NUMBER = dict(
        nr=0,
        wimp=1,
        b8=2,
        dd=3,
        ambe=4,
        cf=5,
        ion=6,
        gammaray=7,
        beta=8,
        ch3t=9,
        c14=10,
        kr83m=11,
        nonetype=12,
    )

def ListInteractionTypes():
    return NEST_INTERACTION_NUMBER.keys()

def GetInteractionObject(name):
    '''
    This function returns the NEST interaction object for a given string.
    Parameters:
        name (str): interaction type (e.g. 'NR' or 'nr'.)
                    To see all options available, run nestpy.ListInteractionTypes().

    Returns:
        nestpy.INTERACTION_TYPE(Number), where Number corresponds to the string you provided.
    '''

    name = name.lower()

    if name == 'er':
        raise ValueError("For 'er', specify either 'gammaray' or 'beta'")

    interaction_object = INTERACTION_TYPE(NEST_INTERACTION_NUMBER[name])
    return interaction_object

@np.vectorize
def GetYieldsVectorized(interaction, yield_type, nc=NC, **kwargs):
    '''
    This function calculates nc.GetYields for the various interactions and arguments we pass into it.

    Requires:
        - GetInteractionObject from interactionkeys
            - strings passed through get us the numeric equivalent for each interaction
        - energy array
        - nc.GetYields (pass through interaction, energies, field value)
            - Returns dictionary with yield types and yield values at each interaction energy value.

    Parameters:
        nc (NESTcalc object): must specify nc=nestpy.NESTcalc(detector) to use non-default
        interaction (str): interaction type, here using 'nr' (nuclear recoil),
        gammaray', 'beta', '206Pb', and 'alpha'.
        yield_type (str): Either 'PhotonYield' or 'ElectronYield' to return proper yield values.
        **kwargs (var): Field values (array), energy values (array),
        can also contain other allowed nc.GetYields arguments.

    Calculates:
        yield_object (dict): Keys of yield_type, values of yields for given type based on nc.GetYields

    Returns:
        getattr(yield_object, yield_type) (array): array of yield values for a given yield_object (nr, etc)
        and a given yield_type (photon, electron yield as defined in parameters.)
    '''

    interaction_object = GetInteractionObject(interaction)
    if 'energy' in kwargs.keys():
        if interaction_object == GetInteractionObject('nr') and kwargs['energy'] > 2e2:
            return np.nan
        if interaction_object == GetInteractionObject('gammaray') and kwargs['energy'] > 3e3:
            return np.nan
        if interaction_object == GetInteractionObject('beta') and kwargs['energy'] > 3e3:
            return np.nan
    yield_object = nc.GetYields(interaction = interaction_object, **kwargs)
    # returns the yields for the type of yield we are considering
    return getattr(yield_object, yield_type)

def PhotonYield(**kwargs):
    '''
    Calculates photon yield based on GetYieldsVectorized function.

    Parameters:
        interaction (str): interaction type, here using 'nr' (nuclear reacoil),
        gammaray', 'beta', '206Pb', and 'alpha'.
        energy (array): Array of interactions to calculate yields of each.
            - Array MUST be the dimensions of # of energy values by # of drift fields (i.e. 2000x14 here)
        drift_field (array): Array of drift fields to use, which will be vectorized with energy.

    Returns:
        GetYieldsVectorized(yield_object, yield_type='PhotonYield') (array): array of yield values same dimensions as energies

    '''
    return GetYieldsVectorized(yield_type='PhotonYield', **kwargs)

def ElectronYield(**kwargs):
    '''
    Calculates electron yield based on GetYieldsVectorized function.

    Parameters:
        interaction (str): interaction type, here using 'nr' (nuclear reacoil),
        gammaray', 'beta', '206Pb', and 'alpha'.
        energy (array): Array of interactions to calculate yields of each.
            - Array MUST be the dimensions of # of energy values by # of drift fields (i.e. 2000x14 here)
        drift_field (array): Array of drift fields to use, which will be vectorized with energy.

    Returns:
        GetYieldsVectorized(yield_object, yield_type='ElectronYield') (array): array of yield values same dimensions as energies

    '''
    return GetYieldsVectorized(yield_type='ElectronYield', **kwargs)

def Yield(**kwargs):
    '''
    Calculates both electron and photon yields and puts in single dictionary.
    - Useful for analysis of one interaction_type.

    Parameters:
        Same as PhotonYield and ElectronYield

    Returns:
        (dict): dict with photon and electron yields arranged together by keys.
    '''
    return {'photon': PhotonYield(**kwargs),
            'electron': ElectronYield(**kwargs),
           # What is missing?  Aren't there other parts of YieldObject?
           }
