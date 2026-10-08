from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.riemann.common import gammas, label, note, polyline, region, schematic_tag, strip_axes

C_DLVP = 1 / 5.558691  # sigma > 1 - C/ln t for |t| >= 2 (Mossinghoff, Trudgian & Yang)


class ErrorTerm(VoiceoverScene):
    def construct(self):
        self.two_waves()
        self.theta()
        self.known()
        self.pinching()
        self.quasi()

    # ------------------------------------------------------------------
    def two_waves(self):
        ax = Axes(x_range=[0, 1000, 200], y_range=[-560, 560, 200], x_length=11, y_length=5.0, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_numbers": True, "font_size": 22}).move_to(DOWN * 0.4)
        xs = np.linspace(1, 1000, 3000)
        phase = 14.13 * np.log(xs)
        w_half = polyline(ax, xs, np.sqrt(xs) * np.cos(phase), color=C.ZERO, stroke_width=2.5)
        w_09 = polyline(ax, xs, xs**0.9 * np.cos(phase + 1.0) * 0.98, color=C.DANGER, stroke_width=2.5)
        env_half = VGroup(polyline(ax, xs, np.sqrt(xs), color=C.ZERO, stroke_width=1.5), polyline(ax, xs, -np.sqrt(xs), color=C.ZERO, stroke_width=1.5))
        env_09 = VGroup(polyline(ax, xs, xs**0.9, color=C.DANGER, stroke_width=1.5), polyline(ax, xs, -xs**0.9, color=C.DANGER, stroke_width=1.5))
        for e in (*env_half, *env_09):
            e.set_stroke(opacity=0.6)
        l_half = MathTex(r"\beta = \tfrac12:\ \ \text{size}\ \sim x^{1/2}", font_size=32, color=C.ZERO)
        l_09 = MathTex(r"\beta = 0.9:\ \ \text{size}\ \sim x^{0.9}", font_size=32, color=C.DANGER)
        VGroup(l_half, l_09).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UL, buff=0.45)
        tag = schematic_tag()

        with self.voiceover(
            "Every wave grows like x to the beta. <bookmark mark='h'/> If a zero sits on the critical line, its wave grows like "
            "the square root of x. <bookmark mark='n'/> But if there were a zero with real part 0.9, its wave would grow like x "
            "to the 0.9, <bookmark mark='d'/> and in the long run it would dwarf every wave from the critical line."
        ) as vo:
            self.play(Create(ax), FadeIn(tag))
            vo.wait_until("h")
            self.play(Create(w_half), FadeIn(env_half), FadeIn(l_half), run_time=1.5)
            vo.wait_until("n")
            self.play(Create(w_09), FadeIn(env_09), FadeIn(l_09), run_time=2)
            vo.wait_until("d")
            self.play(Indicate(l_09, color=C.DANGER))
        self.clear_scene()

    # ------------------------------------------------------------------
    def theta(self):
        th = MathTex(r"\Theta", r"=", r"\sup\,\{\, \Real(\rho) : \zeta(\rho) = 0,\ \rho \text{ nontrivial}\,\}", font_size=46)
        th[0].set_color(C.DANGER)
        th.to_edge(UP, buff=0.7)
        th_l = label(r"the real part of the rightmost zero", font_size=30, color=GREY_A).next_to(th, DOWN, buff=0.2)
        errs = VGroup(
            MathTex(r"\psi(x) - x", r"\;\approx\;", r"x^{\Theta}", font_size=48),
            MathTex(r"\pi(x) - \li(x)", r"\;\approx\;", r"x^{\Theta}", font_size=48),
        ).arrange(DOWN, buff=0.35).move_to(DOWN * 0.3)
        for e in errs:
            e[2].set_color(C.DANGER)
        fine = note(r"(up to logarithmic factors, and no smaller exponent works)", font_size=24).next_to(errs, DOWN, buff=0.25)
        rh = VGroup(
            MathTex(r"\text{RH}", r"\iff", r"\Theta = \tfrac12", r"\iff", r"\pi(x) = \li(x) + O\big(\sqrt{x}\,\ln x\big)", font_size=42),
            note(r"H.\ von Koch, 1901", font_size=24),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.6)
        rh[0][2].set_color(C.ZERO)
        box = SurroundingRectangle(rh[0], color=C.ZERO, buff=0.18, corner_radius=0.1)

        with self.voiceover(
            "So the size of the error in counting primes is set by the rightmost zero. <bookmark mark='t'/> Call Theta the "
            "largest real part of any nontrivial zero. <bookmark mark='e'/> Then the error in psi of x, and in pi of x, is about "
            "x to the Theta, and no smaller power of x will do."
        ) as vo:
            vo.wait_until("t")
            self.play(Write(th), FadeIn(th_l))
            vo.wait_until("e")
            self.play(FadeIn(errs, shift=UP * 0.2))
            self.play(FadeIn(fine))
        with self.voiceover(
            "The Riemann hypothesis says Theta is one half: <bookmark mark='r'/> the error is about the square root of x, the "
            "smallest it could possibly be. Von Koch showed in 1901 that these are exactly equivalent. That's the precise sense "
            "in which the primes are as regular as they can be."
        ) as vo:
            vo.wait_until("r")
            self.play(FadeIn(rh), Create(box))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def known(self):
        g = strip_axes(t_max=40, x_length=5.0, y_length=6.2).move_to(LEFT * 3.6 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(0.5, t), radius=0.05, color=C.ZERO) for t in gammas(8)])
        line1 = Line(ax.c2p(1, 0), ax.c2p(1, 40), color=C.ZERO_FREE, stroke_width=7)
        facts = VGroup(
            label(r"$\Theta \ge \tfrac12$: \ there are zeros on the line", font_size=30),
            label(r"$\Theta \le 1$: \ no zeros to the right of $\Real(s) = 1$\\(the Euler product converges there)", font_size=30),
            label(r"\textbf{1896:} \ no zeros \emph{on} the line $\Real(s) = 1$\\$\Rightarrow$ the prime number theorem", font_size=30,
                  color=C.ZERO_FREE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(RIGHT * 2.7 + UP * 0.3)

        with self.voiceover(
            "So what do we actually know? <bookmark mark='a'/> Theta is at least a half, since there are zeros on the line. "
            "<bookmark mark='b'/> And Theta is at most one, because to the right of that line the Euler product converges, and "
            "a convergent product of nonzero factors can't be zero. <bookmark mark='c'/> The prime number theorem itself, in "
            "1896, came down to showing that there are no zeros on the line real-part-one."
        ) as vo:
            self.play(FadeIn(g), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(facts[0], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(facts[1], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(facts[2], shift=RIGHT * 0.2), Create(line1))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pinching(self):
        # Real-scale picture: horizontal = sigma near 1, vertical = log10 of the height t.
        ax = Axes(x_range=[0.75, 1.0, 0.05], y_range=[0, 60, 10], x_length=6.0, y_length=5.8, tips=False,
                  axis_config={"stroke_color": GREY_B, "font_size": 22},
                  x_axis_config={"include_numbers": True, "decimal_number_config": {"num_decimal_places": 2}},
                  y_axis_config={"include_numbers": False}).move_to(LEFT * 2.7 + DOWN * 0.3)
        ylabels = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=24).next_to(ax.c2p(0.75, k), LEFT, buff=0.12) for k in range(10, 61, 10)])
        yname = label(r"height $t$", font_size=26).next_to(ax.c2p(0.75, 60), UP, buff=0.15)
        one = Line(ax.c2p(1, 0), ax.c2p(1, 60), color=C.ZERO_FREE, stroke_width=4)
        ys = np.linspace(0.31, 60, 400)  # log10 t, from t = 2
        sig = 1 - C_DLVP / (ys * np.log(10))
        pts = [ax.c2p(s, y) for s, y in zip(sig, ys)] + [ax.c2p(1, 60), ax.c2p(1, 0.31)]
        sliver = Polygon(*pts, stroke_width=0, fill_color=C.ZERO_FREE, fill_opacity=0.45)
        edge = polyline(ax, sig, ys, color=C.ZERO_FREE, stroke_width=2.5)
        form = VGroup(
            label(r"zero-free region\\(de la Vall\'ee Poussin, 1899)", font_size=30, color=C.ZERO_FREE),
            MathTex(r"\Real(s) > 1 - \frac{c}{\ln t}", font_size=40, color=C.ZERO_FREE),
            note(r"drawn to scale with $c = 1/5.56$\\(Mossinghoff, Trudgian \& Yang)", font_size=22),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.6 + UP * 1.4)
        vk = VGroup(
            label(r"Vinogradov--Korobov (1958):", font_size=28),
            MathTex(r"1 - \frac{c'}{(\ln t)^{2/3}(\ln\ln t)^{1/3}}", font_size=36, color=C.ZERO_FREE),
            label(r"better only at astronomical heights,\\and it still pinches toward 1", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.6 + DOWN * 1.9)
        width_lo = 1 - sig[0]
        width_hi = 1 - sig[-1]
        assert width_lo > 20 * width_hi

        with self.voiceover(
            "Then came zero-free regions. <bookmark mark='d'/> In 1899, de la Vallée Poussin showed there are no zeros in a thin "
            "region hugging that line. <bookmark mark='p'/> But here it is drawn to scale, with the height on a logarithmic "
            "axis. As you go up, the region gets thinner and thinner, like one over the logarithm of the height."
        ) as vo:
            self.play(Create(ax), FadeIn(ylabels), FadeIn(yname), Create(one))
            vo.wait_until("d")
            self.play(FadeIn(sliver), Create(edge), FadeIn(form[:2]))
            vo.wait_until("p")
            self.play(FadeIn(form[2]))
            self.play(Indicate(VGroup(sliver, edge), color=C.ZERO_FREE, scale_factor=1.02))
        with self.voiceover(
            "In 1958, Vinogradov and Korobov found a region that shrinks more slowly, though with the explicit constants known today it only "
            "wins at astronomically large heights. <bookmark mark='s'/> And it still pinches toward the line. For more than a "
            "century, every zero-free region known has had this shape."
        ) as vo:
            self.play(FadeIn(vk[:2]))
            vo.wait_until("s")
            self.play(FadeIn(vk[2]))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quasi(self):
        g = strip_axes(t_max=60, x_length=5.0, y_length=6.2).move_to(LEFT * 3.6 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(0.5, t), radius=0.05, color=C.ZERO) for t in gammas(13)])
        ts = np.linspace(2, 60, 200)
        pinch = 1 - 0.32 / np.log(ts + 1)
        pts = [ax.c2p(s, t) for s, t in zip(pinch, ts)] + [ax.c2p(1, 60), ax.c2p(1, 2)]
        sliver = Polygon(*pts, stroke_width=0, fill_color=C.ZERO_FREE, fill_opacity=0.45)
        theta = 0.8
        band = region(ax, theta, 1.35, 0, 60, opacity=0.35)
        th_line = DashedLine(ax.c2p(theta, 0), ax.c2p(theta, 60), color=C.ZERO_FREE, stroke_width=3)
        th_l = MathTex(r"\theta", font_size=34, color=C.ZERO_FREE).next_to(ax.c2p(theta, 60), UP, buff=0.1)
        stmt = VGroup(
            label(r"\textbf{The quasi-Riemann hypothesis}", font_size=38, color=C.ZERO_FREE),
            label(r"there is a fixed $\theta < 1$ such that\\$\zeta(s) \ne 0$ whenever $\Real(s) > \theta$", font_size=34),
            MathTex(r"\iff \pi(x) = \li(x) + O\big(x^{\theta + \varepsilon}\big)", font_size=38),
            label(r"a ``power saving'' in the prime number theorem", font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.35).move_to(RIGHT * 2.9 + UP * 0.3)
        never = label(r"Before October 2026: not known even for $\theta = 0.999999$", font_size=30, color=YELLOW)
        never.to_edge(DOWN, buff=0.35).shift(RIGHT * 2.4)
        schem = schematic_tag(UL)

        with self.voiceover(
            "And a region that pinches toward the line isn't enough to push Theta below one. <bookmark mark='h'/> Far enough "
            "up, a zero could still be hiding arbitrarily close to the line real-part-one, and the error term would be almost "
            "as big as x itself."
        ) as vo:
            self.play(FadeIn(g), FadeIn(dots), FadeIn(sliver), FadeIn(schem))
            vo.wait_until("h")
            bad = Dot(ax.c2p(0.97, 56), radius=0.08, color=C.DANGER)
            self.play(FadeIn(bad, scale=2))
            self.play(Indicate(bad, color=C.DANGER))

        with self.voiceover(
            "The statement that Theta is strictly less than one, <bookmark mark='b'/> that there's a zero-free strip of fixed "
            "width, the same at every height, <bookmark mark='q'/> is called the quasi-Riemann hypothesis. <bookmark mark='p'/> "
            "For the primes, it says the error is at most x to some fixed power less than one: a power saving. "
            "<bookmark mark='n'/> Before October 2026, no one could prove that there are no zeros past real part 0.999999."
        ) as vo:
            self.play(FadeOut(bad))
            vo.wait_until("b")
            self.play(FadeOut(sliver), FadeIn(band), Create(th_line), FadeIn(th_l))
            vo.wait_until("q")
            self.play(FadeIn(stmt[:2], shift=UP * 0.2))
            vo.wait_until("p")
            self.play(FadeIn(stmt[2:], shift=UP * 0.2))
            vo.wait_until("n")
            self.play(FadeIn(never, shift=UP * 0.2))
        self.wait(0.8)
        self.clear_scene()
