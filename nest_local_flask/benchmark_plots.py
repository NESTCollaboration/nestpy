import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import matplotlib.pylab as pylab

import nestpy 
from interaction_keys import GetInteractionObject

v_nestpy = str(nestpy.__version__)
v_nest = '2.0.1'
version_textbox = " NEST v{0} \n nestpy v{1}".format(v_nest, v_nestpy)

# Figure parameters common throughout all plots
bbox = dict(boxstyle="round", fc="1.00", edgecolor='none')
params = {'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large',
         }
pylab.rcParams.update(params)

fields = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
energies = np.logspace(-1, 4, 2000)
energies = np.broadcast_to(energies, (len(fields), len(energies)))

#Detector identification
detector = nestpy.DetectorExample_XENON10()
# Performing NEST calculations according to the given detector example       
nc = nestpy.NESTcalc(detector)
#Once you have interaction, you can get yields
#Begin with np.vectorize so that we can get yields over a range of interaction types/energies/drift fields.

@np.vectorize
def GetYieldsVectorized(interaction, yield_type, **kwargs):
    # This function does nc.GetYields for the various interactions and arguments we pass into it
    # TODO: Look at docstrings
    interaction_object = GetInteractionObject(interaction)
    if 'energy' in kwargs.keys():
        if interaction_object == GetInteractionObject('nr') and kwargs['energy'] > 3e2:
            return np.nan
        if interaction_object == GetInteractionObject('gammaray') and kwargs['energy'] > 3e3:
            return np.nan
        if interaction_object == GetInteractionObject('beta') and kwargs['energy'] > 3e3:
            return np.nan     
    yield_object = nc.GetYields(interaction = interaction_object, **kwargs)
    # returns the yields for the type of yield we are considering 
    return getattr(yield_object, yield_type)

def PhotonYield(**kwargs):
    return GetYieldsVectorized(yield_type = 'PhotonYield', **kwargs)
 
def ElectronYield(**kwargs):
    return GetYieldsVectorized(yield_type = 'ElectronYield', **kwargs)

def Yield(**kwargs):
    return {'photon' : PhotonYield(**kwargs),
            'electron' : ElectronYield(**kwargs),
           # What is missing?  Aren't there other parts of YieldObject?
           }

#Calculate yields for various benchmark calculations
nr_electrons = ElectronYield(interaction='nr', energy=energies.T, drift_field = fields).T/energies
nr_photons = PhotonYield(interaction='nr', energy=energies.T, drift_field = fields).T/energies
beta_electrons = ElectronYield(interaction='beta', energy=energies.T, drift_field = fields).T/energies
beta_photons = PhotonYield(interaction='beta', energy=energies.T, drift_field = fields).T/energies
gamma_electrons = ElectronYield(interaction='gammaray', energy=energies.T, drift_field = fields).T/energies
gamma_photons = PhotonYield(interaction='gammaray', energy=energies.T, drift_field = fields).T/energies
alpha_electrons = ElectronYield(interaction='ion', Z=2, A = 4, energy=energies.T, drift_field = fields).T/energies
alpha_photons = PhotonYield(interaction='ion',Z=2, A=4, energy=energies.T, drift_field = fields).T/energies
Pb_electrons = ElectronYield(interaction='ion', Z=82, A = 206, energy=energies.T, drift_field = fields).T/energies
Pb_photons = PhotonYield(interaction='ion',Z=82, A=206, energy=energies.T, drift_field = fields).T/energies

