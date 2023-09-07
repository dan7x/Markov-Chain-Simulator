#include <vector>
#include <Eigen/Dense>

#ifndef SIMULATOR_H
#define SIMULATOR_H

class DTMC{

    private:
    // Analysis
    Eigen::MatrixXd n_transitionMatObj;
    Eigen::VectorXd n_stateDistObj;
    std::vector<Eigen::MatrixXd> n_transitionMat;
    std::vector<Eigen::VectorXd> n_stateDistnTheory;
    std::vector<Eigen::VectorXd> n_stateDistnActual;

    // Simulation
    Eigen::MatrixXd transitionMatrixObj;
    std::vector<std::string> states;
    std::vector<double> transitionMatrix; // zero-indexed p_ij = A[i * (size - 1) + j]
    Eigen::VectorXd stateCount;
    int size; // # of states
    int currentState;
    bool programmatic;

    public:
        EIGEN_MAKE_ALIGNED_OPERATOR_NEW
        DTMC(int size): 
        n_transitionMatObj{size, size},
        n_stateDistObj{size},
        transitionMatrixObj{size, size},  
        stateCount{size},
        size{size}, 
        currentState{0},
        programmatic{true}{};
        void read();
        void step(int n = 0);
        void summary();
    
    private:
        void nextState();
};

#endif
