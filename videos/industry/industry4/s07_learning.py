from __future__ import annotations

import math

from videos.industry.industry4.common import *  # noqa: F403

# the chart's frame on screen
XL, XR, YB, YT = -5.2, 4.6, -2.7, 2.2


def view_a(year, price, cap=None):
    """Years across, price up (linear)."""
    return np.array([XL + (XR - XL) * (year - 1975) / 50, YB + (YT - YB) * price / 140, 0])


def view_b(year, price, cap=None):
    """Years across, price up on a log scale ($0.10 to $200)."""
    return np.array([XL + (XR - XL) * (year - 1975) / 50,
                     YB + (YT - YB) * (math.log10(price) + 1) / (math.log10(200) + 1), 0])


def view_c(year, price, cap):
    """Capacity built so far across (log, 1 to 4,096 GW), price up (log)."""
    return np.array([XL + (XR - XL) * math.log2(cap) / 12,
                     YB + (YT - YB) * (math.log10(price) + 1) / (math.log10(200) + 1), 0])


class Learning(VoiceoverScene):
    def construct(self):
        card(self, 6, "Learning", "Why do some things get cheaper every year?",
             "Chapter six. Learning.", lit=("make", "dollar"))
        self.panel()
        self.chart()

    def panel(self):
        S = R["solar"]
        p75, p25 = S["price"][1975], S["price"][2025]
        pan = draw.solar_panel(3.2).move_to([-3.3, 0.3, 0])
        year = ValueTracker(1975)
        yrs = sorted(S["price"])

        def price_at(y):
            y0 = max(v for v in yrs if v <= y) if y >= yrs[0] else yrs[0]
            y1 = min(v for v in yrs if v >= y) if y <= yrs[-1] else yrs[-1]
            if y1 == y0:
                return S["price"][y0]
            t = (y - y0) / (y1 - y0)
            return math.exp((1 - t) * math.log(S["price"][y0]) + t * math.log(S["price"][y1]))
        yr = draw.number(lambda: year.get_value(), 0, size=48, color=GREY_A, commas=False)
        yr.add_updater(lambda m: m.move_to([-3.3, 2.75, 0]), call_updater=True)
        tag_box = RoundedRectangle(corner_radius=0.12, width=3.6, height=1.5, stroke_color=PRICE, stroke_width=3,
                                   fill_color="#141A24", fill_opacity=1).move_to([3.0, 0.9, 0])
        hole = Circle(radius=0.09, stroke_color=PRICE, stroke_width=2).move_to(tag_box.get_left() + RIGHT * 0.3)
        string = Line(hole.get_center(), pan.get_right() + UP * 0.4, stroke_color=GREY_B, stroke_width=1.5)
        w_t = tx("per watt, in 2025 dollars", 18, GREY_B).next_to(tag_box, DOWN, buff=0.15)
        price = draw.number(lambda: price_at(year.get_value()), 2, prefix="$", size=52, color=PRICE)
        price.add_updater(lambda m: m.move_to(tag_box.get_center() + RIGHT * 0.2), call_updater=True)
        roof = draw.number(lambda: 300 * price_at(year.get_value()), 0, prefix="$", size=40, color=WHITE)
        roof.add_updater(lambda m: m.move_to([3.0, -1.55, 0]), call_updater=True)
        roof_t = tx("a 300-watt panel, like one on a roof today", 18, GREY_B).move_to([3.0, -2.15, 0])
        src = source("IRENA and other sources, via Our World in Data; module prices, constant 2025 dollars")
        with self.voiceover(
            "In 1975 a solar module, the panel itself without the frame or the wiring, cost about "
            f"{p75:.0f} dollars for every watt it could produce, in today's money. <bookmark mark='a'/> A panel the "
            "size of one on a roof today would have cost about forty thousand dollars. Solar power was for "
            "satellites. <bookmark mark='b'/> Then, year after year, the price fell. <bookmark mark='c'/> By 2025 "
            f"a watt cost about {100 * p25:.0f} cents. The same panel: about thirty-six dollars. The price fell more "
            f"than a thousandfold."
        ) as vo:
            self.play(FadeIn(pan), FadeIn(yr), FadeIn(src))
            self.play(Create(tag_box), FadeIn(hole), Create(string), FadeIn(price), FadeIn(w_t))
            vo.wait_until("a")
            self.play(FadeIn(roof), FadeIn(roof_t))
            vo.wait_until("b")
            self.play(year.animate.set_value(2000), run_time=4.0, rate_func=linear)
            vo.wait_until("c")
            self.play(year.animate.set_value(2025), run_time=4.0, rate_func=linear)
        for m in (yr, price, roof):
            m.clear_updaters()
        self.clear_scene()

    def chart(self):
        S = R["solar"]
        P, C = S["price"], S["capacity"]
        years = sorted(P)
        frame = VGroup(Line([XL, YB, 0], [XR + 0.2, YB, 0], stroke_color=GREY_B, stroke_width=2),
                       Line([XL, YB, 0], [XL, YT + 0.2, 0], stroke_color=GREY_B, stroke_width=2))
        dots = VGroup(*[Dot(view_a(y, P[y]), radius=0.06, color=PRICE) for y in years])

        def ticks_x_years():
            return VGroup(*[tx(f"{y}", 17, GREY_B).next_to(view_a(y, 0), DOWN, buff=0.1) for y in (1975, 1990, 2005, 2025)])

        def ticks_y_lin():
            return VGroup(*[tx(f"${v}", 17, GREY_B).next_to([XL, view_a(1975, v)[1], 0], LEFT, buff=0.1)
                            for v in (0, 50, 100)])

        def ticks_y_log():
            return VGroup(*[tx(lab, 17, GREY_B).next_to([XL, view_b(1975, v)[1], 0], LEFT, buff=0.1)
                            for v, lab in ((0.1, "$0.10"), (1, "$1"), (10, "$10"), (100, "$100"))])

        def ticks_x_cap():
            return VGroup(*[tx(lab, 17, GREY_B).next_to([view_c(2000, 1, v)[0], YB, 0], DOWN, buff=0.1)
                            for v, lab in ((1, "1 GW"), (10, "10"), (100, "100"), (1000, "1,000"))])
        xt, yt = ticks_x_years(), ticks_y_lin()
        ylab = tx("module price per watt (2025 dollars)", 19, GREY_B).next_to([XL, YT + 0.2, 0], UP, buff=0.1).align_to(
            [XL - 0.4, 0, 0], LEFT)
        xlab = tx("year", 19, GREY_B).move_to([(XL + XR) / 2, YB - 0.75, 0])
        with self.voiceover(
            "Plot the price year by year, and you see a cliff, then a floor. <bookmark mark='a'/> But this picture "
            "hides almost everything. Every fall after 1990 looks like nothing, because the early prices were so "
            "high. <bookmark mark='b'/> Change the vertical scale so that each step up is ten times the last. A fall "
            "from a hundred dollars to ten now looks the same as a fall from a dollar to ten cents, and the cliff "
            "becomes a steady slope: the price kept falling, by roughly the same share, decade after decade."
        ) as vo:
            self.play(Create(frame), FadeIn(xt), FadeIn(yt), FadeIn(ylab), FadeIn(xlab))
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in dots], lag_ratio=0.04), run_time=2.5)
            vo.wait_until("a")
            vo.wait_until("b")
            yt2 = ticks_y_log()
            self.play(*[d.animate.move_to(view_b(y, P[y])) for d, y in zip(dots, years)], ReplacementTransform(yt, yt2),
                      run_time=3.0)
            yt = yt2

        old = VGroup(*[d for d, y in zip(dots, years) if y not in C])
        keep = [(d, y) for d, y in zip(dots, years) if y in C]
        xt2 = ticks_x_cap()
        xlab2 = tx("solar capacity built in the world so far (gigawatts, each step ×10)", 19, GREY_B).move_to(
            [(XL + XR) / 2, YB - 0.75, 0])
        with self.voiceover(
            "Now Wright's idea. <bookmark mark='a'/> Instead of the year, put along the bottom how much solar the "
            "world had built so far, again on a scale where each step is ten times the last. Capacity records start "
            "in 2000, so the earlier years drop out. <bookmark mark='b'/> The points fall onto a line. "
            "<bookmark mark='c'/> Every time the world's solar capacity has doubled, the price of a module has "
            f"fallen by about {100 * S['fit']['learning_rate']:.0f} percent. From 2000 to 2025 the capacity doubled "
            f"almost eleven times, and the price fell to about a fiftieth."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeOut(old), run_time=0.8)
            self.play(*[d.animate.move_to(view_c(y, P[y], C[y])) for d, y in keep], ReplacementTransform(xt, xt2),
                      ReplacementTransform(xlab, xlab2), run_time=3.0)
            vo.wait_until("b")
            fit = S["fit"]
            line = Line(view_c(2000, fit["a"] * 1.2 ** -fit["b"], 1.2), view_c(2025, fit["a"] * 2600 ** -fit["b"], 2600),
                        stroke_color=WHITE, stroke_width=3)
            self.play(Create(line), run_time=1.5)
            vo.wait_until("c")
            steps = VGroup()
            for k in range(3):
                c0 = 8 * 4 ** k
                a_ = view_c(2000, fit["a"] * c0 ** -fit["b"], c0)
                b_ = view_c(2000, fit["a"] * (2 * c0) ** -fit["b"], 2 * c0)
                corner = np.array([b_[0], a_[1], 0])
                steps.add(VGroup(Line(a_, corner, stroke_color=PROFIT, stroke_width=3),
                                 Line(corner, b_, stroke_color=PROFIT, stroke_width=3),
                                 MathTex(r"\times 0.7", font_size=26, color=PROFIT).next_to(corner, UR, buff=0.04)))
            self.play(LaggedStart(*[Create(s_) for s_ in steps], lag_ratio=0.3), run_time=2.4)
        law = MathTex(r"\text{price} = a \times \text{(built so far)}^{-0.5}", font_size=38).move_to([1.6, 1.75, 0])
        r2 = tx(f"fit, 2000 to 2025: {100 * S['fit']['learning_rate']:.0f}% cheaper per doubling;"
                f" R² {S['fit']['r2']:.2f}", 19, GREY_B).next_to(law, DOWN, buff=0.12)
        with self.voiceover(
            "That is Wright's aeroplane rule again, fifty years and an industry away. <bookmark mark='a'/> But be "
            "careful what it says. It is a pattern in the record, not a law of nature. <bookmark mark='b'/> Some of "
            "the fall was learning: thinner wafers, better cells, fewer broken ones. Some was scale: giant factories, "
            "most of them in China. Some was subsidy, and some was cheaper silicon. And the arrow "
            "runs both ways: building more made panels cheaper, but cheaper panels also made people build more. "
            "<bookmark mark='c'/> Still, it is one of the most reliable patterns in industry, and it has a hard "
            "edge: whoever has built the most is furthest down the curve, so the leader's costs keep falling "
            "faster than a newcomer can follow."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(law), FadeIn(r2))
            vo.wait_until("b")
            self.play(Indicate(dots[-1], scale_factor=2.0, color=PRICE))
            vo.wait_until("c")
            self.play(Indicate(law, color=PRICE))
        self.clear_scene()
