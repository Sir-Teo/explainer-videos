"""Evaluation protocol and fixed risk-limit arithmetic; no strategy result is loaded."""
from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import riskmodel as RM
from videos.quant.quant31.common import IC_C, PART


class Envelope(VoiceoverScene):
    def construct(self):
        self.card()
        self.protocol()
        self.fixed_inputs()
        self.limits()
        self.interpretation()
        self.question()

    def card(self):
        c = chapter_card(11, r"Evaluation protocol and independent limits",
                         r"What does a variance floor change, and what can it establish?", part=PART)
        with self.voiceover("Chapter eleven. Separate an evaluation protocol from risk-limit arithmetic. "
                            "This numerical example uses chosen fixed inputs, with no market backtest."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def protocol(self):
        cards = VGroup(
            desk_question(r"before evaluation", r"specify universe, data timing, forecasts, risk, costs, constraints and "
                          r"selection before inspecting evaluation outcomes", width=12.2, font_size=20),
            desk_question(r"after inspection", r"outcome-informed changes require honest new evaluation; reused "
                          r"outcomes do not provide independent evidence", width=12.2, font_size=20),
            desk_question(r"existing registration metadata", r"23,525 prior cumulative charges + 10 existing Part 31 "
                          r"charges = 23,535; historical metadata, not new trials or performance evidence", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Specify the full decision process before evaluation. <bookmark mark='a'/> This includes data timing, "
            "signals, risk, costs, constraints and the selection of alternatives. <bookmark mark='b'/> A change informed "
            "by inspected outcomes needs honest new evaluation; the same outcomes cannot supply independent evidence. "
            "<bookmark mark='c'/> Existing registration metadata totals twenty-three thousand five hundred thirty-five "
            "through this part, including ten existing charges. Restoring unchanged research calculations adds no trials "
            "and supplies no sealed-period verdict."
        ) as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(Indicate(cards[0]))
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def fixed_inputs(self):
        rows = [cmath(r"\alpha", r"=", r"(10^{-5},10^{-5}),\quad\gamma=1,\quad\sigma^2=(10^{-8},4\cdot10^{-4})", font_size=30),
                cmath(r"x_i^*", r"=", r"\frac{\alpha_i}{\gamma\sigma_i^2}\quad\Rightarrow\quad x^*=(1000,0.025)", font_size=34),
                cmath(r"\sigma_i^2\downarrow0", r"\Rightarrow", r"|x_i^*|\uparrow\infty\quad(\alpha_i\ne0)", font_size=34)]
        whys = [why(r"chosen one-period inputs; notional divided by a unit book; diagonal known risk, no constraints or costs"),
                why(r"the unconstrained mean--variance optimum is a mathematical position, not an executable account"),
                why(r"small estimated variance does not guarantee safety against jumps, stale prices or model errors")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Choose two assets with identical forecasts of ten to the minus five and risk aversion one. "
            "<bookmark mark='a'/> Daily variances are chosen as ten to the minus eight and four times ten to the minus four. "
            "<bookmark mark='b'/> Unconstrained diagonal arithmetic gives one thousand and point zero two five times "
            "a unit book. There is no budget constraint, cost or market observation in this example. "
            "<bookmark mark='c'/> At nonzero forecast, inverse variance makes positions diverge as variance approaches zero."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.clear_scene()

    def limits(self):
        alpha, sig2 = np.array([1e-5, 1e-5]), np.array([1e-8, 4e-4])
        raw = alpha / sig2
        floored = alpha / RM.floor_variance(sig2, 1e-4)
        book_cap = RM.cap_positions(floored, book=1, cap=0.05)
        liquid_cap = RM.cap_positions(floored, book=1, cap=0.05, adv=[0.5, 0.1], adv_cap=0.1)
        values = [raw, floored, book_cap, liquid_cap]
        labels = [r"unconstrained", r"variance floor $10^{-4}$", r"then absolute book cap $0.05$",
                  r"also $0.1\times$ chosen ADV $(0.5,0.1)$"]
        tab = VGroup(*[VGroup(label(nm, font_size=22), MathTex(rf"({v[0]:g},\ {v[1]:g})", font_size=30, color=IC_C))
                      .arrange(RIGHT, buff=0.5) for nm, v in zip(labels, values)])
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        if tab.width > 12.4:
            tab.scale_to_fit_width(12.4)
        foot = wrapped_label(r"chosen fixed inputs; existing House functions; not a calibrated policy or backtest",
                             12.2, 17, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Apply existing House functions to the same chosen numbers. <bookmark mark='a'/> A variance floor of "
            "ten to the minus four gives positions point one and point zero two five. "
            "<bookmark mark='b'/> A five-percent absolute book cap gives point zero five and point zero two five. "
            "<bookmark mark='c'/> Chosen daily volumes of point five and point one book units, with a ten-percent "
            "volume cap, give point zero five and point zero one. This is a position bound, not an execution schedule."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]))
        self.clear_scene()

    def interpretation(self):
        cards = VGroup(
            desk_question(r"risk input versus feasible set", r"a floor modifies the risk input; a cap bounds "
                          r"notional positions. Clipping is not the general constrained multi-asset optimum", width=12.2, font_size=20),
            desk_question(r"what the arithmetic establishes", r"the floor makes this inverse-variance toy finite; "
                          r"finite independent caps bound positions even under model error", width=12.2, font_size=20),
            desk_question(r"what still needs evidence", r"thresholds, universe definitions, joint feasibility, costs "
                          r"and model robustness require a specified policy and honest evaluation", width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Interpret the arithmetic narrowly. <bookmark mark='a'/> A floor changes a model input; a cap changes "
            "the feasible set. Clipping is not a general constrained multi-asset solution. <bookmark mark='b'/> "
            "They bound this toy but establish neither model validity nor profitability. <bookmark mark='c'/> "
            "Thresholds, universe exclusions and combined constraints must form a specified policy. Changing a policy "
            "in response to inspected outcomes still changes the research procedure."
        ) as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            self.play(Indicate(cards[0]))
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[2]))
        self.clear_scene()

    def question(self):
        q = pause_card(r"which operation changes a risk input, which bounds positions, and does either establish future profitability?")
        with self.voiceover("Pause and predict. Which operation changes a risk input, which bounds positions, "
                            "and does either establish future profitability?"):
            self.play(FadeIn(q))
        self.clear_scene()
