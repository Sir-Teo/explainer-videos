from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.relativity.common import boxed, label, mtex, note, part_card, stack

FLUX = GOLD_A  # energy flux / momentum density
STRESS = C.METRIC  # pressure and shear


class StressEnergy(VoiceoverScene):
    def construct(self):
        self.card()
        self.boost()
        self.matrix()
        self.fluid()
        self.conservation()

    def card(self):
        c = part_card(3, r"Einstein's equation", r"what curves spacetime, and how")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def boost(self):
        v = 0.6
        gamma = 1 / math.sqrt(1 - v * v)
        assert abs(gamma - 1.25) < 1e-12 and abs(gamma**2 - 1.5625) < 1e-12
        rng = np.random.default_rng(5)
        pts = rng.uniform(-1, 1, (36, 2)) * 1.25
        L = np.array([-3.6, 0.0, 0])
        R = np.array([3.0, 0.0, 0])
        b1 = Square(2.8, color=GREY_A, stroke_width=3).move_to(L)
        d1 = VGroup(*[Dot(L + np.array([x, y, 0]), radius=0.06, color=C.MATTER) for x, y in pts])
        b2 = Rectangle(width=2.8 / gamma, height=2.8, color=GREY_A, stroke_width=3).move_to(R)
        d2 = VGroup(*[Dot(R + np.array([x / gamma, y, 0]), radius=0.085, color=C.MATTER)
                      for x, y in pts])
        arr = Arrow(R + LEFT * 1.6 + UP * 1.9, R + RIGHT * 1.6 + UP * 1.9, buff=0, color=WHITE, stroke_width=4)
        arrl = MathTex(r"v = 0.6\,c", font_size=32).next_to(arr, UP, buff=0.1)
        t1 = label(r"dust at rest", font_size=30).next_to(b1, UP, buff=0.45)
        t2 = VGroup(arr, arrl)
        e1 = mtex(r"\text{energy density} = \rho c^2", font_size=32, color=C.MATTER).next_to(b1, DOWN, buff=0.4)
        facts = VGroup(
            mtex(r"\text{volume:}\ \times \tfrac{1}{\gamma}", r"\ \Rightarrow\ ", r"\text{number density} \times \gamma",
                 font_size=30),
            mtex(r"\text{each particle's energy:}\ \times \gamma", font_size=30),
            mtex(r"\text{energy density:}\ \times\gamma^2 = 1.5625", font_size=34, color=C.MATTER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(b2, DOWN, buff=0.4).set_x(1.6)
        with self.voiceover(
            "Now the other side of the equation: matter. In Newton's theory, the source of gravity is the mass density, "
            "rho. But relativity says mass is a form of energy, E equals m c squared, so the source should be energy "
            "density. <bookmark mark='d'/> Here's a box of dust at rest. Its energy density is rho c squared. "
            "<bookmark mark='b'/> Now look at the same dust from a frame where it's moving at six tenths the speed of "
            "light. <bookmark mark='c'/> Two things change. The box is length-contracted, so the particles are packed more "
            "densely: one factor of gamma. <bookmark mark='e'/> And each particle is moving, so it carries more energy: a "
            "second factor of gamma. <bookmark mark='f'/> The energy density goes up by gamma squared."
        ) as vo:
            vo.wait_until("d")
            self.play(Create(b1), FadeIn(d1), FadeIn(t1), FadeIn(e1))
            vo.wait_until("b")
            self.play(TransformFromCopy(b1, b2), TransformFromCopy(d1, d2), GrowArrow(arr), FadeIn(arrl), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(facts[0]))
            vo.wait_until("e")
            self.play(FadeIn(facts[1]), d2.animate.set_color(YELLOW))
            vo.wait_until("f")
            self.play(FadeIn(facts[2]))
        tens = label(r"Two factors of $\gamma$: the $00$ component of a tensor with \emph{two} indices.", font_size=30,
                     color=C.MATTER).to_edge(UP, buff=0.4)
        with self.voiceover(
            "A scalar wouldn't change at all. A vector's time component would pick up one factor of gamma. Two factors "
            "of gamma is the signature of a tensor with two indices. <bookmark mark='t'/> So the source of gravity can't "
            "be a single number. It has to be the time-time component of a two-index tensor."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(tens))
        self.clear_scene()

    # ------------------------------------------------------------------
    def matrix(self):
        cell = 1.05
        origin = np.array([-4.4, 1.55, 0])
        cells = VGroup()
        names = [[r"T^{00}", r"T^{01}", r"T^{02}", r"T^{03}"], [r"T^{10}", r"T^{11}", r"T^{12}", r"T^{13}"],
                 [r"T^{20}", r"T^{21}", r"T^{22}", r"T^{23}"], [r"T^{30}", r"T^{31}", r"T^{32}", r"T^{33}"]]
        rects = {}
        for i in range(4):
            for j in range(4):
                col = C.MATTER if i == j == 0 else (FLUX if (i == 0 or j == 0) else STRESS)
                op = 0.35 if (i == j == 0 or (i == j and i > 0)) else 0.18
                r = Square(cell, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=op)
                r.move_to(origin + np.array([j * cell, -i * cell, 0]))
                t = MathTex(names[i][j], font_size=30).move_to(r)
                rects[i, j] = VGroup(r, t)
                cells.add(rects[i, j])
        defn = mtex(r"T^{\mu\nu}", r"=", r"\text{flux of } p^\mu \text{ through a surface of constant } x^\nu",
                    font_size=32)
        defn[0].set_color(C.MATTER)
        defn.to_edge(UP, buff=0.35)
        lab = VGroup(
            label(r"energy density", font_size=28, color=C.MATTER),
            label(r"energy flux $=$ momentum density $\times\,c$", font_size=28, color=FLUX),
            label(r"pressure (diagonal)", font_size=28, color=STRESS),
            label(r"shear stress (off-diagonal)", font_size=28, color=STRESS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.1, 0.0, 0])
        sym = mtex(r"T^{\mu\nu} = T^{\nu\mu}\quad(10 \text{ independent components})", font_size=30, color=GREY_A)
        sym.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "That tensor is the stress–energy tensor, T mu nu. <bookmark mark='d'/> Its meaning: T mu nu is the flux of "
            "the mu component of four-momentum through a surface of constant x nu. Let's read it block by block. "
            "<bookmark mark='a'/> T zero zero, momentum's time component, energy, crossing a surface of constant time: "
            "that's simply the energy density. <bookmark mark='b'/> The rest of the top row and the first column: the "
            "flow of energy, which is the same thing as the density of momentum. <bookmark mark='c'/> And the space-space "
            "block is the flow of momentum: stress. On the diagonal, momentum in x flowing across a surface facing x: "
            "that's pressure. <bookmark mark='e'/> Off the diagonal: shear. <bookmark mark='s'/> The tensor is "
            "symmetric, so it has ten independent components: the same number as the metric."
        ) as vo:
            self.play(FadeIn(cells, lag_ratio=0.02))
            vo.wait_until("d")
            self.play(Write(defn))
            vo.wait_until("a")
            self.play(Indicate(rects[0, 0], color=C.MATTER), FadeIn(lab[0]))
            vo.wait_until("b")
            self.play(*[Indicate(rects[0, j], color=FLUX) for j in range(1, 4)],
                      *[Indicate(rects[i, 0], color=FLUX) for i in range(1, 4)], FadeIn(lab[1]))
            vo.wait_until("c")
            self.play(*[Indicate(rects[i, i], color=STRESS) for i in range(1, 4)], FadeIn(lab[2]))
            vo.wait_until("e")
            self.play(*[Indicate(rects[i, j], color=STRESS) for i in range(1, 4) for j in range(1, 4) if i != j],
                      FadeIn(lab[3]))
            vo.wait_until("s")
            self.play(FadeIn(sym))
        self.clear_scene()

    # ------------------------------------------------------------------
    def fluid(self):
        pf = mtex(r"T^{\mu\nu}", r"=", r"\Big(\rho + \frac{p}{c^2}\Big)u^\mu u^\nu", r"+", r"p\,g^{\mu\nu}", font_size=48)
        pf[0].set_color(C.MATTER)
        pf[4][1:].set_color(C.METRIC)
        pf.move_to(UP * 1.8)
        pfl = label(r"a perfect fluid: density $\rho$, pressure $p$, four-velocity $u^\mu$", font_size=28,
                    color=GREY_A).next_to(pf, DOWN, buff=0.25)
        rest = mtex(r"\text{in its rest frame:}\quad T^{\mu\nu} = \begin{pmatrix} \rho c^2 & 0 & 0 & 0 \\ 0 & p & 0 & 0 \\ "
                    r"0 & 0 & p & 0 \\ 0 & 0 & 0 & p \end{pmatrix}", font_size=38)
        rest.next_to(pfl, DOWN, buff=0.6)
        dust = mtex(r"\text{dust } (p = 0):\quad T^{\mu\nu} = \rho\, u^\mu u^\nu", font_size=38, color=C.MATTER)
        dust.next_to(rest, DOWN, buff=0.5)
        with self.voiceover(
            "For most of what follows, matter will be a perfect fluid: something with a density rho and a pressure p, and "
            "no viscosity. <bookmark mark='p'/> Its stress–energy tensor has this form, where u is the fluid's "
            "four-velocity. <bookmark mark='r'/> In the fluid's own rest frame it's diagonal: energy density in the "
            "corner, and the pressure in all three space directions. <bookmark mark='d'/> And with no pressure at all, "
            "it's dust: just rho times u times u, the boosted box we just saw."
        ) as vo:
            vo.wait_until("p")
            self.play(Write(pf), FadeIn(pfl))
            vo.wait_until("r")
            self.play(FadeIn(rest))
            vo.wait_until("d")
            self.play(FadeIn(dust))
        self.clear_scene()

    # ------------------------------------------------------------------
    def conservation(self):
        c1 = mtex(r"\partial_\mu T^{\mu\nu}", r"=", r"0", font_size=50)
        c1[0].set_color(C.MATTER)
        c1.move_to(UP * 2.4)
        cl = label(r"in flat spacetime: what flows out of a region is lost from inside", font_size=28,
                   color=GREY_A).next_to(c1, DOWN, buff=0.2)
        n0 = VGroup(mtex(r"\nu = 0:", font_size=34, color=GREY_A),
                    mtex(r"\frac{\partial\rho}{\partial t} + \nabla\cdot(\rho\mathbf v) = 0", font_size=36),
                    label(r"energy (mass) conservation", font_size=26, color=GREY_A)).arrange(RIGHT, buff=0.4)
        ni = VGroup(mtex(r"\nu = i:", font_size=34, color=GREY_A),
                    mtex(r"\frac{\partial(\rho v_i)}{\partial t} + \partial_j\big(\rho v_i v_j + p\,\delta_{ij}\big) = 0",
                         font_size=36),
                    label(r"momentum: Euler's equation", font_size=26, color=GREY_A)).arrange(RIGHT, buff=0.4)
        rows = VGroup(n0, ni).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(cl, DOWN, buff=0.55)
        sl = note(r"(slow fluid, $p \ll \rho c^2$)", font_size=22).next_to(rows, DOWN, buff=0.15).align_to(rows, RIGHT)
        c2 = mtex(r"\nabla_\mu T^{\mu\nu}", r"=", r"0", font_size=56)
        c2[0].set_color(C.MATTER)
        cb = boxed(c2, color=C.MATTER, buff=0.25).next_to(sl, DOWN, buff=0.45)
        c2l = label(r"curved spacetime: $\partial \to \nabla$", font_size=26, color=GREY_A).next_to(cb, RIGHT, buff=0.4)
        with self.voiceover(
            "One more property, and it's the crucial one. <bookmark mark='c'/> Energy and momentum are conserved, and for "
            "a tensor of fluxes that has a compact form: the divergence of T is zero. Whatever flows out of a small region "
            "is lost from inside it. <bookmark mark='z'/> The time component of this equation is the continuity equation, "
            "conservation of mass and energy. <bookmark mark='i'/> The space components are conservation of momentum: "
            "Euler's equation of fluid motion. So all of fluid dynamics is inside this one line."
        ) as vo:
            vo.wait_until("c")
            self.play(Write(c1), FadeIn(cl))
            vo.wait_until("z")
            self.play(FadeIn(n0))
            vo.wait_until("i")
            self.play(FadeIn(ni), FadeIn(sl))
        with self.voiceover(
            "<bookmark mark='g'/> In curved spacetime, partial derivatives become covariant derivatives: the divergence of "
            "T, taken with nabla, vanishes. Now here's why this matters so much. Whatever we put on the geometry side of "
            "Einstein's equation, it will equal a constant times T. So it must have zero divergence too, and not just "
            "for special solutions: automatically, as an identity, whatever the matter happens to be doing."
        ) as vo:
            vo.wait_until("g")
            self.play(Write(c2), Create(cb[0]), FadeIn(c2l))
        self.clear_scene()
