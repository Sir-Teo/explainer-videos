from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum.common import boxed, label, load, mtex, note, num, place_whys, stack, why


class Uncertainty(VoiceoverScene):
    def construct(self):
        self.statement()
        self.cauchy_schwarz()
        self.derivation()
        self.equality()
        self.plane()
        self.stronger()

    # ------------------------------------------------------------------
    def statement(self):
        hu = MathTex(r"\sigma_x", r"\,", r"\sigma_p", r"\;\ge\;", r"\frac{\hbar}{2}", font_size=72)
        hu[0].set_color(C.XPOS)
        hu[2].set_color(C.MOMENTUM)
        hu[4].set_color(C.HBAR)
        hu.move_to(UP * 1.2)
        hist = label(r"Heisenberg 1927 (the idea); Kennard 1927 (this exact form); Robertson 1929 (any two observables)",
                     font_size=26, color=GREY_A).next_to(hu, DOWN, buff=0.5)
        not1 = label(r"$\sigma$: the standard deviation of the outcomes, over many copies of the same state",
                     font_size=28).next_to(hist, DOWN, buff=0.6)
        not2 = label(r"a statement about the \emph{state}, not about clumsy instruments", font_size=28,
                     color=C.HBAR).next_to(not1, DOWN, buff=0.25)
        with self.voiceover(
            "We've seen hints of it twice now. Squeeze a packet in position and its momentum spreads. Here's the precise "
            "statement: <bookmark mark='h'/> the standard deviation of position times the standard deviation of "
            "momentum is at least h-bar over two. <bookmark mark='n'/> Heisenberg had the idea in 1927; Kennard proved "
            "this exact form the same year; Robertson generalized it two years later. <bookmark mark='s'/> And it's "
            "worth being careful about what it says. The sigmas are spreads of outcomes, over many copies of the same "
            "state. <bookmark mark='t'/> It isn't about measurements disturbing things. It's a property of the state "
            "itself, and we can now prove it in a few lines."
        ) as vo:
            self.play(Write(hu))
            vo.wait_until("n")
            self.play(FadeIn(hist))
            vo.wait_until("s")
            self.play(FadeIn(not1))
            vo.wait_until("t")
            self.play(FadeIn(not2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cauchy_schwarz(self):
        o = LEFT * 3.8 + DOWN * 1.6
        th = ValueTracker(1.0)
        f_len, g_len = 3.6, 2.6

        def pic():
            a = th.get_value()
            f = Arrow(o, o + f_len * RIGHT, buff=0, color=C.XPOS, stroke_width=6, tip_length=0.22)
            gv = g_len * np.array([np.cos(a), np.sin(a), 0])
            g = Arrow(o, o + gv, buff=0, color=C.MOMENTUM, stroke_width=6, tip_length=0.22)
            foot = o + g_len * np.cos(a) * RIGHT
            drop = DashedLine(o + gv, foot, color=GREY_B, stroke_width=2)
            shadow = Line(o, foot, color=C.HBAR, stroke_width=10).set_stroke(opacity=0.6)
            fl = MathTex(r"\ket{f}", font_size=34, color=C.XPOS).next_to(o + f_len * RIGHT, DOWN, buff=0.15)
            gl = MathTex(r"\ket{g}", font_size=34, color=C.MOMENTUM).next_to(o + gv, UP, buff=0.12)
            return VGroup(shadow, f, g, drop, fl, gl)

        pg = always_redraw(pic)
        cs = MathTex(r"|\braket{f}{g}|^2", r"\;\le\;", r"\braket{f}{f}\,\braket{g}{g}", font_size=48).move_to(RIGHT * 3.0 + UP * 1.0)
        cs[0].set_color(C.HBAR)
        csl = label(r"the Cauchy--Schwarz inequality", font_size=28, color=GREY_A).next_to(cs, UP, buff=0.3)
        csn = label(r"a shadow is never longer than the vector:\\equality only when they're parallel", font_size=26,
                    color=GREY_B).next_to(cs, DOWN, buff=0.35)
        tag = note(r"drawn in a real plane, for intuition").to_corner(DL, buff=0.3)
        with self.voiceover(
            "The proof rests on one geometric fact about vectors. <bookmark mark='p'/> The inner product of f with g is "
            "the length of f times the length of g's shadow on it. A shadow is never longer than the vector casting "
            "it, <bookmark mark='c'/> so the inner product squared is at most the product of the two lengths squared. "
            "That's the Cauchy-Schwarz inequality, and it holds in any Hilbert space. <bookmark mark='e'/> It's an "
            "equality only when the two vectors are parallel."
        ) as vo:
            self.add(pg)
            self.play(FadeIn(pg), FadeIn(tag))
            vo.wait_until("p")
            self.play(th.animate.set_value(0.45), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(csl), Write(cs), th.animate.set_value(1.3), run_time=2.5)
            vo.wait_until("e")
            self.play(FadeIn(csn), th.animate.set_value(0.0), run_time=2.0)
        pg.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def derivation(self):
        setup = MathTex(r"\ket{f} = (\hat A - \langle A\rangle)\ket{\psi}", r",\quad", r"\ket{g} = (\hat B - \langle B\rangle)\ket{\psi}",
                        font_size=34).to_edge(UP, buff=0.35)
        setup[0].set_color(C.XPOS)
        setup[2].set_color(C.MOMENTUM)
        sn = MathTex(r"\sigma_A^2 = \braket{f}{f}", r",\quad", r"\sigma_B^2 = \braket{g}{g}", font_size=32).next_to(setup, DOWN, buff=0.2)
        l1 = MathTex(r"\sigma_A^2\,\sigma_B^2", r"\ge", r"|\braket{f}{g}|^2", font_size=36)
        l2 = MathTex(r"\phantom{\sigma_A^2\,\sigma_B^2}", r"\ge", r"\Big(\mathrm{Im}\braket{f}{g}\Big)^2 = \Big(\frac{\braket{f}{g} - \braket{g}{f}}{2i}\Big)^2",
                     font_size=36)
        l3 = MathTex(r"\braket{f}{g} - \braket{g}{f}", r"=", r"\langle \hat A\hat B\rangle - \langle \hat B\hat A\rangle", r"=",
                     r"\langle[\hat A, \hat B]\rangle", font_size=36)
        l4 = MathTex(r"\sigma_A\,\sigma_B", r"\ge", r"\frac{1}{2}\,\big|\langle[\hat A, \hat B]\rangle\big|", font_size=44)
        col = stack(l1, l2, l3, buff=0.38, align=1).next_to(sn, DOWN, buff=0.45)
        l3.shift((l1[1].get_center()[0] - l3[1].get_center()[0]) * RIGHT)
        l4.next_to(col, DOWN, buff=0.5)
        l3[4].set_color(C.HBAR)
        l4[2].set_color(C.HBAR)
        w1 = why(l1, r"Cauchy--Schwarz")
        w2 = why(l2, r"$|z|^2 \ge (\mathrm{Im}\,z)^2$")
        w3 = why(l3, r"multiply out; the $\langle A\rangle\langle B\rangle$ terms cancel")
        place_whys([l1, l2, l3], [w1, w2, w3])
        l4b = boxed(l4, color=C.HBAR, buff=0.2)
        rob = label(r"Robertson, 1929", font_size=24, color=GREY_A).next_to(l4b, RIGHT, buff=0.3)
        with self.voiceover(
            "Take any two observables A and B, and a state psi. <bookmark mark='s'/> Define two vectors: f is A minus "
            "its average, acting on psi, and g is the same for B. <bookmark mark='n'/> Their squared lengths are exactly "
            "the two variances. <bookmark mark='a'/> By Cauchy-Schwarz, the product of the variances is at least the "
            "inner product squared. <bookmark mark='b'/> A complex number's size squared is at least its imaginary part "
            "squared, and the imaginary part is the difference between the inner product and its conjugate, over two i."
        ) as vo:
            self.play(Write(setup))
            vo.wait_until("n")
            self.play(FadeIn(sn))
            vo.wait_until("a")
            self.play(Write(l1), FadeIn(w1))
            vo.wait_until("b")
            self.play(Write(l2[1:]), FadeIn(w2))
        with self.voiceover(
            "<bookmark mark='c'/> Multiply out that difference. The averages cancel, and what's left is the average of "
            "A B minus B A: the commutator. <bookmark mark='d'/> Take a square root: the product of the spreads is at "
            "least half the size of the average commutator. That's Robertson's uncertainty relation, for any pair of "
            "observables at all."
        ) as vo:
            vo.wait_until("c")
            self.play(Write(l3), FadeIn(w3))
            vo.wait_until("d")
            self.play(Write(l4), Create(l4b[0]), FadeIn(rob))
        xp = MathTex(r"[\hat x, \hat p] = i\hbar", r"\;\Rightarrow\;", r"\sigma_x\,\sigma_p \ge \frac{\hbar}{2}", font_size=44)
        xp[0].set_color(C.HBAR)
        xp.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now plug in position and momentum. Their commutator is i h-bar, a constant, so its average is i h-bar in "
            "every state. Half its size is h-bar over two. Notice that no measuring device appears anywhere in this "
            "proof. The uncertainty principle is a consequence of the commutator."
        ):
            self.play(Write(xp))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def equality(self):
        e1 = MathTex(r"\ket{g} = i\lambda\ket{f}", font_size=40)
        e2 = MathTex(r"-i\hbar\,\psi'", r"=", r"\big(\langle p\rangle + i\lambda\,(x - \langle x\rangle)\big)\,\psi", font_size=40)
        e3 = MathTex(r"\psi(x)", r"\propto", r"\exp\!\Big(-\frac{\lambda\,(x - \langle x\rangle)^2}{2\hbar} + \frac{i\langle p\rangle x}{\hbar}\Big)",
                     font_size=40)
        col = stack(e1, e2, e3, buff=0.45, align=None).to_edge(UP, buff=0.8)
        w1 = why(e1, r"Cauchy--Schwarz is tight only for parallel vectors, and the dropped real part must vanish")
        w1.next_to(e1, DOWN, buff=0.12)
        w2 = why(e2, r"write it out with $\hat p = -i\hbar\,d/dx$: a first-order equation")
        w2.next_to(e2, DOWN, buff=0.12)
        col2 = VGroup(e1, w1, e2, w2, e3).arrange(DOWN, buff=0.28).to_edge(UP, buff=0.6)
        res = label(r"the only states with $\sigma_x\sigma_p = \hbar/2$ exactly: \textbf{Gaussians}", font_size=34,
                    color=C.HBAR).next_to(col2, DOWN, buff=0.6)
        q = label(r"When is $\sigma_x\sigma_p = \hbar/2$ exactly?", font_size=40).move_to(UP * 0.3)
        with self.voiceover(
            "When is the bound reached exactly? <bookmark mark='a'/> Both inequalities must be tight: g must be "
            "parallel to f, with a purely imaginary factor. <bookmark mark='b'/> For position and momentum, that's a "
            "first-order differential equation, <bookmark mark='c'/> and its solution is a Gaussian. So Gaussian "
            "packets, the ones we've been using all along, are the least uncertain states there are."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(FadeOut(q), Write(e1), FadeIn(w1))
            vo.wait_until("b")
            self.play(Write(e2), FadeIn(w2))
            vo.wait_until("c")
            self.play(Write(e3))
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plane(self):
        u = load("uncert")
        kind, par, sx, sp, traj = u["kind"], u["par"], u["sx"], u["sp"], u["traj"]
        ax = Axes(x_range=[-1.2, 0.8, 0.5], y_range=[-1.0, 1.4, 0.5], x_length=7.6, y_length=6.2, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(LEFT * 1.9 + DOWN * 0.15)
        L = np.log10
        # forbidden region below the line sigma_x sigma_p = 1/2 (hbar = 1)
        xs = np.linspace(-1.2, 0.8, 50)
        line = ax.plot(lambda v: L(0.5) - v, x_range=[-1.2, 0.8], color=C.HBAR, stroke_width=3.5)
        region = Polygon(*[ax.c2p(v, max(-1.0, L(0.5) - v)) for v in xs], ax.c2p(0.8, -1.0), ax.c2p(-1.2, -1.0),
                         stroke_width=0, fill_color=C.HBAR, fill_opacity=0.18)
        forb = label(r"forbidden", font_size=30, color=C.HBAR).move_to(ax.c2p(-0.75, -0.65))
        ll = MathTex(r"\sigma_x\sigma_p = \tfrac{\hbar}{2}", font_size=30, color=C.HBAR).move_to(ax.c2p(0.45, -1.0 + 0.12)).shift(UP * 0.35)
        ax.x_axis.set_stroke(opacity=0)
        ax.y_axis.set_stroke(opacity=0)
        frame_l = VGroup(Line(ax.c2p(-1.2, -1.0), ax.c2p(0.8, -1.0), color=GREY_B, stroke_width=2),
                         Line(ax.c2p(-1.2, -1.0), ax.c2p(-1.2, 1.4), color=GREY_B, stroke_width=2))
        tks = VGroup()
        for v, s_ in ((-1, "0.1"), (0, "1")):
            tks.add(Line(ax.c2p(v, -1.0), ax.c2p(v, -1.0) + UP * 0.1, color=GREY_B),
                    MathTex(s_, font_size=24, color=GREY_B).next_to(ax.c2p(v, -1.0), DOWN, buff=0.1))
        for v, s_ in ((-1, "0.1"), (0, "1"), (1, "10")):
            tks.add(Line(ax.c2p(-1.2, v), ax.c2p(-1.2, v) + RIGHT * 0.1, color=GREY_B),
                    MathTex(s_, font_size=24, color=GREY_B).next_to(ax.c2p(-1.2, v), LEFT, buff=0.1))
        xl = MathTex(r"\sigma_x", font_size=32, color=C.XPOS).next_to(ax.c2p(0.8, -1.0), RIGHT, buff=0.1)
        yl = MathTex(r"\sigma_p", font_size=32, color=C.MOMENTUM).next_to(ax.c2p(-1.2, 1.4), UP, buff=0.1)
        logn = note(r"both axes logarithmic; $\hbar = m = 1$ (box: $L = 1$; oscillator: $\omega = 1$)").to_corner(DL, buff=0.25)

        def dots(k, color):
            sel = kind == k
            return VGroup(*[Dot(ax.c2p(L(a), L(b)), radius=0.08, color=color) for a, b in zip(sx[sel], sp[sel])])

        dg, db, dh = dots("gauss", WHITE), dots("box", C.ENERGY), dots("ho", GOLD)
        leg = VGroup(
            VGroup(Dot(radius=0.08, color=WHITE), label(r"Gaussians: on the line", font_size=26)).arrange(RIGHT, buff=0.15),
            VGroup(Dot(radius=0.08, color=C.ENERGY), label(r"box states $n = 1 \dots 5$", font_size=26)).arrange(RIGHT, buff=0.15),
            VGroup(Dot(radius=0.08, color=GOLD), label(r"oscillator states $n = 0 \dots 3$", font_size=26)).arrange(RIGHT, buff=0.15),
            VGroup(Line(ORIGIN, RIGHT * 0.3, color=C.XPOS, stroke_width=4), label(r"a free Gaussian, spreading", font_size=26)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_corner(UR, buff=0.4)
        b1 = float(sx[kind == "box"][0] * sp[kind == "box"][0])
        assert abs(b1 - 0.568) < 0.001
        bl = MathTex(r"0.568\,\hbar", font_size=26, color=C.ENERGY).next_to(db[0], LEFT, buff=0.12)
        tr = VMobject(color=C.XPOS, stroke_width=4)
        tr.set_points_as_corners(ax.c2p(L(traj[:, 1]), L(traj[:, 2])).T)
        with self.voiceover(
            "Let's map it out. Here's the plane of position spread against momentum spread, on logarithmic axes, so "
            "the bound becomes a straight line, <bookmark mark='f'/> and everything below it is forbidden. "
            "<bookmark mark='g'/> Gaussians of every width sit exactly on the line. <bookmark mark='b'/> The box's "
            "stationary states sit above it: the lowest at 0.568 h-bar, the others higher and higher. "
            "<bookmark mark='o'/> The harmonic oscillator's states, which we'll meet next, sit at n plus one half "
            "times h-bar."
        ) as vo:
            self.play(Create(frame_l), FadeIn(tks), FadeIn(xl), FadeIn(yl), FadeIn(logn), Create(line))
            vo.wait_until("f")
            self.play(FadeIn(region), FadeIn(forb), FadeIn(ll))
            vo.wait_until("g")
            self.play(FadeIn(dg), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(FadeIn(db), FadeIn(leg[1]), FadeIn(bl))
            vo.wait_until("o")
            self.play(FadeIn(dh), FadeIn(leg[2]))
        with self.voiceover(
            "And a free Gaussian packet, as it spreads, slides away from the line: its position spread grows while its "
            "momentum spread stays fixed. <bookmark mark='q'/> So does it become more uncertain? In one sense, yes. But "
            "something subtler is going on."
        ) as vo:
            self.play(Create(tr), FadeIn(leg[3]), run_time=2.5)
            vo.wait_until("q")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stronger(self):
        u = load("uncert")
        traj = u["traj"]
        sr = MathTex(r"\sigma_x^2\,\sigma_p^2", r"\;\ge\;", r"\Big(\tfrac{1}{2}\langle \hat x\hat p + \hat p\hat x\rangle - \langle x\rangle\langle p\rangle\Big)^2",
                     r"+", r"\Big(\frac{\hbar}{2}\Big)^2", font_size=36).to_edge(UP, buff=0.5)
        sr[2].set_color(C.CURRENT)
        sr[4].set_color(C.HBAR)
        srl = label(r"Schr\"odinger, 1930: keep the real part we dropped", font_size=26, color=GREY_A).next_to(sr, DOWN, buff=0.2)
        cl = MathTex(r"\text{covariance of } x \text{ and } p", font_size=28, color=C.CURRENT).next_to(srl, DOWN, buff=0.15)
        rows = [[num(t, 1), num(sx, 3), num(sp, 3), num(cv + 0.0, 3).replace("{-}0.000", "0.000"), num((sx * sp) ** 2 - cv**2, 4)]
                for t, sx, sp, cv in traj[::15]]
        assert all(abs(float(r[4]) - 0.25) < 1e-4 for r in rows)
        from videos.quantum.common import num_table
        tab = num_table([r"t", r"\sigma_x", r"\sigma_p", r"\text{cov}", r"\sigma_x^2\sigma_p^2 - \text{cov}^2"], rows, font_size=32,
                        col_colors=[C.QTIME, C.XPOS, C.MOMENTUM, C.CURRENT, C.HBAR]).next_to(cl, DOWN, buff=0.55)
        expl = label(r"position and momentum become correlated (the fast part runs ahead):\\the spreading packet still "
                     r"has the least uncertainty quantum mechanics allows", font_size=26).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In the derivation we threw away the real part of the inner product. Schrödinger kept it in 1930, and got a "
            "stronger bound: <bookmark mark='c'/> the extra term is the covariance between position and momentum. "
            "<bookmark mark='t'/> For our spreading packet, the covariance grows, because the faster components are out "
            "in front, <bookmark mark='e'/> and the product of the variances minus the covariance squared stays at "
            "exactly one quarter, h-bar squared over four, at every moment. The spreading packet never gets any less "
            "sharp than quantum mechanics allows; its uncertainty just becomes correlated."
        ) as vo:
            self.play(Write(sr), FadeIn(srl))
            vo.wait_until("c")
            self.play(FadeIn(cl))
            vo.wait_until("t")
            self.play(FadeIn(tab.header), Create(tab.rule), LaggedStart(*[FadeIn(r) for r in tab.rows], lag_ratio=0.3),
                      run_time=2)
            vo.wait_until("e")
            self.play(Indicate(tab.cols[4], color=C.HBAR), FadeIn(expl))
        self.wait(0.5)
        self.clear_scene()
