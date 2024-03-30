import numpy as np
import manim as mn

class DotSeries:
    def __init__(self, n:int, a_rad:float, b_rad:float, a_h:float, b_h:float, a_sig:float, b_sig:float, y_offset:float=0):
        # calculate total width
        self.width = n*2*a_rad + (n+1)*2*b_rad

        # store the initialization parameters
        self.n = n
        self.a_sig, self.b_sig = a_sig, b_sig
        self.a_rad, self.b_rad = a_rad, b_rad
        self.a_h, self.b_h = a_h, b_h
        self.y_offset = y_offset

        # create arrays
        self.centers = np.zeros((2*n+1,2))
        self.sigs = np.zeros((2*n+1,))
        self.heights = np.zeros((2*n+1,))

        # set all the parameters to base values
        self.reset()

    @property
    def x_min(self):
        return -self.width/2
    
    @property
    def x_max(self):
        return self.width/2
    
    def reset(self):
        # create a list of center points for each dot
        # these are evenly spaced so it's fairly simple
        self.centers[:,0] = [self.x_min + self.b_rad + i*(self.a_rad+self.b_rad) for i in range(2*self.n+1)]
        self.centers[:,1] = self.y_offset

        # list of sigmas for each dot --  these are alternating
        self.sigs[0::2] = self.b_sig
        self.sigs[1::2] = self.a_sig

        # heights for each dot -- also just alternating
        self.heights[0::2] = self.b_h
        self.heights[1::2] = self.a_h

    def __call__(self, x, y):
        # turn the input into a vector
        r = np.array([x,y])
        # calculate distances to each of the dots
        d = np.linalg.norm(self.centers - r, axis=1)
        # calculate a sum of gaussian distributions from each dot
        return np.sum(self.heights * np.exp(-0.5*(d/self.sigs)**2))

    def get_index(self, dot:str):
        return 2 * int(dot[1]) + (dot[0] == 'A' or dot[0] == 'P')
    
    def tunnel_across(self, dot):
        # make sure we are trying to tunnel across a barrier
        if dot[0] != 'B' and dot[0] != 'X':
            raise ValueError('Dot name must start with "B" or "X"')
        # get the index of the dot to tunnel across
        i = self.get_index(dot)
        # move previous dot a bit forward
        if i != 0:
            self.centers[i-1,0] = self.centers[i,0] - self.a_sig
        # move the next dot a bit back
        if i != 2*self.n:
            self.centers[i+1,0] = self.centers[i,0] + self.a_sig
        # drop the barrier
        self.heights[i] = 0


class Dots:
    def __init__(
        self,
        names: "list[str]" = [],
        positions: np.ndarray = np.array([]).reshape(0, 2),
        radii: np.ndarray = np.array([]).reshape(0, 1),
        heights: np.ndarray = np.array([]).reshape(0, 1),
    ):
        self.names = names
        self.positions = positions
        self.radii = radii
        self.heights = heights

    def __call__(self, x, y) -> float:
        s = np.array([x, y]).reshape(
            2,
        )
        dists = np.linalg.norm(self.positions - s, axis=1)
        return np.sum(self.heights * np.exp(-((2 * dists / self.radii) ** 2)))

    def add_dot(
        self, name: str, x: float, y: float, radius: float, height: float
    ) -> None:
        # make sure the name is unique
        if name in self.names:
            raise ValueError(f"Attempted to add dot with duplicate name '{name}'")
        # add the dot
        self.names.append(name)
        self.positions = np.append(self.positions, np.array([[x, y]]), axis=0)
        self.radii = np.append(self.radii, radius)
        self.heights = np.append(self.heights, height)

    def edit_height(self, name: str, new_height: float) -> None:
        i = self.names.index(name)
        self.heights[i] = new_height

    def edit_radius(self, name: str, new_radius: float) -> None:
        i = self.names.index(name)
        self.radii[i] = new_radius

    def add_alternating(self, n:int, p_rad:float, x_rad:float, spacing:float, p_h:float=0, x_h:float=0, y_offset:float=0, prefixes='PX') -> None:
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
        p_pfx, x_pfx = prefixes
        # compute total width
        total_width = 2 * n * p_rad + (n + 1) * spacing
        # add p dots
        for i in range(n):
            x = -total_width/2 + spacing + p_rad + i*(2*p_rad + spacing)
            self.add_dot(f'{p_pfx}{i}', x, y_offset, p_rad, p_h)
        # add x dots
        for i in range(n+1):
            x = -total_width/2 + spacing/2 + i*(2*p_rad + spacing)
            self.add_dot(f'{x_pfx}{i}', x, y_offset, x_rad, x_h)
        # return bounding coordinates
        return (-total_width / 2, total_width / 2)

    def get_pos(self, name: str) -> np.ndarray:
        i = self.names.index(name)
        return self.positions[i]


class SquareBath:
    def __init__(self, x, y, bounding:str, width:float=1, height:float=0):
        self._x = np.array([x,y])
        self._height = height
        self._width = width
        # set sign array
        if bounding.upper() == "UR":
            self._signs = np.array([-1, -1])
        elif bounding.upper() == "UL":
            self._signs = np.array([1, -1])
        elif bounding.upper() == "DR":
            self._signs = np.array([-1, 1])
        elif bounding.upper() == "DL":
            self._signs = np.array([1, 1])
        else:
            raise ValueError('Bounding must be one of "UR", "UL", "DR", or "DL".')

    def __call__(self, x, y) -> float:
        s = np.array([x,y]).reshape(2,) - self._x
        return self._height/(1 + np.sum(np.exp(self._signs * s * 5 / self._width)))

class Electron(mn.Dot):
    def __init__(self, pos:np.ndarray, radius:float=0.05):
        super().__init__(pos, radius=radius)
    
    @property
    def pos(self) -> np.ndarray:
        return self.get_center()
    
    def distance_to(self, other:'Electron') -> float:
        return np.linalg.norm(self.pos - other.pos)
    
    def distance_to_point(self, other:np.ndarray) -> float:
        return np.linalg.norm(self.pos - other)

class ElectronGroup:
    def __init__(self, *electrons):
        self.electrons = list(electrons)
    
    def add(self, electron:'Electron') -> None:
        self.electrons.append(electron)
    
    def closest_electron(self, pos:np.ndarray) -> 'tuple[Electron,float]':
        return min([(e, e.distance_to_point(pos)) for e in self.electrons], key=lambda x: x[1])
    
    def add_bunch(self, center:np.ndarray, n:int, sample_radius:float, electron_radius:float) -> None:
        # loop to randomly add electrons
        for _ in range(n):
            angle = 2*np.pi*np.random.rand()
            rad = np.random.rand() * sample_radius
            pos = center + rad*np.array([np.cos(angle), np.sin(angle)])

            self.add(Electron(pos, electron_radius))

class CombinedGeometry:
    def __init__(self, *geoms):
        self._geoms = list(geoms)
    
    def add(self, g):
        self._geoms.append(g)
    
    def __call__(self, x:float, y:float) -> float:
        return sum([g(x,y) for g in self._geoms])
