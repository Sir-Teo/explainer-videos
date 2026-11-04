from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import rates as R
from videos.quant.quant18.common import BAD, GOOD, PART, ZERO, ask, illustration, load

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
            wrapped_label(r"no principal changes hands: only the difference of the two interest payments", 11.0, 21,
                          GREY_A),
            wrapped_label(r"a bank with fixed-rate mortgages pays fixed to turn them floating; a company with a "
                          r"floating loan pays fixed to lock its cost; a fund receives fixed to add duration without "
                          r"buying bonds", 11.0, 21, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.6)
        head = label(r"An interest rate swap", font_size=32).to_edge(UP, buff=0.5)
        with self.voiceover(
            "An interest rate swap is two streams of interest on the same notional amount, in opposite directions. "
            "One side pays a fixed rate agreed today; the other pays the floating overnight rate, SOFR, compounded "
            "over each period. <bookmark mark='a'/> No principal changes hands, only the difference. "
            "<bookmark mark='b'/> A bank holding fixed-rate mortgages pays fixed to make its income float with its "
            "deposits; a company with a floating loan pays fixed to lock its cost; a pension fund receives fixed to "
            "add duration without buying bonds. Interest rate swaps are the largest derivatives market in the world."
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
                cmath(r"V_{\text{receiver}}", r"=", r"(K - K^*)\,A,\qquad \text{DV01} \approx A \times 0.0001",
                      font_size=40, colors={r"V_{\text{receiver}}": GOOD})]
        whys = [why(r"a floating-rate loan resets to the market rate each period, so it is worth par at every reset: "
                    r"the floating payments are worth 1 now minus the principal they omit at $T$"),
                why(r"the fixed payments: a rate times the annuity $A$, the value of 1 a year for the swap's life"),
                why(rf"the par swap rate makes both legs equal. On 31 December 2025, off the Treasury curve: "
                    rf"10 years, {100 * k10:.2f}\%, annuity {A10:.2f}"),
                why(r"after inception the swap's value is the rate's move times the annuity: an annuity's worth of "
                    r"duration, with no bond bought")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-2.0, buff=0.6, edge=6.9)
        with self.voiceover(
            "How is the fixed rate set? A floating-rate loan resets to the market rate every period, so it is always "
            "worth par at a reset. The floating payments are therefore worth one today, minus the principal they leave "
            "out at the end: one minus the discount factor at T. <bookmark mark='a'/> The fixed payments are the rate "
            "times the annuity: the value of one dollar a year for the swap's life. <bookmark mark='b'/> The par swap "
            "rate makes the legs equal. Off the Treasury curve of the last day of 2025, a ten-year swap would fix at "
            f"{100 * k10:.2f} percent. <bookmark mark='c'/> Once the swap exists, its value moves with the swap rate "
            "times the annuity: it carries a bond's duration without anyone buying a bond."
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
        g = axes([2000.5, 2017], [-80, 120], x_length=9.0, y_length=4.6, xlabel=r"year",
                 ylabel=r"swap rate minus Treasury yield, bp", xticks=[2002, 2006, 2010, 2014], yticks=[-80, -40, 0, 40, 80, 120],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        zero = Line(ax.c2p(2000.5, 0), ax.c2p(2017, 0), color=WHITE, stroke_width=1.5)
        lines = VGroup(*[curve(ax, np.asarray(s[m]["t"]), np.clip(np.asarray(s[m]["bp"]), -80, 120), MCOL[m],
                               stroke_width=2.2) for m in ("2", "5", "10", "30")])
        leg = legend([(MCOL[m], rf"{m}-year") for m in ("2", "5", "10", "30")], font_size=18).to_edge(RIGHT,
                                                                                                  buff=0.5).shift(UP * 1.6)

        def ymd(x):
            return f"{x // 10000}-{x // 100 % 100:02d}-{x % 100:02d}"
        f30, f10 = s["30"]["first_negative"], s["10"]["first_negative"]
        side = VGroup(
            wrapped_label(rf"2001--07 average: {s['10']['mean_2001_2007']:.0f} bp at 10 years", 3.6, 18, GREY_A),
            wrapped_label(rf"30-year negative from {ymd(f30)}", 3.6, 18, MCOL["30"]),
            wrapped_label(rf"10-year negative from {ymd(f10)}", 3.6, 18, MCOL["10"]),
            wrapped_label(rf"October 2016, the last day FRED publishes: 30-year {s['30']['last_bp']:.0f} bp", 3.6, 18,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(leg, DOWN, buff=0.4, aligned_edge=LEFT)
        with self.voiceover(
            "Now compare swap rates with Treasury yields of the same maturity. Before 2008 swaps fixed above "
            "Treasuries, by about sixty basis points at ten years. That made sense: the floating side was LIBOR, an "
            "unsecured rate between banks, with bank credit risk in it; Treasuries have none. <bookmark mark='a'/> In "
            "October 2008 the thirty-year spread went negative, and it stayed there. <bookmark mark='b'/> In "
            "September 2015 the ten-year followed. A fixed rate on a contract with a bank, below the rate on the "
            "United States government. <bookmark mark='c'/> By October 2016, when FRED stops publishing these swap "
            f"rates, the thirty-year spread was {s['30']['last_bp']:.0f} basis points."
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
            label(r"the arbitrage on paper:", font_size=24),
            label(r"1.\ buy the 30-year Treasury, financed in repo", font_size=22, color=ZERO),
            label(r"2.\ pay fixed on a 30-year swap", font_size=22, color=FIX),
            label(r"3.\ earn the spread, if repo stays near SOFR, for 30 years", font_size=22, color=GOOD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(UP, buff=0.6).to_edge(LEFT, buff=0.8)
        cost = VGroup(
            label(r"why it stayed open:", font_size=24),
            wrapped_label(r"the bond sits on a dealer's balance sheet for 30 years; the swap barely does. After 2008, "
                          r"leverage ratios charge capital for the whole balance sheet, however safe the asset", 6.0, 20,
                          BAD),
            wrapped_label(r"Jermann (2020): with a cost of holding Treasuries, the no-arbitrage swap spread is negative, "
                          r"and largest at long maturities, as observed", 6.0, 20, GREY_A),
            wrapped_label(r"demand: pension funds and insurers receive fixed at the long end to hedge their "
                          r"liabilities, pushing long swap rates down", 6.0, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.6)
        with self.voiceover(
            "Why does nobody arbitrage it? On paper it is easy: buy the thirty-year bond, finance it in repo, pay fixed "
            "on the swap, and pocket the difference for thirty years. <bookmark mark='a'/> In practice the bond has to "
            "sit on a dealer's balance sheet for thirty years, and after 2008 regulators began charging capital for the "
            "size of the whole balance sheet, however safe the assets in it. The swap uses almost none. Urban Jermann "
            "showed in 2020 that a cost of holding bonds is enough to make the no-arbitrage swap spread negative, and "
            "most negative at the long end, which is what the data show. <bookmark mark='b'/> On the other side, "
            "pension funds and insurers receive fixed at the long end to match their liabilities. The limit to "
            "arbitrage here is not risk; it is balance sheet."
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
        self.wait(0.5)
        self.clear_scene()
