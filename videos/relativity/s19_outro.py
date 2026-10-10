from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity.common import BHShader, Raster, boxed, label, load, mtex, note


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.finale()
        self.credits()

    # ------------------------------------------------------------------
    def recap(self):
        sh = BHShader(load("bh80"), exposure=0.8)
        t = ValueTracker(0.0)
        W = 5.3
        img = Raster(lambda v: sh(v), t, W, W * 720 / 1280, center=[4.3, 0.4, 0], alpha=0.0)

        def item(head, formula, color):
            h = label(head, font_size=26, color=GREY_A)
            f = MathTex(formula, font_size=32, color=color)
            return VGroup(h, f).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        items = VGroup(
            item(r"free fall erases gravity locally, so gravity is geometry:",
                 r"ds^2 = -\big(1 + \tfrac{2\Phi}{c^2}\big)c^2dt^2 + \cdots", C.PROPER_TIME),
            item(r"falling is maximal aging; Newton is the geodesic equation:",
                 r"\ddot x^\lambda + \Gamma^\lambda{}_{\mu\nu}\dot x^\mu\dot x^\nu = 0", C.CONNECTION),
            item(r"what can't be erased, tides, is curvature:",
                 r"\tfrac{D^2\xi^\mu}{d\tau^2} = R^\mu{}_{\nu\rho\sigma}u^\nu u^\rho\xi^\sigma", C.CURVATURE),
            item(r"conservation + Bianchi + Newton (or one action):",
                 r"G_{\mu\nu} + \Lambda g_{\mu\nu} = \tfrac{8\pi G}{c^4}T_{\mu\nu}", C.MATTER),
            item(r"Schwarzschild: $43''$ for Mercury, $1.75''$ for light, black holes;",
                 r"\text{and ripples at } c:\ \Box\,\bar h_{\mu\nu} = -\tfrac{16\pi G}{c^4}T_{\mu\nu}", C.WAVE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT, buff=0.5)
        limit = img.get_left()[0] - 0.25
        for it in items:
            if it.get_right()[0] > limit:
                it.scale_to_fit_width(limit - it.get_left()[0]).align_to(items, LEFT)
        with self.voiceover(
            "Let's put it all together. <bookmark mark='a'/> It started with a falling elevator: in free fall, gravity "
            "disappears, at least locally. So gravity can't be an ordinary force. It has to be part of the geometry of "
            "spacetime, and its slow-motion part lives in the rate of clocks, in the time component of the metric. "
            "<bookmark mark='b'/> Free objects follow the paths of maximal proper time, and for slow objects, the geodesic "
            "equation reproduces Newton's law."
        ) as vo:
            self.add(img)
            self.play(img.fade(1.0), t.animate.set_value(6.0), run_time=1.5, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(items[0], shift=RIGHT * 0.2), t.animate.set_value(20), run_time=vo.until("b"), rate_func=linear)
            self.play(FadeIn(items[1], shift=RIGHT * 0.2), t.animate.set_value(32), run_time=vo.remaining(), rate_func=linear)
        with self.voiceover(
            "<bookmark mark='c'/> What falling can't erase is tides: neighboring free paths converging and spreading apart. "
            "That's curvature, measured by the Riemann tensor. <bookmark mark='d'/> Matter enters through the stress–energy "
            "tensor, and the requirement that the geometry side conserve energy and momentum as automatically as matter "
            "does, together with Newton's limit, leaves exactly one equation. Hilbert's action gives the same one, and "
            "Lovelock showed there's no other. <bookmark mark='e'/> Its first solution explained Mercury and predicted the "
            "bending of light, and it went on to predict black holes, and waves in spacetime itself, a hundred years "
            "before they were observed."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeIn(items[2], shift=RIGHT * 0.2), t.animate.set_value(44), run_time=vo.until("d"), rate_func=linear)
            self.play(FadeIn(items[3], shift=RIGHT * 0.2), t.animate.set_value(60), run_time=vo.until("e"), rate_func=linear)
            self.play(FadeIn(items[4], shift=RIGHT * 0.2), t.animate.set_value(76), run_time=vo.remaining(), rate_func=linear)
        img.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def finale(self):
        eq = mtex(r"G_{\mu\nu}", r"=", r"\frac{8\pi G}{c^4}", r"\,T_{\mu\nu}", font_size=90)
        eq[0].set_color(C.CURVATURE)
        eq[3].set_color(C.MATTER)
        eb = boxed(eq, color=C.CURVATURE, buff=0.4).move_to(UP * 0.7)
        q = VGroup(label(r"Spacetime tells matter how to move;", font_size=34),
                   label(r"matter tells spacetime how to curve.", font_size=34)).arrange(DOWN, buff=0.15)
        q.next_to(eb, DOWN, buff=0.7)
        with self.voiceover(
            "Ten equations, one line. <bookmark mark='q'/> Spacetime tells matter how to move; matter tells spacetime "
            "how to curve. Thanks for watching."
        ) as vo:
            self.play(Write(eq), Create(eb[0]), run_time=2)
            vo.wait_until("q")
            self.play(FadeIn(q, lag_ratio=0.3))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def credits(self):
        hist = VGroup(
            label(r"Newton (1687) \quad Gauss (1827) \quad Riemann (1854) \quad Christoffel (1869) \quad "
                  r"Ricci \& Levi-Civita (1900) \quad Bianchi (1902)", font_size=22, color=GREY_A),
            label(r"Einstein (1905, 1907, 1911, 1915) \quad Grossmann (1913) \quad Hilbert (1915) \quad "
                  r"Schwarzschild (1916) \quad Flamm (1916) \quad Eddington, Dyson, Crommelin, Davidson (1919)",
                  font_size=22, color=GREY_A),
            label(r"Friedmann (1922) \quad Birkhoff (1923) \quad Pound \& Rebka (1959) \quad Lovelock (1971) \quad "
                  r"Luminet (1979) \quad Baez \& Bunn (2005) \quad LIGO (2015) \quad EHT (2019)", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.2)
        made = VGroup(
            label(r"Every orbit, light ray, curvature component and number in this video is computed and checked "
                  r"against the formula it illustrates.", font_size=22),
            label(r"Gravitational-wave data: LIGO via gwosc.org. \ M87* image: EHT Collaboration (ESO), CC BY 4.0.",
                  font_size=22, color=GREY_B),
            label(r"Animated with Manim Community; narrated by Kokoro-82M; source: \texttt{videos/relativity}",
                  font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.16)
        g = VGroup(label(r"The ideas in this video", font_size=34), hist, made).arrange(DOWN, buff=0.5)
        self.play(FadeIn(g, shift=UP * 0.2))
        self.wait(6)
        self.play(FadeOut(g))
