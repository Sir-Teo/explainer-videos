from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant28.common import BAD, GOOD, HURDLE, PART, WORD, comma, fit_right, load


def _yr(d):
    d = np.asarray(d)
    return d // 10000 + ((d // 100) % 100 - 0.5) / 12


class FOMC(VoiceoverScene):
    def construct(self):
        f = load("form")
        self.card()
        self.documents()
        self.hmp()
        self.dissent()
        self.more_papers()
        self.minutes(f)
        self.question()

    def card(self):
        c = chapter_card(7, r"Inside the FOMC: transparency and deliberation", r"Does publishing the words change the "
                         r"words?", part=PART)
        with self.voiceover("Chapter seven. Text is not only an input to trading; it is evidence about how decisions are "
                            "made. And when the people speaking know they will be read, do they speak differently?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def documents(self):
        rows = VGroup()
        items = [(r"statement", r"the decision and the outlook, released at the end of the meeting", r"since 1994"),
                 (r"minutes", r"a summary of the discussion, unattributed; three weeks after the meeting since January "
                              r"2005, after the next meeting before", r"for decades"),
                 (r"transcripts", r"every word, attributed, released with a five-year lag", r"from the 1970s tapes"),
                 (r"press conference", r"the chair answers questions after the statement", r"since April 2011"),
                 (r"projections", r"each participant's forecasts and the `dot plot' of rate paths", r"since 2007, dots 2012")]
        for name, what, since in items:
            r_ = VGroup(label(name, font_size=24, color=WORD), wrapped_label(what, 7.2, 18, GREY_A),
                        label(since, font_size=18, color=GREY_B))
            r_[0].move_to([-5.0, 0, 0]).align_to(np.array([-6.3, 0, 0]), LEFT)
            r_[1].move_to([0.6, 0, 0])
            r_[2].move_to([5.6, 0, 0])
            rows.add(r_)
        rows.arrange(DOWN, buff=0.42).move_to(DOWN * 0.1)
        head = label(r"what the committee publishes", font_size=30).to_edge(UP, buff=0.5)
        with self.voiceover(
            "The committee speaks through several documents. <bookmark mark='a'/> The statement, since 1994. The "
            "minutes, a summary of the discussion without names, published three weeks after each meeting since "
            "January 2005. <bookmark mark='b'/> The transcripts: every word, with names, released five years later. "
            "And since 2007 the participants' own projections, since 2011 a press conference. <bookmark mark='c'/> "
            "Each is a different text, written for a different reader, at a different delay."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]), FadeIn(rows[4]))
            vo.wait_until("c")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def hmp(self):
        card = firm_card(r"Hansen, McMahon and Prat (2018)", r"`Transparency and deliberation within the FOMC': the "
                         r"meetings were taped from the 1970s to help write the minutes, and members believed the tapes "
                         r"were erased. In October 1993 Greenspan revealed that transcripts existed; the Fed agreed to "
                         r"release them with a five-year lag. A natural experiment in being read",
                         numbers=((r"\text{LDA}", r"topic shares of every speaker's words, before and after"),
                                  (r"+", r"discipline: less experienced members came better prepared, with more data"),
                                  (r"-", r"conformity: and stayed closer to the chair's line"),
                                  (r"\checkmark", r"on net, deliberation became more informative")),
                         source=r"\textit{Quarterly Journal of Economics} 133 (2018)", kind=r"Paper file", width=10.6,
                         font_size=21).move_to(ORIGIN)
        with self.voiceover(
            "That makes a natural experiment. <bookmark mark='a'/> The meetings had been taped since the 1970s to help "
            "write the minutes, and members believed the tapes were erased afterwards. In October 1993 Alan Greenspan "
            "revealed that the transcripts existed, and the Fed agreed to publish them with a five-year lag. Overnight, "
            "every member knew their words would be read. <bookmark mark='b'/> Stephen Hansen, Michael McMahon and "
            "Andrea Prat ran a topic model over every speaker's words before and after. They found two effects. "
            "Discipline: less experienced members came better prepared, with more data. Conformity: they also stayed "
            "closer to the chair's line. On balance, the debate became more informative."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def dissent(self):
        rows = [cmath(r"\text{discipline}", r":", r"\text{being read makes members work harder: better arguments}", font_size=30,
                      colors={r"\text{discipline}": GOOD}),
                cmath(r"\text{conformity}", r":", r"\text{being read makes members fear looking wrong: fewer dissents}",
                      font_size=30, colors={r"\text{conformity}": BAD}),
                cmath(r"\text{text}", r"\Rightarrow", r"\text{measure both, speaker by speaker}", font_size=30)]
        whys = [why(r"career-concerns theory: an expert who knows she will be evaluated puts in more effort"),
                why(r"the same theory: she also herds toward the view an informed observer expects. Meade and Stasavage "
                    r"(2008) found that the probability of dissent at the FOMC fell after 1993"),
                why(r"before text as data, only votes could be counted; topic models let Hansen, McMahon and Prat measure "
                    r"what each member talked about, and how")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Theory predicted both effects. <bookmark mark='a'/> An expert who knows they will be judged works harder: "
            "discipline. <bookmark mark='b'/> The same expert also fears looking wrong, and drifts toward the view an "
            "observer expects: conformity. Ellen Meade and David Stasavage had already shown that dissents at the FOMC "
            "became rarer after 1993. <bookmark mark='c'/> But votes are a crude record. Text lets you measure what "
            "each member said, and how, which is what turned an old question in the economics of committees into a "
            "measurement."
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


    def more_papers(self):
        cards = VGroup(
            desk_question(r"Shapiro and Wilson (2022)", r"the sentiment of FOMC transcripts, minutes and speeches, read against the economy, reveals what the committee was trying to achieve: its objectives estimated from its own words", width=12.4, font_size=19),
            desk_question(r"Gorodnichenko, Pham and Talavera (2023), `The voice of monetary policy'", r"the emotion in the chair's voice at press conferences, measured by a neural network, moves stock prices and exchange rates beyond what the words say", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Two more papers read the committee itself. <bookmark mark='a'/> Adam Shapiro and Daniel Wilson used the tone "
            "of transcripts, minutes and speeches to estimate what the committee was actually aiming for: its objectives "
            "inferred from its own words. <bookmark mark='b'/> And Yuriy Gorodnichenko, Tho Pham and Oleksandr Talavera "
            "measured the emotion in the chair's voice at press conferences: tone of voice moves markets beyond the text."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, mk in enumerate(('a', 'b')):
                vo.wait_until(mk)
                if k > 0:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()


    def minutes(self, f):
        x = _yr(f["min_dates"])
        w = np.asarray(f["min_words"], float)
        top = float(np.ceil(w.max() / 2000) * 2000)
        g = axes([1996, 2021], [0, top], x_length=9.0, y_length=4.2, xlabel=r"", ylabel=r"words in the minutes' discussion",
                 xticks=[2000, 2005, 2010, 2015, 2020], yticks=[0, top / 2, top], font_size=15).move_to(LEFT * 0.8 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup(*[Line(ax.c2p(a, 0), ax.c2p(a, b), color=WORD, stroke_width=2.4) for a, b in zip(x, w)])
        mark = DashedLine(ax.c2p(2005.0, 0), ax.c2p(2005.0, top), color=HURDLE)
        tag = label(r"2005: minutes released three weeks after the meeting", font_size=22, color=HURDLE).to_edge(UP, buff=0.5)
        early = float(np.median(w[x < 2005]))
        late = float(np.median(w[x >= 2009]))
        side = wrapped_label(rf"median {comma(early)} words before 2005; {comma(late)} since 2009", 3.2, 17,
                             GREY_A).to_edge(RIGHT, buff=0.35).shift(UP * 1.2)
        fit_right(side)
        with self.voiceover(
            "Our own corpus shows the minutes changing too. <bookmark mark='a'/> Each bar is one set of minutes, "
            "counting only the paragraphs of discussion. <bookmark mark='b'/> From 2005 the minutes arrived three weeks "
            "after the meeting rather than after the next one, and became a market-moving document in their own right. "
            f"The median grew from about {early:,.0f} words before 2005 to about {late:,.0f} since 2009. When a "
            "chart compares eras with different policy topics and regimes, and does not isolate an effect of the publication rule."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.01), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(mark), FadeIn(tag), FadeIn(side))
        self.add(wrapped_label(r"Descriptive era comparison; publication rules, policy regimes and topics change together", 11.8, 18, GREY_B).to_edge(DOWN, buff=0.3))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a model trained on minutes from before 2005 is used on minutes after. Why might its scores "
                       r"drift even if nothing about the economy changed?")
        with self.voiceover(
            "Pause and predict. A model trained on minutes from before 2005 is used on minutes written after. Why might "
            "its scores drift, even if nothing about the economy changed?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
