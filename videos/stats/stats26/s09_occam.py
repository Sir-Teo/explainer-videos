from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats26.common import *  # noqa: F403


class Occam(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.fits()
        self.evidence()
        self.factor()
        self.lessons()

    def card(self):
        card = chapter_card(8, r"Occam's razor, \ built in", r"The evidence penalizes flexibility", lit=(1992,), part=PART)
        with self.voiceover("Chapter eight. Occam's razor, built in."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        A = axes([0, 10], [0, 0.5], x_length=7.4, y_length=4.0, xlabel=r"one-dimensional illustration; \ tails outside viewport",
                 ylabel=r"$p(y \mid \text{model})$", xticks=[], yticks=[], center=[-2.0, 0.3, 0])
        ax = A.ax
        xs = np.linspace(0, 10, 300)
        simple = stats.norm.pdf(xs,3.5,.9)
        flex = stats.norm.pdf(xs,5.,3.)
        c1 = curve(ax, xs, simple, SHRUNK, 3.5)
        c2 = curve(ax, xs, flex, RES, 3.5)
        obs = DashedLine(ax.c2p(3.8, 0), ax.c2p(3.8, 0.48), color=PATH, stroke_width=2.5)
        rows = fit_rows(VGroup(
            label(r"each model's probabilities sum to one", font_size=22),
            label(r"green: \ a simple model, \ few predictions, \ confident", font_size=22, color=SHRUNK),
            label(r"red: \ a flexible model, \ spread over everything", font_size=22, color=RES),
            label(r"yellow: \ data the simple model predicts", font_size=22, color=PATH),
            label(r"the simple model wins: \ it risked more", font_size=22, color=HIT),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Bayes factors carry a built-in Occam's razor, as David MacKay explained in 1992. "
            "Line up every data set that could possibly occur. Each model's predictions must sum to one over them. "
            "<bookmark mark='b'/> A simple model makes few, confident predictions: a tall narrow curve. <bookmark "
            "mark='c'/> In this illustration the flexible model's prior spreads its predictions more widely. "
            "Flexibility alone does not determine a model's prior predictive distribution. <bookmark mark='d'/> If "
            "the data land where the simple model predicted, <bookmark mark='e'/> it wins, even though the flexible "
            "one could fit them just as well, because it committed to them in advance. No penalty term was added: the"
            " razor is in the arithmetic of probability."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(obs), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def fits(self):
        d = load("occam")
        x, y, xx = np.asarray(d["x"]), np.asarray(d["y"]), np.asarray(d["xx"])
        A = axes([-1.05, 1.05], [-0.6, 2.2], x_length=7.4, y_length=4.4, xlabel=r"$x$", ylabel=r"$y$", xticks=[-1, 0, 1],
                 yticks=[0, 1, 2], center=[-2.0, 0.3, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=WHITE) for a, b in zip(x, y)])
        truth = DashedVMobject(curve(ax, xx, d["truth"], TRUE, 2.5), num_dashes=50)
        cols = {1: RAW, 3: SHRUNK, 8: RES}
        fits = {k: clip_curve(ax, xx, np.asarray(d["fits"][k]), cols[k], 3, ymin=-0.6, ymax=2.2) for k in (1, 3, 8)}
        rows = fit_rows(VGroup(
            label(r"20 points: \ a cubic plus noise, \ $\sigma = 0.25$", font_size=22),
            label(r"gold dashed: \ the truth", font_size=22, color=TRUE),
            label(r"blue: \ degree 1", font_size=22, color=RAW),
            label(r"green: \ degree 3", font_size=22, color=SHRUNK),
            label(r"red: \ degree 8, \ coefficients $\sim N(0, 1)$", font_size=22, color=RES),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A concrete case: twenty noisy points from a cubic curve. <bookmark mark='b'/> The gold "
            "dashed line is the truth. Fit Bayesian polynomial regressions, with each coefficient given a standard normal "
            "prior. <bookmark mark='c'/> A straight line misses the bends. <bookmark mark='d'/> A cubic follows them. "
            "<bookmark mark='e'/> A degree-eight polynomial follows them too, and wiggles a little more between the points. "
            "Which degree do the data support?"
        ) as vo:
            self.add(simulated_tag(r"simulated: \ a seeded example"))
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in dots], lag_ratio=0.05), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(truth), FadeIn(rows[1]))
            for k, m_ in zip((1, 3, 8), "cde"):
                vo.wait_until(m_)
                self.play(Create(fits[k]), FadeIn(rows[{1: 2, 3: 3, 8: 4}[k]]))
        self.clear_scene()

    def evidence(self):
        d = load("occam")
        degs = np.asarray(d["degs"])
        ev, ll = np.asarray(d["log_ev"]), np.asarray(d["max_ll"])
        A = axes([-0.6, 8.6], [-16, 8], x_length=7.4, y_length=4.4, xlabel=r"polynomial degree", ylabel=r"log scale",
                 xticks=list(range(9)), yticks=[-15, -10, -5, 0, 5], center=[-2.0, 0.3, 0])
        ax = A.ax
        cl = polyline(ax, degs, ll, RES, 3)
        dl = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=RES) for a, b in zip(degs, ll)])
        ce = polyline(ax, degs, ev, SHRUNK, 3.5)
        de = VGroup(*[Dot(ax.c2p(a, b), radius=0.08, color=SHRUNK) for a, b in zip(degs, ev)])
        best = int(np.argmax(ev))
        rows = fit_rows(VGroup(
            label(r"red: \ the best fit's log likelihood: \ always rises", font_size=22, color=RES),
            label(r"green: \ the log evidence, \ $\log p(y \mid \text{degree})$", font_size=22, color=SHRUNK),
            label(rf"peak at degree {d['best']}, \ the truth", font_size=22, color=HIT),
            label(rf"degree 8: \ {ev[8] - ev[best]:.1f} below: \ a gentle razor", font_size=22, color=GREY_A),
            label(r"the $N(0, 1)$ prior already keeps extra terms small", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The best-fitting log likelihood, in red, rises with every added degree, as it must. "
            "<bookmark mark='b'/> The log evidence, in green, the probability of the data averaged over each model's prior, "
            "behaves differently. <bookmark mark='c'/> It jumps at degree three, the truth, and peaks there. "
            "<bookmark mark='d'/> Beyond three it declines, but only gently: degree eight is about half a unit of log "
            "evidence lower. <bookmark mark='e'/> The razor is gentle here because the standard normal prior already keeps "
            "the extra coefficients small, so those models barely spread their predictions further. With a vaguer prior "
            "on the coefficients, the penalty would be steeper: Bartlett's effect again."
        ) as vo:
            self.add(simulated_tag(r"simulated: \ a seeded example"))
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(cl), FadeIn(dl), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ce), FadeIn(de), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(de[best].animate.scale(1.8), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def factor(self):
        rows = [
            cmath(r"p(y \mid M)", r"=", r"\textstyle\int p(y \mid w, M)\, p(w \mid M)\, dw", font_size=30),
            cmath(r"", r"\approx", r"p(y \mid \hat w, M) \times \dfrac{\sigma_{w \mid y}}{\sigma_w}", font_size=32),
            cmath(r"\text{Occam factor}", r"=", r"\dfrac{p(y\mid M)}{\sup_w p(y\mid w,M)}\le1", font_size=30),
            cmath(r"k \text{ parameters}", r":", r"\text{one factor each: } \ \log p(y) \approx \ell(\hat w) - \tfrac k2 \log n + O(1)", font_size=28),
        ]
        rows[1][-1].set_color(SHRUNK)
        whys = [why(r"the evidence"), why(r"best fit times a shrinkage of volume"),
                why(r"how much the data narrowed the parameter"), why(r"chapter six's BIC, \ recovered")]
        intro = label('An exact evidence-to-best-likelihood ratio is at most one', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Evidence averages the likelihood over a proper prior. Dividing it by the maximum "
            "likelihood gives an exact factor no larger than one. <bookmark mark='b'/> For a concentrated unimodal "
            "posterior and a broad, locally flat prior, Laplace approximation interprets this as a posterior-to-prior"
            " volume ratio. <bookmark mark='c'/> A single width ratio is a heuristic in that setting; posterior "
            "standard deviation is not always smaller than prior standard deviation. Correlated parameters require a "
            "joint volume calculation. <bookmark mark='d'/> In regular fixed-dimensional models, widths of order one "
            "over root n yield the leading BIC penalty, with prior-dependent terms of order one omitted."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"empirical Bayes for hyperparameters: \ maximize the evidence over $\alpha$, \ $\sigma$", font_size=24, color=SHRUNK),
            label(r"`type II maximum likelihood': \ Part 25's REML is one", font_size=24),
            label(r"Gaussian processes choose their length scales this way \ (Part 39)", font_size=24),
            label(r"the evidence asks about the prior too: \ a silly prior loses", font_size=24, color=RES),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The evidence is also a tool for tuning. Maximizing it over hyperparameters, like "
            "the prior precision or the noise level, is empirical Bayes once more, <bookmark mark='b'/> called type "
            "two maximum likelihood; REML has a related fixed-design interpretation through error contrasts or "
            "integration over beta. Its improper-flat-prior constant cannot compare different fixed-effect spaces. "
            "<bookmark mark='c'/> Gaussian processes choose their length scales the same way, in Part 39. <bookmark "
            "mark='d'/> And because the evidence averages over the prior, it judges the prior as well as the model: "
            "the choice of prior is part of the prediction being judged. Tuning hyperparameters also leaves "
            "uncertainty that plug-in estimates do not propagate."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
