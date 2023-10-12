import numpy as np
import matplotlib.pyplot as plt


ELECTRON_CHARGE = 0.1
CG1 = 0.5
CG2 = 0.5
CL = 0.2
CR = 0.2
CM = 10 #1e-5
C1 = CL+CG1+CM
C2 = CR+CG2+CM

EC1 = ELECTRON_CHARGE**2/C1 * (1/(1-CM**2/(C1*C2)))
EC2 = ELECTRON_CHARGE**2/C2 * (1/(1-CM**2/(C1*C2)))
ECM = ELECTRON_CHARGE**2/CM * (1/(C1*C2/CM**2 - 1))

N = 4
print(f'C1 = {C1}, C2 = {C2}, CM = {CM}')
print(f'EC1 = {EC1}, EC2 = {EC2}, ECM = {ECM}')

def mu1(n1,n2, vg1, vg2):
    return (n1-0.5)*EC1 + n2*ECM - (CG1*vg1*EC1 + CG2*vg2*ECM)/ELECTRON_CHARGE

def mu2(n1, n2, vg1, vg2):
    return (n2-0.5)*EC2 + n1*ECM - (CG1*vg1*ECM + CG2*vg2*EC2)/ELECTRON_CHARGE


v1_1 = [] # v1 for type 1
v1_2 = [] # v1 for type 2
v2_1 = [] # v2 for type 1
v2_2 = [] # v2 for type 2

for A in range(0,N):
    for B in range(0,N):
        v11 = ELECTRON_CHARGE/CG1 * (A + EC2/2 * (EC1-ECM)/(EC1*EC2-ECM**2))
        v1_1.append(v11)
        v2_1.append((ELECTRON_CHARGE*((B+.5)*EC2 + A*ECM) - CG1*v11*ECM)/(CG2*EC2))

        if A == 0 or B == 0:
            continue
        v12 = ELECTRON_CHARGE/CG1 * (A + EC2/2 * (EC1-ECM)/(ECM**2-EC1*EC2))
        v1_2.append(v12)
        v2_2.append((ELECTRON_CHARGE*(A*ECM + (B-.5)*EC2) - CG1*v12*ECM)/(CG2*EC2))

print(mu1(0,0,v1_1[0], v2_1[0]))
print(mu2(0,0,v1_1[0], v2_1[0]))
print(mu1(1,1,v1_2[0], v2_2[0]))
print(mu2(1,1,v1_2[0], v2_2[0]))

plt.scatter(v1_1, v2_1, color='r', marker='o', label='type 1')
plt.scatter(v1_2, v2_2, color='b', marker='o', label='type 2')
plt.xlabel('Gate Voltage Dot 1')
plt.ylabel('Gate Voltage Dot 2')
plt.legend()
plt.show()

