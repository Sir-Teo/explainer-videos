from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import valuation
from videos.quant.quant3.common import CASH, DEBT, EQUITY, PART, VALUE, load

FCF = 100 * 1.05 ** np.arange(1, 6)


def fdcf(r, g):
    return valuation.dcf(FCF, r, g)


class DCF(VoiceoverScene, ThreeDScene):
    def construct(self):
        d = load("dcf")
        self.card()
        self.fcf_wacc()
        self.bars(d)
        self.surface(d)

    def card(self):
        c = chapter_card(3, r"Discounted cash flow", r"What is a whole firm worth?", part=PART)
        with self.voiceover("Chapter three. Discounted cash flow."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def fcf_wacc(self):
        f1 = cmath(r"\text{FCF}", r"=", r"\text{EBIT}(1 - t)", r"+", r"\text{depreciation}", r"-", r"\text{capital spending}",
                   r"-", r"\Delta\,\text{working capital}", font_size=34, colors={r"\text{FCF}": CASH})
        w = cmath(r"\text{WACC}", r"=", r"\frac{E}{V}\,r_E", r"+", r"\frac{D}{V}\,r_D(1 - t)", font_size=44,
                  colors={r"\text{WACC}": VALUE, r"\frac{E}{V}\,r_E": EQUITY, r"\frac{D}{V}\,r_D(1 - t)": DEBT})
        ex = MathTex(rf"\text{{equity 600 at 9\%, debt 200 at 5\%, tax 21\%:}}\quad "
                     rf"{100 * valuation.wacc(600, 200, 0.09, 0.05, 0.21):.2f}\%", font_size=30, color=GREY_A)
        VGroup(f1, w, ex).arrange(DOWN, buff=0.7).move_to(UP * 0.4)
        n1 = why(r"the cash the business could pay out to all its investors, before any of it goes to lenders or owners")
        n1.next_to(f1, DOWN, buff=0.2)
        foot = note(r"$r_E$, the return owners demand, is estimated from risk in Part 5's factor models and Part 9's "
                    r"no-arbitrage pricing", font_size=19, color=GREY_B).to_edge(DOWN, buff=0.4)
        VGroup(w, ex).shift(DOWN * 0.3)
        with self.voiceover(
            "To value a whole firm rather than one share, an analyst discounts its free cash flow: the cash its "
            "business throws off after taxes and after the investment needed to keep it growing, before anything is "
            "paid to lenders or owners. Operating profit after tax, plus the depreciation that cost no cash, minus "
            "the spending on new plant, minus the cash tied up in stock and unpaid bills. <bookmark mark='a'/> "
            "Because that cash belongs to both lenders and owners, it is discounted at a blend of what each "
            "demands: the weighted average cost of capital. Debt's cost is cut by the tax rate, because interest "
            "is deductible. <bookmark mark='b'/> Our toy firm, with equity worth six hundred that wants nine "
            "percent and debt of two hundred at five, has a cost of capital a little under eight percent."
        ) as vo:
            self.play(Write(f1))
            self.play(FadeIn(n1))
            vo.wait_until("a")
            self.play(Write(w), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(ex))
        self.wait(0.4)
        self.clear_scene()

    def bars(self, d):
        base = fdcf(0.08, 0.02)
        pv = FCF / 1.08 ** np.arange(1, 6)
        g = axes([0, 7], [0, 1600], x_length=6.8, y_length=4.6, ylabel=r"present value", yticks=[0, 500, 1000, 1500],
                 xticks=[], font_size=18).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        ax = g.ax
        w = ax.c2p(0.7, 0)[0] - ax.c2p(0, 0)[0]
        bars = VGroup()
        for k, v in enumerate(list(pv) + [base["terminal"]]):
            x = k + 1 if k < 5 else 6.3
            col = CASH if k < 5 else VALUE
            r = Rectangle(width=w, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to(ax.c2p(x, 0), aligned_edge=DOWN)
            bars.add(r)
        xl = VGroup(*[MathTex(str(k), font_size=22, color=GREY_B).next_to(bars[k - 1], DOWN, buff=0.12) for k in range(1, 6)],
                    label(r"after", font_size=18, color=VALUE).next_to(bars[5], DOWN, buff=0.12))
        side = VGroup(
            label(r"free cash flow 100, growing 5\% for five years,", font_size=22, color=GREY_A),
            label(r"then 2\% forever; discounted at 8\%", font_size=22, color=GREY_A),
            MathTex(rf"\text{{years 1--5:}}\ {base['explicit']:,.0f}".replace(",", "{,}"), font_size=32, color=CASH),
            MathTex(rf"\text{{terminal value:}}\ {base['terminal']:,.0f}".replace(",", "{,}"), font_size=32, color=VALUE),
            MathTex(rf"\text{{firm value:}}\ {base['value']:,.0f}".replace(",", "{,}"), font_size=38),
            label(rf"{100 * d['base_tv_share']:.0f}\% of it is the terminal value", font_size=24, color=VALUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.6)
        tv = cmath(r"\text{TV}_5", r"=", r"\frac{\text{FCF}_5\,(1 + g)}{r - g}", font_size=34,
                   colors={r"\text{TV}_5": VALUE}).next_to(side, DOWN, buff=0.4).align_to(side, LEFT)
        with self.voiceover(
            "A standard valuation: five years of explicit forecasts, free cash flow of a hundred growing five "
            "percent a year, and after that a terminal value, Gordon's formula again, assuming two percent growth "
            "forever. Discount it all at eight percent. <bookmark mark='a'/> The five forecast years, the ones the "
            "analyst actually thought about, are worth about four hundred and sixty. <bookmark mark='b'/> The "
            "terminal value, one line of arithmetic about everything after year five, is worth nearly fifteen "
            f"hundred. {100 * d['base_tv_share']:.0f} percent of the answer is the part nobody forecast."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[:2]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[:5]], lag_ratio=0.2), FadeIn(xl[:5]),
                      FadeIn(side[2]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[5], DOWN), FadeIn(xl[5]), FadeIn(side[3]), FadeIn(tv))
            self.play(FadeIn(side[4]), FadeIn(side[5]))
        self.wait(0.4)
        self.clear_scene()

    def surface(self, d):
        ax = ThreeDAxes(x_range=[0.06, 0.12, 0.02], y_range=[0.0, 0.04, 0.01], z_range=[0, 5600, 1000], x_length=7.0,
                        y_length=5.0, z_length=3.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.7 + RIGHT * 0.6)
        surf = price_surface(ax, lambda r, g: fdcf(r, g)["value"], (0.06, 0.12), (0.0, 0.04), resolution=(36, 24),
                             z_lo=900, z_hi=5500)

        def pin(r, g, col):
            v = fdcf(r, g)["value"]
            return VGroup(Line(ax.c2p(r, g, 0), ax.c2p(r, g, v), stroke_color=col, stroke_width=3),
                          Dot3D(ax.c2p(r, g, v), radius=0.08, color=col))

        p0, p1 = pin(0.08, 0.02, WHITE), pin(0.07, 0.03, YELLOW)
        hint = VGroup(label(r"discount rate $r$: 6\% to 12\%", font_size=24, color=QC.IMPLIED),
                      label(r"terminal growth $g$: 0\% to 4\%", font_size=24, color=CASH),
                      label(r"firm value", font_size=24, color=VALUE)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        hint.to_corner(UL, buff=0.4)
        rd = VGroup(
            MathTex(rf"r = 8\%,\ g = 2\%:\ {fdcf(0.08, 0.02)['value']:,.0f}".replace(",", "{,}"), font_size=30),
            MathTex(rf"r = 7\%,\ g = 2\%:\ {fdcf(0.07, 0.02)['value']:,.0f}".replace(",", "{,}"), font_size=30,
                    color=GREY_A),
            MathTex(rf"r = 8\%,\ g = 3\%:\ {fdcf(0.08, 0.03)['value']:,.0f}".replace(",", "{,}"), font_size=30,
                    color=GREY_A),
            MathTex(rf"r = 7\%,\ g = 3\%:\ {d['alt']:,.0f}\ \ (+{100 * (d['alt'] / d['base'] - 1):.0f}\%)".replace(",", "{,}"),
                    font_size=30, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.4)
        lo, hi = fdcf(0.12, 0.0)["value"], fdcf(0.06, 0.04)["value"]
        rng = label(rf"over this ordinary range of assumptions, from {lo:,.0f} to {hi:,.0f}".replace(",", "{,}"),
                    font_size=22, color=GREY_B).to_corner(DR, buff=0.35)
        self.set_camera_orientation(phi=66 * DEGREES, theta=-125 * DEGREES, zoom=0.78)
        self.add_fixed_in_frame_mobjects(hint, rd, rng)
        self.remove(hint, rd, rng)
        with self.voiceover(
            "Now let the two numbers nobody can know vary: the discount rate, from six to twelve percent, and the "
            "growth rate forever, from nothing to four percent. Each point on this surface is the firm's value. "
            "<bookmark mark='a'/> Our valuation sits here, at about nineteen hundred. <bookmark mark='b'/> Take "
            "one point off the discount rate: twenty-three hundred. Add one point of growth instead: twenty-two "
            "hundred. Do both, and the same firm, with the same five years of forecasts, is worth forty-five percent "
            "more. <bookmark mark='c'/> The surface rises steeply into the corner where growth approaches the "
            "discount rate, the same cliff as Gordon's formula. Across ordinary assumptions the value runs from "
            "about a thousand to over five thousand. A DCF is less a measurement than a translation: it turns "
            "beliefs about rates and growth into a price, and the market's price can be turned back into the beliefs "
            "it implies."
        ) as vo:
            self.play(FadeIn(hint), Create(ax), run_time=1.5)
            self.play(Create(surf), run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(p0), FadeIn(rd[0]))
            vo.wait_until("b")
            self.play(FadeIn(rd[1]), FadeIn(rd[2]))
            self.play(FadeIn(p1), FadeIn(rd[3]))
            vo.wait_until("c")
            self.move_camera(theta=-160 * DEGREES, phi=70 * DEGREES, added_anims=[FadeIn(rng)],
                             run_time=max(vo.remaining(1.0) - 1.0, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, surf, p0, p1)), FadeOut(hint),
                                                                  FadeOut(rd), FadeOut(rng)], run_time=1.5)
        self.clear_scene()
