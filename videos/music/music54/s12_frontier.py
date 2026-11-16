from __future__ import annotations

import numpy as np

from videos.music.music54.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ arrays, \ beamforming and linearization", r"Can many microphones listen in one direction?")
        self.beam()
        self.quiz()
        self.mems()
        self.linear()
        self.problem()

    # ------------------------------------------------------------------
    def beam(self):
        d = load("beam")
        ang = np.array(d["angles"])
        ax = frame_axes(width=8.0, height=3.0, xlo=-90, xhi=90, ylo=0, yhi=1.05, center=LEFT * 0.8 + DOWN * 0.3)
        cols = {"500": GREY_A, "1000": BLUE, "2000": TUNE, "4000": EAR}
        cs = VGroup(*[curve(ang, d["pattern"][k], ax.to, color=c, width=2.5) for k, c in cols.items()])
        key = VGroup(*[label(rf"{int(k)} Hz", font_size=17, color=c) for k, c in cols.items()]).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.4)
        xt = VGroup(*[label(f"{v}$^\\circ$", font_size=14, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.1) for v in (-90, -40, 0, 40, 90)])
        note = label(r"eight microphones 5 cm apart, \ delayed and summed towards straight ahead: \ narrow at high frequencies, \ blind to direction at low ones", font_size=17, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"an array's pattern", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "One microphone's pattern is fixed; many can be steered. <bookmark mark='a'/> Put eight in a line, five centimetres "
            "apart, delay each so that sound from the chosen direction lines up, and add. <bookmark mark='b'/> At four "
            "kilohertz the result is a narrow beam; at five hundred hertz it is barely directional at all, because the array, "
            "thirty-five centimetres long, is shorter than the wavelength. Conference systems, smart speakers and phones all do "
            "this."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(ghost(cs, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(note))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c_) for c_ in cs[::-1]], lag_ratio=0.3), FadeIn(key), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("beam")
        c = clip("beam.two")
        card = listen_card(r"Two singers: \ a tenor straight ahead, \ a soprano 40 degrees to the side. \ Once one microphone; \ once eight "
                           r"microphones steered at the tenor. \ Which was the array?", width=10.0)
        with self.voiceover(
            "Your turn. Two singers, a tenor straight ahead and a soprano forty degrees to the side. Once one microphone; once "
            "eight microphones steered at the tenor. Which was the array?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two singers, \ twice", kind="synthesized", detail=r"Part 8's voices", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["single"], st["array"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["array"], c.duration, buff=0.08)
        with self.voiceover(
            "The second. The soprano is quieter and duller there: overall about "
            f"{say(-d['rejection_db'])} decibels down, but much more at her upper harmonics than at her fundamentals, exactly as "
            "the pattern predicted. This small conventional delay-and-sum array has little bass directivity; other array designs can trade robustness and noise for more."
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def linear(self):
        items = [
            (r"a small loudspeaker driven hard is nonlinear: \ its motor and suspension change with the cone's position", WHITE),
            (r"distortion and compression follow, \ worst in the bass where the cone travels furthest", WHITE),
            (r"linearization: \ model the driver's nonlinear circuit, \ track it as it heats and ages, \ and pre-distort the signal so the cone moves as intended", WHITE),
            (r"phones and smart speakers do this to sound bigger than their size", WHITE),
            (r"the same idea, \ run backwards, \ as Part 50's amplifier models", TUNE),
        ]
        rows_scene(self, r"making a small speaker behave", items,
                   "The second frontier is the loudspeaker itself. <bookmark mark='b'/> A small one driven hard is nonlinear: its "
                   "motor strength and suspension change with the cone's position, <bookmark mark='c'/> and distortion and "
                   "compression follow, worst in the bass where the cone travels furthest. <bookmark mark='d'/> Linearization models "
                   "the driver's nonlinear circuit, tracks it as it heats and ages, and pre-distorts the signal so that the cone "
                   "moves as intended. <bookmark mark='e'/> Phones and smart speakers do this to sound bigger than they are. "
                   "<bookmark mark='f'/> It is Part 50's amplifier modelling, run backwards.", marks="bcdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"take a small driver's nonlinear model: \ $Bl(x)$, \ $K(x)$, \ the coil's heating", WHITE),
            (r"pre-distort the signal through its inverse, \ with the parameters estimated as it plays", WHITE),
            (r"measure distortion, \ excursion and loudness, \ and listen blind", WHITE),
            (r"$\bigstar$ \ research problem: \ how much louder and deeper can a given small speaker be made to sound, \ safely, \ by control alone?", EAR),
            (r"an answer would set the size of every phone and earbud", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A research problem to end on. <bookmark mark='a'/> Take a small driver's nonlinear model: its motor strength and "
            "stiffness as functions of position, and the coil's heating. <bookmark mark='b'/> Pre-distort the signal through "
            "its inverse, with the parameters estimated while it plays. <bookmark mark='c'/> Measure distortion, excursion and "
            "loudness, and listen blind. <bookmark mark='d'/> The question: how much louder and deeper can a given small speaker "
            "be made to sound, safely, by control alone? <bookmark mark='e'/> An answer would set the size of every phone and "
            "earbud."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mems(self):
        items = [
            (r"MEMS microphones: \ a condenser etched in silicon, \ a millimetre across, \ made like a chip", WHITE),
            (r"matched to each other almost exactly, \ so arrays of them can be built cheaply", WHITE),
            (r"a phone has three or four; \ a smart speaker six or seven, \ in a ring", WHITE),
            (r"their signals feed beamformers, \ cancellers and speech recognizers at once", WHITE),
            (r"the microphone has become a sensor array with software behind it", TUNE),
        ]
        rows_scene(self, r"microphones on a chip", items,
                   "Arrays became cheap because microphones became chips. <bookmark mark='b'/> A MEMS microphone is a condenser etched in silicon, a millimetre across, made like any other chip, <bookmark mark='c'/> and production gives compact, consistent sensors, though mismatch and calibration still matter, so arrays of them cost little. <bookmark mark='d'/> Microphone counts vary by device; phones and smart speakers often use several, in a ring, <bookmark mark='e'/> feeding beamformers, cancellers and speech recognizers at once. <bookmark mark='f'/> The microphone has become a sensor array with software behind it.", marks="bcdef")
