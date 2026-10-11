from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum2.common import (ab_movie, label, load, mtex, note, phase_img, phase_rgba, phasor_chain, signed_img, to_img)
from videos.quantum2.compute import AB


def framed(img, caption):
    box = Rectangle(width=img.width + 0.08, height=img.height + 0.08, stroke_color=GREY_C, stroke_width=1.5).move_to(img)
    cap = label(caption, font_size=20, color=GREY_A).next_to(box, DOWN, buff=0.08)
    return Group(img, box, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.map_()
        self.motif()
        self.gallery()
        self.beyond()

    # ------------------------------------------------------------------
    def map_(self):
        cols = [
            (r"symmetry", C.QTIME, [r"time $\to$ $i\hbar\,\partial_t\psi = \hat H\psi$", r"space $\to$ $[\hat x, \hat p] = i\hbar$", r"boosts $\to$ $\hat H = \hat p^2/2m + V$",
                                    r"rotations $\to$ spin $\tfrac12$", r"local phase $\to$ electromagnetism"]),
            (r"sums over paths", C.ACTION, [r"$\int\mathcal Dx\,e^{iS/\hbar}$ $\to$ Schr\"odinger", r"$\hbar \to 0$ $\to$ Newton", r"WKB $\to$ $(n + \tfrac12)h$",
                                           r"tunneling $\to$ alpha decay"]),
            (r"approximations", C.PERTURB, [r"perturbation theory", r"level repulsion", r"asymptotic series", r"the golden rule $\to$ lifetimes"]),
            (r"many particles", C.FERMION, [r"bosons and fermions", r"Pauli $\to$ the periodic table", r"exchange $\to$ Hund's rule", r"Bloch $\to$ bands, metals"]),
            (r"open systems", C.COHERENCE, [r"density matrices", r"Gleason $\to$ the Born rule", r"decoherence"]),
            (r"relativity", C.DIRAC_POS, [r"Dirac $\to$ $g = 2$, antimatter", r"fine structure", r"$\to$ QED"]),
        ]
        g = VGroup()
        for title, c, items in cols:
            col = VGroup(label(title, font_size=26, color=c), *[label(i, font_size=19, color=GREY_A) for i in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            g.add(col)
        top = VGroup(*g[:3]).arrange(RIGHT, buff=0.6, aligned_edge=UP)
        bot = VGroup(*g[3:]).arrange(RIGHT, buff=0.6, aligned_edge=UP)
        allg = VGroup(top, bot).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        if allg.width > 13.2:
            allg.width = 13.2
        allg.move_to(DOWN * 0.2)
        t = label(r"Part 2, on one screen", font_size=36, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's look back. <bookmark mark='a'/> The rules that Part 1 guessed came out of symmetry: time gave the "
            "Schrödinger equation, space gave the commutator, boosts gave the Hamiltonian, rotations allowed spin, and "
            "local phase demanded electromagnetism. <bookmark mark='b'/> Feynman's sum over paths gave the same equation, "
            "and in the limit of small h-bar, Newton's laws, the old quantum rules and alpha decay. "
            "<bookmark mark='c'/> Perturbation theory and the golden rule turned it into numbers for real atoms. "
            "<bookmark mark='d'/> Exchange symmetry built the periodic table and the bands of solids. "
            "<bookmark mark='e'/> Density matrices gave us the Born rule and decoherence. <bookmark mark='f'/> And "
            "relativity, through Dirac, gave spin's magnetism, fine structure and antimatter."
        ) as vo:
            self.play(FadeIn(t))
            for m, c in zip("abcdef", g):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=DOWN * 0.1), run_time=0.9)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def motif(self):
        rows = VGroup(
            VGroup(label(r"translate, then boost", font_size=28), MathTex(r"e^{-i\,mva/\hbar}:\ \ \text{area of a phase-space rectangle}", font_size=30)).arrange(RIGHT, buff=0.5),
            VGroup(label(r"Aharonov--Bohm", font_size=28), MathTex(r"e^{iq\Phi/\hbar}:\ \ \text{flux through the loop}", font_size=30)).arrange(RIGHT, buff=0.5),
            VGroup(label(r"Bohr--Sommerfeld", font_size=28), MathTex(r"\oint p\,dx = (n + \tfrac12)h:\ \ \text{area of the orbit}", font_size=30)).arrange(RIGHT, buff=0.5),
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(DOWN * 0.3)
        t = MathTex(r"\text{phase} = \frac{\text{area}}{\hbar}", font_size=56, color=C.HBAR).to_edge(UP, buff=0.6)
        with self.voiceover(
            "And one idea kept coming back: <bookmark mark='a'/> a phase is an area divided by h-bar. The area of a "
            "rectangle in phase space, when translations and boosts fail to commute; <bookmark mark='b'/> the magnetic "
            "flux through a loop, in the Aharonov-Bohm effect; <bookmark mark='c'/> and the area of a classical orbit, in "
            "the quantum condition."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(t), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gallery(self):
        h = 2.0
        mv = ab_movie(0.5)
        P = AB
        f = np.asarray(mv[95, 44:244, 50:290], np.float32)
        psi = (f[..., 0] + 1j * f[..., 1])[::-1]
        gain = np.ones(240, np.float32)
        gain[int(P["wall"][1] - 50) + 1:] = 3.0
        ab = to_img(phase_rgba(psi * gain[None, :], vmax=0.016, gamma=0.6), height=h, width=h * 240 / 200)
        s = load("stationary")
        ch = phasor_chain(s["arrows_1"], unit=3.2, stroke_width=2.5, tips=False)
        ch.height = h * 0.9
        chain = Group(Rectangle(width=h * 1.2, height=h, stroke_width=0).set_opacity(0), ch)
        ch.move_to(chain[0])
        w = load("wkb")
        wx, wp = w["wig_x"], w["wig_p"]
        W = w["wig"][np.ix_(np.abs(wp) <= 8.5, np.abs(wx) <= 2.6)]
        wig = signed_img(W[::-1], height=h, width=h * 0.85)
        he = load("helium")
        tri = phase_img(he["tp_trip"][::-1].astype(complex), height=h, width=h, gamma=0.7)
        d = load("decoherence")
        cat = signed_img(d["W"][0][::-1], height=h, width=h * 1.4)
        tiles = Group(framed(ab, r"Aharonov--Bohm, $\Phi = h/2e$"), framed(chain, r"a Cornu spiral of paths"), framed(wig, r"a WKB orbit's Wigner function"),
                      framed(tri, r"helium's triplet, $(r_1, r_2)$"), framed(cat, r"a cat, before decoherence")).arrange_in_grid(rows=2, buff=(0.6, 0.45))
        cap = note(r"every picture in this video was computed from the equations, not drawn").to_edge(DOWN, buff=0.25)
        tiles.next_to(cap, UP, buff=0.3)
        if tiles.get_top()[1] > 3.8:
            tiles.scale((3.8 - tiles.get_bottom()[1]) / tiles.height).next_to(cap, UP, buff=0.3)
        with self.voiceover(
            "As in Part 1, every picture you've seen came from solving equations, not from an artist's impression: the "
            "electron going around a flux tube, the arrows of a thrown ball's paths, an orbit in phase space, the two "
            "electrons of helium keeping apart, and a cat state about to lose its fringes."
        ):
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tiles], lag_ratio=0.3), FadeIn(cap), run_time=3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def beyond(self):
        title = label(r"Where to go next", font_size=44).to_edge(UP, buff=0.6)
        items = VGroup(
            label(r"\textbf{quantum field theory}: particles as excitations of fields; why the vacuum shifts levels", font_size=28),
            label(r"\textbf{quantum information}: entanglement and density matrices as a resource; quantum computers", font_size=28),
            label(r"\textbf{the measurement problem}: what, if anything, makes one outcome real", font_size=28),
            label(r"\textbf{gauge theories}: local symmetry, applied to more than a phase, gives the other forces", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(title, DOWN, buff=0.6)
        if items.width > 13.2:
            items.width = 13.2
        end = label(r"Thanks for watching.", font_size=36, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "From here, the roads lead to quantum field theory, where particles are excitations of fields and the vacuum "
            "itself shifts atomic levels; to quantum information, where entanglement is a resource; to the measurement "
            "problem, still open; and to gauge theories, where the same local-symmetry argument that gave us "
            "electromagnetism gives the other forces of nature. Thanks for watching."
        ):
            self.play(FadeIn(title))
            self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.15) for i in items], lag_ratio=0.5), run_time=6)
            self.play(FadeIn(end))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects])
