from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity2.common import KerrShader, Raster, boxed, label, load, mtex, note


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.finale()
        self.credits()

    # ------------------------------------------------------------------
    def recap(self):
        sh = KerrShader(load("kerr80"))
        t = ValueTracker(0.0)
        W = 5.3
        img = Raster(lambda v: sh(v), t, W, W * 720 / 1280, center=[4.3, 0.4, 0], alpha=0.0)

        def item(head, formula, color):
            h = label(head, font_size=26, color=GREY_A)
            f = MathTex(formula, font_size=32, color=color)
            return VGroup(h, f).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        items = VGroup(
            item(r"the right coordinates see through the horizon; inside, $r$ is time:",
                 r"UV = \Big(1 - \frac{r}{2M}\Big)e^{r/2M}", C.CURVATURE),
            item(r"gravity focuses, so trapped surfaces mean singularities:",
                 r"\frac{d\theta}{d\tau} = -\tfrac13\theta^2 - \sigma^2 + \omega^2 - R_{\mu\nu}u^\mu u^\nu", C.EXPANSION),
            item(r"spinning holes drag spacetime, and store extractable energy:",
                 r"dM = \tfrac{\kappa}{8\pi}\,dA + \Omega_H\,dJ,\qquad dA \ge 0", C.SPIN),
            item(r"waves carry energy; orbits shrink and chirp:",
                 r"L = \tfrac15\big\langle\dddot Q_{ij}\dddot Q_{ij}\big\rangle", C.WAVE),
            item(r"quantum fields make horizons glow:",
                 r"T_H = \frac{\hbar c^3}{8\pi GMk_B},\qquad S = \frac{k_Bc^3A}{4G\hbar}", C.TEMPERATURE),
            item(r"and the universe itself is a solution:",
                 r"H^2 = \tfrac{8\pi G}{3}\rho - \tfrac{kc^2}{a^2} + \tfrac{\Lambda c^2}{3}", C.METRIC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(LEFT, buff=0.5)
        limit = img.get_left()[0] - 0.25
        for it in items:
            if it.get_right()[0] > limit:
                it.scale_to_fit_width(limit - it.get_left()[0]).align_to(items, LEFT)
        with self.voiceover(
            "Let's put it together. <bookmark mark='a'/> Choosing coordinates that follow light showed us that the "
            "horizon is an ordinary place to cross, and that inside, r becomes time. <bookmark mark='b'/> "
            "Raychaudhuri's equation showed that gravity always focuses, so once a trapped surface forms, a singularity "
            "is unavoidable. <bookmark mark='c'/> Spinning black holes drag spacetime around them, and store energy "
            "that can be mined, while their area only grows."
        ) as vo:
            self.add(img)
            self.play(img.fade(1.0), t.animate.set_value(8.0), run_time=1.5, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(items[0], shift=RIGHT * 0.2), t.animate.set_value(30), run_time=vo.until("b"), rate_func=linear)
            self.play(FadeIn(items[1], shift=RIGHT * 0.2), t.animate.set_value(50), run_time=vo.until("c"), rate_func=linear)
            self.play(FadeIn(items[2], shift=RIGHT * 0.2), t.animate.set_value(70), run_time=vo.remaining(), rate_func=linear)
        with self.voiceover(
            "<bookmark mark='d'/> Gravitational waves carry energy away, and from that one fact we derived the chirp "
            "of merging black holes and the slow death of the binary pulsar. <bookmark mark='e'/> Quantum theory turned "
            "the laws of black-hole mechanics into real thermodynamics, with a temperature and an entropy. "
            "<bookmark mark='f'/> And the same equation, applied to everything at once, describes an expanding "
            "universe, with horizons of its own."
        ) as vo:
            vo.wait_until("d")
            self.play(FadeIn(items[3], shift=RIGHT * 0.2), t.animate.set_value(90), run_time=vo.until("e"), rate_func=linear)
            self.play(FadeIn(items[4], shift=RIGHT * 0.2), t.animate.set_value(110), run_time=vo.until("f"), rate_func=linear)
            self.play(FadeIn(items[5], shift=RIGHT * 0.2), t.animate.set_value(130), run_time=vo.remaining(), rate_func=linear)
        img.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def finale(self):
        eq = mtex(r"G_{\mu\nu}", r"+", r"\Lambda g_{\mu\nu}", r"=", r"\frac{8\pi G}{c^4}", r"\,T_{\mu\nu}", font_size=84)
        eq[0].set_color(C.CURVATURE)
        eq[2].set_color(C.LAMBDA)
        eq[5].set_color(C.MATTER)
        eb = boxed(eq, color=C.CURVATURE, buff=0.4).move_to(UP * 0.7)
        q = VGroup(label(r"From a falling elevator", font_size=34),
                   label(r"to the edge of the observable universe.", font_size=34)).arrange(DOWN, buff=0.15)
        q.next_to(eb, DOWN, buff=0.7)
        with self.voiceover(
            "All of it from one line, <bookmark mark='q'/> derived from a falling elevator, and reaching to the edge of "
            "the observable universe. Thanks for watching."
        ) as vo:
            self.play(Write(eq), Create(eb[0]), run_time=2)
            vo.wait_until("q")
            self.play(FadeIn(q, lag_ratio=0.3))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def credits(self):
        hist = VGroup(
            label(r"Eddington (1924) \quad Einstein \& Rosen (1935) \quad Oppenheimer \& Snyder (1939) \quad Raychaudhuri (1955) "
                  r"\quad Regge \& Wheeler (1957)", font_size=21, color=GREY_A),
            label(r"Finkelstein (1958) \quad Kruskal, Szekeres (1960) \quad Fuller \& Wheeler (1962) \quad Kerr (1963) "
                  r"\quad Penrose (1963, 1965, 1969) \quad Peters \& Mathews (1963)", font_size=21, color=GREY_A),
            label(r"Boyer \& Lindquist (1967) \quad Carter (1968) \quad Christodoulou (1970) \quad Hawking (1971, 1974) "
                  r"\quad Bardeen, Press \& Teukolsky (1972) \quad Bekenstein (1972)", font_size=21, color=GREY_A),
            label(r"Bardeen, Carter \& Hawking (1973) \quad Bardeen (1973) \quad Hulse \& Taylor (1974) \quad Leaver (1985) "
                  r"\quad Gravity Probe B (2011) \quad LIGO--Virgo--KAGRA (2015--2025)", font_size=21, color=GREY_A),
            label(r"Friedmann (1922) \quad Lema\^itre (1927) \quad Hubble (1929) \quad Robertson \& Walker (1935--37) "
                  r"\quad Davis \& Lineweaver (2004) \quad Planck (2018) \quad EHT (2019, 2022)", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.18)
        made = VGroup(
            label(r"Every worldline, light ray, black-hole image, ringdown, spectrum and number in this video is computed, "
                  r"and checked against the formula it illustrates.", font_size=21),
            label(r"Gravitational-wave data: LIGO via gwosc.org. \ Event parameters: LVK (GWTC-1; GW250114, PRL 2025).",
                  font_size=21, color=GREY_B),
            label(r"Animated with Manim Community; narrated by Kokoro-82M; source: \texttt{videos/relativity2}", font_size=21,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.15)
        g = VGroup(label(r"The ideas in this video", font_size=34), hist, made).arrange(DOWN, buff=0.45)
        self.play(FadeIn(g, shift=UP * 0.2))
        self.wait(6)
        self.play(FadeOut(g))
