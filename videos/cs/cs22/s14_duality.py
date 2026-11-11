from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs22.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, fit, load, mono, words)

COL5 = [DATA, YES, LAM, HEAD, CTRL]


class Duality(VoiceoverScene):
    def construct(self):
        self.card()
        self.dual()
        self.arrangements()
        self.ham()

    def card(self):
        card = chapter_card(13, r"Duality and the ham sandwich", r"Can points become lines?", lit=(1942, 1994),
                            extra=((1942, r"Stone--Tukey"), (1994, r"Lo, \ Matou\v{s}ek and Steiger")), part=PART)
        with self.voiceover("Chapter thirteen. Duality and the ham sandwich."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def dual(self):
        d = load("duality")
        P = [tuple(p) for p in d["dual_pts"]]
        head = label(r"Points become lines, \ lines become points", font_size=32).to_edge(UP, buff=0.3)
        L0, R0 = np.array([-3.6, -0.6, 0]), np.array([3.6, -0.6, 0])
        sc = 0.75

        def pl(p, o):
            return o + np.array([p[0] * sc, p[1] * sc, 0])
        axL = VGroup(Line(pl((-4, 0), L0), pl((4, 0), L0), color=GREY_D, stroke_width=1),
                     Line(pl((0, -3.2), L0), pl((0, 3.2), L0), color=GREY_D, stroke_width=1))
        axR = VGroup(Line(pl((-4, 0), R0), pl((4, 0), R0), color=GREY_D, stroke_width=1),
                     Line(pl((0, -3.2), R0), pl((0, 3.2), R0), color=GREY_D, stroke_width=1))
        pts = VGroup(*[Dot(pl(p, L0), radius=0.09, color=c) for p, c in zip(P, COL5)])

        def dual_line(p, color, width=2.4):
            a, b = p
            out = []
            for x in np.linspace(-4, 4, 161):
                y = a * x - b
                if abs(y) <= 3.2:
                    out.append(pl((x, y), R0))
            return Line(out[0], out[-1], color=color, stroke_width=width)
        lines = VGroup(*[dual_line(p, c) for p, c in zip(P, COL5)])
        ttl = VGroup(label(r"primal: \ points", font_size=22, color=GREY_A).next_to(axL, UP, buff=0.15),
                     label(r"dual: \ lines", font_size=22, color=GREY_A).next_to(axR, UP, buff=0.15))
        rule = MathTex(r"(a, b) \;\longleftrightarrow\; y = a x - b", font_size=32, color=WHITE).to_edge(DOWN, buff=0.9)
        # the line through points 0 and 3, and the intersection of their duals
        p0, p3 = P[0], P[3]
        m = (p3[1] - p0[1]) / (p3[0] - p0[0])
        c = p0[1] - m * p0[0]
        thr = Line(pl((-4, m * -4 + c), L0), pl((4, m * 4 + c), L0), color=WHITE, stroke_width=1.8)
        meet = Dot(pl((m, -c), R0), radius=0.1, color=WHITE)
        facts = VGroup(
            label(r"the line through two points $\leftrightarrow$ the point where their dual lines cross", font_size=21,
                  color=WHITE),
            label('point above line $\\leftrightarrow$ dual line below point; \\ incidence is preserved', font_size=21, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Map a point a, b to the line y equals a x minus b. <bookmark mark='a'/> Each coloured point becomes a line of the same colour. A nonvertical line y equals m x plus c maps to the point m, minus c. <bookmark mark='b'/> Incidence is preserved: two primal points on a line become two dual lines meeting at its dual point. <bookmark mark='c'/> Check the inequality carefully. If b is greater than m a plus c, then a m minus b is less than minus c. A point above a primal line therefore becomes a dual line below its dual point. This convention reverses the above relation; the algebra fixes the direction."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axL), FadeIn(axR), FadeIn(ttl), FadeIn(pts))
            vo.wait_until("a")
            self.play(FadeIn(rule), LaggedStart(*[Create(x) for x in lines], lag_ratio=0.25), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeOut(rule), Create(thr), FadeIn(facts[0]), Indicate(pts[0]), Indicate(pts[3]))
            self.play(FadeIn(meet, scale=1.8), Indicate(lines[0]), Indicate(lines[3]))
            vo.wait_until("c")
            self.play(FadeIn(facts[1]))
        self.wait(0.3)
        self.clear_scene()

    def arrangements(self):
        head = label(r"Arrangements of lines", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label('no parallels or triple intersections: \\ $\\binom n2+n+1$ arrangement faces', font_size=22,
                  color=WHITE),
            label(r"the \textbf{zone theorem}: \ a new line meets only $O(n)$ edges of the faces it crosses, \ so the "
                  r"arrangement is built in $O(n^2)$", font_size=22, color=LAM),
            label(r"``are any three points collinear?'' \ becomes \ ``do any three dual lines meet?'': \ a vertex of "
                  r"the arrangement, \ $O(n^2)$", font_size=22, color=YES),
            label('3SUM reductions give conditional barriers; \\ no unrestricted quadratic lower bound is claimed', font_size=22,
                  color=NO),
            label(r"the same duality turns the hull of points into the intersection of half-planes, \ and the "
                  r"lifting map's Voronoi into an upper envelope \ (chapter 7)", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.34).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "An arrangement partitions the plane with lines. <bookmark mark='a'/> With no parallels and no triple intersections, n lines give n choose two plus n plus one faces. Degeneracies reduce that count. <bookmark mark='b'/> The zone theorem bounds the total boundary complexity of faces crossed by another line by order n, supporting quadratic construction. <bookmark mark='c'/> Collinearity becomes concurrency under our duality. An arrangement algorithm that explicitly handles degeneracies can therefore detect three collinear distinct input points. <bookmark mark='d'/> Three-sum reductions explain conditional barriers to a truly subquadratic algorithm in stated models. They are not an unconditional quadratic lower bound, and logarithmic improvements are possible. <bookmark mark='e'/> Duality also links convex hulls, half-plane intersections and envelopes. Each transformation needs its incidence and sign conventions checked."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                if ln is not lines[0]:
                    self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def ham(self):
        d = load("duality")
        red = [tuple(p) for p in d["red"]]
        blue = [tuple(p) for p in d["blue"]]
        f, s = fit(red + blue, center=LEFT * 2.5 + DOWN * 0.4, w=7.4, h=5.2)
        head = label(r"The ham-sandwich cut", font_size=34).to_edge(UP, buff=0.3)
        R = VGroup(*[Dot(f(p), radius=0.09, color=NO) for p in red])
        B = VGroup(*[Dot(f(p), radius=0.09, color=DATA) for p in blue])
        p, q = d["p"], d["q"]
        dx, dy = q[0] - p[0], q[1] - p[1]
        a = (p[0] - 0.3 * dx, p[1] - 0.3 * dy)
        b = (q[0] + 0.3 * dx, q[1] + 0.3 * dy)
        cut = Line(f(a), f(b), color=HEAD, stroke_width=3)
        side = VGroup(
            label(r"two sets in the plane: \\ one line halves both at once", font_size=22, color=WHITE),
            label(r"Stone and Tukey (1942): \ in $d$ dimensions, \\ one hyperplane halves any $d$ sets", font_size=22,
                  color=HEAD),
            label(rf"here {len(red)} red and {len(blue)} blue: \ 4 of each \\ on either side, \ one of each on the line",
                  font_size=22, color=YES),
            label(r"found by trying lines through a red and a blue \\ point; \ Lo, \ Matou\v{s}ek and Steiger (1994): "
                  r"\\ $O(n)$, \ by duality and prune-and-search", font_size=21, color=LAM),
            label(r"used to split work evenly: \ partition trees, \\ fair division, \ balanced geometric "
                  r"divide-and-conquer", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        if side.width > 5.6:
            side.width = 5.6
            side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "One more theorem with a sandwich in its name. <bookmark mark='a'/> Scatter red points and blue points. "
            "Is there a single line that cuts both sets in half? <bookmark mark='b'/> Always. Arthur Stone and John "
            "Tukey proved in 1942 that in d dimensions one hyperplane halves any d sets: bread, ham and cheese in "
            "three. <bookmark mark='c'/> Here nine red and nine blue points, and a line with four of each on either "
            "side and one of each on it. <bookmark mark='d'/> We found it by trying lines through a red and a blue "
            "point; Lo, Matoušek and Steiger find it in linear time, by dualizing the points to lines and pruning. "
            "<bookmark mark='e'/> Halving cuts like this are how geometric divide-and-conquer splits its work evenly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(R), FadeIn(B))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cut), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()
