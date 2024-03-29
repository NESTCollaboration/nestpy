'''
benchmark_plots.py
Makes plots of nestpy.

This contains all of the functions that are used to make the plots 
which will be called via flask on main.py

The main components are:
1. Getting the yields for the interaction types of interest (done via numpy vectorized, rather than a loop)
2. Defining the plots for each of the yields (these aren't looped over because each of them slightly differs)
3. Making the plots via one function so that in main.py, you only have to call the one makeplots() 
function to make all plots.

Main ingredients for the above steps: 
1. np.vectorize, dictionary with yields, field array and energy array.
    - Note: some of the yields will crash the plots at too high of energies (way above physical meaning)
    so np.nan is returned to keep things running.
2. Plotting tools via matplotlib, but note that all plots are saved in an arbitrary "IMAGE_OBJECTS" object,
which, rather than a file, will store the images in a dictionary when called in main.py 
(easier for using with flask.)
'''

import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import numpy as np
import os

import nestpy
from nestpy import GetInteractionObject

# Figure parameters common throughout all plots
version_textbox = "NEST v{0} \n nestpy v{1}".format(nestpy.__nest_version__, nestpy.__version__)
bbox = dict(boxstyle="round", fc="1.00", edgecolor='none')
params = {'xtick.labelsize':'x-large',
        'ytick.labelsize':'x-large',
        }
# Updates plots to apply the above formatting to all plots in doc
pylab.rcParams.update(params)

@np.vectorize
def GetYieldsVectorized(interaction, yield_type, **kwargs):
    '''
    This function calculates nc.GetYields for the various interactions and arguments we pass into it.

    Requires:
        - GetInteractionObject from interactionkeys
            - strings passed through get us the numeric equivalent for each interaction
        - energy array 
        - nc.GetYields (pass through interaction, energies, field value)
            - Returns dictionary with yield types and yield values at each interaction energy value.
    
    Parameters:
        interaction (str): interaction type, here using 'nr' (nuclear reacoil), 
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
    return GetYieldsVectorized(yield_type = 'PhotonYield', **kwargs)
 
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
    return GetYieldsVectorized(yield_type = 'ElectronYield', **kwargs)

def Yield(**kwargs):
    '''
    Calculates both electron and photon yields and puts in single dictionary.
    - Useful for analysis of one interaction_type.
    
    Parameters:
        Same as PhotonYield and ElectronYield

    Returns:
        (dict): dict with photon and electron yields arranged together by keys.
    '''
    return {'photon' : PhotonYield(**kwargs),
            'electron' : ElectronYield(**kwargs),
           # What is missing?  Aren't there other parts of YieldObject?
           }

def make_subplot(
    x,
    y_photons,
    y_electrons,
    driftFields,
    plot_type,
):
    fig1, ax1 = plt.subplots(1, 1, figsize=(9,6))
    fig2, ax2 = plt.subplots(1, 1, figsize=(9,6))

    ax1.plot([],[],label=f" NEST v{nestpy.__nest_version__} \n nestpy v{nestpy.__version__}\n", marker='',linestyle='')
    ax2.plot([],[],label=f" NEST v{nestpy.__nest_version__} \n nestpy v{nestpy.__version__}\n", marker='',linestyle='')
    
    for i in range(0, len(driftFields)-2):
        ax1.plot(x[i,:], y_photons[i,:], label="{0} V/cm".format(driftFields[i]))
        ax2.plot(x[i,:], y_electrons[i,:], label="{0} V/cm".format(driftFields[i])) 

    for ax in ax1, ax2:
        ax.set_xscale('log')
        ax.set_ylim(0)
        ax.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left',fontsize=14)
        ax.set_xlabel('Recoil Energy [keV]', fontsize=20)
        ax.margins(0)

    # ax1.text(1.05, 0.0, 
    #             version_textbox, 
    #             bbox=bbox, horizontalalignment='right', fontsize='x-large')
    # ax2.text(1.05, 0.0, 
    #             version_textbox, 
    #             bbox=bbox, horizontalalignment='right', fontsize='x-large')

    ax1.set_ylabel('Light Yield [n$_\gamma$/keV]', fontsize=20)
    ax1.set_title('Light Yields for Nuclear Recoils', fontsize=24)
    ax2.set_title('Charge Yields for Nuclear Recoils', fontsize=24)
    ax2.set_ylabel('Charge Yield [n$_e$/keV]', fontsize=20) 
    fig1.tight_layout()
    fig2.tight_layout()
    fig1.savefig(f'plots/{plot_type}_LY.png')
    fig2.savefig(f'plots/{plot_type}_QY.png')    


if __name__ == "__main__":
    if not os.path.isdir("plots/"):
        os.makedirs("plots/")
    
    # Detector identification
    detector = nestpy.DetectorExample_XENON10()
    # Performing NEST calculations according to the given detector example       
    nc = nestpy.NESTcalc(detector)
    #Once you have interaction, you can get yields

    '''
    Below are field and energy arrays.
    - Energies are broadcase to be repeated by the dimensions of the fields, 
    owing to the nature of vectorized functions below. 
    - Functions will loop over each energy and field simultaneously that way,
    rather than nesting for loops inside each other.
    ''' 
    fields = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
    energies = np.logspace(-1, 4, 2000)
    energies = np.broadcast_to(energies, (len(fields), len(energies)))

    # Calculate yields for various benchmark calculations
    '''
    This is where the nest calculations actually occur.
    - All functions below are essentially the same exact thing, jus__version__ = .nestpy.__version__
    __nest_version__ = .nestpy.__nest_version__t iterated over the 5 interaction types
    and the 2 yield types (electron and photon yields).
    - Everything done from this point on is just plotting all of this info.
    '''
    kwargs = {'energy': energies.T, 'drift_field': fields}
    nr_electrons = ElectronYield(interaction='nr', **kwargs).T/energies
    nr_photons = PhotonYield(interaction='nr', **kwargs).T/energies
    beta_electrons = ElectronYield(interaction='beta', **kwargs).T/energies
    beta_photons = PhotonYield(interaction='beta', **kwargs).T/energies
    gamma_electrons = ElectronYield(interaction='gammaray', **kwargs).T/energies
    gamma_photons = PhotonYield(interaction='gammaray', **kwargs).T/energies
    alpha_electrons = ElectronYield(interaction='ion', Z=2, A = 4, **kwargs).T/energies
    alpha_photons = PhotonYield(interaction='ion',Z=2, A=4, **kwargs).T/energies
    Pb_electrons = ElectronYield(interaction='ion', Z=82, A = 206, **kwargs).T/energies
    Pb_photons = PhotonYield(interaction='ion',Z=82, A=206, **kwargs).T/energies

    '''
    This function just takes the above plots and combines into one function to make main.py
    easier to manage.
    Each are essentially the same thing. 

    Parameters:
    energies (array): energies broadcasted to the dimensions of fields. (in keV)
    photon and electron yields: e.g. nr_photons, nr_electrions (array): calculated from GetYields
    fields (array): field values of interest for plotting (V/cm)
    IMAGE_DICT (dict): Dictionary that will store the images as objects to call later in flask app.
    '''
    make_subplot(energies, nr_photons, nr_electrons, fields, "NR")
    make_subplot(energies, beta_photons, beta_electrons, fields, "beta")
    make_subplot(energies, gamma_photons, gamma_electrons, fields, "gamma")
    make_subplot(energies, alpha_photons, alpha_electrons, fields, "alpha")
    make_subplot(energies, Pb_photons, Pb_electrons, fields, "Pb206")