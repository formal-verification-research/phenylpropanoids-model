import itertools
import subprocess
import sys
import os
#itertools.combination(list of enzymes, number of changed enzymes)

enzymes = {'E_TAL':53967, 'E_4CL':62559, 'E_C3H':57055, 'E_COMT':24602, 'E_CCOMT':30600, 'E_DCS':42047, 'E_CURS':43034}
concentrations = [10,25,50]
combinations_2 = itertools.combinations(enzymes,2)
combinations_3 = itertools.combinations(enzymes,3)

comb2 = []
for item in combinations_2:
    comb2.append(item)

comb3 = []
for item in combinations_3:
    comb3.append(item)

statements = []
files = []

for comb in comb2:
    for i in range(3):
        for j in range(3):
            enzyme1 = concentrations[i]*1000/enzymes[comb[0]]
            enzyme2 = concentrations[j]*1000/enzymes[comb[1]]
            statement = "-const " + str(comb[0]) + "=" + str(enzyme1) + "," + str(comb[1]) + "=" + str(enzyme2) + ","
            filename = str(comb[0].replace('E_','')) + str(concentrations[i]) + "_" + str(comb[1].replace('E_','')) + str(concentrations[j]) + ".txt:csv"
            files.append(filename)
            for enzyme in enzymes:
                if enzyme not in comb:
                    statement += str(enzyme) + "=" + str(25*1000/enzymes[enzyme])
                    if enzyme != "E_CURS":
                        statement += ","
            statements.append(statement)


for comb in comb3:
    for i in range(3):
        for j in range(3):
            for k in range(3):
                enzyme1 = concentrations[i]*1000/enzymes[comb[0]]
                enzyme2 = concentrations[j]*1000/enzymes[comb[1]]
                enzyme3 = concentrations[k]*1000/enzymes[comb[2]]
                statement = "-const " + str(comb[0]) + "=" + str(enzyme1) + "," + str(comb[1]) + "=" + str(enzyme2) + "," + str(comb[2]) + "=" + str(enzyme3) + ","
                filename = str(comb[0].replace('E_','')) + str(concentrations[i]) + "_" + str(comb[1].replace('E_','')) + str(concentrations[j]) + "_" + str(comb[2].replace('E_','')) + str(concentrations[k]) + ".txt:csv"
                files.append(filename)
                for enzyme in enzymes:
                    if enzyme not in comb:
                        statement += str(enzyme) + "=" + str(25*1000/enzymes[enzyme])
                        if enzyme != "E_CURS":
                            statement += ","
                statements.append(statement)

# file=open("Statements.txt", 'wb')
# for i in range(len(statements)):
#     file.write(statements[i].encode())
#     file.write("\n".encode())
#     file.write(files[i].encode())
#     file.write("\n\n".encode())


fullStatement = "prism ../pathway_curcumin.sm ../curcuminRewards.csl " + statements[42] + " -sim -simsamples 100 -const T=0.0:3600:172800 -v -cuddmaxmem 110g -exportresults " + str(files[42])
subprocess.run([fullStatement], shell=True)

'''
for i in range (len(statements)):
    fullStatement = "prism ../pathway_curcumin.sm ../curcuminRewards.csl " + statements[i] + " -sim -simsamples 100 -const T=172800 -v -cuddmaxmem 110g -exportresults " + str(files[i])
    subprocess.run([fullStatement], shell=True)
'''

#subprocess.run(["prism ../pathway_curcumin.sm ../curcuminMassReward.csl -const E_TAL=0.18529842311041933 -sim -simsamples 100 -const T=172800 -v -cuddmaxmem 110g -exportresults results.txt:csv"], shell=True)


# for i in combinations_2:
#     file.write(('const double ' + combinations_3[i][0] + ';').encode())

'''
const double E_TAL = (gen_E/MW_TAL)*1000;
const double
'''

# Create and pass in a properties file
# The error PRISM is giving is "Error: Empty property"
# https://www.prismmodelchecker.org/manual/PropertySpecification/PropertiesFiles

'''
https://www.digitalocean.com/community/tutorials/how-to-use-subprocess-to-run-external-programs-in-python-3
 result = subprocess.run([sys.executable, "-c", "print('ocean')"])
 sys.executable = program to be run
 -c is a python command line option that allows you to pass a string
  with an entire python program to execute. In this case, we pass a program
  that prints the string ocean
 [sys.executable, "-c", "print('ocean')"] translates roughly to:
    /usr/local/bin/python -c "print('ocean')"
 
 
 result = subprocess.run([sys.executable, "-c", "print('ocean')"], 
    capture_output=True, text=True)
 print("stdout:", result.stdout)
 print("stderr:", result.stderr)
 
 Output
 stdout: ocean
 stderr: 
 

 result = subprocess.run([sys.executable, "-c", "import sys; print(sys.stdin.read())"],
        input=b"underwater")
        
 Output
 underwater
'''
#
# result = subprocess.run([sys.executable, "-c", "print('ocean')"], capture_output=True, text=True)
# print("stdout:", result.stdout)
# print("stderr:", result.stderr)
