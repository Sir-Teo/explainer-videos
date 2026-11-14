from __future__ import annotations

import numpy as np

from videos.music.music13.common import *  # noqa: F403


class ScaleChords(SoundScene):
    def construct(self):
        chapter(self, 3, r"The chords of a scale", r"Which chords does a scale contain?")
        self.seven()
        self.numerals()
        self.primary()

    # ------------------------------------------------------------------
    def seven(self):
        d = load("scale")
        c = clip("scale.triads")
        rows = d["rows"]
        row = chord_row([r["names"] for r in rows] + [["C5", "E5", "G5"]], width=11.5, space=0.24, above=[r["symbol"] for r in rows] + ["C"],
                        below=[r["roman"] for r in rows] + ["I"], font_size=30, below_color=WHITE).move_to(UP * 0.7)
        for k, r in enumerate(rows + [rows[0]]):
            row.notes[k].ink.set_color(KIND_COLOR[r["kind"]])
            row.above[k].set_color(KIND_COLOR[r["kind"]])
        tally = VGroup(label(r"3 major", font_size=32, color=MAJOR_C), label(r"3 minor", font_size=32, color=MINOR_C), label(r"1 diminished", font_size=32, color=DIM_C)).arrange(RIGHT, buff=1.0).to_edge(DOWN, buff=1.3)
        with self.voiceover(
            "Take the C major scale, and build a triad on each of its notes, using only notes of the "
            "scale: every other one, three at a time. <bookmark mark='a'/> You do not get seven chords "
            "of one kind. On C, on F and on G, the triad is major. <bookmark mark='b'/> On D, on E and "
            "on A, it is minor. <bookmark mark='c'/> And on B it is diminished: the one place where the "
            "scale's tritone lands between the root and the fifth. Three, three and one. Listen up the "
            "scale."
        ) as vo:
            self.play(FadeIn(row.staff), FadeIn(row.above), run_time=1.5)
            vo.wait_until("a")
            self.play(*[Indicate(row.notes[k], color=MAJOR_C, scale_factor=1.15) for k in (0, 3, 4)], FadeIn(tally[0]))
            vo.wait_until("b")
            self.play(*[Indicate(row.notes[k], color=MINOR_C, scale_factor=1.15) for k in (1, 2, 5)], FadeIn(tally[1]))
            vo.wait_until("c")
            self.play(Indicate(row.notes[6], color=DIM_C, scale_factor=1.15), FadeIn(tally[2]))
        with self.listen(c) as snd:
            window(snd, r"a triad on every degree", detail=r"C major: \ Part 7's piano", corner=DL, tag_corner=DR)
            for k in range(8):
                pulse(snd, row.above[k], d["times"][k], d["times"][k + 1] if k < 7 else c.duration, buff=0.1)
        self.row, self.tally = row, tally

    # ------------------------------------------------------------------
    def numerals(self):
        row, tally = self.row, self.tally
        keysrow = VGroup(label(r"in C: \ V is G", font_size=30, color=GREY_A), label(r"in E$\flat$: \ V is B$\flat$", font_size=30, color=GREY_A), label(r"in A: \ V is E", font_size=30, color=GREY_A)).arrange(RIGHT, buff=1.0).to_edge(DOWN, buff=1.3)
        with self.voiceover(
            "Musicians number these chords by the degree of the scale they stand on, in Roman numerals. "
            "<bookmark mark='a'/> Capitals for major, small letters for minor, a little circle for "
            "diminished. One, two, three, four, five, six, seven. <bookmark mark='b'/> The numerals are "
            "worth learning because they do not depend on the key. In C major, five is a G chord. In E "
            "flat major, five is B flat. In A major it is E. The letter changes; the job the chord does "
            "in the key is the same, and it is the job that you hear."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in row.below], lag_ratio=0.25), run_time=3.5)
            vo.wait_until("b")
            self.play(FadeOut(tally), FadeIn(keysrow), Indicate(row.below[4], color=TUNE, scale_factor=1.4))
        self.wait(0.4)
        self.play(FadeOut(keysrow))

    # ------------------------------------------------------------------
    def primary(self):
        d = load("scale")
        c = clip("scale.primary")
        row = self.row
        cover = VGroup(*[label(x, font_size=34, color=TUNE) for x in "CDEFGAB"]).arrange(RIGHT, buff=0.5)
        cap = label(r"I, \ IV and V between them hold every note of the scale", font_size=28, color=GREY_A)
        g = VGroup(cover, cap).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Three of the seven matter most. One, four and five are the three major triads, "
            "<bookmark mark='a'/> and between them they contain every note of the scale. C, E, G; F, A, "
            "C; G, B, D. So any melody in a major key can be accompanied with just these three chords, "
            "and a great many songs are. Here they are in order: one, four, five, and one again."
        ) as vo:
            self.play(*[row.notes[k].animate.set_opacity(0.25) for k in (1, 2, 5, 6)], *[row.above[k].animate.set_opacity(0.25) for k in (1, 2, 5, 6)],
                      *[row.below[k].animate.set_opacity(0.25) for k in (1, 2, 5, 6)])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in cover], lag_ratio=0.15), FadeIn(cap), run_time=2.0)
        order = [0, 3, 4, 7]
        with self.listen(c) as snd:
            window(snd, r"I, \ IV, \ V, \ I", detail=r"with a bass note under each", corner=DL, tag_corner=DR)
            for j, k in enumerate(order):
                pulse(snd, VGroup(row.above[k], row.below[k], row.notes[k]), d["primary_times"][j], d["primary_times"][j + 1] if j < 3 else c.duration, buff=0.12)
        with self.voiceover(
            "Home, away, further away, and home. You have heard that journey ten thousand times. Why "
            "five pulls back to one is the subject of Part 15; the reason is already on the screen, and "
            "chapter 6 will find it."
        ):
            self.play(Indicate(row.below[4], color=TUNE, scale_factor=1.4), Indicate(row.below[7], color=TUNE, scale_factor=1.4))
        self.wait(0.4)
        self.clear_scene()
