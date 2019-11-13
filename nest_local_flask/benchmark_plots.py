import os
import io
import collections

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes as axes

import nestpy 
v_nestpy = str(nestpy.__version__)
v_nest = '2.0.1'

__version__ = '0.0.3'


fields = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
energies = np.logspace(-1, 4, 2000)
energies = np.broadcast_to(energies, (len(fields), len(energies)))

#Detector identification
detector = nestpy.DetectorExample_XENON10()

# Performing NEST calculations according to the given detector example       
nc = nestpy.NESTcalc(detector)

#GetInteractionObject grabs the number for the interaction you want so you don't have to always reference the dictionary. Just type e.g., 'ion'
#It just changes the name to a number for nestpy to do its work.
def GetInteractionObject(name):
    name = name.lower()
    
    if name == 'er':
        raise ValueError("For 'er', specify either 'gammaray' or 'beta'")
    
    nest_interaction_number = dict(
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
    
    interaction_object = nestpy.INTERACTION_TYPE(nest_interaction_number[name])
    return interaction_object

#Once you have interaction, you can get yields
#Begin with np.vectorize so that we can get yields over a range of interaction types/energies/drift fields.

@np.vectorize
def GetYieldsVectorized(interaction, yield_type, **kwargs):
    # This function does nc.GetYields for the various interactions and arguments we pass into it
    # TODO: Look at docstrings
    interaction_object = GetInteractionObject(interaction)
    # problem is here with "nan" statements. 
    if 'energy' in kwargs.keys():
        if interaction_object == GetInteractionObject('nr') and kwargs['energy'] > 3e2:
            return np.nan
        if interaction_object == GetInteractionObject('gammaray') and kwargs['energy'] > 3e3:
            return np.nan
        if interaction_object == GetInteractionObject('beta') and kwargs['energy'] > 3e3:
            return np.nan     
    yield_object = nc.GetYields(interaction = interaction_object, **kwargs)
    # returns the yields for the type of yield we are considering be it ElectronYield or PhotonYield (an attribute of yield)
    return getattr(yield_object, yield_type)

#Gives us photon yield values
def PhotonYield(**kwargs):
    return GetYieldsVectorized(yield_type = 'PhotonYield', **kwargs)
#Gives electron yields    
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


#Plotting basics 
class Plotting:
    __version__ = '0.1.1'
# ## Nuclear Recoils Plotting 
    def nr_subplot(x, y_photons, y_electrons, driftFields, IMAGE_DICT):
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
        bbox = dict(boxstyle="round", fc="1.00")  
        ax1.text(energies[0][np.argmax(nr_photons)-35], 1, 
                    " NEST: v {0} \n Nestpy: v {1}".format(v_nest, v_nestpy), 
                    bbox=bbox, horizontalalignment='right', fontsize='x-large')
        ax2.text(energies[0][np.argmax(nr_photons)-35], 7.6, 
                    " NEST: v {0} \n Nestpy: v {1}".format(v_nest, v_nestpy), 
                    bbox=bbox, horizontalalignment='right', fontsize='x-large')

        ax1.set_ylabel('Light Yield [n$_\gamma$/keV]', fontsize=20)
        ax1.set_title('Light Yields for Nuclear Recoils', fontsize=24)
        ax2.set_title('Charge Yields for Nuclear Recoils', fontsize=24)
        ax2.set_ylabel('Charge Yield [n$_e$/keV]', fontsize=20) 
        fig1.tight_layout()
        fig2.tight_layout()
        fig1.savefig(IMAGE_DICT['nr_LY.png'])
        fig2.savefig(IMAGE_DICT['nr_QY.png'])

    def beta_subplot(x, y_photons, y_electrons, driftFields, IMAGE_DICT):
        fig1, ax1 = plt.subplots(1, 1, figsize=(9,6))
        fig2, ax2 = plt.subplots(1, 1, figsize=(9,6))
        bbox = dict(boxstyle="round", fc="0.95")
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
                    " NEST: v {0} \n Nestpy: v {1}".format(v_nest, v_nestpy), 
                    bbox=bbox, horizontalalignment='left', fontsize='x-large')
        ax2.text(energies[0][np.argmax(beta_electrons)-35], 74, 
                    " NEST: v {0} \n Nestpy: v {1}".format(v_nest, v_nestpy), 
                    bbox=bbox, horizontalalignment='right', fontsize='x-large')

        ax1.set_ylabel('Light Yield [n$_\gamma$/keV]', fontsize=20)
        ax1.set_title('Light Yields for $\\beta$ Electron Recoils', fontsize=24)
        ax2.set_title('Charge Yields for $\\beta$ Electron Recoils', fontsize=24)
        ax2.set_ylabel('Charge Yield [n$_e$/keV]', fontsize=20) 
        fig1.tight_layout()
        fig2.tight_layout()
        fig1.savefig(IMAGE_DICT['beta_LY.png'])
        fig2.savefig(IMAGE_DICT['beta_QY.png'])

    # # ## $\gamma$ electron recoils
    def gamma_subplot(x, y_photons, y_electrons, driftFields, IMAGE_DICT):
        fig1, ax1 = plt.subplots(1, 1, figsize=(9,6))
        fig2, ax2 = plt.subplots(1, 1, figsize=(9,6))
        bbox = dict(boxstyle="round", fc="0.95")
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
                    " NEST: v {0} \n Nestpy: v {1}".format(v_nest, v_nestpy), 
                    bbox=bbox, horizontalalignment='right', fontsize='x-large')
        ax2.text(energies[0][np.argmax(gamma_electrons)-35], 68, 
                    " NEST: v {0} \n Nestpy: v {1}".format(v_nest, v_nestpy), 
                    bbox=bbox, horizontalalignment='right', fontsize='x-large')

        ax1.set_ylabel('Light Yield [n$_\gamma$/keV]', fontsize=20)
        ax1.set_title('Light Yields for $\\gamma$ Electron Recoils', fontsize=24)
        ax2.set_title('Charge Yields for $\\gamma$ Electron Recoils', fontsize=24)
        ax2.set_ylabel('Charge Yield [n$_e$/keV]', fontsize=20) 
        fig1.tight_layout()
        fig2.tight_layout()
        fig1.savefig(IMAGE_DICT['gamma_LY.png'])
        fig2.savefig(IMAGE_DICT['gamma_QY.png'])

    # ## $\alpha$-particle recoils
    def alpha_subplot(x, y_photons, y_electrons, driftFields, IMAGE_DICT):
        fig1, ax1 = plt.subplots(1, 1, figsize=(9,6))
        fig2, ax2 = plt.subplots(1, 1, figsize=(9,6))
        bbox = dict(boxstyle="round", fc="0.95")
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
                    " NEST: v {0} \n Nestpy: v {1}".format(v_nest, v_nestpy), 
                    bbox=bbox, horizontalalignment='right', fontsize='x-large')
        ax2.text(energies[0][800], 3, 
                    " NEST: v {0} \n Nestpy: v {1}".format(v_nest, v_nestpy), 
                    bbox=bbox, horizontalalignment='right', fontsize='x-large')

        ax1.set_ylabel('Light Yield [n$_\gamma$/keV]', fontsize=20)
        ax1.set_title('Light Yields for $\\alpha$-Particle Nuclear Recoils', fontsize=24)
        ax2.set_title('Charge Yields for $\\alpha$-Particle Nuclear Recoils', fontsize=24)
        ax2.set_ylabel('Charge Yield [n$_e$/keV]', fontsize=20) 
        fig1.tight_layout()
        fig2.tight_layout()
        fig1.savefig(IMAGE_DICT['alpha_LY.png'])
        fig2.savefig(IMAGE_DICT['alpha_QY.png'])


    # ## $^{206}$Pb nuclear recoils
    def Pb_subplot(x, y_photons, y_electrons, driftFields, IMAGE):
        fig1, ax1 = plt.subplots(1, 1, figsize=(9,6))
        fig2, ax2 = plt.subplots(1, 1, figsize=(9,6))
        bbox = dict(boxstyle="round", fc="0.95")
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

        ax1.text(1.2, 5.3, 
                    " NEST: v {0} \n Nestpy: v {1}".format(v_nest, v_nestpy), 
                    bbox=bbox, horizontalalignment='left', fontsize='x-large')
        ax2.text(1.2, 0.85, 
                    " NEST: v {0} \n Nestpy: v {1}".format(v_nest, v_nestpy), 
                    bbox=bbox, horizontalalignment='left', fontsize='x-large')
        ax1.set_ylim(0,10)
        ax1.set_ylabel('Light Yields [n$_\gamma$/keV]', fontsize=20)
        ax1.set_title('Light Yields for Nuclear Recoils from $^{206}$Pb', fontsize=24)
        ax2.set_title('Charge Yields for Nuclear Recoils from $^{206}$Pb', fontsize=24)
        ax2.set_ylabel('Charge Yield [n$_e$/keV]', fontsize=20) 
        fig1.tight_layout()
        fig2.tight_layout()
        fig1.savefig(IMAGE['208Pb_LY.png'])
        fig2.savefig(IMAGE['208Pb_QY.png'])


    #Doing the actual functions
    # The following are the energy and field ranges for each interaction in the detector we care about showing.
    def makeplots(IMAGE_DICT):
        __version__ = '0.0.2'
        # Make in memory file objects for putting plots in
        nr_subplot(energies, nr_photons, nr_electrons, fields, IMAGE_DICT)
        beta_subplot(energies, beta_photons, beta_electrons, fields, IMAGE_DICT)
        gamma_subplot(energies, gamma_photons, gamma_electrons, fields, IMAGE_DICT)
        alpha_subplot(energies, alpha_photons, alpha_electrons, fields, IMAGE_DICT)
        Pb_subplot(energies, Pb_photons, Pb_electrons, fields, IMAGE_DICT)