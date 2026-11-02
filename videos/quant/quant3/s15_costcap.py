from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import valuation
from videos.quant.quant3.common import CASH, DEBT, EQUITY, PART, PRICE, VALUE, load, real_data

IMPLIED_CODE = [
    "def implied_rate(price, cf0, growth, growth_long, years=5):",
    "    t = np.arange(1, years + 1)",
    "    cf = cf0 * (1 + growth) ** t",
    "    def value(r):",
    "        tv = cf[-1] * (1 + growth_long) / (r - growth_long)",
    "        return np.sum(cf / (1 + r) ** t) + tv / (1 + r) ** years",
    "    # value(r) falls as r rises, so exactly one r matches the price",
    "    return brentq(lambda r: value(r) - price, growth_long + 1e-6, 0.5)",
]


class CostOfCapital(VoiceoverScene):
    def construct(self):
        e = load("erp")
        self.card()
        self.wacc()
        self.beam(e)
        self.lab(e)
        self.history(e)

    def card(self):
        c = chapter_card(7, r"The cost of capital the market implies", r"What return does a price promise?", part=PART)
        with self.voiceover("Chapter seven. The cost of capital the market implies."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def wacc(self):
        rows = [
            cmath(r"\text{WACC}", r"=", r"\frac{E}{V}\,r_E + \frac{D}{V}\,r_D(1 - t)", font_size=40,
                  colors={r"\text{WACC}": VALUE}),
            cmath(r"\beta_E", r"=", r"\beta_A + (\beta_A - \beta_D)\,\frac{D}{E}", font_size=40,
                  colors={r"\beta_E": EQUITY}),
            cmath(r"r_E", r"=", r"r_f + \beta_E\times\text{ERP}", font_size=40, colors={r"r_E": EQUITY}),
            cmath(r"\text{APV}", r"=", r"V_U + \text{PV(tax shield)} - \text{PV(distress)}", font_size=40,
                  colors={r"\text{APV}": VALUE}),
        ]
        ex = valuation.wacc(600, 200, 0.09, 0.05, 0.21)
        whys = [why(rf"a blend of what lenders and owners demand; interest is tax-deductible. Equity 600 at 9\%, "
                    rf"debt 200 at 5\%, tax 21\%: {100 * ex:.2f}\%"),
                why(r"Modigliani--Miller's second proposition (chapter 10) applied to betas: leverage levers risk"),
                why(r"the CAPM (Part 23): the riskless rate plus beta times the equity risk premium"),
                why(r"or value the firm unlevered and add financing effects one by one: adjusted present value")]
        step = ladder(self, rows, whys, keep=4, top=2.7, x=-1.2, buff=0.62, edge=6.9)
        with self.voiceover(
            "Free cash flow is discounted at the weighted average cost of capital, debt's cost cut by the tax rate: "
            f"{100 * ex:.2f} percent for the toy firm. <bookmark mark='a'/> Leverage scales the owners' risk: the equity beta. "
            "<bookmark mark='b'/> The CAPM prices it: the riskless rate plus beta times the equity risk premium. "
            "<bookmark mark='c'/> Or value the firm unlevered and add the tax shield and distress costs: APV. Each needs one number "
            "nobody observes: the premium."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def beam(self, e):
        L = e["lab"]["2020"]
        P, cf0, g, gl = L["price"], L["cash"], L["growth"], L["bond"]
        target = L["implied"]
        r = ValueTracker(0.12)
        pivot = DOWN * 0.6

        def value(rr):
            t = np.arange(1, 6)
            cf = cf0 * (1 + g) ** t
            pv = cf / (1 + rr) ** t
            tv = cf[-1] * (1 + gl) / (rr - gl) / (1 + rr) ** 5
            return pv, tv

        scale = 1 / 2200

        def scene_():
            rr = r.get_value()
            pv, tv = value(rr)
            right = pv.sum() + tv
            tilt = float(np.clip((right - P) / P, -1, 1)) * 0.22
            beam = Line(LEFT * 4.2, RIGHT * 4.2, color=GREY_B, stroke_width=6).rotate(-tilt).move_to(pivot)
            lp, rp = beam.get_start(), beam.get_end()
            block = Rectangle(width=1.4, height=P * scale, stroke_width=0, fill_color=PRICE, fill_opacity=0.85)
            block.move_to(lp, aligned_edge=DOWN)
            bl = MathTex(rf"\text{{S\&P 500}}\ {P:,.0f}".replace(",", "{,}"), font_size=24, color=PRICE)
            bl.next_to(block, UP, buff=0.1)
            stack = VGroup()
            y = rp[1]
            for k_, v in enumerate(list(pv) + [tv]):
                h = v * scale
                stack.add(Rectangle(width=1.4, height=max(h, 0.01), stroke_width=0.5, stroke_color=BLACK,
                                    fill_color=CASH if k_ < 5 else VALUE, fill_opacity=0.85)
                          .move_to([rp[0], y + h / 2, 0]))
                y += h
            sl = MathTex(rf"\text{{PV of cash}}\ {right:,.0f}".replace(",", "{,}"), font_size=24, color=CASH)
            sl.next_to(stack, UP, buff=0.1)
            dial = MathTex(rf"r = {100 * rr:.2f}\%", font_size=40, color=QC.IMPLIED).move_to(UP * 3.0)
            return VGroup(beam, block, bl, stack, sl, dial)

        tri = Triangle(color=GREY_B, fill_opacity=1, stroke_width=0).scale(0.25).move_to(pivot + DOWN * 0.22)
        b = always_redraw(scene_)
        inputs = VGroup(
            label(rf"end-2020 inputs (Damodaran): cash paid out {cf0:.1f} a year (dividends and buybacks),", font_size=19,
                  color=GREY_A),
            label(rf"growing {100 * g:.2f}\% for five years, then at the 10-year yield, {100 * gl:.2f}\%", font_size=19,
                  color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The market's price can supply it. A balance: on the left, the S&P 500 at the end of 2020; on the right, its expected "
            "cash to owners, dividends and buybacks, growing at analysts' forecasts, then at the bond yield, each discounted. "
            "<bookmark mark='a'/> Turn the dial on the rate: at twelve percent the cash is worth too little; lower it and the stack "
            f"grows. <bookmark mark='b'/> Level at {100 * target:.2f} percent: the return the price implies. Less the ten-year "
            f"yield, {100 * (target - gl):.2f} percent is the implied premium, which Damodaran has published since 1960."
        ) as vo:
            self.add(tri, b)
            self.play(FadeIn(inputs))
            vo.wait_until("a")
            self.play(r.animate.set_value(0.035), run_time=4)
            vo.wait_until("b")
            self.play(r.animate.set_value(target), run_time=3)
        b.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def lab(self, e):
        card = lab_card(r"the implied cost of capital", IMPLIED_CODE, source="explainer/quant/house/valuation.py",
                        width=7.4, font_size=17).to_corner(UL, buff=0.3)
        rows = []
        for y in ("1999", "2008", "2020"):
            L = e["lab"][y]
            rows.append(f"{y}: price {L['price']:7.1f}  cash {L['cash']:5.1f}  -> r {100 * L['implied']:5.2f}%  "
                        f"ERP {100 * L['erp']:4.2f}%  (published {100 * L['published']:4.2f}%)")
        with self.voiceover(
            "The House's version is eight lines: the cash flows, their value at a trial rate, and a root finder. The value falls "
            "as the rate rises, so exactly one rate matches the price. <bookmark mark='a'/> Run it at three year-ends: December "
            "1999, the top of the technology bubble; December 2008, after Lehman; and December 2020. The implied premium was "
            "lowest when prices were highest and highest when everyone was frightened. Beside each, Damodaran's published number."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            lab_run(self, card, ["for year in (1999, 2008, 2020):", *rows], font_size=17)
        self.wait(0.4)
        self.clear_scene()

    def history(self, e):
        yr, ours, pub = np.asarray(e["year"]), np.asarray(e["ours"]), np.asarray(e["published"])
        w = yr <= 2020
        g = axes([1960, 2021], [0, 0.09], x_length=8.4, y_length=4.4, ylabel=r"implied equity risk premium",
                 xticks=[1960, 1980, 2000, 2020], xfmt=lambda v: f"{int(v)}", yticks=[0, 0.02, 0.04, 0.06, 0.08],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        kt = ValueTracker(0)
        l_ours = tracing(ax, yr[w], ours[w], kt, QC.HOUSE)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.045, color=GREY_A) for a, b in zip(yr[w], pub[w])])
        leg = legend([(QC.HOUSE, r"the House's rebuild"), (GREY_A, r"Damodaran's published column (dots)")],
                     font_size=20).to_edge(RIGHT, buff=0.4).shift(UP * 2.3)
        ok = e["within20"]
        side = VGroup(
            MathTex(rf"\text{{within 0.2 pt in }}{ok}\text{{ of }}{e['n_window']}\text{{ years}}", font_size=28),
            wrapped_label(r"the two agree where his inputs are the table's; they part (1995--2009) where his "
                          r"published column used cash-flow estimates the table does not carry", 4.6, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(leg, DOWN, buff=0.5).align_to(leg, LEFT)
        pp = desk_question(r"Pause and predict: in December 1999 the implied premium was about 2\%. What did that "
                           r"forecast for the next decade?", width=5.0, font_size=20).to_edge(RIGHT, buff=0.4)
        pp.to_edge(DOWN, buff=0.4)
        src = real_data(r"Damodaran, histimpl.xls (S\&P 500, year ends); rebuilt by the House's implied\_rate")
        with self.voiceover(
            "Run the rebuild for every year since 1960 and lay Damodaran's published premiums on top. <bookmark mark='a'/> "
            f"In {ok} of {e['n_window']} years they agree within a fifth of a point; where they part, mostly from 1995 to 2009, his "
            "published column used cash-flow estimates the spreadsheet's plain inputs do not carry. A rebuild that disagrees is a "
            "finding too. <bookmark mark='b'/> Read the line as a forecast: the premium was high in the late seventies, before two "
            "strong decades, and lowest in 1999. Pause and predict: what did two percent promise? <bookmark mark='c'/> Close to "
            "nothing: the 2000s were a lost decade for American stocks."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg))
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.03, run_time=2))
            self.add(l_ours)
            self.play(kt.animate.set_value(int(w.sum()) - 1), run_time=5, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(side))
            vo.wait_until("b")
            self.play(FadeIn(pp))
            vo.wait_until("c")
            self.play(Indicate(dots[int(np.flatnonzero(yr[w] == 1999)[0])], color=QC.LOSS, scale_factor=2.5))
        l_ours.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
