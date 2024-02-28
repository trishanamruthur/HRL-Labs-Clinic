import manim as mn
from potential import *
import matplotlib.pyplot as plt 
import numpy as np
from geom import *


mn.config.media_width = "75%"
mn.config.verbosity = "WARNING"



class gatepot(mn.ThreeDScene):
    def construct(self):
        g = GateGeometry()

        g.add_alternating(
            n=3,
            p_size=90e-9,
            x_size=50e-9,
            gap=10e-9,
            p_voltage=-2e-3,
            x_voltage=1e-3,
            y_offset=95e-9,
            create_source_and_drain=True,
            s_voltage=1e-4,
            d_voltage=0)

        g.add_measure(
            m_size=90e-9,
            z_size=50e-9,
            gap=10e-9,
            m_voltage=-1e-3,
            z_voltage=1e-3,
            y_offset=-95e-9)

        self.set_camera_orientation(phi=0, theta=-mn.PI/2, zoom=1)
        
        ax = mn.ThreeDAxes(
            x_range=(-400e-9, 400e-9, 100e-9), 
            y_range=(-200e-9, 200e-9, 100e-9), 
            z_range=(-5e-4, 5e-4, 1e-4),
            axis_config={'include_ticks': True},
            tips=False)
        
        
        self.play(mn.Create(ax))
        self.wait(1)

        rects = []
        for name in g.gate_names:
            if name != 'S' and name != 'D':
                # create the rectangle scaled to fit the plot
                rects.append(mn.Rectangle(
                    width=ax.coords_to_point(g[name].width)[0],
                    height=ax.coords_to_point(g[name].height)[0],
                    fill_opacity=0.1,
                    color=mn.RED).move_to(ax.coords_to_point(*g[name].pos)))
                
                # add the name of the gate
                t = mn.Text(name).scale(0.5)
                t.move_to(rects[-1].get_top())
                t.shift(0.9 * t.height * mn.DOWN)
                rects.append(t)
        # add a rectangle for the source and the drain
        rects.append(mn.Rectangle(width=10, height=10, fill_opacity=0.1, color=mn.RED).move_to((ax.coords_to_point(g['S'].R)[0] - 5) * mn.RIGHT))
        rects.append(mn.Rectangle(width=10, height=10, fill_opacity=0.1, color=mn.RED).move_to((ax.coords_to_point(g['D'].L)[0] + 5) * mn.RIGHT))
        # add source and drain names
        rects.append(mn.Text('Source').rotate(mn.PI/2).move_to(6*mn.LEFT))
        rects.append(mn.Text('Drain').rotate(-mn.PI/2).move_to(6*mn.RIGHT))
        rects = mn.VGroup(*rects)

        self.play(mn.Create(rects))
        self.wait(2)

        surf = ax.plot_surface(
            function=g,
            u_range=(-400e-9, 400e-9),
            v_range=(-300e-9, 300e-9),
            fill_opacity=0.3)
        
        self.play(mn.Create(surf))
        self.wait(2)

        self.move_camera(phi=60 * mn.DEGREES, theta=-60 * mn.DEGREES, zoom=0.9)
        self.wait(2)

        self.play(mn.FadeOut(rects), run_time=1)
        self.wait(1)
        
        # wiggle gate voltages
        for name, v in [('P1', -0.001), ('P1', -0.002), ('P2', -0.0005), ('P2', -0.002)]: #, ('P1', -0.002), ('X0', 0.0015), ('P0', -0.0015), ('P1', -0.001), ('X2', 0.0015), ('S', 0.0003), ('D', -3e-4)]:
            g[name].set_voltage(v)
            surf.target = ax.plot_surface(
                function=g,
                u_range=(-400e-9, 400e-9),
                v_range=(-300e-9, 300e-9),
                fill_opacity=0.3)
            
            self.play(mn.MoveToTarget(surf), run_time=2)
            self.wait(1.5)
        

