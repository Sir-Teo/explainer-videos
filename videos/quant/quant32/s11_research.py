from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import systematic as SY
from videos.quant.quant32.common import BAD, GOOD, HURDLE, PART, SPY_C, TREND_C, fit_right, load


class Research(VoiceoverScene):
    def construct(self):
        t = load("theory")
        self.card()
        self.setup_()
        self.identity()
        self.mean()
        self.moments()
        self.limit_proof()
        self.theorem()
        self.sims(t)
        self.limit(t)
        self.smile(t)
        self.data(t)
        self.diversify(t)
        self.sign_rule()
        self.filters()
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"Why trend following is long a straddle", r"Can the shape of trend's returns be proved, not "
                          r"just observed?", part=PART)
        with self.voiceover("For the researcher. Chapter two showed a picture and an identity. This chapter turns the "
                            "identity into a theorem: what the trend rule earns, how its returns are shaped, and why."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_(self):
        rows = [cmath(r"r_1, \dots, r_n", r":", r"\text{one block of returns}", font_size=34),
                cmath(r"x_t", r"=", r"\textstyle\sum_{s<t} r_s", font_size=38, colors={r"x_t": TREND_C}),
                cmath(r"P", r"=", r"\textstyle\sum_{t=1}^{n} x_t\, r_t", font_size=38, colors={r"P": GOOD})]
        whys = [why(r"daily returns, standardised so the volatility is one; a block is a month or a quarter"),
                why(r"the linear trend rule: the position on day $t$ is the return so far in the block, so it is long "
                    r"after a rise and short after a fall"),
                why(r"its profit over the block; the next block starts flat")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The setup. <bookmark mark='a'/> One block of n returns, a month or a quarter of days, standardised to unit "
            "volatility. <bookmark mark='b'/> The linear trend rule holds the return so far: long after a rise, short "
            "after a fall, more of each the further the market has gone. <bookmark mark='c'/> Its profit is the sum of "
            "position times return. The sign rule of Chapter one is a cruder cousin; this one can be solved."
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

    def identity(self):
        rows = [cmath(r"P", r"=", r"\textstyle\sum_{s<t} r_s\, r_t", font_size=38),
                cmath(r"S^2", r"=", r"\big(\textstyle\sum_t r_t\big)^2 = \textstyle\sum_t r_t^2 + 2\sum_{s<t} r_s r_t",
                      font_size=34),
                cmath(r"P", r"=", r"\tfrac12\big(S^2 - Q\big),\qquad Q = \textstyle\sum_t r_t^2", font_size=40,
                      colors={r"P": GOOD})]
        whys = [why(r"substitute the position: every earlier return times every later one"),
                why(r"the square of a sum is the squares plus twice the cross products"),
                why(r"exact, for any path: the payoff of a straddle on the block's return, $S^2/2$, financed by half its "
                    r"realised variance $Q/2$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Lemma one, the identity. <bookmark mark='a'/> Substituting the position, the profit is the sum of every "
            "earlier return times every later one. <bookmark mark='b'/> The square of the block's total return is the "
            "sum of squares plus twice those cross products. <bookmark mark='c'/> So the profit is half the squared "
            "block return minus half the realised variance, for any path whatever: a straddle on the block, financed by "
            "the block's own variance. No distribution has been assumed."
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

    def mean(self):
        rows = [cmath(r"\mathbb E\,P", r"=", r"\textstyle\sum_{s<t}\mathbb E[r_s r_t]", font_size=36),
                cmath(r"\mathbb E\,P", r"=", r"\textstyle\sum_{k=1}^{n-1} (n - k)\,\gamma_k + \binom n2 \mu^2", font_size=36,
                      colors={r"\gamma_k": HURDLE}),
                cmath(r"\text{random walk}", r":", r"\gamma_k = 0\ \Rightarrow\ \mathbb E\,P = \binom n2\mu^2", font_size=32)]
        whys = [why(r"take expectations of the identity"),
                why(r"for a stationary series with mean $\mu$ and autocovariances $\gamma_k$: each lag $k$ appears $n - k$ "
                    r"times"),
                why(r"without autocorrelation the rule earns only the drift's square, tiny over a month: trend's profit is "
                    r"the market's autocorrelation, and nothing else")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Lemma two, the mean. <bookmark mark='a'/> Take expectations. <bookmark mark='b'/> For a stationary series, "
            "each autocovariance at lag k appears n minus k times, plus a term in the squared drift. "
            "<bookmark mark='c'/> For a random walk the autocovariances are zero, and the rule earns only the drift "
            "squared, which over a month is negligible. Trend following's expected profit is the market's "
            "autocorrelation, weighted by lag, and nothing else. The skew, as we shall see, is free."
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

    def moments(self):
        rows = [cmath(r"Y", r"=", r"\textstyle\sum_{s<t} z_s z_t,\quad z \overset{\text{iid}}{\sim} N(0, 1)", font_size=34),
                cmath(r"\mathbb E\,Y^2", r"=", r"\binom n2 = \tfrac{n(n-1)}{2}", font_size=36),
                cmath(r"\mathbb E\,Y^3", r"=", r"3!\,\binom n3 = n(n-1)(n-2)", font_size=36, colors={r"\mathbb E\,Y^3": GOOD})]
        whys = [why(r"under i.i.d. normal returns, $P = \sigma^2 Y$ exactly"),
                why(r"a product of two pair-sums has non-zero mean only when the pairs are the same pair"),
                why(r"three pairs have non-zero mean only if each index appears exactly twice: the three sides of a "
                    r"triangle $\{a, b, c\}$, chosen in any of $3!$ orders")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Lemma three, the moments, for independent normal returns. <bookmark mark='a'/> The profit is sigma squared "
            "times a sum over pairs of standard normals. <bookmark mark='b'/> Its second moment: the product of two "
            "pair-sums has a non-zero mean only when the two pairs are the same, so n choose two. "
            "<bookmark mark='c'/> Its third moment: three pairs have a non-zero mean only when every index appears "
            "exactly twice, which happens exactly when the pairs are the three sides of a triangle. There are n choose "
            "three triangles and three factorial ways to pick their sides in order."
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


    def limit_proof(self):
        rows = [cmath(r"\frac{S}{\sigma\sqrt n}", r"\Rightarrow", r"Z \sim N(0, 1)", font_size=36),
                cmath(r"\frac{Q}{n\sigma^2}", r"\xrightarrow{p}", r"1", font_size=36),
                cmath(r"\frac{P}{n\sigma^2}", r"=", r"\tfrac12\Big(\frac{S^2}{n\sigma^2} - \frac{Q}{n\sigma^2}\Big)\ "
                      r"\Rightarrow\ \tfrac12(Z^2 - 1)", font_size=32, colors={r"\tfrac12(Z^2 - 1)": GOOD})]
        whys = [why(r"the central limit theorem, for the block's total return"),
                why(r"the law of large numbers, for its realised variance"),
                why(r"Slutsky's theorem, applied to the identity: the limit law of the profit, a shifted chi-square, needs "
                    r"only finite variance, not normality")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Lemma four, the limit, which needs much less than normality. <bookmark mark='a'/> By the central limit "
            "theorem, the block's return over its standard deviation tends to a standard normal. <bookmark mark='b'/> By "
            "the law of large numbers, the realised variance over its expectation tends to one. <bookmark mark='c'/> Put "
            "both into the identity, and by Slutsky's theorem the scaled profit tends to half of Z squared minus one: "
            "the same shifted chi-square, for any independent returns with finite variance."
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

    def theorem(self):
        st = VGroup(MathTex(r"P = \tfrac12\big(S^2 - Q\big),\qquad \mathbb E\,P = \textstyle\sum_{k}(n - k)\gamma_k + "
                            r"\binom n2\mu^2", font_size=30),
                    MathTex(r"\operatorname{skew}(P) = \frac{2^{3/2}(n - 2)}{\sqrt{n(n - 1)}}\ \xrightarrow[n\to\infty]{}\ "
                            r"2\sqrt2,\qquad \Pr(P > 0) \to \Pr(|Z| > 1) = 31.7\%", font_size=28),
                    wrapped_label(r"the identity holds for every path; the mean for stationary returns; the skewness and "
                                  r"the limit for i.i.d. normal returns, where $P/(n\sigma^2) \to \frac12(Z^2 - 1)$, a "
                                  r"shifted chi-square with one degree of freedom", 9.6, 20)).arrange(DOWN, buff=0.35)
        card = theorem_card(r"The linear trend rule", st, r"after Potters and Bouchaud (2005); Fung and Hsieh (2001)",
                            width=11.6, font_size=22)
        with self.voiceover(
            "The theorem. <bookmark mark='a'/> The profit is a straddle minus realised variance; its mean is the "
            "lag-weighted autocovariance. <bookmark mark='b'/> Under independent normal returns its skewness is two to "
            "the three halves times n minus two over the root of n times n minus one, rising from zero at two days to "
            "two root two. In the limit the profit is a shifted chi-square with one degree of freedom, so it is positive "
            "only when the block's move exceeds one standard deviation: about thirty-two percent of the time. Many "
            "small losses, a few large gains, by construction, with no autocorrelation needed at all."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(st[1], color=HURDLE, scale_factor=1.03))
        self.wait(0.5)
        self.clear_scene()

    def sims(self, t):
        rows = t["sims"]
        hx = [-4.6, -2.4, -0.2, 2.0, 4.4]
        head = VGroup(label(r"$n$", font_size=18, color=GREY_B), label(r"skewness, simulated", font_size=18, color=TREND_C),
                      label(r"theorem", font_size=18, color=GOOD), label(r"share of blocks won", font_size=18,
                                                                         color=TREND_C),
                      label(r"identity error", font_size=18, color=GREY_B))
        tab = VGroup(head)
        for r in rows:
            if r["n"] not in (2, 3, 5, 10, 21, 63, 252):
                continue
            tab.add(VGroup(MathTex(str(r["n"]), font_size=24), MathTex(f"{r['skew']:.2f}", font_size=24),
                           MathTex(f"{r['theory']:.2f}", font_size=24), MathTex(rf"{100 * r['win']:.1f}\%", font_size=24),
                           MathTex(rf"{r['identity_err']:.0e}".replace("e-", r"\times 10^{-") + "}", font_size=22)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.5 - 0.6 * j, 0])
        foot = wrapped_label(r"i.i.d. standard normal returns, about 400{,}000 days for each $n$; the identity checked "
                             r"block by block in floating point", 11.4, 16, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Checked by simulation. <bookmark mark='a'/> For blocks from two days to a year, the simulated skewness "
            "follows the theorem: zero at two, above two by ten, approaching two root two. <bookmark mark='b'/> The share "
            "of blocks that make money falls from a half toward thirty-two percent. And the identity holds to the last "
            "bits of floating point."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_[:3])) for r_ in tab[1:]], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_[3:])) for r_ in tab[1:]], lag_ratio=0.15))
        self.wait(0.4)
        self.clear_scene()

    def limit(self, t):
        g = axes([-1, 6], [0, 1.0], x_length=7.0, y_length=4.0, xlabel=r"$P/(n\sigma^2)$, the block's profit",
                 ylabel=r"density", xticks=[0, 2, 4, 6], yticks=[], font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        xs = np.linspace(-0.49, 6, 300)
        dens = np.array([1 / math.sqrt(2 * math.pi * (2 * u + 1)) * math.exp(-(2 * u + 1) / 2) * 2 for u in xs])
        c = curve(ax, xs, np.minimum(dens, 1.0), TREND_C, stroke_width=3)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 1.0), color=GREY_C, stroke_width=1.5)
        def dens_f(u):
            return 2 / math.sqrt(2 * math.pi * (2 * u + 1)) * math.exp(-(2 * u + 1) / 2)

        def area(a_, b_, col, op):
            us = np.linspace(a_, b_, 120)
            pts = [ax.c2p(a_, 0)] + [ax.c2p(u, min(1.0, dens_f(u))) for u in us] + [ax.c2p(b_, 0)]
            return Polygon(*pts, color=col, fill_opacity=op, stroke_width=0)
        lo = area(-0.49, 0, BAD, 0.4)
        hi = area(0, 6, GOOD, 0.3)
        txt = VGroup(label(r"68\% of blocks lose, never more than $\frac12$", font_size=17, color=BAD),
                     label(r"32\% win, without limit", font_size=17, color=GOOD)).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.15)
        txt.to_edge(RIGHT, buff=0.4).shift(UP * 1.0)
        fit_right(txt)
        with self.voiceover(
            "The limit law, drawn. <bookmark mark='a'/> Half of Z squared minus one: the loss is bounded, never more "
            "than half the block's variance, and it happens in about sixty-eight percent of blocks. "
            "<bookmark mark='b'/> The gains are unbounded and rare. That is the payoff of a bought straddle, and the "
            "experience of a trend follower: the premium paid quietly, month after month, and the occasional large win. Marc "
            "Potters and Jean-Philippe Bouchaud put it in a title in 2005: trend followers lose more often than they "
            "gain."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(Create(c), FadeIn(lo))
            vo.wait_until("b")
            self.play(FadeIn(hi), FadeIn(txt))
        self.wait(0.4)
        self.clear_scene()

    def smile(self, t):
        S, Q, P = (np.asarray(t["spy"][k], float) for k in ("S", "Q", "P"))
        lim = float(np.ceil(np.abs(S).max()))
        top = float(np.ceil(P.max() / 10) * 10)
        bot = float(np.floor(P.min() / 10) * 10)
        g = axes([-lim, lim], [bot, top], x_length=6.6, y_length=4.4, xlabel=r"the block's return $S$ (standardised)",
                 ylabel=r"the linear rule's profit $P$", xticks=[-lim / 2, 0, lim / 2], yticks=[bot, 0, top],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 2.0 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=SPY_C, fill_opacity=0.85) for a, b in zip(S, P)])
        qbar = float(np.mean(Q))
        xs = np.linspace(-lim, lim, 100)
        par = curve(ax, xs, np.clip(0.5 * (xs ** 2 - qbar), bot, top), GOOD, stroke_width=3)
        txt = wrapped_label(rf"SPY, 63-day blocks, 2006--2020, returns over their prior-day volatility forecast; the curve "
                            rf"$\frac12(S^2 - \bar Q)$ with the average realised variance $\bar Q = {qbar:.0f}$; each dot "
                            r"lies exactly on its own parabola $\frac12(S^2 - Q)$", 3.8, 16,
                            GREY_A).to_edge(RIGHT, buff=0.4).shift(UP * 0.4)
        fit_right(txt)
        with self.voiceover(
            "Here is the smile without noise. <bookmark mark='a'/> For American stocks, each dot is a quarter of days: "
            "the block's standardised return across, the linear rule's profit up. <bookmark mark='b'/> The curve is half "
            "of S squared minus the average realised variance. Every dot lies exactly on its own parabola, shifted by "
            "its own realised variance. The smile against the market that Part twenty-four found in AQR's data is this "
            "parabola, blurred by holding many markets at once."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.03))
            vo.wait_until("b")
            self.play(Create(par), FadeIn(txt))
        self.wait(0.4)
        self.clear_scene()

    def data(self, t):
        rows = t["data"]
        hx = [-4.8, -2.6, -0.6, 1.4, 3.4, 5.4]
        head = VGroup(label(r"block", font_size=17, color=GREY_B), label(r"skewness, 23 funds", font_size=17,
                                                                         color=TREND_C),
                      label(r"theorem", font_size=17, color=GOOD), label(r"share won", font_size=17, color=TREND_C),
                      label(r"limit", font_size=17, color=GOOD), label(r"mean vs autocov.", font_size=17, color=HURDLE))
        tab = VGroup(head)
        for r in rows:
            tab.add(VGroup(MathTex(rf"{r['n']}\ \text{{days}}", font_size=24), MathTex(f"{r['skew']:.2f}", font_size=24),
                           MathTex(f"{r['theory']:.2f}", font_size=24), MathTex(rf"{100 * r['win']:.1f}\%", font_size=24),
                           MathTex(r"31.7\%", font_size=24), MathTex(f"{r['corr_mean_pred']:.2f}", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.85 * j, 0])
        foot = wrapped_label(r"every fund's daily excess returns over their prior-day EWMA volatility, 2006--2020, pooled "
                             r"blocks; the last column: the correlation across the 23 funds of each fund's average block "
                             r"profit with $\sum_k (n - k)\hat\gamma_k$ from its own autocovariances", 11.6, 15,
                             GREY_A).to_edge(DOWN, buff=0.35)
        r21, r63 = rows
        with self.voiceover(
            "And the twenty-three funds. <bookmark mark='a'/> Pooling every fund's blocks, the skewness is "
            f"{r21['skew']:.2f} for monthly blocks and {r63['skew']:.2f} for quarterly ones, against {r21['theory']:.2f} "
            "and "
            f"{r63['theory']:.2f}; real returns have fat tails, which make a sample skewness noisy, and both are large "
            f"and positive. The share of blocks won, {100 * r21['win']:.0f} and {100 * r63['win']:.0f} percent, sits "
            "near the limit of thirty-two. <bookmark mark='b'/> And the mean: across funds, each one's average profit "
            f"correlates {r21['corr_mean_pred']:.2f} and {r63['corr_mean_pred']:.2f} with the prediction from its own "
            "autocovariances. The funds that trended were the funds whose returns were autocorrelated, as Lemma two "
            "requires."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_[:5])) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_[5]) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def diversify(self, t):
        n_eff = 23
        sk = SY.trend_skew_theory(21)
        skn = sk / math.sqrt(n_eff)
        rows = [cmath(r"\operatorname{skew}\big(\textstyle\sum_{i=1}^{N} P_i\big)", r"=", r"\frac{\operatorname{skew}(P)}"
                      r"{\sqrt N}\quad\text{(independent, equal risk)}", font_size=32),
                cmath(r"N = 23", r":", rf"{sk:.2f}/\sqrt{{23}} = {sk / math.sqrt(n_eff):.2f}", font_size=34),
                cmath(r"\text{the TSMOM book, monthly}", r":", rf"{t['tsmom_monthly_skew']:.2f}", font_size=34,
                      colors={r"\text{the TSMOM book, monthly}": TREND_C})]
        whys = [why(r"the third cumulant of a sum of independent variables adds, the variance adds too: skewness falls "
                    r"like one over the square root of the number of markets"),
                why(r"for monthly blocks, the theorem's skewness spread over 23 independent markets"),
                why(r"the registered book: sign instead of linear, a year's lookback, correlated markets, and still "
                    r"positively skewed")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Why, then, is the registered book's skewness so much smaller? <bookmark mark='a'/> Diversification. The "
            "third cumulants of independent profits add, and so do their variances, so a book of N equal, independent "
            "markets has a skewness one over root N as large. <bookmark mark='b'/> For monthly blocks over twenty-three "
            f"markets that is {skn:.2f}. <bookmark mark='c'/> The registered book, with the sign rule "
            f"and a year's lookback, had a monthly skewness of {t['tsmom_monthly_skew']:.2f}: smaller, and still "
            "positive. Breadth buys Sharpe ratio and sells skewness."
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


    def sign_rule(self):
        rows = [cmath(r"x_t^{\text{sign}}", r"=", r"\operatorname{sign}\big(\textstyle\sum_{s<t} r_s\big)", font_size=36,
                      colors={r"x_t^{\text{sign}}": TREND_C}),
                cmath(r"P^{\text{sign}}", r"=", r"\textstyle\sum_t \operatorname{sign}(X_{t-1})\,r_t\ \approx\ |S| - "
                      r"\text{(the crossings' cost)}", font_size=32),
                cmath(r"\text{both}", r":", r"\text{convex in the block's move: long gamma}", font_size=32,
                      colors={r"\text{both}": GOOD})]
        whys = [why(r"the rule of Chapter 1 takes only the direction of the trend, not its size"),
                why(r"its profit is the absolute value of the move, less what it loses each time the running return "
                    r"crosses zero and the position flips: a lookback straddle, in Fung and Hsieh's sense"),
                why(r"the linear rule is a straddle in $S^2$, the sign rule one in $|S|$: the identity's shape survives the "
                    r"change of rule, its exact constants do not")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "And the sign rule of Chapter one? <bookmark mark='a'/> It takes only the trend's direction. "
            "<bookmark mark='b'/> Its profit is roughly the absolute size of the move, less a cost each time the "
            "running return crosses zero and the position flips: Fung and Hsieh's lookback straddle. "
            "<bookmark mark='c'/> One rule is a straddle in the square of the move, the other in its absolute value. "
            "Both are convex, both are long gamma, and the theorem's shape survives the change of rule even though its "
            "constants do not."
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

    def filters(self):
        rows = [cmath(r"P_w", r"=", r"\textstyle\sum_{s<t} w_{t-s}\, r_s r_t", font_size=36),
                cmath(r"\mathbb E\,P_w", r"=", r"\textstyle\sum_k w_k (n - k)\gamma_k", font_size=36),
                cmath(r"w^*", r"\propto", r"\Gamma^{-1}\gamma\quad\text{(a matched filter, to first order)}", font_size=34,
                      colors={r"w^*": GOOD})]
        whys = [why(r"any linear trend filter, such as a moving average or an exponential one, weights past returns by "
                    r"their lag"),
                why(r"its expected profit is the filter's inner product with the autocovariances"),
                why(r"maximising the mean per unit of risk, with $\Gamma$ the autocovariance matrix of the lagged returns, "
                    r"picks the filter matched to the autocovariances: the Wiener--Kolmogorov predictor")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A generalisation. <bookmark mark='a'/> Any linear trend filter weights each past return by its lag: a "
            "moving average, an exponential average, a breakout. <bookmark mark='b'/> Its expected profit is the "
            "filter's inner product with the autocovariances. <bookmark mark='c'/> So the best filter, per unit of risk, "
            "is the one matched to the market's own autocovariance structure. Under stationarity this has a known "
            "answer; the hard part is that the autocovariances move."
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
            desk_question(r"open: non-stationary trends", r"autocovariances that change with regimes, crowding and policy "
                          r"make the matched filter a moving target; the optimal adaptive filter, with its estimation "
                          r"error, is not known", width=12.4, font_size=18),
            desk_question(r"open: trend with costs", r"the linear rule trades every day; the optimal no-trade band for a "
                          r"long-straddle strategy, and its effect on skewness, has no closed form", width=12.4,
                          font_size=18),
            desk_question(r"open: who supplies the autocorrelation?", r"slow-moving capital, central-bank smoothing, "
                          r"hedgers and under-reaction all predict it; as trend capital grows, its own trading may erase "
                          r"the effect it harvests", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> Autocovariances change with regimes, crowding and policy; the "
            "best adaptive filter, allowing for its own estimation error, is not known. <bookmark mark='b'/> The linear "
            "rule trades every day; the optimal no-trade band for a long-straddle strategy, and what it does to the "
            "skewness, has no closed form. <bookmark mark='c'/> And who supplies the autocorrelation: slow-moving "
            "capital, central banks smoothing rates, hedgers, investors who under-react? As trend capital grows, its own "
            "trading may erase the effect it harvests."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"returns are i.i.d. normal. Over a 63-day block, what is the expected profit of the linear rule, "
                       r"and its skewness?")
        with self.voiceover(
            "Pause and predict. Returns are independent and normal. Over a sixty-three-day block, what is the linear "
            "rule's expected profit, and what is its skewness?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
