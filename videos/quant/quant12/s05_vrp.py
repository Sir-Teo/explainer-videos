from __future__ import annotations

from datetime import date

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, load, real_data


def _t(s):
    if isinstance(s, str):
        d = date.fromisoformat(s)
    else:
        s = int(s)
        d = date(s // 10000, (s // 100) % 100, s % 100)
    return d.year + (d.timetuple().tm_yday - 1) / 365


def _nice(day):
    d = date.fromisoformat(day)
    return f"{d.day} {d.strftime('%B')} {d.year}"


class VRP(VoiceoverScene):
    def construct(self):
        p = load("vrp_pnl")
        x = load("spx_vrp")
        self.card()
        self.series(p)
        self.derive()
        self.ledger(p)
        self.predict(p)
        self.spx(x)

    def card(self):
        c = chapter_card(12, r"The variance risk premium, measured", r"Why is implied above realized on average?",
                         part=PART)
        with self.voiceover("Chapter twelve. The variance risk premium, measured."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def series(self, p):
        t = np.array([_t(d) for d in p["days"]])
        kv, rv = np.sqrt(np.asarray(p["kvar"])), np.sqrt(np.asarray(p["rv"]))
        n = len(t)
        g = axes([2021.2, 2026], [0.2, 1.4], x_length=8.0, y_length=4.2, ylabel=r"30-day bitcoin volatility",
                 xticks=[2022, 2023, 2024, 2025], xfmt=lambda u: f"{u:.0f}", yticks=[0.4, 0.8, 1.2],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16).to_edge(LEFT, buff=0.5).shift(DOWN * 0.1)
        ax = g.ax
        tr = ValueTracker(2)

        def upto(y, col):
            i = int(max(tr.get_value(), 2))
            return curve(ax, t[:i], np.clip(y[:i], 0.2, 1.4), col, stroke_width=2.5)
        ck = always_redraw(lambda: upto(kv, IV))
        cr = always_redraw(lambda: upto(rv, RV))
        rm, rt = np.asarray(p["run_mean"]), np.asarray(p["run_t"])

        def at(arr):
            v = float(arr[int(min(max(tr.get_value(), 1), n) - 1)])
            return v if np.isfinite(v) else 0.0
        ro = VGroup(readout(r"\text{weeks} =", lambda: min(tr.get_value(), n), digits=0, font_size=28, color=GREY_A),
                    readout(r"\text{mean } (K_{\text{var}} - RV) =", lambda: at(rm), digits=3, font_size=28, color=IV),
                    readout(r"t_{\text{NW}} =", lambda: at(rt), digits=1, font_size=28, color=OPT)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(UP * 1.0)
        leg = legend([(IV, r"variance-swap rate, each Wednesday's surface"), (RV, r"realized over the next 30 days")],
                     font_size=17).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = label(rf"implied {100 * p['implied_mean']:.0f}\%, realized {100 * p['realized_mean']:.0f}\% on average; "
                     rf"premium positive in {100 * p['share_pos']:.0f}\% of {n} weeks", font_size=20,
                     color=GREY_A).to_edge(DOWN, buff=0.3)
        src = real_data(r"Deribit surfaces, April 2021 -- November 2025; Binance BTCUSDT hourly", corner=UR)
        im, re_, sp, tt = 100 * p["implied_mean"], 100 * p["realized_mean"], 100 * p["share_pos"], p["t"]
        with self.voiceover(
            "The desk question: why is implied above realized on average? Every Wednesday since April 2021, the House "
            "read the thirty-day variance-swap rate off that morning's surface, in orange, and thirty days later "
            "measured what Bitcoin realized, in teal. <bookmark mark='a'/> Watch the averages accumulate: the 2021 "
            "bull market, the crashes of 2022, the quiet of 2023, the ETF rally. "
            f"<bookmark mark='b'/> In the end: implied {im:.0f} percent on average, realized {re_:.0f}. The premium "
            f"was positive in {sp:.0f} percent of weeks, and its Newey-West t-statistic is {tt:.1f}, after allowing "
            "for the four-week overlap of consecutive thirty-day windows."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg), FadeIn(ro))
            self.add(ck, cr)
            vo.wait_until("a")
            self.play(tr.animate.set_value(n), run_time=12, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(side))
        for m_ in (ck, cr, *[r_.num for r_ in ro]):
            m_.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"\mathbb{E}^Q[X]", r"=", r"\frac{\mathbb{E}^P[mX]}{\mathbb{E}^P[m]}", font_size=40,
                      colors={r"\mathbb{E}^Q[X]": QC.Q}),
                cmath(r"\mathbb{E}^Q[RV] - \mathbb{E}^P[RV]", r"=", r"\frac{\text{cov}^P(m, RV)}{\mathbb{E}^P[m]}", font_size=38),
                cmath(r"\text{cov}^P(m, RV) > 0", r"\Rightarrow", r"\text{VRP} > 0", font_size=38, colors={r"\text{VRP} > 0": IV}),
                cmath(r"\hat V", r"=", r"\hat\gamma_0 + 2\sum_{L=1}^{4}\Big(1 - \frac{L}{5}\Big)\hat\gamma_L", font_size=38,
                      colors={r"\hat V": OPT}),
                cmath(r"r_{t \to t+30}", r"=", r"\alpha + \beta\,\big(K_{\text{var},t} - RV_{t-30 \to t}\big) + \varepsilon",
                      font_size=36, colors={r"r_{t \to t+30}": SPOT})]
        whys = [why(r"Part 9: risk-neutral prices are real-world expectations weighted by the discount factor $m$"),
                why(r"expand: the gap between the two expectations is a covariance"),
                why(r"variance is high exactly when marginal utility is high (bad times): buyers pay for insurance "
                    r"(Carr and Wu 2009)"),
                why(r"Newey--West with four lags: weekly samples of 30-day windows overlap by about four"),
                why(r"Bollerslev, Tauchen and Zhou (2009): the ex-ante premium, implied minus trailing realized, predicts "
                    r"S\&P 500 returns at quarterly horizons")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.6, buff=0.72, edge=6.9)
        with self.voiceover(
            "Why a premium at all? A risk-neutral expectation is a real-world one weighted by the discount factor m. "
            "<bookmark mark='a'/> So the gap between the two expectations of variance is a covariance between m and "
            "variance. <bookmark mark='b'/> Variance is highest when markets fall, exactly when wealth is worth most: "
            "the covariance is positive, and variance is insurance. Carr and Wu measured the premium in 2009. "
            "<bookmark mark='c'/> Overlapping windows need Newey and West's estimator. <bookmark mark='d'/> And "
            "Bollerslev, Tauchen and Zhou found that the premium measured in advance predicts S&P 500 returns a "
            "quarter ahead. We will test that on Bitcoin."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def ledger(self, p):
        t = np.array([_t(d) for d in p["days"]])
        pnl, cum, dd = np.asarray(p["pnl"]), np.asarray(p["cum"]), np.asarray(p["dd"])
        g = axes([2021.2, 2026], [-1.2, 1.0], x_length=8.4, y_length=2.4, ylabel=r"short variance swap, P\&L per week "
                 r"(variance units)", xticks=[], yticks=[-1, 0, 1], font_size=15).to_edge(UP, buff=0.5)
        bars = VGroup(*[Line(g.ax.c2p(a, 0), g.ax.c2p(a, float(np.clip(b, -1.2, 1.0))), color=RV if b > 0 else BAD,
                             stroke_width=2) for a, b in zip(t, pnl)])
        hi = float(cum.max()) * 1.1
        g2 = axes([2021.2, 2026], [float(min(dd.min(), 0)) - 0.5, hi], x_length=8.4, y_length=2.4,
                  ylabel=r"cumulative, and its drawdown", xticks=[2022, 2023, 2024, 2025], xfmt=lambda u: f"{u:.0f}",
                  yticks=[0, round(hi, 0)], font_size=15).next_to(g, DOWN, buff=0.45)
        cl = curve(g2.ax, t, cum, IV, stroke_width=3)
        ddb = band(g2.ax, t, cum + dd, cum, BAD, 0.3)
        wi = int(np.argmin(pnl))
        flag = VGroup(glow_dot(g.ax.c2p(t[wi], float(np.clip(pnl[wi], -1.2, 1))), color=BAD, radius=0.08),
                      label(rf"worst: the month from {_nice(p['worst_day'])}", font_size=17, color=BAD).next_to(
                          g.ax.c2p(t[wi], -1.1), RIGHT, buff=0.15))
        side = label(rf"skewness of the weekly P\&L {p['skew']:.2f}; best {p['best']:+.2f}, worst {p['worst']:+.2f}",
                     font_size=20, color=GREY_A).to_edge(DOWN, buff=0.3)
        src = real_data(r"each week: sell the 30-day variance swap at the strip's price, receive realized variance", corner=DR)
        sk, w, b = p["skew"], p["worst"], p["best"]
        assert p["worst_day"] == "2021-05-12", p["worst_day"]  # the narration names this week
        sp = 100 * p["share_pos"]
        with self.voiceover(
            "Now look at it from the seller's side: the insurer. Each week, sell the thirty-day variance swap at the "
            "strip's price and pay out what Bitcoin realizes. Most weeks are small gains, in green. "
            f"<bookmark mark='a'/> And a few are not. The worst month was the one that began on the twelfth of May 2021, the week before "
            f"Bitcoin's May 2021 crash: a loss of {w:.2f} in variance units, larger than the best gain of {b:.2f}. The "
            f"skewness of the weekly profits is {sk:.2f}. <bookmark mark='b'/> The cumulative line climbs, with the "
            "drawdowns shaded under it. Pause and predict: a strategy that wins "
            f"{sp:.0f} percent of weeks: is it a good one? Look at the other weeks first. Part eleven's crisis file "
            "shows what this left tail looks like when a fund adds leverage."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), LaggedStart(*[Create(x) for x in bars], lag_ratio=0.005, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(flag), FadeIn(side))
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(cl), FadeIn(ddb), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def predict(self, p):
        b, bl = p["btz"], p["btz_late"]
        by = p["by_year"]
        rows = VGroup(label(r"year \quad implied \quad realized \quad premium $> 0$", font_size=22, color=GREY_A))
        for y in sorted(by):
            r = by[y]
            rows.add(label(rf"{y} \quad {100 * r['implied']:.0f}\% \quad {100 * r['realized']:.0f}\% \quad "
                           rf"{100 * r['positive']:.0f}\% of {r['n']} weeks", font_size=22))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(LEFT, buff=0.8).shift(UP * 0.8)
        reg = VGroup(
            label(r"does the premium predict bitcoin's next 30 days? (descriptive; no strategy is registered)", font_size=21,
                  color=GREY_A),
            MathTex(rf"2021\text{{--}}2025:\ \beta = {b['slope']:+.3f},\ t_{{NW}} = {b['t']:+.2f},\ R^2 = {b['r2']:.3f}",
                    font_size=30, color=SPOT),
            MathTex(rf"2024\text{{--}}2025:\ \beta = {bl['slope']:+.3f},\ t_{{NW}} = {bl['t']:+.2f},\ R^2 = {bl['r2']:.3f}",
                    font_size=30, color=SPOT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.6)
        src = real_data(r"weekly Deribit surfaces and Binance hourly prices", corner=UR)
        sig = abs(b["t"]) >= 2
        branch = ("It is significant, which would be worth a registered test before anyone traded on it. " if sig else
                  "Nothing: the slope is indistinguishable from zero, in the full sample and in the last two years. "
                  "Whatever the variance premium pays for in Bitcoin, it does not forecast Bitcoin's next month. ")
        t1, t2 = b["t"], bl["t"]
        with self.voiceover(
            "Year by year, the premium never disappears: implied above realized on average in every calendar year, "
            "positive in most weeks of each. <bookmark mark='a'/> Now Bollerslev, Tauchen and Zhou's question. "
            "Regress the next thirty days' Bitcoin return on the premium measured in advance. This is a description of "
            "the data, not a strategy test, so the trial counter does not move. The t-statistic is "
            f"{t1:+.2f} over the whole sample, and {t2:+.2f} in the last two years. " + branch +
            "For the S&P 500 the predictability they found was at quarterly horizons, and the next question is whether "
            "the same premium exists there."
        ) as vo:
            self.play(FadeIn(src), LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.3, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(reg))
        self.wait(0.4)
        self.clear_scene()

    def spx(self, x):
        t = np.array([_t(d) for d in x["d"]])
        vx, rv = np.asarray(x["vix"]), np.asarray(x["rv"])
        g = axes([1990, 2026], [0, 0.9], x_length=9.0, y_length=4.2, ylabel=r"S\&P 500: VIX against the next 21 days' realized",
                 xticks=[1990, 2000, 2010, 2020], xfmt=lambda u: f"{u:.0f}", yticks=[0, 0.4, 0.8],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16).to_edge(UP, buff=0.7)
        lv_ = curve(g.ax, t, np.clip(vx, 0, 0.9), IV, stroke_width=2)
        lr = curve(g.ax, t, np.clip(rv, 0, 0.9), RV, stroke_width=1.5)
        riv = band(g.ax, t, np.clip(np.minimum(vx, rv), 0, 0.9), np.clip(vx, 0, 0.9), IV, 0.25)
        leg = legend([(IV, r"the VIX (monthly samples)"), (RV, r"realized over the next 21 trading days")], font_size=17
                     ).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = label(rf"{x['start'] // 10000}--{x['end'] // 10000}: VIX {100 * x['vix_mean']:.1f} vs realized "
                     rf"{100 * x['rv_mean']:.1f} on average; VIX$^2$ above realized variance on {100 * x['share_pos']:.0f}\% "
                     rf"of days", font_size=20, color=GREY_A).next_to(g, DOWN, buff=0.45)
        side2 = label(r"Dew-Becker, Giglio, Le and Rodriguez (2017): the premium is concentrated at the shortest "
                      r"maturities", font_size=19, color=GREY_B).next_to(side, DOWN, buff=0.2)
        src = real_data(r"FRED VIXCLS; Yahoo Finance $\hat{}$GSPC daily closes", corner=DR)
        a, b, s = 100 * x["vix_mean"], 100 * x["rv_mean"], 100 * x["share_pos"]
        with self.voiceover(
            "The S&P 500 since 1990: the VIX in orange, realized volatility over the next twenty-one trading days in "
            f"teal. <bookmark mark='a'/> The orange runs above: {a:.1f} against {b:.1f} on average, and VIX squared "
            f"above realized variance on {s:.0f} percent of days. The exceptions are spikes no index priced in time; the "
            "worst start date was late February 2020. <bookmark mark='b'/> Ian Dew-Becker and co-authors found the "
            "premium concentrated at the shortest maturities."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg), Create(lv_), Create(lr), run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(riv), FadeIn(side))
            vo.wait_until("b")
            self.play(FadeIn(side2))
        self.wait(0.4)
        self.clear_scene()
