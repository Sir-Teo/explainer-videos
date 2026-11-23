from __future__ import annotations

from videos.industry.industry4.common import *  # noqa: F403


class Order(VoiceoverScene):
    def construct(self):
        card(self, 1, "Take the order?", "Would you sell below what it costs you to make?",
             "Chapter one. Take the order?", lit=("dollar", "make"))
        self.situation()

    def situation(self):
        P = R["plant"]
        fac = draw.factory(2.6).move_to([-4.6, 1.55, 0])
        belt = draw.conveyor(5.2, 8, item_color=VAR, item=0.26).move_to([-3.9, -0.2, 0])
        for k, it in enumerate(belt.items):
            if k % 2:
                it.set_opacity(0)
        cap = tx("half the plant is idle: 200,000 of 400,000 a year", 20, GREY_B).next_to(belt, DOWN, buff=0.3)

        # the average-cost curve
        ax = CornerAxes(x_range=[0, 420, 100], y_range=[0, 140, 20], x_length=5.6, y_length=4.2,
                        axis_config=dict(color=GREY_B, include_ticks=False)).move_to([3.5, 0.15, 0])
        xl = tx("units a year (thousands)", 17, GREY_B).next_to(ax, DOWN, buff=0.15)
        yl = tx("$ per unit", 17, GREY_B).rotate(PI / 2).next_to(ax, LEFT, buff=0.15)
        ticks = VGroup(*[tx(f"{v}", 14, GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.05) for v in (100, 200, 300, 400)],
                       *[tx(f"${v}", 14, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.05) for v in (40, 80, 120)])
        ac = ax.plot(lambda q: P["variable"] + P["fixed"] / (q * 1000), x_range=[80, 400], color=FIXED, stroke_width=4)
        vc = ax.plot(lambda q: P["variable"], x_range=[0, 400], color=VAR, stroke_width=3)
        ac_t = tx("average cost", 18, FIXED).next_to(ax.c2p(110, 131), RIGHT, buff=0.1)
        vc_t = tx("cost of one more: $40", 18, VAR).next_to(ax.c2p(250, 40), DOWN, buff=0.1)
        price = DashedLine(ax.c2p(0, P["price"]), ax.c2p(400, P["price"]), stroke_color=PRICE, stroke_width=2.5)
        price_t = tx("your price: $80", 18, PRICE).next_to(ax.c2p(320, 80), UP, buff=0.08)
        q = ValueTracker(200)
        dot = always_redraw(lambda: glow_dot(ax.c2p(q.get_value(), P["variable"] + P["fixed"] / (q.get_value() * 1000)),
                                             color=FIXED, radius=0.09))
        eq = MathTex(r"\text{average cost} = \$40 + \frac{\$10{,}000{,}000}{\text{units}}", font_size=32).move_to(
            [3.5, 3.0, 0])
        profit = ValueTracker(P["profit"] / 1e6)
        pr = always_redraw(lambda: VGroup(
            tx("profit this year", 18, GREY_B),
            tx(f"${profit.get_value():+.1f}m".replace("+", "+ ").replace("-", "- "), 36,
               PROFIT if profit.get_value() >= -0.05 else LOSS, bold=True)).arrange(DOWN, buff=0.05).move_to(
            [-4.6, -2.75, 0]))
        tag = estimate_tag("illustrative: a model plant", corner=DR)
        with self.voiceover(
            "Start with a decision, and make it yourself. <bookmark mark='a'/> You run a factory. Its rent, its "
            "machines, its managers and its loans cost ten million dollars a year whether it makes anything or not. "
            "Each unit it makes adds forty dollars of materials, power and labour. <bookmark mark='b'/> Business is "
            "slow: you are selling two hundred thousand units a year at eighty dollars, and half the plant stands "
            "idle. <bookmark mark='c'/> Spread the ten million over two hundred thousand units and each one really "
            "costs you ninety dollars: forty of its own, and fifty of the fixed costs. At eighty dollars you are "
            "losing two million a year."
        ) as vo:
            self.play(FadeIn(fac), FadeIn(belt), FadeIn(tag))
            draw.run_belt(belt, 0.6)
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(ticks), Write(eq))
            self.play(Create(vc), FadeIn(vc_t))
            vo.wait_until("b")
            self.play(FadeIn(cap), Create(price), FadeIn(price_t))
            vo.wait_until("c")
            self.play(Create(ac), FadeIn(ac_t), run_time=1.5)
            self.play(FadeIn(dot), FadeIn(pr))

        truck = draw.truck(1.8).move_to([-9, -1.6, 0])
        offer = VGroup(tx("an offer", 18, GREY_B), tx("100,000 more units", 24, bold=True),
                       tx("at $60 each", 28, PRICE, bold=True)).arrange(DOWN, buff=0.06).move_to([0.2, 2.6, 0])
        box = SurroundingRectangle(offer, color=PRICE, buff=0.2, corner_radius=0.12)
        ask = tx("$60 is below your $90 average cost. Take it?", 30, bold=True).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Then a new customer calls. <bookmark mark='a'/> She wants a hundred thousand units, for a market you do "
            "not sell to, at sixty dollars each. <bookmark mark='b'/> Sixty is well below your ninety-dollar average "
            "cost. Do you take it? Pause and decide."
        ) as vo:
            vo.wait_until("a")
            self.play(truck.animate.move_to([-1.6, -1.6, 0]), FadeIn(offer), Create(box), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(ask, shift=UP * 0.1))
        self.wait(2.0)

        extra = VGroup(*[it for k, it in enumerate(belt.items) if k % 2 and k < 6])
        gain = MathTex(r"100{,}000 \times (\$60 - \$40) = +\$2{,}000{,}000", font_size=32, color=PROFIT).move_to(
            [3.5, -2.85, 0])
        with self.voiceover(
            "Take it. <bookmark mark='a'/> The ten million of fixed costs is spent whatever you decide. The order "
            "only has to cover what it adds: forty dollars a unit. Each unit brings in sixty, so each one adds twenty "
            "dollars of profit. <bookmark mark='b'/> A hundred thousand of them add two million, and your two-million "
            "loss becomes break-even. Your average cost falls too, to about seventy-three dollars, because the fixed "
            "costs are now spread over three hundred thousand units. <bookmark mark='c'/> The lesson of this whole "
            "part is in that decision. What matters for a choice is what it changes: the cost of one more, not the "
            "average. One warning: if your regular customers find out and demand sixty dollars too, the arithmetic "
            "turns against you, and in the long run every cost, fixed ones included, has to be paid."
        ) as vo:
            self.play(FadeOut(ask), Indicate(vc, color=VAR), Indicate(vc_t, color=VAR))
            vo.wait_until("a")
            self.play(Write(gain))
            vo.wait_until("b")
            self.play(extra.animate.set_opacity(1), q.animate.set_value(300), profit.animate.set_value(
                P["profit_after"] / 1e6), truck.animate.shift(RIGHT * 0.01), run_time=2.5)
            vo.wait_until("c")
            self.play(Indicate(eq, color=FIXED))
        belt.items.clear_updaters()
        self.clear_scene()
