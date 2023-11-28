from __future__ import division
import os,sys,math,csv,numpy as npy
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)

#======================================================
#Loading Heat Capacity Data
#======================================================
# Polymer_Type ='PVME'
# Polymer_Weight = '60kilo'
# global Abelow,Bbelow,Aabove,Babove,A,B,deltaCp,T0_excluding_Tg,M0_excluding_Tg,C0_excluding_Tg,P0_excluding_Tg,I0_excluding_Tg,Tg0_excluding_Tg,T0_above_Tg,M0_above_Tg,C0_above_Tg,P0_above_Tg,I0_above_Tg,Tg0_above_Tg,T0_at_Tg,M0_at_Tg,C0_at_Tg,P0_at_Tg,I0_at_Tg,Tg0_at_Tg,T0_below_Tg,M0_below_Tg,C0_below_Tg,P0_below_Tg,I0_below_Tg,Tg0_below_Tg

def loadSpecificHeatExperimentalData(**kwargs):
	
	for key,value in kwargs.items():
		exec "%s='%s'" % (key,value)
	
	print 'Polymer Type', Polymer_Type, 'Polymer Weight', Polymer_Weight, 'Referenced from', Reference

	exec "Folder_and_File='DataSpecificHeat/%s_%s_TMCP.csv'" %(Polymer_Type,Polymer_Weight)

	with open(Folder_and_File,'rb') as csvfile:
		datareader = csv.reader(csvfile)
		#x0 = (float(column[1]) for column in datareader)
		index1 = 0
		index2 = 0
		for row in datareader:
			if index1 == 4:
				numpts = int(float(row[0]))
				T0_complete_Tg = range(0,numpts)
				M0_complete_Tg = range(0,numpts)
				C0_complete_Tg = range(0,numpts)
				P0_complete_Tg = range(0,numpts)
				I0_complete_Tg = range(0,numpts)
				Tg0_complete_Tg = range(0,numpts)
			if index1 >= 6:
				T0_complete_Tg[index2] = float(row[0])
				M0_complete_Tg[index2] = float(row[1])
				C0_complete_Tg[index2] = float(row[2])
				P0_complete_Tg[index2] = float(row[3])
				I0_complete_Tg[index2] = 'constant molar mass'
				Tg0_complete_Tg[index2] = float(row[4])
				index2 = index2 + 1
			index1 = index1 + 1
		
	#Diving Data into Below, At, Above Glass Transition and Exluding Glass Transition
	Tg_start=0
	for j in range (0,len(C0_complete_Tg)):
		if Tg0_complete_Tg[j]==1.0 and Tg_start==0:
			Tg_index_start=j
			Tg_start=Tg_start+1
		
		if Tg0_complete_Tg[j]==1.0 and Tg_start==1:
			Tg_index_end=j

	T0_below_Tg=range(0,Tg_index_start)
	M0_below_Tg=range(0,Tg_index_start)
	C0_below_Tg=range(0,Tg_index_start)
	P0_below_Tg=range(0,Tg_index_start)
	I0_below_Tg=range(0,Tg_index_start)
	Tg0_below_Tg=range(0,Tg_index_start)

	T0_at_Tg=range(0,Tg_index_end-Tg_index_start+1)
	M0_at_Tg=range(0,Tg_index_end-Tg_index_start+1)
	C0_at_Tg=range(0,Tg_index_end-Tg_index_start+1)
	P0_at_Tg=range(0,Tg_index_end-Tg_index_start+1)
	I0_at_Tg=range(0,Tg_index_end-Tg_index_start+1)
	Tg0_at_Tg=range(0,Tg_index_end-Tg_index_start+1)

	T0_above_Tg=range(0,len(Tg0_complete_Tg)-Tg_index_end-1)
	M0_above_Tg=range(0,len(Tg0_complete_Tg)-Tg_index_end-1)
	C0_above_Tg=range(0,len(Tg0_complete_Tg)-Tg_index_end-1)
	P0_above_Tg=range(0,len(Tg0_complete_Tg)-Tg_index_end-1)
	I0_above_Tg=range(0,len(Tg0_complete_Tg)-Tg_index_end-1)
	Tg0_above_Tg=range(0,len(Tg0_complete_Tg)-Tg_index_end-1)


	for j in range(Tg_index_start):
		T0_below_Tg[j]=T0_complete_Tg[j]
		M0_below_Tg[j]=M0_complete_Tg[j]
		C0_below_Tg[j]=C0_complete_Tg[j]
		P0_below_Tg[j]=P0_complete_Tg[j]
		I0_below_Tg[j]=I0_complete_Tg[j]
		Tg0_below_Tg[j]=Tg0_complete_Tg[j]

	for j in range(Tg_index_end-Tg_index_start+1):
		T0_at_Tg[j]=T0_complete_Tg[Tg_index_start+j]
		M0_at_Tg[j]=M0_complete_Tg[Tg_index_start+j]
		C0_at_Tg[j]=C0_complete_Tg[Tg_index_start+j]
		P0_at_Tg[j]=P0_complete_Tg[Tg_index_start+j]
		I0_at_Tg[j]=I0_complete_Tg[Tg_index_start+j]
		Tg0_at_Tg[j]=Tg0_complete_Tg[Tg_index_start+j]

	for j in range(len(Tg0_complete_Tg)-Tg_index_end-1):
		T0_above_Tg[j]=T0_complete_Tg[Tg_index_end+1+j]
		M0_above_Tg[j]=M0_complete_Tg[Tg_index_end+1+j]
		C0_above_Tg[j]=C0_complete_Tg[Tg_index_end+1+j]
		P0_above_Tg[j]=P0_complete_Tg[Tg_index_end+1+j]
		I0_above_Tg[j]=I0_complete_Tg[Tg_index_end+1+j]
		Tg0_above_Tg[j]=Tg0_complete_Tg[Tg_index_end+1+j]

	T0_excluding_Tg = npy.concatenate((T0_below_Tg,T0_above_Tg),axis=0)
	M0_excluding_Tg = npy.concatenate((M0_below_Tg,M0_above_Tg),axis=0)
	C0_excluding_Tg = npy.concatenate((C0_below_Tg,C0_above_Tg),axis=0)
	P0_excluding_Tg = npy.concatenate((P0_below_Tg,P0_above_Tg),axis=0)
	I0_excluding_Tg = npy.concatenate((I0_below_Tg,I0_above_Tg),axis=0)
	Tg0_excluding_Tg = npy.concatenate((Tg0_below_Tg,Tg0_above_Tg),axis=0)

	# print T0_below_Tg
	# print Tg0_below_Tg
	# print C0_below_Tg

	if Polymer_Type=='PVAc' and Polymer_Weight=='00kilo' and Reference=='Sandberg':
		A=0.34997622
		B=0.00231786
		Abelow=A
		Bbelow=B
		#Sandberg
		Aabove= 1.5965204698921966
		Babove= 2.0384654945360126e-05
		deltaCp= 0.51364961482

	if Polymer_Type=='PVAc' and Polymer_Weight=='00kilo' and Reference=='Roland':
		A=0.34997622
		B=0.00231786
		Abelow=A
		Bbelow=B
		#Roland
		Aabove= 1.5965204698921966
		Babove= 2.0384654945360126e-05
		deltaCp= 0.53202941758

	if Polymer_Type=='PVAc' and Polymer_Weight=='01kilo' and Reference=='Sandberg':
		A=2.6799e-09
		B=0.00287418
		Abelow=A
		Bbelow=B
		#Sandberg
		Aabove= 0.9714382629577871
		Babove= 0.0010954249673367222
		deltaCp= 0.404015404858

	if Polymer_Type=='PVAc' and Polymer_Weight=='01kilo' and Reference=='Roland':
		A=2.6799e-09
		B=0.00287418
		Abelow=A
		Bbelow=B
		#Roland
		Aabove= 0.9714382629577871
		Babove= 0.0010954249673367222
		deltaCp= 0.41824544512

	if Polymer_Type=='PVAc' and Polymer_Weight=='189kilo' and Reference=='Sandberg':
		A=-0.51533657
		B=0.00524197
		Abelow=A
		Bbelow=B
		#Sandberg
		Aabove= 1.0964144500072748
		Babove= 0.0015537737955917397
		deltaCp= 0.435216430801

	if Polymer_Type=='PVAc' and Polymer_Weight=='189kilo' and Reference=='Roland':
		A=3.5733199510445957e-08
		B=0.0035109342957952983
		Abelow=A
		Bbelow=B
		#Roland
		Aabove= 1.0964144500072748
		Babove= 0.0015537737955917397
		deltaCp= 0.487737498709

	if Polymer_Type=='PMMA' and Polymer_Weight=='44kilo' and Reference=='Grassia':
		A=3.6870e-11
		B=0.00551656
		Abelow=A
		Bbelow=B
		#Grassia
		Aabove= 1.213961491641069
		Babove= 0.0032988341670163734
		deltaCp= 0.433321998394

	if Polymer_Type=='PMMA' and Polymer_Weight=='44kilo' and Reference=='Olabisi':
		A=3.6870e-11
		B=0.00551656
		Abelow=A
		Bbelow=B
		#Olabisi
		Aabove= 1.213961491641069
		Babove= 0.0032988341670163734
		deltaCp= 0.375661126736

	if Polymer_Type=='PMMA' and Polymer_Weight=='140kilo' and Reference=='Grassia':
		A=3.6870e-11
		B=0.00390689
		Abelow=A
		Bbelow=B
		# Grassia
		Aabove= 0.34874011589845466
		Babove= 0.0036718353529252568
		deltaCp= 0.266000880091

	if Polymer_Type=='PMMA' and Polymer_Weight=='140kilo' and Reference=='Olabisi':
		A=3.6870e-11
		B=0.00390689
		Abelow=A
		Bbelow=B
		#Olabisi
		Aabove= 0.34874011589845466
		Babove= 0.0036718353529252568
		deltaCp= 0.259889459267

	if Polymer_Type=='PC' and Polymer_Weight=='00kilo':
		A=0.11396855
		B=0.00306293
		Abelow=A
		Bbelow=B
		Aabove= 0.9021031822167815
		Babove= 0.0017477994427264054
		deltaCp= 0.231308354267

	if Polymer_Type=='PC' and Polymer_Weight=='01kilo':
		A=8.4781e-11
		B=0.00336962
		Abelow=A
		Bbelow=B
		Aabove= 0.33744016581004943
		Babove= 0.002769897033872093
		deltaCp= 0.0835174618667

	if Polymer_Type=='PVME' and Polymer_Weight=='60kilo':
		A=0.35758515
		B=0.00280566
		Abelow=A
		Bbelow=B
		Aabove= 1.134414611630321
		Babove= 0.0017677152665089846
		deltaCp= 0.519834345618

	if Polymer_Type=='PS' and Polymer_Weight=='36kilo':
		A=3.6870e-11
		B=0.00372975
		Abelow=A
		Bbelow=B
		Aabove= 0.514699302779895
		Babove= 0.0031326703310323722
		deltaCp= 0.291391506549

	if Polymer_Type=='LPP' and Polymer_Weight=='15kilo' and Reference=='Hollander':
		A=0.28422214761473374
		B=0.003813324978954924
		Abelow=A
		Bbelow=B
		#Hollander
		Aabove= 0.7451911667351108
		Babove= 0.0039264439201676105
		deltaCp= 0.489384497154

	if Polymer_Type=='LPP' and Polymer_Weight=='15kilo' and Reference=='Passaglia':
		A=0.28422214761473374
		B=0.003813324978954924
		Abelow=A
		Bbelow=B
		#Passaglia
		Aabove= 0.7451911667351108
		Babove= 0.0039264439201676105
		deltaCp= 0.488513481307

	if Polymer_Type=='BPP' and Polymer_Weight=='15kilo' and Reference=='Hollander':
		A=0.29275405786160325
		B=0.003708909528818305
		Abelow=A
		Bbelow=B
		#Hollander
		Aabove= 0.7462812751196035
		Babove= 0.0038525661369011033
		deltaCp= 0.489613757208

	if Polymer_Type=='BPP' and Polymer_Weight=='15kilo' and Reference=='Passaglia':
		A=0.29275405786160325
		B=0.003708909528818305
		Abelow=A
		Bbelow=B
		#Passaglia
		Aabove= 0.7462812751196035
		Babove= 0.0038525661369011033
		deltaCp= 0.488507601325


	'''
	with open('DataSpecificHeat/240kilo_PS_TMCP.csv','rb') as csvfile:
		datareader = csv.reader(csvfile)
		#x0 = (float(column[1]) for column in datareader)
		index1 = 0
		index2 = 0
		for row in datareader:
			if index1 == 4:
				numpts = int(float(row[0]))
				T0_240K = range(0,numpts)
				M0_240K = range(0,numpts)
				C0_240K = range(0,numpts)
				P0_240K = range(0,numpts)
				I0_240K = range(0,numpts)
			if index1 >= 6:
				T0_240K[index2] = float(row[0])
				M0_240K[index2] = float(row[1])
				C0_240K[index2] = float(row[2])
				P0_240K[index2] = float(row[3])
				I0_240K[index2] = 'constant molar mass'
				index2 = index2 + 1
			index1 = index1 + 1

	T0 = npy.concatenate((T0,T0_240K),axis=0)
	M0 = npy.concatenate((M0,M0_240K),axis=0)
	C0 = npy.concatenate((C0,C0_240K),axis=0)
	P0 = npy.concatenate((P0,P0_240K),axis=0)
	I0 = npy.concatenate((I0,I0_240K),axis=0)

	with open('DataSpecificHeat/179kilo_PS_TMCP.csv','rb') as csvfile:
		datareader = csv.reader(csvfile)
		#x0 = (float(column[1]) for column in datareader)
		index1 = 0
		index2 = 0
		for row in datareader:
			if index1 == 4:
				numpts = int(float(row[0]))
				T0_179K = range(0,numpts)
				M0_179K = range(0,numpts)
				C0_179K = range(0,numpts)
				P0_179K = range(0,numpts)
				I0_179K = range(0,numpts)
			if index1 >= 6:
				T0_179K[index2] = float(row[0])
				M0_179K[index2] = float(row[1])
				C0_179K[index2] = float(row[2])
				P0_179K[index2] = float(row[3])
				I0_179K[index2] = 'constant molar mass'
				index2 = index2 + 1
			index1 = index1 + 1

	T0 = npy.concatenate((T0,T0_179K),axis=0)
	M0 = npy.concatenate((M0,M0_179K),axis=0)
	C0 = npy.concatenate((C0,C0_179K),axis=0)
	P0 = npy.concatenate((P0,P0_179K),axis=0)
	I0 = npy.concatenate((I0,I0_179K),axis=0)
	'''




	'''

	#======================================================
	#Loading PVT Data
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

	'''
	return Abelow,Bbelow,Aabove,Babove,A,B,deltaCp,T0_excluding_Tg,M0_excluding_Tg,C0_excluding_Tg,P0_excluding_Tg,I0_excluding_Tg,Tg0_excluding_Tg,T0_above_Tg,M0_above_Tg,C0_above_Tg,P0_above_Tg,I0_above_Tg,Tg0_above_Tg,T0_at_Tg,M0_at_Tg,C0_at_Tg,P0_at_Tg,I0_at_Tg,Tg0_at_Tg,T0_below_Tg,M0_below_Tg,C0_below_Tg,P0_below_Tg,I0_below_Tg,Tg0_below_Tg,T0_complete_Tg,M0_complete_Tg,C0_complete_Tg,P0_complete_Tg,I0_complete_Tg,Tg0_complete_Tg
