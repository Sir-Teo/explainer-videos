from __future__ import annotations

import numpy as np

from videos.music.music53.common import *  # noqa: F403

NAMES = {0: "C-", 1: "C#", 2: "D-", 3: "D#", 4: "E-", 5: "F-", 6: "F#", 7: "G-", 8: "G#", 9: "A-", 10: "A#", 11: "B-"}


def tracker_text(cell):
    if cell is None:
        return "--- --"
    k, ins = cell
    if isinstance(k, str):
        return f"{k.upper():<3} 04"
    num = {"lead": "01", "bass": "02", "arp": "03"}.get(ins, "04")
    return f"{NAMES[k % 12]}{k // 12 - 1} {num}"


class Seq(SoundScene):
    def construct(self):
        chapter(self, 6, r"Sequencers: \ steps, \ rolls and trackers", r"How do you write music for a machine to play?")
        self.steps()
        self.heard()
        self.roll()
        self.tracker()
        self.daw()

    # ------------------------------------------------------------------
    def steps(self):
        d = load("steps")
        line = {s: (k, a, sl) for s, k, a, sl in d["line"]}
        cells = VGroup()
        for s in range(16):
            on = s in line
            k, a, sl = line.get(s, (None, 0, 0))
            box = Square(side_length=0.62, stroke_color=GREY_B, stroke_width=1.5, fill_color=EAR if a else TUNE, fill_opacity=0.75 if on else 0.0)
            txt = label(NAMES[k % 12].replace("-", "").replace("#", r"$\sharp$") if on else "", font_size=14, color=WHITE) if on else VGroup()
            sl_m = label(r"slide", font_size=11, color=BLUE).next_to(box, DOWN, buff=0.08) if sl else VGroup()
            cells.add(VGroup(box, txt.move_to(box) if on else txt, sl_m))
        cells.arrange(RIGHT, buff=0.08).move_to(UP * 0.6)
        notes = VGroup(label(r"sixteen steps a bar; \ each step: \ a note or a rest, \ an accent \ (pink), \ a slide into the next", font_size=18, color=WHITE),
                       label(r"the analogue sequencers of the 1960s had a knob per step; \ the 1981 TB-303 stored patterns like this one", font_size=18, color=GREY_A),
                       label(r"a step sequencer thinks in a grid, \ not in time: \ the loop repeats until you change it", font_size=18, color=TUNE)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.7)
        head = label(r"a step sequencer", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The simplest sequencer is a row of steps. <bookmark mark='a'/> Sixteen steps a bar; each holds a note or a rest, "
            "may be accented, and may slide into the next. <bookmark mark='b'/> The analogue sequencers of the 1960s had a knob "
            "per step; the bass machine of 1981 that defined acid house stored patterns exactly like this one. "
            "<bookmark mark='c'/> A step sequencer thinks in a grid, not in time: the loop repeats until you change it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(cells, 0.3)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.05), FadeIn(notes[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("steps")
        c = clip("steps.one")
        line = {s: (k, a, sl) for s, k, a, sl in d["line"]}
        cells = VGroup(*[Square(side_length=0.62, stroke_color=GREY_B, stroke_width=1.5, fill_color=EAR if line.get(s, (0, 0, 0))[1] else TUNE,
                                fill_opacity=0.75 if s in line else 0.0) for s in range(16)]).arrange(RIGHT, buff=0.08).move_to(UP * 0.4)
        cap = label(rf"{d['bpm']} beats a minute, \ four bars, \ a sawtooth through Part 51's ladder", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"the pattern, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear it, four bars, through Part 51's ladder: accents open the filter further; slides glide into the next note."):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        step = 60 / d["bpm"] / 4
        with self.listen(c) as snd:
            window(snd, r"sixteen steps", kind="synthesized", detail=r"sawtooth and ladder", corner=DL, tag_corner=DR)
            box = SurroundingRectangle(cells[0], color=WHITE, buff=0.04, stroke_width=3)
            snd.show(box)
            snd.drive(box, lambda m, t: m.move_to(cells[int(t / step) % 16].get_center()))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def roll(self):
        items = [
            (r"the piano roll: \ time across, \ pitch up, \ a bar for each note \ (Part 10, \ and the player piano)", WHITE),
            (r"draw, \ drag and stretch notes with a mouse; \ velocity as a lane beneath", WHITE),
            (r"quantize: \ pull every note to the nearest grid line; \ swing: \ pull every other one late \ (Part 38)", WHITE),
            (r"record a performance and edit it like a document", WHITE),
            (r"one idea from 1983 to now: \ notes as editable objects, \ not marks on paper", TUNE),
        ]
        rows_scene(self, r"the piano roll", items,
                   "Computers brought a second way. <bookmark mark='b'/> The piano roll: time across, pitch up, a bar for each note, "
                   "as Part 10 drew it and the player piano punched it. <bookmark mark='c'/> Notes are drawn, dragged and stretched "
                   "with a mouse, with velocity as a lane beneath. <bookmark mark='d'/> Quantizing pulls every note to the nearest "
                   "grid line; swing pulls every other one late, as Part 38 measured. <bookmark mark='e'/> A performance can be "
                   "recorded and edited like a document. <bookmark mark='f'/> The idea has held from 1983 to now: notes as editable "
                   "objects, not marks on paper.", marks="bcdef")

    # ------------------------------------------------------------------
    def tracker(self):
        d = load("tune53")
        rows = d["rows"][:16]
        lines = VGroup()
        for r, row in enumerate(rows):
            txt = f"{r:02X} | " + " | ".join(tracker_text(None if c is None else (c[0], c[1])) for c in row)
            lines.add(Text(txt, font="DejaVu Sans Mono", font_size=15, color=TUNE if r % 4 == 0 else GREY_A))
        lines.arrange(DOWN, buff=0.06, aligned_edge=LEFT).move_to(LEFT * 1.6 + DOWN * 0.3)
        hdr = Text("row | lead   | bass   | arp    | drum", font="DejaVu Sans Mono", font_size=15, color=WHITE).next_to(lines, UP, buff=0.15).align_to(lines, LEFT)
        side = VGroup(label(r"1987: \ Karsten Obarski's Soundtracker, \ for the Amiga's four sample channels", font_size=16, color=WHITE),
                      label(r"time runs down the screen, \ one row at a time", font_size=16, color=GREY_A),
                      label(r"each cell: \ a note, \ an instrument number, \ and an effect, \ typed in hexadecimal", font_size=16, color=GREY_A),
                      label(r"the demoscene and game music lived in trackers", font_size=16, color=TUNE)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(RIGHT, buff=0.3)
        side.set_width(min(side.width, 4.4))
        head = label(r"the tracker: \ the Tune's first phrase", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "A third way came from home computers. <bookmark mark='a'/> In 1987 Karsten Obarski's Soundtracker, for the Amiga's "
            "four sample channels, turned the score on its side: time runs down the screen, one row at a time, and each "
            "column is a channel. <bookmark mark='b'/> Each cell holds a note, an instrument number and an effect, typed in "
            "hexadecimal by people who were also programmers. Here is the Tune's first phrase as Variation 53 will play it. "
            "The demoscene and a generation of game music lived in trackers, Part 44's chip music among them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr), FadeIn(ghost(lines, 0.3)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in lines], lag_ratio=0.05), FadeIn(side[:2]), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(side[2:]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def daw(self):
        items = [
            (r"the digital audio workstation joins them: \ tracks of audio and of MIDI, \ side by side on one timeline", WHITE),
            (r"mixing, \ effects and synthesizers inside, \ all as software", WHITE),
            (r"some arrange clips in a grid to be launched live, \ the step sequencer's loop come back", WHITE),
            (r"under every one of them: \ an engine computing audio in blocks, \ against a clock", TUNE),
            (r"before the engine, \ one more way to write: \ as text", GREY_A),
        ]
        rows_scene(self, r"the workstation", items,
                   "Today one program holds all of these. <bookmark mark='b'/> The digital audio workstation lays tracks of audio and "
                   "of MIDI side by side on one timeline, <bookmark mark='c'/> with mixing, effects and synthesizers inside, all as "
                   "software. <bookmark mark='d'/> Some arrange clips in a grid to be launched live, the step sequencer's loop come "
                   "back. <bookmark mark='e'/> Under every one of them is an engine computing audio in blocks, against a clock. "
                   "<bookmark mark='f'/> Before the engine, one more way to write: as text.", marks="bcdef")
