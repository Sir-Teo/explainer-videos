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
        self.crisis(b)

    def card(self):
        c = chapter_card(11, r"Selling volatility on real Bitcoin", r"Is the implied volatility too high?",
                         lit=(2021, 2024), part=PART)
        with self.voiceover("Chapter eleven. Selling volatility on real Bitcoin."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def series(self, b):
        t1 = np.array([year_of(x) for x in b["dvol_t"]])
        t2 = np.array([year_of(x) for x in b["rv30_t"]])
        iv, rv = np.asarray(b["dvol"], float), np.asarray(b["rv30"], float)
        g = axes([2021.25, 2026], [0.15, 1.25], x_length=11.6, y_length=4.4, xlabel=r"",
                 ylabel=r"annualized volatility", xticks=[2022, 2023, 2024, 2025], yticks=[0.25, 0.5, 0.75, 1.0],
                 xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=20).shift(DOWN * 0.6)
        ax = g.ax
        l_iv = curve(ax, t1, iv, IMP, stroke_width=2.5)
        l_rv = curve(ax, t2, np.minimum(rv, 1.24), REA, stroke_width=2)
        leg = legend([(IMP, r"implied: Deribit DVOL (30 days ahead)"),
                      (REA, r"realized over the next 30 days (Binance, hourly)")], font_size=22)
        leg.move_to(ax.c2p(2024.9, 1.12))
        setup = wrapped_label(
            rf"Every day at 08:00 UTC from {ts_date(b['start'][0], '%B %Y')}: sell a 30-day at-the-money call at "
            rf"DVOL, hedge every hour until expiry. {b['n']:,} trades.".replace(",", "{,}", 1), 6.4, 24, GREY_A)
        setup.to_corner(UR, buff=0.35)
        with self.voiceover(
            "Chapter six said a hedged option seller earns the gap between implied and realized volatility. So is "
            "there a gap, on average, in a real market? The House runs the experiment on Bitcoin. Every day at "
            f"eight in the morning, from {ts_date(b['start'][0], '%B %Y')}, it sells a thirty-day at-the-money "
            "call at the volatility the market quotes, Deribit's DVOL index, and hedges it every hour on Binance's "
            f"prices until it expires: {b['n']:,} trades. <bookmark mark='a'/> In orange, the implied volatility "
            "the House sold at. In teal, the volatility Bitcoin actually realized over the following thirty days. "
            "Most of the time orange is above teal: the market charges more for volatility than Bitcoin then "
            f"delivers. On average {100 * b['mean_iv']:.0f} against {100 * b['mean_rv']:.0f} percent. "
            "<bookmark mark='b'/> But not always: when Bitcoin crashes, realized volatility jumps far above what "
            "was charged, and those are the spikes of teal above orange."
        ) as vo:
            self.play(FadeIn(g), FadeIn(setup))
            self.play(Create(l_iv), FadeIn(leg[0]), run_time=4)
            vo.wait_until("a")
            self.play(Indicate(leg[0]), run_time=1)
            self.play(Create(l_rv), FadeIn(leg[1]), run_time=3)
            vo.wait_until("b")
            spikes = np.where(rv - np.interp(t2, t1, iv) > 0.15)[0]
            if len(spikes):
                marks = VGroup(*[Dot(ax.c2p(t2[i], min(rv[i], 1.24)), radius=0.05, color=LOSS) for i in spikes[::3]])
                self.play(LaggedStart(*[FadeIn(m, scale=2) for m in marks], lag_ratio=0.05))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scatter(self, b):
        gap = np.asarray(b["iv"], float) - np.asarray(b["rv"], float)
        pnl = np.asarray(b["pnl"], float)
        g = axes([-0.5, 0.5], [-4, 11], x_length=6.2, y_length=4.6, xlabel=r"implied minus realized volatility",
                 ylabel=r"the seller's P\&L, per 100 of BTC", xticks=[-0.4, -0.2, 0, 0.2, 0.4], yticks=[-4, 0, 4, 8],
                 xfmt=lambda v: f"{100 * v:+.0f}" if v else "0", font_size=20).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(np.clip(x, -0.49, 0.49), np.clip(y, -3.9, 10.9)), radius=0.025,
                            color=GAIN if y > 0 else LOSS, fill_opacity=0.65) for x, y in zip(gap, pnl)])
        zero = VGroup(DashedLine(ax.c2p(0, -4), ax.c2p(0, 11), color=GREY_C, stroke_width=1.2),
                      DashedLine(ax.c2p(-0.5, 0), ax.c2p(0.5, 0), color=GREY_C, stroke_width=1.2))
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
            "Each dot is one month's trade: across, the gap between the implied volatility it was sold at and the "
            "volatility that followed; up, the hedged profit per hundred dollars of Bitcoin. They line up, "
            f"correlation {corr:.2f}: the profit is the volatility gap, as the formula said. The spread around the "
            "line is chapter seven's gamma weighting: when in the month the moves came. <bookmark mark='a'/> And "
            "the ledger accounts for every trade. Summed over a month, the theta term, the decay collected, and the "
            "gamma term, the squared moves paid out, explain the profit to within a few hundredths: the expansion "
            "behind the formula holds even for hourly Bitcoin."
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
            label(rf"DVOL sits about {gap_pts:.1f} points above at-the-money vol", font_size=22, color=GREY_A),
            label(rf"(it includes the smile): about {adj:+.2f} left", font_size=22, color=GREY_A),
            label(r"the left tail is where the risk lives", font_size=22, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(stats, DOWN, buff=0.45).align_to(stats, LEFT)
        with self.voiceover(
            f"Over all {b['n']:,} months the seller made {b['mean']:.2f} per hundred dollars of Bitcoin, on premiums "
            f"averaging {np.mean(b['premium']):.2f}, and won in {100 * b['p_win']:.0f} percent of them. The months "
            "overlap, so the honest statistic uses one trade per thirty days: "
            f"{b['nonoverlap_mean']:.2f} plus or minus {b['nonoverlap_se']:.2f}, over {b['nonoverlap_n']} "
            "independent months. That is the variance risk premium: people pay more for options than they are worth "
            "on average, as insurance buyers do. <bookmark mark='a'/> Before believing it, subtract what the "
            "simulation leaves out. Hedging costs, even at a market maker's two basis points a trade, take it to "
            f"{b['mean_cost']:.2f}. And DVOL, computed like the VIX from the whole smile, sat about "
            f"{gap_pts:.1f} points above the at-the-money volatility on our Surface morning; selling at the "
            f"money at that lower volatility would leave about {adj:.2f}. Still positive, and still with the left "
            "tail of the histogram: months that lose two or three times what a good month earns."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[GrowFromEdge(x, DOWN) for x in bars], lag_ratio=0.02, run_time=2.5))
            self.play(FadeIn(over_lab))
            self.play(FadeIn(stats, shift=LEFT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(honest, shift=UP * 0.2))
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
            f"The worst month began on {ts_date(b['worst_start'], '%d %B %Y').lstrip('0')}. The House sold at "
            f"{100 * b['worst_iv']:.0f} percent; three weeks later the yen carry trade unwound, Bitcoin fell with "
            "every risky asset, and on the fifth of August the VIX printed sixty-five before New York opened. That "
            f"month realized {100 * b['worst_rv']:.0f} percent, and the seller lost {-b['worst']:.2f}, more than two "
            "average months' profit. This is the shape of every insurance business, and of every short-volatility "
            "strategy in this series: many small gains, and an occasional large loss that arrives exactly when "
            "everything else is losing too. Part twelve's crisis file, Volmageddon, is the same story with "
            "leverage."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
            self.play(LaggedStart(*[Indicate(s, color=QC.CRISIS) for s in card.stats], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()
