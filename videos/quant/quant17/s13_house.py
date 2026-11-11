from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import axes, data_range
import numpy as np

from videos.quant.quant17.common import BAD, GOOD, NET, PART, REF, load



class House(VoiceoverScene):
    def construct(self):
        env = load("envelope")
        self.card()
        self.validation_plan()
        self.module(env)

    def card(self):
        c = chapter_card(19, r"Rule 17: the validation plan", r"Is a hedger better than the simulator it was trained on?", part=PART)
        with self.voiceover("Chapter nineteen. The House's rule seventeen: a validation plan, with its unfinished empirical test made explicit."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def validation_plan(self):
        title = label(r"Cross-generator validation: required evidence", font_size=32).to_edge(UP, buff=0.4)
        entries = [
            (r"Before evaluation", r"freeze policy, preprocessing, payoff, costs and metrics"),
            (r"Independent simulations", r"common paths under GBM and a distinct generator; report uncertainty"),
            (r"Historical replay", r"dates disjoint from fitting and tuning; account for overlapping windows"),
            (r"Scope of this pass", r"legacy BTC-through-2025 job not run; no cross-generator scores claimed"),
        ]
        cards = VGroup(*[desk_question(q, a, width=12.0, font_size=23) for q, a in entries]).arrange(DOWN, buff=0.28)
        if cards.height > 6.1:
            cards.scale_to_fit_height(6.1)
        cards.next_to(title, DOWN, buff=0.3)
        with self.voiceover("Rule seventeen requires validation across generators and history before use. The original cross-generator job is not evidence for that full claim: it fits a GARCH model on the first eighty percent of BTC history through 2025, then includes overlapping fitted history in its replay. We have not run it in this pass. <bookmark mark='a'/> A defensible plan freezes the policy, preprocessing, payoff, costs and metrics first. Evaluate daily delta, the classical band and learned policies on common independently simulated paths, with uncertainty. Keep fitting and historical evaluation dates disjoint. <bookmark mark='b'/> For each world, report the empirical short-call risk, costs, holdings and tail diagnostics. Under physical drift, subtract the optimized no-claim baseline before calling a cash amount an indifference premium. Preserve a final registered window for its authorized opening. This is a validation design, not a completed cross-generator test or permission for a network to trade.") as vo:
            self.play(FadeIn(title), FadeIn(cards[3]))
            vo.wait_until("a")
            self.play(FadeIn(cards[0]), FadeIn(cards[1]))
            vo.wait_until("b")
            self.play(FadeIn(cards[2]))
        self.wait(0.6)
        self.clear_scene()

    def module(self, env):
        chart = house_chart(PART, lit=("vol", "research")).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{calib\_net}, \texttt{calibrate\_neural}", r"rough Bergomi through a network, with a Monte Carlo check"),
            (r"\texttt{train\_differential}, \texttt{gp\_with\_gradients}", r"differential machine learning and its twin"),
            (r"\texttt{deep\_bsde}, \texttt{deep\_stopping}", r"high-dimensional pricing and exercise"),
            (r"\texttt{Hedger}, \texttt{train\_hedger\_on}", r"the deep hedger on any simulator: entropic or CVaR, "
             r"band networks with a Whalley--Wilmott start"),
            (r"\texttt{leland\_sigma}, \texttt{merton\_hedge}", r"the classical answers it is checked against"),
            (r"\texttt{NeuralSV}", r"neural SDEs and numerical model sensitivity"),
            (r"\texttt{train\_sig\_generator}, \texttt{train\_ddpm}", r"market generators, scored by \texttt{stylized\_facts}"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=19, color=QC.HOUSE), label(b, font_size=19, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 6.4)
        tab.next_to(chart, DOWN, buff=0.3)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 17: no network is used without a slower, independent engine that can check it; inputs "
                             r"outside the region it was trained on go to that engine instead; and a hedger is tested on at "
                             r"least two market generators and on replayed history before it trades.  "
                             rf"No new registered market trial in this pass; the counter remains {env['trials']}.", 12.4, 22,
                             QC.HOUSE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            f"The codebase supplies neural calibration, differential regression, Gaussian processes, BSDE and stopping solvers, hedgers and generators. These are implementations with different assumptions and approximation errors; the Gaussian process solves its chosen regularized statistical system, not every pricing problem exactly. <bookmark mark='a'/> The rule proposes independent checks where available, explicit training-region controls and evaluation on multiple generators and disjoint history before deployment. A slow engine is useful only within its own validated scope. <bookmark mark='b'/> This pass corrects explanations and reviews fixed numerical illustrations. It does not implement the proposed routing or monitoring service, complete the withheld historical test, or certify deployment. There is no new registered market trial; the cumulative counter remains {env['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["vol"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=6))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()
