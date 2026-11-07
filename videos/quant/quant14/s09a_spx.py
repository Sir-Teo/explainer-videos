from __future__ import annotations

from datetime import date, datetime, timezone

import numpy as np

from videos.quant.quant14.common import axes, data_range, skew_range

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import (BAD, IV, MODEL_COL, OPT, PART, ROUGH, RV, VAR, load, loglog_curve,
                                         loglog_skew_axes, pause, real_data)


def _yr(d):
    d = np.asarray(d, int)
    y, m, dd = d // 10000, (d // 100) % 100, d % 100
    return y + (m - 1) / 12 + (dd - 1) / 365


class SPX(VoiceoverScene):
    def construct(self):
        s = load("pdv_spx")
        c = load("crisis_aug2024")
        self.card()
        self.vix(s)
        self.terms(s)
        self.crisis(s, c)
        self.bitcoin(c)

    def card(self):
        c = chapter_card(14, r"PDV on the S\&P 500, and 5 August 2024", r"What does the past explain, and what not?",
                         lit=(2024,), part=PART)
        with self.voiceover("Chapter fourteen. Path-dependent volatility on the S&P 500, and the fifth of August 2024."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def vix(self, s):
        t = _yr(s["date"])
        v, p = np.asarray(s["vix"], float), np.asarray(s["pred"], float)
        ok = t >= 1993
        t, v, p = t[ok], v[ok], p[ok]
        step = 3
        t, v, p = t[::step], v[::step], p[::step]
        g = axes([1993, 2026], [0, 0.9], x_length=11.0, y_length=4.2, ylabel=r"VIX", xticks=[1995, 2000, 2005, 2010, 2015,
                                                                                           2020, 2025],
                 yticks=[0, 0.2, 0.4, 0.6, 0.8], yfmt=lambda u: f"{100 * u:.0f}", font_size=15).move_to(DOWN * 0.4)
        ax = g.ax
        tr = ValueTracker(0)
        lv = tracing(ax, t, v, tr, IV, stroke_width=1.6)
        lp = tracing(ax, t, p, tr, MODEL_COL["PDV"], stroke_width=1.6)
        cut = DashedLine(ax.c2p(2019, 0), ax.c2p(2019, 0.9), stroke_color=GREY_A)
        tr0 = DashedLine(ax.c2p(2000, 0), ax.c2p(2000, 0.9), stroke_color=GREY_D)
        cl = label(r"fitted 2000--2018; after 2019, out of sample", font_size=16, color=GREY_A).next_to(ax.c2p(2019, 0.9), LEFT, buff=0.1)
        leg = legend([(IV, r"VIX"), (MODEL_COL["PDV"], r"PDV, from the US market's own daily returns")], font_size=17).to_corner(UL, buff=0.35)
        side = VGroup(MathTex(rf"R^2:\ {s['r2_train']:.2f}\ \text{{(in)}},\ {s['r2_test']:.2f}\ \text{{(out)}}", font_size=28,
                              color=MODEL_COL["PDV"]),
                      MathTex(rf"\text{{21-day realized vol: }} {s['r2_base_train']:.2f},\ {s['r2_base_test']:.2f}",
                              font_size=24, color=GREY_B)).arrange(DOWN, aligned_edge=RIGHT, buff=0.1).to_corner(UR, buff=0.35)
        src = real_data(r"FRED VIXCLS; Ken French daily market return (value-weighted, a stand-in for the S\&P 500)")
        with self.voiceover(
            f"Guyon and Lekeufack's home ground was the S&P 500 and the VIX. Replicate it. The input is only the US market's own daily returns since 1986, Ken French's value-weighted market standing in for the S&P; the target is the VIX. Fit on 2000 to 2018, then freeze. <bookmark mark='a'/> Watch thirty years trace out: the dot-com bust, 2008, Volmageddon, March 2020. <bookmark mark='b'/> In sample, it explains {100 * s['r2_train']:.0f} percent of the VIX's variation; out of sample, from 2019 to 2025, {100 * s['r2_test']:.0f} percent, against {100 * s['r2_base_test']:.0f} for a line in the last month's realized volatility. Most of the VIX is a function of the path the market has taken. This uses the same-day return to reconstruct the same-day VIX close. It is a proxy replication with a different equity-return series, not an ex-ante forecast or proof that the VIX has no independent innovations."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(src), FadeIn(lv), FadeIn(lp), FadeIn(cut), FadeIn(tr0), FadeIn(cl))
            vo.wait_until("a")
            self.play(tr.animate.set_value(len(t) - 1), run_time=max(vo.remaining(0.0) - 5, 8), rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(side))
        lv.clear_updaters()
        lp.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def terms(self, s):
        b = s["beta"]
        x = s["x"]
        c = s["contrib"]
        rows = [cmath(r"\sigma_t", r"=", rf"{b[0]:.3f} {b[1]:+.1f}\,R_{{1,t}} + {b[2]:.2f}\sqrt{{R_{{2,t}}}}", font_size=40,
                      colors={r"\sigma_t": IV}),
                cmath(r"\sigma^{\rm imp}_t - \hat\sigma^{\rm PDV}_t", r"=", '\\text{fitted proxy residual}',
                      font_size=36, colors={r"\sigma^{\rm imp}_t - \hat\sigma^{\rm PDV}_t": BAD})]
        whys = [why(rf"the trend's coefficient is negative: falls raise volatility, the leverage effect. One s.d. of the "
                    rf"trend term moves the VIX by {100 * c['trend']:.1f} points, of activity by {100 * c['activity']:.1f}"),
                why('Residuals can include omitted path features, parameter error, risk premia, index construction and liquidity; this fit does not separate them.')]
        step = ladder(self, rows, whys, keep=2, top=2.6, x=-0.6, buff=0.9, edge=6.9)
        q = pause(r"The S\&P 500 falls 3\% in a day. Which term moves the PDV forecast more, trend or activity?",
                  width=7.0, font_size=22).to_edge(DOWN, buff=1.6)
        bound = wrapped_label(rf"the trend kernel's exponent sits at its lower bound, $\alpha_1 = {x[0]:.3f}$: the trend's memory "
                              r"wants to be as long as the 1{,}000-day window allows, so its exact shape is not identified"
                              if s["at_bound"] else rf"trend kernel: $\alpha_1 = {x[0]:.2f}$, $\delta_1 = {365 * x[1]:.0f}$ days",
                              11.0, 18, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            f"Here, unlike Bitcoin, the trend matters. The fitted trend coefficient is negative: when the market has been falling, the VIX is higher. That is the leverage effect, and the raw material of the Zumbach effect of the next chapter. <bookmark mark='a'/> Pause and predict: the S&P falls three percent in a day. Which term moves the forecast more? <bookmark mark='b'/> Both move it, and the trend carries the sign: a fall raises both, a rally of the same size raises activity but lowers the trend term. Over the sample, one standard deviation of the trend term is worth {100 * s['contrib']['trend']:.1f} VIX points, of activity {100 * s['contrib']['activity']:.1f}. <bookmark mark='c'/> One caution: the trend kernel's exponent ran to the edge of its range, so its memory is longer than our window can pin down. <bookmark mark='d'/> And the residual is everything the path does not explain. A regression residual is everything this fitted feature set misses; it need not be everything any possible price-path model would miss."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("b")
            vo.wait_until("c")
            self.play(FadeIn(bound))
            vo.wait_until("d")
            self.play(FadeOut(q))
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def crisis(self, s, c):
        d = s["days"]
        a2, a5, a6 = d["20240802"], d["20240805"], d["20240806"]
        gap = 100 * (a5["vix"] - a5["pdv"])
        card = crisis_card(r"5 August 2024", r"The VIX spike", body=(
            r"The yen carry trade unwinds; the Nikkei 225 falls " + f"{-100 * c['nikkei_0805']:.1f}" + r"\% that day. Before "
            r"the US open the VIX prints above 65 "
            r"(SEC staff working paper, Li and Askanazi 2025), while VIX futures stay below 35. It closes at "
            + f"{100 * a5['vix']:.2f}" + r", from " + f"{100 * a2['vix']:.2f}" + r" on Friday."),
            stats=[(rf"{100 * a5['vix']:.1f}", r"VIX close, 5 August (FRED)"),
                   (rf"{100 * a5['pdv']:.1f}", r"PDV, from past returns only"),
                   (rf"{gap:.0f}", r"points the path does not explain")], width=7.6, font_size=22).to_edge(LEFT, buff=0.4)
        cards = VGroup(
            wrapped_label(r"BIS Bulletin 95 (Todorov and Vilkov, 29 October 2024): the VIX's biggest ever one-day spike; "
                          r"because the VIX is computed from quotes, not trades, dealers' quote-setting and the widening of "
                          r"bid--ask spreads, particularly for puts, contributed; VIX ETFs and dispersion trades were "
                          r"unlikely the main driver", 4.8, 17, GREY_A),
            wrapped_label(r"SEC DERA working paper (April 2025): more out-of-the-money puts entered the calculation, and the "
                          r"surge was driven by their mid-quotes", 4.8, 17, GREY_A),
            wrapped_label(r"BIS Bulletin 90 (27 August 2024): the unwinding of leveraged trades in equity and currency "
                          r"markets amplified the initial reaction", 4.8, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35)
        vm = d["20180205"]
        with self.voiceover(
            f"The fifth of August 2024. The yen carry trade was unwinding; Japan's Nikkei fell {-100 * c['nikkei_0805']:.1f} percent that day. Before the US open, the VIX printed above sixty-five, according to an SEC staff working paper, while VIX futures stayed below thirty-five. It closed at {100 * a5['vix']:.2f}, from {100 * a2['vix']:.2f} on the Friday. <bookmark mark='a'/> Feed the path-dependent model only the returns up to that day: it says {100 * a5['pdv']:.1f}. The gap, {gap:.0f} points, is what the path does not explain. <bookmark mark='b'/> What was it? The BIS's anatomy of the spike, by Karamfil Todorov and Grigory Vilkov, points at the quotes: the VIX is computed from quotes, not trades, and put bid-ask spreads blew out. The SEC staff paper agrees. A liquidity event in the quotes, on top of a real deleveraging. <bookmark mark='c'/> For comparison, on Volmageddon, the fifth of February 2018, the VIX closed at {100 * vm['vix']:.1f} and the model said {100 * vm['pdv']:.1f}. The PDV number includes August fifth's return and refers to the close. The pre-open VIX high is a different timestamp. The cited quote mechanism helps explain the intraday index spike; our close-to-close regression residual does not identify its causal contribution."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(card.stats[2], color=QC.CRISIS))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cards], lag_ratio=0.4))
            vo.wait_until("c")
        self.wait(0.4)
        self.clear_scene()

    def bitcoin(self, c):
        t = np.asarray(c["dvol_t"], float)
        hh = (t - datetime(2024, 7, 29, tzinfo=timezone.utc).timestamp()) / 86400
        cl, hi = np.asarray(c["dvol_close"], float), np.asarray(c["dvol_high"], float)
        dr = data_range(cl, hi)
        g = axes([0, 12], list(dr), x_length=6.6, y_length=2.8, ylabel=r"DVOL, hourly", xticks=[0, 4, 7, 11],
                 xfmt=lambda u: {0: "29 Jul", 4: "2 Aug", 7: "5 Aug", 11: "9 Aug"}[int(round(u))], yticks=[40, 60, 80, 100],
                 font_size=14).to_corner(UL, buff=0.45)
        tr = ValueTracker(0)
        lc = tracing(g.ax, hh, cl, tr, IV, stroke_width=2)
        lh = tracing(g.ax, hh, hi, tr, BAD, stroke_width=1)
        rvd = np.asarray(c["btc_rv_days"])
        rv = np.asarray(c["btc_rv"]) * 100
        d0 = int(datetime(2024, 7, 29, tzinfo=timezone.utc).timestamp() // 86400)
        g2 = axes([-0.5, 11.5], [0, max(250, rv.max() * 1.1)], x_length=6.6, y_length=1.8, ylabel=r"bitcoin realized vol, by day (\%)",
                  xticks=[0, 4, 7, 11], xfmt=lambda u: {0: "29 Jul", 4: "2 Aug", 7: "5 Aug", 11: "9 Aug"}[int(round(u))],
                  yticks=[0, 100, 200], font_size=14).next_to(g, DOWN, buff=0.5).align_to(g, LEFT)  # both inside the frame
        bars = VGroup(*[Rectangle(width=0.35, height=max(g2.ax.c2p(0, v)[1] - g2.ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                  fill_color=BAD if dd - d0 == 7 else RV, fill_opacity=0.85).move_to(g2.ax.c2p(dd - d0, v / 2))
                        for dd, v in zip(rvd, rv)])
        k5 = str(d0 + 7)
        bp = c["btc_pdv"].get(k5, {"dvol": float("nan"), "pdv": float("nan")})
        yr = skew_range(*[c[key]["skew"] for key in ("skew_before", "skew_after") if c.get(key)])
        g3 = loglog_skew_axes(x_length=4.6, y_length=3.0, t_lo=2 / 365, y_range=yr, font_size=12).to_corner(UR, buff=0.4).shift(DOWN * 0.3)
        sk = VGroup()
        for key, col in (("skew_before", GREY_B), ("skew_after", BAD)):
            w = c.get(key)
            if w:
                sk.add(loglog_curve(g3.ax, w["T"], w["skew"], col, y_range=yr))
        leg3 = legend([(GREY_B, r"31 July"), (BAD, r"7 August")], font_size=14).next_to(g3, DOWN, buff=0.15)
        mx = float(np.nanmax(hi[(hh >= 7) & (hh < 8)])) if np.any((hh >= 7) & (hh < 8)) else float("nan")
        rv5 = float(rv[rvd - d0 == 7][0]) if np.any(rvd - d0 == 7) else float("nan")
        note_ = VGroup(MathTex(rf"\text{{DVOL close}}\ {100 * bp['dvol']:.0f},\ \text{{PDV}}\ {100 * bp['pdv']:.0f}", font_size=24,
                               color=MODEL_COL["PDV"])).next_to(leg3, DOWN, buff=0.3).align_to(g3, LEFT)
        src = real_data(r"Deribit DVOL hourly; Binance 5-minute returns; the Surface on two Wednesdays", corner=DR)
        with self.voiceover(
            f"""Bitcoin during the same episode. DVOL's hourly high on August fifth reaches {mx:.0f}. <bookmark mark='a'/> Daily realized volatility from five-minute returns is {rv5:.0f} percent annualized, a different horizon and measure from a thirty-day implied index. <bookmark mark='b'/> Including that day's return, the frozen proxy reconstructs DVOL's close at {100 * bp['pdv']:.0f}, against {100 * bp['dvol']:.0f} observed. This close fit does not prove a causal contrast between Bitcoin prices and equity-option quotes. <bookmark mark='c'/> At right are the original July thirty-first and August seventh skew magnitudes. The curves preserve the available expiries; neither measures the pre-open VIX episode or establishes a zero-maturity limit. Next: joint SPX and VIX modeling."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(lc), FadeIn(lh), FadeIn(src))
            self.play(tr.animate.set_value(len(hh) - 1), run_time=5, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(g2), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(note_))
            vo.wait_until("c")
            self.play(FadeIn(g3), LaggedStart(*[Create(x) for x in sk], lag_ratio=0.5), FadeIn(leg3))
        lc.clear_updaters()
        lh.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
