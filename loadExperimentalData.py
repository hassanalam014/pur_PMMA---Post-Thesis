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

with open('Data/402K_PS_11E4_PVT.csv','rb') as csvfile:
	datareader = csv.reader(csvfile)
	#x0 = (float(column[1]) for column in datareader)
	index1 = 0
	index2 = 0
	for row in datareader:
		if index1 == 4:
			numpts = int(float(row[0]))
			P0_402K = range(0,numpts)
			T0_402K = range(0,numpts)
			R0_402K = range(0,numpts)
			M0_402K = range(0,numpts)
			I0_402K = range(0,numpts)
		if index1 >= 6:
			P0_402K[index2] = float(row[0])
			T0_402K[index2] = float(row[1])
			R0_402K[index2] = float(row[2])
			M0_402K[index2] = float(row[3])
			I0_402K[index2] = 'isotherm'
			index2 = index2 + 1
		index1 = index1 + 1
		
P0 = P0_402K
T0 = T0_402K
R0 = R0_402K
M0 = M0_402K
I0 = I0_402K

with open('Data/412K_PS_11E4_PVT.csv','rb') as csvfile:
	datareader = csv.reader(csvfile)
	#x0 = (float(column[1]) for column in datareader)
	index1 = 0
	index2 = 0
	for row in datareader:
		if index1 == 4:
			numpts = int(float(row[0]))
			P0_412K = range(0,numpts)
			T0_412K = range(0,numpts)
			R0_412K = range(0,numpts)
			M0_412K = range(0,numpts)
			I0_412K = range(0,numpts)
		if index1 >= 6:
			P0_412K[index2] = float(row[0])
			T0_412K[index2] = float(row[1])
			R0_412K[index2] = float(row[2])
			M0_412K[index2] = float(row[3])
			I0_412K[index2] = 'isotherm'
			index2 = index2 + 1
		index1 = index1 + 1

P0 = npy.concatenate((P0,P0_412K),axis=0)
T0 = npy.concatenate((T0,T0_412K),axis=0)
R0 = npy.concatenate((R0,R0_412K),axis=0)
M0 = npy.concatenate((M0,M0_412K),axis=0)
I0 = npy.concatenate((I0,I0_412K),axis=0)

with open('Data/422K_PS_11E4_PVT.csv','rb') as csvfile:
	datareader = csv.reader(csvfile)
	#x0 = (float(column[1]) for column in datareader)
	index1 = 0
	index2 = 0
	for row in datareader:
		if index1 == 4:
			numpts = int(float(row[0]))
			P0_422K = range(0,numpts)
			T0_422K = range(0,numpts)
			R0_422K = range(0,numpts)
			M0_422K = range(0,numpts)
			I0_422K = range(0,numpts)
		if index1 >= 6:
			P0_422K[index2] = float(row[0])
			T0_422K[index2] = float(row[1])
			R0_422K[index2] = float(row[2])
			M0_422K[index2] = float(row[3])
			I0_422K[index2] = 'isotherm'
			index2 = index2 + 1
		index1 = index1 + 1

P0 = npy.concatenate((P0,P0_422K),axis=0)
T0 = npy.concatenate((T0,T0_422K),axis=0)
R0 = npy.concatenate((R0,R0_422K),axis=0)
M0 = npy.concatenate((M0,M0_422K),axis=0)
I0 = npy.concatenate((I0,I0_422K),axis=0)

with open('Data/432K_PS_11E4_PVT.csv','rb') as csvfile:
	datareader = csv.reader(csvfile)
	#x0 = (float(column[1]) for column in datareader)
	index1 = 0
	index2 = 0
	for row in datareader:
		if index1 == 4:
			numpts = int(float(row[0]))
			P0_432K = range(0,numpts)
			T0_432K = range(0,numpts)
			R0_432K = range(0,numpts)
			M0_432K = range(0,numpts)
			I0_432K = range(0,numpts)
		if index1 >= 6:
			P0_432K[index2] = float(row[0])
			T0_432K[index2] = float(row[1])
			R0_432K[index2] = float(row[2])
			M0_432K[index2] = float(row[3])
			I0_432K[index2] = 'isotherm'
			index2 = index2 + 1
		index1 = index1 + 1

