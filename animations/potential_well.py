%%manim -qm PotentialWell

class PotentialWell(Scene):
    def construct(self):
        graph = ImplicitFunction(
        lambda x, y: -(x**2-2)*(x**2-2)+2 -y,color=YELLOW)

        dot = Dot(color=BLUE).shift(3*LEFT)



        # Rectangles (Gates)
        rect1 = Rectangle(width=2.0, height=6.0,color=GRAY_D)
        rect1.set_fill(GRAY_D,opacity=0.5)
        rect2 = Rectangle(width=1.0, height=6.0,color=GRAY_D)
        rect2.set_fill(GRAY_D,opacity=0.5)
        rect3 = Rectangle(width=2.0, height=6.0,color=GRAY_D)
        rect3.set_fill(GRAY_D,opacity=0.5)
        rects = VGroup(rect1,rect2,rect3).arrange(buff=0.3)
        rects.set_z_index(graph.z_index - 1 )

        # Labels (Gates)
        text1 = Text('T1')
        text2 = Text('M1')
        text3 = Text('T2')
        labels = VGroup(text1, text2, text3).arrange(buff=1.3)
        labels.move_to(3.5*UP)

        # Labels 
        source = Text('Source').scale(1).move_to([-5,2,0])
        drain = Text('Drain').scale(1).move_to([5,2,0])

        # Energy Levels
        line1 = Line(0,1, color=RED)
        line1.put_start_and_end_on([-0.75,0,0], [0.75,0,0])
        line2 = Line(0,1, color=RED)
        line2.put_start_and_end_on([-10,0,0], [-1.9,0,0])
        line3 = Line(0,1, color=RED)
        line3.put_start_and_end_on([1.9,0,0], [10,0,0])
        redlabel = Text("Fermi Energy Levels", color=RED).scale(0.5).move_to([-5,-0.5,0])
        energy = VGroup(line1,line2,line3,redlabel)

        self.add(graph, source, energy, drain, rects, labels)
        self.add(rects, labels)

        # self.play(line3.put_start_and_end_on([1.9,3,0], [10,0,0]))
        line3_new = Line(0,1, color=RED).put_start_and_end_on([1.9,3,0], [10,3,0])
        
        # Regular energy
        
        self.wait(1)
        self.play(Create(dot))
        self.wait(1)
        self.play(Rotating(dot, radians=-PI, about_point=[-1.5,0,0], run_time=2))
        self.wait()
        self.play(Rotating(dot, radians=-PI, about_point=[1.5,0,0], run_time=2))
        self.wait()
        self.play(FadeOut(dot))

        # Lower energy 
        dot.move_to([-3,0,0])
        self.wait(2)
        self.play(line1.animate.shift(0.25*DOWN))
        self.play(Create(dot))
        self.wait(1)
        self.play(Rotating(dot, radians=-PI, about_point=[-1.5,0,0], run_time=2))
        self.wait()
        self.play(line1.animate.shift(0.25*UP))
        self.wait()
        self.play(Rotating(dot, radians=-PI, about_point=[1.5,0,0], run_time=2))
        self.wait()
        self.play(FadeOut(dot))

        # Higher ending energy  (coulomb blockade)
        dot.move_to([-3,0,0])
        self.wait(2)
        self.play(line1.animate.shift(0.25*UP))
        self.play(Create(dot))
        self.wait()
        moretext = Text("dot unable to move", color=RED).scale(0.5).move_to([-5,0.5,0])
        self.play(Create(moretext))
        self.wait()
        self.play(FadeOut(moretext))
        self.play(FadeOut(dot))