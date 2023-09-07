#include <iostream>
#include <format>
#include <vector>
#include <random>
#include <iterator>
#include <numeric>
#include <Eigen/Dense>
#include "simulator.h"
#include "eigenutil.h"

using std::cin, std::cout, std::endl;

void DTMC::read(){
    // Read in the properties of the DTMC 

    std::string input;
    cout << "Enter a unique identifier for each state:" << endl;
    for(int i = 0; i < size; ++i){
        cin >> input;

        // todo: check unique
        states.push_back(input);
        stateCount(i) = 0;
        n_stateDistObj(i) = 0;
    }
    stateCount[0] = 1;
    n_stateDistObj(0) = 1;
    const int transitionMatrixSize = size * size;
    cout 
    << "Provide the entries in the transition matrix p_ij. Expecting a " 
    << size << " X " << size 
    << " matrix (" << transitionMatrixSize << " entries)."
    << endl;

    for(int i = 0; i < transitionMatrixSize; ++i){
        cin >> input;
        // todo: check valid
        double p_ij = std::stod(input);
        transitionMatrix.push_back(p_ij);
    }
    // assert stochastic row-wise

    for(int i = 0; i < size; ++i){
        for(int j = 0; j < size; ++j){
            int ij = i * size + j;
            double pij = transitionMatrix[ij];
            transitionMatrixObj.row(i)(j) = transitionMatrix[ij];
            // cout << "P(" << states[i] << " -> " << states[j] << ") = " << pij << endl;
        }
    }
    // cout << "tobj" << endl << transitionMatrixObj << endl;

    // for(auto it = transitionMatrix.begin(); it < transitionMatrix.end(); ++it){
    //     cout << *it << endl;
    // }
}

/// @brief Simulate n steps thru the markov chain.
/// @param n 
void DTMC::step(int n){
    // count is the number of steps to advance.

    // Initialize the n-th transition matrix to matrix for n=1
    n_transitionMatObj = transitionMatrixObj;

    // assert count > 0?
    for(int i = 0; i < n; ++i){
        nextState();
    }

    // Push the final state of things
    Eigen::MatrixXd final_transitionMat = n_transitionMatObj;
    n_transitionMat.push_back(final_transitionMat);

    Eigen::VectorXd final_stateCount = stateCount;
    n_stateDistnActual.push_back(final_stateCount);

    // cout << "ass : " << n_stateDistObj.cols() << " -- " << transitionMatrixObj.rows() << endl;
    // Record the previous theoretical state distn
    Eigen::VectorXd final_theroyStateCount = n_stateDistObj;
    n_stateDistnTheory.push_back(final_theroyStateCount);

}

void DTMC::nextState(){
    int fromStateRow = currentState * size;
    std::vector<double>::iterator fromStateRowIterStart = transitionMatrix.begin() + fromStateRow; // start of transition row
    std::vector<double>::iterator fromStateRowIterEnd = fromStateRowIterStart + size; // end of transition row

    // cout << "dist: " << std::distance(fromStateRowIterStart, fromStateRowIterEnd) << endl;
    // for(auto it = fromStateRowIterStart; it < fromStateRowIterEnd; ++it){
    //     cout << "; pij = " << *it << endl;
    // }

    std::discrete_distribution<std::size_t> pij{fromStateRowIterStart, fromStateRowIterEnd};
    std::mt19937 gen(std::random_device{}());

    int nextState = pij(gen);

    // cout << "Moving from state " << states[currentState] << " to next state " << states[nextState] << endl;
    currentState = nextState;
    // ++stateCount[currentState];

    // Record the discarded transition matrix
    Eigen::MatrixXd old_transitionMat = n_transitionMatObj;
    n_transitionMat.push_back(old_transitionMat);
    n_transitionMatObj *= transitionMatrixObj;

    // Record the previous actual state distn
    Eigen::VectorXd old_stateCount = stateCount;
    n_stateDistnActual.push_back(old_stateCount);
    ++stateCount(currentState);

    // cout << "ass : " << n_stateDistObj.cols() << " -- " << transitionMatrixObj.rows() << endl;
    // Record the previous theoretical state distn
    Eigen::VectorXd old_theroyStateCount = n_stateDistObj;
    n_stateDistnTheory.push_back(old_theroyStateCount);
    n_stateDistObj = transitionMatrixObj.transpose() * n_stateDistObj;
}

void DTMC::summary(){
    std::string delim = "====";
    if(programmatic){
        cout << delim << endl;
        cout << states[currentState] << endl;
    }else{
        // see non-programmatic for expected ordering
        cout << "== Properties ==" << endl;
        cout << "Final State: " << states[currentState] << endl;
    }

    if(programmatic){
        cout << delim << endl;
    }else{
        cout << "== Transition probabilities ==" << endl;
    }
    for(int i = 0; i < size; ++i){
        for(int j = 0; j < size; ++j){
            int ij = i * size + j;
            double pij = transitionMatrix[ij];
            cout << "P(" << states[i] << " -> " << states[j] << ") = " << pij << endl;
        }
    }

    int totalIterations = std::accumulate(stateCount.begin(), stateCount.end(), 0);
    // The final state count
    if(programmatic){
        cout << delim << endl;
    }else{
        cout << "== Final Distribution of visited states ==" << endl;
    }
    for(int i = 0; i < size; ++i){
        int ct = stateCount[i];
        double pct = 100 * ct / totalIterations;
        cout << states[i] << ": " << ct << " (" << pct << "%)" << endl;
    }

    int n = 0;
    // The n-th transition matrix (i.e., probability that in n iterations, you
    // move from state i on time 0, to state j at time n)
    if(programmatic){
        cout << delim << endl;
    }else{
        cout << "== N-th Transition Probabilities [P_ij(n)] ==" << endl;
    }
    for(const auto &m: n_transitionMat){
        cout << "n = " << n << endl << m << endl;
        ++n;
    }
    n = 0;

    // Probability of being on each state at time n, given you start at the provided start state
    if(programmatic){
        cout << delim << endl;
    }else{
        cout << "== N-th Actual State Frequencies [\\pi_\\infinity] ==" << endl;
    }
    for(const auto &pi: n_stateDistnActual){
        cout << "n = " << n << " - " << pi.transpose() << endl;
        ++n;
    }
    n = 0;

    // Theoretical probability of being on each state at time n, given you start at the provided start state
    if(programmatic){
        cout << delim << endl;
    }else{
        cout << "== N-th Theoretical State Probabilities [\\pi_n] ==" << endl;
    }
    for(auto const &pij_n: n_stateDistnTheory){
        cout << "n = " << n << " - " << pij_n.transpose() << endl;
        ++n;
    }

    // Eigen::MatrixXd m(2,2);
    // m(0,0) = 0.9;
    // m(1,0) = 0.1;
    // m(0,1) = 0.9;
    // m(1,1) = 0.1;
    // cout << m << endl;

    // cout << "sol: " << endl;
    if(programmatic){
        cout << delim << endl;
    }else{
        cout << "== Theoretical Stationary Distribution ==" << endl;
    }
    std::vector<std::tuple<float, Eigen::VectorXd>> eigen_results = EigenUtil::get_eigenvals_vecs(transitionMatrixObj);
    for(auto const &v : eigen_results){
        cout << "Eigenvalue: " << std::get<0>(v) << endl;
        cout << "Eigenvector: " << endl;
        cout << std::get<1>(v) << endl;
    }
}


