from __future__ import annotations

from videos.stats.stats57.common import *  # noqa: F403


class OpenProblems(VoiceoverScene):
    def construct(self):
        self.card()
        self.map_()
        self.checklist()
        self.problems()
        self.op_class()
        self.op_eff()
        self.op_dep()
        self.op_train()
        self.op_struct()
        self.op_func()

    def card(self):
        card = chapter_card(10, r"Open problems", r"Between the possible and the impossible", part=PART)
        with self.voiceover("Chapter ten. Open problems, between the possible and the impossible."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def map_(self):
        hdr = [r"target", r"guarantee", r"assumes"]
        body = [
            [r"a new outcome", r"marginal, \ exact", r"exchangeability"],
            [r"a new outcome, \ by group", r"each named group", r"exchangeability"],
            [r"a new outcome, \ every $x$", r"impossible \ (finite length)", r"---"],
            [r"under drift", r"$1 - \alpha - $ a TV term", r"nothing"],
            [r"online", r"long-run frequency", r"nothing"],
            [r"a mean, \ $P(Y{=}1 \mid x)$", r"impossible", r"---"],
        ]
        cols = [GREY_B, COVC, COVC, MISSC, WEIGHTC, WEIGHTC, MISSC]
        tab = table_rows([hdr] + body, font_size=28, col_buff=0.8, row_buff=0.3, colors=cols).move_to([0, 0.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The part in one table. <bookmark mark='b'/> A new outcome can be covered marginally and "
            "exactly, assuming only exchangeability; and within each named group, with the same assumption. Coverage at every "
            "single x is impossible with finite intervals. Under drift, coverage degrades by a total-variation term, with no "
            "assumption. Online, the long-run frequency of misses is controlled for any sequence. And a mean, or a conditional "
            "probability, has no distribution-free interval at all."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in tab[1:]], lag_ratio=0.6), run_time=16.0)
        self.wait(1.0)
        self.clear_scene()

    def checklist(self):
        rows = [
            cmath(r"\text{ask}", r":", r"\text{what is being covered: \ an observable, \ or a parameter?}", font_size=34),
            cmath(r"\text{then}", r":", r"\text{marginal, \ group-conditional, \ or under shift?}", font_size=34),
            cmath(r"\text{and}", r":", r"\text{is exchangeability plausible, \ or are weights needed?}", font_size=34),
            cmath(r"\text{finally}", r":", r"\text{how large is the calibration set?}", font_size=36),
        ]
        rows[3][-1].set_color(TESTPT)
        whys = [why(r"chapter 3's boundary"), why(r"chapters 4, \ 5, \ 9"), why(r"chapters 5, \ 6"), why(r"chapter 1's Beta law")]
        with self.voiceover(
            "<bookmark mark='a'/> A checklist for reading a distribution-free claim. What is being covered: an "
            "observable outcome, or a parameter of the distribution? <bookmark mark='b'/> Is the guarantee marginal, "
            "conditional on named groups, or under a shift? <bookmark mark='c'/> Is exchangeability plausible, or are "
            "weights needed? <bookmark mark='d'/> And how large is the calibration set, which decides how much the "
            "realized coverage can vary from one deployment to another?"
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def op_class(self):
        rows = [
            cmath(r"\text{problem 1}", r":", r"\text{choose } \mathcal F \text{ from the data, \ keep the guarantee}", font_size=34),
            cmath(r"\text{known}", r":", r"\text{penalized classes: \ an estimable slack}", font_size=36),
            cmath(r"\text{naive}", r":", r"\text{pick } \mathcal F \text{ on the calibration data: \ invalid}", font_size=36),
            cmath(r"\text{open}", r":", r"\text{adaptive classes, \ exact, \ no lost data}", font_size=36),
        ]
        rows[1][-1].set_color(COVC)
        rows[2][-1].set_color(MISSC)
        whys = [why(r"which groups?"), why(r"Gibbs, \ Cherian \& Cand\`es"), why(r"Part 56's problem, \ again"), why(r"a sample split wastes data")]
        with self.voiceover(
            "<bookmark mark='a'/> Problem one in more detail. The group-conditional guarantee depends on a class of "
            "functions chosen in advance. Can it be chosen from the data? <bookmark mark='b'/> For penalized infinite "
            "classes, such as kernel functions with a ridge penalty, Gibbs, Cherian and Candès give coverage with a "
            "slack that can be estimated. <bookmark mark='c'/> But choosing the class on the calibration data is Part "
            "fifty-six's problem again: selection invalidates the guarantee. <bookmark mark='d'/> Splitting the data "
            "off for the choice is valid, and wasteful. What is open is a way to adapt the class with exact coverage "
            "and no data thrown away."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def op_eff(self):
        rows = [
            cmath(r"\text{problem 2}", r":", r"\text{the shortest sets that keep the guarantee}", font_size=36),
            cmath(r"\text{known}", r":", r"\text{consistent scores approach the oracle's sets}", font_size=36),
            cmath(r"\text{but}", r":", r"\text{in finite samples, \ the score is the whole game}", font_size=34),
            cmath(r"\text{open}", r":", r"\text{a finite-sample theory of optimal scores}", font_size=36),
        ]
        rows[1][-1].set_color(COVC)
        whys = [why(r"efficiency"), why(r"Lei, \ Robins \& Wasserman (2013)"), why(r"CQR vs residuals"), why(r"beyond asymptotics")]
        with self.voiceover(
            "<bookmark mark='a'/> Problem two: efficiency. Validity is free; length is not. Which sets are shortest "
            "among those that keep the guarantee? <bookmark mark='b'/> Asymptotically the answer is known: with a "
            "consistent estimate of the conditional density or quantiles, conformal sets approach the oracle's, as "
            "Lei, Robins and Wasserman showed for density level sets. <bookmark mark='c'/> In finite samples the "
            "choice of score is everything, as Part thirty-four's comparison of residuals and quantile regression "
            "showed. <bookmark mark='d'/> A finite-sample theory of optimal scores is open."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def op_dep(self):
        rows = [
            cmath(r"\text{problem 3}", r":", r"\text{dependent data: \ time series, \ space, \ networks}", font_size=34),
            cmath(r"\text{known}", r":", r"\text{coverage} \ge 1 - \alpha - \textstyle\sum_i \tilde w_i\, d_{\mathrm{TV}}(Z, Z^i)", font_size=34),
            cmath(r"\text{but}", r":", r"\text{the TV terms are unknown, \ and rarely estimable}", font_size=34),
            cmath(r"\text{open}", r":", r"\text{sharp bounds under mixing; \ data-chosen weights}", font_size=36),
        ]
        rows[1][-1].set_color(COVC)
        rows[2][-1].set_color(MISSC)
        whys = [why(r"no exchangeability"), why(r"chapter 5's theorem"), why(r"the bound is not a number"), why(r"Chernozhukov, \ W\"uthrich \& Zhu")]
        with self.voiceover(
            "<bookmark mark='a'/> Problem three: dependence. Time series, spatial data and networks are not "
            "exchangeable. <bookmark mark='b'/> Chapter five's theorem bounds the loss by weighted total-variation "
            "terms, <bookmark mark='c'/> but those terms are unknown, and rarely estimable from the data, so the bound "
            "is not a number one can report. <bookmark mark='d'/> Sharp guarantees under mixing conditions, building "
            "on work such as Chernozhukov, Wüthrich and Zhu's on block structures, and weights that may be chosen from "
            "the data without breaking the theorem, are open."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def op_train(self):
        rows = [
            cmath(r"\text{problem 4}", r":", r"\text{coverage given the training and calibration data}", font_size=34),
            cmath(r"\text{split}", r":", r"\text{chapter 1's Beta law: \ a PAC guarantee}", font_size=36),
            cmath(r"\text{full, \ jackknife}+", r":", r"\text{no such guarantee in general}", font_size=36),
            cmath(r"\text{open}", r":", r"\text{which algorithms, \ under what stability, \ get one}", font_size=34),
        ]
        rows[1][-1].set_color(COVC)
        rows[2][-1].set_color(MISSC)
        whys = [why(r"the deployed model"), why(r"Vovk (2012)"), why(r"Bian \& Barber (2023)"), why(r"stability again")]
        with self.voiceover(
            "<bookmark mark='a'/> Problem four: the deployed model. A practitioner has one training set and one "
            "calibration set, and wants coverage given them, not on average over data they never saw. <bookmark "
            "mark='b'/> For split conformal, chapter one's Beta law gives that, a probably-approximately-correct "
            "guarantee. <bookmark mark='c'/> For full conformal and jackknife plus, Michael Bian and Barber showed "
            "there is no such guarantee in general. <bookmark mark='d'/> Which algorithms, under what stability, earn "
            "one is open."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def op_struct(self):
        rows = [
            cmath(r"\text{problem 5}", r":", r"\text{sets of graphs, \ texts, \ trajectories}", font_size=36),
            cmath(r"\text{known}", r":", r"\text{conformal factuality: \ filter claims to control errors}", font_size=34),
            cmath(r"\text{but}", r":", r"\text{the set must be usable, \ not just valid}", font_size=36),
            cmath(r"\text{open}", r":", r"\text{guarantees when prompts drift, \ and useful set shapes}", font_size=34),
        ]
        rows[1][-1].set_color(COVC)
        rows[2][-1].set_color(WEIGHTC)
        whys = [why(r"structured outputs"), why(r"Mohri \& Hashimoto (2024)"), why(r"a set of a million texts"), why(r"chapter 5, \ again")]
        with self.voiceover(
            "<bookmark mark='a'/> Problem five: structured outputs. What is a prediction set of graphs, of paragraphs, "
            "of trajectories? <bookmark mark='b'/> Chapter eight's conformal factuality, from Christopher Mohri and "
            "Tatsunori Hashimoto, controls errors by filtering claims. <bookmark mark='c'/> But a set must be usable, "
            "not just valid: a set of a million possible paragraphs is correct and useless. <bookmark mark='d'/> "
            "Guarantees when the stream of prompts drifts, and set shapes a person can act on, are open."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def op_func(self):
        rows = [
            cmath(r"\text{problem 6}", r":", r"\text{which functionals have distribution-free intervals?}", font_size=34),
            cmath(r"\text{Bahadur \& Savage}", r":", r"\text{the mean: \ none}", font_size=38),
            cmath(r"\text{Donoho (1988)}", r":", r"\text{one-sided bounds exist for semicontinuous functionals}", font_size=32),
            cmath(r"\text{open}", r":", r"\text{the weakest assumptions that make a functional estimable}", font_size=32),
        ]
        rows[1][-1].set_color(MISSC)
        rows[2][-1].set_color(COVC)
        whys = [why(r"the theme of the part"), why(r"chapter 0"), why(r"e.g. a lower bound on modes"), why(r"between the two")]
        with self.voiceover(
            "<bookmark mark='a'/> Problem six, the part's theme. Which functionals of a distribution admit intervals "
            "with no assumptions? <bookmark mark='b'/> Bahadur and Savage: not the mean. <bookmark mark='c'/> David "
            "Donoho showed in 1988 that one-sided bounds exist for functionals that are semicontinuous in the right "
            "sense, such as a lower bound on the number of modes of a density. <bookmark mark='d'/> Between these, the "
            "weakest assumptions that make a given functional estimable, and the price of each, remain to be mapped."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def problems(self):
        rows = fit_rows(VGroup(
            label(r"Open problems", font_size=40, color=S.ACCENT),
            label(r"1. \ The right function class: \ choosing $\mathcal F$ from data without losing the guarantee", font_size=25),
            label(r"2. \ Efficiency: \ the shortest sets with a guarantee; \ optimal scores beyond quantile regression", font_size=25),
            label(r"3. \ Dependence: \ sharp guarantees for time series and spatial data, \ estimable TV terms", font_size=25),
            label(r"4. \ Conditional on the calibration set: \ PAC-style guarantees that are not wasteful", font_size=25),
            label(r"5. \ Structured outputs: \ sets of graphs, \ texts, \ trajectories; \ risk control for language models", font_size=25),
            label(r"6. \ The weakest assumptions under which a functional of $P$ becomes estimable", font_size=25),
        ), 12.6, 0.42, [0, 0, 0])
        rows[0].set_x(0)
        with self.voiceover(
            "<bookmark mark='a'/> Six open problems. <bookmark mark='b'/> First, choosing the function class from the data "
            "without losing the guarantee. <bookmark mark='c'/> Second, efficiency: the shortest sets that keep the guarantee, "
            "and optimal scores. <bookmark mark='d'/> Third, dependence: sharp guarantees for time series and spatial data, with "
            "total-variation terms one can estimate. <bookmark mark='e'/> Fourth, guarantees conditional on the calibration set "
            "that are not wasteful. <bookmark mark='f'/> Fifth, structured outputs, such as sets of graphs or texts, and risk "
            "control for language models. <bookmark mark='g'/> And sixth, the weakest assumptions under which a functional of "
            "the distribution becomes estimable at all."
        ) as vo:
            for k, m_ in enumerate("abcdefg"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
        self.wait(1.5)
        self.clear_scene()
