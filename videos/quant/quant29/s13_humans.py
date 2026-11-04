from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import FORMULA, GOOD, HURDLE, PART


class Humans(VoiceoverScene):
    def construct(self):
        self.card()
        self.three()
        self.priors()
        self.question()

    def card(self):
        c = chapter_card(12, r"What remains for humans", r"If machines can search, write and test, what is the "
                         r"researcher for?", part=PART)
        with self.voiceover("Chapter twelve. If machines can search, write code and backtest, what is left for the "
                            "researcher?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def three(self):
        cards = VGroup(
            desk_question(r"the prior", r"which kinds of formulas deserve to be searched at all: an economic reason (who "
                          r"is on the other side, and why do they keep paying?) shrinks the search space from $10^{56}$ "
                          r"to something a counter can survive", width=12.4, font_size=19),
            desk_question(r"the data", r"what to measure, cleaned, point in time, free of survivorship: the miner can only "
                          r"find what the data contain", width=12.4, font_size=19),
            desk_question(r"the judgement", r"when to stop searching, how many trials to admit, what costs and capacity "
                          r"allow, and when a strategy that worked has stopped working", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three things. <bookmark mark='a'/> The prior: which formulas deserve to be searched at all. An economic "
            "reason, someone on the other side who keeps paying for a reason, cuts the space from ten to the fifty-six "
            "to something a trial counter can survive. <bookmark mark='b'/> The data: what to measure, cleaned and stamped "
            "in time, with nothing lost to survivorship. A miner can only find what the data contain. "
            "<bookmark mark='c'/> And judgement: when to stop searching, how many trials to admit to, what costs and "
            "capacity allow, and when a strategy that worked has stopped working."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def priors(self):
        rows = [cmath(r"\text{hurdle}(N)", r"\approx", r"\sqrt{2\ln N}\ \cdot\ \text{s.e.}", font_size=34,
                      colors={r"\text{hurdle}(N)": HURDLE}),
                cmath(r"N = 10^{4}", r"\to", r"4.3\ \text{s.e.},\qquad N = 10^{2} \to 3.0\ \text{s.e.}", font_size=32),
                cmath(r"\text{a prior}", r"=", r"\text{a smaller } N \text{ with the same chance of containing the truth}",
                      font_size=28, colors={r"\text{a prior}": GOOD})]
        whys = [why(r"the best of $N$ independent noise statistics sits about $\sqrt{2\ln N}$ standard errors above zero "
                    r"(Part 26's expected maximum)"),
                why(r"a hundredfold smaller search lowers the bar by more than a standard error"),
                why(r"so a human's prior is worth exactly what it removes from the search without removing the signal")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "There is arithmetic behind the first. <bookmark mark='a'/> The best of N pure-noise statistics sits about the "
            "square root of two log N standard errors above zero. <bookmark mark='b'/> Ten thousand tries put the bar at "
            "four point three standard errors; a hundred tries at three. <bookmark mark='c'/> So a researcher's prior is "
            "worth exactly what it removes from the search without removing the truth."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        q = pause_card(r"an economic argument cuts a search from a million formulas to a thousand. By how many standard "
                       r"errors does the hurdle fall?")
        with self.voiceover(
            "Pause and predict. An economic argument cuts a search from a million formulas to a thousand. By how many "
            "standard errors does the hurdle fall?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
