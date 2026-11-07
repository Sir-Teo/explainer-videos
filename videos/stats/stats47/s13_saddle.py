from __future__ import annotations

import numpy as np

from videos.stats.stats47.common import *  # noqa: F403


class Saddlepoint(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.density()
        self.tails()
        self.lr()
        self.uses()

    def card(self):
        card = chapter_card(12, r"Saddlepoint approximations", r"Accuracy far into the tails", lit=(1954,), part=PART)
        with self.voiceover("Chapter twelve. Saddlepoint approximations: accuracy far into the tails."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = [
            cmath(r"K(s)", r"=", r"\log E e^{sX}: \ \text{the cumulant generating function}", font_size=32),
            cmath(r"f_s(x)", r"=", r"e^{sx - K(s)} f(x): \ \text{tilt the law until its mean is } \bar x", font_size=32),
            cmath(r"K'(\hat s)", r"=", r"\bar x: \ \text{the saddlepoint}", font_size=36),
            cmath(r"f_{\bar X}(\bar x)", r"\approx", r"\sqrt{\frac{n}{2\pi K''(\hat s)}}\, \exp\{n[K(\hat s) - \hat s \bar x]\}", font_size=32),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Part 43's Cramér"), why(r"exponential tilting"), why(r"solve for $\hat s$"), why(r"Daniels (1954)")]
        with self.voiceover(
            "<bookmark mark='a'/> Henry Daniels's idea of 1954. Start from the cumulant generating function, as in "
            "Part forty-three's large deviations. <bookmark mark='b'/> Tilt the distribution exponentially, choosing "
            "the tilt so that its mean is exactly the value x-bar where we want the density. <bookmark mark='c'/> "
            "That tilt solves the saddlepoint equation. <bookmark mark='d'/> Under the tilted law, x-bar is at the "
            "centre, where the normal approximation is at its best; untilting gives this formula. Under the needed "
            "smooth nonlattice cumulant-generating-function conditions, relative-error expansions hold over specified"
            " saddlepoint ranges inside the tilting domain. This can greatly improve tails over a plain normal "
            "approximation; it is not a uniform claim over every arbitrarily distant endpoint."
        ) as vo:
            heading=label('Exponential tilting moves a tail point into the center',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def density(self):
        d = load("saddle")
        x = np.asarray(d["x"])
        A = axes([0, 3], [-0.1, 1.0], x_length=7.4, y_length=4.4, xlabel=r"$\bar x$, \ the mean of 5 Exp(1)", ylabel=r"density",
                 xticks=[0, 1, 2, 3], yticks=[-0.1,0,0.5,1], center=[-2.5, 0.2, 0])
        ax = A.ax
        ce = polyline(ax, x, d["exact"], LIMC, 5)
        cn = polyline(ax, x, d["normal"], MLEC, 3)
        cg = clip_curve(ax, x, d["edgeworth"], S.PRIOR, 3, ymin=-0.1, ymax=1.0)
        cs = polyline(ax, x, d["saddle"], GOODC, 3)
        side = fit_rows(VGroup(
            label(r"white: \ exact, \ Gamma$(5, 1/5)$", font_size=22, color=LIMC),
            label(r"blue: \ the normal: \ symmetric, \ positive below 0", font_size=22, color=MLEC),
            label(r"purple: \ one-term Edgeworth: \ better, \ can go negative", font_size=22, color=S.PRIOR),
            label(rf"green: \ saddlepoint: \ exact $\times$ {d['saddle_ratio']:.3f}, \ everywhere", font_size=22, color=GOODC),
            label(r"renormalize, \ and it is exact here", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The mean of five exponentials, whose exact density is a gamma: the white curve. <bookmark "
            f"mark='b'/> The normal approximation is symmetric and puts weight below zero. <bookmark mark='c'/> The one-term "
            f"Edgeworth correction bends it toward the skewness, but can go negative. <bookmark mark='d'/> The saddlepoint "
            f"approximation, in green, is the exact density multiplied by a constant, {say(d['saddle_ratio'], 3)}, at every "
            f"point: Stirling's error in the gamma function. <bookmark mark='e'/> Renormalized to integrate to one, it is "
            f"exact. With five observations."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact formulas")))
            for k, (m_, c) in enumerate(zip("abcd", (ce, cn, cg, cs))):
                vo.wait_until(m_)
                self.play(Create(c), FadeIn(side[k]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def tails(self):
        d = load("saddle")
        xt = np.asarray(d["xt"])
        lg = lambda v: np.log10(np.maximum(np.asarray(v, float), 1e-12))  # noqa: E731
        A = axes([1, 3], [-6, 0], x_length=7.4, y_length=4.4, xlabel=r"$x$", ylabel=r"$\log_{10} P(\bar X \ge x)$, \ $n = 5$",
                 xticks=[1, 1.5, 2, 2.5, 3], yticks=[-6, -4, -2, 0], center=[-2.5, 0.2, 0])
        ax = A.ax
        ce = polyline(ax, xt, lg(d["tail_exact"]), LIMC, 5)
        cn = polyline(ax, xt, lg(d["tail_normal"]), MLEC, 3)
        cl = DashedVMobject(polyline(ax, xt, lg(d["tail_lr"]), GOODC, 4), num_dashes=40)
        a2 = d["at2"]
        side = fit_rows(VGroup(
            label(r"white: \ the exact tail", font_size=22, color=LIMC),
            label(r"blue: \ the normal: \ too thin, \ by orders of magnitude", font_size=22, color=MLEC),
            label(r"green dashed: \ Lugannani--Rice", font_size=22, color=GOODC),
            label(rf"at $x = 2$: \ {a2['exact']:.4f}, \ {a2['normal']:.4f}, \ {a2['lr']:.4f}", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Tail probabilities, on a log scale. The exact tail of the mean of five exponentials. "
            f"<bookmark mark='b'/> The normal approximation's tail falls far too fast: off by a factor of more than two at "
            f"x equal to two, and by orders of magnitude beyond. <bookmark mark='c'/> The Lugannani–Rice saddlepoint formula "
            f"lies on top of the exact curve. <bookmark mark='d'/> At x equal to two: exactly {say(a2['exact'], 3)}, normal "
            f"{say(a2['normal'], 3)}, saddlepoint {say(a2['lr'], 3)}."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact formulas")))
            for k, (m_, c) in enumerate(zip("abc", (ce, cn, cl))):
                vo.wait_until(m_)
                self.play(Create(c), FadeIn(side[k]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def lr(self):
        rows = [
            cmath(r"\hat w", r"=", r"\mathrm{sign}(\hat s)\sqrt{2n[\hat s\bar x - K(\hat s)]}", font_size=34),
            cmath(r"\hat u", r"=", r"\hat s\sqrt{n K''(\hat s)}", font_size=34),
            cmath(r"P(\bar X \ge \bar x)", r"\approx", r"1 - \Phi(\hat w) + \phi(\hat w)\Big(\frac1{\hat u} - \frac1{\hat w}\Big)", font_size=32),
            cmath(r"\hat w", r":", r"\text{the signed root of the likelihood ratio statistic}", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"a signed root"), why(r"a Wald-type statistic"), why(r"Lugannani \& Rice (1980)"), why(r"chapter 8's LR, \ refined")]
        with self.voiceover(
            "<bookmark mark='a'/> The tail formula of Robert Lugannani and Stephen Rice uses two quantities. The "
            "first is the signed square root of a likelihood ratio statistic for the tilted family; <bookmark "
            "mark='b'/> the second is the tilt times the square root of n times the tilted variance. At the mean the "
            "formula has a removable singularity, handled by its continuous limit. <bookmark mark='c'/> The tail "
            "probability is the normal tail at the first, corrected by a term involving their reciprocals. <bookmark "
            "mark='d'/> With the required cumulant and smoothness conditions, its error can be controlled uniformly "
            "over an admissible range of saddlepoints: higher-order asymptotics, built on the same likelihood ratio "
            "that chapter eight treated to first order."
        ) as vo:
            heading=label('Lugannani-Rice corrects a signed likelihood-ratio tail',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def uses(self):
        rows = fit_rows(VGroup(
            label(r"Applications of saddlepoint approximations", font_size=36, color=GREY_A),
            label(r"tail p-values for rank and permutation tests, \ without enumeration", font_size=26, color=GOODC),
            label(r"the bootstrap without resampling: \ saddlepoint bootstrap distributions \ (Davison \& Hinkley 1988)", font_size=26),
            label(r"Barndorff-Nielsen's $p^*$: \ refined conditional likelihood approximation under additional regularity", font_size=26, color=S.ACCENT),
            label(r"risk theory and finance: \ the tails of sums of claims and losses", font_size=26, color=GREY_A),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Saddlepoints have many uses. <bookmark mark='b'/> With the appropriate lattice or "
            "conditional version they can approximate tail probabilities for rank and permutation tests without full "
            "enumeration. <bookmark mark='c'/> They approximate bootstrap distributions without resampling, as "
            "Anthony Davison and David Hinkley showed. <bookmark mark='d'/> Ole Barndorff-Nielsen's p-star formula "
            "gives a refined likelihood approximation, often conditional on an ancillary in the relevant regular "
            "model. Its accuracy order depends on that structure, not just on the estimator being an MLE. <bookmark "
            "mark='e'/> And in insurance and finance, they are a standard tool for the far tails of sums of claims "
            "and losses."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
