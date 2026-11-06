from __future__ import annotations

from videos.philosophy.philosophy25.common import *  # noqa: F403


class Relativity(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Special relativity", r"Is there a fact about what is happening now, \ far away?",
                            lit=(1905, 1908), part=PART)
        with self.voiceover("Chapter seven. Special relativity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.postulates()
        self.diagram()
        self.strikes()
        self.invariant()
        self.twins()

    def postulates(self):
        hc = history_card(1905, r"Albert Einstein", r"`On the Electrodynamics of Moving Bodies'", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = stack([(r"1. \ the laws of physics are the same in every inertial frame", SPACE),
                      (r"2. \ the speed of light is the same in every inertial frame", LIGHT),
                      (r"together: \ observers in relative motion disagree about lengths, \ durations, \ and "
                       r"simultaneity", BAD)], font_size=22, aligned_edge=LEFT, width=11.6, buff=0.3).move_to(
            [0, 0.9, 0])
        q = quote_card(r"Henceforth space by itself, \ and time by itself, \ are doomed to fade away into mere "
                       r"shadows, \ and only a kind of union of the two will preserve an independent reality.",
                       r"Hermann Minkowski", r"`Space and Time' \ (1908)", width=10.4, font_size=24).to_edge(DOWN,
                                                                                                buff=0.4)
        with self.voiceover(
            "In 1905 Einstein took two principles. <bookmark mark='a'/>The laws of physics are the same in every "
            "inertial frame: Galileo's ship, extended to electromagnetism. <bookmark mark='b'/>And the speed of light "
            "is the same in every inertial frame. <bookmark mark='c'/>Together they force a revolution: observers in "
            "relative motion disagree about lengths, about durations, and about which distant events are "
            "simultaneous. <bookmark mark='d'/>Three years later his former teacher Hermann Minkowski put it in "
            "geometric form: henceforth space by itself, and time by itself, are doomed to fade away into mere "
            "shadows, and only a kind of union of the two will preserve an independent reality."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(q))
        self.clear_scene()

    def diagram(self):
        head = label(r"A Minkowski diagram", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        o = np.array([-2.4, -0.6, 0])
        s = 1.1
        P = lambda t, x: o + s * np.array([x, t, 0])  # noqa: E731
        xa = Arrow(P(0, -2.8), P(0, 2.8), buff=0, color=GREY_B, stroke_width=2)
        ta = Arrow(P(-2.4, 0), P(2.6, 0), buff=0, color=GREY_B, stroke_width=2)
        xl = MathTex(r"x", font_size=26, color=GREY_A).next_to(P(0, 2.8), RIGHT, buff=0.1)
        tl = MathTex(r"t", font_size=26, color=GREY_A).next_to(P(2.6, 0), UP, buff=0.1)
        cone = VGroup(DashedLine(P(-2.4, -2.4), P(2.4, 2.4), color=LIGHT), DashedLine(P(-2.4, 2.4), P(2.4, -2.4),
                                                                                       color=LIGHT))
        cl = label(r"light", font_size=18, color=LIGHT).next_to(P(2.4, 2.4), RIGHT, buff=0.1)
        v = ValueTracker(0.0)

        def frame():
            vv = v.get_value()
            wl = Line(P(-2.3, -2.3 * vv), P(2.4, 2.4 * vv), color=MATTER, stroke_width=4)
            slices = VGroup(*[Line(P(c - 2.6 * vv, -2.6), P(c + 2.6 * vv, 2.6), color=TIME, stroke_width=2,
                                   stroke_opacity=0.9 if c == 0 else 0.45)
                              for c in (-1.6, -0.8, 0.0, 0.8, 1.6)])
            return VGroup(slices, wl)

        fr = always_redraw(frame)
        vlab = always_redraw(lambda: label(rf"$v = {v.get_value():.2f}\,c$", font_size=24, color=MATTER).move_to(
            o + np.array([2.2, 3.1, 0])))
        side = stack([(r"each point: \ an event, \ a place at a time", WHITE),
                      (r"dashed: \ light, \ at $45^\circ$ in every frame", LIGHT),
                      (r"orange: \ a moving observer's worldline", MATTER),
                      (r"teal: \ that observer's slices of simultaneity, \ tilting toward the light line", TIME),
                      (r"different observers, \ different `nows'", BAD)], font_size=21, aligned_edge=LEFT,
                     width=5.0, buff=0.28).move_to([3.9, -0.3, 0])
        with self.voiceover(
            "Draw it. <bookmark mark='a'/>Time runs up the page and one dimension of space runs across. Every point "
            "is an event: a place at a time. <bookmark mark='b'/>Light travels on the diagonals, at forty-five degrees, "
            "and by Einstein's second principle it does so for every observer. <bookmark mark='c'/>Now an observer "
            "moving to the right. Their worldline leans over. <bookmark mark='d'/>And their slices of simultaneity, "
            "the events they count as happening at the same time, tilt up toward the light line by the same angle. "
            "As the speed grows, the tilt grows. <bookmark mark='e'/>So observers in relative motion slice spacetime "
            "differently. There is no single now spread across space."
        ) as vo:
            self.play(FadeIn(head), GrowArrow(xa), GrowArrow(ta), FadeIn(xl), FadeIn(tl), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cone), FadeIn(cl), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(fr), FadeIn(vlab), FadeIn(side[2]))
            self.play(v.animate.set_value(0.35), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            self.play(v.animate.set_value(0.7), run_time=2.5)
            vo.wait_until("e")
            self.play(v.animate.set_value(-0.5), FadeIn(side[4]), run_time=2.5)
        fr.clear_updaters()
        vlab.clear_updaters()
        self.clear_scene()

    def strikes(self):
        d = load("simul")
        head = label(r"Two strikes of lightning", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"v", r"t'_A", r"t'_B", r"\text{first}"]
        rows = [[MathTex(f"{r['v']:+.1f}", font_size=24, color=MATTER), MathTex(f"{r['tA']:+.3f}", font_size=24),
                 MathTex(f"{r['tB']:+.3f}", font_size=24), MathTex(r"\text{" + r["first"] + "}", font_size=24,
                                                                   color=LIGHT)] for r in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[1.6, 2.0, 2.0, 2.6], cell_h=0.5, font_size=22).move_to([-2.6, -0.2, 0])
        f = MathTex(r"t' = \gamma\,(t - v x), \qquad \gamma = \frac{1}{\sqrt{1 - v^2}}", font_size=32,
                    color=ABS).next_to(head, DOWN, buff=0.35)
        side = stack([(r"A at $x = -1$, \ B at $x = +1$, \ both at $t = 0$ on the platform", WHITE),
                      (r"moving right: \ B first; \ moving left: \ A first", BAD),
                      (r"for events that could be causally connected, \ every frame agrees on the order", OK)],
                     font_size=21, aligned_edge=LEFT, width=4.6, buff=0.3).move_to([4.4, -0.4, 0])
        assert all(r["timelike_order_kept"] for r in d["rows"])
        with self.voiceover(
            "Make it concrete with Einstein's train. <bookmark mark='a'/>Lightning strikes at two points, A and B, "
            "one unit either side of an observer on the platform, at the same moment in the platform's frame. "
            "<bookmark mark='b'/>The Lorentz transformation gives the times in a moving frame. <bookmark mark='c'/>"
            "For a passenger moving right at three tenths of the speed of light, B strikes first; at six tenths, "
            "first by an even larger margin. For a passenger moving left, A strikes first. Which strike came first "
            "has no frame-independent answer. <bookmark mark='d'/>But this only happens for events too far apart for "
            "any signal to connect them. For pairs that could be cause and effect, every frame agrees on the order, "
            "which is why relativity never lets an effect precede its cause."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Write(f), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("c")
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def invariant(self):
        head = label(r"What every observer agrees on", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        ev = (2.0, 0.5)
        vals = [(v, *S.lorentz(v, [ev])[0]) for v in (0.0, 0.3, 0.6, -0.6)]
        hd = [r"v", r"t'", r"x'", r"t'^2 - x'^2"]
        rows = [[MathTex(f"{v:+.1f}", font_size=24, color=MATTER), MathTex(f"{t:.3f}", font_size=24),
                 MathTex(f"{x:+.3f}", font_size=24), MathTex(f"{t * t - x * x:.3f}", font_size=24, color=OK)]
                for v, t, x in vals]
        grid = ValueGrid(hd, rows, col_w=[1.6, 2.0, 2.0, 2.6], cell_h=0.5, font_size=22).move_to([-2.4, 0.0, 0])
        side = stack([(r"an event at $t = 2$, \ $x = 0.5$, \ seen from four frames", WHITE),
                      (r"time and place both change; \ the interval does not", OK),
                      (r"Minkowski spacetime: \ light cones and intervals are absolute; \ simultaneity is not", SPACE),
                      (r"the same lesson as chapter 6: \ the laws' symmetries fix the structure", GOAL)], font_size=21,
                     aligned_edge=LEFT, width=4.6, buff=0.3).move_to([4.4, -0.2, 0])
        with self.voiceover(
            "What is left that everyone agrees on? <bookmark mark='a'/>Take an event two units of time up and half a "
            "unit across, and look at it from four frames. <bookmark mark='b'/>Its time and its place both change "
            "from frame to frame. But t squared minus x squared, the spacetime interval, is the same in all of them: "
            "three point seven five. <bookmark mark='c'/>That is the structure of Minkowski spacetime: light cones "
            "and intervals are absolute, simultaneity is not. <bookmark mark='d'/>Chapter six's lesson again: the "
            "symmetries of the laws decide which structure is real. The Lorentz symmetry of Maxwell's equations "
            "dissolves absolute simultaneity, just as Galileo's symmetry dissolved absolute rest."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def twins(self):
        d = load("twins")
        head = label(r"The twins", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        T = d["T"]
        o, sc = np.array([-5.0, -3.1, 0]), 0.45            # screen origin of (t, x) = (0, 0); units per year

        def P(t, x):
            return o + np.array([x * sc, t * sc, 0])

        axes = VGroup(Arrow(P(-0.2, 0), P(T + 0.8, 0), buff=0, color=GREY_C, stroke_width=2,
                            max_tip_length_to_length_ratio=0.03),
                      Arrow(P(0, -3.2), P(0, 5.6), buff=0, color=GREY_C, stroke_width=2,
                            max_tip_length_to_length_ratio=0.03))
        tl = label(r"$t$ (years)", font_size=17, color=GREY_A).next_to(axes[0].get_end(), LEFT, buff=0.12)
        xl = label(r"$x$ (light-years)", font_size=17, color=GREY_A).next_to(axes[1], RIGHT, buff=0.08)
        home = Line(P(0, 0), P(T, 0), color=TIME, stroke_width=5)
        trip = d["rows"][3]
        assert trip["v"] == 0.8 and trip["tau"] == 6.0
        away = VMobject(stroke_color=MATTER, stroke_width=5).set_points_as_corners(
            [P(0, 0), P(T / 2, 0.8 * T / 2), P(T, 0)])
        wig = VGroup(*[VMobject(stroke_color=GREY_B, stroke_width=1.2, stroke_opacity=0.5).set_points_as_corners(
            [P(t, x) for t, x in ex]) for ex in d["examples"]])
        lab_h = label(r"stays home: \ 10 years", font_size=19, color=TIME).next_to(P(T, 0), RIGHT, buff=0.2).shift(
            UP * 0.15)
        lab_a = label(r"out and back at $0.8c$: \ 6 years", font_size=19, color=MATTER).next_to(P(T / 2, 4), RIGHT,
                                                                                              buff=0.15)
        f = MathTex(r"\tau = \int \sqrt{dt^2 - dx^2}", font_size=32, color=SPACE).move_to([5.2, 2.3, 0])
        hd = [r"v", r"\tau \text{ (years)}"]
        rows = [[MathTex(f"{r['v']:g}", font_size=24, color=MATTER), MathTex(f"{r['tau']:.3f}", font_size=24)]
                for r in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[1.4, 2.0], cell_h=0.4, font_size=20).move_to([2.0, 0.4, 0])
        assert d["n_wiggly"] == 200 and d["max_wiggly"] < T
        side = stack([(r"the straight worldline is the \textit{longest}", OK),
                      (rf"200 random worldlines between the same events: \ the most is {d['max_wiggly']:.3f}", WHITE),
                      (r"the asymmetry: \ one worldline is bent, \ the other straight", GOAL),
                      (r"proper time is path-dependent, \ like distance in space", SPACE)], font_size=19,
                     aligned_edge=LEFT, width=7.0, buff=0.22).move_to([3.3, -2.5, 0])
        with self.voiceover(
            "The interval also settles the most famous puzzle of relativity. <bookmark mark='a'/>One twin stays home "
            "for ten years. The other flies out at four fifths of the speed of light and comes back. "
            "<bookmark mark='b'/>The time a clock records along a worldline, its proper time, adds up the square "
            "root of d t squared minus d x squared. Along the bent path it comes to six years: the traveller "
            "returns four years younger. <bookmark mark='c'/>The Reasoner computes it for several speeds. "
            "<bookmark mark='d'/>Isn't the situation symmetric, since each twin sees the other moving? No. In "
            "Minkowski geometry the triangle inequality is reversed: of all the worldlines between two events, the "
            "straight one has the most proper time. The Reasoner draws two hundred random worldlines between the "
            "same two events: none reaches ten years. <bookmark mark='e'/>The asymmetry is geometric. One worldline "
            "is bent, the other straight, and proper time depends on the path, just as distance in space does."
        ) as vo:
            self.play(FadeIn(head), Create(axes), FadeIn(tl), FadeIn(xl))
            vo.wait_until("a")
            self.play(Create(home), FadeIn(lab_h))
            self.play(Create(away), FadeIn(lab_a))
            vo.wait_until("b")
            self.play(Write(f))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.3)
            vo.wait_until("d")
            self.play(FadeIn(side[0]))
            self.play(LaggedStart(*[Create(w) for w in wig], lag_ratio=0.1), FadeIn(side[1]), run_time=2)
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
            self.play(FadeIn(side[3]))
        self.clear_scene()
