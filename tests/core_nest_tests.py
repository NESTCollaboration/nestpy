import unittest
import nestpy


class ConstructorTest(unittest.TestCase):
    """Test constructors

    These are used in the setup of later tests.  Therefore, seperate test
    here.
    """

    def test_vdetector_constructor(self):
        detector = nestpy.VDetector()
        assert detector is not None
        assert isinstance(detector, nestpy.VDetector)

    def test_vdetector_initialization(self):
        detector = nestpy.VDetector()
        detector.Initialization()
        assert detector is not None
        assert isinstance(detector, nestpy.VDetector)

    def test_xenon_example_constructor(self):
        detector = nestpy.DetectorExample_XENON10()
        assert detector is not None
        assert isinstance(detector, nestpy.DetectorExample_XENON10)

    def test_nestcalc_constructor(self):
        nestcalc = nestpy.NESTcalc()
        assert nestcalc is not None
        assert isinstance(nestcalc, nestpy.nestpy.NESTcalc)

    def test_nestcalc_constructor_vdetect(self):
        detector = nestpy.VDetector()
        detector.Initialization()
        nestcalc = nestpy.NESTcalc(detector)
        assert nestcalc is not None
        assert isinstance(nestcalc, nestpy.nestpy.NESTcalc)

    def test_intteraction_type_constructor(self):
        it = nestpy.INTERACTION_TYPE(0)
        assert it is not None
        assert str(it) != ""
        assert isinstance(it, nestpy.INTERACTION_TYPE)


class VDetectorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.detector = nestpy.VDetector()
        cls.detector.Initialization()

    def test_fit_s1(self):
        self.detector.FitS1(1.0, 2.0, 3.0)

    def test_fit_ef(self):
        self.detector.FitEF(1.0, 2.0, 3.0)

    def test_fit_s2(self):
        self.detector.FitS2(1.0, 2.0)

    def test_fit_tba(self):
        self.detector.FitTBA(1.0, 2.0, 3.0)


class NESTcalcTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.detector = nestpy.VDetector()
        cls.detector.Initialization()
        cls.it = nestpy.INTERACTION_TYPE(0)
        cls.nestcalc = nestpy.NESTcalc(cls.detector)

    def test_nestcalc_binom_fluct(self):
        binom = self.nestcalc.BinomFluct(1, 20.)
        assert binom > 0

    def test_interaction_type_constructor(self):
        for i in range(5):
            it = nestpy.nestpy.INTERACTION_TYPE(i)

    def test_nestcalc_full_calculation(self):
        result = self.nestcalc.FullCalculation(self.it, 1., 2., 3., 4, 5, [1, 1], [1,1], False)
        assert isinstance(result, nestpy.NESTresult)

    def test_nestcalc_get_photon_times(self):
        self.nestcalc.GetPhotonTimes(self.it, 10, 10, 10., 10.)

    def test_nestcalc_get_yields(self):
        yields = self.nestcalc.GetYields(
            self.it, 10., 10., 10., 10., 10., [1, 1])

    def test_nestcalc_get_spike(self):
        self.nestcalc.GetSpike(10, 10., 20., 30., 10., 10., [0, 1, 2])

    def test_nestcalc_calculate_g2(self):
        assert self.nestcalc.CalculateG2(True)[3] > 10

    def test_nestcalc_set_drift_velocity(self):
        self.nestcalc.SetDriftVelocity(190, 10, 10)

    def test_nestcalc_set_drift_velocity_mag_boltz(self):
        self.nestcalc.SetDriftVelocity_MagBoltz(10, 10)

    def test_nestcalc_set_drift_velocity_non_uniform(self):
        self.nestcalc.SetDriftVelocity_NonUniform(190, 10, 10, 10)

    def test_nestcalc_set_denisty(self):
        self.nestcalc.SetDensity(190, 10)

    def test_nestcalc_photon_energy(self):
        self.nestcalc.PhotonEnergy(True, True, 190)

    def test_nestcalc_calc_electron_LET(self):
        self.nestcalc.CalcElectronLET(100)

    def test_nest_calc_get_detector(self):
        self.nestcalc.GetDetector()


class NESTcalcFullCalculationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.detector = nestpy.VDetector()
        cls.detector.Initialization()
        cls.it = nestpy.INTERACTION_TYPE(0)
        cls.nestcalc = nestpy.NESTcalc(cls.detector)
        cls.result = cls.nestcalc.FullCalculation(
            cls.it, 10., 3., 100., 131, 56, 
            [11.,1.1,0.0480,-0.0533,12.6,0.3,2.,0.3,2.,0.5,1.],
            [1.,1.,0.1,0.5,0.07],            
            True)

    def test_nestcalc_photon_time(self):
        self.nestcalc.AddPhotonTransportTime(
            self.result.photon_times, 1.0, 2.0, 3.0)

    def test_nestcalc_add_photon_transport_time(self):
        self.nestcalc.AddPhotonTransportTime(
            self.result.photon_times, 1.0, 2.0, 3.0)

    def test_nestcalc_get_quanta(self):
        self.nestcalc.GetQuanta(self.result.yields, 10., [1,2,3])

    def test_nestcalc_get_s1(self):
        self.nestcalc.GetS1(self.result.quanta, 0, 1, 10., 10.,
                            self.it, 100, 10., 10., 0, False, [0, 1, 2], [0., 1., 2.])

class testNESTTest(unittest.TestCase):

    def test_testNEST_random_pos(self):
        detector = nestpy.DetectorExample_XENON10()
        #  test with -1 for fObs and seed (1)
        nestpy.testNEST(detector, 10, 'NR', 100., 120., 10., "0., 0., 0.", "120.", -1., 1, True)

    def test_testNEST_pos(self):
        detector = nestpy.DetectorExample_XENON10()
        #  test with actual position [0.,0.,0.] and seed(1)
        nestpy.testNEST(detector, 10, 'NR', 100., 120., 10., "0., 0., 10.", "120.",
                        1., 1, True) 

    def test_testNEST_pos_random_seed(self):
        detector = nestpy.DetectorExample_XENON10()
	#  test with actual position [0.,0.,0.] and randomSeed
        nestpy.testNEST(detector, 10, 'NR', 100., 120., 10., "0., 0., 10.", "120.", 1, 1, True)

    def test_testNEST_random_z(self):
        detector = nestpy.DetectorExample_XENON10()
	#  test with actual position [0.,0.,0.] and randomSeed
        nestpy.testNEST(detector, 10, 'NR', 100., 120., 10., "0., 0., -1", "120.", 1, 1, True)

    def test_testNEST_random_xy(self):
        detector = nestpy.DetectorExample_XENON10()
	#  test with actual position [0.,0.,0.] and randomSeed
        nestpy.testNEST(detector, 10, 'NR', 100., 120., 10., "-999, -999, 10.", "120", 1, 1, True)

if __name__ == "__main__":
    unittest.main()
