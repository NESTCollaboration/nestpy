
import nestpy 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes as axes
import os

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
    
    if 'energy' in kwargs.keys():
        if interaction_object == GetInteractionObject('nr') and kwargs['energy'] > 3e2:
            return np.nan
    if interaction_object == GetInteractionObject('gammaray') and kwargs['energy'] > 3e3:
            return np.nan
    if interaction_object == GetInteractionObject('beta') and kwargs['energy'] > 3e3:
            return np.nan     
    yield_object = nc.GetYields(interaction = interaction_object, **kwargs)
    #this returns the yields for the type of yield we are considering be it ElectronYield or PhotonYield (an attribute of yield)
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


#we are able to do nestpy with 13 different interaction types and that's all we're going to use here.
# interaction_types = np.array(['nr','wimp','b8','dd','ambe','cf','ion', 'gammaray', 'beta', 'ch3t', 'c14', 'kr83m', 'nonetype'])

fields = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
energies = np.logspace(-1, 4, 2000)
energies = np.broadcast_to(energies, (len(fields), len(energies)))

file_path = './Images/'
directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    os.makedirs(directory)

# ## Nuclear Recoils
def nr_subplot(x, y_photons, y_electrons, driftFields):
    plt.figure(1, figsize=(9,6))
    subplot1 = plt.subplot(111)
    plt.figure(2, figsize=(9,6))
    subplot2 = plt.subplot(111)
    for i in range(0, len(driftFields)-2):
        subplot1.plot(x[i,:], y_photons[i,:], label="{0} V/cm".format(driftFields[i]))
        subplot2.plot(x[i,:], y_electrons[i,:], label="{0} V/cm".format(driftFields[i]))   

    #Just formatting to look presentable    
    subplot1.set_xscale('log')
    subplot2.set_xscale('log')
    subplot1.set_ylim(bottom=0)
    subplot2.set_ylim(bottom=0)
    
    subplot1.legend(loc='best', fontsize= 9, ncol=3)
    subplot1.set_xlabel('Recoil Energy [keV]')
    subplot1.set_ylabel('Light Yields [n$_\gamma$/keV]')
    subplot1.set_title('Light Yields for Nuclear Recoils')
    subplot1.margins(0)         
    subplot2.legend(loc='best', fontsize= 9, ncol=3)    
    subplot2.set_xlabel('Recoil Energy [keV]')
    subplot2.set_title('Charge Yields for Nuclear Recoils')
    subplot2.set_ylabel('Charge Yield [n$_e$/keV]') 
    subplot2.margins(0)

    #Here's where we are actually saving our plots! 
    plt.figure(1)
    plt.tight_layout()
    plt.savefig(os.path.join(file_path, 'nr_LY.png'))
    plt.figure(2)
    plt.tight_layout()
    plt.savefig(os.path.join(file_path, 'nr_QY.png'))


def beta_subplot(x, y_photons, y_electrons, driftFields):
    plt.figure(3, figsize=(9,6))
    subplot1 = plt.subplot(111)
    plt.figure(4, figsize=(9,6))
    subplot2 = plt.subplot(111)
    for i in range(0, len(driftFields)):
        subplot1.plot(x[i,:], y_photons[i,:], label="{0} V/cm".format(driftFields[i]))
        subplot2.plot(x[i,:], y_electrons[i,:], label="{0} V/cm".format(driftFields[i]))   

    #Just formatting to look presentable    
    subplot1.set_xscale('log')
    subplot2.set_xscale('log')
    subplot1.set_ylim(bottom=0)
    subplot2.set_ylim(bottom=0)
    
    subplot1.legend(loc='best', fontsize= 9, ncol=1)
    subplot1.set_xlabel('Energy [keV]')
    subplot1.set_ylabel('Light Yields [n$_\gamma$/keV]')
    subplot1.set_title('Light Yields for $\\beta$ Electron Recoils')
    subplot1.margins(0)         
    subplot2.legend(loc='best', fontsize= 9, ncol=1)    
    subplot2.set_xlabel('Energy [keV]')
    subplot2.set_title('Charge Yields for $\\beta$ Electron Recoils')
    subplot2.set_ylabel('Charge Yield [n$_e$/keV]') 
    subplot2.margins(0)
    
    #Here's where we are actually saving our plots! 
    plt.figure(3)
    plt.tight_layout()
    plt.savefig(os.path.join(file_path, 'beta_LY.png'))
    plt.figure(4)
    plt.tight_layout()
    plt.savefig(os.path.join(file_path, 'beta_QY.png'))


# ## $\gamma$ electron recoils
def gamma_subplot(x, y_photons, y_electrons, driftFields):
    plt.figure(5, figsize=(9,6))
    subplot1 = plt.subplot(111)
    plt.figure(6, figsize=(9,6))
    subplot2 = plt.subplot(111)
    for i in range(0, len(driftFields)):
        subplot1.plot(x[i,:], y_photons[i,:], label="{0} V/cm".format(driftFields[i]))
        subplot2.plot(x[i,:], y_electrons[i,:], label="{0} V/cm".format(driftFields[i]))   

    #Just formatting to look presentable    
    subplot1.set_xscale('log')
    subplot2.set_xscale('log')
    subplot1.set_ylim(bottom=0)
    subplot2.set_ylim(bottom=0)
    
    subplot1.legend(loc='best', fontsize= 9, ncol=1)
    subplot1.set_xlabel('Energy [keV]')
    subplot1.set_ylabel('Light Yields [n$_\gamma$/keV]')
    subplot1.set_title('Light Yields for $\\gamma$ Electron Recoils')
    subplot1.margins(0)         
    subplot2.legend(loc='best', fontsize= 9, ncol=1)    
    subplot2.set_xlabel('Energy [keV]')
    subplot2.set_title('Charge Yields for $\\gamma$ Electron Recoils')
    subplot2.set_ylabel('Charge Yield [n$_e$/keV]') 
    subplot2.margins(0)

    #Here's where we are actually saving our plots! 
    plt.figure(5)
    plt.tight_layout()
    plt.savefig(os.path.join(file_path, 'gamma_LY.png'))
    plt.figure(6)
    plt.tight_layout()
    plt.savefig(os.path.join(file_path, 'gamma_QY.png'))


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
    plt.savefig(os.path.join(file_path, 'alpha_LY.png'))
    plt.figure(8)
    plt.tight_layout()
    plt.savefig(os.path.join(file_path, 'alpha_QY.png'))


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
    plt.savefig(os.path.join(file_path, '208Pb_LY.png'))
    plt.figure(10)
    plt.tight_layout()
    plt.savefig(os.path.join(file_path, '208Pb_QY.png'))


#Doing the actual functions
# The following are the energy and field ranges for each interaction in the detector we care about showing.
def makeplots():
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

# makeplots()