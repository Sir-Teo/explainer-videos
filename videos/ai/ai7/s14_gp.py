from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import DICKENS, HIDDEN, PART, card_in, load

FN = HIDDEN  # the unknown function
DATA = DICKENS


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
        ylo, yhi = 0.0, float(max(y.max(), (mean + 2 * sd).max(), prior.max())) * 1.05
        ax = Axes(x_range=[0, len(x), 25], y_range=[ylo, yhi, 10], x_length=10.4, y_length=4.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([0, -0.5, 0])
        xl = label(r"page of \textit{Great Expectations}", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yl = label(r"``her'' per $1{,}000$ words", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=DICKENS) for a, b in zip(x, y)])

        def curve(v, color, sw=2.5, op=1.0):
            return VMobject(color=color, stroke_width=sw, stroke_opacity=op).set_points_smoothly(
                [ax.c2p(a, float(np.clip(b, ylo, yhi))) for a, b in zip(xs, v)])

        def band(m, s, color=FN, op=0.22):
            hi = [ax.c2p(a, float(np.clip(b, ylo, yhi))) for a, b in zip(xs, m + 2 * s)]
            lo = [ax.c2p(a, float(np.clip(b, ylo, yhi))) for a, b in zip(xs[::-1], (m - 2 * s)[::-1])]
            return Polygon(*hi, *lo, stroke_width=0, fill_color=color, fill_opacity=op)

        pri = VGroup(*[curve(v, FN, 2, 0.8) for v in prior])
        pos = VGroup(*[curve(v, FN, 2, 0.8) for v in post])
        mline, mband = curve(mean, WHITE, 4), band(mean, sd)
        m20line, m20band = curve(mean20, WHITE, 4), band(mean20, sd20)
        cut = DashedLine(ax.c2p(m20 - 0.5, ylo), ax.c2p(m20 - 0.5, yhi), color=GREY_B, stroke_width=2)
        colors = {r"f": FN}
        f = cmath(r"f", r"\sim", r"\mathcal{GP}\big(m,\; k(x, x')\big)", colors=colors, font_size=38).to_corner(UR, buff=0.4)
        kf = cmath(r"k(x, x') = s^2 e^{-(x - x')^2 / 2\ell^2}", font_size=30).next_to(f, DOWN, buff=0.2).align_to(f, RIGHT)
        ell = label(rf"length scale $\ell = {g['ell']:g}$ pages, \ chosen by the data", font_size=24, color=C.BITS)
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
            "together: strongly when the pages are close, hardly at all when they're far apart. Before seeing any "
            "data, here are five functions drawn from it: wiggly, with a typical width "
            "of wiggle, the length scale. <bookmark mark='b'/> Now condition on the pages. Only functions that pass "
            "near the data survive."
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
            "Their average is the best guess, and the band around it shows the uncertainty. "
            f"<bookmark mark='a'/> The length scale, about {g['ell']:g} pages, wasn't set by hand: it's the one under "
            "which the data was most probable. <bookmark mark='b'/> Show the model only the first twenty pages, and "
            "with the kernel settings held fixed, the band opens wide beyond them. This is uncertainty under our model, "
            "useful when deciding where to look next."
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
            "the most in this example. <bookmark mark='c'/> With kernel settings fixed, the variance is the prior's, minus what the data explains. It "
            "never looks at the values themselves, only at where the pages are. Rasmussen and Williams' book of "
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
        ylo, yhi = -8.0, float(max(y.max(), (means + 2 * sds).max())) * 1.02
        ax = Axes(x_range=[0, len(x), 25], y_range=[ylo, yhi, 10], x_length=10.4, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([0, -0.7, 0])
        xl = label(r"page of \textit{Great Expectations}", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        k = ValueTracker(0)

        def bandf():
            i = int(round(k.get_value()))
            m, s_ = means[i], sds[i]
            hi = [ax.c2p(a, float(np.clip(b, ylo, yhi))) for a, b in zip(xs, m + 2 * s_)]
            lo = [ax.c2p(a, float(np.clip(b, ylo, yhi))) for a, b in zip(xs[::-1], (m - 2 * s_)[::-1])]
            return VGroup(Polygon(*hi, *lo, stroke_width=0, fill_color=FN, fill_opacity=0.28),
                          VMobject(color=WHITE, stroke_width=3).set_points_smoothly(
                              [ax.c2p(a, float(np.clip(b, ylo, yhi))) for a, b in zip(xs, m)]))

        def dotsf():
            i = int(round(k.get_value()))
            sel = order[:ns[i]]
            return VGroup(*[Dot(ax.c2p(x[j], y[j]), radius=0.05, color=DATA) for j in sel])

        bd = always_redraw(bandf)
        dd = always_redraw(dotsf)
        nv = Integer(0, font_size=30)
        sv = DecimalNumber(msd[0], num_decimal_places=2, font_size=30, color=FN)
        read = VGroup(VGroup(label(r"pages seen:", font_size=24, color=GREY_A), nv).arrange(RIGHT, buff=0.15),
                      VGroup(label(r"average uncertainty $\sigma_*$:", font_size=24, color=GREY_A), sv).arrange(RIGHT, buff=0.15))
        read.arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.35)
        tag = note(r"the pages arrive in a random order; \ the kernel's settings as fitted", font_size=20).next_to(read, DOWN, buff=0.1)
        hist = cite(r"D.~Krige (1951), \ G.~Matheron (1963): \ kriging; \ C.~E.~Rasmussen \& C.~K.~I.~Williams (2006)", corner=DR)
        with self.voiceover(
            "Now watch the band shrink as pages land, in a random order. With no data, it's the prior: the same "
            "wide band everywhere. <bookmark mark='a'/> Each page pins the function down near it, and the band "
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
