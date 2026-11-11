from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant27.common import PART, ask


class Firms(VoiceoverScene):
    def construct(self):
        self.card()
        self.renaissance()
        self.twosigma()
        self.governance()
        self.lessons()
        self.question()

    def card(self):
        c = chapter_card(14, r"From the public record: Two Sigma and Renaissance",
                         r"What do the most successful model shops show, and hide?", lit=(1982, 2001), part=PART)
        with self.voiceover("Chapter fourteen. Two firms that run on models, as far as the public record shows them."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def renaissance(self):
        card = firm_card(r"Renaissance Technologies", r"founded in 1982 by the mathematician James Simons; its Medallion "
                         r"fund became restricted to insiders after outside capital was returned; the historical account describes short-horizon trading across many "
                         r"markets with very high turnover. Its methods are not public; its returns were reconstructed by "
                         r"the journalist Gregory Zuckerman",
                         numbers=((r"66.1\%", r"reported annual average before fees, 1988--2018"),
                                  (r"39.1\%", r"reported annual average after fees")),
                         source=r"Zuckerman, \textit{The Man Who Solved the Market} (2019)", width=10.6, font_size=26)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Renaissance Technologies was founded in 1982 by James Simons. <bookmark mark='a'/> Gregory Zuckerman's 2019 history reports Medallion's annual averages from 1988 through 2018 at about sixty-six percent before fees and thirty-nine percent after fees. Access became restricted to insiders after outside capital was returned. These are reported historical averages from that account, not an audited current offering or a return available to a new investor. <bookmark mark='b'/> Its proprietary models and signal construction are not public. The history can motivate questions about breadth, turnover and capacity, but it cannot establish which machine-learning architecture or causal mechanism produced the record."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def twosigma(self):
        card = firm_card(r"Two Sigma", r"founded in 2001 by David Siegel and John Overdeck, who had met at D.~E.~Shaw, "
                         r"as a bet that data science and engineering could find value in the world's data; it describes "
                         r"itself as a technology company that invests. This source-dated account does not assert current assets, leadership or proprietary model details; "
                         r"the focus is research infrastructure and model controls",
                         numbers=((r"2001", r"founding year"),
                                  (r"2025", r"dated SEC enforcement source")),
                         source=r"company disclosures and press reports", width=10.6, font_size=26)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Two Sigma was co-founded in 2001 and describes an investment process built around data, research and engineering. Its public identity does not reveal its current proprietary signals or their contribution to returns. <bookmark mark='a'/> The useful comparison here is organisational: many models require a reproducible chain from data and code to positions, with records of who can change a model and how those changes are detected. The next source provides a dated example of failures in that chain."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def governance(self):
        card = crisis_card(r"16 January 2025", r"The SEC and Two Sigma's models",
                           'The SEC order found known model vulnerabilities in or before March 2019, delayed remediation until August 2023, and failures to supervise unauthorised model changes. The firm settlement also covered separate whistleblower-protection violations; it did not admit or deny the findings.',
                           stats=((r"\$90\,\text{m}", r"civil penalties"),
                                  (r"\$165\,\text{m}", r"repaid to affected funds and accounts, voluntarily")),
                           width=10.6, font_size=26)
        card.move_to(ORIGIN)
        src = note(r"SEC press release 2025-15 (16 January 2025)", font_size=20, color=GREY_C).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "On January sixteenth, 2025, the SEC announced settled charges against Two Sigma Investments and Two Sigma Advisers. <bookmark mark='a'/> According to its order, employees recognised model vulnerabilities in or before March 2019, but the firm waited until August 2023 to address them and failed to supervise an employee's unauthorised changes to more than a dozen models. The advisers agreed to ninety million dollars in total penalties, without admitting or denying the findings, and voluntarily repaid affected funds and accounts 165 million dollars. The settlement also included separate whistleblower-protection violations. <bookmark mark='b'/> This is a dated account of the firm settlement, not a statement about the current status of separate proceedings. It shows why recorded model changes, access controls, review and prompt remediation belong in an investment process."
        ) as vo:
            self.play(FadeIn(card), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[Indicate(s_, color=QC.CRISIS) for s_ in card.stats], lag_ratio=0.5))
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"measure economic breadth", r"separate nominal signal counts from common exposures and correlated strategy returns", width=12.2, font_size=30),
            desk_question(r"measure performance at scale", r"turnover, impact, access and capital affect implementation; fund closure alone does not identify capacity", width=12.2, font_size=30),
            desk_question(r"models are code under control", r"versioned, reviewed, changed only through a process that "
                          r"someone other than their author approves: Part 20's London Whale and this case agree",
                          width=12.2, font_size=30),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three protocol lessons can be drawn without pretending to know a proprietary strategy. <bookmark mark='a'/> Ask how many economically distinct exposures support a reported result, and which common risks make nominal breadth redundant. <bookmark mark='b'/> Ask how turnover, market impact, access restrictions and capital affect what can be earned at a particular scale. A closed fund alone does not identify its capacity limit. <bookmark mark='c'/> And preserve an auditable chain of model versions, reviews and authorised changes. These are questions to investigate and controls to implement; the public histories do not prove a universal recipe for exceptional returns."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"a historical account reports high returns and a fund declines new money. Which capacity explanation is plausible, what alternatives remain, and what evidence could distinguish them?")
        with self.voiceover(
            'Pause and predict. A historical account reports high after-fee returns and a fund declines new capital. What capacity explanation is plausible, what other explanations remain possible, and what evidence would distinguish them?'
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