# ## Nuclear Recoils Plotting 
def nr_subplot(x, y_photons, y_electrons, driftFields, IMAGE_OBJECTS):
    fig1, ax1 = plt.subplots(1, 1, figsize=(9,6))
    fig2, ax2 = plt.subplots(1, 1, figsize=(9,6))
    
    for i in range(0, len(driftFields)-2):
        ax1.plot(x[i,:], y_photons[i,:], label="{0} V/cm".format(driftFields[i]))
        ax2.plot(x[i,:], y_electrons[i,:], label="{0} V/cm".format(driftFields[i])) 

    for ax in ax1, ax2:
        ax.set_xscale('log')
        ax.set_ylim(0)
        ax.legend(loc='best', ncol=3, fontsize='large')
        ax.set_xlabel('Recoil Energy [keV]', fontsize=20)
        ax.margins(0)

    ax1.text(energies[0][np.argmax(nr_photons)-35], 1, 
                version_textbox, 
                bbox=bbox, horizontalalignment='right', fontsize='x-large')
    ax2.text(energies[0][np.argmax(nr_photons)-35], 7.6, 
                version_textbox, 
                bbox=bbox, horizontalalignment='right', fontsize='x-large')

    ax1.set_ylabel('Light Yield [n$_\gamma$/keV]', fontsize=20)
    ax1.set_title('Light Yields for Nuclear Recoils', fontsize=24)
    ax2.set_title('Charge Yields for Nuclear Recoils', fontsize=24)
    ax2.set_ylabel('Charge Yield [n$_e$/keV]', fontsize=20) 
    fig1.tight_layout()
    fig2.tight_layout()
    fig1.savefig(IMAGE_OBJECTS['nr_LY.png'])
    fig2.savefig(IMAGE_OBJECTS['nr_QY.png'])

def beta_subplot(x, y_photons, y_electrons, driftFields, IMAGE_OBJECTS):
    fig1, ax1 = plt.subplots(1, 1, figsize=(9,6))
    fig2, ax2 = plt.subplots(1, 1, figsize=(9,6))
    for i in range(0, len(driftFields)-2):
        ax1.plot(x[i,:], y_photons[i,:], label="{0} V/cm".format(driftFields[i]))
        ax2.plot(x[i,:], y_electrons[i,:], label="{0} V/cm".format(driftFields[i])) 

    for ax in ax1, ax2:
        ax.set_xscale('log')
        ax.set_ylim(0)
        ax.legend(loc='best', ncol=1, fontsize='large')
        ax.set_xlabel('Energy [keV]', fontsize=20)
        ax.margins(0)

    ax1.text(energies[0][32], 20, 
                version_textbox, 
                bbox=bbox, horizontalalignment='left', fontsize='x-large')
    ax2.text(energies[0][np.argmax(beta_electrons)-35], 74, 
                version_textbox, 
                bbox=bbox, horizontalalignment='right', fontsize='x-large')

    ax1.set_ylabel('Light Yield [n$_\gamma$/keV]', fontsize=20)
    ax1.set_title('Light Yields for $\\beta$ Electron Recoils', fontsize=24)
    ax2.set_title('Charge Yields for $\\beta$ Electron Recoils', fontsize=24)
    ax2.set_ylabel('Charge Yield [n$_e$/keV]', fontsize=20) 
    fig1.tight_layout()
    fig2.tight_layout()
    fig1.savefig(IMAGE_OBJECTS['beta_LY.png'])
    fig2.savefig(IMAGE_OBJECTS['beta_QY.png'])

# # ## $\gamma$ electron recoils
def gamma_subplot(x, y_photons, y_electrons, driftFields, IMAGE_OBJECTS):
    fig1, ax1 = plt.subplots(1, 1, figsize=(9,6))
    fig2, ax2 = plt.subplots(1, 1, figsize=(9,6))
    for i in range(0, len(driftFields)-2):
        ax1.plot(x[i,:], y_photons[i,:], label="{0} V/cm".format(driftFields[i]))
        ax2.plot(x[i,:], y_electrons[i,:], label="{0} V/cm".format(driftFields[i])) 

    for ax in ax1, ax2:
        ax.set_xscale('log')
        ax.set_ylim(0)
        ax.legend(loc='best', ncol=1, fontsize='large')
        ax.set_xlabel('Energy [keV]', fontsize=20)
        ax.margins(0)

    ax1.text(energies[0][np.argmax(gamma_photons)-35], 3, 
                version_textbox, 
                bbox=bbox, horizontalalignment='right', fontsize='x-large')
    ax2.text(energies[0][np.argmax(gamma_electrons)-35], 68, 
                version_textbox, 
                bbox=bbox, horizontalalignment='right', fontsize='x-large')

    ax1.set_ylabel('Light Yields [n$_\gamma$/keV]', fontsize=20)
    ax1.set_title('Light Yields for $\\gamma$ Electron Recoils', fontsize=24)
    ax2.set_title('Charge Yields for $\\gamma$ Electron Recoils', fontsize=24)
    ax2.set_ylabel('Charge Yield [n$_e$/keV]', fontsize=20) 
    fig1.tight_layout()
    fig2.tight_layout()
    fig1.savefig(IMAGE_OBJECTS['gamma_LY.png'])
    fig2.savefig(IMAGE_OBJECTS['gamma_QY.png'])

