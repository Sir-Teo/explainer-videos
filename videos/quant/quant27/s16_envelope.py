"""Evaluation design for learned models; excluded originals remain unopened."""
from __future__ import annotations
import math
from explainer.quant import *  # noqa: F403
from explainer.quant.house import pit
from videos.quant.quant27.common import PART, ask, comma


class Envelope(VoiceoverScene):
    def construct(self):
        self.card()
        self.pipeline()
        self.selection()
        self.accounting()
        self.comparison()
        self.boundary()

    def card(self):
        c = chapter_card(15, r"Registration and evaluation for learned models",
                         r"What must be fixed before the next model comparison?", part=PART)
        with self.voiceover("Chapter fifteen. Registration and evaluation for learned models. The original panel-sealing routine and strategy envelope are excluded from this review. This chapter designs an evaluation protocol without loading their caches, opening a strategy experiment or reporting a sealed score."):
            self.play(FadeIn(c[0], shift=UP * .2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def pipeline(self):
        cards = VGroup(
            desk_question(r"data and target clock", r"release vintages, archive membership, feature availability, label end dates and executable decision times", width=12, font_size=30),
            desk_question(r"transformations and fitting", r"fit preprocessing inside training; separate validation and calibration; lock seeds, optimisation budget and stopping choices", width=12, font_size=30),
            desk_question(r"portfolio implementation", r"position and capital definitions, turnover, spreads, impact, borrow and financing; volume weights are not market-cap weights", width=12, font_size=30),
        ).arrange(DOWN, buff=.28)
        with self.voiceover("The object to freeze is the entire pipeline. <bookmark mark='a'/> Record when each input was available, which assets entered the archive, when each label matures, and which price can actually be traded after the decision. <bookmark mark='b'/> Fit transformations inside training. Allocate distinct roles to validation and calibration, and freeze seeds, optimisation budgets and stopping choices. <bookmark mark='c'/> Define positions, capital and costs. A trading-volume-weighted long-short illustration does not become a market-cap portfolio or an executable strategy merely because its forecasts were held out.") as vo:
            self.play(FadeIn(cards[0], shift=UP * .2))
            vo.wait_until('b'); self.play(FadeIn(cards[1], shift=UP * .2))
            vo.wait_until('c'); self.play(FadeIn(cards[2], shift=UP * .2))
        self.clear_scene()

    def selection(self):
        cards = VGroup(
            desk_question(r"compare the same prediction task", r"match information, target horizon, training dates, tuning opportunities, compute budget and economic constraints", width=12, font_size=30),
            desk_question(r"account for the search", r"architecture, features, penalties, seeds, validation reuse and informal revisions can all select the reported winner", width=12, font_size=30),
            desk_question(r"state what uncertainty covers", r"point estimates, paired comparisons, multiplicity and calibration assumptions answer different questions", width=12, font_size=30),
        ).arrange(DOWN, buff=.28)
        with self.voiceover("A comparison needs a common task before it needs a bigger network. <bookmark mark='a'/> Match the information, horizon, training dates, tuning opportunities, compute budget and economic constraints. A reversal rule with a target's own lag has information that a model fed unrelated predictors may lack. <bookmark mark='b'/> Count architecture, feature, penalty and seed choices, including informal revisions and validation reuse. A single final display does not erase the selection that produced it. <bookmark mark='c'/> Then state the uncertainty question: uncertainty about one mean is different from a paired model difference, a searched winner, or an interval under exchangeability.") as vo:
            self.play(FadeIn(cards[0], shift=UP * .2))
            vo.wait_until('b'); self.play(FadeIn(cards[1], shift=UP * .2))
            vo.wait_until('c'); self.play(FadeIn(cards[2], shift=UP * .2))
        self.clear_scene()

    def accounting(self):
        n = pit.trials_upto(PART); previous = pit.trials_upto(PART - 1)
        count = MathTex(rf"\text{{existing cumulative registrations through Part 27}}:\ {comma(n)}", font_size=30).to_edge(UP, buff=.65)
        if count.width > 12.3: count.scale_to_fit_width(12.3)
        cards = VGroup(
            desk_question(r"existing ledger metadata", rf"{comma(n - previous)} additional recorded configurations relative to Part 26; no new registration by this review", width=12, font_size=30),
            desk_question(r"the wider research search", r"recorded configurations are a lower bound, and dependence prevents a simple independent-trial interpretation", width=12, font_size=30),
        ).arrange(DOWN, buff=.35).next_to(count, DOWN, buff=.6)
        with self.voiceover(f"The existing registration ledger through Part twenty-seven contains {n:,} configurations, {n - previous} more than the count through Part twenty-six. Those are already recorded metadata. <bookmark mark='a'/> This review adds no registration, strategy opening or market trial. It restores only audited ordinary originals and keeps the excluded experiment routines unchanged. <bookmark mark='b'/> A recorded count remains a lower bound on the broader search. Correlated configurations and adaptive research do not become independent tests because their names were counted.") as vo:
            self.play(FadeIn(count), FadeIn(cards[0]))
            vo.wait_until('b'); self.play(FadeIn(cards[1]))
        self.clear_scene()

    def comparison(self):
        eq = MathTex(r"D_t=A_t-B_t,\quad \sigma_D^2=\sigma_A^2+\sigma_B^2-2\rho\sigma_A\sigma_B", font_size=38).to_edge(UP, buff=.4)
        if eq.width > 12.3: eq.scale_to_fit_width(12.3)
        # the same arithmetic as geometry: the one- and two-sd ellipses of (A, B); the spread of D = A - B is their
        # width across the diagonal, sqrt(2 (1 - rho)), which shrinks as the correlation rises
        rho = ValueTracker(0.0)
        g = axes([-3, 3], [-3, 3], x_length=4.3, y_length=4.3, xticks=[-2, 0, 2], yticks=[-2, 0, 2], font_size=16).move_to(LEFT * 3.4 + DOWN * .35)
        ax = g.ax
        ang = np.linspace(0, 2 * np.pi, 121)
        def ellipse(k, width, op):
            r = rho.get_value()
            major, minor = k * np.sqrt(1 + r), k * np.sqrt(1 - r)  # along (1, 1) and (1, -1)
            x = (major * np.cos(ang) + minor * np.sin(ang)) / np.sqrt(2)
            y = (major * np.cos(ang) - minor * np.sin(ang)) / np.sqrt(2)
            return curve(ax, x, y, QC.SPOT, stroke_width=width).set_stroke(opacity=op)
        def across():
            h = np.sqrt(1 - rho.get_value()) / np.sqrt(2)
            return Line(ax.c2p(-h, h), ax.c2p(h, -h), color=QC.P, stroke_width=6)
        shapes = VGroup(always_redraw(lambda: ellipse(2, 2, .45)), always_redraw(lambda: ellipse(1, 3, 1)), always_redraw(across))
        diag = DashedLine(ax.c2p(-2.9, -2.9), ax.c2p(2.9, 2.9), color=GREY_C, stroke_width=1.5)
        names = VGroup(MathTex("A", font_size=28).next_to(ax.c2p(3, -3), RIGHT, buff=.12), MathTex("B", font_size=28).next_to(ax.c2p(-3, 3), UP, buff=.1))
        sd = lambda: float(np.sqrt(2 * (1 - rho.get_value())))
        reads = VGroup(readout(r"\rho=", rho.get_value, digits=2, font_size=34),
                       readout(r"\sigma_D=\sqrt{2(1-\rho)}=", sd, digits=3, font_size=32, color=QC.P),
                       readout(r"\operatorname{se}(\bar D)=\sigma_D/\sqrt{100}=", lambda: sd() / 10, digits=4, font_size=32, color=QC.P),
                       label(r"fixed mathematical example; arbitrary units", font_size=20, color=GREY_A)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=.38).next_to(g, RIGHT, buff=.9)
        foot = wrapped_label(r"This is paired-mean arithmetic, not a historical strategy result or a Sharpe-difference formula. Serial dependence, estimated risk and model selection need additional treatment.", 12, 22, GREY_A).to_edge(DOWN, buff=.35)
        with self.voiceover("For a mean comparison, use the paired difference. The variance of A minus B includes their covariance. <bookmark mark='a'/> In a fixed mathematical example, both standard deviations are one, correlation is point eight, and there are one hundred independent paired observations. The difference has standard deviation about point six three two, so its mean has standard error about point zero six three two. Ignoring covariance would answer the wrong precision question. <bookmark mark='b'/> These are invented arbitrary units, not a new strategy test or a formula for a difference of Sharpe ratios. Serial dependence, estimated risk and selection require further analysis.") as vo:
            self.play(FadeIn(eq), FadeIn(g), FadeIn(diag), FadeIn(names), FadeIn(shapes), FadeIn(reads))
            vo.wait_until('a')
            self.play(rho.animate.set_value(0.8), run_time=4.0)
            self.play(Indicate(reads[1], color=QC.P, scale_factor=1.06))
            self.play(Indicate(reads[2], color=QC.P, scale_factor=1.06))
            vo.wait_until('b'); self.play(FadeIn(foot))
        self.clear_scene()

    def boundary(self):
        head = label(r"The excluded strategy experiment remains unopened", font_size=32, color=QC.HOUSE).to_edge(UP, buff=.65)
        if head.width > 12.3: head.scale_to_fit_width(12.3)
        text = wrapped_label(r"No panel-sealing output, strategy envelope cache, payload, result row or substitute historical test is used. Public archives contain later observations, and original calendar masks can have boundary contamination; ordinary research diagnostics are not a fresh sealed evaluation.", 12, 23, GREY_A).next_to(head, DOWN, buff=.55)
        question = ask(r"Two models have similar standalone uncertainty. What must you know about their paired errors, information and selection before declaring a winner?")
        with self.voiceover("The boundary remains explicit. The panel-sealing output and strategy envelope are not loaded, opened or scored. Original ordinary research calculations can read later public archive vintages and have calendar-boundary contamination; that does not certify a fresh evaluation. <bookmark mark='a'/> Before declaring a winner, explain its information, paired errors, search history and execution assumptions. A result becomes useful through that evidence, not through the size of the model or a registration timestamp alone.") as vo:
            self.play(FadeIn(head), FadeIn(text))
            vo.wait_until('a'); self.play(FadeIn(question))
        self.clear_scene()
