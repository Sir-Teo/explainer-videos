from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, METHOD_COL, OPT, PART, illustration, load, loglog, polyline, predict


def unit_square(side, center, color=GREY_C):
    sq = Square(side_length=side, stroke_color=color, stroke_width=1.5).move_to(center)
    return sq


def tiling(sq, pts, nx, ny):
    """The square cut into nx x ny boxes; each box green with exactly one point, red if empty or crowded."""
    side = sq.width
    dl = sq.get_corner(DL)
    c = np.zeros((nx, ny), int)
    for x, y in pts:
        c[min(int(x * nx), nx - 1), min(int(y * ny), ny - 1)] += 1
    g = VGroup()
    for i in range(nx):
        for j in range(ny):
            col = GOOD if c[i, j] == 1 else BAD
            g.add(Rectangle(width=side / nx, height=side / ny, stroke_color=GREY_B, stroke_width=1, fill_color=col,
                            fill_opacity=0.28).move_to(dl + np.array([(i + 0.5) * side / nx, (j + 0.5) * side / ny, 0])))
    return g, int((c == 0).sum()), int((c > 1).sum())


class QMC(VoiceoverScene):
    def construct(self):
        q = load("qmc")
        d = load("discrepancy")
        df = load("drop_first")
        self.card()
        self.points(q)
        self.nets(d)
        self.proof(d)
        self.rates(d)
        self.scramble(d, df)

    def card(self):
        c = chapter_card(5, r"Quasi-Monte Carlo: filling space evenly", r"Can points beat randomness?", part=PART)
        with self.voiceover("Chapter five. Quasi-Monte Carlo: filling space evenly."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def points(self, q):
        boxes = VGroup()
        for pts, col, ttl in ((np.asarray(q["rand"]), GREY_B, r"256 pseudo-random points"),
                              (np.asarray(q["sobol"]), METHOD_COL["Sobol"], r"256 Sobol points")):
            sq = Square(side_length=4.2, stroke_color=GREY_C, stroke_width=1.5)
            dots = VGroup(*[Dot(sq.get_corner(DL) + 4.2 * np.array([x, y, 0]), radius=0.035, color=col) for x, y in pts])
            t = label(ttl, font_size=22, color=col).next_to(sq, UP, buff=0.15)
            boxes.add(VGroup(sq, dots, t))
        boxes.arrange(RIGHT, buff=1.2).move_to(DOWN * 0.1)
        with self.voiceover(
            "Look at what random points actually do. Two hundred and fifty-six of them in a square: they clump, and "
            "leave holes. <bookmark mark='a'/> These are two hundred and fifty-six points of Ilya Sobol's sequence "
            "from 1967. No clumps, no holes. Averaging a smooth function over such points can converge almost like "
            "one over n, instead of one over root n. This chapter is about why, and the next one about when."
        ) as vo:
            self.play(FadeIn(boxes[0][0]), FadeIn(boxes[0][2]), LaggedStart(*[FadeIn(d) for d in boxes[0][1]],
                                                                              lag_ratio=0.005, run_time=2))
            vo.wait_until("a")
            self.play(FadeIn(boxes[1][0]), FadeIn(boxes[1][2]), LaggedStart(*[FadeIn(d) for d in boxes[1][1]],
                                                                              lag_ratio=0.005, run_time=2))
        self.wait(0.4)
        self.clear_scene()

    def nets(self, d):
        sob = np.asarray(d["sobol256"])[:16]
        rnd = np.asarray(d["random256"])[:16]
        sides = []
        groups = VGroup()
        for pts, col, ttl, x in ((sob, METHOD_COL["Sobol"], r"the first 16 Sobol points", -3.3),
                                 (rnd, GREY_B, r"16 random points", 3.3)):
            sq = unit_square(4.6, [x, -0.4, 0])
            dots = VGroup(*[Dot(sq.get_corner(DL) + 4.6 * np.array([a, b, 0]), radius=0.07, color=col) for a, b in pts])
            t = label(ttl, font_size=22, color=col).next_to(sq, UP, buff=0.15)
            groups.add(VGroup(sq, dots, t))
            sides.append((sq, pts))
        shapes = [(1, 16), (2, 8), (4, 4), (8, 2), (16, 1)]
        tiles = []
        for nx, ny in shapes:
            ts, cnt = VGroup(), []
            for sq, pts in sides:
                g, e, dd = tiling(sq, pts, nx, ny)
                ts.add(g)
                cnt.append((e, dd))
            tiles.append((ts, cnt))
        rd = MathTex(r"1 \times 16", font_size=30, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"every box of area $1/16$: green holds exactly one point, red is empty or crowded", font_size=20,
                    color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "What makes them special is a property you can check by eye. Take the first sixteen Sobol points, and "
            "cut the square into sixteen boxes of equal area: sixteen thin columns. Every column holds exactly one "
            "point. <bookmark mark='a'/> Now eight by two, four by four, two by eight, sixteen thin rows. Every box, "
            "of every shape, holds exactly one point. That is a digital net. <bookmark mark='b'/> Sixteen random "
            f"points fail every time: with four by four boxes, {tiles[2][1][1][0]} are empty and "
            f"{tiles[2][1][1][1]} are crowded. The net property holds at every power of two, and it is what the "
            "error bound of the next derivation rewards."
        ) as vo:
            self.play(FadeIn(groups), FadeIn(cap))
            self.play(FadeIn(tiles[0][0]), FadeIn(rd))
            vo.wait_until("a")
            for k in range(1, 5):
                nx, ny = shapes[k]
                self.play(FadeOut(tiles[k - 1][0]), FadeIn(tiles[k][0]),
                          Transform(rd, MathTex(rf"{nx} \times {ny}", font_size=30, color=GREY_A).move_to(rd)), run_time=1.2)
                self.wait(0.6)
            vo.wait_until("b")
            self.play(FadeOut(tiles[4][0]), FadeIn(tiles[2][0]),
                      Transform(rd, MathTex(r"4 \times 4", font_size=30, color=GREY_A).move_to(rd)))
        self.wait(0.4)
        self.clear_scene()

    def proof(self, d):
        vdc = d["vdc"]
        tab = VGroup()
        for r in vdc[:7]:
            bits = r["bits"]
            tab.add(VGroup(MathTex(str(r["n"]), font_size=26), MathTex(bits, font_size=26, color=GREY_A),
                           MathTex(r"0." + bits[::-1], font_size=26, color=METHOD_COL["Sobol"]),
                           MathTex(f"{int(bits[::-1], 2) / 2 ** len(bits):g}", font_size=26, color=OPT)).arrange(RIGHT, buff=0.45))
        for row in tab:
            for j, cell in enumerate(row):
                cell.set_x([-5.9, -5.0, -3.7, -2.4][j])
        tab.arrange(DOWN, buff=0.12)
        for row in tab:
            for j, cell in enumerate(row):
                cell.set_x([-5.9, -5.0, -3.7, -2.4][j])
        tab.to_edge(DOWN, buff=0.4)
        head = label(r"$n$ \quad binary \quad reversed \quad point", font_size=18, color=GREY_B).next_to(tab, UP, buff=0.15)
        head.align_to(tab, LEFT)
        rows = [
            cmath(r"D_n^*", r"=", r"\sup_{a \in [0,1]^d}\Big|\frac{\#\{x_i \in [0, a)\}}{n} - \prod_j a_j\Big|",
                  font_size=32, colors={r"D_n^*": OPT}),
            cmath(r"\Big|\frac1n\sum_i f(x_i) - \int f\Big|", r"\le", r"V_{HK}(f)\; D_n^*", font_size=32,
                  colors={r"\le": GOOD}),
            cmath(r"D_n^*", r"=", r"O\Big(\frac{(\log n)^d}{n}\Big)\ \text{(Sobol, Halton)}\quad\text{vs}\quad "
                  r"O\Big(\sqrt{\tfrac{\log\log n}{n}}\Big)\ \text{(random)}", font_size=30),
            cmath(r"\phi_2(n)", r"=", r"\sum_k a_k\,2^{-k-1}\quad\text{for}\ n = \sum_k a_k 2^k", font_size=32,
                  colors={r"\phi_2(n)": METHOD_COL["Sobol"]}),
        ]
        whys = [why(r"star discrepancy: the worst gap between the share of points in a box anchored at the origin "
                    r"and its volume"),
                why(r"Koksma--Hlawka: variation times discrepancy. In one dimension, integrate by parts: the error is "
                    r"$-\int_0^1 (F_n(x) - x) f'(x)\,dx$"),
                why(r"better for fixed $d$; but $(\log n)^d/n$ beats $n^{-1/2}$ only once $n$ is far beyond $e^d$"),
                why(r"van der Corput: write $n$ in binary and mirror the digits after the point; Sobol does this in "
                    r"every coordinate with a different binary matrix")]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-0.2, buff=0.42, edge=6.9)
        with self.voiceover(
            "Why evenness pays. Measure unevenness by the star discrepancy: over every box anchored at the origin, "
            "the worst gap between the fraction of points inside and the box's volume. <bookmark mark='a'/> The "
            "Koksma–Hlawka inequality bounds the integration error by the function's variation times that "
            "discrepancy. In one dimension it is integration by parts. <bookmark mark='b'/> For Sobol and Halton "
            "points the discrepancy falls like log n to the power d, over n; for random points like one over root n. "
            "Better, but only once n is far beyond e to the d. <bookmark mark='c'/> And the "
            "construction is beautifully simple. The van der Corput sequence writes n in binary and mirrors the "
            "digits after the point: one becomes a half, two a quarter, three three quarters. Each new point lands in "
            "the largest gap. Sobol does this in every coordinate with a different binary matrix; SciPy uses Joe "
            "and Kuo's direction numbers, from 2008."
        ) as vo:
            for i, mk in enumerate("abc"):
                step(i)
                vo.wait_until(mk)
            step(3)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.3, run_time=3))
        self.wait(0.4)
        self.clear_scene()

    def rates(self, d):
        r2, r16 = d["rows"]["2"], d["rows"]["16"]
        g = loglog(1.7, 4.3, -4.5, -1, r"points $n$", r"$L_2$-star discrepancy", x_length=5.6, y_length=3.8,
                   xt=[2, 3, 4], yt=[-4, -3, -2, -1], font_size=14).to_corner(UL, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        cols = {"random": GREY_B, "Halton": QC.THETA, "Sobol": METHOD_COL["Sobol"]}
        lines2 = VGroup(*[polyline(ax, np.log10(r2["ns"]), np.clip(np.log10(r2[k]), -4.5, -1), cols[k]) for k in cols])
        lines16 = VGroup(*[DashedVMobject(polyline(ax, np.log10(r16["ns"]), np.clip(np.log10(r16[k]), -4.5, -1), cols[k],
                                                   dots=False)[0], num_dashes=25) for k in cols])
        leg = legend([(cols[k], k) for k in cols] + [(GREY_C, r"dashed: 16 dimensions")], font_size=16)
        leg.next_to(g, DOWN, buff=0.2).align_to(g, LEFT)
        s2 = np.polyfit(np.log10(r2["ns"]), np.log10(r2["Sobol"]), 1)[0]
        sr = np.polyfit(np.log10(r2["ns"]), np.log10(r2["random"]), 1)[0]
        boxes = VGroup()
        for pts, col, ttl in ((d["halton_29_30"], QC.THETA, r"Halton, coordinates 29 and 30"),
                              (d["sobol_29_30"], METHOD_COL["Sobol"], r"Sobol (Joe--Kuo), 29 and 30")):
            sq = Square(side_length=2.9, stroke_color=GREY_C, stroke_width=1.5)
            dots = VGroup(*[Dot(sq.get_corner(DL) + 2.9 * np.array([x, y, 0]), radius=0.018, color=col)
                            for x, y in np.asarray(pts)])
            boxes.add(VGroup(sq, dots, label(ttl, font_size=17, color=col).next_to(sq, UP, buff=0.1)))
        boxes.arrange(RIGHT, buff=0.4).to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
        side = wrapped_label(rf"in 2 dimensions Sobol's slope is {s2:.2f} against random's {sr:.2f}; in 16, with these $n$, "
                             r"neither low-discrepancy set beats random points on this measure yet", 6.0, 18, GREY_A)
        side.next_to(boxes, DOWN, buff=0.35)
        with self.voiceover(
            "Measured. In two dimensions the discrepancy of Sobol and Halton points falls with a slope near minus "
            f"one, {s2:.2f} for Sobol, against {sr:.2f} for random points. <bookmark mark='a'/> In sixteen dimensions, "
            "dashed, the story at these sizes is different: the low-discrepancy sets have not yet overtaken random "
            "points at all. The log n to the d is still winning. <bookmark mark='b'/> And dimension can bite in a "
            "second way. Plot Halton's coordinates twenty-nine and thirty, a thousand points: they lie on a few "
            "stripes, because their large prime bases cycle in step. Sobol's, with Joe and Kuo's direction numbers, "
            "chosen to keep such projections even, fill the square."
        ) as vo:
            self.play(FadeIn(g), Create(lines2), FadeIn(leg[:3]))
            vo.wait_until("a")
            self.play(Create(lines16), FadeIn(leg[3]))
            vo.wait_until("b")
            self.play(FadeIn(boxes), FadeIn(side))
        self.wait(0.5)
        self.clear_scene()

    def scramble(self, d, df):
        est = np.asarray(d["rqmc"])
        ex = d["exact"]
        m, se = est.mean(), est.std(ddof=1) / np.sqrt(len(est))
        g = axes([10.43, 10.47], [0, 11], x_length=6.0, y_length=3.4, xlabel=r"call price from 1{,}024 points",
                 xticks=[10.44, 10.45, 10.46], xfmt=lambda v: f"{v:.2f}", font_size=15).to_edge(LEFT, buff=0.8).shift(UP * 0.4)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(e, k + 1), radius=0.07, color=METHOD_COL["Sobol"]) for k, e in enumerate(est)])
        truth = DashedLine(ax.c2p(ex, 0), ax.c2p(ex, 11), stroke_color=WHITE, stroke_width=1.5)
        bar = Line(ax.c2p(m - 1.96 * se, 0.4), ax.c2p(m + 1.96 * se, 0.4), stroke_color=GOOD, stroke_width=6)
        txt = MathTex(rf"{m:.4f} \pm {1.96 * se:.4f}\ \ (\text{{exact}}\ {ex:.4f})", font_size=28, color=GOOD)
        txt.next_to(g, DOWN, buff=0.25)
        rows = df["rows"]
        q = predict(r"Drop the first Sobol point (the origin) to avoid $\Phi^{-1}(0) = -\infty$. Harmless?", width=5.4,
                    font_size=21).to_corner(UR, buff=0.4)
        tab = VGroup(label(r"error of scrambled Sobol on $\int e^{u_1 + u_2}$, 100 scramblings", font_size=18,
                           color=GREY_A))
        for n_, r in rows.items():
            tab.add(MathTex(rf"n = {int(n_):,}".replace(",", "{,}") + rf":\ \ \text{{keep}}\ {r['keep']:.1e}\ \ "
                            rf"\text{{drop}}\ {r['drop']:.1e}\ \ (\times {r['drop'] / r['keep']:.0f})", font_size=24))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(q, DOWN, buff=0.35).align_to(q, LEFT)
        last = list(rows.values())[-1]
        with self.voiceover(
            "One weakness: a deterministic set of points has no error bar. Art Owen's fix, scrambling, randomises "
            "the digits while keeping the net property. Ten independently scrambled copies give ten unbiased "
            "estimates of the call, and their spread is an honest error bar, and much smaller than plain Monte "
            "Carlo's for the same points. <bookmark mark='a'/> Pause and predict. The first Sobol point is the "
            "origin, where the inverse normal is minus infinity. Many codes simply skip it. Harmless? "
            "<bookmark mark='b'/> No. Skipping it breaks the net. On a smooth integral the error with the point "
            f"dropped is {list(rows.values())[0]['drop'] / list(rows.values())[0]['keep']:.0f} times larger at "
            f"sixty-four points and {last['drop'] / last['keep']:.0f} times at four thousand, growing like root n, "
            "as Owen showed in 2022. Scramble instead; a scrambled point is never exactly zero."
        ) as vo:
            self.play(FadeIn(g), FadeIn(truth), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.2), FadeIn(bar),
                      FadeIn(txt))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.3, run_time=2.5))
        self.wait(0.5)
        self.clear_scene()
