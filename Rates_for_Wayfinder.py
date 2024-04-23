E_TAL = 25
Km_TAL = 1492.2
Kcat_TAL = 155

E_4CL = 25
Km_4CL_pca = 26
Kcat_4CL_pca = 88.68
Km_4CL_fa = 27
Kcat_4CL_fa = 126
Km_4CL_ca = 44
Kcat_4CL_ca = 31.4

Km_C3H_pca = 8
Kcat_C3H_pca = 10.2
Km_C3H_pcoa = 8
Kcat_C3H_pcoa = 10.2
Km_COMT_ca = 68.75
Kcat_COMT_ca = 0.092
Km_COMT_ccoa = 83.04
Kcat_COMT_ccoa = 51.22
Km_CURS_fcoa = 18
Kcat_CURS_fcoa = 0.01833
Km_CURS_pcoa = 189
Kcat_CURS_pcoa = 0.01416667

Kcat_DCS_fcoa = 0.02
S50_DCS_fcoa = 46
n_DCS_fcoa = 1.8

STEP = 1

def rate_finder(state, rate_constant, reaction_name) -> float:
  LTyr, PCou, Caf, FerA, FCoa, FDCoa, Curc = state
  if reaction_name == "r1":
    return (((Kcat_TAL*E_TAL*LTyr)/(Km_TAL+LTyr))/STEP)
  elif reaction_name == "r2":
    return 
  else:
    raise Exception(f"Reaction name \"{reaction_name}\" unrecognized")
    
