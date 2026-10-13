from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis3.common import load, plain_axes, polyline, saw, saw_partial
from videos.analysis3.compute import trap


def signed_area(ax, x, y, pos=C.CONNECTED_SET, neg=C.PATHOLOGY, opacity=0.45) -> VGroup:
    """The region between y and 0, green where y > 0 and red where y < 0 (one polygon per run of constant sign)."""
    g, s = VGroup(), np.sign(y)
    start = 0
    for i in range(1, len(x) + 1):
        if i == len(x) or s[i] != s[start]:
            if s[start] != 0 and i - start > 1:
                xs, ys = x[start:i], y[start:i]
                pts = [ax.c2p(xs[0], 0)] + [ax.c2p(a, b) for a, b in zip(xs, ys)] + [ax.c2p(xs[-1], 0)]
                g.add(Polygon(*pts, stroke_width=0, fill_color=pos if s[start] > 0 else neg, fill_opacity=opacity))
            start = i
    return g


def saw_graph(ax, a, b, color=WHITE, stroke_width=3) -> VGroup:
    """The sawtooth (pi - x)/2 (period 2 pi) on [a, b], drawn as separate segments between the jumps."""
    g = VGroup()
    k0 = int(np.floor(a / (2 * np.pi)))
    for k in range(k0, int(np.ceil(b / (2 * np.pi))) + 1):
        lo, hi = max(a, 2 * np.pi * k), min(b, 2 * np.pi * (k + 1))
        if hi - lo > 1e-6:
            lo_, hi_ = lo + 1e-4, hi - 1e-4
            g.add(Line(ax.c2p(lo_, float(saw(np.array([lo_]))[0])), ax.c2p(hi_, float(saw(np.array([hi_]))[0])),
                       color=color, stroke_width=stroke_width))
    return g


