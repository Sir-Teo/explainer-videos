from __future__ import annotations

import numpy as np

from videos.stats.stats39.common import *  # noqa: F403


class GPML(VoiceoverScene):
    def construct(self):
        self.card()
        self.same()
        self.occam()
        self.emulators()
        self.ei()
        self.run()
        self.result()
        self.wider()

    def card(self):
        card = chapter_card(13, r"Gaussian processes in machine learning", r"Kriging, \ renamed", lit=(1989, 1998), part=PART)
        with self.voiceover("Chapter thirteen. Gaussian processes in machine learning."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def same(self):
        rows = [[r"geostatistics", r"machine learning"],
                [r"kriging", r"GP regression"],
                [r"covariance, \ variogram", r"kernel"],
                [r"range, \ sill, \ nugget", r"length-scale, \ signal variance, \ noise"],
                [r"REML, \ variogram fitting", r"maximizing the marginal likelihood"],
                [r"kriging variance", r"predictive uncertainty"]]
        tab = table_rows(rows, font_size=26, col_buff=1.4, row_buff=0.32, colors=[GREY_A, FIELDC, TAUC, BANDC, PTC, AREAC]).move_to([0, 0.6, 0])
        foot = label(r"Rasmussen \& Williams, \ \emph{Gaussian Processes for Machine Learning} \ (2006)", font_size=22, color=GREY_A).move_to([0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Machine learning rediscovered kriging in the 1990s, under other names. <bookmark "
            "mark='b'/> Kriging is Gaussian process regression. <bookmark mark='c'/> The covariance is the kernel. "
            "<bookmark mark='d'/> The range, sill and nugget are the length-scale, the signal variance and the noise. "
            "<bookmark mark='e'/> Fitting them by likelihood is maximizing the marginal likelihood, <bookmark mark='f'/> and "
            "the kriging variance is the predictive uncertainty. Carl Rasmussen and Christopher Williams's book of 2006 is "
            "the machine-learning reference."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            for k, m_ in enumerate("bcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1]))
            self.play(FadeIn(foot))
        self.clear_scene()

    def emulators(self):
        rows = fit_rows(VGroup(
            label(r"Sacks, \ Welch, \ Mitchell \& Wynn (1989): \ computer experiments", font_size=26, color=TAUC),
            label(r"a simulator takes hours per run: \ a climate model, \ a crash test, \ a reactor", font_size=26),
            label(r"run it at a few designed inputs, \ krige the outputs: \ an emulator", font_size=26, color=FIELDC),
            label(r"no noise: \ the GP interpolates, \ and its variance says where to run next", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Before machine learning, statisticians had already moved kriging off the map. Jerome "
            "Sacks, William Welch, Toby Mitchell and Henry Wynn wrote in 1989 on the design and analysis of computer "
            "experiments. <bookmark mark='b'/> A simulator, a climate model or a crash test, may take hours for each run. "
            "<bookmark mark='c'/> Run it at a few well-chosen inputs and krige the outputs over the input space: an "
            "emulator, cheap to evaluate anywhere. <bookmark mark='d'/> The simulator has no noise, so the process "
            "interpolates, and its variance shows where the emulator is unsure, and so where to run the simulator next."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def ei(self):
        rows = [
            cmath(r"f^* ", r"=", r"\min_i f(x_i): \ \text{the best value so far}", font_size=30),
            cmath(r"\text{EI}(x)", r"=", r"E\big[\max(f^* - f(x), 0)\big], \ \ f(x) \sim N(\mu(x), s(x)^2)", font_size=30),
            cmath(r"\text{EI}(x)", r"=", r"(f^* - \mu)\, \Phi(z) + s\, \phi(z), \ \ z = (f^* - \mu)/s", font_size=30),
            cmath(r"\text{next}", r":", r"x_{n+1} = \arg\max_x \text{EI}(x)", font_size=30),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"minimize an expensive $f$"), why(r"Jones, \ Schonlau \& Welch (1998)"), why(r"exploit low $\mu$, \ explore high $s$"),
                why(r"Bayesian optimization")]
        with self.voiceover(
            "<bookmark mark='a'/> That leads to Bayesian optimization. We want the minimum of an expensive function, and "
            "have evaluated it a few times. <bookmark mark='b'/> Donald Jones, Matthias Schonlau and William Welch's "
            "expected improvement of 1998 asks, for each candidate input, how much we expect to beat the best value so "
            "far, under the Gaussian process's predictive distribution. <bookmark mark='c'/> It has a closed form, and it "
            "balances two pulls: a low predicted mean, exploitation, and a high predictive spread, exploration. <bookmark "
            "mark='d'/> Evaluate next where it is largest, update, and repeat."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def _frame(self, d, s, k):
        grid = np.asarray(d["grid"], float)
        A = axes([-2, 2], [-1.5, 3], x_length=7.6, y_length=3.1, xlabel=r"$x$", ylabel=r"$f(x)$", xticks=[-2, -1, 0, 1, 2],
                 yticks=[-1, 0, 1, 2, 3], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-1.6, 1.3, 0])
        ax = A.ax
        mu, sd = np.asarray(s["mu"], float), np.asarray(s["sd"], float)
        lo, hi = np.clip(mu - 1.645 * sd, -1.5, 3), np.clip(mu + 1.645 * sd, -1.5, 3)
        g = VGroup(band(ax, grid, lo, hi, FIELDC, 0.25), polyline(ax, grid, np.clip(mu, -1.5, 3), FIELDC, 3),
                   scatter(ax, s["x"], s["y"], OBSC, 0.08))
        ei = np.asarray(s["ei"], float)
        B = axes([-2, 2], [0, 1], x_length=7.6, y_length=1.3, xlabel=r"", ylabel=r"EI", xticks=[], yticks=[],
                 center=[-1.6, -2.3, 0])
        bx = B.ax
        e = polyline(bx, grid, ei / max(ei.max(), 1e-12), TAUC, 3)
        nx = DashedLine(bx.c2p(s["next"], 0), ax.c2p(s["next"], 3), color=TAUC, stroke_width=2)
        t = label(rf"after {len(s['x'])} evaluations", font_size=24, color=GREY_A).move_to([4.8, 2.4, 0])
        return A, B, g, e, nx, t

    def run(self):
        d = load("bayesopt")
        grid = np.asarray(d["grid"], float)
        steps = d["steps"]
        A, B, g, e, nx, t = self._frame(d, steps[0], 0)
        truth = polyline(A.ax, grid, np.asarray(d["f"], float), GREY_B, 2, 0.6)
        side = fit_rows(VGroup(
            label(r"grey: \ the hidden function", font_size=22, color=GREY_B),
            label(r"blue: \ the GP mean and 90\% band", font_size=22, color=FIELDC),
            label(r"gold: \ expected improvement \ (scaled)", font_size=22, color=TAUC),
        ), 3.6, 0.4, [5.0, 0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A one-dimensional example. A function with two dips, hidden from the optimizer, "
            "evaluated at three points. <bookmark mark='b'/> The Gaussian process's mean and band, <bookmark mark='c'/> and "
            "below, the expected improvement, which points first to the unexplored right side. <bookmark mark='d'/> Each "
            "new evaluation updates the process. The first tries probe the right, where the band was wide, and then the "
            "search moves left, into the deeper dip."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(truth), FadeIn(side[0]), FadeIn(t))
            self.play(FadeIn(g[2]))
            vo.wait_until("b")
            self.play(FadeIn(g[0]), Create(g[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(B), Create(e), Create(nx), FadeIn(side[2]))
            vo.wait_until("d")
            for k in (2, 4, 7):
                A2, B2, g2, e2, nx2, t2 = self._frame(d, steps[k], k)
                self.play(ReplacementTransform(g, g2), ReplacementTransform(e, e2), ReplacementTransform(nx, nx2),
                          ReplacementTransform(t, t2), run_time=1.2)
                g, e, nx, t = g2, e2, nx2, t2
                self.wait(1.0)
        self.clear_scene()

    def result(self):
        d = load("bayesopt")
        rows = fit_rows(VGroup(
            label(rf"the true minimum: \ $x = {d['true_min']:.2f}$, \ $f = {d['f_min']:.2f}$", font_size=28, color=TRUEC),
            label(rf"found: \ $x = {d['found']:.2f}$, \ within eight evaluations", font_size=28, color=BANDC),
            label(r"a grid search at the same resolution: \ 401 evaluations", font_size=28, color=MISSC),
            label(r"Snoek, \ Larochelle \& Adams (2012): \ tuning neural networks this way", font_size=28, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The true minimum is at " + say(d["true_min"], 2) + ". <bookmark mark='b'/> Bayesian "
            "optimization found " + say(d["found"], 2) + " within eight evaluations, counting the first three. <bookmark "
            "mark='c'/> A grid at the same resolution would need four hundred and one. <bookmark mark='d'/> Jasper "
            "Snoek, Hugo Larochelle and Ryan Adams showed in 2012 that this beats experts at tuning the hyperparameters of "
            "neural networks, where each evaluation is a full training run. Krige's mine valuation, choosing learning "
            "rates."
        ) as vo:
            self.add(seeded_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def wider(self):
        rows = fit_rows(VGroup(
            label(r"Neal (1996): \ a neural network with one infinitely wide hidden layer \ is a Gaussian process", font_size=26, color=FIELDC),
            label(r"kernel ridge regression \ (Part 29) \ = the GP posterior mean", font_size=26, color=TAUC),
            label(r"splines \ (Kimeldorf \& Wahba 1970) \ = a GP with a particular covariance", font_size=26, color=BANDC),
            label(r"one object, \ found by miners, \ meteorologists, \ statisticians and computer scientists", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The connections run further. Radford Neal showed in 1996 that a neural network with one "
            "hidden layer becomes a Gaussian process as the layer grows infinitely wide. <bookmark mark='b'/> Part "
            "twenty-nine's kernel ridge regression is the posterior mean of a Gaussian process, <bookmark mark='c'/> and "
            "George Kimeldorf and Grace Wahba showed in 1970 that smoothing splines are too. <bookmark mark='d'/> One "
            "mathematical object, found independently by miners, meteorologists, statisticians and computer scientists."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def occam(self):
        rows = [
            cmath(r"\log p(y \mid \theta)", r"=", r"-\tfrac12 y^\top K_\theta^{-1} y \; - \; \tfrac12 \log |K_\theta| \; - \; \tfrac n2 \log 2\pi", font_size=30),
            cmath(r"\text{fit}", r":", r"-\tfrac12 y^\top K_\theta^{-1} y \ \text{ rewards kernels that explain } y", font_size=30),
            cmath(r"\text{complexity}", r":", r"-\tfrac12 \log|K_\theta| \ \text{ penalizes kernels that could explain anything}", font_size=30),
            cmath(r"\text{so}", r":", r"\text{wiggly kernels fit better, \ but pay}", font_size=30),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"chapter 6's likelihood"), why(r"the data term"), why(r"the volume of plausible data"),
                why(r"MacKay (1992)")]
        with self.voiceover(
            "<bookmark mark='a'/> Machine learning fits the kernel's hyperparameters by the log marginal likelihood, "
            "which is chapter six's likelihood with the field integrated out. <bookmark mark='b'/> Its first term rewards "
            "kernels under which the observed data are typical. <bookmark mark='c'/> Its second penalizes kernels that "
            "spread their probability over many possible data sets, such as a very short length-scale, which could fit "
            "almost anything. <bookmark mark='d'/> So a wigglier kernel fits better but pays for it: David MacKay called "
            "this the automatic Occam's razor of Bayesian evidence, the same balance as Part twenty-eight's model choice."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
