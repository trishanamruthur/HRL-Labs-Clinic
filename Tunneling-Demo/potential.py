import numpy as np

def g(u, v, d):
    ''' g function (equation 3.12 in the davies paper) '''
    R = np.sqrt(u**2 + v**2 + d**2)
    return 1/(2*np.pi) * np.arctan(u*v/(d*R))


def phi_rect(x, y, d, Vg, L, R, B, T):
    ''' phi equation (3.11, davies paper)'''
    return Vg*(g(x-L, y-B, d) + g(x-L, T-y, d) + g(R-x, y-B, d) + g(R-x, T-y, d))

def phi_gates(x, y, d, V1, Vp, V2, Vd, gate_width, dot_width, gap=0, gate_height=1, V0=0, inf=1e5):
    ''' returns the potential for a gate structure '''
    phi = 0
    # first rectangle is T=+inf, B=-inf, L=-inf, R=0
    phi += phi_rect(x, y, d, V0, -inf, 0, -inf, inf)
    # V1: L = gap, R = gate_width+gap
    phi += phi_rect(x, y, d, V1, gap, gate_width+gap, -gate_height/2, gate_height/2)
    # Vp: L = gate_width+2gap, R = gate_width+2gap+dot_width
    phi += phi_rect(x,y,d,Vp, gate_width + 2*gap, gate_width + 2*gap+dot_width, -gate_height/2, gate_height/2)
    #V2: L = gate_width+3gap+dot_width, R = 2*gate_width+3gap+dot_width
    phi += phi_rect(x, y, d, V2, gate_width + 3*gap + dot_width, 2*gate_width + 3*gap + dot_width, -gate_height/2, gate_height/2)
    #Vd: L=2*gate_width+4gap+dot_width, R=inf
    phi += phi_rect(x,y,d,Vd,2*gate_width + 4*gap + dot_width, inf, -inf, inf)
    # return the potential accounting for all gates
    return phi



# testing
if __name__ == '__main__':
    import matplotlib.pyplot as plt

    xs = np.linspace(-150e-9, 400e-9, 500)
    ys = np.zeros_like(xs)

    gate_width, dot_width = 50e-9, 90e-9
    gap = 10e-9
    for i, x in enumerate(xs):
        ys[i] = phi_gates(x, 0, 50e-9, 1e-3, -1e-3, 1e-3, -0.1e-3, gate_width, dot_width, gap=gap)
    
    # plot the gates
    plt.plot([-150e-9, 0], [0, 0], color='r')
    plt.plot([gap, gate_width+gap], [0, 0], color='r')
    plt.plot([gate_width+2*gap, gate_width+2*gap+dot_width], [0, 0], color='r')
    plt.plot([gate_width+3*gap+dot_width, 2*gate_width+3*gap+dot_width], [0, 0], color='r')
    plt.plot([2*gate_width+4*gap+dot_width, 400e-9], [0, 0], color='r')

    plt.plot(xs, ys)
    plt.xlabel('x position')
    plt.ylabel('Potential (V)')
    plt.show()



