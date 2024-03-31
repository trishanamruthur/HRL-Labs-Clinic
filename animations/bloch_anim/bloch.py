# import qutip as qt
import numpy as np
import manim

# create blank bloch sphere


N_VEC = np.array([-np.sqrt(3)/2, 0, -0.5])

class BlochSphere(manim.ThreeDScene):
    def get_bloch_sphere(self):
        '''Returns a V-Group containing the bloch sphere, axes, and labels. '''
        bloch_sphere = manim.Sphere(radius=1, resolution=(15, 15), fill_opacity=0)
        axes = manim.ThreeDAxes(
            x_range=[-1.5, 1.5], y_range=[-1.5, 1.5], z_range=[-1.5, 1.5],
            x_length=3, y_length=3, z_length=3,
            axis_config={"tip_width":0.1, "tip_height":0.1, "include_ticks":False})
        label = axes.get_z_axis_label(label=r"\vert{0}\rangle").scale(0.8)
        return manim.VGroup(bloch_sphere, axes, label)

    def qubit(self, qubit:np.ndarray, **kwargs):
        return manim.Arrow3D(start=manim.ORIGIN, end=qubit, base_radius=0.05, height=0.1, **kwargs)
    
    def axis(self, ax:np.ndarray, **kwargs):
        return manim.Line3D(start=-ax, end=ax, thickness=0.02, **kwargs)
    
    def title_text(self, text:str, **kwargs):
        return manim.Tex(text, **kwargs).scale(0.8).to_edge(manim.UP)
    
    def construct(self):
        # orient the camera
        self.set_camera_orientation(phi=60 * manim.DEGREES, theta=140 * manim.DEGREES, zoom=1.7)

        # initialize objects
        bloch_sphere = self.get_bloch_sphere()
        z_ax = self.axis(manim.OUT, color=manim.BLUE_D)
        n_ax = self.axis(N_VEC, color=manim.RED_D)
        qb = self.qubit(manim.OUT, color=manim.YELLOW_C)

        # get and create the bloch sphere
        self.add(bloch_sphere)
        self.wait(1)

        # add the qubit to the frame
        t = self.title_text(r"Qubit is initialized on the $+z$ axis in the $\vert{0}\rangle$ state",  color=manim.YELLOW_C)
        self.add_fixed_in_frame_mobjects(t)
        self.play(manim.Create(qb), run_time=1)
        self.wait(1)
        self.remove(t)
        self.wait(1)

        # update the text
        t = self.title_text(r"The $P_2$ gate rotates the qubit about the $\textbf{n}$ axis", color=manim.RED_D)
        self.add_fixed_in_frame_mobjects(t)

        # add the n axis
        ax_lbl = manim.Tex(r"\textbf{n}", color=manim.RED_D).scale(0.8).move_to(manim.UP*1.7+manim.LEFT*1.5)
        self.add_fixed_in_frame_mobjects(ax_lbl)
        self.play(manim.Create(n_ax))
        self.wait(1)

        # rotate the qubit about the n axis
        self.play(manim.Rotate(qb, angle=7*np.pi/3, axis=N_VEC, about_point=manim.ORIGIN), run_time=2*7/3)
        self.remove(ax_lbl)
        self.play(manim.Uncreate(n_ax))
        self.remove(t)
        self.wait(1)

        # update the text
        t = self.title_text(r"The $P_1$ gate rotates the qubit about the $\textbf{z}$ axis", color=manim.BLUE_D)
        self.add_fixed_in_frame_mobjects(t)

        # create the z axis
        ax_lbl = manim.Tex(r"$\textbf{z}$", color=manim.BLUE_D).scale(0.8).move_to(manim.UP*1.8+manim.RIGHT*0.3)
        self.add_fixed_in_frame_mobjects(ax_lbl)
        self.play(manim.Create(z_ax))
        self.wait(1)

        # rotate the qubit about the z axis
        self.play(manim.Rotate(qb, angle=15*np.pi/6, axis=manim.OUT, about_point=manim.ORIGIN), run_time=2*15/6)
        self.remove(ax_lbl)
        self.play(manim.Uncreate(z_ax))
        self.remove(t)
        self.wait(1)

class ElectronInteractions(manim.Scene):

    def construct(self):
        # create the electrons
        e1 = manim.Dot(color=manim.YELLOW_D).move_to(manim.LEFT*2)
        e2 = manim.Dot(color=manim.YELLOW_D)
        e3 = manim.Dot(color=manim.YELLOW_D).move_to(manim.RIGHT*2)

        # create the gates
        p1_line = manim.Line(e1.get_center()+manim.UP*1, e2.get_center()+manim.UP*1, color=manim.BLUE_D)
        p1_lbl = manim.Tex(r"$P_1$", color=manim.BLUE_D).scale(0.8).next_to(p1_line.get_center(), direction=manim.UP)
        p1_gate = manim.VGroup(p1_line, p1_lbl)

        p2_line = manim.Line(e2.get_center()+manim.UP*1, e3.get_center()+manim.UP*1, color=manim.RED_D)
        p2_lbl = manim.Tex(r"$P_2$", color=manim.RED_D).scale(0.8).next_to(p2_line.get_center(), direction=manim.UP)
        p2_gate = manim.VGroup(p2_line, p2_lbl)
        
        self.add(e1, e2, e3)
        self.add(p1_gate, p2_gate)
        self.wait(1)

        # p2 gate interaction
        # generate targets
        e2.generate_target()
        e3.generate_target()
        p2_gate.generate_target()
        e2.target.shift(manim.RIGHT*0.9)
        e3.target.shift(manim.LEFT*0.9)
        p2_gate.target.shift(manim.DOWN*0.7)
        # save states
        e2.save_state()
        e3.save_state()
        p2_gate.save_state()
        # play animations
        self.play(manim.MoveToTarget(e2), manim.MoveToTarget(e3), manim.MoveToTarget(p2_gate), run_time=1)
        self.wait(2*7/3)
        self.play(manim.Restore(e2), manim.Restore(e3), manim.Restore(p2_gate), run_time=1)
        self.wait(1)

        # p2 gate interaction
        # generate targets
        e1.generate_target()
        e2.generate_target()
        p1_gate.generate_target()
        e1.target.shift(manim.RIGHT*0.9)
        e2.target.shift(manim.LEFT*0.9)
        p1_gate.target.shift(manim.DOWN*0.7)
        # save states
        e1.save_state()
        e2.save_state()
        p1_gate.save_state()
        # play animations
        self.play(manim.MoveToTarget(e1), manim.MoveToTarget(e2), manim.MoveToTarget(p1_gate), run_time=1)
        self.wait(2*15/6)
        self.play(manim.Restore(e1), manim.Restore(e2), manim.Restore(p1_gate), run_time=1)
        self.wait(1)

