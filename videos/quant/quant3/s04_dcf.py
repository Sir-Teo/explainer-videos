from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import valuation
from videos.quant.quant3.common import CASH, DEBT, EQUITY, PART, VALUE, live, load

FCF = 100 * 1.05 ** np.arange(1, 6)


def fdcf(r, g):
    return valuation.dcf(FCF, r, g)


class DCF(VoiceoverScene, ThreeDScene):
    def construct(self):
        d = load("dcf")
        mc = load("dcf_mc")
        self.card()
        self.fcf()
        self.driver()
        self.bars(d)
        self.surface(d)
        self.ronic(mc)
        self.monte_carlo(mc)

    def card(self):
        c = chapter_card(6, r"Free cash flow and the DCF surface", r"What is a whole firm worth?", part=PART)
        with self.voiceover("Chapter six. Free cash flow, and the DCF surface."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def fcf(self):
        rows = [
            cmath(r"\text{FCFF}", r"=", r"\text{EBIT}(1 - t)", r"+", r"\text{Dep}", r"-", r"\text{Capex}", r"-",
                  r"\Delta\text{NWC}", font_size=38, colors={r"\text{FCFF}": CASH}),
            cmath(r"\text{FCFF}", r"=", r"\text{NOPAT}\,(1 - \text{IR})", r",\quad", r"\text{IR} = \frac{\text{Capex} - "
                  r"\text{Dep} + \Delta\text{NWC}}{\text{NOPAT}}", font_size=38, colors={r"\text{FCFF}": CASH}),
            cmath(r"g", r"=", r"\text{IR}\times\text{RONIC}", font_size=42, colors={r"g": CASH}),
        ]
        whys = [why(r"chapter 3's cash flow statement before any payment to lenders or owners: operating profit after "
                    r"tax, depreciation added back, net investment taken off"),
                why(r"NOPAT: net operating profit after tax; IR: the share of it reinvested"),
                why(r"profits grow only by reinvesting: each reinvested dollar earns the return on new invested capital")]
        step = ladder(self, rows, whys, keep=3, top=2.5, x=-1.2, buff=0.85, edge=6.9)
        with self.voiceover(
            "To value a whole firm rather than one share, an analyst discounts its free cash flow. Read it off chapter three's "
            "ledgers: operating profit after tax, plus the depreciation that cost no cash, minus the spending on new plant, minus "
            "the cash tied up in working capital. It is the cash the business could pay to all its investors, lenders and owners "
            "together. <bookmark mark='a'/> Write the investment as a share of after-tax operating profit, the reinvestment rate, "
            "and free cash flow is profit times one minus that rate. <bookmark mark='b'/> And growth is not free. Profits grow only "
            "because something was reinvested, and each reinvested dollar earns the return on new invested capital, RONIC. So "
            "growth equals the reinvestment rate times RONIC."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def driver(self):
        rows = [
            cmath(r"\text{TV}", r"=", r"\frac{\text{FCFF}_{T+1}}{\text{WACC} - g}", r"=",
                  r"\frac{\text{NOPAT}_{T+1}\,(1 - g/\text{RONIC})}{\text{WACC} - g}", font_size=40,
                  colors={r"\text{TV}": VALUE}),
            cmath(r"\frac{\partial\,\text{TV}}{\partial g}", r"\propto", r"\frac{1}{\text{WACC}} - \frac{1}{\text{RONIC}}",
                  font_size=40, colors={r"\frac{\partial\,\text{TV}}{\partial g}": VALUE}),
            cmath(r"\frac{\partial\,\text{TV}}{\partial g} > 0", r"\iff", r"\text{RONIC} > \text{WACC}", font_size=42,
                  colors={r"\text{RONIC} > \text{WACC}": QC.HOUSE}),
        ]
        whys = [why(r"steady state: positive NOPAT, fixed RONIC and WACC, $g<\text{WACC}$; "
                    r"$\text{IR}=g/\text{RONIC}$ (Koller et al.)"),
                why(r"differentiate in $g$: the sign is that of $\text{RONIC} - \text{WACC}$"),
                why(r"growth creates value only where new investment earns more than it costs")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-0.6, buff=0.5, edge=6.9)
        bridge = wrapped_label(r"the bridge to equity: enterprise value $-$ net debt $-$ minorities $-$ preferred "
                               r"$-$ debt-like items (leases, pension deficits) $+$ non-operating assets", 12.0, 22,
                               GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Put that into Gordon's formula for the value after the forecast years. Free cash flow is profit times one minus g over "
            "RONIC, and the terminal value becomes McKinsey's value-driver formula. <bookmark mark='a'/> Differentiate it in g, and "
            "the sign of the result is the sign of RONIC minus the cost of capital. <bookmark mark='b'/> Faster growth adds value "
            "only if new investment earns more than it costs. A firm that earns exactly its cost of capital can double its growth "
            "and be worth not a cent more. <bookmark mark='c'/> That value is the enterprise's. Owners get it after the lenders: "
            "subtract net debt, minority interests, preferred stock and the debt-like items, leases and pension deficits, and add "
            "back anything the business does not need."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(bridge))
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
            "A standard valuation: five years of forecasts, free cash flow of a hundred growing five percent, then two percent "
            "forever, all discounted at eight. <bookmark mark='a'/> The five forecast years are worth about four hundred and "
            "sixty. <bookmark mark='b'/> The terminal value, one line of arithmetic about everything after, is worth nearly "
            f"fifteen hundred: {100 * d['base_tv_share']:.0f} percent of the answer."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[:2]), GrowFromEdge(bars[0], DOWN), FadeIn(xl[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[1:5]], lag_ratio=0.2), FadeIn(xl[1:5]),
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
            "Now vary the two numbers nobody knows: the discount rate from six to twelve percent, growth forever from nothing to "
            "four. <bookmark mark='a'/> Our valuation sits here, about nineteen hundred. <bookmark mark='b'/> A point less on the "
            "rate and a point more of growth: forty-five percent more, for the same forecasts. <bookmark mark='c'/> The surface "
            "climbs into the corner where growth nears the rate, Gordon's cliff. A DCF translates beliefs about rates and growth "
            "into a price, and a price can be translated back."
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
        self.play(FadeOut(VGroup(ax, surf, p0, p1)), FadeOut(hint), FadeOut(rd), FadeOut(rng), run_time=0.4)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1)
        self.clear()

    def ronic(self, mc):
        gs, ron, S = np.asarray(mc["gs"]), np.asarray(mc["ronic"]), np.asarray(mc["vd"])
        ax = ThreeDAxes(x_range=[0, 0.05, 0.01], y_range=[0.04, 0.20, 0.04], z_range=[0, 2400, 400], x_length=6.4,
                        y_length=5.0, z_length=3.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 1.1 + RIGHT * 0.4)  # low enough that the peak stays under the readout in the top-right corner

        def f(g_, r_):
            return float(np.clip(1250 * 0.08 * (1 - g_ / r_) / (0.08 - g_), 0, 2400))

        surf = loss_surface(ax, f, (0.0, 0.05), (0.04, 0.20), resolution=(26, 24), z_lo=300, z_hi=2400)
        ridge = ParametricFunction(lambda u: ax.c2p(u, 0.08, f(u, 0.08)), t_range=[0, 0.05], color=QC.HOUSE,
                                   stroke_width=6)
        balls = VGroup(*[Dot3D(ax.c2p(0.0, rr, f(0.0, rr)), radius=0.1, color=c_)
                         for rr, c_ in ((0.16, QC.GAIN), (0.05, QC.LOSS))])
        hint = VGroup(label(r"growth $g$: 0 to 5\%", font_size=22, color=CASH),
                      label(r"RONIC: 4\% to 20\%", font_size=22, color=QC.HOUSE),
                      label(r"value of NOPAT 100 at WACC 8\%", font_size=22, color=VALUE)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                buff=0.1)
        hint.to_corner(UL, buff=0.4)
        rd = VGroup(MathTex(rf"\text{{RONIC}} = \text{{WACC}}:\ {mc['vd_flat']:,.0f}\ \text{{for every }} g"
                            .replace(",", "{,}"), font_size=28, color=QC.HOUSE),
                    MathTex(r"\text{RONIC } 16\%:\ \text{growth uphill}", font_size=28, color=QC.GAIN),
                    MathTex(r"\text{RONIC } 5\%:\ \text{growth downhill}", font_size=28, color=QC.LOSS))
        rd.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.5)  # the landscape peaks top-right; the lower-right corner stays empty
        clipnote = wrapped_label(r"surface clipped to 0--2{,}400; $g>\text{RONIC}$ requires external funding",
                                 6.8, 16, GREY_B).to_corner(DL, buff=0.3)
        self.set_camera_orientation(phi=66 * DEGREES, theta=-130 * DEGREES, zoom=0.72)
        self.add_fixed_in_frame_mobjects(hint, rd, clipnote)
        self.remove(hint, rd, clipnote)
        with self.voiceover(
            "That statement as a landscape: growth across, RONIC back, and the value of a hundred of operating profit at an eight "
            "percent cost of capital. <bookmark mark='a'/> Along the orange line, RONIC equals the cost of capital and the "
            "surface is flat. <bookmark mark='b'/> A firm earning sixteen percent rolls uphill as it grows. "
            "<bookmark mark='c'/> One earning five rolls downhill: growth bought below the cost of capital destroys value."
        ) as vo:
            self.play(FadeIn(hint), FadeIn(clipnote), Create(ax), run_time=1.5)
            self.play(Create(surf), run_time=3)
            vo.wait_until("a")
            self.play(Create(ridge), FadeIn(rd[0]))
            vo.wait_until("b")
            self.play(FadeIn(balls[0]), FadeIn(rd[1]))
            self.play(balls[0].animate.move_to(ax.c2p(0.05, 0.16, f(0.05, 0.16))), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(balls[1]), FadeIn(rd[2]))
            self.play(balls[1].animate.move_to(ax.c2p(0.05, 0.05, f(0.05, 0.05))), run_time=2.5)
            self.move_camera(theta=-116 * DEGREES, run_time=max(vo.remaining(1.0) - 0.5, 1.0))
        self.play(FadeOut(VGroup(ax, surf, ridge, balls)), FadeOut(hint), FadeOut(rd), FadeOut(clipnote), run_time=0.4)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1)
        self.clear()

    def monte_carlo(self, mc):
        V = np.asarray(mc["V"])
        base = mc["base"]
        g = axes([800, 4000], [0, 1.0], x_length=8.4, y_length=4.0, xlabel=r"firm value",
                 xticks=[1000, 2000, 3000, 4000], yticks=[], font_size=17).move_to(DOWN * 0.6 + LEFT * 1.6)
        ax = g.ax
        bins = np.linspace(800, 4000, 41)
        k = ValueTracker(32)

        def hist():
            n = int(k.get_value())
            if n < 1:
                return VGroup()
            h, _ = np.histogram(np.clip(V[:n], 800, 3999), bins=bins)
            h = h / max(h.max(), 1)
            w = ax.c2p(bins[1], 0)[0] - ax.c2p(bins[0], 0)[0]
            return VGroup(*[Rectangle(width=w * 0.92, height=max(v * 3.6, 0.002), stroke_width=0, fill_color=VALUE,
                                      fill_opacity=0.8).move_to(ax.c2p((a + b) / 2, 0), aligned_edge=DOWN)
                            for a, b, v in zip(bins[:-1], bins[1:], h)])

        def counter():
            return live(r"\text{draws:}", int(k.get_value()), 0, font_size=28, color=GREY_A,
                        group_sep=True).to_corner(UL, buff=0.5)

        hb, cnt = always_redraw(hist), always_redraw(counter)
        bl = DashedLine(ax.c2p(base, 0), ax.c2p(base, 1.0), color=WHITE, stroke_width=2)
        bt = label(rf"base case {base:,.0f}".replace(",", "{,}"), font_size=20).next_to(bl, UP, buff=0.08)
        band_ = VGroup(DashedLine(ax.c2p(mc["q05"], 0), ax.c2p(mc["q05"], 0.85), color=QC.HOUSE),
                       DashedLine(ax.c2p(mc["q95"], 0), ax.c2p(mc["q95"], 0.85), color=QC.HOUSE))
        side = VGroup(
            label(r"20{,}000 draws:", font_size=22, color=GREY_A),
            MathTex(r"r \sim U[6\%, 10\%]", font_size=28, color=QC.IMPLIED),
            MathTex(r"g \sim U[0, 3\%]", font_size=28, color=CASH),
            MathTex(r"\text{cash flow} \times U[0.8, 1.2]", font_size=28),
            MathTex(rf"5\text{{--}}95\%:\ {mc['q05']:,.0f}\ \text{{to}}\ {mc['q95']:,.0f}".replace(",", "{,}"),
                    font_size=30, color=QC.HOUSE),
            MathTex(rf"= {mc['q05'] / base:.2f}\times\ \text{{to}}\ {mc['q95'] / base:.2f}\times\ \text{{base}}",
                    font_size=28, color=QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4)
        pp = desk_question(r"Pause and predict: a firm earns exactly its cost of capital on new investment. What "
                           r"does faster growth add?", width=6.4, font_size=21).to_edge(UP, buff=0.3).shift(RIGHT * 2.6)
        with self.voiceover(
            "A Monte Carlo shows what not knowing the inputs does: draw the rate, the growth and the cash flows, and value the "
            "firm each time. <bookmark mark='a'/> Twenty thousand valuations pile up. <bookmark mark='b'/> The middle ninety "
            f"percent runs from {mc['q05']:,.0f} to {mc['q95']:,.0f}, with a long right tail. A DCF that reports one number is "
            "reporting one draw. <bookmark mark='c'/> Pause and predict: a firm earns exactly its cost of capital on new "
            "investment. What does faster growth add? Nothing."
            " Every number on that surface hangs on one input, the discount rate. Next: the rate the market itself implies."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[:4]), Create(bl), FadeIn(bt))
            self.add(hb, cnt)
            vo.wait_until("a")
            self.play(k.animate.set_value(len(V)), run_time=8, rate_func=lambda x: x ** 2)
            vo.wait_until("b")
            self.play(Create(band_), FadeIn(side[4:]))
            vo.wait_until("c")
            self.play(FadeIn(pp))
        hb.clear_updaters()
        cnt.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
