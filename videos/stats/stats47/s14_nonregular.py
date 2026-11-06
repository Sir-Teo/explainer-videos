from __future__ import annotations

import numpy as np

from videos.stats.stats47.common import *  # noqa: F403


class NonRegular(VoiceoverScene):
    def construct(self):
        self.card()
        self.uniform()
        self.failure()
        self.chart()
        self.mofn()
        self.others()
        self.board()

    def card(self):
        card = chapter_card(13, r"Non-regular models", r"When the support moves, \ the rate changes", part=PART)
        with self.voiceover("Chapter thirteen. Non-regular models: when the support moves, the rate changes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def uniform(self):
        rows = [
            cmath(r"X_i \sim U(0, \theta)", r":", r"M = \max X_i, \ \ P(M \le \theta(1 - t/n)) = (1 - t/n)^n \to e^{-t}", font_size=30),
            cmath(r"n(\theta - M)/\theta", r"\Rightarrow", r"\mathrm{Exp}(1): \ \text{rate } n, \ \text{not } \sqrt n", font_size=32),
            cmath(r"\text{the local experiment}", r":", r"\text{a shifted exponential, \ not a Gaussian shift: \ no LAN}", font_size=30),
            cmath(r"\text{the best estimators}", r":", r"\tfrac{n+1}{n} M, \ \text{or the Pitman-type } \tfrac{n+2}{n+1} M, \ \text{biased toward } \theta", font_size=28),
        ]
        rows[1][-1].set_color(S.ACCENT)
        rows[2][-1].set_color(HODC)
        whys = [why(r"exact"), why(r"Part 45's $1/n^2$ variance"), why(r"chapter 7's QMD fails"), why(r"one-sided errors")]
        with self.voiceover(
            "<bookmark mark='a'/> The standard non-regular case: the uniform on zero to theta, estimated by the maximum. The "
            "chance that the maximum falls more than t over n below theta is one minus t over n, to the n, which tends to e "
            "to the minus t. <bookmark mark='b'/> So n times the shortfall, scaled by theta, is asymptotically exponential: "
            "the rate is n, faster than root n, matching Part forty-five's variances of order one over n squared. <bookmark "
            "mark='c'/> The local experiments converge to a shifted exponential, not a Gaussian shift, so none of chapter "
            "nine's theory applies directly. <bookmark mark='d'/> Good estimators correct the maximum's one-sided error "
            "upward, by a factor like n plus one over n."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def failure(self):
        d = load("nonreg")
        rows = [
            cmath(r"M^* = \max X_i^*", r":", r"M^* = M \ \text{whenever the top point is resampled}", font_size=32),
            cmath(r"P^*(M^* = M)", r"=", rf"1 - (1 - 1/n)^n \to 1 - e^{{-1}} = {d['limit_atom']:.3f}", font_size=32),
            cmath(r"n(M - M^*)", r":", r"\text{an atom at } 0 \text{ of mass } 0.63, \ \text{while the truth is continuous}", font_size=30),
            cmath(r"\text{so}", r":", r"\text{the bootstrap is inconsistent for the maximum}", font_size=34),
        ]
        rows[3][-1].set_color(HODC)
        whys = [why(r"resampling cannot exceed $M$"), why(r"Bickel \& Freedman (1981)"), why(rf"simulated: \ {d['atom']:.3f} at $n = {d['n']}$"), why(r"not Hadamard differentiable")]
        with self.voiceover(
            f"<bookmark mark='a'/> Now try the bootstrap. A resample's maximum equals the sample maximum whenever the top "
            f"observation is drawn at least once, <bookmark mark='b'/> which happens with probability one minus one minus one "
            f"over n to the n, tending to one minus one over e, {say(d['limit_atom'], 3)}. <bookmark mark='c'/> So the "
            f"bootstrap distribution of n times M minus M star has an atom of mass sixty-three percent at zero, while the "
            f"true distribution is a continuous exponential. <bookmark mark='d'/> The bootstrap is inconsistent here, as Peter "
            f"Bickel and David Freedman noted in 1981: the maximum is not a smooth functional of the distribution."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("nonreg")
        e = np.asarray(d["edges"])
        A = axes([0, 5], [0, 3.0], x_length=7.4, y_length=4.4, xlabel=r"$k(M - M^*)$", ylabel=r"density",
                 xticks=[0, 1, 2, 3, 4, 5], yticks=[0, 1, 2, 3], center=[-2.5, 0.2, 0])
        ax = A.ax
        hb = hist_bars(ax, e, np.minimum(np.asarray(d["hist_boot"]), 3.0), color=HODC, opacity=0.5)
        hm = hist_bars(ax, e, np.minimum(np.asarray(d["hist_m"]), 3.0), color=GOODC, opacity=0.6)
        u = np.linspace(0, 5, 200)
        ex = polyline(ax, u, np.exp(-u), LIMC, 4)
        side = fit_rows(VGroup(
            label(rf"red: \ the bootstrap: \ {100 * d['atom']:.0f}\% at 0", font_size=22, color=HODC),
            label(r"green: \ $m$-out-of-$n$, \ $m = 40$ from $n = 2{,}000$", font_size=22, color=GOODC),
            label(r"white: \ the true limit, \ Exp(1)", font_size=22, color=LIMC),
            label(rf"KS distance to Exp(1): \ {d['ks_boot']:.2f} \ vs \ {d['ks_m']:.2f}", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The ordinary bootstrap distribution, from one sample of {d['n']}: a spike at zero holding "
            f"{100 * d['atom']:.0f} percent of the mass, and a thin remainder. <bookmark mark='b'/> In green, the m out of n "
            f"bootstrap: resample only forty points from two thousand. <bookmark mark='c'/> The true limit is the white "
            f"exponential density. <bookmark mark='d'/> The m out of n version is close to it, with a Kolmogorov distance of "
            f"{say(d['ks_m'], 2)}; the ordinary bootstrap is off by {say(d['ks_boot'], 2)}."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"simulated: 20,000 resamples")))
            vo.wait_until("a")
            self.play(FadeIn(hb), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(hm), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ex), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def mofn(self):
        rows = [
            cmath(r"m \to \infty, \ \ m/n \to 0", r":", r"\text{resample } m \text{ points; \ rescale by the rate at } m", font_size=30),
            cmath(r"P^*(\text{the top point drawn})", r"\approx", r"m/n \to 0: \ \text{the atom disappears}", font_size=32),
            cmath(r"\text{subsampling}", r":", r"m \text{ points without replacement: \ consistent whenever a limit exists}", font_size=28),
            cmath(r"\text{the price}", r":", r"\text{choosing } m, \ \text{and knowing the rate } (n \text{ here})", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(HODC)
        whys = [why(r"Bickel, \ Götze \& van Zwet (1997)"), why(r"the reason it works"), why(r"Politis \& Romano (1994)"), why(r"no free lunch")]
        with self.voiceover(
            "<bookmark mark='a'/> The repair is to resample fewer points than you have: m of them, with m growing but small "
            "compared with n, and rescale by the rate at sample size m. <bookmark mark='b'/> The chance of drawing the top "
            "point is then about m over n, which vanishes, and so does the atom. <bookmark mark='c'/> Subsampling, drawing m "
            "points without replacement, is consistent under the bare assumption that the statistic has some limit "
            "distribution, as Dimitris Politis and Joseph Romano proved. <bookmark mark='d'/> The price is choosing m, and "
            "knowing or estimating the rate."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def others(self):
        rows = fit_rows(VGroup(
            label(r"other non-regular cases, \ and the bootstrap's trouble with them:", font_size=26, color=GREY_A),
            label(r"a parameter on the boundary \ (Part 46's Chernoff): \ the bootstrap fails at the boundary \ (Andrews 2000)", font_size=24, color=HODC),
            label(r"a unit root \ (Part 44's Dickey--Fuller): \ the AR bootstrap fails; \ resample the differences", font_size=24, color=HODC),
            label(r"the number of mixture components; \ change points; \ cube-root asymptotics \ (Kim \& Pollard 1990)", font_size=24, color=HODC),
            label(r"the general lesson: \ check that the statistic is smooth \emph{at this} $F$", font_size=26, color=S.ACCENT),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The maximum is one of a family of non-regular problems. <bookmark mark='b'/> A parameter on "
            "the boundary, Part forty-six's Chernoff mixture: Donald Andrews showed in 2000 that the bootstrap is "
            "inconsistent there too. <bookmark mark='c'/> A unit root, Part forty-four's Dickey–Fuller law: the ordinary "
            "autoregressive bootstrap fails, and one must resample differences instead. <bookmark mark='d'/> Mixture orders, "
            "change points, and estimators that converge at the cube root of n, like the mode and the shorth, studied by "
            "Jeankyung Kim and David Pollard. <bookmark mark='e'/> The general lesson: before trusting an asymptotic or "
            "bootstrap approximation, check that the statistic is smooth at the distribution in question."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = board_rows("uniform maximum", "m-out-of-n")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Coverage Board: a ninety percent interval for theta from the ordinary bootstrap "
                   "of the maximum, two hundred observations, covers eighty percent of the time: broken. <bookmark mark='b'/> "
                   "The m out of n bootstrap, with m equal to forty, covers ninety-two percent: kept, within the simulation's "
                   "error.",
                   [("a", [0]), ("b", [1])])
