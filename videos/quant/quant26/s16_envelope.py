"""Conceptual evaluation protocol; no experiment payload or score is accessed."""
from __future__ import annotations
from explainer.quant import *  # noqa: F403
from explainer.quant.house import pit
from videos.quant.quant26.common import PART, ask, comma

class Envelope(VoiceoverScene):
    def construct(self):
        self.card()
        self.freeze()
        self.accounting()
        self.precision()
        self.boundary()

    def card(self):
        c=chapter_card(15,r"Registration and evaluation accounting",r"What would a fresh strategy test require?",part=PART)
        with self.voiceover("Chapter fifteen. Registration and evaluation accounting. This review preserves the original experiment code but excludes its cache, payload and score. We examine the conditions a fresh test would need."):
            self.play(FadeIn(c[0],shift=UP*.2),FadeIn(c[1]))
        self.play(FadeOut(c))

    def freeze(self):
        cards=VGroup(
            desk_question(r"freeze the trading rule",r"code hash, parameters, signal and execution timestamps, universe and data vintages",width=12,font_size=21),
            desk_question(r"freeze the implementation",r"spread, impact, borrow, financing, corporate actions, constraints and capital base",width=12,font_size=21),
            desk_question(r"freeze the evaluation",r"window, benchmark, statistic, uncertainty calculation, stopping rule and all variants considered",width=12,font_size=21),
        ).arrange(DOWN,buff=.28)
        with self.voiceover("A defensible test begins before its outcomes are inspected. <bookmark mark='a'/> Freeze the rule, its code hash, parameters, signal and execution timestamps, universe and publication vintages. <bookmark mark='b'/> Freeze trading, borrow and financing assumptions and the capital base. <bookmark mark='c'/> Freeze the evaluation window, benchmark, uncertainty calculation and stopping rule. Record every variant considered. A timestamp cannot make an already examined sample unseen.") as vo:
            for i,mk in enumerate(('a','b','c')):
                if i:vo.wait_until(mk)
                self.play(FadeIn(cards[i],shift=UP*.2))
        self.clear_scene()

    def accounting(self):
        n=pit.trials_upto(PART)
        count=MathTex(rf"\text{{existing cumulative registrations through Part 26}}:\ {comma(n)}",font_size=30).to_edge(UP,buff=.7)
        if count.width>12.3:count.scale_to_fit_width(12.3)
        cards=VGroup(
            desk_question(r"this visual review",r"zero new registrations, market trials, sealed openings or scores",width=12,font_size=22),
            desk_question(r"the broader search",r"registered trials are a recorded lower bound; informal variants and adaptive research also select results",width=12,font_size=22),
        ).arrange(DOWN,buff=.35).next_to(count,DOWN,buff=.6)
        with self.voiceover(f"The existing cumulative ledger through Part twenty-six contains {n:,} registered trials. That is existing metadata, not a new registration by this review. <bookmark mark='a'/> This review adds no market trials, registrations, sealed openings or scores. <bookmark mark='b'/> A recorded count is a lower bound on the broader research search. Informal variants and adaptive decisions can matter even when no separate registration was made.") as vo:
            self.play(FadeIn(count));vo.wait_until('a');self.play(FadeIn(cards[0]));vo.wait_until('b');self.play(FadeIn(cards[1]))
        self.clear_scene()

    def precision(self):
        eq=MathTex(r"t\approx SR_{\rm annual}\sqrt{Y},\qquad {\rm se}(\widehat{SR}_{\rm annual})\approx Y^{-1/2}",font_size=35).to_edge(UP,buff=.45)
        # the same arithmetic as a picture; the green dot is the illustrative estimate of 0.4 and its t-statistic
        years=ValueTracker(1.0)
        gauge=SharpePrecision(years,alt=0.4,mark=0.4).next_to(eq,DOWN,buff=.4)
        foot=wrapped_label(r"Stable IID, modest-Sharpe approximation only. Dependence, tails, selection and costs can change the uncertainty or economic conclusion. No realised experiment result is displayed.",12,21,GREY_A).to_edge(DOWN,buff=.35)
        with self.voiceover("Five years can still be a noisy test. Under an independent, stable, modest-Sharpe approximation, the mean t-statistic is the annual Sharpe ratio times the square root of years. <bookmark mark='a'/> At five years, the rough standard error is point four five. A fixed illustrative Sharpe ratio of point four gives a t-statistic near point eight nine. These numbers are arithmetic examples, not a sealed outcome. <bookmark mark='b'/> Dependence, tails, selection and costs can change the conclusion. Nonrejection of zero does not establish equivalence or absence of an economic effect.") as vo:
            self.play(FadeIn(eq),FadeIn(gauge))
            self.play(years.animate.set_value(5.0),run_time=4.0)
            vo.wait_until('a')
            self.play(Indicate(gauge.readouts[1],color=WHITE,scale_factor=1.08))
            self.play(Indicate(gauge.readouts[4],color=QC.GAIN,scale_factor=1.08))
            vo.wait_until('b');self.play(FadeIn(foot))
        self.clear_scene()

    def boundary(self):
        head=label(r"The experiment remains unopened in this review",font_size=33,color=QC.HOUSE).to_edge(UP,buff=.65)
        text=wrapped_label(r"Original experiment code is preserved and excluded. No experiment cache, payload, result row or substitute historical test is used. Public archive vintages may contain later observations; this is distinct from accessing the sealed experiment.",12,24,GREY_A).next_to(head,DOWN,buff=.6)
        question=ask(r"A prespecified test has $t\approx0.89$ after five years. What does nonrejection establish, and what still depends on costs, selection and uncertainty?")
        with self.voiceover("The boundary is explicit. Original experiment code is preserved but excluded. No experiment cache, payload, performance row or substitute historical strategy test is used. Public archive readers can retrieve later published observations before their historical cut; that does not certify a blind test. <bookmark mark='a'/> Pause and predict. A prespecified test has a t-statistic near point eight nine after five years. What does nonrejection establish, and what remains uncertain about costs, selection and future performance?") as vo:
            self.play(FadeIn(head),FadeIn(text));vo.wait_until('a');self.play(FadeIn(question))
        self.clear_scene()
