"""Registration and holdout accounting; this chapter accesses no experiment payload."""
from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant24.common import PART, ask


class Track(VoiceoverScene):
    def construct(self):
        self.card()
        self.registration()
        self.costs()
        self.precision()
        self.trials()
        self.boundary()

    def card(self):
        c=chapter_card(13, r"Registration and holdout accounting",
                       r"What would a fresh test have to establish?", part=PART)
        with self.voiceover("Chapter thirteen. Registration and holdout accounting. This review does not open or score the sealed experiment. Instead, we examine what a fresh test would require, and how little precision five years can offer."):
            self.play(FadeIn(c[0], shift=UP*0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def registration(self):
        cards=VGroup(
            desk_question(r"freeze the rule",r"code hash; universe; formation and holding clocks; missing-data rule; publication vintages",width=12.0,font_size=20),
            desk_question(r"freeze implementation assumptions",r"turnover, spread, impact, financing, collateral, borrow and capacity; record all variants considered",width=12.0,font_size=20),
            desk_question(r"freeze the evaluation",r"sample window, benchmark, statistic and decision rule before examining the test outcomes",width=12.0,font_size=20),
        ).arrange(DOWN,buff=0.3)
        with self.voiceover("A registration is a timestamped commitment. <bookmark mark='a'/> Freeze the code, universe, formation and holding clocks, missing-data treatment and available publication vintages. <bookmark mark='b'/> Freeze the cost and funding assumptions, and retain every variant considered. <bookmark mark='c'/> Freeze the evaluation window, benchmark, statistic and decision rule before examining outcomes. A hash documents the commitment; it cannot make a previously examined sample unseen.") as vo:
            for i,mk in enumerate(('a','b','c')):
                if i:vo.wait_until(mk)
                self.play(FadeIn(cards[i],shift=UP*0.2))
        self.clear_scene()

    def costs(self):
        eq=MathTex(r"r^{\rm net}_{t}=r^{\rm gross}_{t}-c^{\rm trade}_{t}-c^{\rm funding}_{t}-c^{\rm borrow}_{t}",font_size=34).to_edge(UP,buff=0.8)
        text=wrapped_label(r"Bookkeeping schematic: costs depend on positions, turnover and execution. A constant annual haircut is an assumption, not observed implementation performance.",12.0,24,GREY_A).next_to(eq,DOWN,buff=0.65)
        with self.voiceover("Gross factor returns are research objects. A net implementation must account for trading, funding and borrow costs on a consistent capital base. <bookmark mark='a'/> This equation is a bookkeeping schematic. A constant annual cost haircut may be useful for a declared sensitivity exercise, but it does not reconstruct actual turnover, market impact, collateral or capacity. No net historical strategy series is generated here.") as vo:
            self.play(FadeIn(eq));vo.wait_until('a');self.play(FadeIn(text))
        self.clear_scene()

    def precision(self):
        eq=MathTex(r"t\approx SR_{\rm annual}\sqrt{Y},\qquad {\rm se}(\widehat{SR}_{\rm annual})\approx {1\over\sqrt{Y}}",font_size=34).to_edge(UP,buff=0.45)
        # the same arithmetic as a picture: the estimate's sampling density narrowing as the years of test grow
        years=ValueTracker(1.0)
        gauge=SharpePrecision(years).next_to(eq,DOWN,buff=0.4)
        foot=wrapped_label(r"IID, stable, modest-Sharpe approximation. Serial dependence, tails, estimation and selection can materially change uncertainty. No realised holdout statistic is displayed.",12.0,20,GREY_A).to_edge(DOWN,buff=0.35)
        with self.voiceover("Five years is a short test. Under a stable independent-return approximation, the mean t-statistic is the annual Sharpe ratio times the square root of years. <bookmark mark='a'/> At five years, the rough standard error of an estimated annual Sharpe ratio is forty-five hundredths. Reaching a t-statistic of two would require about point eight nine. These are fixed arithmetic illustrations, not results from the sealed sample. <bookmark mark='b'/> Serial dependence, tails and selection can make the approximation unreliable; failure to reject zero is not evidence that two strategies are equivalent.") as vo:
            self.play(FadeIn(eq),FadeIn(gauge))
            self.play(years.animate.set_value(5.0),run_time=4.0)
            vo.wait_until('a')
            self.play(Indicate(gauge.readouts[1],color=WHITE,scale_factor=1.08))
            self.play(Indicate(gauge.readouts[2],color=QC.LOSS,scale_factor=1.08))
            vo.wait_until('b');self.play(FadeIn(foot))
        self.clear_scene()

    def trials(self):
        cards=VGroup(
            desk_question(r"local accounting",r"zero new market trials, registrations or scores in this review",width=12.0,font_size=22),
            desk_question(r"the broader search",r"a published factor may inherit many choices: universes, signals, lags, weights and samples",width=12.0,font_size=22),
            desk_question(r"a fresh holdout",r"requires genuine prior separation and a prespecified evaluation; a familiar published history cannot be made fresh by renaming it",width=12.0,font_size=22),
        ).arrange(DOWN,buff=0.3)
        with self.voiceover("A trial ledger records what a process actually tried. <bookmark mark='a'/> This review adds no market trials, registrations or scores. <bookmark mark='b'/> That does not mean the published factors arrived without selection. Their authors and later users may have examined many universes, signals, lags, weights and samples. <bookmark mark='c'/> A fresh holdout requires genuine separation and a prespecified evaluation. Renaming familiar history cannot create one. Part twenty-five studies the wider search.") as vo:
            for i,mk in enumerate(('a','b','c')):
                if i:vo.wait_until(mk)
                self.play(FadeIn(cards[i],shift=UP*0.2))
        self.clear_scene()

    def boundary(self):
        head=label(r"The experiment remains unopened in this review",font_size=33,color=QC.HOUSE).to_edge(UP,buff=0.7)
        text=wrapped_label(r"The original envelope computation is preserved but excluded. No experiment cache, payload, performance row or substitute historical test is used here. Named public data files may contain later published observations; that is separate from opening the sealed experiment.",12.0,24,GREY_A).next_to(head,DOWN,buff=0.7)
        question=ask(r"A registered strategy has an estimated Sharpe ratio of 0.4 after five years. Under the stated approximation, what is its t-statistic, and what can that establish?")
        with self.voiceover("The boundary is explicit. The original envelope computation is preserved and excluded from this review. No experiment payload, cache or performance row is accessed, and no substitute historical test is created. Named public data files can contain later published observations; that is a different access path, and it does not certify a blind experiment. <bookmark mark='a'/> Pause and predict. A registered strategy has an estimated Sharpe ratio of point four after five years. Under the stated approximation its t-statistic is about point eight nine. What can that establish, given selection, costs and the short sample?") as vo:
            self.play(FadeIn(head),FadeIn(text));vo.wait_until('a');self.play(FadeIn(question))
        self.clear_scene()
