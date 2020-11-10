from .nestpy import INTERACTION_TYPE

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
    #list_interaction_types

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