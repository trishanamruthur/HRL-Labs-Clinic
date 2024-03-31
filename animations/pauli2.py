from manim import *
import numpy as np
from scipy.stats import norm

class PauliSpinBlockade2(Scene):
    def construct(self):
        # interaction energy of two electrons (arbitrary)
        U = 10
        # maximum exchange energy (arbitrary)
        JMAX = U / 2
        # tunnel coupling (arbitrary)
        tc = .3
        # plot range---chosen to show all important spaghetti diagram features
        YMIN = -9
        YMAX = 4
        # points for plotting eigenenergies
        # we want 10n + 1 points for points at exactly bias=0, 10, 15
        NUM = 101
        # range must be greater than (-U-JMAX, U+JMAX)
        BIASRANGE = 2.5 * U

        # x-axis of spaghetti diagram
        biases = np.linspace(-BIASRANGE, BIASRANGE, NUM)

        # axes for spaghetti diagram
        spaghetti = Axes(y_range=[YMIN, YMAX],
                         x_range=[-BIASRANGE, BIASRANGE],
                         axis_config={'include_ticks':False})
        
        # calculate eigen(values|vectors) for various biases
        singlet_vals = []
        triplet_vals = []
        for i in range(NUM):
            singval = np.linalg.eig(
                np.array([[U - biases[i], np.sqrt(2)*tc, 0],
                          [np.sqrt(2)*tc, 0, np.sqrt(2)*tc],
                          [0, np.sqrt(2)*tc, U + biases[i]]]))
            paired = [(val, vec) for val, vec in zip(singval.eigenvalues,
                                                     singval.eigenvectors)]
            singlet_vals.append(sorted(paired, key=lambda x: x[0]))
            tripval = np.linalg.eig(
                np.array([[U + JMAX - biases[i], np.sqrt(2)*tc, 0],
                          [np.sqrt(2)*tc, 0, np.sqrt(2)*tc],
                          [0, np.sqrt(2)*tc, U + JMAX + biases[i]]]))
            paired = [(val, vec) for val, vec in zip(tripval.eigenvalues,
                                                     tripval.eigenvectors)]
            triplet_vals.append(sorted(paired, key=lambda x: x[0]))

        # arrays make for nicer slicing
        singlet_eigvals = np.zeros((NUM, 3))
        triplet_eigvals = np.zeros((NUM, 3))
        for i in range(NUM):
            singlet_eigvals[i] = np.array([elem[0] for elem in singlet_vals[i]])
            triplet_eigvals[i] = np.array([elem[0] for elem in triplet_vals[i]])

        # plot lines on graph
        # must use line_graph because we have no explicit funtion
        # line_graph does not check bounds so we must do it
        singlet_noodles = []
        triplet_noodles = []
        # ground state energy
        dots = singlet_eigvals[:,0]
        singlet_noodles.append(spaghetti.plot_line_graph(
            biases[dots>YMIN], dots[dots>YMIN], line_color=PURE_BLUE,
            add_vertex_dots=False))
        # (0, 2) part of middle energy
        dots = singlet_eigvals[:NUM//2,1]
        singlet_noodles.append(spaghetti.plot_line_graph(
            biases[:NUM//2][dots<YMAX], dots[dots<YMAX],
            line_color=PURE_BLUE, add_vertex_dots=False))
        # (2, 0) part of middle energy
        dots = singlet_eigvals[NUM//2:,1]
        singlet_noodles.append(spaghetti.plot_line_graph(
            biases[NUM//2:][dots<YMAX], dots[dots<YMAX],
            line_color=PURE_BLUE, add_vertex_dots=False))
        # biggest eigenenergy is never relevant and isn't graphed

        # repeat for triplet values
        dots = triplet_eigvals[:,0]
        triplet_noodles.append(spaghetti.plot_line_graph(
            biases[dots>YMIN], dots[dots>YMIN], line_color=PURE_RED,
            add_vertex_dots=False))
        dots = triplet_eigvals[:NUM//2,1]
        triplet_noodles.append(spaghetti.plot_line_graph(
            biases[:NUM//2][dots<YMAX], dots[dots<YMAX],
            line_color=PURE_RED, add_vertex_dots=False))
        dots = triplet_eigvals[NUM//2:,1]
        triplet_noodles.append(spaghetti.plot_line_graph(
            biases[NUM//2:][dots<YMAX], dots[dots<YMAX],
            line_color=PURE_RED, add_vertex_dots=False))

        # spaghetti and condiments
        dish = VGroup()
        dish.add(spaghetti, *singlet_noodles, *triplet_noodles)
        dish.add(spaghetti.get_axis_labels(
            x_label=r'\epsilon', y_label=r'\text{Eigenenergy}'))

        # display spaghetti diagram
        self.add(dish)
        self.wait(1)
        # move it to left side of screen
        self.play(dish.animate.scale(.4).to_edge(LEFT))
        self.wait(1)

        def bias2ind(x):
            """Returns index s.t. bias[index] is closest possible to x"""
            if not (np.abs(x) <= BIASRANGE):
                raise ValueError("bias2ind: bias out of bounds")
            return int((x + BIASRANGE) / (2 * BIASRANGE) * NUM)

        # variable index of bias that we currently display in animation
        t = ValueTracker(bias2ind(0))
        def getBias():
            """Returns bias corresponding to current t"""
            return biases[int(t.get_value())]

        # parameters for dot potential graph, chosen to look reasonable
        # x-value where potential graph starts
        IMAGESTART = 30
        # distance between dots
        DOTWIDTH = 30
        # SD of Gaussians
        SIGMA = 6
        # potential outside of dots
        FLATVAL = 1.2 * YMAX
        # parameters for magnitude of Gaussians
        SCALE = 180
        SCALE_T = 2.1
        dotxs = np.linspace(IMAGESTART, IMAGESTART + 3 * DOTWIDTH, 200)
        def potfunc(x):
            """Calculate made-up potential function, using Gaussians for each
            dot's potential because they look pretty"""
            dot1 = (SCALE + SCALE_T*getBias()) * norm(IMAGESTART + DOTWIDTH, SIGMA).pdf(x)
            dot2 = (SCALE - SCALE_T*getBias()) * norm(IMAGESTART + 2*DOTWIDTH, SIGMA).pdf(x)
            return FLATVAL - dot1 - dot2
        # create dynamic potential plot
        dotplots = always_redraw(
            lambda: spaghetti.plot_line_graph(dotxs, [potfunc(x) for x in dotxs],
                                              line_color=WHITE, add_vertex_dots=False))
        # current bias marker on spaghetti diagram
        biasMarker = always_redraw(lambda: DashedLine(spaghetti.c2p(getBias(), YMIN), spaghetti.c2p(getBias(), YMAX), color=WHITE))

        # makes sure marker energies are within range of plot
        def valid_val(vals, state):
            """vals: list of eigenvalues to check from
            state: which eigenvalue to choose, as stored in the eigenvalue table"""
            val = vals[int(t.get_value()),state]
            if YMIN < val < YMAX:
                return val
            else:
                # intentionally out of frame
                return 50

        # markers for eigenenergies
        singMarker1 = always_redraw(lambda: DashedLine(spaghetti.c2p(-BIASRANGE, valid_val(singlet_eigvals, 0)),
                                 spaghetti.c2p(IMAGESTART + 3*DOTWIDTH, valid_val(singlet_eigvals, 0)), color=BLUE))
        singMarker2 = always_redraw(lambda: DashedLine(spaghetti.c2p(-BIASRANGE, valid_val(singlet_eigvals, 1)),
                                 spaghetti.c2p(IMAGESTART + 3*DOTWIDTH, valid_val(singlet_eigvals, 1)), color=BLUE))
        tripMarker1 = always_redraw(lambda: DashedLine(spaghetti.c2p(-BIASRANGE, valid_val(triplet_eigvals, 0)),
                                 spaghetti.c2p(IMAGESTART + 3*DOTWIDTH, valid_val(triplet_eigvals, 0)), color=RED))
        tripMarker2 = always_redraw(lambda: DashedLine(spaghetti.c2p(-BIASRANGE, valid_val(triplet_eigvals, 1)),
                                 spaghetti.c2p(IMAGESTART + 3*DOTWIDTH, valid_val(triplet_eigvals, 1)), color=RED))
        # arrow and label showing bias between dot potentials
        biasArrow = always_redraw(lambda: DoubleArrow(spaghetti.c2p(IMAGESTART + DOTWIDTH * 1.5, potfunc(IMAGESTART+DOTWIDTH)),
                                                      spaghetti.c2p(IMAGESTART + DOTWIDTH * 1.5, potfunc(IMAGESTART+2*DOTWIDTH)),
                                                      buff=0, tip_length=.2))
        biasLabel = always_redraw(lambda: Tex(r'$\epsilon$', font_size=32).next_to(biasArrow, LEFT, buff=.2))
        # same for exchange energy. not currently used
        exchangeArrow = always_redraw(lambda: DoubleArrow(spaghetti.c2p(IMAGESTART + DOTWIDTH * .8, valid_val(singlet_eigvals, 0)),
                                                          spaghetti.c2p(IMAGESTART + DOTWIDTH * .8,
                                                                        valid_val(triplet_eigvals, 0) if valid_val(singlet_eigvals, 0) < 50 else 50),
                                                          buff=0, tip_length=.2))
        exchangeLabel = always_redraw(lambda: Tex(r'$J$', font_size=32).next_to(exchangeArrow, LEFT, buff=.2))

        # add dot potentials, bias marker on spaghetti diagram,
        # and bias arrow & label on dot potentials
        dish.add(dotplots, biasMarker, biasLabel, biasArrow)
        # move the bias around a bit
        self.play(t.animate.set_value(bias2ind(U)))
        self.wait(.1)
        self.play(t.animate.set_value(bias2ind(0)))
        self.wait(1)
        # remove arrow & label from potentials
        dish.remove(biasLabel, biasArrow)
        # add markers for eigenenergies
        dish.add(singMarker1, tripMarker1)

        def getAngle(vals, state):
            """Returns portion of 2pi radians corresponding to probability
            of finding a second electron in dot 1"""
            vec = vals[int(t.get_value())][state][1]
            # we ignore (0,2) as very unlikely ( < 10^-4)
            return vec[0]**2 / (vec[0]**2 + vec[1]**2) * 2 * PI

        # radius of electron circles
        RADIUS = 0.1
        def dote(vals, dot):
            """Draw the variable electron in dot dot according to the singlet/triplet vals"""
            angle = getAngle(vals, 0)
            color = PURE_BLUE if vals == singlet_vals else PURE_RED
            eigvals = singlet_eigvals if vals == singlet_vals else triplet_eigvals
            if dot == 1:
                return AnnularSector(0, RADIUS, angle, (PI - angle) / 2, color=color).next_to(
                    spaghetti.c2p(IMAGESTART+DOTWIDTH, valid_val(eigvals, 0)), RIGHT, buff=RADIUS*.6)
            else:
                return AnnularSector(0, RADIUS, 2*PI - angle, (PI + angle) / 2, color=color).next_to(
                    spaghetti.c2p(IMAGESTART+2*DOTWIDTH, valid_val(eigvals, 0)), RIGHT, buff=RADIUS*.6)

        # the electrons, shown as circle (sectors), in potentials
        singletGroundElectron1 = always_redraw(lambda: AnnularSector(0, RADIUS, 2 * PI, 0, color=PURE_BLUE).next_to(
            spaghetti.c2p(IMAGESTART+DOTWIDTH, valid_val(singlet_eigvals, 0)), LEFT, buff=RADIUS*.6))
        singletGroundElectron2a = always_redraw(lambda: dote(singlet_vals, 1))
        singletGroundElectron2b = always_redraw(lambda: dote(singlet_vals, 2))

        tripletGroundElectron1 = always_redraw(lambda: AnnularSector(0, RADIUS, 2 * PI, 0, color=PURE_RED).next_to(
            spaghetti.c2p(IMAGESTART+DOTWIDTH, valid_val(triplet_eigvals, 0)), LEFT, buff=RADIUS*.6))
        tripletGroundElectron2a = always_redraw(lambda: dote(triplet_vals, 1))
        tripletGroundElectron2b = always_redraw(lambda: dote(triplet_vals, 2))

        # just follow the captions
        caption = Tex('At $\epsilon=0$, one electron is in each dot, regardless of spin', font_size=40).next_to(dish, DOWN)
        dish.add(tripletGroundElectron1, tripletGroundElectron2a, tripletGroundElectron2b,
                 singletGroundElectron1, singletGroundElectron2a, singletGroundElectron2b)
        self.add(caption)
        self.wait(2)
        self.play(t.animate.set_value(bias2ind(U/2)), run_time=2.5)
        self.remove(caption)
        caption = Tex('At $\epsilon=U$ a spin-singlet pair begins to favor the (2,0) state', font_size=40).next_to(dish, DOWN)
        self.add(caption)
        self.play(t.animate.set_value(bias2ind(U)), run_time=5)
        self.wait(2)
        self.remove(caption)
        caption = Tex('Pauli Spin Blockade: when $U<\epsilon<U+J$, spin-singlets pairs are likely\nboth in dot 1, but spin-triplets remain separated',
                           font_size=40).next_to(dish, DOWN)
        self.add(caption)
        self.play(t.animate.set_value(bias2ind(1.25*U)), run_time=3)
        self.wait(5)
        self.remove(caption)
        caption = Tex('At $\epsilon>U+J$, both electrons will be found in dot 1 regardless of spin state', font_size=40).next_to(dish, DOWN)
        self.add(caption)
        self.play(t.animate.set_value(bias2ind(1.7*U)), run_time=4)
        self.wait(2)
        self.remove(caption)
        self.wait(2)

