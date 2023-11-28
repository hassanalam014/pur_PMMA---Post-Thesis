#Sanchez-Lacombe parameters for the pure POLYMER.

#======================================================
#Characteristic or Molecular Parameters
#======================================================
from __future__ import division
GLi_Pstar = 407.4
GLi_Tstar = 739.1
GLi_Rstar = 1.108

#Full range including glass transition.
# Self_Pstar = 249.943441
# Self_Tstar = 665.399415
# Self_Rstar = 1.09659744

#Only from 402K and up.
Self_Pstar = 421.762455
Self_Tstar = 687.788143
Self_Rstar = 1.11768655

#For M=34500 Data2
# Self_Pstar = 441.228
# Self_Tstar = 683.193
# Self_Rstar = 1.1176

#My values
#Self_Pstarstar= 4236.99551
#Self_Tstarstar= 3259.82974
#Self_Rstarstar= 6.39600739
#Against Full Range of P* T* R* paramters:
# Self_Pstarstar= 8737.82469
# Self_Tstarstar= 5924.59463
# Self_Rstarstar= 5.40346613

#Random Values
# Self_Pstar = 850.762455
# Self_Tstar = 665.788143
# Self_Rstar = 1.11768655
# Self_Pstarstar= 1.782469
# Self_Tstarstar= 0
# Self_Rstarstar= 1110

'''
Fitted Data:

Below Tg:

    Fitting Base Curve:

    A:      1.9071e-08 +/- 0.03693046 (193643806.43%) (init = 0.03)
    B:      0.00357274 +/- 1.4912e-04 (4.17%) (init = 0.00438658)
    Pstar:  421.7625 (fixed)
    Tstar:  687.7881 (fixed)
    Rstar:  1.117687 (fixed)
    Pc0:    0.001 (fixed)
    Tc0:    265 (fixed)
    Rc0:    0.0001 (fixed)
    [[Correlations]] (unreported correlations are < 0.100)
    C(A, B) = -0.999


    Fitting At Glass Transition:

    A:          1.907134e-08 (fixed)
    B:          0.003572742 (fixed)
    Pstarstar:  0.00174380 +/- 4.4316e-04 (25.41%) (init = 0.00051759)
    Tstarstar:  10.6147737 +/- 0.85946526 (8.10%) (init = 6.518)
    Rstarstar:  6.9976e+46 +/- 7.8490e+47 (1121.67%) (init = 6.5113e+60)
    Pstar:      421.7625 (fixed)
    Tstar:      687.7881 (fixed)
    Rstar:      1.117687 (fixed)
    Pc0:        0.001 (fixed)
    Tc0:        265 (fixed)
    Rc0:        0.0001 (fixed)
    [[Correlations]] (unreported correlations are < 0.100)
    C(Pstarstar, Tstarstar) =  0.972
    C(Pstarstar, Rstarstar) = -0.931
    C(Tstarstar, Rstarstar) = -0.820

Above Tg:

    Fitting Base Curve:

    [[Variables]]
    A:      0.47472309 +/- 0.05158951 (10.87%) (init = 0.03)
    B:      0.00302384 +/- 1.2342e-04 (4.08%) (init = 0.003392431)
    Pstar:  421.7625 (fixed)
    Tstar:  687.7881 (fixed)
    Rstar:  1.117687 (fixed)
    Pc0:    0.001 (fixed)
    Tc0:    265 (fixed)
    Rc0:    0.0001 (fixed)
    [[Correlations]] (unreported correlations are < 0.100)
    C(A, B) = -0.997

    Fitting At Glass Transition:

   [[Variables]]
    A:          0.4747231 (fixed)
    B:          0.003023843 (fixed)
    Pstarstar:  1.2855e-05 +/- 3.3140e-05 (257.81%) (init = 5.2504e-05)
    Tstarstar:  1.58456913 +/- 1.47814620 (93.28%) (init = 2.762495)
    Rstarstar:  3.999e+141 +/- 1.156e+144 (28910.43%) (init = 2.333e+105)
    Pstar:      421.7625 (fixed)
    Tstar:      687.7881 (fixed)
    Rstar:      1.117687 (fixed)
    Pc0:        0.001 (fixed)
    Tc0:        265 (fixed)
    Rc0:        0.0001 (fixed)
    [[Correlations]] (unreported correlations are < 0.100)
    C(Pstarstar, Tstarstar) =  0.965
    C(Pstarstar, Rstarstar) = -0.845
    C(Tstarstar, Rstarstar) = -0.675

Exlucing Tg:

    Fitting Base Curve:

    [[Variables]]
    A:      3.3632e-10 (init = 0.03)
    B:      0.00399243 (init = 0.00438658)
    Pstar:  421.7625 (fixed)
    Tstar:  687.7881 (fixed)
    Rstar:  1.117687 (fixed)
    Pc0:    0.001 (fixed)
    Tc0:    265 (fixed)
    Rc0:    0.0001 (fixed)
    
    Fitting Glass Transition:

    [[Variables]]
    A:          3.363225e-10 (fixed)
    B:          0.003992431 (fixed)
    Pstarstar:  1.7274e-04 +/- 1.0891e-04 (63.05%) (init = 0.0017438)
    Tstarstar:  4.36981412 +/- 0.91336827 (20.90%) (init = 10.61477)
    Rstarstar:  1.3155e+80 +/- 6.4001e+81 (4865.26%) (init = 6.9976e+46)
    Pstar:      421.7625 (fixed)
    Tstar:      687.7881 (fixed)
    Rstar:      1.117687 (fixed)
    Pc0:        0.001 (fixed)
    Tc0:        265 (fixed)
    Rc0:        0.0001 (fixed)
    [[Correlations]] (unreported correlations are < 0.100)
    C(Pstarstar, Tstarstar) =  0.953
    C(Pstarstar, Rstarstar) = -0.877
    C(Tstarstar, Rstarstar) = -0.690
'''