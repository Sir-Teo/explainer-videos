from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs52.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


def integrand(x):
    """The test integrand of our instrument: e^x cos 3x on [0, 2]."""
    return math.exp(x) * math.cos(3 * x)


def partition(f, a, b, tol):
    """The intervals adaptive Simpson accepts (the instrument's rule, |S2 - S1| <= 15 tol): for drawing only."""
    def s(a, b):
        return (b - a) / 6 * (f(a) + 4 * f((a + b) / 2) + f(b))

    out = []

    def rec(a, b, whole, tol, depth):
        m = (a + b) / 2
        left, right = s(a, m), s(m, b)
        if depth > 30 or abs(left + right - whole) <= 15 * tol:
            out.append((a, b))
            return
        rec(a, m, left, tol / 2, depth + 1)
        rec(m, b, right, tol / 2, depth + 1)

    rec(a, b, s(a, b), tol, 0)
    return out


def sci(v: float, digits: int = 1) -> str:
    """A number as TeX: 2.3 x 10^{-14}."""
    e = math.floor(math.log10(abs(v)))
    return rf"{v / 10 ** e:.{digits}f} \times 10^{{{e}}}"


class Quadrature(VoiceoverScene):
    def construct(self):
        self.card()
        self.rules()
        self.gauss()
        self.measured()
        self.adaptive()
        self.montecarlo()

    def card(self):
        card = chapter_card(12, r"Quadrature", r"How few samples does an integral need?",
                            lit=(1814, 1949), extra=((1814, r"Gauss: \ optimal nodes"),
                                                     (1949, r"Metropolis and Ulam: \ Monte Carlo")), part=PART)
        with self.voiceover("Chapter twelve. Quadrature."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def plot(self, center, x_length=5.8, y_length=3.8):
        ax = Axes(x_range=[0, 2, 0.5], y_range=[-3, 8, 1], x_length=x_length, y_length=y_length, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False})
        ax.move_to([*center, 0])
        curve = ax.plot(integrand, x_range=[0, 2, 0.01], color=DATA, stroke_width=3)
        ticks = VGroup(*[label(f"{v:g}", font_size=16, color=GREY_B).next_to(ax.c2p(v, -3), DOWN, buff=0.1)
                         for v in (0, 1, 2)])
        return ax, curve, ticks

    def rules(self):
        q = load("quad")
        rows_ = {int(r["n"]): r for r in q["rows"]}
        head = label(r"Trapezoids, \ then Simpson", font_size=36).to_edge(UP, buff=0.3)
        ax, curve, ticks = self.plot((-3.6, 0.2))
        fl = MathTex(r"\int_0^2 e^x \cos 3x \, dx", rf"= {q['exact']:.7f}", font_size=28,
                     color=DATA).next_to(ax, DOWN, buff=0.5)
        area = ax.get_area(curve, x_range=[0, 2], color=DATA, opacity=0.18)
        n = 4
        xs = [2 * i / n for i in range(n + 1)]
        traps = VGroup(*[Polygon(ax.c2p(xs[i], 0), ax.c2p(xs[i], integrand(xs[i])),
                                 ax.c2p(xs[i + 1], integrand(xs[i + 1])), ax.c2p(xs[i + 1], 0),
                                 stroke_color=KERN, stroke_width=2, fill_color=KERN, fill_opacity=0.25)
                         for i in range(n)])
        dots = VGroup(*[Dot(ax.c2p(x, integrand(x)), radius=0.06, color=KERN) for x in xs])
        tl = label(rf"4 trapezoids: \ error {rows_[4]['trapezoid']:.3f}", font_size=18, color=KERN).next_to(
            fl, DOWN, buff=0.2)
        cols = {r"h^2": KERN, r"h^4": LAM}
        rows = VGroup(
            cmath(r"T_h", r"=", r"h\left(\tfrac12 f_0 + f_1 + \cdots + f_{n-1} + \tfrac12 f_n\right)", font_size=30),
            cmath(r"I - T_h", r"=", r"-\frac{(b-a)}{12}", r"h^2", r"f''(\xi)", colors=cols, font_size=30),
            cmath(r"S", r"=", r"\frac{4\,T_{h/2} - T_h}{3}", font_size=30),
            cmath(r"I - S", r"=", r"-\frac{(b-a)}{180}", r"h^4", r"f^{(4)}(\xi)", colors=cols, font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.62).move_to([3.0, 0.3, 0])
        whys = VGroup(
            label(r"join the samples with straight lines", font_size=18, color=GREY_B),
            label(r"halve $h$: \ a quarter of the error", font_size=18, color=KERN),
            label(r"combine two sums so the $h^2$ terms cancel", font_size=18, color=GREY_B),
            label(r"Simpson's rule: \ halve $h$, \ a sixteenth of the error", font_size=18, color=LAM),
        )
        for w, rr in zip(whys, rows):
            w.next_to(rr, DOWN, buff=0.1).align_to(rr, LEFT)
        with self.voiceover(
            "To integrate, sample the function and add up. Our test integral is e to the x times cosine three x, "
            "from nought to two. Its exact value is about minus one hundredth: a small difference of large areas. "
            "<bookmark mark='a'/> The trapezoid rule joins the samples with straight lines. "
            "<bookmark mark='b'/> Its error shrinks like h squared: halve the spacing and the error falls "
            "fourfold. <bookmark mark='c'/> Combine two trapezoid sums, four times the finer one minus the coarser, "
            "over three, and the h squared terms cancel. That is Simpson's rule, <bookmark mark='d'/> and its "
            "error falls like h to the fourth."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks), Create(curve), FadeIn(area), FadeIn(fl))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]), FadeIn(dots), FadeIn(traps), FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[1].copy(), rows[3]), FadeIn(whys[3]))
        self.wait(0.4)
        self.clear_scene()

    def gauss(self):
        head = label(r"Gauss: \ choose the points too", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            cmath(r"\int_{-1}^{1} f", r"\approx", r"w_1 f(x_1) + w_2 f(x_2)", font_size=30),
            MathTex(r"w_1 + w_2 = 2, \quad w_1 x_1 + w_2 x_2 = 0", r"\\",
                    r"w_1 x_1^2 + w_2 x_2^2 = \tfrac23, \quad w_1 x_1^3 + w_2 x_2^3 = 0", font_size=30),
            cmath(r"w_1 = w_2 = 1", r",\quad", r"x_{1,2} = \pm \frac{1}{\sqrt 3}", font_size=30, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([-3.2, 0.9, 0])
        whys = VGroup(
            label(r"four unknowns: \ two nodes, \ two weights", font_size=18, color=GREY_B),
            label(r"demand exactness for $1, x, x^2, x^3$", font_size=18, color=GREY_B),
            label(r"two samples, \ exact for every cubic", font_size=18, color=HEAD),
        )
        for w, rr in zip(whys, rows):
            w.next_to(rr, DOWN, buff=0.12).align_to(rr, LEFT)
        gen = VGroup(
            wrapped_label(r"$n$ points: \ exact to degree $2n - 1$; \ the nodes are the roots of the Legendre "
                          r"polynomial $P_n$", 5.8, font_size=20, color=WHITE),
            wrapped_label(r"Golub and Welsch \ (1969): \ the nodes are the eigenvalues of a symmetric tridiagonal "
                          r"matrix, \ found by Chapter 6's QR algorithm", 5.8, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(whys[2], DOWN, buff=0.45).align_to(rows, LEFT)
        L, C = 5.4, np.array([3.7, 0.2, 0])
        lines = VGroup()
        for k, n in enumerate(range(2, 9)):
            y = 2.0 - 0.62 * k
            x, w = np.polynomial.legendre.leggauss(n)
            base = Line(C + np.array([-L / 2, y, 0]), C + np.array([L / 2, y, 0]), color=GREY_D, stroke_width=1.5)
            ds = VGroup(*[Dot(C + np.array([xi * L / 2, y, 0]), radius=0.05 + 0.09 * wi, color=HEAD)
                          for xi, wi in zip(x, w)])
            nl = label(f"{n}", font_size=17, color=GREY_A).next_to(base, LEFT, buff=0.15)
            lines.add(VGroup(base, ds, nl))
        ends = VGroup(MathTex(r"-1", font_size=22, color=GREY_B).next_to(lines[-1][0], DOWN, buff=0.12).align_to(
            lines[-1][0], LEFT), MathTex(r"1", font_size=22, color=GREY_B).next_to(lines[-1][0], DOWN, buff=0.12)
            .align_to(lines[-1][0], RIGHT))
        cap = label(r"Gauss--Legendre nodes for $n = 2, \dots, 8$; \ dot size: \ weight", font_size=17,
                    color=GREY_A).next_to(lines, UP, buff=0.25)
        with self.voiceover(
            "Both rules fix the sample points and choose only the weights. In 1814 Carl Friedrich Gauss chose the "
            "points too. <bookmark mark='a'/> With two points there are four unknowns, two nodes and two weights, "
            "<bookmark mark='b'/> so we may demand the right answer for one, x, x squared and x cubed. "
            "<bookmark mark='c'/> Solving gives weights of one at plus and minus one over root three: two samples, "
            "exact for every cubic. <bookmark mark='d'/> With n points the rule is exact up to degree two n minus "
            "one. The nodes are the roots of Legendre polynomials, crowded towards the ends like chapter eleven's "
            "Chebyshev points. <bookmark mark='e'/> Gene Golub and John Welsch showed in 1969 that they are the "
            "eigenvalues of a symmetric tridiagonal matrix, so chapter six's QR algorithm computes them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(gen[0]), FadeIn(cap), FadeIn(ends))
            self.play(LaggedStart(*[FadeIn(ln) for ln in lines], lag_ratio=0.25), run_time=2.5)
            vo.wait_until("e")
            self.play(FadeIn(gen[1]))
        self.wait(0.4)
        self.clear_scene()

    def measured(self):
        q = load("quad")
        rows_ = q["rows"]
        head = label(r"Four rules, \ computed", font_size=36).to_edge(UP, buff=0.3)
        ax = CornerAxes(x_range=[1, 6, 1], y_range=[-16, 1, 4], x_length=6.4, y_length=4.4, tips=False,
                        axis_config={"stroke_color": GREY_C})
        ax.move_to([-2.4, 0.15, 0])
        xt = VGroup(*[label(f"{2 ** p}", font_size=16, color=GREY_B).next_to(ax.c2p(p, -16), DOWN, buff=0.1)
                      for p in range(1, 7)])
        yt = VGroup(*[MathTex(rf"10^{{{p}}}", font_size=20, color=GREY_B).next_to(ax.c2p(1, p), LEFT, buff=0.1)
                      for p in (-16, -12, -8, -4, 0)])
        xl = label(r"$n$: \ intervals or points \ (log scale)", font_size=17, color=GREY_A).next_to(xt, DOWN,
                                                                                                 buff=0.08)
        yl = label(r"error \ (Monte Carlo: \ root mean square over 200 runs)", font_size=17,
                   color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        specs = [("trapezoid", r"trapezoid", KERN), ("simpson", r"Simpson", LAM), ("gauss", r"Gauss", YES),
                 ("monte_carlo", r"Monte Carlo", NO)]
        series, tags = VGroup(), VGroup()
        for key, name, c in specs:
            pts = [ax.c2p(math.log2(r["n"]), max(-16, math.log10(r[key]))) for r in rows_]
            series.add(VGroup(VMobject(color=c, stroke_width=3).set_points_as_corners(pts),
                              *[Dot(p, radius=0.05, color=c) for p in pts]))
            tags.add(label(name, font_size=18, color=c).next_to(pts[-1], RIGHT, buff=0.15))
        by = {int(r["n"]): r for r in rows_}
        notes = VGroup(
            label(rf"trapezoid, \ 64: \ ${sci(by[64]['trapezoid'])}$ \ ($h^2$)", font_size=19, color=KERN),
            label(rf"Simpson, \ 64: \ ${sci(by[64]['simpson'])}$ \ ($h^4$)", font_size=19, color=LAM),
            label(rf"Gauss, \ 16 points: \ ${sci(by[16]['gauss'])}$", font_size=19, color=YES),
            label(rf"Monte Carlo, \ 65 samples: \ {by[64]['monte_carlo']:.2f}", font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.6, 0.7, 0]).align_to([2.55, 0, 0], LEFT)
        gnote = wrapped_label(r"for a smooth integrand Gauss converges geometrically, \ like Chebyshev "
                              r"interpolation, \ until rounding stops it", 3.9, font_size=18, color=GREY_A).next_to(
            notes, DOWN, buff=0.4).align_to(notes, LEFT)
        with self.voiceover(
            "Here are four rules on our integral, computed. <bookmark mark='a'/> The trapezoid error falls "
            "fourfold each time the points double, to about a thousandth at sixty-four intervals. "
            "<bookmark mark='b'/> Simpson's falls sixteenfold, to about a millionth. <bookmark mark='c'/> Gauss "
            "reaches four times ten to the minus fifteen with just sixteen points, and then can go no further: "
            "that is rounding. For a smooth integrand its error falls geometrically, like Chebyshev "
            "interpolation. <bookmark mark='d'/> Monte Carlo, the average of f at random points, is worst by far: "
            "with sixty-five samples its typical error is still more than a half."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            for mk, s, t, nt in zip("abcd", series, tags, notes):
                vo.wait_until(mk)
                self.play(Create(s), FadeIn(t), FadeIn(nt), run_time=1.5)
                if mk == "c":
                    self.play(FadeIn(gnote))
        self.wait(0.4)
        self.clear_scene()

    def adaptive(self):
        q = load("quad")
        ad = q["adaptive"]
        head = label(r"Adaptive quadrature", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 2, 0.5], y_range=[0, 1.2, 0.5], x_length=5.8, y_length=3.0, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False})
        ax.move_to([-3.5, 0.9, 0])
        cusp = 0.7

        def g(x):
            return math.sqrt(abs(x - cusp))
        curve = VGroup(ax.plot(g, x_range=[0, cusp, 0.002], color=DATA, stroke_width=3),
                       ax.plot(g, x_range=[cusp, 2, 0.002], color=DATA, stroke_width=3))
        gl = MathTex(r"\sqrt{|x - 0.7|}", font_size=26, color=DATA).next_to(ax.c2p(1.6, 1.1), UP, buff=0.05)
        ticks = VGroup(*[label(f"{v:g}", font_size=16, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                         for v in (0, 1, 2)], gl)
        parts = partition(g, 0.0, 2.0, 1e-3)
        marks = VGroup(*[Line(ax.c2p(a, 0), ax.c2p(a, 0) + DOWN * 0.3, color=HEAD, stroke_width=2)
                         for a, _ in parts], Line(ax.c2p(2, 0), ax.c2p(2, 0) + DOWN * 0.3, color=HEAD,
                                                  stroke_width=2))
        marks.shift(DOWN * 0.45)
        ml = note(rf"illustrative: \ the {len(parts)} intervals accepted for a tolerance of $10^{{-3}}$, \ "
                  rf"crowded at the cusp", font_size=17).next_to(marks, DOWN, buff=0.15)
        res = wrapped_label(rf"our smooth test integral, \ tolerance $10^{{-10}}$: \ {ad['calls']:.0f} "
                            rf"evaluations, \ error ${sci(ad['error'])}$ \ (computed); \ Gauss needed 16: \ "
                            rf"adaptivity pays when the trouble is local, \ a kink or a spike", 5.8, font_size=19,
                            color=HEAD).next_to(ml, DOWN, buff=0.35)
        cols = {r"\frac{S_2 - S_1}{15}": YES}
        rows = VGroup(
            cmath(r"S_1 = S(a, b)", r",\quad", r"S_2 = S(a, m) + S(m, b)", font_size=30),
            cmath(r"I - S_1 \approx E", r",\quad", r"I - S_2 \approx 2\cdot\frac{E}{2^5} = \frac{E}{16}",
                  font_size=30),
            cmath(r"I - S_2", r"\approx", r"\frac{S_2 - S_1}{15}", colors=cols, font_size=30),
            cmath(r"|S_2 - S_1| \le 15\,\text{tol}", r"\ ?", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.62).move_to([3.3, 0.45, 0])
        whys = VGroup(
            label(r"Simpson on the interval, \ and on its halves", font_size=18, color=GREY_B),
            label(r"the error grows like the width to the fifth", font_size=18, color=GREY_B),
            label(r"subtract: \ an error estimate, \ for free", font_size=18, color=YES),
            wrapped_label(r"yes: \ accept $S_2$ plus the estimate; \ no: \ split, \ and recurse on each half with "
                          r"half the tolerance", 5.4, font_size=18, color=GREY_B),
        )
        for w, rr in zip(whys, rows):
            w.next_to(rr, DOWN, buff=0.1).align_to(rr, LEFT)
        with self.voiceover(
            "A smooth stretch deserves few points and a wild one many. Adaptive quadrature decides where, by "
            "itself. <bookmark mark='a'/> Apply Simpson's rule to an interval, and again to its two halves. "
            "<bookmark mark='b'/> Simpson's error grows like the fifth power of the width, so the two halves "
            "together err by a sixteenth as much. <bookmark mark='c'/> Subtracting gives an estimate of the error, "
            "for free. <bookmark mark='d'/> If it is small enough, accept, adding the estimate back as a "
            "correction; if not, split and recurse, each half with half the tolerance. <bookmark mark='e'/> On an "
            "integrand with a cusp, the intervals pile up at the cusp and stay wide elsewhere. On our smooth test "
            "integral, asked for ten to the minus ten, our instrument used nine hundred and eighty-five "
            "evaluations, where Gauss needed sixteen: adaptivity pays when the trouble is local."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks), Create(curve))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(LaggedStart(*[Create(m) for m in marks], lag_ratio=0.05), FadeIn(ml), run_time=2)
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def montecarlo(self):
        head = label(r"Monte Carlo: \ slow, \ but blind to dimension", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"\frac{\sigma}{\sqrt N}": NO, r"N^{-2/d}": KERN}
        rows = VGroup(
            cmath(r"I", r"\approx", r"\frac{b - a}{N} \sum_{i=1}^{N} f(U_i)", font_size=30),
            cmath(r"\operatorname{Var}\Big[\tfrac1N \textstyle\sum_i f(U_i)\Big]", r"=", r"\frac{\sigma^2}{N}",
                  font_size=30),
            cmath(r"\text{error}", r"\sim", r"\frac{\sigma}{\sqrt N}", colors=cols, font_size=30),
            cmath(r"h = N^{-1/d}", r"\ \Rightarrow\ ", r"\text{error}", r"\sim", r"h^2", r"=", r"N^{-2/d}",
                  colors=cols, font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([-3.4, 0.35, 0])
        whys = VGroup(
            label(r"$U_i$ uniform random points: \ $I$ is an average", font_size=18, color=GREY_B),
            label(r"independent samples: \ variances add", font_size=18, color=GREY_B),
            label(r"in any dimension", font_size=18, color=NO),
            label(r"a grid of $N$ points in $d$ dimensions, \ trapezoid rule", font_size=18, color=KERN),
        )
        for w, rr in zip(whys, rows):
            w.next_to(rr, DOWN, buff=0.1).align_to(rr, LEFT)
        ax = CornerAxes(x_range=[0, 10, 1], y_range=[0, 2, 0.5], x_length=5.0, y_length=3.2, tips=False,
                        axis_config={"stroke_color": GREY_C})
        ax.move_to([3.7, 0.55, 0])
        bars = VGroup(*[Rectangle(width=0.32, height=ax.c2p(0, 2 / d)[1] - ax.c2p(0, 0)[1], stroke_width=0,
                                  fill_color=KERN, fill_opacity=0.85).move_to(ax.c2p(d - 0.5, 0), aligned_edge=DOWN)
                        for d in range(1, 11)])
        mc = DashedLine(ax.c2p(0, 0.5), ax.c2p(10, 0.5), color=NO, stroke_width=3)
        xt = VGroup(*[label(f"{d}", font_size=16, color=GREY_B).next_to(ax.c2p(d - 0.5, 0), DOWN, buff=0.1)
                      for d in range(1, 11)])
        yt = VGroup(*[MathTex(t, font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for t, v in ((r"0", 0), (r"\tfrac12", 0.5), (r"1", 1), (r"2", 2))])
        xl = label(r"dimension $d$", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yl = label(r"rate: \ error $\sim N^{-\text{rate}}$", font_size=17, color=GREY_A).next_to(
            ax, UP, buff=0.15).align_to(ax, LEFT)
        kl = VGroup(label(r"grid, \ trapezoid: \ $2/d$", font_size=18, color=KERN),
                    label(r"Monte Carlo: \ $1/2$", font_size=18, color=NO)).arrange(RIGHT, buff=0.5)
        kl.next_to(xl, DOWN, buff=0.2)
        win = label(r"above $d = 4$, \ Monte Carlo wins", font_size=20, color=NO).next_to(kl, DOWN, buff=0.2)
        with self.voiceover(
            "Monte Carlo loses in one dimension, and wins in many. <bookmark mark='a'/> An integral is an "
            "average, so estimate it by averaging f at N random points: the first algorithm on this part's list "
            "of ten, from Los Alamos. <bookmark mark='b'/> The variance of an average of N independent samples is "
            "the variance of one sample over N, <bookmark mark='c'/> so the error falls like one over root N, "
            "whatever the dimension. <bookmark mark='d'/> A grid with N points in d dimensions has spacing N to "
            "the minus one over d, and the trapezoid error falls like N to the minus two over d. "
            "<bookmark mark='e'/> Above four dimensions, Monte Carlo wins, and in the hundreds of dimensions of "
            "finance and physics nothing else is feasible."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            self.play(Create(mc), FadeIn(kl[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(whys[3]))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15), FadeIn(kl[0]),
                      run_time=2)
            vo.wait_until("e")
            self.play(*[b.animate.set_fill(opacity=0.3) for b in bars[:4]], FadeIn(win))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