P0 = npy.concatenate((P0,P0_432K),axis=0)
T0 = npy.concatenate((T0,T0_432K),axis=0)
R0 = npy.concatenate((R0,R0_432K),axis=0)
M0 = npy.concatenate((M0,M0_432K),axis=0)
I0 = npy.concatenate((I0,I0_432K),axis=0)

with open('Data/442K_PS_11E4_PVT.csv','rb') as csvfile:
	datareader = csv.reader(csvfile)
	#x0 = (float(column[1]) for column in datareader)
	index1 = 0
	index2 = 0
	for row in datareader:
		if index1 == 4:
			numpts = int(float(row[0]))
			P0_442K = range(0,numpts)
			T0_442K = range(0,numpts)
			R0_442K = range(0,numpts)
			M0_442K = range(0,numpts)
			I0_442K = range(0,numpts)
		if index1 >= 6:
			P0_442K[index2] = float(row[0])
			T0_442K[index2] = float(row[1])
			R0_442K[index2] = float(row[2])
			M0_442K[index2] = float(row[3])
			I0_442K[index2] = 'isotherm'
			index2 = index2 + 1
		index1 = index1 + 1

P0 = npy.concatenate((P0,P0_442K),axis=0)
T0 = npy.concatenate((T0,T0_442K),axis=0)
R0 = npy.concatenate((R0,R0_442K),axis=0)
M0 = npy.concatenate((M0,M0_442K),axis=0)
I0 = npy.concatenate((I0,I0_442K),axis=0)

with open('Data/452K_PS_11E4_PVT.csv','rb') as csvfile:
	datareader = csv.reader(csvfile)
	#x0 = (float(column[1]) for column in datareader)
	index1 = 0
	index2 = 0
	for row in datareader:
		if index1 == 4:
			numpts = int(float(row[0]))
			P0_452K = range(0,numpts)
			T0_452K = range(0,numpts)
			R0_452K = range(0,numpts)
			M0_452K = range(0,numpts)
			I0_452K = range(0,numpts)
		if index1 >= 6:
			P0_452K[index2] = float(row[0])
			T0_452K[index2] = float(row[1])
			R0_452K[index2] = float(row[2])
			M0_452K[index2] = float(row[3])
			I0_452K[index2] = 'isotherm'
			index2 = index2 + 1
		index1 = index1 + 1

P0 = npy.concatenate((P0,P0_452K),axis=0)
T0 = npy.concatenate((T0,T0_452K),axis=0)
R0 = npy.concatenate((R0,R0_452K),axis=0)
M0 = npy.concatenate((M0,M0_452K),axis=0)
I0 = npy.concatenate((I0,I0_452K),axis=0)

with open('Data/463K_PS_11E4_PVT.csv','rb') as csvfile:
	datareader = csv.reader(csvfile)
	#x0 = (float(column[1]) for column in datareader)
	index1 = 0
	index2 = 0
	for row in datareader:
		if index1 == 4:
			numpts = int(float(row[0]))
			P0_463K = range(0,numpts)
			T0_463K = range(0,numpts)
			R0_463K = range(0,numpts)
			M0_463K = range(0,numpts)
			I0_463K = range(0,numpts)
		if index1 >= 6:
			P0_463K[index2] = float(row[0])
			T0_463K[index2] = float(row[1])
			R0_463K[index2] = float(row[2])
			M0_463K[index2] = float(row[3])
			I0_463K[index2] = 'isotherm'
			index2 = index2 + 1
		index1 = index1 + 1

P0 = npy.concatenate((P0,P0_463K),axis=0)
T0 = npy.concatenate((T0,T0_463K),axis=0)
R0 = npy.concatenate((R0,R0_463K),axis=0)
M0 = npy.concatenate((M0,M0_463K),axis=0)
I0 = npy.concatenate((I0,I0_463K),axis=0)

