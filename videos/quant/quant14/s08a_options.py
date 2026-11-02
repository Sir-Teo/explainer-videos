from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import (BAD, IV, MODEL_COL, OPT, PART, ROUGH, RV, VAR, illustration, load,
                                         loglog_skew_axes, pause, real_data, running_min)


class Options(VoiceoverScene):
    def construct(self):
        w = load("skew_weekly")
        b2 = load("bergomi2f")
        self.card()
        self.fans(w)
        self.board()
        self.derive()
        self.ours(b2)

    def card(self):
        c = chapter_card(12, r"The debate II: what the options say", r"Do option prices need a rough model?", part=PART)
        with self.voiceover("Chapter twelve. The debate, part two: what the options say."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def fans(self, w):
        weeks = w["weeks"]
        g = loglog_skew_axes(x_length=7.0, y_length=4.6, t_lo=2 / 365, y_range=(-1.6, 0.8)).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        lines, better = VGroup(), []
        for x in weeks:
            T = np.asarray(x["T"])
            Tf = np.exp(np.linspace(np.log(max(T.min(), 2 / 365)), np.log(T.max()), 20))
            b = x["rm_s"] < x["rm_p"] - 0.01
            better.append(b)
            y = np.clip(np.log10(x["c_s"] * (Tf + x["eps"]) ** (-x["a_s"]) if b else x["c"] * Tf ** (-x["a"])), -1.6, 0.8)
            lines.add(curve(ax, np.log10(Tf), y, GOLD if b else IV, stroke_width=1.2).set_stroke(opacity=0.5))
        eps = np.array([365 * x["eps"] for x, b in zip(weeks, better) if b])
        h = axes([0, 75], [0, max(8, int(np.histogram(eps, bins=8, range=(0, 75))[0].max()) + 1)], x_length=4.0,
                 y_length=2.4, xlabel=r"bounded form's shift $\varepsilon$ (days)", xticks=[0, 25, 50, 75], yticks=[],
                 font_size=13).to_edge(RIGHT, buff=0.5).shift(DOWN * 1.4)
        cnt, ed = np.histogram(eps, bins=8, range=(0, 75))
        bars = VGroup(*[Rectangle(width=h.ax.c2p(75 / 8, 0)[0] - h.ax.c2p(0, 0)[0] - 0.04,
                                  height=max(h.ax.c2p(0, c_)[1] - h.ax.c2p(0, 0)[1], 0.001), stroke_width=0,
                                  fill_color=GOLD, fill_opacity=0.85).move_to(h.ax.c2p(e + 75 / 16, c_ / 2))
                        for c_, e in zip(cnt, ed[:-1])])
        side = VGroup(MathTex(rf"{int(sum(better))}\ \text{{of}}\ {len(weeks)}\ \text{{weeks}}", font_size=34, color=GOLD),
                      label(r"the bounded form wins by more than 0.01 in log error", font_size=18, color=GREY_A),
                      MathTex(rf"\text{{median shift}}\ {w['eps_median_days']:.0f}\ \text{{days}}", font_size=28, color=GOLD)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(h, UP, buff=0.4).align_to(h, LEFT)
        src = real_data(r"Deribit, weekly, 2024--2025: each week's fitted term structure", corner=DL)
        share = w["bounded_share"]
        verdict = ("so for most weeks the power law is as good a description as its rival"
                   if share < 0.5 else "so for most weeks the skew does stop growing at the shortest expiries")
        with self.voiceover(
            "The options have their own say. Here are chapter one's weekly fits again, all on one chart: blue where "
            "a power law is as good as anything, gold where a skew that stops growing at short expiries wins by a "
            f"clear margin. <bookmark mark='a'/> {int(sum(better))} of {len(weeks)} weeks are gold, {verdict}. "
            "<bookmark mark='b'/> Where the bounded form wins, how far does the flattening reach? The shifts spread "
            f"widely, with a median of {w['eps_median_days']:.0f} days. Some weeks the short-end flattening is real; "
            "others, it is noise in a few thin expiries."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.02, run_time=4))
            vo.wait_until("a")
            self.play(FadeIn(side[:2]))
            vo.wait_until("b")
            self.play(FadeIn(h), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def board(self):
        cards = VGroup(
            history_card(2018, r"Livieri, Mouti, Pallavicini and Rosenbaum",
                         r"Short-dated at-the-money S\&P 500 options confirm rough volatility, with $H$ of order 0.3, "
                         r"larger than from the time series, explained by the smoothing of the remaining maturity.",
                         color=ROUGH, width=6.2, font_size=19),
            history_card(2022, r"R{\o}mer (Quantitative Finance 22(10))",
                         r"SPX options 2004--2019: one-factor rough Bergomi and rough Heston struggle to produce a strong "
                         r"enough term structure of the smile; the joint SPX--VIX problem is largely solved by a classical "
                         r"two-factor volatility, without roughness or jumps.", color=VAR, width=6.2, font_size=19),
            history_card(2023, r"Guyon and El Amrani (Risk, Cutting Edge)",
                         r"S\&P 500, Euro Stoxx 50 and DAX, 2020--21: a two-parameter power law fails for the ATM skew "
                         r"once short maturities are included.", color=VAR, width=6.2, font_size=19),
            history_card(2025, r"Abi Jaber and Li (Mathematical Finance 35(4))",
                         r"Rough models are inconsistent with the global shape of SPX smiles; from 1 week to 3 months "
                         r"they lose to one-factor Markov models, and a path-dependent and a two-factor Markov model with "
                         r"3--4 parameters win from 1 week to 3 years.", color=VAR, width=6.2, font_size=19))
        grid = VGroup(VGroup(cards[0], cards[1]).arrange(RIGHT, buff=0.3, aligned_edge=UP),
                      VGroup(cards[2], cards[3]).arrange(RIGHT, buff=0.3, aligned_edge=UP)).arrange(DOWN, buff=0.25)
        if grid.height > 7.2:
            grid.scale_to_fit_height(7.2)
        grid.move_to(ORIGIN)
        with self.voiceover(
            "The published horse races. In 2018 Giulia Livieri, Saad Mouti, Andrea Pallavicini and Mathieu "
            "Rosenbaum read roughness off short-dated S&P options: H of order three-tenths, larger than the time "
            "series, which they explained by the smoothing of the option's own maturity. <bookmark mark='a'/> "
            "Sigurd Rømer calibrated fifteen years of S&P options and found one-factor rough models too weak in the "
            "term structure of the smile, while a classical two-factor model fitted S&P and VIX together. Risk named "
            "him its 2023 Rising Star in quant finance. <bookmark mark='b'/> Guyon and El Amrani showed the power "
            "law failing at the short end. <bookmark mark='c'/> And in 2025 Eduardo Abi Jaber and Shaun Li found "
            "rough models inconsistent with the global shape of S&P smiles, beaten by a path-dependent model and a "
            "two-factor Markov model with three or four parameters. The options side of the debate leans against "
            "one-factor rough models."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[3], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"K(\tau)", r"=", r"\eta_1 e^{-\kappa_1\tau} + \eta_2 e^{-\kappa_2\tau}", font_size=40,
                      colors={r"K(\tau)": VAR}),
                cmath(r"\psi(T)", r"\propto", r"\sum_{i = 1}^2 \eta_i\Big(\frac{1}{\kappa_i T} - \frac{1 - e^{-\kappa_i T}}"
                      r"{\kappa_i^2 T^2}\Big)", font_size=38, colors={r"\psi(T)": IV}),
                cmath(r"\kappa_1 \approx 50,\ \kappa_2 \approx 1", r"\Rightarrow", r"\psi \approx T^{-0.4}\ \text{on [1 week, 1 year]}",
                      font_size=36, colors={r"\kappa_1 \approx 50,\ \kappa_2 \approx 1": VAR})]
        whys = [why(r"a two-factor Bergomi model: two exponential kernels, a fast one and a slow one, still Markov"),
                why(r"chapter 2's first-order formula, term by term"),
                why(r"each term is flat below $1/\kappa_i$ and falls like $1/T$ above: two scales a decade or two apart "
                    r"imitate a power law between them")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-1.2, buff=0.8, edge=6.9)
        q = pause(r"Two factors with half-lives of 5 days and 1 year. Can they fake a power-law skew from 1 week to 6 months?",
                  width=7.4, font_size=22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Why can a classical two-factor model compete? Give Bergomi's kernel two exponentials, a fast one and a "
            "slow one. <bookmark mark='a'/> Chapter two's formula, applied term by term, gives a sum of two "
            "skews, each flat below its own time scale and falling like one over T above it. <bookmark mark='b'/> "
            "Pause and predict: with half-lives of five days and a year, can the pair fake a power law from a week "
            "to six months? <bookmark mark='c'/> Approximately, yes: between the two time scales, the sum bends "
            "smoothly from one regime to the other, and on a log-log chart it looks straight. It is the lift of "
            "chapter ten with two factors, and no claim of roughness."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("c")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def ours(self, b2):
        curve_ = running_min(b2["curve"])
        steps = np.arange(len(curve_))
        best = b2["best"]
        idx = sorted(set([0, 1, len(best) // 2, len(best) - 1]))
        ck = [best[i]["eval"] for i in idx]
        names = [r"$\kappa_1$", r"$\kappa_2$", r"$\eta_1$", r"$\eta_2$", r"$\rho$"]

        def frame(j):
            x = best[idx[j]]["x"]
            return VGroup(*[MathTex(rf"{n_[1:-1]} = {v:.2f}", font_size=30, color=VAR) for n_, v in zip(names, x)]).arrange(
                DOWN, aligned_edge=LEFT, buff=0.18)

        rp = TrainingReplay(steps, curve_, frame, ck, ylabel=r"fit error (vol points)", xlabel=r"model evaluation",
                            color=VAR, left=LEFT * 4.2, right=RIGHT * 2.6, x_length=5.6, y_length=3.0)
        rp.to_edge(UP, buff=0.6)
        rh = load("rheston")
        pr = next(r for r in load("rprofile")["rows"] if abs(r["H"] - 0.1) < 1e-9)
        rbm = b2["rbergomi_rmse"]
        rs = load("rbskew")
        rows = [(r"rough Bergomi (3 numbers + curve)", rbm, MODEL_COL["rBergomi"]),
                (r"two-factor Bergomi (5 numbers + curve)", b2["rmse"], VAR),
                (r"rough Heston, free (6)", rh["rmse"], MODEL_COL["rough Heston"]),
                (r"Heston (5)", rs["heston_rmse_same"], MODEL_COL["Heston"]),
                (r"rough Heston, $H = 0.1$ (5)", pr["rmse"], ROUGH)]
        tab = VGroup(*[VGroup(label(n_, font_size=19, color=c), MathTex(f"{v:.2f}", font_size=26, color=c)).arrange(RIGHT, buff=0.3)
                       for n_, v, c in sorted(rows, key=lambda r: r[1])]).arrange(DOWN, aligned_edge=RIGHT, buff=0.14)
        cap = label(r"our board: error on the Surface, vol points, re-priced on fresh paths", font_size=18, color=GREY_A)
        board = VGroup(cap, tab).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35)
        hl = b2["half_lives_days"]
        beats = b2["rmse"] < rbm
        verdict = ("the two-factor model beats rough Bergomi on our Surface, as Abi Jaber and Li found on the S&P"
                   if beats else "rough Bergomi still wins on our Surface, with fewer numbers")
        src = real_data(r"the Surface; 20{,}000 paths, common random numbers; Part 13's variance curve", corner=DR)
        with self.voiceover(
            "Now our own race, on the Surface's quotes. A two-factor Bergomi model with Part thirteen's variance "
            "curve, five numbers fitted by least squares on twenty thousand paths, the fit replayed. "
            "<bookmark mark='a'/> The fitted half-lives are "
            f"{hl[0]:.1f} days and {hl[1]:.0f} days: one fast factor and one slow one, as the algebra suggested. "
            f"<bookmark mark='b'/> Re-priced on fresh paths its error is {b2['rmse']:.2f} volatility points, against "
            f"rough Bergomi's {rbm:.2f}. So {verdict}. One day of one market settles nothing; the honest "
            "reading is that rough and multi-factor models are close competitors on prices, and the choice turns on "
            "dynamics, speed and hedging."
            " A third view says volatility is driven by the price path itself. Next."
        ) as vo:
            self.play(FadeIn(rp), FadeIn(src))
            rp.play(self, run_time=6)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(board))
        self.wait(0.4)
        self.clear_scene()
