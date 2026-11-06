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
            label(r"above $\leftrightarrow$ above: \ order is preserved, \ so a question about one becomes a question "
                  r"about the other", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Some of geometry's best tricks change what the objects are. <bookmark mark='a'/> Send the point a, b to "
            "the line y equals a x minus b. Each point on the left becomes a line on the right, in the same colour. "
            "<bookmark mark='b'/> Now take the line through two of the points: the white one. It becomes a single "
            "point, and that point is exactly where the two dual lines cross. <bookmark mark='c'/> And the map "
            "preserves above and below: a point above a line becomes a line above a point. So a question about "
            "points and the lines through them becomes a question about lines and their crossings, and sometimes "
            "the second is much easier to answer."
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
            label(r"$n$ lines cut the plane into $\binom{n}{2} + n + 1$ faces: \ the \textbf{arrangement}", font_size=22,
                  color=WHITE),
            label(r"the \textbf{zone theorem}: \ a new line meets only $O(n)$ edges of the faces it crosses, \ so the "
                  r"arrangement is built in $O(n^2)$", font_size=22, color=LAM),
            label(r"``are any three points collinear?'' \ becomes \ ``do any three dual lines meet?'': \ a vertex of "
                  r"the arrangement, \ $O(n^2)$", font_size=22, color=YES),
            label(r"nobody knows how to do it faster: \ the frontier chapter shows why \ (3SUM)", font_size=22,
                  color=NO),
            label(r"the same duality turns the hull of points into the intersection of half-planes, \ and the "
                  r"lifting map's Voronoi into an upper envelope \ (chapter 7)", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.34).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Dual lines meet in arrangements. <bookmark mark='a'/> n lines in general position cut the plane into "
            "about n squared over two faces. <bookmark mark='b'/> The zone theorem says a new line passes through "
            "faces whose boundaries have only order n edges in all, so the whole arrangement can be built "
            "incrementally in n squared time. <bookmark mark='c'/> That answers questions like this: are any three "
            "of n points on one line? Dualize, and ask whether any three dual lines pass through one vertex of the "
            "arrangement. <bookmark mark='d'/> n squared, and nobody knows how to do it fundamentally faster; the "
            "frontier chapter explains why that is no accident. <bookmark mark='e'/> The same duality turns the hull "
            "of a set of points into an intersection of half-planes, and it is the reason the Voronoi diagram is an "
            "upper envelope of planes."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
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
