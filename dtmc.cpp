#include <iostream>
#include <format>
#include <vector>
#include <random>
#include <iterator>
#include "simulator.h"

void DTMC::read(){
    // Read in the properties of the DTMC

    std::string input;
    std::cout << "Enter a unique identifier for each state:" << std::endl;
    for(int i = 0; i < size; ++i){
        std::cin >> input;

        // todo: check unique
        states.push_back(input);
        stateCount.push_back(0);
    }
    const int transitionMatrixSize = size * size;
    std::cout 
    << "Provide the entries in the transition matrix p_ij. Expecting a " 
    << size << " X " << size 
    << "matrix (" << transitionMatrixSize << "entries)."
    << std::endl;

    for(int i = 0; i < transitionMatrixSize; ++i){
        std::cin >> input;
        // todo: check valid
        double p_ij = std::stod(input);
        transitionMatrix.push_back(p_ij);
    }
    // assert stochastic row-wise

    // for(auto it = transitionMatrix.begin(); it < transitionMatrix.end(); ++it){
    //     std::cout << *it << std::endl;
    // }
}

void DTMC::step(int count){
    // count is the number of steps to advance.

    // assert count > 0
    for(int i = 0; i < count; ++i){
        nextState();
    }
}

void DTMC::nextState(){
    int fromStateRow = currentState * size;
    std::vector<double>::iterator fromStateRowIterStart = transitionMatrix.begin() + fromStateRow; // start of transition row
    std::vector<double>::iterator fromStateRowIterEnd = fromStateRowIterStart + size; // end of transition row

    // std::cout << "dist: " << std::distance(fromStateRowIterStart, fromStateRowIterEnd) << std::endl;
    // for(auto it = fromStateRowIterStart; it < fromStateRowIterEnd; ++it){
    //     std::cout << "; pij = " << *it << std::endl;
    // }

    std::discrete_distribution<std::size_t> pij{fromStateRowIterStart, fromStateRowIterEnd};
    std::mt19937 gen(std::random_device{}());

    int nextState = pij(gen);

    std::cout << "Moving from state " << states[currentState] << " to next state " << states[nextState] << std::endl;
    ++stateCount[currentState];
    currentState = nextState;
}
