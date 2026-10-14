from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis4.common import load, plain_axes, polyline, square_axes


class Contraction(VoiceoverScene):
    def construct(self):
        self.card()
        self.cobweb()
        self.proof()
        self.complete()
        self.newton()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(4, r"The contraction principle", r"When does iterating a map find a solution?", lit=(),
                            part=4)
        with self.voiceover("Chapter four: the contraction principle, the engine of this part."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def cobweb(self):
        d = load("contraction")
        x, fix, errs, bound, c = d["x"], float(d["fix"]), d["errs"], d["bound"], float(d["c"])
        ax = square_axes([0, 1.1, 0.5], [0, 1.1, 0.5], 4.9, numbers=True, font_size=20,
                         x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                         y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.4, -0.6, 0])
        t = np.linspace(0, 1.1, 300)
        cg = polyline(ax, t, np.cos(t), color=C.FUNC, stroke_width=3.5)
        dg = polyline(ax, t, t, color=GREY_B, stroke_width=2.5)
        cl = MathTex(r"y = \cos x", font_size=28, color=C.FUNC).move_to(ax.c2p(0.27, 0.78))  # under the curve, left of the web
        dl = MathTex(r"y = x", font_size=28, color=GREY_B).next_to(ax.c2p(0.3, 0.12), RIGHT, buff=0.05)  # below the diagonal
        web = VGroup()
        for k in range(9):
            a, b = x[k], x[k + 1]
            web.add(Line(ax.c2p(a, a if k else 0), ax.c2p(a, b), color=C.EPS, stroke_width=2.5))
            web.add(Line(ax.c2p(a, b), ax.c2p(b, b), color=C.EPS, stroke_width=2.5))
        fdot = Dot(ax.c2p(fix, fix), radius=0.08, color=WHITE)
        head = VGroup(label(r"Solve $\cos x = x$ by iterating: \ $x_{n+1} = \cos x_n$", font_size=34),
                      label(r"on $[0, 1]$, \ $|\cos' x| = |\sin x| \le \sin 1 = c$: \ every distance shrinks by $c$",
                            font_size=24, color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        tab = VGroup(MathTex(r"n", r"x_n", r"|x_n - x^*|", r"\frac{c^n}{1 - c}|x_1 - x_0|",
                             font_size=26, color=GREY_A))
        for n in (0, 1, 2, 3, 5, 10, 20, 30):
            tab.add(MathTex(rf"{n}", rf"{x[n]:.6f}", rf"{sci(float(errs[n]), 2)}", rf"{sci(float(bound[n]), 2)}",
                            font_size=26))
        # rows on a fixed pitch (the superscripts in some rows would otherwise space them unevenly)
        y_top = 1.55
        for i, row in enumerate(tab):  # each row placed by its index n, which has no superscript
            row.shift(UP * (y_top - (0.0 if i == 0 else 0.68 + 0.42 * (i - 1)) - row[0].get_y()))
        assert tab[0].get_bottom()[1] > tab[1].get_top()[1] + 0.05
        x0 = 0.6
        cols_x = (0.0, 0.55, 2.0, 3.75)  # fixed column starts (scene units from the table's left edge)
        for row in tab:
            for j in range(4):
                row[j].set_x(x0 + cols_x[j] + row[j].width / 2)
        assert tab.get_right()[0] <= 6.6 and tab.get_top()[1] < 2.2
        fl = MathTex(rf"x^* = {fix:.10f}", font_size=30, color=C.EPS).next_to(tab, DOWN, buff=0.3)
        assert np.all(errs <= bound + 1e-15) and abs(c - math.sin(1)) < 1e-15
        with self.voiceover(
            "<bookmark mark='a'/> To solve cosine of x equals x, just iterate: start anywhere, apply the cosine, and "
            "apply it again. <bookmark mark='b'/> On the graph, bounce between the curve and the diagonal: the path "
            "spirals in on the crossing. <bookmark mark='c'/> Why it works: on this interval the cosine's slope is at "
            "most sine of one, about 0.84, so each application shrinks distances by that factor. The errors shrink "
            "geometrically, and the theorem we're about to prove even predicts a bound for them in advance, the last "
            "column. <bookmark mark='d'/> The solution is 0.7390851332, the only one there is."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), Create(dg), FadeIn(dl))
            vo.wait_until("a")
            self.play(Create(cg), FadeIn(cl))
            vo.wait_until("b")
            self.play(Create(web), run_time=4.0, rate_func=linear)
            self.play(FadeIn(fdot, scale=1.5))
            vo.wait_until("c")
            self.play(FadeIn(head[1]), FadeIn(tab[0]))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.25), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(fl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proof(self):
        head = VGroup(label(r"The contraction principle", font_size=34),
                      VGroup(label(r"$X$ complete, \ $d(\varphi x, \varphi y) \le c\, d(x, y)$ with $c < 1$ \ "
                                   r"$\Rightarrow$ \ exactly one fixed point", font_size=26, color=C.EPS),
                             label(r"(Rudin 9.23)", font_size=22, color=GREY_B)).arrange(RIGHT, buff=0.25,
                                                                                     aligned_edge=DOWN)
                      ).arrange(DOWN, buff=0.14).to_edge(UP, buff=0.3)
        pm = ProofMap([r"steps shrink like $c^n$", r"so $(x_n)$ is Cauchy", r"$X$ complete: \ $x_n \to x$",
                       r"$\varphi(x) = x$; \ unique"], font_size=22, width=2.9, buff=0.28)
        pm.next_to(head, DOWN, buff=0.2)
        assert pm.width <= 13.2
        unit = 1.25
        ax = square_axes([-2.6, 2.6, 1], [-2.0, 2.0, 1], unit)
        ax.move_to([-3.4, 0, 0]).shift(UP * (pm.get_bottom()[1] - 0.35 - ax.c2p(0, 1.5)[1]))
        ax.set_opacity(0)
        star = np.array([0.5, -0.2])
        c, th = 0.62, math.radians(48)
        R = c * np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
        pts = [np.array([-2.0, 1.4])]
        for _ in range(10):
            pts.append(star + R @ (pts[-1] - star))
        pts = np.array(pts)
        d10 = np.linalg.norm(pts[1] - pts[0])
        for n in range(len(pts)):
            assert np.linalg.norm(pts[n] - star) <= c**n / (1 - c) * d10 + 1e-12
        dots = VGroup(*[Dot(ax.c2p(*p), radius=0.07 if n < 6 else 0.05, color=C.SEQ) for n, p in enumerate(pts)])
        steps = VGroup(*[Line(ax.c2p(*pts[n]), ax.c2p(*pts[n + 1]), color=C.EPS, stroke_width=3) for n in range(10)])
        xl = MathTex(r"x_0", font_size=28).next_to(dots[0], UL, buff=0.05)
        fixd = Dot(ax.c2p(*star), radius=0.09, color=WHITE)
        rows = [
            MathTex(r"d(x_{n+1}, x_n)", r"\le", r"c^n\, d(x_1, x_0)", font_size=30),
            MathTex(r"d(x_m, x_n)", r"\le", r"\frac{c^n}{1 - c}\, d(x_1, x_0)", font_size=30),
            MathTex(r"\varphi(x)", r"=", r"\lim \varphi(x_n) = \lim x_{n+1} = x", font_size=30),
            MathTex(r"d(x, y)", r"=", r"d(\varphi x, \varphi y) \le c\, d(x, y) \;\Rightarrow\; x = y", font_size=30),
        ]
        whys = [why(r"$\varphi$ shrinks every distance by $c$"), why(r"triangle inequality, geometric series: \ Cauchy"),
                why(r"$\varphi$ is continuous"), why(r"uniqueness")]
        step = ladder(self, rows, whys, keep=4, top=pm.get_bottom()[1] - 0.35, buff=0.42, x=2.4)
        lad_left = min(m_.get_left()[0] for m_ in rows + [w_ for w_ in whys if w_ is not None])
        # the Cauchy discs: every later point lies within c^n / (1 - c) d(x_1, x_0) of x_n. The first ones are
        # larger than the frame; show those that fit beside the derivation, which shrink to nothing.

        def disc_box(n):
            cen, r = ax.c2p(*pts[n]), unit * c**n / (1 - c) * d10
            return cen[0] - r, cen[0] + r, cen[1] - r, cen[1] + r

        fit = [n for n in range(9) if disc_box(n)[0] > -7.0 and disc_box(n)[1] < lad_left - 0.15
               and disc_box(n)[2] > -3.95 and disc_box(n)[3] < pm.get_bottom()[1] - 0.05]
        assert fit == list(range(fit[0], 9)) and fit[0] <= 3, fit
        for n in fit:  # each disc does hold every later point, and the fixed point
            r = c**n / (1 - c) * d10
            assert np.all(np.linalg.norm(pts[n:] - pts[n], axis=1) <= r) and np.linalg.norm(star - pts[n]) <= r
        discs = [Circle(radius=unit * c**n / (1 - c) * d10, color=C.CONNECTED_SET, stroke_width=2).move_to(
            ax.c2p(*pts[n])).set_fill(C.CONNECTED_SET, 0.06) for n in fit]
        with self.voiceover(
            "<bookmark mark='a'/> The theorem, Rudin 9.23: on a complete metric space, a map that shrinks every "
            "distance by a factor c less than one has exactly one fixed point. Start anywhere and iterate. "
            "<bookmark mark='b'/> Each step is at most c times the one before, so the n-th step is at most c to the n "
            "times the first. <bookmark mark='c'/> Adding up the steps between the n-th point and any later one gives a "
            "geometric series: every later point lies in a disc of radius c to the n over one minus c times the first "
            "step. The discs shrink to nothing, so the sequence is Cauchy. <bookmark mark='d'/> The space is complete, "
            "so the points converge, and because the map is continuous, the limit is fixed. <bookmark mark='e'/> And "
            "two fixed points would have to be closer to each other than they are, so there's only one."
        ) as vo:
            self.play(FadeIn(pm), FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(dots[0], scale=1.5), FadeIn(xl))
            self.play(LaggedStart(*[AnimationGroup(Create(s_), FadeIn(d_)) for s_, d_ in zip(steps, dots[1:])],
                                  lag_ratio=0.4), run_time=3.0)
            vo.wait_until("b")
            self.play(*pm.light(0))
            step(0)
            vo.wait_until("c")
            self.play(*pm.light(1))
            step(1)
            self.play(FadeIn(discs[0]))
            for k in range(1, len(discs)):
                self.play(ReplacementTransform(discs[k - 1], discs[k]), run_time=0.6)
            vo.wait_until("d")
            self.play(*pm.light(2))
            self.play(FadeIn(fixd, scale=2))
            self.play(*pm.light(3))
            step(2)
            vo.wait_until("e")
            step(3)
            self.play(*pm.done())
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def complete(self):
        xs = [Fraction(1)]
        for _ in range(5):
            xs.append(xs[-1] / 2 + 1 / xs[-1])
        assert xs[1:4] == [Fraction(3, 2), Fraction(17, 12), Fraction(577, 408)]
        for a, b in zip(xs[1:], xs[2:]):  # a contraction with c = 1/2 on [1, 2]: |phi'(x)| = |1/2 - 1/x^2| <= 1/2
            assert abs(b - (a / 2 + 1 / a)) == 0
        head = VGroup(label(r"Why completeness matters: \ $\varphi(x) = \frac x2 + \frac1x$ on $\mathbb Q \cap [1, 2]$",
                            font_size=34),
                      label(r"maps rationals to rationals, \ and $|\varphi'(x)| = |\tfrac12 - \tfrac1{x^2}| \le \tfrac12$:"
                            r" \ a contraction", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        L = 11.0
        nl = NumberLine(x_range=[1, 2, 0.25], length=L, include_numbers=True, font_size=18,
                        decimal_number_config={"num_decimal_places": 2}).move_to([0, 1.05, 0])
        # an invisible pair of axes on the number line, for the magnifier
        nax = Axes(x_range=[1, 2, 0.25], y_range=[-1, 1, 1], x_length=L, y_length=2.0, tips=False,
                   axis_config={"stroke_opacity": 0, "include_ticks": False}).move_to(nl.n2p(1.5))
        assert np.allclose(nax.c2p(1.25, 0), nl.n2p(1.25))
        dots = VGroup(*[Dot(nl.n2p(float(q)), radius=0.08, color=C.SEQ) for q in xs[:5]])
        labs = VGroup(*[MathTex(rf"\tfrac{{{q.numerator}}}{{{q.denominator}}}" if q.denominator > 1 else "1",
                                font_size=30, color=C.SEQ).next_to(dots[i], UP, buff=0.15) for i, q in enumerate(xs[:2])])
        r2 = math.sqrt(2)
        hole = Circle(radius=0.11, color=C.HOLE, stroke_width=3).move_to(nl.n2p(r2))
        # 17/12 is 0.0025 from sqrt 2, and 577/408 only 2.1e-6: on the line they are one blob. A magnifier
        # x145 separates 17/12; 577/408 still sits on sqrt 2 (2.1e-6 is 0.003 units even there).
        wx = (1.4125, 1.4175)
        W, H = 7.0, 2.0
        inset, mag = magnifier(nax, wx, (-0.15, 0.15), center=[2.75, -0.95, 0], width=W, height=H, color=GREY_B)
        sc = W / (wx[1] - wx[0])
        assert wx[0] < r2 < float(xs[3]) < float(xs[2]) < wx[1]
        assert sc * (float(xs[2]) - r2) > 2.0 and sc * (float(xs[3]) - r2) < 0.005
        iline = NumberLine(x_range=[1.413, 1.417, 0.001], length=sc * 0.004, include_numbers=True, font_size=18,
                           decimal_number_config={"num_decimal_places": 3})
        iline.shift(np.array([inset.c2p(1.415, 0)[0], mag.frame.get_y() + 0.1, 0]) - iline.n2p(1.415))
        assert np.allclose(iline.n2p(1.413)[0], inset.c2p(1.413, 0)[0])
        idots = VGroup(Dot(iline.n2p(float(xs[2])), radius=0.08, color=C.SEQ),
                       Dot(iline.n2p(float(xs[3])), radius=0.08, color=C.SEQ))
        ilabs = VGroup(MathTex(r"\tfrac{17}{12}", font_size=30, color=C.SEQ).next_to(idots[0], UP, buff=0.15),
                       MathTex(r"\tfrac{577}{408}", font_size=30, color=C.SEQ).next_to(idots[1], UP, buff=0.15))
        ihole = VGroup(Circle(radius=0.13, color=C.HOLE, stroke_width=3).move_to(iline.n2p(r2)),
                       MathTex(r"\sqrt 2 \notin \mathbb Q", font_size=28, color=C.HOLE))
        ihole[1].next_to(iline.numbers, DOWN, buff=0.12).set_x(iline.n2p(r2)[0])
        assert ihole[1].get_bottom()[1] > mag.frame.get_bottom()[1] + 0.1
        assert ilabs.get_top()[1] < mag.frame.get_top()[1] - 0.05
        gap = float(xs[3]) - r2
        assert 2.0e-6 < gap < 2.2e-6
        gl = MathTex(rf"\tfrac{{577}}{{408}} - \sqrt 2 = {sci(gap, 1)}", font_size=26, color=GREY_A)
        gl.next_to(mag.frame, DOWN, buff=0.15).align_to(mag.frame, RIGHT)
        out = VGroup(label(r"the iterates are Cauchy,", font_size=26),
                     label(r"but their limit would be $\sqrt 2$:", font_size=26),
                     label(r"no fixed point in $\mathbb Q$", font_size=26, color=C.HOLE),
                     label(r"(Part 1's hole; \ Newton's method for $\sqrt 2$)", font_size=24, color=GREY_A),
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        out.next_to([-6.6, -0.95, 0], RIGHT, buff=0)
        assert out.get_right()[0] < mag.frame.get_left()[0] - 0.3
        assert mag.tag.get_top()[1] < nl.numbers.get_bottom()[1] - 0.1 and gl.get_bottom()[1] > -3.6
        assert nl.get_top()[1] < head.get_bottom()[1] - 0.6
        with self.voiceover(
            "<bookmark mark='a'/> Completeness can't be dropped. The map x over two plus one over x sends rationals to "
            "rationals, and on the interval from one to two it shrinks distances by at least half. "
            "<bookmark mark='b'/> Iterate from one: three halves, seventeen twelfths, five hundred seventy-seven over "
            "four hundred eight. <bookmark mark='c'/> The iterates form a Cauchy sequence, but the point they close in "
            "on is the square root of two, the hole in the rationals from Part 1. Among the rationals, there is no "
            "fixed point at all."
        ) as vo:
            self.play(FadeIn(head[0]), Create(nl), FadeIn(dots[0]), FadeIn(labs[0]))
            vo.wait_until("a")
            self.play(FadeIn(head[1]))
            vo.wait_until("b")
            self.play(FadeIn(dots[1], scale=1.5), FadeIn(labs[1]), run_time=0.7)
            self.play(FadeIn(dots[2], scale=1.5), Create(mag.src), Create(mag.guides), FadeIn(mag.frame),
                      FadeIn(mag.tag), Create(iline), run_time=0.9)
            self.play(FadeIn(idots[0], scale=1.5), FadeIn(ilabs[0]), run_time=0.7)
            self.play(FadeIn(dots[3]), FadeIn(idots[1], scale=1.5), FadeIn(ilabs[1]), run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(dots[4]), Create(hole), Create(ihole[0]), FadeIn(ihole[1]), FadeIn(gl))
            self.play(FadeIn(out))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def newton(self):
        d = load("contraction")
        xn, nerr = d["xn"], d["nerr"]
        r2 = math.sqrt(2)
        ax = plain_axes([1.0, 2.0, 0.5], [1.0, 2.0, 0.5], 4.6, 4.6, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 1}}).move_to([-3.75, -0.85, 0])
        t = np.linspace(1.0, 2.0, 300)
        g = t / 2 + 1 / t
        gg = polyline(ax, t, g, color=C.FUNC, stroke_width=3.5)
        dg = polyline(ax, t, t, color=GREY_B, stroke_width=2.5)
        tang = DashedLine(ax.c2p(1.0, r2), ax.c2p(1.75, r2), color=C.EPS, stroke_width=2.5)
        tl_ = MathTex(r"\text{slope } 0 \text{ at } \sqrt 2", font_size=24, color=C.EPS).next_to(ax.c2p(1.75, r2), DR,
                                                                                             buff=0.06)
        # the cobweb from x_0 = 1: up to the graph, across to the diagonal
        assert np.allclose(xn[:4], [1, 1.5, 17 / 12, 577 / 408])
        web_pts = [(xn[0], xn[0])]
        for k in range(3):
            web_pts += [(xn[k], xn[k + 1]), (xn[k + 1], xn[k + 1])]
        web = VGroup(*[Line(ax.c2p(*a_), ax.c2p(*b_), color=C.EPS, stroke_width=2.5)
                       for a_, b_ in zip(web_pts[:-1], web_pts[1:])])
        # from x_2 on the steps are a hundredth of a unit: a magnifier at (sqrt 2, sqrt 2), equal scales
        W, H, hw = 1.9, 1.3, 0.004
        xw, yw = (r2 - hw, r2 + hw), (r2 - hw * H / W, r2 + hw * H / W)
        inset, mag = magnifier(ax, xw, yw, center=[-2.25, -2.4, 0], width=W, height=H, color=GREY_B)
        sc = W / (2 * hw)
        assert sc * (xn[2] - r2) > 0.5 and sc * (xn[3] - r2) < 0.002  # x_2 visibly off, x_3 on sqrt 2

        def clip(p, q):
            """The part of the segment p -> q inside the magnified window (Liang-Barsky), or None."""
            p, q = np.asarray(p, float), np.asarray(q, float)
            t0, t1, dv = 0.0, 1.0, q - p
            for lo, hi, pc, dc in ((xw[0], xw[1], p[0], dv[0]), (yw[0], yw[1], p[1], dv[1])):
                for num_, den_ in ((pc - lo, -dc), (hi - pc, dc)):
                    if abs(den_) < 1e-15:
                        if num_ < 0:
                            return None
                        continue
                    t_ = num_ / den_
                    t0, t1 = (max(t0, t_), t1) if den_ < 0 else (t0, min(t1, t_))
            return (p + t0 * dv, p + t1 * dv) if t1 - t0 > 1e-9 else None

        iweb = VGroup()
        for a_, b_ in zip(web_pts[:-1], web_pts[1:]):
            cp = clip(a_, b_)
            if cp is not None:
                iweb.add(Line(inset.c2p(*cp[0]), inset.c2p(*cp[1]), color=C.EPS, stroke_width=2.5))
        assert len(iweb) >= 3
        zt = np.linspace(*xw, 200)
        igg = polyline(inset, zt, zt / 2 + 1 / zt, color=C.FUNC, stroke_width=3.5)
        idg = polyline(inset, zt, zt, color=GREY_B, stroke_width=2.5)
        assert np.all(np.abs(zt / 2 + 1 / zt - r2) < yw[1] - r2)  # g is flat across the whole window
        head = VGroup(label(r"Newton's method is a contraction near a simple root", font_size=34),
                      MathTex(r"g(x) = x - \frac{f(x)}{f'(x)}, \qquad g'(x) = \frac{f(x) f''(x)}{f'(x)^2} = 0 "
                              r"\text{ at the root}", font_size=30)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.3)
        gl = MathTex(r"g(x) = \frac x2 + \frac1x \quad (f = x^2 - 2)", font_size=26, color=C.FUNC).next_to(ax, UP,
                                                                                                   buff=0.05)
        tab = VGroup(MathTex(r"n", r"\quad |x_n - \sqrt 2|", font_size=28, color=GREY_A))
        for n in range(5):
            tab.add(MathTex(rf"{n}", r"\quad " + (f"{nerr[n]:.4f}" if nerr[n] > 1e-3 else sci(float(nerr[n]), 1)),
                            font_size=28))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        regrid(tab)
        tab.next_to([0.9, 1.3, 0], DR, buff=0)
        side = VGroup(label(r"flat at the fixed point:", font_size=24),
                      label(r"near it, $c$ is as small as we like,", font_size=24),
                      label(r"so each step beats the last:", font_size=24),
                      label(r"the error squares, \ the digits double", font_size=24, color=C.EPS),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        side.next_to(tab, DOWN, buff=0.45, aligned_edge=LEFT)
        assert side.get_right()[0] <= 6.6 and side.get_bottom()[1] > -3.6 and tab.get_left()[0] > tl_.get_right()[0] + 0.15
        assert tl_.get_bottom()[1] > mag.frame.get_top()[1] + 0.05 and tab.get_top()[1] < head.get_bottom()[1] - 0.2
        assert nerr[4] < 1e-11
        with self.voiceover(
            "<bookmark mark='a'/> And Newton's method from the opening is a contraction too. Its step is the map g of "
            "x equals x minus f over f prime, and at a simple root its derivative is zero. <bookmark mark='b'/> For "
            "the square root of two, g is flat where it crosses the diagonal, so near the root it shrinks distances by "
            "a factor as small as we like. <bookmark mark='c'/> That's why Newton's method is so fast: each step "
            "contracts harder than the one before, the error squares, and the number of correct digits doubles."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), Create(dg))
            vo.wait_until("a")
            self.play(FadeIn(head[1]), Create(gg), FadeIn(gl))
            vo.wait_until("b")
            self.play(Create(tang), FadeIn(tl_))
            self.play(Create(mag.src), Create(mag.guides), FadeIn(mag.frame), FadeIn(mag.tag), Create(igg),
                      Create(idg), run_time=1.0)
            vo.wait_until("c")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            for k in range(3):
                self.play(Create(web[2 * k]), Create(web[2 * k + 1]), FadeIn(tab[k + 2]), run_time=0.7)
            self.play(Create(iweb), FadeIn(tab[5]), run_time=1.0)
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()
