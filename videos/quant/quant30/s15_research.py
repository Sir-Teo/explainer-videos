from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant30.common import BAD, EST_C, GOOD, HURDLE, PART, REAL_C, SHRINK_C, TRUE_C, fit_right, load


class Research(VoiceoverScene):
    def construct(self):
        t = load("theory")
        self.card()
        self.setup_()
        self.insample()
        self.lemma()
        self.outsample()
        self.theorem()
        self.sims(t)
        self.hists(t)
        self.beyond(load("shrink"))
        self.data(t)
        self.shrunk(t)
        self.correction(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"Why the optimizer underestimates its own risk", r"How much riskier is the sample "
                          r"minimum-variance portfolio than it believes, exactly?", part=PART)
        with self.voiceover("For the researcher: exact sampling laws under a fixed Gaussian model. Sample GMV's self-reported variance is biased downward across repeated samples, while its true population variance cannot beat the population minimum. That does not mean every realised self-report is too low. We will state the assumptions, distributions and limits separately."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_(self):
        rows = [cmath(r"w^*", r"=", r"\frac{\Sigma^{-1}1}{1^\top\Sigma^{-1}1},\qquad \sigma^2_{\min} = \frac{1}{1^\top\Sigma^{-1}1}",
                      font_size=32, colors={r"w^*": TRUE_C}),
                cmath(r"\hat w", r"=", r"\frac{\hat\Sigma^{-1}1}{1^\top\hat\Sigma^{-1}1},\qquad n\hat\Sigma \sim W_K(n, \Sigma),\ n = T - 1",
                      font_size=30, colors={r"\hat w": EST_C}),
                cmath(r"\hat\sigma^2_{\text{in}} = \hat w^\top\hat\Sigma\hat w", r",", r"\quad \sigma^2_{\text{out}} = "
                      r"\hat w^\top\Sigma\hat w", font_size=32, colors={r"\hat\sigma^2_{\text{in}} = \hat w^\top\hat\Sigma\hat w": EST_C})]
        whys = [why(r"the global minimum-variance portfolio of $K$ assets and its variance"),
                why(r"IID Gaussian, fixed $\Sigma\succ0$, $n=T-1\ge K$; $n\hat\Sigma$ is Wishart"),
                why(r"what the optimizer reports about itself, and what it actually has")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Fix a population before drawing data. <bookmark mark='a'/> Let returns be independent identically distributed Gaussian vectors with fixed positive-definite covariance Sigma. The population GMV has unit budget and no inequality constraints. <bookmark mark='b'/> From T observations form the demeaned divisor-T-minus-one covariance, so n times the estimate is Wishart with n equal to T minus one. Require n at least K for an invertible sample covariance. <bookmark mark='c'/> The reported variance uses that fitted covariance; the true variance evaluates the same fitted weights under fixed Sigma. The latter is population risk, not one future sample variance."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def insample(self):
        rows = [cmath(r"\hat\sigma^2_{\text{in}}", r"=", r"\frac{1}{1^\top\hat\Sigma^{-1}1}", font_size=34,
                      colors={r"\hat\sigma^2_{\text{in}}": EST_C}),
                cmath(r"\frac{a^\top\Sigma^{-1}a}{a^\top W^{-1}a}", r"\sim", r"\chi^2_{n - K + 1}\quad (W \sim W_K(n, \Sigma))",
                      font_size=30, colors={r"\frac{a^\top\Sigma^{-1}a}{a^\top W^{-1}a}": HURDLE}),
                cmath(r"\frac{\hat\sigma^2_{\text{in}}}{\sigma^2_{\min}}", r"=", r"\frac{\chi^2_{n-K+1}}{n},\qquad \mathbb E = "
                      r"\frac{n - K + 1}{n} \to 1 - \gamma", font_size=30, colors={r"\frac{\hat\sigma^2_{\text{in}}}{\sigma^2_{\min}}": EST_C})]
        whys = [why(r"in sample, the optimizer's variance is the reciprocal of a quadratic form in the inverse estimate"),
                why('Wishart identity (Muirhead 1982, Theorem 3.2.12): for fixed nonzero $a$, positive-definite $\\Sigma$ and $n\\ge K$, this ratio is chi-square'),
                why(r"take $a = 1$ and $W = n\hat\Sigma$: the reported variance is the true minimum times a chi-square over "
                    r"$n$, which loses $K - 1$ degrees of freedom; $\gamma = K/T$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The in-sample distribution. <bookmark mark='a'/> Reported GMV variance is the reciprocal of the ones-vector quadratic form in the inverse estimate. <bookmark mark='b'/> For fixed nonzero a and full-rank Wishart W, the ratio of population inverse quadratic form to Wishart inverse quadratic form is chi-square with n minus K plus one degrees of freedom. <bookmark mark='c'/> Set a to ones and W to n times the sample covariance. Expected reported variance relative to the population minimum is n minus K plus one over n. It is below one for K greater than one, but the chi-square has an unbounded upper tail: an individual report can exceed the minimum or its own population risk."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def lemma(self):
        rows = [cmath(r"a = e_1", r":", r"\text{rotate and scale so the vector is the first coordinate}", font_size=30,
                      colors={r"a = e_1": HURDLE}),
                cmath(r"(W^{-1})_{11}", r"=", r"\frac{1}{W_{11\cdot 2}},\quad W_{11\cdot2} = W_{11} - W_{12}W_{22}^{-1}W_{21}",
                      font_size=30),
                cmath(r"W_{11\cdot2}", r"\sim", r"\sigma_{11\cdot2}\,\chi^2_{n - K + 1},\quad (\Sigma^{-1})_{11} = "
                      r"\frac{1}{\sigma_{11\cdot 2}}", font_size=30, colors={r"W_{11\cdot2}": HURDLE}),
                cmath(r"\frac{(\Sigma^{-1})_{11}}{(W^{-1})_{11}}", r"=", r"\frac{W_{11\cdot2}}{\sigma_{11\cdot2}} \sim "
                      r"\chi^2_{n-K+1}", font_size=30)]
        whys = [why(r"the ratio is unchanged by an invertible change of coordinates applied to $a$, $W$ and $\Sigma$ "
                    r"together"),
                why(r"the inverse of a partitioned matrix: the top-left entry of the inverse is one over a Schur complement"),
                why(r"the Schur complement of a Wishart matrix is Wishart with $K - 1$ fewer degrees of freedom: regressing "
                    r"on the other $K - 1$ coordinates uses them up"),
                why(r"so the ratio is a chi-square with $n - K + 1$ degrees of freedom, as claimed")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "Why the lemma holds, in four lines. <bookmark mark='a'/> Change coordinates so the fixed vector is the first "
            "axis; the ratio does not change. <bookmark mark='b'/> The top-left entry of an inverse matrix is one over a "
            "Schur complement: the first variance left over after regressing on the others. <bookmark mark='c'/> For a "
            "Wishart matrix that complement is again Wishart, a scaled chi-square, with K minus one fewer degrees of "
            "freedom: each of the other coordinates uses one up. <bookmark mark='d'/> Divide by the true complement, and "
            "the ratio is a chi-square with n minus K plus one degrees of freedom. The optimizer's optimism is exactly "
            "those lost degrees of freedom."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def outsample(self):
        rows = [cmath(r"W=Z^\top Z=\begin{pmatrix}a&b^\top\\ b&C\end{pmatrix}", r":", r"\beta=C^{-1}b,\quad x=(1,-\beta^\top)^\top", font_size=28),
                cmath(r"\beta\mid C", r"\sim", r"N_{K-1}(0,C^{-1}),\quad C\sim W_{K-1}(n,I)", font_size=29),
                cmath(r"\frac{\sigma^2_{\text{out}}}{\sigma^2_{\min}}", r"\sim", r"1+\|\beta\|^2=1+\frac{K-1}{n-K+2}F_{K-1,n-K+2}", font_size=29),
                cmath(r"\mathbb E[\sigma^2_{\text{out}}/\sigma^2_{\min}]", r"=", r"\frac{n-1}{n-K},\quad n>K,\quad K\ge2", font_size=30)]
        whys = [why(r"whiten returns and rotate the transformed budget to $e_1$; unit-budget weights are $(1,-\beta)$"),
                why(r"Gaussian regression: conditional normal coefficients; mixing over Wishart $C$ gives a multivariate $t$"),
                why(r"$\nu=n-K+2$: $\sqrt{\nu}\,\beta$ is spherical $t_\nu$; its squared norm is $(K-1)F_{K-1,\nu}$"),
                why(r"the finite mean needs $n>K$; $K=1$ has true-risk ratio identically one")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover("The population risk distribution. <bookmark mark='a'/> Whiten and rotate the transformed budget vector to the first coordinate. In these coordinates sample GMV weights are one followed by minus the regression coefficient beta. <bookmark mark='b'/> Conditional on the remaining Wishart block C, beta is normal with covariance C inverse. Mixing over C gives a spherical multivariate t with n minus K plus two degrees of freedom. <bookmark mark='c'/> Population risk relative to its minimum is one plus beta squared, giving the displayed F law for K at least two. <bookmark mark='d'/> Its finite expectation requires n greater than K and equals n minus one over n minus K. With one asset the true-risk ratio is exactly one.") as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def theorem(self):
        st = VGroup(MathTex(r"\frac{\hat\sigma^2_{\text{in}}}{\sigma^2_{\min}} \xrightarrow{p} 1 - \gamma,\qquad "
                            r"\frac{\sigma^2_{\text{out}}}{\sigma^2_{\min}} \xrightarrow{p} \frac{1}{1 - \gamma},\qquad "
                            r"\frac{\sigma^2_{\text{out}}}{\hat\sigma^2_{\text{in}}} \xrightarrow{p} \frac{1}{(1 - \gamma)^2}",
                            font_size=30),
                    wrapped_label(r"for i.i.d.\ normal returns, $K, T \to \infty$, $K/T \to \gamma < 1$; extensions require "
                                  r"additional moment, dependence and spectral conditions (Bai, Liu and Wong 2009; El Karoui "
                                  r"2010)", 9.6, 20)).arrange(DOWN, buff=0.35)
        card = theorem_card(r"The optimizer's risk illusion", st, r"Kempf and Memmel (2006); El Karoui (2010)", width=11.4,
                            font_size=22)
        with self.voiceover(
            "A sequence of dimensions and samples. <bookmark mark='a'/> Let K and T grow with K over T tending to gamma strictly below one. Under the stated IID Gaussian model the chi-square and F components concentrate. Reported variance divided by the population minimum tends in probability to one minus gamma; true risk tends to one over one minus gamma. Their random ratio tends to one over one minus gamma squared. With gamma one half the limiting multiplier is four. <bookmark mark='b'/> Extensions beyond normality need explicit moment, dependence and spectral regularity conditions. The limit alone does not validate every heavy-tailed or changing-covariance backtest."
        ) as vo:
            self.add(card)
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.5)
        self.clear_scene()

    def sims(self, t):
        Ts = sorted(int(k) for k in t["sims"])
        K = t["K"]
        gam = np.array([K / T for T in Ts])
        gg = np.linspace(0.07, 0.83, 60)
        g = axes([0, 0.9], [0, 7], x_length=7.4, y_length=4.4, xlabel=r"$\gamma = K/T$ ($K = 49$)",
                 ylabel=r"variance relative to the true minimum", xticks=[0, 0.3, 0.6, 0.9], yticks=[0, 1, 3, 7],
                 font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        lin = curve(ax, gg, 1 - gg, EST_C, stroke_width=2.5)
        lout = curve(ax, gg, 1 / (1 - gg), REAL_C, stroke_width=2.5)
        one = DashedLine(ax.c2p(0, 1), ax.c2p(0.9, 1), color=GREY_B, stroke_width=1.2)
        din = VGroup(*[Dot(ax.c2p(a, t["sims"][str(T)]["in"]), radius=0.06, color=EST_C) for a, T in zip(gam, Ts)])
        dout = VGroup(*[Dot(ax.c2p(a, t["sims"][str(T)]["out"]), radius=0.06, color=REAL_C) for a, T in zip(gam, Ts)])
        leg = legend([(EST_C, r"reported: $1 - \gamma$"), (REAL_C, r"true: $1/(1 - \gamma)$")], font_size=15
                     ).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        s60, s120 = t["sims"]["60"], t["sims"]["120"]
        side = wrapped_label(rf"dots: 1{{,}}000 simulated samples each, from the industries' covariance; at $T = 120$: "
                             rf"{s120['in']:.3f} and {s120['out']:.3f}, exact {s120['in_th']:.3f} and {s120['out_th']:.3f}",
                             3.4, 15, GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Check it, with the industries' own covariance as the truth. <bookmark mark='a'/> The red line is the limit of "
            "what the optimizer reports, the teal one the limit of what it has. <bookmark mark='b'/> The dots are "
            "simulations, a thousand samples at each length. At ten years of data they give "
            f"{s120['in']:.3f} and {s120['out']:.3f}, against exact values of {s120['in_th']:.3f} and {s120['out_th']:.3f}. "
            f"At five years the true variance is {s60['out']:.1f} times the minimum, while the optimizer reports "
            f"{s60['in']:.2f}."
        ) as vo:
            self.play(FadeIn(g), Create(one), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(lin), Create(lout))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in din], lag_ratio=0.2), LaggedStart(*[FadeIn(d_) for d_ in dout],
                                                                                            lag_ratio=0.2), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def hists(self, t):
        s = t["sims"]["120"]
        hi, ho = np.asarray(s["hist_in"], float), np.asarray(s["hist_out"], float)
        ym = float(np.ceil(max(hi.max(), ho.max()) / 1000 * 20) / 20)
        g1 = axes([0, 2], [0, ym], x_length=5.0, y_length=3.4, xlabel=r"reported $\hat\sigma^2_{\text{in}}/\sigma^2_{\min}$",
                  ylabel=r"share of 1,000", xticks=[0, 1, 2], yticks=[0, ym], font_size=14).move_to(LEFT * 3.4 + DOWN * 0.3)
        g2 = axes([0, 6], [0, ym], x_length=5.0, y_length=3.4, xlabel=r"true $\sigma^2_{\text{out}}/\sigma^2_{\min}$",
                  ylabel=r"share of 1,000", xticks=[0, 1, 3, 6], yticks=[0, ym], font_size=14).move_to(RIGHT * 3.2 + DOWN * 0.3)

        def bars(ax, h, x0, x1, col):
            w = (x1 - x0) / len(h)
            m = h.max()
            return VGroup(*[Rectangle(width=ax.c2p(w, 0)[0] - ax.c2p(0, 0)[0] - 0.01,
                                      height=max(ax.c2p(0, v / 1000)[1] - ax.c2p(0, 0)[1], 0.001), stroke_width=0,
                                      fill_color=col, fill_opacity=0.85).move_to(ax.c2p(x0 + (k + 0.5) * w, 0),
                                                                                 aligned_edge=DOWN)
                            for k, v in enumerate(h) if v > 0])
        b1, b2 = bars(g1.ax, hi, 0, 2, EST_C), bars(g2.ax, ho, 0, 6, REAL_C)
        l1 = DashedLine(g1.ax.c2p(1, 0), g1.ax.c2p(1, ym), color=GREY_B)
        l2 = DashedLine(g2.ax.c2p(1, 0), g2.ax.c2p(1, ym), color=GREY_B)
        title = label(r"$T = 120$ months, $K = 49$: 1{,}000 samples", font_size=20, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "The saved thousand-draw distributions at T equal to a hundred and twenty. <bookmark mark='a'/> Here the displayed reported-risk counts lie below the population minimum, and every cached draw falls within the shown bins. Each height is its count divided by a thousand, not its fraction of the peak. This finite sample does not remove the chi-square upper tail. <bookmark mark='b'/> True population variance is at least the population minimum by definition of the optimum. Its right tail reflects directional estimation error. Neither fact implies that the reported variance is below true variance for every possible draw."
        ) as vo:
            self.play(FadeIn(title), FadeIn(g1), FadeIn(g2), Create(l1), Create(l2))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in b1], lag_ratio=0.03))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in b2], lag_ratio=0.03))
        self.wait(0.4)
        self.clear_scene()

    def beyond(self, sh):
        Ts = ["60", "120", "240"]
        gam = np.array([49 / int(T) for T in Ts])
        gg = np.linspace(0.15, 0.85, 50)
        g = axes([0, 0.9], [0, 7], x_length=7.4, y_length=4.4, xlabel=r"$\gamma = K/T$", ylabel=r"true variance "
                 r"relative to the minimum", xticks=[0, 0.3, 0.6, 0.9], yticks=[0, 1, 3, 7], font_size=15
                 ).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        lout = curve(ax, gg, 1 / (1 - gg), REAL_C, stroke_width=2.5)
        cols = {"sample": BAD, "LW const-corr": SHRINK_C, "nonlinear": GOOD}
        dots = VGroup()
        for k, c in cols.items():
            dots.add(VGroup(*[Dot(ax.c2p(a, sh["sims"][T][k]["gmv"]), radius=0.07, color=c) for a, T in zip(gam, Ts)]))
        leg = legend([(REAL_C, r"the theorem: sample covariance"), (BAD, r"sample, simulated"),
                      (SHRINK_C, r"constant-correlation shrinkage"), (GOOD, r"nonlinear shrinkage")], font_size=15
                     ).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        s60 = sh["sims"]["60"]
        with self.voiceover(
            f"""The exact laws concern sample-covariance GMV. <bookmark mark='a'/> The teal curve is its high-dimensional limit; the dots average a hundred Gaussian draws in Chapter four, so finite-sample expectations and Monte Carlo variation remain relevant. <bookmark mark='b'/> At sixty observations, nonlinear shrinkage has true-risk ratio {s60['nonlinear']['gmv']:.2f}, versus {s60['sample']['gmv']:.1f} for sample covariance. This different estimator has a different law. Its improvement in the chosen population is not a universal escape from estimation risk."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(lout), FadeIn(dots[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots[1]), FadeIn(dots[2]))
        self.wait(0.4)
        self.clear_scene()

    def data(self, t):
        rows = t["data"]
        hx = [-4.0, -1.4, 1.2, 3.6, 5.6]
        head = VGroup(label(r"window", font_size=18, color=GREY_B), label(r"reported vol", font_size=18, color=EST_C),
                      label(r"realised vol", font_size=18, color=REAL_C), label(r"ratio of variances", font_size=18,
                                                                                color=GREY_B),
                      label(r"normal theory", font_size=18, color=HURDLE))
        tab = VGroup(head)
        for r in rows:
            tab.add(VGroup(MathTex(rf"{r['W']}\ \text{{months}}", font_size=24), MathTex(rf"{100 * r['pred_vol']:.1f}\%", font_size=24),
                           MathTex(rf"{100 * r['real_vol']:.1f}\%", font_size=24), MathTex(f"{r['ratio']:.1f}", font_size=26),
                           MathTex(f"{r['theory']:.1f}", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.0 - 0.75 * j, 0])
        foot = wrapped_label(r"the sample minimum-variance portfolio of the 49 industries, re-estimated each year 1980--2020 "
                             r"on the trailing window; realised: the variance of its next 12 monthly returns; theory: "
                             r"$\frac{n - 1}{n - K}\big/\frac{n - K + 1}{n}$", 11.6, 16, GREY_A).to_edge(DOWN, buff=0.5)
        r60, r120 = rows[0], rows[2]
        with self.voiceover(
            f"""A descriptive check on research-period industry returns. <bookmark mark='a'/> With sixty-month windows, average forecast variance and average next-twelve-month realised variance correspond to {100 * r60['pred_vol']:.1f} and {100 * r60['real_vol']:.1f} percent annualised volatility. Their ratio is {r60['ratio']:.0f}, versus {r60['theory']:.0f} for the ratio of Gaussian expectations. At a hundred and twenty months the values are {r120['ratio']:.1f} and {r120['theory']:.1f}. This is a ratio of averages, not an average of individual ratios. The comparison does not identify how much of the gap comes from tails, dependence, covariance changes or noisy realised-variance measurement."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def shrunk(self, t):
        Ws = [r["W"] for r in t["data"]]
        xs = np.arange(len(Ws))
        samp = np.log10([r["ratio"] for r in t["data"]])
        lw = np.log10([r["ratio"] for r in t["lw"]])
        th = np.log10([r["theory"] for r in t["data"]])
        g = axes([-0.3, len(Ws) - 0.7], [0, 2], x_length=7.4, y_length=4.4, xlabel=r"estimation window, months",
                 ylabel=r"next-year over fitted variance (log scale)", xticks=list(xs), yticks=[0, 1, 2],
                 xfmt=lambda v: f"{Ws[int(round(v))]}", yfmt=lambda v: f"10^{{{int(v)}}}", font_size=15
                 ).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        ls, ll, lt = (curve(ax, xs, y, c, stroke_width=3) for y, c in ((samp, BAD), (lw, SHRINK_C), (th, HURDLE)))
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=c) for y, c in ((samp, BAD), (lw, SHRINK_C)) for a, b in
                        zip(xs, y)])
        one = DashedLine(ax.c2p(-0.3, 0), ax.c2p(len(Ws) - 0.7, 0), color=GREY_B, stroke_width=1.2)
        leg = legend([(BAD, r"sample covariance, the industries"), (HURDLE, r"normal theory"),
                      (SHRINK_C, r"constant-correlation shrinkage")], font_size=15).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        r0, l0 = t["data"][0]["ratio"], t["lw"][0]["ratio"]
        r2, l2 = t["data"][2]["ratio"], t["lw"][2]["ratio"]
        with self.voiceover(
            f"""Descriptive research-period calibration. <bookmark mark='a'/> Red is the ratio of average next-year realised variance to average sample-covariance forecast; yellow is a Gaussian ratio of expectations. <bookmark mark='b'/> The constant-correlation rule, now assessed with its own fitted covariance, gives ratios {l0:.1f} and {l2:.1f}, versus sample values {r0:.0f} and {r2:.1f}. This differs from Chapter two's common sample-risk proxy. Changing weights and forecast estimators together does not isolate a causal shrinkage effect, and it does not ensure conditional risk forecasts are accurate."""
        ) as vo:
            self.play(FadeIn(g), Create(one), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(ls), Create(lt), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(ll), FadeIn(dots), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def correction(self, t):
        rows = [cmath(r"\tilde\sigma^2", r"=", r"\hat\sigma^2_{\text{in}}\cdot\frac{n(n - 1)}{(n - K + 1)(n - K)}", font_size=32,
                      colors={r"\tilde\sigma^2": GOOD}),
                cmath(r"\text{or}", r"\ ", '\\text{regularisation needs a separate sampling-risk analysis}', font_size=30),
                cmath(r"\text{and}", r"\ ", '\\text{measure realised risk on appropriately timed independent data}', font_size=30)]
        whys = [why(r"for $n>K$: ensemble-unbiased estimate of expected fitted-portfolio population variance; not conditional risk"),
                why('shrinkage changes both the estimator and its sampling law; the sample-GMV correction does not transfer automatically (Chapter 2 uses a common sample-risk proxy)'),
                why(r"independent timed risk measurement also has uncertainty; no sealed result is used here")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "What the bias correction means. <bookmark mark='a'/> Under the fixed IID Gaussian model and n greater than K, multiply the sample-GMV reported variance by the displayed ratio of expectations. Across repeated training samples this estimates the ensemble mean of fitted weights' true variance without bias. It is not a conditional guarantee for this particular fitted portfolio, and not the expected ratio of true to reported variance. <bookmark mark='b'/> Shrinkage changes the estimator and its distribution; the sample-only factor does not automatically transfer. <bookmark mark='c'/> Independent, appropriately timed data can measure risk with its own uncertainty. Dependence, regime changes, selection and execution still need separate treatment."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: beyond normal and stationary", 'useful risk laws beyond fixed IID Gaussian returns require explicit tail, dependence and covariance assumptions; the data comparison identifies no single cause', width=12.4, font_size=18),
            desk_question(r"open: the optimal shrinkage for the portfolio", 'Frobenius covariance loss and portfolio variance need not select the same shrinkage; portfolio-loss results require their own assumptions (Ledoit and Wolf 2017; Bodnar et al. 2018)', width=12.4, font_size=18),
            desk_question('open: $K \\ge T$', 'demeaning makes the sample covariance singular for $K \\ge T$; ridge and factor estimators define different problems with separate assumptions',
                          width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three research directions. <bookmark mark='a'/> Derive useful finite-sample or robust risk laws for explicitly specified heavy-tailed, dependent and changing-covariance models. Broad distribution classes need not admit one universal formula. <bookmark mark='b'/> Optimise the estimator for portfolio loss, rather than assume Frobenius covariance loss has the same optimum; account for tuning and implementation costs. <bookmark mark='c'/> When K is at least T, demeaning makes the sample covariance singular. Ridge, factor and other regularizers define different feasible estimation problems that need their own assumptions and validation."
        ) as vo:
            self.add(cards[0])
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card('IID Gaussian high-dimensional GMV: at $\\gamma = 100/250$, what is the limiting true-to-reported variance ratio? Why is this not a known ratio for one fitted portfolio?')
        with self.voiceover(
            'Pause and predict. In the IID Gaussian high-dimensional GMV model, take gamma equal to one hundred over two hundred and fifty. What is the limiting true-to-reported variance ratio, and why is it not a known ratio for one fitted portfolio?'
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
