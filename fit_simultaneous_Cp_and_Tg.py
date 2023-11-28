from __future__ import division
import os,sys,math,matplotlib.pyplot as plt,numpy as npy
from loadSpecificHeatExperimentalData import *
from loadExperimentalData import Pc0,Tc0,Rc0
# from calculatePureVariables import density
from lmfit import minimize, Parameters, report_fit
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
# from calculateSimpleFlexibilityResidual import calculatePureSpecificHeatResidual,calculatePureSpecificHeatResidual2
# from calculatePureVariables import calculateNewMolecularParameters,calculateCharacteristicParametersGamma,calculateCharacteristicParameters,returnCharacteristicParameters
# from wrapperFunctions import calculatePressure,calculateTemperature,calculateDensity
# from isListOrNpyArray import *
from loadPhysicalConstants import *
from scipy.optimize import bisect,fsolve
from scipy.interpolate import interp1d
from sympy import *
from optimizeResidualFunctions import pureEOSResidual,pureChemicalPotentialResidual
from Parameters_of_Different_Polymers import *

def density(P,T,M,**kwargs):
	
	for key,value in kwargs.items():
		exec "%s=%s" % (key,value)
	
	r = (Pstar*M)/(kB*Tstar*Rstar)
	
	phi = bisect(pureEOSResidual,0.000000001,0.9999999999,args=(P,T,M,Pstar,Tstar,Rstar))
	
	R = phi*Rstar
		
	return R

def glassTransitionCriteria(T,P,M,x,Rratio,Tratio,Vratio,Pstar,Tstar,Rstar):  
	
	r = (Pstar*M)/(kB*Tstar*Rstar)
	
	R=density(P,T,M,Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)

	Ptilde=P/Pstar
	Ttilde=T/Tstar
	Rtilde=R/Rstar

	Pratio=Tratio/Vratio

	Tstarstar=Tratio*Tstar
	Pstarstar=Pratio*Pstar
	Rstarstar=Rratio*Rstar

	# MY Theory:
	Own_Criteria_1=(Pstar/(Rstar*Tstar))*(-((1-Rtilde)*(ln(1-Rtilde))/Rtilde)-((ln(Rtilde))/r)+((1/Ttilde)*Rratio*(exp(-((Tratio)**2)/(Pratio*Ttilde)))/(1+Rratio*exp(-((Tratio)**2)/(Pratio*Ttilde))))+((Pratio/Tratio)*ln(1+Rratio*exp(-(Tratio**2)/(Pratio*Ttilde))))-(x)-((((x)*Pratio)/Tratio)*ln(1+Rratio)))

	res=Own_Criteria_1

	return res

def glassTemp(Pg,**kwargs):
	
	for key,value in kwargs.items():
		exec "%s=%s" % (key,value)
	
	Tstarstar=epsilon_2/kB
	Tratio=Tstarstar/Tstar
	
	Tg = bisect(glassTransitionCriteria,100,10000,args=(Pg,Mg,x,Rratio,Tratio,Vratio,Pstar,Tstar,Rstar))
	
	return Tg

def specificHeat(P,T,R,M,fit_type,**kwargs):    
	
	for key,value in kwargs.items():
		exec "%s=%s" % (key,value)

	r = (Pstar*M)/(kB*Tstar*Rstar)

	Ptilde=P/Pstar
	Ttilde=T/Tstar
	Rtilde=R/Rstar
	
	if 'Fit_above_Tg' in fit_type:
		
		Tstarstar=epsilon_2/kB
		Tratio=Tstarstar/Tstar

		Pratio=Tratio/Vratio

		Tstarstar=Tratio*Tstar
		Pstarstar=Pratio*Pstar
		Rstarstar=Rratio*Rstar
		
		C1=(Pstar/(Rstar*Tstar))*((((1+(Ptilde/(Rtilde**2)))**2)/(((Ttilde/Rtilde)*(((Ttilde/Rtilde)*((Rtilde/(1-Rtilde))+(1/r)))-2)))))
		C2=(Pstar/(Rstar*Tstar))*((((((Tratio**3)*Rratio/Pratio)/(Ttilde**2))*(exp(-(((Tratio**2)/Pratio)/Ttilde))))/((1+(Rratio*(exp(-(((Tratio**2)/Pratio)/Ttilde)))))**2)))
		C3=A+B*T
		C=C1+C2+C3
		# print epsilon_2
		# print Rratio

	if 'Fit_below_Tg' in fit_type:
		C1=(Pstar/(Rstar*Tstar))*((((1+(Ptilde/(Rtilde**2)))**2)/(((Ttilde/Rtilde)*(((Ttilde/Rtilde)*((Rtilde/(1-Rtilde))+(1/r)))-2)))))
		C3=A+B*T
		C=C1+C3
		print A
		print B

	return	C

