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
        # initialize the dots
        dots = Dots()

        # parameters
        WELL = -5e-4
        M_WELL = -1e-3
        SOURCE_WELL = -3e-4
        DRAIN_WELL = -7e-4
        SOFT_WELL = -5e-5
        BARRIER = 1e-4
        Y_OFFSET = 95e-9
        P_RAD = 135E-9
        X_RAD = 90E-9
        SPACING = -30E-9
        M_RAD = 135E-9

        # alternating quantum dots
        dots_left_bound, dots_right_bound = dots.add_alternating(
            n=3,
            p_rad=P_RAD,
            x_rad=X_RAD,
            spacing=SPACING,
            p_h=WELL,
            x_h=BARRIER,
            y_offset=-Y_OFFSET)
        
        # add baths
        source_bath = SquareBath(dots_left_bound, -Y_OFFSET, 'DL', 1e-8, SOURCE_WELL)
        drain_bath = SquareBath(dots_right_bound, -Y_OFFSET, 'DR', 1e-8, DRAIN_WELL)

        # add measure dot
        left_bound, right_bound = dots.add_alternating(
            n=1,
            p_rad=M_RAD,
            x_rad=X_RAD,
            spacing=SPACING,
            p_h=M_WELL,
            x_h=BARRIER,
            y_offset=Y_OFFSET,
            prefixes='MZ')
        
        # add baths
        m_drain_bath = SquareBath(left_bound, Y_OFFSET, 'UL', 1e-7, DRAIN_WELL)
        m_source_bath = SquareBath(right_bound, Y_OFFSET, 'UR', 1e-7, SOURCE_WELL)
        
        # initialize the combined geometry
        geom = CombinedGeometry(dots, drain_bath, source_bath, m_drain_bath, m_source_bath)

        # initialize axes
        ax = mn.ThreeDAxes(
            x_range=(-400e-9, 400e-9, 100e-9), 
            y_range=(-200e-9, 200e-9, 100e-9), 
            z_range=(-1.5e-3, 1.5e-3, 1e-4),
            axis_config={'include_ticks': True},
            tips=False)
        # self.add(ax) # add the axes

        # plot the potential as a surface
        surf = ax.plot_surface(
            function=geom,
            u_range=(-400e-9, 400e-9),
            v_range=(-300e-9, 300e-9),
            fill_opacity=0.3)
        self.add(surf)

        # set the camera position
        # self.set_camera_orientation(phi=60*mn.DEGREES, theta=60*mn.DEGREES, zoom=0.75)
        self.set_camera_orientation(phi=60*mn.DEGREES, theta=(180+80)*mn.DEGREES, zoom=0.75)

        start_pos = ax.coords_to_point(dots_left_bound-30e-9, -Y_OFFSET, 0)
        # add electrons!
        e0 = mn.Dot(point=start_pos, radius=0.1)
        # e0 = mn.Dot(
        #     point = ax.coords_to_point(*dots.get_pos('P0'), 0), radius=0.2)
        # e1 = mn.Dot(
        #     point = ax.coords_to_point(*dots.get_pos('P1'), 0), radius=0.2)
        # self.add(e0) # , e1)

        # wait for a second
        self.wait(1)

        # targets for interaction animation
        # dots.edit_height('P0', SOFT_WELL)
        
        # e0.generate_target()
        # e0.target.move_to(ax.coords_to_point(*dots.get_pos('X0'),0))

        surf.save_state()
        dots.edit_height('X0', SOURCE_WELL)
        surf.target = ax.plot_surface(
            function=geom,
            u_range=(-400e-9, 400e-9),
            v_range=(-300e-9, 300e-9),
            fill_opacity=0.3)
        
        self.play(mn.Succession(mn.MoveToTarget(surf), mn.Restore(surf)), run_time=2)

        surf.save_state()
        dots.edit_height('P0', SOFT_WELL)
        dots.edit_height('X1', WELL)
        dots.edit_height('P1', SOFT_WELL)
        surf.target = ax.plot_surface(
            function=geom,
            u_range=(-400e-9, 400e-9),
            v_range=(-300e-9, 300e-9),
            fill_opacity=0.3)
        
        self.play(mn.Succession(mn.MoveToTarget(surf), mn.Restore(surf)), run_time=2)


        surf.save_state()
        dots.edit_height('P1', SOFT_WELL)
        dots.edit_height('X2', WELL)
        dots.edit_height('P2', SOFT_WELL)
        surf.target = ax.plot_surface(
            function=geom,
            u_range=(-400e-9, 400e-9),
            v_range=(-300e-9, 300e-9),
            fill_opacity=0.3)
        
        self.play(mn.Succession(mn.MoveToTarget(surf), mn.Restore(surf)), run_time=2)

        surf.save_state()
        dots.edit_height('Z0', WELL)
        dots.edit_height('M0', SOFT_WELL)
        surf.target = ax.plot_surface(
            function=geom,
            u_range=(-400e-9, 400e-9),
            v_range=(-300e-9, 300e-9),
            fill_opacity=0.3)
        
        self.play(mn.Succession(mn.MoveToTarget(surf), mn.Restore(surf)), run_time=2)

        '''
        self.play(mn.MoveToTarget(e0, rate_func=mn.rate_functions.ease_in_sine), mn.MoveToTarget(surf, rate_func=mn.rate_functions.ease_in_sine), run_time=2)

        e0.generate_target()
        e0.target.move_to(ax.coords_to_point(*dots.get_pos('P0'),0))

        self.play(mn.MoveToTarget(e0, rate_func=mn.rate_functions.ease_out_sine), mn.Restore(surf, rate_func=mn.rate_functions.ease_out_sine), run_time=2)

        '''
        # self.play(mn.Succession(mn.MoveToTarget(surf), mn.Restore(surf)),
        #     mn.Succession(mn.MoveToTarget(e0), mn.Restore(e0)), run_time=2)
            # mn.Succession(mn.MoveToTarget(e1), mn.Restore(e1)), run_time=2)

        self.wait(2)

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

