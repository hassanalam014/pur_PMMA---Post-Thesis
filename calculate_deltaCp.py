from __future__ import division
import os,sys,math,matplotlib.pyplot as plt,numpy as npy
from lmfit import minimize, Parameters, report_fit
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from loadPhysicalConstants import *
from scipy.optimize import bisect,fsolve
from scipy.interpolate import interp1d
from sympy import *
from optimizeResidualFunctions import pureEOSResidual
from loadSpecificHeatExperimentalData import *
from Parameters_of_Different_Polymers import *

def density(P,T,M,**kwargs):
	
	for key,value in kwargs.items():
		exec "%s=%s" % (key,value)
	
	r = (Pstar*M)/(kB*Tstar*Rstar)
	
	phi = bisect(pureEOSResidual,0.0000000000000001,0.9999999999999999,args=(P,T,M,Pstar,Tstar,Rstar))
	
	R = phi*Rstar
		
	return R

def specificHeat(P,T,R,M,**kwargs):     #Cp/mass  and **kwargs must contain "three" characteristic parameters and "three" flexibility parameters.
	
	for key,value in kwargs.items():
		exec "%s=%s" % (key,value)
	
	r = (Pstar*M)/(kB*Tstar*Rstar)
	
	Ptilde=P/Pstar
	Ttilde=T/Tstar
	Rtilde=R/Rstar
	
	C_kier=(Pstar/(Rstar*Tstar))*((((1+(Ptilde/(Rtilde**2)))**2)/(((Ttilde/Rtilde)*(((Ttilde/Rtilde)*((Rtilde/(1-Rtilde))+(1/r)))-2)))))
	C_line=A+B*T
	C_total=C_kier+C_line

	return C_total,C_kier,C_line

def specificHeatResidualArray(params,C,P,T,R,M,I,fit_type):
	
	A = params['A'].value
	B = params['B'].value
	Pstar = params['Pstar'].value
	Tstar = params['Tstar'].value
	Rstar = params['Rstar'].value

	kwargs = {'Pstar':Pstar,'Tstar':Tstar,'Rstar':Rstar,'A':A,'B':B}
	# print 'A is:',A
	# print 'B is:',B
	# print '----------------------'

	residual=npy.zeros(len(C))

	for j in range(0,len(C)):
		C_calculated,discard1,discard2 = specificHeat(P[j],T[j],R[j],M[j],**kwargs)
		residual[j] = (C[j]-C_calculated)

	return residual


Program_Running_For=['PMMA Grassia 140kilo']

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

P0=P_atm
M0=M0_complete_Tg[0]

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

print T0_below_Tg
print 'Fitting Below Tg'

#Fitting Data to the base curve below glass transition:
params_below_Tg = Parameters()
#The following code sets up the model's parameters. It includes both fitting parameters and parameters that will remain fixed
#for the fitting. The values given are the inital guesses of fitting parameters and values of fixed parameters.
#						(Name,			Value,		        Vary?,	Min,	Max,	Expr)
params_below_Tg.add_many(('A',			0.03,			    True,	0,		None,	None),
				(		'B',			0.003392431,		True,	0,		None,	None),
				(		'Pstar',		Pstar,				False,	0,		None,	None),
				(		'Tstar',		Tstar,				False,	0,		None,	None),
				(		'Rstar',		Rstar,				False,	0,		None,	None))

#Running the Levenberg-Marquart algorithm on the residuals in order to do least squares fitting. This will return the fitted value of the RESIDUALS.
#These need to be added to the experimental datapints to find the fitted specific heat.
fit = minimize(specificHeatResidualArray,params_below_Tg,args=(C0_below_Tg,P0_below_Tg,T0_below_Tg,R0_below_Tg,M0_below_Tg,I0_below_Tg,'C_below_Tg'))

#Reporting the values of the parameters. NEED TO FIGURE OUT HOW TO PRINT THIS TO FILE.
report_fit(fit.params)

if 'A' in fit.params and 'B' in fit.params:
	Abelow = fit.params['A'].value
	Bbelow = fit.params['B'].value
	#kwargs = {'A':AIterated,'B':BIterated}

print 'Abelow is: ', Abelow
print 'Bbelow is: ', Bbelow


Abelow=A
Bbelow=B

print T0_above_Tg
print 'Fitting Above Tg'

#Fitting Data to the base curve above glass transition:
params_above_Tg = Parameters()
#The following code sets up the model's parameters. It includes both fitting parameters and parameters that will remain fixed
#for the fitting. The values given are the inital guesses of fitting parameters and values of fixed parameters.
#						(Name,			Value,		        Vary?,	Min,	Max,	Expr)
params_above_Tg.add_many(('A',			0.03,			    True,	0,		None,	None),
				(		'B',			0.003392431,		True,	0,		None,	None),
				(		'Pstar',		Pstar,				False,	0,		None,	None),
				(		'Tstar',		Tstar,				False,	0,		None,	None),
				(		'Rstar',		Rstar,				False,	0,		None,	None))

