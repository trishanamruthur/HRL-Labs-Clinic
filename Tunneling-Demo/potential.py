import numpy as np

class GatePotential:
    def __init__(self, gate_width, dot_width, gap, V1, VP, V2, VD, V0=0, depth=50e-9, height=1, inf=1e5):
        # set all of the variables
        self.gate_width = gate_width
        self.dot_width = dot_width
        self.height = height
        self.gap = gap
        self.V1 = V1
        self.VP = VP
        self.V2 = V2
        self.VD = VD
        self.V0 = V0
        self.inf = inf
        self.depth = depth

    @staticmethod
    def g(u, v, d):
        ''' g function (equation 3.12 in the davies paper) '''
        R = np.sqrt(u**2 + v**2 + d**2)
        return 1/(2*np.pi) * np.arctan(u*v/(d*R))

    @staticmethod
    def phi_rect(x, y, d, Vg, L, R, B, T):
        ''' phi equation (3.11, davies paper)'''
        return Vg*(GatePotential.g(x-L, y-B, d) + GatePotential.g(x-L, T-y, d) + GatePotential.g(R-x, y-B, d) + GatePotential.g(R-x, T-y, d))

    def __call__(self, x, y=0):
        ''' returns the potential for a gate structure '''
        out = 0
        # first rectangle is T=+inf, B=-inf, L=-inf, R=0
        out += GatePotential.phi_rect(x, y, self.depth, self.V0, -self.inf, 0, -self.inf, self.inf)
        # V1: L = gap, R = gate_width+gap
        out += GatePotential.phi_rect(x, y, self.depth, self.V1, self.gap, self.gate_width+self.gap, -self.height/2, self.height/2)
        # Vp: L = gate_width+2gap, R = gate_width+2gap+dot_width
        out += GatePotential.phi_rect(x, y, self.depth, self.VP, self.gate_width + 2*self.gap, self.gate_width + 2*self.gap+self.dot_width, -self.height/2, self.height/2)
        #V2: L = gate_width+3gap+dot_width, R = 2*gate_width+3gap+dot_width
        out += GatePotential.phi_rect(x, y, self.depth, self.V2, self.gate_width + 3*self.gap + self.dot_width, 2*self.gate_width + 3*self.gap + self.dot_width, -self.height/2, self.height/2)
        #Vd: L=2*gate_width+4gap+dot_width, R=inf
        out += GatePotential.phi_rect(x,y,self.depth,self.VD,2*self.gate_width + 4*self.gap + self.dot_width, self.inf, -self.inf, self.inf)
        # return the potential accounting for all gates
        return out

# testing
if __name__ == '__main__':
    import matplotlib.pyplot as plt

    xs = np.linspace(-300e-9, 500e-9, 10000)
    ys = np.zeros_like(xs)

    phi = GatePotential(50e-9, 90e-9, 10e-9, 1e-3, -1e-3, 1e-3, -1e-5)

    for i, x in enumerate(xs):
        ys[i] = phi(x, 0, 50e-9)
    
    # plot the gates
    # plt.plot([-150e-9, 0], [0, 0], color='r')
    # plt.plot([gap, gate_width+gap], [0, 0], color='r')
    # plt.plot([gate_width+2*gap, gate_width+2*gap+dot_width], [0, 0], color='r')
    # plt.plot([gate_width+3*gap+dot_width, 2*gate_width+3*gap+dot_width], [0, 0], color='r')
    # plt.plot([2*gate_width+4*gap+dot_width, 400e-9], [0, 0], color='r')

    plt.plot(xs, ys)
    plt.xlabel('x position')
    plt.ylabel('Potential (V)')
    plt.show()



