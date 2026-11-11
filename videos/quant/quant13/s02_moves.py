from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, OPT, PART, RV, SPOT, VAR, load, pause, real_data


def _yr(ts):
    return 1970 + np.asarray(ts, float) / (365.2425 * 86400)


class Moves(VoiceoverScene):
    def construct(self):
        f = load("facts")
        vf = load("vol_facts")
        self.card()
        self.series(f)
        self.scatter(f, vf)
        self.clustering(vf)
        self.crash(vf)

    def card(self):
        c = chapter_card(1, r"Why volatility must move", r"What does a constant volatility leave out?", lit=(1987,),
                         part=PART)
        with self.voiceover("Chapter one. Why volatility must move."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c), run_time=0.35)

    def series(self, f):
        t = _yr(f["t"])
        rv = np.asarray(f["rv30"])
        td = _yr(f["dvol_t"])
        dv = np.asarray(f["dvol"])
        g = axes([2021.25, 2026], [0, 1.65], x_length=8.2, y_length=4.2, ylabel=r"bitcoin volatility, annualized",
                 xticks=[2022, 2023, 2024, 2025], yticks=[0, 0.4, 0.8, 1.2], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        lr = curve(ax, t, rv, RV, stroke_width=2.2)
        ld = curve(ax, td, dv, IV, stroke_width=2.2)
        leg = legend([(RV, r"realized over the past 30 days"), (IV, r"DVOL: implied, 30 days ahead")],
                     font_size=18).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = VGroup(
            MathTex(rf"{100 * f['rv_min']:.0f}\% \ \text{{to}}\ {100 * f['rv_max']:.0f}\%", font_size=34, color=RV),
            wrapped_label(r"the range of 30-day realized volatility, April 2021 to November 2025: Black and Scholes "
                          r"assumed one number", 4.0, 20, GREY_A),
            MathTex(rf"\text{{vol of vol}} \approx {100 * f['volvol']:.0f}\%", font_size=32, color=VAR),
            wrapped_label(r"the annualized volatility of DVOL's own daily log changes: volatility is itself a risky "
                          r"asset, and options on it trade", 4.0, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Binance BTCUSDT daily; Deribit DVOL daily")
        with self.voiceover(
            (
            "Black, Scholes and Merton assumed one volatility, fixed for the life of the option. Here is Bitcoin's. In "
            "green, the volatility it realized over each past thirty days. <bookmark mark='a'/> It ranged from "
            f"{100 * f['rv_min']:.0f} to {100 * f['rv_max']:.0f} percent a year. <bookmark mark='b'/> In orange, "
            "DVOL, the market's thirty-day implied volatility. It moves too: measured like a price, its volatility "
            f"is about {100 * f['volvol']:.0f} percent a year. Volatility is a second random river beside the price, "
            "and an option is a bet on both."
        )
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg[0]), Create(lr), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(leg[1]), Create(ld), FadeIn(side[2]), FadeIn(side[3]), run_time=2.5)
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def scatter(self, f, vf):
        P = np.asarray(vf["pairs"])
        P = P[np.argsort(P[:, 2])]
        g = axes([-0.2, 0.2], [-0.35, 0.35], x_length=6.0, y_length=4.6, xlabel=r"bitcoin's daily return",
                 ylabel=r"the same day's change in log DVOL", xticks=[-0.15, 0, 0.15], yticks=[-0.3, 0, 0.3],
                 xfmt=lambda u: f"{100 * u:+.0f}\\%" if u else "0", yfmt=lambda u: f"{100 * u:+.0f}\\%" if u else "0",
                 font_size=16).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        ycol = {2021: GREY_B, 2022: BAD, 2023: RV, 2024: IV, 2025: VAR}
        P = P[(np.abs(P[:, 0]) < 0.2) & (np.abs(P[:, 1]) < 0.35)]
        dots = VGroup(*[Dot(ax.c2p(a_, b_), radius=0.028, color=ycol[int(c_)], fill_opacity=0.75) for a_, b_, c_ in P])
        n = ValueTracker(2)

        def fitline():
            k = max(int(n.get_value()), 3)
            sl, ic = np.polyfit(P[:k, 0], P[:k, 1], 1)
            return Line(ax.c2p(-0.2, ic - 0.2 * sl), ax.c2p(0.2, ic + 0.2 * sl), color=WHITE, stroke_width=3)

        ln = always_redraw(fitline)
        cnt = always_redraw(lambda: MathTex(rf"{int(n.get_value())}\ \text{{days}}", font_size=24, color=GREY_A)
                            .next_to(g, UP, buff=0.1).align_to(g, RIGHT))
        leg = legend([(ycol[y], str(y)) for y in ycol], font_size=18).arrange(RIGHT, buff=0.3).next_to(g, DOWN, buff=0.15)
        by = f["by_year"]
        side = VGroup(
            wrapped_label(r"one dot per day: the return, against what implied volatility did that day; the line is the "
                          r"least-squares fit to the days so far", 4.4, 19, GREY_A),
            *[MathTex(rf"{y}:\ \rho = {by[str(y)]:+.2f}", font_size=28, color=ycol[y]) for y in ycol],
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.6)
        src = real_data(r"Binance BTCUSDT daily; Deribit DVOL daily, 2021--2025")
        with self.voiceover(
            (
            (
            f"""The scatter pairs each day's Bitcoin return with its log-DVOL change. Its line is a descriptive regression. On days Bitcoin fell more than five percent, the mean log-DVOL change, multiplied by one hundred, was {f['dvol_change_down5']:.0f}. <bookmark mark='a'/> The 2022 correlation was {by['2022']:+.2f}. <bookmark mark='b'/> In 2023 it was {by['2023']:+.2f}; that sign change does not identify a cause. Across {f['n']} paired days it was {f['leverage_corr']:+.2f}, so the same-day linear fit accounts for about {100 * f['leverage_corr'] ** 2:.0f} percent of log-DVOL-change variance. The remainder is not proof of independent volatility noise. Nor does this regression test GARCH, whose state depends on the full return history. Stochastic-volatility models add a separate shock as a modelling choice."""
        )
        )
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg), FadeIn(side[0]))
            self.add(ln, cnt)
            k22 = int(np.searchsorted(P[:, 2], 2023.0))
            k23 = int(np.searchsorted(P[:, 2], 2024.0))
            self.play(n.animate.set_value(k22), LaggedStart(*[FadeIn(d_) for d_ in dots[:k22]], lag_ratio=0.02),
                      run_time=vo.until("a"), rate_func=linear)
            self.play(FadeIn(side[1:3]))
            vo.wait_until("b")
            self.play(n.animate.set_value(k23), LaggedStart(*[FadeIn(d_) for d_ in dots[k22:k23]], lag_ratio=0.02),
                      FadeIn(side[3]), run_time=3, rate_func=linear)
            self.play(n.animate.set_value(len(P)), LaggedStart(*[FadeIn(d_) for d_ in dots[k23:]], lag_ratio=0.02),
                      FadeIn(side[4:]), run_time=3, rate_func=linear)
        ln.clear_updaters()
        cnt.clear_updaters()
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def clustering(self, vf):
        acf_a, acf_r = np.asarray(vf["acf_abs"]), np.asarray(vf["acf_ret"])
        lags = np.arange(1, len(acf_a) + 1)
        g = axes([0, 61], [-0.1, 0.2], x_length=6.0, y_length=2.5, xlabel=r"lag (days)", ylabel=r"autocorrelation",
                 xticks=[1, 20, 40, 60], yticks=[-0.1, 0, 0.1, 0.2], font_size=16).to_edge(LEFT, buff=0.8).to_edge(UP, buff=1.0)
        # short enough that the three-row ladder below starts clear of its axis labels
        ax = g.ax
        w = 0.42 * (ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0])  # two bars per lag, side by side, with a gap

        def bars(vals, col, dx):
            return VGroup(*[Rectangle(width=w, height=max(abs(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]), 1e-3), stroke_width=0,
                                      fill_color=col, fill_opacity=0.85).move_to(ax.c2p(l_ + dx, v / 2))
                            for l_, v in zip(lags, vals)])

        br, ba = bars(acf_r, GREY_B, -0.23), bars(acf_a, VAR, 0.23)
        band_ = Rectangle(width=abs(ax.c2p(61, 0)[0] - ax.c2p(0, 0)[0]), height=abs(ax.c2p(0, 0.096)[1] - ax.c2p(0, 0)[1]),
                          stroke_width=0, fill_color=GREY_D, fill_opacity=0.35).move_to(ax.c2p(30.5, 0))
        leg = legend([(GREY_B, 'returns $r_t$: small linear autocorrelations'), (VAR, 'sizes $|r_t|$: volatility clustering')], font_size=18).next_to(
            g, UP, buff=0.12).align_to(g, LEFT)
        hl = vf["dvol_halflife_days"]
        rows = [cmath(r"\widehat{\text{vol of vol}}", r"=", r"\operatorname{sd}\big(\Delta\log\text{DVOL}\big)\sqrt{365}",
                      font_size=30, colors={r"\widehat{\text{vol of vol}}": VAR}),
                cmath(r"\log\text{DVOL}_{t+1}", r"=", rf"a + {vf['ar1_phi']:.4f}\,\log\text{{DVOL}}_t + \varepsilon_t",
                      font_size=30, colors={r"\log\text{DVOL}_{t+1}": IV}),
                cmath(r"t_{1/2}", r"=", rf"\frac{{\ln 2}}{{-\ln\phi}} = {hl:.0f}\ \text{{days}}", font_size=30,
                      colors={r"t_{1/2}": IV})]
        whys = [why(r"measured like a price's volatility, on the daily changes of the log", font_size=20),
                why(r"an AR(1): the discretised Ornstein--Uhlenbeck process of Part 5", font_size=20),
                why(r"how long a shock to volatility takes to decay by half", font_size=20)]
        step = ladder(self, rows, whys, keep=3, top=-1.0, x=-2.6, buff=0.3, edge=6.9)
        src = real_data(r"Binance BTCUSDT daily and Deribit DVOL daily, April 2021 -- November 2025")
        with self.voiceover(
            (
            f"""Two descriptive patterns. Return autocorrelations are small against this pointwise noise guide; that does not establish independence or no memory. <bookmark mark='a'/> Absolute returns cluster: lag-one autocorrelation is {acf_a[0]:.2f}, with positive dependence still visible at longer lags. <bookmark mark='b'/> Log DVOL also shows persistence. <bookmark mark='c'/> Regress tomorrow's log level on today's: the fitted daily AR-one slope is {vf['ar1_phi']:.3f}. <bookmark mark='d'/> An OU-style interpretation gives a half-life of {hl:.0f} days. Exponentiating the fitted long-run log level gives {100 * vf['dvol_mean']:.0f} percent; that is not the arithmetic mean of DVOL. These are sample summaries, not fixed laws of the market."""
        )
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(band_), FadeIn(leg[0]),
                      LaggedStart(*[GrowFromEdge(b_, DOWN if v >= 0 else UP) for b_, v in zip(br, acf_r)], lag_ratio=0.02),
                      run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(leg[1]), LaggedStart(*[GrowFromEdge(b_, DOWN if v >= 0 else UP) for b_, v in zip(ba, acf_a)],
                                                  lag_ratio=0.02), run_time=2.5)
            vo.wait_until("b")
            step(0)
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            step(2)
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def crash(self, vf):
        c = vf["crash1987"]
        card = crisis_card(r"19 October 1987", r"Black Monday",
                           r"The S\&P 500 fell from " + f"{c['close_before']:.2f}" + r" to " + f"{c['close']:.2f}" +
                           r" in one day. Before the crash, index options traded close to one flat volatility; ever "
                           r"since, out-of-the-money puts have been dear: the skew (Rubinstein 1994). Bates (2000) "
                           r"found crash fears priced in S\&P 500 futures options for years after.",
                           stats=[(rf"{100 * c['ret']:.1f}\%", r"the day's log return"),
                                  (rf"{c['z']:.0f}\,\sigma", r"against the prior year's daily volatility"),
                                  (rf"10^{{{c['log10p']:.0f}}}", r"its probability under a constant-volatility normal model")],
                           width=7.4)
        card.move_to(LEFT * 2.6)
        pp = pause(r"Bitcoin rose 10\% today. Does its implied volatility rise or fall?", width=4.6).to_corner(DR, buff=0.4)
        src = real_data(r"S\&P 500 daily closes, 1986--1987 (Yahoo Finance)", corner=DL)
        with self.voiceover(
            (
            f"""On 19 October 1987 the S&P 500 fell from {c['close_before']:.0f} to {c['close']:.0f}, a log return of {100 * c['ret']:.1f} percent. <bookmark mark='a'/> Against the preceding 250 trading days' standard deviation, that is {abs(c['z']):.0f} standard deviations. A fixed-volatility Gaussian benchmark assigns a one-sided probability of roughly ten to the minus {abs(c['log10p']):.0f}. This is conditional on that deliberately restrictive benchmark, not an estimated real-world crash probability. Post-crash index downside skew became especially prominent. <bookmark mark='b'/> Pause: Bitcoin rises ten percent. Must implied volatility rise or fall? The sample shows both signs of association; it gives no deterministic answer. Next, what random volatility does to prices."""
        )
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[Indicate(s_, color=QC.CRISIS, scale_factor=1.08) for s_ in card.stats], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(pp))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)
