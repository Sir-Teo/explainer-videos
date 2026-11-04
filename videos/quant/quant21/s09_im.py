from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant21.common import BAD, GOOD, IM_C, PART, ask, fit_right, illustration, load


class IM(VoiceoverScene):
    def construct(self):
        m = load("im")
        self.card()
        self.rules()
        self.simm(m)
        self.profile(m)

    def card(self):
        c = chapter_card(8, r"Initial margin", r"How much must each side post in advance?", part=PART)
        with self.voiceover("Chapter eight. Initial margin: collateral posted in advance, against the gap."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def rules(self):
        rows = [cmath(r"\text{IM}", r"\approx", r"\text{the 99th percentile of the 10-day change in value}", font_size=36,
                      colors={r"\text{IM}": IM_C}),
                cmath(r"\text{IM}_{\text{SIMM}}", r"=", r"\sqrt{\textstyle\sum_{k,l} \rho_{kl}\,WS_k\,WS_l},\quad WS_k = "
                      r"RW_k\,s_k", font_size=36, colors={r"\text{IM}_{\text{SIMM}}": IM_C})]
        whys = [why(r"variation margin settles yesterday's move; initial margin covers the move during the margin period "
                    r"of risk, posted by both sides to a third party, and not re-usable. Required for uncleared "
                    r"derivatives between large firms in phases from September 2016 to September 2022"),
                why(r"ISDA's Standard Initial Margin Model: sensitivities $s_k$ by risk factor (here, DV01 by tenor), "
                    r"risk weights, and correlations that let offsetting tenors net. The weights here are illustrative, "
                    r"not ISDA's calibration")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Variation margin covers yesterday's move. Initial margin is posted in advance, by both sides, to cover the "
            "move during the margin period of risk, at about the ninety-ninth percentile, and it is held by a third "
            "party, so it cannot be re-used. After 2008, regulators required it between large firms for derivatives "
            "that are not centrally cleared, phased in from 2016 to 2022. <bookmark mark='a'/> To agree on the number, "
            "the industry wrote a common model, ISDA's SIMM: sensitivities by risk factor, times risk weights, "
            "combined with correlations so that offsetting positions net."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def simm(self, m):
        keys, dv = np.asarray(m["keys"]), np.asarray(m["dv01"]) * 1e3
        g = axes([-0.5, 8.5], [-80, 30], x_length=7.2, y_length=4.2, xlabel=r"tenor",
                 ylabel=r"key-rate DV01, \$ thousand per bp", xticks=[], yticks=[-80, -40, 0, 20], font_size=14
                 ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        zero = Line(ax.c2p(-0.5, 0), ax.c2p(8.5, 0), color=WHITE, stroke_width=1.2)
        bars = VGroup()
        for i, (k, v) in enumerate(zip(keys, dv)):
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
            bars.add(VGroup(Rectangle(width=0.55, height=max(abs(y1 - y0), 0.01), stroke_width=0,
                                      fill_color=BAD if v < 0 else GOOD, fill_opacity=0.8).move_to(
                [ax.c2p(i, 0)[0], (y0 + y1) / 2, 0]), label(f"{k:g}y", font_size=15).next_to(ax.c2p(i, -80), DOWN, buff=0.1)))
        side = VGroup(
            MathTex(rf"\text{{IM}} = \${m['im']:.1f}\text{{m}}", font_size=32, color=IM_C),
            label(r"on \$200 million of swaps", font_size=19, color=GREY_A),
            wrapped_label(r"the book's risk sits at 3, 5 and 10 years and partly offsets: pay 10 years, receive 5. Without "
                          r"the correlations the margin would be the sum of the parts", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "For the netting set: its rate sensitivity tenor by tenor, in thousands of dollars a basis point. "
            "<bookmark mark='a'/> The ten-year payer dominates, partly offset by the five-year receiver. "
            f"<bookmark mark='b'/> Weighted and combined, the initial margin is about {m['im']:.1f} million dollars, "
            "posted by each side, on two hundred million of swaps."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def profile(self, m):
        t, p = np.asarray(m["times"]), np.asarray(m["profile"])
        g = axes([0, 10], [0, max(p) * 1.2], x_length=7.4, y_length=4.2, xlabel=r"years", ylabel=r"initial margin, \$ million",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 1, 2, 3], font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, t, p, IM_C, stroke_width=3.5)
        side = wrapped_label(r"initial margin falls as the swaps run off, and is funded every day it is posted: the "
                             r"funding cost of this profile is MVA (chapter 5). For a dealer with thousands of trades, "
                             r"margin became one of the largest uses of cash", 3.8, 18, GREY_A).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The margin must be funded for as long as the trades live. <bookmark mark='a'/> As the swaps run off, the "
            "required margin falls, step by step. The cost of funding this whole profile is the margin valuation "
            "adjustment of chapter five; for large dealers, posting margin became one of the biggest uses of cash on "
            "the balance sheet."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side), run_time=2)
        q = ask(r"initial margin is set at the 99th percentile of a 10-day move. What happens to it, and to everyone "
                r"posting it, the day volatility doubles?")
        with self.voiceover("Initial margin is set at the ninety-ninth percentile of ten days' moves. What happens to it, "
                            "and to everyone posting it, the day volatility doubles?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
