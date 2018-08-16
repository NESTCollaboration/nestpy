from nestpy import nestpy
from types import *
import unittest
from enum import Enum

import sys

def trace(frame, event, arg):
    print "%s, %s:%d" % (event, frame.f_code.co_filename, frame.f_lineno)
    return trace

#   struct for YieldResult
class YieldResult:

    def __init__(self, photon_yield=0.0, electron_yield=0.0, exciton_ratio=0.0, lindhard=0.0, electric_field=0.0,
                 delta_t_scint=0.0):
        self.Yield = nestpy.YieldResult()
        self.Yield.PhotonYield = photon_yield
        self.Yield.ElectronYield = electron_yield
        self.Yield.ExcitonRatio = exciton_ratio
        self.Yield.Lindhard = lindhard
        self.Yield.ElectricField = electric_field
        self.Yield.DeltaT_Scint = delta_t_scint

    #   Setters for Parameters
    def set_photon_yield(self, photon_yield):
        self.Yield.PhotonYield = photon_yield

    def set_electron_yield(self, electron_yield):
        self.Yield.ElectronYield = electron_yield

    def set_exciton_ratio(self, exciton_ratio):
        self.Yield.ExcitonRatio = exciton_ratio

    def set_lindard(self, lindhard):
        self.Yield.Lindhard = lindhard

    def set_electric_field(self, electric_field):
        self.Yield.ElectricField = electric_field

    def set_delta_t_scint(self, delta_t_scint):
        self.Yield.DeltaT_Scint = delta_t_scint

    #   Getters for Parameters
    def get_photon_yield(self):
        return self.Yield.PhotonYield

    def get_electron_yield(self):
        return self.Yield.ElectronYield

    def get_exciton_ratio(self):
        return self.Yield.ExcitonRatio

    def get_lindard(self):
        return self.Yield.Lindhard

    def get_electric_field(self):
        return self.Yield.ElectricField

    def get_delta_t_scint(self):
        return self.Yield.DeltaT_Scint

    #   Print values of YieldResult
    def print_values(self):
        print("YieldResult;\n - Photon yield; %s\n - Electron yield; %s\n - Exciton ratio; %s\n - Lindhard; %s\n"
              " - Electric field; %s\n - Delta T Scint; %s\n" % (self.Yield.PhotonYield, self.Yield.ElectronYield,
                                                                 self.Yield.ExcitonRatio, self.Yield.Lindhard,
                                                                 self.Yield.ElectricField, self.Yield.DeltaT_Scint))


#   struct for QuantaResult
class QuantaResult:

    def __init__(self, photons = 0, electrons = 0, ions = 0, excitons = 0):
        self.Quanta = nestpy.QuantaResult()
        self.Quanta.photons = int(photons)
        self.Quanta.electrons = int(electrons)
        self.Quanta.ions = int(ions)
        self.Quanta.excitons = int(excitons)

    #   Setters for Parameters
    def set_photons(self, photons):
        self.Quanta.photons = photons

    def set_electrons(self, electrons):
        self.Quanta.electrons = electrons

    def set_ions(self, ions):
        self.Quanta.ions = ions

    def set_excitons(self, excitons):
        self.Quanta.excitons = excitons

    #   Getters for Parameters
    def get_photons(self):
        return self.Quanta.photons

    def get_electrons(self):
        return self.Quanta.electrons

    def get_ions(self):
        return self.Quanta.ions

    def get_excitons(self):
        return self.Quanta.excitons

    #   Print values of QuantaResult
    def print_values(self):
        print("QuantaResult;\n - photons; %s\n - electrons; %s\n - ions; %s\n - excitons; %s\n" % (self.Quanta.photons,
                                                                                                   self.Quanta.electrons,
                                                                                                   self.Quanta.ions,
                                                                                                   self.Quanta.excitons))


class INTERACTION_TYPE:

    def __init__(self, int_type):
        assert type(int_type) is IntType and int_type >= 0 and int_type <= 12, "int_type must be of type INT and " \
                                                                               "0 <= int_type <= 12!"
        self.type = nestpy.INTERACTION_TYPE(int_type)


