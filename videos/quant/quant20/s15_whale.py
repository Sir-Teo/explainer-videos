from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, PART, RISKY, ask, fit_right, illustration, load


class Whale(VoiceoverScene):
    def construct(self):
        self.card()
        self.case()
        self.var()
        self.lessons()

    def card(self):
        c = chapter_card(14, r"2012: the London Whale", r"How does a hedge become the risk?", lit=(2012,), part=PART)
        with self.voiceover("Chapter fourteen. 2012, the London Whale: when a credit hedge became the bank's largest "
                            "risk."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def case(self):
        cc = crisis_card(r"January--May 2012", r"J.P. Morgan's Chief Investment Office",
                         r"the CIO's synthetic credit portfolio, meant as a hedge of the bank's credit exposure, grew "
                         r"into large positions in credit indices and their tranches, among them protection sold on an "
                         r"investment-grade index in a size so big that market participants called its trader the London Whale. "
                         r"As other dealers traded against it and the positions moved, the losses mounted",
                         stats=[(r"\$6.2\,\text{bn}", r"losses, 2012 (JPMorgan Task Force)"),
                                (r"\$920\,\text{m}", r"penalties to U.S. and U.K. regulators, September 2013")],
                         width=8.6, font_size=20).move_to(UP * 0.4)
        foot = wrapped_label(r"from the public record: JPMorgan Chase, Report of the Management Task Force Regarding "
                             r"2012 CIO Losses (January 2013); U.S. Senate Permanent Subcommittee on Investigations, "
                             r"JPMorgan Chase Whale Trades (March 2013)", 11.5, 18, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "In 2012 the largest bank in the United States lost six point two billion dollars on credit derivatives. "
            "The trades sat in its Chief Investment Office, in London, in a portfolio meant to hedge the bank's "
            "credit risk. It had grown into huge positions in credit indices and their tranches, one so large that "
            "the market nicknamed its trader the London Whale. <bookmark mark='a'/> The bank's own task force and a "
            "Senate subcommittee both published their findings. By the Senate's account, the portfolio's net notional "
            "size tripled in the first quarter of 2012, from about fifty-one billion dollars to one hundred and "
            "fifty-seven billion, as the office kept adding to positions that were losing money. Regulators in the "
            "United States and Britain later imposed nine hundred and twenty million dollars in penalties."
        ) as vo:
            self.play(FadeIn(cc))
            vo.wait_until("a")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def var(self):
        rows = [cmath(r"\text{VaR}_{95\%}", r"\approx", r"1.65\,\sigma_{\text{P\&L}}", font_size=40,
                      colors={r"\text{VaR}_{95\%}": RISKY}),
                cmath(r"\sigma_{\text{P\&L}}", r"\propto", r"\sqrt{\text{hazard-rate volatility}}", font_size=36,
                      colors={r"\sigma_{\text{P\&L}}": BAD}),
                cmath(r"\frac{\text{a} - \text{b}}{\text{sum}}", r"\ \text{vs}\ ", r"\frac{\text{a} - \text{b}}{\text{average}}",
                      font_size=36, colors={r"\frac{\text{a} - \text{b}}{\text{sum}}": BAD})]
        whys = [why(r"in January 2012 the CIO switched to a new value-at-risk model, and the portfolio's reported VaR "
                    r"fell by about half"),
                why(r"the task force found the new model had been built in spreadsheets, with values copied by hand"),
                why(r"and one formula divided a change in hazard rates by their sum instead of their average, muting "
                    r"volatility by a factor of two: risk reported at half its size")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "How did the risk stay hidden? The task force's answers are a lesson in model risk. "
            "<bookmark mark='a'/> In January 2012 the office adopted a new value-at-risk model, which roughly halved "
            "the reported risk of the portfolio. <bookmark mark='b'/> The model ran in spreadsheets, with figures "
            "copied in by hand. <bookmark mark='c'/> And one formula divided a change in hazard rates by their sum "
            "rather than their average, which by itself cut the measured volatility in half. The limits were set "
            "against a number that was wrong by construction."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.add(illustration(r"JPMorgan Chase Task Force report (January 2013): the VaR model's implementation"))
        self.wait(0.4)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"a hedge must hedge something", r"a credit hedge is judged by what it offsets: if no one can "
                          r"say which exposure it reduces, or by how much, it is a position", width=12.0, font_size=22),
            desk_question(r"size is a risk factor", r"a position large enough to be known by the market cannot be "
                          r"exited at the marks; liquidity of the size, not of the instrument, sets the loss",
                          width=12.0, font_size=22),
            desk_question(r"models are code", r"a risk model needs version control, tests and independent review "
                          r"like any other software; the House's Rules 13, 16 and 17 exist for this", width=12.0,
                          font_size=22),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Three lessons the House keeps. A hedge must say what it hedges, and by how much; otherwise it is a "
            "position. <bookmark mark='a'/> Size is a risk factor of its own: a position the whole market knows about "
            "cannot be sold at its marks. <bookmark mark='b'/> And a risk model is software: it needs tests, version "
            "control and a second pair of eyes, like every function in the House's library."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a risk number halves overnight because of a model change, and the position did not change. What "
                r"should the risk desk do before accepting it?")
        with self.voiceover("A risk number halves overnight because the model changed, not the position. What should "
                            "the risk desk do before accepting it?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
