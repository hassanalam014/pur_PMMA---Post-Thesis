# Author: Hassan Alam
# Date: 2019
#
# Description: The purpose of this file is to ..............
#
from __future__ import division
import os,sys,math,matplotlib.pyplot as plt,numpy as npy
from math import *
#from matplotlib.ticker import AutoMinorLocator
# from all_p_params import *
# from loadSpecificHeatExperimentalData import *
from lmfit import minimize, Parameters, report_fit
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from findVectors import findVectors
from calculatePureVariables import calculateNewMolecularParameters,calculateCharacteristicParametersGamma,calculateCharacteristicParameters,returnCharacteristicParameters
from wrapperFunctions import calculatePressure,calculateTemperature,calculateDensity
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
import mpmath

def density(P,T,M,**kwargs):
	
	for key,value in kwargs.items():
		exec "%s=%s" % (key,value)
	
	r = (Pstar*M)/(kB*Tstar*Rstar)
	
	phi = bisect(pureEOSResidual,0.000000001,0.9999999999,args=(P,T,M,Pstar,Tstar,Rstar))
	
	R = phi*Rstar
		
	return R

### Programs My Theory as well as Condo Theory

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
	# S=(Pstar/(Rstar*Tstar))*(-((1-Rtilde)*(ln(1-Rtilde))/Rtilde)-((ln(Rtilde))/r)+((1/Ttilde)*Rratio*(exp(-((Tratio)**2)/(Pratio*Ttilde)))/(1+Rratio*exp(-((Tratio)**2)/(Pratio*Ttilde))))+((Pratio/Tratio)*ln(1+Rratio*exp(-(Tratio**2)/(Pratio*Ttilde)))))
	# dS_dT_p=(Pstar/(Rstar*Tstar))*((1/T)*((((1+(Ptilde/((Rtilde)**2)))**2)/((Ttilde/(Rtilde))*(((Ttilde/Rtilde)*((Rtilde/(1-Rtilde))+(1/r)))-2)))+((Pratio/Tratio)*(((Tratio*Tstarstar)/(Pratio*T))**2)*((Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T)))/((1+(Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T))))**2)))))
	# dS_dT_v=(Pstar/(Rstar*Tstar))*((1/T)*(((Pratio/Tratio)*(((Tratio*Tstarstar)/(Pratio*T))**2)*((Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T)))/((1+(Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T))))**2)))))
	# dCp_dT_p=(Pstar/(Rstar*Tstar*(T)))*(((((Tratio*Tstarstar)/(Pratio*T))**2)*((Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T)))/(1+Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T))))*(1-((Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T)))/(1+Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T)))))*((((Tratio*Tstarstar)/(Pratio*T))*(1-(2*((Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T)))/(1+Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T)))))))-2))+((Tratio/(Pratio*Ttilde))*((T*((1/T)*((1+(Ptilde/(Rtilde**2)))/(((Ttilde/Rtilde)*((Rtilde/(1-Rtilde))+(1/r)))-2))))**2)*Rtilde*((3*(1+(Ptilde/(Rtilde**2))))-(2*(Ttilde/Rtilde)*((Rtilde/(1-Rtilde))+(1/r)))+((Ttilde*T*((1/T)*((1+(Ptilde/(Rtilde**2)))/(((Ttilde/Rtilde)*((Rtilde/(1-Rtilde))+(1/r)))-2)))/Rtilde)*(((Rtilde/(1-Rtilde))**2)-(1/r)))-2)))
	# d2S_dT2_p=(Pstar/(Rstar*Tstar*(T**2)))*(((((Tratio*Tstarstar)/(Pratio*T))**2)*((Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T)))/(1+Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T))))*(1-((Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T)))/(1+Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T)))))*((((Tratio*Tstarstar)/(Pratio*T))*(1-(2*((Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T)))/(1+Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T)))))))-3))+((Tratio/(Pratio*Ttilde))*((T*((1/T)*((1+(Ptilde/(Rtilde**2)))/(((Ttilde/Rtilde)*((Rtilde/(1-Rtilde))+(1/r)))-2))))**2)*Rtilde*((3*(1+(Ptilde/(Rtilde**2))))-(3*(Ttilde/Rtilde)*((Rtilde/(1-Rtilde))+(1/r)))+((Ttilde*T*((1/T)*((1+(Ptilde/(Rtilde**2)))/(((Ttilde/Rtilde)*((Rtilde/(1-Rtilde))+(1/r)))-2)))/Rtilde)*(((Rtilde/(1-Rtilde))**2)-(1/r)))	)))
	# d2S_dT2_p_1st_Term_Only=(Pstar/(Rstar*Tstar*(T**2)))*(((((Tratio*Tstarstar)/(Pratio*T))**2)*((Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T)))/(1+Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T))))*(1-((Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T)))/(1+Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T)))))*((((Tratio*Tstarstar)/(Pratio*T))*(1-(2*((Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T)))/(1+Rratio*exp(-(Tratio*Tstarstar)/(Pratio*T)))))))-3)))
	# d2S_dT2_p_2nd_Term_Only=(Pstar/(Rstar*Tstar*(T**2)))*((Tratio/(Pratio*Ttilde))*((T*((1/T)*((1+(Ptilde/(Rtilde**2)))/(((Ttilde/Rtilde)*((Rtilde/(1-Rtilde))+(1/r)))-2))))**2)*Rtilde*((3*(1+(Ptilde/(Rtilde**2))))-(3*(Ttilde/Rtilde)*((Rtilde/(1-Rtilde))+(1/r)))+((Ttilde*T*((1/T)*((1+(Ptilde/(Rtilde**2)))/(((Ttilde/Rtilde)*((Rtilde/(1-Rtilde))+(1/r)))-2)))/Rtilde)*(((Rtilde/(1-Rtilde))**2)-(1/r)))	))

	# Own_Criteria_2_old=(Pstar/(Rstar*Tstar))*(-((1-Rtilde)*(ln(1-Rtilde))/Rtilde)-((ln(Rtilde))/r)-(x)*(((1/Ttilde)*Rratio*(exp(-((Tratio)**2)/(Pratio*Ttilde)))/(1+Rratio*exp(-((Tratio)**2)/(Pratio*Ttilde))))+((Pratio/Tratio)*ln(1+Rratio*exp(-(Tratio**2)/(Pratio*Ttilde))))))
	# Own_Criteria_2=(Pstar/(Rstar*Tstar))*((x*(-((1-Rtilde)*(ln(1-Rtilde))/Rtilde)-((ln(Rtilde))/r)))-((1-x)*(((1/Ttilde)*Rratio*(exp(-((Tratio)**2)/(Pratio*Ttilde)))/(1+Rratio*exp(-((Tratio)**2)/(Pratio*Ttilde))))+((Pratio/Tratio)*ln(1+Rratio*exp(-(Tratio**2)/(Pratio*Ttilde)))))))
	Own_Criteria_1=(Pstar/(Rstar*Tstar))*(-((1-Rtilde)*(ln(1-Rtilde))/Rtilde)-((ln(Rtilde))/r)+((1/Ttilde)*Rratio*(exp(-((Tratio)**2)/(Pratio*Ttilde)))/(1+Rratio*exp(-((Tratio)**2)/(Pratio*Ttilde))))+((Pratio/Tratio)*ln(1+Rratio*exp(-(Tratio**2)/(Pratio*Ttilde))))-(x)-((((x)*Pratio)/Tratio)*ln(1+Rratio)))
	
	#Condo Theory:
	# I have replaced (z-2) with Rratio
	# S_condo=(Pstar/(Rstar*Tstar))*(-((1-Rtilde)*(ln(1-Rtilde))/Rtilde)-((ln(Rtilde))/r)-((1/r)*ln(1/r))-1-((ln(2/((Rratio)+2))-1)/r)-((r-2)/r)*(ln(1-(((Rratio)*exp(-epsilon_2/(kB*T)))/(1+(Rratio)*exp(-epsilon_2/(kB*T)))))-((((Rratio)*exp(-epsilon_2/(kB*T)))/(1+(Rratio)*exp(-epsilon_2/(kB*T))))*epsilon_2/(kB*T))))
	# S_condo_again=(Pstar/(Rstar*Tstar))*(-(((1-Rtilde)/Rtilde)*(ln(1-Rtilde)))-((ln(Rtilde))/r)+((ln(r))/r)-1-(((ln(2/(Rratio+2)))-1)/r)-(((r-2)/r)*((ln(1-((Rratio*(exp(-epsilon_2/(kB*T))))/(1+(Rratio*(exp(-epsilon_2/(kB*T))))))))-((((Rratio*(exp(-epsilon_2/(kB*T))))/(1+(Rratio*(exp(-epsilon_2/(kB*T))))))*epsilon_2)/(kB*T)))))
	# dS_dTg_condo=(1+(ln(1-Rtilde)/Rtilde))*(1/Rtilde)*(dPtilde_dT+(1/Tstar)*(ln(1-Rtilde)+Rtilde))-(((((Rratio)*exp(-epsilon_2/(kB*T)))/(1+((Rratio)*exp(-epsilon_2/(kB*T)))))*epsilon_2)/(kB*T**2))*(((1-(((Rratio)*exp(-epsilon_2/(kB*T)))/(1+((Rratio)*exp(-epsilon_2/(kB*T))))))*epsilon_2)/(kB*T))*(2*Rtilde-(Ttilde/(1-Rtilde))+Ttilde)
	# dS_dTg_condo_again=(((r-2)/r)*((epsilon_2/(kB*T))**2)*(((Rratio*(exp(-epsilon_2/(kB*T))))/(1+(Rratio*(exp(-epsilon_2/(kB*T))))))*(1-((Rratio*(exp(-epsilon_2/(kB*T))))/(1+(Rratio*(exp(-epsilon_2/(kB*T)))))))/T)*((Rtilde)**2)*(((Ttilde/Rtilde)*((1/r)+(Rtilde/(1-Rtilde))))-2))+((((ln(1-Rtilde))/(Rtilde))+1-(1/r))*((dPtilde_dT)+((1/Tstar)*((ln(1-Rtilde))+((1-(1/r))*Rtilde)))))

	res=Own_Criteria_1

	return res

