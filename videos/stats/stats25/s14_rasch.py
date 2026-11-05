from __future__ import annotations

import numpy as np
from scipy import special

from videos.stats.stats25.common import *  # noqa: F403


class Rasch(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.curves()
        self.recovery()
        self.abilities()
        self.information()
        self.beyond()

    def card(self):
        card = chapter_card(13, r"Item response theory", r"Exams as mixed models", lit=(1960,), part=PART)
        with self.voiceover("Chapter thirteen. Item response theory."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def model(self):
        rows = [
            cmath(r"\mathrm{logit}\,P(y_{pi} = 1)", r"=", r"\theta_p - b_i", font_size=32),
            cmath(r"\theta_p \sim N(0, \sigma^2)", r":", r"\text{persons random; \ items fixed}", font_size=30),
            cmath(r"\text{sufficiency}", r":", r"\text{the raw score } \textstyle\sum_i y_{pi} \text{ carries all about } \theta_p", font_size=28),
            cmath(r"\text{2PL}", r":", r"\mathrm{logit}\,P = a_i(\theta_p - b_i), \ \text{items discriminate}", font_size=28),
        ]
        rows[0][2].set_color(SHRUNK)
        whys = [why(r"Rasch (1960): \ ability minus difficulty"), why(r"a GLMM: \ chapter ten's machinery"),
                why(r"`specific objectivity'"), why(r"Birnbaum (1968)")]
        with self.voiceover(
            "<bookmark mark='a'/> In 1960 the Danish mathematician Georg Rasch proposed that the log odds of a person "
            "answering an exam question correctly is the person's ability minus the question's difficulty. "
            "<bookmark mark='b'/> Treat the persons as a sample, with abilities drawn from a normal, and the items as fixed, "
            "and it is a logistic mixed model, fitted by chapter ten's machinery. <bookmark mark='c'/> A special property: "
            "a person's raw score, the number of correct answers, is a sufficient statistic for their ability, so persons "
            "can be compared without reference to which items were used, what Rasch called specific objectivity. "
            "<bookmark mark='d'/> Allan Birnbaum's two-parameter model lets items also differ in how sharply they "
            "discriminate."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def curves(self):
        d = load("rasch")
        b = np.asarray(d["diff_true"])
        A = axes([-4, 4], [0, 1], x_length=7.6, y_length=4.4, xlabel=r"ability $\theta$", ylabel=r"P(correct)",
                 xticks=[-4, -2, 0, 2, 4], yticks=[0, 0.5, 1], center=[-1.8, 0.3, 0])
        ax = A.ax
        th = np.linspace(-4, 4, 200)
        cols = color_gradient([BLUE, PATH, RED], len(b))
        cs = VGroup(*[curve(ax, th, special.expit(th - bi), c, 2.2) for bi, c in zip(b, cols)])
        half = DashedLine(ax.c2p(-4, 0.5), ax.c2p(4, 0.5), color=GREY_C, stroke_width=1.5)
        rows = fit_rows(VGroup(
            label(r"15 items: \ one curve each", font_size=22),
            label(r"blue: \ easy; \ red: \ hard", font_size=22, color=GREY_A),
            label(r"each item's difficulty: \ where its curve crosses $\tfrac12$", font_size=22, color=PATH),
            label(r"Rasch: \ the same slope for every item", font_size=22, color=GREY_A),
        ), 4.2, 0.42, [4.7, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A simulated exam of fifteen questions, each with its item characteristic curve: the chance "
            "of a correct answer as ability rises. <bookmark mark='b'/> Easy questions in blue, hard ones in red. "
            "<bookmark mark='c'/> An item's difficulty is the ability at which its curve crosses one half. "
            "<bookmark mark='d'/> In Rasch's model the curves are parallel, shifted copies of one logistic."
        ) as vo:
            self.play(FadeIn(A), Create(half))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in cs], lag_ratio=0.1), FadeIn(rows[0]), run_time=2.5)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def recovery(self):
        d = load("rasch")
        bt, bh, se = np.asarray(d["diff_true"]), np.asarray(d["diff_hat"]), np.asarray(d["se"])
        A = axes([-2.4, 2.4], [-2.4, 2.4], x_length=4.8, y_length=4.8, xlabel=r"true difficulty", ylabel=r"estimated",
                 xticks=[-2, 0, 2], yticks=[-2, 0, 2], center=[-3.0, 0.1, 0])
        ax = A.ax
        diag = DashedLine(ax.c2p(-2.4, -2.4), ax.c2p(2.4, 2.4), color=GREY_B, stroke_width=1.5)
        bars = VGroup(*[Line(ax.c2p(a, b - 1.96 * s), ax.c2p(a, b + 1.96 * s), color=PATH, stroke_width=2) for a, b, s in zip(bt, bh, se)])
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=PATH) for a, b in zip(bt, bh)])
        rows = fit_rows(VGroup(
            label(rf"{d['P']} persons $\times$ {d['I']} items, \ Laplace", font_size=22),
            label(rf"difficulties: \ correlation {np.corrcoef(bt, bh)[0, 1]:.3f} with the truth", font_size=22, color=PATH),
            label(rf"SEs about {np.median(se):.2f}: \ 200 answers per item", font_size=22, color=GREY_A),
            label(rf"ability SD: \ $\hat\sigma = {d['sigma']:.2f}$ \ (truth 1)", font_size=22, color=SHRUNK),
        ), 5.4, 0.42, [3.7, 0.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two hundred simulated test-takers answer all fifteen. <bookmark mark='b'/> The fitted "
            "difficulties fall on the diagonal, a correlation of point nine eight seven with the truth, <bookmark mark='c'/> "
            "with standard errors near point one eight from two hundred answers each. <bookmark mark='d'/> The spread of ability is "
            "estimated at point nine nine, against a true one."
        ) as vo:
            self.add(simulated_tag(r"simulated: \ a seeded example"))
            self.play(FadeIn(A), Create(diag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromCenter(x) for x in dots], lag_ratio=0.08), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(x) for x in bars], lag_ratio=0.05), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def abilities(self):
        d = load("rasch")
        sc, ah, at = np.asarray(d["raw_score"]), np.asarray(d["ability_hat"]), np.asarray(d["ability_true"])
        A = axes([-0.5, 15.5], [-3.2, 3.2], x_length=7.2, y_length=4.6, xlabel=r"raw score: \ correct answers out of 15",
                 ylabel=r"ability", xticks=[0, 5, 10, 15], yticks=[-3, 0, 3], center=[-2.0, 0.3, 0])
        ax = A.ax
        g = np.random.Generator(np.random.PCG64(60))
        jit = 0.35 * (g.random(len(sc)) - 0.5)
        tdots = VGroup(*[Dot(ax.c2p(s + j, np.clip(t, -3.2, 3.2)), radius=0.04, color=TRUE, fill_opacity=0.6) for s, j, t in zip(sc, jit, at)])
        order = np.argsort(sc)
        mline = polyline(ax, sc[order], ah[order], SHRUNK, 4)
        rows = fit_rows(VGroup(
            label(r"gold: \ each person's true ability", font_size=22, color=TRUE),
            label(r"green: \ the estimate, \ a function of the raw score alone", font_size=22, color=SHRUNK),
            label(rf"correlation with the truth: \ {np.corrcoef(at, ah)[0, 1]:.2f}", font_size=22),
            label(r"15 questions measure ability only roughly", font_size=22, color=RES),
            label(r"extreme scores are shrunk: \ 15 of 15 is not infinite ability", font_size=22, color=SHRUNK),
        ), 4.4, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> And the persons. In gold, each person's true ability against their raw score. "
            "<bookmark mark='b'/> In green, the model's estimate: a smooth function of the raw score alone, as sufficiency "
            "promised. <bookmark mark='c'/> Its correlation with the truth is point eight six: <bookmark mark='d'/> fifteen "
            "questions measure ability only roughly, which is why the gold cloud is so wide at each score. "
            "<bookmark mark='e'/> And the random-effects estimate is shrunk: a perfect score doesn't mean infinite ability, "
            "which is what fixed-effects maximum likelihood would say."
        ) as vo:
            self.add(simulated_tag(r"simulated: \ a seeded example"))
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in tdots], lag_ratio=0.005), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(mline), FadeIn(rows[1]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def beyond(self):
        rows = fit_rows(VGroup(
            label(r"PISA, \ the GRE, \ national exams: \ item response models", font_size=24, color=PATH),
            label(r"adaptive testing: \ ask the item most informative at the current $\hat\theta$", font_size=24),
            label(r"equating: \ put two forms of an exam on one scale", font_size=24),
            label(r"Part 64: \ the same model rates AI systems on benchmark questions", font_size=24, color=SHRUNK),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Item response models score international surveys like PISA and admissions tests like the "
            "GRE. <bookmark mark='b'/> Computerized adaptive tests choose each next question to be the most informative at "
            "the current ability estimate, so fewer questions are needed. <bookmark mark='c'/> And equating puts different "
            "versions of an exam on one scale through shared items. <bookmark mark='d'/> Part 64 uses the same model to rate "
            "AI systems by the benchmark questions they answer, separating how hard a question is from how good a system is."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def information(self):
        d = load("rasch")
        b = np.asarray(d["diff_true"])
        A = axes([-4, 4], [0, 4], x_length=7.4, y_length=4.4, xlabel=r"ability $\theta$", ylabel=r"information",
                 xticks=[-4, -2, 0, 2, 4], yticks=[0, 1, 2, 3, 4], center=[-1.9, 0.3, 0])
        ax = A.ax
        th = np.linspace(-4, 4, 300)
        P = special.expit(th[:, None] - b[None, :])
        items = VGroup(*[curve(ax, th, P[:, j] * (1 - P[:, j]), GREY_B, 1.4) for j in range(len(b))])
        info = (P * (1 - P)).sum(1)
        tot = curve(ax, th, info, PATH, 4)
        sem = curve(ax, th, np.minimum(1 / np.sqrt(info), 4), RES, 3)
        rows = fit_rows(VGroup(
            label(r"grey: \ each item's information $p(1 - p)$", font_size=22, color=GREY_B),
            label(rf"yellow: \ the test's, \ the sum: \ peak {info.max():.1f}", font_size=22, color=PATH),
            label(r"red: \ the SE of $\hat\theta$, \ $1/\sqrt{I(\theta)}$", font_size=22, color=RES),
            label(r"precise in the middle; \ poor at the extremes", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> How precisely does the exam measure? Each item's Fisher information about ability is p "
            "times one minus p, largest for people for whom the item is a coin flip. <bookmark mark='b'/> The test's "
            "information is the sum, peaking at about two point nine in the middle of the difficulties. "
            "<bookmark mark='c'/> One over its square root is the standard error of an ability estimate, about point five nine "
            "at best, <bookmark mark='d'/> and much worse for the very able and the struggling, whom no item challenges. "
            "Test designers shape this curve by choosing items."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in items], lag_ratio=0.05), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(tot), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(sem), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
