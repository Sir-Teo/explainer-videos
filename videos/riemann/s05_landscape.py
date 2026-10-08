from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.riemann.common import (
    LANDSCAPE, PLATT_TRUDGIAN_ZEROS, color_wheel, gammas, label, landscape_image, load, note, polyline, strip_axes,
)


class ZeroLandscape(VoiceoverScene):
    def construct(self):
        self.coloring()
        self.features()
        self.symmetry()
        self.statement()
        self.evidence()

    # ------------------------------------------------------------------
    def make_axes(self):
        (s0, s1), (t0, t1) = LANDSCAPE["sig"], LANDSCAPE["t"]
        xl = 8.8
        yl = xl * LANDSCAPE["ny"] / LANDSCAPE["nx"]
        ax = Axes(x_range=[s0, s1, 1], y_range=[t0, t1, 5], x_length=xl, y_length=yl, tips=False,
                  axis_config={"stroke_color": WHITE, "stroke_width": 1.5, "stroke_opacity": 0.6, "include_ticks": False})
        ax.move_to(LEFT * 2.0 + DOWN * 0.15)
        return ax

    def tick_labels(self, ax):
        (s0, s1), (t0, t1) = LANDSCAPE["sig"], LANDSCAPE["t"]
        g = VGroup()
        for v in (-4, -2, 0, 1, 2):
            g.add(MathTex(str(v), font_size=22, color=GREY_B).next_to(ax.c2p(v, t0), DOWN, buff=0.1))
        for v in (10, 20, 30):
            g.add(MathTex(str(v), font_size=22, color=GREY_B).next_to(ax.c2p(s0, v), LEFT, buff=0.1))
        return g

    def coloring(self):
        ax = self.make_axes()
        self.ax = ax
        img = landscape_image(ax)
        S = np.linspace(*LANDSCAPE["sig"], LANDSCAPE["nx"])[None, :].repeat(LANDSCAPE["ny"], 0)
        full_alpha = img.pixel_array[:, :, 3].copy()
        frame = SurroundingRectangle(img, buff=0, color=GREY_B, stroke_width=1.5)

        def reveal(cut):
            img.pixel_array[:, :, 3] = np.where(S >= cut, full_alpha, 0).astype(np.uint8)

        reveal(1.0)
        wheel = color_wheel(0.75).move_to(RIGHT * 4.9 + UP * 2.2)
        wl = VGroup(
            MathTex(r"\arg \zeta(s)", font_size=30).next_to(wheel, UP, buff=0.12),
            MathTex(r"1", font_size=24).next_to(wheel, RIGHT, buff=0.08),
            MathTex(r"i", font_size=24).next_to(wheel, UP, buff=0.02).shift(RIGHT * 0.95),
            MathTex(r"-1", font_size=24).next_to(wheel, LEFT, buff=0.08),
        )
        wl[2].move_to(wheel.get_top() + UP * 0.12 + RIGHT * 0.0)
        wl[0].next_to(wl[2], UP, buff=0.1)
        bright = label(r"dark: $|\zeta|$ small\\bright: $|\zeta|$ large", font_size=26, color=GREY_A).next_to(wheel, DOWN, buff=0.3)
        hue = label(r"color = direction of $\zeta(s)$", font_size=26).next_to(bright, DOWN, buff=0.25)
        sig_l = MathTex(r"\Real(s)", font_size=26).next_to(ax.c2p(LANDSCAPE["sig"][1], LANDSCAPE["t"][0]), RIGHT, buff=0.12)
        t_l = MathTex(r"\Imag(s)", font_size=26).next_to(ax.c2p(LANDSCAPE["sig"][0], LANDSCAPE["t"][1]), UP, buff=0.08)
        conv = label(r"series converges", font_size=24).move_to(ax.c2p(2.5, 31.0))
        conv.add_background_rectangle(opacity=0.7, buff=0.05)

        with self.voiceover(
            "To see all of zeta at once, we'll color the complex plane. <bookmark mark='c'/> Each point s gets a color for the "
            "direction that zeta of s points in, <bookmark mark='b'/> and a brightness for its size. Wherever zeta is zero, every "
            "color meets at a single dark point."
        ) as vo:
            ticks = self.tick_labels(ax)
            self.axl_ticks = ticks
            self.play(FadeIn(frame), FadeIn(img), FadeIn(sig_l), FadeIn(t_l), FadeIn(conv), FadeIn(ticks))
            vo.wait_until("c")
            self.play(FadeIn(wheel), FadeIn(wl), FadeIn(hue))
            vo.wait_until("b")
            self.play(FadeIn(bright))

        with self.voiceover(
            "Where the series converges, on the right, zeta is calm, close to one. <bookmark mark='w'/> Then analytic "
            "continuation fills in everything else."
        ) as vo:
            vo.wait_until("w")
            self.play(FadeOut(conv), UpdateFromAlphaFunc(img, lambda m, a: reveal(1.0 - a * 5.7)), run_time=3.5,
                      rate_func=smooth)
        self.img, self.frame = img, frame
        self.legend = VGroup(wheel, wl, bright, hue)
        self.axl = VGroup(sig_l, t_l, self.axl_ticks)

    # ------------------------------------------------------------------
    def features(self):
        ax = self.ax
        pole = Dot(ax.c2p(1, 0), radius=0.07, color=WHITE)
        pole_l = label(r"pole at $s = 1$\\(harmonic series)", font_size=24).next_to(ax.c2p(1, 0), RIGHT, buff=0.5).shift(UP * 0.55)
        pole_l.add_background_rectangle(opacity=0.75, buff=0.05)
        pole_a = Arrow(pole_l.get_left(), ax.c2p(1, 0), buff=0.08, color=WHITE, stroke_width=2.5)
        triv = VGroup(*[Dot(ax.c2p(-2 * k, 0), radius=0.07, color=GREY_A) for k in range(1, 3)])
        triv_l = label(r"trivial zeros: $-2, -4, -6, \ldots$", font_size=26).next_to(ax.c2p(-3, 0), DOWN, buff=0.45)
        triv_l.add_background_rectangle(opacity=0.75, buff=0.05)
        g = gammas(5)
        zeros = VGroup(*[Dot(ax.c2p(0.5, t), radius=0.07, color=C.ZERO) for t in g])
        strip = Rectangle(width=ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0], height=self.img.height,
                          stroke_color=C.ZERO, stroke_width=2).move_to([ax.c2p(0.5, 0)[0], self.img.get_center()[1], 0])
        crit = DashedLine(ax.c2p(0.5, LANDSCAPE["t"][0]), ax.c2p(0.5, LANDSCAPE["t"][1]), color=C.ZERO, stroke_width=2,
                          dash_length=0.1)
        zl = VGroup(*[MathTex(rf"\tfrac12 + {t:.2f}\,i", font_size=24, color=C.ZERO) for t in g])
        for d, l in zip(zeros, zl):
            l.next_to(d, RIGHT, buff=0.12)
            l.add_background_rectangle(opacity=0.8, buff=0.04)
        strip_l = label(r"critical strip\\$0 < \Real(s) < 1$", font_size=26, color=C.ZERO).move_to(RIGHT * 4.9 + DOWN * 1.6)
        strip_a = Arrow(strip_l.get_left(), ax.c2p(1.05, 9), buff=0.1, color=C.ZERO, stroke_width=2.5)

        with self.voiceover(
            "The bright spot at s equals one is the pole, <bookmark mark='p'/> where zeta blows up: that's our harmonic series "
            "again."
        ) as vo:
            vo.wait_until("p")
            self.play(FadeIn(pole), GrowArrow(pole_a), FadeIn(pole_l))

        with self.voiceover(
            "On the negative real axis, there are zeros <bookmark mark='z'/> at minus two, minus four, minus six, and so on. "
            "These are called the trivial zeros. They're forced by a simple factor in zeta's symmetry, and they're completely "
            "understood."
        ) as vo:
            vo.wait_until("z")
            self.play(LaggedStart(*[FadeIn(d, scale=2) for d in triv], lag_ratio=0.25), FadeIn(triv_l))

        with self.voiceover(
            "All the other zeros, the nontrivial ones, live inside <bookmark mark='s'/> the critical strip, where the real part "
            "is between zero and one. <bookmark mark='l'/> And look where they are: at heights 14.13, 21.02, 25.01, 30.42, "
            "and 32.94. <bookmark mark='h'/> Every one of them sits on the line where the real part is exactly one half."
        ) as vo:
            vo.wait_until("s")
            self.play(FadeOut(self.legend), FadeOut(VGroup(pole_l, pole_a)), Create(strip), FadeIn(strip_l), GrowArrow(strip_a))
            vo.wait_until("l")
            for d, l in zip(zeros, zl):
                self.play(FadeIn(d, scale=2), FadeIn(l), run_time=0.45)
            vo.wait_until("h")
            self.play(Create(crit))
        self.wait(0.5)
        self.play(FadeOut(Group(self.img, self.frame, self.axl, pole, triv, triv_l, zeros, zl, strip, strip_l, strip_a, crit)))
        self.remove(self.img)

    # ------------------------------------------------------------------
    def symmetry(self):
        fe = VGroup(
            label(r"Riemann's functional equation", font_size=34),
            MathTex(r"\Lambda(s) = \Lambda(1 - s), \qquad \Lambda(s) = \pi^{-s/2}\,\Gamma(\tfrac s2)\,\zeta(s)", font_size=38),
        ).arrange(DOWN, buff=0.25).to_edge(UP, buff=0.35)
        g = strip_axes(t_max=32, t_min=-32, x_length=4.6, y_length=5.6, labels=False).move_to(LEFT * 3.0 + DOWN * 0.75)
        ax = g.ax
        lab = VGroup(MathTex("0", font_size=26).next_to(ax.c2p(0, -32), DOWN, buff=0.1),
                     MathTex(r"\tfrac12", font_size=28, color=C.ZERO).next_to(ax.c2p(0.5, -32), DOWN, buff=0.08),
                     MathTex("1", font_size=26).next_to(ax.c2p(1, -32), DOWN, buff=0.1))
        real_axis = Line(ax.c2p(-0.35, 0), ax.c2p(1.35, 0), color=GREY_C, stroke_width=1.5)
        b, t = 0.78, 20.0
        bad = Dot(ax.c2p(b, t), radius=0.09, color=C.DANGER)
        partners = VGroup(Dot(ax.c2p(1 - b, t), radius=0.09, color=C.DANGER), Dot(ax.c2p(b, -t), radius=0.09, color=C.DANGER),
                          Dot(ax.c2p(1 - b, -t), radius=0.09, color=C.DANGER))
        mirror = DoubleArrow(ax.c2p(b - 0.05, t), ax.c2p(1 - b + 0.05, t), buff=0.05, color=GREY_B, stroke_width=2,
                             tip_length=0.15)
        conj = DoubleArrow(ax.c2p(b, t - 2), ax.c2p(b, -t + 2), buff=0.05, color=GREY_B, stroke_width=2, tip_length=0.15)
        hypo = label(r"a hypothetical zero\\off the line", font_size=26, color=C.DANGER).next_to(ax.c2p(1.35, t), RIGHT, buff=0.15)
        notes = VGroup(
            label(r"$s \leftrightarrow 1 - s$: \ mirror image across $\Real(s) = \tfrac12$", font_size=28),
            label(r"$s \leftrightarrow \bar s$: \ mirror image across the real axis", font_size=28),
            label(r"so an off-line zero brings three partners", font_size=28, color=C.DANGER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.2 + DOWN * 0.6)
        zd = VGroup(*[Dot(ax.c2p(0.5, s * gg), radius=0.05, color=C.ZERO) for gg in gammas(5) for s in (1, -1)])

        self.play(FadeIn(fe[0]))
        with self.voiceover(
            "There's a deeper reason for this line. <bookmark mark='f'/> Riemann proved a functional equation: after multiplying "
            "zeta by a simple gamma-function factor, the result is unchanged when you swap s with one minus s. "
            "<bookmark mark='m'/> That's a reflection across the line where the real part is one half."
        ) as vo:
            vo.wait_until("f")
            self.play(Write(fe[1]))
            vo.wait_until("m")
            self.play(FadeIn(g), FadeIn(lab), Create(real_axis), FadeIn(zd))
            self.play(FadeIn(notes[0]))

        with self.voiceover(
            "Zeta also takes mirror-image values above and below the real axis. <bookmark mark='z'/> So if there were ever a zero "
            "off the line, <bookmark mark='p'/> it would have to bring three partners with it: one reflected across the critical "
            "line, and two more below."
        ) as vo:
            self.play(FadeIn(notes[1]))
            vo.wait_until("z")
            self.play(FadeIn(bad, scale=2), FadeIn(hypo))
            vo.wait_until("p")
            self.play(GrowFromCenter(mirror), FadeIn(partners[0]))
            self.play(GrowFromCenter(conj), FadeIn(partners[1:]))
            self.play(FadeIn(notes[2]))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def statement(self):
        rh = VGroup(
            label(r"\textbf{The Riemann hypothesis}", font_size=50),
            label(r"Every nontrivial zero of $\zeta(s)$ has real part exactly $\tfrac12$.", font_size=40, color=C.ZERO),
        ).arrange(DOWN, buff=0.45).move_to(UP * 1.2)
        box = SurroundingRectangle(rh, color=C.ZERO, buff=0.35, corner_radius=0.12)
        quote = VGroup(
            label(r"``\emph{Es ist sehr wahrscheinlich, dass alle Wurzeln reell sind.}''", font_size=30, color=GREY_A),
            label(r"``It is very probable that all the roots are real.''", font_size=30),
            note(r"B.\ Riemann, \emph{\"Uber die Anzahl der Primzahlen unter einer gegebenen Gr\"osse}, 1859. (``Real'' in his "
                 r"variable means on the critical line.)", font_size=22),
        ).arrange(DOWN, buff=0.22).next_to(box, DOWN, buff=0.6)
        with self.voiceover(
            "The Riemann hypothesis says that never happens: <bookmark mark='r'/> every nontrivial zero has real part exactly one "
            "half. <bookmark mark='q'/> In his 1859 paper, Riemann wrote that this was 'very probable', and that he had set "
            "aside the search for a proof, after a few fleeting attempts."
        ) as vo:
            vo.wait_until("r")
            self.play(FadeIn(rh), Create(box))
            vo.wait_until("q")
            self.play(FadeIn(quote, shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def evidence(self):
        h = load("hardy")
        ts, Z = h["t"], h["Z"]
        ax = Axes(x_range=[0, 52, 10], y_range=[-4, 4, 2], x_length=11.5, y_length=3.4, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_numbers": True, "font_size": 22}).to_edge(UP, buff=0.8)
        curve = polyline(ax, ts, Z, color=C.ZERO, stroke_width=3)
        gz = gammas(10)
        gz = gz[gz < 52]
        dots = VGroup(*[Dot(ax.c2p(t, 0), radius=0.07, color=WHITE) for t in gz])
        zl = label(r"Hardy's $Z(t)$: \ $|Z(t)| = |\zeta(\tfrac12 + it)|$, \ and $Z(t)$ is real", font_size=28).next_to(ax, UP, buff=0.15)
        tl = MathTex("t", font_size=30).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        sign_changes = int(np.count_nonzero(np.diff(np.sign(Z)) != 0))
        assert sign_changes == len(gz), (sign_changes, len(gz))

        with self.voiceover(
            "The evidence for it is overwhelming. Along the critical line, zeta can be rotated into a real-valued function, "
            "Hardy's Z function. <bookmark mark='c'/> Every zero on the line is a place where this curve crosses the axis. "
            "Here are the first ten."
        ) as vo:
            self.play(Create(ax), FadeIn(zl), FadeIn(tl))
            self.play(Create(curve), run_time=2.5, rate_func=linear)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.1))

        facts = VGroup(
            label(r"\textbf{1914}\quad Hardy: infinitely many zeros lie on the line", font_size=28),
            label(r"\textbf{1989}\quad Conrey: more than 40\% of them do", font_size=28),
            label(r"\textbf{2021}\quad Platt \& Trudgian: the first $" + PLATT_TRUDGIAN_ZEROS + r"$ zeros\\"
                  r"\phantom{\textbf{2021}\quad }(all up to height $3\times10^{12}$) are on the line", font_size=28),
            label(r"\textbf{2026}\quad preprints: more than two thirds are on the line (and simple)", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(ax, DOWN, buff=0.55)
        with self.voiceover(
            "In 1914, Hardy proved that infinitely many zeros lie on the line. <bookmark mark='c'/> Later work showed that a "
            "positive fraction do, more than forty percent by 1989. <bookmark mark='p'/> And computers have checked the zeros "
            "one by one: in 2021, Platt and Trudgian verified that the first twelve trillion zeros, every one up to a height of "
            "three trillion, lie exactly on the line. <bookmark mark='n'/> This year, a preprint whose argument is credited to "
            "an AI model, Anthropic's Claude, checked by Levent Alpöge and Ralph Furman, pushed the proven fraction past two "
            "thirds, and a second, independent proof followed."
        ) as vo:
            self.play(FadeIn(facts[0], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(facts[1], shift=RIGHT * 0.2))
            vo.wait_until("p")
            self.play(FadeIn(facts[2], shift=RIGHT * 0.2))
            vo.wait_until("n")
            self.play(FadeIn(facts[3], shift=RIGHT * 0.2))
        self.play(FadeOut(VGroup(ax, curve, dots, zl, tl)), facts.animate.to_edge(UP, buff=0.6))

        hist = VGroup(
            label(r"\textbf{1900}\quad Hilbert's list of 23 problems: number 8", font_size=30),
            label(r"\textbf{2000}\quad Clay Millennium Prize: \$1{,}000{,}000", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(facts, DOWN, buff=0.7).align_to(facts, LEFT)
        q = label(r"But why should the \emph{primes} care where these zeros are?", font_size=38, color=YELLOW).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Hilbert put the problem on his famous list in 1900, <bookmark mark='c'/> and in 2000 the Clay Mathematics Institute "
            "offered a million dollars for a proof. <bookmark mark='q'/> But why should the primes care where these zeros are?"
        ) as vo:
            self.play(FadeIn(hist[0], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(hist[1], shift=RIGHT * 0.2))
            vo.wait_until("q")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.wait(0.8)
        self.clear_scene()