class bath_test(mn.ThreeDScene):
    def construct(self):
        g = SquareBath(np.array([0,0]), 'UR', 1e-7, -1e-3)
        # g.add_dot('P2', 160e-9, -95e-9, 20e-9, -1e-3)

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
        
        # add surface plot
        self.add(surf)

        # move camera
        self.set_camera_orientation(phi=60*mn.DEGREES, theta=80*mn.DEGREES, zoom=0.75)

        # wait for a second
        self.wait(1)

class new_tunneling(mn.ThreeDScene):
    def construct(self):
        # initialize the dots
        dots = Dots()

        # parameters
        WELL = -8e-4
        BARRIER = 4e-4
        P_RAD = 135E-9
        X_RAD = 90E-9

        # alternating quantum dots
        dots = DotSeries(3, P_RAD, X_RAD, WELL, BARRIER, P_RAD/2, X_RAD/2, 0)
        
        # initialize axes
        ax = mn.ThreeDAxes(
            x_range=(-8e-7, 8e-7, 1e-7), 
            y_range=(-2e-7, 2e-7, 1e-7), 
            z_range=(-1.5e-3, 1.5e-3, 1e-4),
            axis_config={'include_ticks': True},
            tips=False)
        # self.add(ax) # add the axes

        # plot the potential as a surface
        surf = ax.plot_surface(
            function=dots,
            u_range=(-8e-7, 8e-7),
            v_range=(-6e-7, 6e-7),
            fill_opacity=0.3)
        self.add(surf)

        # set the camera position
        # self.set_camera_orientation(phi=60*mn.DEGREES, theta=60*mn.DEGREES, zoom=0.75)
        self.set_camera_orientation(phi=60*mn.DEGREES, theta=(180+80)*mn.DEGREES, zoom=0.75)

        # wait for a second
        self.wait(1)

        # targets for interaction animation
        dots.tunnel_across('X1')
        surf.save_state()
        surf.target = ax.plot_surface(
            function=dots,
            u_range=(-8e-7, 8e-7),
            v_range=(-6e-7, 6e-7),
            fill_opacity=0.3)
        dots.reset()
        
        self.play(mn.Succession(mn.MoveToTarget(surf), mn.Restore(surf)), run_time=2)

        dots.tunnel_across('X2')
        surf.save_state()
        surf.target = ax.plot_surface(
            function=dots,
            u_range=(-8e-7, 8e-7),
            v_range=(-6e-7, 6e-7),
            fill_opacity=0.3)
        dots.reset()

        self.play(mn.Succession(mn.MoveToTarget(surf), mn.Restore(surf)), run_time=2)
        
        
        '''
        self.play(mn.Succession(mn.MoveToTarget(surf), mn.Restore(surf)), run_time=2)


        surf.save_state()
        dots.edit_height('P1', SOFT_WELL)
        dots.edit_height('X2', WELL)
        dots.edit_height('P2', SOFT_WELL)
        surf.target = ax.plot_surface(
            function=geom,
            u_range=(-400e-9, 400e-9),
            v_range=(-300e-9, 300e-9),
            fill_opacity=0.3)
        
        self.play(mn.Succession(mn.MoveToTarget(surf), mn.Restore(surf)), run_time=2)

        surf.save_state()
        dots.edit_height('Z0', WELL)
        dots.edit_height('M0', SOFT_WELL)
        surf.target = ax.plot_surface(
            function=geom,
            u_range=(-400e-9, 400e-9),
            v_range=(-300e-9, 300e-9),
            fill_opacity=0.3)
        
        self.play(mn.Succession(mn.MoveToTarget(surf), mn.Restore(surf)), run_time=2)

        self.play(mn.MoveToTarget(e0, rate_func=mn.rate_functions.ease_in_sine), mn.MoveToTarget(surf, rate_func=mn.rate_functions.ease_in_sine), run_time=2)

        e0.generate_target()
        e0.target.move_to(ax.coords_to_point(*dots.get_pos('P0'),0))

        self.play(mn.MoveToTarget(e0, rate_func=mn.rate_functions.ease_out_sine), mn.Restore(surf, rate_func=mn.rate_functions.ease_out_sine), run_time=2)

        '''
        # self.play(mn.Succession(mn.MoveToTarget(surf), mn.Restore(surf)),
        #     mn.Succession(mn.MoveToTarget(e0), mn.Restore(e0)), run_time=2)
            # mn.Succession(mn.MoveToTarget(e1), mn.Restore(e1)), run_time=2)

        self.wait(2)

