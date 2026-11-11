from __future__ import annotations

from datetime import date

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, load, real_data


def _yr(d):
    if isinstance(d, str):
        x = date.fromisoformat(d)
    else:
        d = int(d)
        x = date(d // 10000, (d // 100) % 100, d % 100)
    return x.year + (x.timetuple().tm_yday - 1) / 365


class VIX(VoiceoverScene):
    def construct(self):
        v = load("vixcomp")
        self.card()
        self.lab(v)
        self.derive(v)
        self.dvol(v)
        self.history(v)

    def card(self):
        c = chapter_card(11, r"The VIX, and our own", r"What exactly does a volatility index compute?", part=PART)
        with self.voiceover("Chapter eleven. The VIX, and our own."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def lab(self, v):
        card = lab_card(r"the VIX recipe on one expiry", [
            "o = np.argsort(K)",
            "K, C, P = K[o], C[o], P[o]",
            "i0 = int(np.searchsorted(K, F, side='right') - 1)",
            "K0 = K[i0]                                 # first strike below F",
            "Q = np.where(K < K0, P, C)                 # out of the money",
            "Q[i0] = 0.5 * (P[i0] + C[i0])",
            "dK = np.empty_like(K)",
            "dK[1:-1] = (K[2:] - K[:-2]) / 2",
            "dK[0], dK[-1] = K[1] - K[0], K[-1] - K[-2]",
            "s2 = 2 / T * np.sum(dK / K**2 * np.exp(r*T) * Q) - (F / K0 - 1)**2 / T",
            "return float(np.sqrt(max(s2, 0.0)))",
        ], source="explainer/quant/house/volsurface.py", width=8.4, font_size=17).to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.4)
        p0, p1 = v["pair"]
        # the bars: each strike's contribution, in the order the sum adds them
        K, c = np.asarray(p0["K"]), np.asarray(p0["contrib"])
        F = p0["F"]
        g = axes([K.min(), K.max()], [0, float(c.max()) * 1.1], x_length=4.0, y_length=2.6, xlabel=r"strike",
                 ylabel=r"$\frac{2}{T}\frac{\Delta K}{K^2}Q(K)$", xticks=[], yticks=[], font_size=14).to_edge(RIGHT, buff=0.4
                                                                                                         ).shift(UP * 1.6)
        bars = VGroup(*[Line(g.ax.c2p(a, 0), g.ax.c2p(a, b), color=BAD if a < p0["K0"] else IV, stroke_width=4)
                        for a, b in zip(K, c)])
        k0 = DashedLine(g.ax.c2p(p0["K0"], 0), g.ax.c2p(p0["K0"], float(c.max()) * 1.1), color=GREY_B)
        out = [f"{p0['expiry']}: {p0['n']} strikes, K0={p0['K0']:,.0f}, sigma={100 * p0['sigma']:.1f}%",
               f"{p1['expiry']}: {p1['n']} strikes, K0={p1['K0']:,.0f}, sigma={100 * p1['sigma']:.1f}%",
               f"30-day: {100 * v['our_vix']:.1f}%    Deribit DVOL at 08:00: {100 * v['dvol']:.1f}%"]
        s1, s2, ours, dv = 100 * p0["sigma"], 100 * p1["sigma"], 100 * v["our_vix"], 100 * v["dvol"]
        with self.voiceover(
            f"""The VIX is a discretized, annualized variance-price measure, quoted as a volatility. Find K zero at or below the forward, use puts below and calls above, average the pair at K zero, weight by strike spacing over strike squared, and subtract the prescribed correction. <bookmark mark='a'/> Our Bitcoin illustration applies that formula to model marks on the two available expiries around thirty days, not the full SPX index eligibility and liquidity rules. <bookmark mark='b'/> Its expiry values are {s1:.1f} and {s2:.1f} percent; total-variance interpolation gives {ours:.1f}. The hourly DVOL observation is {dv:.1f}. Pooling and time aggregation differ, so these are not synchronized executable index prices."""
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(g), Create(k0))
            self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.08, run_time=3.5))
            vo.wait_until("b")
            lab_run(self, card, out)
        self.wait(0.6)
        self.clear_scene()

    def derive(self, v):
        rows = [cmath(r"\sigma^2", r"=", r"\frac{2}{T}\sum_i \frac{\Delta K_i}{K_i^2}e^{rT}Q(K_i) - \frac1T\Big(\frac{F}{K_0} - 1"
                      r"\Big)^2", font_size=36, colors={r"\sigma^2": IV}),
                cmath(r"\frac{2}{T}\int_{K_0}^F \frac{(K - S)^+ - (S - K)^+}{K^2}\,dK", r"\approx",
                      r"\frac{1}{T}\Big(\frac{F}{K_0} - 1\Big)^2", font_size=32),
                cmath(r"\sigma^2_{30}", r"=", r"\Big[T_1\sigma_1^2\frac{N_2 - N_{30}}{N_2 - N_1} + T_2\sigma_2^2\frac{N_{30} - N_1}"
                      r"{N_2 - N_1}\Big]\frac{N_{365}}{N_{30}}", font_size=32, colors={r"\sigma^2_{30}": LV})]
        whys = [why(r"Cboe's formula: the strip of Chapter 9 as a sum over listed strikes, $Q$ the out-of-the-money "
                    r"price"),
                why(r"centring at $K_0 \le F$ instead of $F$ uses a call where a put belongs between them; parity turns "
                    r"the difference into the forward correction, to second order"),
                why(r"linear in total variance between the two expiries around thirty days, then annualized ($N$: "
                    r"minutes)")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "On paper: the discretized strip with one correction. <bookmark mark='a'/> The strip should switch from puts to calls at the forward, but switches at K zero, just below; between them it holds calls where puts belong, and put-call parity, to second order, motivates the prescribed subtracted term. It is a discretization correction, not an exact continuum identity. <bookmark mark='b'/> Then two expiries around thirty days are combined linearly in total variance. That is Cboe's rebuild of September 2003, designed with Goldman Sachs; Robert Whaley's original of 1993 averaged at-the-money implied volatilities on the S&P 100."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def dvol(self, v):
        t = np.array([_yr(d) for d in v["days"]])
        ours, dv = np.asarray(v["ours"]), np.asarray(v["dvol_w"])
        g = axes([2021.2, 2026], [0.2, 1.4], x_length=8.6, y_length=4.0, ylabel=r"30-day bitcoin volatility index",
                 xticks=[2022, 2023, 2024, 2025], xfmt=lambda u: f"{u:.0f}", yticks=[0.4, 0.8, 1.2],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16).to_edge(UP, buff=0.7)
        lo = curve(g.ax, t, np.clip(ours, 0.2, 1.4), IV, stroke_width=3)
        ld = curve(g.ax, t, np.clip(dv, 0.2, 1.4), LV, stroke_width=2.5)
        gap = band(g.ax, t, np.clip(np.minimum(ours, dv), 0.2, 1.4), np.clip(np.maximum(ours, dv), 0.2, 1.4), BAD, 0.35)
        leg = legend([(IV, r"ours: the variance strike of each Wednesday's fitted surface"), (LV, r"Deribit's DVOL, same hour")],
                     font_size=17).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = VGroup(MathTex(rf"\text{{mean}}\ {100 * v['mean_ours']:.1f}\%\ \text{{vs}}\ {100 * v['mean_dvol']:.1f}\%,\ \ "
                              rf"\text{{corr}}\ {v['corr']:.3f}", font_size=28),
                      wrapped_label(rf"gap {v['gap_mean']:+.1f} $\pm$ {v['gap_sd']:.1f} vol points; quote selection, "
                            r"liquidity filters, fitting, wings and observation times differ", max_width=11.8, font_size=19, color=GREY_A)).arrange(DOWN, buff=0.2).next_to(g, DOWN, buff=0.4)
        q = label(r"pause and predict: drop every option beyond $\pm 20\%$. Does the index rise or fall?", font_size=21,
                  color=QC.HOUSE).to_corner(DR, buff=0.3)  # beside the source line, below the stats
        src = real_data(r"weekly Deribit surfaces; DVOL from Deribit", corner=DL)
        n, a, b, c_, gm, gs = v["n_weeks"], 100 * v["mean_ours"], 100 * v["mean_dvol"], v["corr"], v["gap_mean"], v["gap_sd"]
        with self.voiceover(
            f"""Compare the fitted proxy with DVOL over {n} Wednesdays. Deribit's March 2021 index uses a related variance-strip approach, with its own liquidity, delta and smoothing rules. <bookmark mark='a'/> Their correlation is {c_:.3f}; our proxy averages {gm:.1f} points higher, with sample standard deviation {gs:.1f}. Model extrapolation of unquoted wings can contribute, alongside quote selection, mark fitting and different observation windows. This comparison does not isolate one cause. Pause and predict: holding the rest of a positive option strip fixed, removing strikes beyond twenty percent removes positive contributions. The truncated variance estimate falls."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(lo), FadeIn(leg[0]), run_time=2)
            vo.wait_until("a")
            self.play(Create(ld), FadeIn(leg[1]), run_time=2)
            self.play(FadeIn(gap), FadeIn(side))
            self.play(FadeIn(q))
        self.wait(0.4)
        self.clear_scene()

    def history(self, v):
        t = np.array([_yr(d) for d in v["vix_d"]])
        x = np.asarray(v["vix_x"])
        g = axes([1990, 2026], [0, 90], x_length=8.6, y_length=3.0, ylabel=r"the VIX, daily close (every fifth day)",
                 xticks=[1990, 2000, 2010, 2020], xfmt=lambda u: f"{u:.0f}", yticks=[0, 40, 80], font_size=15
                 ).to_edge(UP, buff=0.5)
        line = curve(g.ax, t, x, IV, stroke_width=1.8)
        mx = Dot(g.ax.c2p(_yr(v["vix_max_d"]), v["vix_max"]), color=BAD, radius=0.07)
        mxl = label(rf"16 March 2020: {v['vix_max']:.2f}", font_size=17, color=BAD).next_to(mx, LEFT, buff=0.1)
        tops = VGroup()
        for d, a, b, ch in v["top"][:3]:
            dd = Dot(g.ax.c2p(_yr(d), b), color=QC.CRISIS, radius=0.06)
            tops.add(dd)
        tt = np.array([_yr(d) for d in v["ts_d"]])
        rr = np.asarray(v["ts_ratio"])
        g2 = axes([1990, 2026], [0.7, 1.5], x_length=8.6, y_length=2.0, ylabel=r"VIX $/$ VIX3M (above 1: inverted)",
                  xticks=[2008, 2018, 2025], xfmt=lambda u: f"{u:.0f}", yticks=[0.8, 1.0, 1.2], font_size=15
                  ).next_to(g, DOWN, buff=0.45)
        one = DashedLine(g2.ax.c2p(2007.9, 1), g2.ax.c2p(2026, 1), color=GREY_C)
        rl = curve(g2.ax, tt, rr, LV, stroke_width=1.5)
        t1, t2, t3 = v["top"][0], v["top"][1], v["top"][2]
        snap = v["ts_snap"]
        side = label(rf"largest one-day rises: {t1[0] // 10000} ({100 * t1[3]:+.0f}\%), {t2[0] // 10000} "
                     rf"({100 * t2[3]:+.0f}\%), {t3[0] // 10000} ({100 * t3[3]:+.0f}\%); VIX below VIX3M on "
                     rf"{100 * v['contango']:.0f}\% of days since {v['ts_start'] // 10000}", font_size=19,
                     color=GREY_A).to_edge(DOWN, buff=0.25)
        src = real_data(r"FRED: VIXCLS (1990--2025), VXVCLS (2007--2025)", corner=UR)
        mxv = v["vix_max"]
        r1, r2 = snap["20180202"], snap["20180205"]
        cg = 100 * v["contango"]
        j1 = 100 * t1[3]
        with self.voiceover(
            f"And the VIX itself, back to 1990, the start of Cboe's recalculated history. Long calm stretches, and spikes: 1998, 2002, the financial crisis, and the highest close on record, {mxv:.2f}, on the sixteenth of March 2020. <bookmark mark='a'/> The largest one-day rise is not any of those: it is the fifth of February 2018, {j1:+.0f} percent, the subject of Chapter fifteen. <bookmark mark='b'/> Underneath, the VIX divided by its three-month cousin. Below one, the term structure slopes up: that was true on {cg:.0f} percent of days since December 2007. On the second of February 2018 the ratio was {r1:.3f}; on the fifth, {r2:.3f}. Next: how these variance prices compare with subsequent realized volatility."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(line), run_time=3)
            self.play(FadeIn(mx), FadeIn(mxl))
            vo.wait_until("a")
            self.play(FadeIn(tops), Flash(tops[0], color=QC.CRISIS))
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(one), Create(rl), run_time=2.5)
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()