#Running the Levenberg-Marquart algorithm on the residuals in order to do least squares fitting. This will return the fitted value of the RESIDUALS.
#These need to be added to the experimental datapints to find the fitted specific heat.
fit = minimize(specificHeatResidualArray,params_above_Tg,args=(C0_above_Tg,P0_above_Tg,T0_above_Tg,R0_above_Tg,M0_above_Tg,I0_above_Tg,'C_above_Tg'))

#Reporting the values of the parameters. NEED TO FIGURE OUT HOW TO PRINT THIS TO FILE.
report_fit(fit.params)

if 'A' in fit.params and 'B' in fit.params:
	Aabove = fit.params['A'].value
	Babove = fit.params['B'].value
	#kwargs = {'A':AIterated,'B':BIterated}

print 'Aabove=',Aabove
print 'Babove=',Babove

#To Calculate Delta Cp at Tg:
R0_at_Tg=density(P0,Tg_atm,M0,Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)
C_total_below_at_Tg,C_kier_below_at_Tg,C_line_below_at_Tg = specificHeat(P0,Tg_atm,R0_at_Tg,M0,Pstar=Pstar,Tstar=Tstar,Rstar=Rstar,A=Abelow,B=Bbelow)
C_total_above_at_Tg,C_kier_above_at_Tg,C_line_above_at_Tg = specificHeat(P0,Tg_atm,R0_at_Tg,M0,Pstar=Pstar,Tstar=Tstar,Rstar=Rstar,A=Aabove,B=Babove)

deltaCp=C_total_above_at_Tg-C_total_below_at_Tg
print 'deltaCp=',deltaCp

#######################################################################################

#######################################################################################
#Initializing the array of densities.
T0_below = npy.linspace(100,Tg_atm,100)
T0_above = npy.linspace(Tg_atm,600,100)

C_total_below=npy.zeros(len(T0_below))
C_kier_below=npy.zeros(len(T0_below))
C_line_below=npy.zeros(len(T0_below))
R0_below=npy.zeros(len(T0_below))

C_total_above=npy.zeros(len(T0_above))
C_kier_above=npy.zeros(len(T0_above))
C_line_above=npy.zeros(len(T0_above))
R0_above=npy.zeros(len(T0_above))

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
output_folder = 'plot_specificHeat'

#Checking for existence of output directory. If such a directory doesn't exist, one is created.
if not os.path.exists('./'+output_folder):
    os.makedirs('./'+output_folder)

#Defining linetype
# M179_line = '-'

for i in range(0,len(T0_below)):
	R0_below[i]=density(P0,T0_below[i],M0,Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)

for i in range(0,len(T0_below)):
	C_total_below[i],C_kier_below[i],C_line_below[i] = specificHeat(P0,T0_below[i],R0_below[i],M0,Pstar=Pstar,Tstar=Tstar,Rstar=Rstar,A=Abelow,B=Bbelow)


for i in range(0,len(T0_above)):
	R0_above[i]=density(P0,T0_above[i],M0,Pstar=Pstar,Tstar=Tstar,Rstar=Rstar)

for i in range(0,len(T0_above)):
	C_total_above[i],C_kier_above[i],C_line_above[i] = specificHeat(P0,T0_above[i],R0_above[i],M0,Pstar=Pstar,Tstar=Tstar,Rstar=Rstar,A=Aabove,B=Babove)

#General line properties.
linewidth = 1
markersize = 1

arrow_ls = 'dashdot'
show_arrows = True
#print M179K_C
#==================================================================================
#P versus R plots.
figPUREPS=plt.figure(num=None, figsize=(10,6), dpi=img_dpi, facecolor='w', edgecolor='k')
ax = plt.axes()

plt.axvline(x=Tg_atm,lw=0.5,color='k', linestyle='-.')

plt.plot(T0_below,C_total_below,'k',color='r',lw=linewidth,ls='-',label='C_Total')
plt.plot(T0_below,C_kier_below,'k',color='b',lw=linewidth,ls='--',label='C_Kier theory')
plt.plot(T0_below,C_line_below,'k',color='c',lw=linewidth,ls=':',label='C_A+BT theory')

plt.plot(T0_above,C_total_above,'k',color='r',lw=linewidth,ls='-',label='C_Total')
plt.plot(T0_above,C_kier_above,'k',color='b',lw=linewidth,ls='--',label='C_Kier theory')
plt.plot(T0_above,C_line_above,'k',color='c',lw=linewidth,ls=':',label='C_A+BT theory')

plt.plot(T0_complete_Tg,C0_complete_Tg,'sk',ms=markersize)#,label='36kilo experiment')
plt.xlabel('Temperature T (K)',fontsize=axis_size)
plt.ylabel(r'Specific Heat $c_P$ ($J/g.K$)',fontsize=axis_size)
# plt.axis([250,450,1.00,2.25])
plt.legend(loc=4,fontsize=size,numpoints=1)
plt.subplots_adjust(bottom=0.3)
plt.show()
