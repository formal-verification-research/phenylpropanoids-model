import csv
import math
import numpy.polynomial
from scipy.optimize import brentq
import os.path
import subprocess
import matplotlib.pyplot as plt
from datetime import datetime

# Normal distribution is given by:
#          1      -((x-u)^2)/(2s^2)
# y = -----------e
#     s*sqrt(2pi)
# Where s is the standard deviation of the curve and m is the mean
#
# We will fit each time to a normal distribution dependent on concentration
#
#   Linearized:
#              1      (x-u)^2
# ln(y) = -----------(-------)
#         s*sqrt(2pi)  2s^2
#
# And we can use quadratic regression:

# C - list of concentrations
# P - list of probabilities at those concentrations
def fit_to_dist(c, p, vfind):
    c = [float(i) for i in c]
    p = [float(i) for i in p]
    sum = p[len(p)-1]
    for i in range(len(p) - 2, -1, -1):
        p[i] -= sum
        sum += p[i]
    for i in range(len(p)-1, -1, -1):  # Linearize data
        if p[i] <= 0:
            p.pop(i)
            c.pop(i)
        elif p[i] >= 1:
            return c[i], 0, 0
        else:
            p[i] = math.log(p[i])
    if len(c) == 2:
        if c[1] > c[0]:
            if vfind:
                return c[1], 0, 0
            else:
                return c[1]
        else:
            if vfind:
                return c[0], 0, 0
            else:
                return c[0]
    if len(c) == 1:
        if vfind:
            return c[0], 0, 0
        else:
            return c[0]
    if len(c) == 0:
        print("Not enough data to fit to a quadratic")
        return False, False, False  # Not enough data to fit to a quadratic

    coeff = numpy.polyfit(c, p, 2)  # Fit linearized data to a quadratic
    if (coeff[2] > 0 and coeff[0] < 0) or (coeff[2] < 0 and coeff[0] > 0):
        return 0, 0, 0
    u = math.sqrt(coeff[2]/coeff[0])

    if vfind is True:   # Calculate standard deviation and r squared
        ndistfunc = lambda x: (math.log(x*math.sqrt(2*math.pi)))/(2*x)
        s = brentq(ndistfunc, 0.00000000000000000001, 1)

        # r-squared:
        pol = numpy.poly1d(coeff)
        phat = pol(c)                         # or [p(z) for z in x]
        pbar = numpy.sum(p)/len(p)          # or sum(y)/len(y)
        ssreg = numpy.sum((phat-pbar)**2)   # or sum([ (yihat - ybar)**2 for yihat in yhat])
        sstot = numpy.sum((p - pbar)**2)    # or sum([ (yi - ybar)**2 for yi in y])
        rsqrd = (ssreg/sstot)

        return u, s, rsqrd#, coeff

    return u

'''
fit_to_dist test code:
temp_c = [0, 0.5, 1, 1.5, 1.75, 2.15, 2.5, 3, 3.5, 4]
# temp_p = [0.00026766, 0.0088637, 0.10798193, 0.48394145, 0.7413065, 0.7413065, 0.48394145, 0.10798193, 0.0088637, 0.00026766]
temp_p = [0.00026766+0.0088637+0.10798193+0.48394145+0.7413065+0.7413065+0.48394145+0.10798193+0.0088637+0.00026766, 0.0088637+0.10798193+0.48394145+0.7413065+0.7413065+0.48394145+0.10798193+0.0088637+0.00026766, 0.10798193+0.48394145+0.7413065+0.7413065+0.48394145+0.10798193+0.0088637+0.00026766, 0.48394145+0.7413065+0.7413065+0.48394145+0.10798193+0.0088637+0.00026766, 0.7413065+0.7413065+0.48394145+0.10798193+0.0088637+0.00026766, 0.7413065+0.48394145+0.10798193+0.0088637+0.00026766, 0.48394145+0.10798193+0.0088637+0.00026766, 0.10798193+0.0088637+0.00026766, 0.0088637+0.00026766, 0.00026766]
print(fit_to_dist(temp_c, temp_p, True))
'''

