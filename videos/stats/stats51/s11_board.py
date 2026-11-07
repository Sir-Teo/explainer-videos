from __future__ import annotations

import math

import numpy as np

from videos.stats.stats51.common import *  # noqa: F403

N = 200
LA = math.log(4 / 0.05)


def wald(p):
    return 1.96 * np.sqrt(p * (1 - p) / N)


def hoeffding():
    return math.sqrt(math.log(2 / 0.05) / (2 * N))


def bernstein(p):
    return np.sqrt(2 * p * (1 - p) * N / (N - 1) * LA / N) + 7 * LA / (3 * (N - 1))


class ConcentrationIntervals(VoiceoverScene):
    def construct(self):
        self.card()
        self.intervals()
        self.widths()
        self.board()
        self.exact()
        self.anytime()
        self.lesson()

    def exact(self):
        from scipy import stats as ST

        k = 4
        lo, hi = ST.beta.ppf(0.025, k, N - k + 1), ST.beta.ppf(0.975, k + 1, N - k)
        ph = k / N
        rows = [[r"interval, \ $x = 4$ of $n = 200$", r"lower", r"upper", r"width"],
                [r"Wald"] + [f"{max(ph - wald(ph), 0):.4f}", f"{ph + wald(ph):.4f}", f"{min(ph+wald(ph),1)-max(ph-wald(ph),0):.4f}"],
                [r"Clopper--Pearson (exact)"] + [f"{lo:.4f}", f"{hi:.4f}", f"{hi - lo:.4f}"],
                [r"empirical Bernstein"] + [f"{max(ph - bernstein(ph), 0):.4f}", f"{ph + bernstein(ph):.4f}", f"{min(ph + bernstein(ph), 1) - max(ph - bernstein(ph), 0):.4f}"],
                [r"Hoeffding"] + [f"{max(ph - hoeffding(), 0):.4f}", f"{ph + hoeffding():.4f}", f"{min(ph + hoeffding(), 1) - max(ph - hoeffding(), 0):.4f}"]]
        tab = table_rows(rows, font_size=28, col_buff=0.7, row_buff=0.4, colors=[GREY_B, BADC, EXACTC, GOODC, BNDC])
        tab.move_to([0, 0.9, 0])
        foot = label(r"for one Bernoulli mean, \ the exact interval beats both bounds", font_size=24, color=GREY_A).move_to([0, -1.3, 0])
        foot2 = label(r"concentration earns its keep where no exact law exists: \ sums of matrices, \ suprema, \ sequences", font_size=24, color=GOODC).move_to([0, -2.1, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> An honest comparison. With four successes in two hundred trials, the Wald interval runs "
            f"from about zero to {say(ph + wald(ph), 3)}. The exact Clopper–Pearson interval of Part eleven runs from "
            f"{say(lo, 4)} to {say(hi, 4)}, and is valid at every n too. The empirical Bernstein and Hoeffding intervals are "
            f"wider still. <bookmark mark='b'/> For a single Bernoulli mean, where the exact law is the binomial, the exact "
            f"interval beats both bounds. <bookmark mark='c'/> Concentration earns its keep where no exact law is available: "
            f"for sums of random matrices, suprema over function classes, and confidence sequences, which is to say, for "
            f"most of modern statistics."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(exact_tag(r"exact")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def card(self):
        card = chapter_card(10, r"The Board: \ intervals from concentration", r"Valid at every $n$, \ and what that costs", part=PART)
        with self.voiceover("Chapter ten. The Board: intervals from concentration, valid at every n, and what that costs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def intervals(self):
        rows = [
            cmath(r"\text{Wald}", r":", r"\bar x \pm 1.96\sqrt{\bar x(1 - \bar x)/n}: \ \text{CLT; fixed }0<p<1,\ n\to\infty", font_size=32),
            cmath(r"\text{Hoeffding}", r":", r"\bar x \pm \sqrt{\log(2/\alpha)/(2n)}: \ \text{valid at every } n", font_size=32),
            cmath(r"\text{empirical Bernstein}", r":", r"\bar x \pm \Big(\sqrt{2V_n\log(4/\alpha)/n} + \tfrac{7\log(4/\alpha)}{3(n-1)}\Big)", font_size=30),
            cmath(r"V_n=\tfrac1{n-1}\sum_i(X_i-\bar X)^2,\ n\ge2", r":", r"\text{guarantees at every } n \text{ cost width; \ the variance buys some back}", font_size=30),
        ]
        rows[0][-1].set_color(BADC)
        rows[1][-1].set_color(BNDC)
        rows[2][-1].set_color(GOODC)
        whys = [why(r"Part 11"), why(r"chapter 1, \ inverted"), why(r"Maurer \& Pontil (2009)"), why(r"no free lunch")]
        heading = label('Unbiased sample variance enters empirical Bernstein intervals', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Three intervals for a probability from n yes-or-no outcomes. The Wald interval of Part eleven uses the central limit theorem, and so is only asymptotically right. <bookmark mark='b'/> Inverting Hoeffding's inequality from chapter one gives an interval whose coverage is guaranteed at every sample size for independent observations bounded in zero to one, whatever the probability, but whose width ignores the variance. <bookmark mark='c'/> Andreas Maurer and Massimiliano Pontil's empirical Bernstein interval of 2009 uses the sample variance, with a correction for having estimated it, and keeps the guarantee. <bookmark mark='d'/> The trade: guarantees that hold at every n cost width, and using the variance buys some of it back when the variance is small."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def widths(self):
        A = axes([0, 0.5], [0, 0.2], x_length=7.4, y_length=4.4, xlabel=rf"observed proportion $\hat p$, \ $n = {N}$", ylabel=r"half-width, \ 95\%",
                 xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], yticks=[0, 0.05, 0.1, 0.15, 0.2], center=[-2.5, 0.2, 0])
        ax = A.ax
        p = np.linspace(0.001, 0.5, 200)
        cw = polyline(ax, p, wald(p), BADC, 4)
        ch = polyline(ax, p, np.full_like(p, hoeffding()), BNDC, 4)
        cb = polyline(ax, p, bernstein(p), GOODC, 4)
        cross = float(p[np.argmin(np.abs(bernstein(p) - hoeffding()))])
        side = fit_rows(VGroup(
            label(rf"half-widths at $n = {N}$, \ evaluated at the observed proportion; \ unbiased sample variance", font_size=22),
            label(rf"red: \ Wald, \ {wald(0.02):.3f} at $p = 0.02$", font_size=22, color=BADC),
            label(rf"purple: \ Hoeffding, \ {hoeffding():.3f} for every $p$", font_size=22, color=BNDC),
            label(rf"green: \ empirical Bernstein, \ {bernstein(0.02):.3f} at $p = 0.02$", font_size=22, color=GOODC),
            label(rf"Bernstein beats Hoeffding below $p \approx {cross:.2f}$", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Their half-widths with two hundred observations, as a function of the observed sample proportion. The unbiased sample variance is used for empirical Bernstein. <bookmark mark='b'/> Wald's, in red, shrinks to {say(wald(0.02), 3)} for a rare event with probability two percent. <bookmark mark='c'/> Hoeffding's, in purple, is {say(hoeffding(), 3)} whatever the probability: five times wider for the rare event. <bookmark mark='d'/> The empirical Bernstein interval, in green, adapts to the variance, {say(bernstein(0.02), 3)} at two percent, but pays for its constants near one half. <bookmark mark='e'/> It is the narrower of the two guaranteed intervals below a probability of about {say(cross, 2)}."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact formulas")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cw), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ch), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cb), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def board(self):
        rows = board_rows("interval")
        d = load("board")
        a = [x["achieved"] for x in d["rows"]]
        show_board(self, rows,
                   f"<bookmark mark='a'/> On the Coverage Board, nominal ninety-five percent, twenty thousand samples of two "
                   f"hundred. For a rare event with probability two percent, the Wald interval covers only "
                   f"{100 * a[0]:.1f} percent: with an expected four successes the central limit theorem has not arrived, "
                   f"and samples with no successes at all give an interval of width zero. <bookmark mark='b'/> Hoeffding's "
                   f"and the empirical Bernstein intervals cover every time, conservatively. <bookmark mark='c'/> At "
                   f"probability one half the Wald interval covers {100 * a[3]:.1f} percent, close to nominal but still short. "
                   f"<bookmark mark='d'/> The guaranteed intervals cover {100 * a[4]:.1f} and {100 * a[5]:.0f} percent: valid "
                   f"always, and wider than needed whenever the central limit theorem has in fact arrived.",
                   [("a", [0]), ("b", [1, 2]), ("c", [3]), ("d", [4, 5])])

    def anytime(self):
        rows = [
            cmath(r"\text{a sequence of intervals}", r":", r"P\big(\forall n: \ p \in CI_n\big) \ge 1 - \alpha", font_size=34),
            cmath(r"\text{union over } n", r":", r"\alpha_n = \alpha / (n(n+1)): \ \text{Hoeffding at each } n", font_size=32),
            cmath(r"\text{Ville's inequality}", r":", r"P\big(\sup_n M_n \ge 1/\alpha\big) \le \alpha \ \text{for a nonnegative martingale, }M_0=1", font_size=30),
            cmath(r"\text{the payoff}", r":", r"\text{look at the data as often as you like: \ valid at stopping times; \ wider than fixed-time intervals}", font_size=30),
        ]
        rows[0][-1].set_color(GOODC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"time-uniform"), why(r"crude: \ a $\log n$ price"), why(r"Part 44's betting paths"), why(r"Part 35's peeking, \ solved")]
        heading = label('Confidence sequences pay width for simultaneous validity over time', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Concentration has one more gift. A confidence sequence is a sequence of intervals that covers the truth at every sample size simultaneously, with probability ninety-five percent. <bookmark mark='b'/> The crude way is a union bound over sample sizes, spending a smaller error rate at each, which puts a log n inside the square-root width. <bookmark mark='c'/> The sharp way uses Ville's inequality of 1939: a nonnegative martingale starting at one exceeds one over alpha with probability at most alpha, ever. Part forty-four's betting paths are such martingales. <bookmark mark='d'/> The payoff is that an analyst may look at the data as often as they like and stop whenever they choose, with the confidence-sequence guarantee. The intervals pay for this through their width: the peeking problem of Part thirty-five, solved by concentration."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"what high-dimensional probability says about practice:", font_size=28, color=GREY_A),
            label(r"a bound that holds at every $n$ protects you where the CLT has not arrived", font_size=26, color=BNDC),
            label(r"in high dimension, \ sample spectra are spread even with no signal: \ compare with a null", font_size=26, color=MATC),
            label(r"maxima of many Gaussians are nearly constant: \ $\sqrt{2\log p}$ is a scale; \ calibrate finite-sample error", font_size=26, color=GAUSSC),
            label(r"the measurements a convex method needs can be computed in advance", font_size=26, color=SPHC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What the theory says about practice. <bookmark mark='b'/> A bound that holds at every sample size protects you exactly where the central limit theorem has not yet arrived, as with rare events. <bookmark mark='c'/> In high dimensions, sample covariance spectra are spread out even when there is no signal at all, so a spectrum must be compared with a null, from Marchenko–Pastur or from shuffling. <bookmark mark='d'/> The maximum of many Gaussians is nearly a constant, so root two log p identifies the maximum scale, while a finite-sample error guarantee still requires calibration. <bookmark mark='e'/> And the number of measurements a convex method needs can be computed before any data are collected."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
