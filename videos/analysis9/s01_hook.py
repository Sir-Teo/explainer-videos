from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis9.common import area_under, load, plain_axes, polyline, rho


TOP = 4.2  # the top of the spike panels


def spike_halves(ax, x, y, color, stroke_width, top=TOP):
    """The graph of a spike peaked at 0, cut where it leaves the window (never flattened), as two pieces, left and
    right of the peak: the group keeps one shape whether or not the spike fits."""
    out = VGroup()
    for side in (x <= 0, x >= 0):
        xs, ys = x[side], y[side]
        if side[0]:  # left half: rising
            k = np.flatnonzero(ys > top)
            if len(k):
                i = k[0]
                xc = xs[i - 1] + (top - ys[i - 1]) * (xs[i] - xs[i - 1]) / (ys[i] - ys[i - 1])
                xs, ys = np.append(xs[:i], xc), np.append(ys[:i], top)
        else:  # right half: falling
            k = np.flatnonzero(ys > top)
            if len(k):
                i = k[-1]
                xc = xs[i] + (ys[i] - top) * (xs[i + 1] - xs[i]) / (ys[i] - ys[i + 1])
                xs, ys = np.insert(xs[i + 1:], 0, xc), np.insert(ys[i + 1:], 0, top)
        out.add(polyline(ax, xs, ys, color=color, stroke_width=stroke_width))
    return out


