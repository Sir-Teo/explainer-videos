from __future__ import annotations

from videos.industry.industry9.common import *  # noqa: F403

WAITC = "#7EC8F5"


class Plan(VoiceoverScene):
    def construct(self):
        card(self, 4, "The mine plan and the option to wait", "When should a deposit be dug, and in what order?",
             "Chapter four. The mine plan, and the option to wait.", lit=("make", "change"))
        self.plan()
        self.option()

    def plan(self):
        RR = R["run"]
        out, costs, grades = RR["output"], RR["costs"], RR["grades"]
        ground = Rectangle(width=7.0, height=3.6, stroke_width=0, fill_color="#4E4034", fill_opacity=1).move_to(
            [-3.5, -0.6, 0])
        surface = Line([-7.0, 1.2, 0], [0.0, 1.2, 0], stroke_color="#C9A98A", stroke_width=2)
        shells = VGroup()
        n = 5
        for k in range(n, 0, -1):
            f = k / n
            top_w, bot_w, d = 1.6 + 4.6 * f, 0.6 + 1.4 * f, 0.6 + 2.6 * f
            col = interpolate_color(ManimColor(COPPER), ManimColor("#6B5440"), (k - 1) / (n - 1))
            shells.add(Polygon([-top_w / 2, 0, 0], [top_w / 2, 0, 0], [bot_w / 2, -d, 0], [-bot_w / 2, -d, 0],
                               stroke_color="#1A1410", stroke_width=1.5, fill_color=col, fill_opacity=1))
        shells = VGroup(*reversed(shells))  # shells[0] is the first, innermost
        for s_ in shells:
            s_.shift([-3.5, 1.2, 0])
        stage = VGroup(*[tx(f"{3 * k + 1}-{3 * k + 3}", 14, WHITE).move_to(
            shells[k].get_bottom() + UP * 0.22) for k in range(n)])
        pit_lab = tx("the mine plan: five pushbacks, the richest first", 18, GREY_A).next_to(surface, UP, buff=0.2
                                                                                               ).align_to(surface, LEFT)
        pa = viz.plot_axes([0.4, 15.6], [0, 200], x_length=5.4, y_length=2.2, xticks=[1, 5, 10, 15], yticks=[100, 200],
                           xfmt=lambda v: f"year {int(v)}", yfmt=lambda v: f"{v:g} kt", size=13).move_to([3.7, 1.6, 0])
        bars = viz.year_bars(pa, range(1, 16), out, COPPER, width=0.25)
        ttl1 = tx("copper produced", 16, COPPER).next_to(pa, UP, buff=0.08)
        pb = viz.plot_axes([0.4, 15.6], [1.5, 2.6], x_length=5.4, y_length=2.0, xticks=[1, 5, 10, 15], yticks=[2.0, 2.5],
                           xfmt=lambda v: f"year {int(v)}", yfmt=lambda v: f"${v:.2f}", size=13).move_to([3.7, -1.8, 0])
        cl = VMobject(stroke_color=COST, stroke_width=3).set_points_as_corners(
            [pb.ax.c2p(t + 1, c) for t, c in enumerate(costs)])
        ttl2 = tx("cash cost a pound", 16, COST).next_to(pb, UP, buff=0.08)
        tag = estimate_tag("the Works' model mine (mine.py): grade falls 2% a year", corner=DR, size=14)
        with self.voiceover(
            "A mine is dug to a plan. Engineers drill the deposit on a grid, build a three-dimensional model of the "
            "grade, block by block, and then decide the order in which to dig it. <bookmark mark='a'/> An open pit "
            "grows in stages called pushbacks: each one widens and deepens the hole. <bookmark mark='b'/> Because money "
            "now is worth more than money later, the plan takes the richest, cheapest rock first. "
            "<bookmark mark='c'/> So in our model mine, output is highest in the first year, "
            f"{out[0]:.0f} thousand tonnes, and falls every year after, to {out[-1]:.0f}. <bookmark mark='d'/> And the "
            f"cost of a pound climbs, from {costs[0]:.2f} dollars to {costs[-1]:.2f}. A mine's best years are its first. "
            "Every mine is a declining asset, and the plan makes it decline on purpose."
        ) as vo:
            self.play(FadeIn(ground), Create(surface), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in reversed(shells)], lag_ratio=0.25), FadeIn(pit_lab),
                      run_time=2.0)
            self.play(FadeIn(stage))
            vo.wait_until("b")
            self.play(FadeIn(pa), FadeIn(ttl1), FadeIn(pb), FadeIn(ttl2))
            vo.wait_until("c")
            for k in range(n):
                self.play(shells[k].animate.set_fill(BACKGROUND, opacity=1), FadeOut(stage[k]),
                          LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[3 * k:3 * k + 3]], lag_ratio=0.3),
                          run_time=1.1)
            vo.wait_until("d")
            self.play(Create(cl), run_time=2.5)
        self.clear_scene()

    def option(self):
        W = R["wait"]
        be, cross = W["breakeven"], W["cross"]
        cur = W["curve"]
        ps = [c["price"] for c in cur]
        pa = viz.plot_axes([ps[0], ps[-1]], [-3200, 5600], x_length=8.2, y_length=5.0,
                           xticks=[2.5, 3.5, 4.5, 5.5, 6.5], yticks=[-2000, 0, 2000, 4000],
                           xfmt=lambda v: f"${v:.2f}", yfmt=lambda v: f"${v / 1000:+.0f}bn" if v else "$0",
                           ylabel="value of the deposit today", size=15).move_to([-1.3, -0.2, 0])
        xl = tx("copper price today, a pound", 15, "#9AA3B2").next_to(pa, DOWN, buff=0.12)
        now_l = VMobject(stroke_color=COPPER, stroke_width=4).set_points_smoothly(
            [pa.ax.c2p(c["price"], max(c["now"], -3200)) for c in cur])
        wait_l = VMobject(stroke_color=WAITC, stroke_width=4).set_points_smoothly(
            [pa.ax.c2p(c["price"], c["wait"]) for c in cur])
        zero = DashedLine(pa.ax.c2p(ps[0], 0), pa.ax.c2p(ps[-1], 0), stroke_color=GREY_B, stroke_width=1.2)
        lab_now = tx("build now", 19, COPPER, bold=True).next_to(pa.ax.c2p(ps[-3], cur[-3]["now"]), UP + LEFT * 0.3,
                                                                  buff=0.1)
        lab_wait = tx("keep the right to build", 19, WAITC, bold=True).next_to(pa.ax.c2p(ps[3], cur[3]["wait"]), UP,
                                                                              buff=0.3)
        be_dot = Dot(pa.ax.c2p(be, 0), color=COPPER, radius=0.08)
        be_lab = VGroup(tx(f"break-even ${be:.2f}", 16, COPPER), tx("building now is worth zero", 14, GREY_A)
                        ).arrange(DOWN, buff=0.03).next_to(be_dot, DR, buff=0.12)
        wait_at_be = float(np.interp(be, ps, [c["wait"] for c in cur]))
        be_up = Arrow(pa.ax.c2p(be, 0), pa.ax.c2p(be, wait_at_be), buff=0.05, stroke_width=3, color=WAITC,
                      tip_length=0.14)

        x_dot = Dot(pa.ax.c2p(cross, float(np.interp(cross, ps, [c["now"] for c in cur]))), color=WHITE, radius=0.09)
        x_lab = VGroup(tx(f"build when copper reaches ${cross:.2f}", 18, WHITE, bold=True),
                       tx(f"{100 * (W['cross_ratio'] - 1):.0f}% above break-even", 15, GREY_A)).arrange(
            DOWN, buff=0.04).next_to(x_dot, DR, buff=0.15)
        region = Polygon(*[pa.ax.c2p(c["price"], c["wait"]) for c in cur if c["price"] <= cross],
                         *[pa.ax.c2p(c["price"], max(c["now"], -3200)) for c in reversed(cur) if c["price"] <= cross],
                         stroke_width=0, fill_color=WAITC, fill_opacity=0.15)
        side = VGroup(tx("Why waiting is worth something", 20, WHITE, bold=True),
                      tx("If the price rises, you build", 16, GREY_A), tx("and keep the upside.", 16, GREY_A),
                      tx("If it falls, you don't,", 16, GREY_A), tx("and lose nothing.", 16, GREY_A),
                      tx("Building kills the choice.", 16, WAITC),
                      tx("At break-even: building now, $0;", 16, WHITE),
                      tx(f"the right to wait, ${wait_at_be:,.0f}m.", 16, WAITC, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to([5.1, 1.4, 0])
        side[-2].shift(DOWN * 0.15)
        side[-1].shift(DOWN * 0.15)
        tag = estimate_tag("the Works (mine.py): price a year on lognormal, 25% volatility; values discounted at 8%",
                           corner=DR, size=13)
        src = source("after Avinash Dixit and Robert Pindyck, Investment under Uncertainty (Princeton, 1994)", size=13)
        with self.voiceover(
            "Now the hardest decision: when to build at all. Take the model deposit again, and ask what it is worth at "
            "different copper prices. <bookmark mark='a'/> The orange line is the value of building it now. It crosses "
            f"zero at the break-even price, {be:.2f} dollars a pound. Above that, building adds value; below it, "
            "building destroys it. <bookmark mark='b'/> The blue line is the value of something else: owning the "
            "deposit and keeping the right to build it next year, once you have seen the price. <bookmark mark='c'/> "
            f"At break-even, building now is worth nothing, but the right to wait is worth about {wait_at_be:,.0f} "
            "million dollars. If the price rises, you build and keep the gain; if it falls, you leave the copper in the "
            "ground and lose nothing. The moment you build, that choice is gone, and so is its value. "
            f"<bookmark mark='d'/> So the rule is not to build at break-even. Build when the price is well above it: "
            f"here, at about {cross:.2f} dollars, {100 * (W['cross_ratio'] - 1):.0f} percent higher, where building now "
            "finally beats waiting. Economists Avinash Dixit and Robert Pindyck made this idea the heart of a famous "
            "book on investment. <bookmark mark='e'/> It explains a pattern you will see again in this film. Miners "
            "approve new mines only in booms, when the price is far above their costs, and the mines arrive years "
            "later, often into a market that has turned."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), Create(zero), FadeIn(tag), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(now_l), FadeIn(lab_now), run_time=2.0)
            self.play(FadeIn(be_dot, scale=2), FadeIn(be_lab))
            vo.wait_until("b")
            self.play(Create(wait_l), FadeIn(lab_wait), run_time=2.0)
            vo.wait_until("c")
            self.play(GrowArrow(be_up))
            self.play(LaggedStart(*[FadeIn(m) for m in side], lag_ratio=0.25), run_time=2.4)
            vo.wait_until("d")
            self.play(FadeIn(region), FadeIn(x_dot, scale=2), FadeIn(x_lab))
            vo.wait_until("e")
            self.play(Indicate(x_lab, color=WHITE, scale_factor=1.05))
        self.clear_scene()
