from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats43.common import *  # noqa: F403


class Stable(VoiceoverScene):
    def construct(self):
        self.card()
        self.divisible()
        self.stable()
        self.pareto()
        self.dax()
        self.aggregate()
        self.board()

    def card(self):
        card = chapter_card(11, r"Infinitely divisible and stable laws", r"What can a sum converge to?", lit=(1925,), part=PART)
        with self.voiceover("Chapter eleven. Infinitely divisible and stable laws: what else a sum can converge to."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def divisible(self):
        rows = [
            cmath(r"\text{ID}", r":", r"\text{for every } n, \ X \overset{d}{=} Y_{n1} + \cdots + Y_{nn}, \ \text{i.i.d.}", font_size=32),
            cmath(r"\log \varphi(t)", r"=", r"i b t - \tfrac12 \sigma^2 t^2 + \textstyle\int \big(e^{itx} - 1 - itx 1_{|x| < 1}\big) \nu(dx)", font_size=30),
            cmath(r"\text{in}", r":", r"\text{normal } (\nu = 0), \ \text{Poisson } (\nu = \lambda \delta_1), \ \text{gamma, Cauchy, } t", font_size=30),
            cmath(r"\text{not}", r":", r"\text{uniform, binomial: \ bounded and non-degenerate}", font_size=32),
        ]
        rows[1][-1].set_color(LAWC)
        whys = [why(r"infinitely divisible"), why(r"L\'evy--Khintchine"), why(r"drift, \ Gaussian part, \ jumps"), why(r"no bounded law but a point")]
        with self.voiceover(
            "<bookmark mark='a'/> Which laws can be limits of sums in an infinitesimal triangular array, where every "
            "summand becomes small in probability? Exactly the infinitely divisible ones: those that can be written, "
            "for every n, as a sum of n independent identical pieces. <bookmark mark='b'/> Lévy and Khintchine "
            "described them all. The logarithm of the characteristic function is a drift, a Gaussian part, and an "
            "integral against a Lévy measure nu that records how often jumps of each size occur, with no mass at zero"
            " and finite integral of the smaller of one and x squared. <bookmark mark='c'/> The normal has no jumps; "
            "the Poisson has jumps of size one at rate lambda; the gamma, the Cauchy and Student's t are infinitely "
            "divisible too. <bookmark mark='d'/> The uniform and the binomial are not: no bounded law other than a "
            "point can be. Part forty-four's Lévy processes are these laws, unrolled in time."        ) as vo:
            heading=label('Infinitesimal independent arrays have infinitely divisible limits',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def stable(self):
        rows = [
            cmath(r"\text{stable}", r":", r"X_1 + \cdots + X_n \overset{d}{=} n^{1/\alpha} X \ \ \text{(symmetric case)}", font_size=32),
            cmath(r"\varphi(t)", r"=", r"e^{-c|t|^\alpha}, \ \ 0 < \alpha \le 2: \ \ \alpha = 2 \text{ normal}, \ \alpha = 1 \text{ Cauchy}", font_size=30),
            cmath(r"P(|X| > x)", r"\sim", r"C x^{-\alpha} \ \ (\alpha < 2): \ \text{infinite variance}", font_size=32),
            cmath(r"\text{generalized CLT}", r":", r"0<\alpha<2:\ \text{regular variation + tail balance; centering and slowly varying scale}", font_size=28),
        ]
        rows[3][-1].set_color(S.ACCENT)
        whys = [why(r"sums keep their shape"), why(r"L\'evy (1925)"), why(r"power-law tails"), why(r"domains of attraction")]
        with self.voiceover(
            "<bookmark mark='a'/> Among them, the stable laws are the possible limits of normalized sums of identical"
            " variables: a sum of n copies has the same shape as one copy, scaled by n to the one over alpha. "
            "<bookmark mark='b'/> In the symmetric case the characteristic function is e to the minus c times "
            "absolute t to the alpha, with alpha between zero and two. Alpha two is the normal; alpha one is the "
            "Cauchy. <bookmark mark='c'/> Below two, the tails fall off like a power, x to the minus alpha, so the "
            "variance is infinite. <bookmark mark='d'/> The generalized central limit theorem: for alpha strictly "
            "below two, stable domains of attraction require regularly varying tails and a limiting tail balance. In "
            "general the normalization includes a slowly varying factor and centering; a pure n to the one over alpha"
            " scale is a special case such as our symmetric Pareto example. The normal domain has a separate "
            "truncated-variance criterion. The normal law is the one stable law with a finite variance, which is why "
            "it is everywhere; but it is not the only possible limit."
        ) as vo:
            heading=label('Stable domains need the correct centering and normalization',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def pareto(self):
        d = load("stable")
        t = np.array([0.25, 0.5, 1.0, 2.0])
        A = axes([0, 2.2], [0, 1], x_length=7.4, y_length=4.4, xlabel=r"$t$", ylabel=r"$\text{Re}\, \varphi(t)$ of $S_n / n^{2/3}$",
                 xticks=[0, 0.5, 1, 1.5, 2], yticks=[0, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        ts = np.linspace(0, 2.2, 200)
        lim = curve(ax, ts, np.exp(-d["c"] * ts ** d["alpha"]), LIMC, 4)
        cols = [GREY_B, LAWC, S.ALT]
        pts = VGroup()
        for r, c in zip(d["rows"], cols):
            pts.add(VGroup(*[Dot(ax.c2p(a, b), radius=0.08, color=c) for a, b in zip(t, r["emp"])]))
        side = fit_rows(VGroup(
            label(r"symmetric Pareto: \ $P(|X| > x) = x^{-3/2}$, \ $x \ge 1$", font_size=22),
            label(rf"limit: \ $e^{{-c|t|^{{3/2}}}}$, \ $c = \Gamma(-\tfrac12)\cos(\tfrac{{3\pi}}{{4}}) = {d['c']:.3f}$", font_size=22, color=LIMC),
            label(r"grey, \ blue, \ teal: \ $n = 10, \ 100, \ 1{,}000$", font_size=22, color=GREY_A),
            label(r"converging, \ slowly: \ the error shrinks like $n^{-1/3}$", font_size=22, color=S.ACCENT),
            label(rf"90\% of $|S_n/n^{{2/3}}|$ below {d['rows'][-1]['q90']:.2f} \ (limit {d['limit_q90']:.2f})", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A test of the generalized theorem. Take symmetric Pareto variables whose tails fall like x to the minus three halves: infinite variance, finite mean. <bookmark mark='b'/> The theorem predicts that sums divided by n to the two thirds converge to the symmetric stable law with alpha three halves, whose characteristic function, in gold, has a constant c that comes from the tail: gamma of minus a half times the cosine of three pi over four, {say(d['c'], 2)}. <bookmark mark='c'/> The dots are empirical characteristic functions of twenty thousand normalized sums each, for ten, a hundred and a thousand terms. <bookmark mark='d'/> They approach the limit, but slowly: the leftover error shrinks only like n to the minus one third, because the Pareto law's bounded core still adds a little Gaussian-like variance. <bookmark mark='e'/> This particular Pareto law has a slow approach. Exact stable inputs already preserve their shape under summation, so heavy tails do not slow every limit theorem."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"simulated: 20,000 sums at each $n$")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lim), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.5), FadeIn(side[2]), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def dax(self):
        d = load("stable")
        h = np.asarray(d["dax_hist"])
        edges = np.linspace(-6, 6, 61)
        mid = (edges[:-1] + edges[1:]) / 2
        A = axes([-6, 6], [0, 0.6], x_length=7.4, y_length=4.4, xlabel=r"daily log return, \ standardized", ylabel=r"density",
                 xticks=[-6, -4, -2, 0, 2, 4, 6], yticks=[0, 0.3, 0.6], center=[-2.5, 0.2, 0])
        ax = A.ax
        bars = bars_at(ax, mid, h, edges[1] - edges[0], LAWC, opacity=0.75)
        xs = np.linspace(-6, 6, 300)
        nc = curve(ax, xs, stats.norm.pdf(xs), LIMC, 3)
        hl = d["dax_hill"]
        side = fit_rows(VGroup(
            label(rf"the DAX, \ {d['dax_n']:,} trading days, \ 1991--1998", font_size=22),
            label(rf"excess kurtosis {d['dax_kurt']:.1f}: \ a sharp peak, \ heavy tails", font_size=22, color=LAWC),
            label(rf"beyond 4 SD: \ {100 * d['dax_tail']:.2f}\% of days vs {100 * d['normal_tail']:.4f}\% normal", font_size=22, color=BADC),
            label(rf"Hill's tail index: \ {hl['100']:.1f}--{hl['25']:.1f} \ (100 to 25 largest)", font_size=22, color=S.ACCENT),
            label(r"Hill estimates do not prove finite variance or a dependent CLT", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Real data with heavy tails. Here are {d['dax_n']:,} daily returns of the German stock index, the DAX, from 1991 to 1998, standardized, against the normal curve. <bookmark mark='b'/> The peak is too sharp and the tails too heavy: the excess kurtosis is {say(d['dax_kurt'], 1)}. <bookmark mark='c'/> Days beyond four standard deviations happen {100 * d['dax_tail']:.2f} percent of the time, some fifty times more often than a normal law allows. <bookmark mark='d'/> Bruce Hill's estimator of the tail index, from the largest hundred down to the largest twenty-five returns, gives between {say(hl['100'], 1)} and {say(hl['25'], 1)}. <bookmark mark='e'/> Those estimates exceed two, which is compatible with a finite-variance tail model. They cannot establish a tail exponent or finite variance from this record, and a CLT for dependent returns needs further assumptions. Benoît Mandelbrot argued in 1963 that cotton prices had stable laws with alpha below two; this one DAX record does not settle a universal tail model for stock returns."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"EuStockMarkets: \ the DAX, \ 1991--1998")))
            vo.wait_until("a")
            self.play(FadeIn(bars), Create(nc), FadeIn(side[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k + 1]))
        self.clear_scene()

    def aggregate(self):
        d = load("stable")
        rows = [[r"returns over", r"observations", r"excess kurtosis", r"KS distance to $N$"]] + [
            [f"{r['m']} day{'s' if r['m'] > 1 else ''}", f"{r['n']:,}", f"{r['kurt']:.2f}", f"{r['ks']:.3f}"] for r in d["dax_sums"]]
        tab = table_rows(rows, font_size=28, col_buff=0.7, row_buff=0.22).move_to([0, 0.8, 0])
        msg = fit_rows(VGroup(
            label(r"summing days into weeks and months, \ the sample kurtosis falls: \ a descriptive aggregation pattern", font_size=24, color=GOODC),
            label(r"the KS distances barely move: \ fewer, \ longer periods mean more sampling noise", font_size=22, color=GREY_A),
            label(r"real returns are dependent too: \ volatility clusters \ (Part 38's GARCH); \ Part 44 handles dependence", font_size=22, color=S.ACCENT),
        ), 12.4, 0.3, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Sum the daily returns into weekly and monthly ones. <bookmark mark='b'/> The excess"
            " kurtosis falls from six to about one and then to about point three seven: a descriptive aggregation "
            "pattern, which finance calls aggregational Gaussianity. <bookmark mark='c'/> The Kolmogorov distances "
            "barely move, because there are fewer and fewer months to estimate them from. <bookmark mark='d'/> And "
            "real returns are not independent: their volatility clusters, as Part thirty-eight's GARCH models showed."
            " Limit theorems for dependent sequences are the subject of the next part."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(msg[k]))
        self.clear_scene()

    def board(self):
        show_board(self, board_rows("Pareto"),
                   "<bookmark mark='a'/> On the Board, t intervals for the mean of Pareto data. With tail index two and a "
            "half, the variance is finite but the third moment is not, and a hundred observations cover only "
            "eighty-four percent: broken. <bookmark mark='b'/> With tail index one and a half, the variance is "
            "infinite, the standardized mean does not converge to a normal at all, and even a thousand observations "
            "cover seventy percent: broken, and increasing the sample size does not restore the usual Gaussian "
            "studentized limit. The seventy-percent figure is this finite simulation, not a proof about every sample "
            "size.",
                   [("a", [0]), ("b", [1])])
