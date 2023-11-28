from __future__ import division
# from loadExperimentalData import *
# from calculateSimpleResidual import calculatePureResidual
import os,sys,math,matplotlib.pyplot as plt,numpy as npy
from math import *
# from all_p_params import *
from lmfit import minimize, Parameters, report_fit
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
# from findVectors import findVectors
from calculatePureVariables import calculateNewMolecularParameters,calculateCharacteristicParametersGamma,calculateCharacteristicParameters,returnCharacteristicParameters
# from wrapperFunctions import calculatePressure,calculateTemperature,calculateDensity
# from wrapperFlexibilityFunctions import calculateSpecificHeat
from isListOrNpyArray import *
from Parameters_of_Different_Polymers import *
from loadPhysicalConstants import *
from scipy.optimize import bisect,fsolve
from scipy.interpolate import interp1d
from sympy import *
from optimizeResidualFunctions import pureEOSResidual,pureChemicalPotentialResidual
from loadSpecificHeatExperimentalData import *
from sympy import Symbol, nsolve
import sympy
# import mpmath

def density(P,T,M,**kwargs):
	
	for key,value in kwargs.items():
		exec "%s=%s" % (key,value)
	
	# r = (Pstar*M)/(kB*Tstar*Rstar)
	
	phi = bisect(pureEOSResidual,0.000000001,0.9999999999,args=(P,T,M,Pstar,Tstar,Rstar))
	
	R = phi*Rstar
		
	return R

def SimultaneousEquationSolver(Vratio,P_atm,Tg_atm,Rg_atm,deltaCp,M,**kwargs):

	for key,value in kwargs.items():
		exec "%s=%s" % (key,value)
	
	r = (Pstar*M)/(kB*Tstar*Rstar)

	P=P_atm
	T=Tg_atm
	R=Rg_atm

	# Ptilde=P/Pstar
	Rtilde=R/Rstar
	# Ttilde=T/Tstar

	#Simultaneous Equation Solver, Finding g_min by changing 'x':

	x= npy.linspace(0.24,0.65,10)
	epsilon_2_array=npy.zeros(len(x))
	Rratio_array=npy.zeros(len(x))
	# mpmath.mp.dps = 15

	for i in range(0,len(x)):
		
		# Incorrect Equation below:
		# Own_Criteria_1=(Pstar/(Rstar*Tstar))*(-((1-Rtilde)*(ln(1-Rtilde))/Rtilde)-((ln(Rtilde))/r)+((1/Ttilde)*Rratio*(exp(-((Vratio*epsilon_2))/(kB*T)))/(1+Rratio*exp(-((Vratio*epsilon_2))/(kB*T))))+((1/Vratio)*ln(1+Rratio*exp(-(Vratio*epsilon_2)/(kB*T))))-(x[i])-((x[i]/Vratio)*ln(1+Rratio)))
	
		# print 'Program is iterating for the cycle number = ',i+1,' with x= ', x[i]
		Rratio = Symbol('Rratio', real=True, positive=True, negative=False)
		epsilon_2 = Symbol('epsilon_2', real=True, positive=True, negative=False)
		#All correct Equations below:
		Own_Criteria_1=(Pstar/(Rstar*Tstar))*(-((1/Rtilde)*(1-Rtilde)*(ln(1-Rtilde)))-((1/r)*(ln(Rtilde)))+((epsilon_2/(kB*T))*((Rratio*exp(-Vratio*epsilon_2/(kB*T)))/(1+(Rratio*exp(-Vratio*epsilon_2/(kB*T))))))-((1/Vratio)*(ln(1-((Rratio*exp(-Vratio*epsilon_2/(kB*T)))/(1+(Rratio*exp(-Vratio*epsilon_2/(kB*T))))))))-(x[i])-((x[i]/Vratio)*(ln(1+Rratio))))
		Cp_GlassRHS=((Pstar/(Rstar*Tstar))*(Vratio)*((epsilon_2/(kB*T))**2)*((Rratio*exp(-Vratio*epsilon_2/(kB*T)))/(1+(Rratio*exp(-Vratio*epsilon_2/(kB*T)))))*(1-((Rratio*exp(-Vratio*epsilon_2/(kB*T)))/(1+(Rratio*exp(-Vratio*epsilon_2/(kB*T)))))))-deltaCp
		# F=((Rratio*exp(-Vratio*epsilon_2/(kB*T)))/(1+(Rratio*exp(-Vratio*epsilon_2/(kB*T)))))

		answer=nsolve((Own_Criteria_1, Cp_GlassRHS), (Rratio, epsilon_2), (70.1629527934053, 582.5546910106218),verify=True)

		Rratio_array[i]=answer[0]
		epsilon_2_array[i]=answer[1]

		# print Rratio_array[i]
		# print epsilon_2_array[i]

	Rratio=Rratio_array
	epsilon_2=epsilon_2_array

	# print 'Thus, the answers are:'
	Rratio_min=min(Rratio)
	index_min=npy.argmin(Rratio)
	epsilon_2_min=epsilon_2[index_min]
	x_min=x[index_min]
	x_min_upper=x[index_min+1]
	x_min_lower=x[index_min-1]

	# print 'Rratio_min is:',Rratio_min
	# print 'epsilon_2_min is:',epsilon_2_min
	# print 'x_min is:',x_min
	# print 'x_min_upper is:',x_min_upper
	# print 'x_min_lower is:',x_min_lower

	return Rratio_min,epsilon_2_min,x_min,x_min_upper,x_min_lower

