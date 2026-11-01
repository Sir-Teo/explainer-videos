from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import DICKENS, HIDDEN, PART, card_in, load

FN = HIDDEN  # the unknown function
DATA = DICKENS


def gp_viewport(*values):
    """One inclusive ordinate range for every state drawn in the same axes."""
    arrays = [np.asarray(v, dtype=float).ravel() for v in values]
    if not arrays or any(not len(v) or not np.isfinite(v).all() for v in arrays):
        raise ValueError("GP viewport requires nonempty finite plotted values")
    low, high = min(v.min() for v in arrays), max(v.max() for v in arrays)
    span = high - low if high > low else max(abs(low), 1.0)
    return float(low - 0.05 * span), float(high + 0.05 * span)


class GP(VoiceoverScene):
    def construct(self):
        card_in(self, 13, r"Gaussian processes", r"What if the hidden thing is a whole function?",
                "Chapter thirteen. Gaussian processes.")
        self.functions()
        self.derive()
        self.land()

    def functions(self):
        g = load("gp")
        x, y, xs = np.asarray(g["x"]), np.asarray(g["y"]), np.asarray(g["xs"])
        mean, sd, prior, post = (np.asarray(g[k]) for k in ("mean", "sd", "prior", "post"))
        mean20, sd20, m20 = np.asarray(g["mean20"]), np.asarray(g["sd20"]), int(g["m20"])
        ylo, yhi = gp_viewport(y, prior, post, mean, mean - 2 * sd, mean + 2 * sd,
                              mean20, mean20 - 2 * sd20, mean20 + 2 * sd20)
        ax = Axes(x_range=[0, len(x), 25], y_range=[ylo, yhi, 10], x_length=10.4, y_length=4.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([0, -0.5, 0])
        xl = label(r"page of \textit{Great Expectations}", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yl = label(("每 $1{,}000$ 词中 ``her'' 的次数 \\\\ 阴影带：潜在函数 $f \\pm 2$ 条件标准差" if zh() else "``her'' per $1{,}000$ words \\\\ band: latent $f \\pm 2$ conditional SD"), font_size=20,
                   color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=DICKENS) for a, b in zip(x, y)])

        def curve(v, color, sw=2.5, op=1.0):
            return VMobject(color=color, stroke_width=sw, stroke_opacity=op).set_points_as_corners(
                [ax.c2p(a, float(b)) for a, b in zip(xs, v)])

        def band(m, s, color=FN, op=0.22):
            hi = [ax.c2p(a, float(b)) for a, b in zip(xs, m + 2 * s)]
            lo = [ax.c2p(a, float(b)) for a, b in zip(xs[::-1], (m - 2 * s)[::-1])]
            return Polygon(*hi, *lo, stroke_width=0, fill_color=color, fill_opacity=op)

        pri = VGroup(*[curve(v, FN, 2, 0.8) for v in prior])
        pos = VGroup(*[curve(v, FN, 2, 0.8) for v in post])
        mline, mband = curve(mean, WHITE, 4), band(mean, sd)
        m20line, m20band = curve(mean20, WHITE, 4), band(mean20, sd20)
        cut = DashedLine(ax.c2p(m20 - 0.5, ylo), ax.c2p(m20 - 0.5, yhi), color=GREY_B, stroke_width=2)
        colors = {r"f": FN}
        f = cmath(r"f", r"\sim", r"\mathcal{GP}\big(m,\; k(x, x')\big)", colors=colors, font_size=38).to_corner(UR, buff=0.4)
        kf = cmath(r"k(x, x') = s^2 e^{-(x - x')^2 / 2\ell^2}", font_size=30).next_to(f, DOWN, buff=0.2).align_to(f, RIGHT)
        ell = label((f"全部书页拟合：\\ $\\ell = {g['ell']:g}$ 页 \\\\ 均值、核与噪声固定" if zh() else f"all-page fit: \\ $\\ell = {g['ell']:g}$ pages \\\\ mean, kernel and noise held fixed"), font_size=20,
                    color=C.BITS)
        ell.next_to(kf, DOWN, buff=0.2).align_to(f, RIGHT)

        def mini_bell(xlab):
            a = Axes(x_range=[-3, 3, 1], y_range=[0, 1.1, 1], x_length=2.4, y_length=0.55, tips=False,
                     axis_config={"stroke_color": GREY_C, "include_ticks": False})
            bell = a.plot(lambda t: math.exp(-t * t / 2), color=FN, stroke_width=3)
            return VGroup(a, bell, MathTex(xlab, font_size=24, color=GREY_B).next_to(a, RIGHT, buff=0.1))

        g_card = gloss(r"Gaussian", r"bell-shaped: \ the value is uncertain, \\ most likely near the middle",
                       mini_bell(r"y"), corner=UL, width=5.0, color=FN)
        k_card = gloss(r"kernel $k(x, x')$", r"how strongly two pages' values move together: \\ strongly when "
                       r"close, \ hardly when far apart", mini_bell(r"x - x'"), corner=UL, width=5.0, color=FN)
        for card in (g_card, k_card):  # top middle, between the axis label and the formulas
            card.move_to([0.9, 0, 0]).to_edge(UP, buff=0.12)
        with self.voiceover(
            "Sometimes the hidden thing is a whole function. Here's how often each page of Great Expectations says "
            "'her', from the start of the novel to the end. It rises and falls as the story moves between "
            "characters. <bookmark mark='a'/> A Gaussian process is a probability distribution over "
            "functions; our kernel makes them smooth. Gaussian means bell-shaped: at every page, the value is uncertain, most likely near the "
            "middle of a bell. <bookmark mark='k'/> The kernel, k, says how strongly two pages' values move "
            "together: strongly when the pages are close, hardly at all when they're far apart. We already fitted "
            "the mean, kernel and noise settings using all these pages. Here are five draws from that fitted "
            "empirical-Bayes prior, before conditioning on the individual values again. Their typical width of "
            "wiggle is the length scale. <bookmark mark='b'/> Now condition on the pages with those settings fixed. "
            "The draws move toward functions compatible with the noisy observations."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01),
                      run_time=2.0)
            vo.wait_until("a")
            self.play(Write(f), FadeIn(g_card, shift=DOWN * 0.2))
            vo.wait_until("k")
            self.play(FadeIn(kf), FadeOut(g_card), FadeIn(k_card))
            self.play(LaggedStart(*[Create(c) for c in pri], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeOut(k_card))
            self.play(*[Transform(a, b) for a, b in zip(pri, pos)], run_time=2.5)
        with self.voiceover(
            "The white curve is the conditional mean. The band is plus or minus two conditional standard "
            "deviations of the latent function, given the fitted settings. It excludes observation noise and "
            "uncertainty in those settings. "
            f"<bookmark mark='a'/> The length scale, about {g['ell']:g} pages, was chosen by the all-page marginal "
            "likelihood among the settings tried. <bookmark mark='b'/> Now condition only on the first "
            f"{m20} pages, still holding the all-page fitted mean, kernel and noise fixed. This is a subset-conditioning "
            "demonstration, not a held-out forecast: those later pages already helped choose the settings."
        ) as vo:
            self.play(FadeIn(mband), Create(mline), pri.animate.set_stroke(opacity=0.3))
            vo.wait_until("a")
            self.play(FadeIn(ell))
            vo.wait_until("b")
            self.play(FadeOut(pri), dots[m20:].animate.set_opacity(0.2), Create(cut),
                      Transform(mband, m20band), Transform(mline, m20line), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"\mu_*": FN, r"\sigma_*^2": FN, r"\mathbf{y}": DATA, r"\mathbf{k}_*": C.BITS}
        rows = [
            cmath(r"\begin{bmatrix} \mathbf{y} \\ f_* \end{bmatrix}", r"\sim",
                  r"\mathcal{N}\!\left(0,\; \begin{bmatrix} K + \sigma_n^2 I & \mathbf{k}_* \\ \mathbf{k}_*^{\top} & k_{**}"
                  r"\end{bmatrix}\right)", colors=colors, font_size=34),
            cmath(r"f_* \mid \mathbf{y}", r"\sim", r"\mathcal{N}(", r"\mu_*", r",\;", r"\sigma_*^2", r")", colors=colors,
                  font_size=36),
            cmath(r"\mu_*", r"=", r"\mathbf{k}_*^{\top}", r"(K + \sigma_n^2 I)^{-1}", r"\mathbf{y}", colors=colors,
                  font_size=36),
            cmath(r"\sigma_*^2", r"=", r"k_{**}", r"-", r"\mathbf{k}_*^{\top}", r"(K + \sigma_n^2 I)^{-1}", r"\mathbf{k}_*",
                  colors=colors, font_size=36),
        ]
        whys = [why(r"any finite set of values: \\ jointly Gaussian, \ covariances from $k$"),
                why(r"condition a Gaussian \\ on part of itself"),
                why(r"the mean: \ a weighted sum \\ of the observed pages"),
                why(r"the prior's variance, minus what \\ the data explains \ (a Schur complement)")]
        step = ladder(self, rows, whys, keep=4, top=2.7, x=-2.0, buff=0.55, edge=6.8)
        head = label(r"The posterior is one formula", font_size=32).to_edge(UP, buff=0.25)
        nb = label(r"fixed kernel: \ conditioning is linear algebra; \ $\sigma_*^2$ does not depend on $\mathbf{y}$",
                   font_size=24, color=C.BITS).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Why is conditioning so easy? First subtract the mean. Under a Gaussian process, the pages we've seen and the value at any new "
            "page are jointly Gaussian, with covariances given by the kernel. <bookmark mark='a'/> And a Gaussian, "
            "conditioned on some of its coordinates, is still Gaussian. Completing the square gives its mean and "
            "variance. <bookmark mark='b'/> The mean is a weighted sum of the observed values: nearby pages weigh "
            "the most in this example. <bookmark mark='c'/> With mean and kernel settings fixed, the conditional "
            "latent variance is the prior's, minus what conditioning explains. It depends on the page locations, "
            "not directly on their observed values. But our fitted settings depend on all the values; this "
            "plug-in variance omits their uncertainty. Rasmussen and Williams' book of "
            "2006 builds the whole subject on these two lines."
        ) as vo:
            self.play(FadeIn(head))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            self.play(FadeIn(nb))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def land(self):
        g, gl = load("gp"), load("gpland")
        x, y, xs = np.asarray(g["x"]), np.asarray(g["y"]), np.asarray(g["xs"])
        means, sds = np.asarray(gl["means"]), np.asarray(gl["sds"])
        ns, order = [int(v) for v in gl["ns"]], np.asarray(gl["order"])
        msd = np.asarray(gl["mean_sd"])
        ylo, yhi = gp_viewport(y, means, means - 2 * sds, means + 2 * sds)
        ax = Axes(x_range=[0, len(x), 25], y_range=[ylo, yhi, 10], x_length=10.4, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([0, -0.7, 0])
        xl = label(r"page of \textit{Great Expectations}", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        k = ValueTracker(0)

        def bandf():
            i = int(round(k.get_value()))
            m, s_ = means[i], sds[i]
            hi = [ax.c2p(a, float(b)) for a, b in zip(xs, m + 2 * s_)]
            lo = [ax.c2p(a, float(b)) for a, b in zip(xs[::-1], (m - 2 * s_)[::-1])]
            return VGroup(Polygon(*hi, *lo, stroke_width=0, fill_color=FN, fill_opacity=0.28),
                          VMobject(color=WHITE, stroke_width=3).set_points_as_corners(
                              [ax.c2p(a, float(b)) for a, b in zip(xs, m)]))

        def dotsf():
            i = int(round(k.get_value()))
            sel = order[:ns[i]]
            return VGroup(*[Dot(ax.c2p(x[j], y[j]), radius=0.05, color=DATA) for j in sel])

        bd = always_redraw(bandf)
        dd = always_redraw(dotsf)
        nv = Integer(0, font_size=30)
        sv = DecimalNumber(msd[0], num_decimal_places=2, font_size=30, color=FN)
        read = VGroup(VGroup(label(('用于条件化的书页：' if zh() else 'conditioning pages:'), font_size=22, color=GREY_A), nv).arrange(RIGHT, buff=0.15),
                      VGroup(label(('潜在函数条件标准差的均值：' if zh() else 'mean latent conditional SD:'), font_size=22, color=GREY_A), sv).arrange(RIGHT, buff=0.15))
        read.arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.35)
        tag = note(('随机顺序条件化；潜在函数 $f \\pm 2$ 条件标准差 \\\\ 用全部书页拟合的均值、核与噪声固定' if zh() else 'random-order conditioning; latent $f \\pm 2$ conditional SD \\\\ all-page fitted mean, kernel and noise held fixed'),
                   font_size=18).next_to(read, DOWN, buff=0.1)
        hist = cite(r"D.~Krige (1951), \ G.~Matheron (1963): \ kriging; \ C.~E.~Rasmussen \& C.~K.~I.~Williams (2006)", corner=DR)
        with self.voiceover(
            "Now reveal conditioning pages in a random order. At zero revealed pages, this is the fitted "
            "empirical-Bayes prior; its mean, kernel and noise already used all the pages. We hold those settings "
            "fixed throughout. The band is plus or minus two latent conditional standard deviations, not an "
            "observation prediction band or full Bayesian uncertainty. <bookmark mark='a'/> Each conditioning page "
            "reduces the uncertainty near it, and the band "
            "pinches there. <bookmark mark='b'/> With all " + f"{ns[-1]} pages, the average uncertainty has fallen "
            f"from {msd[0]:.1f} to {msd[-1]:.1f}. Between the pages, where the kernel says the rate could still "
            "wander, it stays open. <bookmark mark='c'/> Mining engineers did this first: Danie Krige estimated "
            "gold grades between boreholes in the 1950s, and Georges Matheron made it a theory, kriging. Machine "
            "learning took it up in the 1990s."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(read), FadeIn(tag), FadeIn(bd), FadeIn(dd))
            vo.wait_until("a")
            for i in range(1, 9):
                self.play(k.animate.set_value(i), ChangeDecimalToValue(nv, ns[i]), ChangeDecimalToValue(sv, msd[i]),
                          run_time=0.9)
            vo.wait_until("b")
            for i in range(9, len(ns)):
                self.play(k.animate.set_value(i), ChangeDecimalToValue(nv, ns[i]), ChangeDecimalToValue(sv, msd[i]),
                          run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(hist))
        bd.clear_updaters()
        dd.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
