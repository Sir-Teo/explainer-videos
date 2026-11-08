from __future__ import annotations

from videos.philosophy.philosophy18.common import *  # noqa: F403


class Models(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Models and idealization", r"How can a false model explain?", lit=(1983, 2013),
                            part=PART)
        with self.voiceover("Chapter thirteen. Models and idealization."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.pendulum()
        self.kinds()
        self.simulation()

    def pendulum(self):
        d = load("pendulum")["rows"]
        head = label(r"The idealized pendulum, \ and how false it is", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        pivot = np.array([-4.6, 2.0, 0])
        L = 2.6
        ang = ValueTracker(0.5)
        rod = always_redraw(lambda: Line(pivot, pivot + L * np.array([np.sin(ang.get_value()),
                                                                       -np.cos(ang.get_value()), 0]),
                                         color=GREY_B, stroke_width=3))
        bob = always_redraw(lambda: Dot(pivot + L * np.array([np.sin(ang.get_value()), -np.cos(ang.get_value()), 0]),
                                        radius=0.15, color=REAL))
        eqs = VGroup(MathTex(r"\ddot\theta = -\tfrac{g}{L}\sin\theta \;\approx\; -\tfrac{g}{L}\,\theta", font_size=30,
                             color=THEORY),
                     MathTex(r"T_0 = 2\pi\sqrt{L/g} \quad\text{(every amplitude)}", font_size=28, color=THEORY),
                     MathTex(r"T = \frac{T_0}{\mathrm{AGM}\big(1, \cos(\theta_0/2)\big)}", font_size=28, color=REAL)
                     ).arrange(DOWN, buff=0.25).move_to([-3.6, -1.6, 0])
        ax = Axes(x_range=[0, 180, 30], y_range=[1, 2.6, 0.5], x_length=5.6, y_length=3.4,
                  axis_config={"color": GREY_B, "font_size": 18, "include_numbers": True}).move_to([3.2, 0.2, 0])
        pts = [(r["amp"], r["ratio"]) for r in d]
        cv = series_plot(ax, [y for _, y in pts], REAL, xs=[x for x, _ in pts], width=4)
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.05, color=REAL) for x, y in pts])
        xl = label(r"amplitude \ (degrees)", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yl = label(r"$T / T_0$", font_size=18, color=REAL).next_to(ax, UP, buff=0.1).shift(LEFT * 2.2)
        r10 = next(r for r in d if r["amp"] == 10)["ratio"]
        r90 = next(r for r in d if r["amp"] == 90)["ratio"]
        note = stack([(r"at $10^\circ$: \ off by " + f"{(r10 - 1) * 100:.2f}" + r"\%", OK),
                      (r"at $90^\circ$: \ off by " + f"{(r90 - 1) * 100:.0f}" + r"\%", BAD),
                      (r"false everywhere, \ yet the explanation of a clock", GOAL)], font_size=19, aligned_edge=LEFT,
                     width=5.4).next_to(xl, DOWN, buff=0.25)
        with self.voiceover(
            "Science runs on models that are known to be false. <bookmark mark='a'/>The textbook pendulum replaces "
            "the sine of the angle by the angle itself. <bookmark mark='b'/>Then its period is the same at every "
            "amplitude: Galileo's isochronism, and the principle of the pendulum clock. "
            "<bookmark mark='c'/>The exact period divides that by the arithmetic-geometric mean of one and the "
            "cosine of half the amplitude. The Reasoner computes how false the idealization is. "
            "<bookmark mark='d'/>At ten degrees the error is a fifth of a percent. At ninety degrees it is eighteen "
            "percent, and near the top it diverges. <bookmark mark='e'/>The idealized model is false at every "
            "amplitude, and yet it explains why pendulum clocks keep time. Why do false models explain?"
        ) as vo:
            self.play(FadeIn(head), Create(rod), FadeIn(bob))
            self.play(ang.animate.set_value(-0.5), run_time=1, rate_func=there_and_back)
            vo.wait_until("a")
            self.play(Write(eqs[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]))
            vo.wait_until("c")
            self.play(Write(eqs[2]), Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(cv), FadeIn(dots), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(note[0]), FadeIn(note[1]))
            vo.wait_until("e")
            self.play(FadeIn(note[2]))
        self.clear_scene()

    def kinds(self):
        head = label(r"Three kinds of idealization \ (Weisberg, \ 2013)", font_size=30, color=CONN).to_edge(UP,
                                                                                                    buff=0.35)
        rows = [
            (r"Galilean", r"distort to make a problem tractable, \ and remove the distortions as methods improve: \ "
                          r"the frictionless plane", THEORY),
            (r"minimalist", r"include only the factors that make a difference: \ the Ising model of a magnet "
                            r"\ (Batterman and Rice, \ 2014)", OK),
            (r"multiple models", r"keep several incompatible models, \ each for a purpose: \ the liquid-drop and "
                                 r"shell models of the nucleus", REAL),
            (r"Cartwright \ (1983)", r"\textit{How the Laws of Physics Lie}: \ fundamental laws are true only of "
                                     r"models, \ not of the world", BAD),
            (r"Box \ (1976)", r"`all models are wrong, \ but some are useful'", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.6, x_text=-2.6)
        with self.voiceover(
            "Michael Weisberg distinguishes three kinds of idealization. <bookmark mark='a'/>Galilean "
            "idealization distorts to make a problem tractable, and expects to remove the distortion later: the "
            "frictionless plane. <bookmark mark='b'/>Minimalist idealization keeps only the factors that make a "
            "difference. The Ising model is a minimal model: it is false about every real magnet, and explains "
            "their critical behaviour because the falsehoods are irrelevant, as the last chapter showed. "
            "<bookmark mark='c'/>And multiple-models idealization keeps incompatible models side by side, like the "
            "liquid-drop and shell models of the atomic nucleus. <bookmark mark='d'/>Nancy Cartwright went further: "
            "the fundamental laws of physics are true only of models, never of the messy world. "
            "<bookmark mark='e'/>The statistician George Box's summary: all models are wrong, but some are useful."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def simulation(self):
        head = label(r"Simulations as experiments?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the practice", r"climate, \ galaxies, \ proteins: \ much of modern science is computed, \ not "
                              r"observed", THEORY),
            (r"the claim", r"a simulation is an experiment on a model \ (Parker, \ 2009; \ Morrison, \ 2009)", REAL),
            (r"the worry", r"an experiment can surprise us about the world; \ a simulation only about our equations",
             BAD),
            (r"the reply", r"Winsberg \ (2010): \ simulations need their own epistemology: \ verification, \ "
                           r"validation, \ robustness across models", OK),
            (r"this series", r"every number on screen comes from a simulation the Reasoner ran: \ what has it shown?",
             GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.6, x_text=-2.6)
        with self.voiceover(
            "Models increasingly come as computer simulations. <bookmark mark='a'/>Climate, galaxy formation and "
            "protein folding are studied largely by computation. <bookmark mark='b'/>Wendy Parker and Margaret "
            "Morrison argue that a simulation can be an experiment, performed on a model rather than on the world. "
            "<bookmark mark='c'/>The worry is that an experiment can surprise us about nature, while a simulation "
            "can only surprise us about our own equations. <bookmark mark='d'/>Eric Winsberg answers that "
            "simulations need their own epistemology: verifying the code, validating against data, and checking "
            "that the result is robust across different models. <bookmark mark='e'/>The question applies to this "
            "series: every number on screen comes from a simulation the Reasoner ran. What, exactly, has each one "
            "shown?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