with open('Data/473K_PS_11E4_PVT.csv','rb') as csvfile:
	datareader = csv.reader(csvfile)
	#x0 = (float(column[1]) for column in datareader)
	index1 = 0
	index2 = 0
	for row in datareader:
		if index1 == 4:
			numpts = int(float(row[0]))
			P0_473K = range(0,numpts)
			T0_473K = range(0,numpts)
			R0_473K = range(0,numpts)
			M0_473K = range(0,numpts)
			I0_473K = range(0,numpts)
		if index1 >= 6:
			P0_473K[index2] = float(row[0])
			T0_473K[index2] = float(row[1])
			R0_473K[index2] = float(row[2])
			M0_473K[index2] = float(row[3])
			I0_473K[index2] = 'isotherm'
			index2 = index2 + 1
		index1 = index1 + 1

P0 = npy.concatenate((P0,P0_473K),axis=0)
T0 = npy.concatenate((T0,T0_473K),axis=0)
R0 = npy.concatenate((R0,R0_473K),axis=0)
M0 = npy.concatenate((M0,M0_473K),axis=0)
I0 = npy.concatenate((I0,I0_473K),axis=0)

with open('Data/482K_PS_11E4_PVT.csv','rb') as csvfile:
	datareader = csv.reader(csvfile)
	#x0 = (float(column[1]) for column in datareader)
	index1 = 0
	index2 = 0
	for row in datareader:
		if index1 == 4:
			numpts = int(float(row[0]))
			P0_482K = range(0,numpts)
			T0_482K = range(0,numpts)
			R0_482K = range(0,numpts)
			M0_482K = range(0,numpts)
			I0_482K = range(0,numpts)
		if index1 >= 6:
			P0_482K[index2] = float(row[0])
			T0_482K[index2] = float(row[1])
			R0_482K[index2] = float(row[2])
			M0_482K[index2] = float(row[3])
			I0_482K[index2] = 'isotherm'
			index2 = index2 + 1
		index1 = index1 + 1

P0 = npy.concatenate((P0,P0_482K),axis=0)
T0 = npy.concatenate((T0,T0_482K),axis=0)
R0 = npy.concatenate((R0,R0_482K),axis=0)
M0 = npy.concatenate((M0,M0_482K),axis=0)
I0 = npy.concatenate((I0,I0_482K),axis=0)

with open('Data/492K_PS_11E4_PVT.csv','rb') as csvfile:
	datareader = csv.reader(csvfile)
	#x0 = (float(column[1]) for column in datareader)
	index1 = 0
	index2 = 0
	for row in datareader:
		if index1 == 4:
			numpts = int(float(row[0]))
			P0_492K = range(0,numpts)
			T0_492K = range(0,numpts)
			R0_492K = range(0,numpts)
			M0_492K = range(0,numpts)
			I0_492K = range(0,numpts)
		if index1 >= 6:
			P0_492K[index2] = float(row[0])
			T0_492K[index2] = float(row[1])
			R0_492K[index2] = float(row[2])
			M0_492K[index2] = float(row[3])
			I0_492K[index2] = 'isotherm'
			index2 = index2 + 1
		index1 = index1 + 1

P0 = npy.concatenate((P0,P0_492K),axis=0)
T0 = npy.concatenate((T0,T0_492K),axis=0)
R0 = npy.concatenate((R0,R0_492K),axis=0)
M0 = npy.concatenate((M0,M0_492K),axis=0)
I0 = npy.concatenate((I0,I0_492K),axis=0)

with open('Data/503K_PS_11E4_PVT.csv','rb') as csvfile:
	datareader = csv.reader(csvfile)
	#x0 = (float(column[1]) for column in datareader)
	index1 = 0
	index2 = 0
	for row in datareader:
		if index1 == 4:
			numpts = int(float(row[0]))
			P0_503K = range(0,numpts)
			T0_503K = range(0,numpts)
			R0_503K = range(0,numpts)
			M0_503K = range(0,numpts)
			I0_503K = range(0,numpts)
		if index1 >= 6:
			P0_503K[index2] = float(row[0])
			T0_503K[index2] = float(row[1])
			R0_503K[index2] = float(row[2])
			M0_503K[index2] = float(row[3])
			I0_503K[index2] = 'isotherm'
			index2 = index2 + 1
		index1 = index1 + 1