#   struct for NESTresult
class NESTresult:

    def __init__(self, yields, quanta, photons_times, constructor_type=0):
        self.Nresult = nestpy.NESTresult()
        if constructor_type == 0:
            self.Nresult.yields = yields.Yield
            self.Nresult.quanta = quanta.Quanta
            self.yields = yields
            self.quanta = quanta
        else:
            self.Nresult.yields = yields
            self.Nresult.quanta = quanta
            self.yields = YieldResult(yields.PhotonYield, yields.ElectronYield, yields.ExcitonRatio, yields.Lindhard,
                                      yields.ElectricField, yields.DeltaT_Scint)
            self.quanta = QuantaResult(quanta.photons, quanta.electrons, quanta.ions, quanta.excitons)
            self.Nresult.photon_times = photons_times

    #   Setters for Parameters
    def set_yields(self, yields):
        self.Nresult.yields = yields.Yields

    def set_quanta(self, quanta):
        self.Nresult.quanta = quanta.Quanta

    def set_photon_times(self, photon_times):
        self.Nresult.photon_times = photon_times

    #   Getters for Parameters
    def get_yields(self):
        return self.yields

    def get_quanta(self):
        return self.quanta

    def get_photon_times(self):
        return self.Nresult.photon_times


#   class for VDetector
class VDetector:

    def __init__(self, detector=None):
        if detector is None:
            self.Detector = nestpy.VDetector()
        else:
            self.Detector = detector

    #   default initialization
    def initialization(self):
        self.Detector.Initialization()

    #   Setters for parameters
    def set_g1(self, g1):
        self.Detector.set_g1(g1)

    def set_sPEres(self, sPEres):
        self.Detector.set_sPEres(sPEres)

    def set_sPEthr(self, sPEthr):
        self.Detector.set_sPEthr(sPEthr)

    def set_sPEeff(self, sPEeff):
        self.Detector.set_sPEeff(sPEeff)

    def set_noise(self, noise_1, noise_2):
        self.Detector.set_noise(noise_1, noise_2)

    def set_P_dphe(self, P_dphe):
        self.Detector.set_P_dphe(P_dphe)

    def set_coinWind(self, coinWind):
        self.Detector.set_coinWind(coinWind)

    def set_coinLevel(self, coinLevel):
        self.Detector.set_coinLevel(int(coinLevel))

    def set_numPMTs(self, numPMTs):
        self.Detector.set_numPMTs(int(numPMTs))

    def set_g1_gas(self, g1_gas):
        self.Detector.set_g1_gas(g1_gas)

    def set_s2Fano(self, s2Fano):
        self.Detector.set_s2Fano(s2Fano)

    def set_s2_thr(self, s2_thr):
        self.Detector.set_s2_thr(s2_thr)

    def set_E_gas(self, E_gas):
        self.Detector.set_E_gas(E_gas)

    def set_eLife_us(self, eLife_us):
        self.Detector.set_eLife_us(eLife_us)

    def set_inGas(self, inGas):
        assert type(inGas) is bool, "inGas must be a bool"
        self.Detector.set_inGas(inGas)

    def set_T_Kelvin(self, T_Kelvin):
        self.Detector.set_T_Kelvin(T_Kelvin)

    def set_p_bar(self, p_bar):
        self.Detector.set_p_bar(p_bar)

    def set_dtCntr(self, dtCntr):
        self.Detector.set_dtCntr(dtCntr)

    def set_dt_min(self, dt_min):
        self.Detector.set_dt_min(dt_min)

    def set_dt_max(self, dt_max):
        self.Detector.set_dt_max(dt_max)

    def set_radius(self, radius):
        self.Detector.set_radius(radius)

    def set_radmax(self, radmax):
        self.Detector.set_radmax(radmax)

    def set_TopDrift(self, TopDrift):
        self.Detector.set_TopDrift(TopDrift)

    def set_anode(self, anode):
        self.Detector.set_anode(anode)

    def set_cathode(self, cathode):
        self.Detector.set_cathode(cathode)

    def set_gate(self, gate):
        self.Detector.set_gate(gate)

    def set_PosResExp(self, PosResExp):
        self.Detector.set_PosResExp(PosResExp)

    def set_PosResBase(self, PosResBase):
        self.Detector.set_PosResBase(PosResBase)

    #   Getters for parameters
    def get_g1(self):
        return self.Detector.get_g1()

    def get_sPEres(self):
        return self.Detector.get_sPEres()

    def get_sPEthr(self):
        return self.Detector.get_sPEthr()

    def get_sPEeff(self):
        return self.Detector.get_sPEeff()

    def get_noise(self):
        return self.Detector.get_noise()

    def get_P_dphe(self):
        return self.Detector.get_P_dphe()

    def get_coinWind(self):
        return self.Detector.get_coinWind()

    def get_coinLevel(self):
        return self.Detector.get_coinLevel()

    def get_numPMTs(self):
        return self.Detector.get_numPMTs()

    def get_g1_gas(self):
        return self.Detector.get_g1_gas()

    def get_s2Fano(self):
        return self.Detector.get_s2Fano()

    def get_s2_thr(self):
        return self.Detector.get_s2_thr()

    def get_E_gas(self):
        return self.Detector.get_E_gas()

    def get_eLife_us(self):
        return self.Detector.get_eLife_us()

    def get_inGas(self):
        return self.Detector.get_inGas()

    def get_T_Kelvin(self):
        return self.Detector.get_T_Kelvin()

    def get_p_bar(self):
        return self.Detector.get_p_bar()

    def get_dtCntr(self):
        return self.Detector.get_dtCntr()

    def get_dt_min(self):
        return self.Detector.get_dt_min()

    def get_dt_max(self):
        return self.Detector.get_dt_max()

    def get_radius(self):
        return self.Detector.get_radius()

    def get_radmax(self):
        return self.Detector.get_radmax()

    def get_TopDrift(self):
        return self.Detector.get_TopDrift()

    def get_anode(self):
        return self.Detector.get_anode()

    def get_cathode(self):
        return self.Detector.get_cathode()

    def get_gate(self):
        return self.Detector.get_gate()

    def get_PosResExp(self):
        return self.Detector.get_PosResExp()

    def get_PosResBase(self):
        return self.Detector.get_PosResBase()

    #   various functions
    def FitS1(self, xPos_mm, yPos_mm, zPos_mm):
        return self.Detector.FitS1(xPos_mm, yPos_mm, zPos_mm)

    def FitEF(self, xPos_mm, yPos_mm, zPos_mm):
        return self.Detector.FitEF(xPos_mm, yPos_mm, zPos_mm)

    def FitS2(self, xPos_mm, yPos_mm):
        return self.Detector.FitS2(xPos_mm, yPos_mm)

    def FitTBA(self, xPos_mm, yPos_mm, zPos_mm):
        return self.Detector.FitTBA(xPos_mm, yPos_mm, zPos_mm)

    def OptTrans(self, xPos_mm, yPos_mm, zPos_mm):
        return self.Detector.OptTrans(xPos_mm, yPos_mm, zPos_mm)

    def SinglePEWaveForm(self, area, t0):
        return self.Detector.SinglePEWaveForm(area, t0)

