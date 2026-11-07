from __future__ import annotations

import numpy as np

from videos.stats.stats54.common import *  # noqa: F403


class Surrogates(VoiceoverScene):
    def construct(self):
        self.card()
        self.losses()
        self.calibration()
        self.chart()
        self.noise_rates()
        self.probability()
        self.multiclass()

    def card(self):
        card = chapter_card(9, r"Classification-calibrated surrogates", r"Why minimizing the wrong loss is safe", lit=(2006,), part=PART)
        with self.voiceover("Chapter nine. Classification-calibrated surrogates: why minimizing the wrong loss is safe."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def losses(self):
        u = np.linspace(-2, 2.5, 200)
        A = axes([-2, 2.5], [0, 4], x_length=7.0, y_length=4.4, xlabel=r"margin $m = y f(x)$", ylabel=r"loss $\phi(m)$",
                 xticks=[-2, -1, 0, 1, 2], yticks=[0, 1, 2, 3, 4], center=[-2.7, 0.2, 0])
        ax = A.ax
        zo = VGroup(Line(ax.c2p(-2, 1), ax.c2p(0, 1), color=TRUTHC, stroke_width=4), Line(ax.c2p(0, 0), ax.c2p(2.5, 0), color=TRUTHC, stroke_width=4))
        hinge = clip_curve(ax, u, np.maximum(0, 1 - u), CLASSC, 4, ymin=0, ymax=4)
        logi = clip_curve(ax, u, np.log2(1 + np.exp(-u)), TESTC, 4, ymin=0, ymax=4)
        expo = clip_curve(ax, u, np.exp(-u), BADC, 4, ymin=0, ymax=4)
        sq = clip_curve(ax, u, (1 - u) ** 2, BOUNDC, 3, ymin=0, ymax=4)
        side = fit_rows(VGroup(
            label(r"white: \ $1\{m\le0\}$; general ERM can be hard", font_size=22, color=TRUTHC),
            label(r"gold: \ hinge $(1 - m)_+$ \ (SVM)", font_size=22, color=CLASSC),
            label(r"blue: \ logistic $\log_2(1 + e^{-m})$", font_size=22, color=TESTC),
            label(r"red: \ exponential $e^{-m}$ \ (AdaBoost)", font_size=22, color=BADC),
            label(r"purple: \ squared $(1 - m)^2$", font_size=22, color=BOUNDC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Zero-one loss is discontinuous; minimizing it over general families can be computationally hard. A step loss alone does not imply every class is hard. <bookmark mark='b'/> Many methods instead optimize a convex surrogate such as hinge loss. <bookmark mark='c'/> The blue logistic loss is in bits, using log base two, consistently with its psi transform. <bookmark mark='d'/> Exponential loss gives boosting. <bookmark mark='e'/> Squared margin loss is another surrogate. These losses upper-bound the displayed step with the chosen scaling, but optimization and statistical consistency are separate questions."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(zo), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(hinge), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(logi), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(expo), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(sq), FadeIn(side[4]))
        self.clear_scene()

    def calibration(self):
        rows = [
            cmath(r"\text{calibrated}", r":", r"\text{the surrogate's minimizer has the sign of } 2\eta(x) - 1", font_size=34),
            cmath(r"\phi\text{ convex, differentiable at }0", r":", r"\text{calibrated} \iff \phi'(0) < 0", font_size=36),
            cmath(r"\psi\big(R(f) - R^*\big)", r"\le", r"R_\phi(f) - R_\phi^*: \ \text{the } \psi\text{-transform}", font_size=34),
            cmath(r"\text{so}", r":", r"\text{surrogate excess} \to 0 \ \Rightarrow \ \text{0--1 excess} \to 0", font_size=34),
        ]
        rows[1][-1].set_color(GOODC)
        rows[2][-1].set_color(BOUNDC)
        whys = [why(r"the Bayes rule"), why(r"Bartlett, \ Jordan \& McAuliffe (2006)"), why(r"a quantitative link"), why(r"consistency transfers")]
        heading = label('Calibration transfers excess risk relative to unrestricted optima', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Binary classification calibration means that restricting a conditional score to the wrong sign increases the best attainable surrogate risk. <bookmark mark='b'/> For convex margin losses, calibration is equivalent to differentiability at zero with negative derivative there; differentiability is part of the condition. <bookmark mark='c'/> The psi inequality compares with the unrestricted measurable-score optimum. In a restricted model, approximation error must also be accounted for. <bookmark mark='d'/> Vanishing unrestricted surrogate excess implies vanishing classification excess. Merely minimizing within a misspecified class does not ensure Bayes consistency."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("surrogate")
        th = np.asarray(d["theta"])
        A = axes([0, 1.02], [0, 1.02], x_length=7.4, y_length=4.4, xlabel=r"excess 0--1 risk $\theta$", ylabel=r"$\psi(\theta)$: \ guaranteed surrogate excess",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.25, 0.5, 0.75, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"hinge": CLASSC, "logistic": TESTC, "exponential": BADC, "squared": BOUNDC}
        cs = {k: polyline(ax, th, d[k], c, 4) for k, c in cols.items()}
        side = fit_rows(VGroup(
            label(r"the $\psi$-transforms (Bartlett, \ Jordan \& McAuliffe)", font_size=22),
            label(r"gold: \ hinge, \ $\psi(\theta) = |\theta|$: \ linear", font_size=22, color=CLASSC),
            label(r"purple: \ squared, \ $\theta^2$; \ red: \ exponential, \ $1 - \sqrt{1 - \theta^2}$", font_size=22, color=BOUNDC),
            label(r"blue: \ logistic in bits; \ quadratic near 0", font_size=22, color=TESTC),
            label(r"quadratic $\psi$: \ excess 0--1 risk $\lesssim \sqrt{\text{surrogate excess}}$", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The psi functions themselves. <bookmark mark='b'/> For the hinge loss, psi of theta is the absolute value of theta: linear, so a surrogate excess of epsilon means a classification excess of at most epsilon. <bookmark mark='c'/> For the squared and exponential losses, psi is quadratic near zero, <bookmark mark='d'/> and so is the logistic loss's. <bookmark mark='e'/> A quadratic psi means the classification excess is at most a loss-dependent constant times the root of the surrogate excess: still consistent, but with a slower translation of rates, unless a noise condition from chapter four improves it."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cs["hinge"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cs["squared"]), Create(cs["exponential"]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cs["logistic"]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def noise_rates(self):
        rows = [
            cmath(r"\text{Tsybakov noise}", r":", r"P\big(|2\eta(X) - 1| \le t\big) \le C t^{\kappa}", font_size=34),
            cmath(r"R(f) - R^*", r"\le", r"c\,\big(R_\phi(f) - R_\phi^*\big)^{(1+\kappa)/(2+\kappa)}", font_size=36),
            cmath(r"\kappa = 0", r":", r"\text{square root, \ the worst case}; \ \ \kappa \to \infty \ (\text{Massart}): \ \text{linear}", font_size=34),
            cmath(r"\text{so}", r":", r"\text{a fast surrogate rate becomes a fast classification rate}", font_size=34),
        ]
        rows[1][-1].set_color(GOODC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"chapter 4's margin condition"), why(r"Bartlett, \ Jordan \& McAuliffe, \ Thm 3"), why(r"few points near the boundary"), why(r"rates transfer")]
        heading = label('A noise condition can improve the quadratic calibration rate', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> A Tsybakov noise condition can improve the conversion from surrogate excess to classification excess. <bookmark mark='b'/> For the quadratic calibration behaviour of squared, logistic or exponential loss, suitable conditional curvature bounds yield the displayed exponent. It is not a universal formula for every calibrated loss. <bookmark mark='c'/> Without a noise condition the conversion is square root; under a fixed Massart gap it can be linear. Hinge already has a linear conversion without this improvement. <bookmark mark='d'/> These compare with unrestricted optima. Learning rates still require controlling approximation, optimization and surrogate estimation errors."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def probability(self):
        rows = [
            cmath(r"\text{proper losses}", r":", r"\text{their minimizer is } \eta(x) \text{ itself, \ not just its sign}", font_size=34),
            cmath(r"\text{logistic}", r":", r"\text{log-odds: \ a probability model}", font_size=34),
            cmath(r"\text{hinge}", r":", r"\text{only } \mathrm{sign}(2\eta - 1): \ \text{SVMs give no probabilities}", font_size=34),
            cmath(r"\text{so}", r":", r"\text{for decisions with costs, \ use a proper loss (Part 34)}", font_size=34),
        ]
        rows[1][-1].set_color(GOODC)
        rows[2][-1].set_color(BADC)
        whys = [why(r"Part 34's scoring rules"), why(r"proper composite loss; \ finite-sample calibration is separate"), why(r"Platt scaling estimates a probability link"), why(r"costs change thresholds")]
        heading = label('Proper composite losses identify probabilities through a link', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> A strictly proper probability loss uniquely minimizes conditional expected loss at the true class probability. <bookmark mark='b'/> Logistic margin loss is proper composite: its score is the log odds, and the inverse link converts it to a probability. A finite sample or misspecified model need not be calibrated in probability. <bookmark mark='c'/> Hinge minimization primarily identifies a class sign; an SVM score is not itself a probability. Platt scaling can estimate a link on separate data, without an automatic calibration guarantee. <bookmark mark='d'/> Cost-sensitive decisions need suitable probability estimates or a method designed for the relevant decision threshold."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def multiclass(self):
        rows = fit_rows(VGroup(
            label(r"Calibrated losses for multiclass prediction", font_size=36, color=WHITE),
            label(r"multiclass hinge losses can be inconsistent \ (Tewari \& Bartlett 2007)", font_size=26, color=BADC),
            label(r"the multinomial logistic loss, \ cross-entropy, \ is calibrated", font_size=26, color=GOODC),
            label(r"and it estimates probabilities, \ not just labels: \ Part 34's calibration", font_size=26, color=TESTC),
            label(r"which is one reason deep networks are trained with cross-entropy", font_size=26, color=CLASSC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> With more than two classes, care is needed. <bookmark mark='b'/> Some natural multiclass "
            "versions of the hinge loss are not calibrated, as Ambuj Tewari and Bartlett showed in 2007. <bookmark "
            "mark='c'/> The multinomial logistic loss, cross-entropy, is. <bookmark mark='d'/> It also estimates the class "
            "probabilities themselves, not just the labels, which connects it to Part thirty-four's calibration. <bookmark "
            "mark='e'/> That is one reason deep networks are trained with cross-entropy."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
