# Discrete Time Markov Chain Simulator and Analyzer

A simulator and analyzer for discrete-time markov chains written in Python/C++.

# Python Version

todo: write this

pip install pipfile and run viz.py

# C++ Version

## Requires
- [Eigen-3.4.0](https://eigen.tuxfamily.org/index.php?title=Main_Page)

Run `make` to compile.

## Usage

The program consumes a (time-homogenous) discrete time markov chain specification along with some simulation params (see below) and returns the results of a simulated random walk from the starting state given the simulation parameters.

Run with the following (assume the txt file contains the chain and simulation specs):
```
./sim < markovChainSpec.txt
```

The sim files have the following format:
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
Denotes the following chain:

[img]

### Annotated Sample Output:
```
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
