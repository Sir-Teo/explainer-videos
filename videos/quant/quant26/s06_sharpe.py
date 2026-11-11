from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant26.common import BAD, BUG, GOOD, HONEST, HURDLE, MKT, PART, RULE, ask, fit_right, illustration, load


class SharpeError(VoiceoverScene):
    def construct(self):
        s = load("sharpe")
        self.card()
        self.spread(s["sim"])
        self.derive()
        self.years(s)
        self.tails(s)
        self.smooth(s["smooth"])
        self.question()

    def card(self):
        c = chapter_card(5, r"The Sharpe ratio's error", r"How long before a Sharpe ratio means anything?", lit=(2002,),
                         part=PART)
        with self.voiceover("Chapter five. The Sharpe ratio is an estimate, and estimates have errors."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def spread(self, sm):
        e = np.asarray(sm["edges"])
        c = (e[:-1] + e[1:]) / 2
        h = np.asarray(sm["hist"])
        g = axes([-1.5, 2.5], [0, h.max() * 1.1], x_length=8.0, y_length=4.2,
                 xlabel=r"estimated Sharpe ratio after five years of monthly returns", ylabel=r"density",
                 xticks=[-1, 0, 0.5, 1, 2], yticks=[], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        ax = g.ax
        w = ax.c2p(e[1], 0)[0] - ax.c2p(e[0], 0)[0]
        bars = VGroup(*[Rectangle(width=w * 0.92, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0,
                                  fill_color=BAD if x < 0 else RULE, fill_opacity=0.8).move_to(
            [ax.c2p(x, 0)[0], (ax.c2p(0, v)[1] + ax.c2p(0, 0)[1]) / 2, 0]) for x, v in zip(c, h) if v > 0])
        true = DashedLine(ax.c2p(0.5, 0), ax.c2p(0.5, h.max() * 1.1), color=HURDLE, stroke_width=2)
        side = VGroup(
            MathTex(r"\text{true}:\ 0.5", font_size=28, color=HURDLE),
            MathTex(rf"\text{{spread}}:\ \pm {sm['sd']:.2f}", font_size=28, color=RULE),
            MathTex(rf"\text{{negative}}:\ {100 * sm['neg']:.0f}\%", font_size=28, color=BAD),
            wrapped_label(r"20,000 simulated five-year histories of a strategy whose true annual Sharpe ratio is 0.5, "
                          r"a respectable long-run equity premium".replace("20,000", "20{,}000"), 3.4, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            f"Take an explicitly simulated strategy with true annual Sharpe ratio one half and independent Gaussian monthly returns. <bookmark mark='a'/> In the saved twenty thousand five-year histories, the estimated ratio has standard deviation {sm['sd']:.2f}. <bookmark mark='b'/> {100*sm['neg']:.1f} percent have a negative estimated ratio. This illustrates low precision; it does not say that every five-year record is incapable of rejecting zero. Serial dependence and a search over strategies would require further treatment."
        ) as vo:
            self.play(FadeIn(g), Create(true), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.01), FadeIn(side[1]),
                      FadeIn(side[3]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"\widehat{SR}", r"=", r"\hat\mu / \hat\sigma", font_size=40, colors={r"\widehat{SR}": RULE}),
                cmath(r"\operatorname{Var}\hat\mu", r"=", r"\sigma^2/T,\qquad \operatorname{Var}\hat\sigma \approx "
                      r"\sigma^2/(2T)", font_size=36, colors={r"\operatorname{Var}\hat\mu": WHITE}),
                cmath(r"\operatorname{Var}\widehat{SR}", r"\approx", r"\frac{1}{T}\Big(1 + \tfrac12 SR^2\Big)",
                      font_size=38, colors={r"\operatorname{Var}\widehat{SR}": HURDLE}),
                cmath(r"\operatorname{Var}\widehat{SR}", r"\approx", r"\frac{1}{T}\Big(1 - \gamma_3\,SR + "
                      r"\tfrac{\gamma_4 - 1}{4}\,SR^2\Big)", font_size=38, colors={r"\operatorname{Var}\widehat{SR}": BUG})]
        whys = [why(r"per period: the estimated mean over the estimated volatility"),
                why(r"for $T$ independent normal returns: the mean's error, and the volatility's, which is "
                    r"independent of it for the normal"),
                why(r"the delta method: $\partial SR/\partial\mu = 1/\sigma$, $\partial SR/\partial\sigma = -SR/\sigma$. "
                    r"The 1 is the mean's error; the $\frac12 SR^2$ the volatility's (Lo 2002). Annualised: multiply by "
                    r"the number of periods a year"),
                why(r"Mertens (2002): skewness $\gamma_3$ and kurtosis $\gamma_4$ ($= 3$ for the normal). Negative "
                    r"skew and fat tails can widen it; this IID formula does not correct serial dependence")]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-0.5, buff=0.3, edge=6.9)
        with self.voiceover(
            "Where the spread comes from. <bookmark mark='a'/> The Sharpe ratio, per period, is the estimated mean "
            "divided by the estimated volatility. <bookmark mark='b'/> For independent normal returns the mean's error "
            "has variance sigma squared over T, and the volatility's about sigma squared over two T. <bookmark mark='c'/> "
            "The delta method combines them: the variance of the estimate is one over T, times one plus half the "
            "Sharpe ratio squared. The one is the mean's error and dominates for ordinary Sharpe ratios; Andrew Lo "
            "published this in 2002. <bookmark mark='d'/> Drop the normal assumption, as Thomas Mertens did the same "
            "year, and skewness and kurtosis enter. Negative skew and fat tails widen the error, so the strategies "
            "that sell insurance, whose returns are exactly like that, are the ones measured worst."
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

    def years(self, s):
        srs, yrs = np.asarray(s["srs"]), np.asarray(s["years_2se"])
        g = axes([0.2, 2.0], [0, 102], x_length=7.4, y_length=4.2, xlabel=r"true annual Sharpe ratio",
                 ylabel=r"years of monthly data before it is two standard errors from zero", xticks=[0.25, 0.5, 1.0, 1.5, 2.0],
                 yticks=[0, 25, 50, 75, 100], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        ax = g.ax
        keep = np.ones(len(yrs), dtype=bool)
        line = curve(ax, srs[keep], yrs[keep], HURDLE, stroke_width=3)
        pts = VGroup()
        for v in (0.5, 1.0, 2.0):
            y = float(np.interp(v, srs, yrs))
            pts.add(VGroup(Dot(ax.c2p(v, y), color=RULE, radius=0.07),
                           MathTex(rf"{y:.0f}\ \text{{yrs}}" if y >= 1.5 else rf"{y:.1f}\ \text{{yrs}}", font_size=22,
                                   color=RULE).next_to(ax.c2p(v, y), UR, buff=0.08)))
        side = VGroup(
            MathTex(r"T_{\text{years}} \approx \frac{4}{SR^2}", font_size=34, color=HURDLE),
            wrapped_label(r"two standard errors means $SR\,\sqrt{T_{\text{years}}} \ge 2$. The market's own premium, "
                          r"about 0.4 to 0.5, needs a working lifetime; a claimed 2 needs one year", 3.4, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "Turn it around: how long must a track record be? <bookmark mark='a'/> For the estimate to be two standard "
            "errors from zero, the Sharpe ratio times the square root of the number of years must exceed two, so the "
            "years needed are about four over the Sharpe ratio squared. <bookmark mark='b'/> A Sharpe ratio of one half "
            "needs sixteen years. One needs four. Two needs one. The equity premium itself, at about point four or "
            "point five, takes a working lifetime to see clearly, which is why Part six needed a century of data for "
            "it."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def tails(self, s):
        m, p = s["mkt"], s["put"]
        rows = VGroup(
            VGroup(label(r"US market, 1926--2020", font_size=24, color=MKT),
                   MathTex(rf"SR = {m['sr']:.2f} \pm {m['se']:.2f}", font_size=30),
                   label(rf"skew {m['skew']:+.2f}, kurtosis {m['kurt']:.1f}: non-normal error {m['se_nn']:.2f}",
                         font_size=18, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            VGroup(label(r"Cboe S\&P 500 PutWrite, 2007--2020", font_size=24, color=BUG),
                   MathTex(rf"SR = {p['sr']:.2f} \pm {p['se']:.2f}\ \to\ \pm {p['se_nn']:.2f}", font_size=30),
                   label(rf"skew {p['skew']:+.2f}, kurtosis {p['kurt']:.1f}: a seller of insurance", font_size=18,
                         color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6).scale(1.35).move_to(UP * 0.4)
        foot = wrapped_label(r"annual Sharpe ratios of monthly excess returns, with the iid and the non-normal standard "
                             r"errors. These are standard errors, not 95\% bounds; independent-return assumptions may fail. The "
                             r"shorter put-writing record has greater estimated uncertainty", 12.0, 18, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            f"Two historical summaries, using the original public data. <bookmark mark='a'/> The US market has {m['years']:.1f} years of monthly observations, Sharpe ratio {m['sr']:.2f}, IID standard error {m['se']:.2f}, and moment-adjusted error {m['se_nn']:.2f}. <bookmark mark='b'/> The put-writing index has {p['months']} months, ratio {p['sr']:.2f}, skewness {p['skew']:.2f} and kurtosis {p['kurt']:.1f}. Its standard error changes from {p['se']:.2f} to {p['se_nn']:.2f}. These are asymptotic estimates under independent-return assumptions. Neither formula handles serial dependence, guarantees tail estimation accuracy or certifies future performance."
        ) as vo:
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.2), FadeIn(foot))
        self.add(illustration(r"Ken French; Cboe PUT index; the House's \texttt{backtest.sharpe\_se}"))
        self.wait(0.4)
        self.clear_scene()

    def smooth(self, sm):
        rows = [cmath(r"r^{\text{reported}}_t", r"=", r"0.5\,r_t + 0.3\,r_{t-1} + 0.2\,r_{t-2}", font_size=38,
                      colors={r"r^{\text{reported}}_t": BUG}),
                cmath(r"SR(q)", r"=", r"\eta(q)\,SR,\qquad \eta(q) = \frac{q}{\sqrt{q + 2\sum_{k=1}^{q-1}(q - k)\rho_k}}",
                      font_size=36, colors={r"SR(q)": HURDLE})]
        whys = [why(r"an illiquid portfolio, marked from stale or appraised prices, reports a smoothed return: today's "
                    r"true return spread over three months (Getmansky, Lo and Makarov 2004)"),
                why(r"Lo (2002), stationary arithmetic sums: nonzero autocorrelations change scaling; positive weighted "
                    r"autocorrelation reduces this ratio relative to naive square-root scaling")]
        step = ladder(self, rows, whys, keep=2, top=3.0, x=-0.5, buff=0.4, edge=6.9)
        bars = [(r"true", sm["true"], GOOD), (r"$\sqrt{12} \times$ monthly", sm["naive"], BUG),
                (r"Lo's $\eta(12) \times$ monthly", sm["lo"], HURDLE)]
        g = VGroup()
        for i, (nm, v, c) in enumerate(bars):
            b = Rectangle(width=v * 3.6, height=0.4, stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([-1.5 + v * 1.8, -1.0 - 0.6 * i, 0])
            g.add(VGroup(label(nm, font_size=19, color=c).next_to([-1.6, -1.0 - 0.6 * i, 0], LEFT, buff=0.15), b,
                         MathTex(f"{v:.2f}", font_size=24).next_to(b, RIGHT, buff=0.15)))
        foot = wrapped_label(rf"annual Sharpe ratio of the reported returns, true value 1. Smoothing hides "
                             rf"{100 * (1 - 0.616):.0f}\% of the volatility and overstates the annual figure by "
                             rf"{100 * sm['overstated']:.0f}\%; Lo found up to 65\% in hedge funds' own reports",
                             12.0, 18, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            f"Smoothing can also distort naive annualisation. <bookmark mark='a'/> This original Gaussian illustration reports a weighted mixture of current and lagged returns, as a simple stale-mark mechanism. <bookmark mark='b'/> For stationary arithmetic-sum moments, the scaling factor depends on all relevant autocorrelations. Positive weighted autocorrelation lowers that factor relative to square-root scaling. This is not an identity for compounded returns. <bookmark mark='c'/> In the saved simulation the naive annual ratio is {sm['naive']:.2f}, the Lo-adjusted ratio {sm['lo']:.2f}, and the original generating ratio {sm['true']:.2f}. The naive ratio exceeds the adjusted one by {100*sm['overstated']:.1f} percent. These results do not prove the same mechanism or magnitude for any particular historical fund."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.2) for b_ in g], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"a manager shows you three years of monthly returns with a Sharpe ratio of 2.0 and a first-order "
                r"autocorrelation of 0.4. What is a fair range for the true annual Sharpe ratio?")
        with self.voiceover(
            "Pause and predict. A manager shows you three years of monthly returns, a Sharpe ratio of two, and a "
            "first-order autocorrelation of point four. What is a fair range for the true annual Sharpe ratio?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
