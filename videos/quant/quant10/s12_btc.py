from __future__ import annotations

from datetime import datetime, timezone

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant10.common import GAIN, GAM, IMP, LOSS, PART, REA, THE, load, ts_date


def year_of(ts):
    d = datetime.fromtimestamp(float(ts), tz=timezone.utc)
    return d.year + (d.timetuple().tm_yday - 1) / 365.0


class BTC(VoiceoverScene):
    def construct(self):
        b = load("btc")
        im = load("implied")
        self.card()
        self.series(b)
        self.scatter(b)
        self.distribution(b, im)
        self.replay(load("btc_replay"))
        self.crisis(b)

    def card(self):
        c = chapter_card(15, r"Selling volatility on real Bitcoin", r"Is the implied volatility too high?",
                         lit=(2021, 2024), part=PART)
        with self.voiceover("Chapter fifteen. Selling volatility on real Bitcoin."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def series(self, b):
        t1 = np.array([year_of(x) for x in b["dvol_t"]])
        t2 = np.array([year_of(x - 30 * 86400) for x in b["rv30_t"]])
        iv, rv = np.asarray(b["dvol"], float), np.asarray(b["rv30"], float)
        g = axes([2021.25, 2026], [0.15, 1.6], x_length=11.6, y_length=4.4, xlabel=r"",
                 ylabel=r"annualized volatility", xticks=[2022, 2023, 2024, 2025], yticks=[0.5, 1.0, 1.5],
                 xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=20).shift(DOWN * 0.6)
        ax = g.ax
        l_iv = curve(ax, t1, iv, IMP, stroke_width=2.5)
        l_rv = curve(ax, t2, rv, REA, stroke_width=2)
        leg = legend([(IMP, r"implied: Deribit DVOL (30 days ahead)"),
                      (REA, r"realized over the next 30 days (Binance, hourly)")], font_size=22)
        leg.move_to(ax.c2p(2024.9, 1.42))
        setup = wrapped_label(
            rf"Every day at 08:00 UTC from {ts_date(b['start'][0], '%B %Y')}: sell a 30-day at-the-money call at "
            rf"DVOL, hedge every hour until expiry. {b['n']:,} trades.".replace(",", "{,}", 1), 6.4, 24, GREY_A)
        setup.to_corner(UR, buff=0.35)
        with self.voiceover(
            f"Does the mechanism appear in historical prices? Every day at eight from {ts_date(b['start'][0], '%B %Y')}, price a hypothetical thirty-day dollar call using DVOL and hedge hourly on Binance: {b['n']:,} overlapping windows. DVOL is a smile-wide index, rather than an executable ATM call quote. <bookmark mark='a'/> Orange is starting DVOL; teal is realized volatility over the following thirty days, both aligned at the start. The window averages are {100 * b['mean_iv']:.0f} and {100 * b['mean_rv']:.0f} percent. <bookmark mark='b'/> Realized volatility sometimes surges above the proxy. This is a historical model experiment, with zero rates and no funding or execution constraints. The implementation aligns hourly DVOL closes at the supplied candle timestamps and interpolates twelve missing spot hours. Entry-time data availability has not been established, so it is not a point-in-time strategy backtest."
        ) as vo:
            self.play(FadeIn(g), FadeIn(setup))
            self.play(Create(l_iv), FadeIn(leg[0]), run_time=4)
            vo.wait_until("a")
            self.play(Indicate(leg[0]), run_time=1)
            self.play(Create(l_rv), FadeIn(leg[1]), run_time=3)
            vo.wait_until("b")
            spikes = np.where(rv - np.interp(t2, t1, iv) > 0.15)[0]
            if len(spikes):
                marks = VGroup(*[Dot(ax.c2p(t2[i], rv[i]), radius=0.05, color=LOSS) for i in spikes[::3]])
                self.play(LaggedStart(*[FadeIn(m, scale=2) for m in marks], lag_ratio=0.05))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scatter(self, b):
        gap = np.asarray(b["iv"], float) - np.asarray(b["rv"], float)
        pnl = np.asarray(b["pnl"], float)
        g = axes([-0.6, 0.75], [-4, 11], x_length=6.2, y_length=4.6, xlabel=r"implied minus realized volatility",
                 ylabel=r"the seller's P\&L, per 100 of BTC", xticks=[-0.4, -0.2, 0, 0.2, 0.4], yticks=[-4, 0, 4, 8],
                 xfmt=lambda v: f"{100 * v:+.0f}" if v else "0", font_size=20).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.025,
                            color=GAIN if y > 0 else LOSS, fill_opacity=0.65) for x, y in zip(gap, pnl)])
        zero = VGroup(DashedLine(ax.c2p(0, -4), ax.c2p(0, 11), color=GREY_C, stroke_width=1.2),
                      DashedLine(ax.c2p(-0.6, 0), ax.c2p(0.75, 0), color=GREY_C, stroke_width=1.2))
        corr = float(np.corrcoef(gap, pnl)[0, 1])
        res = np.asarray(b["residual"], float)
        expl = VGroup(
            MathTex(rf"\rho = {corr:.2f}", font_size=40, color=GREY_A),
            label(r"each month's P\&L, split by the ledger:", font_size=24, color=GREY_A),
            MathTex(rf"\text{{gamma}}\ {np.mean(b['gamma']):+.2f}", font_size=30, color=GAM),
            MathTex(rf"\text{{theta}}\ {np.mean(b['theta']):+.2f}", font_size=30, color=THE),
            MathTex(rf"\text{{residual}}\ {np.mean(np.abs(res)):.3f}", font_size=30, color=GREY_B),
            label(r"(averages; the residual is the mean absolute size)", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.6)
        with self.voiceover(
            f"""Each dot is one overlapping window: the volatility gap across, hedged profit per hundred up. Correlation {corr:.2f} summarizes this sample; gamma weighting makes the relation path dependent. <bookmark mark='a'/> The ledger separates gamma, theta and a residual. The displayed residual is its average absolute size, so it does not bound the largest error."""
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.0008, run_time=3))
            self.play(FadeIn(expl[0]))
            vo.wait_until("a")
            self.play(FadeIn(expl[1:], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def distribution(self, b, im):
        pnl = np.asarray(b["pnl"], float)
        lo, hi = -4, 5
        g = axes([lo, hi], [0, 1.05], x_length=7.4, y_length=3.6, xlabel=r"P\&L per 100 of BTC, one month",
                 xticks=[-4, -2, 0, 2, 4], font_size=20).to_edge(LEFT, buff=0.7).shift(DOWN * 0.4)
        h, e = np.histogram(pnl, bins=54, range=(lo, hi))
        over = int(np.sum(pnl > hi))
        h = h / h.max()
        bars = VGroup(*[Rectangle(width=g.ax.x_length / 54 * 0.94, height=max(g.ax.y_length * v, 0.002), stroke_width=0,
                                  fill_color=GAIN if (e[i] + e[i + 1]) / 2 > 0 else LOSS, fill_opacity=0.85)
                        .move_to(g.ax.c2p((e[i] + e[i + 1]) / 2, 0), aligned_edge=DOWN) for i, v in enumerate(h)])
        over_lab = label(rf"+{over} months above {hi}", font_size=22, color=GAIN).move_to(g.ax.c2p(3.7, 0.95))
        gap_pts = 100 * (im["dvol_ref"] - im["atm30"])
        adj = b["mean_cost"] - b["mean_vega"] * (im["dvol_ref"] - im["atm30"])
        stats = VGroup(
            MathTex(rf"\text{{mean}}\ {b['mean']:+.2f}", font_size=34, color=GAIN),
            label(rf"on an average premium of {np.mean(b['premium']):.2f}", font_size=22, color=GREY_A),
            MathTex(rf"\text{{winning months}}\ {100 * b['p_win']:.0f}\%", font_size=32),
            MathTex(rf"\text{{worst}}\ {b['worst']:+.2f},\ \text{{best}}\ {b['best']:+.2f}", font_size=30),
            label(rf"non-overlapping months: {b['nonoverlap_mean']:+.2f} $\pm$ {b['nonoverlap_se']:.2f} "
                  rf"(n = {b['nonoverlap_n']})", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.5).shift(UP * 1.4)
        honest = VGroup(
            label(r"Before believing it:", font_size=26, color=IMP),
            label(rf"costs of 2 bp per trade: mean {b['mean_cost']:+.2f}", font_size=22, color=GREY_A),
            label(rf"one snapshot: DVOL minus ATM = {gap_pts:.1f} points", font_size=22, color=GREY_A),
            label(rf"single-snapshot sensitivity only: {adj:+.2f}", font_size=22, color=GREY_A),
            label(r"dollar-call model; no inverse-contract hedge", font_size=22, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(stats, DOWN, buff=0.45).align_to(stats, LEFT)
        with self.voiceover(
            f"""Across {b['n']:,} windows, mean gross profit is {b['mean']:.2f} per hundred on average model premiums of {np.mean(b['premium']):.2f}; {100 * b['p_win']:.0f} percent are positive. Sampling every thirty days gives {b['nonoverlap_mean']:.2f} plus or minus {b['nonoverlap_se']:.2f}, an ordinary standard error over {b['nonoverlap_n']} non-overlapping windows. They may still be dependent. <bookmark mark='a'/> Two basis points per unit of spot traded reduce the mean to {b['mean_cost']:.2f}, excluding option spreads and funding. Our single Surface snapshot puts DVOL {gap_pts:.1f} points above ATM volatility. Applying that gap to all years is only a sensitivity illustration: {adj:.2f}, not an estimated executable return. Coin settlement also changes numeraire and hedge accounting; this dollar-call experiment does not implement the inverse contract."""
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[GrowFromEdge(x, DOWN) for x in bars], lag_ratio=0.02, run_time=2.5))
            self.play(FadeIn(over_lab))
            self.play(FadeIn(stats, shift=LEFT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(honest, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self, r):
        t = np.array([year_of(x) for x in r["start"]])
        x = np.asarray(r["pnl"], float)
        run = np.asarray(r["running"], float)
        lo, hi = np.asarray(r["lo"], float), np.asarray(r["hi"], float)
        n = len(x)
        top = axes([2021.25, 2026], [-1, 4], x_length=8.4, y_length=2.6, ylabel=r"running mean, per 100 of BTC",
                   xticks=[2022, 2023, 2024, 2025], yticks=[0, 2, 4], xfmt=lambda v: f"{int(v)}", font_size=18)
        top.to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.6)
        bot = axes([2021.25, 2026], [-6, 6], x_length=8.4, y_length=2.6, ylabel=r"each month's P\&L",
                   xticks=[2022, 2023, 2024, 2025], yticks=[-4, 0, 4], xfmt=lambda v: f"{int(v)}", font_size=18)
        bot.next_to(top, DOWN, buff=0.5).align_to(top, LEFT)
        k = ValueTracker(0)
        z1 = DashedLine(top.ax.c2p(2021.25, 0), top.ax.c2p(2026, 0), color=GREY_C, stroke_width=1.2)
        z2 = DashedLine(bot.ax.c2p(2021.25, 0), bot.ax.c2p(2026, 0), color=GREY_C, stroke_width=1.2)

        def upper():
            j = max(int(k.get_value()), 6)
            ok = slice(5, j)
            g = VGroup()
            lo_, hi_ = np.nanmin(lo[:, ok], 0), np.nanmax(hi[:, ok], 0)
            g.add(band(top.ax, t[ok], lo_, hi_, IMP, 0.25))
            g.add(curve(top.ax, t[:j], run[:j], WHITE, stroke_width=3))
            return g

        def lower():
            j = max(int(k.get_value()), 1)
            return VGroup(*[Rectangle(width=0.09, height=max(abs(bot.ax.c2p(0, v)[1] - bot.ax.c2p(0, 0)[1]), 0.01),
                                      stroke_width=0, fill_color=GAIN if v > 0 else LOSS, fill_opacity=0.9)
                            .move_to(bot.ax.c2p(a, v / 2)) for a, v in zip(t[:j], x[:j])])

        def side():
            j = min(max(int(k.get_value()), 1), n) - 1
            return VGroup(label(ts_date(r["start"][j], "%b %Y"), font_size=26, color=GREY_A),
                          MathTex(rf"\text{{gamma}}\ {r['gamma'][j]:+.2f}", font_size=28, color=GAM),
                          MathTex(rf"\text{{theta}}\ {r['theta'][j]:+.2f}", font_size=28, color=THE),
                          MathTex(rf"\text{{month}}\ {x[j]:+.2f}", font_size=28, color=GAIN if x[j] > 0 else LOSS)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.5).shift(UP * 0.4)

        up_, low_, side_ = always_redraw(upper), always_redraw(lower), always_redraw(side)
        cap = note(r"pointwise 90\% block-bootstrap intervals; 5 seeds $\times$ 200 resamples; shaded: outer envelope",
                   font_size=18).to_edge(DOWN, buff=0.25)
        fp = r["first_positive"] if r["first_positive"] is not None else r["start"][-1]
        clear_early = bool(np.nanmin(lo[:, 5]) > 0)
        band_line = (f"Even early on, the band sits above zero, and it ends between {r['final_lo']:.2f} and "
                     f"{r['final_hi']:.2f}." if clear_early else
                     f"It lifts clear of zero only from {ts_date(fp, '%B %Y')}, and ends between "
                     f"{r['final_lo']:.2f} and {r['final_hi']:.2f}.")
        with self.voiceover(
            f"""Replay all {n} non-overlapping windows. Below is each profit; on the right its gamma and theta terms. Above is the running mean with pointwise ninety-percent block-bootstrap intervals. Five seeds with two hundred resamples each show Monte Carlo variability of the intervals, not five independent market histories. <bookmark mark='a'/> {band_line} These intervals depend on the resampling assumptions, and repeated inspection is not a simultaneous confidence statement. The result describes our DVOL-priced model experiment."""
        ) as vo:
            self.play(FadeIn(top), FadeIn(bot), Create(z1), Create(z2), FadeIn(cap))
            self.add(up_, low_, side_)
            self.play(k.animate.set_value(n), run_time=max(vo.until("a") + 4.0, 10.0), rate_func=linear)
            for m_ in (up_, low_, side_):
                m_.clear_updaters()
            self.wait(max(vo.remaining(1.0) - 0.5, 0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def crisis(self, b):
        card = crisis_card(
            rf"{ts_date(b['worst_start'])} to {ts_date(b['worst_start'] + 30 * 86400)}",
            r"The worst month: the yen carry unwind",
            r"Bitcoin fell with every risk asset as the yen carry trade unwound; on 5 August 2024 the VIX printed "
            r"65 before the US open. The month sold at the lowest DVOL of the summer realized the most volatility.",
            stats=[(rf"{100 * b['worst_iv']:.0f}\%", r"implied, sold at"),
                   (rf"{100 * b['worst_rv']:.0f}\%", r"realized"),
                   (rf"{b['worst']:+.2f}", r"P\&L per 100 of BTC")],
            width=9.6, font_size=29).move_to(ORIGIN)
        with self.voiceover(
            f"The worst month began on {ts_date(b['worst_start'], '%d %B %Y').lstrip('0')}, sold at "
            f"{100 * b['worst_iv']:.0f} percent; three weeks later the yen carry trade unwound and on the fifth of "
            f"August the VIX printed sixty-five before New York opened. The month realized "
            f"{100 * b['worst_rv']:.0f} percent; the seller lost {-b['worst']:.2f}. Many small gains, and an "
            "occasional large loss exactly when everything else is losing: Part twelve's Volmageddon is the same "
            "story with leverage."
            " The formula's worst day came long before Bitcoin. Next: October 1987."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
            self.play(LaggedStart(*[Indicate(s, color=QC.CRISIS) for s in card.stats], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()
