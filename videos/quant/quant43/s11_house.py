from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant43.common import ladder
from explainer.quant.house import skill as SK
from videos.quant.quant43.common import (ACT_C, BAD, COST_C, GOOD, HURDLE, LUCK_C, MKT_C, PART, REC_C, SKILL_C,
                                         comma, house_lab, load)


class House(VoiceoverScene):
    def construct(self):
        self.answer()
        self.card()
        self.last_report()
        self.rules()
        self.policy()
        self.complete()
        self.advice()
        self.lab()
        self.module()
        self.test()

    def answer(self):
        rows=[cmath(r"\text{benchmark}",r":",r"\text{a justified default for the mandate}",font_size=38),
              cmath(r"\text{candidate change}",r":",r"\text{burden of evidence after costs, risk and selection}",font_size=34),
              cmath(r"\text{capital decision}",r":",r"\text{uncertainty, constraints and independent risk review}",font_size=34)]
        whys=[why(r"a market index is a teaching benchmark, not a universal portfolio for every liability"),
              why(r"registration and a test window support evaluation; they do not guarantee skill"),
              why(r"no capital allocation or deployment approval follows from this presentation")]
        step=ladder(self,rows,whys,keep=3,top=2.6,x=0,buff=.6)
        with self.voiceover(
            "The last rule, stated as proposed governance. <bookmark mark='a'/> Choose a defensible benchmark for "
            "the mandate. An index is the teaching default here, rather than a universal answer for every liability. "
            "<bookmark mark='b'/> Put the burden of evidence on a candidate change, after costs, risk and selection. "
            "<bookmark mark='c'/> A capital decision must also reflect uncertainty, constraints and independent risk "
            "review. This lecture does not approve a strategy, a sleeve or a deployment."
        ) as vo:
            step(0)
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:step(k)
        self.clear_scene()

    def last_report(self):
        lines=VGroup(
            label(r"A proposed cross-desk review",font_size=28,color=QC.HOUSE),
            wrapped_label(r"risk: forecasts, validation evidence, assumptions and model limitations",11.6,22),
            wrapped_label(r"treasury: funding, margin, collateral and liquidity stresses",11.6,22),
            wrapped_label(r"agents: interactions, copies, deviations and regime changes",11.6,22),
            wrapped_label(r"research: prospective protocol, selection and complete reporting",11.6,22),
            wrapped_label(r"portfolio: mandate, benchmark, costs and justified risk budget",11.6,22)
        ).arrange(DOWN,aligned_edge=LEFT,buff=.3)
        with self.voiceover(
            "A proposed cross-desk review. <bookmark mark='a'/> Risk reports validation, assumptions and limitations. "
            "<bookmark mark='b'/> Treasury examines funding, collateral, margin and liquidity stresses. "
            "<bookmark mark='c'/> Agents are examined in interaction, including copies and deviations. "
            "<bookmark mark='d'/> Research reports its prospective design and all planned results. "
            "<bookmark mark='e'/> Portfolio decisions require a mandate, benchmark, costs and a justified risk budget. "
            "These are review responsibilities, not claims that every test has been passed."
        ) as vo:
            self.play(FadeIn(lines[0]),FadeIn(lines[1]))
            for k,mark in enumerate(('a','b','c','d','e')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(lines[k+1],shift=RIGHT*.2))
        self.clear_scene()

    def card(self):
        c = chapter_card(10, r"Rule 43: the market is the default", r"After forty-three parts, how should the House invest?",
                         part=PART)
        with self.voiceover("Chapter ten. The forty-third rule belongs to the whole House, and it is the one every other "
                            "rule was building toward: the burden of proof is on the strategy, not on the market."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def rules(self):
        items = [(r"Rule 1", r"point in time: nothing is known before it was known"),
                 (r"Rule 14", r"a new model is adopted only if it beats the simpler one out of sample"),
                 (r"Rule 26", r"the backtest protocol: register, count every trial, deflate"),
                 (r"Rule 40", r"a risk number is a forecast, reported with its backtest"),
                 (r"Rule 41", r"survive the margin call you have not been sent"),
                 (r"Rule 42", r"test the agent against the market it creates"),
                 (r"Rule 43", r"the market is the default; the record must argue otherwise")]
        rows = VGroup(*[VGroup(label(a_, font_size=21, color=REC_C if a_ != "Rule 43" else SKILL_C),
                               label(b_, font_size=19, color=GREY_A)).arrange(RIGHT, buff=0.4) for a_, b_ in items])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(ORIGIN)
        with self.voiceover(
            "Some of the rules that got the House here. <bookmark mark='a'/> The first: point in time. "
            "<bookmark mark='b'/> A new model must beat the simpler one out of sample. <bookmark mark='c'/> The "
            "backtest protocol: register, count, deflate. <bookmark mark='d'/> A risk number is a forecast; survive the "
            "margin call you have not been sent; test the agent against the market it creates. "
            "<bookmark mark='e'/> And the last: the market is the default."
        ) as vo:
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[3:6]], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(rows[6], shift=RIGHT * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def policy(self):
        rows=[cmath(r"\text{benchmark}",r":",r"\text{match liabilities, horizon and constraints}",font_size=36),
              cmath(r"\text{research candidate}",r":",r"\text{document hypothesis and independent evaluation}",font_size=32),
              cmath(r"\text{risk budget}",r":",r"\text{account for uncertainty and implementation}",font_size=34),
              cmath(r"\text{controls}",r":",r"\text{liquidity, concentration and interaction limits}",font_size=34)]
        whys=[why(r"index cost is relevant when an investable market benchmark matches the mandate"),
              why(r"a published factor label alone does not establish a portfolio's future return"),
              why(r"an estimated alpha is not a certain cash flow"),
              why(r"model validation and operational approval are separate responsibilities")]
        step=ladder(self,rows,whys,keep=4,top=2.8,x=0,buff=.5)
        with self.voiceover(
            "A policy template for the teaching House. <bookmark mark='a'/> Match the benchmark to the mandate. "
            "<bookmark mark='b'/> Treat any proposed active rule as a research candidate requiring evidence, including "
            "a mix of published factors. <bookmark mark='c'/> Build the risk budget around uncertainty and actual "
            "implementation. <bookmark mark='d'/> Apply liquidity, concentration and interaction controls. This is a "
            "template for decisions, not a report of executed positions or an allocation justified by sealed outcomes."
        ) as vo:
            step(0)
            for k,mark in enumerate(('a','b','c','d')):
                vo.wait_until(mark)
                if k:step(k)
        self.clear_scene()

    def complete(self):
        chart = house_chart(PART, lit=tuple(DESKS.keys()))
        with self.voiceover(
            "The House, complete. Data and technology across the top; the trading desks, from volatility and rates to "
            "credit, macro and digital assets; research, portfolio and risk, execution and market making; and "
            "treasury and compliance underneath. Forty-three parts ago it was an empty building and a sealed envelope."
        ):
            self.play(FadeIn(chart))
            self.wait(2)
        self.clear_scene()

    def advice(self):
        cards = VGroup(
            desk_question(r"to a new analyst", r"write down the test before you run it; count what you try; keep the "
                          r"last years sealed; report the costs", width=12.4, font_size=19),
            desk_question(r"to a portfolio manager", r"choose a mandate-consistent benchmark; assess independent "
                          r"evidence and implementation; know who is on the other side", width=12.4, font_size=19),
            desk_question(r"to a researcher", r"prove what you claim, then check it on data the proof never saw; and "
                          r"publish the null results", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What the House would tell the people who join it. <bookmark mark='a'/> To a new analyst: write down the "
            "test before you run it, count what you try, keep the last years sealed, and report the costs. "
            "<bookmark mark='b'/> To a portfolio manager: choose a mandate-consistent benchmark, examine independent "
            "evidence and implementation, and know who is on the other side. <bookmark mark='c'/> And to a researcher: prove what you "
            "claim, check it on data the proof never saw, and publish the null results."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"Counting skill without finding it", SK.storey_pi0, "p = np.asarray(p, float)", 2,
                         extra=((SK.bsw, "pi0 = storey_pi0(p, lam)", 6),), width=10.6)
        with self.voiceover(
            "The House's code for Chapter two. Storey's estimate is two lines: the share of p-values above lambda, "
            "scaled up and capped at one. The component shares then use a positive-part tail subtraction. Those guards "
            "do not inherit the uncapped expectation proof; Chapter R states the distinction."
        ):
            self.play(FadeIn(card))
        self.wait(0.5)
        self.clear_scene()

    def module(self):
        chart=house_chart(PART,lit=('research','portfolio','compliance')).scale(.62).to_edge(UP,buff=.2)
        pairs=[(r"\texttt{beat\_prob}, \texttt{fund\_population}",r"stylised luck examples"),
               (r"\texttt{storey\_pi0}, \texttt{bsw}, \texttt{berk\_green}",r"estimators and allocation model"),
               (r"\texttt{rolling\_autocorr}, \texttt{variance\_ratio}",r"descriptive sample statistics")]
        tab=VGroup()
        for i,(left,right)in enumerate(pairs):
            a=label(left,font_size=16,color=QC.HOUSE);b=label(right,font_size=16,color=GREY_A)
            if a.width>6:a.scale_to_fit_width(6)
            if b.width>5.4:b.scale_to_fit_width(5.4)
            a.move_to([-3.4,-.8-.37*i,0]);b.move_to([3.3,-.8-.37*i,0]);tab.add(VGroup(a,b))
        rule=wrapped_label(r"Proposed Rule 43: justify the benchmark; require independent net evidence for a change; "
                           r"apply risk and implementation review before capital decisions.",12.4,19,QC.HOUSE).to_edge(DOWN,buff=.3)
        with self.voiceover(
            "The ordinary skill-module tools used here. <bookmark mark='a'/> Stylised luck calculations, estimators, "
            "an allocation model and descriptive sample statistics. Their names do not certify empirical skill. "
            "<bookmark mark='b'/> Proposed Rule forty-three: justify the benchmark, require independent net evidence "
            "for a change, and review risk and implementation before allocating capital."
        ) as vo:
            self.play(FadeIn(chart),FadeIn(tab[0]))
            vo.wait_until('a');self.play(FadeIn(tab[1]),FadeIn(tab[2]))
            vo.wait_until('b');self.play(FadeIn(rule))
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"a fund that beat the market for five years", r"ask how many funds tried, what luck alone "
                          r"would give, and whether its record was registered before it was run (Chapter 2)", width=12.0,
                          font_size=19),
            desk_question(r"a manager with real skill", r"ask who receives it: the manager, through size and fees, or "
                          r"you (Chapter 3)", width=12.0, font_size=19),
            desk_question(r"a strategy that worked for decades", r"ask whether the market that paid it still exists "
                          r"(Chapter 4), and how an independent evaluation would test it (Chapter 5)", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three last tests to carry away. <bookmark mark='a'/> When a fund beat the market for five years, ask how "
            "many tried, what luck alone would give, and whether its record was registered before it was run. "
            "<bookmark mark='b'/> When a manager has real skill, ask who receives it. <bookmark mark='c'/> And when a "
            "strategy worked for decades, examine whether its mechanism persists and how an independent evaluation would test it."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
