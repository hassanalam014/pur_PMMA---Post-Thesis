import os,sys,math,numpy as npy
from loadSolubilityExperimentalData import *
from loadSwellingExperimentalData import *
from lmfit import minimize, Parameters, report_fit
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
# from calculateSimpleResidual import calculatePureResidual
from calculateBinaryResidual import calculateBinaryResidualCHV

Ppstar=316.2
Tpstar=662.8
Rpstar=0.8685
Mp=9E9
Psstar=419.9
Tsstar=341.8
Rsstar=1.397
Ms=9E9
fs=0.0		#Hassan: For simultaneous fit of solubility and swelling experimental data, fs will be the weight of swelling residual as compare to solubility residual. 

N = len(P0)
deltaP = max(P0)-min(P0)
deltaT = max(T0)-min(T0)
print('Performing fit with {} datapoints over a temperature range of {}-{}K and a pressure range of {}-{}MPa.'.format(N,min(T0),max(T0),round(min(P0),2),max(P0)))

#Initializing the parameters.
params = Parameters()
#The following code sets up the model's parameters. It includes both fitting parameters and parameters that will remain fixed
#for the fitting. The values given are the inital guesses of fitting parameters and values of fixed parameters.
#				(Name,		Value,		Vary?,	Min,	Max,	Expr)
params.add_many(('zeta',	1.110,		True,	0,		None,	None),
				('delta',	0.75,		True,	0,		None,	None),
				('Ppstar',	Ppstar,		False,	0,		None,	None),
				('Tpstar',	Tpstar,		False,	0,		None,	None),
				('Rpstar',	Rpstar,		False,	0,		None,	None),
				('Mp',			Mp,		False,	0,		None,	None),
				('Psstar',	Psstar,		False,	0,		None,	None),
				('Tsstar',	Tsstar,		False,	0,		None,	None),
				('Rsstar',	Rsstar,		False,	0,		None,	None),
				('Ms',			Ms,		False,	0,		None,	None),
				('fs',			fs,		False,	0.0,	1.0,	None),
				('Pc0',		0.0,		False,	0,		None,	None),
				('Tc0',		0.0,		False,	0,		None,	None),
				('Rc0',		0.0,		False,	0,		None,	None))

#Running the Levenberg-Marquart algorithm on the residuals in order to do least squares fitting. This will return the fitted value of the RESIDUALS.
#These need to be added to the experimental datapints to find the fitted pressures.

volume_correction='disparate'
fit_type='X'

fit = minimize(calculateBinaryResidualCHV,params,args=(P0_X,T0_X,X0_X,P0_S,T0_S,S0_S,fit_type,volume_correction))
#Reporting the values of the parameters. NEED TO FIGURE OUT HOW TO PRINT THIS TO FILE.
report_fit(fit.params)

if 'Ppstar' in fit.params and 'Tpstar' in fit.params and 'Rpstar' in fit.params:
	zetaIterated = fit.params['zeta'].value
	deltaIterated = fit.params['delta'].value
	kwargs = {'zeta':zetaIterated,'delta':deltaIterated}
#print(zetaIterated,deltaIterated)
