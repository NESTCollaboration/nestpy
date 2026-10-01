import unittest
import nestpy
import platform

import awkward as ak
import numpy as np

class ConstructorTest(unittest.TestCase):
    """Test constructors

    These are used in the setup of later tests.  Therefore, seperate test
    here.
    """

    def test_vdetector_constructor(self):
        detector = nestpy.detectors.VDetector()
        assert detector is not None
        assert isinstance(detector, nestpy.detectors.VDetector)

    def test_vdetector_initialization(self):
        detector = nestpy.detectors.VDetector()
        detector.Initialization()
        assert detector is not None
        assert isinstance(detector, nestpy.detectors.VDetector)

    def test_xenon_example_constructor(self):
        detector = nestpy.detectors.DetectorExample_XENON10()
        assert detector is not None
        assert isinstance(detector, nestpy.detectors.DetectorExample_XENON10)

    def test_nestcalc_constructor_vdetect(self):
        detector = nestpy.detectors.VDetector()
        detector.Initialization()
        nestcalc = nestpy.NESTcalc(detector)
        assert nestcalc is not None
        assert isinstance(nestcalc, nestpy.NESTcalc)

    def test_intteraction_type_constructor(self):
        it = nestpy.interactions.NR
        assert it is not None
        assert str(it) != ""
        assert isinstance(it, nestpy.interactions)


class VDetectorTest(unittest.TestCase):

   @classmethod
   def setUpClass(cls):
       cls.detector = nestpy.detectors.VDetector()
       cls.detector.Initialization()
       cls.it = nestpy.interactions.NR
       cls.nestcalc = nestpy.NESTcalc(cls.detector)
       cls.nuisance = cls.nestcalc.default_nr_parameters
       cls.free = cls.nestcalc.default_nr_er_width_parameters
       cls.nestcalc = nestpy.NESTcalc(cls.detector)
   # def test_fit_s1(self):
   #     self.detector.FitS1(1.0, 2.0, 3.0)

   def test_fit_ef(self):
       self.detector.FitEF(1.0, 2.0, 3.0)

   # def test_fit_s2(self):
   #     self.detector.FitS2(1.0, 2.0, 3.0)

   def test_fit_tba(self):
       self.detector.FitTBA(1.0, 2.0, 3.0)


class NESTcalcTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.detector = nestpy.detectors.VDetector()
        cls.detector.Initialization()
        cls.it = nestpy.interactions.NR
        cls.nestcalc = nestpy.NESTcalc(cls.detector)

        cls.nuisance = cls.nestcalc.default_nr_parameters
        cls.free = cls.nestcalc.default_nr_er_width_parameters
        cls.er_params = cls.nestcalc.default_er_parameters

    def test_nestcalc_full_calculation(self):
        result = self.nestcalc.FullCalculation(self.it, 1., 2., 3., 4, 5,
                                               self.nuisance,
                                               self.free,
                                               self.er_params,
                                               False)
        assert isinstance(result, nestpy.NESTresult)

    def test_nestcalc_get_photon_times(self):
        self.nestcalc.GetPhotonTimes(self.it, 10, 10, 10., 10.)

    def test_nestcalc_get_yields(self):
        yields = self.nestcalc.GetYields(
            self.it, 10., 10., 10., 10., 10., self.nuisance)

    def test_nestcalc_get_yields_defaults(self):
        yields = self.nestcalc.GetYields(nestpy.interactions.NR,
                                         10)

    def test_nestcalc_get_yields_named(self):
        yields = self.nestcalc.GetYields(nestpy.interactions.NR,
                                         energy=10)

    # def test_nestcalc_get_spike(self):
    #     # This is stalling some builds. Need to improe the test.
    #     self.nestcalc.GetSpike(10, 10., 20., 30., 10., 10., [0, 1, 2])
    
    def test_nestcalc_get_yield_ER_weighted(self):
        self.nestcalc.GetYieldERWeighted(energy=5.2, 
                                         density=2.9, 
                                         drift_field=124, 
                                        )
    
    def test_nestcalc_calculate_g2(self):
        assert self.nestcalc.CalculateG2(True)[3] > 10

    def test_nestcalc_set_drift_velocity(self):
        self.nestcalc.SetDriftVelocity(190, 10, 10, 1.8)

    def test_nestcalc_set_drift_velocity_non_uniform(self):
        self.nestcalc.SetDriftVelocity_NonUniform(2.9, 1, 170, 1.8, 0., 0.)

    def test_nestcalc_set_denisty(self):
        self.nestcalc.SetDensity(190, 10)

    def test_nestcalc_photon_energy(self):
        self.nestcalc.PhotonEnergy(True, True, 190)

    def test_nestcalc_calc_electron_LET(self):
        # shouldn't have to set third argument..
        # but not a used feature by many so non-urgent to solve
        self.nestcalc.CalcElectronLET(100., 54, True) # energy, atom num.(Xe), CSDA

    def test_nest_calc_get_detector(self):
        self.nestcalc.GetDetector()

    def test_equality(self):
        # Will call a test for the nearlyEqual function to ensure it still works.
        self.nestcalc.GetYields(nestpy.interactions.NR, 100., 2.9, 100., 0., 54, nestpy.default_nr_parameters, nestpy.default_er_parameters)


class TestSpectraWIMPTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = nestpy.spectra
    
    def test_WIMP_spectrum(self):
        self.spec.WIMP_prep_spectrum( 50., 10. ) #mass and energy integration step
        self.spec.WIMP_spectrum( self.spec.WIMP_prep_spectrum( 50., 10. ), 50., 0. )


class NESTcalcFullCalculationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.detector = nestpy.detectors.VDetector()
        cls.detector.Initialization()
        cls.it = nestpy.interactions.NR

        cls.nestcalc = nestpy.NESTcalc(cls.detector)
        cls.nuisance = cls.nestcalc.default_nr_parameters
        cls.free = cls.nestcalc.default_nr_er_width_parameters
        cls.er_params = cls.nestcalc.default_er_parameters
        cls.result = cls.nestcalc.FullCalculation(
            cls.it, 10., 3., 100., 131, 56,
            cls.nuisance,
            cls.free,
            cls.er_params,
            True)

        cls.position = [2,3,4]

    def test_nestcalc_add_photon_transport_time(self):
       # print(self.result.photon_times)
       self.nestcalc.AddPhotonTransportTime(
           self.result.photon_times, 1.0, 2.0, 3.0)

    def test_nestcalc_get_quanta(self):
        self.nestcalc.GetQuanta(self.result.yields, 10., self.free)

    def test_nestcalc_get_quanta_defaults(self):
        self.nestcalc.GetQuanta(self.result.yields)

    def test_nestcalc_get_s1(self):
        self.nestcalc.GetS1(self.result.quanta,
                            10., 10., -30.,
                            10., 10., -30.,
                            10., 10.,
                            self.it,
                            100, 10., 10.,
                            nestpy.S1CalculationMode.Full, False,
                            [0, 1, 2],
                            [0., 1., 2.])

    def test_nestcalc_get_s2(self):
        self.nestcalc.GetS2(self.result.quanta.electrons, #int ne
                            10., 10., -30., #truth pos x y z
                            10., 10., -30., #smear pos x y z
                            10., 10.,
                            100, 10.,
                            nestpy.S2CalculationMode.Full, False,
                            [0, 1, 2],
                            [0., 1., 2.],
                            [0., 82., 2., 3., 4.])

    def test_nestcalc_get_xyresolution(self):
        self.detector = nestpy.detectors.DetectorExample_XENON10()
        self.detector.Initialization()
        self.nestcalc = nestpy.NESTcalc(self.detector)
        self.nestcalc.xyResolution(
                            0., 1.,2.)

class LArNESTTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.detector = nestpy.detectors.VDetector()
        cls.detector.Initialization()
        cls.it = nestpy.LArInteraction(0)

        cls.larnest = nestpy.LArNEST(cls.detector)
        cls.result = cls.larnest.full_calculation(
            cls.it, 100., 1., 500., 1.393, True
        )
    
    def test_larnest_get_yields(self):
        self.larnest.get_yields(self.it, 100., 1., 500., 1.393)

class RunNESTvecNumpyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.detector = nestpy.detectors.DetectorExample_XENON10()
        cls.it = nestpy.interactions.NR
        n = 300
        cls.energies = np.linspace(1., 50., n)
        cls.positions = np.column_stack((np.zeros(n), np.zeros(n), np.linspace(10., 110., n)))

    def simulate(self, energies=None, positions=None):
        return nestpy.array.runNESTvec(
            self.detector, self.it,
            self.energies if energies is None else energies,
            self.positions if positions is None else positions,
            seed=3)

    def test_numpy_input_matches_lists(self):
        from_arrays = self.simulate()
        from_lists = self.simulate(self.energies.tolist(), self.positions.tolist())
        self.assertEqual(from_arrays.to_list(), from_lists.to_list())
        # Other dtypes and memory layouts are converted
        self.simulate(self.energies.astype(np.float32), np.asfortranarray(self.positions))

    def test_invalid_shapes(self):
        for e, p in [(self.energies, self.positions.T), (self.energies, self.positions[:, :2]),
                     (self.energies[:, None], self.positions), (self.energies, self.positions[:-1])]:
            with self.assertRaises(ValueError):
                self.simulate(e, p)
        self.assertEqual(len(self.simulate([], [])), 0)

    def test_returns_awkward_array(self):
        result = self.simulate()
        self.assertIsInstance(result, ak.Array)
        self.assertEqual(len(result), len(self.energies))
        self.assertEqual(str(result.s1c_phd.type), "300 * float64")
        self.assertEqual(str(result.s1_photon_times.type), "300 * var * float64")
        # Fields share memory with the C++ result, which stays alive with them
        s1c_phd = ak.to_numpy(result.s1c_phd)
        self.assertFalse(s1c_phd.flags.writeable)
        expected = s1c_phd.tolist()
        del result
        self.assertEqual(s1c_phd.tolist(), expected)

    def test_run_nest(self):
        result = self.simulate()
        run = nestpy.helpers.run_nest(self.it, self.detector, self.energies, self.positions, seed=3)
        self.assertEqual(run[result.fields].to_list(), result.to_list())
        self.assertEqual(run["energy_keV"].to_list(), self.energies.tolist())

if __name__ == "__main__":
    unittest.main()