#   class for NESTcalc
class NESTcalc:

    def __init__(self, detector=None):
        if detector is None:
            self.calc = nestpy.NESTcalc()
        else:
            assert isinstance(detector, VDetector), "detector must be of type VDetector!"
            self.calc = nestpy.NESTcalc(detector.Detector)

    #   main NESTcalc functions
    def BinomFluct(self, x, y):
        return self.calc.BinomFluct(x, y)

    #   Full calculation
    def FullCalculation(self, species, energy, density, dfield, A, Z, NuisParam=[1, 1]):
        result = self.calc.FullCalculation(species.type, energy, density, dfield, A, Z, NuisParam)
        return(NESTresult(result.yields, result.quanta, result.photon_times, constructor_type=1))

    #   PhotonTime
    def PhotonTime(self, species, exciton, dfield, energy):
        return self.calc.PhotonTime(species.type, exciton, dfield, energy)

    #   AddPhotonTransportTime
    def AddPhotonTransportTime(self, emmited_times, x, y, z):
        return self.calc.AddPhotonTransportTime(emmited_times, x, y, z)

    #   GetPhotonTimes
    def GetPhotonTimes(self, species, total_photons, excitons, dfield, energy):
        return self.calc.GetPhotonTimes(species.type, total_photons, excitons, dfield, energy)

    #   GetYields
    def GetYields(self, species, energy, density, dfield, A, Z, NuisParam):
        result = self.calc.GetYields(species.type, energy, density, dfield, A, Z, NuisParam)
        return YieldResult(result.PhotonYield, result.ElectronYield, result.ExcitonRatio, result.Lindhard,
                                      result.ElectricField, result.DeltaT_Scint)

    #   GetQuanta
    def GetQuanta(self, yields, density):
        result =  self.calc.GetQuanta(yields.Yield, density)
        return QuantaResult(result.photons, result.electrons, result.ions, result.excitons)

    #   GetS1
    def GetS1(self, quanta, truthPos, smearPos, driftSpeed, dS_mid, species, evtNum, dfield, energy, useTiming,
              outputTiming, wf_time, wf_amp):
        return self.calc.GetS1(quanta.Quanta, truthPos, smearPos, driftSpeed, dS_mid, species.type, evtNum, dfield,
                               energy, useTiming, outputTiming, wf_time, wf_amp)

    #   GetSpike
    def GetSpike(self, Nph, dx, dy, dz, driftSpeed, dS_mid, origScint):
        return self.calc.GetSpike(Nph, dx, dy, dz, driftSpeed, dS_mid, origScint)

    #   GetS2
    def GetS2(self, Ne, truthPos, smearPos, dt, driftSpeed, evtNum, dfield, useTiming, outputTiming, wf_time, wf_amp,
              g2_params):
        return self.calc.GetS2(Ne, truthPos, smearPos, dt, driftSpeed, evtNum, dfield, useTiming, outputTiming, wf_time,
                               wf_amp, g2_params)

    #   CalculateG2
    def CalculateG2(self, verbosity):
        return self.calc.CalculateG2(verbosity)

    #   SetDriftVelocity
    def SetDriftVelocity(self, T, D, F):
        return self.calc.SetDriftVelocity(T, D, F)

    #   SetDriftVelocity_MagBoltz
    def SetDriftVelocity_MagBoltz(self, D, F):
        return self.calc.SetDriftVelocity_MagBoltz(D, F)

    #   SetDriftVelocity_NonUniform
    def SetDriftVelocity_NonUniform(self, rho, zStep, dx, dy):
        return self.calc.SetDriftVelocity_NonUniform(rho, zStep, dx, dy)

    #   SetDensity
    def SetDensity(self, T, P):
        return self.calc.SetDensity(T, P)

    #   xyResolution
    def xyResolution(self, xPos_mm, yPos_mm, A_top):
        return self.calc.xyResolution(xPos_mm, yPos_mm, A_top)

    #   PhotonEnergy
    def PhotonEnergy(self, s2Flag, state, tempK):
        return self.calc.PhotonEnergy(s2Flag, state, tempK)

    #   CalcElectronLET
    def CalcElectronLET(self, E):
        return self.calc.CalcElectronLET(E)

    #   GetDetector
    def GetDetector(self):
        return VDetector(self.calc.GetDetector())

