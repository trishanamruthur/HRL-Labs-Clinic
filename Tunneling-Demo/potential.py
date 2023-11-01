import numpy as np

class RectGate:
    ''' Defines the geometry of a rectangular gate which can be called upon later to produce a potential when supplied with a voltage. '''
    def __init__(self, x, y, width, height, voltage=0):
        self.pos = np.array([x,y,0])
        self.width = width
        self.height = height
        self.L = x - width/2
        self.R = x + width/2
        self.B = y - height/2
        self.T = y + height/2
        self.V = voltage

    @staticmethod
    def from_edges(left, right, bottom, top, voltage=0):
        ''' Construct a rectangular gate by defining the left, right, bottom, and top edges. '''
        return RectGate((left + right)/2, (bottom+top)/2, right-left, top-bottom, voltage=voltage)
    
    @staticmethod
    def g(u, v, d):
        ''' g(u,v) function from the paper '''
        r = np.sqrt(u**2 + v**2 + d**2)
        return 1/(2*np.pi) * np.arctan(u*v/(d*r))

    def __call__(self, x, y, d):
        ''' returns the potential from this gate at a position (x,y,-d) when this gate is held at a voltage V '''
        return self.V*(
            RectGate.g(x - self.L, y - self.B, d) + 
            RectGate.g(x - self.L, self.T - y, d) + 
            RectGate.g(self.R - x, y - self.B, d) + 
            RectGate.g(self.R - x, self.T - y, d))

    def set_voltage(self, voltage):
        self.V = voltage

    def __repr__(self):
        return f'RectGate({self.L} < x < {self.R}, {self.B} < y < {self.T}, V={self.V})'

class GateGeometry:
    ''' Defines a geometry of multiple gates '''
    def __init__(self, source_bath_x, drain_bath_x, source_voltage=0, drain_voltage=-1e-3, inf=1e5,  gates={}, depth=50e-9):
        self.source = RectGate(source_bath_x - inf/2, 0, inf, inf, voltage=source_voltage)
        self.drain = RectGate(drain_bath_x + inf/2, 0, inf, inf, voltage=drain_voltage)
        self.inf = inf # value of infinity
        self._gates = gates # dictionary of 'gate name': (gate, voltage)
        self._gates['S'] = self.source
        self._gates['D'] = self.drain
        self._depth = depth # default depth for call

    # +++ BUILT IN +++

    def __repr__(self):
        return self._gates.__repr__()

    def __getitem__(self, key):
        return self._gates[key]
    
    def __call__(self, x, y, depth=None):
        # set depth
        if depth is None: depth = self._depth
        # sum contributions of each gate
        out = 0
        for name in self.gate_names:
            out += self._gates[name](x, y, depth)
        return out

    # +++ PROPERTIES +++

    @property
    def gate_names(self):
        return list(self._gates)
    
    # +++ METHODS +++

    def add_gate(self, name, gate):
        ''' Add a gate to the geometry. '''
        self._gates[name] = gate

def alternating_spacing(num_dots, dot_width, gate_width, height, gap=0, dot_voltage=0, gate_voltage=0, source_voltage=0, drain_voltage=-1e-3):
    total_width = num_dots * dot_width + (num_dots + 1) * gate_width + (2 * num_dots + 2) * gap
    # length between the center of the dots on either side
    total_dots_length = total_width - 2 * gate_width - 4 * gap - dot_width
    # length between the center of the gates on either side
    total_gates_width = total_width - 2 * gap - gate_width
    # initialize the geometry with the baths
    geo = GateGeometry(-total_width/2, total_width/2, source_voltage, drain_voltage)
    # loop to construct dots
    for i in range(num_dots):
        x = total_dots_length * (i/(num_dots-1) - 0.5)
        geo.add_gate(f'P{i}', RectGate(x, 0, dot_width, height, voltage=dot_voltage))
    # loop to construct dots
    for i in range(num_dots+1):
        x = total_gates_width * (i/num_dots - 0.5)
        geo.add_gate(f'X{i}', RectGate(x, 0, gate_width, height, voltage=gate_voltage))
    # return the populated geometry    
    return geo

if __name__ == '__main__':
    g = alternating_spacing(3, 5, 2, 4, gap=1, dot_voltage=-0.002, gate_voltage=0.001)
