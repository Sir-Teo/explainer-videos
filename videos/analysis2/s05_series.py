from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis2.common import load, magnifier_above, plain_axes, polyline, runs_in_range


def bars(a, x0=-5.9, base=-2.7, w=0.34, H=3.2, color=C.SEQ, opacity=0.75) -> VGroup:
    """Terms a_1, a_2, ... as bars of width ``w`` standing on y = base (height H * a_n)."""
    g = VGroup()
    for i, v in enumerate(a):
        g.add(Rectangle(width=w * 0.86, height=max(0.004, H * v), stroke_width=0, fill_color=color,
                        fill_opacity=opacity).move_to([x0 + w * (i + 0.5), base + H * v / 2, 0]))
    return g


def box_on(ax, x0, x1, y0, y1, color, stroke_width=2.5, fill_opacity=0.15) -> Polygon:
    """The rectangle [x0, x1] x [y0, y1] in the coordinates of ``ax``."""
    return Polygon(ax.c2p(x0, y0), ax.c2p(x1, y0), ax.c2p(x1, y1), ax.c2p(x0, y1), color=color,
                   stroke_width=stroke_width, fill_color=color, fill_opacity=fill_opacity)


class Series(VoiceoverScene):
    X0, BASE, W, H = -5.9, -2.7, 0.34, 3.2

    def construct(self):
        self.card()
        self.criterion()
        self.harmonic()
        self.geometric()
        self.condensation()
        self.p_series()
        self.no_boundary()

    def bx(self, n):
        """The screen x of the left edge of bar n (n = 1, 2, ...)."""
        return self.X0 + self.W * (n - 1)

    def by(self, v):
        return self.BASE + self.H * v

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(4, r"Series, and the comparison tests", r"When does adding forever give a number?",
                            lit=(), part=2)
        with self.voiceover(
            "Chapter four. A series is a sequence in disguise: the sequence of its partial sums. Everything from the "
            "last two chapters applies, and a few new tools appear."
        ):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def criterion(self):
        dfn = MathTex(r"\sum_{n=1}^{\infty} a_n = s", r"\quad\text{means}\quad", r"s_n = a_1 + \cdots + a_n \to s",
                      font_size=38).to_edge(UP, buff=0.35)
        crit = VGroup(label(r"\textbf{Cauchy criterion} (Rudin 3.22): \ $\sum a_n$ converges $\iff$", font_size=28),
                      MathTex(r"\forall \varepsilon > 0 \;\exists N:\; m \ge n \ge N \Rightarrow "
                              r"\Big| a_n + a_{n+1} + \cdots + a_m \Big| \le \varepsilon", font_size=34)
                      ).arrange(DOWN, buff=0.15).next_to(dfn, DOWN, buff=0.3)
        crit[1][0][0:4].set_color(C.EPS)
        nec = VGroup(label(r"take $m = n$: \ $|a_n| \le \varepsilon$, \ so $a_n \to 0$ \ (Rudin 3.23);", font_size=28),
                     label(r"necessary, \ but not sufficient", font_size=28, color=C.PATHOLOGY)).arrange(RIGHT, buff=0.25)
        nec.to_edge(DOWN, buff=0.25)
        # a block of terms, stacked into one tower: far enough out, every tower stays under epsilon
        n_max, eps, H, W, X0, B = 30, 0.3, 3.0, 0.28, -6.35, -2.65
        a = 1 / np.arange(1, n_max + 1) ** 2
        bs = bars(a, X0, B, W, H, color=C.SEQ, opacity=0.8)
        base = Line([X0 - 0.1, B, 0], [X0 + W * n_max + 0.1, B, 0], color=GREY_C, stroke_width=2)
        alab = MathTex(r"a_n = \tfrac{1}{n^2}", font_size=32, color=C.SEQ).move_to([-3.2, -0.3, 0])
        tx = 4.2
        tbase = Line([tx - 0.7, B, 0], [tx + 0.7, B, 0], color=GREY_C, stroke_width=2)
        eline = DashedLine([tx - 0.8, B + H * eps, 0], [tx + 0.8, B + H * eps, 0], color=C.EPS, stroke_width=2.5)
        elab = MathTex(r"\varepsilon", font_size=30, color=C.EPS).next_to(eline, RIGHT, buff=0.12)
        tlab = MathTex(r"|a_n + \cdots + a_m|", font_size=28).move_to([tx, -0.3, 0])
        tail = [float(np.sum(1 / np.arange(k, 200001, dtype=float) ** 2)) for k in (3, 4)]
        N = 4  # the tail from 4 on is below 0.3 (so is every block in it); from 3 on it is not
        assert tail[0] > eps > tail[1]
        Nline = DashedLine([X0 + W * (N - 1), B - 0.1, 0], [X0 + W * (N - 1), B + 1.5, 0], color=C.DELTA,
                           stroke_width=2.5)
        Nlab = MathTex(r"N", font_size=30, color=C.DELTA).next_to(Nline, UP, buff=0.08)

        def block(n, m):
            """The highlight over bars n..m and the tower they stack into (green under epsilon, red above)."""
            tot = float(a[n - 1:m].sum())
            col = C.CONNECTED_SET if tot <= eps else C.PATHOLOGY
            hl = Rectangle(width=W * (m - n + 1) + 0.04, height=0.18, stroke_width=0, fill_color=col,
                           fill_opacity=0.9).move_to([X0 + W * (n - 1 + (m - n + 1) / 2), B - 0.16, 0])
            stack, y = VGroup(), B
            for k in range(n, m + 1):
                h = max(0.004, H * a[k - 1])
                stack.add(Rectangle(width=0.9, height=h, stroke_width=0.6, stroke_color=BACKGROUND, fill_color=col,
                                    fill_opacity=0.85).move_to([tx, y + h / 2, 0]))
                y += h
            lab = MathTex(rf"n = {n},\ m = {m}" if m > n else rf"n = m = {n}", font_size=24, color=col)
            lab.next_to(stack, UP, buff=0.12).set_y(max(B + H * eps + 0.3, stack.get_top()[1] + 0.25))
            return VGroup(hl, stack, lab), tot

        def show(prev, n, m, rt=1.2):
            (hl, stack, lab), tot = block(n, m)
            src = VGroup(*[bs[k - 1] for k in range(n, m + 1)])
            anims = [FadeOut(prev)] if prev is not None else []
            self.play(*anims, FadeIn(hl), run_time=0.4)
            self.play(TransformFromCopy(src, stack), FadeIn(lab), run_time=rt)
            return VGroup(hl, stack, lab), tot

        with self.voiceover(
            "A series converges to s when its partial sums do. <bookmark mark='c'/> So the Cauchy criterion carries "
            "over: the series converges exactly when every long enough block of consecutive terms, far enough out, adds "
            "up to something small. <bookmark mark='n'/> A block can be a single term, so the terms must go to zero. "
            "<bookmark mark='p'/> That's necessary, but it's not enough, and the classic example is seven centuries old."
        ) as vo:
            self.play(FadeIn(dfn))
            self.play(Create(base), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bs], lag_ratio=0.04), FadeIn(alab),
                      run_time=1.4)
            vo.wait_until("c")
            self.play(FadeIn(crit), Create(tbase), Create(eline), FadeIn(elab), FadeIn(tlab))
            cur, t0 = show(None, 2, 3)
            self.play(Create(Nline), FadeIn(Nlab), run_time=0.6)
            cur, t1 = show(cur, 4, 9)
            cur, t2 = show(cur, 5, 30)
            vo.wait_until("n")
            cur, t3 = show(cur, 6, 6, rt=0.8)
            self.play(FadeIn(nec[0]))
            vo.wait_until("p")
            self.play(FadeIn(nec[1]))
        assert t0 > eps and max(t1, t2, t3) < eps
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def harmonic(self):
        n_max = 32
        a = 1 / np.arange(1, n_max + 1)
        bs = bars(a, self.X0, self.BASE, self.W, self.H)
        base = Line([self.X0 - 0.1, self.BASE, 0], [self.bx(n_max + 1) + 0.1, self.BASE, 0], color=GREY_C,
                    stroke_width=2)
        head = MathTex(r"1 + \tfrac12 + \tfrac13 + \tfrac14 + \cdots", font_size=42, color=C.SEQ).to_edge(UP, buff=0.45)
        sub = label(r"the harmonic series: \ terms $\to 0$", font_size=28, color=GREY_A).next_to(head, DOWN, buff=0.12)
        cols = [C.SEQ, C.FREQ]
        blocks = VGroup()
        floors = VGroup()
        tags = VGroup()
        d = load("pseries")
        for k in range(0, 5):
            lo, hi = 2**k + 1, 2 ** (k + 1)
            blocks.add(VGroup(*[bs[j - 1] for j in range(lo, hi + 1)]))
            h = 1 / hi
            fl = Rectangle(width=self.W * (hi - lo + 1), height=self.H * h, stroke_color=C.EPS, stroke_width=2.5,
                           fill_color=C.EPS, fill_opacity=0.25)
            fl.move_to([(self.bx(lo) + self.bx(hi + 1)) / 2, self.BASE + self.H * h / 2, 0])
            floors.add(fl)
            top = self.BASE + self.H / lo  # the block's first, tallest bar
            br = Brace(Line([self.bx(lo) + 0.02, top, 0], [self.bx(hi + 1) - 0.02, top, 0]), direction=UP, buff=0.06,
                       color=C.EPS)
            t = MathTex(r"\ge \tfrac12", font_size=28, color=C.EPS).next_to(br, UP, buff=0.06)
            if k == 0:
                t.shift(RIGHT * 0.2)  # clear of the first bar, a_1
            tags.add(VGroup(br, t))
        oresme = label(r"Oresme, about 1350: \ block $k$ is at least $2^k \cdot \tfrac{1}{2^{k+1}} = \tfrac12$", font_size=30).move_to([2.5, 1.2, 0])
        res = MathTex(r"s_{2^k} \ge 1 + \tfrac{k}{2} \to \infty", font_size=38, color=C.PATHOLOGY).next_to(oresme, DOWN,
                                                                                                         buff=0.3)
        with self.voiceover(
            "The harmonic series: one, plus a half, plus a third, and so on. <bookmark mark='a'/> The terms shrink to "
            "zero. <bookmark mark='b'/> But group them in blocks that double in length: a half; a third and a quarter; "
            "the next four; the next eight. <bookmark mark='c'/> In each block every term is at least the last one, "
            "so the block is at least its length times its last term, which is exactly one half. "
            "<bookmark mark='d'/> Infinitely many halves: the sum grows without bound. This argument is from Nicole "
            "Oresme, around 1350."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), Create(base))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bs], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("b")
            self.play(*[blocks[k].animate.set_color(cols[k % 2]) for k in range(5)])
            vo.wait_until("c")
            for k in range(5):
                self.play(FadeIn(floors[k]), FadeIn(tags[k]), run_time=0.5)
            vo.wait_until("d")
            self.play(FadeIn(oresme), FadeIn(res))
        assert d["blocks"].min() >= 0.5
        self.wait(0.3)
        self.clear_scene()

        lx = plain_axes([0, 6.2, 1], [0, 15, 5], 10.6, 4.4, numbers=False).move_to([0.2, -0.6, 0])
        ticks = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=22, color=GREY_B).next_to(lx.c2p(k, 0), DOWN, buff=0.12)
                         for k in range(0, 7)])
        ylab = VGroup(*[MathTex(f"{v}", font_size=22, color=GREY_B).next_to(lx.c2p(0, v), LEFT, buff=0.1)
                        for v in (5, 10, 15)])
        lg = np.log10(d["n"])
        curve = polyline(lx, lg, d["p1"], color=C.SEQ, stroke_width=4)
        # ln n + gamma, dashed over the partial sums so both stay visible where they coincide
        approx = DashedVMobject(polyline(lx, lg, np.log(d["n"]) + float(d["gamma"]), color=WHITE, stroke_width=2),
                                num_dashes=90).set_z_index(1)
        assert np.max(np.abs(d["p1"] - np.log(d["n"]) - float(d["gamma"]))[d["n"] >= 10]) < 0.05
        c_l = MathTex(r"s_n = 1 + \tfrac12 + \cdots + \tfrac1n", font_size=30, color=C.SEQ).move_to(lx.c2p(1.6, 11))
        a_l = MathTex(r"\ln n + 0.5772\ldots", font_size=30).move_to(lx.c2p(4.6, 7.8))
        end = MathTex(rf"s_{{10^6}} = {float(d['p1'][-1]):.2f}", font_size=30).next_to(lx.c2p(6, d["p1"][-1]), UP,
                                                                                    buff=0.15).shift(LEFT * 0.6)
        head = label(r"It diverges, \ but slowly", font_size=34).to_edge(UP, buff=0.4)
        with self.voiceover(
            "<bookmark mark='a'/> It diverges, but slowly: on a logarithmic scale the partial sums are a straight line, "
            "hugging the natural log of n plus Euler's constant. <bookmark mark='b'/> A million terms add up to only "
            "about fourteen point four."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(lx), FadeIn(ticks), FadeIn(ylab))
            self.play(Create(curve), FadeIn(c_l), run_time=1.6)
            self.play(Create(approx), FadeIn(a_l))
            vo.wait_until("b")
            self.play(FadeIn(end))
        assert abs(d["p1"][-1] - 14.39) < 0.01
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def geometric(self):
        comp = VGroup(label(r"\textbf{Comparison} (Rudin 3.25)", font_size=32),
                      label(r"$|a_n| \le c_n$ and $\sum c_n$ converges $\Rightarrow$ $\sum a_n$ converges", font_size=28),
                      label(r"$a_n \ge d_n \ge 0$ and $\sum d_n$ diverges $\Rightarrow$ $\sum a_n$ diverges", font_size=28)
                      ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.45)
        why1 = label(r"(blocks of $\sum a_n$ are no bigger than blocks of $\sum c_n$: \ the Cauchy criterion)",
                     font_size=24, color=GREY_B).next_to(comp, DOWN, buff=0.15)
        geo = MathTex(r"\sum_{n=0}^{\infty} x^n = \frac{1}{1 - x} \quad (0 \le x < 1)", font_size=38).move_to([0, 0.3, 0])
        geo_r = note(r"Rudin 3.26; \ the standard thing to compare with").next_to(geo, DOWN, buff=0.12)
        # the comparison test, pictured: a_n (filled) inside the bars of a convergent c_n (outlined)
        nb, Hc, wb, xb0, yb = 10, 6.0, 0.62, -6.2, -2.75
        nn = np.arange(1, nb + 1)
        cv = 0.5**nn
        av = cv * (0.4 + 0.5 * np.abs(np.sin(nn)))
        assert np.all((0 < av) & (av < cv))
        outl = VGroup(*[Rectangle(width=wb * 0.86, height=Hc * c_, stroke_color=C.UPPER_SUM, stroke_width=2.5)
                        .move_to([xb0 + wb * (i + 0.5), yb + Hc * c_ / 2, 0]) for i, c_ in enumerate(cv)])
        fills = bars(av, xb0, yb, wb, Hc, color=C.SEQ, opacity=0.8)
        cbase = Line([xb0 - 0.1, yb, 0], [3.0, yb, 0], color=GREY_C, stroke_width=2)
        c_lab = MathTex(r"c_n = 2^{-n}", font_size=30, color=C.UPPER_SUM).next_to(outl[0], RIGHT, buff=0.3).align_to(
            outl[0], UP)
        a_lab = MathTex(r"|a_n| \le c_n", font_size=30, color=C.SEQ).next_to(c_lab, DOWN, buff=0.15).align_to(c_lab, LEFT)
        # one block, n = 3..6: its terms stacked into towers, a's inside c's
        b0, b1, tx = 3, 6, 1.6
        blk = BraceBetweenPoints([xb0 + wb * (b0 - 1), yb - 0.08, 0], [xb0 + wb * b1, yb - 0.08, 0], direction=DOWN,
                                 color=WHITE)
        ct, at_, y_c, y_a = VGroup(), VGroup(), yb, yb
        for j in range(b0, b1 + 1):
            hc, ha = Hc * cv[j - 1], Hc * av[j - 1]
            ct.add(Rectangle(width=0.9, height=hc, stroke_color=C.UPPER_SUM, stroke_width=2.5).move_to([tx, y_c + hc / 2, 0]))
            at_.add(Rectangle(width=0.6, height=ha, stroke_width=0.8, stroke_color=BACKGROUND, fill_color=C.SEQ,
                              fill_opacity=0.85).move_to([tx, y_a + ha / 2, 0]))
            y_c += hc
            y_a += ha
        assert av[b0 - 1:b1].sum() < cv[b0 - 1:b1].sum()
        t_lab = MathTex(r"a_3 + \cdots + a_6", r"\le", r"c_3 + \cdots + c_6", font_size=30).next_to(ct, RIGHT, buff=0.35)
        t_lab[0].set_color(C.SEQ)
        t_lab[2].set_color(C.UPPER_SUM)
        cmp_pic = VGroup(outl, fills, cbase, c_lab, a_lab, blk, ct, at_, t_lab)
        nl_y = -2.0
        X = lambda v: -5.5 + v * 5.5  # noqa: E731
        line = Line([X(0) - 0.2, nl_y, 0], [X(2) + 0.3, nl_y, 0], color=GREY_C, stroke_width=2)
        lab = VGroup(*[MathTex(str(v), font_size=26, color=GREY_B).next_to([X(v), nl_y, 0], DOWN, buff=0.2)
                       for v in (0, 1, 2)])
        segs = VGroup()
        s = 0.0
        for k in range(10):
            t = 0.5**k
            col = C.SEQ if k % 2 == 0 else C.FREQ
            segs.add(Line([X(s), nl_y + 0.12, 0], [X(s + t), nl_y + 0.12, 0], color=col, stroke_width=10))
            s += t
        gap = label(r"each term covers half of the remaining gap to $2$", font_size=26, color=GREY_A).next_to(
            line, UP, buff=0.5)
        with self.voiceover(
            "The basic tool is comparison. <bookmark mark='a'/> If each term is at most the corresponding term of a "
            "convergent series of positive terms, the series converges, because its blocks are smaller. If each term is "
            "at least a divergent series's terms, it diverges. <bookmark mark='g'/> The standard series to compare "
            "with is the geometric series: <bookmark mark='h'/> one plus a half plus a quarter, and so on, each term "
            "covering half the remaining distance to two."
        ) as vo:
            self.play(FadeIn(comp[0]))
            vo.wait_until("a")
            self.play(FadeIn(comp[1:]), FadeIn(why1), Create(cbase), Create(outl), FadeIn(c_lab), run_time=1.2)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in fills], lag_ratio=0.1), FadeIn(a_lab), run_time=1.2)
            self.play(GrowFromCenter(blk), run_time=0.5)
            self.play(TransformFromCopy(VGroup(*outl[b0 - 1:b1]), ct), TransformFromCopy(VGroup(*fills[b0 - 1:b1]), at_),
                      run_time=1.4)
            self.play(FadeIn(t_lab))
            vo.wait_until("g")
            self.play(FadeOut(cmp_pic), FadeIn(geo), FadeIn(geo_r))
            vo.wait_until("h")
            self.play(Create(line), FadeIn(lab), FadeIn(gap))
            self.play(LaggedStart(*[Create(x) for x in segs], lag_ratio=0.5), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def condensation(self):
        n_max = 32
        p = 1.5
        a = np.arange(1, n_max + 1, dtype=float) ** -p
        bs = bars(a, self.X0, self.BASE, self.W, self.H, color=C.SEQ, opacity=0.7)
        base = Line([self.X0 - 0.1, self.BASE, 0], [self.bx(n_max + 1) + 0.1, self.BASE, 0], color=GREY_C,
                    stroke_width=2)
        thm = VGroup(label(r"\textbf{Condensation} (Rudin 3.27) \ If $a_1 \ge a_2 \ge \cdots \ge 0$:", font_size=30),
                     MathTex(r"\sum_{n=1}^\infty a_n \text{ converges} \iff \sum_{k=0}^\infty 2^k a_{2^k}"
                             r"\text{ converges}", font_size=36)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.4)
        ex = MathTex(r"a_n = n^{-3/2}", font_size=32, color=C.SEQ).move_to([3.6, 1.2, 0])
        ups, los = VGroup(), VGroup()
        for k in range(0, 5):
            lo, hi = 2**k, 2 ** (k + 1) - 1
            h = a[lo - 1]
            u = Rectangle(width=self.W * (hi - lo + 1), height=self.H * h, stroke_color=C.UPPER_SUM, stroke_width=3,
                          fill_color=C.UPPER_SUM, fill_opacity=0.12)
            u.move_to([(self.bx(lo) + self.bx(hi + 1)) / 2, self.BASE + self.H * h / 2, 0])
            ups.add(u)
            lo2, hi2 = 2**k + 1, 2 ** (k + 1)
            h2 = a[hi2 - 1] if hi2 <= n_max else 2.0 ** (-(k + 1) * p)
            lw = Rectangle(width=self.W * (hi2 - lo2 + 1), height=self.H * h2, stroke_color=C.LOWER_SUM,
                           stroke_width=3, fill_color=C.LOWER_SUM, fill_opacity=0.25)
            lw.move_to([(self.bx(lo2) + self.bx(hi2 + 1)) / 2, self.BASE + self.H * h2 / 2, 0])
            los.add(lw)
        up_t = VGroup(label(r"over each block $[2^k, 2^{k+1})$,", font_size=26, color=C.UPPER_SUM),
                      label(r"a box of height $a_{2^k}$:", font_size=26, color=C.UPPER_SUM),
                      MathTex(r"s_n \le \sum_k 2^k a_{2^k}", font_size=34, color=C.UPPER_SUM)
                      ).arrange(DOWN, buff=0.12).move_to([-1.3, 0.8, 0])
        lo_t = VGroup(label(r"under each block $(2^k, 2^{k+1}]$,", font_size=26, color=C.LOWER_SUM),
                      label(r"a box of height $a_{2^{k+1}}$:", font_size=26, color=C.LOWER_SUM),
                      MathTex(r"s_{2^{k}} \ge \tfrac12 \sum_{j \le k} 2^j a_{2^j}", font_size=34, color=C.LOWER_SUM)
                      ).arrange(DOWN, buff=0.12).move_to([3.6, 0.8, 0])
        # the bars as a plot (bar n over [n - 1, n]), and a vertical magnifier on n = 8 .. 32, where the boxes are thin
        src = Axes(x_range=[0, n_max, 1], y_range=[0, 1, 1], x_length=n_max * self.W, y_length=self.H, tips=False,
                   axis_config={"stroke_opacity": 0, "include_ticks": False})
        src.shift(np.array([self.X0, self.BASE, 0]) - src.c2p(0, 0))
        mx, my = (7, n_max), (0.0, 0.05)
        ins, deco = magnifier_above(src, mx, my, height=1.75, gap=0.3)
        assert a[7] < my[1]  # the tallest bar in the window, a_8, fits
        ibars = VGroup(*[box_on(ins, j - 1 + 0.07, j - 0.07, 0, a[j - 1], C.SEQ, stroke_width=0, fill_opacity=0.7)
                         for j in range(8, n_max + 1)])

        def clip_box(x0, x1, h, color, fill):
            x0, x1 = max(x0, mx[0]), min(x1, mx[1])
            return box_on(ins, x0, x1, 0, h, color, stroke_width=3, fill_opacity=fill)

        iups = VGroup(*[clip_box(2**k - 1, 2 ** (k + 1) - 1, a[2**k - 1], C.UPPER_SUM, 0.12) for k in (3, 4)])
        ilos = VGroup(*[clip_box(2**k, 2 ** (k + 1), a[2 ** (k + 1) - 1], C.LOWER_SUM, 0.25) for k in (2, 3, 4)])
        with self.voiceover(
            "Cauchy's condensation test turns a slowly decreasing series into a fast one. <bookmark mark='t'/> If the "
            "terms decrease to zero, the series converges exactly when the condensed series, two to the k times the "
            "term at two to the k, converges. <bookmark mark='a'/> Here's why, with n to the minus three halves. "
            "<bookmark mark='u'/> Over each block from two to the k up to the next power of two, the terms are at most "
            "the first one, so a box of height a at two to the k covers the block: the partial sums are bounded by the "
            "condensed series. <bookmark mark='l'/> And under each block fits a box of the block's last height, which "
            "gives the reverse bound, up to a factor of two. The two series converge or diverge together."
        ) as vo:
            self.play(Create(base), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bs], lag_ratio=0.04), run_time=1.6)
            vo.wait_until("t")
            self.play(FadeIn(thm))
            vo.wait_until("a")
            self.play(FadeIn(ex))
            vo.wait_until("u")
            self.play(FadeIn(deco), FadeIn(ibars), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(u) for u in ups], lag_ratio=0.25), FadeIn(iups), FadeIn(up_t), run_time=2.0)
            vo.wait_until("l")
            self.play(LaggedStart(*[FadeIn(x) for x in los], lag_ratio=0.25), FadeIn(ilos), FadeIn(lo_t), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def p_series(self):
        d = load("pseries")
        rows = [MathTex(r"\sum_k 2^k \big(2^k\big)^{-p}", r"=", r"\sum_k \big(2^{1-p}\big)^k", font_size=40)]
        whys = [why(r"geometric, with ratio $2^{1-p}$: \ converges exactly when $p > 1$")]
        thm = label(r"\textbf{Rudin 3.28} \ $\displaystyle\sum \frac{1}{n^p}$ converges if $p > 1$ and diverges if "
                    r"$p \le 1$", font_size=32).to_edge(UP, buff=0.4)
        step = ladder(self, rows, whys, keep=1, top=2.0, buff=0.4, x=-0.6)
        lx = plain_axes([0, 6.2, 1], [0, 3.2, 1], 10.4, 3.3, numbers=False).move_to([0.0, -1.8, 0])
        ticks = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=22, color=GREY_B).next_to(lx.c2p(k, 0), DOWN, buff=0.12)
                         for k in range(0, 7)])
        ylab = VGroup(*[MathTex(f"{v}", font_size=22, color=GREY_B).next_to(lx.c2p(0, v), LEFT, buff=0.1)
                        for v in (1, 2, 3)])
        lg = np.log10(d["n"])
        keep = d["p1"] <= 3.2
        c1 = polyline(lx, lg[keep], d["p1"][keep], color=C.SEQ, stroke_width=3)
        c15 = polyline(lx, lg, d["p15"], color=C.FREQ, stroke_width=3)
        c2 = polyline(lx, lg, d["p2"], color=C.EPS, stroke_width=3)
        z15 = DashedLine(lx.c2p(0, float(d["zeta15"])), lx.c2p(6.2, float(d["zeta15"])), color=C.FREQ, stroke_width=1.5)
        z2 = DashedLine(lx.c2p(0, math.pi**2 / 6), lx.c2p(6.2, math.pi**2 / 6), color=C.EPS, stroke_width=1.5)
        l1 = MathTex(r"p = 1", font_size=26, color=C.SEQ).next_to(lx.c2p(lg[keep][-1], 3.2), RIGHT, buff=0.15)
        l15 = MathTex(r"p = \tfrac32 \to 2.612\ldots", font_size=26, color=C.FREQ).next_to(lx.c2p(6.2, 2.62), RIGHT,
                                                                                         buff=0.1).shift(LEFT * 2.2 + UP * 0.25)
        l2 = MathTex(r"p = 2 \to \tfrac{\pi^2}{6}", font_size=26, color=C.EPS).next_to(lx.c2p(6.2, 1.645), RIGHT,
                                                                                    buff=0.1).shift(LEFT * 2.0 + UP * 0.3)
        with self.voiceover(
            "<bookmark mark='t'/> Applied to one over n to the p, <bookmark mark='a'/> the condensed series is "
            "geometric, with ratio two to the one minus p. It converges exactly when p is bigger than one. "
            "<bookmark mark='g'/> The partial sums: for p equal to one they climb forever; for three halves they level "
            "off near 2.612; and for p equal to two at pi squared over six, a value Euler found in 1734. Notice how "
            "slowly the three-halves series settles: after a million terms it's still two thousandths short."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(thm))
            vo.wait_until("a")
            step(0)
            vo.wait_until("g")
            self.play(Create(lx), FadeIn(ticks), FadeIn(ylab))
            self.play(Create(c1), FadeIn(l1), run_time=1.2)
            self.play(Create(c15), Create(z15), FadeIn(l15), run_time=1.4)
            self.play(Create(c2), Create(z2), FadeIn(l2), run_time=1.4)
        gap15 = float(d["zeta15"]) - float(d["p15"][-1])
        assert 0.0015 < gap15 < 0.0025, gap15
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def no_boundary(self):
        d = load("pseries")
        rows = VGroup(
            MathTex(r"\sum \frac{1}{n}", r"\quad\text{diverges}", font_size=36),
            MathTex(r"\sum \frac{1}{n \log n}", r"\quad\text{diverges (like } \log\log n\text{)}", font_size=36),
            MathTex(r"\sum \frac{1}{n (\log n)^{1.01}}", r"\quad\text{converges}", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.6, 0])
        rows[0][1].set_color(C.PATHOLOGY)
        rows[1][1].set_color(C.PATHOLOGY)
        rows[2][1].set_color(C.CONNECTED_SET)
        ref = note(r"Rudin 3.29, by condensation").next_to(rows, UP, buff=0.3)
        val = label(rf"$\sum_{{n=2}}^{{10^6}} \frac{{1}}{{n \log n}} \approx {float(d['nlog_end']):.2f}$", font_size=28,
                    color=GREY_A).next_to(rows, DOWN, buff=0.4)
        foot = label(r"There is no slowest divergent series and no slowest convergent one (Rudin, Exercises 3.11--3.12).",
                     font_size=26, color=C.EPS).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Condensation keeps going. <bookmark mark='a'/> One over n log n still diverges, but only like log log n: a "
            "million terms add up to about three point four. <bookmark mark='b'/> Raise the log to the power 1.01 and "
            "it converges. <bookmark mark='c'/> And there's no last word: Rudin's exercises show that for any divergent "
            "series there's one diverging more slowly, and for any convergent series one converging more slowly. There "
            "is no sharp line between convergence and divergence."
        ) as vo:
            self.play(FadeIn(ref), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(val))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        assert 3.3 < float(d["nlog_end"]) < 3.5
        self.wait(0.5)
        self.clear_scene()
