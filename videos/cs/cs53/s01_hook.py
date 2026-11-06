from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs53.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


def _bytes(n: int) -> str:
    b = 16 * 2 ** n                                    # one complex number in double precision: 16 bytes
    for unit, k in (("EB", 60), ("PB", 50), ("TB", 40), ("GB", 30), ("MB", 20), ("kB", 10)):
        if b >= 2 ** k:
            return rf"{b / 2 ** k:,.0f} {unit}"
    return rf"{b} bytes"


class Hook(VoiceoverScene):
    def construct(self):
        self.feynman()
        self.thesis()
        self.plan()

    def feynman(self):
        head = label(r"Simulating nature is exponentially hard", font_size=36).to_edge(UP, buff=0.3)
        quote = wrapped_label(r"``Nature isn't classical, dammit, \ and if you want to make a simulation of nature, \ "
                              r"you'd better make it quantum mechanical.'' \ --- Richard Feynman, \ 1981",
                              11.5, font_size=21, color=GREY_A).next_to(head, DOWN, buff=0.35)
        rows = VGroup()
        for n, col in ((10, YES), (20, YES), (30, HEAD), (40, HEAD), (50, NO)):
            bar_w = 0.11 * n
            bar = Rectangle(width=bar_w, height=0.38, stroke_width=0, fill_color=col, fill_opacity=0.85)
            t = label(rf"{n} particles", font_size=20, color=WHITE)
            v = label(rf"$2^{{{n}}}$ amplitudes: \ {_bytes(n)}", font_size=20, color=col)
            rows.add(VGroup(t, bar, v))
        for r in rows:
            r[0].move_to([-5.3, 0, 0])
            r[1].next_to([-4.2, 0, 0], RIGHT, buff=0)
            r[2].next_to(r[1], RIGHT, buff=0.25)
        rows.arrange(DOWN, buff=0.28, aligned_edge=LEFT).next_to(quote, DOWN, buff=0.45).to_edge(LEFT, buff=0.6)
        atoms = wrapped_label(rf"at 300 particles, \ $2^{{300}} \approx 10^{{{300 * math.log10(2):.0f}}}$ "
                              r"amplitudes: \ more than the roughly $10^{80}$ atoms in the observable universe",
                              12.0, font_size=21, color=WHITE).to_edge(DOWN, buff=0.45)
        note_ = note(r"each amplitude stored as one complex number, \ 16 bytes", font_size=16).next_to(atoms, UP,
                                                                                                   buff=0.2)
        with self.voiceover(
            "In 1981 Richard Feynman gave a talk with a simple question: can a computer simulate physics? "
            "<bookmark mark='a'/> For classical physics, yes. But a system of quantum particles is described by one "
            "complex number, an amplitude, for every combination of their states. <bookmark mark='b'/> Ten "
            "two-state particles need about a thousand amplitudes, which fit in sixteen kilobytes. Twenty need "
            "sixteen megabytes. Thirty, sixteen gigabytes; forty, sixteen terabytes; fifty, sixteen petabytes. "
            "<bookmark mark='c'/> Three hundred particles need more numbers than there are atoms in the observable "
            "universe. Feynman suspected no classical computer could keep up, and proposed the alternative: build "
            "the computer out of quantum parts, and let nature do the arithmetic."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(quote))
            vo.wait_until("b")
            for r in rows:
                self.play(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(atoms), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def thesis(self):
        head = label(r"The one serious challenge to Part 1's thesis", font_size=36).to_edge(UP, buff=0.3)
        ect = wrapped_label(r"\textbf{the extended Church--Turing thesis}: \ any reasonable model of computation can "
                            r"be simulated by a probabilistic Turing machine \ with at most polynomial slowdown",
                            11.5, font_size=23, color=WHITE).next_to(head, DOWN, buff=0.5)
        boxes = VGroup()
        for t, d, c in ((r"1985", r"Deutsch: \ a universal quantum computer", DATA),
                        (r"1994", r"Shor: \ factoring in polynomial time, \ breaking Part 30's RSA", NO),
                        (r"1996", r"Grover: \ search in $\sqrt N$ steps, \ and no faster", HEAD),
                        (r"2024", r"error correction below threshold, \ in hardware", YES)):
            r = RoundedRectangle(width=3.0, height=1.9, corner_radius=0.15, stroke_color=c, stroke_width=2,
                                 fill_color=BG, fill_opacity=1)
            g = VGroup(label(t, font_size=24, color=c), wrapped_label(d, 2.7, font_size=17, color=GREY_A)).arrange(
                DOWN, buff=0.15).move_to(r)
            boxes.add(VGroup(r, g))
        boxes.arrange(RIGHT, buff=0.25).next_to(ect, DOWN, buff=0.55)
        foot = wrapped_label(r"if large quantum computers can be built, \ the thesis is false: \ factoring is easy for "
                             r"them, \ and no one knows a fast classical algorithm", 12.4, font_size=21,
                             color=LAM).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Part 1 met the extended Church–Turing thesis: any reasonable computer can be simulated by a "
            "probabilistic Turing machine with at most polynomial slowdown. <bookmark mark='a'/> In 1985 David "
            "Deutsch described a universal quantum computer. <bookmark mark='b'/> In 1994 Peter Shor showed that "
            "such a machine could factor large numbers in polynomial time, which would break the cryptography of "
            "Part 30. <bookmark mark='c'/> In 1996 Lov Grover showed it could search an unsorted list in about the "
            "square root of its length, and no quantum algorithm can do better. <bookmark mark='d'/> And in "
            "2024 an experiment showed quantum error correction getting better, not worse, as the code grows. "
            "<bookmark mark='e'/> If large machines can be built, the extended thesis is false. This part builds the "
            "mathematics, and a simulator, and runs every algorithm on it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ect))
            for mk, b in zip("abcd", boxes):
                vo.wait_until(mk)
                self.play(FadeIn(b, shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Quantum Computation", font_size=36).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"reversible computing, \ and the price of forgetting",
            r"the qubit, \ the Bloch sphere and entanglement",
            r"interference: \ Deutsch--Jozsa, \ Bernstein--Vazirani, \ Simon",
            r"the quantum Fourier transform and phase estimation",
            r"Shor factors 15 and 21; \ Grover searches",
            r"error correction, \ and what quantum computers cannot do",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 53 of Computer Science, Built. <bookmark mark='a'/> We start with the energy cost of "
            "forgetting a bit, and computation that never forgets. Then the qubit, the Bloch sphere and "
            "entanglement; interference as the resource behind every quantum algorithm; the quantum Fourier "
            "transform, built from Part 19's butterflies; Shor's algorithm factoring fifteen and twenty-one on our "
            "own simulator; Grover's search; error correction; and an honest account of what quantum computers "
            "cannot do."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (KERN, LAM, NO, YES)
