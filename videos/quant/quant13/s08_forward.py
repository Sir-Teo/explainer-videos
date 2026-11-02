from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, illustration, load

ORDER = ("LV", "Heston", "Bates", "VG", "SLV")
NAMES = {"LV": r"local vol", "Heston": r"Heston", "Bates": r"Bates", "VG": r"variance gamma", "SLV": r"SLV"}


class Forward(VoiceoverScene):
    def construct(self):
        e = load("exotics")
        self.card()
        self.smiles(e)
        self.exotics(e)
        self.puzzle()

    def card(self):
        c = chapter_card(7, r"The forward smile, and model risk", r"Same vanillas, same exotic price?", part=PART)
        with self.voiceover("Chapter seven. The forward smile, and model risk."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def smiles(self, e):
        k = np.asarray(e["k"])
        g = axes([-0.25, 0.25], [0.38, 0.66], x_length=6.6, y_length=4.2, xlabel=r"log-moneyness of a 30-day option",
                 ylabel=r"implied volatility", xticks=[-0.2, -0.1, 0, 0.1, 0.2], yticks=[0.4, 0.5, 0.6],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        today = DashedVMobject(curve(ax, k, np.asarray(e["today"]), WHITE, stroke_width=3), num_dashes=40)
        lines = {m: curve(ax, k, np.clip(np.asarray(e["models"][m]["fwd_iv"]), 0.38, 0.66), MODEL_COL[m], stroke_width=2.8)
                 for m in ORDER}
        leg = legend([(WHITE, r"today's 30-day smile")] + [(MODEL_COL[m], NAMES[m]) for m in ORDER], font_size=17)
        leg.next_to(g, RIGHT, buff=0.4).align_to(g, UP)
        sk = VGroup(label(r"skew of the forward smile (90\% minus 110\%)", font_size=19, color=GREY_A),
                    MathTex(rf"\text{{today}}\ \ {100 * e['today_skew']:.1f}", font_size=26),
                    *[MathTex(rf"\text{{{NAMES[m]}}}\ \ {100 * e['models'][m]['fwd_skew']:.1f}", font_size=26,
                              color=MODEL_COL[m]) for m in ORDER]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        sk.next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        src = illustration(r"each model fitted to the Surface; the 30-day smile starting in 60 days, 40{,}000 paths")
        lv, he, vg = (e["models"][m] for m in ("LV", "Heston", "VG"))
        with self.voiceover(
            "Every model in this part was fitted to the same Surface. Ask each one the same question: what will the "
            "thirty-day smile look like sixty days from now? That forward smile is not quoted anywhere; it is a "
            "model's opinion. <bookmark mark='a'/> Local volatility, as Part twelve showed, says it will flatten: a "
            f"skew of {100 * lv['fwd_skew']:.1f} points, against {100 * e['today_skew']:.1f} today. "
            "<bookmark mark='b'/> Heston and Bates keep today's skew, because their variance is random whenever "
            "you start. Variance gamma's increments are stationary, so its forward smile is today's smile for that "
            "maturity, but it fitted today's badly. And the stochastic local volatility model sits in between, where "
            "its mixing fraction puts it. Five models, one set of vanilla prices, five different futures."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(today), FadeIn(leg[0]), FadeIn(sk[:2]))
            vo.wait_until("a")
            self.play(Create(lines["LV"]), FadeIn(leg[1]), FadeIn(sk[2]))
            vo.wait_until("b")
            self.play(*[Create(lines[m]) for m in ORDER[1:]], FadeIn(leg[2:]), FadeIn(sk[3:]), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def exotics(self, e):
        cl = {m: e["models"][m]["cliquet"] for m in ORDER}
        fs = {m: e["models"][m]["forward_start"] for m in ORDER}

        def bars(vals, title, fmt, lo, hi, ticks):
            g = axes([-0.6, len(ORDER) - 0.4], [lo, hi], x_length=5.2, y_length=3.4, xticks=list(range(len(ORDER))),
                     xfmt=lambda u: NAMES[ORDER[int(round(u))]], yticks=ticks, yfmt=fmt, font_size=14)
            ax = g.ax
            bs_ = VGroup(*[Rectangle(width=0.55, height=abs(ax.c2p(0, vals[m])[1] - ax.c2p(0, lo)[1]), stroke_width=0,
                                     fill_color=MODEL_COL[m], fill_opacity=0.85).move_to(ax.c2p(i, (vals[m] + lo) / 2))
                           for i, m in enumerate(ORDER)])
            t = label(title, font_size=20).next_to(g, UP, buff=0.15)
            v = np.array(list(vals.values()))
            spread = MathTex(rf"\text{{spread}}\ {100 * (v.max() - v.min()) / v.mean():.0f}\%", font_size=28,
                             color=BAD).next_to(g, DOWN, buff=0.25)
            return VGroup(g, t, bs_, spread)

        p1 = bars(cl, r"a cliquet: four monthly returns, each floored at 0 and capped at 10\%",
                  lambda u: f"{100 * u:.0f}\\%", 0.12, 0.145, [0.12, 0.13, 0.14])
        p2 = bars(fs, r"a forward-start at-the-money call: 30 days, starting in 60",
                  lambda u: f"{100 * u:.1f}\\%", 0.045, 0.057, [0.045, 0.05, 0.055])
        VGroup(p1, p2).arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.8)
        foot = wrapped_label(r"prices per unit of notional; the vanilla options all models were fitted to are the same. "
                             r"Model risk is this spread, and a desk reports it: the House prices every exotic under at "
                             r"least two models fitted to the same surface", 11.5, 20, GREY_A).to_edge(DOWN, buff=0.4)
        v1, v2 = np.array(list(cl.values())), np.array(list(fs.values()))
        with self.voiceover(
            "Now price two exotics that are bets on the future smile. A cliquet pays the sum of four monthly returns, "
            "each floored at zero and capped at ten percent. Under the five models it costs between "
            f"{100 * v1.min():.1f} and {100 * v1.max():.1f} percent of notional: a spread of "
            f"{100 * (v1.max() - v1.min()) / v1.mean():.0f} percent. <bookmark mark='a'/> A forward-start option, "
            "struck at the money in sixty days, is worse: a spread of "
            f"{100 * (v2.max() - v2.min()) / v2.mean():.0f} percent. Local volatility, with the flattest forward smile "
            "but the highest forward volatility, prices it dearest. <bookmark mark='b'/> No vanilla price can settle "
            "this. That spread is model risk, and an honest desk reports it, rather than quoting one model's number "
            "as if it were the price."
        ) as vo:
            self.play(FadeIn(p1[:2]), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in p1[2]], lag_ratio=0.15), FadeIn(p1[3]))
            vo.wait_until("a")
            self.play(FadeIn(p2[:2]), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in p2[2]], lag_ratio=0.15), FadeIn(p2[3]))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def puzzle(self):
        h1 = history_card(2008, r"Gatheral, Bachelier Congress, London",
                          r"The VIX is a 30-day variance swap on the S\&P 500, and options on the VIX trade too. A "
                          r"model fitted to S\&P options must also price VIX options. Gatheral showed that a diffusion "
                          r"with two variance factors could fit both markets only approximately.", color=QC.IDEA, width=5.8)
        h2 = history_card(2020, r"Guyon, \textit{Risk}", r"``The joint S\&P 500/VIX smile calibration puzzle solved'': "
                          r"an exact joint fit by a non-parametric discrete-time model built with optimal transport, the "
                          r"same mathematics as Part 9's martingale bounds. Continuous-time models that fit both are "
                          r"still a research front (Part 14).", color=QC.IDEA, width=5.8)
        VGroup(h1, h2).arrange(RIGHT, buff=0.5, aligned_edge=UP).move_to(UP * 0.3)
        foot = label(r"the puzzle is stated here for the S\&P 500 and the VIX; Part 14 returns to it",
                     font_size=20, color=GREY_B).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "There is a harder test still. The VIX is a thirty-day variance swap on the S&P 500, and options on the "
            "VIX trade as well. A model fitted to S&P options makes a prediction about VIX options, and for years no "
            "standard model got both right. Jim Gatheral showed in 2008 that a diffusion with two variance factors "
            "could fit both, but only approximately. <bookmark mark='a'/> In 2020 Julien Guyon fitted both exactly, "
            "with a discrete-time model built by optimal transport, the mathematics of Part nine's bounds. Continuous "
            "models that do it are a research front, and Part fourteen picks it up."
        ) as vo:
            self.play(FadeIn(h1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(h2, shift=UP * 0.2), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
