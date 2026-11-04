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
        with self.voiceover("For the researcher: Chapter two showed every rule that inverts an estimated covariance "
                            "promising less risk than it delivered. For the sample minimum-variance portfolio, with normal "
                            "returns, the size of that lie can be computed exactly."):
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
                why(r"the sample version, with $T$ normal observations: the sample covariance is a Wishart matrix"),
                why(r"what the optimizer reports about itself, and what it actually has")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The setup. <bookmark mark='a'/> The minimum-variance portfolio of K assets is the inverse covariance times "
            "the vector of ones, normalised; its variance is one over one-transpose Sigma-inverse one. "
            "<bookmark mark='b'/> The sample version uses the sample covariance, which for normal returns is a Wishart "
            "matrix with T minus one degrees of freedom. <bookmark mark='c'/> Two numbers: the variance the optimizer "
            "reports, measured with its own estimate, and the variance it truly has."
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
                why(r"a classical fact about Wishart matrices (Muirhead 1982, Theorem 3.2.12): for any fixed vector $a$, "
                    r"this ratio has a chi-square law, whatever $\Sigma$ is"),
                why(r"take $a = 1$ and $W = n\hat\Sigma$: the reported variance is the true minimum times a chi-square over "
                    r"$n$, which loses $K - 1$ degrees of freedom; $\gamma = K/T$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "In sample first. <bookmark mark='a'/> The variance the optimizer reports is one over the quadratic form of the "
            "ones vector in the inverse estimate. <bookmark mark='b'/> A classical result about Wishart matrices, in Robb "
            "Muirhead's textbook: for any fixed vector, the ratio of the true quadratic form to the estimated one is a "
            "chi-square variable with n minus K plus one degrees of freedom, whatever the true covariance. "
            "<bookmark mark='c'/> So the reported variance is the true minimum times a chi-square over n. Its average is "
            "n minus K plus one over n, and as the number of assets grows with the sample, it tends to one minus gamma. "
            "The optimizer reports less than the minimum possible risk."
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
        rows = [cmath(r"\Sigma = I", r":", r"\hat w \propto W^{-1}1,\quad \sigma^2_{\text{out}} \propto \frac{\|W^{-1}1\|^2}{(1^\top W^{-1}1)^2}",
                      font_size=30, colors={r"\Sigma = I": HURDLE}),
                cmath(r"\frac{\sigma^2_{\text{out}}}{\sigma^2_{\min}}", r"=", r"1 + \frac{\|P_\perp W^{-1}1\|^2}{\|P_1 W^{-1}1\|^2}",
                      font_size=30, colors={r"\frac{\sigma^2_{\text{out}}}{\sigma^2_{\min}}": REAL_C}),
                cmath(r"\frac{\sigma^2_{\text{out}}}{\sigma^2_{\min}}", r"\sim", r"1 + \frac{K - 1}{n - K + 2}\,F_{K-1,\,n-K+2}",
                      font_size=30, colors={r"\frac{\sigma^2_{\text{out}}}{\sigma^2_{\min}}": REAL_C}),
                cmath(r"\mathbb E\Big[\frac{\sigma^2_{\text{out}}}{\sigma^2_{\min}}\Big]", r"=", r"\frac{n - 1}{n - K} \to "
                      r"\frac{1}{1 - \gamma}", font_size=30, colors={r"\mathbb E\Big[\frac{\sigma^2_{\text{out}}}{\sigma^2_{\min}}\Big]": REAL_C})]
        whys = [why(r"the ratio is invariant to linear changes of coordinates, so whiten: take $\Sigma = I$"),
                why(r"split $W^{-1}1$ into its component along $1$ and the rest: the excess risk is the share of the "
                    r"estimate that points away from the true optimum"),
                why(r"by the Bartlett decomposition of $W$ the two pieces are independent chi-squares: an $F$ ratio "
                    r"(Kempf and Memmel 2006)"),
                why(r"its mean: the portfolio's true variance exceeds the minimum by $(K - 1)/(n - K)$")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "Then out of sample. <bookmark mark='a'/> The ratio does not change under linear changes of coordinates, so "
            "whiten: take the true covariance to be the identity. <bookmark mark='b'/> Split the estimated direction into "
            "its component along the true optimum and the rest. The excess risk is the size of the rest relative to the "
            "part that points the right way. <bookmark mark='c'/> By Bartlett's decomposition of the Wishart matrix, the "
            "two pieces are independent chi-squares, so the excess is an F ratio, as Alexander Kempf and Christoph Memmel "
            "showed in 2006. <bookmark mark='d'/> Its average: the true variance exceeds the minimum by K minus one over "
            "n minus K, which tends to one over one minus gamma."
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

    def theorem(self):
        st = VGroup(MathTex(r"\frac{\hat\sigma^2_{\text{in}}}{\sigma^2_{\min}} \xrightarrow{p} 1 - \gamma,\qquad "
                            r"\frac{\sigma^2_{\text{out}}}{\sigma^2_{\min}} \xrightarrow{p} \frac{1}{1 - \gamma},\qquad "
                            r"\frac{\sigma^2_{\text{out}}}{\hat\sigma^2_{\text{in}}} \xrightarrow{p} \frac{1}{(1 - \gamma)^2}",
                            font_size=30),
                    wrapped_label(r"for i.i.d.\ normal returns, $K, T \to \infty$, $K/T \to \gamma < 1$; the same limits hold "
                                  r"for far more general returns by random matrix theory (Bai, Liu and Wong 2009; El Karoui "
                                  r"2010)", 9.6, 20)).arrange(DOWN, buff=0.35)
        card = theorem_card(r"The optimizer's risk illusion", st, r"Kempf and Memmel (2006); El Karoui (2010)", width=11.4,
                            font_size=22)
        with self.voiceover(
            "Stated as a limit. <bookmark mark='a'/> As assets and observations grow together, with ratio gamma, the "
            "reported variance tends to one minus gamma times the minimum, the true variance to the minimum over one minus "
            "gamma, and so the truth exceeds the report by one over one minus gamma, squared. With gamma one half, a "
            "factor of four. <bookmark mark='b'/> Random matrix theory extends the same limits far beyond normal returns."
        ) as vo:
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
        g = axes([0, 0.9], [0, 6], x_length=7.4, y_length=4.4, xlabel=r"$\gamma = K/T$ ($K = 49$)",
                 ylabel=r"variance relative to the true minimum", xticks=[0, 0.3, 0.6, 0.9], yticks=[0, 1, 3, 6],
                 font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        lin = curve(ax, gg, 1 - gg, EST_C, stroke_width=2.5)
        lout = curve(ax, gg, np.minimum(1 / (1 - gg), 6), REAL_C, stroke_width=2.5)
        one = DashedLine(ax.c2p(0, 1), ax.c2p(0.9, 1), color=GREY_B, stroke_width=1.2)
        din = VGroup(*[Dot(ax.c2p(a, t["sims"][str(T)]["in"]), radius=0.06, color=EST_C) for a, T in zip(gam, Ts)])
        dout = VGroup(*[Dot(ax.c2p(a, min(t["sims"][str(T)]["out"], 6)), radius=0.06, color=REAL_C) for a, T in zip(gam, Ts)])
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
        g1 = axes([0, 2], [0, 1], x_length=5.0, y_length=3.4, xlabel=r"reported $\hat\sigma^2_{\text{in}}/\sigma^2_{\min}$",
                  ylabel=r"share", xticks=[0, 1, 2], yticks=[], font_size=14).move_to(LEFT * 3.4 + DOWN * 0.3)
        g2 = axes([0, 6], [0, 1], x_length=5.0, y_length=3.4, xlabel=r"true $\sigma^2_{\text{out}}/\sigma^2_{\min}$",
                  ylabel=r"share", xticks=[0, 1, 3, 6], yticks=[], font_size=14).move_to(RIGHT * 3.2 + DOWN * 0.3)

        def bars(ax, h, x0, x1, col):
            w = (x1 - x0) / len(h)
            m = h.max()
            return VGroup(*[Rectangle(width=ax.c2p(w, 0)[0] - ax.c2p(0, 0)[0] - 0.01,
                                      height=max(ax.c2p(0, v / m)[1] - ax.c2p(0, 0)[1], 0.001), stroke_width=0,
                                      fill_color=col, fill_opacity=0.85).move_to(ax.c2p(x0 + (k + 0.5) * w, 0),
                                                                                 aligned_edge=DOWN)
                            for k, v in enumerate(h) if v > 0])
        b1, b2 = bars(g1.ax, hi, 0, 2, EST_C), bars(g2.ax, ho, 0, 6, REAL_C)
        l1 = DashedLine(g1.ax.c2p(1, 0), g1.ax.c2p(1, 1), color=GREY_B)
        l2 = DashedLine(g2.ax.c2p(1, 0), g2.ax.c2p(1, 1), color=GREY_B)
        title = label(r"$T = 120$ months, $K = 49$: 1{,}000 samples", font_size=20, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "The whole distributions, for ten years of data. <bookmark mark='a'/> Every single sample reports less than "
            "the true minimum: the red histogram lies entirely left of one. <bookmark mark='b'/> And every sample's true "
            "variance lies right of one, by definition of the minimum, with a long right tail: the F distribution's. "
            "The optimizer is always optimistic, never by chance."
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
        g = axes([0, 0.9], [0, 6], x_length=7.4, y_length=4.4, xlabel=r"$\gamma = K/T$", ylabel=r"true variance "
                 r"relative to the minimum", xticks=[0, 0.3, 0.6, 0.9], yticks=[0, 1, 3, 6], font_size=15
                 ).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        lout = curve(ax, gg, np.minimum(1 / (1 - gg), 6), REAL_C, stroke_width=2.5)
        cols = {"sample": BAD, "LW const-corr": SHRINK_C, "nonlinear": GOOD}
        dots = VGroup()
        for k, c in cols.items():
            dots.add(VGroup(*[Dot(ax.c2p(a, min(sh["sims"][T][k]["gmv"], 6)), radius=0.07, color=c) for a, T in zip(gam, Ts)]))
        leg = legend([(REAL_C, r"the theorem: sample covariance"), (BAD, r"sample, simulated"),
                      (SHRINK_C, r"constant-correlation shrinkage"), (GOOD, r"nonlinear shrinkage")], font_size=15
                     ).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        s60 = sh["sims"]["60"]
        with self.voiceover(
            "The theorem is about the sample covariance, and shrinkage escapes it. <bookmark mark='a'/> The teal line is "
            "the limit, and the red dots, Chapter four's simulations of the sample matrix, sit on it. "
            "<bookmark mark='b'/> The shrunk estimators sit far below: at gamma of about point eight, "
            f"{s60['nonlinear']['gmv']:.2f} times the minimum instead of {s60['sample']['gmv']:.1f}. The loss of K minus "
            "one degrees of freedom is the price of estimating every covariance freely; a structured or shrunk estimate "
            "does not pay it in full."
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
            "And on the real industries. <bookmark mark='a'/> With five-year windows, the optimizer reported a volatility "
            f"of {100 * r60['pred_vol']:.1f} percent and had {100 * r60['real_vol']:.1f}: a ratio of variances of "
            f"{r60['ratio']:.0f}, against {r60['theory']:.0f} from the normal theory. With ten years, {r120['ratio']:.1f} "
            f"against {r120['theory']:.1f}. Real returns are worse than the theory, because they are fat-tailed and their "
            "covariance drifts, but the theory gets the shape and most of the size."
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
                 ylabel=r"true over reported variance (log scale)", xticks=list(xs), yticks=[0, 1, 2],
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
            "Does shrinkage cure the illusion? <bookmark mark='a'/> The red line is the sample matrix's ratio of true to "
            "reported variance on the industries, the yellow one the normal theory. <bookmark mark='b'/> Shrink the "
            f"covariance first and the ratio collapses: from {r0:.0f} to {l0:.1f} with five-year windows, from "
            f"{r2:.1f} to {l2:.1f} with ten. A shrunk optimizer still flatters itself a little, but no longer by an order "
            "of magnitude."
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
                cmath(r"\text{or}", r"\ ", r"\text{shrink first: Chapter 4 brings the ratio close to one}", font_size=30),
                cmath(r"\text{and}", r"\ ", r"\text{report risk only from data the weights did not see}", font_size=30)]
        whys = [why(r"an unbiased forecast of the true variance, under normality, from the reported one"),
                why(r"shrinkage reduces the error the optimizer exploits, so its self-report is less wrong (Chapter 2's "
                    r"outlined bars)"),
                why(r"the general cure: a hold-out estimate of risk, which is what the envelope is for")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "What to do with it. <bookmark mark='a'/> Under normality, multiply the reported variance by this factor and "
            "you have an unbiased forecast of the truth. <bookmark mark='b'/> Better, shrink first: a shrunk covariance "
            "gives the optimizer less error to exploit, and its report comes much closer to the truth. "
            "<bookmark mark='c'/> And in general, never let a portfolio grade its own risk: measure it on data the "
            "weights did not see."
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
            desk_question(r"open: beyond normal and stationary", r"exact finite-sample laws for heavy-tailed, dependent "
                          r"returns, where the data show the illusion is larger, are not known", width=12.4, font_size=18),
            desk_question(r"open: the optimal shrinkage for the portfolio", r"shrinkage tuned to the covariance's error is "
                          r"not the shrinkage that minimises the portfolio's true variance; Ledoit and Wolf (2017) and "
                          r"Bodnar, Parolya and Schmid (2018) give partial answers", width=12.4, font_size=18),
            desk_question(r"open: $K > T$", r"when there are more assets than observations the sample matrix is singular; "
                          r"the limits of regularised and factor-based minimum variance there are an active topic",
                          width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> Exact finite-sample laws for fat-tailed, dependent returns, where "
            "the data show the illusion is larger, are not known. <bookmark mark='b'/> The shrinkage that is best for the "
            "covariance is not the shrinkage that is best for the portfolio's true variance; there are partial answers. "
            "<bookmark mark='c'/> And with more assets than observations the sample matrix cannot be inverted at all; "
            "what regularised minimum variance achieves there is still being worked out."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"100 assets and 250 observations. By what factor does the true variance of the sample "
                       r"minimum-variance portfolio exceed what it reports, approximately?")
        with self.voiceover(
            "Pause and predict. A hundred assets and two hundred and fifty observations. By roughly what factor does the "
            "true variance exceed the reported one?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