def glassTemp(P,**kwargs):
	
	for key,value in kwargs.items():
		exec "%s=%s" % (key,value)
	
	Tg = bisect(glassTransitionCriteria,100,10000,args=(P,M,x,Rratio,Tratio,Vratio,Pstar,Tstar,Rstar))
	
	return Tg

def ResidualArray(params,P,Tg):
	
	Pstar = params['Pstar'].value
	Tstar = params['Tstar'].value
	Rstar = params['Rstar'].value
	M = params['M'].value
	epsilon_2 = params['epsilon_2'].value
	Rratio = params['Rratio'].value
	Vratio = params['Vratio'].value
	x = params['x'].value
	Tg_atm = params['Tg_atm'].value

	Tstarstar=epsilon_2/kB
	Tratio=Tstarstar/Tstar

	kwargs = {'Pstar':Pstar,'Tstar':Tstar,'Rstar':Rstar,'M':M,'Tratio':Tratio,'Rratio':Rratio,'Vratio':Vratio,'x':x,'Tg_atm':Tg_atm}
	
	print Rratio
	print Vratio
	print epsilon_2
	print x
	
	residual=npy.zeros(len(P))

	for j in range(0,len(P)):
		Tg_calculated = glassTemp(P[j],**kwargs)
		residual[j] = abs((Tg[j]-Tg_calculated))
	
	return residual

