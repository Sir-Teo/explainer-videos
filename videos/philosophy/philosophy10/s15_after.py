from __future__ import annotations

from videos.philosophy.philosophy10.common import *  # noqa: F403


class After(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"What became of Kant's examples", r"Was the synthetic a priori refuted?",
                            lit=(1829, 1919), part=PART)
        with self.voiceover("Chapter fourteen. What became of Kant's examples."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.geometry()
        self.eclipse()
        self.relativized()

    def geometry(self):
        head = label(r"Other geometries", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        three = VGroup(*[VGroup(label(a, font_size=26, color=c), label(b, font_size=20, color=GREY_A),
                                MathTex(e, font_size=30, color=c)).arrange(DOWN, buff=0.18) for a, b, e, c in (
            (r"Euclid", r"exactly one parallel", r"\alpha + \beta + \gamma = 180^\circ", WHITE),
            (r"Lobachevsky, \ Bolyai \ (1829--32)", r"infinitely many parallels", r"\alpha + \beta + \gamma < 180^\circ",
             SENSE),
            (r"Riemann \ (1854)", r"no parallels: \ a sphere", r"\alpha + \beta + \gamma > 180^\circ", REASON))]
        ).arrange(RIGHT, buff=0.8).move_to([0, 0.8, 0])
        rows = VGroup(label(r"each is consistent if Euclid's is: \ the parallel postulate is independent", font_size=24,
                            color=GOAL),
                      label(r"so which describes space \ is a question for physics, \ not for pure intuition",
                            font_size=24, color=BAD)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Kant's examples did not fare well. <bookmark mark='a'/>Within fifty years of the Critique, Nikolai "
            "Lobachevsky and János Bolyai built a geometry in which, through a point off a line, there are infinitely "
            "many parallels, and the angles of a triangle sum to less than two right angles. Bernhard Riemann, in "
            "1854, described geometries with no parallels at all, like the sphere's, where the angles sum to more. "
            "<bookmark mark='b'/>Each is consistent if Euclid's is: the parallel postulate is independent of the "
            "other axioms. <bookmark mark='c'/>So which geometry describes physical space cannot be settled by pure "
            "intuition. It became a question for physics."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in three], lag_ratio=0.6), run_time=6)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def eclipse(self):
        d = load("light")
        hc = history_card(1919, r"Arthur Eddington \& Frank Dyson", r"the eclipse expeditions to Sobral and Príncipe",
                          width=6.0, color=HIST).to_corner(UL, buff=0.35)
        sun = Circle(radius=0.9, color=GOAL, fill_color=GOAL, fill_opacity=0.25).move_to([-2.6, -0.8, 0])
        star = Dot([4.0, 1.4, 0], color=WHITE)
        seen = Dot([4.0, 1.75, 0], color=WHITE).set_opacity(0.45)
        earth = Dot([-6.3, -0.6, 0], color=REASON)
        ray = VMobject(color=WHITE, stroke_width=2).set_points_smoothly([earth.get_center(), [-3.0, 0.2, 0],
                                                                         star.get_center()])
        app = DashedLine(earth.get_center(), seen.get_center(), color=GREY_B, stroke_width=1.5)
        hd = [label(r"", font_size=22), label(r"deflection", font_size=22, color=P.CLAIM)]
        rows = [[label(r"`Newtonian' \ (Soldner, 1801)", font_size=22), MathTex(rf"{d['newton']:.2f}''", font_size=28)],
                [label(r"Einstein \ (general relativity, 1915)", font_size=22),
                 MathTex(rf"{d['einstein']:.2f}''", font_size=28, color=OK)],
                [label(r"Sobral, 1919", font_size=22), MathTex(rf"{d['sobral_1919']:.2f}''", font_size=28)],
                [label(r"Príncipe, 1919", font_size=22), MathTex(rf"{d['principe_1919']:.2f}''", font_size=28)]]
        grid = ValueGrid(hd, rows, col_w=[4.3, 2.3], cell_h=0.5, font_size=22).move_to([3.45, -1.4, 0])
        rcalc = label(r"starlight grazing the sun: \ the Reasoner computes $4GM/c^2R$", font_size=20,
                      color=GREY_A).next_to(grid, UP, buff=0.2)
        with self.voiceover(
            "Physics answered. <bookmark mark='a'/>Einstein's general relativity, in 1915, says that space-time is "
            "curved by matter, so that light passing the sun is bent. <bookmark mark='b'/>The Reasoner computes the "
            "prediction for starlight grazing the sun's edge: one point seven five seconds of arc, twice the value "
            "that a Newtonian particle of light would give. <bookmark mark='c'/>In 1919 Arthur Eddington and Frank "
            "Dyson sent expeditions to photograph stars near the eclipsed sun, from Brazil and from an island off "
            "Africa. They reported about two seconds and one point six, and announced that Einstein was right. "
            "<bookmark mark='d'/>Physical space is not Euclidean. The geometry Kant thought we know a priori is, of "
            "the world, false, and known to be false a posteriori."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(sun), FadeIn(earth), FadeIn(star), Create(ray))
            vo.wait_until("b")
            self.play(FadeIn(seen), Create(app), FadeIn(rcalc), FadeIn(grid.head), FadeIn(grid.rows_bg),
                      FadeIn(grid.rule), FadeIn(VGroup(*grid.cell[0])), FadeIn(VGroup(*grid.cell[1])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*grid.cell[2])), FadeIn(VGroup(*grid.cell[3])))
            vo.wait_until("d")
            self.play(Indicate(VGroup(*grid.cell[1]), color=OK))
        self.clear_scene()

    def relativized(self):
        head = label(r"What survives: \ a relativized a priori", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        rows = rows_at([
            (r"Frege (1884)", r"arithmetic is analytic, \ not synthetic \ (Part 9)"),
            (r"quantum mechanics", r"some events may have no determining cause \ (Part 26)"),
            (r"Reichenbach (1920)", r"two senses of a priori: \ necessary and unrevisable, \ or \textit{constitutive}"),
            (r"Carnap", r"frameworks are chosen, \ then reasoned within"),
            (r"Friedman (2001)", r"\textit{Dynamics of Reason}: \ each science has a constitutive a priori, \ which "
                                 r"changes in revolutions"),
        ], x_left=-6.3, x_right=-2.6, y0=1.8, dy=0.8, font_size=24, left_color=HIST)
        foot = label(r"Kant was right that experience needs a framework; \ wrong that the framework cannot change "
                     r"\ (Part 18)", font_size=24, color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The other examples fared no better. <bookmark mark='a'/>Frege argued that arithmetic is analytic, as "
            "Part 9 showed. <bookmark mark='b'/>And quantum mechanics suggests that some events have no determining "
            "cause, as Part 26 will show. <bookmark mark='c'/>But something survives. Hans Reichenbach, in 1920, "
            "distinguished two senses of a priori: necessary and unrevisable, which relativity refuted; and "
            "constitutive, the principles that make a physical theory's measurements meaningful in the first place, "
            "which every theory has. <bookmark mark='d'/>Rudolf Carnap made the frameworks a matter of choice. "
            "<bookmark mark='e'/>And Michael Friedman, in Dynamics of Reason, argued that each science has a "
            "constitutive a priori, which changes in scientific revolutions. <bookmark mark='f'/>Kant was right that "
            "experience needs a framework the mind brings to it, and wrong that the framework can never change. Part "
            "18 takes up the revolutions."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()