def alpha_subplot(x, y_photons, y_electrons, driftFields, IMAGE_OBJECTS):
    fig1, ax1 = plt.subplots(1, 1, figsize=(9,6))
    fig2, ax2 = plt.subplots(1, 1, figsize=(9,6))
    for i in range(0, len(driftFields)-2):
        ax1.plot(x[i,:], y_photons[i,:], label="{0} V/cm".format(driftFields[i]))
        ax2.plot(x[i,:], y_electrons[i,:], label="{0} V/cm".format(driftFields[i])) 

    for ax in ax1, ax2:
        ax.set_xscale('log')
        ax.set_ylim(0)
        ax.set_xlim(1, 1e4)
        ax.legend(loc='best', ncol=2, fontsize='large')
        ax.set_xlabel('Energy [keV]', fontsize=20)
        ax.margins(0)

    ax1.text(energies[0][np.argmax(alpha_photons)-35], 3, 
                version_textbox, 
                bbox=bbox, horizontalalignment='right', fontsize='x-large')
    ax2.text(energies[0][740], 2, 
                version_textbox, 
                bbox=bbox, horizontalalignment='right', fontsize='x-large')

    ax1.set_ylabel('Light Yields [n$_\gamma$/keV]', fontsize=20)
    ax1.set_title('Light Yields for $\\alpha$-Particle Nuclear Recoils', fontsize=24)
    ax2.set_title('Charge Yields for $\\alpha$-Particle Nuclear Recoils', fontsize=24)
    ax2.set_ylabel('Charge Yield [n$_e$/keV]', fontsize=20) 
    fig1.tight_layout()
    fig2.tight_layout()
    fig1.savefig(IMAGE_OBJECTS['alpha_LY.png'])
    fig2.savefig(IMAGE_OBJECTS['alpha_QY.png'])


# ## $^{206}$Pb nuclear recoils
def Pb_subplot(x, y_photons, y_electrons, driftFields, IMAGE):
    fig1, ax1 = plt.subplots(1, 1, figsize=(9,6))
    fig2, ax2 = plt.subplots(1, 1, figsize=(9,6))
    for i in range(0, len(driftFields)-2):
        ax1.plot(x[i,:], y_photons[i,:], label="{0} V/cm".format(driftFields[i]))
        ax2.plot(x[i,:], y_electrons[i,:], label="{0} V/cm".format(driftFields[i])) 

    for ax in ax1, ax2:
        ax.set_xscale('log')
        ax.set_ylim(0)
        ax.set_xlim(1, 1e2)
        ax.legend(loc='best', ncol=2, fontsize='large')
        ax.set_xlabel('Recoil Energy [keV]', fontsize=20)
        ax.margins(0)

    ax1.text(40, 0.3, 
                version_textbox, 
                bbox=bbox, horizontalalignment='left', fontsize='x-large')
    ax2.text(40, 0.03, 
                version_textbox, 
                bbox=bbox, horizontalalignment='left', fontsize='x-large')
    ax1.set_ylim(0,10)
    ax1.set_ylabel('Light Yields [n$_\gamma$/keV]', fontsize=20)
    ax1.set_title('Light Yields for Nuclear Recoils from $^{206}$Pb', fontsize=24)
    ax2.set_title('Charge Yields for Nuclear Recoils from $^{206}$Pb', fontsize=24)
    ax2.set_ylabel('Charge Yield [n$_e$/keV]', fontsize=20) 
    fig1.tight_layout()
    fig2.tight_layout()
    fig1.savefig(IMAGE['206Pb_LY.png'])
    fig2.savefig(IMAGE['206Pb_QY.png'])

#Just makes all the plots from all the fancy work before
def makeplots(IMAGE_DICT):
    nr_subplot(energies, nr_photons, nr_electrons, fields, IMAGE_DICT)
    beta_subplot(energies, beta_photons, beta_electrons, fields, IMAGE_DICT)
    gamma_subplot(energies, gamma_photons, gamma_electrons, fields, IMAGE_DICT)
    alpha_subplot(energies, alpha_photons, alpha_electrons, fields, IMAGE_DICT)
    Pb_subplot(energies, Pb_photons, Pb_electrons, fields, IMAGE_DICT)