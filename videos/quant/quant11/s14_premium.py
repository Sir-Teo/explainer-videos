from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant11.common import (ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, load, pause, real_data)


class Premium(VoiceoverScene):
    def construct(self):
        p = load("premium")
        self.card()
        self.ledgers(p)
        self.papers(p)
        self.derive(p)

    def card(self):
        c = chapter_card(6, r"The volatility premium in option returns", r"What does buying options earn?", part=PART)
        with self.voiceover("Chapter six. The volatility risk premium, in option returns."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def ledgers(self, p):
        book = np.asarray(p["book"])          # weeks x days (0..28)
        pnl = np.asarray(p["pnl"])
        n, nd = book.shape
        cols, rws = 8, 12
        cw, ch = 0.62, 0.36
        sc = 8.0
        origin = np.array([-6.4 + cw / 2, 3.0, 0])
        grid = VGroup()
        for j in range(n):
            r_, c_ = j // cols, j % cols
            grid.add(Rectangle(width=cw - 0.06, height=ch - 0.08, stroke_color=GREY_D, stroke_width=1).move_to(
                origin + np.array([c_ * cw, -r_ * ch, 0])))
        w = ValueTracker(0.0)

        def fills():
            gr = VGroup()
            now = w.get_value()
            for j in range(n):
                prog = float(np.clip((now - j) / 4.0, 0, 1))
                if prog <= 0:
                    continue
                v = at_index(book[j], ValueTracker(prog * (nd - 1)))
                frac = float(np.clip(abs(v) / sc, 0.04, 1))
                cell = grid[j]
                ww = (cw - 0.1) * frac
                gr.add(Rectangle(width=ww, height=ch - 0.14, stroke_width=0, fill_color=QC.GAIN if v > 0 else QC.LOSS,
                                 fill_opacity=0.35 + 0.5 * prog).move_to(cell.get_left() + RIGHT * (ww / 2 + 0.03)))
            return gr
        f = always_redraw(fills)
        g = axes([0, n], [-4, 2], x_length=4.6, y_length=3.0, xlabel=r"weeks completed", ylabel=r"running mean, per 100",
                 xticks=[0, 48, 96], yticks=[-4, -2, 0, 2], font_size=15).to_corner(UR, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        k = np.arange(1, n + 1)
        rm = np.cumsum(pnl) / k
        sd = np.array([pnl[:i].std(ddof=1) if i > 1 else 0 for i in k])
        se = 2 * sd / np.sqrt(k) * np.sqrt(4)      # four-week windows overlap: about four times the variance
        lo, hi = np.clip(rm - se, -4, 2), np.clip(rm + se, -4, 2)
        zl = DashedLine(ax.c2p(0, 0), ax.c2p(n, 0), color=GREY_C, stroke_width=1.5)

        def runner():
            m = int(np.clip(w.get_value() - 4, 0, n))
            if m < 3:
                return VGroup()
            return VGroup(band(ax, k[2:m], lo[2:m], hi[2:m], VEGA, 0.25), curve(ax, k[:m], np.clip(rm[:m], -4, 2), VEGA))
        rl = always_redraw(runner)
        side = VGroup(
            MathTex(rf"\text{{mean }} {p['mean']:+.2f},\ \ t_{{NW}} = {p['t']:.1f}", font_size=30, color=VEGA),
            label(rf"positive in {100 * p['share_pos']:.0f}\% of weeks", font_size=22, color=GREY_A),
            wrapped_label(rf"realized below the 28-day ATM implied in {100 * p['share_rv_below']:.0f}\% of the windows",
                          4.6, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(g, DOWN, buff=0.45).align_to(g, LEFT)
        src = real_data(r"a straddle bought at the 28-day ATM implied of each Wednesday's Deribit smile, hedged hourly "
                        r"on Binance, 2024--2025")
        tsay = (f"The mean is {p['mean']:.2f} per hundred of Bitcoin, with a Newey-West t-statistic of {p['t']:.1f}: "
                "buying volatility and hedging it lost money, reliably." if p["t"] < -2 else
                f"The mean is {p['mean']:.2f}, with a t-statistic of only {p['t']:.1f}: too noisy to call.")
        with self.voiceover(
            "Chapter five's straddles were not hedged. Now hedge them. Every Wednesday, buy a four-week straddle at "
            "the market's own at-the-money implied volatility, and hedge it every hour. Each cell is one trade's "
            "ledger, filling in green or red as its four weeks pass. <bookmark mark='a'/> Two years go by. Most "
            "cells end red. <bookmark mark='b'/> On the right, the running average of the finished trades with a "
            f"two-standard-error band, settling below zero. {tsay} <bookmark mark='c'/> This is measured at the "
            "market's own smile, not at the volatility index, so it complements Part twelve's variance-swap premium: "
            "the same premium, seen through an option a trader can actually buy."
        ) as vo:
            self.play(FadeIn(grid), FadeIn(g), Create(zl), FadeIn(src))
            self.add(f, rl)
            self.play(w.animate.set_value(n * 0.6), run_time=vo.until("a"), rate_func=linear)
            self.play(w.animate.set_value(n + 4), run_time=vo.until("b"), rate_func=linear)
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side], lag_ratio=0.4, run_time=2))
            vo.wait_until("c")
        f.clear_updaters()
        rl.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def papers(self, p):
        cards = VGroup(
            theorem_card(r"Coval and Shumway (2001)", r"Zero-beta, at-the-money S\&P 500 straddles lost about 3\% a "
                         r"week on average: some risk beyond the market's beta, such as volatility, is priced.",
                         who=r"\textit{Expected option returns}, Journal of Finance", color=QC.IDEA, width=6.2,
                         font_size=21),
            theorem_card(r"Bakshi and Kapadia (2003)", r"Delta-hedged gains of S\&P 500 options are negative, most "
                         r"of all at the money and when volatility is high: the market price of volatility risk is "
                         r"negative.", who=r"\textit{Delta-hedged gains and the negative market volatility risk premium}, "
                         r"RFS", color=QC.IDEA, width=6.2, font_size=21),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).to_edge(UP, buff=0.45)
        if cards.width > 13.0:
            cards.scale_to_fit_width(13.0)
        btc = VGroup(
            label(r"bitcoin, 2024--2025, the same 96 weeks:", font_size=22, color=GREY_A),
            label(rf"unhedged straddle: mean return {100 * p['straddle_ret_mean']:+.0f}\% of the premium per four "
                  rf"weeks, median {100 * p['straddle_ret_median']:+.0f}\% ($t = {p['straddle_ret_t']:.1f}$)",
                  font_size=21, color=OPT),
            label(rf"delta-hedged: mean {p['mean']:+.2f} per 100, $t = {p['t']:.1f}$", font_size=21, color=VEGA),
            wrapped_label(r"the hedge removes the direction, the noise that hides the premium: the same sign, now "
                          r"visible", 11.0, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(cards, DOWN, buff=0.5)
        hsay = ("the hedged one shows it clearly" if p["t"] < -2 else "even hedged it is hard to see")
        with self.voiceover(
            "The academic record says the same. Joshua Coval and Tyler Shumway found in 2001 that at-the-money S&P "
            "500 straddles, built to have no market exposure, lost about three percent a week on average. "
            "<bookmark mark='a'/> Gurdip Bakshi and Nikunj Kapadia hedged them instead, in 2003: the delta-hedged "
            "gains were negative, most of all at the money, which is exactly what a negative price of volatility "
            "risk predicts. <bookmark mark='b'/> On Bitcoin over the same ninety-six weeks, the unhedged straddle "
            f"lost {100 * -p['straddle_ret_mean']:.0f} percent of its premium per four weeks on average, with a median "
            f"of {100 * p['straddle_ret_median']:.0f} percent, too noisy to call; {hsay}. Hedging strips out the "
            "direction, the noise that hides the premium."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in btc], lag_ratio=0.4, run_time=3))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self, p):
        rows = [
            cmath(r"\Pi_T", r"=", r"\int_0^T \tfrac12\,\Gamma_t S_t^2\left(\sigma_{r,t}^2 - \sigma_i^2\right)dt + "
                  r"\varepsilon", font_size=36, colors={r"\Pi_T": OPT}),
            cmath(r"\mathbb{E}^P[\Pi_T] < 0", r"\iff", r"\sigma_i^2 > \mathbb{E}^P_{\Gamma}\big[\sigma_r^2\big]",
                  font_size=36, colors={r"\mathbb{E}^P[\Pi_T] < 0": QC.P}),
            cmath(r"\mathbb{E}^Q[\Pi_T]", r"=", r"0", font_size=38, colors={r"\mathbb{E}^Q[\Pi_T]": QC.Q}),
            cmath(r"\mathbb{E}^P[\Pi_T] - \mathbb{E}^Q[\Pi_T]", r"=", r"\text{the price of variance risk} < 0",
                  font_size=36),
        ]
        whys = [why(r"Part 10's hedger's identity: the hedged option collects gamma-weighted realized minus implied "
                    r"variance"),
                why(r"so it loses on average exactly when implied exceeds the gamma-weighted expected realized variance"),
                why(r"under the pricing measure a self-financing hedged position is a martingale started at zero"),
                why(r"the gap between the two measures is a risk premium: sellers are paid to carry variance risk, which "
                    r"rises in crashes, when money is worth most")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-0.4, buff=0.55, edge=6.9)
        pc = pause(r"If the premium is so reliable, why doesn't everyone sell straddles?", width=5.2, font_size=22)
        with self.voiceover(
            "Why is it a premium and not a mistake? Start from Part ten's identity: the hedged option collects "
            "gamma-weighted realized variance minus implied variance. <bookmark mark='a'/> So it loses on average "
            "exactly when implied variance is above the realized variance one expects, weighted by gamma. "
            "<bookmark mark='b'/> Under the pricing measure, Q, a hedged, self-financing position is a martingale "
            "that starts at zero: its expectation is zero. <bookmark mark='c'/> The negative average under the real "
            "world measure, P, is therefore the difference between the two measures: a risk premium. Sellers of "
            "volatility are paid for bearing variance risk, which explodes in crashes, exactly when money is worth "
            "most. <bookmark mark='d'/> Pause and predict: if it is so reliable, why doesn't everyone sell straddles? "
            "Chapter sixteen answers with two funds that did."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(pc))
        self.wait(0.4)
        self.clear_scene()
