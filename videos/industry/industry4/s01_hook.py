from __future__ import annotations

from videos.industry.industry4.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.line()
        self.curve()
        self.title()

    def line(self):
        W = R["wright"]
        place = tx("Buffalo, New York  ·  1936", 26, GREY_B).to_edge(UP, buff=0.35)
        fac = draw.factory(3.2).move_to([-4.6, 0.6, 0])
        belt = draw.conveyor(7.6, 6, item_color="#9FB8F2", item=0.0001)
        belt.items.set_opacity(0)
        belt.move_to([0.9, -0.55, 0])
        planes = VGroup(*[draw.plane(1.3) for _ in range(5)])
        for k, p in enumerate(planes):
            p.move_to([-2.5 - 1.6 * k, -0.15, 0])
        count = ValueTracker(1)
        hours = ValueTracker(W["hours"][0])
        ctr = always_redraw(lambda: VGroup(
            tx("aircraft built so far", 18, GREY_B),
            tx(f"{int(round(count.get_value())):,}", 40, "#9FB8F2", bold=True)).arrange(DOWN, buff=0.06).move_to(
            [-4.6, -2.35, 0]))
        bar_bg = Rectangle(width=0.7, height=3.2, stroke_color=GREY_D, stroke_width=1.5, fill_opacity=0).move_to(
            [5.4, 0.85, 0], aligned_edge=DOWN).shift(DOWN * 1.6)

        def bar():
            h = 3.2 * hours.get_value() / W["hours"][0]
            return Rectangle(width=0.7, height=max(h, 0.02), stroke_width=0, fill_color=VAR, fill_opacity=0.9).move_to(
                bar_bg.get_bottom(), aligned_edge=DOWN)
        hbar = always_redraw(bar)
        hlab = always_redraw(lambda: VGroup(
            tx("hours of work in the next one", 17, GREY_B),
            tx(f"{100 * round(hours.get_value() / 100):,.0f}", 32, VAR, bold=True)).arrange(DOWN, buff=0.05).next_to(
            bar_bg, DOWN, buff=0.15))
        tag = estimate_tag("illustrative: an 80% curve from 100,000 hours", corner=DR)
        with self.voiceover(
            "In 1936 an engineer at the Curtiss-Wright aircraft company in Buffalo, Theodore Wright, published a "
            "paper about a pattern he had been watching on the factory floor for more than a decade. "
            "<bookmark mark='a'/> Build an aeroplane, then another, then another. Each one takes less work than the "
            "one before: the workers learn, the jigs improve, the steps get reorganized. <bookmark mark='b'/> And the "
            "fall follows a rule. Every time the number built so far doubles, the hours of work in the next one fall "
            "by about a fifth. <bookmark mark='c'/> Two planes, four, eight, sixteen: a fifth off, and a fifth off "
            "again. After a hundred and twenty-eight aircraft, the next one takes about a fifth of the work of the "
            "first."
        ) as vo:
            self.play(FadeIn(place), FadeIn(fac), FadeIn(belt), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(planes[0], shift=RIGHT * 0.3), FadeIn(ctr), FadeIn(bar_bg), FadeIn(hbar), FadeIn(hlab))
            self.play(planes[0].animate.shift(RIGHT * 5.4), run_time=1.6, rate_func=smooth)
            vo.wait_until("b")
            for k in range(1, 8):
                p = planes[k % 5]
                p.move_to([-2.5, -0.15, 0])
                self.add(p)
                self.play(p.animate.shift(RIGHT * 5.4), count.animate.set_value(W["units"][k]),
                          hours.animate.set_value(W["hours"][k]), run_time=0.9 if k < 4 else 0.7)
                if k == 3:
                    vo.wait_until("c")
        self.clear_scene()

    def curve(self):
        W = R["wright"]
        ax = CornerAxes(x_range=[0, 7.4, 1], y_range=[0, 110, 20], x_length=8.0, y_length=4.6,
                        axis_config=dict(color=GREY_B, include_ticks=False)).move_to([0.2, -0.3, 0])
        xl = tx("doublings of the number built", 20, GREY_B).next_to(ax, DOWN, buff=0.3)
        yl = tx("hours in the next aircraft (thousands)", 20, GREY_B).rotate(PI / 2).next_to(ax, LEFT, buff=0.3)
        xs = np.linspace(0, 7, 120)
        b = W["b"]
        curve = ax.plot(lambda x: 100 * (2 ** x) ** -b, x_range=[0, 7], color=VAR, stroke_width=4)
        dots = VGroup(*[Dot(ax.c2p(k, W["hours"][k] / 1000), radius=0.07, color=VAR) for k in range(8)])
        steps = VGroup(*[MathTex(r"\times 0.8", font_size=26, color=GREY_A).move_to(
            ax.c2p(k + 0.5, W["hours"][k] / 1000 * 0.92 + 6)) for k in range(4)])
        eq = MathTex(r"\text{cost}_n \;=\; \text{cost}_1 \times n^{-b},\qquad 2^{-b} = 0.8", font_size=40,
                     color=WHITE).to_edge(UP, buff=0.5)
        punch = tx("Costs are not fixed facts. They fall with experience,\nand they fall fastest for whoever has made the most.",
                   26, PRICE).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Draw it, and you get one of the most useful curves in all of industry. <bookmark mark='a'/> Each step "
            "to the right is a doubling; each step down, the same twenty percent. <bookmark mark='b'/> Wright wrote "
            "it as a power law: the cost of the n-th unit is the cost of the first times n to a negative power. "
            "Economists call it the learning curve, or Wright's law, and it has since been found in ships, chips, "
            "cars, batteries and solar panels. <bookmark mark='c'/> It says something unsettling: costs are not "
            "fixed facts about a product. They fall with experience, and they fall fastest for whoever has made the "
            "most."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(curve), LaggedStart(*[FadeIn(d, scale=1.6) for d in dots], lag_ratio=0.15), run_time=2.4)
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(Write(eq))
            vo.wait_until("c")
            self.play(FadeIn(punch, shift=UP * 0.1))
        del xs
        self.clear_scene()

    def title(self):
        card_ = part_title(PART, ASK)
        with self.voiceover(
            "Industry, Built. Part four: the cost curve. What does one more cost, and why does that decide almost "
            "everything? This part follows costs through factories, airlines, power stations and chip plants, "
            "and shows how the shape of an industry's costs sets its prices, its fights and its winners."
        ):
            self.play(FadeIn(card_[0]), run_time=0.8)
            self.play(FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.2)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
