from __future__ import annotations

import numpy as np

from videos.music.music16.common import *  # noqa: F403


class Onsets(SoundScene):
    def construct(self):
        chapter(self, 4, r"Starting together", r"Can thirty milliseconds split one sound into two?", extra=((1978, r"Rasch's onset asynchrony"),))
        self.quiz()
        self.ladder()
        self.bach()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("onsets")
        c = clip("onsets.quiz")
        card = listen_card(r"An octave, \ twice. \ In one, \ the upper note starts a little late. \ In which do you hear two notes: \ A or B?", width=9.4)
        with self.voiceover("A third cue. Here is an octave, twice. In one of them, the upper note starts a little late. In which do you hear two notes: A or B?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        def pic(delay):
            ax = Line(LEFT * 2.2, RIGHT * 2.2, color=DIM, stroke_width=2)
            lo = RoundedRectangle(width=3.6, height=0.18, corner_radius=0.08, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to(UP * 0.5 + RIGHT * 0.1)
            hi = RoundedRectangle(width=3.6 - delay, height=0.18, corner_radius=0.08, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to(UP * 1.2 + RIGHT * (0.1 + delay / 2))
            return VGroup(ax, lo, hi)
        pA, pB = pic(0.0).move_to(LEFT * 3.2 + UP * 0.6), pic(0.35).move_to(RIGHT * 3.2 + UP * 0.6)
        la, lb = label(r"A", font_size=40, color=GREY_A).next_to(pA, UP, buff=0.2), label(r"B", font_size=40, color=GREY_A).next_to(pB, UP, buff=0.2)
        self.play(FadeOut(card), FadeIn(pA), FadeIn(pB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", kind="synthesized", detail=r"organ tones, \ an octave apart", corner=DL, tag_corner=DR)
            pulse(snd, pA, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.15)
            pulse(snd, pB, d["starts"]["B"], c.duration, buff=0.15)
        ans = VGroup(label(r"A: \ started together: \ one tone", font_size=26, color=GREY_A).next_to(pA, DOWN, buff=0.4),
                     label(rf"B: \ the upper note {d['delay_ms']} ms late: \ two tones, \ at least at first", font_size=26, color=TUNE).next_to(pB, DOWN, buff=0.4))
        with self.voiceover(
            f"B. The upper note came in thirty-five thousandths of a second late, far too short to "
            "hear as a rhythm, and yet it is enough for the ear to notice a second tone arriving. "
            "<bookmark mark='a'/> Rudolf Rasch measured this in 1978: an asynchrony of a few tens of "
            "milliseconds helps listeners pick out each of two simultaneous notes, and performers "
            "use it without knowing: in ensembles, the notes that are supposed to start together "
            "usually do not."
        ) as vo:
            self.play(FadeIn(ans))
            vo.wait_until("a")
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ladder(self):
        d = load("more")["ladder"]
        c = clip("more.ladder")
        head = label(r"how late must a note be, \ to be heard as a second note?", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        cells = VGroup()
        for ms in d["delays"]:
            off = 1.6 * ms / 60.0
            lo = RoundedRectangle(width=1.9, height=0.16, corner_radius=0.07, stroke_width=0, fill_color=WHITE, fill_opacity=1)
            hi = RoundedRectangle(width=1.9 - off * 0.5, height=0.16, corner_radius=0.07, stroke_width=0, fill_color=TUNE if ms else WHITE, fill_opacity=1)
            hi.move_to(lo.get_center() + UP * 0.55).align_to(lo, RIGHT)
            cells.add(VGroup(hi, lo, label(rf"{ms} ms", font_size=26, color=GREY_A).next_to(lo, DOWN, buff=0.35)))
        cells.arrange(RIGHT, buff=0.6).move_to(UP * 0.4)
        note = VGroup(label(r"I. Hirsh \ (1959): \ about 20 ms to tell which of two sounds came first", font_size=24, color=WHITE),
                      label(r"R. Rasch \ (1979): \ in ensembles, \ `together' means 30 to 50 ms apart", font_size=24, color=WHITE)).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "How small can the gap be? Here is the octave five times, with the upper note zero, ten, "
            "twenty, thirty-five and sixty thousandths of a second late. Listen for the moment it "
            "stops being one sound."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(x) for x in cells], lag_ratio=0.2), run_time=2.5)
        with self.listen(c) as snd:
            window(snd, r"0, \ 10, \ 20, \ 35, \ 60 ms", kind="synthesized", detail=r"organ tones, \ an octave apart", corner=DL, tag_corner=DR)
            st = d["starts"] + [c.duration]
            for k, cell in enumerate(cells):
                pulse(snd, cell, st[k], st[k + 1] - 0.4, buff=0.12)
        with self.voiceover(
            "At ten milliseconds most listeners hear one tone with a slightly different attack. Somewhere "
            "around twenty, a second note can be heard arriving. <bookmark mark='a'/> That is close to the "
            "figure Ira Hirsh measured in 1959 for telling which of two sounds came first. And it is "
            "smaller than the gaps musicians leave without meaning to: Rasch, recording trios and "
            "ensembles, found the notes that are written together typically thirty to fifty "
            "milliseconds apart. Ensemble playing is never perfectly together, and that is part of why "
            "the voices stay audible."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bach(self):
        d = load("onsets")["together_by_species"]
        ch = columns([100 * d[k] for k in "1234"], [r"first", r"second", r"third", r"fourth"], width=7.0, height=2.6, color=WEAK, hot=(3,), hot_color=TUNE, fmt="{:.0f}", font_size=24, top=100).move_to(LEFT * 2.4 + DOWN * 0.9)
        yl = label(r"notes that begin with a note of the other voice, \ in a hundred, \ by species", font_size=22, color=GREY_B).next_to(ch, DOWN, buff=0.15)
        text = VGroup(label(r"D. Huron \ (1993, \ 2008):", font_size=26, color=WHITE), label(r"in Bach, \ notes that would fuse", font_size=26, color=WHITE),
                      label(r"tend not to begin together", font_size=26, color=TUNE)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(RIGHT * 4.0 + UP * 0.2)
        head = label(r"onset synchrony, \ and the species", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "So three cues tell the ear that two notes belong to one source: they fuse, they move "
            "together, and they start together. Counterpoint can fight the third with rhythm. "
            "<bookmark mark='a'/> In first species every note of the new voice begins with a note of "
            "the cantus. In second species about half do; in third, a quarter; in fourth species, "
            "where the new voice is syncopated, almost none. <bookmark mark='b'/> Huron found the same "
            "strategy in Bach. Counting the onsets in his two-part Inventions, and later across "
            "polyphonic music generally, he found that the intervals that fuse most, octaves and "
            "fifths, are the ones most likely to be reached with the two notes starting at different "
            "times."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ch), FadeIn(yl))
            vo.wait_until("b")
            self.play(FadeIn(text))
        self.wait(0.4)
        self.clear_scene()
