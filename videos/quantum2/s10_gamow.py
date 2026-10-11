from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum2.common import (label, lframe, load, mtex, note, plain_axes, polyline, sci, tick_labels, why)


class Gamow(VoiceoverScene):
    def construct(self):
        self.puzzle()
        self.barrier()
        self.exponent()
        self.data()

    # ------------------------------------------------------------------
    def puzzle(self):
        g = load("gamow")
        (qu, tu), (qp, tp) = g["u238"], g["po212"]
        yr = 365.25 * 86400
        assert abs(tu / yr / 1e9 - 4.46) < 0.02 and abs(tp - 2.95e-7) < 1e-9
        cards = VGroup()
        for name, q, t in ((r"uranium-238", qu, r"4.5\ \text{billion years}"), (r"polonium-212", qp, r"0.3\ \mu\text{s}")):
            c = VGroup(label(name, font_size=34, color=C.NUCLEUS),
                       MathTex(r"E_\alpha \approx Q = " + f"{q:.2f}" + r"\ \text{MeV}", font_size=32),
                       MathTex(r"t_{1/2} = " + t, font_size=32, color=C.QTIME)).arrange(DOWN, buff=0.25)
            box = SurroundingRectangle(c, color=GREY_D, buff=0.3, corner_radius=0.15)
            cards.add(VGroup(box, c))
        cards.arrange(RIGHT, buff=1.2).move_to(UP * 0.6)
        ratio = MathTex(r"\times 2 \text{ in energy}", r"\quad\Longleftrightarrow\quad", r"\times 10^{24} \text{ in lifetime}", font_size=38).next_to(cards, DOWN, buff=0.6)
        ratio[2].set_color(C.QTIME)
        assert 23.5 < np.log10(tu / tp) < 24.0
        gn = note(r"Geiger \& Nuttall (1911): the empirical pattern; data: NNDC NuDat 3, AME2020").to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "WKB's formula for tunneling solved one of the great puzzles of the 1920s. <bookmark mark='a'/> "
            "Uranium-238 emits alpha particles with about 4.27 million electron volts of energy, and has a half-life of "
            "four and a half billion years. <bookmark mark='b'/> Polonium-212 emits them with 8.95, and lasts a third of "
            "a microsecond. <bookmark mark='c'/> Twice the energy, ten to the twenty-four times faster. Geiger and "
            "Nuttall had found the pattern in 1911; nobody could explain it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0]))
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(Write(ratio), FadeIn(gn))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def barrier(self):
        g = load("gamow")
        R, b, G2 = g["u238_R_b_2G"]
        Q = float(g["u238"][0])
        k = 2 * 90 * 1.43996
        ax = plain_axes((0, 75), (-12, 32), 10.0, 5.0).move_to(DOWN * 0.4 + LEFT * 0.6)
        rl = MathTex(r"r\ (\text{fm})", font_size=28, color=C.XPOS).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        vl = MathTex(r"V\ (\text{MeV})", font_size=28, color=C.POTENTIAL).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        rr = np.linspace(R, 75, 400)
        coul = polyline(ax, rr, k / rr, color=C.POTENTIAL, stroke_width=4)
        well = VMobject(stroke_color=C.POTENTIAL, stroke_width=4).set_points_as_corners([ax.c2p(0, -10), ax.c2p(R, -10), ax.c2p(R, k / R)])
        el = DashedLine(ax.c2p(0, Q), ax.c2p(75, Q), color=C.ENERGY, stroke_width=3)
        ql = MathTex(r"Q = 4.27\ \text{MeV}", font_size=26, color=C.ENERGY).next_to(ax.c2p(60, Q), UP, buff=0.1)
        forb = Polygon(*[ax.c2p(r_, k / r_) for r_ in np.linspace(R, b, 120)], ax.c2p(b, Q), ax.c2p(R, Q), stroke_width=0,
                       fill_color=C.HBAR, fill_opacity=0.3)
        fl = label(r"forbidden", font_size=24, color=C.HBAR).move_to(ax.c2p(22, 9))
        Rl = MathTex(r"R \approx " + f"{R:.1f}" + r"\ \text{fm}", font_size=24, color=C.NUCLEUS).next_to(ax.c2p(R, -10), DOWN, buff=0.12)
        bl = MathTex(r"b \approx " + f"{b:.0f}" + r"\ \text{fm}", font_size=24, color=C.ENERGY).next_to(ax.c2p(b, Q), DOWN, buff=0.15)
        hl = MathTex(r"V(R) \approx " + f"{k / R:.0f}" + r"\ \text{MeV}", font_size=24, color=C.POTENTIAL).next_to(ax.c2p(R, k / R), RIGHT, buff=0.15)
        alpha = Dot(ax.c2p(R / 2, Q), radius=0.1, color=C.NUCLEUS)
        cl = MathTex(r"V(r) = \frac{2Z_d e^2}{4\pi\varepsilon_0 r}", font_size=32, color=C.POTENTIAL).to_corner(UR, buff=0.5)
        sch = note(r"uranium-238 $\to$ thorium-234; the inside of the nucleus drawn as a flat well (schematic)").to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "In 1928, George Gamow, and independently Ronald Gurney and Edward Condon, pictured the alpha particle "
            "rattling around inside the nucleus, <bookmark mark='a'/> held in by the electric repulsion of the rest of "
            "the nucleus once it's outside. <bookmark mark='b'/> The repulsion makes a barrier about twenty-eight million "
            "electron volts high at the nuclear surface, far above the alpha's energy. <bookmark mark='c'/> Classically "
            "it could only escape beyond sixty femtometers, and it could never get there."
        ) as vo:
            self.play(Create(ax), FadeIn(rl), FadeIn(vl), Create(well), FadeIn(alpha), FadeIn(sch))
            vo.wait_until("a")
            self.play(Create(coul), Write(cl))
            vo.wait_until("b")
            self.play(Create(el), FadeIn(ql), FadeIn(hl), FadeIn(Rl))
            self.play(alpha.animate.shift(RIGHT * 0.35), rate_func=there_and_back, run_time=0.6)
            self.play(alpha.animate.shift(LEFT * 0.35), rate_func=there_and_back, run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(forb), FadeIn(fl), FadeIn(bl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def exponent(self):
        g = load("gamow")
        R, b, G2 = g["u238_R_b_2G"]
        Rp, bp, G2p = g["po212_R_b_2G"]
        nu = float(g["u238_nu"])
        P = np.exp(-G2)
        assert 87.5 < G2 < 88.5 and 31.8 < G2p < 32.8 and 5e-39 < P < 7e-39 and 5e20 < nu < 1e21
        e1 = MathTex(r"T", r"\approx", r"e^{-2G}", r",\qquad", r"2G = \frac{2}{\hbar}\int_R^b \sqrt{2\mu\,(V(r) - Q)}\;dr", font_size=36).to_edge(UP, buff=0.4)
        e1[2].set_color(C.HBAR)
        e2 = MathTex(r"2G", r"=", r"\frac{2\sqrt{2\mu Q}}{\hbar}\, b\,\Big[\arccos\sqrt{\tfrac Rb} - \sqrt{\tfrac Rb\big(1 - \tfrac Rb\big)}\Big]", font_size=34).next_to(e1, DOWN, buff=0.35)
        e2w = note(r"Coulomb barrier: the integral in closed form").next_to(e2, DOWN, buff=0.1)
        rows = VGroup(
            MathTex(r"\text{uranium-238:}", r"\quad 2G = " + f"{G2:.0f}", r",\quad e^{-2G} \approx " + sci(P, 1), font_size=32),
            MathTex(r"\text{knocks on the wall } \nu \approx v/2R \approx " + sci(nu, 1) + r"\ \text{s}^{-1}", font_size=32),
            MathTex(r"t_{1/2} = \frac{\ln 2}{\nu\, e^{-2G}} \approx " + f"{float(g['model'][list(g['names']).index('U-238')]) / (365.25 * 86400) / 1e9:.1f}" + r"\ \text{billion years}",
                    font_size=32),
            MathTex(r"\text{polonium-212:}", r"\quad 2G = " + f"{G2p:.0f}", r"\quad\Rightarrow\quad e^{-2G}\ \text{larger by}\ 10^{" + f"{(G2 - G2p) / np.log(10):.0f}" + r"}",
                    font_size=32),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(e2w, DOWN, buff=0.5)
        rows[0][1].set_color(C.HBAR)
        rows[3][1].set_color(C.HBAR)
        with self.voiceover(
            "Quantum mechanically, it tunnels, and WKB gives the probability: <bookmark mark='a'/> e to the minus two "
            "times the integral of kappa across the forbidden region, where kappa is the square root of 2 mu times V "
            "minus Q, over h-bar. <bookmark mark='b'/> For a Coulomb barrier the integral can be done in closed form. "
            "<bookmark mark='c'/> For uranium the exponent is 88: each time the alpha hits the wall, it gets through "
            "with a probability of about one in ten to the thirty-eight. <bookmark mark='d'/> It hits the wall nearly "
            "ten to the twenty-one times a second, <bookmark mark='e'/> so it takes billions of years. "
            "<bookmark mark='f'/> For polonium-212, with twice the energy, the barrier is thinner, the exponent drops to "
            "32, and the decay takes a fraction of a microsecond."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(e1))
            vo.wait_until("b")
            self.play(Write(e2), FadeIn(e2w))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
            vo.wait_until("f")
            self.play(FadeIn(rows[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def data(self):
        g = load("gamow")
        Z, Q, T, model, names = g["Z"], g["Q"], g["T"], g["model"], list(g["names"])
        gx = (Z - 2) / np.sqrt(Q)
        ax = Axes(x_range=[26, 45, 2], y_range=[-8, 20, 4], x_length=8.6, y_length=4.7, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(LEFT * 1.3 + UP * 0.45)
        tks = tick_labels(ax, xs=(28, 32, 36, 40, 44), ys=(-8, -4, 0, 4, 8, 12, 16, 20), fmt=lambda v: f"{v:g}" if v > 25 else f"10^{{{int(v)}}}")
        fr = lframe(ax)
        xl = MathTex(r"Z_d/\sqrt{Q/\text{MeV}}", font_size=26).next_to(fr[0].get_end(), RIGHT, buff=0.15)
        yl = MathTex(r"t_{1/2}\ (\text{s})", font_size=28, color=C.QTIME).next_to(fr[1].get_end(), UP, buff=0.1)
        pts = VGroup(*[Dot(ax.c2p(x, np.log10(t)), radius=0.07, color=WHITE) for x, t in zip(gx, T)])
        mods = VGroup(*[Cross(scale_factor=0.09, stroke_color=C.APPROX, stroke_width=3).move_to(ax.c2p(x, np.log10(m))) for x, m in zip(gx, model)])
        leg = VGroup(VGroup(Dot(radius=0.07, color=WHITE), label(r"measured (29 nuclides)", font_size=24)).arrange(RIGHT, buff=0.15),
                     VGroup(Cross(scale_factor=0.09, stroke_color=C.APPROX, stroke_width=3), label(r"Gamow's tunneling formula", font_size=24, color=C.APPROX)).arrange(RIGHT, buff=0.15),
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.45)
        span = BraceBetweenPoints(ax.c2p(45.2, np.log10(T.min())), ax.c2p(45.2, np.log10(T.max())), direction=RIGHT, color=C.QTIME)
        sl = MathTex(r"10^{24}", font_size=32, color=C.QTIME).next_to(span, RIGHT, buff=0.1)
        ann = {}
        for nm in ("U-238", "Po-212", "Po-210"):
            i = names.index(nm)
            ann[nm] = label(nm.replace("-", "-"), font_size=20, color=GREY_A).next_to(pts[i], LEFT if nm != "Po-212" else RIGHT, buff=0.1)
        med = float(np.median(np.abs(g["resid"])))
        assert med < 0.3 and g["resid_std"] < 0.4
        po = names.index("Po-210")
        assert abs(g["resid"][po]) == np.abs(g["resid"]).max()
        msg = VGroup(
            label(r"one radius ($R = 1.2\,(A_d^{1/3} + 4^{1/3})$ fm), no fitting:", font_size=24, color=GREY_A),
            label(r"typical miss: a factor of " + f"{10 ** med:.1f}" + r", across 24 decades", font_size=24, color=C.APPROX),
            label(r"worst: Po-210 and Po-208, at the closed neutron shell $N = 126$", font_size=24, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.2)
        src = note(r"half-lives: NNDC NuDat 3 (partial alpha); $Q$: AME2020").to_corner(UL, buff=0.2)
        with self.voiceover(
            "Here are 29 alpha emitters, <bookmark mark='a'/> their half-lives from the nuclear data tables spanning "
            "twenty-four orders of magnitude, plotted against the nuclear charge over the square root of the energy. "
            "<bookmark mark='b'/> The crosses are Gamow's formula, with one assumed nuclear radius and no fitting to these "
            "data. <bookmark mark='c'/> It follows the measurements across all twenty-four decades, typically within a "
            "factor of two. <bookmark mark='d'/> The worst misses, polonium-210 and 208, sit at a closed shell of 126 "
            "neutrons, where forming an alpha particle inside the nucleus is harder: physics this simple picture leaves "
            "out. One integral, from the semiclassical limit of the Schrödinger equation, explains the rest."
        ) as vo:
            self.play(Create(fr), FadeIn(tks), FadeIn(xl), FadeIn(yl), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in pts], lag_ratio=0.04), FadeIn(leg[0]), GrowFromCenter(span), FadeIn(sl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in mods], lag_ratio=0.04), FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(FadeIn(msg[0]), FadeIn(msg[1]), FadeIn(ann["U-238"]), FadeIn(ann["Po-212"]))
            vo.wait_until("d")
            self.play(FadeIn(msg[2]), FadeIn(ann["Po-210"]), Indicate(pts[po], color=C.APPROX))
        self.wait(0.4)
        self.clear_scene()
