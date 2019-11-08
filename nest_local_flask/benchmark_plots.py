import os
import io
import collections

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes as axes

import nestpy 
v_nestpy = str(nestpy.__version__)
v_nest = '2.0.1'

IMAGE_OBJECTS = collections.defaultdict(io.BytesIO)
# interaction_types = np.array(['nr','wimp','b8','dd','ambe','cf','ion', 'gammaray', 'beta', 'ch3t', 'c14', 'kr83m', 'nonetype'])

fields = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
energies = np.logspace(-1, 4, 2000)
energies = np.broadcast_to(energies, (len(fields), len(energies)))

#Detector identification
detector = nestpy.DetectorExample_XENON10()
# detector = nestpy.VDetector()
# Performing NEST calculations according to the given detector example       
nc = nestpy.NESTcalc(detector) #can also be left empty    


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
bbox = dict(boxstyle="round", fc="0.95")    
# ## Nuclear Recoils Plotting 
def nr_subplot(x, y_photons, y_electrons, driftFields):
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
                " NEST: v {0} \n Nestpy: v {1}".format(v_nest, v_nestpy), 
                bbox=bbox, horizontalalignment='right', fontsize='x-large')
    ax2.text(energies[0][np.argmax(nr_photons)-35], 7.6, 
                " NEST: v {0} \n Nestpy: v {1}".format(v_nest, v_nestpy), 
                bbox=bbox, horizontalalignment='right', fontsize='x-large')

    ax1.set_ylabel('Light Yields [n$_\gamma$/keV]', fontsize=20)
    ax1.set_title('Light Yields for Nuclear Recoils', fontsize=24)
    ax2.set_title('Charge Yields for Nuclear Recoils', fontsize=24)
    ax2.set_ylabel('Charge Yield [n$_e$/keV]', fontsize=20) 
    fig1.tight_layout()
    fig2.tight_layout()
    fig1.savefig(IMAGE_OBJECTS['nr_LY.png'])
    fig2.savefig(IMAGE_OBJECTS['nr_QY.png'])

def beta_subplot(x, y_photons, y_electrons, driftFields):
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

    ax1.set_ylabel('Light Yields [n$_\gamma$/keV]', fontsize=20)
    ax1.set_title('Light Yields for $\\beta$ Electron Recoils', fontsize=24)
    ax2.set_title('Charge Yields for $\\beta$ Electron Recoils', fontsize=24)
    ax2.set_ylabel('Charge Yield [n$_e$/keV]', fontsize=20) 
    fig1.tight_layout()
    fig2.tight_layout()
    fig1.savefig(IMAGE_OBJECTS['beta_LY.png'])
    fig2.savefig(IMAGE_OBJECTS['beta_QY.png'])

# # ## $\gamma$ electron recoils
def gamma_subplot(x, y_photons, y_electrons, driftFields):
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

    ax1.set_ylabel('Light Yields [n$_\gamma$/keV]', fontsize=20)
    ax1.set_title('Light Yields for $\\gamma$ Electron Recoils', fontsize=24)
    ax2.set_title('Charge Yields for $\\gamma$ Electron Recoils', fontsize=24)
    ax2.set_ylabel('Charge Yield [n$_e$/keV]', fontsize=20) 
    fig1.tight_layout()
    fig2.tight_layout()
    fig1.savefig(IMAGE_OBJECTS['gamma_LY.png'])
    fig2.savefig(IMAGE_OBJECTS['gamma_QY.png'])

# ## $\alpha$-particle recoils
def alpha_subplot(x, y_photons, y_electrons, driftFields):
    plt.figure(7, figsize=(9,6))
    subplot1 = plt.subplot(111)
    plt.figure(8, figsize=(9,6))
    subplot2 = plt.subplot(111)
    for i in range(0, len(driftFields)):
        subplot1.plot(x[i,:], y_photons[i,:], label="{0} V/cm".format(driftFields[i]))
        subplot2.plot(x[i,:], y_electrons[i,:], label="{0} V/cm".format(driftFields[i]))   

    #Just formatting to look presentable    
    subplot1.set_xscale('log')
    subplot2.set_xscale('log')
    subplot1.set_ylim(bottom=0)
    subplot2.set_ylim(bottom=0)
    subplot1.set_xlim(1, 1e4)
    subplot2.set_xlim(1, 1e4)
    
    subplot1.legend(loc='best', fontsize= 9, ncol=2)
    subplot1.set_xlabel('Energy [keV]')
    subplot1.set_ylabel('Light Yields [n$_\gamma$/keV]')
    subplot1.set_title('Light Yields for $\\alpha$-Particle Nuclear Recoils')
    subplot1.margins(0)         
    subplot2.legend(loc='best', fontsize= 9, ncol=2)    
    subplot2.set_xlabel('Energy [keV]')
    subplot2.set_title('Charge Yields for $\\alpha$-Particle Nuclear Recoils')
    subplot2.set_ylabel('Charge Yield [n$_e$/keV]') 
    subplot2.margins(0)

    #Here's where we are actually saving our plots! 
    plt.figure(7)
    plt.tight_layout()
    plt.savefig(IMAGE_OBJECTS['alpha_LY.png'])
    plt.figure(8)
    plt.tight_layout()
    plt.savefig(IMAGE_OBJECTS['alpha_QY.png'])