class NESTcalcTestt(unittest.TestCase):
    # y = YieldResult(0, 1, 2, 3, 4, 5)
    # y.print_values()
    # z = QuantaResult(0, 1, 2, 3.)
    # z.print_values()
    # x = NESTresult(y, z, [1, 1, 1])
    #
    # detec = VDetector()
    # detec.initialization()
    # nest = NESTcalc(detec)
    # int_type = INTERACTION_TYPE(0)
    # result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5)

    def test_vdetector_const(self):
        detec = VDetector()
        detec.initialization()
        print(detec.OptTrans(1, 2, 3))

    def test_vdetector_fit_s1(self):
        detec = VDetector()
        detec.initialization()
        print(detec.FitS1(1.0, 2.0, 3.0))

    def test_vdetector_fit_ef(self):
        detec = VDetector()
        detec.initialization()
        print(detec.FitEF(1.0, 2.0, 3.0))

    def test_vdetector_fit_s2(self):
        detec = VDetector()
        detec.initialization()
        print(detec.FitS2(1.0, 2.0))

    def test_vdetector_fit_tba(self):
        detec = VDetector()
        detec.initialization()
        print(detec.FitTBA(1.0, 2.0, 3.0))

    def test_nestcalc_const(self):
        nest = NESTcalc()

    def test_nestcalc_const_vdetect(self):
        detec = VDetector()
        detec.initialization()
        nest = NESTcalc(detec)

    def test_nestcalc_binom_fluct(self):
        detec = VDetector()
        detec.initialization()
        nest = NESTcalc(detec)
        print(nest.BinomFluct(1, 20.))

    def test_nestcalc_full_calculation(self):
        detec = VDetector()
        detec.initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5)
        result.get_yields().print_values()
        result.get_quanta().print_values()
        print(result.get_photon_times())

    def test_nestcalc_photon_time(self):
        detec = VDetector()
        detec.initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5)
        print(nest.AddPhotonTransportTime(result.get_photon_times(), 1.0, 2.0, 3.0))

    def test_nestcalc_add_photon_transport_time(self):
        detec = VDetector()
        detec.initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5)
        print(nest.AddPhotonTransportTime(result.get_photon_times(), 1.0, 2.0, 3.0))

    def test_nestcalc_get_photon_times(self):
        detec = VDetector()
        detec.initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5)
        print(nest.GetPhotonTimes(int_type, 10, 10, 10., 10.))

    def test_nestcalc_get_yields(self):
        detec = VDetector()
        detec.initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5)
        nest.GetYields(int_type, 10., 10., 10., 10., 10., [1, 1]).print_values()

    def test_nestcalc_get_quanta(self):
        detec = VDetector()
        detec.initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5)
        nest.GetQuanta(result.get_yields(), 10.).print_values()

    def test_nestcalc_get_s1(self):
        detec = VDetector()
        detec.initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5)
        print(nest.GetS1(result.get_quanta(), 0, 1, 10., 10., int_type, 100, 10., 10., 0, False, [0,1,2], [0.,1.,2.]))

    def test_nestcalc_get_spike(self):
        detec = VDetector()
        detec.initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5)
        print(nest.GetSpike(10, 10., 20., 30., 10., 10., [0, 1, 2]))

    def test_nestcalc_get_s2(self):
        detec = VDetector()
        detec.initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5)
        print(nest.GetS2(10, 1, 1, 10., 10., 100, 10., 1, False, [0,1,2], [1,2,3], [1]))

    def test_nestcalc_calculate_g2(self):
        detec = VDetector()
        detec.initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5)
        print(nest.CalculateG2(True))

    def test_nestcalc_set_drift_velocity(self):
        detec = VDetector()
        detec.initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5)
        print(nest.SetDriftVelocity(190, 10, 10))

    def test_nestcalc_set_drift_velocity_mag_boltz(self):
        detec = VDetector()
        detec.initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5)
        print(nest.SetDriftVelocity_MagBoltz(10, 10))

    def test_nestcalc_set_drift_velocity_non_uniform(self):
        detec = VDetector()
        detec.initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5)
        print(nest.SetDriftVelocity_NonUniform(190, 10, 10, 10))

    def test_nestcalc_set_denisty(self):
        detec = VDetector()
        detec.initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5)
        print(nest.SetDensity(190, 10))

    def test_nestcalc_xy_resolution(self):
        detec = VDetector()
        detec.initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5)
        print(nest.xyResolution(100, 100, 100000))

    def test_nestcalc_photon_energy(self):
        detec = VDetector()
        detec.initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5)
        print(nest.PhotonEnergy(True, True, 190))

    def test_nestcalc_calc_electron_LET(self):
        detec = VDetector()
        detec.initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        result = nest.FullCalculation(int_type, 1., 2., 3., 4, 5)
        print(nest.CalcElectronLET(100))

    def test_nest_calc_get_detector(self):
        detec = VDetector()
        detec.initialization()
        nest = NESTcalc(detec)
        int_type = INTERACTION_TYPE(0)
        print(nest.GetDetector())


if __name__ == "__main__":
    #sys.settrace(trace)
    unittest.main()
