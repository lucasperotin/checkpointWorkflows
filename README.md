-------HOW TO USE-------

Requirements: 
	python3
	C++17
	workflowhub (install with "python3 -m pip install workflowhub")

STEP 1: Generate the workflows
"python3 generate_pegasus.py nbs s"
nbs is the requested number of tasks for each sample, and s is the number of workflow per workflow type. This will generate s workflows of n tasks for each type, output these workflow in text with .json format.
Repeat this if you want to test for several value of n.
For the experiment, we used 
"python3 generate_pegasus.py 8840 30"
"python3 generate_pegasus.py 12500 30"
"python3 generate_pegasus.py 17680 30"
"python3 generate_pegasus.py 25000 30"
"python3 generate_pegasus.py 35350 30"
"python3 generate_pegasus.py 50000 30"
"python3 generate_pegasus.py 70700 30"

WARNING: for large values of n (as in our experiment), you will need lot of space


STEP 2: Transform the workflows to match our in-home simulator
Simply use
"g++ transformer.cpp"
"./a.out"


STEP 3: Specify the parameters of your experiments
Open generate-args.py
Specify the values of p,c,u,n you want to test. at the top of the code. Here p corresponds to the total number of processors, and u to the MTBF. 
Specify the base values (For example, if p is varied, these will be the values of the other parameters)
The values used for our experiment are in the file.
Type "python3 generate-args.py nbs nbf nbm"
nbs is the number of sample workflow you want to test for each set of parameters
nbf is the number of failure scenario you want to generate for each sample
nbm is the number of cores at your disposal in your own machine to run the experiment
For the experiment we used "python3 generate-args.py 30 50 6"

This will generate a launch file you will use later

WARNINGS: the specified n must mached the one you used in STEP 1. The nbs you use must be smaller or equal than the one used in STEP 1


STEP 4: Compile the simulator
just type "g++ simu.cc -O3"

WARNING: Do not specify an outfile, as it will make launch fail

STEP 5: Launch experiment
Use "bash launch"
Each line appearing will correspond to one sample and one set of parameters simulated. 

STEP 6: Generate plots
Open plotter.py
Specify the values of p,c,u,n, as well as the base values. They must match what you wrote in generate-args.py
Write "python3 plotter.py id", where id is an identifier for the name of the files in case you want to run several experiments
This will generate 4 plots for each workflow type, as well as one plot for a comparaison of all workflow, located in ./results/plots

STEP 7: clear all files used except plot
Use "bash clean"

