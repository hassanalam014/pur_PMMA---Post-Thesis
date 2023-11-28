import os,sys,math,numpy as npy
from loadExperimentalData import *
from lmfit import minimize, Parameters, report_fit
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from calculateSimpleResidual import calculatePureResidual

N = len(P0)
deltaP = max(P0)-min(P0)
deltaT = max(T0)-min(T0)
print('Performing fit with {} datapoints over a temperature range of {}-{}K and a pressure range of {}-{}MPa.'.format(N,min(T0),max(T0),round(min(P0),2),max(P0)))

PE = 1.5
TE = 15.0

#Initializing the parameters.
params = Parameters()
#The following code sets up the model's parameters. It includes both fitting parameters and parameters that will remain fixed
#for the fitting. The values given are the inital guesses of fitting parameters and values of fixed parameters.
#				(Name,		Value,		Vary?,	Min,	Max,	Expr)
params.add_many(('Pstar',	60,		True,	0,		None,	None),
				('Tstar',	50,		True,	0,		None,	None),
				('Rstar',	2,		True,	max(R0),		None,	None),
				('Pc0',		Pc0,		False,	0,		None,	None),
				('Tc0',		Tc0,		False,	0,		None,	None),
				('Rc0',		Rc0,		False,	0,		None,	None))

#Running the Levenberg-Marquart algorithm on the residuals in order to do least squares fitting. This will return the fitted value of the RESIDUALS.
#These need to be added to the experimental datapints to find the fitted pressures.

fit = minimize(calculatePureResidual,params,args=(P0,T0,R0,M0,I0,PE,TE,'P'))
#Reporting the values of the parameters. NEED TO FIGURE OUT HOW TO PRINT THIS TO FILE.
report_fit(fit.params)

if 'Pstar' in fit.params and 'Tstar' in fit.params and 'Rstar' in fit.params:
	PstarIterated = fit.params['Pstar'].value
	TstarIterated = fit.params['Tstar'].value
	RstarIterated = fit.params['Rstar'].value
	kwargs = {'Pstar':PstarIterated,'Tstar':TstarIterated,'Rstar':RstarIterated}
#print(PstarIterated,TstarIterated,RstarIterated)
