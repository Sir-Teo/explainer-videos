from __future__ import annotations

import numpy as np

from videos.stats.stats21.common import *  # noqa: F403


class OptimAndInference(VoiceoverScene):
    def construct(self):
        self.card()
        self.curvature()
        self.picture()
        self.error_budget()
        self.sandwich()
        self.warnings()
        self.summary()

    def card(self):
        card = chapter_card(11, r"Optimization and inference", r"The shape of the peak is the uncertainty", part=PART)
        with self.voiceover("Chapter eleven. Optimization, and inference."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def curvature(self):
        d = load("inference")
        se, bs = d["se"], d["boot_se"]
        rows = [
            cmath(r"\hat J", r"=", r"-\nabla^2 \ell(\hat\theta), \ \text{the observed information}", font_size=30),
            cmath(r"\widehat{\mathrm{Var}}(\hat\theta)", r"\approx", r"\hat J^{-1}", font_size=30),
            cmath(r"\text{the vote, \ slope}", r":", rf"\text{{SE}} = {se[1]:.3f}\ \ (\text{{bootstrap}}\ {bs:.3f})", font_size=30),
            cmath(r"\text{Newton}", r":", r"\text{its last Hessian is } -\hat J: \ \text{the SEs come free}", font_size=28),
        ]
        rows[1][2].set_color(NEWT)
        whys = [why(r"the curvature at the top"), why(r"sharp peak: \ small variance; \ Part 9"),
                why(r"2,000 adults, \ per $\log_{10}$ income"), why(r"Fisher scoring: \ the expected information")]
        with self.voiceover(
            "The optimizer doesn't just find the estimate; it measures its uncertainty. <bookmark mark='a'/> At the maximum, "
            "the negative Hessian of the log likelihood is the observed information, <bookmark mark='b'/> and its inverse "
            "estimates the variance of the estimator: a sharply curved peak means a precise estimate, a flat one an uncertain "
            "estimate, as Part 9 showed in one dimension. <bookmark mark='c'/> For the World's vote, the slope's standard error "
            "from the curvature is point one eight three; a bootstrap gives point one nine six. <bookmark mark='d'/> And "
            "Newton's method computes that Hessian anyway, at every step: the standard errors cost nothing extra."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        c = load("convex")
        b, ll = np.asarray(c["b"]), np.asarray(c["logistic"])
        j = int(np.argmax(ll))
        h = (ll[j + 1] - 2 * ll[j] + ll[j - 1]) / (b[1] - b[0]) ** 2
        quad = ll[j] + 0.5 * h * (b - b[j]) ** 2
        se = 1 / np.sqrt(-h)
        lo = float(ll[j] - 8)
        A = axes([b[j] - 0.6, b[j] + 0.6], [lo, float(ll[j]) + 0.8], x_length=8.0, y_length=4.4, xlabel=r"slope $\beta$",
                 ylabel=r"log likelihood", xticks=[round(b[j] - 0.5, 2), round(b[j], 2), round(b[j] + 0.5, 2)], center=[-1.6, 0.3, 0])
        ax = A.ax
        m = (b > b[j] - 0.6) & (b < b[j] + 0.6) & (ll > lo)
        cv = curve(ax, b[m], ll[m], FIT, 3.5)
        mq = (b > b[j] - 0.6) & (b < b[j] + 0.6) & (quad > lo)
        qv = curve(ax, b[mq], quad[mq], PATH, 2.5)
        bar = Line(ax.c2p(b[j] - 1.96 * se, ll[j] - 1.92), ax.c2p(b[j] + 1.96 * se, ll[j] - 1.92), color=TRUE, stroke_width=5)
        rows = fit_rows(VGroup(
            label(r"800 adults, \ per SD of log income", font_size=22),
            label(r"blue: \ the log likelihood; \ gold: \ its quadratic at the top", font_size=22, color=PATH),
            label(rf"curvature $\to$ SE {se:.3f}", font_size=24, color=NEWT),
            label(r"the bar: \ $\pm 1.96$ SE, \ 1.92 below the top", font_size=22, color=TRUE),
            label(r"the likelihood-ratio interval uses the blue curve itself", font_size=20, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's what that means in a picture: chapter one's logistic log likelihood for the slope, "
            "near its peak. <bookmark mark='b'/> In gold, the quadratic Newton fits at the top. <bookmark mark='c'/> Its "
            "curvature gives the standard error. <bookmark mark='d'/> The ninety-five percent Wald interval is where the "
            "quadratic has fallen by one point nine two, half of three point eight four, the chi-squared critical value. "
            "<bookmark mark='e'/> Using the real curve instead of its quadratic gives the likelihood-ratio interval, which is "
            "better when the two disagree. Part 22 goes deeper."
        ) as vo:
            self.play(FadeIn(A), Create(cv), FadeIn(rows[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(qv), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(bar), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def error_budget(self):
        d = load("inference")
        e = np.maximum(np.asarray(d["opt_err"]), 1e-8)
        ks = np.arange(1, len(e) + 1) * 10
        se = d["se"][1]
        A = axes([1, np.log10(ks[-1])], [-6, 1], x_length=8.4, y_length=4.2, xlabel=r"gradient-ascent iterations (log scale)",
                 ylabel=r"$|\beta_k - \hat\beta|$ (log$_{10}$)", xticks=[1, 2, 3], yticks=[-6, -4, -2, 0], center=[-1.4, 0.3, 0],
                 xfmt=lambda v: f"{10 ** v:,.0f}")
        ax = A.ax
        ln = polyline(ax, np.log10(ks), np.clip(np.log10(e), -6, 1), GRAD, 3.5)
        sl = DashedLine(ax.c2p(1, np.log10(se)), ax.c2p(np.log10(ks[-1]), np.log10(se)), color=TRUE, stroke_width=2.5)
        sl10 = DashedLine(ax.c2p(1, np.log10(se / 10)), ax.c2p(np.log10(ks[-1]), np.log10(se / 10)), color=HIT, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"red: \ optimization error, \ gradient ascent", font_size=22, color=GRAD),
            label(rf"gold: \ the statistical error, \ SE {se:.3f}", font_size=22, color=TRUE),
            label(rf"green: \ SE/10, \ reached after {d['first_below']:,} iterations", font_size=22, color=HIT),
            label(r"below that: \ more digits of a number known to $\pm 0.18$", font_size=22, color=GREY_A),
            label(r"Bottou \& Bousquet (2008): \ stop at the statistical error", font_size=20, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> That gives a natural place to stop. Here's gradient ascent's distance from the exact maximum, "
            "falling as it runs. <bookmark mark='b'/> In gold, the estimate's standard error: the size of its statistical "
            "uncertainty. <bookmark mark='c'/> Once the optimization error is a tenth of that, after about a thousand "
            "iterations here, it's negligible beside the statistical error: the two add in quadrature, so it changes the total "
            "by half a percent. <bookmark mark='d'/> Going further computes more digits of a number we only know to plus or "
            "minus point one eight. <bookmark mark='e'/> Léon Bottou and Olivier Bousquet made this trade-off precise for large "
            "data in 2008: with a fixed computing budget, it's better to use more data with a sloppier optimizer than less data "
            "optimized perfectly."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(sl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(sl10), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def sandwich(self):
        d = load("sandwich")
        rows = [
            cmath(r"\text{curvature}", r":", r"A = -\nabla^2 \ell(\hat\theta)", font_size=30),
            cmath(r"\text{spread of the scores}", r":", r"B = \textstyle\sum_i \nabla \ell_i \nabla \ell_i'", font_size=30),
            cmath(r"\text{sandwich}", r":", r"\widehat{\mathrm{Var}} = A^{-1} B A^{-1}", font_size=30),
            cmath(r"\text{the vote, \ no age or region}", r":", rf"{d['se_model']:.4f}\ \text{{vs}}\ {d['se_sandwich']:.4f}; \ \text{{true}}\ {d['sd_reps']:.4f}", font_size=28),
        ]
        rows[2][2].set_color(NEWT)
        whys = [why(r"what the optimizer measures"), why(r"how much each observation pulls"),
                why(r"$= A^{-1}$ only if the model is right"), why(r"400 samples of 2,000: \ here they agree")]
        with self.voiceover(
            "One warning before the next part. <bookmark mark='a'/> The curvature, A, gives the variance only if the model is "
            "right. <bookmark mark='b'/> In general we also need B, the spread of each observation's score, its pull on the "
            "estimate. <bookmark mark='c'/> The honest variance is the sandwich, A inverse B A inverse, which equals A inverse "
            "when the model holds. <bookmark mark='d'/> For the World's vote, modelled on income alone though age and region "
            "matter too, the curvature-based standard error is point zero five zero eight, the sandwich point zero five one "
            "three, and the actual spread over four hundred samples point zero four nine seven: here they agree. Part 22 shows "
            "a model wrong enough that they don't."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.78, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def warnings(self):
        rows = fit_rows(VGroup(
            label(r"a flat direction: \ a huge SE; \ perhaps a parameter the data cannot identify", font_size=24, color=RES),
            label(r"a long ridge: \ strongly correlated estimates \ (chapter five's intercept and slope)", font_size=24, color=OBS),
            label(r"the optimizer failing to converge: \ often the model is the problem", font_size=24, color=GRAD),
            label(r"separation in logistic regression: \ the maximum is at infinity", font_size=22, color=GREY_A),
            label(r"the optimizer's struggles are diagnostics", font_size=26, color=PATH),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The shape of the problem also warns us. A direction in which the likelihood is flat means a "
            "huge standard error, and perhaps a parameter the data simply can't identify. <bookmark mark='b'/> A long ridge, "
            "like chapter five's, means strongly correlated estimates, which centring the predictor would remove. "
            "<bookmark mark='c'/> An optimizer that won't converge is often a sign that the model, not the algorithm, is wrong. "
            "<bookmark mark='d'/> In logistic regression, if a predictor separates the outcomes perfectly, the maximum is at "
            "infinity, and the iterations march off forever. <bookmark mark='e'/> The optimizer's struggles are diagnostics."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def summary(self):
        rows = fit_rows(VGroup(
            label(r"estimate: \ the optimum", font_size=26, color=PATH),
            label(r"uncertainty: \ the curvature at the optimum", font_size=26, color=NEWT),
            label(r"accuracy needed: \ a fraction of the standard error", font_size=26, color=HIT),
            label(r"problems: \ read in the landscape's shape", font_size=26, color=OBS),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So: the estimate is the optimum; <bookmark mark='b'/> its uncertainty is the curvature there; "
            "<bookmark mark='c'/> the accuracy worth having is a fraction of that uncertainty; <bookmark mark='d'/> and the "
            "landscape's shape tells us when something is wrong."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
