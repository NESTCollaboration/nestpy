import unittest
import nestpy


class nestpyExamplesTest(unittest.TestCase):

    def test_readme_example(self):
        # This is same as C++ NEST with naming
        nc = nestpy.NESTcalc()

        A = 131.293
        Z = 54.
        density = 2.9  # g/cm^3

        interaction = nestpy.INTERACTION_TYPE(0)  # NR
        E = 10  # keV
        print('For an %s keV %s' % (E, interaction))

        # Get particle yields
        y = nc.GetYields(interaction,
                         E,
                         density,
                         124,  # Drift field, V/cm
                         A,
                         Z,
                         (1, 1))

        print('The photon yield is:', y.PhotonYield)

        print('With statistical fluctuations',
              nc.GetQuanta(y, density).photons)

if __name__ == "__main__":
    unittest.main()
