#include <iostream>
#include <vector>
#include "simulator.h"

int main(){
    std::string input;
    std::cout << "Enter number of states:" << std::endl;
    std::cin >> input; 
    int size = std::stoi(input);

    DTMC x(size);
    x.read();
    x.step(1000);

    return 0;
}
