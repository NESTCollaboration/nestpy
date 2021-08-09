__version__ = '1.4.11'
__nest_version__ = '2.2.3'

from .nestpy import *

from .helpers import Yield, PhotonYield, ElectronYield, GetYieldsVectorized, GetInteractionObject, ListInteractionTypes

# Populate namespace with interaction types to allow e.g. nestpy.NR
for interaction_type in ListInteractionTypes(): # interaction_type is string
    vars()[interaction_type] = GetInteractionObject(interaction_type)
