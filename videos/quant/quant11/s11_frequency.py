from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant11.common import (ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, day_str, load, pause, real_data)

RULES = [("hourly", r"every hour", GAMMA), ("daily", r"once a day", VEGA), ("2% moves", r"on 2\% moves", ALT)]


class Frequency(VoiceoverScene):
    def construct(self):
        f = load("frequency")
        self.card()
        self.race(f)
        self.scatter(f)
        self.derive(f)

    def card(self):
        c = chapter_card(3, r"How often to hedge", r"Hourly, daily, or when the price moves?", part=PART)
        with self.voiceover("Chapter three. How often to hedge."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def race(self, f):
        p = np.asarray(f["race_path"])
        H = len(p) - 1
        t = np.arange(H + 1) / 24
        sub = np.arange(0, H + 1, 2)
        g1 = axes([0, 30], [p.min() * 0.97, p.max() * 1.03], x_length=6.6, y_length=2.1, ylabel=r"bitcoin (per 100)",
                  xticks=[0, 10, 20, 30], yticks=[90, 100, 110, 120, 130], font_size=15)
        g2 = axes([0, 30], [-1, 1], x_length=6.6, y_length=2.1, ylabel=r"hedge held (units)",
                  xticks=[0, 10, 20, 30], yticks=[-1, 0, 1], font_size=15)
        VGroup(g1, g2).arrange(DOWN, buff=0.45).to_edge(LEFT, buff=0.6).shift(DOWN * 0.15)
        tr = ValueTracker(0.0)
        ls = tracing(g1.ax, t[sub], p[sub], tr, SPOT, stroke_width=2.5)
        hs = VGroup(*[tracing(g2.ax, t[sub], np.clip(np.asarray(f[f"race shares {k}"])[sub], -1, 1), tr, c,
                              stroke_width=2.2) for k, _, c in RULES])
        books = {k: np.asarray(f[f"race book {k}"])[sub] for k, _, _ in RULES}
        lo = min(b.min() for b in books.values())
        hi = max(b.max() for b in books.values())
        sc = max(abs(lo), abs(hi)) * 1.1
        rows = VGroup()
        for k, txt, c in RULES:
            nm = label(txt, font_size=21, color=c)
            rows.add(nm)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.55).to_edge(RIGHT, buff=3.4).shift(UP * 0.4)
        zero_x = rows.get_right()[0] + 1.5
        zl = Line([zero_x, rows.get_top()[1] + 0.3, 0], [zero_x, rows.get_bottom()[1] - 0.3, 0], color=GREY_C)

        def bar(k, c, y):
            def make():
                v = at_index(books[k], tr)
                w = float(np.clip(v / sc, -1, 1)) * 1.4
                return Rectangle(width=max(abs(w), 0.01), height=0.32, stroke_width=0, fill_color=c,
                                 fill_opacity=0.85).move_to([zero_x + w / 2, y, 0])
            return always_redraw(make)
        bars = VGroup(*[bar(k, c, r_.get_y()) for (k, _, c), r_ in zip(RULES, rows)])
        nums = VGroup(*[always_redraw(lambda k=k, c=c, y=r_.get_y(): MathTex(f"{at_index(books[k], tr):+.2f}",
                                                                             font_size=24, color=c).move_to(
            [zero_x + 2.0, y, 0])) for (k, _, c), r_ in zip(RULES, rows)])
        head = label(r"the hedged straddle's P\&L so far", font_size=20, color=GREY_A).next_to(rows, UP, buff=0.4).align_to(
            rows, LEFT)
        n_mv = int(np.sum(np.abs(np.diff(np.asarray(f["race shares 2% moves"]))) > 1e-12))
        foot = wrapped_label(rf"one month from {day_str(f['race_start'])}: implied {100 * f['race_iv']:.0f}\%, realized "
                             rf"{100 * f['race_rv']:.0f}\%; the 2\% rule traded {n_mv} times, the hourly hedger 720",
                             5.6, 19, GREY_B).to_edge(RIGHT, buff=0.4).to_edge(DOWN, buff=0.9)
        src = real_data(r"Binance BTCUSDT hourly; Deribit DVOL; the House's \texttt{delta\_hedge}")
        ends = [books[k][-1] for k, _, _ in RULES]
        spread = max(ends) - min(ends)
        race_say = (f"They end within {spread:.1f} of each other: on one month, the order of "
                    "the moves matters more than the rule." if spread < 2 else
                    f"They end {spread:.1f} apart: on one month, the rule's timing can matter a lot.")
        with self.voiceover(
            "Part ten showed that hedging at discrete times leaves an error. So how often should a scalper hedge? "
            "Race three of them on the same month and the same straddle. One rehedges every hour, in gold; one once a "
            "day, in blue; and one only when the price has moved two percent since its last trade, in green. "
            "<bookmark mark='a'/> Watch their hedges: the hourly one is a smooth curve, the daily one a staircase, "
            "and the move-triggered one steps only when something happens. <bookmark mark='b'/> Their ledgers race "
            f"beside them. {race_say}"
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(src), FadeIn(rows), FadeIn(head), Create(zl))
            self.add(ls, hs, bars, nums)
            self.play(tr.animate.set_value(len(sub) * 0.45), run_time=vo.until("a"), rate_func=linear)
            self.play(tr.animate.set_value(len(sub) * 0.8), run_time=vo.until("b"), rate_func=linear)
            self.play(tr.animate.set_value(len(sub) - 1), FadeIn(foot), run_time=max(vo.remaining(1.0) - 0.3, 1.0))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scatter(self, f):
        gap = (np.asarray(f["rv"]) - np.asarray(f["iv"])) * 100
        st = {(r_["rule"], r_["cost"]): r_ for r_ in f["stats"]}
        g = axes([-60, 80], [-20, 20], x_length=6.8, y_length=4.6, xlabel=r"realized minus implied vol (points)",
                 ylabel=r"hedged straddle P\&L, per 100", xticks=[-40, 0, 40, 80], yticks=[-20, -10, 0, 10, 20],
                 font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        n = len(gap)
        tr = ValueTracker(0)

        def cloud(k, c):
            y = np.clip(np.asarray(f[f"pnl {k} 0.0"]), -20, 20)
            x = np.clip(gap, -60, 80)

            def make():
                m = int(tr.get_value())
                return VGroup(*[Dot(ax.c2p(x[i], y[i]), radius=0.03, color=c, fill_opacity=0.7) for i in range(m)])
            return always_redraw(make)
        clouds = VGroup(*[cloud(k, c) for k, _, c in RULES])
        tab = VGroup(label(r"rule", font_size=19, color=GREY_B), label(r"mean", font_size=19, color=GREY_B),
                     label(r"s.d.", font_size=19, color=GREY_B), label(r"corr.", font_size=19, color=GREY_B),
                     label(r"mean, 10 bp", font_size=19, color=GREY_B))
        for k, txt, c in RULES:
            a, b = st[(k, 0.0)], st[(k, 0.001)]
            tab.add(label(txt, font_size=19, color=c), MathTex(f"{a['mean']:+.2f}", font_size=24, color=c),
                    MathTex(f"{a['sd']:.2f}", font_size=24, color=c), MathTex(f"{a['corr']:.2f}", font_size=24, color=c),
                    MathTex(f"{b['mean']:+.2f}", font_size=24, color=c))
        tab.arrange_in_grid(rows=4, cols=5, buff=(0.3, 0.22), col_alignments="lcccc").to_edge(RIGHT, buff=0.35)
        tab.shift(UP * 1.2)
        tsig = abs(f["diff_hd_t"]) >= 2
        verdict = (rf"hourly minus daily: {f['diff_hd_mean']:+.2f}, $t = {f['diff_hd_t']:.1f}$: frequency changed the "
                   r"mean" if tsig else rf"hourly minus daily: {f['diff_hd_mean']:+.2f}, $t = {f['diff_hd_t']:.1f}$: "
                   r"no difference in the mean, only in the spread")
        side = VGroup(wrapped_label(verdict, 5.4, 20, GREY_A),
                      wrapped_label(r"with a 10 bp cost on every trade, the hourly hedger pays for its precision", 5.4,
                                    20, THETA)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.4)
        side.align_to(tab, LEFT)
        src = real_data(rf"{f['n']} thirty-day straddles at DVOL, started weekly, April 2021--November 2025")
        h, d = st[("hourly", 0.0)], st[("daily", 0.0)]
        hc, dc = st[("hourly", 0.001)], st[("daily", 0.001)]
        mean_say = ("The means barely differ: hedging more often does not make the trade better on average. "
                    if not tsig else "Here the means do differ, by more than their noise. ")
        with self.voiceover(
            f"Now every month. Buy a thirty-day straddle at DVOL every week from April 2021 to November 2025, {f['n']} "
            "of them, and hedge each with the three rules. Each dot is one straddle: its profit against how much "
            "realized volatility beat implied. <bookmark mark='a'/> The clouds line up along the gap, as Part ten's "
            f"identity says they must. {mean_say}<bookmark mark='b'/> What frequency buys is precision. The standard "
            f"deviation falls from {d['sd']:.2f} for daily hedging to {h['sd']:.2f} for hourly, and the profit tracks "
            f"the volatility gap more tightly: correlation {d['corr']:.2f} against {h['corr']:.2f}. "
            "<bookmark mark='c'/> And precision costs money. Charge ten basis points a trade and the hourly hedger's "
            f"mean falls to {hc['mean']:.2f}, against {dc['mean']:.2f} for the daily one. All the means are negative "
            "for the same reason: DVOL sat above what was realized, the premium of chapter six."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(tab[:5]))
            self.add(clouds)
            self.play(tr.animate.set_value(n), run_time=vo.until("a"), rate_func=linear)
            self.play(LaggedStart(*[FadeIn(m) for m in tab[5:]], lag_ratio=0.05, run_time=2))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
        clouds.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self, f):
        rows = [
            cmath(r"\epsilon_k", r"\approx", r"\tfrac12\Gamma S^2\left(r_k^2 - \sigma^2\Delta t\right),\quad "
                  r"\operatorname{sd}\Big(\sum_k \epsilon_k\Big) \propto \sqrt{\Delta t}", font_size=34),
            cmath(r"\operatorname{Var}\Big(\sum_{j=1}^{24} r_j\Big)", r"=",
                  r"24\,\sigma_h^2\Big(1 + 2\sum_{j}\big(1 - \tfrac{j}{24}\big)\rho_j\Big)", font_size=34),
            cmath(r"\text{gain from hourly}", r"\approx", r"\tfrac12\Gamma S^2\left(24\,\sigma_h^2 - \sigma_d^2\right)"
                  r"\ \text{per day}", font_size=34),
            cmath(r"\text{trade when } \left|S/S_{\text{last}} - 1\right| > h", r"\Rightarrow",
                  r"\text{each trade locks} \approx \tfrac12\Gamma S^2 h^2", font_size=34),
        ]
        whys = [why(r"Part 10: each step's error is gamma times the surprise in the squared move; their sum shrinks "
                    r"like the square root of the step"),
                why(r"the variance of a sum: if hourly returns are negatively autocorrelated, a day varies less than "
                    r"24 hours do"),
                why(r"the hourly hedger is paid the hourly variance; the daily one only the daily"),
                why(r"Zakamouline (2006) and the practitioners' rule: hedge on a band in spot, not on the clock")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-0.6, buff=0.55, edge=6.9)
        vr = f["variance_ratio"]
        pc = pause(r"If bitcoin trends within the day, does hedging more often help the long-gamma trader?",
                   width=5.0, font_size=21)
        vr_say = (f"For Bitcoin from 2021 to 2025 the daily variance is {vr:.3f} times twenty-four hourly ones: a "
                  "trace of mean reversion inside the day, too small to matter." if 0.95 < vr < 1.05 else
                  f"For Bitcoin from 2021 to 2025 the ratio is {vr:.3f}: the frequency changes what you are paid.")
        with self.voiceover(
            "Why does frequency buy precision and not profit? Each hedging step leaves an error, gamma times the "
            "surprise in the squared move; their sum shrinks like the square root of the step, but its mean is "
            "zero. <bookmark mark='a'/> The mean changes only if returns are correlated in time. The variance of a "
            "day is twenty-four hourly variances, adjusted by the autocorrelations. <bookmark mark='b'/> If hourly "
            "returns mean-revert, the hourly hedger is paid more variance than the daily one. "
            f"{vr_say} <bookmark mark='c'/> And the move-triggered rule trades only when a move of h has happened, "
            "locking in about one half gamma S squared h squared each time: fewer trades, the same precision. "
            "<bookmark mark='d'/> Pause and predict: if Bitcoin trended within the day, would hedging more often "
            "help a long-gamma trader? No: with positive autocorrelation the daily hedger lets the trend run, and "
            "collects more."
            " Delta and gamma are the price risks. Next: the volatility risks, vega, vanna and volga."
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