class tunneling(mn.ThreeDScene):
    def construct(self):
        g = GateGeometry()

        g.add_alternating(
            n=3,
            p_size=90e-9,
            x_size=50e-9,
            gap=10e-9,
            p_voltage=-2e-3,
            x_voltage=1.5e-3,
            y_offset=95e-9,
            create_source_and_drain=True,
            s_voltage=1e-4,
            d_voltage=0)

        g.add_measure(
            m_size=90e-9,
            z_size=50e-9,
            gap=10e-9,
            m_voltage=-1e-3,
            z_voltage=1e-3,
            y_offset=-95e-9)

        # add axes
        ax = mn.ThreeDAxes(
            x_range=(-400e-9, 400e-9, 100e-9), 
            y_range=(-200e-9, 200e-9, 100e-9), 
            z_range=(-5e-4, 5e-4, 1e-4),
            axis_config={'include_ticks': True},
            tips=False)
        self.add(ax)

        # add surface plot
        surf = ax.plot_surface(
            function=g,
            u_range=(-400e-9, 400e-9),
            v_range=(-300e-9, 300e-9),
            fill_opacity=0.3)
        self.add(surf)

        # move camera
        # self.set_camera_orientation(phi=60*mn.DEGREES, theta=60*mn.DEGREES, zoom=0.75)
        self.set_camera_orientation(phi=60*mn.DEGREES, theta=80*mn.DEGREES, zoom=0.75)

        # wait for a second
        self.wait(1)

        # create electron
        electron = mn.Sphere(
            center=ax.coords_to_point(-375e-9, 95e-9, 20e-6),
            radius=0.2,
            color=mn.RED)
        self.add(electron)
        self.wait(1)

        # create electron target in P0
        electron.generate_target()
        electron.target.move_to(ax.coords_to_point(-160e-9, 95e-9, -300e-6))
        # create surface target while electron moves
        surf.save_state()
        g['X0'].set_voltage(-1.5e-3)
        surf.target = ax.plot_surface(
            function=g,
            u_range=(-400e-9, 400e-9),
            v_range=(-300e-9, 300e-9),
            fill_opacity=0.3)
        g['X0'].set_voltage(1.5e-3)
        self.play(
            mn.Succession(mn.MoveToTarget(surf), mn.Restore(surf)),
            mn.MoveToTarget(electron))
        
        self.wait(2)

        # create electron target in P1
        electron.generate_target()
        electron.target.move_to(ax.coords_to_point(0, 95e-9, -300e-6))
        # create surface target while electron moves
        surf.save_state()
        g['X1'].set_voltage(-1.5e-3)
        surf.target = ax.plot_surface(
            function=g,
            u_range=(-400e-9, 400e-9),
            v_range=(-300e-9, 300e-9),
            fill_opacity=0.3)
        g['X1'].set_voltage(1.5e-3)
        self.play(
            mn.Succession(mn.MoveToTarget(surf), mn.Restore(surf)),
            mn.MoveToTarget(electron))
        
        self.wait(2)

        # create electron target in P1
        electron.generate_target()
        electron.target.move_to(ax.coords_to_point(160e-9, 95e-9, -300e-6))
        # create surface target while electron moves
        surf.save_state()
        g['X2'].set_voltage(-1.5e-3)
        surf.target = ax.plot_surface(
            function=g,
            u_range=(-400e-9, 400e-9),
            v_range=(-300e-9, 300e-9),
            fill_opacity=0.3)
        g['X2'].set_voltage(1.5e-3)
        self.play(
            mn.Succession(mn.MoveToTarget(surf), mn.Restore(surf)),
            mn.MoveToTarget(electron))
        '''
        # wiggle gate voltages
        for name, v in [('X0', -1e-3), ('X0', 1.5e-3), ('X1', -1e-3), ('X1', 1.5e-3)]:
            g[name].set_voltage(v)
            surf.target = ax.plot_surface(
                function=g,
                u_range=(-400e-9, 400e-9),
                v_range=(-300e-9, 300e-9),
                fill_opacity=0.3)
            
            self.play(mn.MoveToTarget(surf), run_time=2)
            self.wait(1.5)
        '''
        pass


