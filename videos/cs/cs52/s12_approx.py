from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs52.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


def clipped(ax, xs, ys, lo, hi, color, width=3):
    """A curve through (x, y), drawn only where it stays inside [lo, hi] (it leaves the chart elsewhere)."""
    runs, cur = [], []
    for x, y in zip(xs, ys):
        if lo <= y <= hi:
            cur.append(ax.c2p(x, y))
        else:
            if len(cur) > 1:
                runs.append(cur)
            cur = []
    if len(cur) > 1:
        runs.append(cur)
    return VGroup(*[VMobject(color=color, stroke_width=width).set_points_as_corners(r) for r in runs])


def node_poly(nodes, x):
    """The node polynomial: the product of (x - x_j)."""
    return float(np.prod([x - xj for xj in nodes]))


def sci(v: float, digits: int = 1) -> str:
    """A number as TeX: 6.3 x 10^{14}."""
    e = math.floor(math.log10(abs(v)))
    return rf"{v / 10 ** e:.{digits}f} \times 10^{{{e}}}"


def runge_f(x):
    return 1 / (1 + 25 * x * x)


class Approx(WatchScene):
    def construct(self):
        self.card()
        self.runge()
        self.chebyshev()
        self.convergence()

    def card(self):
        self.chapter(11, r"Approximation", r"Which polynomial should stand in for a function?", lit=(1901, 2004), extra=((1901, r"Runge's phenomenon"),
                                                     (2004, r"Battles and Trefethen: \ Chebfun")), part=PART, said="Chapter eleven. Approximation.")

    def chart(self, center, x_length=7.0, y_length=4.2, lo=-1.0, hi=2.0):
        ax = Axes(x_range=[-1, 1, 0.5], y_range=[lo, hi, 1], x_length=x_length, y_length=y_length, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False})
        ax.move_to([*center, 0])
        xt = VGroup(*[label(f"{v:g}", font_size=16, color=GREY_B).next_to(ax.c2p(v, lo), DOWN, buff=0.1)
                      for v in (-1, 0, 1)])
        yt = VGroup(*[label(f"{v:g}", font_size=16, color=GREY_B).next_to(ax.c2p(-1, v), LEFT, buff=0.1)
                      for v in range(int(lo), int(hi) + 1)])
        return ax, VGroup(xt, yt)

    def runge(self):
        self.ask(r"Interpolate $1/(1 + 25x^2)$ at more and more \\ equally spaced points. Near the ends, the error...",
                 [r"shrinks", r"explodes"], 1,
                 say="Pass a polynomial through more and more equally spaced samples of Runge's function. What happens near the ends?",
                 reveal="The error explodes. Chebyshev points fix it.")
        r = load("runge")
        rows_ = {row["n"]: row for row in r["rows"]}
        c10, c20 = r["curves"]["10"], r["curves"]["20"]
        head = label(r"Runge's phenomenon", font_size=36).to_edge(UP, buff=0.3)
        ax, ticks = self.chart((-2.5, -0.1))
        f = VMobject(color=WHITE, stroke_width=3.5).set_points_smoothly([ax.c2p(x, y) for x, y in zip(c10["x"],
                                                                                                    r["f"])])
        p10 = clipped(ax, c10["x"], c10["equi"], -1, 2, KERN)
        p20 = clipped(ax, c20["x"], c20["equi"], -1, 2, NO)
        d10 = VGroup(*[Dot(ax.c2p(x, runge_f(x)), radius=0.06, color=KERN) for x in c10["nodes_e"]])
        d20 = VGroup(*[Dot(ax.c2p(x, runge_f(x)), radius=0.05, color=NO) for x in c20["nodes_e"]])
        fl = MathTex(r"f(x) = \frac{1}{1 + 25x^2}", font_size=30, color=WHITE)
        notes = VGroup(
            fl,
            label(rf"11 equally spaced points: \ error {rows_[10]['equispaced']:.2f}", font_size=19, color=KERN),
            label(rf"21 points: \ error {rows_[20]['equispaced']:.1f}", font_size=19, color=NO),
            label(rf"81 points: \ error ${sci(rows_[80]['equispaced'])}$", font_size=19, color=NO),
            wrapped_label(r"more data, \ a worse answer: \ the function is innocent, \ the points are to blame", 3.6,
                          font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.75, 0.1, 0])
        cap = note(r"largest error on $[-1, 1]$, \ computed; \ the curves leave the chart near the ends",
                   font_size=16).next_to(ax, DOWN, buff=0.45)
        with self.voiceover(
            "To stand in for a function, the obvious idea is to sample it and pass a polynomial through the "
            "samples. <bookmark mark='a'/> In 1901 Carl Runge tried it on a perfectly smooth function, one over one "
            "plus twenty-five x squared. <bookmark mark='b'/> Through eleven equally spaced points, the polynomial "
            "follows it in the middle but swings near the ends. <bookmark mark='c'/> Through twenty-one points "
            "it is far worse: near the ends the error is about sixty. <bookmark mark='d'/> With eighty-one points "
            "it is six times ten to the fourteen. More data gives a worse answer. The function is innocent: the "
            "points are to blame."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks))
            vo.wait_until("a")
            self.play(Create(f), FadeIn(notes[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(d10))
            self.play(Create(p10), FadeIn(notes[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(p10.animate.set_stroke(opacity=0.3), d10.animate.set_opacity(0.3), FadeIn(d20))
            self.play(Create(p20), FadeIn(notes[2]), FadeIn(cap), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
            self.play(FadeIn(notes[4]))
        self.wait(0.4)
        self.clear_scene()

    def chebyshev(self):
        r = load("runge")
        c10 = r["curves"]["10"]
        n = len(c10["nodes_c"]) - 1
        head = label(r"Chebyshev points", font_size=36).to_edge(UP, buff=0.3)
        R, C = 2.6, np.array([-3.7, -0.6, 0])
        diam = Line(C + LEFT * R, C + RIGHT * R, color=GREY_C, stroke_width=2)
        arc = Arc(radius=R, start_angle=0, angle=PI, color=GREY_C, stroke_width=2).move_arc_center_to(C)
        tops = VGroup(*[Dot(C + R * np.array([math.cos(j * PI / n), math.sin(j * PI / n), 0]), radius=0.06,
                            color=GREY_A) for j in range(n + 1)])
        drops = VGroup(*[DashedLine(t.get_center(), [t.get_x(), C[1], 0], color=GREY_B, stroke_width=1.2)
                         for t in tops])
        bots = VGroup(*[Dot([t.get_x(), C[1], 0], radius=0.07, color=HEAD) for t in tops])
        fm = MathTex(r"x_j = \cos\frac{j\pi}{n}", font_size=30, color=HEAD).next_to(diam, DOWN, buff=0.35)
        cols = {r"\ell(x)": HEAD}
        rows = VGroup(
            cmath(r"f(x) - p(x)", r"=", r"\frac{f^{(n+1)}(\xi)}{(n+1)!}", r"\,", r"\ell(x)", colors=cols,
                  font_size=32),
            cmath(r"\ell(x)", r"=", r"\prod_{j=0}^{n} (x - x_j)", colors=cols, font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([3.2, 1.75, 0])
        whys = VGroup(label(r"the interpolation error: \ $f$'s part, \ times", font_size=18, color=GREY_B),
                      label(r"the node polynomial: \ the part we choose", font_size=18, color=HEAD))
        for w, rr in zip(whys, rows):
            w.next_to(rr, DOWN, buff=0.1).align_to(rr, LEFT)
        ax = Axes(x_range=[-1, 1, 0.5], y_range=[0, 1, 0.5], x_length=5.4, y_length=1.9, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False})
        ax.next_to(whys[1], DOWN, buff=0.75).set_x(3.3)
        xs = np.linspace(-1, 1, 401)
        le = [abs(node_poly(c10["nodes_e"], x)) for x in xs]
        lc = [abs(node_poly(c10["nodes_c"], x)) for x in xs]
        top = max(le)
        ce = VMobject(color=NO, stroke_width=2.5).set_points_as_corners([ax.c2p(x, v / top) for x, v in zip(xs, le)])
        cc = VMobject(color=HEAD, stroke_width=2.5).set_points_as_corners(
            [ax.c2p(x, v / top) for x, v in zip(xs, lc)])
        mid = max(le[180:221])
        ttl = label(rf"$|\ell(x)|$ for {n + 1} points, \ computed", font_size=17, color=GREY_A).next_to(
            ax, UP, buff=0.1).align_to(ax, LEFT)
        k1 = label(rf"equispaced: \ ${sci(top)}$ near the ends, \ ${sci(mid)}$ in the middle", font_size=17,
                   color=NO)
        k2 = label(rf"Chebyshev: \ at most ${sci(max(lc))}$ everywhere \ $\approx 2^{{1-n}}$", font_size=17,
                   color=HEAD)
        keys = VGroup(k1, k2).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(ax, DOWN, buff=0.2)
        keys.align_to(ax, LEFT)
        with self.voiceover(
            "The cure is to choose the points. <bookmark mark='a'/> Space points evenly around a semicircle and "
            "drop them onto the diameter. These are Chebyshev points, crowded towards the ends. "
            "<bookmark mark='b'/> Why there? The interpolation error is a derivative of f, which we cannot "
            "change, <bookmark mark='c'/> times the node polynomial, the product of x minus each sample point, "
            "which we can. <bookmark mark='d'/> For equally spaced points it is small in the middle and nearly a "
            "hundred times larger near the ends. For Chebyshev points it ripples evenly and never exceeds two to "
            "the one minus n, within a factor of two of the smallest maximum any choice of points can have."
        ) as vo:
            self.play(FadeIn(head), Create(arc), Create(diam))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in tops], lag_ratio=0.08))
            self.play(Create(drops), LaggedStart(*[FadeIn(b) for b in bots], lag_ratio=0.05), FadeIn(fm))
            vo.wait_until("b")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(Create(ax), FadeIn(ttl))
            self.play(Create(ce), FadeIn(k1), run_time=1.2)
            self.play(Create(cc), FadeIn(k2), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    def convergence(self):
        r = load("runge")
        rows_ = r["rows"]
        c20 = r["curves"]["20"]
        head = label(r"Geometric convergence", font_size=36).to_edge(UP, buff=0.3)
        ax, ticks = self.chart((-3.6, 1.35), x_length=5.2, y_length=2.1, lo=0.0, hi=1.0)
        f = VMobject(color=WHITE, stroke_width=4).set_points_smoothly([ax.c2p(x, y) for x, y in zip(c20["x"],
                                                                                                  r["f"])])
        pc = VMobject(color=YES, stroke_width=2.5).set_points_smoothly(
            [ax.c2p(x, y) for x, y in zip(c20["x"], c20["cheb"])])
        dc = VGroup(*[Dot(ax.c2p(x, runge_f(x)), radius=0.045, color=YES) for x in c20["nodes_c"]])
        r20 = next(x for x in rows_ if x["n"] == 20)
        fit = label(rf"21 Chebyshev points: \ error {r20['chebyshev']:.3f}", font_size=18, color=YES).next_to(
            ax, DOWN, buff=0.35)
        rho = (1 + math.sqrt(26)) / 5
        cols = {r"\rho": HEAD}
        der = VGroup(
            cmath(r"1 + 25x^2 = 0", r"\ \Rightarrow\ ", r"x = \pm\tfrac{i}{5}", font_size=30),
            cmath(r"\rho", r"=", r"\left|z + \sqrt{z^2 - 1}\right|_{z = i/5}", colors=cols, font_size=30),
            cmath(r"\rho", r"=", r"\frac{1 + \sqrt{26}}{5}", r"\approx", rf"{rho:.3f}", colors=cols, font_size=30),
            cmath(r"\|f - p_n\|", r"\sim", r"\rho", r"^{-n}", colors=cols, font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(fit, DOWN, buff=0.35).align_to(ax, LEFT)
        dw = label(r"poles in the complex plane", font_size=17, color=GREY_B).next_to(der[0], RIGHT, buff=0.25)
        dw2 = label(r"the ellipse through them", font_size=17, color=GREY_B).next_to(der[1], RIGHT, buff=0.25)
        bx = CornerAxes(x_range=[0, 80, 20], y_range=[-8, 16, 4], x_length=4.6, y_length=4.4, tips=False,
                        axis_config={"stroke_color": GREY_C})
        bx.move_to([3.7, 0.0, 0])
        yt = VGroup(*[MathTex(rf"10^{{{p}}}", font_size=20, color=GREY_B).next_to(bx.c2p(0, p), LEFT, buff=0.1)
                      for p in (-8, -4, 0, 4, 8, 12, 16)])
        xt = VGroup(*[label(f"{v}", font_size=16, color=GREY_B).next_to(bx.c2p(v, -8), DOWN, buff=0.1)
                      for v in (0, 20, 40, 60, 80)])
        xl = label(r"degree $n$", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yl = label(r"largest error, \ computed", font_size=17, color=GREY_A).next_to(bx, UP, buff=0.15).align_to(
            bx, LEFT)

        def line(key, color):
            pts = [bx.c2p(x["n"], math.log10(x[key])) for x in rows_]
            return VGroup(VMobject(color=color, stroke_width=3).set_points_as_corners(pts),
                          *[Dot(p, radius=0.05, color=color) for p in pts])
        le, lc = line("equispaced", NO), line("chebyshev", YES)
        theo = DashedLine(bx.c2p(0, 0), bx.c2p(80, -80 * math.log10(rho)), color=HEAD, stroke_width=2)
        te = label(r"equispaced", font_size=17, color=NO).move_to(bx.c2p(40, 9.5), aligned_edge=RIGHT)
        tc = label(r"Chebyshev", font_size=17, color=YES).next_to(bx.c2p(40, -3.5), DOWN, buff=0.15)
        tt = label(r"$\rho^{-n}$", font_size=20, color=HEAD).next_to(bx.c2p(80, -80 * math.log10(rho)), UP,
                                                                     buff=0.15).shift(LEFT * 0.25)
        last = rows_[-1]
        res = label(rf"$n = {last['n']}$: \ ${sci(last['chebyshev'])}$ against ${sci(last['equispaced'])}$",
                    font_size=18, color=WHITE).next_to(xl, DOWN, buff=0.2)
        with self.voiceover(
            "Here is the difference, computed. <bookmark mark='a'/> Through twenty-one Chebyshev points, the "
            "polynomial is already within two hundredths of Runge's function everywhere. <bookmark mark='b'/> As "
            "the degree grows, the equispaced error explodes, and the Chebyshev error falls geometrically, to about "
            "one ten-millionth at degree eighty. <bookmark mark='c'/> The rate is set by where f stops being "
            "smooth: poles at plus and minus i over five, off the real line. <bookmark mark='d'/> The ellipse "
            "around the interval that passes through them has a parameter rho, one plus root twenty-six, over "
            "five, about one point two two, <bookmark mark='e'/> and the error falls like rho to the minus n: the "
            "dashed line."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks), Create(bx), FadeIn(yt), FadeIn(xt), FadeIn(xl),
                      FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(f), FadeIn(dc))
            self.play(Create(pc), FadeIn(fit))
            vo.wait_until("b")
            self.play(Create(le), FadeIn(te), run_time=1.5)
            self.play(Create(lc), FadeIn(tc), FadeIn(res), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(der[0]), FadeIn(dw))
            vo.wait_until("d")
            self.play(FadeIn(der[1]), FadeIn(dw2))
            self.play(TransformMatchingTex(der[1].copy(), der[2]))
            vo.wait_until("e")
            self.play(FadeIn(der[3]), Create(theo), FadeIn(tt))
        self.wait(0.4)
        self.clear_scene()




_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
