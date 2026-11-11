from __future__ import annotations

from explainer.quant import *  # noqa: F403
from explainer.quant.house import systematic as SY
from videos.quant.quant32.common import BAD, GOOD, HURDLE, PART, house_lab
from videos.quant.quant32.illustrations import covariance_case, currency_case


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet()
        self.lab_trend()
        self.lab_risk()
        self.lab_identity()
        self.module()
        self.test()

    def card(self):
        c = chapter_card(10, r"Rule 32: specify the macro book",
                         r"What is the model contract, and which evidence supports each claim?", part=PART)
        with self.voiceover(
            "Chapter ten. The House's thirty-second rule is to specify the macro book before "
            "judging it. State the instruments, information timing, risk and financing conventions, "
            "and distinguish a mathematical check from evidence about attainable performance. "
            "A plausible premium story is a hypothesis, not a substitute for the relevant evidence."
        ):
            self.play(FadeIn(c[0]), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self):
        a, fx = covariance_case(), currency_case()
        rows = VGroup(
            label(r"fixed trend paths: same S=4, but P=6 or P=0 as Q changes", font_size=25),
            label(r"risk target 10\%, forecast 10\%, true SD 20\%: scaled risk 20\%", font_size=25),
            label(rf"chosen inverse-vol base: risk {100 * a['base_risk']:.2f}\%, target leverage {a['leverage']:.3f}",
                  font_size=25),
            label(r"old positions under correlation change: chosen risk 10\% to 14.14\%", font_size=25),
            label(rf"foreign deposit 6\%, cash 2\%, spot -5\%: excess "
                  rf"{100 * fx['cases'][0]['excess_over_domestic']:.1f}\%", font_size=25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        foot = wrapped_label(r"chosen mathematical checks only; no strategy Sharpe, held-out result or allocation verdict",
                             12.2, 18, GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "The first sheet records what the chosen calculations established. A common terminal "
            "increment does not determine linear-trend profit because path variation differs. "
            "<bookmark mark='a'/> A volatility target also needs a correct forecast; a covariance "
            "stress changes risk even before a new trade occurs. "
            "<bookmark mark='b'/> Inverse-volatility budgets require a covariance convention, "
            "and a foreign rate advantage can be outweighed by currency depreciation. These "
            "checks establish units, timing and conditional identities. They do not supply "
            "a realised strategy Sharpe, an allocation verdict or a causal attribution of a crisis."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]), FadeIn(rows[4]))
        self.clear_scene()

    def lab_trend(self):
        lab = house_lab(r"Lab: exact existing signal code", SY.tsmom_positions, "past = cs", 6, width=11.8)
        self.play(FadeIn(lab))
        with self.voiceover(
            "Read the existing signal code literally. The past-return statistic is a sum, "
            "eligibility requires at least ninety percent of the lookback observations, and "
            "the linear alternative uses a clipped volatility-normalised signal. Coefficients "
            "are stored at the close. The separate book function applies yesterday's coefficient "
            "to today's return and defines its active-market denominator. Those masks and "
            "timing conventions are part of the algorithm; an attractive description cannot "
            "replace checking them."
        ):
            self.wait(0.2)
        self.clear_scene()

    def lab_risk(self):
        lab = house_lab(r"Lab: inverse-vol weights and gross-cap scaling",
                        SY.inverse_vol_weights, "v = np.asarray", 4,
                        extra=((SY.risk_parity, "if w.sum() > 0:", 6),), width=11.8)
        self.play(FadeIn(lab))
        with self.voiceover(
            "The risk code first normalises inverse volatilities among valid assets. In the "
            "hierarchical rule, group standalone volatilities determine another set of scales. "
            "The final lines use the estimated covariance to target overall risk and cap "
            "gross exposure. This does not solve a general equal group Euler-contribution "
            "problem. Nor does the cap certify liquidity or attainable funding. The original "
            "algorithm remains exactly as written; the lesson states what its construction "
            "does and what additional assumptions a performance claim would need."
        ):
            self.wait(0.2)
        self.clear_scene()

    def lab_identity(self):
        lab = house_lab(r"Lab: the exact block identity", SY.linear_trend_blocks,
                        "pos = np.cumsum", 5, width=11.8)
        self.play(FadeIn(lab))
        with self.voiceover(
            "The block helper makes a different mathematical object. Positions equal the "
            "sum of earlier increments within each block. Profit is their inner product "
            "with later increments, and S and Q are the arithmetic sum and sum of squares. "
            "The equality to half S squared minus half Q is pathwise. It needs no Gaussian "
            "distribution, but its mean and distributional theorems need further assumptions. "
            "Dropping missing observations before blocking also changes the observation clock "
            "if this helper is applied to empirical data."
        ):
            self.wait(0.2)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("macro", "portfolio"))
        foot = wrapped_label(r"Rule 32: preserve the model, timing, research history, net cash flows and claim-specific evidence",
                             12.2, 19, HURDLE).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(chart), FadeIn(foot))
        with self.voiceover(
            "The macro desk proposes signals and exposure designs; the portfolio desk must "
            "understand their joint risks, not just their names. "
            "<bookmark mark='a'/> Preserve the rule and research history, distinguish available "
            "information from later revisions, and account for collateral, funding and execution. "
            "<bookmark mark='b'/> Report distributions and stress sensitivities with the sample "
            "and uncertainty appropriate to each claim. A risk identity, a calibration check "
            "and independent net-performance evidence answer different questions. The decision "
            "must also fit the institution's objectives and constraints."
        ) as vo:
            vo.wait_until("a")
            self.wait(0.2)
            vo.wait_until("b")
            self.wait(0.2)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"income pitch", r"separate coupon or option income from mark-to-market losses, "
                          r"tail exposure, collateral and net costs", width=12.2, font_size=20),
            desk_question(r"balanced-risk pitch", r"identify covariance assumptions, leverage, financing "
                          r"and what happens to existing positions when inputs change", width=12.2, font_size=20),
            desk_question(r"crisis-hedge pitch", r"specify the rule, horizon, prior exposure and range of "
                          r"episodes; a convex mechanism does not guarantee every crisis outcome",
                          width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cards[0]))
        with self.voiceover(
            "Apply the rule to three pitches. Income is not the same as profit: ask what "
            "mark-to-market losses and tail exposures accompany it. "
            "<bookmark mark='a'/> For balanced risk, identify covariance assumptions, leverage "
            "and financing, including the risk of positions already held when inputs change. "
            "<bookmark mark='b'/> For a crisis hedge, specify the horizon and prior exposure, "
            "and examine a suitable range of episodes rather than one selected success. "
            "A mathematical mechanism can make a claim precise. It cannot supply missing "
            "evidence merely by giving the strategy a reassuring name."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()
