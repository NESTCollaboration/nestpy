__version__ = '1.3.1'
__nest_version__ = '2.1.1'

from .nestpy import *
from nestpy.vectorized_yields import Yield, PhotonYield, ElectronYield, GetYieldsVectorized
from nestpy.interaction_keys import GetInteractionObject, ListInteractionTypes

# # Populate namespace with interaction types to allow e.g. nestpy.NR
# for interaction_type in ListInteractionTypes(): # interaction_type is string
#     vars()[interaction_type] = GetInteractionObject(interaction_type)
    # setattr(nestpy, interaction_type.upper(), GetInteractionObject(interaction_type))