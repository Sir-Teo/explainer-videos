from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, GOOD, PART, RISKY, SAFE, ask, fit_right, illustration, load


class Altman(VoiceoverScene):
    def construct(self):
        m = load("models")
        d = load("dataset")
        self.card()
        self.z()
        self.zones(m)
        self.refit(load("altfit"))
        self.ratios(d)

    def card(self):
        c = chapter_card(8, r"Altman's Z", r"Can five ratios predict bankruptcy?", part=PART)
        with self.voiceover("Chapter eight. Altman's Z: predicting bankruptcy from five numbers in the accounts."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def z(self):
        rows = [cmath(r"Z", r"=", r"1.2\,\frac{\text{WC}}{\text{TA}} + 1.4\,\frac{\text{RE}}{\text{TA}} + 3.3\,"
                      r"\frac{\text{EBIT}}{\text{TA}} + 0.6\,\frac{\text{ME}}{\text{TL}} + 1.0\,\frac{\text{Sales}}{\text{TA}}",
                      font_size=34, colors={r"Z": RISKY}),
                cmath(r"Z < 1.81", r"\ ", r"\text{distress};\quad 1.81 \le Z < 2.99\ \text{grey};\quad Z \ge 2.99\ "
                      r"\text{safe}", font_size=32, colors={r"Z < 1.81": BAD})]
        whys = [why(r"Altman (1968): linear discriminant analysis on 66 manufacturers, half of them bankrupt: working "
                    r"capital, retained earnings, operating profit and sales over assets, and the market value of "
                    r"equity over total liabilities"),
                why(r"the zones of the original paper. No parameters are fitted here: the 1968 formula, applied to every "
                    r"filer since 2010")]
        step = ladder(self, rows, whys, keep=2, top=2.6, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "In 1968 Edward Altman took sixty-six manufacturing companies, half of which had gone bankrupt, and found "
            "the weighted sum of five ratios that best separated them: liquidity, accumulated profits, operating "
            "profit, the market's cushion over the debt, and sales, each scaled by size. <bookmark mark='a'/> Below "
            "1.81, distress; above 2.99, safe. We fit nothing: the formula of 1968, applied to every company in the "
            "dataset, fifty years and a different economy later."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def zones(self, m):
        z = m["zones"]
        res = m["results"]
        rates = [z["distress"], z["grey"], z["safe"]]
        share = z["share"]
        cols = [BAD, QC.IMPLIED, SAFE]
        names = [r"distress, $Z < 1.81$", r"grey, $1.81$--$2.99$", r"safe, $Z \ge 2.99$"]
        g = axes([0.4, 3.6], [0, 2.4], x_length=6.0, y_length=4.2, xlabel=r"", ylabel=r"bankruptcy rate, \% a year",
                 xticks=[], yticks=[0, 0.5, 1.0, 1.5, 2.0], font_size=14).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for i, (r_, c_, n_, sh) in enumerate(zip(rates, cols, names, share)):
            x = i + 1
            b_ = Rectangle(width=0.7, height=max(ax.c2p(0, 100 * r_)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                           fill_color=c_, fill_opacity=0.8).move_to([ax.c2p(x, 0)[0], (ax.c2p(0, 100 * r_)[1] +
                                                                                      ax.c2p(0, 0)[1]) / 2, 0])
            bars.add(VGroup(b_, MathTex(rf"{100 * r_:.2f}\%", font_size=24).next_to(b_, UP, buff=0.1),
                            label(n_, font_size=16).next_to(ax.c2p(x, 0), DOWN, buff=0.2),
                            label(rf"{100 * sh:.0f}\% of firms", font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN,
                                                                                                     buff=0.55)))
        h = res["holdout"]
        side = VGroup(
            MathTex(rf"\text{{AUC, 2021--23: }} {h['auc']['altman']:.3f}", font_size=28, color=RISKY),
            wrapped_label(rf"{h['n']:,} firm-years and {h['defaults']} bankruptcies in the sealed years. The zones still "
                          r"sort risk, but more than half of today's filers sit in 'distress': Altman's sample was "
                          r"manufacturers, today's filers include many young firms with no profits yet. The safe zone "
                          r"is not safer than the grey one", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "On the sealed years, 2021 to 2023: <bookmark mark='a'/> companies in Altman's distress zone filed for "
            f"bankruptcy at {100 * rates[0]:.1f} percent a year, those above it at a fraction of that. "
            "<bookmark mark='b'/> Ranking every firm by Z, the chance that a random bankrupt firm scores below a "
            f"random survivor, the area under the curve, is {h['auc']['altman']:.2f}. But {100 * share[0]:.0f} percent "
            "of today's filers are in the distress zone: Altman studied manufacturers, and many of today's public "
            "companies are young firms with no profits yet. The weights have aged; the idea has not."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def refit(self, a):
        names = [r"WC/TA", r"RE/TA", r"EBIT/TA", r"ME/TL", r"Sales/TA"]
        bs = np.asarray(a["beta_std"])
        hx = [-4.4, -1.6, 1.4]
        heads = [r"ratio", r"Altman's weight (1968)", r"logit, per s.d. (2010--16)"]
        rows = VGroup(VGroup(*[label(h_, font_size=19, color=GREY_A).move_to([x, 2.1, 0]) for h_, x in zip(heads, hx)]))
        for i, (n_, w_, b_) in enumerate(zip(names, a["altman"], bs)):
            y = 1.4 - 0.55 * i
            rows.add(VGroup(MathTex(n_.replace("/", r"/"), font_size=26).move_to([hx[0], y, 0]),
                            MathTex(f"{w_:+.1f}", font_size=26).move_to([hx[1], y, 0]),
                            MathTex(f"{-b_:+.2f}", font_size=26, color=SAFE if -b_ > 0 else BAD).move_to([hx[2], y, 0])))
        v = a["auc_val"]
        foot = wrapped_label(
            rf"signs flipped so that, like Z, positive means safer. On the validation years (2017--20; the sealed "
            rf"years are not used again) the re-weighted ratios score AUC {v['refit']:.3f} against {v['altman_1968']:.3f} "
            r"for the 1968 weights. Working capital and operating profit carry most of the information; retained "
            r"earnings and sales almost none once the others are known", 12.4, 18, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "How much of the formula's age shows? Keep Altman's five ratios, and let a logit re-weight them on the "
            "fit years. <bookmark mark='a'/> Working capital and operating profit carry most of the weight. Retained "
            "earnings and sales add almost nothing once the others are known, and the market cushion less than "
            "Altman gave it. <bookmark mark='b'/> On the validation years the re-weighted ratios score "
            f"{v['refit']:.2f}, against {v['altman_1968']:.2f} for the weights of 1968. Same information, better "
            "weights: most of the next chapter's gain will come from new inputs and from interactions."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[1:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def ratios(self, d):
        X, y, fy = np.asarray(d["X"], float), np.asarray(d["y"], int), np.asarray(d["fy"], int)
        fit = fy <= 2016
        names = [(0, r"working capital / assets"), (2, r"operating profit / assets"), (6, r"liabilities / assets"),
                 (3, r"market equity / liabilities")]
        panels = VGroup()
        for j, name in names:
            x = X[fit, j]
            ok = np.isfinite(x)
            lo, hi = np.nanpercentile(x[ok], [2, 98])
            if j == 3:
                x = np.log10(np.clip(x, 1e-3, None))
                lo, hi = np.nanpercentile(x[ok], [2, 98])
            edges = np.linspace(lo, hi, 26)
            h0 = np.histogram(np.clip(x[ok & (y[fit] == 0)], lo, hi), edges, density=True)[0]
            h1 = np.histogram(np.clip(x[ok & (y[fit] == 1)], lo, hi), edges, density=True)[0]
            top = max(h0.max(), h1.max()) * 1.1
            g = axes([lo, hi], [0, top], x_length=3.0, y_length=2.4, xlabel=name if j != 3 else r"log$_{10}$ market "
                     r"equity / liabilities", ylabel=r"", xticks=[], yticks=[], font_size=12)
            mid = 0.5 * (edges[1:] + edges[:-1])
            panels.add(VGroup(g, curve(g.ax, mid, h0, SAFE, stroke_width=2.5, smooth=True),
                              curve(g.ax, mid, h1, BAD, stroke_width=2.5, smooth=True)))
        panels.arrange(RIGHT, buff=0.35).shift(DOWN * 0.3)
        if panels.width > 13.2:
            panels.scale_to_fit_width(13.2)
        leg = legend([(SAFE, r"survived the next year"), (BAD, r"filed for bankruptcy")], font_size=18).arrange(
            RIGHT, buff=0.6).to_edge(UP, buff=0.6)
        foot = wrapped_label(r"fit years 2010--2016: the distributions overlap heavily, ratio by ratio. Each one alone is "
                             r"a weak signal; together, and allowed to interact, they become a forecast", 12.0, 19,
                             GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Why do combinations matter? Look at four of the ratios, for firms that survived the next year and firms "
            "that filed. <bookmark mark='a'/> Bankrupt firms have less working capital, lower profits, more debt, and "
            "less market equity per dollar owed. But every pair of distributions overlaps: no single ratio "
            "separates them. Together, and allowed to interact, they can."
        ) as vo:
            self.play(FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in panels], lag_ratio=0.3, run_time=3), FadeIn(foot))
        q = ask(r"Altman's sample was 33 bankrupt and 33 healthy manufacturers. Why does a 50-50 sample make the "
                r"probabilities, but not the ranking, wrong?")
        with self.voiceover("Altman's sample was half bankrupt firms. Why does that make his probabilities wrong, but "
                            "not his ranking?"):
            self.play(FadeOut(foot), FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
