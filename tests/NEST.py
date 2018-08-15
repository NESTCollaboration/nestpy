from nestpy import nestpy
from types import *

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


#   struct for NESTresult
class NESTresult:

    def __init__(self, yields, quanta, photons_times):
        self.Nresult = nestpy.NESTresult()
        self.Nresult.yields = yields.Yield
        self.Nresult.quanta = quanta.Quanta
        self.Nresult.photon_times = photons_times

        self.yields = self.Nresult.yields
        self.quanta = self.Nresult.quanta
        self.photon_times = self.Nresult.photon_times


#   class for VDetector
class VDetector:

    def __init__(self):
        self.Detector = nestpy.VDetector()

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

    def __init__(self):
        self.calc = nestpy.NESTcalc()

if __name__ == "__main__":
    y = YieldResult(0,1,2,3,4,5)
    y.print_values()
    z = QuantaResult(0,1,2,3.)
    z.print_values()
    x = NESTresult(y, z, [1,1,1])

    detec = VDetector()
    detec.initialization()
    print(detec.OptTrans(1,2,3))