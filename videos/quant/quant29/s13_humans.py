from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import FORMULA, GOOD, HURDLE, PART


class Humans(VoiceoverScene):
    def construct(self):
        self.card()
        self.three()
        self.priors()
        self.economics()
        self.stopping()
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
        import math
        h4, h2 = math.sqrt(2 * math.log(1e4)), math.sqrt(2 * math.log(1e2))
        rows = [cmath(r"\text{hurdle}(N)", r"\approx", r"\sqrt{2\ln N}\ \cdot\ \text{s.e.}", font_size=34,
                      colors={r"\text{hurdle}(N)": HURDLE}),
                cmath(r"N = 10^{4}", r"\to", rf"{h4:.1f}\ \text{{s.e.}},\qquad N = 10^{{2}} \to {h2:.1f}\ \text{{s.e.}}", font_size=32),
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
            f"{h4:.1f} standard errors; a hundred tries at {h2:.1f}. <bookmark mark='c'/> So a researcher's prior is "
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

    def economics(self):
        cards = VGroup(
            desk_question(r"leverage constraints", r"investors who cannot borrow buy risky assets to get risk, bidding them "
                          r"up and their future returns down (Frazzini and Pedersen, `Betting against beta', 2014)",
                          width=12.4, font_size=19),
            desk_question(r"lottery demand", r"assets with extreme daily jumps are bought as lottery tickets and earn less "
                          r"afterwards (Bali, Cakici and Whitelaw, 2011, the MAX effect)", width=12.4, font_size=19),
            desk_question(r"a prior predicts, it does not only explain", r"each story says where the effect should be "
                          r"strongest: where borrowing is costly, or where retail attention is high; that is the test, "
                          r"and it must be stated before the data are seen", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        head = label(r"Calm coins beat wild ones: who would leave that on the table?", font_size=28).to_edge(UP, buff=0.4)
        if cards.height > 6.0:
            cards.scale_to_fit_height(6.0)
        cards.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "Take the pattern our miners found: calm coins beat wild ones. A researcher's first job is to ask why anyone "
            "would leave that on the table. <bookmark mark='a'/> One answer is leverage constraints: investors who "
            "cannot borrow buy risky assets to get risk, which bids them up and lowers their later returns, Andrea "
            "Frazzini and Lasse Pedersen's betting against beta. <bookmark mark='b'/> Another is lottery demand: assets "
            "with extreme daily jumps are bought like lottery tickets and do worse afterwards, as Turan Bali, Nusret "
            "Cakici and Robert Whitelaw found in stocks. <bookmark mark='c'/> A story earns its place only if it "
            "predicts where the effect should be strongest, and the prediction is written down before the data are "
            "looked at. A story told afterwards, to fit what was found, is just one more trial."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def stopping(self):
        rows = [cmath(r"\mathbb E\max_{i \le N} \hat\theta_i", r"\approx", r"\sigma\sqrt{2\ln N}", font_size=32,
                      colors={r"\mathbb E\max_{i \le N} \hat\theta_i": HURDLE}),
                cmath(r"\frac{d}{dN}\,\sigma\sqrt{2\ln N}", r"=", r"\frac{\sigma}{N\sqrt{2\ln N}}", font_size=32),
                cmath(r"\text{stop when}", r"\ ", r"\text{a new trial's expected gain} < \text{its cost} + "
                      r"\text{the bar's rise}", font_size=28, colors={r"\text{stop when}": GOOD})]
        whys = [why(r"the best of $N$ draws of pure noise, the yardstick for every search"),
                why(r"the gain from one more trial shrinks almost like $1/N$: the thousandth formula is worth a thousandth "
                    r"of the first"),
                why(r"every trial also raises the bar the winner must clear by the same amount: past a point, searching "
                    r"more makes the result less believable, not more")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "And judgement includes knowing when to stop. <bookmark mark='a'/> The best of N noise draws sits at sigma "
            "times the root of two log N. <bookmark mark='b'/> Its slope falls almost like one over N: the thousandth "
            "formula adds a thousandth as much as the first. <bookmark mark='c'/> But every trial also raises the bar "
            "that the winner must clear, by exactly the same amount. So past a point, a larger search does not make the "
            "result more convincing. It makes it less."
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
