from __future__ import annotations

from videos.industry.industry6.common import *  # noqa: F403


def money(v):
    return ("-" if v < 0 else "") + f"${abs(v):.1f}bn"


class Leverage(VoiceoverScene):
    def construct(self):
        card(self, 11, "Leverage", "Why does a small fall in sales become a big fall in profit?",
             "Chapter eleven. Leverage.", lit=("change", "make"))
        self.model()
        self.real()

    def model(self):
        # a business with $100 of sales: variable costs are half of sales, fixed costs $30, profit $20
        rev = ValueTracker(100.0)
        fixed, var_share, debt = 30.0, 0.5, 6.0
        x, base, u = -2.6, -2.9, 0.05

        def stack():
            r_ = rev.get_value()
            parts = [(var_share * r_, "#5B6372", "costs that follow sales"), (fixed, CAP, "fixed costs"),
                     (r_ - var_share * r_ - fixed, BOOM, "operating profit")]
            g = VGroup()
            y = base
            for v, col, _ in parts:
                h = max(v * u, 0.004)
                g.add(Rectangle(width=1.8, height=h, stroke_width=1, stroke_color="#0E1117", fill_color=col,
                                fill_opacity=0.9).move_to([x, y + h / 2, 0]))
                y += h
            return g
        bar = always_redraw(stack)
        labels = VGroup(tx("costs that follow sales", 17, GREY_A), tx("fixed costs: plant, depreciation", 17, CAP),
                        tx("operating profit", 17, BOOM))

        def place(_):
            g = bar
            for k, l_ in enumerate(labels):
                l_.next_to(g[k], RIGHT, buff=0.3)
        labels.add_updater(place)
        rn = draw.number(lambda: rev.get_value(), 0, prefix="sales $", size=28, color=WHITE)
        rn.add_updater(lambda g: g.next_to([x, base + rev.get_value() * u, 0], UP, buff=0.15))
        pn = draw.number(lambda: rev.get_value() * (1 - var_share) - fixed, 0, prefix="profit $", size=28, color=BOOM)
        pn.move_to([4.6, 1.6, 0])
        chg = VGroup(tx("sales -20%", 26, ORDER, bold=True), tx("profit -50%", 30, BUST, bold=True)).arrange(
            DOWN, buff=0.15).move_to([4.6, 0.0, 0])
        debt_b = Rectangle(width=1.8, height=debt * u, stroke_width=1, stroke_color="#0E1117", fill_color=PRICE,
                           fill_opacity=0.95)
        debt_t = tx("interest on the debt", 17, PRICE)
        after = VGroup(tx("profit after interest", 18, GREY_A), tx("$14 → $4: -71%", 26, BUST, bold=True)).arrange(
            DOWN, buff=0.08).move_to([4.6, -1.8, 0])
        tag = estimate_tag("a model business, dollars", corner=DR)
        with self.voiceover(
            "When the cycle turns, sales fall. Why do profits fall so much more? <bookmark mark='a'/> Take a "
            "business with a hundred dollars of sales. Half its costs move with sales: materials, energy, the "
            "people paid by the hour. Thirty dollars are fixed: the plant and its wear, which cost the same however "
            "much it makes. That leaves twenty dollars of profit. <bookmark mark='b'/> Now sales fall by a fifth. "
            "The costs that follow sales fall by a fifth too. The fixed costs do not move. <bookmark mark='c'/> "
            "Profit halves, from twenty to ten. That is operating leverage: the more of a business's costs are "
            "fixed, the harder a fall in sales hits its profit. Ships, chip plants and mines are almost all fixed "
            "cost. <bookmark mark='d'/> And there is a second lever. Suppose the business borrowed to build its "
            "plant, at the top of the cycle, and owes six dollars of interest a year. Interest is fixed too. "
            "<bookmark mark='e'/> Profit after interest falls from fourteen to four: by more than two thirds. The "
            "companies that borrowed most in the boom are the ones that fail in the bust."
        ) as vo:
            self.add(bar, labels, rn)
            self.play(FadeIn(tag), FadeIn(pn))
            vo.wait_until("a")
            self.play(Indicate(labels[1], color=CAP), Indicate(labels[2], color=BOOM))
            vo.wait_until("b")
            self.play(rev.animate.set_value(80.0), run_time=2.4)
            vo.wait_until("c")
            self.play(FadeIn(chg, shift=UP * 0.1))
            vo.wait_until("d")
            bar.clear_updaters()
            debt_b.move_to(bar[2].get_bottom(), aligned_edge=DOWN)
            debt_t.next_to(debt_b, LEFT, buff=0.3)
            self.play(FadeIn(debt_b), FadeIn(debt_t))
            vo.wait_until("e")
            self.play(FadeIn(after, shift=UP * 0.1))
        labels.clear_updaters()
        rn.clear_updaters()
        pn.clear_updaters()
        self.clear_scene()

    def real(self):
        L = R["leverage"]
        mu, mk = L["micron"], L["maersk"]

        def pair(name, glyph, rev, prof, dep, col, x):
            d_rev = rev[1] / rev[0] - 1
            g = VGroup(glyph.scale_to_fit_height(0.8), tx(name, 22, col, bold=True)).arrange(DOWN, buff=0.12)
            rows = VGroup(
                VGroup(tx("sales", 18, GREY_A), tx(f"${rev[0]:.1f}bn → ${rev[1]:.1f}bn", 22, WHITE),
                       tx(f"{100 * d_rev:+.0f}%", 22, ORDER, bold=True)).arrange(RIGHT, buff=0.25),
                VGroup(tx("operating profit", 18, GREY_A), tx(f"${prof[0]:.1f}bn → {money(prof[1])}", 22, WHITE),
                       tx(f"{100 * (prof[1] / prof[0] - 1):+.0f}%", 22, BUST, bold=True)).arrange(RIGHT, buff=0.25),
                VGroup(tx("depreciation", 18, GREY_A), tx(f"${dep[0]:.1f}bn → ${dep[1]:.1f}bn", 22, WHITE),
                       tx("up", 22, CAP, bold=True)).arrange(RIGHT, buff=0.25)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            return VGroup(g, rows.next_to(g, DOWN, buff=0.35)).move_to([x, 0.2, 0])
        a = pair("Micron, fiscal 2022 → 2023", draw.wafer(0.6), mu["rev"], mu["oi"], mu["dep"], "#B58CFF", -3.5)
        b = pair("Maersk, 2022 → 2023", draw.ship(1.6), mk["rev"], mk["ebit"], mk["dep"], CAP, 3.5)
        src = source("Micron Forms 10-K; Maersk annual reports (ESEF)", size=13)
        with self.voiceover(
            "Here is what that looks like in real accounts. <bookmark mark='a'/> In Micron's fiscal 2023, its sales "
            f"fell by about half, from {mu['rev'][0]:.1f} billion dollars to {mu['rev'][1]:.1f} billion. Its "
            f"operating profit of {mu['oi'][0]:.1f} billion became a loss of {-mu['oi'][1]:.1f} billion, while its "
            "depreciation, the cost of the plants it had already built, went up. <bookmark mark='b'/> Maersk, the "
            f"same year: sales down {-100 * (mk['rev'][1] / mk['rev'][0] - 1):.0f} percent, operating profit down "
            f"{-100 * (mk['ebit'][1] / mk['ebit'][0] - 1):.0f} percent, and depreciation up. A business that is "
            "mostly plant cannot shrink its costs as fast as its customers shrink their orders."
        ) as vo:
            self.play(FadeIn(src), FadeIn(a[0]), FadeIn(b[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in a[1]], lag_ratio=0.5), run_time=2.4)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in b[1]], lag_ratio=0.5), run_time=2.4)
        self.clear_scene()
