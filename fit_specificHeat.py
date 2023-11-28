from __future__ import division
import os,sys,math,matplotlib.pyplot as plt,numpy as npy
from loadSpecificHeatExperimentalData import *
from loadExperimentalData import Pc0,Tc0,Rc0
from calculatePureVariables import density
from lmfit import minimize, Parameters, report_fit
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from calculateSimpleFlexibilityResidual import calculatePureSpecificHeatResidual#,calculatePureSpecificHeatResidual2
from calculatePureVariables import calculateNewMolecularParameters,calculateCharacteristicParametersGamma,calculateCharacteristicParameters,returnCharacteristicParameters
from wrapperFunctions import calculatePressure,calculateTemperature,calculateDensity
from isListOrNpyArray import *
from loadPhysicalConstants import *
from scipy.optimize import bisect,fsolve
from scipy.interpolate import interp1d
from sympy import *
from optimizeResidualFunctions import pureEOSResidual,pureChemicalPotentialResidual
from Parameters_of_Different_Polymers import *


# Pstar = 421.762455
# Tstar = 687.788143
# Rstar = 1.11768655

Polymer_Type='PVAc'
Reference='Roland'
Polymer_Weight='189kilo'
kwargs = {'Polymer_Type':Polymer_Type,'Reference':Reference,'Polymer_Weight':Polymer_Weight}

Pstar,Tstar,Rstar,Tg_atm,dTg_dP_atm,Pg_exp,Tg_exp,P_upper,T_upper=Parameters_of_Different_Polymers(**kwargs)
Abelow,Bbelow,Aabove,Babove,A,B,deltaCp,T0_excluding_Tg,M0_excluding_Tg,C0_excluding_Tg,P0_excluding_Tg,I0_excluding_Tg,Tg0_excluding_Tg,T0_above_Tg,M0_above_Tg,C0_above_Tg,P0_above_Tg,I0_above_Tg,Tg0_above_Tg,T0_at_Tg,M0_at_Tg,C0_at_Tg,P0_at_Tg,I0_at_Tg,Tg0_at_Tg,T0_below_Tg,M0_below_Tg,C0_below_Tg,P0_below_Tg,I0_below_Tg,Tg0_below_Tg,T0_complete_Tg,M0_complete_Tg,C0_complete_Tg,P0_complete_Tg,I0_complete_Tg,Tg0_complete_Tg=loadSpecificHeatExperimentalData(**kwargs)


# N = len(P0)
# deltaP = max(P0)-min(P0)
# deltaT = max(T0)-min(T0)
# print('Performing fit with {} datapoints over a temperature range of {}-{}K and a pressure range of {}-{}MPa.'.format(N,min(T0),max(T0),round(min(P0),2),max(P0)))

R0=npy.zeros(len(C0_complete_Tg))
for j in range(0,len(C0_complete_Tg)):
	R0[j]=density(P0_complete_Tg[j],T0_complete_Tg[j],M0_complete_Tg[j],Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)

R0_below_Tg=npy.zeros(len(T0_below_Tg))
for j in range(0,len(T0_below_Tg)):
	R0_below_Tg[j]=density(P0_below_Tg[j],T0_below_Tg[j],M0_below_Tg[j],Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)

R0_at_Tg=npy.zeros(len(T0_at_Tg))
for j in range(0,len(T0_at_Tg)):
	R0_at_Tg[j]=density(P0_at_Tg[j],T0_at_Tg[j],M0_at_Tg[j],Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)

R0_above_Tg=npy.zeros(len(T0_above_Tg))
for j in range(0,len(T0_above_Tg)):
	R0_above_Tg[j]=density(P0_above_Tg[j],T0_above_Tg[j],M0_above_Tg[j],Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)

R0_excluding_Tg=npy.zeros(len(T0_excluding_Tg))
for j in range(0,len(T0_excluding_Tg)):
	R0_excluding_Tg[j]=density(P0_excluding_Tg[j],T0_excluding_Tg[j],M0_excluding_Tg[j],Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)

PE = 1.5
TE = 15.0
print T0_below_Tg
print 'First Fitting Base Curve'

#Fitting Data to the base curve below glass transition:
params_below_Tg = Parameters()
#The following code sets up the model's parameters. It includes both fitting parameters and parameters that will remain fixed
#for the fitting. The values given are the inital guesses of fitting parameters and values of fixed parameters.
#						(Name,			Value,		        Vary?,	Min,	Max,	Expr)
params_below_Tg.add_many(('A',			0.03,			    True,	0,		None,	None),
				(		'B',			0.003392431,		True,	0,		None,	None),
				(		'Pstar',		Pstar,				False,	0,		None,	None),
				(		'Tstar',		Tstar,				False,	0,		None,	None),
				(		'Rstar',		Rstar,				False,	0,		None,	None),
				(		'Pc0',			Pc0,		        False,	0,		None,	None),
				(		'Tc0',			Tc0,		        False,	0,		None,	None),
				(		'Rc0',			Rc0,		        False,	0,		None,	None))

