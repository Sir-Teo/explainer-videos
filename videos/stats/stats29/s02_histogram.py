from __future__ import annotations

import numpy as np

from videos.stats.stats29.common import *  # noqa: F403


class Histogram(VoiceoverScene):
    def construct(self):
        self.card()
        self.upgrade()
        self.target()
        self.bias_var()
        self.optimum()
        self.curves()
        self.rate()

    def card(self):
        card = chapter_card(1, r"Histograms as estimators", r"Bias, \ variance, \ and the cube-root bin", lit=(1926,), part=PART)
        with self.voiceover("Chapter one. The histogram, as an estimator."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def upgrade(self):
        card = upgrade_card(1, r"bin width trades variance against bias; \ Scott's rule is $3.49\, s\, n^{-1/3}$",
                            r"the rule was quoted, \ not derived, \ and `error' was never defined",
                            r"define the error as MISE, \ derive it, \ and find the optimal bin and its rate")
        with self.voiceover(
            "<bookmark mark='a'/> Part 1 said that the histogram's bin width trades variance against bias, and quoted David "
            "Scott's rule, three point four nine s times n to the minus a third. <bookmark mark='b'/> It never said what "
            "error was being traded, or where the cube root came from. <bookmark mark='c'/> Now we define the error, derive "
            "it, and find the best bin width and how fast the error falls."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card[0]), FadeIn(card[1][0]), FadeIn(card[1][1][0]))
            vo.wait_until("b")
            self.play(FadeIn(card[1][1][1]))
            vo.wait_until("c")
            self.play(FadeIn(card[1][1][2]))
        self.clear_scene()

    def target(self):
        rows = [
            cmath(r"\hat f(x)", r"=", r"\dfrac{N_j}{n h}, \ \ x \in B_j", font_size=32),
            cmath(r"\text{ISE}", r"=", r"\textstyle\int (\hat f - f)^2", font_size=32),
            cmath(r"\text{MISE}", r"=", r"E\,\text{ISE} = \textstyle\int \mathrm{Var}\,\hat f + \int \text{bias}^2", font_size=30),
            cmath(r"\text{exact}", r":", r"\tfrac{1}{nh} - \tfrac{n+1}{nh} \textstyle\sum_j p_j^2 + \int f^2", font_size=30),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"the count in bin $j$, \ scaled to a density"), why(r"one data set's whole-curve error"),
                why(r"averaged over data sets"), why(r"$p_j$: \ the bin's probability, \ equal bins")]
        with self.voiceover(
            "<bookmark mark='a'/> The histogram's height in bin j is the count there, divided by n times the bin width h, so "
            "that the area is one. <bookmark mark='b'/> Its error, for one data set, is the integrated squared difference "
            "from the true density. <bookmark mark='c'/> Averaged over data sets, the mean integrated squared error splits "
            "into integrated variance plus integrated squared bias. <bookmark mark='d'/> For a histogram it can even be "
            "computed exactly, from the bins' probabilities: each count is binomial."
        ) as vo:
            intro=label('Integrated squared error separates variance and squared bias',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bias_var(self):
        rows = [
            cmath(r"\mathrm{Var}\,\hat f(x)", r"=", r"\dfrac{p_j(1 - p_j)}{n h^2} \approx \dfrac{f(x)}{nh}", font_size=30),
            cmath(r"\text{bias}(x)", r"=", r"\tfrac{p_j}{h} - f(x) \approx f'(x)\,(c_j - x)", font_size=30),
            cmath(r"\textstyle\int \text{bias}^2", r"\approx", r"\tfrac{h^2}{12} \textstyle\int f'^2 = \tfrac{h^2}{12} R(f')", font_size=30),
            cmath(r"\text{AMISE}(h)", r"=", r"\dfrac{1}{nh} + \dfrac{h^2}{12} R(f')", font_size=32),
        ]
        rows[3][2].set_color(PATH)
        whys = [why(r"binomial count, \ $p_j \approx h f(x)$"), why(r"$c_j$ the bin's centre: \ a tilted top"),
                why(r"$(c_j - x)$ uniform over the bin: \ variance $h^2/12$"), why(r"variance falls with $h$, \ bias grows")]
        with self.voiceover(
            "<bookmark mark='a'/> The count in a bin is binomial, so the height's variance is about f over n h: wide bins "
            "collect more points and wobble less. <bookmark mark='b'/> The bias: a flat top can't follow a sloping density, "
            "and at a point x the error is the slope times the distance from the bin's centre. <bookmark mark='c'/> Averaged "
            "over the bin, that distance squared is h squared over twelve, so the integrated squared bias is h squared over "
            "twelve times the integral of f prime squared, written R of f prime. <bookmark mark='d'/> The asymptotic MISE: "
            "one over n h, falling with h, plus a bias term growing like h squared."
        ) as vo:
            intro=label('Flat bins create first-order local approximation error',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def optimum(self):
        rows = [
            cmath(r"\dfrac{d}{dh}\,\text{AMISE}", r"=", r"-\dfrac{1}{nh^2} + \dfrac{h}{6} R(f') = 0", font_size=30),
            cmath(r"h^*", r"=", r"\Bigl(\dfrac{6}{n R(f')}\Bigr)^{1/3}", font_size=32),
            cmath(r"\text{normal}", r":", r"R(f') = \tfrac{1}{4\sqrt\pi \sigma^3}: \ \ h^* = 3.49\,\sigma\, n^{-1/3}", font_size=28),
            cmath(r"\text{AMISE}(h^*)", r"=", r"\tfrac{3}{2}\,(R(f')/6)^{1/3}\, n^{-2/3}", font_size=30),
        ]
        rows[1][2].set_color(HISTC)
        whys = [why(r"balance the two terms"), why(r"the cube-root bin"), why(r"Scott (1979): \ Part 1's rule, \ derived"),
                why(r"the error falls like $n^{-2/3}$, \ not $n^{-1}$")]
        with self.voiceover(
            "<bookmark mark='a'/> Differentiate and set to zero. <bookmark mark='b'/> The best bin width is six over n R of f "
            "prime, to the one third: that is the cube root. <bookmark mark='c'/> For a normal density R of f prime is one "
            "over four root pi sigma cubed, which gives three point four nine sigma n to the minus a third: Part 1's rule, "
            "Scott's, derived. <bookmark mark='d'/> Plugged back in, the best achievable error falls like n to the minus two "
            "thirds. A parametric estimate's error falls like one over n; estimating a whole curve is slower."
        ) as vo:
            intro=label('Balancing variance and squared bias gives a cube-root bin width',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def curves(self):
        d = load("histmise")
        hs = np.log10(np.asarray(d["hs"]))
        A = axes([-1.7, 0.2], [-3.2, -0.2], x_length=7.4, y_length=4.4, xlabel=r"bin width $h$ \ (log scale)",
                 ylabel=r"exact MISE \ (log scale)", xticks=[-1.5, -1, -0.5, 0], yticks=[-3, -2, -1],
                 xfmt=lambda v: f"{10 ** v:.2g}", yfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.0, 0.3, 0])
        ax = A.ax
        lines, dots = {}, {}
        cols = {100: HISTC, 1000: KDEC, 10000: SPLC}
        for n in d["ns"]:
            m = np.log10(np.asarray(d[f"mise_{n}"]))
            keep = (m > -3.2) & (m < -0.2)
            lines[n] = polyline(ax, hs[keep], m[keep], cols[n], 3)
            b = d[f"best_{n}"]
            dots[n] = Dot(ax.c2p(np.log10(b["h"]), np.log10(b["mise"])), radius=0.08, color=WHITE)
        rows = fit_rows(VGroup(
            label(r"truth: \ a two-humped stand-in for Old Faithful", font_size=22),
            label(rf"$n = 100$: \ best $h = {d['best_100']['h']:.2f}$ \ (formula {d['amise_h']['100']:.2f})", font_size=22, color=HISTC),
            label(rf"$n = 1{{,}}000$: \ ${d['best_1000']['h']:.3f}$ \ ({d['amise_h']['1000']:.3f})", font_size=22, color=KDEC),
            label(rf"$n = 10{{,}}000$: \ ${d['best_10000']['h']:.3f}$ \ ({d['amise_h']['10000']:.3f})", font_size=22, color=SPLC),
            label(r"left: \ variance; \ \ right: \ bias", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Exactly computed curves of MISE against bin width, for a two-humped density shaped "
            "like Old Faithful's. <bookmark mark='b'/> With a hundred observations the best bin is a third of a "
            "minute wide, and the formula says the same. <bookmark mark='c'/> With a thousand, point one five. "
            "<bookmark mark='d'/> With ten thousand, point oh seven: ten times the data, bins narrower by the cube "
            "root of ten. <bookmark mark='e'/> Each curve rises steeply on the left, where variance dominates, and "
            "more gently on the right, where bias does; both extremes are costly; the relative loss depends on the "
            "density and the range considered."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            for k, (n, m_) in enumerate(((100, "b"), (1000, "c"), (10000, "d"))):
                vo.wait_until(m_)
                self.play(Create(lines[n]), FadeIn(dots[n]), FadeIn(rows[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def rate(self):
        d = load("histmise")
        k = load("kdemise")
        hdr = [r"\textbf{$n$}", r"\textbf{best histogram MISE}", r"\textbf{best kernel MISE}", r"\textbf{ratio}"]
        body = [[f"{n:,}", f"{d[f'best_{n}']['mise']:.5f}", f"{k[f'best_{n}']['mise']:.5f}",
                 f"{d[f'best_{n}']['mise'] / k[f'best_{n}']['mise']:.1f}"] for n in d["ns"]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.32, colors=[GREY_A] + [None] * 3)
        for r in tb[1:]:
            r[1].set_color(HISTC)
            r[2].set_color(KDEC)
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(rf"fitted slopes on log $n$: \ histogram ${d['slope']:.3f}$ \ (theory $-2/3$); \ kernel ${k['slope']:.3f}$ \ (theory $-4/5$)", font_size=22),
            label(r"the histogram's flat tops cost it a whole order: \ next, \ smooth bumps", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The rates, from the exact errors. The histogram's best MISE falls with slope minus "
            "point six five in log n, close to the theory's minus two thirds. <bookmark mark='b'/> The kernel "
            "estimate of the next chapter falls faster, slope minus point seven six on its way to minus four fifths: "
            "two and a half times better at a hundred points and four times better at ten thousand. For smooth "
            "densities away from boundaries, flat histogram bins have bias of order h, whereas symmetric second-order"
            " kernels have bias of order h squared."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), LaggedStart(*[FadeIn(r) for r in tb[1:]], lag_ratio=0.3), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
        self.wait(1.0)
        self.clear_scene()
