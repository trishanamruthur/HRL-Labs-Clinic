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
        # list of linked gates
        self._linked = []

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
        # update linked gates
        for gate in self._linked:
            gate.set_voltage(voltage)

    def link(self, gate):
        self._linked.append(gate)
    
    def unlink(self, gate):
        self._linked.remove(gate)

    def __repr__(self):
        return f'RectGate({self.L} < x < {self.R}, {self.B} < y < {self.T}, V={self.V})'

class GateGeometry:
    ''' Defines a geometry of multiple gates. '''
    def __init__(self, gates={}, depth=50e-9):
        self._gates = gates # dictionary of 'gate name': (gate, voltage)
        self._depth = depth # default depth for call
        self._sx, self._dx = None, None # source and drain x positions

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
        ''' List of the names of each gate in this geometry. '''
        return list(self._gates)
    
    @property
    def width(self) -> 'Union[float, None]':
        ''' Returns the width of the geometry - i.e. the distance between the source and drain gates. '''
        if self._sx is None or self._dx is None:
            return None
        else:
            return self._dx - self._sx
    
    # +++ METHODS +++

    def add_gate(self, name:str, gate) -> None:
        ''' Add a gate to the geometry.
        
        Parameters
        ----------
        name : str
            Name of the gate.
        gate : Any
            The gate object to be added.
        '''
        self._gates[name] = gate

    def add_source_and_drain(self, source_x:float, drain_x:float, source_voltage:float=0, drain_voltage:float=-1e-3, inf:float=1e5, y_offset:float=0):
        ''' Add source and drain gates to the geometry.
        
        The source gate is bounded by (-inf, source_x) in the x direction and (-inf+y_offset, inf+y_offset) in the y direction. The drain gate is bounded by (drain_x, inf) in the x direction and (-inf+y_offset, inf+y_offset) in the y direction. The source and drain gates are assigned the keys 'S' and 'D', respectively.

        Parameters
        ----------
        source_x : float
            The x position of the source gate.
        drain_x : float
            The x position of the drain gate.
        source_voltage : float (default=0)
            The voltage of the source gate.
        drain_voltage : float (default=-1e-3)
            The voltage of the drain gate.
        inf : float (default=1e5)
            The infinity value for the gate.
        y_offset : float (default=0)
            The y offset of the source and drain gates.
        '''
        # create source and drain
        s = RectGate.from_edges(-inf, source_x, -inf+y_offset, inf+y_offset, voltage=source_voltage)
        d = RectGate.from_edges(drain_x, inf, -inf+y_offset, inf+y_offset, voltage=drain_voltage)
        # add the gates
        self.add_gate('S', s)
        self.add_gate('D', d)
        # update internal variables
        self._sx, self._dx = source_x, drain_x

    def add_alternating(self, n:int, p_size:float, x_size:float, gap:'Union[float,None]'=None, p_voltage:float=0, x_voltage:float=0, y_offset:float=0, create_source_and_drain:bool=False, s_voltage:float=0, d_voltage:float=0) -> None:
        ''' Add alternating gates to the geometry.
        
        Parameters
        ----------
        n : int
            Number of plunger gates.
        p_size : float
            The size of the plunger gates.
        x_size : float
            The size of the barrier gates.
        gap : Union[float,None] (default=None)
            The gap between the gates. If the gap is none, it will be interpreted from pre-existing source and drain gates. If there are no source and drain gates, an error will be raised.
        p_voltage : float (default=0)
            The voltage of the potential gates.
        x_voltage : float (default=0)
            The voltage of the potential gates.
        y_offset : float (default=0)
            The y offset of the potential gates.
        create_source_and_drain : bool (default=False)
            If true and all three size parameters (p_size, x_size, gap) are specified, the source and drain will be created with default parameters. Note that the y_offset only applies to the P and X gates, not the source and drain gates.
        s_voltage : float (default=0)
            The voltage of the source gate (if this method is creating it).
        d_voltage : float (default=-1e-3)
            The voltage of the drain gate (if this method is creating it).

        Throws
        ------
        AttributeError
            If there are no source and drain gates and the gap is not specified.
        '''
        # check for source and drain gates if gap is unspecified
        if gap is None:
            if ('S' not in self._gates) or ('D' not in self._gates):
                raise AttributeError('Source and drain gates must be added before the alternating gates, or a gap must be specified.')
            else:
                # otherwise, calculate the gap
                gap = (self.width - n*p_size - (n+1)*x_size) / (2*(n+1))
        elif create_source_and_drain:
            # don't overwrite source and drain gates if they already exist
            if ('S' in self._gates) or ('D' in self._gates):
                raise AttributeError('Source and drain gates already exist. Cannot create new source and drain gates.')
            else:
                # create source and drain gates with default parameters
                width = n*p_size + (n+1)*x_size + 2*gap*(n+1)
                self.add_source_and_drain(-width/2, width/2, source_voltage=s_voltage, drain_voltage=d_voltage)
        # check all dimensions are >= 0
        if gap < 0 or p_size < 0 or x_size < 0:
            raise ValueError(f'All gate dimensions must be non-negative. Got gap={gap}, p_size={p_size}, x_size={x_size}.')
        # calculate the top and bottom of the gates
        x_top, x_bottom = y_offset + x_size/2, y_offset - x_size/2
        p_top, p_bottom = y_offset + p_size/2, y_offset - p_size/2
        # create p gates
        for i in range(n):
            gate = RectGate.from_edges(
                self._sx + (i+1)*(2*gap + x_size) + i*p_size,
                self._sx + (i+1)*(2*gap + x_size) + (i+1)*p_size,
                p_bottom, p_top, voltage=p_voltage)
            self.add_gate(f'P{i}', gate)
        # create x gates
        for i in range(n+1):
            gate = RectGate.from_edges(
                self._sx + gap + i*(2*gap + x_size + p_size),
                self._sx + gap + i*(2*gap + x_size + p_size) + x_size,
                x_bottom, x_top, voltage=x_voltage)
            self.add_gate(f'X{i}', gate)
    
    def add_measure(self, m_size:float, z_size:float, gap:float, m_voltage:float=0, z_voltage:float=0, y_offset:float=0):
        '''
        Add a measurement dot to the gate geometry.

        Parameters
        ----------
        m_size : float
            The size of the measure dot.
        z_size : float
            The size of the barrier gates.
        gap : float
            The gap between the gates.
        m_voltage : float (default=0)
            The voltage of the measure dot.
        z_voltage : float (default=0)
            The voltage of the barrier gates.
        y_offset : float (default=0)
            The y offset of the measurement dot and associated gates.
        
        Throws
        ------
        ValueError
            If there are no source and drain gates.
        '''
        # check for source and drain gates
        if ('S' not in self._gates) or ('D' not in self._gates):
            raise ValueError('Source and drain gates must be added before the measure dot.')
        # calculate how much to extend source and drain gates by
        ext = (self.width - m_size - 2*z_size - 4*gap) / 2
        # ensure all dimensions are >= 0
        if ext < 0 or m_size < 0 or z_size < 0 or gap < 0:
            raise ValueError(f'All gate dimensions must be non-negative. Got ext={ext}, m_size={m_size}, x_size={z_size}, gap={gap}.')
        # calculate top and bottom of m and x gates
        m_top, m_bottom = y_offset + m_size/2, y_offset - m_size/2
        z_top, z_bottom = y_offset + z_size/2, y_offset - z_size/2
        
        # create source and drain extensions
        if ext != 0:
            gate = RectGate.from_edges(self._sx, self._sx + ext, m_bottom, m_top, voltage=self['S'].V)
            self.add_gate('S_ext', gate)
            gate = RectGate.from_edges(self._dx - ext, self._dx, m_bottom, m_top, voltage=self['D'].V)
            self.add_gate('D_ext', gate)

            # link source and drain gates with extensions
            self['S'].link(self['S_ext'])
            self['D'].link(self['D_ext'])
        
        # create barrier gates
        self.add_gate('Z0',
            RectGate.from_edges(self._sx + ext + gap, self._sx + ext + gap + z_size, z_bottom, z_top, voltage=z_voltage))
        self.add_gate('Z1',
            RectGate.from_edges(self._dx - ext - gap - z_size, self._dx - ext - gap, z_bottom, z_top, voltage=z_voltage))
        
        # create measure dot
        self.add_gate('M',
            RectGate.from_edges(self._sx + ext + 2*gap + z_size, self._dx - ext - 2*gap - z_size, m_bottom, m_top, voltage=m_voltage))
