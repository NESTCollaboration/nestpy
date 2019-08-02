import unittest


class nestpyExamplesTest(unittest.TestCase):

    def test_readme_example(self):
        import nestpy

        # This is same as C++ NEST with naming
        nc = nestpy.NESTcalc()
        A = 131.293
        Z = 54.
        density = 2.9  # g/cm^3
        
        interaction = nestpy.INTERACTION_TYPE(0)  # NR
        
        E = 10  # keV
        print('For an %s keV %s' % (E, interaction))
        
        # Nuisance parameters: see NEST.cpp to know how to adjust
        # these defaults.
        nuisance_parameters = [11., 1.1, 0.0480, -0.0533, 12.6,
                               0.3, 2., 0.3, 2., 0.5, 1.]
        
        # Get particle yields
        y = nc.GetYields(interaction,
                         E,
                         density,
                         124,  # Drift field, V/cm
                         A,
                         Z,
                         nuisance_parameters)
        
        print('The photon yield is:', y.PhotonYield)
        print('With statistical fluctuations',
              nc.GetQuanta(y, density,
                           nuisance_parameters
              ).photons)

if __name__ == "__main__":
    unittest.main()
