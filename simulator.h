#include <vector>

#ifndef SIMULATOR_H
#define SIMULATOR_H

class DTMC{

    private:
    std::vector<std::string> states;
    std::vector<double> transitionMatrix; // zero-indexed p_ij = A[i * (size - 1) + j]
    std::vector<int> stateCount;
    int size; // # of states
    int currentState;
    
    public:
        DTMC(int size): size{size}, currentState{0}{}
        void read();
        void step(int count = 0);
        void summary();
    
    private:
        void nextState();
};

#endif
