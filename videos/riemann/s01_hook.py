from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.riemann.common import (
    RELEASE, gammas, label, load, polyline, region, staircase, strip_axes, zero_dots,
)


class Hook(VoiceoverScene):
    def construct(self):
        self.grid_of_primes()
        self.staircase_and_curve()
        self.waves()
        self.hypothesis()
        self.news()
        self.roadmap()

    # ------------------------------------------------------------------
    def grid_of_primes(self):
        primes = set(int(p) for p in load("primes")["primes"][:30])
        cells = VGroup()
        for n in range(1, 101):
            t = MathTex(str(n), font_size=30, color=GREY_C)
            t.n = n
            cells.add(t)
        cells.arrange_in_grid(rows=10, cols=10, buff=(0.42, 0.18))
        cells.move_to(ORIGIN)
        prime_cells = [c for c in cells if c.n in primes]

        with self.voiceover(
            "Here are the prime numbers. <bookmark mark='p'/> Two, three, five, seven, eleven, thirteen: the whole numbers "
            "that can't be split into smaller factors. <bookmark mark='a'/> They're the atoms of arithmetic, and yet they "
            "seem to appear almost at random."
        ) as vo:
            self.play(FadeIn(cells, lag_ratio=0.01), run_time=1.5)
            vo.wait_until("p")
            self.play(LaggedStart(*[c.animate.set_color(C.PRIME).scale(1.15) for c in prime_cells], lag_ratio=0.12),
                      run_time=vo.until("a"))
            gaps = VGroup(*[SurroundingRectangle(VGroup(*[c for c in cells if lo <= c.n <= hi]), color=GREY_B,
                                                 buff=0.06, stroke_width=1.5)
                            for lo, hi in [(91, 96)]])
            self.play(Create(gaps))
            gap_l = label(r"91 through 96: not a single prime", font_size=26, color=GREY_B).next_to(cells, DOWN, buff=0.25)
            self.play(FadeIn(gap_l))
        self.clear_scene()

    # ------------------------------------------------------------------
    def staircase_and_curve(self):
        primes = load("primes")["primes"]
        ax = Axes(x_range=[0, 100, 10], y_range=[0, 26, 5], x_length=10.5, y_length=5.2,
                  axis_config={"stroke_color": GREY_B, "include_numbers": True, "font_size": 24},
                  tips=False).move_to(DOWN * 0.3)
        xl = MathTex("x", font_size=34).next_to(ax.x_axis.get_end(), RIGHT, buff=0.15)
        yl = label(r"number of primes up to $x$", font_size=28, color=C.PRIME).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        stairs = staircase(ax, primes[primes <= 100], x0=0, x1=100, color=C.PRIME)

        with self.voiceover(
            "Count them as you go, <bookmark mark='s'/> and you get a staircase that climbs by one at every prime. "
            "It's jagged and irregular in its details."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("s")
            self.play(Create(stairs), run_time=vo.remaining(), rate_func=linear)

        # Zoom out: up to 100,000
        X = 100_000
        ax2 = Axes(x_range=[0, X, 20_000], y_range=[0, 10_000, 2_000], x_length=10.5, y_length=5.2,
                   axis_config={"stroke_color": GREY_B, "include_numbers": True, "font_size": 24},
                   tips=False).move_to(DOWN * 0.3)
        xs = np.linspace(2, X, 1500)
        pis = np.searchsorted(primes, xs, side="right")
        stairs2 = polyline(ax2, xs, pis, color=C.PRIME, stroke_width=4)
        from videos.riemann.compute import li
        lis = np.array([li(x) for x in xs[::10]])
        curve = polyline(ax2, xs[::10], lis, color=C.SMOOTH, stroke_width=3)
        cl = label(r"a smooth curve", font_size=30, color=C.SMOOTH).next_to(ax2.c2p(70_000, li(70_000)), UP + LEFT, buff=0.2)

        with self.voiceover(
            "But zoom out, <bookmark mark='z'/> say to a hundred thousand, and the staircase follows <bookmark mark='c'/> a "
            "smooth curve almost perfectly. The primes are random in the small, but astonishingly regular in the large."
        ) as vo:
            vo.wait_until("z")
            self.play(ReplacementTransform(ax, ax2), ReplacementTransform(stairs, stairs2), run_time=2)
            vo.wait_until("c")
            self.play(Create(curve), run_time=1.5)
            self.play(FadeIn(cl))
        self.clear_scene()

    # ------------------------------------------------------------------
    def waves(self):
        d = load("riemann_pi")
        x, smooth, osc = d["x"], d["smooth"], d["osc"]
        primes = load("primes")["primes"]
        ax = Axes(x_range=[0, 100, 10], y_range=[0, 26, 5], x_length=10.5, y_length=5.0,
                  axis_config={"stroke_color": GREY_B, "include_numbers": True, "font_size": 24},
                  tips=False).move_to(DOWN * 0.55)
        stairs = staircase(ax, primes[primes <= 100], x0=0, x1=100, color=C.PRIME, stroke_width=3).set_stroke(opacity=0.45)

        def approx(K):
            return polyline(ax, x, smooth - osc[:K].sum(0), color=C.SMOOTH if K == 0 else C.ZERO, stroke_width=3.5)

        head = Tex(r"Riemann, 1859:\quad staircase $=$ ", r"smooth curve", r" $-$ ", r"a wave for every zero of $\zeta$",
                   font_size=34).to_edge(UP, buff=0.4)
        head[1].set_color(C.SMOOTH)
        head[3].set_color(C.ZERO)
        counter = VGroup(label(r"waves added:", font_size=28), Integer(0, font_size=34, color=C.ZERO)).arrange(RIGHT, buff=0.2)
        counter.next_to(ax.c2p(5, 24), RIGHT, buff=0)
        cur = approx(0)

        with self.voiceover(
            "In 1859, Bernhard Riemann found the reason. <bookmark mark='e'/> He found that the staircase is exactly equal to "
            "a smooth curve, <bookmark mark='w'/> plus a sum of waves, and that each wave comes from a single point where one "
            "particular function, the zeta function, equals zero."
        ) as vo:
            self.play(Create(ax), FadeIn(stairs))
            vo.wait_until("e")
            self.play(Create(cur), FadeIn(head), run_time=1.5)
            vo.wait_until("w")
            self.play(FadeIn(counter))
            w1 = polyline(ax, x, 8 - osc[0], color=C.ZERO, stroke_width=3)
            self.play(Create(w1), run_time=1.5)
            self.play(FadeOut(w1))

        steps = [1, 2, 3, 5, 10, 20, 50, 100, 200]
        with self.voiceover(
            "Add the waves one at a time, and the smooth curve bends, step by step, into the exact staircase of the primes. "
            "<bookmark mark='m'/> The zeros of zeta are like the frequencies in the music of the primes."
        ) as vo:
            per = (vo.until("m") - 0.3) / len(steps)
            for K in steps:
                self.play(Transform(cur, approx(K)), counter[1].animate.set_value(K), run_time=per)
            self.play(stairs.animate.set_stroke(opacity=1.0), run_time=0.8)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hypothesis(self):
        g = strip_axes(t_max=50, x_length=3.6, y_length=6.4).move_to(LEFT * 4.2 + DOWN * 0.2)
        ax = g.ax
        dots = zero_dots(ax, gammas(10))
        sl = MathTex(r"\Real(s)", font_size=28).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        tl = MathTex(r"\Imag(s)", font_size=28).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        statement = VGroup(
            label(r"\textbf{The Riemann hypothesis} (1859)", font_size=40),
            label(r"every nontrivial zero of the zeta function\\lies on the line $\Real(s) = \tfrac12$",
                  font_size=34, color=C.ZERO),
        ).arrange(DOWN, buff=0.35).move_to(RIGHT * 2.6 + UP * 1.4)
        prize = VGroup(
            MathTex(r"\$1{,}000{,}000", font_size=60, color=YELLOW),
            label(r"Clay Millennium Prize", font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.2).move_to(RIGHT * 2.6 + DOWN * 1.6)

        with self.voiceover(
            "Riemann guessed that all of these zeros <bookmark mark='l'/> lie on a single straight line. "
            "<bookmark mark='h'/> That guess, the Riemann hypothesis, is perhaps the most famous open problem in mathematics. "
            "<bookmark mark='p'/> It has been open for 167 years, and there's a million-dollar prize for a proof."
        ) as vo:
            self.play(FadeIn(g), FadeIn(sl), FadeIn(tl))
            self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.15), run_time=1.5)
            vo.wait_until("l")
            self.play(Indicate(g.crit, color=C.ZERO, scale_factor=1.03), run_time=1.2)
            vo.wait_until("h")
            self.play(FadeIn(statement, shift=UP * 0.2))
            vo.wait_until("p")
            self.play(FadeIn(prize, shift=UP * 0.2))
        self.play(FadeOut(statement), FadeOut(prize))
        self.strip = VGroup(g, dots, sl, tl)

    # ------------------------------------------------------------------
    def news(self):
        g = self.strip[0]
        ax = g.ax
        date = label(RELEASE["date"], font_size=40, color=C.DIM)
        head = label(rf"OpenAI releases {RELEASE['manuscripts']} AI-written math manuscripts", font_size=36)
        claim = label(r"including a claimed proof of the\\\textbf{quasi-Riemann hypothesis}", font_size=36, color=C.ZERO_FREE)
        VGroup(date, head, claim).arrange(DOWN, buff=0.35).move_to(RIGHT * 2.7 + UP * 1.6)
        line78 = DashedLine(ax.c2p(7 / 8, 0), ax.c2p(7 / 8, 50), color=C.ZERO_FREE, stroke_width=3)
        l78 = MathTex(r"\tfrac78", font_size=36, color=C.ZERO_FREE).next_to(ax.c2p(7 / 8, 50), UP, buff=0.12)
        shade = region(ax, 7 / 8, 1.35, 0, 50, opacity=0.3)
        nz = label(r"no zeros here", font_size=30, color=C.ZERO_FREE).move_to(ax.c2p(1.35, 10) + RIGHT * 1.9)
        nz_arrow = Arrow(nz.get_left(), ax.c2p(1.12, 10), buff=0.1, color=C.ZERO_FREE, stroke_width=3)
        weaker = label(r"weaker than the Riemann hypothesis, but long out of reach", font_size=30, color=GREY_A)
        weaker.next_to(claim, DOWN, buff=0.5)

        with self.voiceover(
            "On <bookmark mark='d'/> October sixth, 2026, OpenAI released 722 mathematical manuscripts written by an "
            "unreleased AI model. <bookmark mark='c'/> Among them is a claimed proof of something weaker than the Riemann "
            "hypothesis, but long out of reach: the quasi-Riemann hypothesis. <bookmark mark='z'/> It says that no zero lies to "
            "the right of the line where the real part is seven eighths."
        ) as vo:
            vo.wait_until("d")
            self.play(FadeIn(date, shift=DOWN * 0.2), FadeIn(head))
            vo.wait_until("c")
            self.play(FadeIn(claim, shift=UP * 0.2))
            vo.wait_until("z")
            self.play(FadeIn(shade), Create(line78), FadeIn(l78))
            self.play(FadeIn(nz), GrowArrow(nz_arrow))
            self.play(FadeIn(weaker))
        self.clear_scene()

    # ------------------------------------------------------------------
    def roadmap(self):
        parts = VGroup(
            label(r"\textbf{1.} The Riemann hypothesis: primes, zeta, and its zeros", font_size=34),
            label(r"\textbf{2.} Why the zeros control the primes", font_size=34),
            label(r"\textbf{3.} The quasi-Riemann claim: what it says, and how the proof works", font_size=34),
            label(r"\textbf{4.} What is verified, and what it does \emph{not} prove", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(ORIGIN)
        with self.voiceover(
            "In this video, <bookmark mark='a'/> we'll build up what the Riemann hypothesis really says, <bookmark mark='b'/> "
            "and why its zeros control the primes. <bookmark mark='c'/> Then we'll see what the new result claims and how its "
            "proof works, <bookmark mark='d'/> and finally what has been checked, and what it does not prove."
        ) as vo:
            for i, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(parts[i], shift=RIGHT * 0.2), run_time=0.8)
        self.wait(0.5)
        self.play(FadeOut(parts))

        card = VGroup(
            label(r"The Riemann Hypothesis", font_size=72),
            label(r"primes, zeros, and the 2026 quasi-Riemann proof", font_size=38, color=GREY_A),
        ).arrange(DOWN, buff=0.4)
        self.play(FadeIn(card, scale=1.05), run_time=1.2)
        self.wait(2.5)
        self.play(FadeOut(card))
