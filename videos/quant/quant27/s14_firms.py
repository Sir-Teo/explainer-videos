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
        c = chapter_card(13, r"From the public record: Two Sigma and Renaissance",
                         r"What do the most successful model shops show, and hide?", lit=(1982, 2001), part=PART)
        with self.voiceover("Chapter thirteen. Two firms that run on models, as far as the public record shows them."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def renaissance(self):
        card = firm_card(r"Renaissance Technologies", r"founded in 1982 by the mathematician James Simons; its Medallion "
                         r"fund, open only to employees since 2005, trades short-horizon statistical patterns across many "
                         r"markets with very high turnover. Its methods are not public; its returns were reconstructed by "
                         r"the journalist Gregory Zuckerman",
                         numbers=((r"66.1\%", r"Medallion's average annual return before fees, 1988--2018"),
                                  (r"39.1\%", r"after fees")),
                         source=r"Zuckerman, \textit{The Man Who Solved the Market} (2019)", width=10.6, font_size=22)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Renaissance Technologies was founded in 1982 by James Simons, a mathematician who had broken codes for the "
            "American government. <bookmark mark='a'/> Its Medallion fund, open only to its own employees since 2005, "
            "trades short-horizon statistical patterns across many markets. According to Gregory Zuckerman's history of "
            "the firm, it returned an average of sixty-six percent a year before fees from 1988 to 2018, and "
            "thirty-nine percent after them, the best long record in the public domain. <bookmark mark='b'/> What it "
            "learned and how is not public. What is public is the shape: many small, weak signals, short horizons, "
            "enormous breadth, and a fund kept small enough that its own trading does not destroy the patterns."
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
                         r"itself as a technology company that invests. Run since September 2024 by co-chief executives, "
                         r"with the founders as co-chairmen",
                         numbers=((r"\approx\$70\,\text{bn}", r"assets under management, 2025 (reported)"),
                                  (r"2001", r"founded")),
                         source=r"company disclosures and press reports", width=10.6, font_size=22)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Two Sigma was founded in 2001 by David Siegel and John Overdeck, who had met at the quantitative firm D. E. "
            "Shaw, as a bet that data science and engineering could find value in the world's data. It manages around "
            "seventy billion dollars, by reported figures, and describes itself as a technology company that invests. "
            "<bookmark mark='a'/> Where Renaissance is a closed fund, Two Sigma is a large organisation of researchers "
            "and engineers producing many models: which makes the next part of its public record the more instructive."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def governance(self):
        card = crisis_card(r"16 January 2025", r"The SEC and Two Sigma's models",
                           r"the SEC found that Two Sigma had known since March 2019 of vulnerabilities in the investment "
                           r"models behind some of its funds, did not address them until August 2023, and failed to "
                           r"supervise an employee who made unauthorised changes to more than a dozen models. The firm "
                           r"settled without admitting or denying the findings; criminal charges against the individual "
                           r"are allegations, not findings",
                           stats=((r"\$90\,\text{m}", r"civil penalties"),
                                  (r"\$165\,\text{m}", r"repaid to affected funds and accounts, voluntarily")),
                           width=10.6, font_size=22)
        card.move_to(ORIGIN)
        src = note(r"SEC press release 2025-15 (16 January 2025)", font_size=16, color=GREY_C).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In January 2025 the Securities and Exchange Commission settled charges against two Two Sigma advisers. "
            "<bookmark mark='a'/> It found that the firm had known since March 2019 of weaknesses in the models behind "
            "some of its funds, had not fixed them until August 2023, and had failed to supervise an employee who made "
            "unauthorised changes to more than a dozen models. Two Sigma paid ninety million dollars without admitting "
            "or denying the findings, and had already repaid a hundred and sixty-five million to the affected funds. "
            "Charges against the individual are, so far, allegations. <bookmark mark='b'/> The lesson is not about one "
            "firm. In a model shop, the model is the product, and who may change its parameters, and how anyone would "
            "know, is as much a part of it as the mathematics."
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
            desk_question(r"breadth beats brilliance", r"the public shape of both firms is many weak signals traded across "
                          r"many assets: chapter 1's arithmetic, at industrial scale", width=12.2, font_size=20),
            desk_question(r"capacity is the constraint", r"a short-horizon edge is small per trade and shrinks with size; "
                          r"Medallion is kept small for that reason", width=12.2, font_size=20),
            desk_question(r"models are code under control", r"versioned, reviewed, changed only through a process that "
                          r"someone other than their author approves: Part 20's London Whale and this case agree",
                          width=12.2, font_size=20),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three lessons from the record. <bookmark mark='a'/> Breadth beats brilliance: both firms' public shape is "
            "many weak signals across many assets, the arithmetic of chapter one at industrial scale. "
            "<bookmark mark='b'/> Capacity is the constraint: a short-horizon edge is small per trade and shrinks with "
            "size. <bookmark mark='c'/> And models are code under control: versioned, reviewed, and changed only through "
            "a process someone other than their author approves. Part twenty's London Whale and this case teach the "
            "same thing from opposite ends."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"a fund earns 39\% a year after fees but cannot take new money. Why might its managers prefer that to "
                r"growing, and what does it tell you about the strategy's capacity?")
        with self.voiceover(
            "Pause and predict. A fund earns thirty-nine percent a year after fees, and refuses new money. Why might its "
            "managers prefer that to growing, and what does it tell you about the strategy's capacity?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
