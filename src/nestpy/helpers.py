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


from nestpy import (
    DetectorExample_XENON10,
    NESTcalc,
    INTERACTION_TYPE,
)  # This is C++ library

from nestpy import array

# Detector identification for default
# Performing NEST calculations according to the given detector example.
# Yields are ambivalent to detector.
# DETECTOR = DetectorExample_XENON10()
# NC = NESTcalc(DETECTOR)

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


# Add local variable to cache the NESTcalc(DETECTOR) object
_NestCalcInit = dict()


def ListInteractionTypes():
    return NEST_INTERACTION_NUMBER.keys()


def GetInteractionObject(name):
    """
    This function returns the NEST interaction object for a given string.
    Parameters:
        name (str): interaction type (e.g. 'NR' or 'nr'.)
                    To see all options available, run nestpy.ListInteractionTypes().

    Returns:
        nestpy.INTERACTION_TYPE(Number), where Number corresponds to the string you provided.
    """

    name = name.lower()

    if name == "er":
        raise ValueError("For 'er', specify either 'gammaray' or 'beta'")

    interaction_object = INTERACTION_TYPE(NEST_INTERACTION_NUMBER[name])
    return interaction_object


@np.vectorize(excluded={"nuisance_parameters", "ERYieldsParam"})
def get_all_yields(energy, nest_calc, interaction, **kwargs):
    """Get a list of NEST yield objects

    Args:
        energy (array[float]): An array of energies in keV
        interaction (INTERACTION_TYPE): The type of interaction be studied
        nest_calc (NESTCalc): A NEST calculator defined for a given detector

    Returns:
        list[YieldResult]: A list of NEST yield objects
    """
    return nc.GetYields(energy=energy, interaction=interaction, **kwargs)

def get_yields_df(energy, nest_calc, interaction, **kwargs):
        """Get a pandas dataframe of the yield parameters for an interaction

    Args:
        energy (array[float]): An array of energies in keV
        interaction (INTERACTION_TYPE): The type of interaction be studied
        nest_calc (NESTCalc): A NEST calculator defined for a given detector

    Returns:
        list[YieldResult]: A list of NEST yield objects
    """

    try:
        import pandas as pd
    except ImportError as exc:
        msg = "The get_yields_df method requires the 'pandas' package.  Please install via 'pip install pandas'"
        raise ImportError(msg) from exc

    yields = get_all_yields(energy=energy, interaction=interaction, nest_calc=nest_calc, **kwargs)
    items = {"PhotonYield", "ElectronYield", "ExcitonRatio", "Lindhard"}
    df = pd.DataFrame({j:getattr(i, j) for j in items} for i in yields)
    df["energy"] = energy
    return df

@np.vectorize(excluded={"nuisance_parameters", "ERYieldsParam"})
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
            _NestCalcInit["default"] = NESTcalc(DetectorExample_XENON10())
        nc = _NestCalcInit["default"]
    if type(interaction) == str:
        interaction_object = GetInteractionObject(interaction)
    else:
        interaction_object = interaction

    yield_object = nc.GetYields(interaction=interaction_object, **kwargs)
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


def nest_vector(
    interaction,
    detector,
    energy,
    pos: list[list[float]] = None,
    df: bool = False,
    **kwargs
):

    try:
        import awkward as ak
        import pandas as pd
    except ImportError as exc:
        msg = "The runNESTframe method requires the 'pandas' and 'awkward' package.  Please install via 'pip install pandas awkward'"
        raise ImportError(msg) from exc

    interaction = GetInteractionObject(interaction) if isinstance(interaction, str) else interaction

    # If no position given then randomly sample
    if pos is None:
        pos = get_random_position(detector, energy.shape)

    # Compute the NEST outputs
    result = array.runNESTvec(
        detector, interaction, energy.tolist(), pos.tolist(), **kwargs
    )

    # Create the pandas dataframe
    arr = ak.Array(
        {i: getattr(result, i) for i in result.__dir__() if not i.startswith("_")}
    )

    # Save truth information
    arr["energy_keV"] = energy
    arr["x_mm"] = pos[:, 0]
    arr["y_mm"] = pos[:, 1]
    arr["z_mm"] = pos[:, 2]

    if df:
        print(
            "Making a simple dataframe,  will lose any photon timing or waveform information"
        )
        fields = [i for i in arr.fields if arr[i].ndim == 1]
        arr = pd.DataFrame({i: arr[i] for i in fields})

    return arr
