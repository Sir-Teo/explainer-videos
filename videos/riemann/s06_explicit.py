from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.riemann.common import part_card, gammas, label, load, note, polyline, psi_approx, psi_steps, psi_wave, staircase

X_MAX = 50.0


def main_axes():
    return Axes(x_range=[0, X_MAX, 10], y_range=[0, 55, 10], x_length=10.5, y_length=4.7, tips=False,
                axis_config={"stroke_color": GREY_B, "include_numbers": True, "font_size": 22}).move_to(DOWN * 1.15)


def explicit_formula(font_size=44) -> MathTex:
    f = MathTex(r"\psi(x)", r"=", r"x", r"-", r"\sum_{\rho} \frac{x^{\rho}}{\rho}", r"-", r"\ln 2\pi",
                r"-", r"\tfrac12 \ln\!\big(1 - x^{-2}\big)", font_size=font_size)
    f[0].set_color(C.PRIME)
    f[2].set_color(C.SMOOTH)
    f[4].set_color(C.ZERO)
    f[6:].set_color(GREY_B)
    return f


class ExplicitFormula(VoiceoverScene):
    def construct(self):
        self.card()
        self.chebyshev()
        self.formula()
        self.single_waves()
        self.rebuild()
        self.spectrum()

    def card(self):
        c = part_card(2, r"Why the zeros control the primes", r"waves, errors, and coin flips")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.8)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def chebyshev(self):
        ax = main_axes()
        jumps, heights = psi_steps(X_MAX)
        stairs = staircase(ax, jumps, heights, x0=0, x1=X_MAX, color=C.PRIME)
        line = ax.plot(lambda x: x, x_range=[0, X_MAX], color=C.SMOOTH, stroke_width=3)
        line_l = MathTex("y = x", font_size=32, color=C.SMOOTH).next_to(ax.c2p(46, 50), UP, buff=0.1)
        defn = MathTex(r"\psi(x)", r"=", r"\sum_{p^k \le x} \ln p", font_size=46).to_edge(UP, buff=0.5)
        defn[0].set_color(C.PRIME)
        cheb = note(r"Chebyshev's function: a jump of $\ln p$ at every prime power $p,\ p^2,\ p^3, \ldots$", font_size=26)
        cheb.next_to(defn, DOWN, buff=0.2)
        marks = VGroup()
        for x, txt in [(2, r"\ln 2"), (3, r"\ln 3"), (4, r"\ln 2"), (5, r"\ln 5"), (8, r"\ln 2"), (9, r"\ln 3")]:
            y = sum(h for j, h in zip(jumps, heights) if j <= x)
            m = MathTex(txt, font_size=20, color=C.PRIME).next_to(ax.c2p(x, y), LEFT, buff=0.06).shift(UP * 0.12)
            marks.add(m)
        pnt = label(r"prime number theorem $\iff \psi(x) \approx x$", font_size=30, color=C.SMOOTH)
        pnt.next_to(ax.c2p(4, 50), RIGHT, buff=0.1)

        with self.voiceover(
            "To see the connection, it's cleanest to count primes with weights. <bookmark mark='d'/> Instead of adding one at "
            "each prime, add the logarithm of p, and also count prime powers, like four, eight, and nine. "
            "<bookmark mark='s'/> This gives Chebyshev's function, psi of x, another staircase."
        ) as vo:
            vo.wait_until("d")
            self.play(Write(defn), FadeIn(cheb))
            vo.wait_until("s")
            self.play(Create(ax))
            self.play(Create(stairs), run_time=2.5, rate_func=linear)
        with self.voiceover(
            "The weights make it simpler: <bookmark mark='l'/> the prime number theorem now just says that psi of x is close "
            "to x."
        ) as vo:
            vo.wait_until("l")
            self.play(Create(line), FadeIn(line_l), FadeIn(pnt))
        self.play(FadeOut(VGroup(defn, cheb, pnt)))
        self.ax, self.stairs, self.line, self.line_l = ax, stairs, line, line_l

    # ------------------------------------------------------------------
    def formula(self):
        f = explicit_formula().to_edge(UP, buff=0.45)
        b_x = Brace(f[2], DOWN, buff=0.12, color=C.SMOOTH)
        b_x_l = label(r"smooth", font_size=24, color=C.SMOOTH).next_to(b_x, DOWN, buff=0.06)
        b_s = Brace(f[4], DOWN, buff=0.12, color=C.ZERO)
        b_s_l = label(r"one term for each zero $\rho$", font_size=24, color=C.ZERO).next_to(b_s, DOWN, buff=0.06)
        b_r = Brace(f[6:], DOWN, buff=0.12, color=GREY_B)
        b_r_l = label(r"small corrections", font_size=24, color=GREY_B).next_to(b_r, DOWN, buff=0.06)
        who = note(r"Riemann (1859); proved by von Mangoldt (1895)", font_size=24).to_corner(UR, buff=0.25)
        with self.voiceover(
            "Riemann's insight, made rigorous by von Mangoldt, is an exact formula for this staircase. "
            "<bookmark mark='x'/> It's x, <bookmark mark='s'/> minus a sum over all the nontrivial zeros, rho, of x to the rho "
            "over rho, <bookmark mark='c'/> minus a couple of small correction terms. That's it. Exact, for every x."
        ) as vo:
            self.play(Write(f), FadeIn(who), run_time=2)
            vo.wait_until("x")
            self.play(GrowFromCenter(b_x), FadeIn(b_x_l))
            vo.wait_until("s")
            self.play(GrowFromCenter(b_s), FadeIn(b_s_l))
            vo.wait_until("c")
            self.play(GrowFromCenter(b_r), FadeIn(b_r_l))
        self.wait(0.5)
        self.play(FadeOut(VGroup(b_x, b_x_l, b_s, b_s_l, b_r, b_r_l, who)))
        self.f = f

    # ------------------------------------------------------------------
    def single_waves(self):
        self.play(FadeOut(VGroup(self.ax, self.stairs, self.line, self.line_l)))
        rho = MathTex(r"\rho", r"=", r"\beta", r"+", r"i\gamma", font_size=40)
        rho[0].set_color(C.ZERO)
        rho[2].set_color(C.DANGER)
        rho[4].set_color(C.CHARACTER)
        xr = MathTex(r"x^{\rho}", r"=", r"x^{\beta}", r"\cdot", r"e^{\,i\gamma \ln x}", font_size=40)
        xr[0].set_color(C.ZERO)
        xr[2].set_color(C.DANGER)
        xr[4].set_color(C.CHARACTER)
        pair = MathTex(r"\frac{x^\rho}{\rho} + \frac{x^{\bar\rho}}{\bar\rho}", r"=", r"\frac{2\,x^{\beta}}{|\rho|}",
                       r"\cos\!\big(\gamma\ln x - \arg\rho\big)", font_size=40)
        pair[2].set_color(C.DANGER)
        pair[3].set_color(C.CHARACTER)
        col = VGroup(rho, xr, pair).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
        amp = label(r"real part $\beta$: how fast the wave grows", font_size=28, color=C.DANGER)
        freq = label(r"height $\gamma$: its frequency (in $\ln x$)", font_size=28, color=C.CHARACTER)
        VGroup(amp, freq).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(col, DOWN, buff=0.5).align_to(col, LEFT)

        with self.voiceover(
            "Each zero, together with its mirror image below the axis, contributes one wave. "
            "<bookmark mark='r'/> Write rho as beta plus i gamma. <bookmark mark='x'/> Then x to the rho is x to the beta, "
            "times e to the i gamma log x, <bookmark mark='p'/> and the pair of conjugate zeros adds up to a cosine. "
            "<bookmark mark='f'/> The height gamma sets the frequency of the wave, <bookmark mark='a'/> and the real part "
            "beta sets how fast its amplitude grows."
        ) as vo:
            vo.wait_until("r")
            self.play(Write(rho))
            vo.wait_until("x")
            self.play(Write(xr))
            vo.wait_until("p")
            self.play(Write(pair))
            vo.wait_until("f")
            self.play(FadeIn(freq, shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(amp, shift=RIGHT * 0.2))

        self.play(FadeOut(VGroup(rho, xr, amp, freq)), pair.animate.scale(0.8).to_corner(UL, buff=0.4).shift(DOWN * 1.2))
        g = gammas(3)
        rows = VGroup()
        for k in range(3):
            a = Axes(x_range=[0, X_MAX, 10], y_range=[-1.6, 1.6, 1], x_length=7.6, y_length=1.45, tips=False,
                     axis_config={"stroke_color": GREY_C, "include_ticks": False})
            xs, ys = psi_wave(k, X_MAX)
            curve = polyline(a, xs, ys, color=C.ZERO, stroke_width=2.5)
            tag = MathTex(rf"\rho = \tfrac12 + {g[k]:.2f}\,i", font_size=28, color=C.ZERO).next_to(a, LEFT, buff=0.3)
            rows.add(VGroup(a, curve, tag))
        rows.arrange(DOWN, buff=0.3).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.9)
        with self.voiceover(
            "Here's the wave from the first zero, at height 14.13. <bookmark mark='n'/> And here are the next two. "
            "On their own, they don't look like anything at all."
        ) as vo:
            self.play(Create(rows[0][0]), FadeIn(rows[0][2]), Create(rows[0][1]), run_time=1.5)
            vo.wait_until("n")
            for r in rows[1:]:
                self.play(Create(r[0]), FadeIn(r[2]), Create(r[1]), run_time=1.0)
        self.play(FadeOut(VGroup(rows, pair)))

    # ------------------------------------------------------------------
    def rebuild(self):
        ax = main_axes()
        jumps, heights = psi_steps(X_MAX)
        stairs = staircase(ax, jumps, heights, x0=0, x1=X_MAX, color=C.PRIME, stroke_width=3).set_stroke(opacity=0.5)

        def approx(K):
            xs, ys = psi_approx(K, X_MAX)
            return polyline(ax, xs, ys, color=C.SMOOTH if K == 0 else C.ZERO, stroke_width=3.2)

        counter = VGroup(label(r"zeros used:", font_size=30), Integer(0, font_size=36, color=C.ZERO)).arrange(RIGHT, buff=0.2)
        counter.next_to(ax.c2p(2, 50), RIGHT, buff=0)
        cur = approx(0)
        self.play(Create(ax), FadeIn(stairs))
        steps = [1, 2, 5, 10, 20, 50, 100, 300, 1000]
        with self.voiceover(
            "But start from the smooth line, x, <bookmark mark='s'/> and subtract the waves, one zero at a time. One. Two. Five. "
            "Twenty. A hundred. A thousand. <bookmark mark='e'/> The line bends, and bends, until it has become the staircase, "
            "jumping by log p at every prime power. Every prime is hiding in the zeros."
        ) as vo:
            self.play(Create(cur), FadeIn(counter))
            vo.wait_until("s")
            per = max(0.4, (vo.until("e") - 0.2) / len(steps))
            for K in steps:
                self.play(Transform(cur, approx(K)), counter[1].animate.set_value(K), run_time=per)
            self.play(stairs.animate.set_stroke(opacity=1.0))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spectrum(self):
        d = load("spectrum")
        g, f = d["g"], d["f"]
        ax = Axes(x_range=[0, 60, 10], y_range=[-2, 7, 2], x_length=11.5, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_numbers": True, "font_size": 22,
                               "numbers_to_exclude": [0]}).move_to(DOWN * 0.9)
        curve = polyline(ax, g, f, color=C.PRIME, stroke_width=2.5)
        zs = gammas(13)
        zs = zs[zs < 60]
        lines = VGroup(*[DashedLine(ax.c2p(z, -2), ax.c2p(z, 7), color=C.ZERO, stroke_width=1.8, dash_length=0.08) for z in zs])
        formula = MathTex(r"-\sum_{p^k \le 10^6} \frac{\ln p}{\sqrt{p^k}}\; w(p^k)\, \cos\!\big(t \ln p^k\big)", font_size=40)
        formula.to_edge(UP, buff=0.5)
        formula[0].set_color(C.PRIME)
        sub = note(r"real computation over the 78{,}734 prime powers below a million ($w$: a smooth taper)", font_size=24)
        sub.next_to(formula, DOWN, buff=0.2)
        tl = MathTex("t", font_size=30).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        zl = label(r"dashed: the zeros of $\zeta$", font_size=26, color=C.ZERO).next_to(ax, DOWN, buff=0.35)
        n_pp = int(np.count_nonzero(load("primes")["prime_powers"] <= 10_000))  # sanity: data present
        assert n_pp > 0
        from videos.riemann.compute import sieve
        primes = np.flatnonzero(sieve(10**6))
        count = sum(int(np.floor(np.log(10**6) / np.log(p) + 1e-12)) for p in primes)
        assert count == 78_734, count

        with self.voiceover(
            "And it works in reverse. <bookmark mark='f'/> Take only the primes and their powers below a million, and add up "
            "cosine waves, one for each, with frequency log p. <bookmark mark='c'/> As a function of t, the total is mostly "
            "noise, except for sharp peaks. <bookmark mark='z'/> And the peaks fall exactly at the zeros of zeta: 14.13, 21.02, "
            "25.01, and on and on."
        ) as vo:
            vo.wait_until("f")
            self.play(Write(formula), FadeIn(sub))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(tl))
            self.play(Create(curve), run_time=2.5, rate_func=linear)
            vo.wait_until("z")
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.1), FadeIn(zl), run_time=2)

        summary = label(r"The primes and the zeros are two descriptions of the same thing:\\"
                        r"heights $\gamma$ $\to$ where the steps fall; \ real parts $\beta$ $\to$ how big the waves are",
                        font_size=30)
        summary.to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The zeros are the frequencies of the primes, and the explicit formula is their Fourier series. The heights of the "
            "zeros decide where the steps fall. <bookmark mark='b'/> Their real parts decide how big the waves are. And that "
            "second fact is what the Riemann hypothesis is really about."
        ) as vo:
            self.play(FadeOut(zl))
            vo.wait_until("b")
            self.play(FadeIn(summary, shift=UP * 0.2))
        self.wait(0.8)
        self.clear_scene()
