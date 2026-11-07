from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs52.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


def sci(v: float, digits: int = 1) -> str:
    """A number as TeX: 2.9 x 10^{-5}."""
    e = math.floor(math.log10(abs(v)))
    return rf"{v / 10 ** e:.{digits}f} \times 10^{{{e}}}"


def mode_icon(k: int, n: int, width=1.5, height=0.36, color=GREY_B):
    """Sine mode k sampled on n interior points (plus the zero ends), as a small polyline."""
    pts = [[width * j / (n + 1), height * math.sin(k * math.pi * j / (n + 1)), 0] for j in range(n + 2)]
    return VMobject(color=color, stroke_width=2).set_points_as_corners(pts)


def spectrum_bars(vals, half, x0=-5.6, y0=-1.6, width=11.2, height=3.3, top=2.4):
    """One bar per sine mode: the size of the error's component along it."""
    step = width / len(vals)
    g = VGroup()
    for k, v in enumerate(vals):
        h = max(0.012, height * v / top)
        g.add(Rectangle(width=step * 0.72, height=h, stroke_width=0, fill_color=DATA if k < half else KERN,
                        fill_opacity=0.9).move_to([x0 + (k + 0.5) * step, y0, 0], aligned_edge=DOWN))
    return g


class Multigrid(VoiceoverScene):
    def construct(self):
        self.card()
        self.smoothing()
        self.spectrum()
        self.coarse()
        self.vcycle()
        self.cost()

    def card(self):
        card = chapter_card(9, r"Multigrid", r"Can a solver cost no more than reading its input?",
                            lit=(1964, 1977), extra=((1964, r"Fedorenko: \ two grids"),
                                                     (1977, r"Brandt: \ multilevel solvers")), part=PART)
        with self.voiceover("Chapter nine. Multigrid."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def smoothing(self):
        s = load("spectrum")
        n, fac = s["n"], s["factor"]
        head = label(r"Relaxation smooths", font_size=36).to_edge(UP, buff=0.3)
        sn = r"\sin^2\!\tfrac{k\pi}{2(n+1)}"
        cols = {r"g_k": HEAD, r"e": NO}
        rows = VGroup(
            cmath(r"x", r"\leftarrow", r"x", r"+", r"\omega D^{-1}", r"(b - Ax)", font_size=32),
            cmath(r"e", r"\leftarrow", r"(I - \tfrac{\omega}{2} A)", r"e", colors=cols, font_size=32),
            cmath(r"A v_k", r"=", r"4" + sn, r"\, v_k", font_size=32),
            cmath(r"g_k", r"=", r"1 -", r"2\omega", sn, colors=cols, font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.62).move_to([-3.55, -0.05, 0])
        last = cmath(r"g_k", r"=", r"1 -", r"\tfrac{4}{3}", sn, colors=cols, font_size=32).move_to(
            rows[3], aligned_edge=LEFT)
        whys = VGroup(
            wrapped_label(r"weighted Jacobi on $A = \operatorname{tridiag}(-1, 2, -1)$, \ $n = %d$: \ $D = 2I$" % n,
                          5.6, font_size=18, color=GREY_B),
            label(r"the error $e = x - x_*$: \ $b$ cancels", font_size=18, color=GREY_B),
            label(r"the sine waves $v_k$ are $A$'s eigenvectors", font_size=18, color=GREY_B),
            label(r"so each sweep multiplies mode $k$ by $g_k$", font_size=18, color=GREY_B),
        )
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.1).align_to(r, LEFT)
        why_last = label(r"with $\omega = 2/3$", font_size=18, color=HEAD).move_to(whys[3], aligned_edge=LEFT)
        ax = CornerAxes(x_range=[0, 64, 16], y_range=[0, 1, 0.5], x_length=5.2, y_length=3.3, tips=False,
                        axis_config={"stroke_color": GREY_C})
        ax.move_to([3.55, 0.35, 0])
        xt = VGroup(*[label(f"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for v in (1, 16, 32, 48, 63)])
        yt = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for t, v in ((r"0", 0), (r"\tfrac13", 1 / 3), (r"1", 1))])
        xl = label(r"mode $k$: \ smooth $\to$ rough", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"$|g_k|$, \ the factor per sweep", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.15)
        yl.align_to(ax, LEFT)
        curve = VMobject(color=HEAD, stroke_width=3).set_points_smoothly(
            [ax.c2p(k + 1, v) for k, v in enumerate(fac)])
        third = DashedLine(ax.c2p(0, 1 / 3), ax.c2p(64, 1 / 3), color=GREY_B, stroke_width=1.5)
        band = Rectangle(width=ax.c2p(63, 0)[0] - ax.c2p(32, 0)[0], height=ax.c2p(0, 1 / 3)[1] - ax.c2p(0, 0)[1],
                         stroke_width=0, fill_color=YES, fill_opacity=0.18).move_to(ax.c2p(32, 0), aligned_edge=DL)
        l_lo = label(rf"mode 1: \ {fac[0]:.3f}, \ barely moves", font_size=17, color=NO).move_to(
            ax.c2p(3, 0.17), aligned_edge=LEFT)
        l_hi = label(r"upper half: \ at most $\tfrac13$", font_size=17, color=YES).next_to(band, UP, buff=0.12)
        with self.voiceover(
            "Go back to Poisson's equation, in one dimension to start: sixty-three unknowns, two on the diagonal "
            "and minus one beside it. <bookmark mark='a'/> The simplest iteration, weighted Jacobi, moves each "
            "unknown part of the way towards the value its own equation wants. <bookmark mark='b'/> Subtract the "
            "true solution and b cancels: the error is multiplied by the same matrix at every sweep. "
            "<bookmark mark='c'/> That matrix shares its eigenvectors with A, and they are sine waves: mode one "
            "is a single smooth hump, mode sixty-three a zigzag. <bookmark mark='d'/> So each sweep simply scales "
            "each mode, by a factor we can write down. <bookmark mark='e'/> Moving two thirds of the way, the "
            "rough upper half of the modes shrinks by at least a factor of three per sweep. The smoothest mode "
            "keeps nought point nine nine nine of itself."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(rows[3], last), ReplacementTransform(whys[3], why_last))
            self.play(Create(curve), run_time=2)
            self.play(FadeIn(band), Create(third), FadeIn(l_hi), FadeIn(l_lo))
        self.wait(0.4)
        self.clear_scene()

    def spectrum(self):
        s = load("spectrum")
        n, sp = s["n"], s["spectrum"]
        half = n // 2
        head = label(r"The error spectrum under relaxation", font_size=36).to_edge(UP, buff=0.3)
        top = max(sp["0"])
        bars = {k: spectrum_bars(sp[k], half, top=top) for k in ("0", "1", "3", "10")}
        base = Line([-5.7, -1.6, 0], [5.7, -1.6, 0], color=GREY_C, stroke_width=1.5)
        ic_lo = VGroup(mode_icon(1, 15, color=DATA), label(r"mode 1: \ smooth", font_size=17, color=DATA))
        ic_lo.arrange(DOWN, buff=0.12).next_to(base, DOWN, buff=0.25).align_to(base, LEFT).shift(RIGHT * 0.1)
        ic_hi = VGroup(mode_icon(15, 15, color=KERN), label(rf"up to mode {n}: \ zigzags", font_size=17,
                                                          color=KERN))
        ic_hi.arrange(DOWN, buff=0.12).next_to(base, DOWN, buff=0.25).align_to(base, RIGHT).shift(LEFT * 0.1)
        cap = note(rf"a random error on {n} points, \ its size along each sine mode, \ computed",
                   font_size=17).next_to(base, DOWN, buff=0.35)
        counts = {k: label(rf"after {k} sweep{'s' if k != '1' else ''}", font_size=26, color=HEAD)
                  for k in ("0", "1", "3", "10")}
        for c in counts.values():
            c.move_to([4.4, 2.35, 0])
        s0, s10 = sp["0"], sp["10"]
        res = VGroup(
            label(rf"mode 1: \ {s0[0]:.3f} $\to$ {s10[0]:.3f}", font_size=19, color=DATA),
            label(rf"upper half: \ largest {max(s0[half:]):.2f} $\to$ ${sci(max(s10[half:]))}$", font_size=19,
                  color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        res.next_to(cap, DOWN, buff=0.35)
        foot = label(r"relaxation alone is hopeless, \ but it \textbf{smooths}", font_size=21,
                     color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Watch it happen. <bookmark mark='a'/> These bars are a random error, measured along each of the "
            "sixty-three sine waves: smooth modes on the left, rough ones on the right. <bookmark mark='b'/> One "
            "sweep, and the right half drops. <bookmark mark='c'/> Three sweeps. <bookmark mark='d'/> After ten, "
            "the rough half has all but vanished, and the smoothest mode has lost less than one percent. "
            "<bookmark mark='e'/> So relaxation on its own is hopeless: the error that remains is smooth, and "
            "smooth error barely moves. But relaxation does one thing superbly. It smooths."
        ) as vo:
            self.play(FadeIn(head), Create(base), FadeIn(ic_lo), FadeIn(ic_hi))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars["0"]], lag_ratio=0.03),
                      FadeIn(counts["0"]), FadeIn(cap), run_time=2)
            cur, cl = bars["0"], counts["0"]
            for mk, k in (("b", "1"), ("c", "3"), ("d", "10")):
                vo.wait_until(mk)
                self.play(Transform(cur, bars[k]), ReplacementTransform(cl, counts[k]), run_time=1.5)
                cl = counts[k]
            self.play(FadeIn(res))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def coarse(self):
        head = label(r"Smooth on the fine grid, \ rough on the coarse", font_size=36).to_edge(UP, buff=0.3)
        k, nf = 6, 15
        ax = Axes(x_range=[0, 1, 0.25], y_range=[-1.2, 1.2, 1], x_length=5.6, y_length=2.2, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False})
        ax.move_to([-3.5, 1.15, 0])
        wave = ax.plot(lambda x: math.sin(k * math.pi * x), x_range=[0, 1, 0.005], color=GREY_C, stroke_width=2)
        fine = VGroup(*[Dot(ax.c2p(j / (nf + 1), math.sin(k * math.pi * j / (nf + 1))), radius=0.06, color=DATA)
                        for j in range(1, nf + 1)])
        odd = VGroup(*[fine[j - 1] for j in range(1, nf + 1, 2)])
        even = VGroup(*[fine[j - 1] for j in range(2, nf + 1, 2)])
        ill = note(r"illustrative", font_size=16).next_to(ax, UP, buff=0.05).align_to(ax, RIGHT)
        t_f = wrapped_label(rf"fine grid, \ {nf} points: \ mode {k} of {nf}, \ in the lower half: \ slow to relax",
                            5.6, font_size=19, color=DATA).next_to(ax, DOWN, buff=0.3)
        t_c = wrapped_label(rf"coarse grid, \ every other point: \ mode {k} of {(nf - 1) // 2}, \ in the upper "
                            rf"half: \ fast", 5.6, font_size=19, color=HEAD).next_to(t_f, DOWN, buff=0.25)
        t_f.align_to(ax, LEFT)
        t_c.align_to(ax, LEFT)
        hist = wrapped_label(r"two grids: \ Fedorenko \ (1964); \ made practical by Brandt in the 1970s", 5.6,
                             font_size=19, color=GREY_A).next_to(t_c, DOWN, buff=0.4).align_to(ax, LEFT)
        steps = VGroup(
            cmath(r"x", r"\leftarrow", r"S^{\nu}(x)", font_size=30),
            cmath(r"r", r"=", r"b - A_h x", font_size=30),
            cmath(r"A_{2h}\, e_{2h}", r"=", r"R\, r", font_size=30),
            cmath(r"x", r"\leftarrow", r"x + P\, e_{2h}", font_size=30),
            cmath(r"x", r"\leftarrow", r"S^{\nu}(x)", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.0, 0.0, 0])
        whys = VGroup(
            label(r"relax a few sweeps: \ the error is now smooth", font_size=18, color=GREY_B),
            label(r"the residual, \ $A_h e = r$", font_size=18, color=GREY_B),
            label(r"restrict $r$ to the coarse grid, \ solve there", font_size=18, color=HEAD),
            label(r"interpolate the correction back, \ add it", font_size=18, color=GREY_B),
            label(r"relax again", font_size=18, color=GREY_B),
        )
        for w, r in zip(whys, steps):
            w.next_to(r, DOWN, buff=0.08).align_to(r, LEFT)
        nums = VGroup(*[label(f"{i}", font_size=20, color=GREY_A).next_to(r, LEFT, buff=0.3)
                        for i, r in enumerate(steps, 1)])
        loop = SurroundingRectangle(steps[2], color=HEAD, buff=0.07, stroke_width=1.6)
        whys[2].next_to(loop, DOWN, buff=0.06).align_to(steps[2], LEFT)
        rec = label(r"the same kind of problem: \ recurse", font_size=18, color=HEAD).next_to(loop, RIGHT, buff=0.2)
        with self.voiceover(
            "Here is the trick. <bookmark mark='a'/> A smooth wave on a fine grid of fifteen points, mode six, sits "
            "in the lower half of the spectrum, where relaxation is slow. <bookmark mark='b'/> Keep every other "
            "point. On the coarse grid of seven, the same wave is mode six of seven: in the upper half, where "
            "relaxation is fast. <bookmark mark='c'/> So relax a few times, compute the residual, and carry it "
            "down to the coarse grid. Solve there for the correction, interpolate it back, add it, and relax "
            "again. Radii Fedorenko published this two-grid scheme in 1964, and Achi Brandt made it practical in "
            "the 1970s. <bookmark mark='d'/> The coarse problem is the same kind of problem, so treat it the "
            "same way."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(wave), FadeIn(ill))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in fine], lag_ratio=0.08), FadeIn(t_f))
            vo.wait_until("b")
            self.play(odd.animate.set_opacity(0.15), *[d.animate.set_color(HEAD).scale(1.4) for d in even], FadeIn(t_c))
            vo.wait_until("c")
            for i in range(5):
                self.play(FadeIn(nums[i]), FadeIn(steps[i]), FadeIn(whys[i]), run_time=0.7)
            self.play(FadeIn(hist))
            vo.wait_until("d")
            self.play(Create(loop), FadeIn(rec))
        self.wait(0.4)
        self.clear_scene()

    def vcycle(self):
        rows_ = load("multigrid")["rows"]
        head = label(r"The V-cycle", font_size=36).to_edge(UP, buff=0.3)
        ys = [1.9, 0.85, -0.2, -1.25]
        xl_, xm, xr = -6.0, -3.9, -1.8
        down = [np.array([xl_ + (xm - xl_) * i / 3, y, 0]) for i, y in enumerate(ys)]
        up = [np.array([xm + (xr - xm) * i / 3, y, 0]) for i, y in enumerate(ys[::-1])]
        nodes = VGroup(*[Circle(radius=0.14, color=DATA, fill_color=BG, fill_opacity=1).move_to(p)
                         for p in down[:-1]],
                       Square(side_length=0.3, color=YES, fill_color=YES, fill_opacity=0.4).move_to(down[-1]),
                       *[Circle(radius=0.14, color=KERN, fill_color=BG, fill_opacity=1).move_to(p) for p in up[1:]])
        pts = down + up[1:]
        edges = VGroup(*[Line(pts[i], pts[i + 1], color=GREY_B, stroke_width=2, buff=0.17) for i in range(6)])
        levels = VGroup(*[MathTex(t, font_size=24, color=GREY_A).move_to([-6.55, y, 0])
                          for t, y in zip((r"h", r"2h", r"4h", r"8h"), ys)])
        t_down = label(r"relax, \ restrict", font_size=17, color=DATA).next_to(edges[1], LEFT, buff=0.12)
        t_up = label(r"interpolate, \ relax", font_size=17, color=KERN).next_to(edges[4], RIGHT, buff=0.12)
        t_bot = label(r"solve exactly", font_size=17, color=YES).next_to(nodes[3], DOWN, buff=0.15)
        path = VMobject().set_points_as_corners(pts)
        runner = Dot(pts[0], radius=0.09, color=HEAD)
        vnote = wrapped_label(r"our instrument: \ two weighted-Jacobi sweeps before and after on each level, \ "
                              r"full-weighting restriction, \ bilinear interpolation", 5.2, font_size=17,
                              color=GREY_A).move_to([-3.95, -2.7, 0])
        ax = CornerAxes(x_range=[0, 10, 2], y_range=[-8, 0, 2], x_length=5.0, y_length=3.3, tips=False,
                        axis_config={"stroke_color": GREY_C})
        ax.move_to([3.6, 0.55, 0])
        yt = VGroup(*[MathTex(rf"10^{{{p}}}", font_size=20, color=GREY_B).next_to(ax.c2p(0, p), LEFT, buff=0.1)
                      for p in (-8, -6, -4, -2, 0)])
        xt = VGroup(*[label(f"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(v, -8), DOWN, buff=0.1)
                      for v in (0, 2, 4, 6, 8, 10)])
        xlab = label(r"V-cycles", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        ylab = label(r"relative residual, \ 2D Poisson, \ computed", font_size=17, color=GREY_A).next_to(
            ax, UP, buff=0.15).align_to(ax, LEFT)
        colors = (GREY_B, DATA, LAM, HEAD)
        curves = VGroup(*[VMobject(color=c, stroke_width=3).set_points_as_corners(
            [ax.c2p(i, math.log10(v)) for i, v in enumerate(r["residuals"])]) for r, c in zip(rows_, colors)])
        keys = VGroup(*[label(rf"{r['m']} $\times$ {r['m']}, \ {r['n']:,} unknowns: \ "
                              rf"{r['factor']:.2f} per cycle", font_size=18, color=c)
                        for r, c in zip(rows_, colors)]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        keys.next_to(xlab, DOWN, buff=0.3).align_to(ax, LEFT)
        with self.voiceover(
            "Recursing gives the V-cycle. <bookmark mark='a'/> Relax and restrict, down through coarser and "
            "coarser grids to one of a few points; solve that exactly; then interpolate and relax on the way back "
            "up. <bookmark mark='b'/> Our instrument runs it on the two-dimensional Poisson problem. On a grid of "
            "two hundred and twenty-five unknowns, each cycle cuts the residual by a factor of about five. "
            "<bookmark mark='c'/> On nine hundred and sixty-one unknowns, the same. On sixteen thousand, the same. "
            "The curves lie on top of one another, and ten cycles reach a few parts in a hundred million on every "
            "grid. The number of cycles does not grow with the problem."
        ) as vo:
            self.play(FadeIn(head), FadeIn(levels), Create(edges), FadeIn(nodes))
            vo.wait_until("a")
            self.play(FadeIn(t_down), FadeIn(runner))
            self.play(MoveAlongPath(runner, path), FadeIn(t_bot, run_time=1), FadeIn(t_up, run_time=2),
                      run_time=3, rate_func=linear)
            self.play(FadeIn(vnote))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(xlab), FadeIn(ylab))
            self.play(Create(curves[0]), FadeIn(keys[0]), run_time=1.5)
            vo.wait_until("c")
            for c, kk in zip(curves[1:], keys[1:]):
                self.play(Create(c), FadeIn(kk), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    def cost(self):
        head = label(r"Order $n$", font_size=36).to_edge(UP, buff=0.3)
        cols = {r"W(n)": HEAD}
        rows = VGroup(
            cmath(r"W(n)", r"=", r"c\,n", r"+", r"W(n/4)", colors=cols, font_size=34),
            cmath(r"W(n)", r"=", r"c\,n", r"\left(1 + \tfrac14 + \tfrac1{16} + \cdots\right)", colors=cols,
                  font_size=34),
            cmath(r"W(n)", r"=", r"\tfrac43", r"c\,n", colors=cols, font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.75).move_to([-4.1, 0.6, 0])
        whys = VGroup(
            wrapped_label(r"relax on the finest grid, \ then a cycle on a grid with a quarter of the points "
                          r"\ (2D)", 5.4, font_size=18, color=GREY_B),
            label(r"unroll the recursion", font_size=18, color=GREY_B),
            label(r"a geometric series: \ a constant times $n$", font_size=18, color=YES),
        )
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.12).align_to(r, LEFT)
        ax = CornerAxes(x_range=[2, 6, 1], y_range=[2, 18, 4], x_length=3.9, y_length=4.0, tips=False,
                        axis_config={"stroke_color": GREY_C})
        ax.move_to([1.5, 0.2, 0])
        xt = VGroup(*[MathTex(rf"10^{{{p}}}", font_size=20, color=GREY_B).next_to(ax.c2p(p, 2), DOWN, buff=0.1)
                      for p in (2, 4, 6)])
        yt = VGroup(*[MathTex(rf"10^{{{p}}}", font_size=20, color=GREY_B).next_to(ax.c2p(2, p), LEFT, buff=0.1)
                      for p in (2, 6, 10, 14, 18)])
        xlab = label(r"unknowns $n$", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        ylab = label(r"work, \ 2D Poisson \ (orders of growth; \ constants omitted)", font_size=17,
                     color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        specs = [(3.0, r"dense elimination, \ $n^3$", NO), (2.0, r"band, \ row by row: \ $n^2$", KERN),
                 (1.5, r"nested dissection; \ CG: \ $n^{3/2}$", LAM), (1.0, r"multigrid: \ $n$", YES)]
        lines, tags = VGroup(), VGroup()
        for p, t, c in specs:
            lines.add(Line(ax.c2p(2, 2 * p), ax.c2p(6, 6 * p), color=c, stroke_width=3))
            tags.add(label(t, font_size=17, color=c).next_to(ax.c2p(6, 6 * p), RIGHT, buff=0.12))
        foot = wrapped_label(r"order $n$ is the cost of reading the right-hand side: \ no method can do better. \ "
                             r"\textbf{Algebraic multigrid} builds the coarse levels from the matrix alone, \ and "
                             r"often serves as CG's preconditioner", 12.4, font_size=20, color=WHITE).to_edge(
            DOWN, buff=0.3)
        with self.voiceover(
            "And each cycle is cheap. <bookmark mark='a'/> It relaxes on the finest grid, work proportional to n, "
            "and then does the same on a grid with a quarter of the points. <bookmark mark='b'/> Unroll that: n, "
            "times one plus a quarter plus a sixteenth and so on, <bookmark mark='c'/> which is four thirds of the "
            "work on the finest grid alone. <bookmark mark='d'/> Now compare the ways of solving the same "
            "Poisson problem. Dense elimination grows like n cubed; the band, row by row, like n squared; nested "
            "dissection, and conjugate gradients, like n to the three halves. Multigrid grows like n. "
            "<bookmark mark='e'/> That is the cost of reading the right-hand side, so no method can do better. For "
            "unstructured problems, algebraic multigrid builds its coarse levels from the matrix itself, and is "
            "often the preconditioner inside conjugate gradients."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xlab), FadeIn(ylab))
            for ln, tg in zip(lines, tags):
                self.play(Create(ln), FadeIn(tg), run_time=0.8)
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
