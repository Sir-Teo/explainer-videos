from __future__ import annotations

import numpy as np

from videos.music.music48.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ converter limits, \ and sampling below Nyquist", r"What limits a converter, \ and must we always sample at twice the band?")
        self.limits()
        self.sparse()
        self.problem()

    # ------------------------------------------------------------------
    def limits(self):
        items = [
            (r"a 24-bit word could hold 146 dB; \ no converter reaches it: \ the thermal noise of its own resistors sets the floor", WHITE),
            (r"the best converters reach a dynamic range of roughly 120 to 130 decibels: \ about 20 usable bits", WHITE),
            (r"jitter, \ the modulator's stability, \ and the reference voltage's noise set the rest", WHITE),
            (r"for audio this is far below anything a room or an ear can show", TUNE),
            (r"the open problems are cost, \ power and size: \ converters in earbuds and hearing aids", GREY_A),
        ]
        rows_scene(self, r"what limits a converter", items,
                   "Two frontiers. First, what limits a converter? <bookmark mark='b'/> A twenty-four-bit word could hold a hundred "
                   "and forty-six decibels, but no converter reaches it: the thermal noise of its own resistors sets the floor. "
                   "<bookmark mark='c'/> The best converters reach a dynamic range of roughly a hundred and twenty to a hundred and "
                   "thirty decibels: about twenty usable bits. <bookmark mark='d'/> Jitter, the modulator's stability and the reference voltage's noise set "
                   "the rest. <bookmark mark='e'/> Such converter noise is often below room and microphone noise in ordinary recording, while audibility depends on gain and listening conditions. "
                   "<bookmark mark='f'/> The open problems are cost, power and size: converters in earbuds and hearing aids.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def sparse(self):
        items = [
            (r"the theorem asks for twice the band; \ but a signal with few degrees of freedom may need far fewer samples", WHITE),
            (r"Martin Vetterli, \ Pina Marziliano and Thierry Blu \ (2002): \ a few spikes, \ recovered exactly from a few samples", WHITE),
            (r"Emmanuel Cand\`es, \ Justin Romberg and Terence Tao, \ and David Donoho \ (2006): \ compressed sensing", WHITE),
            (r"a signal sparse in some basis is recovered from random measurements by an $\ell_1$ minimisation", TUNE),
            (r"music is not sparse in time, \ but often nearly sparse in frequency: \ where the theorem's fine print can be renegotiated", GREY_A),
        ]
        rows_scene(self, r"sampling below Nyquist", items,
                   "Second, must we always sample at twice the band? <bookmark mark='b'/> The theorem asks that much of any band-limited signal, but a signal with few degrees of freedom may need far fewer samples. In 2002 Martin Vetterli, Pina Marziliano and Thierry Blu showed that a few spikes can be recovered exactly from a few samples. <bookmark mark='d'/> In 2006 Emmanuel Candès, Justin Romberg and Terence Tao, and David Donoho, founded compressed sensing: <bookmark mark='e'/> a sufficiently sparse signal can be recovered from suitable measurements under incoherence or related recovery conditions, often by l-one optimization. <bookmark mark='f'/> Music is not sparse in time, but it is often nearly sparse in frequency, and that is where the theorem's fine print can be renegotiated.",
                   marks="bdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"take a recording's short frames; \ measure how sparse each is in a good basis", WHITE),
            (r"sample them at random below the Nyquist rate and recover them by $\ell_1$ minimisation", WHITE),
            (r"measure the error against the sample count, \ frame by frame, \ for many kinds of music", WHITE),
            (r"$\bigstar$ \ research problem: \ how far below Nyquist can music be sampled before listeners notice?", EAR),
            (r"an answer would turn the theorem's worst case into music's typical case", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A research problem to end on. <bookmark mark='a'/> Take a recording's short frames, and measure how sparse each "
            "is in a good basis. <bookmark mark='b'/> Acquire suitable nonuniform or compressed measurements below the conventional full-band sample count, accounting for analog front-end and reconstruction assumptions, and recover them by "
            "minimising an l-one norm. <bookmark mark='c'/> Measure the error against the number of samples, frame by frame, "
            "for many kinds of music. <bookmark mark='d'/> The question: how far below the Nyquist rate can music be sampled "
            "before listeners notice? <bookmark mark='e'/> An answer would turn the theorem's worst case into music's typical "
            "case."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
