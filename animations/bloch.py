# import qutip as qt
import numpy as np
import manim

# create blank bloch sphere


N_VEC = np.array([-np.sqrt(3)/2, 0, -0.5])

def Rz(theta:float) -> np.ndarray:
    return np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]])

def Rn(theta:float) -> np.ndarray:
    Rn_z = np.array([
        [0.5, 0, np.sqrt(3)/2],
        [0, 1, 0],
        [-np.sqrt(3)/2, 0, 0.5]])
    # rotate n to z, rotate z by theta, then rotate z back to n
    return np.matmul(np.matmul(Rn_z, Rz(theta)), np.linalg.inv(Rn_z))

class BlochSphere(manim.ThreeDScene):
    def construct(self):
        bloch_sphere = manim.Sphere(radius=1, resolution=(15, 15), fill_opacity=0)
        self.set_camera_orientation(phi=60 * manim.DEGREES, theta=30 * manim.DEGREES, zoom=2)
        self.wait(1)
        self.play(manim.Create(bloch_sphere))
        self.wait(1)
        t = manim.Tex(r"ABC").move_to([0, 0, 1.2])
        self.add(t)
        self.wait(1)

        # # create and animate a qubit
        # qubit = qt.basis(2, 0)
        # qubit = Rn(np.pi/4) @ qubit
        # qubit = Rz(np.pi/2) @ qubit
        # qubit = Rn(-np.pi/4) @ qubit
        # qubit = qt.Qobj(qubit)
        # qubit = qt.Qubit(qubit)
        # qubit = manim.Sphere
