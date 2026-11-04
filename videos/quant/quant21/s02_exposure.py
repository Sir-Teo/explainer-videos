from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant21.common import BAD, EXPO, NEG, PART, PFE_C, ask, fit_right, illustration, load


class Exposure(VoiceoverScene):
    def construct(self):
        e = load("exposure")
        self.card()
        self.define()
        self.fan(e)
        self.profiles(e)
        self.netting(e)

    def card(self):
        c = chapter_card(1, r"Exposure", r"What could the other side owe you, and when?", part=PART)
        with self.voiceover("Chapter one. Exposure: what the other side of a trade could owe you, and when."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def define(self):
        rows = [cmath(r"E(t)", r"=", r"\max\big(V(t),\ 0\big)", font_size=44, colors={r"E(t)": EXPO}),
                cmath(r"\text{EE}(t)", r"=", r"\mathbb{E}\big[\max(V(t), 0)\big],\quad \text{ENE}(t) = \mathbb{E}\big[\min(V(t), "
                      r"0)\big]", font_size=34, colors={r"\text{EE}(t)": EXPO}),
                cmath(r"\text{PFE}_{95}(t)", r"=", r"\text{the 95th percentile of } \max(V(t), 0)", font_size=36,
                      colors={r"\text{PFE}_{95}(t)": PFE_C})]
        whys = [why(r"if the counterparty defaults at $t$ while the trade is worth $V(t)$ to you, you lose it if positive; "
                    r"if negative, you still owe it: the asymmetry of default"),
                why(r"the expected exposure and its mirror, the expected negative exposure: what the counterparty may "
                    r"owe you, and what you may owe it"),
                why(r"potential future exposure, the number a credit limit is set against")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.0, buff=0.7, edge=6.9)
        with self.voiceover(
            "A swap is worth zero to both sides when it is struck. Then rates move, and it becomes an asset to one "
            "and a liability to the other. If the counterparty defaults when the swap is worth something to you, you "
            "lose it; if it is worth something to them, you still owe it. <bookmark mark='a'/> So the exposure is the "
            "positive part of the value, and its average over the paths rates might take is the expected exposure. "
            "<bookmark mark='b'/> Banks also set credit limits against a high percentile of it, the potential future "
            "exposure."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def fan(self, e):
        t, fan, q = np.asarray(e["times"]), np.asarray(e["fan"]), np.asarray(e["q"])
        g = axes([0, 10], [-25, 30], x_length=8.2, y_length=4.4, xlabel=r"years", ylabel=r"value to the bank, \$ million",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[-20, -10, 0, 10, 20, 30], font_size=14).to_edge(LEFT, buff=0.5
                                                                                               ).shift(DOWN * 0.3)
        ax = g.ax
        zero = Line(ax.c2p(0, 0), ax.c2p(10, 0), color=WHITE, stroke_width=1.5)
        paths = VGroup(*[curve(ax, np.r_[0, t], np.clip(np.r_[0, p_], -25, 30), EXPO, stroke_width=1).set_stroke(
            opacity=0.35) for p_ in fan[:50]])
        band = Polygon(*[ax.c2p(a, b) for a, b in zip(np.r_[0, t], np.r_[0, q[2]])],
                       *[ax.c2p(a, b) for a, b in zip(np.r_[0, t][::-1], np.r_[0, q[0]][::-1])], stroke_width=0,
                       fill_color=EXPO, fill_opacity=0.15)
        b0 = e["book"][0]
        side = VGroup(
            label(rf"pay fixed {100 * b0['K']:.2f}\% for 10 years on \$100 million, at par", font_size=19, color=GREY_A),
            wrapped_label(rf"Hull--White fitted in Part 19 ($a = {e['a']:.4f}$, $\sigma = {100 * e['sigma']:.2f}\%$), "
                          r"20{,}000 paths; band: 5th to 95th percentile", 3.6, 17, GREY_A),
            wrapped_label(r"the fan widens as rates have time to move, then narrows as the swap's remaining payments "
                          r"run off: two forces, and a hump between them", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Here is one swap: the bank pays a fixed rate for ten years on a hundred million dollars. Fifty of twenty "
            "thousand paths of its value, simulated with the Hull and White model of Part nineteen. "
            "<bookmark mark='a'/> The fan widens at first, as rates have time to move. <bookmark mark='b'/> Then it "
            "narrows, because each year one payment fewer remains to be affected. Diffusion pushes the exposure up, "
            "amortisation pulls it down, and the profile between them has a hump."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(p_) for p_ in paths], lag_ratio=0.03, run_time=3), FadeIn(band))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def profiles(self, e):
        t = np.asarray(e["times"])
        s = e["single"]
        g = axes([0, 10], [-12, 22], x_length=8.2, y_length=4.4, xlabel=r"years", ylabel=r"\$ million",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[-10, 0, 10, 20], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        zero = Line(ax.c2p(0, 0), ax.c2p(10, 0), color=WHITE, stroke_width=1.2)
        lee = curve(ax, np.r_[0, t], np.r_[0, s["EE"]], EXPO, stroke_width=3.5)
        lene = curve(ax, np.r_[0, t], np.r_[0, s["ENE"]], NEG, stroke_width=3.5)
        lpfe = curve(ax, np.r_[0, t], np.r_[0, s["PFE"]], PFE_C, stroke_width=3)
        k = int(np.argmax(s["EE"]))
        side = VGroup(
            legend([(EXPO, r"EE"), (NEG, r"ENE"), (PFE_C, r"PFE, 95\%")], font_size=17),
            MathTex(rf"\max \text{{EE}} = \${s['EE'][k]:.1f}\text{{m at }} {t[k]:.1f}\ \text{{years}}", font_size=24),
            MathTex(rf"\max \text{{PFE}} = \${max(s['PFE']):.1f}\text{{m}}", font_size=24, color=PFE_C),
            wrapped_label(r"the payer side gains when rates rise, and the curve slopes up, so the expected positive "
                          r"value exceeds the negative: EE is larger than $|$ENE$|$", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Averaged over the paths: <bookmark mark='a'/> the expected exposure peaks at about "
            f"{s['EE'][k]:.1f} million dollars, {t[k]:.0f} years in, and the expected negative exposure mirrors it. "
            f"<bookmark mark='b'/> The ninety-fifth percentile reaches {max(s['PFE']):.0f} million: that is the "
            "number the bank's credit officers set a limit against, for a trade that was worth nothing on the day it "
            "was done."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(lee), Create(lene), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lpfe), FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def netting(self, e):
        t = np.asarray(e["times"])
        g = axes([0, 10], [0, 8], x_length=7.6, y_length=4.4, xlabel=r"years", ylabel=r"EE, \$ million",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 2, 4, 6, 8], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        lg = curve(ax, np.r_[0, t], np.r_[0, e["gross_EE"]], BAD, stroke_width=3)
        ln = curve(ax, np.r_[0, t], np.r_[0, e["net"]["EE"]], EXPO, stroke_width=3.5)
        book = e["book"]
        side = VGroup(
            legend([(BAD, r"three trades, each on its own"), (EXPO, r"one netting set")], font_size=17),
            *[label(rf"{'pay' if b['payer'] else 'receive'} {100 * b['K']:.2f}\% for {b['T']:.0f} years on "
                    rf"\${b['N']:.0f}m", font_size=17, color=GREY_A) for b in book],
            MathTex(rf"\text{{netting cuts EPE by }} {100 * e['netting_benefit']:.0f}\%", font_size=26),
            wrapped_label(r"under one ISDA master agreement, a defaulter's trades are closed out together: what it owes "
                          r"on one swap offsets what you owe on another", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Banks rarely face a counterparty with one trade. Under a master agreement, all the trades with one "
            "counterparty are closed out together on default, and only the net amount is owed. "
            "<bookmark mark='a'/> Add a five-year swap the other way and a short one the same way, and compare: "
            "summed one by one, the exposures are the red curve; netted, the blue. <bookmark mark='b'/> Netting cuts "
            f"the average exposure by {100 * e['netting_benefit']:.0f} percent here, and in a dealer's book of "
            "thousands of offsetting trades, by far more. It is the single most important tool in counterparty risk."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), LaggedStart(*[FadeIn(r_) for r_ in side[1:4]], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(Create(lg), Create(ln), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[4]), FadeIn(side[5]))
        q = ask(r"a bank has two swaps with the same counterparty that exactly offset. What is its exposure with netting, "
                r"and without it?")
        with self.voiceover("A bank has two swaps with one counterparty that exactly offset. What is its exposure with "
                            "netting, and without?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
