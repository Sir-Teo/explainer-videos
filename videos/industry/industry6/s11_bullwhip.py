from __future__ import annotations

from videos.industry.industry6.common import *  # noqa: F403


class Bullwhip(VoiceoverScene):
    def construct(self):
        card(self, 9, "The bullwhip", "Why do factories feel booms and busts that shoppers never had?",
             "Chapter nine. The bullwhip.", lit=("change", "dollar"))
        self.chain()
        self.real()

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
            "a small flick of the wrist, and a crack at the far end."
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
