import numpy as np

class Dots:
    def __init__(self, names:'list[str]'=[], positions:np.ndarray=np.array([]).reshape(0,2), radii:np.ndarray=np.array([]).reshape(0,1), heights:np.ndarray=np.array([]).reshape(0,1)):
        self.names = names
        self.positions = positions
        self.radii = radii
        self.heights = heights

    def __call__(self, x, y) -> float:
        s = np.array([x,y]).reshape(2,)
        dists = np.linalg.norm(self.positions - s, axis=1)
        return np.sum(self.heights*np.exp(-(2*dists/self.radii)**2))

    def add_dot(self, name:str, x:float, y:float, radius:float, height:float) -> None:
        # make sure the name is unique
        if name in self.names:
            raise ValueError(f"Attempted to add dot with duplicate name '{name}'")
        # add the dot
        self.names.append(name)
        self.positions = np.append(self.positions, np.array([[x,y]]), axis=0)
        self.radii = np.append(self.radii, radius)
        self.heights = np.append(self.heights, height)

    def edit_height(self, name:str, new_height:float) -> None:
        i = self.names.index(name)
        self.height[i] = new_height
    
    def edit_radius(self, name:str, new_radius:float) -> None:
        i = self.names.index(name)
        self.radii[i] = new_radius
    
    def edit_position(self, name:str, new_radius:float) -> None:
        i = self.names.index(name)
        self.radii[i] = new_radius

    def add_alternating(self, n:int, p_rad:float, x_rad:float, gap:'Union[float,None]'=None, p_dep:float=0, x_dep:float=0, y_offset:float=0) -> None:
        ''' Add alternating gates to the geometry.
        
        Parameters
        ----------
        n : int
            Number of P dots that will be added.
        p_rad : float
            The radius of the plunger dots.
        x_rad : float
            The size of the barrier gates.
        gap : Union[float,None] (default=None)
            The gap between the gates. If the gap is none, it will be interpreted from pre-existing source and drain gates. If there are no source and drain gates, an error will be raised.
        p_h : float (default=0)
            The height of the potential dots.
        x_h : float (default=0)
            The height of the barrier dots.
        y_offset : float (default=0)
            The y offset of the potential gates.

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
    
# class Dot:
#     def __init__(self, pos:np.ndarray, radius:float, depth:float):
#         self._pos = pos
#         self.radius = radius
#         self.depth = depth

#     def __str__(self):
#         return f"Dot({self.pos}, r={self.radius}, d={self.depth})"
    
#     def pos(self, z=None):
#         if z is None:
#             return self.pos
#         else:
#             return np.array([self.pos[0], self.pos[1], z])
        
#     def __call__(self, x:np.ndarray):
#         r = np.linalg.norm(x - self.pos)
#         if r >= self.radius:
#             return 0
#         else:
#             return self.depth * (r/self.radius - 1)**2 * (r/self.radius + 1)**2