class fun_tunneling(mn.ThreeDScene):
    def construct(self):
        g = Dots()
        # g.add_dot('P0', -160e-9, 95e-9, 20e-9, -1e-3)
        # g.add_dot('P1', 0, 0, 50e-9, 1e-3)
        # g.add_dot('P2', 160e-9, -95e-9, 20e-9, -1e-3)

        WELL = -1e-3
        SOFT_WELL = -0.2e-3
        BARRIER = 1e-4
        g.add_alternating(
            n=3,
            p_rad=90e-9,
            x_rad=135e-9,
            spacing=5e-9,
            p_h=WELL,
            x_h=BARRIER,
            y_offset=95e-9)
        
        # add axes
        ax = mn.ThreeDAxes(
            x_range=(-400e-9, 400e-9, 100e-9), 
            y_range=(-200e-9, 200e-9, 100e-9), 
            z_range=(-1.5e-3, 1.5e-3, 1e-4),
            axis_config={'include_ticks': True},
            tips=False)
        self.add(ax)

        # add surface plot
        surf = ax.plot_surface(
            function=g,
            u_range=(-400e-9, 400e-9),
            v_range=(-300e-9, 300e-9),
            fill_opacity=0.3)
        self.add(surf)

        # move camera
        # self.set_camera_orientation(phi=60*mn.DEGREES, theta=60*mn.DEGREES, zoom=0.75)
        self.set_camera_orientation(phi=60*mn.DEGREES, theta=80*mn.DEGREES, zoom=0.75)

        # wait for a second
        self.wait(1)

        # add electrons!
        e0 = mn.Sphere(
            center = ax.coords_to_point(*g.get_pos('P0'), 0), radius=0.2, color=mn.RED)
        e1 = mn.Sphere(
            center = ax.coords_to_point(*g.get_pos('P1'), 0), radius=0.2, color=mn.RED)
        
        # targets for interaction animation
        surf.save_state()
        g.edit_height('P0', SOFT_WELL)
        g.edit_height('X1', WELL)
        g.edit_height('P1', SOFT_WELL)

        e0.save_state()
        e1.save_state()
        e0.generate_target()
        e1.generate_target()
        x, y, _ = ax.coords_to_point(*g.get_pos('X1'),0)
        e0.target.move_to(np.array([x-0.3, y, 0]))
        e1.target.move_to(np.array([x+0.3, y, 0]))

        surf.target = ax.plot_surface(
            function=g,
            u_range=(-400e-9, 400e-9),
            v_range=(-300e-9, 300e-9),
            fill_opacity=0.3)
        
        self.play(mn.Succession(mn.MoveToTarget(surf), mn.Restore(surf)),
            mn.Succession(mn.MoveToTarget(e0), mn.Restore(e0)),
            mn.Succession(mn.MoveToTarget(e1), mn.Restore(e1)), run_time=2)

        self.wait(2)

        '''
        # create electron
        electron = mn.Sphere(
            center=ax.coords_to_point(-375e-9, 95e-9, 20e-6),
            radius=0.2,
            color=mn.RED)
        self.add(electron)
        self.wait(1)

        # create electron target in P0
        electron.generate_target()
        electron.target.move_to(ax.coords_to_point(-160e-9, 95e-9, -300e-6))
        # create surface target while electron moves
        surf.save_state()
        g['X0'].set_voltage(-1.5e-3)
        surf.target = ax.plot_surface(
            function=g,
            u_range=(-400e-9, 400e-9),
            v_range=(-300e-9, 300e-9),
            fill_opacity=0.3)
        g['X0'].set_voltage(1.5e-3)
        self.play(
            mn.Succession(mn.MoveToTarget(surf), mn.Restore(surf)),
            mn.MoveToTarget(electron))
        
        self.wait(2)

        # create electron target in P1
        electron.generate_target()
        electron.target.move_to(ax.coords_to_point(0, 95e-9, -300e-6))
        # create surface target while electron moves
        surf.save_state()
        g['X1'].set_voltage(-1.5e-3)
        surf.target = ax.plot_surface(
            function=g,
            u_range=(-400e-9, 400e-9),
            v_range=(-300e-9, 300e-9),
            fill_opacity=0.3)
        g['X1'].set_voltage(1.5e-3)
        self.play(
            mn.Succession(mn.MoveToTarget(surf), mn.Restore(surf)),
            mn.MoveToTarget(electron))
        
        self.wait(2)

        # create electron target in P1
        electron.generate_target()
        electron.target.move_to(ax.coords_to_point(160e-9, 95e-9, -300e-6))
        # create surface target while electron moves
        surf.save_state()
        g['X2'].set_voltage(-1.5e-3)
        surf.target = ax.plot_surface(
            function=g,
            u_range=(-400e-9, 400e-9),
            v_range=(-300e-9, 300e-9),
            fill_opacity=0.3)
        g['X2'].set_voltage(1.5e-3)
        self.play(
            mn.Succession(mn.MoveToTarget(surf), mn.Restore(surf)),
            mn.MoveToTarget(electron))
        
        '''
        
        '''
        # wiggle gate voltages
        for name, v in [('X0', -1e-3), ('X0', 1.5e-3), ('X1', -1e-3), ('X1', 1.5e-3)]:
            g[name].set_voltage(v)
            surf.target = ax.plot_surface(
                function=g,
                u_range=(-400e-9, 400e-9),
                v_range=(-300e-9, 300e-9),
                fill_opacity=0.3)
            
            self.play(mn.MoveToTarget(surf), run_time=2)
            self.wait(1.5)
        '''
        pass

class testing(mn.ThreeDScene):
    def construct(self):
        # self.set_camera_orientation(phi=60 * mn.DEGREES, theta=-60 * mn.DEGREES, zoom=0.9)

        # ax = mn.ThreeDAxes((-400e-9, 400e-9, 100e-9), (-200e-9, 200e-9, 100e-9), (-2e-4, 8e-4, 1e-4), axis_config={'include_tip': True})
        
        # # self.play(mn.Create(rects))
        # self.play(mn.Create(ax))
        # self.wait(1)
        
        self.set_camera_orientation(phi=2*mn.PI/5, theta=mn.PI/5)
        # axes = mn.ThreeDAxes(
        #     x_range=(-6e-9, 6e-9, 1e-9),
        #     y_range=(-6e-9, 6e-9, 1e-9))
        axes = mn.ThreeDAxes(
            x_range=(-400e-9, 400e-9, 100e-9), 
            y_range=(-200e-9, 200e-9, 100e-9), 
            z_range=(-5e-4, 5e-4, 1e-4),
            axis_config={'include_ticks': True},
            tips=False)
        # axes = mn.NumberLine(
        #     x_range=(0, 400e-9, 20e-9),
        #     include_tip=True,
        #     length=8
        #     )
            # axis_config={"include_numbers": True})
        # labels = axes.get_axis_labels(
        #     mn.Tex("x-axis").scale(0.7), mn.Text("y-axis").scale(0.45), mn.Text("z-axis").scale(0.45)
        # )
        self.play(mn.Create(axes))
        # self.wait(1)
        # self.play(mn.Create(labels))
        self.wait(2)