def ResidualArray(params,Pg,Tg,C,P,T,R,M,I,fit_type):
	
	Pstar = params['Pstar'].value
	Tstar = params['Tstar'].value
	Rstar = params['Rstar'].value
	epsilon_2 = params['epsilon_2'].value
	Rratio = params['Rratio'].value
	Vratio = params['Vratio'].value
	A = params['A'].value
	B = params['B'].value
	Tg_atm = params['Tg_atm'].value
	dP_dT_atm = params['dP_dT_atm'].value
	Mg = params['Mg'].value
	x = params['x'].value

	# Tstarstar=epsilon_2/kB
	# Tratio=Tstarstar/Tstar

	residual_C=npy.zeros(len(C))
	residual_Tg=npy.zeros(len(Pg))

	if 'Fit_below_Tg' in fit_type:
		kwargs = {'Pstar':Pstar,'Tstar':Tstar,'Rstar':Rstar,'Mg':Mg,'epsilon_2':epsilon_2,'Rratio':Rratio,'Vratio':Vratio,'A':A,'B':B,'x':x,'Tg_atm':Tg_atm,'dP_dT_atm':dP_dT_atm}
	
		for j in range(0,len(C)):
			C_calculated = specificHeat(P[j],T[j],R[j],M[j],fit_type,**kwargs)
			residual_C[j] = (C[j]-C_calculated)

		residual=residual_C

		print 'A =', A
		print 'B =', B

	if 'Fit_above_Tg' in fit_type:
		kwargs = {'Pstar':Pstar,'Tstar':Tstar,'Rstar':Rstar,'Mg':Mg,'epsilon_2':epsilon_2,'Rratio':Rratio,'Vratio':Vratio,'A':A,'B':B,'x':x,'Tg_atm':Tg_atm,'dP_dT_atm':dP_dT_atm}

		for j in range(0,len(C)):
			C_calculated = specificHeat(P[j],T[j],R[j],M[j],fit_type,**kwargs)
			residual_C[j] = (((C[j]-C_calculated)/C[j])/len(C))		#To make error independent of number of data points and unit.

		for j in range(0,len(Pg)):
			Tg_calculated = glassTemp(Pg[j],**kwargs)
			residual_Tg[j] = (((Tg[j]-Tg_calculated)/Tg[j])/len(Pg))	#To make error independent of number of data points and unit.
	
		residual = npy.concatenate((residual_C, residual_Tg),axis=0)

		print 'epsilon_2	=', epsilon_2
		print 'Rratio	=', Rratio
		print 'x	=', x

	return residual

dP_dT_atm=1/dTg_dP_atm

##########################################################################################################

##########################################################################################################

R0_complete_Tg=npy.zeros(len(C0_complete_Tg))
for j in range(0,len(C0_complete_Tg)):
	R0_complete_Tg[j]=density(P0_complete_Tg[j],T0_complete_Tg[j],M0_complete_Tg[j],Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)

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

