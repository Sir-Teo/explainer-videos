from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs22.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Orient(VoiceoverScene):
    def construct(self):
        self.card()
        self.area()
        self.rounding()
        self.adaptive()

    def card(self):
        card = chapter_card(1, r"The one primitive", r"Left, right, or on the line?", lit=(1997, 2008),
                            extra=((1997, r"Shewchuk's predicates"), (2008, r"Kettner et al.")), part=PART)
        with self.voiceover("Chapter one. The one primitive."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def area(self):
        head = label(r"Orientation is the sign of an area", font_size=34).to_edge(UP, buff=0.35)
        P, Q, R = np.array([-5.6, -1.6, 0]), np.array([-1.6, -2.2, 0]), np.array([-2.6, 1.6, 0])
        tri = Polygon(P, Q, R, color=DATA, stroke_width=2.5).set_fill(DATA, 0.25)
        lab = VGroup(MathTex("p", font_size=32).next_to(P, LEFT, buff=0.1),
                     MathTex("q", font_size=32).next_to(Q, RIGHT, buff=0.1),
                     MathTex("r", font_size=32).next_to(R, UP, buff=0.1))
        arc = CurvedArrow(P + (Q - P) * 0.35 + UP * 0.35, P + (R - P) * 0.35 + RIGHT * 0.35, angle=1.2, color=HEAD,
                          stroke_width=2, tip_length=0.14)
        R2 = np.array([-3.2, -3.4, 0])
        side = VGroup(
            MathTex(r"\mathrm{orient}(p, q, r) = \det\begin{pmatrix} q_x - p_x & q_y - p_y \\ r_x - p_x & r_y - p_y"
                    r"\end{pmatrix}", font_size=32, color=LAM),
            label(r"twice the signed area of the triangle $pqr$", font_size=22, color=WHITE),
            label(r"$> 0$: \ $r$ is left of $p \to q$ \ (counter-clockwise)", font_size=22, color=DATA),
            label(r"$< 0$: \ right \ (clockwise); \ \ $= 0$: \ collinear", font_size=22, color=YES),
            label(r"hulls, \ sweeps, \ triangulations and polygon tests \\ are all built from this one sign", font_size=22,
                  color=HEAD),
            label(r"its cousin, \ \textbf{in-circle}, \ is a $3 \times 3$ determinant \ (chapter 6)", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        if side.width > 7.4:
            side.width = 7.4
            side.to_edge(RIGHT, buff=0.45)
        tri2 = Polygon(P, Q, R2, color=YES, stroke_width=2.5).set_fill(YES, 0.2)
        with self.voiceover(
            "Almost every algorithm in this part asks one question, over and over. <bookmark mark='a'/> Walk from p "
            "to q; is r on your left? The answer is the sign of a two by two determinant built from the differences "
            "of the coordinates. <bookmark mark='b'/> The determinant is twice the signed area of the triangle p q "
            "r: <bookmark mark='c'/> positive when the three points turn counter-clockwise, <bookmark mark='d'/> "
            "negative when they turn clockwise, and zero when they lie on one line. <bookmark mark='e'/> Convex "
            "hulls, sweeps, triangulations and point-in-polygon tests are all built from this sign. <bookmark "
            "mark='f'/> Its cousin, the in-circle test, asks whether a point lies inside the circle through three "
            "others; it is a three by three determinant, and we will meet it with Delaunay."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(tri), FadeIn(lab), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), tri.animate.set_fill(DATA, 0.45))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Create(arc))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Transform(tri, tri2), lab[2].animate.next_to(R2, DOWN, buff=0.1),
                      FadeOut(arc))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.wait(0.3)
        self.clear_scene()

    def rounding(self):
        head = label(r"Why floating point gets it wrong", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            MathTex(r"\underbrace{(q_x - p_x)(r_y - p_y)}_{a} \;-\; \underbrace{(q_y - p_y)(r_x - p_x)}_{b}",
                    font_size=34, color=LAM),
            label(r"each subtraction and product rounds to the nearest double: \ relative error $\varepsilon = 2^{-53}$",
                  font_size=22, color=WHITE),
            label(r"near a line, \ $a$ and $b$ almost cancel: \ the rounding errors can be larger than $a - b$ itself",
                  font_size=22, color=NO),
            MathTex(r"|\,\text{error}\,| \;\le\; (3 + 16\varepsilon)\,\varepsilon\,(|a| + |b|)", font_size=34,
                    color=YES),
            label(r"Shewchuk (1997): \ a proved bound, \ so a large answer can be trusted", font_size=22, color=YES),
            label(r"Kettner et al. (2008): \ with wrong signs, \ incremental hulls lose points, \ loop, \ or come out "
                  r"non-convex", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Why does it fail? <bookmark mark='a'/> The determinant is a difference of two products, a minus b. "
            "<bookmark mark='b'/> Each subtraction and each product is rounded to the nearest double, with a "
            "relative error of about one part in nine million billion. <bookmark mark='c'/> Near a line, a and b "
            "are almost equal, and their difference is tiny: smaller than the rounding errors made computing "
            "them. The sign of the result is then noise. <bookmark mark='d'/> But the error can be bounded. "
            "Jonathan Shewchuk proved that it is at most about three epsilon times the sizes of a and b. <bookmark "
            "mark='e'/> So when the computed answer is bigger than that bound, its sign is certainly right. "
            "<bookmark mark='f'/> When it isn't, ignoring the problem is dangerous: Kettner's paper shows the "
            "textbook incremental hull losing points, looping, and returning a polygon that is not convex."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def adaptive(self):
        o = load("orient")
        head = label(r"Adaptive exact predicates", font_size=34).to_edge(UP, buff=0.35)
        steps = VGroup(
            label(r"1. \ compute $a - b$ in floating point", font_size=23, color=WHITE),
            label(r"2. \ if $|a - b| \ge$ the bound: \ \textbf{done}, \ the sign is certain", font_size=23, color=YES),
            label(r"3. \ otherwise: \ redo it exactly \ (Shewchuk: \ expansions of doubles; \ here, \ rationals)",
                  font_size=23, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(head, DOWN, buff=0.45)
        rows = []
        for r in o["rows"]:
            rows.append([r["inputs"], f"{r['float_ns']:.0f} ns", words(r["float_wrong"]), (f"{r['adaptive_ns']:.0f} ns" if r['adaptive_ns'] < 1000 else
                                                                         f"{r['adaptive_ns'] / 1000:.1f} $\\mu$s"),
                         f"{100 * r['exact_share']:.0f}\\%", f"{r['exact_ns'] / 1000:.1f} µs".replace("µ", r"$\mu$")])
        tab = grid_table([r"20,000 tests", r"float", r"float wrong", r"adaptive", r"needed exact", r"always exact"],
                         rows, widths=[2.8, 1.5, 2.0, 1.8, 2.2, 2.2], row_h=0.5, font_size=21, mono_cols=(),
                         colors=[[WHITE, GREY_A, NO, YES, HEAD, GREY_A]] * len(rows))
        tab.next_to(steps, DOWN, buff=0.5).set_x(0)
        foot = VGroup(
            label(r"on ordinary input the filter almost never fails: \ exactness for the price of one comparison",
                  font_size=21, color=YES),
            label(r"integer coordinates below $2^{26}$ make the double computation exact; \ this part's algorithms use "
                  r"integers and Python's exact arithmetic", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "That gives Shewchuk's adaptive predicates. <bookmark mark='a'/> Compute the determinant in floating "
            "point. <bookmark mark='b'/> If it is bigger than the error bound, stop: the sign is certain. <bookmark "
            "mark='c'/> Otherwise compute it again exactly. Shewchuk does this with expansions, sums of doubles that "
            "carry every lost bit; we use rational numbers, which are slower but simple. <bookmark mark='d'/> We "
            "measured twenty thousand tests of each kind. On random points, plain floating point is never wrong, "
            "and the adaptive test never needs its exact stage, so it costs about twice a bare multiplication. On "
            "nearly collinear points, floating point is wrong almost one time in five, and the adaptive test falls "
            "back to exact arithmetic seven times in ten. <bookmark mark='e'/> The point is that you pay for "
            "exactness only where the answer is in doubt. <bookmark mark='f'/> Another route is to keep coordinates "
            "as small integers, for which the computation is exact; the algorithms in this part do that, with "
            "Python's unbounded integers."
        ) as vo:
            self.play(FadeIn(head))
            for mk, st in zip("abc", steps):
                vo.wait_until(mk)
                self.play(FadeIn(st, shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.5))
            vo.wait_until("e")
            self.play(FadeIn(foot[0]))
            vo.wait_until("f")
            self.play(FadeIn(foot[1]))
        self.wait(0.3)
        self.clear_scene()
