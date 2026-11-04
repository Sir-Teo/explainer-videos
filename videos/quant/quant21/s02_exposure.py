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
        self.shapes(load("products"))
        self.netting(e)
        self.legal()
        self.regulatory(load("products"))

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

    def shapes(self, p):
        t = np.asarray(p["times"])
        cols = {"swap": EXPO, "fx_forward": QC.IMPLIED, "xccy": BAD, "option": QC.GAIN}
        names = {"swap": r"interest-rate swap", "fx_forward": r"FX forward", "xccy": r"cross-currency swap",
                 "option": r"bought option"}
        g = axes([0, 10], [0, 30], x_length=7.4, y_length=4.4, xlabel=r"years", ylabel=r"EE on \$100m, \$ million",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 10, 20, 30], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        lines = VGroup(*[curve(ax, np.r_[0, t], np.r_[0 if k != "option" else p[k][0], p[k]], c_, stroke_width=3)
                         for k, c_ in cols.items()])
        side = VGroup(
            legend([(c_, names[k]) for k, c_ in cols.items()], font_size=17),
            wrapped_label(r"the shape is the product's: a swap's payments run off; an FX forward only diffuses; a "
                          r"cross-currency swap exchanges its notionals at the end, so its exposure keeps growing; a bought "
                          r"option is always an asset, its whole value at risk. FX vol 10\%, option vol 20\% "
                          r"(illustrative)", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Every product has its own shape. <bookmark mark='a'/> A swap's exposure has the hump of run-off. An FX "
            "forward settles once, at the end, so its exposure just diffuses, growing with the square root of time. "
            "<bookmark mark='b'/> A cross-currency swap exchanges its principals at maturity, so the exchange-rate "
            "risk on the whole notional keeps growing to the very end. <bookmark mark='c'/> And a bought option is "
            "never a liability: the counterparty owes its whole value, all the time, which is why selling options to "
            "a weak counterparty is cheap and buying from one is not."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(lines[0]), Create(lines[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lines[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(lines[3]), FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def legal(self):
        rows = [cmath(r"\text{claim}", r"=", r"\textstyle\sum_i V_i\quad\text{not}\quad \textstyle\sum_i \max(V_i, 0)\ "
                      r"\text{owed},\ \textstyle\sum_i \min(V_i, 0)\ \text{paid}", font_size=32,
                      colors={r"\text{claim}": EXPO})]
        whys = [why(r"close-out netting: on default every trade under one master agreement is terminated and valued, and "
                    r"the values are added into a single amount; without it, a liquidator could demand payment on the "
                    r"trades it loses on and leave the others as unsecured claims ('cherry-picking')")]
        step = ladder(self, rows, whys, keep=1, top=2.6, x=-0.4, buff=0.8, edge=6.9)
        cards = VGroup(
            desk_question(r"the contract", r"ISDA's master agreements (1987, 1992, 2002): all trades form a single "
                          r"agreement, so a default ends them all at once, at one net amount", width=12.0, font_size=19),
            desk_question(r"the law", r"netting is only worth what courts enforce: dealers collect legal opinions country "
                          r"by country, and count a netting set only where netting is known to hold; US bankruptcy law "
                          r"exempts swaps from the automatic stay (widened in 2005)", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Netting is not arithmetic; it is law. <bookmark mark='a'/> When a counterparty fails, its liquidator "
            "would like to collect on every trade it is winning and leave the bank to queue as an unsecured creditor "
            "on the rest. Close-out netting forbids that: all trades under one master agreement are terminated "
            "together and added into a single amount. <bookmark mark='b'/> The industry's master agreements, from "
            "1987 onwards, make every trade part of one contract for exactly this reason. <bookmark mark='c'/> And "
            "netting is only worth what a court will enforce, so dealers collect legal opinions country by country, "
            "and count a netting set only where it is known to hold. In the United States, swaps are also exempt "
            "from the freeze on creditors that bankruptcy normally imposes, an exemption widened in 2005, and "
            "debated ever since Lehman."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def regulatory(self, p):
        rows = [cmath(r"\text{EE}^{\text{eff}}(t_k)", r"=", r"\max_{j \le k} \text{EE}(t_j)", font_size=40,
                      colors={r"\text{EE}^{\text{eff}}(t_k)": EXPO}),
                cmath(r"\text{EEPE}", r"=", r"\frac{1}{1\,\text{yr}}\int_0^{1\,\text{yr}} \text{EE}^{\text{eff}}(t)\,dt,\quad "
                      r"\text{EAD} = \alpha\,\text{EEPE},\ \alpha = 1.4", font_size=34, colors={r"\text{EEPE}": EXPO})]
        whys = [why(r"the regulators' version for banks with approved models: expected exposure that is never allowed to "
                    r"fall, since maturing trades are assumed to be replaced"),
                why(rf"effective EPE over the first year; here \${p['EEPE']:.2f}m against \${p['EPE_1y']:.2f}m of plain EPE, "
                    r"and $\alpha$ adds a margin for wrong-way risk and model error")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Regulators take the same profile and make it conservative. The effective expected exposure is never "
            "allowed to fall, on the assumption that trades which mature are replaced. <bookmark mark='a'/> Its "
            "average over the first year, times a multiplier alpha of one point four, is the exposure at default "
            "for banks allowed to use their own models; the alpha covers wrong-way risk and model error."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a bank has two swaps with the same counterparty that exactly offset. What is its exposure with netting, "
                r"and without it?")
        with self.voiceover("A bank has two swaps with one counterparty that exactly offset. What is its exposure with "
                            "netting, and without?"):
            self.play(FadeIn(q))
        self.wait(0.5)
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
        self.wait(0.4)
        self.clear_scene()