#################################################################
'''
#################################################################

print T0_below_Tg
print 'First Fitting Base Curve'

#Fitting Data to the base curve below glass transition:
params_below_Tg = Parameters()
#The following code sets up the model's parameters. It includes both fitting parameters and parameters that will remain fixed
#for the fitting. The values given are the inital guesses of fitting parameters and values of fixed parameters.
#						(Name,			Value,		        Vary?,	Min,	Max,	Expr)
params_below_Tg.add_many(('A',			0.1,			    True,	0.0,	None,	None),
				(		'B',			0.00258531,			True,	0,		None,	None),
				(		'Vratio',		1.0,				False,	0,		None,	None),
				(		'epsilon_2',	7000.0,				False,	0,		None,	None),
				(		'Rratio',		3.0,				False,	0,		None,	None),
				(		'Pstar',		Pstar,				False,	0,		None,	None),
				(		'Tstar',		Tstar,				False,	0,		None,	None),
				(		'Rstar',		Rstar,				False,	0,		None,	None),
				(		'x',			0.33,				False,	0.0,	1.0,	None),
				(		'Mg',			9E9,				False,	0.0,	None,	None),
				(		'Tg_atm',		Tg_atm,		        False,	0,		None,	None),
				(		'dP_dT_atm',	dP_dT_atm,	        False,	0,		None,	None))

#Running the Levenberg-Marquart algorithm on the residuals in order to do least squares fitting. This will return the fitted value of the RESIDUALS.
#These need to be added to the experimental datapints to find the fitted specific heat.
fit = minimize(ResidualArray,params_below_Tg,args=(Pg_exp,Tg_exp,C0_below_Tg,P0_below_Tg,T0_below_Tg,R0_below_Tg,M0_below_Tg,I0_below_Tg,'Fit_below_Tg'))

#Reporting the values of the parameters. NEED TO FIGURE OUT HOW TO PRINT THIS TO FILE.
report_fit(fit.params)

if 'A' in fit.params and 'B' in fit.params:
	A = fit.params['A'].value
	B = fit.params['B'].value
	#kwargs = {'A':A,'B':B}

######################################################################
'''
######################################################################

A=2.6799e-09#3.6870e-11		#PMMA 140kilo=3.6870e-11				#PS=3.6870e-11
B=0.00287418#0.00551656		#PMMA 140kilo=0.00390689				#PS=0.00372975

######################################################################

######################################################################

x= npy.linspace(0.20,0.50,5)
epsilon_2=npy.zeros(len(x))
Rratio=npy.zeros(len(x))

for i in range(0,len(x)):
	
	print 'Now, Simultaneous Fit Cp_above_Tg and Tg(P)'
	print 'Program is iterating for the cycle number = ',i+1,' with x= ', x[i]

	#Fitting above to the base curve above glass transition:
	params_above_Tg = Parameters()
	#The following code sets up the model's parameters. It includes both fitting parameters and parameters thabove will remain fixed
	#for the fitting. The values given are the inital guesses of fitting parameters and values of fixed parameters.
	#						(Name,			Value,		        Vary?,	Min,	Max,		Expr)
	params_above_Tg.add_many(('A',			A,				    False,	0,		None,		None),
					(		'B',			B,					False,	0,		None,		None),
					(		'Vratio',		1.0,				False,	0,		None,		None),
					(		'epsilon_2',	6251.31324,			True,	0,		10000.00,	None),
					(		'Rratio',		1.20630412,			True,	0,		None,		None),
					(		'Pstar',		Pstar,				False,	0,		None,		None),
					(		'Tstar',		Tstar,				False,	0,		None,		None),
					(		'Rstar',		Rstar,				False,	0,		None,		None),
					(		'Mg',			9E9,				False,	0.0,	None,		None),
					(		'x',			x[i],				False,	0.0,	1.0,		None),
					(		'Tg_atm',		Tg_atm,		        False,	0,		None,		None),
					(		'dP_dT_atm',	dP_dT_atm,	        False,	0,		None,		None))

	#Running the Levenberg-Marquart algorithm on the residuals in order to do least squares fitting. This will return the fitted value of the RESIDUALS.
	#These need to be added to the experimental daboveapints to find the fitted specific heabove.
	fit = minimize(ResidualArray,params_above_Tg,args=(Pg_exp,Tg_exp,C0_above_Tg,P0_above_Tg,T0_above_Tg,R0_above_Tg,M0_above_Tg,I0_above_Tg,'Fit_above_Tg'))

	#Reporting the values of the parameters. NEED TO FIGURE OUT HOW TO PRINT THIS TO FILE.
	report_fit(fit.params)

	if 'epsilon_2' in fit.params and 'Rratio' in fit.params:
		epsilon_2[i] = fit.params['epsilon_2'].value
		Rratio[i] = fit.params['Rratio'].value
		x[i] = fit.params['x'].value
		#kwargs = {'A':A,'B':B}

Rratio_min=min(Rratio)
index_min=npy.argmin(Rratio)
epsilon_2_min=epsilon_2[index_min]
x_min=x[index_min]

print Rratio_min
print epsilon_2_min
print x_min

print Rratio
print epsilon_2
print x

#######################################################################################################

#######################################################################################################
