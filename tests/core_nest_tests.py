import unittest
from nestpy.nestpy import VDetector, NESTcalc, YieldResult, QuantaResult, NESTresult, INTERACTION_TYPE
class NESTcalcTest(unittest.TestCase):

    def test_vdetector_const(self):
        detec = VDetector()
        detec.Initialization()

    def test_vdetector_fit_s1(self):
        detec = VDetector()
        detec.Initialization()
        detec.FitS1(1.0, 2.0, 3.0)

    def test_vdetector_fit_ef(self):
        detec = VDetector()
        detec.Initialization()
        detec.FitEF(1.0, 2.0, 3.0)

    def test_vdetector_fit_s2(self):
        detec = VDetector()
        detec.Initialization()
        detec.FitS2(1.0, 2.0)

    def test_vdetector_fit_tba(self):
        detec = VDetector()
        detec.Initialization()
        detec.FitTBA(1.0, 2.0, 3.0)

    def test_nestcalc_const(self):
        nest = NESTcalc()

    def test_nestcalc_const_vdetect(self):
        detec = VDetector()
        detec.Initialization()
        nest = NESTcalc(detec)

    def test_nestcalc_binom_fluct(self):
        detec = VDetector()
        detec.Initialization()
        nest = NESTcalc(detec)
        nest.BinomFluct(1, 20.)

    def test_nestcalc_full_calculation(self):
        detec = VDetector()
        detec.Initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5, [1, 1])

    def test_nestcalc_photon_time(self):
        detec = VDetector()
        detec.Initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5, [1, 1])
        nest.AddPhotonTransportTime(result.photon_times, 1.0, 2.0, 3.0)

    def test_nestcalc_add_photon_transport_time(self):
        detec = VDetector()
        detec.Initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5, [1, 1])
        nest.AddPhotonTransportTime(result.photon_times, 1.0, 2.0, 3.0)

    def test_nestcalc_get_photon_times(self):
        detec = VDetector()
        detec.Initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5, [1, 1])
        nest.GetPhotonTimes(int_type, 10, 10, 10., 10.)

    def test_nestcalc_get_yields(self):
        detec = VDetector()
        detec.Initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5, [1, 1])
        yields = nest.GetYields(int_type, 10., 10., 10., 10., 10., [1, 1])

    def test_nestcalc_get_quanta(self):
        detec = VDetector()
        detec.Initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5, [1, 1])
        yields = nest.GetYields(int_type, 10., 10., 10., 10., 10., [1, 1])
        quanta = nest.GetQuanta(yields, 10.)

    def test_nestcalc_get_s1(self):
        detec = VDetector()
        detec.Initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5, [1, 1])
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5, [1, 1])
        yields = nest.GetYields(int_type, 10., 10., 10., 10., 10., [1, 1])
        quanta = nest.GetQuanta(yields, 10.)
        nest.GetS1(quanta, 0, 1, 10., 10., int_type, 100, 10., 10., 0, False, [0,1,2], [0.,1.,2.])

    def test_nestcalc_get_spike(self):
        detec = VDetector()
        detec.Initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5, [1, 1])
        nest.GetSpike(10, 10., 20., 30., 10., 10., [0, 1, 2])


    def test_nestcalc_calculate_g2(self):
        detec = VDetector()
        detec.Initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5, [1, 1])
        nest.CalculateG2(True)

    def test_nestcalc_set_drift_velocity(self):
        detec = VDetector()
        detec.Initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5, [1, 1])
        nest.SetDriftVelocity(190, 10, 10)

    def test_nestcalc_set_drift_velocity_mag_boltz(self):
        detec = VDetector()
        detec.Initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5, [1, 1])
        nest.SetDriftVelocity_MagBoltz(10, 10)

    def test_nestcalc_set_drift_velocity_non_uniform(self):
        detec = VDetector()
        detec.Initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5, [1, 1])
        nest.SetDriftVelocity_NonUniform(190, 10, 10, 10)

    def test_nestcalc_set_denisty(self):
        detec = VDetector()
        detec.Initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5, [1, 1])
        nest.SetDensity(190, 10)


    def test_nestcalc_photon_energy(self):
        detec = VDetector()
        detec.Initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5, [1, 1])
        nest.PhotonEnergy(True, True, 190)

    def test_nestcalc_calc_electron_LET(self):
        detec = VDetector()
        detec.Initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5, [1, 1])
        nest.CalcElectronLET(100)

    def test_nest_calc_get_detector(self):
        detec = VDetector()
        detec.Initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        nest.GetDetector()


if __name__ == "__main__":
    unittest.main()