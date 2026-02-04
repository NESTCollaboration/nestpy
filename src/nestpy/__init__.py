from ._nestpy import * 
from ._nestpy import __nest_version__

from .helpers import Yield, PhotonYield, ElectronYield, GetYieldsVectorized, GetInteractionObject, ListInteractionTypes

# Populate namespace with interaction types to allow e.g. nestpy.NR
for interaction_type in ListInteractionTypes(): # interaction_type is string
    vars()[interaction_type] = GetInteractionObject(interaction_type)
