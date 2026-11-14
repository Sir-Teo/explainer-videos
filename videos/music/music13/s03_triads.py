from __future__ import annotations

import numpy as np

from videos.music.music13.common import *  # noqa: F403


class Triads(SoundScene):
    def construct(self):
        chapter(self, 2, r"Three notes", r"Why are chords built in thirds?", extra=((1558, r"Zarlino's \textit{Istitutioni}"),))
        self.build()
        self.zarlino()
        self.census()
        self.quiz()

    # ------------------------------------------------------------------
    def build(self):
        d = load("triads")
        c = clip("triads.four")
        kinds = d["kinds"]
        row = chord_row([k["names"] for k in kinds], width=9.0, space=0.24, above=[k["kind"] for k in kinds],
                        below=[rf"{k['thirds'][0]} + {k['thirds'][1]}" for k in kinds], font_size=26).move_to(UP * 0.9)
        note = label(r"semitones in the lower third + the upper third", font_size=22, color=GREY_B).next_to(row, DOWN, buff=0.3)
        with self.voiceover(
            "A chord is three or more notes sounded together, and the simplest chords are triads: a "
            "note, the third above it, and the fifth above it. Every other note of a scale. "
            "<bookmark mark='a'/> There are two sizes of third, so there are four ways to stack two of "
            "them. A major third with a minor third on top: a major triad. <bookmark mark='b'/> Minor "
            "then major: a minor triad. <bookmark mark='c'/> Two minor thirds: diminished. "
            "<bookmark mark='d'/> Two major thirds: augmented. Listen to the four, each a note at a "
            "time and then together."
        ) as vo:
            kb = keys(60, 72, width=5.0, height=1.3, lit=(60, 64, 67)).to_edge(DOWN, buff=0.9)
            lead = label(r"a note, \ its third, \ its fifth", font_size=30, color=GREY_A).next_to(kb, UP, buff=0.25)
            self.play(FadeIn(row.staff.systems[0].lines), FadeIn(row.staff.systems[0].clef), FadeIn(row.staff.barlines), FadeIn(row.notes[0]), FadeIn(kb), FadeIn(lead))
            for k, mark in enumerate("abcd"):
                vo.wait_until(mark)
                row.above[k].set_color(KIND_COLOR[kinds[k]["kind"]])
                if k == 0:
                    self.play(FadeOut(kb), FadeOut(lead), row.notes[0].ink.animate.set_color(KIND_COLOR["major"]), FadeIn(row.above[0]), FadeIn(row.below[0]), run_time=0.6)
                    continue
                row.notes[k].ink.set_color(KIND_COLOR[kinds[k]["kind"]])
                self.play(FadeIn(row.notes[k]), FadeIn(row.above[k]), FadeIn(row.below[k]), run_time=0.6)
            self.play(FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"the four triads", detail=r"on middle C: \ Part 7's piano", corner=DL, tag_corner=DR)
            for k in range(4):
                pulse(snd, row.above[k], d["times"][k], (d["times"][k + 1] - 0.2) if k < 3 else c.duration, buff=0.12)
        facts = VGroup(label(r"major and minor: \ the same three intervals, \ in a different order", font_size=28, color=WHITE),
                       label(r"diminished: \ its outer interval is the tritone", font_size=28, color=DIM_C),
                       label(r"augmented: \ three equal steps of the octave; \ no landmark", font_size=28, color=AUG_C)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Major and minor contain the same three intervals: a major third, a minor third and a "
            "perfect fifth. Only the order differs. <bookmark mark='a'/> The diminished triad has no "
            "perfect fifth: its outer interval is the tritone. <bookmark mark='b'/> The augmented triad "
            "has none either, and it cuts the octave into three equal parts; so, like the whole-tone "
            "scale of Part 12, it has no landmark, and no way to tell which of its notes is the bottom."
        ) as vo:
            self.play(FadeOut(note), FadeIn(facts[0]))
            vo.wait_until("a")
            self.play(FadeIn(facts[1]))
            vo.wait_until("b")
            self.play(FadeIn(facts[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def zarlino(self):
        d = load("triads")
        card = history_card(1558, r"Gioseffo Zarlino, \ Venice", r"the major triad is the numbers 4, \ 5, \ 6; \ the minor triad is the same two thirds, \ the other way up", width=10.5, font_size=26).to_edge(UP, buff=0.4)
        f0 = 65.41
        rows = partial_rows([f0], [r"C"], n=16, width=12.0, f_lo=58.0, f_hi=1120.0, row=0.5, colors=(GREY_B,), tick=0.4, font_size=30).move_to(DOWN * 0.5)
        ticks = rows.rows[0].ticks
        nums = VGroup(*[label(str(h + 1), font_size=22 if h < 9 else 17, color=GREY_B).next_to(ticks[h], UP, buff=0.12) for h in range(16)])
        major = VGroup(*[label(t, font_size=30, color=MAJOR_C).next_to(ticks[h], DOWN, buff=0.2) for h, t in ((3, "C"), (4, "E"), (5, "G"))])
        minor = VGroup(*[label(t, font_size=26, color=MINOR_C).next_to(ticks[h], DOWN, buff=0.2) for h, t in ((9, "E"), (11, "G"), (14, "B"))])
        hl = label(r"the harmonics of one low C", font_size=24, color=GREY_B).next_to(rows, UP, buff=0.75)
        rows.add(hl)
        cap = VGroup(label(r"$4 : 5 : 6$ \ \ a major triad", font_size=30, color=MAJOR_C), label(r"$10 : 12 : 15$ \ \ a minor triad", font_size=30, color=MINOR_C)).arrange(RIGHT, buff=1.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Where does the major triad come from? In 1558 Gioseffo Zarlino, in Venice, gave an answer "
            "in numbers. Take frequencies in the proportion four to five to six. <bookmark mark='a'/> "
            "Four to five is the pure major third of Part 6, and four to six the pure fifth. So a major "
            "triad is the fourth, fifth and sixth harmonics of one note: the harmonic series of Part 1, "
            "sounded by three strings instead of one. <bookmark mark='b'/> The minor triad has the same "
            "two thirds the other way up, and the smallest numbers that fit it are ten, twelve and "
            "fifteen: much higher in the series, and over a different fundamental. Keep that asymmetry "
            "in mind. It comes back in chapter 5."
        ) as vo:
            self.play(FadeIn(card))
            self.play(FadeIn(rows), FadeIn(nums))
            vo.wait_until("a")
            self.play(*[ticks[h].animate.set_color(MAJOR_C) for h in (3, 4, 5)], FadeIn(major), FadeIn(cap[0]))
            vo.wait_until("b")
            self.play(*[ticks[h].animate.set_color(MINOR_C) for h in (9, 11, 14)], FadeIn(minor), FadeIn(cap[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def census(self):
        d = load("triads")
        shapes = d["shapes"]
        clocks = VGroup()
        for s in shapes:
            col = WEAK
            if not s["step"]:
                col = {"major triad": MAJOR_C, "minor triad": MINOR_C, "diminished triad": DIM_C, "augmented triad": AUG_C}[s["name"]]
            clocks.add(twelve(s["pcs"], radius=0.42, color=col, names=False, dot=0.05))
        clocks.arrange_in_grid(rows=3, cols=7, buff=(0.42, 0.45)).move_to(UP * 0.5)
        head = label(rf"every shape of three notes on twelve: \ {d['count']}", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
        keep = [k for k, s in enumerate(shapes) if not s["step"]]
        names = VGroup(*[label(shapes[k]["name"].replace(" triad", ""), font_size=20, color=clocks[k].poly.get_stroke_color()).next_to(clocks[k], DOWN, buff=0.1) for k in keep])
        with self.voiceover(
            "But why thirds? Why not stack seconds, or fourths? Part 12 counted every shape that three "
            f"notes can make on twelve. There are {say(d['count'])}. <bookmark mark='a'/> Now strike out "
            "every shape in which two of the notes are neighbours, a semitone or a whole tone apart, "
            "because neighbours fall inside one critical band, and grate. <bookmark mark='b'/> Four "
            "shapes survive. They are exactly the four triads."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(x) for x in clocks], lag_ratio=0.05), run_time=2.5)
            vo.wait_until("a")
            self.play(*[clocks[k].animate.set_opacity(0.15) for k in range(len(shapes)) if k not in keep], run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(names))
        moral = VGroup(label(r"three notes, \ no two of them neighbours: \ that is a stack of thirds.", font_size=30, color=TUNE),
                       label(r"no tritone either: \ major, \ minor and augmented remain.", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.55)
        dim_k = next(k for k in keep if shapes[k]["name"] == "diminished triad")
        with self.voiceover(
            "So a stack of thirds is not a convention. It is what is left when you ask for three notes, "
            "no two of them adjacent. <bookmark mark='a'/> Ask for no tritone either, and three remain: "
            "major, minor and augmented. And of those, only two contain a perfect fifth. The whole of "
            "common harmony rests on the two shapes that pass every test."
        ) as vo:
            self.play(FadeIn(moral[0]))
            vo.wait_until("a")
            self.play(clocks[dim_k].animate.set_opacity(0.3), names[keep.index(dim_k)].animate.set_opacity(0.4), FadeIn(moral[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        c = clip("triads.quiz")
        ev = c.events
        card = listen_card(r"Two triads on the same note. \ Which is major: \ A or B?", width=8.6)
        with self.voiceover("Try your ear. Two triads on the same note. Which is the major one: A or B?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        bx = boxes(("A", "B"), buff=1.2, width=2.4, height=1.2, font_size=48).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"two triads on D", corner=DL, tag_corner=DR)
            pulse(snd, bx[0], ev["A"], ev["B"] - 0.4)
            pulse(snd, bx[1], ev["B"], c.duration)
        ans = VGroup(label(r"A: \ D, \ F, \ A: \ minor", font_size=28, color=MINOR_C), label(r"B: \ D, \ F$\sharp$, \ A: \ major", font_size=28, color=MAJOR_C)).arrange(DOWN, buff=0.3).move_to(DOWN * 1.5)
        with self.voiceover(
            "B. The only difference is the middle note: F in the first, F sharp in the second. One "
            "semitone, in one voice, and the whole character of the chord changes."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()
