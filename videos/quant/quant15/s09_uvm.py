from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, GOOD, IV, OPT, PART, SPOT, illustration, load


class UVM(VoiceoverScene):
    def construct(self):
        u = load("uvm")
        self.card()
        self.model()
        self.bounds(u)

    def card(self):
        c = chapter_card(8, r"Uncertain volatility, and model reserves", r"What should you charge for not knowing the model?",
                         lit=(1995,), part=PART)
        with self.voiceover("Chapter eight. Uncertain volatility, and model reserves."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"\partial_t V + \tfrac12\,\sigma(\Gamma)^2 S^2\,\Gamma + rS\,\partial_S V - rV", r"=", r"0", font_size=34,
                      colors={r"\partial_t V + \tfrac12\,\sigma(\Gamma)^2 S^2\,\Gamma + rS\,\partial_S V - rV": OPT}),
                cmath(r"\sigma(\Gamma)", r"=", r"\begin{cases}\sigma_{\max} & \Gamma > 0 \\ \sigma_{\min} & \Gamma < 0\end{cases}",
                      font_size=34, colors={r"\sigma(\Gamma)": IV})]
        whys = [why(r"Avellaneda, Levy and Par\'as (1995); Lyons (1995): suppose volatility can be anything in a band, "
                    r"chosen against you at every moment"),
                why(r"the seller's price uses the top of the band where the position is long gamma and the bottom where it "
                    r"is short: the cheapest hedge that survives every volatility path in the band. It is non-linear: the "
                    r"price of a book is not the sum of its parts")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.4, buff=1.0, edge=6.9)
        with self.voiceover(
            "Parts thirteen and fourteen showed that models fitted to the same vanillas disagree on exotics. How "
            "much should a desk charge for that? In 1995 Marco Avellaneda, Arnon Levy and Antonio Parás, and "
            "independently Terry Lyons, answered with a worst case. Suppose volatility can be anything within a band, "
            "chosen against you at every moment. <bookmark mark='a'/> Then the price to sell solves a Black–Scholes "
            "equation in which the volatility switches: the top of the band wherever the position is long gamma, the "
            "bottom wherever it is short. It is the cheapest hedge that survives every path in the band. And it is "
            "non-linear: a book's price is not the sum of its parts, because positions can cancel each other's risk."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def bounds(self, u):
        S = np.asarray(u["S"])
        g = axes([70, 130], [0, 1], x_length=6.6, y_length=4.2, xlabel=r"spot", ylabel=r"value of a call spread 95--105, per unit",
                 xticks=[80, 100, 120], yticks=[0, 0.5, 1.0], font_size=15).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        up = curve(ax, S, np.asarray(u["upper"]), BAD, stroke_width=3)
        lo = curve(ax, S, np.asarray(u["lower"]), GOOD, stroke_width=3)
        b15 = DashedVMobject(curve(ax, S, np.asarray(u["bs15"]), GREY_B, stroke_width=2), num_dashes=40)
        b35 = DashedVMobject(curve(ax, S, np.asarray(u["bs35"]), GREY_A, stroke_width=2), num_dashes=40)
        leg = legend([(BAD, r"seller's price, volatility anywhere in 15--35\%"), (GOOD, r"buyer's price"),
                      (GREY_B, r"Black--Scholes at 15\%"), (GREY_A, r"Black--Scholes at 35\%")], font_size=16)
        leg.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        a = u["at100"]
        side = VGroup(
            MathTex(rf"[{a['lower']:.2f},\ {a['upper']:.2f}]", font_size=36, color=OPT),
            wrapped_label(rf"at the money, against {a['bs15']:.2f} to {a['bs35']:.2f} for Black--Scholes anywhere in the band: "
                          r"a call spread is long gamma below and short above, so no single volatility is the worst "
                          r"case, and the band is wider than every constant-volatility price", 4.4, 19, GREY_A),
            wrapped_label(r"desks hold a model reserve: the gap between the marked price and a price like the seller's "
                          r"bound, released as the exotic's risk runs off (Cont 2006 makes model uncertainty a coherent "
                          r"risk measure)", 4.4, 19, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        src = illustration(r"the House's Black--Scholes--Barenblatt solver; six months, rates zero")
        with self.voiceover(
            "Here is a call spread, long the 95 call and short the 105, priced with volatility anywhere between 15 "
            "and 35 percent. <bookmark mark='a'/> The seller's and buyer's prices bracket every constant-volatility "
            f"price. At the money they run from {a['lower']:.2f} to {a['upper']:.2f}, while Black–Scholes anywhere in "
            f"the band gives only {a['bs15']:.2f} to {a['bs35']:.2f}. A call spread is long gamma below its middle and "
            "short above, so the worst case uses high volatility in one place and low in the other, a path no single "
            "volatility can imitate. <bookmark mark='b'/> Desks turn this into money with a model reserve: they mark "
            "an exotic at their model, hold back the gap to a price like the seller's bound, and release it as the "
            "risk runs off."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(b15), Create(b35), FadeIn(leg[2]), FadeIn(leg[3]), run_time=2)
            vo.wait_until("a")
            self.play(Create(up), Create(lo), FadeIn(leg[0]), FadeIn(leg[1]), FadeIn(side[0]), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
