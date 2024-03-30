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
    ''' Rotation matrix for rotating a vector around the n axis by theta. '''
    Rn_z = np.array([
        [0.5, 0, np.sqrt(3)/2],
        [0, 1, 0],
        [-np.sqrt(3)/2, 0, 0.5]])
    # rotate n to z, rotate z by theta, then rotate z back to n
    return np.matmul(np.matmul(Rn_z, Rz(theta)), np.linalg.inv(Rn_z))

class BlochSphere(manim.ThreeDScene):

    def get_bloch_sphere(self):
        bloch_sphere = manim.Sphere(radius=1, resolution=(15, 15), fill_opacity=0)
        axes = manim.ThreeDAxes(
            x_range=[-1.5, 1.5], y_range=[-1.5, 1.5], z_range=[-1.5, 1.5],
            x_length=3, y_length=3, z_length=3,
            axis_config={"tip_width":0.1, "tip_height":0.1, "include_ticks":False})
        labels = axes.get_axis_labels(x_label=r"\vert{x}\rangle", y_label=r"\vert{y}\rangle", z_label=r"\vert{z}\rangle")
        labels[0].rotate(np.pi, axis=manim.OUT, about_point=1.5*manim.RIGHT)
        labels[2].rotate_about_origin(np.pi, axis=manim.OUT)
        for l in labels: l.scale(0.8)
        return manim.VGroup(bloch_sphere, axes, labels)

    def qubit(self, qubit:np.ndarray, **kwargs):
        return manim.Arrow3D(start=manim.ORIGIN, end=qubit, base_radius=0.05, height=0.1, **kwargs)
    
    def construct(self):
        bloch_sphere = self.get_bloch_sphere()
        self.set_camera_orientation(phi=60 * manim.DEGREES, theta=140 * manim.DEGREES, zoom=2)
        self.wait(1)
        self.play(manim.Create(bloch_sphere))
        self.wait(1)

        # create qubit vectors to rotate around
        z_qb = self.qubit(manim.OUT, color=manim.BLUE_A)
        z_qb_bold = self.qubit(manim.OUT, color=manim.BLUE_D)
        n_qb = self.qubit(N_VEC, color=manim.RED_A)
        n_qb_bold = self.qubit(N_VEC, color=manim.RED_D)
        z_qb.target = z_qb_bold
        n_qb.target = n_qb_bold
        z_qb.save_state()
        n_qb.save_state()

        # add rotation axes qubit vectors to the scene
        self.play(manim.Create(z_qb), manim.Create(n_qb))
        self.wait(1)

        # create a qubit vector
        qubit = self.qubit([1,0,0], color=manim.YELLOW_C)
        self.play(manim.Create(qubit))
        self.wait(1)

        # bold the z vector
        self.play(manim.MoveToTarget(z_qb))

        # rotate about the z vector
        self.play(manim.Rotate(qubit, angle=5*np.pi/6, axis=manim.OUT, about_point=manim.ORIGIN), run_time=5/6)

        # unbold the z vector
        self.play(manim.Restore(z_qb))
        self.wait(1)

        # bold the n vector
        self.play(manim.MoveToTarget(n_qb))

        # rotate about the n vector
        self.play(manim.Rotate(qubit, angle=5*np.pi/3, axis=N_VEC, about_point=manim.ORIGIN), run_time=5/3)

        # unbold the n vector
        self.play(manim.Restore(n_qb))
        self.wait(1)

        # self.play(manim.Rotate(qubit, angle=np.pi/3, axis=manim.OUT, about_point=manim.ORIGIN), run_time=2)


        # qubit1 = manim.Arrow3D(start=np.array([0,0,0]), end=np.array([1,0,0]), color=manim.RED, base_radius=0.05, height=0.1)
        # qubit2 = manim.Arrow3D(start=np.array([0,0,0]), end=np.array([-1/2,-np.sqrt(3)/2,0]), color=manim.YELLOW, base_radius=0.05, height=0.1)
        # nv = manim.Arrow3D(start=np.array([0,0,0]), end=N_VEC, color=manim.BLUE, thickness=0.01, base_radius=0.02, height=0.1)
        # self.play(manim.Create(nv))
        # self.wait(1)
        # self.play(manim.Create(qubit1), manim.Create(qubit2))
        # self.wait(1)
        # self.play(
        #     manim.Rotate(qubit1, angle=5*np.pi/2, axis=N_VEC, about_point=np.array([0,0,0])),
        #     manim.Rotate(qubit2, angle=5*np.pi/2, axis=N_VEC, about_point=np.array([0,0,0])), run_time=3)
        # self.wait(1)

        # # create and animate a qubit
        # qubit = qt.basis(2, 0)
        # qubit = Rn(np.pi/4) @ qubit
        # qubit = Rz(np.pi/2) @ qubit
        # qubit = Rn(-np.pi/4) @ qubit
        # qubit = qt.Qobj(qubit)
        # qubit = qt.Qubit(qubit)
        # qubit = manim.Sphere
