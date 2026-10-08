from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.riemann.common import gammas, label, load, note, polyline, psi_approx, psi_steps, region, staircase, strip_axes


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.credits()

    # ------------------------------------------------------------------
    def recap(self):
        # Left: the picture that ties it together (staircase from zeros, then the strip).
        ax = Axes(x_range=[0, 50, 10], y_range=[0, 55, 10], x_length=5.6, y_length=3.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to(LEFT * 3.9 + UP * 1.6)
        jumps, heights = psi_steps(50)
        stairs = staircase(ax, jumps, heights, x0=0, x1=50, color=C.PRIME, stroke_width=2.5)
        xs, ys = psi_approx(300, 50)
        approx = polyline(ax, xs, ys, color=C.ZERO, stroke_width=2)
        g = strip_axes(t_max=50, x_length=3.6, y_length=3.4, labels=False).move_to(LEFT * 3.9 + DOWN * 2.0)
        sax = g.ax
        dots = VGroup(*[Dot(sax.c2p(0.5, t), radius=0.04, color=C.ZERO) for t in gammas(10)])
        shade = VGroup(region(sax, 7 / 8, 1.35, 0, 50, opacity=0.3), region(sax, -0.35, 1 / 8, 0, 50, opacity=0.3))

        items = VGroup(
            label(r"Primes: random in the small, regular in the large.", font_size=26, tex_environment="flushleft"),
            label(r"Euler's product ties $\zeta$ to the primes; continuation extends it.", font_size=26, tex_environment="flushleft"),
            label(r"The explicit formula: primes $=$ smooth trend $-$ a wave per zero.", font_size=26, tex_environment="flushleft"),
            label(r"Real part of the rightmost zero $=$ size of the error.\\RH: $\tfrac12$. \ Quasi-RH: some fixed $\theta < 1$.",
                  font_size=26, tex_environment="flushleft"),
            label(r"M\"obius sums that cancel $\Rightarrow$ zero-free half-planes.", font_size=26, tex_environment="flushleft"),
            label(r"The 2026 claim: hide one M\"obius sum in a sextic family;\\Poisson, Gauss sums, the cubic theta function,"
                  r"\\and the quadratic large sieve tame the family;\\sixth-power copies give $\tfrac{11}{12}$; refinements give $\tfrac78$.",
                  font_size=26, tex_environment="flushleft"),
            label(r"Unrefereed but Lean-formalized; RH itself remains open.", font_size=26, tex_environment="flushleft", color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        items.move_to([0, 0, 0]).align_to([-0.55, 0, 0], LEFT)

        with self.voiceover(
            "Let's recap. <bookmark mark='a'/> The primes look random in the small but are astonishingly regular in the large. "
            "<bookmark mark='b'/> Euler's product ties the zeta function to the primes, and analytic continuation extends it to "
            "the whole complex plane. <bookmark mark='c'/> The explicit formula writes the primes as a smooth trend minus one wave "
            "for every zero."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(items[0]), Create(ax), Create(stairs))
            vo.wait_until("b")
            self.play(FadeIn(items[1]))
            vo.wait_until("c")
            self.play(FadeIn(items[2]), Create(approx), run_time=1.5)
        with self.voiceover(
            "The real part of the rightmost zero sets the size of the error. <bookmark mark='r'/> The Riemann hypothesis says one "
            "half; the quasi-Riemann hypothesis says anything less than one. <bookmark mark='m'/> Cancellation in Möbius sums is "
            "what keeps zeros away."
        ) as vo:
            self.play(FadeIn(items[3]), FadeIn(g), FadeIn(dots))
            vo.wait_until("m")
            self.play(FadeIn(items[4]))
        with self.voiceover(
            "The 2026 claim hides one Möbius sum in a family twisted by sixth-power symbols, tames the family with Poisson "
            "summation, Gauss sums, the cubic theta function and the quadratic large sieve, <bookmark mark='e'/> and uses the "
            "sixth-power copies to reach eleven twelfths, with refinements reaching seven eighths. <bookmark mark='s'/> It's "
            "unrefereed, but formalized in Lean. And the Riemann hypothesis itself is still waiting."
        ) as vo:
            self.play(FadeIn(items[5]))
            vo.wait_until("e")
            self.play(FadeIn(shade))
            vo.wait_until("s")
            self.play(FadeIn(items[6]), Indicate(g.crit, color=C.ZERO))
        self.wait(1.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def credits(self):
        title = label(r"The Riemann Hypothesis, Visualized", font_size=46)
        lines = VGroup(
            label(r"Primary source: OpenAI, \texttt{github.com/openai/math}, family 003 (Sept.\ 30 / Oct.\ 1 / Oct.\ 5, 2026)",
                  font_size=24),
            label(r"B.\ Riemann (1859); H.\ von Koch (1901); J.\ E.\ Littlewood (1912); D.\ Platt \& T.\ Trudgian (2021)", font_size=24),
            label(r"Every zero, prime count, M\"obius walk and Gauss sum on screen was computed (mpmath, NumPy)", font_size=24),
            label(r"Animated with Manim Community; narrated by Kokoro-82M", font_size=24),
            label(r"Sources and fact-check notes: \texttt{videos/riemann/README.md}", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.22)
        VGroup(title, lines).arrange(DOWN, buff=0.6)
        self.play(FadeIn(title, shift=UP * 0.2))
        self.play(LaggedStart(*[FadeIn(l) for l in lines], lag_ratio=0.2), run_time=2)
        self.wait(4)
        self.play(FadeOut(VGroup(title, lines)))
