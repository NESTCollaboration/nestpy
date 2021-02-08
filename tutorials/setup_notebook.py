import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from matplotlib import cm
from matplotlib.colors import LogNorm
from scipy.stats import gaussian_kde, norm, skewnorm
from scipy.optimize import curve_fit
import pandas as pd
import numpy as np


import pprint
pp = pprint.PrettyPrinter(indent=4)

import nestpy 
print('nestpy version: v'+nestpy.__version__)
print('NEST version: v'+nestpy.__nest_version__)

plt.rcParams['xtick.labelsize']=12
plt.rcParams['ytick.labelsize']=12
plt.rcParams['xtick.direction']='out'
plt.rcParams['ytick.direction']='out'

plt.rcParams['xtick.major.size']=10
plt.rcParams['ytick.major.size']=10
plt.rcParams['xtick.major.pad']=5
plt.rcParams['ytick.major.pad']=5

plt.rcParams['xtick.minor.size']=5
plt.rcParams['ytick.minor.size']=5
plt.rcParams['xtick.minor.pad']=5
plt.rcParams['ytick.minor.pad']=5

font_small = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }

font_medium = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 20,
        }

font_large = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 24,
        }
params = {'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large',
         }
# Updates plots to apply the above formatting to all plots in doc
pylab.rcParams.update(params)