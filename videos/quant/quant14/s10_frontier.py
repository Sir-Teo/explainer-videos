from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import PART


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.cards()

    def card(self):
        c = chapter_card(9, r"The frontier, and what desks use", r"Which of these runs on a trading desk?", part=PART)
        with self.voiceover("Chapter nine. The frontier, and what desks use."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def cards(self):
        cards = VGroup(
            history_card(2020, r"Gatheral, Jusselin and Rosenbaum", r"The quadratic rough Heston model: variance is a "
                         r"quadratic function of a rough, weighted sum of past returns, so falls and rallies feed back into "
                         r"volatility (the Zumbach effect). It fits S\&P 500 and VIX smiles together.", color=QC.IDEA,
                         width=6.2, font_size=20),
            history_card(2022, r"Guyon", r"The dispersion-constrained martingale Schr\"odinger problem: an exact joint fit of "
                         r"the S\&P 500 and VIX smiles, by entropy and optimal transport (Part 9's mathematics). A "
                         r"benchmark that any continuous-time model can be measured against.", color=QC.IDEA, width=6.2,
                         font_size=20),
            history_card(2023, r"Cuchiero, Gazzetta and Svaluto-Ferro", r"Signature volatility models: volatility as a "
                         r"linear function of the path signature (Part 5) of a driving process. Linear in the parameters, "
                         r"so calibration to both markets becomes a regression on simulated signatures.", color=QC.IDEA,
                         width=6.2, font_size=20),
            history_card(2021, r"Horvath, Muguruza and Tomas", r"Deep learning volatility: train a network on the model's "
                         r"prices once, then calibrate rough Bergomi in milliseconds. Speed is what kept rough models off "
                         r"desks; surrogates are how they arrive (Part 17).", color=QC.HOUSE, width=6.2, font_size=20),
        )
        grid = VGroup(VGroup(cards[0], cards[1]).arrange(RIGHT, buff=0.35, aligned_edge=UP),
                      VGroup(cards[2], cards[3]).arrange(RIGHT, buff=0.35, aligned_edge=UP)).arrange(DOWN, buff=0.3)
        if grid.height > 7.2:
            grid.scale_to_fit_height(7.2)
        grid.move_to(ORIGIN)
        with self.voiceover(
            "The frontier is moving fast. Jim Gatheral, Paul Jusselin and Mathieu Rosenbaum's quadratic rough Heston "
            "model makes variance a quadratic function of a rough average of past returns, which joins this part's "
            "two ideas, roughness and path-dependence, and fits the S&P 500 and VIX smiles together. "
            "<bookmark mark='a'/> Julien Guyon's martingale Schrödinger construction fits both markets exactly, and "
            "serves as the benchmark. <bookmark mark='b'/> Christa Cuchiero and her co-authors write volatility as a "
            "linear function of a path's signature, so calibration becomes a regression. <bookmark mark='c'/> And "
            "what do desks actually run? Speed decides. Rough Bergomi has no closed form and needs Monte Carlo, too "
            "slow to recalibrate every few seconds. Blanka Horvath, Aitor Muguruza and Mehdi Tomas trained a network "
            "on the model's prices once, and calibrated it in milliseconds. That is how rough models reach a desk, "
            "and it is Part seventeen."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[3], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
