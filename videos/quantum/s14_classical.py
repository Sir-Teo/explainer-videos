from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum import colormap as qcm
from videos.quantum.common import (Raster, WaveView, boxed, corner_wheel, frames_at, image_on, label, load, mtex, note,
                                   num, place_whys, polyline, stack, wave_axes, why, ylabel)


def wigner_rgba(W, vmax=1 / np.pi, alpha=1.0):
    """Wigner function (rows = p ascending) -> RGBA image with p increasing upward; amber > 0, blue < 0."""
    rgb = qcm.real_rgb(W[::-1], vmax, pos=C.WIGNER_POS, neg=C.WIGNER_NEG, gamma=0.8)
    a = np.clip(np.abs(W[::-1]) / vmax * 4, 0, 1) * alpha
    return qcm.rgba(rgb, a)


class ClassicalLimit(VoiceoverScene):
    def construct(self):
        self.ehrenfest()
        self.coherent()
        self.phase_space()
        self.negative()

    # ------------------------------------------------------------------
    def ehrenfest(self):
        l1 = MathTex(r"\frac{d\langle x\rangle}{dt}", r"=", r"\tfrac{i}{\hbar}\big\langle[\hat H, \hat x]\big\rangle", r"=",
                     r"\frac{\langle p\rangle}{m}", font_size=40)
        l2 = MathTex(r"\frac{d\langle p\rangle}{dt}", r"=", r"\tfrac{i}{\hbar}\big\langle[\hat H, \hat p]\big\rangle", r"=",
                     r"-\big\langle V'(x)\big\rangle", font_size=40)
        gen = MathTex(r"\frac{d\langle A\rangle}{dt}", r"=", r"\tfrac{i}{\hbar}\big\langle[\hat H, \hat A]\big\rangle",
                      font_size=36, color=GREY_A).to_edge(UP, buff=0.4)
        col = stack(l1, l2, buff=0.5, align=1).next_to(gen, DOWN, buff=0.5)
        l1[4].set_color(C.MOMENTUM)
        l2[4].set_color(C.POTENTIAL)
        w1 = why(l1, r"$[\hat p^2, \hat x] = -2i\hbar\,\hat p$")
        w2 = why(l2, r"$[V, \hat p] = i\hbar\,V'$")
        place_whys([l1, l2], [w1, w2])
        name = label(r"Ehrenfest's theorem (1927): Newton's laws, for averages", font_size=30, color=C.CLASSICAL)
        name.next_to(col, DOWN, buff=0.4)
        cav = MathTex(r"\big\langle V'(x)\big\rangle", r"\ne", r"V'\big(\langle x\rangle\big)", r"\quad\text{in general}",
                      font_size=36).next_to(name, DOWN, buff=0.4)
        ok = label(r"equal when $V'$ is linear: a free particle, a uniform force, the harmonic oscillator", font_size=28,
                   color=GREY_A).next_to(cav, DOWN, buff=0.3)
        with self.voiceover(
            "How does the classical world emerge from all this? Start with the equation for averages from the "
            "commutator chapter. <bookmark mark='a'/> For position, the commutator of H with x gives the average "
            "momentum over the mass: velocity. <bookmark mark='b'/> For momentum, the commutator with the potential "
            "gives minus the average slope of the potential: the force. <bookmark mark='n'/> This is Ehrenfest's "
            "theorem: averages obey Newton's laws. <bookmark mark='c'/> With one catch: the average of the force isn't "
            "the force at the average position, <bookmark mark='o'/> unless the force is linear in x. For the harmonic "
            "oscillator it is, so the averages follow the classical motion exactly."
        ) as vo:
            self.play(Write(gen))
            vo.wait_until("a")
            self.play(Write(l1), FadeIn(w1))
            vo.wait_until("b")
            self.play(Write(l2), FadeIn(w2))
            vo.wait_until("n")
            self.play(FadeIn(name))
            vo.wait_until("c")
            self.play(Write(cav))
            vo.wait_until("o")
            self.play(FadeIn(ok))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def coherent(self):
        o = load("oscillator")
        xs, tf = o["xs"], o["t_frames"]
        coh, sq = o["coherent_frames"], o["squeezed_frames"]
        mc, ms = o["coherent_mom"], o["squeezed_mom"]
        assert np.allclose(mc[:, 1], 1 / np.sqrt(2), atol=1e-3)
        t = ValueTracker(0.0)
        ax1 = wave_axes((-7, 7), (0, 1.25), x_length=7.6, y_length=2.4).move_to(LEFT * 2.6 + UP * 1.55)
        ax2 = wave_axes((-7, 7), (0, 1.25), x_length=7.6, y_length=2.4).move_to(LEFT * 2.6 + DOWN * 1.85)
        V = lambda x: 0.045 * x**2  # noqa: E731
        xv = np.linspace(-5.2, 5.2, 200)  # V(5.2) = 1.22: the arms stop at the top of each panel
        pots = VGroup(*[polyline(a, xv, V(xv), color=C.POTENTIAL, stroke_width=2).set_stroke(opacity=0.6)
                        for a in (ax1, ax2)])
        w1 = WaveView(ax1, xs, coh[0], mode="density", x_window=(-7, 7)).follow(t, frames_at(tf, coh))
        w2 = WaveView(ax2, xs, sq[0], mode="density", x_window=(-7, 7)).follow(t, frames_at(tf, sq))

        def ball(ax):
            return always_redraw(lambda: Dot(ax.c2p(4 * np.cos(t.get_value()), 1.18), radius=0.09, color=C.CLASSICAL))

        b1, b2 = ball(ax1), ball(ax2)
        l1 = label(r"coherent state", font_size=28).next_to(ax1, UP, buff=0.05).align_to(ax1, LEFT)
        l2 = label(r"squeezed state", font_size=28).next_to(ax2, UP, buff=0.05).align_to(ax2, LEFT)
        defs = VGroup(
            MathTex(r"\hat a\ket{\alpha} = \alpha\ket{\alpha}", font_size=36),
            MathTex(r"\ket{\alpha} = e^{-|\alpha|^2/2}\sum_n \frac{\alpha^n}{\sqrt{n!}}\ket{n}", font_size=32),
            MathTex(r"\alpha(t) = \alpha\,e^{-i\omega t}", font_size=36, color=C.QTIME),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).to_edge(RIGHT, buff=0.4).shift(UP * 1.4)
        def width_readout(lab, mom):
            return always_redraw(lambda: MathTex(r"\sigma_x = " + num(float(np.interp(t.get_value(), tf, mom[:, 1])), 3),
                                                 font_size=30).next_to(lab, RIGHT, buff=0.6))

        sig = [width_readout(l1, mc), width_readout(l2, ms)]
        bl = label(r"sepia dot: a classical particle", font_size=24, color=C.CLASSICAL).to_corner(DR, buff=0.3)
        sim = note(r"split-operator simulation, $\hbar = m = \omega = 1$").to_corner(DL, buff=0.25)
        wheel = corner_wheel(corner=UL, buff=0.15, radius=0.24, labels=False, title=False)
        with self.voiceover(
            "Here's a Gaussian packet in a harmonic potential, displaced from the center and released, simulated by "
            "solving the Schrödinger equation numerically. <bookmark mark='m'/> It swings back and forth exactly in step "
            "with a classical particle, and its shape never changes: the width stays at its minimum, forever. "
            "<bookmark mark='d'/> These are called coherent states: eigenvectors of the lowering operator, whose "
            "label alpha simply rotates in time. They're the most classical states quantum mechanics allows, and "
            "they describe the light from a laser."
        ) as vo:
            self.play(Create(ax1), FadeIn(pots[0]), FadeIn(w1), FadeIn(l1), FadeIn(sim), FadeIn(wheel))
            self.add(b1, sig[0])
            vo.wait_until("m")
            self.play(t.animate.set_value(2 * PI), FadeIn(bl), run_time=5.5, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(defs))
        with self.voiceover(
            "Start with a narrower packet instead, <bookmark mark='s'/> and the center still follows the classical "
            "particle exactly, as Ehrenfest promised, but the width breathes: wide, narrow, wide, twice per swing. "
            "Averages are classical; the shape is not."
        ) as vo:
            self.play(Create(ax2), FadeIn(pots[1]), FadeIn(w2), FadeIn(l2))
            self.add(b2, sig[1])
            vo.wait_until("s")
            self.play(t.animate.set_value(4 * PI), run_time=vo.remaining() + 2.0, rate_func=linear)
        for m in (w1, w2, b1, b2, *sig):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def phase_space(self):
        o = load("oscillator")
        pw, xsw, Wt = o["pw"], o["xs_w"], o["W_orbit"]
        tW = o["t_frames"][::2][: len(Wt)]
        ax = Axes(x_range=[-8, 8, 2], y_range=[-6, 6, 2], x_length=6.8, y_length=5.1, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(LEFT * 2.4 + DOWN * 0.1)
        xl = MathTex("x", font_size=32, color=C.XPOS).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        pl = MathTex("p", font_size=32, color=C.MOMENTUM).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        t = ValueTracker(0.0)

        def W_at(v):
            k = int(np.clip(round(np.interp(v, tW, np.arange(len(tW)))), 0, len(tW) - 1))
            return Wt[k]

        p0, p1 = ax.c2p(-8, -6), ax.c2p(8, 6)
        img = Raster(lambda v: wigner_rgba(W_at(v)), t, p1[0] - p0[0], p1[1] - p0[1], center=(p0 + p1) / 2)
        circ = Circle(radius=(ax.c2p(4, 0) - ax.c2p(0, 0))[0], color=C.CLASSICAL, stroke_width=2).move_to(ax.c2p(0, 0))
        circ.stretch((ax.c2p(0, 4) - ax.c2p(0, 0))[1] / (ax.c2p(4, 0) - ax.c2p(0, 0))[0], 1)
        cdot = always_redraw(lambda: Dot(ax.c2p(4 * np.cos(t.get_value()), -4 * np.sin(t.get_value())), radius=0.07,
                                         color=C.CLASSICAL))
        # the shadows: marginals on the x axis (bottom) and the p axis (left)
        dp, dxw = pw[1] - pw[0], xsw[1] - xsw[0]

        def shadows():
            W = W_at(t.get_value())
            mx = W.sum(axis=0) * dp
            mp = W.sum(axis=1) * dxw
            base_y = ax.c2p(0, -6)[1]
            sx = VMobject(color=C.XPOS, stroke_width=3)
            sx.set_points_as_corners([[ax.c2p(xx, 0)[0], base_y - 0.05 - 1.4 * v, 0] for xx, v in zip(xsw, mx)])
            base_x = ax.c2p(-8, 0)[0]
            sp = VMobject(color=C.MOMENTUM, stroke_width=3)
            sp.set_points_as_corners([[base_x - 0.05 - 1.4 * v, ax.c2p(0, pp)[1], 0] for pp, v in zip(pw, mp)])
            return VGroup(sx, sp)

        sh = always_redraw(shadows)
        wdef = MathTex(r"W(x, p)", r"=", r"\frac{1}{\pi\hbar}\int \psi^*(x + y)\,\psi(x - y)\,e^{2ipy/\hbar}\,dy", font_size=30)
        wdef.to_corner(UR, buff=0.3)
        col_left = np.array([1.75, 0.0, 0.0])  # the text column starts right of the plot
        props = VGroup(
            MathTex(r"\int W\,dp = |\psi(x)|^2", font_size=30, color=C.XPOS),
            MathTex(r"\int W\,dx = |\phi(p)|^2", font_size=30, color=C.MOMENTUM),
            label(r"real, but can be negative", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(wdef, DOWN, buff=0.45).align_to(col_left, LEFT)
        leg = VGroup(VGroup(Square(0.22, fill_color=C.WIGNER_POS, fill_opacity=1, stroke_width=0), label(r"$W > 0$", font_size=24)).arrange(RIGHT, buff=0.12),
                     VGroup(Square(0.22, fill_color=C.WIGNER_NEG, fill_opacity=1, stroke_width=0), label(r"$W < 0$", font_size=24)).arrange(RIGHT, buff=0.12)
                     ).arrange(RIGHT, buff=0.4).next_to(props, DOWN, buff=0.3).align_to(props, LEFT)
        area = label(r"a classical state is a point;\\a quantum state is a blob of area $\sim\hbar$", font_size=26,
                     color=C.CLASSICAL).next_to(leg, DOWN, buff=0.5).align_to(leg, LEFT)
        with self.voiceover(
            "There's a beautiful way to see all of this at once: put position and momentum on the same picture, like a "
            "classical phase space. <bookmark mark='w'/> The Wigner function, defined by this integral over the "
            "wavefunction, lives there. <bookmark mark='s'/> Its shadows are exactly the two probability distributions: "
            "squash it onto the x axis and you get the position density; onto the p axis, the momentum density."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(pl))
            vo.wait_until("w")
            self.add(img)
            self.play(Write(wdef), FadeIn(img))
            vo.wait_until("s")
            self.add(sh)
            self.play(FadeIn(sh), FadeIn(props), FadeIn(leg))
        with self.voiceover(
            "For our coherent state, it's a round blob, <bookmark mark='o'/> and it simply rotates around the origin, "
            "riding on the circle a classical particle traces in phase space. <bookmark mark='a'/> A classical state "
            "is a point; a quantum state is smeared over an area about the size of h-bar, the uncertainty principle "
            "in picture form."
        ) as vo:
            self.play(Create(circ))
            self.add(cdot)
            vo.wait_until("o")
            self.play(t.animate.set_value(2 * PI), run_time=6, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(area))
        for m in (img, cdot, sh):
            m.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def negative(self):
        o = load("oscillator")
        pw, xw, W1, Wcat = o["pw"], o["xw"], o["W1"], o["Wcat"]
        assert abs(W1[len(pw) // 2, len(xw) // 2] + 1 / np.pi) < 2e-3
        # the cat's Wigner function in closed form, for any hbar (ground-state blobs at x = +-3)
        assert np.abs(cat_wigner(*np.meshgrid(xw, pw), 1.0) - Wcat).max() < 2e-3
        axL = Axes(x_range=[-6, 6, 2], y_range=[-5, 5, 2], x_length=5.4, y_length=4.5, tips=False,
                   axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(LEFT * 3.5 + DOWN * 0.3)
        axR = Axes(x_range=[-6, 6, 2], y_range=[-5, 5, 2], x_length=5.4, y_length=4.5, tips=False,
                   axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(RIGHT * 3.5 + DOWN * 0.3)
        selx = (xw >= -6) & (xw <= 6)
        selp = (pw >= -5) & (pw <= 5)
        imL = image_on(axL, wigner_rgba(W1[np.ix_(selp, selx)]), (-6, 6), (-5, 5))
        hb = ValueTracker(1.0)
        X, P = np.meshgrid(np.linspace(-6, 6, 720), np.linspace(-5, 5, 600))
        p0, p1 = axR.c2p(-6, -5), axR.c2p(6, 5)
        imR = Raster(lambda h: wigner_rgba(cat_wigner(X, P, h), vmax=1 / (np.pi * h)), hb, p1[0] - p0[0], p1[1] - p0[1],
                     center=(p0 + p1) / 2)
        labs = VGroup(*[VGroup(MathTex("x", font_size=26, color=C.XPOS).next_to(a.x_axis.get_end(), RIGHT, buff=0.08),
                               MathTex("p", font_size=26, color=C.MOMENTUM).next_to(a.y_axis.get_end(), UP, buff=0.08))
                        for a in (axL, axR)])
        tL = MathTex(r"\ket{1}:\ \text{one rung up}", font_size=32).next_to(labs[0][1], UP, buff=0.15)
        tR = MathTex(r"\ket{\text{cat}} \propto \ket{\psi_0(x - 3)} + \ket{\psi_0(x + 3)}", font_size=30).next_to(labs[1][1], UP, buff=0.15)
        cen = MathTex(r"W(0, 0) = -\frac{1}{\pi\hbar}", font_size=30, color=C.WIGNER_NEG).next_to(axL, DOWN, buff=0.2)
        fr = label(r"fringes between the two blobs:\\interference, in momentum", font_size=26, color=C.WIGNER_NEG).next_to(axR, DOWN, buff=0.2)
        hread = always_redraw(lambda: MathTex(r"\hbar = " + num(hb.get_value(), 2), font_size=32, color=C.HBAR)
                              .next_to(axR, DOWN, buff=0.2))
        hnote = MathTex(r"\text{blob width} \propto \sqrt{\hbar}, \quad \Delta p_{\text{fringe}} = \pi\hbar/3", font_size=26,
                        color=GREY_A).next_to(hread, DOWN, buff=0.15)
        with self.voiceover(
            "But the Wigner function is not a probability distribution. <bookmark mark='o'/> Here's the first excited "
            "state of the oscillator: a ring, and right in the middle it goes negative, down to minus one over pi "
            "h-bar. No classical probability can do that. <bookmark mark='c'/> And here's a superposition of two "
            "displaced packets, a Schrödinger cat state. Between the two blobs are stripes of alternating sign: that's "
            "the interference between the two parts. The sign flips as you move along p, so the interference shows up "
            "in the momentum distribution, while the position distribution shows just two lumps."
        ) as vo:
            self.play(Create(axL), FadeIn(labs[0]), Create(axR), FadeIn(labs[1]))
            vo.wait_until("o")
            self.play(FadeIn(imL), FadeIn(tL))
            self.play(FadeIn(cen))
            vo.wait_until("c")
            self.add(imR)
            self.play(FadeIn(imR), FadeIn(tR))
            self.play(FadeIn(fr))
        with self.voiceover(
            "Negative regions and fringes are the signatures of genuinely quantum states. <bookmark mark='h'/> In the "
            "classical limit, when the distances involved are huge compared with the scale set by h-bar, the blobs "
            "shrink toward points and the fringes become far too fine for any measurement to resolve, and the familiar "
            "classical world appears."
        ) as vo:
            vo.wait_until("h")
            self.play(FadeOut(fr), FadeIn(hread), FadeIn(hnote))
            self.play(hb.animate.set_value(0.1), run_time=max(vo.remaining() - 0.5, 2.0), rate_func=smooth)
        imR.clear_updaters()
        hread.clear_updaters()
        self.wait(0.6)
        self.clear_scene()


def cat_wigner(x, p, hbar):
    """W(x, p) of (psi_0(x - 3) + psi_0(x + 3)), normalized, with m = omega = 1: two blobs plus a fringe term."""
    a = 3.0
    g = lambda u: np.exp(-(u**2 + p**2) / hbar)  # noqa: E731
    norm = 1 / (2 * (1 + np.exp(-a * a / hbar)))
    return norm / (np.pi * hbar) * (g(x - a) + g(x + a) + 2 * g(x) * np.cos(2 * a * p / hbar))
