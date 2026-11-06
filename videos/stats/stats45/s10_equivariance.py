from __future__ import annotations

import numpy as np

from videos.stats.stats45.common import *  # noqa: F403


class Equivariance(VoiceoverScene):
    def construct(self):
        self.card()
        self.location()
        self.pitman()
        self.table()
        self.uniform()
        self.scale()
        self.haar()

    def card(self):
        card = chapter_card(9, r"Equivariance", r"Rules that respect the symmetry of the problem", lit=(1939,), part=PART)
        with self.voiceover("Chapter nine. Equivariance: rules that respect the symmetry of the problem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def location(self):
        rows = [
            cmath(r"X_i = \theta + \varepsilon_i", r",", r"\ \varepsilon_i \sim f \text{ known}: \ \text{a location family}", font_size=32),
            cmath(r"\delta \text{ equivariant}", r":", r"\delta(x_1 + c, \ldots, x_n + c) = \delta(x) + c", font_size=32),
            cmath(r"R(\theta, \delta)", r"=", r"E_0\, (\delta(X) - 0)^2: \ \text{the same for every } \theta", font_size=32),
            cmath(r"\text{so}", r":", r"\text{a best equivariant rule exists: \ minimize one number}", font_size=32),
        ]
        rows[2][-1].set_color(MMC)
        rows[3][-1].set_color(ADMC)
        whys = [why(r"shift the data, \ shift the answer"), why(r"mean, \ median, \ midrange all are"), why(r"constant risk"), why(r"no stopped clocks")]
        with self.voiceover(
            "<bookmark mark='a'/> Chapter one's second escape: restrict the competition by symmetry. In a location family, "
            "each observation is theta plus an error with a known density f. <bookmark mark='b'/> If we shift every "
            "observation by c, the problem is the same problem shifted, so a sensible estimate should shift by c too. Such "
            "rules are called equivariant; the mean, the median and the midrange all are. <bookmark mark='c'/> An "
            "equivariant rule's risk is the same at every theta, because shifting theta just shifts the data. <bookmark "
            "mark='d'/> So the risk curve is a single number, the stopped clocks are excluded, and a best equivariant rule "
            "can exist: we just minimize that number."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def pitman(self):
        rows = [
            cmath(r"\delta = \delta_0 - v(\mathbf y)", r",", r"\ \mathbf y = (x_2 - x_1, \ldots, x_n - x_1): \ \text{every equivariant rule}", font_size=30),
            cmath(r"\text{best } v(\mathbf y)", r"=", r"E_0[\delta_0 \mid \mathbf y]: \ \text{condition on the ancillary}", font_size=32),
            cmath(r"\hat\theta_P", r"=", r"\frac{\int t \prod_i f(x_i - t)\, dt}{\int \prod_i f(x_i - t)\, dt}", font_size=36),
            cmath(r"\text{read as}", r":", r"\text{the posterior mean under a flat prior on } \theta", font_size=32),
        ]
        rows[2][-1].set_color(ADMC)
        rows[3][-1].set_color(BAYESC)
        whys = [why(r"one rule plus a function of the gaps"), why(r"chapter 7's ancillary"), why(r"Pitman (1939)"), why(r"generalized Bayes")]
        with self.voiceover(
            "<bookmark mark='a'/> Every equivariant rule is one of them, say the first observation, minus some function of "
            "the gaps between the observations. <bookmark mark='b'/> The gaps are ancillary: their law does not involve "
            "theta. Minimizing the risk means choosing that function as the conditional mean of the first rule given the "
            "gaps, with theta set to zero. <bookmark mark='c'/> Edwin Pitman worked out the answer in 1939: the integral of "
            "t times the likelihood, over the integral of the likelihood. <bookmark mark='d'/> That is the posterior mean "
            "under a flat, improper prior on theta. The best equivariant estimator is a generalized Bayes rule, as chapter "
            "three said the good ones would be."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("pitman")
        f = d["fams"]
        fmt = lambda v: "---" if v is None else f"{v:.4f}"  # noqa: E731
        rows = [[r"errors", r"mean", r"median", r"Pitman", r"Pitman $\div$ median"]]
        for name in ("normal", "Laplace", "uniform", "Cauchy"):
            r = f[name]
            rows.append([name, fmt(r["mean"]) if name != "Cauchy" else r"$\infty$", fmt(r["median"]), fmt(r["pitman"]), f"{r['rel']:.2f}"])
        tab = table_rows(rows, font_size=28, col_buff=0.9, row_buff=0.3, colors=[GREY_A, MLEC, BAYESC, MMC, INADC]).move_to([0, 0.7, 0])
        note_ = fit_rows(VGroup(
            label(rf"MSE at $n = {d['n']}$, \ {d['reps']:,} samples each; \ Pitman by numerical integration", font_size=24, color=GREY_A),
            label(r"normal: \ Pitman = the mean; \ uniform: \ Pitman = the midrange", font_size=24, color=ADMC),
        ), 12.4, 0.2, [0, -2.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Pitman's estimator under four error laws, five observations each, against the mean and "
            f"the median. <bookmark mark='b'/> For normal errors, it is the mean, and the median is about forty percent "
            f"worse. <bookmark mark='c'/> For Laplace errors, the median beats the mean, and Pitman beats both. <bookmark "
            f"mark='d'/> For uniform errors, Pitman is the midrange, with about a third of the median's mean squared error. "
            f"<bookmark mark='e'/> For Cauchy errors, the mean has no finite risk at all; the median is reasonable, and "
            f"Pitman is still seventeen percent better. In every case the best equivariant rule adapts itself to the shape "
            f"of the errors."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(note_[0]), FadeIn(exact_tag(r"simulated: 4,000 samples per family")))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1]))
                if k == 0:
                    self.play(FadeIn(note_[1]))
        self.clear_scene()

    def uniform(self):
        n = np.arange(2, 51)
        mean = 1 / (12 * n)
        mid = 1 / (2 * (n + 1) * (n + 2))
        A = axes([2, 50], [-4, -1], x_length=7.4, y_length=4.4, xlabel=r"$n$", ylabel=r"$\log_{10}$ MSE",
                 xticks=[10, 20, 30, 40, 50], yticks=[-4, -3, -2, -1], center=[-2.5, 0.2, 0])
        ax = A.ax
        cm = polyline(ax, n, np.log10(mean), MLEC, 4)
        cp = polyline(ax, n, np.log10(mid), MMC, 4)
        side = fit_rows(VGroup(
            label(r"$U(\theta - \tfrac12, \theta + \tfrac12)$, \ exactly:", font_size=22),
            label(r"blue: \ the mean, \ $1/(12 n)$", font_size=22, color=MLEC),
            label(r"gold: \ the midrange, \ $1/(2(n + 1)(n + 2))$", font_size=22, color=MMC),
            label(r"ratio $(n + 1)(n + 2)/6n$: \ 8.8 at $n = 50$", font_size=22, color=S.ACCENT),
            label(r"the $1/n^2$ rate of chapter 8's non-regular models", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The uniform case is worth seeing exactly. <bookmark mark='b'/> The sample mean's mean "
            "squared error is one over twelve n. <bookmark mark='c'/> The midrange, Pitman's estimator here, has one over "
            "two times n plus one times n plus two. <bookmark mark='d'/> The ratio of the two is n plus one times n plus two over six n, which grows without bound: nearly nine at fifty observations, "
            "<bookmark mark='e'/> because it converges at chapter eight's rate of one over n squared: the edges of the "
            "data carry almost all the information."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact formulas")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cm), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cp), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def scale(self):
        rows = [
            cmath(r"X_i = \sigma \varepsilon_i", r":", r"\text{a scale family; \ loss } (d/\sigma^2 - 1)^2", font_size=32),
            cmath(r"\delta(cx)", r"=", r"c^2 \delta(x): \ \text{scale equivariance}", font_size=34),
            cmath(r"\text{normal}", r":", r"\text{the best is } \textstyle\sum (x_i - \bar x)^2 / (n + 1)", font_size=34),
            cmath(r"\text{the minimum-risk scale rule}", r"=", r"\text{generalized Bayes for } \pi(\sigma) \propto 1/\sigma", font_size=30),
        ]
        rows[2][-1].set_color(ADMC)
        rows[3][-1].set_color(BAYESC)
        whys = [why(r"multiply the data, \ multiply the answer"), why(r"invariant loss"), why(r"chapter 3's winner"), why(r"Jeffreys's prior")]
        with self.voiceover(
            "<bookmark mark='a'/> The same idea works for scale. If each observation is sigma times a known error, and the "
            "loss compares the estimate to sigma squared in relative terms, <bookmark mark='b'/> then rescaling the data "
            "should rescale the answer. <bookmark mark='c'/> For normal data, the best scale-equivariant estimator of the "
            "variance divides the sum of squares by n plus one: chapter three's winner, now with a reason. <bookmark "
            "mark='d'/> And again it is generalized Bayes, for the prior one over sigma: Jeffreys's prior for a scale "
            "parameter."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def haar(self):
        rows = fit_rows(VGroup(
            label(r"in general: \ a group acts on the data and the parameter; \ the loss is invariant", font_size=26),
            label(r"the best equivariant rule = \ generalized Bayes for the right Haar measure", font_size=26, color=BAYESC),
            label(r"Girshick \& Savage (1951): \ Pitman's estimator is minimax", font_size=26, color=MMC),
            label(r"Stein (1959), \ Brown (1966): \ admissible in 1 and 2 dimensions, \ \emph{not} in 3", font_size=26, color=INADC),
            label(r"in $\mathbb R^p$ with $f = N(0, I)$: \ Pitman's estimator is $X$ \ itself", font_size=26, color=S.ACCENT),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The general setting: a group acts on the sample space and on the parameter, and the loss "
            "is unchanged by it. <bookmark mark='b'/> Under conditions, the best equivariant rule is the generalized Bayes "
            "rule for the right Haar measure of the group, the flat prior and one over sigma being two cases. <bookmark "
            "mark='c'/> Meyer Girshick and Savage proved in 1951 that Pitman's estimator is minimax. <bookmark mark='d'/> "
            "Stein proved in 1959 that it is admissible in one dimension, and Brown in 1966 that it is admissible in two but, quite generally, not in three or more. "
            "<bookmark mark='e'/> For normal errors in p dimensions, Pitman's estimator is just X: best equivariant, "
            "minimax, and, as the hook showed, inadmissible. Equivariance cannot see Stein's paradox, because the "
            "James–Stein estimator is not translation equivariant: it shrinks toward a particular point."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
