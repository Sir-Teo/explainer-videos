from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant10.common import (DEL, GAIN, IMP, LOSS, OPT, PART, REA, SPOT, load, real_data, ts_date)


class Hook(VoiceoverScene):
    def construct(self):
        b = load("btc")
        self.title_card()
        self.the_month(b)
        self.the_question(b)
        self.objectives()
        self.house()

    # ------------------------------------------------------------------
    def title_card(self):
        card = part_title(PART, r"Manufacturing an option")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            """Part ten. Black, Scholes and Merton. In their continuous, frictionless model, an option can be replicated with stock and cash. We derive that result, examine its failures, and start with a stylized experiment on a real month of Bitcoin prices."""
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    # ------------------------------------------------------------------
    def the_month(self, b):
        S = b["pick_S"]
        H = len(S) - 1
        days = np.arange(H + 1) / 24
        prem = b["pick_premium"]
        value = b["pick_value"]
        book = b["pick_book"]
        naked = prem - value  # the unhedged seller, marked to market every hour
        naked[-1] = prem - max(S[-1] - 100, 0)
        lo, hi = 90, 155
        top = axes([0, 30], [lo, hi], x_length=8.2, y_length=2.7, ylabel=r"Bitcoin, per 100 at the start",
                   xticks=[0, 10, 20, 30], yticks=[100, 125, 150], font_size=18)
        top.to_corner(UL, buff=0.45).shift(DOWN * 0.15)
        ax = top.ax
        strike = DashedLine(ax.c2p(0, 100), ax.c2p(30, 100), color=QC.STRIKE, stroke_width=1.5, dash_length=0.08)
        klab = MathTex(r"K = 100", font_size=22, color=QC.STRIKE).next_to(strike, RIGHT, buff=0.1)
        bot = axes([0, 30], [-42, 6], x_length=8.2, y_length=2.4, xlabel=r"days", ylabel=r"the seller's profit",
                   xticks=[0, 10, 20, 30], yticks=[-40, -20, 0], font_size=18)
        bot.next_to(top, DOWN, buff=0.55).align_to(top, LEFT)
        bx = bot.ax
        zero = DashedLine(bx.c2p(0, 0), bx.c2p(30, 0), color=GREY_D, stroke_width=1.2, dash_length=0.06)
        k = ValueTracker(0.0)
        path = tracing(ax, days, S, k, SPOT, stroke_width=3)
        naked_line = tracing(bx, days, naked, k, LOSS, stroke_width=3)
        book_line = tracing(bx, days, book, k, WHITE, stroke_width=3.5)
        dot = always_redraw(lambda: glow_dot(ax.c2p(at_index(days, k), at_index(S, k)), color=SPOT, radius=0.06))
        # the right column: what the hedger holds, live
        delta_lab = MathTex(r"\Delta", font_size=40, color=DEL)
        delta_num = DecimalNumber(b["pick_delta"][0], num_decimal_places=2, font_size=40, color=DEL)
        delta_unit = label(r"bitcoin held", font_size=24, color=GREY_A)
        col = VGroup(VGroup(delta_lab, MathTex("=", font_size=40), delta_num).arrange(RIGHT, buff=0.15), delta_unit)
        col.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        bar_frame = Rectangle(width=0.5, height=1.8, stroke_color=GREY_C, stroke_width=1.5)
        bar_fill = always_redraw(lambda: Rectangle(width=0.5, height=max(1.8 * at_index(b["pick_delta"], k), 0.01),
                                                   stroke_width=0, fill_color=DEL, fill_opacity=0.85)
                                 .align_to(bar_frame, DOWN).align_to(bar_frame, LEFT))
        one = MathTex(r"1", font_size=22, color=GREY_B).next_to(bar_frame, LEFT, buff=0.1).align_to(bar_frame, UP)
        zer = MathTex(r"0", font_size=22, color=GREY_B).next_to(bar_frame, LEFT, buff=0.1).align_to(bar_frame, DOWN)
        bar = VGroup(bar_frame, bar_fill, one, zer)
        right = VGroup(col, bar).arrange(DOWN, buff=0.25).to_edge(RIGHT, buff=0.7).to_edge(UP, buff=0.65)
        delta_num.add_updater(lambda m: m.set_value(at_index(b["pick_delta"], k)))
        legend_ = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.4, color=LOSS, stroke_width=5), label(r"unhedged", font_size=20, color=LOSS))
            .arrange(RIGHT, buff=0.12),
            VGroup(Line(ORIGIN, RIGHT * 0.4, color=WHITE, stroke_width=5), label(r"hedged every hour", font_size=20))
            .arrange(RIGHT, buff=0.12)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        legend_.to_corner(DR, buff=0.45)
        src = note(rf"BTC/USDT hourly, Binance; implied volatility: Deribit DVOL; from {ts_date(b['pick_start'])}",
                   font_size=17, color=GREY_B).to_corner(UR, buff=0.2)
        call = VGroup(label(r"Model dollar call: 30 days, strike = today's spot", font_size=26),
                      VGroup(label(r"priced at", font_size=24, color=GREY_A),
                             MathTex(rf"\sigma_i = {100 * b['pick_iv']:.0f}\%", font_size=30, color=IMP),
                             label(r"a year:", font_size=24, color=GREY_A),
                             MathTex(rf"{prem:.1f}", font_size=30, color=OPT),
                             label(r"per 100 of bitcoin", font_size=24, color=GREY_A)).arrange(RIGHT, buff=0.15))
        call.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        call_box = SurroundingRectangle(call, buff=0.25, color=OPT, corner_radius=0.1, stroke_width=2)
        call = VGroup(call_box, call).scale(1.25).move_to(UP * 1.6)
        # what the seller owes at expiry: the payoff
        pay = axes([60, 160], [0, 60], x_length=5.6, y_length=2.4, xlabel=r"Bitcoin at expiry, per 100",
                   xticks=[60, 100, 140], yticks=[0, 30, 60], font_size=18).next_to(call, DOWN, buff=0.5)
        pay_line = pay.ax.plot_line_graph([60, 100, 160], [0, 0, 60], line_color=OPT, add_vertex_dots=False,
                                          stroke_width=4)
        pay_lab = MathTex(r"\text{you owe } \max(S_T - K,\, 0)", font_size=30, color=OPT)
        pay_lab.next_to(pay.ax.c2p(62, 47), RIGHT, buff=0.15)  # starts right of the y-axis
        call_slot = call.copy().scale_to_fit_width(4.4).to_edge(RIGHT, buff=0.35).set_y(-1.7)
        with self.voiceover(
            f"""The first of October 2021. Bitcoin is about {b['pick_S0']:,.0f} dollars. Suppose we sell a thirty-day dollar call at today's spot. We use DVOL, {100 * b['pick_iv']:.0f} percent, as a proxy for its volatility: a model premium of {prem:.1f} per hundred of Bitcoin, rather than an observed call execution. <bookmark mark='a'/> Bitcoin rises {S[-1] - 100:.0f} percent. <bookmark mark='b'/> The payoff is {S[-1] - 100:.0f} per hundred; unhedged, the loss is {S[-1] - 100 - prem:.0f}. Pause: how does hourly hedging change it? <bookmark mark='c'/> The seller starts with {b['pick_delta'][0]:.2f} coin units per call, increasing towards one. The white line finishes up {b['pick_pnl']:.2f}, before costs and funding. This window was selected retrospectively for its median profit among {b['n']:,} overlapping windows. It illustrates the mechanism, rather than an executable trading record."""
        ) as vo:
            self.play(FadeIn(call, scale=0.95))
            self.play(FadeIn(pay), Create(pay_line), FadeIn(pay_lab))
            self.wait(max(vo.until("a") - 4.2, 0.5))
            self.play(FadeOut(VGroup(pay, pay_line, pay_lab)), run_time=1)
            self.play(Transform(call, call_slot), FadeIn(top), FadeIn(bot), Create(strike), FadeIn(klab),
                      FadeIn(src), run_time=2)
            self.add(path, dot)
            self.play(k.animate.set_value(H * 0.55), run_time=vo.until("b"), rate_func=linear)
            self.add(naked_line, zero)
            self.play(FadeIn(legend_[0]), k.animate.set_value(H), run_time=2.5, rate_func=linear)
            owe = MathTex(rf"S_T - K = {S[-1] - 100:.0f}", font_size=30, color=OPT).next_to(ax.c2p(30, S[-1]), RIGHT,
                                                                                            buff=0.25)
            self.play(FadeIn(owe))
            vo.wait_until("c")
            k.set_value(0)
            self.add(book_line, right)
            self.play(FadeIn(legend_[1]), FadeIn(right))
            self.play(k.animate.set_value(H), run_time=max(vo.remaining(1.0) - 1.2, 4.0), rate_func=linear)
            end = MathTex(rf"{b['pick_pnl']:+.2f}", font_size=34, color=GAIN).next_to(bx.c2p(26, book[-1]), UP,
                                                                                      buff=0.12)
            self.play(FadeIn(end, scale=1.2))
        self.k, self.month = k, VGroup(top, bot, strike, klab, path, dot, naked_line, book_line, zero, right,
                                       legend_, src, call, owe, end)

    # ------------------------------------------------------------------
    def the_question(self, b):
        iv = MathTex(rf"\sigma_i = {100 * b['pick_iv']:.0f}\%", font_size=54, color=IMP)
        rv = MathTex(rf"\sigma_r = {100 * b['pick_rv']:.0f}\%", font_size=54, color=REA)
        ivl = label(r"the DVOL proxy used in the model", font_size=26, color=IMP)
        rvl = label(r"the volatility Bitcoin delivered", font_size=26, color=REA)
        left = VGroup(iv, ivl).arrange(DOWN, buff=0.2)
        right = VGroup(rv, rvl).arrange(DOWN, buff=0.2)
        pair = VGroup(left, right).arrange(RIGHT, buff=1.4).shift(UP * 0.8)
        q = label(r"How can a bet on a price be built out of the price itself?", font_size=34)
        q.next_to(pair, DOWN, buff=1.0)
        with self.voiceover(
            f"""The shares follow the model delta. Continuous replication cancels first-order stock risk; hourly hedging leaves an error. What pays the seller in this example is the variance gap, weighted by gamma. <bookmark mark='a'/> The DVOL proxy is {100 * b['pick_iv']:.0f} percent against realized volatility of {100 * b['pick_rv']:.0f}. Their difference alone does not determine profit: the path's gamma weights matter. <bookmark mark='b'/> That is the question behind the formula."""
        ) as vo:
            vo.wait_until("a")
            self.play(FadeOut(self.month), run_time=1.0)
            self.play(FadeIn(left, shift=UP * 0.2))
            self.play(FadeIn(right, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Write(q))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def objectives(self):
        card = objectives_card([
            r"Derive the price by replication, solve the PDE as a heat equation, read it as an expectation and a tree",
            r"Read the Greeks as the geometry of one surface, and find the identity that ties gamma to theta",
            r"Derive the short seller's P\&L, $\tfrac12\Gamma S^2(\sigma_i^2 - \sigma_r^2)\,dt$, and test it on paths",
            r"Measure hedging in steps, with jumps, with costs (Leland) and with the wrong volatility",
            r"Invert the formula on 254 real quotes; add the carry; price early exercise",
            r"Test a DVOL-priced BTC model, replay 1987 and 1998, and examine current practice",
        ], title=r"In this part", font_size=29)
        with self.voiceover(
            "The plan. The formula derived and solved three ways. The Greeks as one surface. The hedger's profit "
            "term by term, and how hedging fails: in steps, across jumps, with costs, with the wrong volatility. "
            "The formula inverted on a real market, with dividends and early exercise. And real data: Bitcoin, "
            "1987 replayed, 1998, and how desks and researchers use the formula today."
        ):
            self.play(FadeIn(card.head), FadeIn(card.rows[0], shift=RIGHT * 0.2), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows[1:]],
                                 lag_ratio=0.35), run_time=6)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def house(self):
        before = house_chart(PART - 1)
        after = house_chart(PART, lit=("vol",))
        cap = label(r"The House opens its first trading desk", font_size=28, color=QC.HOUSE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "And the House, the series' own quant firm, opens its first trading desk. So far it has only data and "
            "funding. From this part on it has a volatility desk: a pricer, a hedger and an implied volatility "
            "solver, written and tested in the series' library, and used by every part that comes after. "
            "<bookmark mark='a'/> Its first job is to understand the formula it is about to trade on."
        ) as vo:
            self.play(FadeIn(before))
            vo.wait_until("a")
            self.play(ReplacementTransform(before, after), FadeIn(cap))
        self.wait(0.5)
        self.clear_scene()
