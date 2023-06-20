# Discrete Time Markov Chain Simulator

A simulator for discrete-time markov chain written in C++ (i will make visualizer soon :b).

Compile with:
```
g++ -std=c++17 dtmc.cpp main.cpp -o sim
```

Usage:
```
./sim < markovChainSpec.txt
```

Where the file is in the following format:
```
[# of states (the first one being the starting state)]
[# of simulated iterations]
[aliases for the states]
[transition matrix specified left-to-right, top-to-bottom]
```

For example:
```
2
1000
mcdonalds
tacobell
0.5 0.5
0.5 0.5
```

## Main.cpp

A Markov Chain with *n* states is initialized with:
```
DTMC x(size);
x.read(); // read in the dtmc file from stdin.
```

The simulation is then run as follows:
```
x.step(numberOfIterations); // simulate stepping through the states
x.summary(); // summarize the distribution visited states
```
