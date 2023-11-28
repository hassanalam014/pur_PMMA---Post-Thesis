from __future__ import division
import os,sys,math,csv,numpy as npy
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)

#======================================================
#Critical Point and Molecular Weight
#======================================================

Pc0 = 0.001
Tc0 = 265.0
Rc0 = 0.0001

#======================================================
#Loading Isotherm Data
#======================================================

with open('DataSwelling/453K_LPP_PST.csv','rb') as csvfile:
	datareader = csv.reader(csvfile)
	#S0 = (float(column[1]) for column in datareader)
	index1 = 0
	index2 = 0
	for row in datareader:
		if index1 == 4:
			numpts = int(float(row[0]))
			P0_453K = range(0,numpts)
			S0_453K = range(0,numpts)
			T0_453K = range(0,numpts)
			M0_453K = range(0,numpts)
			I0_453K = range(0,numpts)
		if index1 >= 6:
			P0_453K[index2] = float(row[0])
			S0_453K[index2] = float(row[1])
			T0_453K[index2] = float(row[2])
			M0_453K[index2] = float(row[3])
			I0_453K[index2] = 'isotherm'
			index2 = index2 + 1
		index1 = index1 + 1
		
P0 = P0_453K
S0 = S0_453K
T0 = T0_453K
M0 = M0_453K
I0 = I0_453K

with open('DataSwelling/473K_LPP_PST.csv','rb') as csvfile:
	datareader = csv.reader(csvfile)
	#S0 = (float(column[1]) for column in datareader)
	index1 = 0
	index2 = 0
	for row in datareader:
		if index1 == 4:
			numpts = int(float(row[0]))
			P0_473K = range(0,numpts)
			S0_473K = range(0,numpts)
			T0_473K = range(0,numpts)
			M0_473K = range(0,numpts)
			I0_473K = range(0,numpts)
		if index1 >= 6:
			P0_473K[index2] = float(row[0])
			S0_473K[index2] = float(row[1])
			T0_473K[index2] = float(row[2])
			M0_473K[index2] = float(row[3])
			I0_473K[index2] = 'isotherm'
			index2 = index2 + 1
		index1 = index1 + 1

P0 = npy.concatenate((P0,P0_473K),axis=0)
S0 = npy.concatenate((S0,S0_473K),axis=0)
T0 = npy.concatenate((T0,T0_473K),axis=0)
M0 = npy.concatenate((M0,M0_473K),axis=0)
I0 = npy.concatenate((I0,I0_473K),axis=0)

with open('DataSwelling/493K_LPP_PST.csv','rb') as csvfile:
	datareader = csv.reader(csvfile)
	#S0 = (float(column[1]) for column in datareader)
	index1 = 0
	index2 = 0
	for row in datareader:
		if index1 == 4:
			numpts = int(float(row[0]))
			P0_493K = range(0,numpts)
			S0_493K = range(0,numpts)
			T0_493K = range(0,numpts)
			M0_493K = range(0,numpts)
			I0_493K = range(0,numpts)
		if index1 >= 6:
			P0_493K[index2] = float(row[0])
			S0_493K[index2] = float(row[1])
			T0_493K[index2] = float(row[2])
			M0_493K[index2] = float(row[3])
			I0_493K[index2] = 'isotherm'
			index2 = index2 + 1
		index1 = index1 + 1

P0_S = npy.concatenate((P0,P0_493K),axis=0)
S0_S = npy.concatenate((S0,S0_493K),axis=0)
T0_S = npy.concatenate((T0,T0_493K),axis=0)
M0_S = npy.concatenate((M0,M0_493K),axis=0)
I0_S = npy.concatenate((I0,I0_493K),axis=0)

# print P0
# print S0
# print T0