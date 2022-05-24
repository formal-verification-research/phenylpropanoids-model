#Molecular weights
enzymeMW = {'E_TAL': 53967, 'E_4CL': 62559, 'E_C3H': 57055, 'E_COMT': 24602, 'E_CCOMT': 30600, 'E_DCS': 42047, 'E_CURS': 43034, 'E_CURS2': 43146, 'E_CURS3': 43099}

#Initial concentrations
initialConc = {'E_TAL': 25, 'E_4CL': 10, 'E_C3H': 50, 'E_COMT': 25, 'E_CCOMT': 25, 'E_DCS': 50, 'E_CURS': 50, 'E_CURS2': 50, 'E_CURS3': 50}
enzymes = ['E_4CL', 'E_C3H', 'E_COMT', 'E_DCS', 'E_CURS3']#, 'E_CURS2', 'E_CURS3']
filename = "simulationResults.txt"

statement = "-const "
for i in range(len(enzymes)):
    enzymeConc = initialConc[enzymes[i]]*1000/enzymeMW[enzymes[i]]
    statement = statement + str(enzymes[i]) + "=" + str(enzymeConc)
    if i < (len(enzymes)-1):
        statement = statement + ","

fullStatement = "prism ../pathway_curcumin.sm ../curcuminRewards.csl " + statement + " -sim -simsamples 100 -const T=0.0:3600:172800 -v -cuddmaxmem 110g -exportresults " + filename
# print(fullStatement)
# -const E_TAL=0.18529842311041933,E_4CL=0.15984910244728975,E_C3H=0.43817369205152923,E_COMT=1.0161775465409317,E_CCOMT=0.8169934640522876,E_DCS=0.5945727400290152,E_CURS=0.5809360040897895
# TAL10_4CL10.txt:csv