class Hook(VoiceoverScene):
    def construct(self):
        self.recap()
        self.spike()
        self.step()
        self.plan()

    # ------------------------------------------------------------------
    def recap(self):
        led = ledger(filled=8, highlight=9).scale(0.9)
        with self.voiceover(
            "Eight rows of the ledger are filled. Part 9 builds the spaces in which every function can be "
            "differentiated, <bookmark mark='l'/> and in which the Fourier transform becomes a perfect symmetry."
        ) as vo:
            self.play(FadeIn(led))
            vo.wait_until("l")
            self.play(Indicate(led.rows[8], color=C.EPS, scale_factor=1.03))
        self.play(FadeOut(led))

    # ------------------------------------------------------------------
    def spike(self):
        d = load("delta")
        ns, vals, phi0 = d["ns"], d["vals"], d["phi0"]
        # x numbered (the readout carries the values); no y numbers on the central axis, where the spike runs
        ax = plain_axes([-1.5, 1.5, 0.5], [-0.6, TOP, 1], 6.4, 4.2, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"include_numbers": False}).move_to([-3.1, -0.6, 0])
        x = np.linspace(-1.5, 1.5, 3001)
        rng = np.random.default_rng(1)
        a, b, c = rng.normal(size=3)
        phi = np.exp(-x * x) * (1 + a * x) * np.cos(b * x + c)
        gphi = polyline(ax, x, phi, color=C.TEST_FN, stroke_width=3.5)
        nT = ValueTracker(1.0)
        assert 5 * rho(0.0) < TOP < 6 * rho(0.0)  # n = 5 fits, n = 6 is the first spike taller than the window

        def tall_ramp():
            # 0 while the spike fits, 1 once it is taller than the window: n steps 5 -> 6 at nT = 5.5, and the
            # shading fades out / the arrow fades in across that step instead of switching in one frame
            return float(np.clip((nT.get_value() - 5.25) / 0.5, 0, 1))

        def spike_():
            n = max(1, round(nT.get_value()))  # a sequence: n steps through the integers
            y = n * rho(n * x)
            # all of the spike fits: shade its area (always 1). Taller than the axes: no shading (clipped, it would
            # lose area). The group keeps one shape throughout (become() scrambles a group that changes shape)
            return VGroup(area_under(ax, x, np.minimum(y, TOP), C.DISTRIBUTION, 0.35 * (1 - tall_ramp())),
                          spike_halves(ax, x, y, C.DISTRIBUTION, 3))

        sp = always_redraw(spike_)
        up = Arrow(ax.c2p(0, 3.6), ax.c2p(0, 4.75), buff=0, color=C.DISTRIBUTION, stroke_width=3,
                   max_tip_length_to_length_ratio=0.3)  # taller than the axes: the arrow says it goes on up
        up.add_updater(lambda m: m.set_opacity(tall_ramp()))

        def readout():
            n = max(1, round(nT.get_value()))
            xx = np.linspace(-1.5, 1.5, 60001)
            ph = np.exp(-xx * xx) * (1 + a * xx) * np.cos(b * xx + c)
            v = float(np.sum((ph * n * rho(n * xx))[1:] + (ph * n * rho(n * xx))[:-1]) / 2 * (xx[1] - xx[0]))
            return VGroup(MathTex(rf"n = {n}: \ \int \varphi(x)\, n\rho(nx)\,dx = {v:.5f}", font_size=28,
                                  color=C.DISTRIBUTION),
                          MathTex(rf"\varphi(0) = {phi0[0]:.5f}", font_size=28, color=C.TEST_FN)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.6, 1.5, 0])

        rd = always_redraw(readout)
        assert abs(vals[0, -1] - phi0[0]) < 2e-4
        rows = VGroup(
            label(r"\emph{``a function that is $0$ except at $0$, \ with integral $1$''}", font_size=24),
            label(r"cannot exist: \ an integral cannot see one point", font_size=24, color=C.PATHOLOGY),
            label(r"but its \emph{action} is perfectly clear:", font_size=24),
            MathTex(r"\langle \delta, \varphi\rangle = \varphi(0)", font_size=36, color=C.EPS),
            MathTex(r"\text{10 random } \varphi: \ |\text{integral} - \varphi(0)| < 2 \times 10^{-4} \ (n = 256)",
                    font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.5, -1.3, 0])
        for r_ in rows:
            if r_.width > 6.4:
                r_.width = 6.4
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.5, -1.3, 0])
        lab = MathTex(r"\varphi", font_size=30, color=C.TEST_FN).next_to(ax.c2p(-1.3, float(np.interp(-1.3, x, phi))), UP,
                                                                         buff=0.1)
        head = label(r"Dirac's delta, \ and why it cannot be a function", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Physicists used Dirac's delta for twenty years before mathematicians could say "
            "what it was: a function that is zero everywhere except at one point, with integral one. "
            "<bookmark mark='b'/> No such function exists: an integral can't see a single point. But look at what "
            "the narrowing bumps do. Each has area one; their heights blow up. <bookmark mark='c'/> Integrated "
            "against a fixed smooth function phi, they return phi of zero, more and more exactly. "
            "<bookmark mark='d'/> So stop asking what delta is, and ask what it does: it takes a test function and "
            "returns its value at zero. That's a perfectly good linear functional."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(rows[0]), Create(ax), FadeIn(sp))  # n = 1: the area-1 bump, shaded
            vo.wait_until("b")
            self.add(up.update())
            self.play(FadeIn(rows[1]))
            self.play(nT.animate.set_value(6.0), run_time=3.0)
            vo.wait_until("c")
            self.play(Create(gphi), FadeIn(lab), FadeIn(rd))
            self.play(nT.animate.set_value(40.0), run_time=4.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[2:4]))
            self.play(FadeIn(rows[4]))
        for m in (sp, rd, up):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def step(self):
        ax = plain_axes([-1.5, 1.5, 0.5], [-0.2, 1.3, 0.5], 6.0, 2.4).move_to([-3.2, 1.0, 0])
        # stacked on the same x-range: the lower panel's numbers serve both (as the spike panel's did)
        bx = plain_axes([-1.5, 1.5, 0.5], [-0.3, TOP, 1], 6.0, 2.6, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 1}},
                        y_axis_config={"include_numbers": False}).move_to([-3.2, -2.0, 0])
        x = np.linspace(-1.5, 1.5, 3001)
        nT = ValueTracker(1.5)

        def smooth():
            n = nT.get_value()
            y = n * rho(n * x)
            Hn = np.concatenate([[0], np.cumsum((y[1:] + y[:-1]) / 2 * np.diff(x))])
            return VGroup(polyline(ax, x, Hn, color=C.SEQ, stroke_width=3.5),
                          spike_halves(bx, x, y, C.DISTRIBUTION, 3.5))  # cut at the window, not flattened

        sm = always_redraw(smooth)
        # clipped at the top of the axes: the arrow says it goes on up (a separate mobject, so sm keeps one shape)
        up2 = Arrow(bx.c2p(0, 3.5), bx.c2p(0, 4.7), buff=0, color=C.DISTRIBUTION, stroke_width=3,
                    max_tip_length_to_length_ratio=0.3)
        up2.add_updater(lambda m: m.set_opacity(float(np.clip((nT.get_value() * rho(0.0) - TOP) / 0.8, 0, 1))))
        H = VGroup(Line(ax.c2p(-1.5, 0), ax.c2p(0, 0), color=WHITE, stroke_width=2),
                   Line(ax.c2p(0, 1), ax.c2p(1.5, 1), color=WHITE, stroke_width=2)).set_stroke(opacity=0.5)
        l1 = MathTex(r"H_n \to H \ \text{(Heaviside's step)}", font_size=26, color=C.SEQ).next_to(ax, UP, buff=0.05)
        l2 = MathTex(r"H_n' = n\rho(nx) \to \delta", font_size=26, color=C.DISTRIBUTION).next_to(bx, UP, buff=0.05).align_to(
            bx, LEFT)
        rows = VGroup(
            label(r"Heaviside (1890s): \ $H' = \delta$, \ used to solve circuits", font_size=24),
            label(r"the step has no derivative at $0$ as a function,", font_size=24),
            label(r"but its smoothings have derivatives that act like $\delta$", font_size=24),
            label(r"\textbf{the move} \ (Sobolev 1936, \ Schwartz 1945):", font_size=26, color=C.EPS),
            label(r"define everything by its action on smooth test functions", font_size=26, color=C.EPS),
            label(r"then \emph{every} function has derivatives of every order", font_size=26, color=C.CONNECTED_SET),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.3, -0.4, 0])
        for r_ in rows:
            if r_.width > 6.0:
                r_.width = 6.0
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.3, -0.4, 0])
        assert rows.get_right()[0] <= 6.6
        head = label(r"The derivative of a step", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Heaviside, solving circuit equations in the 1890s, wrote that the derivative of a "
            "step is delta. <bookmark mark='b'/> Smooth the step slightly: the smoothed steps have honest "
            "derivatives, and they're exactly the narrowing bumps. <bookmark mark='c'/> The move that makes this "
            "rigorous, made by Sobolev and then Laurent Schwartz, is to define everything by its action on smooth "
            "test functions. Then every function, and much more, has derivatives of every order."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(bx), FadeIn(H), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(sm), FadeIn(l1), FadeIn(l2))
            self.add(up2.update())
            self.play(nT.animate.set_value(30.0), run_time=4.0)
            self.play(FadeIn(rows[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3:5]))
            self.play(FadeIn(rows[5]))
        sm.clear_updaters()
        up2.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        chapters = [
            r"Test functions", r"Distributions", r"Calculus with distributions", r"Supports and local structure",
            r"Convolution and mollifiers", r"The Fourier transform", r"Inversion and Plancherel",
            r"Tempered distributions", r"Paley--Wiener", r"Sobolev spaces", r"Fundamental solutions",
            r"Wiener and the primes",
        ]
        items = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=28) for i, t in enumerate(chapters)])
        colL = VGroup(*items[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([-3.0, -0.5, 0])
        colR = VGroup(*items[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([3.0, -0.5, 0]).align_to(colL, UP)
        head = label(r"Part 9: \ distributions and the Fourier transform", font_size=40).to_edge(UP, buff=0.4)
        sub = label(r"Rudin, \textit{Functional Analysis}, chapters 6--9, \ and \textit{Real and Complex Analysis}, chapter 9",
                    font_size=24, color=GREY_B).next_to(head, DOWN, buff=0.15)
        with self.voiceover(
            "Here's the plan, following chapters six to nine of Functional Analysis. <bookmark mark='a'/> First the "
            "test functions and the distributions, their calculus and their structure. <bookmark mark='b'/> Then the "
            "Fourier transform, from L one to the tempered distributions, where it becomes a symmetry. "
            "<bookmark mark='c'/> Then what it buys: Paley-Wiener, Sobolev spaces, fundamental solutions of partial "
            "differential equations, and finally Wiener's theorem and the prime numbers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(5)], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(5, 8)], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(items[i], shift=RIGHT * 0.2) for i in range(8, 12)], lag_ratio=0.3))
        self.wait(0.6)
        self.clear_scene()
