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
            desk_question(r"the data", 'what to measure, audit vintage, timing, membership and missing outcomes: the miner can only find what the data contain', width=12.4, font_size=19),
            desk_question(r"the judgement", r"when to stop searching, how many trials to admit, what costs and capacity "
                          r"allow, and when a strategy that worked has stopped working", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three human responsibilities remain. <bookmark mark='a'/> Specify useful hypotheses and economic mechanisms before seeing outcomes, while allowing for the possibility that a prior excludes the truth. <bookmark mark='b'/> Audit data timing, vintage, membership, missing outcomes, revisions and trading access; a broad retrospective archive does not prove that nothing was lost to survivorship. <bookmark mark='c'/> Record the full selection history, choose how to validate or stop, and assess execution, capacity, financing and changing risks. Automated code can enforce defined rules, but cannot turn unspecified assumptions into evidence."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
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
        whys = [why(r"leading independent Gaussian reference: the maximum scale is $\sqrt{2\ln N}$ standard errors; "
                    r"dependence and other tails require a different calibration"),
                why(r"a hundredfold smaller search lowers the bar by more than a standard error"),
                why('an ex-ante restriction may reduce selection burden, but can exclude useful signals; post-hoc priors spend data')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            f"""An ex-ante restriction can reduce a search's selection burden. <bookmark mark='a'/> In the particular independent Gaussian null model, the leading maximum scale is square root two log N standard errors. <bookmark mark='b'/> Ten thousand nominal tests give {h4:.1f}; one hundred give {h2:.1f}. Related scores and adaptive search need a different calibration. <bookmark mark='c'/> A prior may also exclude useful ideas. Choosing or rewriting it after looking at outcomes spends data and creates additional selection. Its value is not exactly the number of strings removed, and no prior supplies a universal independence or error-control guarantee."""
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
        whys = [why(r"leading independent Gaussian reference scale; not a universal yardstick for adaptive searches"),
                why(r"the leading Gaussian-reference slope is $\sigma/(N\sqrt{2\ln N})$, for $N>1$; not a comparison with "
                    r"the singular approximation at $N=1$"),
                why(r"heuristic cost--benefit rule; valid stopping needs specified objectives and a sequential or frozen validation policy; "
                    r"the reference maximum alone cannot decide when to stop")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "When to stop depends on the objective and evidence. <bookmark mark='a'/> For independent Gaussian noise, sigma times square root two log N is a leading maximum scale. <bookmark mark='b'/> Its derivative is sigma divided by N times square root two log N, for N greater than one. This diminishing slope cannot compare the thousandth trial with a singular approximation at N equal to one. <bookmark mark='c'/> Deciding whether further search is worthwhile also needs a prior over real improvements, computational and execution costs, and a validation or sequential-testing policy. The displayed stopping inequality is a heuristic planning rule, not a theorem that more search always makes a result less credible."
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
        q = pause_card(r"an ex-ante argument cuts a search from a million formulas to a thousand. Under the leading "
                       r"independent Gaussian reference, by how many standard errors does the scale fall?")
        with self.voiceover(
            'Pause and predict. An ex-ante argument cuts a search from a million formulas to a thousand. Under the leading independent Gaussian reference, by how many standard errors does the scale fall?'
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
