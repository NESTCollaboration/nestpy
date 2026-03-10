"""
vectorized_yields.py
Makes plots of nestpy.

This contains all of the functions that are used to make the plots
which will be called via flask on main.py

The main components are:
1. Getting the yields for the interaction types of interest (done via numpy vectorized, rather than a loop)

Main ingredients for the above steps:
1. np.vectorize, dictionary with yields, field array and energy array.
"""

import numpy as np

from ._nestpy import NESTcalc, array # This is C++ library
from ._nestpy.detectors import VDetector
import awkward as ak
import pandas as pd


# Add local variable to cache the NESTcalc(DETECTOR) object
_NestCalcInit = dict()

@np.vectorize(excluded={"nr_parameters", "er_parameters"})
def get_all_yields(interaction, energy, nest_calc=NESTcalc(VDetector()), **kwargs):
    """Get a list of NEST yield objects

    Args:
        energy (array[float]): An array of energies in keV
        interaction (INTERACTION_TYPE): The type of interaction be studied
        nest_calc (NESTCalc): A NEST calculator defined for a given detector

    Returns:
        list[YieldResult]: A list of NEST yield objects
    """

    interaction = GetInteractionObject(interaction) if isinstance(interaction, str) else interaction

    return nest_calc.GetYields(energy=energy, interaction=interaction, **kwargs)

def get_yields_df(interaction, energy, nest_calc=NESTcalc(VDetector()), **kwargs):
    """Get a pandas dataframe of the yield parameters for an interaction

    Args:
        energy (array[float]): An array of energies in keV
        interaction (INTERACTION_TYPE): The type of interaction be studied
        nest_calc (NESTCalc): A NEST calculator defined for a given detector

    Returns:
        list[YieldResult]: A list of NEST yield objects
    """

    yields = get_all_yields(energy=energy, interaction=interaction, nest_calc=nest_calc, **kwargs)
    items = {"PhotonYield", "ElectronYield", "ExcitonRatio", "Lindhard"}
    df = pd.DataFrame({j:getattr(i, j) for j in items} for i in yields)
    df["energy"] = energy
    return df

@np.vectorize(excluded={"nr_parameters", "er_parameters"})
def GetYieldsVectorized(interaction, yield_type, nc=None, detector=None, **kwargs):
    """
    This function calculates nc.GetYields for the various interactions and arguments we pass into it.

    Requires:
        - GetInteractionObject from interactionkeys
            - strings passed through get us the numeric equivalent for each interaction
        - energy array
        - nc.GetYields (pass through interaction, energies, field value)
            - Returns dictionary with yield types and yield values at each interaction energy value.

    Parameters:
        nc (NESTcalc object): must specify nc=nestpy.NESTcalc(detector) to use non-default
        if no argument is provided - a default is loaded and written to cache.
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
    """
    if nc is None:
        # Cache the default in _NestCalcInit
        if "default" not in _NestCalcInit:
            _NestCalcInit["default"] = NESTcalc(VDetector())
        nc = _NestCalcInit["default"]

    yield_object = nc.GetYields(interaction=interaction, **kwargs)
    # returns the yields for the type of yield we are considering
    return getattr(yield_object, yield_type)


def PhotonYield(**kwargs):
    """
    Calculates photon yield based on GetYieldsVectorized function.

    Parameters:
        interaction (str): interaction type, here using 'nr' (nuclear reacoil),
        gammaray', 'beta', '206Pb', and 'alpha'.
        energy (array): Array of interactions to calculate yields of each.
            - Array MUST be the dimensions of # of energy values by # of drift fields (i.e. 2000x14 here)
        drift_field (array): Array of drift fields to use, which will be vectorized with energy.

    Returns:
        GetYieldsVectorized(yield_object, yield_type='PhotonYield') (array): array of yield values same dimensions as energies

    """
    return GetYieldsVectorized(yield_type="PhotonYield", **kwargs)


def ElectronYield(**kwargs):
    """
    Calculates electron yield based on GetYieldsVectorized function.

    Parameters:
        interaction (str): interaction type, here using 'nr' (nuclear reacoil),
        gammaray', 'beta', '206Pb', and 'alpha'.
        energy (array): Array of interactions to calculate yields of each.
            - Array MUST be the dimensions of # of energy values by # of drift fields (i.e. 2000x14 here)
        drift_field (array): Array of drift fields to use, which will be vectorized with energy.

    Returns:
        GetYieldsVectorized(yield_object, yield_type='ElectronYield') (array): array of yield values same dimensions as energies

    """
    return GetYieldsVectorized(yield_type="ElectronYield", **kwargs)


def Yield(**kwargs):
    """
    Calculates both electron and photon yields and puts in single dictionary.
    - Useful for analysis of one interaction_type.

    Parameters:
        Same as PhotonYield and ElectronYield

    Returns:
        (dict): dict with photon and electron yields arranged together by keys.
    """
    return {
        "photon": PhotonYield(**kwargs),
        "electron": ElectronYield(**kwargs),
        # What is missing?  Aren't there other parts of YieldObject?
    }


def get_random_position(detector, number: int):
    # Make generator
    rng = np.random.default_rng()

    # Get random positions
    r = detector.get_radius() * np.sqrt(rng.uniform(0, 1, size=number))
    θ = rng.uniform(0, 2 * np.pi, size=number)
    x = r * np.cos(θ)
    y = r * np.sin(θ)
    z = rng.uniform(0, detector.get_TopDrift(), size=number)

    # Return 3 X N array of positions
    return np.vstack((x, y, z)).T


def run_nest(
    interaction,
    detector,
    energy,
    positions: list[list[float]] = None,
    **kwargs
):

    energy = np.asarray(energy)

    interaction = GetInteractionObject(interaction) if isinstance(interaction, str) else interaction

    # If no position given then randomly sample
    if positions is None:
        positions = get_random_position(detector, len(energy))

    # Compute the NEST outputs
    result = array.runNESTvec(
        detector, interaction, energy.tolist(), positions.tolist(), **kwargs
    )

    # Create the pandas dataframe
    arr = ak.Array(
        {i: getattr(result, i) for i in result.__dir__() if not i.startswith("_")}
    )

    # Save truth information
    arr["energy_keV"] = energy
    arr["x_mm"] = positions[:, 0]
    arr["y_mm"] = positions[:, 1]
    arr["z_mm"] = positions[:, 2]

    return arr

def run_nest_df(
    interaction,
    detector,
    energy,
    pos: list[list[float]] = None,
    **kwargs
):

    arr = run_nest(interaction, detector, energy, pos, **kwargs)
    df = pd.DataFrame({i: arr[i] for i in arr.fields if arr[i].ndim == 1})

    return df


def calculate_extraction_parameters(detector, gas_field):
    initial_gas_field = detector.E_gas
    results = []
    for e in gas_field:
        detector.E_gas = e
        result = detector.extraction_parameters
        result["e_gas"] = e
        results.append(result)
    detector.E_gas = initial_gas_field
    return pd.DataFrame(results)