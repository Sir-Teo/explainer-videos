from __future__ import annotations

import numpy as np

from videos.music.music32.common import *  # noqa: F403


class Optic(SoundScene):
    def construct(self):
        chapter(self, 7, r"Five symmetries", r"What exactly is `a chord'?", extra=((2008, r"`Generalized voice-leading spaces'"),))
        self.letters()
        self.mirror()
        self.table()
        self.names()

    # ------------------------------------------------------------------
    def letters(self):
        rows_ = text_rows([
            (r"O, \ octave: \ C4 and C5 count as the same note", WHITE),
            (r"P, \ permutation: \ which voice plays which note does not matter", WHITE),
            (r"T, \ transposition: \ C major and D major count as the same kind of chord", WHITE),
            (r"I, \ inversion: \ a chord and its upside-down image count as the same \ (major and minor!)", TUNE),
            (r"C, \ cardinality: \ doubling a note does not change the chord", WHITE),
        ], font_size=24)
        head = label(r"OPTIC: \ five ways to call two things the same", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Callender, Quinn and Tymoczko noticed that the objects of music theory differ only in which things they call "
            "the same. There are five symmetries. <bookmark mark='a'/> O, the octave: C4 and C5 count as one note. "
            "<bookmark mark='b'/> P, permutation: it does not matter which voice plays which note. <bookmark mark='c'/> T, "
            "transposition: C major and D major are the same kind of chord. <bookmark mark='d'/> I, inversion: a chord and "
            "its mirror image count as one, which makes major and minor the same. <bookmark mark='e'/> And C, cardinality: "
            "doubling a note does not change the chord. Each choice of letters gives a space, and a different object of music "
            "theory."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        d = load("optic")
        keys = ["OP", "OPC", "OPT", "OPTC", "OPTI", "OPTIC"]
        what = [r"chords, \ voices forgotten", r"pitch-class sets", r"chord types", r"chord types, \ doubling ignored", r"set classes, \ with doublings", r"set classes \ (Part 29)"]
        hdr = VGroup(label(r"symmetries", font_size=21, color=GREY_A), label(r"what music calls it", font_size=21, color=GREY_A),
                     label(r"3 notes", font_size=21, color=GREY_A), label(r"4 notes", font_size=21, color=GREY_A))
        rows_ = [hdr]
        for k, w in zip(keys, what):
            rows_.append(VGroup(label(k, font_size=22, color=TUNE), label(w, font_size=20, color=WHITE),
                                label(f"{d['3'][k]:,}", font_size=21, color=WHITE), label(f"{d['4'][k]:,}", font_size=21, color=WHITE)))
        xs = [-4.6, -1.0, 2.8, 4.8]
        tbl = VGroup()
        for i, r in enumerate(rows_):
            for j, cell in enumerate(r):
                cell.move_to([xs[j], 2.0 - 0.62 * i, 0])
            tbl.add(r)
        head = label(r"how many chords of three and four notes \ (twelve-note equal temperament), \ by brute force", font_size=23, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(rf"with O and P alone: \ {d['3']['OP']} three-note chords; \ with all five: \ {d['3']['OPTIC']}", font_size=22, color=EAR).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A program can count the chords in each space by brute force: list every chord of three or four pitch classes, "
            "doublings allowed, and group together those the symmetries make equal. <bookmark mark='a'/> With octave and "
            f"permutation only, there are {say(d['3']['OP'])} three-note chords. Add cardinality, so doublings vanish, and "
            f"{say(d['3']['OPC'])} remain: the pitch-class sets of size one to three. <bookmark mark='b'/> Add transposition "
            f"and there are {say(d['3']['OPT'])} chord types. <bookmark mark='c'/> Add inversion as well and there are "
            f"{say(d['3']['OPTIC'])}: Part 29's set classes of one, two and three notes. Each row of this table is a "
            "different space, with its own geometry."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tbl[0]), FadeIn(tbl[1]))
            vo.wait_until("a")
            self.play(FadeIn(tbl[2]))
            vo.wait_until("b")
            self.play(FadeIn(tbl[3]), FadeIn(tbl[4]))
            vo.wait_until("c")
            self.play(FadeIn(tbl[5]), FadeIn(tbl[6]), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def names(self):
        items = [
            (r"OP: \ `C major triad', \ in any voicing", WHITE),
            (r"OPT: \ `major triad', \ in any key", WHITE),
            (r"OPTI: \ `consonant triad', \ major or minor: \ Riemann's dualism \ (Part 31)", WHITE),
            (r"OPTIC: \ the set class of Part 29, \ the atonal theorist's object", TUNE),
            (r"each space has its own shape: \ the more symmetries, \ the more folded the space", GREY_A),
        ]
        rows_scene(self, r"one family, \ many theories", items,
                   "The letters line up with ordinary words. <bookmark mark='b'/> O and P: a C major triad, in any voicing. "
                   "<bookmark mark='c'/> Add T: a major triad, in any key. <bookmark mark='d'/> Add I: a consonant triad, major or "
                   "minor, the way Riemann's dualism of Part 31 thought of them. <bookmark mark='e'/> All five: the set class of "
                   "Part 29. <bookmark mark='f'/> Each is a quotient space of the same plane, and the more symmetries, the more "
                   "the space is folded.", marks="cdef")

    # ------------------------------------------------------------------
    def mirror(self):
        d = load("mirror")
        c = clip("mirror.two")
        g = mroll(d["notes"], width=10.0, height=2.2, lo=50, hi=70, color=GREY_A, bar_h=0.13).move_to(DOWN * 0.4)
        axis = DashedLine(g.frame.get_left() + UP * (g.frame.height * (60 - 50) / 20 - g.frame.height / 2), g.frame.get_right() + UP * (g.frame.height * (60 - 50) / 20 - g.frame.height / 2), color=EAR, stroke_width=2)
        tags = VGroup(label(r"up from C: \ 4, \ then 3 semitones: \ C major", font_size=22, color=TUNE),
                      label(r"down from C: \ 4, \ then 3: \ F minor", font_size=22, color=BLUE)).arrange(RIGHT, buff=2.4).move_to(UP * 1.6)
        head = label(r"I, \ inversion: \ a chord and its mirror image", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Inversion is the one symmetry the ear may not grant. Build a chord up from C, four semitones and then three: C "
            "major. Now build its mirror image down from C, four semitones and then three: C, A flat, F, which is F minor. "
            "With I among the symmetries, the two are the same object. Listen, and judge whether they sound like the same "
            "kind of thing."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(axis), FadeIn(tags))
        with self.listen(c) as snd:
            window(snd, r"C major, \ then its mirror", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, g.notes, [n[1] * d["unit"] for n in d["notes"]], hot=WHITE, base=GREY_A)
            pulse(snd, tags[0], 0.0, 4 * d["unit"], buff=0.08)
            pulse(snd, tags[1], 4 * d["unit"], c.duration, buff=0.08)
        with self.voiceover(
            "Most listeners hear major and minor as different in mood, one bright and one dark, though alike in stability. So "
            "a theory of tonal harmony usually leaves I out, and a theory of atonal sets, like Part 29's, puts it in. The "
            "letters are a choice about what to ignore."
        ):
            self.wait(0.5)
        self.wait(0.4)
        self.clear_scene()
