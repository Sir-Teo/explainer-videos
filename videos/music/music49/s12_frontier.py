from __future__ import annotations

import numpy as np

from videos.music.music49.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ virtual analog and differentiable effects", r"Can software become the circuit, \ and learn its own settings?")
        self.virtual()
        self.differentiable()
        self.wave()
        self.problem()

    # ------------------------------------------------------------------
    def virtual(self):
        items = [
            (r"virtual analog: \ simulate the circuit itself, \ component by component, \ nonlinearities included", WHITE),
            (r"wave digital filters \ (Alfred Fettweis, \ 1986) \ and state-space models turn circuits into stable recursions", WHITE),
            (r"Vesa V\"alim\"aki and colleagues \ (2012): \ fifty years of artificial reverberation, \ from chambers to networks", WHITE),
            (r"plates and springs are now simulated from their physics, \ as chapter 10 did", TUNE),
            (r"the hard part is the circuit's nonlinear parts, \ which Part 50 begins", GREY_A),
        ]
        rows_scene(self, r"virtual analog", items,
                   "The first frontier is to make software become the circuit. <bookmark mark='b'/> Virtual analogue simulates a "
                   "circuit component by component, nonlinearities included. <bookmark mark='c'/> Alfred Fettweis's wave digital "
                   "filters and state-space models turn circuits into stable recursions. <bookmark mark='d'/> Vesa Välimäki and "
                   "colleagues reviewed fifty years of artificial reverberation in 2012, from chambers to networks, "
                   "<bookmark mark='e'/> and plates and springs are now simulated from their physics, as chapter ten did. "
                   "<bookmark mark='f'/> The hard part is the nonlinear parts of circuits, which Part 50 begins.", marks="bcdef")

    # ------------------------------------------------------------------
    def differentiable(self):
        items = [
            (r"differentiable effects: \ write a filter or a reverb so that its output's gradient can be computed", WHITE),
            (r"then its settings can be learned by gradient descent, \ like a neural network's weights \ (AI, \ Built)", WHITE),
            (r"Jesse Engel and colleagues' DDSP \ (2020) \ made oscillators, \ filters and reverbs differentiable", WHITE),
            (r"given a dry and a processed recording, \ find the equalizer and reverb that turn one into the other", TUNE),
            (r"or fit a feedback delay network's gains and filters to a measured room", GREY_A),
        ]
        rows_scene(self, r"effects that learn", items,
                   "The second frontier is effects that learn. <bookmark mark='b'/> Write a filter or a reverb so that the gradient "
                   "of its output can be computed, <bookmark mark='c'/> and its settings can be learned by gradient descent, like "
                   "a neural network's weights. <bookmark mark='d'/> Jesse Engel and colleagues' DDSP, in 2020, made oscillators, "
                   "filters and reverbs differentiable. <bookmark mark='e'/> Given a dry recording and a processed one, find the "
                   "equalizer and reverb that turn one into the other, <bookmark mark='f'/> or fit a feedback delay network's "
                   "gains and filters to a measured room.", marks="bcdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"measure many rooms by sweep, \ as in chapter 7", WHITE),
            (r"fit to each the smallest feedback delay network that matches its decay in every band and its echo density", WHITE),
            (r"then test, \ blind, \ whether listeners can tell the network from the measured room", WHITE),
            (r"$\bigstar$ \ research problem: \ how small can a network be and still pass for a given room?", EAR),
            (r"an answer would say how much of a room the ear actually needs", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A research problem to end on. <bookmark mark='a'/> Measure many rooms by sweep, as in chapter seven. "
            "<bookmark mark='b'/> Fit to each the smallest feedback delay network that matches its decay in every band and "
            "its echo density. <bookmark mark='c'/> Then test, blind, whether listeners can tell the network from the room. "
            "<bookmark mark='d'/> The question: how small can a network be and still pass for a given room? "
            "<bookmark mark='e'/> An answer would say how much of a room the ear actually needs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wave(self):
        items = [
            (r"image sources ignore diffraction and scattering; \ ray tracing adds scattering but not wave effects", WHITE),
            (r"wave-based methods solve the wave equation on a grid, \ as chapter 10 did for the plate", WHITE),
            (r"a whole concert hall at audio rates needs billions of grid points: \ graphics processors make it possible", WHITE),
            (r"Stefan Bilbao and colleagues simulate rooms, \ instruments and loudspeakers this way", TUNE),
            (r"Part 55 measures and simulates real halls", GREY_A),
        ]
        rows_scene(self, r"rooms from the wave equation", items,
                   "A third frontier is simulating rooms from the wave equation itself. <bookmark mark='b'/> Image sources ignore "
                   "diffraction and scattering; ray tracing adds scattering, but not wave effects. <bookmark mark='c'/> Wave-based "
                   "methods solve the wave equation on a grid, as chapter ten did for the plate. <bookmark mark='d'/> A whole "
                   "concert hall at audio rates needs billions of grid points, and graphics processors now make it possible. "
                   "<bookmark mark='e'/> Stefan Bilbao and colleagues simulate rooms, instruments and loudspeakers this way. "
                   "<bookmark mark='f'/> Part 55 measures and simulates real halls.", marks="bcdef")
