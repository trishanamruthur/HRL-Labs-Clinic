
import numpy as np
import math
from scipy.optimize import fsolve
from scipy import constants

ENERGY = some value constant
VOLTAGE_X1 
VOLTAGE_X2
VOLTAGE_P
VOLTAGE_DRAIN
MASS

K_0 = math.sqrt(2*MASS*ENERGY)/constants.hbar
K_1 = math.sqrt(2*MASS(ENERGY - VOLTAGE_X1))/constants.hbar
K_P = math.sqrt(2*MASS(ENERGY - VOLTAGE_P))/constants.hbar
K_2 = math.sqrt(2*MASS(ENERGY - VOLTAGE_X2))/constants.hbar
K_D = math.sqrt(2*MASS(ENERGY - VOLTAGE_DRAIN))/constants.hbar


def equations(eqn):
    a,b,c,d,e,f,g,h,i, x_1, x_2, x_3 = eqn
    eqn_1 = a+b-c-d

    eqn_2 = j*K_0(a-b)-j*K_1(c-d)

    eqn_3 = c*math.exp(j*K_1*x_1)+ d*math.exp(-j*K_1*x_1)-e*math.exp(j*K_P*x_1)-f*math.exp(-j*K_P*x_1)
    
    eqn_4 = j*K_1*(c*math.exp(j*K_1*x_1)- d*math.exp(-j*K_1*x_1)) - j*K_P*(c*math.exp(j*K_P*x_1)- d*math.exp(-j*K_P*x_1))

    eqn_5 = e*math.exp(j*K_P*x_2)+f*math.exp(-j*K_P*x_2)- g*math.exp(j*K_2)

    eqn_6 = j*K_P*(e*math.exp(j*K_P*x_2)- f*math.exp(-j*K_P*x_2)) - j*K_2*(g*math.exp(j*K_2*x_2)- h*math.exp(-j*K_2*x_2))
