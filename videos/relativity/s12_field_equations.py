from __future__ import annotations

import math

import numpy as np
import sympy as sp

from explainer import *  # noqa: F403
from videos.relativity.common import boxed, label, ladder, load, mtex, note, sci, stack
from videos.relativity.geometry import first_order, same, weak_static


class FieldEquations(VoiceoverScene):
    def construct(self):
        self.requirements()
        self.guess()
        self.bianchi()
        self.failure()
        self.einstein()
        self.kappa()
        self.final()

    # ------------------------------------------------------------------
    def requirements(self):
        head = mtex(r"\big[\ \text{geometry}\ \big]_{\mu\nu}", r"=", r"\kappa\,T_{\mu\nu}", font_size=50)
        head[0].set_color(C.CURVATURE)
        head[2].set_color(C.MATTER)
        head.to_edge(UP, buff=0.5)
        reqs = VGroup(
            label(r"1.\ \ a symmetric tensor with two indices, like $T_{\mu\nu}$", font_size=32),
            label(r"2.\ \ built from $g_{\mu\nu}$ and its first and second derivatives, like $\nabla^2\Phi$", font_size=32),
            label(r"3.\ \ divergence-free \emph{identically}, because $\nabla^\mu T_{\mu\nu} = 0$", font_size=32),
            label(r"4.\ \ reduces to Newton: $\nabla^2\Phi = 4\pi G\rho$", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.7)
        with self.voiceover(
            "We're ready to find Einstein's equation. Like Poisson's equation, it should say: something geometric equals "
            "a constant times the matter. <bookmark mark='h'/> The matter side is the stress–energy tensor. What goes on "
            "the left? It has to satisfy four requirements. <bookmark mark='a'/> It has to be a symmetric tensor with two "
            "indices, to match T. <bookmark mark='b'/> It should be built from the metric and its first and second "
            "derivatives, just as Newton's equation has two derivatives of phi. <bookmark mark='c'/> It has to be "
            "divergence-free automatically, because T is. <bookmark mark='d'/> And in the limit of weak fields and slow "
            "motion, it has to give back Newton."
        ) as vo:
            self.play(Write(head))
            vo.wait_until("h")
            self.play(Indicate(head[2], color=C.MATTER))
            for m, r in zip("abcd", reqs):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.reqs = reqs
        self.clear_scene()

    # ------------------------------------------------------------------
    def guess(self):
        W, (t, x, y, z, eps, Phi) = weak_static()
        assert same(first_order(W.ricci[0, 0], eps), eps * (sp.diff(Phi, x, 2) + sp.diff(Phi, y, 2) + sp.diff(Phi, z, 2)))
        rows = stack(
            mtex(r"\nabla^2\Phi", r"=", r"4\pi G\rho", font_size=44),
            mtex(r"c^2 R_{00}", r"=", r"4\pi G\rho", font_size=44),
            mtex(r"R_{00}", r"=", r"\frac{4\pi G}{c^4}\,T_{00}", font_size=44),
            buff=0.5,
        )
        rows[0][0].set_color(C.POTENTIAL)
        rows[1][0].set_color(C.CURVATURE)
        rows[2][0].set_color(C.CURVATURE)
        rows[2][2].set_color(C.MATTER)
        rows.move_to([-1.2, 1.2, 0])
        whys = VGroup(
            note(r"Newton", font_size=24).next_to(rows[0], RIGHT, buff=0.4),
            note(r"the tidal trace: $c^2 R_{00} = \nabla^2\Phi$", font_size=24).next_to(rows[1], RIGHT, buff=0.4),
            note(r"$T_{00} = \rho c^2$", font_size=24).next_to(rows[2], RIGHT, buff=0.4),
        )
        g = mtex(r"R_{\mu\nu}", r"\overset{?}{=}", r"\kappa\, T_{\mu\nu}", font_size=56)
        g[0].set_color(C.CURVATURE)
        g[2].set_color(C.MATTER)
        g.next_to(rows, DOWN, buff=0.8).set_x(0)
        gl = label(r"(essentially Einstein's proposal of 11 November 1915)", font_size=26, color=GREY_A).next_to(g, DOWN, buff=0.25)
        with self.voiceover(
            "Start from the clue at the end of the last chapter. <bookmark mark='a'/> Newton says the Laplacian of phi is "
            "four pi G rho. <bookmark mark='b'/> And the Laplacian of phi is the trace of the tidal tensor, which is c "
            "squared times the Ricci component R zero zero. <bookmark mark='c'/> And rho c squared is T zero zero. So "
            "Newton's law of gravity is one component of an equation between Ricci and T. <bookmark mark='g'/> The "
            "natural guess is that it holds for every component: Ricci equals kappa times T. Einstein proposed essentially "
            "this in early November 1915."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("g")
            self.play(Write(g), FadeIn(gl))
        self.guess_eq = g
        self.clear_scene()

    # ------------------------------------------------------------------
    def bianchi(self):
        title = label(r"The Bianchi identity", font_size=36).to_corner(UL, buff=0.4)
        rows = [
            mtex(r"0", r"=", r"\nabla_\lambda R_{\rho\sigma\mu\nu} + \nabla_\rho R_{\sigma\lambda\mu\nu} + "
                 r"\nabla_\sigma R_{\lambda\rho\mu\nu}", font_size=40),
            mtex(r"0", r"=", r"\nabla^\mu R_{\rho\sigma\mu\nu} - \nabla_\rho R_{\sigma\nu} + \nabla_\sigma R_{\rho\nu}",
                 font_size=40),
            mtex(r"0", r"=", r"-2\,\nabla^\mu R_{\sigma\mu} + \nabla_\sigma R", font_size=40),
            mtex(r"0", r"=", r"\nabla^\mu\Big(R_{\mu\nu} - \tfrac12 R\, g_{\mu\nu}\Big)", font_size=46),
        ]
        whys = [
            note(r"cyclic in $\lambda\rho\sigma$; check where $\Gamma = 0$", font_size=24),
            note(r"contract $\lambda$ with $\mu$", font_size=24),
            note(r"contract $\rho$ with $\nu$", font_size=24),
            note(r"$\nabla g = 0$", font_size=24),
        ]
        for r in rows:
            r[2].set_color(C.CURVATURE)
        x0 = -1.0
        for r, w in zip(rows, whys):
            r.shift((x0 - r[1].get_center()[0]) * RIGHT)
            w.next_to(r, DOWN, buff=0.08).align_to(r, RIGHT)
        step = ladder(self, rows, whys, keep=4, top=2.2, x=x0, buff=0.62)
        proof = VGroup(
            label(r"In locally inertial coordinates ($\Gamma = 0$ at the point):", font_size=26, color=GREY_A),
            mtex(r"\nabla_\lambda R_{\rho\sigma\mu\nu} = \partial_\lambda\big(\partial_\mu\Gamma_{\rho\nu\sigma} - "
                 r"\partial_\nu\Gamma_{\rho\mu\sigma}\big)", font_size=32),
            label(r"the cyclic sum cancels term by term (partials commute, $\Gamma$ symmetric).", font_size=26, color=GREY_A),
            label(r"A tensor equation true in one system is true in all.", font_size=26, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "But first we need one more fact about curvature. <bookmark mark='a'/> The Riemann tensor obeys a differential "
            "identity: the cyclic sum of its covariant derivatives over the first three indices vanishes. This is the "
            "Bianchi identity. <bookmark mark='p'/> The proof is short: go to a freely falling frame at a point, where "
            "every gamma vanishes. There, Riemann is just derivatives of gamma, and the cyclic sum cancels term by term. "
            "And since it's a tensor equation, it holds in every coordinate system."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            step(0)
            vo.wait_until("p")
            self.play(FadeIn(proof, lag_ratio=0.2), run_time=2)
        with self.voiceover(
            "<bookmark mark='b'/> Now contract it with the metric, pairing the derivative's index with Riemann's third "
            "index. Two of the Riemann tensors become Ricci tensors. <bookmark mark='c'/> Contract once more, and everything is Ricci or the "
            "Ricci scalar: the divergence of Ricci equals half the gradient of R. <bookmark mark='d'/> Move everything "
            "inside one derivative. The combination R mu nu minus one half R g mu nu has zero divergence, always, for any "
            "metric whatsoever."
        ) as vo:
            self.play(FadeOut(proof))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(Circumscribe(rows[3], color=C.CURVATURE))
        self.clear_scene()

    # ------------------------------------------------------------------
    def failure(self):
        g = mtex(r"R_{\mu\nu}", r"=", r"\kappa\, T_{\mu\nu}", font_size=48)
        g[0].set_color(C.CURVATURE)
        g[2].set_color(C.MATTER)
        g.to_edge(UP, buff=0.5)
        rows = stack(
            mtex(r"\nabla^\mu R_{\mu\nu}", r"=", r"\kappa\,\nabla^\mu T_{\mu\nu} = 0", font_size=40),
            mtex(r"\tfrac12\nabla_\nu R", r"=", r"0", font_size=40),
            mtex(r"\nabla_\nu T", r"=", r"0", font_size=40),
            buff=0.45,
        )
        rows.next_to(g, DOWN, buff=0.6)
        whys = VGroup(
            note(r"take the divergence", font_size=24).next_to(rows[0], RIGHT, buff=0.4),
            note(r"Bianchi: $\nabla^\mu R_{\mu\nu} = \tfrac12\nabla_\nu R$", font_size=24).next_to(rows[1], RIGHT, buff=0.4),
            note(r"trace of the guess: $R = \kappa T$", font_size=24).next_to(rows[2], RIGHT, buff=0.4),
        )
        absurd = VGroup(
            mtex(r"T = g^{\mu\nu}T_{\mu\nu} = -\rho c^2 + 3p", font_size=36),
            label(r"would have to be the same everywhere in the universe. \ Wrong.", font_size=30, color=RED_B),
        ).arrange(DOWN, buff=0.2).next_to(rows, DOWN, buff=0.6)
        cross = Cross(g, stroke_color=RED_B, stroke_width=5)
        with self.voiceover(
            "Now test the guess. <bookmark mark='a'/> Take the divergence of both sides. The right side vanishes, because "
            "matter conserves energy and momentum. <bookmark mark='b'/> But by the Bianchi identity, the divergence of "
            "Ricci is half the gradient of the Ricci scalar. So the Ricci scalar would have to be constant. "
            "<bookmark mark='c'/> And taking the trace of the guess, R is kappa times the trace of T. So the trace of T "
            "would have to be constant too: <bookmark mark='d'/> for ordinary matter that's minus the energy density plus "
            "three times the pressure, the same value everywhere in the universe, inside stars and in empty space. That's "
            "absurd. The guess is wrong."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(Write(rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(absurd))
            self.play(Create(cross))
        self.clear_scene()

    # ------------------------------------------------------------------
    def einstein(self):
        G = mtex(r"G_{\mu\nu}", r"\equiv", r"R_{\mu\nu} - \tfrac12 R\, g_{\mu\nu}", font_size=52)
        G[0].set_color(C.CURVATURE)
        G.move_to(UP * 2.0)
        Gl = label(r"the Einstein tensor: $\nabla^\mu G_{\mu\nu} = 0$ for every metric", font_size=30,
                   color=GREY_A).next_to(G, DOWN, buff=0.25)
        eq = mtex(r"G_{\mu\nu}", r"+", r"\Lambda\, g_{\mu\nu}", r"=", r"\kappa\, T_{\mu\nu}", font_size=60)
        eq[0].set_color(C.CURVATURE)
        eq[2].set_color(C.LAMBDA)
        eq[4].set_color(C.MATTER)
        eq.next_to(Gl, DOWN, buff=0.9)
        lam = label(r"$\Lambda$: allowed too, since $\nabla g = 0$ (the cosmological constant)", font_size=28,
                    color=C.LAMBDA).next_to(eq, DOWN, buff=0.4)
        checks = VGroup(*[label(t, font_size=26, color=GREY_A) for t in
                          (r"tensor \checkmark", r"$\le 2$ derivatives of $g$ \checkmark", r"divergence-free \checkmark")])
        checks.arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "But the Bianchi identity also tells us how to fix it. <bookmark mark='g'/> The combination R mu nu minus one "
            "half R g mu nu is divergence-free for every metric. It's called the Einstein tensor, G mu nu. "
            "<bookmark mark='e'/> So set it equal to kappa times T. Now the divergence of the left side is zero "
            "identically, and conservation of energy and momentum is built in, not imposed. <bookmark mark='l'/> One more "
            "term is allowed: a constant times the metric itself, since the metric has zero covariant derivative. That's "
            "the cosmological constant, lambda, which Einstein added in 1917. <bookmark mark='c'/> Three requirements down. "
            "The fourth, Newton, will fix kappa."
        ) as vo:
            vo.wait_until("g")
            self.play(Write(G), FadeIn(Gl))
            vo.wait_until("e")
            self.play(Write(eq[0]), Write(eq[3:]))
            vo.wait_until("l")
            self.play(Write(eq[1:3]), FadeIn(lam))
            vo.wait_until("c")
            self.play(FadeIn(checks, lag_ratio=0.3))
        self.clear_scene()

    # ------------------------------------------------------------------
    def kappa(self):
        title = label(r"Fixing $\kappa$ with Newton", font_size=36).to_corner(UL, buff=0.4)
        rows = [
            mtex(r"R_{\mu\nu} - \tfrac12 R\, g_{\mu\nu}", r"=", r"\kappa\, T_{\mu\nu}", font_size=40),
            mtex(r"R - 2R", r"=", r"\kappa\, T", font_size=40),
            mtex(r"R_{\mu\nu}", r"=", r"\kappa\Big(T_{\mu\nu} - \tfrac12 T\, g_{\mu\nu}\Big)", font_size=40),
            mtex(r"R_{00}", r"=", r"\kappa\Big(\rho c^2 - \tfrac12\rho c^2\Big) = \tfrac12\kappa\rho c^2", font_size=40),
            mtex(r"\frac{\nabla^2\Phi}{c^2}", r"=", r"\tfrac12\,\kappa\,\rho c^2", font_size=40),
            mtex(r"\kappa", r"=", r"\frac{8\pi G}{c^4}", font_size=50),
        ]
        whys = [
            note(r"($\Lambda$ is negligible here)", font_size=24),
            note(r"trace: $g^{\mu\nu}g_{\mu\nu} = 4$", font_size=24),
            note(r"so $R = -\kappa T$: the trace-reversed form", font_size=24),
            note(r"static dust: $T_{00} = \rho c^2$, $T = -\rho c^2$, $g_{00} \approx -1$", font_size=24),
            note(r"$c^2 R_{00} = \nabla^2\Phi$", font_size=24),
            note(r"so that $\nabla^2\Phi = 4\pi G\rho$", font_size=24),
        ]
        for r in rows:
            r[0].set_color(C.CURVATURE)
            r[2].set_color(C.MATTER)
        rows[4][0].set_color(C.POTENTIAL)
        rows[5][0].set_color(WHITE)
        rows[5][2].set_color(WHITE)
        x0 = -1.4
        for r, w in zip(rows, whys):
            r.shift((x0 - r[1].get_center()[0]) * RIGHT)
            w.next_to(r, DOWN, buff=0.08).align_to(r, RIGHT)
        step = ladder(self, rows, whys, keep=4, top=2.3, x=x0, buff=0.62)
        with self.voiceover(
            "<bookmark mark='a'/> Start from G equals kappa T, and take the trace. <bookmark mark='b'/> The trace of the "
            "metric is four, so the left side becomes R minus two R: minus R equals kappa times the trace of T. "
            "<bookmark mark='c'/> Substitute back, and we get an equivalent form, with the trace moved to the matter side: "
            "Ricci equals kappa times T minus one half T g."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        with self.voiceover(
            "<bookmark mark='d'/> Now the Newtonian situation: slowly moving dust, so T zero zero is rho c squared and the "
            "trace is minus rho c squared. The time-time component gives R zero zero equals one half kappa rho c squared. "
            "<bookmark mark='e'/> But R zero zero is the Laplacian of phi over c squared. <bookmark mark='f'/> For this to "
            "be Newton's four pi G rho, kappa must be eight pi G over c to the fourth."
        ) as vo:
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            vo.wait_until("f")
            step(5)
            self.play(Circumscribe(rows[5], color=C.CURVATURE))
        self.clear_scene()

    # ------------------------------------------------------------------
    def final(self):
        c = load("consts")
        kap = float(c["kappa"])
        assert abs(kap - 2.077e-43) < 0.001e-43
        eq = mtex(r"G_{\mu\nu}", r"+", r"\Lambda g_{\mu\nu}", r"=", r"\frac{8\pi G}{c^4}", r"\,T_{\mu\nu}", font_size=76)
        eq[0].set_color(C.CURVATURE)
        eq[2].set_color(C.LAMBDA)
        eq[5].set_color(C.MATTER)
        eb = boxed(eq, color=C.CURVATURE, buff=0.35).move_to(UP * 1.3)
        date = label(r"Einstein, 25 November 1915 \quad ($\Lambda$: 1917)", font_size=30, color=GREY_A).next_to(eb, UP, buff=0.3)
        b1 = Brace(eq[0], DOWN, color=C.CURVATURE, buff=0.5)
        b1l = label(r"curvature", font_size=28, color=C.CURVATURE).next_to(b1, DOWN, buff=0.1)
        b2 = Brace(eq[5], DOWN, color=C.MATTER, buff=0.5)
        b2l = label(r"energy, momentum, stress", font_size=28, color=C.MATTER).next_to(b2, DOWN, buff=0.1)
        stiff = mtex(r"\frac{8\pi G}{c^4} = " + sci(kap, 2) + r"\ \frac{\text{s}^2}{\text{kg}\cdot\text{m}}", font_size=36)
        stiff.next_to(VGroup(b1l, b2l), DOWN, buff=0.6).set_x(0)
        stl = label(r"spacetime is extraordinarily stiff", font_size=28, color=GREY_A).next_to(stiff, DOWN, buff=0.2)
        press = mtex(r"\text{perfect fluid:}\quad \nabla^2\Phi = 4\pi G\Big(\rho + \frac{3p}{c^2}\Big)", font_size=36)
        press.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "<bookmark mark='e'/> And there it is: Einstein's field equations. He presented them to the Prussian Academy "
            "on the twenty-fifth of November, 1915, in the trace-reversed form we just derived; the cosmological constant "
            "came two years later. <bookmark mark='b'/> Curvature on the left, energy and "
            "momentum on the right, ten equations in all. <bookmark mark='k'/> Notice how small the constant is: about "
            "two times ten to the minus forty-three in SI units. Spacetime is extraordinarily stiff. It takes the energy "
            "density of a planet or a star to bend it noticeably."
        ) as vo:
            vo.wait_until("e")
            self.play(Write(eq), Create(eb[0]), FadeIn(date), run_time=2)
            vo.wait_until("b")
            self.play(GrowFromCenter(b1), FadeIn(b1l), GrowFromCenter(b2), FadeIn(b2l))
            vo.wait_until("k")
            self.play(FadeIn(stiff), FadeIn(stl))
        with self.voiceover(
            "There's a bonus inside the trace-reversed form. <bookmark mark='p'/> For a fluid with pressure, the same "
            "calculation gives the Laplacian of phi equals four pi G times rho plus three p over c squared. In Einstein's "
            "theory, pressure gravitates too. That will matter for stars, and for the universe."
        ) as vo:
            vo.wait_until("p")
            self.play(FadeOut(VGroup(stiff, stl)), Write(press))
        self.clear_scene()
