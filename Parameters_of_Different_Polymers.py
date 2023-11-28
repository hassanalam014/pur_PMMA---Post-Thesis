#Sanchez-Lacombe parameters for the pure POLYMERS.

#======================================================
#Characteristic Parameters
#======================================================
# Pstar = [MPa]
# Tstar = [K]
# Rstar = [g/cm3]

#############################################################################################
# Polymer_Type='PVME' #PS or PMMA or DME or LPP or BPP or PLA or LDPE
# Reference='Roland'  #Condo or Kier
#############################################################################################

P_atm = 0.101325
M_infinity = 9E9
# global Pstar,Tstar,Rstar,Tg_atm,dTg_dP_atm,Pg_exp,Tg_exp,P_upper,T_upper


def Parameters_of_Different_Polymers(**kwargs):
	
    for key,value in kwargs.items():
		exec "%s='%s'" % (key,value)
    
    print 'Polymer Type', Polymer_Type, 'Referenced from', Reference

    if Polymer_Type=='PC' and Reference=='Zoller':
        # For PC Ref: Zoller Paper, A Studey of PVT Relationships of Four Related Amorphous Polymers
        Pstar = 574.4             #From huge List of SL EOS Parameters
        Tstar = 728.0             #From huge List of SL EOS Parameters
        Rstar = 1.2925            #From huge List of SL EOS Parameters

        #Experiment Data PC; Zoller Paper
        Tg_atm = 423.4           #Zoller Paper: Unit K
        dTg_dP_atm = 0.530        #Zoller Paper, Unit: K/MPa , Linear fit value upto 60MPa given by Zoller = 0.530  
        Pg_exp=[0.101325,9.7,19.9,29.7,39.5,49.1,59.3,69.3,79.1,89.1,98.9,108.7,118.7,128.5,137.9,147.9,157.9,167.9,177.3]
        Tg_exp=[423.4,429.3,433.4,436.8,444.5,450.8,455.5,459.6,464.8,469.5,472.8,475.8,481.0,484.3,486.9,490.0,490.4,494.9,496.3]
        #Do not take more data linear fit is until 60MPa
        P_upper=59.3
        T_upper=455.5
    
    if Polymer_Type=='PVAc' and Reference=='Sandberg':
        # For PVAc Ref: Roland Paper, Dynamic properties of polyvinylmethylether near the glass transition
        Pstar = 504.2             #From huge List of SL EOS Parameters
        Tstar = 592.0             #From huge List of SL EOS Parameters
        Rstar = 1.2822            #From huge List of SL EOS Parameters

        #Experiment Data PVAc; Sandberg Paper #This data does not seems right to me. Shifted by 10K.
        Tg_atm = 319.0           #Sandberg Paper: Unit K
        dTg_dP_atm = 0.264        #Sandberg Paper, Unit: K/MPa, in low P limit. So take only low pressure values, linear fit value upto 80 MPa.   
        Pg_exp=[0.101325,26.142,79.299,162.381,241.831,353.225,493.251]
        Tg_exp=[319.0,325.53,338.30,355.91,370.70,388.63,407.90]
        #Take only low pressure values. Data has curvature.   
        P_upper=162.381
        T_upper=355.91


    if Polymer_Type=='PVAc' and Reference=='Roland':
        # For PVAc Ref: Roland Paper, Dynamic properties of polyvinylmethylether near the glass transition
        Pstar = 504.2             #From huge List of SL EOS Parameters
        Tstar = 592.0             #From huge List of SL EOS Parameters
        Rstar = 1.2822            #From huge List of SL EOS Parameters
        #Use Experiment Data PVAc; Roland Paper
        Tg_atm = 311.0           #Roland Paper: Unit K
        dTg_dP_atm = 0.216     #My value=0.216 upto 150MPa,     #Roland Paper value is 0.25 in limit of P=0, Unit: K/MPa
        #Experiment Data PVAc; Roland Paper
        Pg_exp=[0.101325,50.0,100.0,150.0,200.0,250.0,300.0,350.0,400.0]
        Tg_exp=[311.0,323.0,333.0,343.5,351.5,359.5,366.5,373.5,380.0]
        #My slope value=0.216 upto 150MPa
        P_upper=150.0
        T_upper=343.5


    if Polymer_Type=='PVME' and Reference=='Casalini':
        # For PVME Ref: Casalini Paper, Dynamic properties of polyvinylmethylether near the glass transition
        Pstar = 463.0             #From huge List of SL EOS Parameters
        Tstar = 567.0             #From huge List of SL EOS Parameters
        Rstar = 1.1198            #From huge List of SL EOS Parameters
        Tg_atm = 247.60           #Casalini Paper: Unit K
        dTg_dP_atm = 0.149 #My Value=0.149 upto 180MPa      #Casalini Paper=0.177 in P=0 limit, Unit: K/MPa

        #Experiment Data PVME; Casalini Paper
        #Curve has significant curvature even at low values of pressure
        Pg_exp=[0.101325,50.16,111.50,177.70,249.75,309.13,375.32,441.51,497.96,556.36,622.55,657.59,687.76]
        Tg_exp=[247.60,256.22,265.21,274.08,282.69,289.25,296.19,302.48,307.49,312.12,317.64,320.34,322.40]

        # Pg_exp=[0.101325,250,375,690]
        # Tg_exp=[247.6,282.5,296.0,322.5]
        #Curve has significant curvature even at low values of pressure
        P_upper=177.70
        T_upper=274.08


    if Polymer_Type=='PS' and Reference=='Quach':
        # For PS Ref: Quach Paper
        Pstar = 357.0
        Tstar = 735.0
        Rstar = 1.105
        Tg_atm = 374.0          #Ref[54] of Quach Paper: Unit K
        dTg_dP_atm = 0.316       #Value in Paper: 0.316      #Ref[54] of Quach Paper, Unit: K/MPa   

        #Experiment Data PS; Quach Ref [54]
        Pg_exp=[0.101325,40,60,80,120,160]
        Tg_exp=[374.0,388.4,392.7,402.8,413.2,428.8]
        P_upper=160.0
        T_upper=428.8


    if Polymer_Type=='PMMA' and Reference=='Grassia':
        # For P*T*R* are from Condo Paper
        Pstar = 503.0
        Tstar = 696.0
        Rstar = 1.269
        Tg_atm = 352.0             
        dTg_dP_atm = 0.3      #Given Value in Paper is: 0.3        #Unit: K/MPa, "It is straight line fit" upto 150MPa

        #Experiment Data PMMA; Luigi Grassia: Isobaric and isothermal glass transition of PMMA
        Pg_exp=[0.101325,10.0,30.0,60.0,80.0,100.0,120.0,150.0]
        Tg_exp=[352.0,356.0,363.5,373.0,379.5,385.0,390.0,397.5]
        P_upper=150.0
        T_upper=397.5


    if Polymer_Type=='PMMA' and Reference=='Olabisi':
        # For PMMA Ref: Olabisi Paper
        Pstar = 503.0
        Tstar = 696.0
        Rstar = 1.269
        Tg_atm = 378.0              #Ref[53] of Olabisi Paper
        dTg_dP_atm = 0.236          #Ref[53] of Olabisi Paper, Unit: K/MPa

        #Experiment Data PMMA; Olabisi Ref [53]
        Pg_exp=[0.101325,30,40,80,120,140,180]
        Tg_exp=[378.0,386.5,386.5,397.5,408.1,408.1,419.7]
        P_upper=180.0
        T_upper=419.7


    if Polymer_Type=='BPP' and Reference=='Hollander':
        # For Brached PP Ref: Kier 
        Pstar = 356.4 
        Tstar = 656.0 
        Rstar = 0.8950 
        Tg_atm = 251.2          #Ref: Actactic PP at High Pressure. Deturon NMR of Glass Temp; Hollander 2001 
        dTg_dP_atm = 0.158      #My Value=0.158 upto 100.4MPa   #In P=0 limit value is given to be 0.158   #Ref: Actactic PP at High Pressure. Deturon NMR of Glass Temp; Hollander 2001 
    
        #Experiment Data PP; Ref: Actactic PP at High Pressure. Deturon NMR of Glass Temp; Hollander 2001
        Pg_exp=[0.101325,0.4,50.5,100.4,199.5,500.3]
        Tg_exp=[251.2,250.0,262.0,267.0,279.0,311.0]
        #My slope value=0.158 upto 100.4MPa 
        P_upper=100.4
        T_upper=267.0


    if Polymer_Type=='BPP' and Reference=='Passaglia':
        # For Brached PP Ref: Kier 
        Pstar = 356.4 
        Tstar = 656.0 
        Rstar = 0.8950 
        Tg_atm = 243.5        #Ref: "Variation of Glass Temperature With Pressure in Polypropylene,Passaglia,1962"
        dTg_dP_atm = 0.204    #Note:It is straight line fit slope on whole data    #Ref: "Variation of Glass Temperature With Pressure in Polypropylene,Passaglia,1962"
        #Experiment Data Linear Polypropylene; Ref: "Variation of Glass Temperature With Pressure in Polypropylene,Passaglia,1962"
        Pg_exp=[0.101325,15,30,40,50,70]
        Tg_exp=[243.5,249.0,251.3,252.3,254.0,258.3]
        P_upper=70.0
        T_upper=258.3

    if Polymer_Type=='LPP' and Reference=='Hollander':
        # For Linear PP Ref: Kier 
        Pstar = 316.2 
        Tstar = 662.8 
        Rstar = 0.8685
        Tg_atm = 251.2          #Ref: Actactic PP at High Pressure. Deturon NMR of Glass Temp; Hollander 2001 
        dTg_dP_atm = 0.158      #My Value=0.158 upto 100.4MPa   #In P=0 limit value is given to be 0.158   #Ref: Actactic PP at High Pressure. Deturon NMR of Glass Temp; Hollander 2001 
    
        #Experiment Data PP; Ref: Actactic PP at High Pressure. Deturon NMR of Glass Temp; Hollander 2001
        Pg_exp=[0.101325,0.4,50.5,100.4,199.5,500.3]
        Tg_exp=[251.2,250.0,262.0,267.0,279.0,311.0]
        #My slope value=0.158 upto 100.4MPa 
        P_upper=100.4
        T_upper=267.0

    if Polymer_Type=='LPP' and Reference=='Passaglia':
        # For Linear PP Ref: Kier 
        Pstar = 316.2 
        Tstar = 662.8 
        Rstar = 0.8685
        Tg_atm = 243.5        #Ref: "Variation of Glass Temperature With Pressure in Polypropylene,Passaglia,1962"
        dTg_dP_atm = 0.204    #Note:It is straight line fit slope on whole data    #Ref: "Variation of Glass Temperature With Pressure in Polypropylene,Passaglia,1962"
        #Experiment Data Linear Polypropylene; Ref: "Variation of Glass Temperature With Pressure in Polypropylene,Passaglia,1962"
        Pg_exp=[0.101325,15,30,40,50,70]
        Tg_exp=[243.5,249.0,251.3,252.3,254.0,258.3]
        P_upper=70.0
        T_upper=258.3
    
    if Polymer_Type=='PS' and Reference=='Kier':
        # For PS Ref: Kier 
        Pstar = 421.8 
        Tstar = 687.8 
        Rstar = 1.118
        Tg_atm = 374.0         #Ref[54] of Condo Paper: Unit K
        dTg_dP_atm = 0.316     #Ref[54] of Condo Paper: Unit K/MPa
        
        #Experiment Data PS; Condo Ref [54]
        Pg_exp=[0.101325,40,60,80,120,160]
        Tg_exp=[373.0,388.4,392.7,402.8,413.2,428.8]
        P_upper=160.0

    if Polymer_Type=='DME' and Reference=='Kier':
        # For DME Ref: Kier 
        Pstar = 313.8 
        Tstar = 450.0 
        Rstar = 0.8146 
        Tg_atm = 1.0
        dTg_dP_atm = 0.0

    if Polymer_Type=='LDPE' and Reference=='Kier':
        # For Low Density PE Ref: Kier 
        Pstar = 407.5 
        Tstar = 586.6 
        Rstar = 0.9271
        Tg_atm = 1.0
        dTg_dP_atm = 0.0

    if Polymer_Type=='PLA' and Reference=='Kier':
        # For PLA Ref: Kier 
        Pstar = 598.4 
        Tstar = 617.3 
        Rstar = 1.347
        Tg_atm = 1.0
        dTg_dP_atm = 0.0

    return (Pstar,Tstar,Rstar,Tg_atm,dTg_dP_atm,Pg_exp,Tg_exp,P_upper,T_upper)
