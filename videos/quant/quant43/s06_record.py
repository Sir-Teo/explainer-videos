from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant43.common import (ACT_C, BAD, COST_C, GOOD, HURDLE, LUCK_C, MKT_C, PART, REC_C, SKILL_C,
                                         ladder)


class Record(VoiceoverScene):
    """Prospective evidence design; no strategy registry, envelope or outcome inputs."""

    def construct(self):
        self.card()
        self.question_first()
        self.protocol()
        self.selection()
        self.costs()
        self.uncertainty()
        self.monitoring()
        self.reporting()
        self.verdict()
        self.question()

    def card(self):
        c = chapter_card(5, r"Design a record before seeing results",
                         r"What would make evidence about skill credible?", part=PART)
        with self.voiceover(
            "Chapter five. A change of task: design evidence before seeing the answer. This presentation does not "
            "open, score or display the House's sealed strategy results, and it does not execute its final ensemble. "
            "The chapter instead connects the previous simulations to a prospective research protocol. A protocol "
            "states what will be measured, when the rule is frozen, how selection is counted and what uncertainty "
            "will be reported. Having such a protocol does not itself demonstrate skill."
        ):
            self.play(FadeIn(c[0], shift=UP * .2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def question_first(self):
        cards = VGroup(
            desk_question(r"the estimand", r"net excess return over a named investable benchmark, in a specified "
                          r"universe, horizon and risk budget", width=12.4, font_size=19),
            desk_question(r"the decision", r"what result would change a research decision, and what result would "
                          r"count against the hypothesis?", width=12.4, font_size=19),
            desk_question(r"the information set", r"publication times, revisions, delistings and execution information "
                          r"available at each simulated decision", width=12.4, font_size=19),
        ).arrange(DOWN, buff=.25)
        with self.voiceover(
            "Begin with the question. <bookmark mark='a'/> Specify the benchmark and net return being estimated. "
            "A claim about excess return is different from a claim about risk reduction or execution quality. "
            "<bookmark mark='b'/> State which result would change the decision and which would count against it. "
            "<bookmark mark='c'/> Then define the information available at each date, including publication lags and "
            "revisions. A later timestamp attached to a feature is not enough if the feature was built with future data."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k, mark in enumerate(('a', 'b', 'c')):
                vo.wait_until(mark)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * .2))
        self.clear_scene()

    def protocol(self):
        rows = [
            cmath(r"\text{research}", r":", r"\text{fit and choose using permitted data only}", font_size=36),
            cmath(r"\text{freeze}", r":", r"\text{code, parameters, costs, metric, stopping rule}", font_size=34),
            cmath(r"\text{evaluation}", r":", r"\text{independent of those choices; report every planned result}", font_size=32),
            cmath(r"\text{revision}", r":", r"\text{new hypothesis; old evaluation is now known information}", font_size=32),
        ]
        whys = [why(r"a validation split used for model choice is part of research"),
                why(r"record the complete decision rule before evaluation"),
                why(r"a small set of favourable outcomes is not the complete planned family"),
                why(r"a hash checks byte identity; it does not erase prior knowledge or enforce an honest process")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=0, buff=.5)
        with self.voiceover(
            "A prospective sequence. <bookmark mark='a'/> Fit and choose on permitted research information. "
            "<bookmark mark='b'/> Freeze the full decision rule, not just its model coefficients. Costs, metrics and "
            "stopping decisions matter too. <bookmark mark='c'/> Evaluate independently of those choices and report "
            "the whole planned family. <bookmark mark='d'/> A revision is a new hypothesis. Reusing a known test "
            "window cannot make it unseen again. Code hashes support an audit, but do not prove information isolation."
        ) as vo:
            step(0)
            for k, mark in enumerate(('a', 'b', 'c', 'd')):
                vo.wait_until(mark)
                if k:
                    step(k)
        self.clear_scene()

    def selection(self):
        rows = [
            cmath(r"Z_j", r"\sim", r"N(0,1),\quad j=1,\ldots,M\quad\text{under the joint null}", font_size=34),
            cmath(r"P(\max_j Z_j>c)", r"\le", r"M\,[1-\Phi(c)]", font_size=40),
            cmath(r"M=20,\ \alpha=.05", r"\Rightarrow", r"c=\Phi^{-1}(1-.05/20)\approx2.81", font_size=34),
        ]
        whys = [why(r"a stylised family of valid standard-normal test statistics, not strategy returns"),
                why(r"the union bound needs no independence, but does need valid marginal null tails"),
                why(r"a one-sided Bonferroni family-wise threshold; not an expected maximum or an FDR threshold")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=0, buff=.6)
        with self.voiceover(
            "Selection changes the question. <bookmark mark='a'/> Imagine twenty valid standard-normal statistics "
            "under their nulls. No experiment is being run here; this is a probability calculation. "
            "<bookmark mark='b'/> The probability that at least one exceeds c is no larger than the sum of their tail "
            "probabilities. This union bound does not require independent tests. <bookmark mark='c'/> A five percent "
            "family-wise error budget across twenty one-sided tests gives a cutoff near two point eight one. This "
            "controls a different error criterion from false discovery rate, and it is not a probability that a winner is skilled."
        ) as vo:
            step(0)
            for k, mark in enumerate(('a', 'b', 'c')):
                vo.wait_until(mark)
                if k:
                    step(k)
        self.clear_scene()

    def costs(self):
        cards = VGroup(
            desk_question(r"returns", r"benchmark, financing and cash treatment must match the economic claim", width=12.4, font_size=19),
            desk_question(r"implementation", r"fees, spread, impact, borrow, turnover, capacity and execution timing", width=12.4, font_size=19),
            desk_question(r"uncertainty", r"report assumptions and sensitivity; a cost model is an estimate, not a fill guarantee", width=12.4, font_size=19),
        ).arrange(DOWN, buff=.25)
        with self.voiceover(
            "Net of what? <bookmark mark='a'/> Use a benchmark and financing convention consistent with the claim. "
            "<bookmark mark='b'/> Include the costs of actually implementing the rule, and distinguish observed fees "
            "from estimated impact or borrow availability. <bookmark mark='c'/> Report sensitivity to those estimates. "
            "Subtracting a constant fee from a frictionless series does not establish executable capacity. A gross "
            "return ranking and a net implementable return ranking need not agree."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k, mark in enumerate(('a', 'b', 'c')):
                vo.wait_until(mark)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * .2))
        self.clear_scene()

    def uncertainty(self):
        rows = [
            cmath(r"\widehat{SR}=\bar r/s", r":", r"\text{iid annual Gaussian excess returns}", font_size=34),
            cmath(r"\operatorname{se}(\widehat{SR})", r"\approx", r"\sqrt{(1+SR^2/2)/T}", font_size=42),
            cmath(r"SR=.5,\ T=20", r"\Rightarrow", r"\operatorname{se}\approx.237", font_size=40),
        ]
        whys = [why(r"frequency and independence assumptions are part of the calculation"),
                why(r"a large-sample delta-method approximation, not an exact small-sample interval"),
                why(r"serial dependence, non-Gaussian tails and selection require additional treatment")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=0, buff=.6)
        with self.voiceover(
            "A point estimate is not the evidence. <bookmark mark='a'/> For independent annual Gaussian excess "
            "returns, a Sharpe ratio has a familiar large-sample uncertainty approximation. "
            "<bookmark mark='b'/> Its standard error is approximately the square root of one plus half the squared "
            "Sharpe, divided by the number of annual observations. <bookmark mark='c'/> At a Sharpe of a half and "
            "twenty observations, that is about point two three seven. These are illustrative assumptions, not a "
            "measurement of any House strategy. Annualising monthly observations changes the formula's inputs; "
            "serial dependence and heavy tails also matter, and a selected winner needs selection-aware inference."
        ) as vo:
            step(0)
            for k, mark in enumerate(('a', 'b', 'c')):
                vo.wait_until(mark)
                if k:
                    step(k)
        self.clear_scene()

    def monitoring(self):
        cards = VGroup(
            desk_question(r"one planned endpoint", r"a fixed-horizon test has its stated error rate under its assumptions", width=12.4, font_size=19),
            desk_question(r"repeated looks", r"stopping when a favourable result first appears changes that error rate", width=12.4, font_size=19),
            desk_question(r"a new design", r"predeclare monitoring or use a justified sequential procedure; count adaptations too", width=12.4, font_size=19),
        ).arrange(DOWN, buff=.25)
        with self.voiceover(
            "Monitoring is another choice. <bookmark mark='a'/> A fixed-horizon test concerns the endpoint that was "
            "planned. <bookmark mark='b'/> Looking repeatedly and stopping at the first favourable number generally "
            "does not retain that test's nominal error rate. <bookmark mark='c'/> Predeclare monitoring or use a "
            "sequential procedure justified for the data-generating assumptions. Neither the word hold-out nor a "
            "registration date automatically solves optional stopping, repeated tuning or leakage across related strategies."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k, mark in enumerate(('a', 'b', 'c')):
                vo.wait_until(mark)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * .2))
        self.clear_scene()

    def reporting(self):
        cards = VGroup(
            desk_question(r"the record should contain", r"all planned estimates, benchmark and cost definitions, uncertainty and failures", width=12.4, font_size=19),
            desk_question(r"comparability", r"different windows, universes and risks do not become one fair ranking by sharing a table", width=12.4, font_size=19),
            desk_question(r"interpretation", r"unexpected performance is a question to investigate; it is not proof of its preferred cause", width=12.4, font_size=19),
        ).arrange(DOWN, buff=.25)
        with self.voiceover(
            "What should the eventual report contain? <bookmark mark='a'/> The complete planned set of estimates, "
            "with cost assumptions, uncertainty and failures. <bookmark mark='b'/> Check that rows have comparable "
            "windows, risk exposure and benchmarks before ranking them. A regression across heterogeneous rows is "
            "descriptive and does not by itself identify decay or a forecast for the next strategy. "
            "<bookmark mark='c'/> Unexpected results can reflect sampling, changing exposures, selection or a new "
            "mechanism. The result alone does not tell us which explanation is correct."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k, mark in enumerate(('a', 'b', 'c')):
                vo.wait_until(mark)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * .2))
        self.clear_scene()

    def verdict(self):
        cards = VGroup(
            desk_question(r"what this chapter establishes", r"an evidence design and analytical selection/uncertainty examples", width=12.4, font_size=19),
            desk_question(r"what remains to be established", r"whether a particular investable rule adds value under an independently justified evaluation", width=12.4, font_size=19),
            desk_question(r"the next chapter", r"pricing-fit summaries also require matching targets, units, weights and evaluation design", width=12.4, font_size=19),
        ).arrange(DOWN, buff=.25)
        with self.voiceover(
            "The conclusion has a defined scope. <bookmark mark='a'/> This chapter establishes a design and works "
            "through analytical error and uncertainty calculations. <bookmark mark='b'/> It does not establish the "
            "performance of a particular strategy, ensemble or sleeve. No sealed strategy outcomes are inputs to this "
            "presentation. <bookmark mark='c'/> The same discipline carries to pricing: summaries become comparable "
            "only after their targets, units, weights and evaluation procedures have been checked."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k, mark in enumerate(('a', 'b', 'c')):
                vo.wait_until(mark)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * .2))
        self.clear_scene()

    def question(self):
        q = pause_card(r"two pricing RMSEs come from the same market date. What else must match before ranking the models?")
        with self.voiceover(
            "Pause and predict. Two pricing RMSEs come from the same market date. What else must match before "
            "ranking the models? Think of targets, quotes, weights, units and the evaluation procedure."
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
