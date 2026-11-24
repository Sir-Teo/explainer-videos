from __future__ import annotations

from videos.industry.industry8.common import *  # noqa: F403


class Swing(VoiceoverScene):
    def construct(self):
        card(self, 9, "Why the price swings so hard", "Why can a small shortage double the price?",
             "Chapter nine. Why the price swings so hard.", lit=("change",))
        self.curves()
        self.year()

    def curves(self):
        pa = viz.plot_axes([80, 120], [0, 200], x_length=6.4, y_length=4.4, xticks=[90, 100, 110],
                           yticks=[50, 100, 150, 200], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}",
                           xlabel="million barrels a day", size=14)
        pa.move_to([-2.6, -0.4, 0])
        eps = ValueTracker(0.05)
        shift = ValueTracker(0.0)  # share of supply lost
        q0, p0 = 100.0, 70.0

        def demand():
            e = eps.get_value()
            ps = np.linspace(20, 200, 80)
            return VMobject(stroke_color=BRENT, stroke_width=4).set_points_smoothly(
                [pa.ax.c2p(q0 * (p / p0) ** (-e), p) for p in ps])

        def supply():
            e = eps.get_value()
            ps = np.linspace(20, 200, 80)
            return VMobject(stroke_color=CRUDE, stroke_width=4).set_points_smoothly(
                [pa.ax.c2p(q0 * (1 - shift.get_value()) * (p / p0) ** e, p) for p in ps])
        d, s_ = always_redraw(demand), always_redraw(supply)

        def price():
            e = eps.get_value()
            return p0 * (1 - shift.get_value()) ** (1 / (-e - e))
        dot = always_redraw(lambda: glow_dot(pa.ax.c2p(q0 * (price() / p0) ** (-eps.get_value()), min(price(), 199)),
                                             color=PRICE, radius=0.1))
        pn = draw.number(price, 0, prefix="$", size=34, color=PRICE)
        pn.add_updater(lambda m: m.move_to([3.6, 2.1, 0]))
        el = draw.memo_redraw(lambda: round(eps.get_value(), 2),
                              lambda v: tx(f"buyers and sellers each respond {v:.2f}% to a 1% price change", 16, GREY_A),
                              lambda m: m.move_to([3.6, 1.4, 0]))
        lost = draw.number(lambda: 100 * shift.get_value(), 0, prefix="supply lost: ", suffix="%", size=24, color=STATE)
        lost.add_updater(lambda m: m.move_to([3.6, 0.6, 0]))
        rows = VGroup(*[tx(f"lose {100 * r['loss']:.0f}%, response {r['eps']:.2f}: price x{r['mult']:.2f}", 16, WHITE)
                        for r in R["inelastic"]["rows"] if r["eps"] in (0.05, 0.1)]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        rows.move_to([3.6, -1.6, 0])
        labs = VGroup(tx("demand", 16, BRENT).move_to(pa.ax.c2p(86, 185)), tx("supply", 16, CRUDE).move_to(pa.ax.c2p(110, 185)))
        tag = estimate_tag("the Works' model: constant elasticities, the same for buyers and sellers", corner=DR, size=14)
        with self.voiceover(
            "In the short run, almost nobody can change how much oil they use, or how much they produce. "
            "<bookmark mark='a'/> Drivers still drive to work, and planes still fly. That is a steep demand curve. "
            "<bookmark mark='b'/> And wells already pump flat out, while new ones take months or years. That is a "
            "steep supply curve. <bookmark mark='c'/> Now take away five percent of the supply. With both sides this "
            "unresponsive, the price has to rise by two-thirds before enough buyers give up enough oil. "
            "<bookmark mark='d'/> Make both sides twice as responsive, and the same shortage raises the price by less "
            "than a third. <bookmark mark='e'/> Small shortages, huge price moves: that is the arithmetic of a market "
            "where neither side can move quickly, and it is why oil's price swings more than almost anything else "
            "people buy every day."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(tag))
            vo.wait_until("a")
            self.add(d)
            self.play(FadeIn(labs[0]))
            vo.wait_until("b")
            self.add(s_, dot)
            self.play(FadeIn(labs[1]), FadeIn(pn), FadeIn(el))
            vo.wait_until("c")
            self.add(lost)
            self.play(shift.animate.set_value(0.05), run_time=2.5)
            vo.wait_until("d")
            self.play(eps.animate.set_value(0.10), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(rows))
        for m in (d, s_, dot, pn, el, lost):
            m.clear_updaters()
        self.clear_scene()

    def year(self):
        S = R["shock"]
        dq = S["supply_2026"] / S["supply_2025"] - 1
        dc = S["demand"] / S["consumption_2025"]
        dp = S["brent_2026"] / S["brent_2025"] - 1
        implied = dc / dp
        items = [(f"oil shut in, at the peak (May)", S["shutin_peak"], "m b/d", STATE),
                 ("world production, 2026 against 2025", S["supply_2026"] - S["supply_2025"], "m b/d", CRUDE),
                 ("world consumption, 2026 against 2025", S["demand"], "m b/d", BRENT)]
        bars = VGroup()
        for k, (lab, v, unit, col) in enumerate(items):
            b = Rectangle(width=abs(v) * 0.45, height=0.5, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(
                [-1.5, 1.6 - 0.95 * k, 0], aligned_edge=LEFT)
            t = tx(lab, 17, WHITE).next_to(b, LEFT, buff=0.2).align_to([-1.7, 0, 0], RIGHT)
            n = tx(f"{v:+.1f}{unit[0:0]} million b/d" if k else f"{v:.1f} million b/d", 17, col, bold=True).next_to(
                b, RIGHT, buff=0.15)
            bars.add(VGroup(t, b, n))
        pr = VGroup(tx(f"Brent: ${S['brent_2025']:.0f} in 2025, ${S['brent_2026']:.0f} in 2026 (+{100 * dp:.0f}%)", 20,
                       PRICE, bold=True)).move_to([0, -1.3, 0])
        eq = MathTex(rf"\frac{{{100 * dc:.1f}\%\ \text{{less oil used}}}}{{+{100 * dp:.0f}\%\ \text{{price}}}} \approx {implied:.2f}",
                     font_size=36).move_to([0, -2.4, 0])
        cush = VGroup(tx("what cushioned it:", 16, GREY_B), tx("stocks drawn down; Saudi Arabia's pipeline to the Red Sea;", 16, GREY_A),
                      tx("ships transferring oil at sea off Oman; less flying and less use in China", 16, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.04).to_corner(UR, buff=0.4).shift(DOWN * 0.1)
        src = source("EIA, Short-Term Energy Outlook, 10 November 2026 (2026 partly estimated); this film's division",
                     size=13)
        with self.voiceover(
            "2026 put the arithmetic to the test. <bookmark mark='a'/> At the worst, in May, almost eleven million "
            "barrels a day of Middle Eastern production was shut in, a tenth of the world's supply. The model says "
            "that should have nearly tripled the price. <bookmark mark='b'/> It did not, because the world found "
            "cushions: stocks were drawn down, Saudi Arabia pumped oil across the desert to the Red Sea, ships "
            "passed cargoes from one to another off Oman, and over the year production fell by less than five "
            "percent. <bookmark mark='c'/> Consumption fell by about two million barrels a day, mostly in China and "
            "the Middle East. <bookmark mark='d'/> Set the fall in use against the rise in price, and you get about "
            f"{abs(implied):.2f}: for every one percent rise in price, about {abs(implied) * 100:.0f} hundredths of a "
            "percent less oil used. It is a rough calculation, since other things changed too, but it is close to "
            "the steep demand curve we just drew."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(bars[0][0]), GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]))
            vo.wait_until("b")
            self.play(FadeIn(cush, shift=LEFT * 0.2))
            self.play(FadeIn(bars[1][0]), GrowFromEdge(bars[1][1], LEFT), FadeIn(bars[1][2]))
            vo.wait_until("c")
            self.play(FadeIn(bars[2][0]), GrowFromEdge(bars[2][1], LEFT), FadeIn(bars[2][2]))
            vo.wait_until("d")
            self.play(FadeIn(pr))
            self.play(Write(eq))
        self.clear_scene()
