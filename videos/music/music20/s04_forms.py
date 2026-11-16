from __future__ import annotations

import numpy as np

from videos.music.music20.common import *  # noqa: F403

FORM_NAME = {"P": r"the line", "I": r"inversion: \ upside down", "R": r"retrograde: \ backwards", "RI": r"retrograde inversion: \ both"}


class Forms(SoundScene):
    def construct(self):
        chapter(self, 3, r"Four forms of a line", r"What can be done to a melody that keeps it the same melody?")
        self.quiz()
        self.four()
        self.real()
        self.group()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("forms")
        c = clip("forms.quiz")
        card = listen_card(r"The Tune's first phrase, \ then the same phrase changed. \ Is the second one upside down, \ or backwards?", width=9.6)
        with self.voiceover(
            "First, a question for your ears. You will hear the Tune's first phrase, and then the same phrase "
            "changed. Is the second one upside down, or backwards?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        g1 = voices_roll([d["forms"]["P"]], width=5.0, height=2.2, lo=62, hi=84).move_to(LEFT * 3.2 + DOWN * 0.2)
        q = label(r"?", font_size=80, color=GREY_B).move_to(RIGHT * 3.2 + DOWN * 0.2)
        self.play(FadeOut(card), FadeIn(g1), FadeIn(q))
        with self.listen(c) as snd:
            window(snd, r"the phrase, \ then a form of it", detail=r"a plucked string", corner=DL, tag_corner=DR)
            sing_voices(snd, g1, [d["forms"]["P"]], start=d["quiz_starts"]["P"])
            pulse(snd, q, d["quiz_starts"]["X"], c.duration, buff=0.1)
        g2 = voices_roll([d["forms"]["R"]], width=5.0, height=2.2, lo=62, hi=84, colors=(EAR,)).move_to(RIGHT * 3.2 + DOWN * 0.2)
        with self.voiceover(
            "Backwards. It begins on the phrase's last note, G, climbs to A, and falls by a fifth to end where the phrase "
            "began. The rhythm is backwards too: the long note is now first. Backwards melodies are surprisingly hard "
            "to recognize; upside-down ones, which keep the rhythm, are often easier."
        ):
            self.play(FadeOut(q), FadeIn(g2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def four(self):
        d = load("forms")
        c = clip("forms.four")
        cells = VGroup()
        for k, f in enumerate(("P", "I", "R", "RI")):
            g = voices_roll([d["forms"][f]], width=5.2, height=1.6, lo=62, hi=84, colors=(VOICE_C[k],))
            cells.add(VGroup(label(FORM_NAME[f], font_size=22, color=VOICE_C[k]), g).arrange(DOWN, buff=0.18))
        cells.arrange_in_grid(rows=2, cols=2, buff=(0.8, 0.5)).move_to(DOWN * 0.2)
        with self.voiceover(
            "There are four forms. The line itself. Its inversion, every rising interval made to fall by the same "
            "number of scale steps: the Tune's leap up a fifth becomes a leap down a fifth. Its retrograde, backwards. "
            "And its retrograde inversion, backwards and upside down. Hear all four."
        ):
            self.play(LaggedStart(*[FadeIn(x) for x in cells], lag_ratio=0.3), run_time=2.5)
        with self.listen(c) as snd:
            window(snd, r"the four forms", detail=r"a plucked string", corner=DL, tag_corner=DR)
            for k, f in enumerate(("P", "I", "R", "RI")):
                sing_voices(snd, cells[k][1], [d["forms"][f]], start=d["starts"][f], colors=(VOICE_C[k],))
                pulse(snd, cells[k][0], d["starts"][f], d["starts"][f] + 8 * BEAT, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def real(self):
        d = load("forms")
        g1 = voices_roll([d["forms"]["I"]], width=5.0, height=2.2, lo=60, hi=75, colors=(VOICE_C[1],)).move_to(LEFT * 3.3 + DOWN * 0.4)
        g2 = voices_roll([d["real_inversion"]], width=5.0, height=2.2, lo=60, hi=75, colors=(BLUE,)).move_to(RIGHT * 3.3 + DOWN * 0.4)
        t1 = VGroup(label(r"inverted in the scale", font_size=24, color=VOICE_C[1]), label(r"C C F F E E F", font_size=22, color=WHITE)).arrange(DOWN, buff=0.15).next_to(g1, UP, buff=0.3)
        t2 = VGroup(label(r"inverted exactly", font_size=24, color=BLUE), label(r"C C F F E$\flat$ E$\flat$ F", font_size=22, color=WHITE)).arrange(DOWN, buff=0.15).next_to(g2, UP, buff=0.3)
        cap = label(r"Bach inverts within the key; \ twelve-tone composers invert exactly", font_size=24, color=TUNE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "There are two ways to turn a line upside down. <bookmark mark='a'/> Within the scale, every step down "
            "becomes a step up of the same number of scale degrees: the Tune's rising fifth C to G becomes a falling "
            "fifth C to F, and its rising sixth to A becomes a falling sixth to E. <bookmark mark='b'/> Or exactly, "
            "semitone for semitone: then the falling major sixth from C lands on E flat, a note outside the key. "
            "<bookmark mark='c'/> Bach often adapts inversion to tonal context; real passages can use chromatic alterations; the twelve-tone composers "
            "of Part 29 invert exactly, and have no key to stay in."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(t1))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(g2), FadeIn(t2))
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def group(self):
        d = load("forms")
        forms = ["P", "I", "R", "RI"]
        cell = 0.85
        grid = VGroup()
        for i, f in enumerate(forms):
            for j, g in enumerate(forms):
                r = d["table"][f"{f} {g}"]
                sq = Square(side_length=cell - 0.05, stroke_width=1.5, stroke_color=GREY_B, fill_color=VOICE_C[forms.index(r)], fill_opacity=0.25)
                sq.move_to([(j - 1.5) * cell, (1.5 - i) * cell, 0])
                grid.add(VGroup(sq, label(r, font_size=24, color=WHITE).move_to(sq)))
        heads_top = VGroup(*[label(g, font_size=22, color=GREY_A).move_to([(j - 1.5) * cell, 2.3 * cell, 0]) for j, g in enumerate(forms)])
        heads_left = VGroup(*[label(f, font_size=22, color=GREY_A).move_to([-2.4 * cell, (1.5 - i) * cell, 0]) for i, f in enumerate(forms)])
        tab = VGroup(grid, heads_top, heads_left).move_to(LEFT * 3.2 + DOWN * 0.2)
        cap = label(r"row, \ then column: \ do the column's, \ then the row's", font_size=20, color=GREY_B).next_to(tab, DOWN, buff=0.3)
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"each form twice: \ identity (up to transposition here)", WHITE),
            (r"two different nonidentity operations: \ I then R is RI", WHITE),
            (r"order does not matter", WHITE),
            (r"a group: \ Klein's four-group, \ the symmetries of a rectangle", TUNE),
            (r"add the twelve transpositions: \ the forms of a twelve-tone row \ (Part 29)", GREY_A))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 6.4))
        rows_.move_to(RIGHT * 3.4 + DOWN * 0.1)
        with self.voiceover(
            "The four forms have an arithmetic. Do one and then another, and you always land on one of the four. <bookmark mark='a'/> Each form undoes itself: upside down twice is the right way up. <bookmark mark='b'/> Any two different nonidentity operations make the third: inverting a retrograde gives the retrograde inversion. <bookmark mark='c'/> And the order never matters. <bookmark mark='d'/> Mathematicians call such a set a group, and this one is a standard four-element noncyclic group, Klein's four-group, the symmetries of a rectangle: flip it across, flip it along, or turn it half round. The program checks the table on the Tune itself. <bookmark mark='e'/> With a fixed inversion convention, twelve transpositions give up to forty-eight labeled forms of a twelve-tone row, which Part 29 will need."
        ) as vo:
            self.play(FadeIn(tab), FadeIn(cap))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