#Running the Levenberg-Marquart algorithm on the residuals in order to do least squares fitting. This will return the fitted value of the RESIDUALS.
#These need to be added to the experimental datapints to find the fitted specific heat.
fit = minimize(calculatePureSpecificHeatResidual,params_below_Tg,args=(C0_below_Tg,P0_below_Tg,T0_below_Tg,R0_below_Tg,M0_below_Tg,I0_below_Tg,PE,TE,'C_below_Tg'))

#Reporting the values of the parameters. NEED TO FIGURE OUT HOW TO PRINT THIS TO FILE.
report_fit(fit.params)

if 'A' in fit.params and 'B' in fit.params:
	AIterated = fit.params['A'].value
	BIterated = fit.params['B'].value
	#kwargs = {'A':AIterated,'B':BIterated}

print 'Now, Fitting Glass Transition'

#Fitting Data to the base curve at glass transition:
params_at_Tg = Parameters()
#The following code sets up the model's parameters. It includes both fitting parameters and parameters that will remain fixed
#for the fitting. The values given are the inital guesses of fitting parameters and values of fixed parameters.
#						(Name,			Value,		        Vary?,	Min,				Max,	Expr)
params_at_Tg.add_many(('A',				AIterated,		    False,	0,					None,	None),
				(		'B',			BIterated,			False,	0,					None,	None),
				(		'Pstarstar',	0.00249935,			True,	0,					None,	None),
				(		'Tstarstar',	11.9757060,			True,	0,					None,	None),
				(		'Rstarstar',	1.1013e+40,		  	True,	1.1*(10**40),		None,	None),
				(		'Pstar',		Pstar,		False,	0,					None,	None),
				(		'Tstar',		Tstar,		False,	0,					None,	None),
				(		'Rstar',		Rstar,		False,	0,					None,	None),
				(		'Pc0',			Pc0,		        False,	0,					None,	None),
				(		'Tc0',			Tc0,		        False,	0,					None,	None),
				(		'Rc0',			Rc0,		        False,	0,					None,	None))

#Running the Levenberg-Marquart algorithm on the residuals in order to do least squares fitting. This will return the fitted value of the RESIDUALS.
#These need to be added to the experimental datapints to find the fitted specific heat.
fit = minimize(calculatePureSpecificHeatResidual,params_at_Tg,args=(C0_at_Tg,P0_at_Tg,T0_at_Tg,R0_at_Tg,M0_at_Tg,I0_at_Tg,PE,TE,'C_at_Tg'))

#Reporting the values of the parameters. NEED TO FIGURE OUT HOW TO PRINT THIS TO FILE.
report_fit(fit.params)

if 'Pstarstar' in fit.params and 'Tstarstar' in fit.params and 'Rstarstar' in fit.params:
	Pstarstar = fit.params['Pstarstar'].value
	Tstarstar = fit.params['Tstarstar'].value
	Rstarstar = fit.params['Rstarstar'].value
	#kwargs = {'Pstarstar':Pstarstar,'Tstarstar':Tstarstar,'Rstarstar':Rstarstar,'A':AIterated,'B':BIterated}




'''
#Initializing the parameters to find Pstarstar, Tstarstar and Rstarstar.
params = Parameters()
#The following code sets up the model's parameters. It includes both fitting parameters and parameters that will remain fixed
#for the fitting. The values given are the inital guesses of fitting parameters and values of fixed parameters.
#				(Name,			Value,		        Vary?,	Min,	Max,	Expr)
params.add_many(('A',			0.0,			    False,	0,		None,	None),
				('B',			0.00386580,			False,	0.001,		None,	None),
				('Pstarstar',	5.1759e-04,			False,	0,		None,	None),
				('Tstarstar',	6.51797774,			False,	0,		None,	None),
				('Rstarstar',	2.5016e+59,		  	True,	1.1*(10**40),		None,	None),
				('Pstar',		Pstar,		False,	0,		None,	None),
				('Tstar',		Tstar,		False,	0,		None,	None),
				('Rstar',		Rstar,		False,	0,		None,	None),
				('Pc0',			Pc0,		        False,	0,		None,	None),
				('Tc0',			Tc0,		        False,	0,		None,	None),
				('Rc0',			Rc0,		        False,	0,		None,	None))

#Running the Levenberg-Marquart algorithm on the residuals in order to do least squares fitting. This will return the fitted value of the RESIDUALS.
#These need to be added to the experimental datapints to find the fitted specific heat.
fit = minimize(calculatePureSpecificHeatResidual,params,args=(C0,P0,T0,R0,M0,I0,PE,TE,'C'))

#Reporting the values of the parameters. NEED TO FIGURE OUT HOW TO PRINT THIS TO FILE.
report_fit(fit.params)

if 'Pstarstar' in fit.params and 'Tstarstar' in fit.params and 'Rstarstar' in fit.params and 'A' in fit.params and 'B' in fit.params:
	AIterated = fit.params['A'].value
	BIterated = fit.params['B'].value
	Pstarstar = fit.params['Pstarstar'].value
	Tstarstar = fit.params['Tstarstar'].value
	Rstarstar = fit.params['Rstarstar'].value
	kwargs = {'Pstarstar':Pstarstar,'Tstarstar':Tstarstar,'Rstarstar':Rstarstar,'A':AIterated,'B':BIterated}
#print(Pstarstar,Tstarstar,Rstarstar,AIterated,BIterated)
'''