class FourierSeries(VoiceoverScene):
    def construct(self):
        self.card()
        self.ortho()
        self.best()
        self.bessel()
        self.dirichlet()
        self.dini()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(14, r"Fourier series: \ the best approximation",
                            r"Which trigonometric polynomial is closest to $f$?", lit=(1807, 1829), part=3)
        with self.voiceover(
            "Chapter fourteen. In 1807 Fourier claimed that every function is a sum of sines and cosines, and in 1829 "
            "Dirichlet proved it for a large class of functions."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def ortho(self):
        d = load("fourier")
        gram = d["gram"]
        x = np.linspace(-np.pi, np.pi, 1200)
        ax = plain_axes([-np.pi, np.pi, np.pi / 2], [-1.2, 1.2, 1], 6.4, 2.2).move_to([-3.4, 1.55, 0])
        bx = plain_axes([-np.pi, np.pi, np.pi / 2], [-1.2, 1.2, 1], 6.4, 2.2).move_to([-3.4, -1.55, 0])
        s2 = polyline(ax, x, np.sin(2 * x), color=C.SEQ, stroke_width=3)
        s3 = polyline(ax, x, np.sin(3 * x), color=C.APPROX, stroke_width=3)
        lab = MathTex(r"\sin 2x", r",\ \sin 3x", font_size=28).next_to(ax, UP, buff=0.08)
        lab[0].set_color(C.SEQ)
        lab[1].set_color(C.APPROX)
        prod = np.sin(2 * x) * np.sin(3 * x)
        sq = np.sin(3 * x) ** 2
        pg = polyline(bx, x, prod, color=WHITE, stroke_width=2.5)
        pa = signed_area(bx, x, prod)
        I1, I2 = trap(prod, x), trap(sq, x)
        assert abs(I1) < 1e-6 and abs(I2 - np.pi) < 1e-6
        pl = MathTex(rf"\int \sin 2x \sin 3x\,dx = {abs(I1):.4f}", font_size=28).next_to(bx, UP, buff=0.08)
        qg = polyline(bx, x, sq, color=WHITE, stroke_width=2.5)
        qa = signed_area(bx, x, sq)
        ql = MathTex(rf"\int \sin^2 3x\,dx = {I2:.4f} = \pi", font_size=28).next_to(bx, UP, buff=0.08)
        # the Gram matrix of e^{inx}, |n| <= 3
        ks = list(range(-3, 4))
        cs = 0.43
        o = np.array([2.35, 2.55, 0])
        cells = VGroup()
        for i in range(7):
            for j in range(7):
                v = float(gram[i, j])
                sq_ = Square(side_length=cs * 0.94, stroke_width=0, fill_color=C.INNER if v > 0.5 else GREY_E,
                             fill_opacity=0.9 if v > 0.5 else 0.6).move_to(o + np.array([j * cs, -i * cs, 0]))
                cells.add(VGroup(sq_, MathTex(f"{abs(v):.0f}", font_size=19, color=WHITE if v > 0.5 else GREY_B)
                                 .move_to(sq_)))
        rl = VGroup(*[MathTex(str(k), font_size=20, color=GREY_B).next_to(cells[i * 7], LEFT, buff=0.12)
                      for i, k in enumerate(ks)])
        cl_ = VGroup(*[MathTex(str(k), font_size=20, color=GREY_B).next_to(cells[j], UP, buff=0.1)
                       for j, k in enumerate(ks)])
        gl = MathTex(r"\frac{1}{2\pi}\int_{-\pi}^{\pi} e^{imx}\,\overline{e^{inx}}\,dx = \delta_{mn}", font_size=30,
                     color=C.INNER).next_to(cells, DOWN, buff=0.25)
        gl2 = label(r"(Rudin 8.9; \ computed for $|m|, |n| \le 3$)", font_size=20, color=GREY_B).next_to(gl, DOWN,
                                                                                                   buff=0.1)
        coef = VGroup(MathTex(r"c_n = \frac{1}{2\pi}\int_{-\pi}^{\pi} f(x)\, e^{-inx}\,dx", font_size=30, color=C.FREQ),
                      label(r"$f$'s coordinate along $e^{inx}$", font_size=24, color=GREY_A)
                      ).arrange(DOWN, buff=0.1).next_to(gl2, DOWN, buff=0.35)
        # the opening question, drawn: a triangle wave and its closest polynomial of degree 3 (its Fourier sum)
        tri = 1 - 2 * np.abs(x) / np.pi
        t3 = 8 / np.pi**2 * (np.cos(x) + np.cos(3 * x) / 9)
        assert np.abs(tri - t3).max() < 0.1
        q_f = polyline(ax, x, tri, color=WHITE, stroke_width=3)
        q_t = polyline(ax, x, t3, color=C.FREQ, stroke_width=3)
        q_l = label(r"$f$, \ and the trigonometric polynomial of degree $\le 3$ closest to it", font_size=24).next_to(
            ax, UP, buff=0.08)
        q_l[0].set_color(WHITE)
        with self.voiceover(
            "Rudin starts not from convergence but from a geometric question: which trigonometric polynomial is "
            "closest to f? <bookmark mark='a'/> The key fact is orthogonality. Take two different sine waves, <bookmark mark='b'/> "
            "multiply them, and integrate over a period: the positive and negative parts cancel exactly. "
            "<bookmark mark='c'/> The same wave times itself is positive, and integrates to pi. "
            "<bookmark mark='d'/> In complex form, the exponentials e to the i n x behave like perpendicular unit "
            "vectors: the average of one times the conjugate of another is one if they're the same and zero "
            "otherwise. <bookmark mark='e'/> So the Fourier coefficient c n, the average of f times e to the minus "
            "i n x, is the coordinate of f along the n-th axis."
        ) as vo:
            self.play(Create(ax), Create(bx), Create(q_f), FadeIn(q_l))
            self.play(Create(q_t))
            vo.wait_until("a")
            self.play(FadeOut(q_f), FadeOut(q_t), FadeOut(q_l), Create(s2), Create(s3), FadeIn(lab))
            vo.wait_until("b")
            self.play(FadeIn(pa), Create(pg), FadeIn(pl))
            vo.wait_until("c")
            self.play(FadeOut(pa), FadeOut(pg), FadeOut(pl), FadeIn(qa), Create(qg), FadeIn(ql))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.01), FadeIn(rl), FadeIn(cl_),
                      FadeIn(gl), FadeIn(gl2), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(coef))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def best(self):
        d = load("fourier")
        x, best, worse, samples, sN = d["x"], float(d["best"]), d["worse"], d["samples"], d["sN"]
        f = saw(x)
        ax = plain_axes([-np.pi, np.pi, np.pi / 2], [-2.0, 2.0, 1], 6.0, 2.5).move_to([-3.6, 1.6, 0])
        sg = saw_graph(ax, -np.pi, np.pi)
        bg = polyline(ax, x, sN, color=C.EPS, stroke_width=3)
        tg = polyline(ax, x, samples[0], color=C.APPROX, stroke_width=2.5)
        al = MathTex(r"f", r",\ s_6", r",\ t", font_size=28).next_to(ax, UP, buff=0.08)
        al[1].set_color(C.EPS)
        al[2].set_color(C.APPROX)
        # histogram of the 500 competitors' errors
        edges = np.arange(0.0, 4.21, 0.15)
        counts, _ = np.histogram(np.clip(worse, 0, 4.19), bins=edges)
        hx = plain_axes([0, 4.2, 1], [0, int(counts.max()) + 5, 20], 5.4, 2.4, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 0}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([3.5, 1.5, 0])
        bars = VGroup()
        for a, b, c in zip(edges[:-1], edges[1:], counts):
            if c:
                p0, p1 = hx.c2p(a, 0), hx.c2p(b, c)
                bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=1, stroke_color=C.APPROX,
                                   fill_color=C.APPROX, fill_opacity=0.5).move_to((p0 + p1) / 2))
        bl = Line(hx.c2p(best, 0), hx.c2p(best, counts.max() + 5), color=C.EPS, stroke_width=4)
        bll = MathTex(rf"s_6: {best:.4f}", font_size=24, color=C.EPS).next_to(bl, UP, buff=0.05)
        hl = label(r"$\int |f - t|^2$ \ for 500 random $t$ of degree $\le 6$", font_size=22).next_to(hx, UP, buff=0.35)
        hm = label(rf"smallest: \ ${worse.min():.4f}$", font_size=22, color=C.APPROX).next_to(hx, DOWN, buff=0.35)
        assert worse.min() > best
        # the right triangle (schematic)
        A = np.array([-6.2, -3.2, 0])
        plane = Polygon(A, A + np.array([4.6, 0, 0]), A + np.array([5.8, 1.1, 0]), A + np.array([1.2, 1.1, 0]),
                        stroke_color=GREY_B, stroke_width=1.5, fill_color=GREY_E, fill_opacity=0.5)
        pl_l = label(r"trigonometric polynomials of degree $\le N$", font_size=18, color=GREY_B).next_to(plane, DOWN,
                                                                                                    buff=0.08)
        S = np.array([-3.0, -2.6, 0])
        F = S + np.array([0, 2.2, 0])
        T = np.array([-4.9, -2.85, 0])
        tri = VGroup(Line(F, S, color=C.PATHOLOGY, stroke_width=4), Line(S, T, color=C.APPROX, stroke_width=3),
                     Line(F, T, color=WHITE, stroke_width=3))
        ra = RightAngle(Line(S, F), Line(S, T), length=0.2, color=GREY_B, quadrant=(1, 1))
        pts = VGroup(Dot(F, color=WHITE), Dot(S, color=C.EPS), Dot(T, color=C.APPROX))
        plab = VGroup(MathTex("f", font_size=30).next_to(F, UP, buff=0.08),
                      MathTex("s_N", font_size=30, color=C.EPS).next_to(S, RIGHT, buff=0.1),
                      MathTex("t", font_size=30, color=C.APPROX).next_to(T, DOWN, buff=0.08))
        tag = schematic_tag().scale(0.8).next_to(plane, UP, buff=0.1).align_to(plane, LEFT)
        t0 = samples[0]
        h2, l2 = trap((f - t0) ** 2, x), trap((sN - t0) ** 2, x)
        eq = VGroup(
            label(r"\textbf{Rudin 8.11}: \ $f - s_N$ is orthogonal to every $t$ of degree $\le N$, \ so", font_size=24),
            MathTex(r"\int |f - t|^2", r"=", r"\int |f - s_N|^2", r"+", r"\int |s_N - t|^2", font_size=32),
            MathTex(rf"{h2:.4f}", r"=", rf"{best:.4f}", r"+", rf"{l2:.4f}", font_size=32),
            label(r"the Fourier partial sum is the foot of the perpendicular", font_size=24, color=C.EPS),
        ).arrange(DOWN, buff=0.18).move_to([2.9, -2.1, 0])
        for k, col in ((0, WHITE), (2, C.PATHOLOGY), (4, C.APPROX)):
            eq[1][k].set_color(col)
            eq[2][k].set_color(col)
        assert abs(h2 - best - l2) < 1e-6
        with self.voiceover(
            "<bookmark mark='a'/> Rudin's theorem 8.11: among all trigonometric polynomials of degree at most N, the "
            "one whose coefficients are f's Fourier coefficients is the closest to f in mean square. "
            "<bookmark mark='b'/> Here's the sawtooth, its Fourier partial sum of degree six, and one competitor. "
            "<bookmark mark='c'/> I tried five hundred random competitors near the partial sum: every one has a "
            "larger squared error. The best of them is nearly twice as far. <bookmark mark='d'/> The reason is "
            "Pythagoras. The error f minus s N is orthogonal to every trigonometric polynomial of degree N, so for "
            "any competitor t, the squared distance from f to t is the squared distance to s N plus the squared "
            "distance from s N to t. <bookmark mark='e'/> The Fourier partial sum is the foot of the perpendicular "
            "from f. This is the first glimpse of Hilbert space, the subject of Part 6."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(sg), FadeIn(al[0]))
            vo.wait_until("b")
            self.play(Create(bg), FadeIn(al[1]))
            self.play(Create(tg), FadeIn(al[2]))
            vo.wait_until("c")
            self.play(Create(hx), FadeIn(hl), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.05),
                      run_time=2.0)
            self.play(Create(bl), FadeIn(bll), FadeIn(hm))
            vo.wait_until("d")
            self.play(FadeIn(plane), FadeIn(pl_l), FadeIn(tag), FadeIn(pts), FadeIn(plab))
            self.play(Create(tri), Create(ra), FadeIn(eq[0]))
            self.play(FadeIn(eq[1]))
            self.play(FadeIn(eq[2]))
            vo.wait_until("e")
            self.play(FadeIn(eq[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bessel(self):
        d = load("fourier")
        tot = float(d["tot"])
        W = 9.0
        x0 = -W / 2 - 0.4
        y = -0.55
        outline = Rectangle(width=W, height=0.7, stroke_color=WHITE, stroke_width=2).move_to([x0 + W / 2, y, 0])
        tl = MathTex(r"\frac{1}{2\pi}\int_{-\pi}^{\pi} |f|^2 = \frac{\pi^2}{12} = " + f"{tot:.4f}", font_size=30)
        tl.next_to(outline, UP, buff=0.2)
        segs = VGroup()
        acc = 0.0
        cols = [C.FREQ, C.CLOSED_SET, C.EPS, C.CONNECTED_SET, C.SEQ, C.INNER]
        for n in range(1, 61):
            w = 0.5 / n**2  # |c_n|^2 + |c_{-n}|^2 for the sawtooth
            segs.add(Rectangle(width=W * w / tot, height=0.7, stroke_width=0.6 if n < 12 else 0,
                               stroke_color=BLACK, fill_color=cols[(n - 1) % len(cols)], fill_opacity=0.85)
                     .move_to([x0 + W * (acc + w / 2) / tot, y, 0]))
            acc += w
        assert acc < tot
        nl = VGroup(*[MathTex(rf"n = \pm{n}", font_size=20, color=GREY_A).next_to(segs[n - 1], DOWN, buff=0.12)
                      for n in (1, 2)])
        rows = VGroup(
            MathTex(r"\int |f|^2 = \int |s_N|^2 + \int |f - s_N|^2 \ \ge\ \int |s_N|^2", font_size=30),
            MathTex(r"\sum_{|n| \le N} |c_n|^2 \le \frac{1}{2\pi}\int_{-\pi}^{\pi} |f|^2 \quad \text{for every } N",
                    font_size=34, color=C.EPS),
        ).arrange(DOWN, buff=0.25).to_edge(UP, buff=0.35)
        head_l = label(r"\textbf{Bessel's inequality} \ (Rudin 8.12): \ Pythagoras with $t = 0$", font_size=26,
                       color=GREY_A).next_to(rows, DOWN, buff=0.15)
        tab = VGroup(*[MathTex(rf"N = {N}: \ {v:.4f}", font_size=24) for N, v in
                       zip((1, 2, 5, 10, 100, 1000), d["bessel"])]).arrange(RIGHT, buff=0.45)
        tab.next_to(outline, DOWN, buff=0.7)
        out = VGroup(label(r"so $c_n \to 0$ \ (the Riemann--Lebesgue lemma, for Riemann-integrable $f$)", font_size=26,
                           color=C.EPS),
                     label(r"whether the bar fills completely is chapter 15", font_size=24, color=GREY_A)
                     ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.2)
        # Pythagoras first, on the same bar: the energy of s_3 plus the energy of the error is the energy of f
        e3 = sum(0.5 / n**2 for n in range(1, 4))
        pa = Rectangle(width=W * e3 / tot, height=0.7, stroke_width=0, fill_color=C.SEQ, fill_opacity=0.6).move_to(
            [x0 + W * e3 / tot / 2, y, 0])
        pb = Rectangle(width=W * (tot - e3) / tot, height=0.7, stroke_color=C.PATHOLOGY, stroke_width=2,
                       fill_color=C.PATHOLOGY, fill_opacity=0.3).move_to([x0 + W * (e3 + (tot - e3) / 2) / tot, y, 0])
        pl = VGroup(MathTex(rf"\tfrac{{1}}{{2\pi}}\textstyle\int |s_3|^2 = {e3:.4f}", font_size=26, color=C.SEQ).next_to(
            pa, DOWN, buff=0.2),
                    MathTex(rf"\tfrac{{1}}{{2\pi}}\textstyle\int |f - s_3|^2 = {tot - e3:.4f}", font_size=26,
                            color=C.PATHOLOGY).next_to(pb, DOWN, buff=0.2))
        if pl[1].get_left()[0] < pl[0].get_right()[0] + 0.2:
            pl[1].next_to(pl[0], RIGHT, buff=0.3)
        assert abs(e3 - 49 / 72) < 1e-12 and 0 < tot - e3 < tot
        with self.voiceover(
            "<bookmark mark='a'/> Take the competitor t to be zero. Pythagoras says the energy of f is the energy of "
            "its partial sum plus the energy of the error, so the partial sum has less energy than f. "
            "<bookmark mark='b'/> By orthogonality, the energy of the partial sum is the sum of the squared "
            "coefficients. That's Bessel's inequality: the sum of the squares of the Fourier coefficients never "
            "exceeds the average of f squared. <bookmark mark='c'/> For the sawtooth, the bar's length is pi squared "
            "over twelve, and the squared coefficients, one over two n squared for each pair plus and minus n, stack "
            "up inside it. <bookmark mark='d'/> In particular the coefficients go to zero. Whether they fill the bar "
            "completely is the question of the next chapter."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(outline), FadeIn(tl))
            self.play(GrowFromEdge(pa, LEFT), FadeIn(pl[0]))
            self.play(FadeIn(pb), FadeIn(pl[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(head_l))
            vo.wait_until("c")
            self.play(FadeOut(pa), FadeOut(pb), FadeOut(pl))
            self.play(GrowFromEdge(segs[0], LEFT), FadeIn(nl[0]), FadeIn(tab[0]), run_time=0.8)
            self.play(GrowFromEdge(segs[1], LEFT), FadeIn(nl[1]), FadeIn(tab[1]), run_time=0.6)
            self.play(LaggedStart(*[GrowFromEdge(s_, LEFT) for s_ in segs[2:]], lag_ratio=0.12),
                      LaggedStart(*[FadeIn(t_) for t_ in tab[2:]], lag_ratio=0.5), run_time=4.0)
            vo.wait_until("d")
            self.play(FadeIn(out))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dirichlet(self):
        d = load("fourier")
        Ns, leb = d["Ns"], d["leb"]
        t = np.linspace(-np.pi, np.pi, 4001)

        def D(N):
            with np.errstate(invalid="ignore", divide="ignore"):
                v = np.sin((N + 0.5) * t) / np.sin(t / 2)
            v[np.isclose(t, 0)] = 2 * N + 1
            return v

        ax = plain_axes([-np.pi, np.pi, np.pi / 2], [-10, 42, 10], 6.8, 4.6).move_to([-3.2, -0.6, 0])
        shown = (5, 10, 20)
        curves = [VGroup(signed_area(ax, t, D(N), opacity=0.3), polyline(ax, t, D(N), color=C.FREQ, stroke_width=2.5))
                  for N in shown]
        nl = [MathTex(rf"D_{{{N}}}: \text{{ peak }} {2 * N + 1}", font_size=28, color=C.FREQ).next_to(ax, UP, buff=0.08)
              for N in shown]
        head = VGroup(MathTex(r"s_N(x) = \frac{1}{2\pi}\int_{-\pi}^{\pi} f(x - t)\,D_N(t)\,dt, \qquad "
                              r"D_N(t) = \sum_{|n| \le N} e^{int} = \frac{\sin\!\left((N + \frac12)t\right)}{\sin(t/2)}",
                              font_size=30),
                      label(r"\textbf{Rudin 8.13}: \ the partial sums average $f$ against the Dirichlet kernel",
                            font_size=24, color=GREY_A)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.25)
        tab = VGroup(MathTex(r"N", r"\quad \frac{1}{2\pi}\int |D_N|", font_size=26, color=GREY_A))
        for N, L_ in zip(Ns, leb):
            if N in (1, 5, 20, 100, 500):
                tab.add(MathTex(rf"{int(N)}", rf"\quad {L_:.3f}", font_size=26))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([1.4, -0.55, 0])
        regrid(tab, gap=0.3)
        asym = MathTex(r"\approx \tfrac{4}{\pi^2}\ln N + 1.27", font_size=28, color=C.FREQ).next_to(tab, DOWN, buff=0.25,
                                                                                         aligned_edge=LEFT)
        notes = VGroup(label(r"signed area: \ always $2\pi$", font_size=22, color=GREY_A),
                       label(r"area of $|D_N|$: \ grows without bound", font_size=22, color=C.PATHOLOGY),
                       label(r"unlike the Landau kernel, \ $D_N$ is not positive", font_size=22, color=GREY_A),
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.2, 1.25, 0])
        for N in shown:
            assert abs(trap(D(N), t) - 2 * np.pi) < 1e-3
        assert np.all(np.diff(leb) > 0)
        card = museum_card(r"du Bois-Reymond's function", r"P. du Bois-Reymond, 1873",
                           r"`the Fourier series of a continuous function converges'",
                           r"Rudin, remark after 8.14; \ Part 8: Banach--Steinhaus", width=4.6).scale(0.8)
        card.to_corner(DR, buff=0.2)
        with self.voiceover(
            "<bookmark mark='a'/> To study convergence, write the partial sum as an integral: it's an average of f "
            "against the Dirichlet kernel, the sum of the exponentials up to N. <bookmark mark='b'/> Like the Landau "
            "kernel, it has total signed area two pi and a tall central peak. Unlike it, it isn't positive: its side "
            "lobes alternate in sign and don't shrink fast. <bookmark mark='c'/> The area under its absolute value, "
            "computed here, grows without bound, like the logarithm of N. <bookmark mark='d'/> That growth has a "
            "price. Du Bois-Reymond found a continuous function whose Fourier series diverges at a point; in Part 8, "
            "the uniform boundedness principle will turn this table of numbers into a proof that such functions "
            "exist."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(curves[0]), FadeIn(nl[0]))
            vo.wait_until("b")
            for k in range(1, 3):
                self.play(ReplacementTransform(curves[k - 1], curves[k]), FadeTransform(nl[k - 1], nl[k]), run_time=1.2)
            self.play(FadeIn(notes[0]), FadeIn(notes[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(asym), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(card, scale=0.95))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dini(self):
        d = load("fourier")
        dN, dini = d["dN"], d["dini"]
        x0 = 1.0
        f0 = (np.pi - x0) / 2
        t = np.linspace(-np.pi, np.pi, 8001)
        ft = saw(x0 - t)
        with np.errstate(invalid="ignore", divide="ignore"):
            g = (ft - f0) / np.sin(t / 2)
        g[np.isclose(t, 0)] = 1.0
        g[np.isclose(t, x0, atol=1e-9)] = 0.0
        ax = plain_axes([-np.pi, np.pi, np.pi / 2], [-6.6, 6.6, 2], 6.6, 4.0).move_to([-3.3, -0.7, 0])
        assert np.abs(g).max() < 6.6  # so g and every g sin((N + 1/2)t) stay inside the axes
        num = ft - f0
        numg = VGroup(polyline(ax, t[t < x0 - 1e-3], num[t < x0 - 1e-3], color=GREY_B, stroke_width=3),
                      polyline(ax, t[t > x0 + 1e-3], num[t > x0 + 1e-3], color=GREY_B, stroke_width=3))
        numl = label(r"$f(x - t) - f(x)$: \ the sawtooth at $x = 1$, \ shifted", font_size=24, color=GREY_B)
        gg = VGroup(polyline(ax, t[t < x0 - 1e-3], g[t < x0 - 1e-3], color=C.FUNC, stroke_width=3),
                    polyline(ax, t[t > x0 + 1e-3], g[t > x0 + 1e-3], color=C.FUNC, stroke_width=3))
        nT = ValueTracker(3)

        def osc():
            N = round(nT.get_value())
            y = g * np.sin((N + 0.5) * t)
            return VGroup(signed_area(ax, t, y, opacity=0.35), polyline(ax, t, y, color=C.APPROX, stroke_width=1.5))

        og = always_redraw(osc)
        val = always_redraw(lambda: MathTex(
            rf"N = {round(nT.get_value())}: \ \frac{{1}}{{2\pi}}\int g(t)\sin\!\big((N + \tfrac12)t\big)dt = "
            rf"{nz(trap(g * np.sin((round(nT.get_value()) + 0.5) * t), t) / (2 * np.pi), 4):+.4f}", font_size=26,
            color=C.APPROX).next_to(ax, DOWN, buff=0.2))
        for N in (3, 10, 40):
            n = np.arange(1, N + 1)
            sN_x0 = np.sum(np.sin(n * x0) / n)
            assert abs(trap(g * np.sin((N + 0.5) * t), t) / (2 * np.pi) - (sN_x0 - f0)) < 2e-4
        head = VGroup(label(r"\textbf{Rudin 8.14} \ (Dini's test): \ if $|f(x + t) - f(x)| \le M|t|$ near $t = 0$, "
                            r"then $s_N(x) \to f(x)$", font_size=28),
                      MathTex(r"s_N(x) - f(x) = \frac{1}{2\pi}\int_{-\pi}^{\pi} g(t)\,\sin\!\big((N + \tfrac12)t\big)\,dt,"
                              r"\quad g(t) = \frac{f(x - t) - f(x)}{\sin(t/2)}", font_size=30)
                      ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.25)
        gl = label(r"$g$ is bounded \ (Lipschitz at $x$)", font_size=24, color=C.FUNC).next_to(ax, UP, buff=0.08)
        numl.move_to(gl)
        why_ = label(r"$\to 0$ by Bessel, \ applied to $g$", font_size=24, color=C.EPS)
        cells = [(r"N", r"s_N(\pi/2)", r"s_N(1)")] + [(f"{int(N)}", f"{a:.5f}", f"{b:.5f}") for N, (a, b) in
                                                       zip(dN, dini)] + [(r"f", f"{np.pi / 4:.5f}", f"{f0:.5f}")]
        tab = VGroup()
        for i, (c0, c1, c2) in enumerate(cells):
            col = GREY_A if i == 0 else (C.EPS if i == len(cells) - 1 else WHITE)
            row = VGroup(MathTex(c0, font_size=26, color=col), MathTex(c1, font_size=26, color=col),
                         MathTex(c2, font_size=26, color=col))
            y_ = 0.9 - 0.38 * i
            row[0].move_to([2.15, y_, 0], aligned_edge=RIGHT)
            row[1].move_to([2.55, y_, 0], aligned_edge=LEFT)
            row[2].move_to([4.35, y_, 0], aligned_edge=LEFT)
            tab.add(row)
        why_.next_to(tab, UP, buff=0.2)
        out = label(r"Part 2 proved $\sum \frac{\sin nx}{n}$ converges at every $x$; \ now we know the sum: "
                    r"$\frac{\pi - x}{2}$ on $(0, 2\pi)$", font_size=24, color=C.EPS).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "<bookmark mark='a'/> Pointwise convergence needs a little regularity. Dini's test: if f is Lipschitz at "
            "x, the partial sums converge to f of x. Subtract f of x and the error becomes the integral of a function "
            "g against a sine of higher and higher frequency. <bookmark mark='b'/> Because f is Lipschitz at x, g is "
            "bounded, even near zero, where the denominator vanishes. Here it is for the sawtooth at x equal to one; "
            "its jump is harmless. <bookmark mark='c'/> As N grows, the positive and negative lobes cancel better and "
            "better, and Bessel's inequality, applied to g, shows the integral goes to zero. <bookmark mark='d'/> "
            "Computed: at pi over two and at one, the partial sums close in on the sawtooth's values. "
            "<bookmark mark='e'/> Part 2 proved that this series converges everywhere, but not to what. Now we know: "
            "pi minus x, over two."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax))
            self.play(Create(numg), FadeIn(numl))
            vo.wait_until("b")
            self.play(ReplacementTransform(numg, gg), FadeTransform(numl, gl), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(og), FadeIn(val))
            self.play(nT.animate.set_value(40), run_time=5.0, rate_func=linear)
            self.play(FadeIn(why_))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("e")
            self.play(FadeIn(out))
        for m in (og, val):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
