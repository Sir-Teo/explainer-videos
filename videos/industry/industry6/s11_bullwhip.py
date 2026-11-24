from __future__ import annotations

from videos.industry.industry6.common import *  # noqa: F403


class Bullwhip(VoiceoverScene):
    def construct(self):
        card(self, 9, "The bullwhip", "Why do factories feel booms and busts that shoppers never had?",
             "Chapter nine. The bullwhip.", lit=("change", "dollar"))
        self.chain()
        self.real()
        self.cars()

    def cars(self):
        C = R["cars2021"]
        S = C["series"]

        def xm(m):
            return int(m[:4]) + (int(m[5:7]) - 0.5) / 12
        pa = viz.plot_axes([2019, 2024], [0, 120], x_length=5.6, y_length=2.6, xticks=[2019, 2020, 2021, 2022, 2023],
                           yticks=[50, 100], xfmt=lambda v: f"{int(v)}", size=14)
        pb = viz.plot_axes([2019, 2024], [120, 230], x_length=5.6, y_length=2.6, xticks=[2019, 2020, 2021, 2022, 2023],
                           yticks=[150, 200], xfmt=lambda v: f"{int(v)}", size=14)
        pa.move_to([-3.4, -0.9, 0])
        pb.move_to([3.6, -0.9, 0])
        la = VMobject(stroke_color=CAP, stroke_width=3).set_points_as_corners(
            [pa.ax.c2p(xm(m), v) for m, v in zip(S["IPG3361T3S"]["months"], S["IPG3361T3S"]["values"])])
        lb = VMobject(stroke_color=PRICE, stroke_width=3).set_points_as_corners(
            [pb.ax.c2p(xm(m), v) for m, v in zip(S["CUSR0000SETA02"]["months"], S["CUSR0000SETA02"]["values"])])
        ta = tx("American output of cars and parts (index)", 16, CAP).next_to(pa, UP, buff=0.1).align_to(pa, LEFT)
        tb = tx("price of used cars and trucks (index)", 16, PRICE).next_to(pb, UP, buff=0.1).align_to(pb, LEFT)
        car = VGroup(RoundedRectangle(corner_radius=0.12, width=1.6, height=0.45, stroke_width=0, fill_color="#7EC8F5",
                                      fill_opacity=0.95),
                     RoundedRectangle(corner_radius=0.1, width=0.9, height=0.35, stroke_width=0, fill_color="#5DA9E9",
                                      fill_opacity=0.95).shift(UP * 0.32 + LEFT * 0.1),
                     *[Circle(radius=0.16, stroke_width=0, fill_color="#20242C", fill_opacity=1).shift(
                         DOWN * 0.24 + RIGHT * x) for x in (-0.5, 0.5)]).move_to([-4.6, 2.4, 0])
        inv = VGroup(draw.chip(0.55), VGroup(tx(f"{C['inv19']:.0f} days", 22, BOOM, bold=True), tx("of chips in stock, 2019", 15,
                                                                                               GREY_B)).arrange(DOWN, buff=0.04),
                     Text("→", font_size=32, color=GREY_A),
                     VGroup(tx(f"under {C['inv21']:.0f}", 22, BUST, bold=True), tx("in 2021", 15, GREY_B)).arrange(
                         DOWN, buff=0.04)).arrange(RIGHT, buff=0.3).move_to([2.2, 2.4, 0])
        drop = glow_dot(pa.ax.c2p(xm("2020-04"), C["apr20"]), color=BUST, radius=0.08)
        dip = glow_dot(pa.ax.c2p(xm("2021-09"), C["sep21"]), color=BUST, radius=0.08)
        top = glow_dot(pb.ax.c2p(xm("2022-01"), C["used_jan22"]), color=PRICE, radius=0.08)
        rise = C["used_jan22"] / C["used_feb20"] - 1
        src = source("Federal Reserve industrial production and BLS consumer prices via FRED; US Department of Commerce, "
                     "25 January 2022", size=13)
        with self.voiceover(
            "The whip cracked across the car industry in 2021. <bookmark mark='a'/> When the pandemic began, "
            f"American car plants shut: in April 2020 output was about a fifth of February's. <bookmark mark='b'/> "
            "Buyers came back, and by early 2021 output had recovered. Then it fell "
            "again, through the autumn, by about a sixth. Not for lack of buyers, but for lack of chips. "
            "<bookmark mark='c'/> Companies that buy chips told the Commerce Department that their median stock had "
            f"fallen from {C['inv19']:.0f} days' worth in 2019 to less than {C['inv21']:.0f} in 2021. "
            "<bookmark mark='d'/> With few new cars to be had, the price of used cars rose by "
            f"{100 * rise:.0f} percent between February 2020 and January 2022. A brief fall in demand at one end of "
            "a long chain had become a long shortage at the other."
        ) as vo:
            self.play(FadeIn(src), FadeIn(car, shift=RIGHT * 0.3), FadeIn(pa), FadeIn(ta))
            vo.wait_until("a")
            self.play(Create(la), run_time=2.0, rate_func=linear)
            self.play(FadeIn(drop, scale=2))
            vo.wait_until("b")
            self.play(FadeIn(dip, scale=2))
            self.play(car.animate.shift(RIGHT * 0.6), rate_func=there_and_back, run_time=1.2)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(i_, shift=UP * 0.1) for i_ in inv], lag_ratio=0.3), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(pb), FadeIn(tb), Create(lb), run_time=2.0)
            self.play(FadeIn(top, scale=2))
        self.clear_scene()

    def chain(self):
        B = R["bullwhip"]
        rows = B["chain"]
        n = len(rows[0])
        names = ["the shop's sales", "the shop's orders to the wholesaler", "the wholesaler's orders to the factory",
                 "the factory's orders for parts"]
        cols = [BOOM, ORDER, PRICE, BUST]
        glyphs = [draw.shop(0.9, color=BOOM), draw.truck(1.1, color=ORDER), draw.factory(1.1, color="#8C929B"),
                  draw.chip(0.6)]
        t = ValueTracker(1)
        panels = VGroup()
        lines = []
        for k in range(4):
            pa = viz.plot_axes([0, n - 1], [0, 310], x_length=7.4, y_length=1.15, size=12, grid=False)
            y = 2.35 - 1.6 * k
            pa.move_to([1.6, y, 0])
            mid = DashedLine(pa.ax.c2p(0, 100), pa.ax.c2p(n - 1, 100), stroke_color=GREY_C, stroke_width=1)
            g = glyphs[k].scale_to_fit_height(0.75).move_to([-5.3, y, 0])
            lab = tx(names[k], 15, cols[k]).next_to(pa, UP, buff=0.02).align_to(pa, LEFT)

            def mk(k=k, pa=pa):
                m = max(2, int(t.get_value()))
                return VMobject(stroke_color=cols[k], stroke_width=3).set_points_as_corners(
                    [pa.ax.c2p(i, rows[k][i]) for i in range(min(m, n))])
            ln = always_redraw(mk)
            lines.append(ln)
            panels.add(VGroup(pa, mid, g, lab))
        arrows = VGroup(*[Arrow(panels[k][2].get_bottom(), panels[k + 1][2].get_top(), buff=0.08, color=GREY_B,
                                stroke_width=3, max_tip_length_to_length_ratio=0.25) for k in range(3)])
        sds = VGroup(*[tx(f"swings ±{B['chain_sd'][k]:.0f}", 16, cols[k], bold=True).next_to(panels[k][0], RIGHT,
                                                                                             buff=0.2)
                       for k in range(4)])
        tag = estimate_tag("the Works' chain: each step orders to restore two weeks of stock, forecasting from "
                           "a moving average", corner=DR, size=12)
        with self.voiceover(
            "Cycles do not need a long wait to start. They can be manufactured out of almost nothing, inside a "
            "supply chain. <bookmark mark='a'/> Here is a shop. Its sales wobble a little from week to week, "
            "around a hundred. <bookmark mark='b'/> The shop orders from a wholesaler. It wants to keep two weeks of "
            "stock, and it guesses next week's sales from the last few weeks. When sales tick up, it orders the "
            "extra sales, plus extra to top up its stock for the higher sales it now expects. Its orders swing more "
            "than its sales. <bookmark mark='c'/> The wholesaler sees only those orders, and does the same thing to "
            "the factory. <bookmark mark='d'/> And the factory does it to its own suppliers. At every step up the "
            "chain the swings grow, until the company at the top is lurching between rush orders and none at all, "
            "while the shoppers at the bottom were buying about the same as always. <bookmark mark='e'/> In 1997 "
            "three researchers, Hau Lee, V. Padmanabhan and Seungjin Whang, named it the bullwhip effect: "
            "a small flick of the wrist, and a crack at the far end. <bookmark mark='f'/> They also described the "
            "cures, and the best-run supply chains use them. Share the shop's actual sales with every step up the "
            "chain, so each one sees real demand, not just the orders in front of it. Order smaller amounts, more "
            "often. And stop the price promotions that make shops buy in lumps."
        ) as vo:
            ghosts = VGroup(*[pn[2].copy().set_opacity(0.3) for pn in panels], arrows.copy().set_opacity(0.3))
            self.play(FadeIn(tag), LaggedStart(*[FadeIn(g_, shift=DOWN * 0.15) for g_ in ghosts], lag_ratio=0.2),
                      run_time=1.6)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(panels[k]), *([GrowArrow(arrows[k - 1])] if k else []), run_time=0.8)
                self.add(lines[k])
                if k == 0:
                    self.play(t.animate.set_value(n), run_time=2.4, rate_func=linear)
                else:
                    self.play(Indicate(lines[k], color=WHITE), run_time=0.8)
                self.play(FadeIn(sds[k], shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("e")
            self.remove(ghosts)
            self.play(Indicate(sds[3], color=BUST, scale_factor=1.3))
            vo.wait_until("f")
            share = VGroup(*[CurvedArrow(panels[0][2].get_left() + LEFT * 0.05, panels[k][2].get_left() + LEFT * 0.05,
                                         angle=1.2, color=BOOM, stroke_width=2.5) for k in (1, 2, 3)])
            self.play(LaggedStart(*[Create(a_) for a_ in share], lag_ratio=0.3), run_time=1.8)
        for ln in lines:
            ln.clear_updaters()
        self.clear_scene()

    def real(self):
        B = R["bullwhip"]
        base = -2.0
        u = 1.2
        bars = VGroup()
        for k, (v, name, col, g) in enumerate(((B["sd_retail"], "retail sales", BOOM, draw.shop(0.9, color=BOOM)),
                                               (B["sd_orders"], "factories' new orders", BUST,
                                                draw.factory(1.1, color="#8C929B")))):
            x = -2.0 + 4.0 * k
            r_ = Rectangle(width=1.4, height=100 * v * u, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(
                [x, base, 0], aligned_edge=DOWN)
            bars.add(VGroup(r_, tx(f"{100 * v:.1f}%", 26, col, bold=True).next_to(r_, UP, buff=0.08),
                            tx(name, 18, GREY_A).next_to(r_, DOWN, buff=0.12),
                            g.scale_to_fit_height(0.7).next_to(r_, UP, buff=0.7)))
        head = tx("How much each moves in a typical month, America, 1993-2026", 20, GREY_A).to_edge(UP, buff=0.6)
        times = tx(f"{B['ratio']:.1f}×", 44, GOLD, bold=True).move_to([4.6, 0.3, 0])
        src = source("Census Bureau via FRED: retail sales excluding food services, manufacturers' new orders "
                     "(seasonally adjusted); this film's standard deviations of monthly changes", size=13)
        with self.voiceover(
            "You can see the whip in the national statistics. <bookmark mark='a'/> Take America's retail sales, "
            "month by month, and measure how much they typically change from one month to the next: about "
            f"{100 * B['sd_retail']:.1f} percent. <bookmark mark='b'/> Now do the same for the new orders that "
            f"American factories receive. They move by {100 * B['sd_orders']:.1f} percent. <bookmark mark='c'/> "
            f"The factories feel swings {B['ratio']:.1f} times as large as the shops, though in the end every "
            "order is for something a customer will buy."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(bars[0][3]), GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:3]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1][3]), GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1:3]))
            vo.wait_until("c")
            self.play(FadeIn(times, scale=1.3))
        self.clear_scene()