P0 = npy.concatenate((P0,P0_503K),axis=0)
T0 = npy.concatenate((T0,T0_503K),axis=0)
R0 = npy.concatenate((R0,R0_503K),axis=0)
M0 = npy.concatenate((M0,M0_503K),axis=0)
I0 = npy.concatenate((I0,I0_503K),axis=0)

with open('Data/513K_PS_11E4_PVT.csv','rb') as csvfile:
	datareader = csv.reader(csvfile)
	#x0 = (float(column[1]) for column in datareader)
	index1 = 0
	index2 = 0
	for row in datareader:
		if index1 == 4:
			numpts = int(float(row[0]))
			P0_513K = range(0,numpts)
			T0_513K = range(0,numpts)
			R0_513K = range(0,numpts)
			M0_513K = range(0,numpts)
			I0_513K = range(0,numpts)
		if index1 >= 6:
			P0_513K[index2] = float(row[0])
			T0_513K[index2] = float(row[1])
			R0_513K[index2] = float(row[2])
			M0_513K[index2] = float(row[3])
			I0_513K[index2] = 'isotherm'
			index2 = index2 + 1
		index1 = index1 + 1

P0 = npy.concatenate((P0,P0_513K),axis=0)
T0 = npy.concatenate((T0,T0_513K),axis=0)
R0 = npy.concatenate((R0,R0_513K),axis=0)
M0 = npy.concatenate((M0,M0_513K),axis=0)
I0 = npy.concatenate((I0,I0_513K),axis=0)

with open('Data/524K_PS_11E4_PVT.csv','rb') as csvfile:
	datareader = csv.reader(csvfile)
	#x0 = (float(column[1]) for column in datareader)
	index1 = 0
	index2 = 0
	for row in datareader:
		if index1 == 4:
			numpts = int(float(row[0]))
			P0_524K = range(0,numpts)
			T0_524K = range(0,numpts)
			R0_524K = range(0,numpts)
			M0_524K = range(0,numpts)
			I0_524K = range(0,numpts)
		if index1 >= 6:
			P0_524K[index2] = float(row[0])
			T0_524K[index2] = float(row[1])
			R0_524K[index2] = float(row[2])
			M0_524K[index2] = float(row[3])
			I0_524K[index2] = 'isotherm'
			index2 = index2 + 1
		index1 = index1 + 1

P0 = npy.concatenate((P0,P0_524K),axis=0)
T0 = npy.concatenate((T0,T0_524K),axis=0)
R0 = npy.concatenate((R0,R0_524K),axis=0)
M0 = npy.concatenate((M0,M0_524K),axis=0)
I0 = npy.concatenate((I0,I0_524K),axis=0)

#======================================================
#Isotherm PVT Data
#======================================================

#Including all experimental data.
#temp = ['303K','312K','321K','332K','343K','354K','364K','373K','383K','393K','402K','412K','422K','432K','442K','452K','463K','473K','482K','492K','503K','513K','524K']
#Only data 20K above the glass transition.
#temp = ['402K','412K','422K','432K','442K','452K','463K','473K','482K','492K','503K','513K','524K']
#All data excluding all data within 20K of the glass transition.
#temp = ['303K','312K','321K','332K','343K','402K','412K','422K','432K','442K','452K','463K','473K','482K','492K','503K','513K','524K']

#for i in range(0,len(temp)):
#	exec "P0_%s,T0_%s,R0_%s,M0_%s,I0_%s = loadExperimentalData('%s_PS_11E4_PVT','isotherm',True)" % (temp[i],temp[i],temp[i],temp[i],temp[i],temp[i])