def glassTransitionCriteria(T,P,M,x,Rratio,epsilon_2,Vratio,Pstar,Tstar,Rstar):  
	
	r = (Pstar*M)/(kB*Tstar*Rstar)
	
	R=density(P,T,M,Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)

	# Ptilde=P/Pstar
	# Ttilde=T/Tstar
	Rtilde=R/Rstar

	# Tstarstar=Tratio*Tstar
	# epsilon_2=Tstarstar*kB

	# MY Theory:
	# Own_Criteria_1_incorrect=(Pstar/(Rstar*Tstar))*(-((1-Rtilde)*(ln(1-Rtilde))/Rtilde)-((ln(Rtilde))/r)+((1/Ttilde)*Rratio*(exp(-((Vratio*epsilon_2))/(kB*T)))/(1+Rratio*exp(-((Vratio*epsilon_2))/(kB*T))))+((1/Vratio)*ln(1+Rratio*exp(-(Vratio*epsilon_2)/(kB*T))))-(x)-((x/Vratio)*ln(1+Rratio)))
	Own_Criteria_1=(Pstar/(Rstar*Tstar))*(-((1/Rtilde)*(1-Rtilde)*(ln(1-Rtilde)))-((1/r)*(ln(Rtilde)))+((epsilon_2/(kB*T))*((Rratio*exp(-Vratio*epsilon_2/(kB*T)))/(1+(Rratio*exp(-Vratio*epsilon_2/(kB*T))))))-((1/Vratio)*(ln(1-((Rratio*exp(-Vratio*epsilon_2/(kB*T)))/(1+(Rratio*exp(-Vratio*epsilon_2/(kB*T))))))))-(x)-((x/Vratio)*(ln(1+Rratio))))

	res=Own_Criteria_1

	return res

def GlassTemperature(P,**kwargs):
	
	for key,value in kwargs.items():
		exec "%s=%s" % (key,value)
	
	Tg = bisect(glassTransitionCriteria,100,10000,args=(P,M,x,Rratio,epsilon_2,Vratio,Pstar,Tstar,Rstar))
	
	return Tg

def GlassTemperatureResidual(P0,T0,Vratio,M,**kwargs):

	residual = npy.zeros(len(P0))

	for key,value in kwargs.items():
		exec "%s=%s" % (key,value)
	
	print 'Iterating for:'
	print 'Vratio=', Vratio

	Rratio,epsilon_2,x,x_ub,x_lb=SimultaneousEquationSolver(Vratio,P_atm,Tg_atm,Rg_atm,deltaCp,M,Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)
	
	print 'Simultaneous Solution is:'
	print 'Vratio=', Vratio
	print 'Rratio=', Rratio
	print 'epsilon_2=', epsilon_2
	print 'x=',x

	for j in range(0,len(P0)):
		Tg = GlassTemperature(P0[j],Vratio=Vratio,Rratio=Rratio,epsilon_2=epsilon_2,x=x,M=M,Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)
		residual[j] = (T0[j]-Tg)#/T0[j]
	
	return residual

def calculateGlassTemperatureResidual(params,P0,T0):
	
	if 'Pstar' in params and 'Tstar' in params and 'Rstar' in params:
		Pstar = params['Pstar'].value
		Tstar = params['Tstar'].value
		Rstar = params['Rstar'].value
		Vratio = params['Vratio'].value
		M = params['M'].value
		deltaCp = params['deltaCp'].value
		P_atm = params['P_atm'].value
		Tg_atm = params['Tg_atm'].value
		Rg_atm = params['Rg_atm'].value
		kwargs = {'Pstar':Pstar,'Tstar':Tstar,'Rstar':Rstar,'deltaCp':deltaCp,'P_atm':P_atm,'Tg_atm':Tg_atm,'Rg_atm':Rg_atm}
	# elif 'gamma' in params and 'vh' in params and 'epsilon' in params:
	# 	gamma = params['gamma'].value
	# 	vh = params['vh'].value
	# 	epsilon = params['epsilon'].value
	# 	kwargs = {'gamma':gamma,'vh':vh,'epsilon':epsilon}
	# elif 'alpha' in params and 'vh' in params and 'epsilon' in params:
	# 	alpha = params['alpha'].value
	# 	vh = params['vh'].value
	# 	epsilon = params['epsilon'].value
	# 	kwargs = {'alpha':alpha,'vh':vh,'epsilon':epsilon}
	else:
		raise ValueError('In calculatePureResidual: Either molecular (alpha,vh,epsilon) or characteristic (Pstar,Tstar,Rstar) parameters must be used.')
	
	res = GlassTemperatureResidual(P0,T0,Vratio,M,**kwargs)
	
	print '==> Done for values above.'

	return res

