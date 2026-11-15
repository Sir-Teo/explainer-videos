from __future__ import annotations

import numpy as np

from videos.music.music50.common import *  # noqa: F403


class Cheb(SoundScene):
    def construct(self):
        chapter(self, 2, r"Chebyshev's exact harmonics", r"Can we choose exactly which harmonics a shaper adds?")
        self.identity()
        self.design()
        self.levels()
        self.history()

    # ------------------------------------------------------------------
    def identity(self):
        rows_ = text_rows([
            (r"Pafnuty Chebyshev's polynomials: \ $T_0 = 1$, \ $T_1 = x$, \ $T_{n+1} = 2x\,T_n - T_{n-1}$", WHITE),
            (r"$T_2 = 2x^2 - 1$, \ $T_3 = 4x^3 - 3x$, \ $T_4 = 8x^4 - 8x^2 + 1$, \ ...", WHITE),
            (r"their defining property: \ $T_n(\cos\theta) = \cos(n\theta)$", TUNE),
            (r"so a cosine of full size, \ passed through $T_n$, \ comes out as exactly its $n$-th harmonic", WHITE),
            (r"and through $\sum_n a_n T_n$, \ as exactly the harmonics $a_n$: \ a shaper designed by its spectrum", GREY_A),
        ], font_size=23)
        head = label(r"a polynomial for every harmonic", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "There is a way to choose a shaper's harmonics exactly. <bookmark mark='a'/> Pafnuty Chebyshev's polynomials start "
            "one, x, and each next one is two x times the last, minus the one before. <bookmark mark='b'/> Two x squared minus "
            "one; four x cubed minus three x; and so on. <bookmark mark='c'/> Their defining property: T n of cosine theta is "
            "cosine of n theta. <bookmark mark='d'/> So a full-size cosine passed through T n comes out as exactly its n-th "
            "harmonic, <bookmark mark='e'/> and passed through a weighted sum of them, as exactly those harmonics, at those "
            "weights. A shaper designed by its spectrum."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def design(self):
        d = load("shapers")
        amps = d["cheb_amps"]
        want = [20 * np.log10(a) if a > 0 else -200.0 for a in amps]
        a = harm_bars(want, width=0.34, gap=0.6, floor=-60, height=2.6, color=GREY_A, x0=0, y0=0)
        b = harm_bars(d["cheb"][:5], width=0.34, gap=0.6, floor=-60, height=2.6, color=TUNE, x0=0, y0=0)
        g = VGroup(VGroup(label(r"asked for: \ 1, \ 0, \ 1/2, \ 0, \ 1/4", font_size=18, color=GREY_A), a).arrange(DOWN, buff=0.35),
                   VGroup(label(r"measured at the output", font_size=18, color=TUNE), b).arrange(DOWN, buff=0.35)).arrange(RIGHT, buff=2.0).move_to(DOWN * 0.2)
        eq = MathTex(r"f(x) = T_1(x) + \tfrac12 T_3(x) + \tfrac14 T_5(x)", font_size=36).to_edge(UP, buff=1.0)
        head = label(r"a shaper built from its spectrum", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        m = d["cheb"]
        with self.voiceover(
            "Ask for the fundamental, half of it at the third harmonic, a quarter at the fifth, nothing else. "
            "<bookmark mark='a'/> The shaper is T one plus half T three plus a quarter T five. <bookmark mark='b'/> Feed it a "
            f"full-scale cosine and measure: the third at {say(m[2], 2)} decibels, which is a half, the fifth at "
            f"{say(m[4], 2)}, a quarter, and the even harmonics below two hundred decibels down, nothing but rounding."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq), FadeIn(g[0]))
            vo.wait_until("a")
            self.play(Indicate(eq, color=TUNE))
            vo.wait_until("b")
            self.play(FadeIn(g[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"Marc Le Brun and Daniel Arfib \ (1979): \ waveshaping synthesis, \ a cheap way to make rich spectra", WHITE),
            (r"the catch: \ the harmonics are exact only at full amplitude", WHITE),
            (r"turn the input down and the spectrum changes with it", WHITE),
            (r"so a shaper's timbre follows loudness, \ as an acoustic instrument's does: \ a feature, \ if designed for", TUNE),
            (r"Part 51 builds synthesizers; \ waveshaping is one of their tools", GREY_A),
        ]
        rows_scene(self, r"waveshaping synthesis", items,
                   "Marc Le Brun and Daniel Arfib turned this into a way to synthesize sound in 1979: waveshaping, a cheap way to "
                   "make rich spectra. <bookmark mark='b'/> The catch is that the harmonics are exact only at full amplitude. "
                   "<bookmark mark='c'/> Turn the input down and the spectrum changes with it, <bookmark mark='d'/> so a shaper's "
                   "timbre follows loudness, as an acoustic instrument's does: a feature, if it is designed for. "
                   "<bookmark mark='e'/> Part 51 builds synthesizers, and waveshaping is one of their tools.", marks="bcde")

    # ------------------------------------------------------------------
    def levels(self):
        d = load("cheblevels")
        c = clip("cheblevels.three")
        groups = VGroup()
        for k, name in (("0.25", r"a quarter"), ("0.6", r"0.6"), ("1.0", r"full")):
            g = harm_bars(d["spec"][k], width=0.26, gap=0.42, floor=-70, height=2.4, color=TUNE, x0=0, y0=0)
            groups.add(VGroup(g, label(rf"input: \ {name}", font_size=18, color=WHITE).next_to(g, UP, buff=0.3)))
        groups.arrange(RIGHT, buff=0.9).move_to(DOWN * 0.2)
        cap = label(r"harmonics 1 to 7, \ dB re the fundamental, \ from -70; \ each played back at the same peak level", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(r"one shaper, \ three input levels", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        q, f = d["spec"]["0.25"], d["spec"]["1.0"]
        with self.voiceover(
            "Hear the catch. A shaper designed for harmonics one, three, five and seven at full size, fed a tone at a quarter "
            f"of full size, at 0.6, and at full size. <bookmark mark='a'/> At full size it delivers the design: the seventh at "
            f"{say(f[6])} decibels. At a quarter, the seventh falls to {say(q[6])} and the fifth to {say(q[4])}: the upper "
            f"harmonics fade fast. But the third rises to {say(q[2], 1)}, almost level with the fundamental, because the "
            "polynomials' low terms cancel part of the fundamental. The timbre changes with level, and not always gently."
        ) as vo:
            self.play(FadeIn(head), FadeIn(groups), FadeIn(cap))
            vo.wait_until("a")
            self.play(Indicate(groups[2], color=TUNE, scale_factor=1.02))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"three levels", kind="synthesized", detail=r"a cosine, \ shaped", corner=DL, tag_corner=DR)
            keys = ["quiet", "middle", "full"]
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i < 2 else c.duration
                pulse(snd, groups[i], st[k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()
