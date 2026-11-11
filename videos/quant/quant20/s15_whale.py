from __future__ import annotations

from videos.quant.quant20.common import lesson_cards

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, PART, RISKY, ask, fit_right, illustration, load


class Whale(VoiceoverScene):
    def construct(self):
        self.card()
        self.case()
        self.var()
        self.lessons()
        self.feedback()

    def card(self):
        c = chapter_card(14, r"2012: the London Whale", r"How does a hedge become the risk?", lit=(2012,), part=PART)
        with self.voiceover('Chapter fourteen. The London Whale: how a purported credit hedge became a material source of losses and a test of risk governance.'):
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
        rows = [cmath(r"\mathrm{VaR}_{95\%}", r"\approx", r"1.645\,\sigma_{\mathrm{P\&L}}\quad\text{(zero-mean normal loss)}", font_size=34),
                cmath(r"\Delta V", r"\approx", r"\nabla_s V^\top\Delta s\quad\text{(local linearization)}", font_size=34),
                cmath(r"\mathrm{validation}", r"\ ", r"\text{old/new comparison, stress, independent implementation}", font_size=28)]
        whys = [why(r"the normal approximation needs a horizon, loss convention and distribution; actual tail risk can differ"),
                why(r"risk depends on positions, sensitivities and the covariance of curve changes, not a square root of volatility"),
                why(r"a change in reported risk does not reduce the portfolio's economic exposure")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-.6, buff=.7, edge=6.9)
        with self.voiceover("A risk-model change is not a reduction in the position's economic exposure. <bookmark mark='a'/> The London Whale investigations documented a model change and serious implementation and control failures. <bookmark mark='b'/> The formulas here are general teaching approximations, not a reconstruction of the bank's proprietary model. Normal value at risk needs a specified horizon and loss distribution. Local sensitivity maps curve changes into profit and loss; covariance and nonlinear stress matter. <bookmark mark='c'/> Before adopting a lower reported number, compare the old and new models on the same positions, independently validate the implementation, investigate exceptions and run stressed liquidity and dependence scenarios. A spreadsheet error and a bad modeling assumption require distinct fixes.") as vo:
            step(0)
            vo.wait_until('a'); self.wait(.1)
            vo.wait_until('b'); step(1)
            vo.wait_until('c'); step(2)
        self.wait(.5)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"a hedge must hedge something", r"a credit hedge is judged by what it offsets: if no one can "
                          r"say which exposure it reduces, or by how much, it is a position", width=12.0, font_size=22),
            desk_question(r"size is a risk factor", 'a large, visible exit can move executable prices. Marks are not guaranteed at size; assess sensitivity, concentration, liquidity and the cost of reducing the position',
                          width=12.0, font_size=22),
            desk_question(r"models are code", r"a risk model needs version control, tests and independent review "
                          r"like any other software; the House's Rules 13, 16 and 17 exist for this", width=12.0,
                          font_size=22),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Three lessons the House keeps. A hedge must say what it hedges, and by how much; otherwise it is a position. <bookmark mark='a'/> Size is a risk factor of its own: a large visible exit can be costly, and marks are not guaranteed executable at size. <bookmark mark='b'/> And a risk model is software: it needs tests, version control and a second pair of eyes, like every function in the House's library."
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

    def feedback(self):
        title = wrapped_label('Answer: validate the change on unchanged positions', 12.4, 32, QC.IDEA).to_edge(UP, buff=.6)
        answer = wrapped_label('Compare old and new models, reconcile inputs and units, independently reproduce calculations, investigate exceptions and run liquidity and nonlinear stress scenarios.', 11.8, 27, GREY_A).move_to(ORIGIN)
        with self.voiceover('Before accepting a risk number that halves on unchanged positions, compare the old and new models on exactly the same portfolio. Reconcile inputs, units and conventions, independently reproduce implementation, investigate exceptions and test nonlinear, liquidity and concentration stresses. A lower estimate alone is no evidence of a lower economic exposure.') as vo:
            self.play(FadeIn(title), FadeIn(answer))
        self.wait(.5)
        self.clear_scene()
