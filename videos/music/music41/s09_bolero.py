from __future__ import annotations

import numpy as np

from videos.music.music41.common import *  # noqa: F403
from explainer.music.monochord import orchestra as O


class Bolero(SoundScene):
    def construct(self):
        chapter(self, 8, r"Ravel's harmonics", r"Can instruments become the partials of a new instrument?")
        self.series()
        self.build()
        self.cents()
        self.organ()
        self.plan()
        self.cresc()

    # ------------------------------------------------------------------
    def ladder(self):
        f0 = 261.63
        x0, W = -5.5, 11.0
        fmax = 1700.0
        ax = Line([x0, -1.4, 0], [x0 + W, -1.4, 0], color=GREY_B)
        harms = VGroup()
        for k in range(1, 7):
            x = x0 + W * k * f0 / fmax
            harms.add(VGroup(DashedLine([x, -1.4, 0], [x, 2.0, 0], color=GREY_D, stroke_width=1), label(rf"{k}", font_size=16, color=GREY_A).move_to([x, -1.7, 0])))
        players = VGroup()
        for name, shift, k, col in (("horn", 0, 1, TUNE), ("celesta", 24, 4, BLUE), ("piccolo", 19, 3, EAR), ("piccolo", 28, 5, "#A3E635")):
            f = f0 * 2 ** (shift / 12)
            x = x0 + W * f / fmax
            players.add(VGroup(Arrow([x, 2.4, 0], [x, 0.4, 0], color=col, buff=0, stroke_width=4), label(name, font_size=17, color=col).move_to([x, 2.65, 0])))
        xl = label(r"harmonics of the horn's C", font_size=16, color=GREY_A).move_to([x0 + 1.5, -2.1, 0])
        return ax, harms, players, xl

    def series(self):
        d = load("hook")
        ax, harms, players, xl = self.ladder()
        cap = label(r"the horn plays C4; \ each other instrument sits on one of its harmonics", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.6)
        head = label(r"four instruments on one harmonic series", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here is Ravel's trick, drawn. <bookmark mark='a'/> The horn's C and its first six harmonics. <bookmark mark='b'/> "
            "The celesta plays two octaves up, on the fourth harmonic. One piccolo plays a twelfth up, on the third. The other "
            "plays two octaves and a major third up, on the fifth. Each instrument doubles a partial the horn already has, so "
            "the ear groups them all into one tone, louder in those partials: a new timbre built by hand."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(harms))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(p[0]) for p in players], lag_ratio=0.3), *[FadeIn(p[1]) for p in players], FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def build(self):
        d = load("build")
        c = clip("build.four")
        ax, harms, players, xl = self.ladder()
        steps = VGroup(*[label(t, font_size=20, color=col) for t, col in ((r"horn", TUNE), (r"+ celesta", BLUE), (r"+ piccolo \ (3rd)", EAR), (r"+ piccolo \ (5th)", "#A3E635"))]).arrange(RIGHT, buff=0.9).to_edge(DOWN, buff=1.05)
        cap = label(r"one instrument added each time: \ listen for the moment the sum stops sounding like a chord", font_size=18, color=GREY_A).next_to(steps, DOWN, buff=0.2)
        for p_ in players[1:]:
            p_.set_opacity(0.15)
        with self.voiceover(
            "Hear it assembled one instrument at a time: the horn alone; with the celesta; with the first piccolo; with the "
            "second. Listen for the point at which the sum stops sounding like several instruments and starts sounding like "
            "one."
        ):
            self.play(FadeIn(ax), FadeIn(harms), FadeIn(players), FadeIn(xl), FadeIn(steps), FadeIn(cap))
        beat = d["beat"]
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"built up", kind="synthesized", detail=r"additive instruments", corner=DL, tag_corner=DR)
            for k, t0 in enumerate(st):
                pulse(snd, steps[k], t0, t0 + 8 * beat, buff=0.1)
                if k:
                    snd.drive(players[k], lambda m, t, t0=t0: m.set_opacity(1.0 if t >= t0 else 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cents(self):
        d = load("hook")
        co = d["cents_off"]
        rows_ = VGroup(
            label(rf"celesta, \ two octaves up: \ the 4th harmonic exactly \ ({co['24']:.0f} cents)", font_size=21, color=BLUE),
            label(rf"piccolo, \ a twelfth up \ (G): \ {co['19']:.0f} cents from the 3rd harmonic", font_size=21, color=EAR),
            label(rf"piccolo, \ two octaves and a third up \ (E): \ +{co['28']:.0f} cents from the 5th harmonic", font_size=21, color="#A3E635"),
            label(rf"share of the combination's power on one harmonic series \ (within 20 cents): \ {100 * d['fusion']:.1f}\%", font_size=21, color=TUNE),
            label(r"Ravel's players read equal-tempered notes, \ so the fifth harmonic is 14 cents sharp: \ the mixture shimmers slightly", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"how well do they fit?", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "How well do they fit? <bookmark mark='a'/> The celesta's octaves are exact. The piccolo on G is two cents flat "
            "of the third harmonic, too little to hear. The piccolo on E is fourteen cents sharp of the fifth harmonic, "
            "because the players read equal-tempered notes, Part 6's comma made audible. <bookmark mark='b'/> Monochord's "
            "fusion measure, the share of the combination's power that lies on one harmonic series, is almost exactly one; "
            "the small mistuning of the E gives the mixture a slight shimmer, which may be part of its charm."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[:3].copy().set_opacity(0.2)))
            vo.wait_until("a")
            self.play(FadeIn(rows_[:3]))
            vo.wait_until("b")
            self.play(FadeIn(rows_[3:]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        items = [
            (r"Bol\'ero's plan: \ one tune in two halves, \ eighteen statements, \ always in C until a final lurch to E", WHITE),
            (r"a snare drum plays one two-bar rhythm 169 times, \ from \textit{pianissimo} to \textit{fortissimo}", WHITE),
            (r"the only development is orchestration: \ more instruments, \ new combinations, \ louder", WHITE),
            (r"a fifteen-minute crescendo made of timbre", TUNE),
            (r"Ravel wrote it as a ballet, \ for the dancer Ida Rubinstein", GREY_A),
        ]
        rows_scene(self, r"a crescendo of timbre", items,
                   "The whole piece is built the same way. <bookmark mark='b'/> Boléro states its tune eighteen times, always in "
                   "C, until a final lurch to E near the end. <bookmark mark='c'/> A snare drum plays one two-bar rhythm a hundred "
                   "and sixty-nine times, from very soft to very loud. <bookmark mark='d'/> The only development is orchestration: "
                   "more instruments, new combinations, more volume. <bookmark mark='e'/> A fifteen-minute crescendo made of "
                   "timbre. <bookmark mark='f'/> Ravel wrote it as a ballet, for the dancer Ida Rubinstein.", marks="cdef")

    # ------------------------------------------------------------------
    def cresc(self):
        d = load("cresc")
        c = clip("cresc.four")
        bars = VGroup(*[VGroup(*[Square(0.32, stroke_width=0, fill_color=TUNE, fill_opacity=0.8) for _ in range(n)]).arrange(UP, buff=0.05) for n in d["sizes"]]).arrange(RIGHT, buff=1.4, aligned_edge=DOWN).move_to(DOWN * 0.2)
        labs = VGroup(*[label(rf"{n} \ instrument{'s' if n > 1 else ''}", font_size=18, color=GREY_A).next_to(b, DOWN, buff=0.2) for n, b in zip(d["sizes"], bars)])
        head = label(r"Bol\'ero's plan in miniature", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here is that plan in miniature: our phrase four times, with one, two, four and six instruments, each pass a "
            "little louder."
        ):
            self.play(FadeIn(head), FadeIn(bars), FadeIn(labs))
        beat = d["beat"]
        with self.listen(c) as snd:
            window(snd, r"a crescendo of instruments", kind="synthesized", detail=r"additive instruments", corner=DL, tag_corner=DR)
            for k, t0 in enumerate(d["starts"]):
                pulse(snd, bars[k], t0, t0 + 8 * beat, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def organ(self):
        items = [
            (r"the pipe organ's `mixture' stops sound octaves, \ fifths and thirds above each key: \ built-in harmonics", WHITE),
            (r"organ builders did additive synthesis in pipes for centuries before Ravel", WHITE),
            (r"Messiaen wrote chords as colours, \ and spectral composers \ (Part 30) \ wrote chords from analysed spectra", WHITE),
            (r"a chord on the harmonic series is heard as one tone; \ off it, \ as a chord", TUNE),
            (r"the line between harmony and timbre is the harmonic series", GREY_A),
        ]
        rows_scene(self, r"mixtures before and after Ravel", items,
                   "Ravel was not the first. <bookmark mark='b'/> The pipe organ's mixture stops sound octaves, fifths and thirds above every key: built-in harmonics. <bookmark mark='c'/> Organ builders did additive synthesis in pipes for centuries. <bookmark mark='d'/> Later, Messiaen wrote chords as colours, and the spectral composers of Part 30 wrote chords from analysed spectra. <bookmark mark='e'/> A chord on the harmonic series is heard as one tone; off it, as a chord. <bookmark mark='f'/> The line between harmony and timbre is the harmonic series.", marks="cdef")
