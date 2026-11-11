from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import BAD, GOOD, HURDLE, PART
from videos.quant.quant32.illustrations import covariance_case


class Envelope(VoiceoverScene):
    def construct(self):
        self.card()
        self.protocol()
        self.history()
        self.fixed_rebalance()
        self.interpretation()
        self.question()

    def card(self):
        c = chapter_card(9, r"Evaluation protocol and fixed macro-book arithmetic",
                         r"What does a risk-control calculation establish, and what still needs evidence?", part=PART)
        with self.voiceover(
            "Chapter nine. An evaluation protocol specifies what would be measured before interpreting "
            "a strategy result. Here we examine that protocol and a chosen covariance-change calculation. "
            "The arithmetic is not a historical backtest, an investment verdict or a reconstruction "
            "of the House's registered strategy outcomes."
        ):
            self.play(FadeIn(c[0]), FadeIn(c[1]))
        self.play(FadeOut(c))

    def protocol(self):
        cards = VGroup(
            desk_question(r"before evaluation", r"fix the universe, signal, information lag, scaling, limits, "
                          r"cash-flow conventions and full cost model", width=12.2, font_size=20),
            desk_question(r"research history", r"retain all specifications and selection; a counter is metadata, "
                          r"not an effective number of independent tests", width=12.2, font_size=20),
            desk_question(r"claims", r"distinguish a mathematical identity, forecast calibration, historical "
                          r"performance, causal explanation and an investment decision", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cards[0]))
        with self.voiceover(
            "First fix the universe, signal timing, risk scaling, constraints and cash-flow convention. "
            "State the cost model and what would count as success before examining an outcome. "
            "<bookmark mark='a'/> Retain the research history, including unsuccessful specifications "
            "and reused validation periods. A trial count is useful metadata but does not by itself "
            "estimate an effective number of independent tests. "
            "<bookmark mark='b'/> Then state the claim being assessed. An exact identity, a calibrated "
            "risk forecast, a historical return, a causal explanation and an allocation decision "
            "have different evidential requirements. One cannot stand in for all the others."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def history(self):
        rows = VGroup(
            label(r"existing registration metadata", font_size=29, color=HURDLE),
            MathTex(r"23{,}535+8=23{,}543\quad\text{through Part 32}", font_size=37),
            MathTex(r"23{,}562\quad\text{existing global charges}", font_size=37),
        ).arrange(DOWN, buff=0.6)
        foot = wrapped_label(r"existing research-history counts only; no new registration or performance evidence",
                             12.2, 18, GREY_A).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(foot))
        with self.voiceover(
            "The existing registration history has twenty-three thousand five hundred thirty-five "
            "charges through Part thirty-one and eight more through Part thirty-two, giving "
            "twenty-three thousand five hundred forty-three. "
            "<bookmark mark='a'/> The existing global total is twenty-three thousand five hundred "
            "sixty-two. These counts describe research history. They do not supply a new result, "
            "a confidence interval or a ranking of macro strategies. No additional registration "
            "is needed to demonstrate the fixed arithmetic on the next screen."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def fixed_rebalance(self):
        a, b = covariance_case(), covariance_case(0.6)
        old, new = a["target_weights"], b["target_weights"]
        old_risk_new_cov = float(np.sqrt(old @ b["covariance"] @ old))
        turnover = float(np.abs(new - old).sum())
        fee_bp = 1e4 * 0.0005 * turnover
        bp = r"\text{基点}" if zh() else r"{\rm bp}"
        fee_unit = r"\text{基点，占初始资本}" if zh() else r"{\rm bp\ of\ initial\ capital}"
        rows = VGroup(
            MathTex(r"\sigma=(20\%,10\%),\quad w_{\rm base}=(1/3,2/3),\quad \sigma^*=10\%", font_size=31),
            MathTex(rf"\rho:-0.2\to0.6,\quad L_{{old}}={a['leverage']:.3f},\quad "
                    rf"\sigma_{{old\ positions,new\ cov}}={100 * old_risk_new_cov:.2f}\%", font_size=31),
            MathTex(rf"L_{{new}}={b['leverage']:.3f},\qquad \sum_i|\Delta w_i|={turnover:.4f}", font_size=34),
            MathTex(rf"5\ {bp}\times {turnover:.4f}={fee_bp:.2f}\ {fee_unit}", font_size=32),
        ).arrange(DOWN, buff=0.5)
        foot = wrapped_label(r"chosen instantaneous forecast change at fixed prices; no drift, flows or market "
                             r"trial; desired positions and fee stated per initial capital, fee paid separately",
                             12.2, 18, GREY_A).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(rows[0]), FadeIn(foot))
        with self.voiceover(
            "Choose the two-asset example again, with twenty and ten percent standard deviations "
            "and base weights one third and two thirds. Target ten percent risk. "
            "<bookmark mark='a'/> Change only the covariance forecast, from correlation minus "
            f"point two to plus point six. Old leverage is {a['leverage']:.3f}; the same old "
            f"positions have {100 * old_risk_new_cov:.2f} percent risk under the new covariance. "
            f"<bookmark mark='b'/> Desired new leverage is {b['leverage']:.3f}. With prices and "
            f"capital fixed, absolute notional change is {turnover:.4f} per initial dollar. "
            f"<bookmark mark='c'/> A chosen five-basis-point fee per traded notional costs "
            f"{fee_bp:.2f} basis points of initial capital. We state the fee separately; deducting "
            "it from portfolio wealth would also change any subsequent capital-normalised weights. "
            "No market-return sequence or strategy performance is evaluated."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def interpretation(self):
        cards = VGroup(
            desk_question(r"established here", r"risk sensitivity and notional/fee units under selected covariance, "
                          r"position and financing conventions", width=12.2, font_size=20),
            desk_question(r"not established", r"forecast accuracy, achievable fills, net alpha, crisis protection "
                          r"or the superiority of either allocation", width=12.2, font_size=20),
            desk_question(r"further evidence", r"available data vintages, independent evaluation, dependence-aware "
                          r"uncertainty, stress limits and actual execution assumptions",
                          width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(cards[0]))
        with self.voiceover(
            "The calculation establishes sensitivity and units under its chosen assumptions. "
            "<bookmark mark='a'/> It does not establish that the new covariance forecast is correct, "
            "that the trades can be filled at the chosen fee, or that either allocation earns "
            "net alpha or protects a crisis. "
            "<bookmark mark='b'/> A prospective evaluation would need appropriate data vintages, "
            "independent assessment, dependence-aware uncertainty and execution assumptions. "
            "Stress scenarios can reveal vulnerability without estimating its probability. "
            "The final investment decision also depends on objectives and constraints beyond "
            "the one risk target used in this mathematical illustration."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def question(self):
        panel = VGroup(
            MathTex('\\Sigma_{\\rm old}\\longrightarrow\\Sigma_{\\rm new}', font_size=34),
            MathTex('\\sigma(w_{\\rm old};\\Sigma_{\\rm new})=14.14\\%', font_size=34),
            MathTex('\\sigma(w_{\\rm new};\\Sigma_{\\rm new})=10\\%', font_size=34),
        ).arrange(DOWN, buff=0.6).shift(UP * 0.3)
        self.play(FadeIn(panel))
        q = pause_card(r"A forecast change raises the risk of existing positions from 10\% to 14.14\%. "
                       r"Does a recalculated 10\% target prove that the initial loss was avoided or the forecast correct?")
        with self.voiceover(
            "Pause and predict. A covariance forecast change raises the measured risk of existing "
            "positions from ten to fourteen point one four percent. The rule recalculates desired "
            "weights for ten percent risk. Does that prove an earlier loss was avoided, or that "
            "the new forecast is correct? State what the arithmetic actually establishes."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
