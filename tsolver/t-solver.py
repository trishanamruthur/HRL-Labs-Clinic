
import numpy as np
import math
from scipy.optimize import minimize
from scipy import constants
from mpmath import findroot
from scipy import integrate

ENERGY = 1 #some value constant
VOLTAGE_X1 = 2
VOLTAGE_X2 = 1.5
VOLTAGE_P = -0.5
VOLTAGE_DRAIN = -0.25
MASS = constants.electron_mass
HBAR = constants.hbar

K_0 = (2*MASS*ENERGY)**(0.5)/HBAR
K_1 = (2*MASS*(ENERGY - VOLTAGE_X1))**(0.5)/HBAR
K_P = (2*MASS*(ENERGY - VOLTAGE_P))**(0.5)/HBAR
K_2 = (2*MASS*(ENERGY - VOLTAGE_X2))**(0.5)/HBAR
K_D = (2*MASS*(ENERGY - VOLTAGE_DRAIN))**(0.5)/HBAR

X_1 = 1
X_2 = 2
X_3 = 3

A=1

def equations(eqn):
    b,c,d,e,f,g,h,i= eqn
    eqn_1 = A+b-c-d

    eqn_2 = (0+1j)*K_0*(A-b)-1j*K_1*(c-d)

    eqn_3 = c*np.exp(1j*K_1*X_1)+ d*np.exp(-1j*K_1*X_1)-e*np.exp(1j*K_P*X_1)-f*np.exp(-1j*K_P*X_1)
    
    eqn_4 = 1j*K_1*(c*np.exp(1j*K_1*X_1)- d*np.exp(-1j*K_1*X_1)) - 1j*K_P*(e*np.exp(1j*K_P*X_1)- f*np.exp(-1j*K_P*X_1))

    eqn_5 = e*np.exp(1j*K_P*X_2)+f*np.exp(-1j*K_P*X_2)- g*np.exp(1j*K_2) -h*np.exp(1j*K_2*X_2)

    eqn_6 = 1j*K_P*(e*np.exp(1j*K_P*X_2)- f*np.exp(-1j*K_P*X_2)) - 1j*K_2*(g*np.exp(1j*K_2*X_2)- h*np.exp(-1j*K_2*X_2))

    eqn_7 = g*np.exp(1j*K_2*X_3)+h*np.exp(-1j*K_2*X_3) - i*np.exp(1j*K_D*X_3)
    
    eqn_8 = 1j*K_2*(g*np.exp(1j*K_2*X_3) - h*np.exp(-1j*K_2*X_3)) - 1j*K_D*(i*np.exp(1j*K_D*X_3))

    x = np.array([eqn_1, eqn_2, eqn_3, eqn_4, eqn_5, eqn_6, eqn_7, eqn_8])
    return np.linalg.norm(x)**2

# ans = minimize(equations, x0=np.ones(8)*1e-5)


def eqn_1(b,c,d,e,f,g,h,i):
    return A+b-c-d

def eqn_2(b,c,d,e,f,g,h,i):
    return (0+1j)*K_0*(A-b)-1j*K_1*(c-d)

def eqn_3(b,c,d,e,f,g,h,i):
    return c*np.exp(1j*K_1*X_1)+ d*np.exp(-1j*K_1*X_1)-e*np.exp(1j*K_P*X_1)-f*np.exp(-1j*K_P*X_1)

def eqn_4(b,c,d,e,f,g,h,i):
    return 1j*K_1*(c*np.exp(1j*K_1*X_1)- d*np.exp(-1j*K_1*X_1)) - 1j*K_P*(e*np.exp(1j*K_P*X_1)- f*np.exp(-1j*K_P*X_1))

def eqn_5(b,c,d,e,f,g,h,i):
    return e*np.exp(1j*K_P*X_2)+f*np.exp(-1j*K_P*X_2)- g*np.exp(1j*K_2) -h*np.exp(1j*K_2*X_2)

def eqn_6(b,c,d,e,f,g,h,i):
    return 1j*K_P*(e*np.exp(1j*K_P*X_2)- f*np.exp(-1j*K_P*X_2)) - 1j*K_2*(g*np.exp(1j*K_2*X_2)- h*np.exp(-1j*K_2*X_2))

def eqn_7(b,c,d,e,f,g,h,i):
    return g*np.exp(1j*K_2*X_3)+h*np.exp(-1j*K_2*X_3) - i*np.exp(1j*K_D*X_3)

def eqn_8(b,c,d,e,f,g,h,i):
    return 1j*K_2*(g*np.exp(1j*K_2*X_3) - h*np.exp(-1j*K_2*X_3)) - 1j*K_D*(i*np.exp(1j*K_D*X_3))

ans = findroot([eqn_1, eqn_2, eqn_3, eqn_4, eqn_5, eqn_6, eqn_7, eqn_8], (1,1,1,1,1,1,1,1))
print(ans)
# print(equations((np.ones(8)*1e-5)))
# print(np.exp(1j*K_D*3))
# print(np.abs(i)**2)


def wkb_approx(v_eqn, energy, a):
    integrand_real = lambda x: (np.sqrt((2*constants.electron_mass*(v_eqn-energy))/(constants.hbar)**2)).real
    integrand_imag = lambda x: (np.sqrt((2*constants.electron_mass*(v_eqn-energy))/(constants.hbar)**2)).imag
    integral = integrate.quad(integrand_real,0, a) + 1j*integrate.quad(integrand_imag, 0, a)
    tunneling_rate = np.exp(-2*integral)
    return tunneling_rate