P = P_atm
T=Tg_atm
M=M_infinity
R=density(P,T,M,Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)
r = (Pstar*M)/(kB*Tstar*Rstar)
dP_dT_atm=1/dTg_dP_atm

Ptilde=P/Pstar
Ttilde=T/Tstar
Rtilde=R/Rstar
# vtilde=1/Rtilde	
dPtilde_dT=dP_dT_atm/Pstar
dPtilde_dTtilde=dP_dT_atm*Tstar/Pstar
#####################################################################################################

#####################################################################################################
'''
#Condo Paper Equation Set
#Simultaneous Equation Solver
mpmath.mp.dps = 15
Vratio=1.0
Rratio = Symbol('Rratio')
epsilon_2 = Symbol('epsilon_2')
# F_condo=((Rratio*(exp(-epsilon_2/(kB*T))))/(1+(Rratio*(exp(-epsilon_2/(kB*T))))))
# S_condo=(Pstar/(Rstar*Tstar))*(-((1-Rtilde)*(ln(1-Rtilde))/Rtilde)-((ln(Rtilde))/r)-((1/r)*ln(1/r))-1-((ln(2/((Rratio)+2))-1)/r)-((r-2)/r)*(ln(1-(((Rratio)*exp(-epsilon_2/(kB*T)))/(1+(Rratio)*exp(-epsilon_2/(kB*T)))))-((((Rratio)*exp(-epsilon_2/(kB*T)))/(1+(Rratio)*exp(-epsilon_2/(kB*T))))*epsilon_2/(kB*T))))
S_condo_again=(Pstar/(Rstar*Tstar))*(-(((1-Rtilde)/Rtilde)*(ln(1-Rtilde)))-((ln(Rtilde))/r)+((ln(r))/r)-1-(((ln(2/(Rratio+2)))-1)/r)-(((r-2)/r)*((ln(1-((Rratio*(exp(-epsilon_2/(kB*T))))/(1+(Rratio*(exp(-epsilon_2/(kB*T))))))))-((((Rratio*(exp(-epsilon_2/(kB*T))))/(1+(Rratio*(exp(-epsilon_2/(kB*T))))))*epsilon_2)/(kB*T)))))
# dS_dTg_condo=(1+(ln(1-Rtilde)/Rtilde))*(1/Rtilde)*(dPtilde_dT+(1/Tstar)*(ln(1-Rtilde)+Rtilde))-(((((Rratio)*exp(-epsilon_2/(kB*T)))/(1+((Rratio)*exp(-epsilon_2/(kB*T)))))*epsilon_2)/(kB*T**2))*(((1-(((Rratio)*exp(-epsilon_2/(kB*T)))/(1+((Rratio)*exp(-epsilon_2/(kB*T))))))*epsilon_2)/(kB*T))*(2*Rtilde-(Ttilde/(1-Rtilde))+Ttilde)
dS_dTg_condo_again=(((r-2)/r)*((epsilon_2/(kB*T))**2)*(((Rratio*(exp(-epsilon_2/(kB*T))))/(1+(Rratio*(exp(-epsilon_2/(kB*T))))))*(1-((Rratio*(exp(-epsilon_2/(kB*T))))/(1+(Rratio*(exp(-epsilon_2/(kB*T)))))))/T)*((Rtilde)**2)*(((Ttilde/Rtilde)*((1/r)+(Rtilde/(1-Rtilde))))-2))+((((ln(1-Rtilde))/(Rtilde))+1-(1/r))*((dPtilde_dT)+((1/Tstar)*((ln(1-Rtilde))+((1-(1/r))*Rtilde)))))
answer=nsolve((dS_dTg_condo_again, S_condo_again), (Rratio, epsilon_2), (10.00, 7483.0),verify=False)

Rratio=answer[0]
epsilon_2=answer[1]
print Rratio+2
print epsilon_2
'''
######################################################################################################
'''
######################################################################################################
#Russell Trick to Take Condo Values and Solve for 'x':
epsilon_2=7550.38882		#PMMA 140kilo=6251.31324				#PS=6480.99556
Rratio=63.5105956			#PMMA 140kilo=1.20630412					#PS=1.85399320
Tstarstar=epsilon_2/kB
Tratio=Tstarstar/Tstar
Vratio=1.0
Pratio=Tratio/Vratio

x = Symbol('x')
Own_Criteria_1=(Pstar/(Rstar*Tstar))*(-((1-Rtilde)*(ln(1-Rtilde))/Rtilde)-((ln(Rtilde))/r)+((1/Ttilde)*Rratio*(exp(-((Tratio)**2)/(Pratio*Ttilde)))/(1+Rratio*exp(-((Tratio)**2)/(Pratio*Ttilde))))+((Pratio/Tratio)*ln(1+Rratio*exp(-(Tratio**2)/(Pratio*Ttilde))))-(x)-((((x)*Pratio)/Tratio)*ln(1+Rratio)))
answer= solve(Own_Criteria_1, x)
print answer

#x for PMMA Condo Parameters = 0.369816781806696
#x for PS Condo Parameters= 0.387169766204568
#x for PMMA 140kilo Parameters = 0.359891658197082
#x for PMMA 44kilo Parameters = 0.717785934207030
######################################################################################################

######################################################################################################

x=0.387169766204568
epsilon_2=7151.0
Tstarstar=epsilon_2/kB
Tratio=Tstarstar/Tstar
Rratio=3.0
Vratio=1.0
Pratio=Tratio/Vratio
Own_Criteria_1=(Pstar/(Rstar*Tstar))*(-((1-Rtilde)*(ln(1-Rtilde))/Rtilde)-((ln(Rtilde))/r)+((1/Ttilde)*Rratio*(exp(-((Vratio*epsilon_2))/(kB*T)))/(1+Rratio*exp(-((Vratio*epsilon_2))/(kB*T))))+((1/Vratio)*ln(1+Rratio*exp(-(Vratio*epsilon_2)/(kB*T))))-(x)-((x/Vratio)*ln(1+Rratio)))
# dS_dT_Own_Criteria_1=(Vratio*Ttilde*((1-(1/r))+((ln(1-Rtilde))/Rtilde))*(((1-(1/r))+((ln(1-Rtilde))/Rtilde))+((1/Rtilde)*(dPtilde_dTtilde)))/(Rtilde*(((Ttilde/Rtilde)*((Rtilde/(1-Rtilde))+(1/r)))-2)))+(((Vratio*epsilon_2/(kB*T))**2)*((Rratio*exp(-(Vratio*epsilon_2)/(kB*T)))/(1+Rratio*exp(-(Vratio*epsilon_2)/(kB*T))))*(1-((Rratio*exp(-(Vratio*epsilon_2)/(kB*T)))/(1+Rratio*exp(-(Vratio*epsilon_2)/(kB*T))))))
Own_Criteria_11=(Pstar/(Rstar*Tstar))*(-((1-Rtilde)*(ln(1-Rtilde))/Rtilde)-((ln(Rtilde))/r)+((1/Ttilde)*Rratio*(exp(-((Tratio)**2)/(Pratio*Ttilde)))/(1+Rratio*exp(-((Tratio)**2)/(Pratio*Ttilde))))+((Pratio/Tratio)*ln(1+Rratio*exp(-(Tratio**2)/(Pratio*Ttilde))))-(x)-((((x)*Pratio)/Tratio)*ln(1+Rratio)))

#######################################################################################################
'''
'''
#######################################################################################################
#Fitting on Experimental Data for Own_Criteria_1:
e=2.718281
# x=0.387169766204568#1/e
# Vratio=1.0
# F=((Rratio*exp(-(Vratio*epsilon_2)/(kB*T)))/(1+Rratio*exp(-(Vratio*epsilon_2)/(kB*T))))
# Own_Criteria_1=(Pstar/(Rstar*Tstar))*(-((1-Rtilde)*(ln(1-Rtilde))/Rtilde)-((ln(Rtilde))/r)+((1/Ttilde)*Rratio*(exp(-((Vratio*epsilon_2))/(kB*T)))/(1+Rratio*exp(-((Vratio*epsilon_2))/(kB*T))))+((1/Vratio)*ln(1+Rratio*exp(-(Vratio*epsilon_2)/(kB*T))))-(x)-((x/Vratio)*ln(1+Rratio)))

#Fitting Data to the base curve below glass transition:
params = Parameters()
#The following code sets up the model's parameters. It includes both fitting parameters and parameters that will remain fixed
#for the fitting. The values given are the inital guesses of fitting parameters and values of fixed parameters.
#						(Name,			Value,		        Vary?,	Min,	Max,	Expr)
params.add_many((		'x',			1/e,				True,	0.0,	1.0,	None),
				(		'Vratio',		1.0,				False,	0.0,	None,	None),
				(		'epsilon_2',	7000.0,				True,	2000.0,	None,	None),
				(		'Rratio',		1.40,				False,	0.0,	None,	None),
				(		'Pstar',		Pstar,				False,	0.0,	None,	None),
				(		'Tstar',		Tstar,				False,	0.0,	None,	None),
				(		'Rstar',		Rstar,				False,	0.0,	None,	None),
				(		'M',			M,					False,	0.0,	None,	None),
				(		'Tg_atm',		Tg_atm,		        False,	0.0,	None,	None))

#Running the Levenberg-Marquart algorithm on the residuals in order to do least squares fitting. This will return the fitted value of the RESIDUALS.
#These need to be added to the experimental datapints to find the fitted specific heat.
fit = minimize(ResidualArray,params,args=(Pg_exp,Tg_exp))

#Reporting the values of the parameters. NEED TO FIGURE OUT HOW TO PRINT THIS TO FILE.
report_fit(fit.params)

if 'epsilon_2' in fit.params and 'Rratio' in fit.params:
	epsilon_2 = fit.params['epsilon_2'].value
	Rratio = fit.params['Rratio'].value
	x = fit.params['x'].value
	Vratio = fit.params['Vratio'].value
	#kwargs = {'A':A,'B':B}

#######################################################################################################
'''
'''
#######################################################################################################

z=5.79499958093261  #4.81366805048692				#4.86914200453447				#4.81366805059756
epsilon_2=11513.8982105149  #7114.32278870336		#7210.44342406770			#7114.32278892748

# res=(1+(ln(1-Rtilde)/Rtilde))*(1/Rtilde)*(dPtilde_dT+(1/Tstar)*(ln(1-Rtilde)+Rtilde))-(((((Rratio)*exp(-epsilon_2/(kB*T)))/(1+((Rratio)*exp(-epsilon_2/(kB*T)))))*epsilon_2)/(kB*T**2))*(1+((1-(((Rratio)*exp(-epsilon_2/(kB*T)))/(1+((Rratio)*exp(-epsilon_2/(kB*T))))))*epsilon_2)/(kB*T))*(2*Rtilde-(Ttilde/(1-Rtilde))+Ttilde)
# S_condo=(Pstar/(Rstar*Tstar))*(-((1-Rtilde)*(ln(1-Rtilde))/Rtilde)-((ln(Rtilde))/r)-((1/r)*ln(1/r))-1-((ln(2/((Rratio)+2))-1)/r)-((r-2)/r)*(ln(1-(((Rratio)*exp(-epsilon_2/(kB*T)))/(1+(Rratio)*exp(-epsilon_2/(kB*T)))))-((((Rratio)*exp(-epsilon_2/(kB*T)))/(1+(Rratio)*exp(-epsilon_2/(kB*T))))*epsilon_2/(kB*T))))
# print S_condo
# print res

P_line = npy.linspace(0.101325,200,15)
T_line = npy.zeros(len(P_line))
R_line=npy.zeros(len(P_line))
#d2S_dT2_P_line=npy.zeros(len(P_line))


#Ideal Experimental Straight Line Data
for i in range(0,len(P_line)):
	T_line[i]=((P_line[i]-P)/dP_dT_atm)+T
	#R_line[i]=density(P_line[i],T_line[i],M,Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)
'''
###############################################################################

