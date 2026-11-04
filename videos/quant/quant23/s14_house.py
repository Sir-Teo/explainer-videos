from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import premia as P
from videos.quant.quant23.common import BAD, CONS, GOOD, MKT, PART, SDF, TAN, house_lab, load


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet(load("frontier"), load("capm"), load("hj"), load("puzzle"), load("shiller"), load("bubbles"))
        self.lab()
        self.three_reasons()
        self.pipeline()
        self.module()
        self.test()

    def card(self):
        c = chapter_card(13, r"Rule 23: the research desk", r"What must every expected return come with?", part=PART)
        with self.voiceover("Chapter thirteen. The House's twenty-third rule, for the desk it opens in this part: "
                            "research."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, f, c, h, p, s, b):
        o = f["oos"]
        rows = [(r"tangency Sharpe: in sample, then out of sample", rf"{o['in_sharpe']:.2f}\ \to\ {o['oos_sharpe']:.2f}",
                 TAN),
                (r"equal weights, out of sample", rf"{o['eq_sharpe']:.2f}", GOOD),
                (r"SML slope against the market premium", rf"{100 * c['sml']['slope']:.1f}\%\ \text{{vs}}\ "
                                                          rf"{100 * c['mkt_prem']:.1f}\%", MKT),
                (r"Hansen--Jagannathan: 25 portfolios, in and out", rf"{h['sr_ff25']:.2f},\ {h['sr_ff25_oos']:.2f}", SDF),
                (r"risk aversion the equity premium implies", rf"\gamma \approx {p['gamma_implied']:.0f}", BAD),
                (r"price swings against dividend news", rf"\sigma(p) = {s['sd_p']:.2f}\ \text{{vs}}\ "
                                                         rf"\sigma(p^*) = {s['sd_pstar']:.2f}", CONS),
                (r"industry run-ups that crashed", rf"{100 * b['p_crash']:.0f}\%\ \text{{of}}\ {b['n']}", BAD)]
        hx = [-2.3, 3.7]
        tab = VGroup()
        for j, (a, v, c_) in enumerate(rows):
            y = 2.2 - 0.58 * j
            tab.add(VGroup(label(a, font_size=20, color=c_).move_to([hx[0], y, 0]), MathTex(v, font_size=28).move_to(
                [hx[1], y, 0])))
        title = label(r"The research desk's first sheet", font_size=28).to_edge(UP, buff=0.4)
        foot = wrapped_label(r"every number computed in this part from public data (Kenneth French's library, Robert "
                             r"Shiller's data, FRED and the authors' published factors); none is a forecast, and none is "
                             r"advice", 12.0, 18, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The research desk's first sheet, every number from this part. <bookmark mark='a'/> A tangency portfolio "
            "whose Sharpe ratio falls by more than half out of sample, beaten by equal weights. A security market line about a third as steep as "
            "the CAPM says. Twenty-five portfolios that, in sample, demand a discount factor more volatile than any "
            "consumption model gives. A risk aversion of nearly seventy to explain the premium. Prices that swing more "
            "than their dividends justify. And industry run-ups that crash about half the time. Each is a measurement "
            "and a warning: the expected return of anything is the hardest number in finance to know."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.35), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"Expected returns, in the House", P.tangency, "ex = np.asarray(mu", 3,
                         extra=((P.hj_excess, "mu = np.asarray(mu_ex", 2), (P.shleifer_vishny, "p1 = V - S1", 2)),
                         width=9.0)
        card.to_edge(UP, buff=0.6)
        with self.voiceover(
            "Three excerpts from the House's new module carry most of the part. The tangency portfolio: solve the "
            "covariance matrix against the expected excess returns, and normalise. The Hansen-Jagannathan bound: the "
            "same solve, and its square root is the highest Sharpe ratio the assets can form, which is also the least "
            "volatility any discount factor must have. And Shleifer and Vishny's two prices: the second falls further "
            "when the arbitrageurs' money runs. The first two are the same line of linear algebra. That is the deepest "
            "point of the part: a portfolio choice and a pricing model are the same object seen from two sides, so "
            "every error in the expected returns becomes an error in the portfolio, magnified by the inverse of the "
            "covariance matrix."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def three_reasons(self):
        heads = [(r"risk", MKT, r"the premium is paid for losing in bad times: name the state (a recession, a dealer "
                                r"squeeze, a disaster) and check it is paid there"),
                 (r"a constraint", SDF, r"the premium is paid to whoever has the balance sheet: name whose capital, and "
                                        r"what happens when it shrinks"),
                 (r"an error", BAD, r"the premium is a mispricing: name the bias, and the limit to arbitrage that keeps it "
                                    r"open; expect it to shrink once published")]
        cols = VGroup()
        for nm, col, txt in heads:
            box = RoundedRectangle(width=3.9, height=3.6, corner_radius=0.15, stroke_color=col, stroke_width=2.5)
            t = label(nm, font_size=26, color=col).next_to(box.get_top(), DOWN, buff=0.25)
            w = wrapped_label(txt, 3.4, 18, GREY_A).next_to(t, DOWN, buff=0.25)
            cols.add(VGroup(box, t, w))
        cols.arrange(RIGHT, buff=0.35).shift(DOWN * 0.2)
        title = label(r"Every premium the desk believes in gets one of three reasons", font_size=26).to_edge(UP, buff=0.5)
        foot = wrapped_label(r"the part's whole map: chapters 1--7 are risk, chapters 9--10 constraints, chapters 11--12 "
                             r"errors; the evidence of chapter 8 fits all three", 12.0, 18, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "This part has given three kinds of explanation for why something pays. <bookmark mark='a'/> Risk: the "
            "asset loses in bad times, and the premium is the price of that. The desk must name the bad state and check "
            "the asset actually loses there. <bookmark mark='b'/> A constraint: the premium goes to whoever has the "
            "balance sheet to hold the asset. The desk must name whose capital, and say what happens when it shrinks. "
            "<bookmark mark='c'/> An error: the premium is a mispricing, kept open by a limit to arbitrage. The desk "
            "must name the bias and the limit, and expect the premium to shrink once it is published. "
            "<bookmark mark='d'/> These are not exclusive, and the data rarely decide between them. But the reason "
            "matters for sizing: a risk premium is paid in exactly the state you fear, and an error can be corrected "
            "overnight."
        ) as vo:
            self.play(FadeIn(title))
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cols[i], shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def pipeline(self):
        steps = [(r"1. the claim", r"an expected return, with the state in which it is paid", MKT),
                 (r"2. the reason", r"risk, constraint or error, named before the data are opened", SDF),
                 (r"3. the estimate", r"mean, standard error, and the number of trials that found it", TAN),
                 (r"4. the hold-out", r"out of sample, against equal weights and the market", GOOD),
                 (r"5. the stress", r"its worst month, and who else must sell then", BAD),
                 (r"6. the ledger", r"entered in the Track Record, kept whether it works or not", QC.HOUSE)]
        boxes = VGroup()
        for t, d, col in steps:
            b = RoundedRectangle(width=3.9, height=1.5, corner_radius=0.12, stroke_color=col, stroke_width=2.2)
            tt = label(t, font_size=19, color=col).next_to(b.get_top(), DOWN, buff=0.14)
            dd = wrapped_label(d, 3.5, 15, GREY_A).next_to(tt, DOWN, buff=0.1)
            boxes.add(VGroup(b, tt, dd))
        boxes.arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.45)).shift(DOWN * 0.2)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.05, stroke_width=2.5,
                                max_tip_length_to_length_ratio=0.25, color=GREY_B) for i in (0, 1, 3, 4)])
        arrows.add(Arrow(boxes[2].get_bottom(), boxes[3].get_top(), buff=0.05, stroke_width=2.5, color=GREY_B,
                         path_arc=-0.6))
        title = label(r"How the research desk takes a premium in", font_size=28).to_edge(UP, buff=0.4)
        with self.voiceover(
            "In practice the rule becomes a pipeline, and every later part of Act Four runs through it. "
            "<bookmark mark='a'/> A claim: this asset or strategy earns a premium, and it is paid in a stated state of "
            "the world. <bookmark mark='b'/> A reason, written down before the data are opened. <bookmark mark='c'/> "
            "An estimate, with its standard error and the number of variants tried along the way. "
            "<bookmark mark='d'/> A hold-out: performance on data the estimate never saw, against equal weights and "
            "the market. <bookmark mark='e'/> A stress: its worst month, and who else must sell in it. "
            "<bookmark mark='f'/> And the ledger: the result enters the House's track record, kept whether the "
            "premium survives or not, so that the desk's own trial count is never forgotten. Part twenty-four sends "
            "the first factors through it."
        ) as vo:
            self.play(FadeIn(title))
            for i, mk in enumerate(("a", "b", "c", "d", "e", "f")):
                vo.wait_until(mk)
                anims = [FadeIn(boxes[i], shift=UP * 0.15)]
                if i > 0:
                    anims.append(GrowArrow(arrows[{1: 0, 2: 1, 3: 4, 4: 2, 5: 3}[i]]))
                self.play(*anims)
        self.wait(0.4)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("research",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{frontier\_weights}, \texttt{gmv}, \texttt{tangency}", r"Markowitz and Tobin"),
            (r"\texttt{capm\_betas}, \texttt{sml}", r"the CAPM and its flat line"),
            (r"\texttt{hj\_excess}, \texttt{hj\_gross}, \texttt{crra\_sdf}, \texttt{euler\_moments}", r"the SDF and GMM"),
            (r"\texttt{implied\_gamma}, \texttt{sdf\_ratio}", r"the equity premium puzzle"),
            (r"\texttt{ex\_post\_rational}, \texttt{cs\_decomposition}", r"Shiller, Campbell--Shiller"),
            (r"\texttt{shleifer\_vishny}, \texttt{gk\_multiplier}, \texttt{run\_ups}", r"limits, flows, bubbles"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=16, color=QC.HOUSE), label(b_, font_size=16, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 7.6)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 23: every expected return the House uses comes with its standard error and the number "
                             r"of trials behind it; every premium is given a reason (a risk, a constraint or an error) and "
                             r"the bad state in which it is paid; every set of portfolio weights is judged out of sample, "
                             r"against equal weights; and every premium is sized for its crash, not its average.", 12.4, 20,
                             QC.HOUSE).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The research desk opens with these tools. <bookmark mark='a'/> The frontier, the minimum-variance and "
            "tangency portfolios; betas and the security market line; the discount factor's bounds and its Euler "
            "equations for GMM; the puzzle's arithmetic; Shiller's ex post rational price and the Campbell-Shiller "
            "split; and the limits to arbitrage, the flow multiplier and run-ups. <bookmark mark='b'/> And the "
            "twenty-third rule. Every expected return the House uses comes with its standard error, and the number of "
            "trials behind it. Every premium is given a reason, a risk, a constraint or an error, and the bad state in "
            "which it is paid. Every set of portfolio weights is judged out of sample, against equal weights. And every "
            "premium is sized for its crash, not its average."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"the optimiser", r"a tangency portfolio fitted on 30 years of returns: judged out of sample "
                          r"against 1/N, it loses; the rule keeps the House from trading the in-sample Sharpe ratio",
                          width=12.0, font_size=19),
            desk_question(r"a new anomaly", r"a backtest with $t$ = 2.4 after many tries: the rule asks for the trial "
                          r"count first (Part 25), then the reason, then the state in which it loses", width=12.0,
                          font_size=19),
            desk_question(r"the arbitrage fund, 1998", r"a convergence trade sized on its Sharpe ratio, not on the "
                          r"month investors withdraw: Shleifer and Vishny's chart is the stress test", width=12.0,
                          font_size=19),
            desk_question(r"the industry that doubled", r"a run-up is half a crash: sized for the crash, a position can "
                          r"stay long or short without the date mattering", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.22)
        if cards.height > 6.8:
            cards.scale_to_fit_height(6.8)
        with self.voiceover(
            "Hold the rule against this part's cases. <bookmark mark='a'/> The optimiser: a tangency portfolio judged "
            "out of sample against equal weights would never have been traded on its in-sample Sharpe ratio. "
            "<bookmark mark='b'/> A new anomaly with a t-statistic of two point four: the rule asks how many tries "
            "found it, why it should pay, and in which state it loses, before anyone looks at the backtest's curve. "
            "<bookmark mark='c'/> The arbitrage fund: a convergence trade sized for the month its investors leave. "
            "<bookmark mark='d'/> And the industry that doubled: a position sized for the crash does not need to know "
            "the date. None of this makes the expected return easier to know. It makes the House honest about how "
            "little it knows."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c", "d")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