Program_Running_For=['PMMA Olabisi 44kilo']

Pick_List_Element = Program_Running_For[0]
Divide_List_Picked_Element = Pick_List_Element.split()

print(Divide_List_Picked_Element)

Polymer_Type=Divide_List_Picked_Element[0]
Reference=Divide_List_Picked_Element[1]
Polymer_Weight=Divide_List_Picked_Element[2]
# class Polymer_Type

kwargs = {'Polymer_Type':Polymer_Type,'Reference':Reference,'Polymer_Weight':Polymer_Weight}

Abelow,Bbelow,Aabove,Babove,A,B,deltaCp,T0_excluding_Tg,M0_excluding_Tg,C0_excluding_Tg,P0_excluding_Tg,I0_excluding_Tg,Tg0_excluding_Tg,T0_above_Tg,M0_above_Tg,C0_above_Tg,P0_above_Tg,I0_above_Tg,Tg0_above_Tg,T0_at_Tg,M0_at_Tg,C0_at_Tg,P0_at_Tg,I0_at_Tg,Tg0_at_Tg,T0_below_Tg,M0_below_Tg,C0_below_Tg,P0_below_Tg,I0_below_Tg,Tg0_below_Tg,T0_complete_Tg,M0_complete_Tg,C0_complete_Tg,P0_complete_Tg,I0_complete_Tg,Tg0_complete_Tg=loadSpecificHeatExperimentalData(**kwargs)
Pstar,Tstar,Rstar,Tg_atm,dTg_dP_atm,Pg_exp,Tg_exp,P_upper,T_upper=Parameters_of_Different_Polymers(**kwargs)

# Rg_exp=npy.zeros(len(Pg_exp))
# for i in range(0,len(Pg_exp)):
# 	Rg_exp[i]=density(Pg_exp[i],Tg_exp[i],M_infinity,Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)
# P = P_atm
# T=Tg_atm
# M=M_infinity

Rg_atm=density(P_atm,Tg_atm,M_infinity,Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)

# R=Rg_atm
# r = (Pstar*M)/(kB*Tstar*Rstar)
# dP_dT_atm=1/dTg_dP_atm
# Ptilde=P/Pstar
# Ttilde=T/Tstar
# Rtilde=R/Rstar
# dPtilde_dT=dP_dT_atm/Pstar
# dPtilde_dTtilde=dP_dT_atm*Tstar/Pstar
##################################################
##################################################

N = len(Pg_exp)
deltaP = max(Pg_exp)-min(Pg_exp)
deltaT = max(Tg_exp)-min(Tg_exp)
print('Performing fit with {} datapoints over a glass transition temperature range of {}-{}K and a pressure range of {}-{}MPa.'.format(N,min(Tg_exp),max(Tg_exp),round(min(Pg_exp),2),max(Pg_exp)))

#Initializing the parameters.
params = Parameters()
#The following code sets up the model's parameters. It includes both fitting parameters and parameters that will remain fixed
#for the fitting. The values given are the inital guesses of fitting parameters and values of fixed parameters.
#				(Name,		Value,		Vary?,	Min,	Max,	Expr)
params.add_many(('Vratio',	27.777578091813684,		True,	0.0,	None,	None),
				('Pstar',	Pstar,		False,	None,	None,	None),
				('Tstar',	Tstar,		False,	None,	None,	None),
				('Rstar',	Rstar,		False,	None,	None,	None),
				('M',		M_infinity,	False,	None,	None,	None),
				('deltaCp',	deltaCp,	False,	None,	None,	None),
				('P_atm',	P_atm,		False,	None,	None,	None),
				('Tg_atm',	Tg_atm,		False,	None,	None,	None),
				('Rg_atm',	Rg_atm,		False,	None,	None,	None))

#Running the Levenberg-Marquart algorithm on the residuals in order to do least squares fitting. This will return the fitted value of the RESIDUALS.
#These need to be added to the experimental datapints to find the fitted pressures.

fit = minimize(calculateGlassTemperatureResidual,params,args=(Pg_exp,Tg_exp))
#Reporting the values of the parameters. NEED TO FIGURE OUT HOW TO PRINT THIS TO FILE.
report_fit(fit.params)

if 'Vratio' in fit.params:
	Vratio = fit.params['Vratio'].value
	# kwargs = {'Pstar':PstarIterated,'Tstar':TstarIterated,'Rstar':RstarIterated}

Rratio,epsilon_2,x,x_ub,x_lb=SimultaneousEquationSolver(Vratio,P_atm,Tg_atm,Rg_atm,deltaCp,M_infinity,Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)

print 'Thus, iterated values are'
print 'Vratio=', Vratio
print 'Rratio=', Rratio
print 'epsilon_2=', epsilon_2
print 'x=',x
print 'x_up_bound=',x_ub
print 'x_lower_bound=',x_lb