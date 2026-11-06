from __future__ import annotations

import numpy as np

from videos.stats.stats64.common import *  # noqa: F403


class Judges(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter six. Labels from models: judges with errors, and how to correct for them.", 6,
                            r"Labels from models", r"A judge is a measurement")
        self.judges()
        self.bias()
        self.ppi()
        self.chart()
        self.dsl()
        self.cautions()

    def judges(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Grading open-ended answers by hand is slow, so evaluations increasingly ask another model "
            "to grade: an LLM judge. <bookmark mark='b'/> A judge is a measurement instrument, Part forty-one's, with a "
            "sensitivity and a specificity: how often it passes a correct answer, and how often it fails a wrong one. "
            "<bookmark mark='c'/> Judges are known to prefer longer answers, answers in the first position, and answers that "
            "resemble their own. <bookmark mark='d'/> So a model's score according to a judge is a biased estimate of its "
            "score according to people.",
            [(r"\text{LLM judge}", r":", r"\text{a model grades a model}", 40),
             (r"\text{an instrument}", r":", r"\text{sensitivity, \ specificity}", 40),
             (r"\text{known biases}", r":", r"\text{length, \ position, \ self-preference}", 40),
             (r"\text{so}", r":", r"\text{biased scores}", 40)],
            [r"cheap labels", r"Part 41", r"systematic", r"measurement error"],
            colors=[(3, NAIVEC)])

    def bias(self):
        d = load("judges")
        self.lad_voiceover(
            f"<bookmark mark='a'/> A simulation. A model is truly right on {100 * d['true']:.0f} percent of {d['N']:,} "
            f"questions. <bookmark mark='b'/> A lenient judge passes {100 * d['sens']:.0f} percent of right answers and "
            f"fails only {100 * d['spec']:.0f} percent of wrong ones. <bookmark mark='c'/> Its expected pass rate is the "
            f"sensitivity times the truth plus one minus the specificity times the rest: "
            f"{100 * (d['true'] + d['judge_bias']):.1f} percent, a bias of {100 * d['judge_bias']:.1f} points. <bookmark "
            f"mark='d'/> Five thousand judged answers make the judge's estimate very precise, and precisely wrong: its "
            f"interval covers the truth {100 * d['cov']['judge']:.1f} percent of the time.",
            [(r"\text{truth}", r":", rf"p = {d['true']:.2f}", 40),
             (r"\text{judge}", r":", rf"\text{{sens}} = {d['sens']:.2f}, \ \text{{spec}} = {d['spec']:.2f}", 40),
             (r"E[\text{pass}]", r"=", rf"\text{{sens}} \cdot p + (1 - \text{{spec}})(1 - p) = {d['true'] + d['judge_bias']:.3f}", 38),
             (r"\text{coverage}", r":", rf"{100 * d['cov']['judge']:.1f}\%", 40)],
            [r"seeded", r"a lenient judge", r"bias $+0.025$", r"precisely wrong"],
            colors=[(3, NAIVEC)])

    def ppi(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Part thirty-four's prediction-powered inference fixes it with a few human labels. "
            "<bookmark mark='b'/> Have people grade a small random sample, n of the answers, that the judge also grades. "
            "<bookmark mark='c'/> The estimate is the judge's mean on the large set, plus the average correction, human "
            "minus judge, on the small one: the rectifier. <bookmark mark='d'/> It is unbiased whatever the judge's errors, "
            "and its variance adds the large set's judge variance to the small set's correction variance. A good judge has "
            "small corrections, and then the interval is narrow; a bad judge only costs width, not validity.",
            [(r"\text{humans}", r":", r"n \ \text{random answers, \ also judged}", 40),
             (r"\hat\mu_{\text{PPI}}", r"=", r"\bar f_N + \overline{(y - f)}_n", 40),
             (r"\text{unbiased}", r":", r"\text{for any judge}", 40),
             (r"\mathrm{Var}", r"=", r"\sigma_f^2 / N + \sigma_{y - f}^2 / n", 40)],
            [r"Angelopoulos et al. (2023)", r"a calibration set", r"the rectifier", r"validity from design"],
            colors=[(1, HONC)])

    def chart(self):
        d = load("judges")
        A = axes([0.6, 0.8], [0.4, 3.6], x_length=7.6, y_length=3.6, xlabel=r"estimated accuracy, \ a typical 95\% interval",
                 ylabel=r"", xticks=[0.62, 0.66, 0.70, 0.74, 0.78], xfmt=lambda v: f"{100 * v:.0f}\\%", center=[0.4, 0.6, 0])
        ax = A.ax
        truth = DashedLine(ax.c2p(d["true"], 0.4), ax.c2p(d["true"], 3.6), color=WHITE, stroke_width=2)
        rows = VGroup()
        spec = [("judge", JUDGEC, rf"the judge alone, \ $N = {d['N']:,}$".replace(",", "{,}"), 3),
                ("human", MODA, rf"humans alone, \ $n = {d['n']}$", 2), ("ppi", HONC, r"prediction-powered", 1)]
        for key, c, name, yy in spec:
            m, w = d["mean"][key], d["width"][key]
            rows.add(VGroup(Line(ax.c2p(m - w / 2, yy), ax.c2p(m + w / 2, yy), color=c, stroke_width=6, stroke_opacity=0.6),
                            Dot(ax.c2p(m, yy), radius=0.09, color=c),
                            label(name, font_size=22, color=c).next_to(ax.c2p(0.6, yy), LEFT, buff=0.25),
                            label(rf"covers {100 * d['cov'][key]:.1f}\%", font_size=20, color=c).next_to(ax.c2p(0.8, yy), RIGHT, buff=0.2)))
        note_ = label(rf"PPI's interval is {100 * (1 - d['width']['ppi'] / d['width']['human']):.0f}\% narrower than the humans' alone",
                      font_size=24, color=HONC).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            f"<bookmark mark='a'/> Over {d['reps']:,} simulations: <bookmark mark='b'/> the judge alone gives a tight "
            f"interval around the wrong value, covering {100 * d['cov']['judge']:.1f} percent of the time. <bookmark "
            f"mark='c'/> The {d['n']} human labels alone are unbiased, and wide: {100 * d['width']['human']:.1f} points. "
            f"<bookmark mark='d'/> Prediction-powered inference uses both, covers {100 * d['cov']['ppi']:.1f} percent of the "
            f"time, and its interval, {100 * d['width']['ppi']:.1f} points, is "
            f"{100 * (1 - d['width']['ppi'] / d['width']['human']):.0f} percent narrower than the humans' alone. The judge's "
            f"labels were worth something after all, once their bias was measured."
        ) as vo:
            self.play(FadeIn(A), Create(truth), FadeIn(seeded_tag()))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), FadeIn(note_))
        self.wait(1.0)
        self.clear_scene()

    def dsl(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The same idea in regression. <bookmark mark='b'/> Social scientists now use language "
            "models to code documents, such as whether a speech is populist, and then regress the codes on covariates. "
            "<bookmark mark='c'/> Naoki Egami, Musashi Hinck, Brandon Stewart and Hanying Wei's design-based supervised "
            "learning, in 2023, has experts code a random subsample with known probabilities, and combines the expert and "
            "model codes in a doubly robust pseudo-outcome: Part thirty-six's AIPW, with the expert labels as the "
            "treatment. <bookmark mark='d'/> Valid coefficients and intervals, whatever the model's coding errors, as long as "
            "the subsample is random and its probabilities known.",
            [(r"\text{task}", r":", r"\text{regress model-made codes}", 40),
             (r"\text{DSL}", r":", r"\text{experts code a random subsample}", 40),
             (r"\tilde Y", r"=", r"\hat Y + \frac{R}{\pi}(Y - \hat Y)", 40),
             (r"\text{valid}", r":", r"\text{if } \pi \text{ is known}", 40)],
            [r"computational social science", r"Egami et al. (2023)", r"Part 36's AIPW", r"design, \ not modelling"],
            colors=[(2, HONC)])

    def cautions(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Two cautions. <bookmark mark='b'/> The human labels must be a random sample of the same "
            "answers; humans grading only the hard cases break the design. <bookmark mark='c'/> And the human labels "
            "themselves are measurements, with their own disagreement: the target is what a person would say, not the "
            "truth. <bookmark mark='d'/> When people disagree, report their agreement, for example by Jacob Cohen's kappa, and treat the "
            "rate at which people agree as a ceiling on any judge.",
            [(r"\text{design}", r":", r"\text{a random human subsample}", 40),
             (r"\text{humans}", r":", r"\text{also measurements}", 40),
             (r"\text{estimand}", r":", r"\text{what a person would say}", 40),
             (r"\text{report}", r":", r"\text{inter-rater agreement}", 40)],
            [r"Part 18", r"Part 41", r"say it", r"Cohen's kappa (1960)"],
            colors=[(0, HONC)])
