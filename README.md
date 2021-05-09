# phenylpropanoids-model
##### A probablistic CTMC model used to simulate the biosynthetic microbial production of various phenylpropanoids. 

### Contents
The main pathway file is included in pathway.sm. This file, in and of itself, contains the entire model with both modules, and the simulation of different phenotypes, concentrations, pathways, or other deviations are typically done through commenting and uncommenting certain parts of the code. For example, to test different homologs of STS, one would remove the comments from the four lines that define that homolog (146-149 for AhSTS), and leave the other 12 lines (150-161) commented out. To remove ACC from the biosynthetic pathway, one would comment out that enzyme's command statement (line 167). For both modules, the model defines the kinetic parameters and rates for each enzyme above the module, and then uses commands to represent that enzyme within the module, using the previously defined rates. At the end of the model, reward statements exist to allow for the appropriate data to be collected. Typically, model checking and stochastic simulation in PRISM only allow for probabilities of events to be calculated, and not the actual values of variables. Any time these reward structures are evaluated, they return the value of the variable that they coorespond with, which is the micromolar concentration of each species.

Currently, two property files exist to facilitate the simulation of the model, resveratrolReward and resveratrolMassReward. Both of these reward structures return the amount of resveratrol produced at a specific time T, defined by the user. resveratrolReward returns the value of resveratrol_produced, which is resveratrol concentration in units of uM, and resveratrolMassReward returns the value of resveratrol_produced_mass, which is resveratrol concentration in units of mg/L. New property files can easily be constructed for any reward in the model by following the syntax of any existing property file and changing the reward name.

### Running the Model
To simulate resveratrol production with PRISM, the following command is used:

```prism pathway.sm resveratrolMassReward.csl -sim -simsamples 100 -const T=172800 -v -cuddmaxmem 110g```

The resveratrolMassReward.csl parameter is the property file to run, and can be changed to any property file that cooresponds with a desired reward. In this case, the model will simulate the production of resveratrol in mg/L.

The `-sim` switch causes PRISM to use stochastic simulation rather than comprehensive model checking. This switch can be omitted if model checking is desired. The associated `-simsamples` switch defines how many simulation runs should be used and averaged to produce the final result. This switch should also be omitted if model checking is desired. 

The `-const T=t` switch defines the time that the model will simulate to, referencing the variable T that is defined in the csl file. The time is in seconds, and 172800 seconds is equal to two days, or 48 hours. If the concentrations over a range of time is desired, the following can be used instead:

```-const T=0.0:3600.0:172800.0 ```

With this switch, PRISM will simulate the result every 3600 seconds, up to the final time, 172800 seconds, starting at 0 seconds. These specific values are used to generate plots of the model, but any values can be used for the start, step, and stop time.

The `-v` switch causes verbose output, and can be omitted if desired.

Finally, the `-cuddmaxmem` switch defined the amount of memory to use while running the model. The standard computer for running this model has 128gb of RAM, so 110g is a common value for this switch. However, this value can and should be changed depending on the avaliable memory in the computer. The g at the end of the integer represents GB, and m for MB and k for KB can also be used.

### Notes
Both old folders, old-f20 and old-s21, contain old versions of the project that could potentially be useful in the future, mostly in the form of the inclusion of more native and recombinant enzymes. The contents of these folders are not documented.



###### Utah State University 
###### Biological Engineering Department
###### Electrical & Computer Engineering Department
###### 2019-2021