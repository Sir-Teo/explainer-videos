from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import DICKENS, HIDDEN, load

FN = HIDDEN  # the unknown function


class GP(VoiceoverScene):
    def construct(self):
        self.card()
        self.functions()

    def card(self):
        card = chapter_card(5, r"Gaussian processes", r"What if the hidden thing is a whole function?", part=6)
        with self.voiceover("Chapter five. Gaussian processes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

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
            card.move_to([-0.4, 0, 0]).to_edge(UP, buff=0.12)
        with self.voiceover(
            "Sometimes the hidden thing is a whole function. Here's how often each page of Great Expectations says "
            "'her', from the start of the novel to the end. It rises and falls as the story moves between "
            "characters. <bookmark mark='a'/> A Gaussian process is a probability distribution over smooth "
            "functions. Gaussian means bell-shaped: at every page, the value is uncertain, most likely near the "
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
            "beyond them the band opens wide again. A Gaussian process knows what it doesn't know, which is exactly "
            "what you want when deciding where to look next."
        ) as vo:
            self.play(FadeIn(mband), Create(mline), pri.animate.set_stroke(opacity=0.3))
            vo.wait_until("a")
            self.play(FadeIn(ell))
            vo.wait_until("b")
            self.play(FadeOut(pri), dots[m20:].animate.set_opacity(0.2), Create(cut),
                      Transform(mband, m20band), Transform(mline, m20line), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
