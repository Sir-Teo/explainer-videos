from __future__ import annotations

import numpy as np

from videos.stats.stats19.common import *  # noqa: F403
from videos.stats.stats19.compute import truth_curve


class PredictionError(VoiceoverScene):
    def construct(self):
        self.card()
        self.goal()
        self.fits()
        self.curves()
        self.noise()
        self.optimism()
        self.mallows()
        self.lessons()

    def card(self):
        card = chapter_card(1, r"Prediction error", r"Fitting the past is not predicting the future", part=PART)
        with self.voiceover("Chapter one. Prediction error."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def goal(self):
        rows = [
            cmath(r"\text{data}", r":", r"(x_1, y_1), \ldots, (x_n, y_n)\ \to\ \text{a rule } \hat f", font_size=30),
            cmath(r"\text{training error}", r"=", r"\tfrac1n \textstyle\sum_i \big(y_i - \hat f(x_i)\big)^2", font_size=30),
            cmath(r"\text{test error}", r"=", r"E\big[(Y - \hat f(X))^2\big]\ \ \text{for a new } (X, Y)", font_size=30),
            cmath(r"\text{the gap}", r":", r"\text{training error is optimistic}", font_size=30),
        ]
        rows[2][2].set_color(TEST)
        whys = [why(r"fit a rule to the examples"), why(r"how well it fits the examples it learned from"),
                why(r"how well it predicts the next case: \ what we want"), why(r"Part 16's optimism, \ in general")]
        intro = label('Judge a fitted rule using independent prediction performance', font_size=36)
        with self.voiceover(
            "<bookmark mark='a'/> Prediction starts from examples: pairs of inputs and outputs, from which we build a"
            " rule that predicts y from x. <bookmark mark='b'/> The training error measures how well the rule fits "
            "the examples it was built from. <bookmark mark='c'/> The test error measures what we actually care "
            "about: how well it predicts a new case, drawn from the same source, that it hasn't seen. <bookmark "
            "mark='d'/> For familiar fitting procedures, training error is optimistic on average. An individual test "
            "set can score better or worse, and the direction is not a universal property of every possible rule."
        ) as vo:
            intro.scale_to_fit_width(min(intro.width, 12.5))
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def fits(self):
        d = load("poly")
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        grid = np.asarray(d["grid"])
        A = axes([0, 1], [-1.6, 2.2], x_length=8.4, y_length=4.6, xlabel=r"$x$", ylabel=r"$y$", xticks=[0, 0.5, 1],
                 yticks=[-1, 0, 1, 2], center=[-1.4, 0.2, 0])
        ax = A.ax
        dots = scatter(ax, x, y, color=DATA, radius=0.07)
        tr = series_line(ax, grid, truth_curve(grid), S.TRUTH, 2.5, 0.7)
        cols = {"1": TRAIN, "3": HIT, "5": OBS, "12": RES}
        curves = {k: series_line(ax, grid, np.asarray(v), cols[k], 3) for k, v in d["fits"].items()}
        rows = fit_rows(VGroup(
            label(r"30 points from a known curve, \ plus noise", font_size=22),
            label(r"gold: \ the truth", font_size=22, color=S.TRUTH),
            label(r"degree 1: \ too stiff", font_size=22, color=TRAIN),
            label(r"degree 3: \ about right", font_size=22, color=HIT),
            label(r"degree 5: \ a little wiggly", font_size=22, color=OBS),
            label(r"degree 12: \ chases every point", font_size=22, color=RES),
        ), 4.0, 0.36, [5.0, 0.2, 0])
        tag = simulated_tag(r"$y = \sin 2\pi x + x/2 + N(0, 0.3^2)$", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> A small experiment where we know the truth: thirty points from a smooth curve, plus noise. "
            "<bookmark mark='b'/> The true curve is the gold one. Now fit polynomials by least squares. <bookmark mark='c'/> A "
            "straight line is too stiff: it misses the wave entirely. <bookmark mark='d'/> A cubic follows the truth closely. "
            "<bookmark mark='e'/> Degree five begins to wiggle. <bookmark mark='f'/> And degree twelve threads its way through "
            "the points, bending wildly between them and at the ends. It fits the thirty examples better than any of the "
            "others, and it would predict new points worst."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(dots), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(tr), FadeIn(rows[1]))
            for k, (m_, deg) in enumerate(zip("cdef", ("1", "3", "5", "12"))):
                vo.wait_until(m_)
                self.play(Create(curves[deg]), FadeIn(rows[k + 2]), run_time=1.4)
        self.clear_scene()

    def curves(self):
        d = load("poly")
        tr, te = np.log10(np.asarray(d["train"])), np.log10(np.asarray(d["test"]))
        deg = np.arange(1, 15)
        A = axes([0.5, 14.5], [-1.6, 1.0], x_length=8.4, y_length=4.4, xlabel=r"polynomial degree", ylabel=r"mean squared error",
                 xticks=[1, 3, 5, 7, 9, 11, 13], yticks=[-1.5, -1, -0.5, 0, 0.5, 1], center=[-1.4, 0.3, 0],
                 yfmt=lambda v: f"{10 ** v:.2g}")
        ax = A.ax
        ct = polyline(ax, deg, tr, TRAIN, 3.5)
        cte = polyline(ax, deg, te, TEST, 3.5)
        noise = DashedLine(ax.c2p(0.5, np.log10(d["noise"])), ax.c2p(14.5, np.log10(d["noise"])), color=GREY_B, stroke_width=2)
        best = int(np.argmin(d["test"])) + 1
        rows = fit_rows(VGroup(
            label(r"training error: \ falls with every degree", font_size=22, color=TRAIN),
            label(r"test error, \ 5,000 new points: \ falls, \ then soars", font_size=22, color=TEST),
            MathTex(rf"\text{{best test error: degree }} {best},\ {min(d['test']):.3f}", font_size=26, color=HIT),
            label(r"dashed: \ the noise variance, \ 0.09: \ no rule can beat it", font_size=20, color=GREY_B),
            label(r"degree 14: \ training 0.04, \ test 346", font_size=20, color=RES),
        ), 3.45, 0.38, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here are the two errors for every degree from one to fourteen, on a log scale. The "
            "training error falls every time: more flexibility always fits the examples better. <bookmark mark='b'/> "
            "The test error, measured on five thousand fresh points, falls at first, then turns and soars. <bookmark "
            "mark='c'/> It's smallest at degree three, point one oh. <bookmark mark='d'/> The dashed line is the "
            "noise variance, point oh nine: the unpredictable part, which no rule can remove. The cubic is close to "
            "it. <bookmark mark='e'/> At degree fourteen, the training error is point oh four, below the noise, as "
            "can happen even for a well-specified fitted model, and the test error is three hundred and forty-six."
        ) as vo:
            self.play(FadeIn(A), Create(noise))
            vo.wait_until("a")
            self.play(Create(ct), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cte), FadeIn(rows[1]), run_time=2.0)
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def noise(self):
        rows = [
            cmath(r"Y", r"=", r"f(X) + \varepsilon,\ \ E[\varepsilon\mid X] = 0,\ \mathrm{Var}\,\varepsilon = \sigma^2", font_size=30),
            cmath(r"E\big[(Y - \hat f(x))^2\big]", r"=", r"\sigma^2 + E\big[(f(x) - \hat f(x))^2\big]", font_size=30),
            cmath(r"\sigma^2", r":", r"\text{irreducible}", font_size=30),
            cmath(r"\text{training error} < \sigma^2", r":", r"\text{possible even for a well-specified fitted model}", font_size=30),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"a signal plus noise"), why(r"the cross term vanishes: \ new noise is independent"),
                why(r"the floor for every rule"), why(r"assess overfitting using independent prediction performance")]
        intro = label('Expected prediction error includes irreducible noise', font_size=36)
        with self.voiceover(
            "<bookmark mark='a'/> Why is there a floor? Think of y as a signal f of x plus independent, mean-zero "
            "noise with conditional variance sigma squared at every input. <bookmark mark='b'/> The expected error at"
            " a point splits into the noise variance plus the squared distance between the rule and the true signal, "
            "because the new point's noise is independent of everything the rule learned. <bookmark mark='c'/> The "
            "first term is irreducible. <bookmark mark='d'/> Fitting uses some of the training noise, so training "
            "error can fall below the noise variance even without excessive flexibility. That alone does not "
            "establish harmful overfitting; new-data performance is what matters."
        ) as vo:
            intro.scale_to_fit_width(min(intro.width, 12.5))
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def optimism(self):
        d = load("cp")
        rows = [
            cmath(r"E[\text{test}] - E[\text{train}]", r"=", r"\tfrac{2}{n} \textstyle\sum_i \mathrm{Cov}(\hat y_i, y_i)", font_size=30),
            cmath(r"\text{for least squares with } p \text{ terms}", r"=", r"2\sigma^2 p / n", font_size=30),
            cmath(r"C_p", r"=", r"\text{train} + 2\hat\sigma^2 p / n", font_size=32),
            cmath(r"\text{the cubic approximation}", r":", rf"\text{{train}} = {d['train'][2]:.3f} < \sigma^2 = {d['sigma2']:.2f}", font_size=30),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"Efron (1986, 2004): \ the covariance penalty"), why(r"the trace of the hat matrix: \ Part 12"),
                why(r"Mallows (1973); \ AIC is its likelihood cousin"), why(r"it fits a share $p/n$ of the noise")]
        intro = label('The covariance penalty compares responses at fixed inputs', font_size=36)
        with self.voiceover(
            "How optimistic is the training error, exactly? <bookmark mark='a'/> Bradley Efron's covariance formula "
            "answers: for fresh independent responses at the same fixed training inputs, the expected gap between "
            "prediction and training error is two over n times the sum of the covariances between each fitted value "
            "and its own observation. A rule that follows its data closely has large covariances. <bookmark "
            "mark='b'/> For least squares with p terms, the sum is sigma squared times the trace of the hat matrix, "
            "which is p, so the optimism is two sigma squared p over n. <bookmark mark='c'/> Add it back and you have"
            " Colin Mallows' C p, from 1973: an estimate of same-input prediction error from the training data alone."
            " This is a Cp-style risk score; the traditional dimensionless Cp uses a different rescaling. Akaike's "
            "information criterion is the same idea for likelihoods. <bookmark mark='d'/> It also sharpens the "
            "warning sign of a moment ago: even the well-performing cubic approximation, has training error point oh "
            "seven one, below the noise variance, because fitting four coefficients absorbs noise. The true signal "
            "here is sinusoidal, so the cubic also has approximation error."
        ) as vo:
            intro.scale_to_fit_width(min(intro.width, 12.5))
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def mallows(self):
        d = load("cp")
        lg = lambda v: np.log10(np.asarray(v, float))
        deg = np.asarray(d["deg"])
        A = axes([0.5, 14.5], [-1.6, 1.0], x_length=8.4, y_length=4.4, xlabel=r"polynomial degree", ylabel=r"mean squared error",
                 xticks=[1, 3, 5, 7, 9, 11, 13], yticks=[-1.5, -1, -0.5, 0, 0.5, 1], center=[-1.4, 0.3, 0],
                 yfmt=lambda v: f"{10 ** v:.2g}")
        ax = A.ax
        ct = polyline(ax, deg, lg(d["train"]), TRAIN, 3)
        cte = polyline(ax, deg, lg(d["test"]), TEST, 3)
        ccp = polyline(ax, deg, lg(d["cp"]), OBS, 4)
        fixed = polyline(ax, deg, lg(d['fixed_design_expected_risk']), S.CTRL, 3)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=OBS) for a, b in zip(deg, lg(d["cp"]))])
        rows = fit_rows(VGroup(
            label(r"green: \ training error", font_size=22, color=TRAIN),
            label(r"red: \ test error", font_size=22, color=TEST),
            label(r"gold: \ $C_p$, \ from the training data alone", font_size=22, color=OBS),
            MathTex(rf"\text{{both choose degree }} {d['cp_best']}", font_size=28, color=HIT),
            label(r"but $C_p$ misses the explosion:", font_size=22, color=RES),
            label(r"fixed training inputs versus new random inputs", font_size=20, color=RES),
            label(r"blue: expected risk at the same fixed inputs", font_size=20, color=S.CTRL),
        ), 3.45, 0.4, [5.1, 0.3, 0])
        intro = label('Covariance penalties target prediction at the training inputs', font_size=36).move_to([0, 3.2, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Here are the two curves again, <bookmark mark='b'/> with the Cp-style score in "
            "gold, computed from the thirty training points and the known noise variance. The blue curve is the exact"
            " expected risk at those same fixed inputs, averaged over new training noise and new response noise. "
            "<bookmark mark='c'/> It follows the test error at low degrees and chooses degree three, as the test "
            "error does. <bookmark mark='d'/> But it misses the explosion at high degree: the two curves target "
            "different predictions. The covariance penalty concerns fresh responses at the same fixed inputs; our red"
            " test curve uses new random inputs, including gaps between training points. High-degree polynomials can "
            "be unstable in those gaps. Even with a misspecified signal, the known-variance penalty is valid for the "
            "fixed-design linear projection. Cross-validation can assess new-case performance by holding out inputs "
            "as well as responses."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeIn(A), Create(ct), Create(cte), FadeIn(rows[0]), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(ccp), Create(fixed), FadeIn(dots), FadeIn(rows[2]), FadeIn(rows[6]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]), FadeIn(rows[5]))
        self.wait(1.0)
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"nested OLS spaces cannot increase minimum training error", font_size=24),
            label(r"this example has the classical U-shaped test curve", font_size=24, color=TEST),
            label(r"too stiff: \ underfitting; \ too flexible: \ overfitting", font_size=24, color=OBS),
            label(r"never judge a rule by how well it fits its own data", font_size=24, color=RES),
            label(r"next: \ why the U? \ bias and variance", font_size=24, color=HIT),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So: Within these nested, unpenalized least-squares polynomial spaces, extra terms "
            "cannot increase the minimum training error. <bookmark mark='b'/> This example has the classical U-shaped"
            " test curve. Other problems and fitting methods can have different shapes. <bookmark mark='c'/> On the "
            "left, rules too stiff to follow the signal underfit; on the right, rules flexible enough to follow the "
            "noise overfit. <bookmark mark='d'/> So never judge a prediction rule by how well it fits the data it "
            "learned from. <bookmark mark='e'/> Next: where the U comes from."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
