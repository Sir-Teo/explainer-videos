from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import BAD, GOOD, HURDLE, PART, TREND_C, fit_right
from videos.quant.quant32.illustrations import trend_paths


class Smile(VoiceoverScene):
    def construct(self):
        self.card()
        self.frontier()
        self.terminal(trend_paths())
        self.reversal()
        self.jump()
        self.straddle()
        self.cost()
        self.blend()
        self.evidence()
        self.question()

    def card(self):
        c = chapter_card(2, r"The smile and the crisis", r"What does trend convexity establish about crisis protection?",
                         part=PART)
        with self.voiceover(
            "Chapter two. Crisis alpha is a description of particular historical outcomes, not a guarantee "
            "attached to the word trend. The mathematical mechanism is more precise: an ideal linear rule "
            "has a convex block-profit identity. Its terminal move, path variation, timing and costs all matter. "
            "We will keep that identity separate from a claim about an implementable crisis hedge."
        ):
            self.play(FadeIn(c[0]), FadeIn(c[1]))
        self.play(FadeOut(c))

    def frontier(self):
        g = axes([-6, 6], [-5, 13], x_length=7.4, y_length=4.5,
                 xlabel=r"arithmetic block total $S$", ylabel=r"linear-rule PnL $P$",
                 xticks=[-4, 0, 4], yticks=[-4, 0, 6, 12], font_size=16).move_to(LEFT * 1.9)
        colors = [QC.DELTA, TREND_C, QC.OPTION]
        curves = VGroup()
        for q, col in zip([2.0, 4.0, 8.0], colors):
            xs = np.linspace(-np.sqrt(4 * q), np.sqrt(4 * q), 121)
            curves.add(curve(g.ax, xs, (xs ** 2 - q) / 2, col, stroke_width=3))
        leg = legend([(col, rf"chosen $Q={q}$") for col, q in zip(colors, [2, 4, 8])],
                     font_size=19).to_edge(RIGHT, buff=0.4).shift(UP * 1.4)
        fit_right(leg)
        scope = wrapped_label(r"$n=4$ real increments: $S^2\leq nQ$; every displayed point is feasible. "
                              r"The curves are fixed-$Q$ identities, not fitted historical returns.",
                              3.6, 19, GREY_A).next_to(leg, DOWN, buff=0.6).align_to(leg, LEFT)
        fit_right(scope)
        foot = wrapped_label(r"chosen mathematical inputs; squared increment PnL units; no risk normalisation or costs",
                             12.2, 18, GREY_A).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(g), Create(curves[0]), FadeIn(leg), FadeIn(foot))
        with self.voiceover(
            "Fix four increments and their sum of squares, Q. Profit is half S squared minus half Q. Holding Q "
            "fixed gives a convex parabola in the arithmetic block total S. "
            "<bookmark mark='a'/> Choose Q equal to two, four and eight. Higher path variation lowers the curve "
            "at the same S. We show the entire feasible range for each choice: Cauchy-Schwarz requires "
            "S squared no greater than four Q. Every endpoint is retained. "
            "<bookmark mark='b'/> This is a family of mathematical identities, not a regression through market "
            "quarters. In actual data Q varies with S, risk scaling changes exposure, and several markets "
            "contribute to a book. A convex fixed-Q section therefore does not by itself establish a positive "
            "quadratic coefficient in a particular empirical scatter."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(curves[1]), Create(curves[2]))
            vo.wait_until("b")
            self.play(FadeIn(scope))
        self.clear_scene()

    def terminal(self, paths):
        a, b = paths["persistent rise"], paths["one final jump"]
        rows = VGroup(
            label(r"same terminal total; different path variation", font_size=29, color=HURDLE),
            MathTex(rf"(1,1,1,1):\quad S={a['S']:.0f},\ Q={a['Q']:.0f},\ P={a['P']:.0f}", font_size=34),
            MathTex(rf"(0,0,0,4):\quad S={b['S']:.0f},\ Q={b['Q']:.0f},\ P={b['P']:.0f}", font_size=34),
        ).arrange(DOWN, buff=0.65)
        self.play(FadeIn(rows[0]), FadeIn(rows[1]))
        with self.voiceover(
            "Two chosen blocks expose an important distinction. Four increments of one and a single final "
            "increment of four both finish at S equal to four. "
            "<bookmark mark='a'/> The first has Q equal to four and profit six. The second has Q equal to "
            "sixteen and profit zero. Its position was zero before the jump. "
            "<bookmark mark='b'/> Thus this trading rule's profit is not a function of the terminal total alone. "
            "The identity contains realised Q, which is path dependent. Calling the response convex does not "
            "remove that term. It is possible to discuss a convex mechanism accurately without pretending "
            "that the rule delivers the payoff of one option for every path."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[2]))
            vo.wait_until("b")
            self.wait(0.2)
        self.clear_scene()

    def reversal(self):
        rows = VGroup(
            MathTex(r"r=(1,1,-1,-1)", font_size=38),
            MathTex(r"x=(0,1,2,1)", font_size=38),
            MathTex(r"x_t r_t=(0,1,-2,-1),\qquad P=-2", font_size=36, color=BAD),
        ).arrange(DOWN, buff=0.6)
        foot = wrapped_label(r"fixed four-period linear-rule arithmetic; positions use earlier increments only",
                             12.2, 18, GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "A reversal shows the timing. Choose increments one, one, minus one, minus one. "
            "<bookmark mark='a'/> The positions before those increments are zero, one, two and one, "
            "because only earlier increments enter each decision. "
            "<bookmark mark='b'/> The first negative increment meets a positive position of two and loses two. "
            "The next still meets a positive position of one and loses one. Together with the earlier gain "
            "of one, block profit is minus two. A differently clipped, signed or rebalanced rule can respond "
            "differently. This example explains one mechanism for reversal losses; it does not identify "
            "the cause of any named fund's historical drawdown."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def jump(self):
        cards = VGroup(
            desk_question(r"before the jump", r"exposure comes from earlier information; a sudden move cannot "
                          r"retroactively create a position", width=12.2, font_size=20),
            desk_question(r"during a sustained move", r"a rule can change exposure as observations accumulate; "
                          r"benefit depends on the direction, speed and subsequent path", width=12.2, font_size=20),
            desk_question(r"after a turn", r"stale exposure and repeated reversals can cause losses; horizon "
                          r"blends and volatility controls change the rule", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cards[0]))
        with self.voiceover(
            "The same reasoning explains why crisis speed matters. A sudden move cannot retroactively create "
            "an offsetting position. Exposure already held can help, hurt or be zero. "
            "<bookmark mark='a'/> A sustained move permits new observations to change a signal, but a long "
            "crisis alone does not guarantee profit: the existing signal, sizing and subsequent path matter. "
            "<bookmark mark='b'/> After a turn, exposure can remain pointed in the previous direction. Repeated "
            "turns can create repeated losses. Fast and slow horizons, sign rules and volatility controls "
            "are different designs, so an explanation for the ideal linear rule should not be silently "
            "transferred into a promise about every managed-futures product."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def straddle(self):
        rows = VGroup(
            MathTex(r"\text{centred vanilla straddle payoff: } |z|", font_size=32),
            MathTex(r"\text{linear-rule block profit: }\frac{S^2-Q}{2}", font_size=36),
            wrapped_label(r"convex response is an analogy; realised $Q$ is not a fixed option premium",
                          11.8, 25, HURDLE),
        ).arrange(DOWN, buff=0.7)
        self.play(FadeIn(rows[0]))
        with self.voiceover(
            "Make the option analogy precise. A centred vanilla straddle has a terminal payoff proportional "
            "to the absolute price move, before subtracting its premium. "
            "<bookmark mark='a'/> Our block identity is quadratic in an arithmetic total and subtracts a "
            "path-dependent sum of squares. The functional forms and units differ. "
            "<bookmark mark='b'/> Realised Q is not an option premium fixed at inception. Continuous trading "
            "identities involving realised variation require their own price-process, funding and admissibility "
            "assumptions. Fung and Hsieh's empirical lookback-option factors are also a different construction. "
            "The useful common idea is conditional convex exposure, not an exact equality between every "
            "trend system and a purchased vanilla straddle."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def cost(self):
        rows = VGroup(
            label(r"chosen cost: 0.1 PnL unit per unit position change", font_size=26),
            MathTex(r"\text{persistent rise: turnover }6,\quad 6-0.1(6)=5.4", font_size=31),
            MathTex(r"\text{reversal: turnover }4,\quad -2-0.1(4)=-2.4", font_size=31),
        ).arrange(DOWN, buff=0.65)
        foot = wrapped_label(r"includes flattening at the block end; deterministic units, no capital return, "
                             r"funding or market-impact model", 12.2, 18, GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "The identity was before costs. Choose a linear charge of one tenth of a profit unit for each "
            "unit of position change, including flattening at the block's end. "
            "<bookmark mark='a'/> The persistent rise moves from zero through one, two and three, then back "
            "to zero. Total absolute turnover is six, so profit six becomes five point four. "
            "<bookmark mark='b'/> The reversal moves zero, one, two, one, then zero. Turnover is four, so "
            "profit minus two becomes minus two point four. These are stipulated units and a stipulated fee "
            "rule. Financing, spread variation, nonlinear impact and execution constraints would add "
            "separate terms. Convex gross arithmetic is not a complete net-performance statement."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def blend(self):
        rows = VGroup(
            MathTex(r"\sigma_A=\sigma_B=10\%,\quad w=(0.8,0.2)", font_size=36),
            MathTex(r"\sigma_p^2=w_A^2\sigma_A^2+w_B^2\sigma_B^2+2w_Aw_B\rho\sigma_A\sigma_B", font_size=30),
            MathTex(r"\rho=0:\ \sigma_p=8.25\%,\qquad \rho=1:\ \sigma_p=10\%", font_size=33),
        ).arrange(DOWN, buff=0.65)
        foot = wrapped_label(r"chosen fixed covariance example; no historical fund or 60/40 blend is evaluated",
                             12.2, 18, GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "Diversification is a separate calculation. Choose two books, each with ten percent volatility, "
            "and weights eighty and twenty percent. "
            "<bookmark mark='a'/> The variance includes both standalone terms and their covariance. "
            "<bookmark mark='b'/> If correlation is zero, the combined volatility is about eight point two "
            "five percent; if it is one, volatility is ten percent. Zero correlation does not generally "
            "mean independence, and it does not determine expected returns. A historical blend would "
            "also need specified rebalancing, costs, sample selection and financing. Neither a crisis "
            "label nor a low average correlation guarantees that covariance will remain helpful in stress."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def evidence(self):
        cards = VGroup(
            desk_question(r"measure the book", r"specified universe, rule, lag, horizon, scaling, collateral "
                          r"and net costs; keep all observations and their actual ranges", width=12.2, font_size=20),
            desk_question(r"measure uncertainty", r"dependence, tails, few crisis episodes and specification "
                          r"selection affect what a fitted smile can establish", width=12.2, font_size=20),
            desk_question(r"separate mechanisms", r"a quadratic fit, a pathwise identity and a causal explanation "
                          r"answer different questions", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cards[0]))
        with self.voiceover(
            "What evidence would establish the empirical claim? First define the actual book and keep "
            "its information timing, market coverage, risk scaling, collateral and costs explicit. "
            "<bookmark mark='a'/> Then assess uncertainty. Quarterly observations can be dependent, "
            "extreme episodes are scarce, and repeated specifications change the interpretation of "
            "a fitted curve. A weak coefficient does not by itself prove either absence of a mechanism "
            "or that the sample was merely too short. "
            "<bookmark mark='b'/> Finally separate the questions. An identity can be exact for a chosen "
            "rule; a regression describes a specified sample; a causal account requires additional "
            "identifying evidence. Keeping those claims distinct makes the crisis-alpha discussion testable."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def question(self):
        panel = VGroup(
            MathTex('P=\\tfrac12(S^2-Q)', font_size=34),
            MathTex('S_A=S_B=4,\\qquad Q_A=4,\\quad Q_B=16', font_size=34),
            MathTex('(P_A,P_B)=?', font_size=34),
        ).arrange(DOWN, buff=0.6).shift(UP * 0.3)
        self.play(FadeIn(panel))
        q = pause_card(r"Two four-increment blocks have $S=4$, but $Q=4$ and $Q=16$. "
                       r"What are their linear-rule profits, and why is terminal $S$ insufficient?")
        with self.voiceover(
            "Pause and predict. Two blocks both finish with arithmetic total four. Their sums of squares "
            "are four and sixteen. What profit does the ideal linear rule earn in each, and why "
            "does knowing only the terminal total fail to determine its payoff?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
