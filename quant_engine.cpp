#include <iostream>
#include <vector>
#include <numeric>
#include <cmath>
#include <string>

using namespace std;

double getMean(const vector<double>& data) {
    double sum = accumulate(data.begin(), data.end(), 0.0);
    return sum / data.size();
}

double getStdDev(const vector<double>& data, double mean) {
    double sq_sum = 0;
    for (double val : data) sq_sum += (val - mean) * (val - mean);
    return sqrt(sq_sum / data.size());
}

int main(int argc, char* argv[]) {
    if (argc < 4) {
        cout << "{\"error\": \"Insufficient data points provided.\"}" << endl;
        return 1;
    }

    string operation = argv[1];
    vector<double> data;
    
    for (int i = 2; i < argc; ++i) {
        data.push_back(stod(argv[i]));
    }

    if (operation == "zscore") {
        double current_val = data.back();
        data.pop_back();
        
        double mean = getMean(data);
        double std_dev = getStdDev(data, mean);
        
        double z_score = 0;
        if (std_dev > 0) z_score = (current_val - mean) / std_dev;

        cout << "{\"operation\": \"zscore\", \"mean\": " << mean 
             << ", \"std_dev\": " << std_dev 
             << ", \"z_score\": " << z_score << "}" << endl;
    } 
    else {
        cout << "{\"error\": \"Unknown operation requested.\"}" << endl;
        return 1;
    }

    return 0;
}