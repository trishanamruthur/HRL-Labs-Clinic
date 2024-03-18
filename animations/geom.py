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
        self.heights[i] = new_height
    
    def edit_radius(self, name:str, new_radius:float) -> None:
        i = self.names.index(name)
        self.radii[i] = new_radius
    
    def edit_position(self, name:str, new_radius:float) -> None:
        i = self.names.index(name)
        self.radii[i] = new_radius

    def add_alternating(self, n:int, p_rad:float, x_rad:float, spacing:float, p_h:float=0, x_h:float=0, y_offset:float=0) -> None:
        ''' Add alternating gates to the geometry.
        
        Parameters
        ----------
        n : int
            Number of P dots that will be added.
        p_rad : float
            The radius of the plunger dots.
        x_rad : float
            The radius of the barrier gates.
        spacing : float
            The distance between p gates.
        p_h : float (default=0)
            The (starting) height of the potential dots.
        x_h : float (default=0)
            The (starting) height of the barrier dots.
        y_offset : float (default=0)
            The y offset of all gates in this alternating pattern.

        Returns
        -------
        tuple[float, float]
            The bounding x and y coordinates of the entire geometry (including a gap on either side).
        '''
        # compute total width
        total_width = 2*n*p_rad + (n+1)*spacing
        # add p dots
        for i in range(n):
            x = -total_width/2 + spacing + p_rad + i*(2*p_rad + spacing)
            self.add_dot(f'P{i}', x, y_offset, p_rad, p_h)
        # add x dots
        for i in range(n+1):
            x = -total_width/2 + spacing/2 + i*(2*p_rad + spacing)
            self.add_dot(f'X{i}', x, y_offset, x_rad, x_h)
        # return bounding coordinates
        return (-total_width/2, total_width/2)

    def get_pos(self, name:str) -> np.ndarray:
        i = self.names.index(name)
        return self.positions[i]

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
