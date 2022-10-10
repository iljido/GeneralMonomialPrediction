# GeneralMonomialPrediction


This repository contains the source code for the paper "On the Field-Based Division Property: Applications to MiMC, Feistel MiMC and GMiMC".


## 1. Main components of the codes

The codes for the basic general monomial propagation operations are provided in the file "basic/basic.py".

The codes for MiMC, Feistel MiMC and GMiMC are provided in the folder named by the algorithm. For example, the folder "MiMC" contains several important files:

"mimc_lib.py" : this file defines functions for the general monomial propagation of MiMC.

"mimc_d3.py" : this file shows the implementation of general monomial prediction for MiMC.


## 2. How to use codes

We take MiMC as an example.

First we need to install STP and CRYPTOMINISAT and configure "PATH_CRYPTOMINISAT" and "PATH_STP" in "basic/basic.py" and "mimc_d3.py".

Switch to the folder "MiMC" and edit "mimc_d3.py" to set the "Round" and block size "n" you are interested in.

Type `python3 mimc_d3.py` in the console to run the program.





