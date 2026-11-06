from __future__ import annotations

from videos.philosophy.philosophy10.common import *  # noqa: F403


class Geometry(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Descartes the geometer", r"Can thinking be made as certain as calculation?",
                            lit=(1637,), part=PART)
        with self.voiceover("Chapter two. Descartes the geometer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.coordinates()
        self.normals()
        self.method()

    def coordinates(self):
        hc = history_card(1637, r"René Descartes", r"\textit{La Géométrie}, \ an appendix to the \textit{Discourse}",
                          width=5.6, color=HIST).to_corner(UL, buff=0.35)
        ax = Axes(x_range=[-3, 3, 1], y_range=[-2, 2, 1], x_length=5.6, y_length=3.8, tips=False,
                  axis_config={"color": GREY_C, "stroke_width": 2}).move_to([-2.6, -0.8, 0])
        circ = ax.plot_parametric_curve(lambda t: np.array([1.5 * np.cos(t), 1.5 * np.sin(t), 0]),
                                        t_range=[0, TAU], color=REASON, stroke_width=3)
        line = ax.plot(lambda x: 0.5 * x + 0.5, x_range=[-3, 3], color=SENSE, stroke_width=3)
        eqs = VGroup(MathTex(r"x^2 + y^2 = \tfrac{9}{4}", font_size=34, color=REASON),
                     MathTex(r"y = \tfrac{1}{2}x + \tfrac{1}{2}", font_size=34, color=SENSE),
                     MathTex(r"\Rightarrow\; \tfrac{5}{4}x^2 + \tfrac{1}{2}x - 2 = 0", font_size=34, color=GOAL),
                     label(r"where a line meets a circle \ = \ the roots of a quadratic", font_size=22,
                           color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, -0.6, 0])
        with self.voiceover(
            "Descartes's certainty had a model, and he helped to build it. <bookmark mark='a'/>His Geometry of 1637 "
            "gave every point in the plane a pair of numbers, and every curve an equation. <bookmark mark='b'/>A "
            "circle becomes x squared plus y squared equals a constant. A line becomes y equals m x plus c. "
            "<bookmark mark='c'/>And the question where the line meets the circle becomes a question about the "
            "roots of a quadratic equation. Geometry turns into calculation, and calculation can be checked step by "
            "step."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Create(ax))
            vo.wait_until("b")
            self.play(Create(circ), FadeIn(eqs[0]))
            self.play(Create(line), FadeIn(eqs[1]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[2]), FadeIn(eqs[3]))
        self.clear_scene()

    def normals(self):
        d = load("normal")
        head = label(r"Descartes's method of normals", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[-2, 2, 1], y_range=[-0.5, 3, 1], x_length=5.2, y_length=4.6, tips=False,
                  axis_config={"color": GREY_C, "stroke_width": 2}).move_to([-3.4, -0.7, 0])
        par = ax.plot(lambda x: x * x, x_range=[-1.75, 1.75], color=SENSE, stroke_width=3)
        P = Dot(ax.c2p(1, 1), radius=0.07, color=WHITE)
        pl = MathTex("P = (1, 1)", font_size=26).next_to(P, DR, buff=0.1)
        k = ValueTracker(2.3)

        def circle():
            kk = k.get_value()
            r = np.sqrt(1 + (1 - kk) ** 2)
            return ax.plot_parametric_curve(lambda t: np.array([r * np.cos(t), kk + r * np.sin(t), 0]),
                                            t_range=[0, TAU], color=REASON, stroke_width=2.5)
        circ = always_redraw(circle)
        centre = always_redraw(lambda: Dot(ax.c2p(0, k.get_value()), radius=0.06, color=REASON))
        other = always_redraw(lambda: Dot(ax.c2p(np.sqrt(max(2 * k.get_value() - 2, 0)), 2 * k.get_value() - 2),
                                          radius=0.07, color=BAD))
        rows = VGroup(
            label(r"a circle centred at $(0, k)$ \ through $P$:", font_size=22),
            MathTex(r"x^2 + (y - k)^2 = r^2,\quad x^2 = y", font_size=30),
            MathTex(r"y^2 + (1 - 2k)\,y + k^2 - r^2 = 0", font_size=30, color=GOAL),
            label(r"its two roots: \ $y = 1$ \ (at $P$) \ and \ $y = 2k - 2$ \ (the red point)", font_size=22,
                  color=GREY_A),
            label(r"make them equal, \ a double root: \ the circle touches the curve", font_size=22, color=OK),
            MathTex(r"2k - 2 = 1 \;\Rightarrow\; k = \tfrac{3}{2}", font_size=32, color=OK),
            VGroup(label(r"the line from the centre to $P$ is the normal:", font_size=21, color=REASON),
                   label(r"slope $-\tfrac{1}{2}$, \ the tangent's $2$, \ product $-1$", font_size=21,
                         color=REASON)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)).arrange(DOWN, aligned_edge=LEFT,
                                                                                            buff=0.22)
        for r_ in rows:
            if r_.width > 6.2:
                r_.width = 6.2
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0.5, -0.5, 0], aligned_edge=LEFT)
        assert d["k"] == "3/2" and d["perpendicular"]
        normal = always_redraw(lambda: DashedLine(ax.c2p(0, k.get_value()), ax.c2p(1, 1), color=REASON,
                                                  stroke_width=2))
        with self.voiceover(
            "With coordinates, Descartes solved an old problem: how to find the line at right angles to a curve, its "
            "normal. <bookmark mark='a'/>Take the parabola y equals x squared, and the point P at one, one. "
            "<bookmark mark='b'/>Draw a circle through P, centred somewhere on the vertical axis, at height k. "
            "Substitute the parabola into the circle, and you get a quadratic in y. <bookmark mark='c'/>Its two roots "
            "are where circle and parabola cross: one at P, and the other, in red, at height two k minus two. "
            "<bookmark mark='d'/>Now slide the centre until the two roots coincide. A double root means the circle "
            "touches the curve at P instead of cutting it. That happens when k is three halves. "
            "<bookmark mark='e'/>The line from the centre to P is then the normal, and the Reasoner checks it: its "
            "slope times the tangent's slope is minus one. A problem about curves, solved by algebra."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(par), FadeIn(P), FadeIn(pl))
            vo.wait_until("b")
            self.play(Create(circ), FadeIn(centre), FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(other), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(k.animate.set_value(1.5), run_time=4)
            self.play(FadeIn(rows[4]), FadeIn(rows[5]))
            vo.wait_until("e")
            self.play(Create(normal), FadeIn(rows[6]))
        self.clear_scene()

    def method(self):
        head = label(r"The hope: \ a method for all knowledge", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rules = VGroup(*[VGroup(label(f"{i}.", font_size=24, color=REASON), label(t, font_size=24)).arrange(
            RIGHT, buff=0.2) for i, t in enumerate((
                r"accept nothing as true \ that I do not know clearly to be so",
                r"divide each difficulty into as many parts as possible",
                r"go from the simplest to the most complex, \ in order",
                r"make enumerations so complete \ that nothing is left out"), 1)]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.3, 0])
        foot = label(r"the four rules of the \textit{Discourse} (1637): \ geometry's method, \ for everything",
                     font_size=24, color=GOAL).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Descartes hoped the method of geometry would work everywhere. <bookmark mark='a'/>His Discourse on the "
            "Method gave four rules. Accept nothing as true that you do not clearly know to be so. Divide each "
            "difficulty into as many parts as possible. Proceed in order, from the simplest to the most complex. "
            "And make your enumerations so complete that nothing is left out. <bookmark mark='b'/>It is the method "
            "of the Geometry, offered for all of knowledge, and it is the same hope Leibniz would turn into the "
            "dream of calculation that opened this series."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rules], lag_ratio=0.6), run_time=7)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()
