from __future__ import annotations

import numpy as np

from videos.stats.stats43.common import *  # noqa: F403


class Stein(VoiceoverScene):
    def construct(self):
        self.card()
        self.identity()
        self.equation()
        self.bound()
        self.rates()
        self.n30()
        self.board()

    def card(self):
        card = chapter_card(10, r"Stein's method and the rates", r"How fast, \ with explicit constants?", lit=(1972,), part=PART)
        with self.voiceover("Chapter ten. Stein's method, and how fast the central limit theorem works, with constants."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def identity(self):
        rows = [
            cmath(r"Z \sim N(0, 1)", r"\iff", r"E\big[f'(Z) - Z f(Z)\big] = 0 \ \text{ for all smooth bounded } f", font_size=30),
            cmath(r"\Rightarrow", r":", r"\text{integrate by parts: } \textstyle\int f'(z) \phi(z) dz = \int z f(z) \phi(z) dz", font_size=30),
            cmath(r"\Leftarrow", r":", r"f = \text{the solution below, for } h = 1(\cdot \le x), \ \text{gives } P(W \le x) = \Phi(x)", font_size=28),
            cmath(r"\text{check}", r":", r"E[\cos Z - Z \sin Z] \approx 0; \ \ \text{for } E - 1, \ E \sim \text{Exp}(1): \ \text{not } 0", font_size=28),
        ]
        rows[0][-1].set_color(LAWC)
        whys = [why(r"Stein's identity (1972)"), why(r"$\phi'(z) = -z\phi(z)$"), why(r"the characterization"), why(r"tested in the kit")]
        with self.voiceover(
            "<bookmark mark='a'/> In 1972 Charles Stein found a characterization of the normal law that leads to explicit "
            "error bounds. A random variable is standard normal exactly when the expectation of f prime minus z f is zero "
            "for every smooth bounded f. <bookmark mark='b'/> One direction is integration by parts, because the normal "
            "density's derivative is minus z times the density. <bookmark mark='c'/> The other comes from choosing f cleverly, "
            "as the solution of an equation we write next. <bookmark mark='d'/> The kit checks it numerically: with f the "
            "sine, the expectation is zero for normal draws, and clearly not zero for a centred exponential."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def equation(self):
        rows = [
            cmath(r"f'(w) - w f(w)", r"=", r"h(w) - E h(Z)", font_size=36),
            cmath(r"f_h(w)", r"=", r"e^{w^2/2} \textstyle\int_{-\infty}^{w} \big(h(x) - E h(Z)\big) e^{-x^2/2} dx", font_size=32),
            cmath(r"E h(W) - E h(Z)", r"=", r"E\big[f_h'(W) - W f_h(W)\big]", font_size=34),
            cmath(r"\text{so}", r":", r"\text{bound the right side for the sum } W, \text{ using } \|f_h\|, \|f_h'\|, \|f_h''\|", font_size=30),
        ]
        rows[2][-1].set_color(S.ACCENT)
        whys = [why(r"Stein's equation"), why(r"its bounded solution"), why(r"substitute $W$"), why(r"distance becomes a moment bound")]
        with self.voiceover(
            "<bookmark mark='a'/> For any test function h, Stein's equation asks for an f whose f prime minus w f equals h "
            "minus its normal expectation. <bookmark mark='b'/> It is a first-order linear equation with an explicit bounded "
            "solution, and its derivatives are bounded by constants depending only on h. <bookmark mark='c'/> Substitute "
            "the sum W for w and take expectations: the distance between E h of W and E h of Z equals the expectation of f "
            "prime minus W f at W. <bookmark mark='d'/> The question about distances has become a question about one "
            "expectation, which a Taylor expansion and a clever coupling can bound."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bound(self):
        rows = [
            cmath(r"W", r"=", r"\textstyle\sum_i \xi_i, \ \ \xi_i = X_i / \sqrt n, \ \ E X = 0, \ \text{Var}\, X = 1, \ \ \rho = E|X|^3", font_size=30),
            cmath(r"d_W(W, Z)", r"\le", r"\textstyle\sum_i E|\xi_i|^3 = \rho / \sqrt n", font_size=34),
            cmath(r"d_K(W, Z)", r"\le", r"C \rho / \sqrt n, \ \ C \le 0.4748", font_size=34),
            cmath(r"\text{tight}", r":", r"\text{for a fair coin, } d_K \approx 1/\sqrt{2\pi n}: \ \text{the rate cannot improve}", font_size=30),
        ]
        rows[1][-1].set_color(GOODC)
        rows[2][-1].set_color(S.ACCENT)
        whys = [why(r"standardized sums"), why(r"Stein, \ zero-bias coupling"), why(r"Berry--Esseen; \ Shevtsova (2011)"), why(r"half the largest atom")]
        with self.voiceover(
            "<bookmark mark='a'/> For a standardized sum of independent terms with third absolute moment rho, <bookmark "
            "mark='b'/> Stein's method with Larry Goldstein's zero-bias coupling gives a clean bound on the Wasserstein "
            "distance: at most rho over root n, constant one. <bookmark mark='c'/> For the Kolmogorov distance, the "
            "Berry–Esseen theorem gives C rho over root n, and after decades of work the best known constant for identically "
            "distributed summands is point four seven four eight, by Irina Shevtsova in 2011. <bookmark mark='d'/> The rate "
            "one over root n cannot be improved: a fair coin's standardized sum has atoms of height about one over root two pi "
            "n, and a continuous CDF must miss half of each jump."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rates(self):
        d = load("rates")
        ns = np.log10(np.asarray(d["ns"], float))
        A = axes([0, 3.1], [-3.2, 0], x_length=7.4, y_length=4.4, xlabel=r"$n$", ylabel=r"Kolmogorov distance to $\Phi$ \ (exact)",
                 xticks=[0, 1, 2, 3], yticks=[-3, -2, -1, 0], log_x=True, xfmt=lambda v: f"10^{{{int(v)}}}",
                 yfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.5, 0.2, 0])
        ax = A.ax
        kinds = [("bernoulli", r"coin, \ $p = 1/2$", LAWC), ("bernoulli01", r"coin, \ $p = 0.1$", S.PRIOR),
                 ("poisson", r"Poisson(1)", S.ALT), ("exponential", r"exponential", S.ACCENT)]
        lines, bes = VGroup(), VGroup()
        for kname, nm, c in kinds:
            r = d["rows"][kname]
            lines.add(VGroup(polyline(ax, ns, np.log10(r["kolmogorov"]), c, 3),
                             *[Dot(ax.c2p(a, np.log10(b)), radius=0.05, color=c) for a, b in zip(ns, r["kolmogorov"])]))
            bes.add(DashedLine(ax.c2p(0, np.log10(min(r["be"][0], 1))), ax.c2p(3.01, np.log10(r["be"][-1])), color=c, stroke_width=1.8))
        side = fit_rows(VGroup(*[label(rf"{nm}: \ slope ${d['rows'][k]['slope']:.3f}$, \ up to {100 * d['rows'][k]['ratio_be']:.0f}\% of the bound", font_size=20, color=c)
                                 for k, nm, c in kinds],
                               label(r"dashed: \ Berry--Esseen $0.4748\,\rho/\sqrt n$", font_size=20, color=GREY_A)),
                        4.6, 0.36, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> This is the part's weak-convergence lab. For four kinds of sum, the exact Kolmogorov "
            f"distance from the normal, computed from binomial, Poisson and gamma probabilities, for n from one to a thousand "
            f"and twenty-four, on log-log axes. <bookmark mark='b'/> Every line has slope minus one half to within a few "
            f"thousandths: the one-over-root-n rate, measured. <bookmark mark='c'/> The dashed lines are the Berry–Esseen "
            f"bounds. The fair coin comes within {100 * d['rows']['bernoulli']['ratio_be']:.0f} percent of its bound, so the "
            f"constant is nearly sharp; the exponential sits at about {100 * d['rows']['exponential']['ratio_be']:.0f} "
            f"percent of its own, because a continuous law has no atoms to jump over and its skewness costs less than the "
            f"bound fears."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact: binomial, Poisson and gamma CDFs")))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.4), FadeIn(side[:4]), run_time=4.0)
            vo.wait_until("b")
            self.play(Indicate(side[:4]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(b) for b in bes], lag_ratio=0.3), FadeIn(side[4]), run_time=2.5)
        self.clear_scene()

    def n30(self):
        d = load("rates")
        rows = fit_rows(VGroup(
            label(rf"the exponential at $n = 30$: \ Kolmogorov distance {d['k30']:.3f}, \ bound {d['be30']:.3f}", font_size=26, color=S.ACCENT),
            label(r"so the CDF is within 2.4\% everywhere: \ ``$n \ge 30$'' looks safe", font_size=26, color=GREY_A),
            label(r"but a $t$ interval needs the tails, \ and skewness enters at order $1/\sqrt n$", font_size=26, color=BADC),
            label(r"Part 47's Edgeworth correction: \ $P(T \le z) \approx \Phi(z) + \frac{\gamma}{6\sqrt n}(2z^2 + 1)\phi(z)$", font_size=26, color=GOODC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> What about the folklore of Part six, that thirty is enough? For the exponential at thirty, "
            f"the Kolmogorov distance is {say(d['k30'], 3)}, against a bound of {say(d['be30'], 3)}. <bookmark mark='b'/> The "
            f"sum's CDF is within two and a half percent of normal everywhere, which sounds safe. <bookmark mark='c'/> But a "
            f"confidence interval lives in the tails, where two and a half percent is half of the five percent we promised, "
            f"and the t statistic's skewness enters at exactly the one-over-root-n rate. <bookmark mark='d'/> Part forty-seven's "
            f"Edgeworth expansion will give the correction term; the Board shows what happens without it."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        show_board(self, board_rows("Uniform", "Exp(1)"),
                   "<bookmark mark='a'/> The Coverage Board: nominal ninety percent t intervals for a mean. For uniform data, "
                   "symmetric with light tails, ten observations are plenty: kept. <bookmark mark='b'/> For exponential data, "
                   "ten observations cover eighty-six percent, and a hundred cover eighty-nine point two: both broken, by a "
                   "margin that shrinks like one over root n. <bookmark mark='c'/> At a thousand, coverage reaches ninety "
                   "percent within simulation error: kept.",
                   [("a", [0]), ("b", [1, 2]), ("c", [3])])
