from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant31.common import BAD, FAC_C, GOOD, HURDLE, PART, SPEC_C, comma, fit_right, load

FCOL = {"size": QC.SPOT, "beta": QC.DELTA, "volatility": QC.LOSS, "momentum": QC.GAIN, "reversal": QC.OPTION}


class Model(VoiceoverScene):
    def construct(self):
        m = load("model")
        self.card()
        self.why_factors()
        self.structure()
        self.exposures(m)
        self.industries()
        self.regression(m)
        self.returns(m)
        self.share(m)
        self.bias(m)
        self.kinds()
        self.vendor()
        self.question()

    def card(self):
        c = chapter_card(2, r"Factor risk models", r"How do you forecast the covariance of three thousand stocks?",
                         part=PART)
        with self.voiceover("Chapter two. Part thirty showed that a sample covariance of many assets is mostly noise. "
                            "The industry's answer, for fifty years, has been the factor risk model."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def why_factors(self):
        N, K = 3000, 60
        full = N * (N + 1) // 2
        fac = K * (K + 1) // 2 + N
        rows = [cmath(r"\Sigma", r"=", r"X F X^\top + \Delta", font_size=42, colors={r"X F X^\top": FAC_C, r"\Delta": SPEC_C}),
                cmath(r"\tfrac{N(N+1)}{2}", r"=", rf"{comma(full)}\ \text{{numbers, for }}N = {comma(N)}", font_size=32),
                cmath(r"\tfrac{K(K+1)}{2} + N", r"=", rf"{comma(fac)}\ \text{{numbers, for }}K = {K}", font_size=32,
                      colors={r"\tfrac{K(K+1)}{2} + N": GOOD})]
        whys = [why(r"returns load on $K$ common factors through exposures $X$ ($N\times K$); $F$ is the factors' "
                    r"covariance; assume factor--residual orthogonality and diagonal residual covariance"),
                why(r"a full covariance matrix of three thousand stocks: more numbers than a decade of daily data can "
                    r"pin down"),
                why(r"a factor model: the factor covariance and one specific variance per stock; the exposures are "
                    r"conditioned on here; estimated betas and volatility still carry uncertainty")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"""The idea in one line. <bookmark mark='a'/> Write returns as exposures times factor returns plus residuals. Assuming factors and residuals are uncorrelated, and residual covariance is diagonal, covariance is X F X transpose plus Delta. <bookmark mark='b'/> A full covariance of three thousand stocks has {full:,} entries. <bookmark mark='c'/> Conditional on sixty factor exposures, the covariance model has {fac:,} parameters. This count excludes uncertainty in X: beta and volatility exposures themselves are estimated."""
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

    def structure(self):
        boxes = VGroup()
        items = [(r"exposures $X_t$", r"each asset's standardised characteristics at the close of day $t$", QC.SPOT),
                 (r"factor returns $f_{t+1}$", r"one cross-sectional regression a day: next day's returns on today's "
                                               r"exposures", FAC_C),
                 (r"factor covariance $F$", r"exponentially weighted, with a half-life of weeks to months", FAC_C),
                 (r"specific variances $\Delta$", r"each asset's residual variance, shrunk toward its peers", SPEC_C),
                 (r"forecast $h^\top\Sigma h$", r"for any portfolio $h$, split into factor and specific risk", HURDLE)]
        for t, d, col in items:
            b = VGroup(label(t, font_size=22, color=col), wrapped_label(d, 3.6, 16, GREY_B)).arrange(DOWN, buff=0.12)
            box = SurroundingRectangle(b, buff=0.18, corner_radius=0.1, color=col, stroke_width=1.5)
            boxes.add(VGroup(box, b))
        top = VGroup(*boxes[:3]).arrange(RIGHT, buff=0.5)
        bot = VGroup(*boxes[3:]).arrange(RIGHT, buff=0.9)
        g = VGroup(top, bot).arrange(DOWN, buff=0.8).move_to(DOWN * 0.1)
        for b in g:
            if b.width > 13.0:
                b.width = 13.0
        arrows = VGroup(Arrow(boxes[0].get_right(), boxes[1].get_left(), buff=0.08, color=GREY_B, stroke_width=3),
                        Arrow(boxes[1].get_right(), boxes[2].get_left(), buff=0.08, color=GREY_B, stroke_width=3),
                        Arrow(boxes[1].get_bottom(), boxes[3].get_top(), buff=0.08, color=GREY_B, stroke_width=3),
                        Arrow(boxes[2].get_bottom(), boxes[4].get_top(), buff=0.08, color=GREY_B, stroke_width=3))
        head = label(r"How a fundamental risk model is built", font_size=30).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The machine, in five parts. <bookmark mark='a'/> Exposures: each asset's characteristics, standardised "
            "across the universe every day. <bookmark mark='b'/> Factor returns: a regression across assets, each day, of "
            "the next day's returns on today's exposures; the coefficients are that day's factor returns. "
            "<bookmark mark='c'/> A covariance of those factor returns, weighted toward the recent past. "
            "<bookmark mark='d'/> Each asset's residual variance, shrunk toward its peers. <bookmark mark='e'/> And for "
            "any portfolio, a risk forecast that splits into a factor part and a specific part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes[0]))
            for k, mk in enumerate(("a", "b", "c", "d", "e")):
                vo.wait_until(mk)
                self.play(FadeIn(boxes[k]), GrowArrow(arrows[k - 1])) if k else self.play(Indicate(boxes[0]))
        self.wait(0.4)
        self.clear_scene()

    def exposures(self, m):
        rows = [(r"size", r"log of the 20-day average dollar volume", FCOL["size"]),
                (r"beta", r"60-day regression on the equal-weighted market", FCOL["beta"]),
                (r"volatility", r"20-day standard deviation of daily returns", FCOL["volatility"]),
                (r"momentum", r"return from 59 to 6 days ago", FCOL["momentum"]),
                (r"reversal", r"return over the last 5 days", FCOL["reversal"])]
        tab = VGroup()
        for j, (nm, d, col) in enumerate(rows):
            tab.add(VGroup(label(nm, font_size=24, color=col).move_to([-4.0, 1.9 - 0.75 * j, 0]),
                           label(d, font_size=20, color=GREY_A).move_to([1.6, 1.9 - 0.75 * j, 0])))
        z = cmath(r"x_{ik}", r"=", r"\operatorname{clip}\Big(\tfrac{c_{ik} - \bar c_k}{s_k},\,-3,\,3\Big)", font_size=30)
        z.to_edge(DOWN, buff=1.3)
        foot = wrapped_label(rf"the House's crypto model: every Binance USDT coin with 60 days of history and enough "
                             rf"volume, a median of {m['median_n']:.0f} coins a day, 2018--2020; plus a market factor "
                             r"with exposure one", 12.0, 16, GREY_A).to_edge(DOWN, buff=0.35)
        head = label(r"Five style factors, and a market", font_size=30).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The House builds one, on the coins of Part twenty-nine. <bookmark mark='a'/> Five style exposures, each "
            "known at the close: size, measured by dollar volume; beta to the market; recent volatility; momentum, "
            "skipping the last week; and the last five days' return, for reversal. Plus a market factor to which every "
            "coin has exposure one. <bookmark mark='b'/> Each characteristic is standardised across the coins that day "
            "and clipped at three standard deviations, so a single wild coin cannot dominate a regression."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(z))
        self.wait(0.4)
        self.clear_scene()

    def industries(self):
        rows = [cmath(r"x_{i,\text{ind}}", r"\in", r"\{0, 1\}\ \text{(or fractions, for conglomerates)}", font_size=32),
                cmath(r"\textstyle\sum_{\text{ind}} x_{i,\text{ind}}", r"=", r"1\ \Rightarrow\ \text{collinear with "
                      r"the market}", font_size=32, colors={r"1\ \Rightarrow\ \text{collinear with the market}": BAD}),
                cmath(r"\textstyle\sum_{\text{ind}} w_{\text{ind}} f_{\text{ind}}", r"=", r"0\quad\text{(a constraint on the "
                      r"regression)}", font_size=32, colors={r"0\quad\text{(a constraint on the regression)}": GOOD})]
        whys = [why(r"an equity model adds dozens of industry exposures, and countries and currencies in a global model"),
                why(r"every stock belongs to exactly one industry, so the industry columns add up to the market column"),
                why(r"the commercial fix: cap-weighted industry returns sum to zero, so the market factor is the market "
                    r"and industries are measured relative to it")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "An equity model has more. <bookmark mark='a'/> Dozens of industry exposures, one for each stock's industry, "
            "and in a global model, countries and currencies. The coins have no industries worth the name, so the "
            "House's model has none. <bookmark mark='b'/> Industries bring a technical problem: every stock is in exactly "
            "one, so the industry columns add up to the market column, and the regression cannot separate them. "
            "<bookmark mark='c'/> The commercial models add a constraint: the cap-weighted industry returns sum to zero, "
            "so the market factor is the market, and each industry is measured against it."
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

    def regression(self, m):
        rows = [cmath(r"r_{i,t+1}", r"=", r"\textstyle\sum_k x_{ik,t}\, f_{k,t+1} + u_{i,t+1}", font_size=36,
                      colors={r"f_{k,t+1}": FAC_C, r"u_{i,t+1}": SPEC_C}),
                cmath(r"\hat f_{t+1}", r"=", r"(X_t^\top W X_t+10^{-6}I)^{-1} X_t^\top W\, r_{t+1}", font_size=36,
                      colors={r"\hat f_{t+1}": FAC_C}),
                cmath(r"\hat f_{k,t+1}", r"=", r"\text{unit-exposure mimicking portfolio in the unregularised, full-rank case}", font_size=26),
                cmath(r"R^2", r"\approx", rf"{m['r2_mean']:.2f}\ \text{{a day, on average}}", font_size=32)]
        whys = [why(r"the model for one day: exposures known at $t$, returns realised at $t+1$"),
                why(r"House weights: square root of average quote volume; a fixed ridge stabilises the normal equations"),
                why(r"Fama and MacBeth's insight: each cross-sectional coefficient is itself a portfolio's return"),
                why(r"the factors explain about a fifth of the cross-section of one day's returns: the rest is specific")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            f"""Factor returns come from one regression a day. <bookmark mark='a'/> Today's exposures explain next day's returns, with residuals defined by that fitted identity. <bookmark mark='b'/> The House uses weights proportional to square root of average quote volume and a ridge of ten to the minus six. Size here is a liquidity proxy, not market capitalisation. <bookmark mark='c'/> Without ridge, and with full rank, each coefficient is a unit-exposure mimicking portfolio return. Ridge perturbs that exact exposure property. <bookmark mark='d'/> The saved mean cross-sectional R squared is {m['r2_mean']:.2f}; it measures a fit, not a future return."""
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def returns(self, m):
        d = np.asarray(m["dates"], float)
        from datetime import datetime
        dates = [datetime.strptime(str(int(v)), '%Y%m%d') for v in d]
        x = np.array([v.year + (v - datetime(v.year, 1, 1)).total_seconds() /
                      (datetime(v.year + 1, 1, 1) - datetime(v.year, 1, 1)).total_seconds() for v in dates])
        cum = 100 * np.asarray(m["cum"], float)
        keys = m["factors"]
        lo = float(np.floor(cum[:, 1:].min() / 50) * 50)
        hi = float(np.ceil(cum[:, 1:].max() / 50) * 50)
        g = axes([x[0], x[-1]], [lo, hi], x_length=7.4, y_length=4.4, xlabel=r"research series, including late-2017 warm-up",
                 ylabel=r"sum of daily factor returns, \%", xticks=[2018, 2019, 2020, 2021], yticks=[lo, 0, hi],
                 xfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        lines = VGroup(*[curve(ax, x, cum[:, i], FCOL[k], stroke_width=3) for i, k in enumerate(keys) if k != "market"])
        leg = legend([(FCOL[k], k) for k in keys if k != "market"], font_size=16).to_edge(RIGHT, buff=0.4).shift(UP * 1.3)
        fit_right(leg)
        fs = m["fstats"]
        stats = VGroup(*[label(rf"{k}: {100 * fs[k]['mean']:+.0f}\%/yr, $t$ = {fs[k]['t']:+.1f}", font_size=15,
                               color=FCOL[k]) for k in keys if k != "market"]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        stats.next_to(leg, DOWN, buff=0.5).align_to(leg, LEFT)
        fit_right(stats)
        v, r = fs["volatility"], fs["reversal"]
        with self.voiceover(
            f"""These are arithmetic sums of the saved daily style-factor returns, including the late twenty-seventeen warm-up. They are not compounded wealth. <bookmark mark='a'/> The volatility factor's annualised arithmetic mean was {100 * v['mean']:.0f} percent; reversal's was {100 * r['mean']:.0f} percent. The displayed t statistics use an independent-day reference, without serial-correlation or selection adjustment. <bookmark mark='b'/> These retrospective means establish no future premium. Risk modelling needs covariance forecasts even for factors with no expected premium. The House's exponentially weighted squares and outer products are uncentred second moments, used as a zero-mean approximation."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            self.play(*[Create(l_) for l_ in lines], run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(stats))
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def share(self, m):
        s = m["fac_share"]
        bar_w = 9.0
        fac = Rectangle(width=bar_w * s, height=0.8, fill_color=FAC_C, fill_opacity=0.8, stroke_width=0)
        spec = Rectangle(width=bar_w * (1 - s), height=0.8, fill_color=SPEC_C, fill_opacity=0.8, stroke_width=0)
        bar = VGroup(fac, spec).arrange(RIGHT, buff=0).move_to(UP * 0.6)
        lf = label(rf"factor risk {100 * s:.0f}\%", font_size=22, color=FAC_C).next_to(fac, UP, buff=0.2)
        ls = label(rf"specific {100 * (1 - s):.0f}\%", font_size=22, color=SPEC_C).next_to(spec, UP, buff=0.2)
        txt = wrapped_label(r"median across dates of each date's median factor fraction of forecast asset variance; "
                            r"a model-dependent summary, distinct from cross-sectional return-fit $R^2$", 11.0, 19, GREY_A).next_to(bar, DOWN, buff=0.7)
        with self.voiceover(
            f"""How much forecast asset variance does this model assign to factors? <bookmark mark='a'/> First take the median fraction across eligible coins each day; then the median across dates. The saved value is {100 * s:.0f} percent. It is a forecast-variance allocation, not realised R squared or a general comparison of coins with stocks. <bookmark mark='b'/> Pooling common risk can reduce estimation demands, but only to the extent that the factors and covariance assumptions describe the book."""
        ) as vo:
            self.play(GrowFromEdge(fac, LEFT), FadeIn(lf))
            vo.wait_until("a")
            self.play(GrowFromEdge(spec, LEFT), FadeIn(ls))
            vo.wait_until("b")
            self.play(FadeIn(txt))
        self.wait(0.4)
        self.clear_scene()

    def bias(self, m):
        rows = [cmath(r"z_t", r"=", r"\frac{h_t^\top r_{t+1}}{\sqrt{h_t^\top \hat\Sigma_t h_t}}", font_size=38),
                cmath(r"b", r"=", r"\operatorname{sd}(z_1, \dots, z_T)", font_size=36, colors={r"b": HURDLE}),
                cmath(r"b", r"\in", r"1 \pm \sqrt{2/T}\quad\text{IID Gaussian reference only}", font_size=32)]
        whys = [why(r"each day's realised return, in units of the volatility the model forecast for it the day before"),
                why(r"Barra's bias statistic: the standard deviation of those standardised returns"),
                why(r"approximate 95\% reference half-width 0.055 at 652 days, assuming independent standard-normal $z_t$")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.3, buff=0.45, edge=6.9)
        names = list(m["bias"])
        hx = [-3.0, 2.2]
        tab = VGroup()
        for j, k in enumerate(names):
            b, se = m["bias"][k]
            col = GOOD if abs(b - 1) <= se else BAD
            tab.add(VGroup(label(k, font_size=20, color=GREY_A).move_to([hx[0], -1.9 - 0.45 * j, 0]),
                           MathTex(rf"{b:.2f}", font_size=28, color=col).move_to([hx[1], -1.9 - 0.45 * j, 0])))
        vf = m["bias"]["volatility factor"][0]
        ew = m["bias"]["equal-weighted coins"][0]
        with self.voiceover(
            f"""Check the scale of the forecasts. <bookmark mark='a'/> Divide each realised portfolio return by its forecast volatility. <bookmark mark='b'/> Their sample standard deviation is the bias statistic. With correct conditional scale and negligible conditional mean, its target is one. <bookmark mark='c'/> Independent Gaussian observations give an approximate ninety-five percent reference half-width of square root of two over T: about five point five percent for these six hundred fifty-two observations. Fat tails, serial dependence and adaptive books change that reference. <bookmark mark='d'/> All four saved statistics lie outside this narrow reference. Equal weights give {ew:.2f}; the volatility-factor book gives {vf:.2f}. These scale discrepancies identify neither a unique cause nor a reliable pass or fail test under the actual data distribution."""
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def kinds(self):
        cards = VGroup(
            desk_question(r"fundamental", r"exposures measured from characteristics (industry, size, value, momentum), "
                          r"factor returns estimated: Barra, Axioma's fundamental models; what the House built",
                          width=12.4, font_size=19),
            desk_question(r"statistical", r"factors and exposures both estimated, by principal components of the returns "
                          r"(Connor and Korajczyk, 1986): no economic labels, quick to adapt", width=12.4, font_size=19),
            desk_question(r"macroeconomic", r"factor returns observed (inflation, rates, oil surprises: Chen, Roll and Ross, "
                          r"1986), exposures estimated by time-series regression", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "There are three kinds of factor model. <bookmark mark='a'/> Fundamental models, like the one we just built, "
            "measure the exposures and estimate the factor returns. <bookmark mark='b'/> Statistical models estimate both "
            "from the returns alone, by principal components, as Connor and Korajczyk did in 1986: no economic labels, "
            "but quick to adapt. <bookmark mark='c'/> Macroeconomic models observe the factor returns, such as surprises "
            "in inflation and interest rates, and estimate each asset's exposures, as Chen, Roll and Ross did. Gregory "
            "Connor's comparison in 1995 found the fundamental kind explained the most."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2)) if k else self.play(Indicate(cards[0]))
        self.wait(0.4)
        self.clear_scene()

    def vendor(self):
        card = firm_card(r"Barra", r"founded by Barr Rosenberg in Berkeley in 1975 to sell factor risk models of US stocks, "
                         r"built on his academic work on extra-market covariance; bought by MSCI in 2004. Its models, and "
                         r"those of Axioma and Northfield, became the common language in which managers report risk",
                         source=r"Rosenberg (1974), JFQA; MSCI's public filings", kind=r"Firm file", width=10.6,
                         font_size=22).move_to(UP * 0.2)
        with self.voiceover(
            "The firm file. Barr Rosenberg founded Barra in Berkeley in 1975 to sell exactly this machine, built on his "
            "academic papers on what he called extra-market covariance; MSCI bought it in 2004. Its models, and those of "
            "its competitors, became the common language in which managers, clients and regulators talk about risk. "
            "That has a cost we will meet in Chapter nine: when everyone measures risk the same way, everyone sees the "
            "same opportunities."
        ):
            self.play(FadeIn(card))
            self.wait(1.0)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a portfolio's bias statistic is 1.30 over two years of daily data. Is the model over- or "
                       r"under-forecasting its risk, and by how much in volatility?")
        with self.voiceover(
            "Pause and predict. A portfolio's bias statistic is one point three over two years of daily data. Is the "
            "model over- or under-forecasting its risk, and by how much?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
