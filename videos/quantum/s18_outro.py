from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum import colormap as qcm
from videos.quantum.common import (FieldMovie2D, boxed, label, load, mtex, note, orbital_image)
from videos.quantum.s14_classical import wigner_rgba


def framed(img: Mobject, caption: str) -> Group:
    box = Rectangle(width=img.width + 0.08, height=img.height + 0.08, stroke_color=GREY_C, stroke_width=1.5).move_to(img)
    cap = label(caption, font_size=22, color=GREY_A).next_to(box, DOWN, buff=0.1)
    return Group(img, box, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.one_screen()
        self.gallery()
        self.beyond()

    # ------------------------------------------------------------------
    def one_screen(self):
        se = MathTex(r"i\hbar\,\frac{d}{dt}\ket{\psi}", r"=", r"\hat H\ket{\psi}", font_size=50)
        se[0].set_color(C.ENERGY)
        se[2].set_color(C.ENERGY)
        born = MathTex(r"P(a) = |\braket{a}{\psi}|^2", font_size=46, color=C.BORN)
        cr = MathTex(r"[\hat x, \hat p] = i\hbar", font_size=50, color=C.HBAR)
        top = VGroup(se, born, cr).arrange(RIGHT, buff=0.9).to_edge(UP, buff=0.7)
        if top.width > 13.2:
            top.width = 13.2
        lines = VGroup(
            label(r"states are unit vectors; amplitudes add, probabilities are their squares", font_size=28),
            label(r"observables are Hermitian operators; outcomes are eigenvalues", font_size=28),
            label(r"time evolution turns every energy component at its own rate, $E/\hbar$", font_size=28),
            label(r"non-commuting observables can't both be sharp: $\sigma_x\sigma_p \ge \hbar/2$", font_size=28),
            label(r"energies are quantized when the wave must fit: boxes, wells, atoms", font_size=28),
            label(r"entangled systems share one wavefunction; their correlations beat any local model", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(top, DOWN, buff=0.7)
        with self.voiceover(
            "Let's step back and see how far we've come. <bookmark mark='a'/> The whole theory fits on one line: the "
            "Schrödinger equation, the Born rule, and the commutation relation between position and momentum. "
            "<bookmark mark='b'/> States are vectors whose amplitudes add before you square them. Observables are "
            "Hermitian operators. Time evolution turns each energy component at its own rate. Position and momentum "
            "can't both be sharp. Energies are quantized when a wave has to fit. And entangled particles share a single "
            "wavefunction, with correlations no local model can match."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(se), FadeIn(born), Write(cr), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.15) for l in lines], lag_ratio=0.5), run_time=vo.remaining())
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gallery(self):
        t = ValueTracker(700.0)
        mv = FieldMovie2D(t, width=4.0, boost=2.0, vmax=7e-3, gamma=0.6)
        mv.refresh()  # show the frame at t = 700, then freeze it
        mv.clear_updaters()
        c = load("carpet")
        dens = np.abs(c["carpet"]) ** 2
        d = np.clip(dens / np.percentile(dens, 99.5), 0, 1) ** 0.6
        gold = qcm.hex_rgb(C.BORN)
        carpet = ImageMobject(qcm.to_uint8(qcm.BG + d[..., None] * (gold - qcm.BG)))
        carpet.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        carpet.stretch_to_fit_height(2.5).stretch_to_fit_width(3.4)
        orb = orbital_image("orb_432", height=2.5)
        o = load("oscillator")
        wig = ImageMobject(wigner_rgba(o["Wcat"]))
        wig.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        wig.stretch_to_fit_height(2.5).stretch_to_fit_width(3.4)
        mv.height = 2.5
        tiles = Group(framed(mv, r"two slits"), framed(carpet, r"a quantum carpet"), framed(orb, r"hydrogen, $(4, 3, 2)$"),
                      framed(wig, r"a cat state's Wigner function")).arrange_in_grid(rows=2, buff=(0.8, 0.35))
        cap = note(r"every picture in this video was computed from the equations, not drawn").to_edge(DOWN, buff=0.25)
        tiles.next_to(cap, UP, buff=0.3)
        assert tiles.get_top()[1] < 3.9
        with self.voiceover(
            "And every picture in this video, the wave through the slits, the carpet, the orbitals, the phase-space "
            "pictures, came from solving those equations, not from an artist's impression. A hundred years after "
            "Schrödinger, the same equation runs the transistors in your phone, the lasers in fiber-optic cables and "
            "the magnets in MRI scanners."
        ):
            self.play(LaggedStart(*[FadeIn(g) for g in tiles], lag_ratio=0.3), FadeIn(cap), run_time=3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def beyond(self):
        title = label(r"Where to go next", font_size=44).to_edge(UP, buff=0.6)
        items = VGroup(
            label(r"\textbf{identical particles} and the Pauli principle: why chemistry and solids work", font_size=30),
            label(r"\textbf{perturbation theory}: fine structure, the Lamb shift, real atoms", font_size=30),
            label(r"\textbf{the Dirac equation} (1928) and \textbf{quantum field theory}", font_size=30),
            label(r"\textbf{decoherence} and the measurement problem", font_size=30),
            label(r"\textbf{quantum computing}: the same linear algebra, in $2^n$ dimensions", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(title, DOWN, buff=0.6)
        end = label(r"Thanks for watching.", font_size=36, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "There's much more. Identical particles and the Pauli exclusion principle, which make chemistry possible. "
            "Perturbation theory, for real atoms. Dirac's relativistic equation, and quantum field theory beyond it. "
            "Decoherence, and the still-open question of what measurement really is. And quantum computing, which is "
            "the same linear algebra you've just seen, in two to the n dimensions. But all of it is built on what's on "
            "this screen: complex amplitudes, evolving by the Schrödinger equation. Thanks for watching."
        ):
            self.play(FadeIn(title))
            self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.15) for i in items], lag_ratio=0.5), run_time=6)
            self.play(FadeIn(end))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects])