print("This script has the capability of doing any of three things:\n" +
      "1. Analyze a prism model with model checking or simulation and export the model checking results into a readable, concise output\n" +
      "2. Build a properties model based on concentration steps at different time intervals\n" +
      "3. Fit concentration data at different timepoints to a normal distribution, building a graph of most probable concentration over time")
runnumber = datetime.now().strftime("%m%d%Y-%H%M%S")
print("This run is number " + runnumber + ".\n")
# dir = input("Path to the prism directory: ")
# print("Path to the prism directory: C:/Program Files/prism-4.5/bin")
# dir = "C:/Program Files/prism-4.5/bin"
runb = ""
while runb.lower() != "y" and runb.lower() != "n":
    runb = input("Run a PRISM model? (y/n) ")
if runb.lower() == "y":
    runb = True
else:
    runb = False
if runb:
    model = input("Name of the PRISM model (.sm) to run: ")
    # prop = input("Name of the property file (.csl) to run: ")
    output_directory = input("(Optional) Name of the directory to write to: ")
    if len(output_directory) != 0 and (output_directory[-1] != '/' or output_directory[-1] != '\\'):
        output_directory += "/"
    sorm = ""
    while sorm.lower() != "s" and sorm.lower() != "m":
        sorm = input("Enter an m to check the model, or s if the model is a simulation: ")
    if sorm.lower() == "s":
        simn = input("(Optional) Number of simulations to run: ")
        catch_str_start = "Simulating: P=? [ F[0,"
        catch_str_end = "\n"
    else:
        catch_str_start = "Model checking: P=? [ F[0,"
        catch_str_end = " (value"
    memory = input("(Optional) Enter the amount of memory to use for the model: ")

    propb = ""
    while propb.lower() != "y" and propb.lower() != "n":
        propb = input("Create new properties file? (y/n) ")
    if propb == "y":
        tmax = int(input("Final time: "))
        dt = int(input("Time step to check: "))
        varname = input("Variable to check: ")

        varn = 0
        propname = output_directory + "prop" + runnumber + ".csl"
        props = open(propname, "w+")
        while varname != "":
            varn += 1
            cmax = int(input("Maximum concentration to check for " + varname + ": "))
            dc = int(input("Concentration step to check for " + varname + ": "))
            for t in range(0, tmax, dt):
                for c in range(0, cmax, dc):
                    props.write("P=?[F[0," + str(t+dt) + "] (" + varname + ">=" + str(c) + " & " + varname + "<" + str(c + dc) + ")]\n")
            varname = input("Variable to check (press enter when finished): ")
        props.close()

        print("Created properties file of size " + str(os.path.getsize(propname)/1000) + "kb as prop" + runnumber + ".csl")
    else:
        propname = input("Name of properties file to run (.csl): ")

    print("\nPRISM is running the model...\n")
    prism_input ="prism"
    if sorm == "s":
        if simn is None or simn == "":
            prism_input += " -sim"
        else:
            prism_input += (" -simsamples " + simn)
    prism_input += (" " + model + " " + propname)
    if memory != "":
        prism_input += (" -cuddmaxmem " + memory)
    '''
    # print(prism_input)
    prism_output = subprocess.check_output(prism_input, universal_newlines=True, shell=True)
    # print(prism_output)
    '''
    prism_output = ""
    process = subprocess.Popen(prism_input, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    while True:
        output = process.stdout.readline()
        if process.poll() is not None and output == '':
            break
        if output:
            print(">>> " + output.strip())
            prism_output += output
    retval = process.poll()

    concise_output = "time\tconcentration\tprobability\n"
    i = 0
    varname = ""

    while prism_output.find(catch_str_start, i + 1) >= 0:
        ii = prism_output.find('] (', i + 1) + 3
        jj = prism_output.find('>=', i)
        if varname != prism_output[ii:jj]:
            varname = prism_output[ii:jj]
            concise_output += "variable: " + varname + "\n"
        i = prism_output.find(catch_str_start, i + 1) + len(catch_str_start)
        j = prism_output.find('] (', i)
        concise_output += prism_output[i:j] + "\t"
        i = prism_output.find('>=', i + 1)+2
        j = prism_output.find('&', i)
        concise_output += prism_output[i:j] + "\t"
        i = prism_output.find('Result: ', i + 1)+8
        j = prism_output.find(catch_str_end, i)
        concise_output += prism_output[i:j] + "\n"
        # if sorm != 's': concise_output += "\n"

    concise_output += '\n\n\n\n\nRAW OUTPUT:\n\n\n' + prism_output

    with open(output_directory+"prismrun"+runnumber+".txt", 'w+') as file:
        file.write(concise_output)

    analyze = input("Model successfully ran with output " + output_directory + "prismrun" + runnumber + ".txt\n" +
                    "Analyze data as normal distribution concentration data? (y/n) ")

    if analyze != "y":
        raise SystemExit(0)

    modelname = output_directory+"prismrun"+runnumber+".txt"

else:
    modelname = input("Name of previous model run to analyze: ")
    output_directory = input("(Optional) Name of the directory to write to: ")
    if len(output_directory) != 0 and (output_directory[-1] != '/' or output_directory[-1] != '\\'):
        output_directory += "/"

statb = ''
while statb != 'y' and statb != 'n':
    statb = input("Include statistical analysis with each data point? (y/n) ")
if statb == 'n':
    statb = False
else:
    statb = True

graphb = ''
while graphb != 'y' and graphb != 'n':
    graphb = input("Plot data? (y/n) ")
if graphb == 'n':
    graphb = False
else:
    graphb = True
    graphx = []
    graphy = []

data = list(csv.reader(open(modelname, 'r+'), delimiter='\t'))
#data = list(csv.reader(open("testrunoutput.txt", 'r+'), delimiter='\t'))
dlistc = [0]
dlistp = [0]
time = "-1"
varname = ""
newvarname = ""
header = True
i = 0
resveratrolx = []
resveratroly = []

plt.figure()

if statb:
    print("var\ttime\tmean\tstdev\trsqared")
    processed_output = "var\ttime\tmean\tstdev\trsqared\n"
else:
    print("var\ttime\tconcentration")
    processed_output = "var\ttime\tconcentration\n"

for line in data:
    #print(line)
    if header:
        if len(line) == 0 or line[0] == 'time':
            continue
        elif len(line) == 1:
            varname = line[0][line[0].find("variable: ") + 10:]
            newvarname = line[0][line[0].find("variable: ") + 10:]
            # print("variable: " + varname)
        else:
            time = line[0]
            dlistc = [line[1]]
            dlistp = [line[2]]
            header = False
    if len(line) == 3:
        if line[0] != time:  # new time set, process the old data
            # print("Finished time set at " + time + ":\n" + str(dlistc) + "\n" + str(dlistp))
            if statb:
                u, s, r = fit_to_dist(dlistc, dlistp, statb)
                if u == False:
                    print(varname + "\t" + time + "\tN\tN\tN\tNot enough data at timepoint to fit to normal distribution")
                    processed_output += varname + "\t" + time + "\tN\tN\tN\tNot enough data at timepoint to fit to normal distribution\n"
                else:
                    print(varname + "\t" + time + "\t" + str(u) + "\t" + str(s) + "\t" + str(r))
                    processed_output += varname + "\t" + time + "\t" + str(u) + "\t" + str(s) + "\t" + str(r) + "\n"
            else:
                u = fit_to_dist(dlistc, dlistp, statb)
                if u == False:
                    print(varname + "\t" + time + "\tN\tNot enough data at timepoint to fit to normal distribution")
                    processed_output += varname + "\t" + time + "\tN\tNot enough data at timepoint to fit to normal distribution\n"
                else:
                    print(varname + "\t" + time + "\t" + str(u))
                    processed_output += varname + "\t" + time + "\t" + str(u) + "\n"
            if graphb:
                graphx.append(float(time))
                graphy.append(u)
            if varname != newvarname:
                plt.plot(graphx, graphy, c=numpy.random.rand(3, ), label=varname)
                if varname == "resveratrol":
                    resveratrolx = list(graphx)
                    resveratroly = list(graphy)
                graphx.clear()
                graphy.clear()
                i += 1
                varname = newvarname
            time = line[0]
            dlistc = [line[1]]
            dlistp = [line[2]]
        else:
            dlistc.append(line[1])
            dlistp.append(line[2])
    else:
        if len(line) == 0:
            continue
        elif line[0] == 'RAW OUTPUT:':
            if statb:
                u, s, r = fit_to_dist(dlistc, dlistp, statb)
                if u == False:
                    print(
                        varname + "\t" + time + "\tN\tN\tN\tNot enough data at timepoint to fit to normal distribution")
                    processed_output += varname + "\t" + time + "\tN\tN\tN\tNot enough data at timepoint to fit to normal distribution\n"
                else:
                    print(varname + "\t" + time + "\t" + str(u) + "\t" + str(s) + "\t" + str(r))
                    processed_output += varname + "\t" + time + "\t" + str(u) + "\t" + str(s) + "\t" + str(r) + "\n"
            else:
                u = fit_to_dist(dlistc, dlistp, statb)
                if u == False:
                    print(varname + "\t" + time + "\tN\tNot enough data at timepoint to fit to normal distribution")
                    processed_output += varname + "\t" + time + "\tN\tNot enough data at timepoint to fit to normal distribution\n"
                else:
                    print(varname + "\t" + time + "\t" + str(u))
                    processed_output += varname + "\t" + time + "\t" + str(u) + "\n"
            if graphb:
                graphx.append(float(time))
                graphy.append(u)
            if varname != newvarname:
                plt.plot(graphx, graphy, c=numpy.random.rand(3, ), label=varname)
                if varname == "resveratrol":
                    resveratrolx = graphx
                    resveratroly = graphy
                graphx.clear()
                graphy.clear()
                i += 1
                varname = newvarname
            plt.plot(graphx, graphy, c=numpy.random.rand(3, ), label=varname)
            if varname == "resveratrol":
                resveratrolx = graphx
                resveratroly = graphy
            break
        elif line[0].find("variable: ", 0) >= 0:
            newvarname = line[0][line[0].find("variable: ")+10:]
            # print("variable: " + varname)

with open(output_directory+"analysis"+runnumber+".txt", 'w+') as file:
    file.write(processed_output)
print("Analysis saved to analysis"+runnumber+".txt")

if graphb:
    plt.ylabel("Concentration (uM)")
    plt.xlabel("Time (s)")
    plt.legend()

    if not resveratrolx:
        #plt.show()
        plt.savefig("plot" + runnumber + ".png")
        print("Plot saved to plot"+runnumber+".txt")
    else:
        #plt.show(block=False)
        plt.savefig("intracellular" + runnumber + ".png")
        print("Plot saved to intracellular"+runnumber+".txt")
        plt.figure()
        resveratroly = [(i*0.0006*228.25)/1000 for i in resveratroly]
        plt.plot(resveratrolx, resveratroly, c=numpy.random.rand(3, ), label = "Resveratrol Yield")
        plt.ylabel("Resveratrol Yield (mg)")
        plt.xlabel("Time (s)")
        plt.legend()
        #plt.show()
        plt.savefig("resveratrol" + runnumber + ".png")
        print("Plot saved to resveratrol"+runnumber+".txt")
