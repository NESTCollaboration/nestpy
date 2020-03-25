#ifndef __TESTNEST_H__
#define __TESTNEST_H__ 1

using namespace std;
using namespace NEST;

vector<vector<double>> GetBand(vector<double> S1s, vector<double> S2s,
                               bool resol);

void GetEnergyRes(vector<double> Es);

int testNEST(VDetector* detector, unsigned long int numEvts, string type,
             double eMin, double eMax, double inField, string position, string posiMuon,
             double fPos, int seed, bool no_seed);


struct NESTObservable{
  int s1_nhits_phd;
  int s1_nhits_phe;
  double s1r_phe;
  double s1c_phe;
  double s1r_phd;
  double s1c_phd;

  int Nee;
  double s2r_phe;
  double s2c_phe;
  double s2r_phd;
  double s2c_phd;
};

struct NESTObservableArray{

  vector<int> s1_nhits_phd;
  vector<int> s1_nhits_phe;
  vector<double> s1r_phe;
  vector<double> s1c_phe;
  vector<double> s1r_phd;
  vector<double> s1c_phd;

  vector<int> Nee;
  vector<double> s2r_phe;
  vector<double> s2c_phe;
  vector<double> s2r_phd;
  vector<double> s2c_phd;

  // NESTObservable(int n_events){
  //   s1_nhits_phd.reserve(n_events);
  //   s1_nhits_phe.reserve(n_events);
  //   s1r_phe.reserve(n_events);
  //   s1c_phe.reserve(n_events);
  //   s1r_phd.reserve(n_events);
  //   s1c_phd.reserve(n_events);
  //
  //   Nee.reserve(n_events);
  //   s2r_phe.reserve(n_events);
  //   s2c_phe.reserve(n_events);
  //   s2r_phd.reserve(n_events);
  //   s2c_phd.reserve(n_events);
  // }
};


NESTObservable runNEST(
    VDetector* detector,
    double keV,
    INTERACTION_TYPE type_num,
    double inField,
    double pos_x, double pos_y, double pos_z,
    int seed);

NESTObservableArray runNEST_vec(
    VDetector* detector,
    vector<double> keV_vec,
    INTERACTION_TYPE type_num,
    double inField,
    vector<double> pos_x_vec, vector<double> pos_y_vec, vector<double> pos_z_vec,
    int seed);

#endif