def state(dots):
    def func(x):
        DOTS = np.array(dots)
        SIG = 0.5
        DEP = -2

        d = DOTS - x
        return np.sum(DEP * np.exp(-0.5*(d/SIG)**2))
    return func

class tunneling2D(mn.Scene):
    def construct(self):

        # parameters
        # WELL = -8e-4
        # BARRIER = 4e-4
        # P_RAD = 135E-9
        # X_RAD = 90E-9

        # alternating quantum dots
        # dots = DotSeries(3, P_RAD, X_RAD, WELL, BARRIER, P_RAD/2, X_RAD/2, 0)
        
        # initialize axes
        # ax = mn.Axes(
        #     x_range=(-8e-7, 8e-7, 1e-7), 
        #     y_range=(-1.5e-3, 1.5e-3, 1e-4),
        #     axis_config={'include_ticks': True},
        #     tips=False)
        ax = mn.Axes().add_coordinates()
        # self.add(ax) # add the axes

        # plot the potential as a surface
        # surf = ax.plot_surface(
        #     function=dots,
        #     u_range=(-8e-7, 8e-7),
        #     v_range=(-6e-7, 6e-7),
        #     fill_opacity=0.3)
        # self.add(surf

        e1 = mn.Dot(ax.coords_to_point(-3,0,0), color=mn.RED)
        e2 = mn.Dot(ax.coords_to_point(0,0,0), color=mn.RED)
        e3 = mn.Dot(ax.coords_to_point(3,0,0), color=mn.RED)

        pot = ax.plot(state([-3,0,3]), (-6,6))
        self.play(mn.Create(pot), mn.Create(e1), mn.Create(e2), mn.Create(e3))
        
        # wait for a second
        self.wait(1)

        # targets for interaction animation
        pot.save_state()
        pot.target = ax.plot(state([-1.5,3]), (-6,6))
        e1.save_state()
        e1.generate_target()
        e1.target.move_to(ax.coords_to_point(-1.7,0,0))
        e2.save_state()
        e2.generate_target()
        e2.target.move_to(ax.coords_to_point(-1.3,0,0))

        # play movement
        self.play(
            mn.MoveToTarget(pot),
            mn.MoveToTarget(e1),
            mn.MoveToTarget(e2), run_time=0.5)
        self.wait(1)
        # play reset
        self.play(
            mn.Restore(pot),
            mn.Restore(e1),
            mn.Restore(e2), run_time=0.5)
        self.wait(1)

        # prepare for second interaction animation
        pot.save_state()
        pot.target = ax.plot(state([-3, 1.5]), (-6,6))
        e2.save_state()
        e2.generate_target()
        e2.target.move_to(ax.coords_to_point(1.3,0,0))
        e3.save_state()
        e3.generate_target()
        e3.target.move_to(ax.coords_to_point(1.7,0,0))

        # play movement
        self.play(
            mn.MoveToTarget(pot),
            mn.MoveToTarget(e2),
            mn.MoveToTarget(e3), run_time=0.5)
        self.wait(1)
        # play reset
        self.play(
            mn.Restore(pot),
            mn.Restore(e2),
            mn.Restore(e3), run_time=0.5)
        self.wait(1)


        # dots.tunnel_across('X2')
        # surf.save_state()
        # surf.target = ax.plot_surface(
        #     function=dots,
        #     u_range=(-8e-7, 8e-7),
        #     v_range=(-6e-7, 6e-7),
        #     fill_opacity=0.3)
        # dots.reset()

        # self.play(mn.Succession(mn.MoveToTarget(surf), mn.Restore(surf)), run_time=2)