# ## $^{206}$Pb nuclear recoils
def Pb_subplot(x, y_photons, y_electrons, driftFields):
    plt.figure(9, figsize=(9,6))
    subplot1 = plt.subplot(111)
    plt.figure(10, figsize=(9,6))
    subplot2 = plt.subplot(111)
    for i in range(0, len(driftFields)):
        subplot1.plot(x[i,:], y_photons[i,:], label="{0} V/cm".format(driftFields[i]))
        subplot2.plot(x[i,:], y_electrons[i,:], label="{0} V/cm".format(driftFields[i]))
        
    subplot1.set_xscale('log')
    subplot2.set_xscale('log')
    subplot1.set_ylim(0, 10)
    subplot1.set_xlim(1, 1e2)
    subplot2.set_ylim(bottom=0)
    subplot2.set_xlim(1, 1e2)
    
    subplot1.legend(loc='best', fontsize= 10, ncol=3)
    subplot1.set_xlabel('Energy [keV]')
    subplot1.set_ylabel('Light Yields [n$_\gamma$/keV]')
    subplot1.set_title('Light Yields for Nuclear Recoils from $^{206}$Pb')      
    subplot2.legend(loc='best', fontsize= 10, ncol=3)    
    subplot2.set_xlabel('Energy [keV]')
    subplot2.set_title('Charge Yields for Nuclear Recoils from $^{206}$Pb')
    subplot2.set_ylabel('Charge Yield [n$_e$/keV]') 

    #Here's where we are actually saving our plots! 
    plt.figure(9)
    plt.tight_layout()
    plt.savefig(IMAGE_OBJECTS['208Pb_LY.png'])
    plt.figure(10)
    plt.tight_layout()
    plt.savefig(IMAGE_OBJECTS['208Pb_QY.png'])


#Doing the actual functions
# The following are the energy and field ranges for each interaction in the detector we care about showing.
def makeplots():
    # Make in memory file objects for putting plots in
    num_interactions = 5 #number of types of interactions we're studying, so we can make enough plots.
    nr_electrons = ElectronYield(interaction='nr', energy=energies.T, drift_field = fields).T/energies
    nr_photons = PhotonYield(interaction='nr', energy=energies.T, drift_field = fields).T/energies
    nr_subplot(energies, nr_photons, nr_electrons, fields)

    beta_electrons = ElectronYield(interaction='beta', energy=energies.T, drift_field = fields).T/energies
    beta_photons = PhotonYield(interaction='beta', energy=energies.T, drift_field = fields).T/energies
    beta_subplot(energies, beta_photons, beta_electrons, fields)

    gamma_electrons = ElectronYield(interaction='gammaray', energy=energies.T, drift_field = fields).T/energies
    gamma_photons = PhotonYield(interaction='gammaray', energy=energies.T, drift_field = fields).T/energies
    gamma_subplot(energies, gamma_photons, gamma_electrons, fields)

    alpha_electrons = ElectronYield(interaction='ion', Z=2, A = 4, energy=energies.T, drift_field = fields).T/energies
    alpha_photons = PhotonYield(interaction='ion',Z=2, A=4, energy=energies.T, drift_field = fields).T/energies
    alpha_subplot(energies, alpha_photons, alpha_electrons, fields)

    Pb_electrons = ElectronYield(interaction='ion', Z=82, A = 206, energy=energies.T, drift_field = fields).T/energies
    Pb_photons = PhotonYield(interaction='ion',Z=82, A=206, energy=energies.T, drift_field = fields).T/energies
    Pb_subplot(energies, Pb_photons, Pb_electrons, fields)
