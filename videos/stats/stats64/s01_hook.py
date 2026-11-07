from __future__ import annotations

import numpy as np

from videos.stats.stats64.common import *  # noqa: F403


class Hook(LectureMixin, VoiceoverScene):
    def construct(self):
        self.story()
        self.intervals()
        self.flips()
        self.everywhere()
        self.lesson()
        self.taxonomy()
        self.upgrade()
        self.objectives()

    def story(self):
        d = load("leaderboard")
        rows = fit_rows(VGroup(
            label(r"a constructed example: \ our model scores 85.2\%, \ the previous best 84.7\%", font_size=28, color=WHITE),
            label(r"a benchmark of 1{,}000 questions; \ a new state of the art", font_size=26, color=GREY_A),
            label(r"how much of that half point is the model, \ and how much the questions?", font_size=26, color=MODB),
        ), 12.4, 0.45, [0, 0.4, 0])
        tag = simulated_tag(r"simulated: \ no real model is scored in this part")
        with self.voiceover(
            "<bookmark mark='a'/> A familiar announcement. A new model scores 85.2 percent on a benchmark, against 84.7 percent for the previous best: a new state of the art. <bookmark mark='b'/> The benchmark has a thousand questions. <bookmark mark='c'/> How much of the half point is the model, and how much is the particular thousand questions that happened to be written? This part answers that question, and its relatives, for a field that now runs on leaderboards. The opening table is explicitly constructed for illustration; the remaining examples are seeded simulations or exact calculations. None evaluates a real system."
        ) as vo:
            self.play(FadeIn(tag))
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def intervals(self):
        d = load("leaderboard")
        pc = d["paired"]
        A = axes([0.80, 0.90], [0, 3], x_length=7.4, y_length=2.6, xlabel=r"accuracy on the benchmark", ylabel=r"",
                 xticks=[0.80, 0.82, 0.84, 0.86, 0.88, 0.90], xfmt=lambda v: f"{100 * v:.0f}\\%", center=[0.6, 0.6, 0])
        ax = A.ax
        lb = Leaderboard(ax, [r"new model", r"previous best"], [d["acc_a"], d["acc_b"]], [d["se_a"], d["se_b"]], colors=[MODB, MODA])
        rows = lb.rows(font_size=26)
        side = fit_rows(VGroup(
            label(rf"each: \ $\pm 1.96 \times$ {100 * d['se_a']:.1f} points: \ about $\pm$2.2", font_size=24, color=GREY_A),
            label(rf"the difference: \ {100 * pc['diff']:.1f} points, \ paired 95\% interval ({100 * pc['paired'][0]:.1f}, {100 * pc['paired'][1]:.1f})", font_size=24, color=MODB),
            label(rf"McNemar: \ {d['mcnemar']['n10']} vs {d['mcnemar']['n01']} discordant questions, \ $p = {d['mcnemar']['p']:.2f}$", font_size=24, color=NAIVEC),
        ), 12.4, 0.25, [0, -2.2, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Part eleven's error bars. A thousand yes-or-no questions at 85 percent give a standard "
            f"error of about {100 * d['se_a']:.1f} points, so each score is uncertain by about 2.2 points either way. "
            f"<bookmark mark='b'/> The intervals overlap almost entirely. <bookmark mark='c'/> The better question is about "
            f"the difference, on the same questions: half a point, with a paired ninety-five percent interval from "
            f"{100 * pc['paired'][0]:.1f} to {100 * pc['paired'][1]:.1f} points. <bookmark mark='d'/> Only the questions the "
            f"models disagree on carry information: {d['mcnemar']['n10']} that the new model got right and the old one wrong, "
            f"and {d['mcnemar']['n01']} the other way. McNemar's test gives p of {d['mcnemar']['p']:.2f}."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.wait(1.0)
        self.clear_scene()

    def flips(self):
        d = load("leaderboard")
        self.lad_voiceover(
            f"<bookmark mark='a'/> Another way to see it. Suppose the two models really are 85.2 and 84.7 percent accurate on "
            f"the population of questions the benchmark samples. <bookmark mark='b'/> Write a fresh thousand independent questions under this same latent-probit joint model, "
            f"and score both again. <bookmark mark='c'/> In {d['reps']:,} simulated re-writings, the previous best comes out "
            f"ahead {100 * d['flip']:.0f} percent of the time. <bookmark mark='d'/> A third of the time, the announcement "
            f"would have gone the other way. A leaderboard is an estimate, and its order is a random variable.",
            [(r"\text{truth}", r":", r"85.2\% \ \text{vs} \ 84.7\%", 40),
             (r"\text{re-write}", r":", r"\text{a fresh 1{,}000 questions}", 40),
             (r"P(\text{order flips})", r"\approx", rf"{d['flip']:.2f}", 40),
             (r"\text{so}", r":", r"\text{the ranking is a random variable}", 40)],
            [r"a population of questions", rf"{d['reps']:,} re-writings".replace(",", "{,}"), r"one in three", r"chapter 2"],
            colors=[(2, NAIVEC)])

    def everywhere(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> And the benchmark is the easy case. <bookmark mark='b'/> Arenas rank models by people's "
            "votes between pairs of answers: a logistic regression, Part twenty-four's. <bookmark mark='c'/> Labels are "
            "increasingly produced by other models, which makes them measurements with error, Part forty-one's. Training data "
            "is increasingly produced by models too, which feeds a fitted distribution back into its own fit. <bookmark "
            "mark='d'/> And when a model is deployed, its users interact, Part sixty-two's interference. Every lesson of the "
            "degree has a new home.",
            [(r"\text{benchmarks}", r":", r"\text{samples of questions}", 40),
             (r"\text{arenas}", r":", r"\text{Bradley--Terry regressions}", 40),
             (r"\text{labels and data}", r":", r"\text{from models}", 40),
             (r"\text{deployment}", r":", r"\text{interference}", 40)],
            [r"Parts 8 and 11", r"Part 24", r"Parts 34 and 41", r"Part 62"],
            colors=[(2, JUDGEC)])

    def lesson(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The thesis of this part is modest. <bookmark mark='b'/> Machine learning's evaluations "
            "are statistical estimates, made from samples, often reused, sometimes graded by machines. <bookmark mark='c'/> "
            "The tools to report them honestly already exist: clustered standard errors, paired designs, sandwich "
            "intervals, prediction-powered inference, conformal guarantees, randomized designs. <bookmark mark='d'/> What is "
            "new is the scale, and a few genuinely new questions, such as what happens when a model learns from its own "
            "output.",
            [(r"\text{evaluations}", r":", r"\text{statistical estimates}", 40),
             (r"\text{often}", r":", r"\text{reused, \ machine-graded}", 40),
             (r"\text{the tools}", r":", r"\text{already in the degree}", 40),
             (r"\text{new}", r":", r"\text{scale, \ and self-consumption}", 40)],
            [r"the thesis", r"the setting", r"Parts 11--58", r"chapter 7"],
            colors=[(2, HONC)])

    def taxonomy(self):
        self.list_voiceover(
            "<bookmark mark='a'/> The plan. <bookmark mark='b'/> Chapters one to five: benchmarks as samples, paired "
            "comparisons, arenas, item response theory, and the reuse of test sets. <bookmark mark='c'/> Chapters six to "
            "eight: labels from models, synthetic data and model collapse, and uncertainty for language models. <bookmark "
            "mark='d'/> Chapters nine to twelve: watermarks as tests, simulation-based inference, generative models as "
            "density estimators, and causal questions about deployments.",
            [('Questions about inference for modern AI systems', GREY_A),
             (r"1--5: \ benchmarks, \ pairs, \ arenas, \ IRT, \ test-set reuse", MODB),
             (r"6--8: \ model-made labels, \ model collapse, \ LLM uncertainty", JUDGEC),
             (r"9--12: \ watermarks, \ simulators, \ diffusion, \ deployments", HONC)], head_size=36)

    def upgrade(self):
        cards = [
            upgrade_card(11, r"an interval from $n$ independent observations", r"the questions are independent and used once",
                         r"chapters 1, 2, 5: \ clusters, \ pairs, \ and adaptive reuse"),
            upgrade_card(34, r"prediction-powered inference with a fixed model", r"the predictions are just data",
                         r"chapters 6--7: \ model-made labels, \ and models trained on models"),
        ]
        VGroup(*cards).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Two promises come due. Part eleven built intervals from independent observations, each "
            "used once; chapters one, two and five handle questions that cluster, models that share questions, and test sets "
            "used again and again. <bookmark mark='b'/> Part thirty-four treated a model's predictions as given data; "
            "chapters six and seven ask what happens when the labels, and then the training data, come from models."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 64", font_size=34, color=GREY_B), label(r"Statistics in the Age of AI", font_size=56)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"error bars for benchmarks; \ paired comparisons; \ arenas; \ IRT; \ reusable holdouts",
            r"model-judged labels with PPI; \ model collapse, \ derived; \ conformal factuality",
            r"watermarks as tests; \ calibration of simulators; \ diffusion's memorization",
            r"interference in deployments; \ four Board rows; \ open problems",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Parts 34, \ 57, \ 58").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.evals}, \ the leaderboard").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part sixty-four: statistics in the age of AI. <bookmark mark='b'/> Honest error bars for "
            "benchmarks; paired comparisons and the leaderboard's winner's curse; arenas as Bradley-Terry models; item "
            "response theory; reusable holdouts; model-judged labels; model collapse, derived and computed; conformal "
            "factuality; watermarks as hypothesis tests; calibrating simulators; memorization in diffusion models; "
            "experiments on deployed systems; and open problems."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
