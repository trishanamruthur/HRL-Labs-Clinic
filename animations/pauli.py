from manim import *
import numpy as np

source = 1
gate1_1 = 0
gate1_2s = 1.5
gate1_2t = 2.5
gate2_1 = -2
gate2_2s = -.5
gate2_2t = .5
drain = -1

class PauliSpinBlockade(Scene):
    def construct(self):
        # Rectangles (Dots & Baths)
        rect1 = Rectangle(width=2.0, height=6.0,color=GRAY_D)
        rect1.set_fill(GRAY_D,opacity=0.35)
        rect2 = Rectangle(width=1.0, height=6.0,color=GRAY_D)
        rect2.set_fill(GRAY_D,opacity=0.35)
        rect3 = Rectangle(width=1.0, height=6.0,color=GRAY_D)
        rect3.set_fill(GRAY_D,opacity=0.35)
        rect4 = Rectangle(width=2.0, height=6.0,color=GRAY_D)
        rect4.set_fill(GRAY_D,opacity=0.35)
        rects = VGroup(rect1,rect2,rect3, rect4).arrange(buff=0.3)

        # energy levels
        fermiSource = Line([-3.45, source, 0], [-1.45, source, 0])
        
        gate1 = VGroup()
        gate1.add(Line([-1.15, gate1_1, 0], [-.15, gate1_1, 0]))
        gate1.add(Line([-1.15, gate1_2s, 0], [-.15, gate1_2s, 0]))
        gate1.add(Line([-1.15, gate1_2t, 0], [-.15, gate1_2t, 0]))

        gate2 = VGroup()
        gate2.add(Line([.15, gate2_1, 0], [1.15, gate2_1, 0]))
        gate2.add(Line([.15, gate2_2s, 0], [1.15, gate2_2s, 0]))
        gate2.add(Line([.15, gate2_2t, 0], [1.15, gate2_2t, 0]))

        fermiDrain = Line([1.45, drain, 0], [3.45, drain, 0])

        Uarrow = DoubleArrow([-.85, gate1_1, 0], [-.85, gate1_2s, 0], buff=0, tip_length=.2)
        Jarrow = DoubleArrow([-.45, gate1_2s, 0], [-.45, gate1_2t, 0], buff=0, tip_length=.2)
        Ulabel = Tex('U', font_size=32).next_to(Uarrow, LEFT, buff=.24)
        Jlabel = Tex('J', font_size=32).next_to(Jarrow, RIGHT, buff=.24)

        biasArrow = DoubleArrow([0, gate1_1, 0], [0, gate2_1, 0], buff=0, tip_length=.2)
        biasLabel = Tex(r'$\epsilon$', font_size=32).next_to(biasArrow, RIGHT, buff=.15)

        singlet1 = Arrow([4, 1, 0], [4, 1.25, 0], tip_length=.05, color='blue')
        singlet2 = Arrow([4.1, 1.25, 0], [4.1, 1, 0], tip_length=.05, color='blue')
        singletLabel = Tex(r'Spin-singlet\\electron pair', font_size=32).next_to(singlet2, RIGHT)
        newElectron = Arrow([-2.45, source-.125, 0], [-2.45, source+.125, 0], tip_length=.05, color='yellow')
        flowText = Tex('Electrons can move through dots', font_size=32).next_to([0,3,0], UP)

        triplet1 = Arrow([4, 1, 0], [4, 1.25, 0], tip_length=.05, color='red')
        triplet2 = Arrow([4.1, 1, 0], [4.1, 1.25, 0], tip_length=.05, color='red')
        tripletLabel = Tex(r'Spin-triplet\\electron pair', font_size=32).next_to(triplet2, RIGHT)
        blockadeText = Tex('Blockade: No current can flow', font_size=32).next_to([0,3,0], UP)

        self.add(rects, fermiSource, gate1, gate2, fermiDrain)
        self.play(Create(Uarrow))
        self.add(Ulabel)
        self.play(Create(Jarrow))
        self.add(Jlabel)
        self.play(Create(biasArrow))
        self.add(biasLabel)
        self.wait(2)
        self.remove(Ulabel, Jlabel, Uarrow, Jarrow, biasArrow, biasLabel)
        self.add(singlet1, singlet2, singletLabel)
        self.wait(2)
        self.remove(singletLabel)
        self.play(MoveAlongPath(singlet1, Line([4, 1, 0], [-.65, gate1_1, 0])))
        self.play(MoveAlongPath(singlet2, Line([4.1, 1.25, 0], [.65, gate2_1, 0])))
        self.wait(1)
        self.add(newElectron)
        self.wait(1)
        self.add(flowText)
        self.play(MoveAlongPath(singlet1, Line([-.65, gate1_1, 0], [.65, gate2_2s, 0])))
        self.wait(1)
        self.play(MoveAlongPath(singlet1, Line([.65, gate2_2s, 0], [2.45, drain, 0])))
        self.play(MoveAlongPath(newElectron, Line([-2.45, source, 0], [-.65, gate1_1, 0])))
        self.wait(1)
        self.remove(singlet1)
        self.play(MoveAlongPath(newElectron, Line([-.65, gate1_1, 0], [.65, gate2_2s, 0])))
        self.wait(1)
        self.play(MoveAlongPath(newElectron, Line([.65, gate2_2s, 0], [2.45, drain, 0])))
        self.wait(1)
        self.remove(newElectron, singlet2, flowText)
        newElectron.move_to([-2.45, source, 0])
        newElectron.rotate(np.pi)
        self.add(triplet1, triplet2, tripletLabel)
        self.wait(2)
        self.remove(tripletLabel)
        self.play(MoveAlongPath(triplet1, Line([4, 1, 0], [-.65, gate1_1, 0])))
        self.play(MoveAlongPath(triplet2, Line([4.1, 1, 0], [.65, gate2_1, 0])))
        self.wait(1)
        self.add(newElectron)
        self.wait(1)
        self.add(blockadeText)
        self.play(MoveAlongPath(triplet1, Line([-.65, gate1_1, 0], [-.65+1.3/4, gate1_1+(gate2_2t-gate1_1)/4, 0])))
        self.play(MoveAlongPath(triplet1, Line([-.65+1.3/4, gate1_1+(gate2_2t-gate1_1)/4, 0], [-.65, gate1_1, 0])))
        self.wait(1)
        self.play(MoveAlongPath(newElectron, Line([-2.45, source, 0], [-2.45+1.8/4, source+(gate1_2s-source)/4, 0])))
        self.play(MoveAlongPath(newElectron, Line([-2.45+1.8/4, source+(gate1_2s-source)/4, 0], [-2.45, source, 0])))
        self.remove(newElectron, triplet2, blockadeText)