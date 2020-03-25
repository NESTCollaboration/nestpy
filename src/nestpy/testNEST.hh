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

int runNEST(VDetector* detector,
           double keV,
           INTERACTION_TYPE type_num,
           double inField,
           double pos_x, double pos_y, double pos_z,
           int seed);

// int runNEST_vec(VDetector* detector,
//            vector<double> keV,
//            INTERACTION_TYPE type_num,
//            double inField,
//            vector<double> pos_x, vector<double> pos_y, vector<double> pos_z,
//            int seed)

#endif
