from __future__ import annotations

import numpy as np

from videos.music.music41.common import *  # noqa: F403
from explainer.music.monochord import orchestra as O

ORDER = ["piccolo", "flute", "oboe", "clarinet", "saxophone", "bassoon", "trumpet", "horn", "trombone", "tuba",
         "violin", "viola", "cello", "double bass", "celesta", "harp"]
FAM = {"piccolo": TUNE, "flute": TUNE, "oboe": TUNE, "clarinet": TUNE, "saxophone": TUNE, "bassoon": TUNE,
       "trumpet": EAR, "horn": EAR, "trombone": EAR, "tuba": EAR, "violin": BLUE, "viola": BLUE, "cello": BLUE,
       "double bass": BLUE, "celesta": GREY_A, "harp": GREY_A}


class Ranges(SoundScene):
    def construct(self):
        chapter(self, 2, r"Ranges, \ registers and transposition", r"Where can each instrument play?")
        self.chart_()
        self.registers()
        self.hear_registers()
        self.transposing()
        self.why()

    # ------------------------------------------------------------------
    def chart_(self):
        lo, hi = 21, 108
        x0, W = -3.2, 9.4
        def X(m):
            return x0 + W * (m - lo) / (hi - lo)
        rows_ = VGroup()
        for i, name in enumerate(ORDER):
            a, b, _ = O.RANGES[name]
            y = 2.9 - 0.36 * i
            bar = Rectangle(width=X(b) - X(a), height=0.24, stroke_width=0, fill_color=FAM[name], fill_opacity=0.75).move_to([(X(a) + X(b)) / 2, y, 0])
            rows_.add(VGroup(label(name, font_size=15, color=FAM[name]).move_to([x0 - 0.2, y, 0], aligned_edge=RIGHT), bar))
        axis = VGroup()
        for m, n in ((24, "C1"), (36, "C2"), (48, "C3"), (60, "C4"), (72, "C5"), (84, "C6"), (96, "C7"), (108, "C8")):
            axis.add(VGroup(Line([X(m), -2.95, 0], [X(m), 3.1, 0], color=GREY_D, stroke_width=0.8), label(n, font_size=14, color=GREY_A).move_to([X(m), -3.2, 0])))
        head = label(r"sounding ranges \ (approximate)", font_size=24, color=GREY_A).to_edge(UP, buff=0.15)
        leg = VGroup(*[label(t, font_size=15, color=c) for t, c in ((r"woodwinds", TUNE), (r"brass", EAR), (r"strings", BLUE), (r"others", GREY_A))]).arrange(RIGHT, buff=0.5).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Here is the orchestra laid out by the notes it can sound, from the double bass's low E to the piccolo's top C, "
            "against the keys of the piano. <bookmark mark='a'/> Woodwinds in gold, brass in pink, strings in blue. "
            "<bookmark mark='b'/> Every range has a comfortable middle and difficult ends: the bottom of a flute is weak and "
            "breathy, the top of a trumpet strained, the top of a cello thin. An orchestrator writes in the middle unless "
            "the extreme is the point."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows_], lag_ratio=0.08), FadeIn(leg), run_time=3.0)
            vo.wait_until("b")
            self.play(Indicate(rows_[1]), Indicate(rows_[6]), Indicate(rows_[12]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def registers(self):
        items = [
            (r"an instrument's timbre changes across its range: \ its \textit{registers}", WHITE),
            (r"the clarinet: \ the dark low `chalumeau', \ a weak `throat' around B$\flat$4, \ the bright `clarion' above", WHITE),
            (r"the flute: \ breathy and soft at the bottom, \ brilliant and piercing at the top", WHITE),
            (r"Part 8's physics: \ a different set of bore modes takes over in each register", TUNE),
            (r"our additive orchestra uses one spectrum per instrument: \ it cannot show this", GREY_A),
        ]
        rows_scene(self, r"registers", items,
                   "Within its range, an instrument changes colour: it has registers. <bookmark mark='b'/> The clarinet has a "
                   "dark low register called the chalumeau, a weaker throat around B flat, and a bright clarion register above. "
                   "<bookmark mark='c'/> The flute is breathy and soft at the bottom and brilliant at the top. "
                   "<bookmark mark='d'/> The physics is Part 8's: a different set of the bore's modes takes over in each "
                   "register. <bookmark mark='e'/> Our additive orchestra uses one spectrum per instrument, so it cannot show this; "
                   "the physical models can.", marks="bcde")

    # ------------------------------------------------------------------
    def transposing(self):
        rows_ = VGroup()
        for name, shift, how in ((r"clarinet in B$\flat$", -2, r"written C sounds B$\flat$, \ a tone lower"),
                                 (r"horn in F", -7, r"written C sounds F, \ a fifth lower"),
                                 (r"trumpet in B$\flat$", -2, r"written C sounds B$\flat$, \ a tone lower"),
                                 (r"piccolo", 12, r"sounds an octave higher than written"),
                                 (r"double bass", -12, r"sounds an octave lower than written")):
            rows_.add(VGroup(label(name, font_size=21, color=TUNE), label(how, font_size=19, color=WHITE)).arrange(RIGHT, buff=0.6))
        rows_.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.1)
        cap = label(r"the part is written so the fingering is the same on every size of the instrument", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.8)
        head = label(r"transposing instruments", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Some instruments read one note and sound another. <bookmark mark='a'/> A clarinet in B flat, reading C, sounds "
            "the B flat a tone below. A horn in F, reading C, sounds the F a fifth below. The piccolo sounds an octave higher "
            "than written, the double bass an octave lower. <bookmark mark='b'/> Why? So that the same written note means the "
            "same fingering on every size of the instrument: a player can move from a B flat clarinet to an A clarinet, or "
            "from alto to tenor saxophone, without relearning. The score is written for the hands, not for the ear."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_.copy().set_opacity(0.2)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows_], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        items = [
            (r"natural horns and trumpets once played only one harmonic series: \ one crook per key", WHITE),
            (r"valves \ (from about 1815) \ made them chromatic; \ the transposed notation stayed", WHITE),
            (r"a modern score may be printed `in C', \ all parts at sounding pitch, \ for the conductor", WHITE),
            (r"history kept in notation: \ Part 10's lesson again", TUNE),
            (r"chapter 3: \ what happens when an instrument plays louder", GREY_A),
        ]
        rows_scene(self, r"why transpose?", items,
                   "There is history in this too. <bookmark mark='b'/> Natural horns and trumpets once played only the notes of "
                   "one harmonic series, Part 1's series, and players changed a length of tubing, a crook, for each key. "
                   "<bookmark mark='c'/> Valves, from about 1815, made them chromatic, but the transposed notation stayed. "
                   "<bookmark mark='d'/> A modern score may be printed in C, every part at sounding pitch, for the conductor. "
                   "<bookmark mark='e'/> History kept in notation, Part 10's lesson again. <bookmark mark='f'/> Chapter three "
                   "asks what happens when an instrument plays louder.", marks="cdef")

    # ------------------------------------------------------------------
    def hear_registers(self):
        d = load("registers")
        c = clip("registers.two")
        cells = VGroup(VGroup(label(r"register hole closed", font_size=22, color=TUNE), label(rf"the bore's lowest mode: \ {d['peak_hz']['low']:.0f} Hz", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.15),
                       VGroup(label(r"register hole open", font_size=22, color=EAR), label(rf"the next mode up: \ {d['peak_hz']['high']:.0f} Hz, \ a twelfth higher", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.15)).arrange(RIGHT, buff=1.5).move_to(UP * 0.3)
        cap = label(r"three times the frequency: \ a closed-open cylinder has only odd modes \ (Part 8)", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "The physical model shows a register change directly. Here is Part 8's clarinet, blown the same way twice, first "
            "with its register hole closed and then open. The small hole spoils the bore's lowest mode, so the reed locks onto "
            "the next one, three times the frequency: a twelfth higher, not an octave, because a cylinder closed at one end "
            "has only odd modes. A different register, and a different colour."
        ):
            self.play(FadeIn(cells), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"closed, \ then open", detail=r"Part 8's clarinet model", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], d["starts"]["low"], d["starts"]["high"] - 0.3, buff=0.1)
            pulse(snd, cells[1], d["starts"]["high"], c.duration, buff=0.1)
        self.wait(0.3)
        self.clear_scene()
