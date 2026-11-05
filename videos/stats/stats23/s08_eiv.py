from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats23.common import *  # noqa: F403


class EIV(VoiceoverScene):
    def construct(self):
        self.card()
        self.attenuation()
        self.fathers()
        self.board()
        self.hubble()
        self.which_line()
        self.simex()
        self.in_y()
        self.fixes()

    def card(self):
        card = chapter_card(7, r"Errors in variables", r"A noisy $x$ flattens the slope", lit=(1929,), part=PART)
        with self.voiceover("Chapter seven. Errors in variables."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def attenuation(self):
        rows = [
            cmath(r"y", r"=", r"\alpha + \beta x + \varepsilon, \ \ \text{but we see } w = x + u", font_size=30),
            cmath(r"\hat\beta_w", r"\to", r"\dfrac{\mathrm{Cov}(w, y)}{\mathrm{Var}(w)} = \beta\, \dfrac{\sigma_x^2}{\sigma_x^2 + \sigma_u^2}", font_size=30),
            cmath(r"\lambda", r"=", r"\sigma_x^2/(\sigma_x^2 + \sigma_u^2), \ \ \text{the reliability}", font_size=30),
            cmath(r"\text{more variables}", r":", r"\text{the bias spreads to the other coefficients}", font_size=28),
        ]
        rows[1][2].set_color(NOISY)
        whys = [why(r"$u$: \ measurement error, \ independent of everything"), why(r"the noise adds to $\mathrm{Var}(w)$, \ not to the covariance"),
                why(r"attenuation: \ always towards zero"), why(r"a noisy confounder leaves confounding behind")]
        with self.voiceover(
            "<bookmark mark='a'/> Part 12 assumed the predictors are measured exactly. Suppose instead we see w, the true x "
            "plus independent measurement error. <bookmark mark='b'/> The least squares slope converges to the covariance "
            "of w and y over the variance of w. The error adds to the variance but not to the covariance, so the slope is "
            "beta times a fraction, <bookmark mark='c'/> the reliability lambda, the share of w's variance that is real. "
            "The slope is attenuated, always towards zero, however large the sample. <bookmark mark='d'/> With several "
            "predictors the bias spreads: a confounder measured with error is only partly controlled for, and some of its "
            "effect is credited to the others, as Part 20 found with sodium."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fathers(self):
        d = load("eiv")
        zf, wf, zc = (np.asarray(d[k]) for k in ("fam_zf", "fam_wf", "fam_zc"))
        A = axes([-3.5, 3.5], [-3, 3], x_length=7.0, y_length=4.6, xlabel=r"father's height, \ standardized",
                 ylabel=r"child's height", xticks=[-3, -2, -1, 0, 1, 2, 3], yticks=[-2, 0, 2], center=[-2.0, 0.3, 0])
        ax = A.ax
        exact = VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=OLS_C, fill_opacity=0.7) for a, b in zip(zf, zc) if abs(a) < 3.5])
        noisy = VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=NOISY, fill_opacity=0.7) for a, b in zip(wf, zc) if abs(a) < 3.5])
        s1, s2 = d["slope_exact"], d["slope_noisy"]
        l1 = Line(ax.c2p(-3.5, -3.5 * s1), ax.c2p(3.5, 3.5 * s1), color=OLS_C, stroke_width=4)
        l2 = Line(ax.c2p(-3.5, -3.5 * s2), ax.c2p(3.5, 3.5 * s2), color=NOISY, stroke_width=4)
        rows = fit_rows(VGroup(
            label(r"500 of the World's families", font_size=22),
            label(rf"blue: \ exact heights, \ slope {s1:.3f}", font_size=22, color=OLS_C),
            label(rf"red: \ with error, \ reliability {d['reliability']}", font_size=22, color=NOISY),
            label(rf"its slope: \ {s2:.3f}", font_size=22, color=NOISY),
            label(rf"predicted: \ ${d['reliability']} \times {d['true_slope']:.3f} = {d['predicted']:.3f}$", font_size=22, color=GREY_A),
        ), 3.9, 0.42, [4.8, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Five hundred of the World's families: the child's height against the father's, both "
            "standardized. <bookmark mark='b'/> With exact heights the slope is point three six five; the whole World's is "
            "point three nine one. <bookmark mark='c'/> Now record each father's height with an error big enough that only "
            "sixty percent of the recorded variance is real, a fair description of self-reported heights or of a "
            "single blood pressure reading. The cloud spreads sideways. <bookmark mark='d'/> The slope falls to point two "
            "one seven. <bookmark mark='e'/> The formula predicted point six times point three nine one, point two three "
            "five."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(exact), Create(l1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(ReplacementTransform(exact, noisy), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(l2), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=23) if r.part == 23][4:5]
        b = coverage_board(rows, lit_part=23, placeholders=0, font_size=20, row_h=0.62)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> On the Board: a thousand samples of five hundred families with the noisy fathers. The "
            "usual ninety-five percent interval for the slope covers the World's true slope four times in a thousand. More "
            "data would make this worse, not better: the interval would shrink around the wrong value."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]))
        self.wait(1.0)
        self.clear_scene()

    def hubble(self):
        d = load("eiv")
        dist, vel = np.asarray(d["d"]), np.asarray(d["v"])
        A = axes([0, 2.2], [-400, 1200], x_length=8.0, y_length=4.6, xlabel=r"distance, \ megaparsecs",
                 ylabel=r"velocity, \ km/s", xticks=[0, 0.5, 1, 1.5, 2], yticks=[-250, 0, 250, 500, 750, 1000],
                 center=[-1.6, 0.3, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=GREY_A) for a, b in zip(dist, vel)])

        def line(a, b, col):
            return Line(ax.c2p(0, a), ax.c2p(2.2, a + 2.2 * b), color=col, stroke_width=3.5)

        ols = line(*d["ols"], OLS_C)
        rv = line(*d["reverse_line"], RES)
        dm = line(d["deming2"]["intercept"], d["deming2"]["slope"], GLS_C)
        rows = fit_rows(VGroup(
            label(r"Hubble's 24 nebulae, \ 1929", font_size=22),
            label(rf"blue: \ velocity on distance: \ {d['ols'][1]:.0f}", font_size=22, color=OLS_C),
            label(rf"red: \ distance on velocity: \ {d['reverse_slope']:.0f}", font_size=22, color=RES),
            label(rf"teal: \ Deming: \ {d['deming2']['slope']:.0f}", font_size=22, color=GLS_C),
            label(r"km/s per megaparsec", font_size=20, color=GREY_B),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The most famous regression with a noisy x. In 1929 Edwin Hubble plotted the recession "
            "velocities of twenty-four nebulae against their distances, and found that the farther a galaxy, the faster it "
            "recedes: the expanding universe. His distances were far noisier than his velocities. <bookmark mark='b'/> "
            "Regress velocity on distance: four hundred and fifty-four kilometres per second per megaparsec, attenuated by "
            "the noisy distances. <bookmark mark='c'/> Regress distance on velocity instead and invert: seven hundred and "
            "twenty-nine. The truth, if the errors were all in distance, would be nearer this one. <bookmark mark='d'/> "
            "Deming regression, which needs the ratio of the two error variances, here velocities good to a hundred "
            "kilometres per second and distances to twenty percent, lands between, at five hundred and eighty-two."
        ) as vo:
            self.add(hubble_tag())
            self.play(FadeIn(A), LaggedStart(*[FadeIn(x, scale=0.5) for x in dots], lag_ratio=0.05))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ols), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(rv), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(dm), FadeIn(rows[3]), FadeIn(rows[4]))
        self.clear_scene()

    def which_line(self):
        d = load("eiv")
        rows = [
            cmath(r"\text{Deming}", r":", r"\min \textstyle\sum \{(y_i - \hat y_i)^2 + \delta (w_i - \hat x_i)^2\}", font_size=30),
            cmath(r"\delta = 1", r":", rf"\text{{orthogonal regression, \ total least squares: \ }} {d['deming1']['slope']:.0f}", font_size=28),
            cmath(r"r = " + f"{d['r']:.2f}", r":", r"\text{OLS} \cdot \text{reverse slope}^{-1} = r^2", font_size=30),
            cmath(r"\text{the real error}", r":", rf"\text{{distances 7 times too small: \ today }} H_0 \approx {d['modern_H0']:.0f}", font_size=28),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"$\delta$: \ the ratio of the error variances"), why(r"the smallest singular vector of $[X\ y]$; \ not scale-free"),
                why(r"the two naive lines bracket the truth"), why(r"a calibration error: \ no regression fixes it")]
        with self.voiceover(
            "<bookmark mark='a'/> Deming regression minimizes errors in both directions, with delta, the ratio of the error "
            "variances, deciding how to trade them. <bookmark mark='b'/> With delta equal to one it's orthogonal regression, "
            "or total least squares, computed from the smallest singular vector of the data matrix; but here velocity and "
            "distance have different units, so one is an arbitrary choice and the answer is seven hundred and twenty-nine. "
            "<bookmark mark='c'/> The two naive slopes differ by a factor of r squared, and between them they bracket every "
            "answer the error ratio could give. <bookmark mark='d'/> And a humbling footnote. Hubble's distances weren't "
            "just noisy, they were systematically too small, by a factor of about seven, because of a mistaken calibration "
            "of the stars he used as yardsticks. Today's value is about seventy. No regression method corrects an error "
            "that every observation shares."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def simex(self):
        d = load("eiv")
        lam = np.asarray(d["simex_lams"])
        sl = np.asarray(d["simex"])
        A = axes([-1.2, 2.2], [0, 0.45], x_length=8.0, y_length=4.2, xlabel=r"added error, \ in units of the existing error variance",
                 ylabel=r"slope", xticks=[-1, 0, 1, 2], yticks=[0, 0.1, 0.2, 0.3, 0.4], center=[-1.6, 0.3, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.08, color=NOISY) for a, b in zip(lam, sl)])
        gr = np.linspace(-1, 2, 100)
        q = curve(ax, gr, np.polyval(d["simex_quad"], gr), PATH, 3)
        est = Dot(ax.c2p(-1, d["simex_est"]), radius=0.1, color=PATH)
        tru = DashedLine(ax.c2p(-1.2, d["true_slope"]), ax.c2p(2.2, d["true_slope"]), color=TRUE, stroke_width=2)
        zero = DashedLine(ax.c2p(-1, 0), ax.c2p(-1, 0.42), color=GREY_C, stroke_width=1.5)
        rows = fit_rows(VGroup(
            label(r"red: \ the noisy data, \ then extra noise added", font_size=22, color=NOISY),
            label(r"each step: \ 200 simulations, \ averaged", font_size=22, color=GREY_A),
            label(r"amber: \ a quadratic, \ extrapolated to $-1$", font_size=22, color=PATH),
            label(rf"SIMEX: \ {d['simex_est']:.3f}; \ naive {d['slope_noisy']:.3f}", font_size=22, color=PATH),
            label(rf"gold: \ the World's {d['true_slope']:.3f}", font_size=22, color=TRUE),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> SIMEX, simulation-extrapolation, from John Cook and Leonard Stefanski in 1994, needs only the "
            "error variance. Take the noisy fathers and deliberately add more error, half as much again, then the same "
            "again, twice as much. <bookmark mark='b'/> Average the slope over two hundred simulations at each step: it falls "
            "steadily. <bookmark mark='c'/> Fit a curve through those slopes and extrapolate back to minus one, the "
            "imaginary point where the original error is removed too. <bookmark mark='d'/> The estimate is point three one "
            "three, from a naive point two one seven. <bookmark mark='e'/> The World's slope is point three nine one: SIMEX "
            "recovers most of the loss, and with a quadratic it typically under-corrects."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(A), Create(tru), Create(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x, scale=0.5) for x in dots], lag_ratio=0.3), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(q), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(est), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def in_y(self):
        rows = [
            cmath(r"y^{\text{obs}}", r"=", r"y + v", font_size=30),
            cmath(r"\hat\beta", r"\to", r"\beta: \ \text{no bias}", font_size=30),
            cmath(r"\text{but}", r":", r"\text{larger SEs, \ lower power}", font_size=30),
            cmath(r"\text{unless}", r":", r"v \text{ depends on } x \text{ (differential error)}", font_size=30),
        ]
        rows[1][2].set_color(HIT)
        whys = [why(r"error in the outcome"), why(r"it joins $\varepsilon$"), why(r"the price of a noisy outcome"),
                why(r"e.g. self-reports that vary by group")]
        with self.voiceover(
            "<bookmark mark='a'/> Error in the outcome is a different matter. If what we record is y plus independent noise, "
            "<bookmark mark='b'/> the noise simply joins the regression error, and the slope stays unbiased. "
            "<bookmark mark='c'/> The cost is precision: larger standard errors and less power. <bookmark mark='d'/> The "
            "exception is differential error, noise whose size or direction depends on the predictors, like self-reported "
            "weight that is understated more by some groups than by others; that biases everything."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fixes(self):
        rows = fit_rows(VGroup(
            label(r"know the reliability: \ regression calibration, \ Part 20", font_size=24, color=GLS_C),
            label(r"know the error ratio: \ Deming", font_size=24, color=GLS_C),
            label(r"an instrument correlated with $x$, \ not with $u$: \ IV, \ Part 37", font_size=24, color=OLS_C),
            label(r"simulate more error and extrapolate back: \ SIMEX (Cook \& Stefanski 1994)", font_size=24, color=TEAL),
            label(r"and the whole subject: \ Part 41", font_size=24, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "Every cure needs information from outside the regression itself. <bookmark mark='a'/> If repeated measurements "
            "give the reliability, divide by it: Part 20's regression calibration. <bookmark mark='b'/> If you know the ratio "
            "of error variances, use Deming. <bookmark mark='c'/> If you have an instrument, something correlated with the "
            "true x but not with the measurement error, use instrumental variables, Part 37. <bookmark mark='d'/> SIMEX adds "
            "extra simulated error in steps, watches the slope shrink, and extrapolates back to no error at all. "
            "<bookmark mark='e'/> Part 41 treats measurement error in full."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
