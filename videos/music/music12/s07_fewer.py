from __future__ import annotations

import numpy as np

from videos.music.music12.common import *  # noqa: F403

TITLES = {"pentatonic": r"pentatonic", "whole-tone": r"whole-tone", "octatonic": r"octatonic", "blues": r"blues"}
COLS = {"pentatonic": SHORT, "whole-tone": TUNE, "octatonic": "#C4B5FD", "blues": "#FCA5A5"}


class Fewer(SoundScene):
    def construct(self):
        chapter(self, 6, r"Fewer notes, \ and more", r"What do scales of five, \ six and eight notes do?")
        self.four()
        self.limited()
        self.walks()

    # ------------------------------------------------------------------
    def four(self):
        d = load("fewer")
        c = clip("fewer.four")
        cols = VGroup()
        for k in d["kinds"]:
            cl = twelve(d["notes"][k][:-1], radius=1.05, color=COLS[k], font_size=15, dot=0.08)
            steps = label(r" ".join(str(s) for s in d["steps"][k]), font_size=24, color=GREY_A)
            cols.add(VGroup(label(TITLES[k], font_size=30, color=COLS[k]), cl, steps).arrange(DOWN, buff=0.35))
        cols.arrange(RIGHT, buff=0.55).move_to(UP * 0.4)
        with self.voiceover(
            "Seven is not the only number. <bookmark mark='a'/> Five notes: the pentatonic scale, the "
            "first stop of the stack of fifths. It has no semitones at all, so no two of its notes clash, "
            "and it turns up in the folk music of every inhabited continent. <bookmark mark='b'/> Six "
            "equal steps: the whole-tone scale. <bookmark mark='c'/> Eight notes, in alternating whole "
            "and half steps: the octatonic scale. <bookmark mark='d'/> And the blues scale: a minor "
            "pentatonic with one note added in the crack between two others. Listen to the four."
        ) as vo:
            lead = label(r"seven is not the only number", font_size=34, color=GREY_A).to_edge(DOWN, buff=0.8)
            self.add(lead)
            for mark, col in zip("abcd", cols):
                vo.wait_until(mark)
                self.play(FadeIn(col), run_time=0.6)
            self.play(FadeOut(lead))
        with self.listen(c) as snd:
            window(snd, r"pentatonic, \ whole-tone, \ octatonic, \ blues", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for k, col in zip(d["kinds"], cols):
                t0 = d["starts"][d["kinds"].index(k)]
                n = len(d["notes"][k])
                pulse(snd, col[0], t0, t0 + 0.3 * (n + 1), buff=0.1)
                flash(snd, [col[1].dots[x % 12] for x in d["notes"][k]], [t0 + 0.3 * j for j in range(n)], base=COLS[k], hot=WHITE, fade=0.2)
        self.wait(0.2)
        self.cols = cols

    # ------------------------------------------------------------------
    def limited(self):
        d = load("fewer")
        cols = self.cols
        t = d["transpositions"]
        counts = VGroup(*[label(rf"{t[k]} versions", font_size=28, color=BAD if t[k] < 12 else GREY_A).next_to(col, DOWN, buff=0.3) for k, col in zip(d["kinds"], cols)])
        facts = VGroup(label(r"whole-tone: \ no semitones, \ no fifths, \ no home", font_size=26, color=TUNE),
                       label(r"octatonic: \ every interval, \ but the same from four of its notes", font_size=26, color=COLS["octatonic"])).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Two of these are strange in a way you can count. Move the major scale up a semitone at a "
            "time and you get twelve different sets of notes before it comes home. <bookmark mark='a'/> "
            "The pentatonic and the blues scales have twelve versions too. But the whole-tone scale has "
            "only two: move it up a whole tone and every note lands on another note of the scale. The "
            "octatonic has only three. Olivier Messiaen, who built much of his music from such scales, "
            "called them modes of limited transposition. <bookmark mark='b'/> A scale that maps onto "
            "itself has no landmarks, and so no note that sounds like home. The whole-tone scale has no "
            "fifths either. Composers reach for these scales when they want music to float, or to "
            "threaten, without arriving anywhere."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in counts], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(facts))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def walks(self):
        d = load("fewer")
        c = clip("fewer.walks")
        names = [("five", r"on five notes: \ pentatonic", SHORT), ("seven", r"on seven: \ major", TUNE), ("twelve", r"on all twelve", GREY_A)]
        cols = VGroup()
        for key, text, col in names:
            notes = d["walk_notes"][key]
            xs = np.linspace(-1.6, 1.6, len(notes))
            pts = [np.array([x, 0.11 * n + 0.7, 0]) for x, n in zip(xs, notes)]
            path = VMobject(color=col, stroke_width=2.5).set_points_as_corners(pts)
            dots = VGroup(*[Dot(p, radius=0.06, color=col) for p in pts])
            cols.add(VGroup(label(text, font_size=28, color=col), VGroup(path, dots)).arrange(DOWN, buff=0.4))
        cols.arrange(RIGHT, buff=0.9).move_to(UP * 0.3)
        note = listen_note(r"one random walk, \ played on three scales. \ The moves are the same; \ only the notes allowed are different", width=10.0, font_size=26).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is a small experiment on what the number of notes does. Monochord throws dice to make "
            "a wandering line: up one step, down two, and so on, thirteen moves. Then it plays that same "
            "line three times, on a scale of five notes, of seven, and on all twelve. The throws of the "
            "dice are identical. Only the notes allowed are different."
        ):
            self.play(FadeIn(cols), FadeIn(note))
        self.play(FadeOut(note))
        with self.listen(c) as snd:
            window(snd, r"one walk, \ three scales", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for k, col in enumerate(cols):
                t0 = d["walk_starts"][k]
                pulse(snd, col[0], t0, t0 + 0.26 * 15, buff=0.1)
                flash(snd, list(col[1][1]), [t0 + 0.26 * j for j in range(14)], base=names[k][2], hot=WHITE, fade=0.2)
        with self.voiceover(
            "Most people hear the first as nearly a tune, the second as a tune with a few odd corners, "
            "and the third as wandering. Nobody composed any of them. With five notes and no semitones, "
            "almost anything you do sounds acceptable; that is why beginners are given pentatonic "
            "instruments, and why so many folk melodies are pentatonic. With twelve, nothing is ruled "
            "out, so nothing is implied. A scale is a set of constraints, and the constraints do a good "
            "deal of the composing."
        ):
            self.play(Indicate(cols[0][0], color=WHITE))
        self.wait(0.4)
        self.clear_scene()
