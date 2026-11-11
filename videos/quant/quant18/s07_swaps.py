from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import rates as R
from videos.quant.quant18.common import BAD, GOOD, PART, ZERO, ask, fit_right, illustration, load

FIX = QC.DELTA
FLT = QC.SPOT
MCOL = {"2": QC.SPOT, "5": QC.GAIN, "10": QC.DELTA, "30": QC.OPTION}


class Swaps(VoiceoverScene):
    def construct(self):
        s = load("swaps")
        cd = load("curve_day")["20251231"]
        self.card()
        self.diagram()
        self.price(cd)
        self.spreads(s)
        self.why_negative(s)

    def card(self):
        c = chapter_card(11, r"Swaps and the negative swap spread", r"Why would anyone swap below the Treasury rate?",
                         lit=(2008,), part=PART)
        with self.voiceover("Chapter eleven. Interest rate swaps, and a spread that turned negative."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def diagram(self):
        a = RoundedRectangle(width=3.2, height=1.4, corner_radius=0.15, color=FIX).shift(LEFT * 4)
        b = RoundedRectangle(width=3.2, height=1.4, corner_radius=0.15, color=FLT).shift(RIGHT * 4)
        ta = label(r"fixed-rate payer", font_size=24, color=FIX).move_to(a)
        tb = label(r"fixed-rate receiver", font_size=24, color=FLT).move_to(b)
        top = Arrow(a.get_right() + UP * 0.35, b.get_left() + UP * 0.35, buff=0.1, color=FIX, stroke_width=4)
        bot = Arrow(b.get_left() + DOWN * 0.35, a.get_right() + DOWN * 0.35, buff=0.1, color=FLT, stroke_width=4)
        lt = label(r"fixed rate $K$ on the notional, every year", font_size=21, color=FIX).next_to(top, UP, buff=0.1)
        lb = label(r"SOFR compounded in arrears, every year", font_size=21, color=FLT).next_to(bot, DOWN, buff=0.1)
        notes = VGroup(
            wrapped_label(r"plain-vanilla single-currency example: no principal exchange; interest nets when dates match; margin may still be required", 11.0, 21,
                          GREY_A),
            wrapped_label(r"a bank with fixed-rate mortgages pays fixed to turn them floating; a company with a "
                          r"floating loan pays fixed to lock its cost; a fund receives fixed to add duration without "
                          r"buying bonds", 11.0, 21, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.6)
        head = label(r"An interest rate swap", font_size=32).to_edge(UP, buff=0.5)
        with self.voiceover(
            "A plain-vanilla single-currency interest rate swap exchanges fixed interest against a floating reference rate on a common notional. This modern example uses SOFR compounded in arrears and simplified annual payments. <bookmark mark='a'/> Principal is not exchanged, and matched-date interest payments can net. Collateral and variation margin can still create large liquidity needs. <bookmark mark='b'/> A fixed-rate asset holder can pay fixed to reduce duration, while a floating-rate borrower can pay fixed to reduce rate uncertainty. Receiving fixed can add duration for a liability hedge. Mortgages retain prepayment and basis risk, and loan or deposit rates need not match SOFR."
        ) as vo:
            self.play(FadeIn(head), Create(a), Create(b), FadeIn(ta), FadeIn(tb))
            self.play(GrowArrow(top), FadeIn(lt), GrowArrow(bot), FadeIn(lb))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def price(self, cd):
        cv = R.Curve(cd["nodes_t"], cd["nodes_z"])
        k10 = R.par_swap_rate(cv, 10, freq=1)
        A10 = float(cv.df(np.arange(1, 11)).sum())
        rows = [cmath(r"\text{floating leg}", r"=", r"1 - Z(T)", font_size=42, colors={r"\text{floating leg}": FLT}),
                cmath(r"\text{fixed leg}", r"=", r"K\sum_{i=1}^{n} \tau_i\,Z(t_i) = K\,A", font_size=42,
                      colors={r"\text{fixed leg}": FIX}),
                cmath(r"K^*", r"=", r"\frac{1 - Z(T)}{A}", font_size=46, colors={r"K^*": ZERO}),
                cmath(r"V_{\text{receiver}}", r"=", r"(K-K^*)A,\quad \Delta V\approx -A\,\Delta K^*\ \text{at par}",
                      font_size=40, colors={r"V_{\text{receiver}}": GOOD})]
        whys = [why(r"ideal reset-date, unit-notional, single-curve model with matched projection and discounting; no spreads or payment lags"),
                why(r"the fixed payments: a rate times the annuity $A$, the value of 1 a year for the swap's life"),
                why(rf"the par swap rate makes both legs equal. On 31 December 2025, off the Treasury curve: "
                    rf"10 years, {100 * k10:.2f}\%, annuity {A10:.2f}"),
                why(r"receiver value per unit notional; near par its first-order gain for a 1 bp fall is approximately $A\times10^{-4}$")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-2.0, buff=0.6, edge=6.9)
        with self.voiceover(
            f"In the ideal single-curve model at a reset date, matched floating-rate projection and discounting make the unit-notional floating coupon leg worth one minus the terminal discount factor. Payment lags, spreads and partly fixed periods require adjustments. <bookmark mark='a'/> The fixed leg is K times its discounted accrual annuity. <bookmark mark='b'/> Equating legs gives the par rate. Using our Treasury-derived zero curve and annual unit accruals gives {100 * k10:.2f} percent for ten years. This is synthetic textbook arithmetic, not an observed SOFR swap quote. <bookmark mark='c'/> Receiver value is K minus the current par rate, times the current annuity, per unit notional. Near par, a one-basis-point fall gives approximately A times ten to the minus four. Away from par, changes in the annuity also enter; real valuation needs the appropriate discount and projection conventions."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.add(illustration(r"one curve for both discounting and the floating rate: the textbook simplification "
                              r"(Part 19 separates them)"))
        self.wait(0.4)
        self.clear_scene()

    def spreads(self, s):
        g = axes([2000.5, 2017], [-80, 160], x_length=8.0, y_length=4.6, xlabel=r"year",
                 ylabel=r"swap rate minus Treasury yield, bp", xticks=[2002, 2006, 2010, 2014], yticks=[-80, -40, 0, 40, 80, 120, 160],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        zero = Line(ax.c2p(2000.5, 0), ax.c2p(2017, 0), color=WHITE, stroke_width=1.5)
        lines = VGroup(*[curve(ax, np.asarray(s[m]["t"]), np.asarray(s[m]["bp"]), MCOL[m],
                               stroke_width=2.2) for m in ("2", "5", "10", "30")])
        leg = legend([(MCOL[m], rf"{m}-year") for m in ("2", "5", "10", "30")], font_size=18).to_edge(RIGHT,
                                                                                                  buff=0.5).shift(UP * 1.6)

        def ymd(x):
            return f"{x // 10000}-{x // 100 % 100:02d}-{x % 100:02d}"
        f30, f10 = s["30"]["first_negative"], s["10"]["first_negative"]
        side = VGroup(
            wrapped_label(rf"available pre-2008 average: {s['10']['mean_2001_2007']:.0f} bp at 10 years", 3.2, 18, GREY_A),
            wrapped_label(rf"30-year persistence-rule date: {ymd(f30)}", 3.2, 18, MCOL["30"]),
            wrapped_label(rf"10-year persistence-rule date: {ymd(f10)}", 3.2, 18, MCOL["10"]),
            wrapped_label(rf"last saved daily reading, October 2016: 30-year {s['30']['last_bp']:.0f} bp", 3.2, 18,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(leg, DOWN, buff=0.4, aligned_edge=LEFT)
        fit_right(side)
        fit_right(leg)
        with self.voiceover(
            f"This historical panel uses LIBOR-referencing ICE swap rates, not today's SOFR swaps. The plotted data are weekly observations of swap yields minus same-maturity Treasury yields, with the full range retained. The available pre-2008 ten-year mean is {s['10']['mean_2001_2007']:.0f} basis points; its window begins in July 2000. Bank funding, Treasury liquidity, collateral and supply-demand effects all matter. <bookmark mark='a'/> The saved thirty-year persistence-rule date is {ymd(f30)}. <bookmark mark='b'/> The ten-year date is {ymd(f10)}. These are not the first isolated negative observations: the code looks forward over up to two hundred fifty observations and requires more than eighty percent negative readings. It is a retrospective description, not a real-time signal. <bookmark mark='c'/> The last saved daily thirty-year spread is {s['30']['last_bp']:.0f} basis points in October 2016. Negative spreads do not compare identical funding and cash-flow risks."
        ) as vo:
            self.play(FadeIn(g), Create(zero), Create(lines), FadeIn(leg), FadeIn(side[0]), run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(side[1]), Indicate(leg[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), Indicate(leg[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.add(illustration(r"FRED: DSWP2--30 (ICE swap rates, to Oct 2016) minus DGS2--30; weekly"))
        self.wait(0.4)
        self.clear_scene()

    def why_negative(self, s):
        steps_ = VGroup(
            label(r"a proposed cash-and-swap position:", font_size=24),
            label(r"1.\ buy the 30-year Treasury, financed in repo", font_size=22, color=ZERO),
            label(r"2.\ pay fixed on a 30-year swap", font_size=22, color=FIX),
            label(r"3.\ floating receipts must cover uncertain repo and other costs", font_size=22, color=GOOD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(UP, buff=0.6).to_edge(LEFT, buff=0.8)
        cost = VGroup(
            label(r"frictions and remaining risks:", font_size=24),
            wrapped_label(r"Treasury inventory and repo consume balance-sheet capacity; swaps also create exposure, collateral and capital requirements. Regulations and netting affect the comparison", 6.0, 20,
                          BAD),
            wrapped_label(r"Jermann (2020): bond-holding frictions can support negative equilibrium swap spreads; this is a model mechanism, not unique causal identification", 6.0, 20, GREY_A),
            wrapped_label(r"demand: pension funds and insurers receive fixed at the long end to hedge their "
                          r"liabilities, pushing long swap rates down", 6.0, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.6)
        with self.voiceover(
            "Buying the Treasury in repo and paying fixed on a swap is a position with risks, rather than a locked thirty-year arbitrage. The coupon stream, swap schedule and floating index differ, and repo funding must be rolled. <bookmark mark='a'/> Balance-sheet capacity, haircuts, margin and capital have costs. Swaps also use collateral and regulatory exposure; their cost is not zero. Jermann's 2020 model shows how frictions in holding bonds can support negative swap spreads in equilibrium. It does not establish that regulation alone caused every observed spread. <bookmark mark='b'/> Liability hedgers' demand to receive fixed can also lower long swap rates. Their choice trades duration exposure against financing, liquidity, collateral and basis risks."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r_) for r_ in steps_], lag_ratio=0.4, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(cost[0]), FadeIn(cost[1]), FadeIn(cost[2]))
            vo.wait_until("b")
            self.play(FadeIn(cost[3]))
        q = ask(r"a 10-year swap pays fixed 3.6\%; the 10-year Treasury yields 3.75\%. Who is happy to receive the "
                r"lower rate, and why?")
        with self.voiceover("One to try. Who is happy to receive fixed on a swap below the Treasury yield, and why?"):
            self.play(FadeIn(q))
        self.wait(2.5)
        self.clear_scene()
        q.to_edge(UP, buff=0.6)
        answer = wrapped_label(r"A liability hedger may prefer receiving fixed without financing a Treasury position. The lower quoted rate comes with different funding, collateral, liquidity and basis exposures.", 11.8, 26, GOOD).move_to(ORIGIN)
        with self.voiceover("A liability hedger may prefer receiving fixed without financing a Treasury position. The lower quoted rate comes with different funding, collateral, liquidity and basis exposures."):
            self.play(FadeIn(q), FadeIn(answer))
        self.clear_scene()
