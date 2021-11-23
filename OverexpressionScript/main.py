import itertools
import subprocess
import sys
import os
#itertools.combination(list of enzymes, number of changed enzymes)

enzymes = {'E_TAL':53967, 'E_4CL':62559, 'E_C3H':57055, 'E_COMT':24602, 'E_CCOMT':30600, 'E_DCS':42047, 'E_CURS':43034}
differentConcentration = 10
concentration = 25
comb = 0
combinations_2 = itertools.combinations(enzymes,2)
combinations_3 = itertools.combinations(enzymes,3)

comb2 = []
for item in combinations_2:
    comb2.append(item)

comb3 = []
for item in combinations_3:
    comb3.append(item)

file = open('OverExpression.txt','wb')
file.write("const double T;\n".encode())

#2 enzymes
for enzyme in comb2[comb]:
    constant = 'const double ' + str(enzyme) + ' = ' + str(differentConcentration*1000/enzymes[enzyme]) + ';\n'
    file.write(constant.encode())

#
# #3 enzymes
# for enzyme in comb3[comb]:
#     constant = 'const double ' + str(enzyme) + ' = ' + str(conc*1000/enzymes[enzyme]) + ';\n'
#     file.write(constant.encode())

for enzyme in enzymes:
    if enzyme not in comb2[comb]:
        constant = 'const double ' + str(enzyme) + ' = ' + str(concentration*1000/enzymes[enzyme]) + ';\n'
        file.write(constant.encode())

file.write("\n\n".encode())
rewards = 'R{"p_coumaric_acid_produced"}=? [I=T]\n' \
          'R{"caffeic_acid_produced"}=? [I=T]\n' \
          'R{"ferulic_acid_produced"}=? [I=T]\n' \
          'R{"p_coumaroyl_CoA_produced"}=? [I=T]\n' \
          'R{"caffeoyl_CoA_produced"}=? [I=T]\n' \
          'R{"feruloyl_CoA_produced"}=? [I=T]\n' \
          'R{"feruloylacetyl_CoA_produced"}=? [I=T]\n' \
          'R{"curcumin_produced"}=? [I=T]\n' \
          'R{"curcumin_produced_mass"}=? [I=T]\n'
file.write(rewards.encode())
file.close()

"-param E_TAL=0.18529842311041933:0.18529842311041933"
results = subprocess.run(["prism ../pathway_curcumin.sm ../curcuminRewards.csl -const E_TAL=0.18529842311041933 -sim -simsamples 100 -const T=172800 -v -cuddmaxmem 110g"], shell=True)
#results = subprocess.run(["prism", "../pathway_curcumin.sm", "../curcuminRewards.csl", "-const E_TAL=0.18529842311041933", "-sim", "-simsamples 100", "-const T=172800", "-v", "-cuddmaxmem 110g"])
#print(results)

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