###############################################################################




Rratio =	2.50780099		#PMMA 140kilo=1.20630412				#PS=1.85399320
epsilon_2 = 6672.351494		#PMMA 140kilo=6251.31324				#PS=6480.99556
x=0.18903349			#PMMA 140kilo= 0.359891658197082    	#PS=0.381795#1/e
Tstarstar=epsilon_2/kB
Tratio=Tstarstar/Tstar
Vratio=1.0

#Initializing the array of densities.
P = npy.linspace(0.101325,600,20)
R=npy.zeros(len(P))
# Tg_From_S=npy.zeros(len(P))		
# Tg_From_Deriv=npy.zeros(len(P0))
Tg_calculated=npy.zeros(len(P))

for i in range(0,len(P)):

	# Tg_From_S[i]=CondoGlassTempFromEntropy(P0[i],M,z,epsilon_2,Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)
	#Tg_From_Deriv[i]=CondoGlassTempFromDeriv(P0[i],M,dP_dT_atm,z,epsilon_2,Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)
	Tg_calculated[i]=glassTemp(P[i],M=M,x=x,Rratio=Rratio,Tratio=Tratio,Vratio=Vratio,Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)
	print P[i]

# for i in range(0,len(P0)):
# 	R0[i]=density(P0[i],T0[i],M,Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)	
	
