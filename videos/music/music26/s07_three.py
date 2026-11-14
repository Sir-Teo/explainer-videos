from __future__ import annotations

import numpy as np

from videos.music.music26.common import *  # noqa: F403


class Three(SoundScene):
    def construct(self):
        chapter(self, 6, r"Haydn, \ Mozart, \ Beethoven", r"What did each do with the same language?", extra=((1806, r"Beethoven's `Razumovsky' quartets"),))
        self.careers()
        self.measured()
        self.quiz()

    # ------------------------------------------------------------------
    def careers(self):
        items = [
            (r"Haydn, \ 1732--1809: \ thirty years in the Esterházy household, \ then fame in London", WHITE),
            (r"economy: \ whole movements from one idea; \ wit; \ surprise", WHITE),
            (r"Mozart, \ 1756--1791: \ prodigy, \ freelance in Vienna, \ the opera ensembles of \textit{Figaro} and \textit{Don Giovanni}", WHITE),
            (r"Beethoven, \ 1770--1827: \ Haydn's pupil, \ then motives and expansion: \ longer, \ wider, \ louder", TUNE),
            (r"the three in one city, \ within one lifetime: \ the `Viennese Classics' is a later label", GREY_A),
        ]
        rows_scene(self, r"three careers", items,
                   "Three composers, one city, overlapping lives. <bookmark mark='b'/> Joseph Haydn spent thirty years "
                   "as music director to the Esterházy princes, then found fame in London in the 1790s. "
                   "<bookmark mark='c'/> His art is economy: whole movements spun from one idea, with wit and surprise. "
                   "<bookmark mark='d'/> Wolfgang Amadeus Mozart, a child prodigy, lived as a freelance in Vienna and "
                   "brought the style to opera, in the ensembles of Figaro and Don Giovanni. <bookmark mark='e'/> Ludwig "
                   "van Beethoven came to Vienna in 1792 to study with Haydn, and pushed the language outward: motives "
                   "worked to exhaustion, movements longer, wider and louder. <bookmark mark='f'/> Calling them together "
                   "the Viennese Classics is a later habit; they did not think of themselves as a school.", marks="cdef")

    # ------------------------------------------------------------------
    def measured(self):
        d = load("three")["stats"]
        names = ("haydn", "mozart", "beethoven")
        cols = [TUNE, BLUE, EAR]
        panels = VGroup()
        for key, lab_, top in (("bars", r"bars per movement", 320.0), ("span", r"semitones each instrument spans", 40.0)):
            bars = VGroup()
            for j, n in enumerate(names):
                v = d[n][key]
                h = 2.6 * v / top
                r = Rectangle(width=0.8, height=max(h, 0.02), stroke_width=0, fill_color=cols[j], fill_opacity=0.9).move_to([1.0 * j, h / 2, 0])
                bars.add(VGroup(r, label(rf"{v:.0f}", font_size=20, color=WHITE).next_to(r, UP, buff=0.08), label(n.title(), font_size=18, color=GREY_A).next_to(r, DOWN, buff=0.15)))
            panels.add(VGroup(bars, label(lab_, font_size=20, color=GREY_A).next_to(bars, DOWN, buff=0.55)))
        panels.arrange(RIGHT, buff=2.0, aligned_edge=DOWN).move_to(DOWN * 0.2)
        cnt = label(rf"single movements: \ Haydn {d['haydn']['movements']}, \ Mozart {d['mozart']['movements']}, \ Beethoven {d['beethoven']['movements']}", font_size=20, color=GREY_B).to_edge(UP, buff=0.5)
        cap = label(r"bars are not equal units \ (a bar of 3/8 is short): \ the lengths are rough", font_size=19, color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The expansion can be measured on the corpus. <bookmark mark='a'/> Haydn's and Mozart's quartet movements "
            f"average about {say(round(d['haydn']['bars'], -1))} and {say(round(d['mozart']['bars'], -1))} bars; "
            f"Beethoven's, {say(round(d['beethoven']['bars'], -1))}, three times as long, though a bar is not a fixed unit "
            "of time and the figures are rough. <bookmark mark='b'/> And each of Beethoven's instruments covers about "
            f"{say(round(d['beethoven']['span']))} semitones on average, against about {say(round(d['haydn']['span']))} for "
            "Haydn and Mozart: nearly an octave more, the strings pushed higher and lower."
        ) as vo:
            self.play(FadeIn(cnt), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(panels[0]))
            vo.wait_until("b")
            self.play(FadeIn(panels[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("three")
        c = clip("three.quiz")
        card = listen_card(r"Two quartet openings, \ half a century apart: \ Haydn's first, \ and one of Beethoven's middle period. \ "
                           r"Which is Beethoven, \ A or B? \ Listen for register and for who has the tune.", width=10.6)
        with self.voiceover(
            "Two openings, half a century apart: Haydn's very first quartet, and one of Beethoven's from 1806. Which is "
            "Beethoven, A or B? Listen for the register, and for who has the tune."
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        gA = voices_roll(d["A"], width=5.4, height=2.8, colors=[TUNE, BLUE, EAR, GREY_A], bar_h=0.1).move_to(LEFT * 3.3 + DOWN * 0.2)
        gB = voices_roll(d["B"], width=5.4, height=2.8, colors=[TUNE, BLUE, EAR, GREY_A], bar_h=0.1).move_to(RIGHT * 3.3 + DOWN * 0.2)
        la = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"from the encodings, \ Part 7's bowed string", corner=DL, tag_corner=DR)
            flash_voices(snd, gA, d["A"], d["starts"]["A"], d["unitA"], colors=[TUNE, BLUE, EAR, GREY_A])
            flash_voices(snd, gB, d["B"], d["starts"]["B"], d["unitB"], colors=[TUNE, BLUE, EAR, GREY_A])
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        ans = VGroup(label(r"Haydn, \ Op. 1 No. 1 \ (about 1757)", font_size=22, color=TUNE).next_to(gA, DOWN, buff=0.35),
                     label(r"Beethoven, \ Op. 59 No. 1 \ (1806): \ the cello has the tune", font_size=22, color=EAR).next_to(gB, DOWN, buff=0.35))
        with self.voiceover(
            "B is Beethoven, the first of the quartets he wrote for Count Razumovsky in 1806, where the long opening tune "
            "is given to the cello, under a quietly pulsing accompaniment. A is Haydn's first quartet, from the 1750s, "
            "light and quick, the first violin on top."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()