#Setting font size
axis_size = 20
title_size = 20
size = 14
label_size = 20
plt.rcParams['xtick.labelsize'] = label_size
plt.rcParams['ytick.labelsize'] = label_size

#Setting saved image properties
img_extension = '.png'
img_dpi = None
output_folder = 'plots'

#Checking for existence of output directory. If such a directory doesn't exist, one is created.
if not os.path.exists('./'+output_folder):
    os.makedirs('./'+output_folder)

#General line properties.
linewidth = 1
markersize = 6

arrow_ls = 'dashdot'
show_arrows = True

#==================================================================================
#Plots.
figPUREPS=plt.figure(num=None, figsize=(10,6), dpi=img_dpi, facecolor='w', edgecolor='k')
ax = plt.axes()

#plt.plot(P0,Tg_From_S,'k',color='g',lw=linewidth,ls='-',label='T Versus P of Pure PMMA Condo from S')
#plt.plot(P0,Tg_From_Deriv,'k',color='r',lw=linewidth,ls='-',label='T Versus P of Pure PMMA Condo from Deriv')

plt.plot(P,Tg_calculated,'k',color='g',lw=linewidth,ls='-',label='Fit')
# plt.plot(P_line,T_line,'k',color='r',lw=linewidth,ls='-',label='Pure PMMA Ideal Straight Line')
plt.plot(Pg_exp,Tg_exp,'sk',ms=markersize,label='Exp. Data')

# plt.axvline(x=378,lw=0.5,color='k', linestyle='-.')

plt.xlabel('Pressure P (MPa)',fontsize=axis_size)
plt.ylabel(r'Glass Temperature (K)',fontsize=axis_size)
#plt.axis([300,500,0,1.5])
plt.legend(loc=4,fontsize=size,numpoints=1)
plt.subplots_adjust(bottom=0.3)

#figPUREPS.savefig('./'+output_folder+r'\pure_PMMA_Tg vs P'+img_extension,dpi=img_dpi)

plt.show()
