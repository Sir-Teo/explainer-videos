from __future__ import annotations

import numpy as np

from videos.music.music24.common import *  # noqa: F403


class Melody(SoundScene):
    def construct(self):
        chapter(self, 5, r"The line", r"What makes a line singable?")
        self.rules()
        self.counted()

    # ------------------------------------------------------------------
    def rules(self):
        items = [
            (r"mostly steps; \ leaps of a third, \ fourth, \ fifth, \ octave; \ the ascending minor sixth", WHITE),
            (r"never a seventh, \ an augmented or diminished interval, \ or more than an octave", WHITE),
            (r"after a leap, \ turn back by step \ (Part 14's `gap fill')", WHITE),
            (r"one high point, \ approached and left gently", WHITE),
            (r"each voice singable on its own: \ the texture is four or five good melodies", TUNE),
        ]
        rows_scene(self, r"rules for a line", items,
                   "The style has rules for each line, too, set out by Jeppesen and taught ever since. <bookmark mark='b'/> "
                   "Mostly steps; leaps of a third, a fourth, a fifth or an octave, and the minor sixth only upwards. "
                   "<bookmark mark='c'/> Never a seventh, never an augmented or diminished interval, never more than an "
                   "octave. <bookmark mark='d'/> After a leap, turn back by step, the gap fill that Part 14 measured in "
                   "folk tunes. <bookmark mark='e'/> One high point, reached and left gently. <bookmark mark='f'/> The "
                   "point of all this: every voice is a good melody on its own, and the texture is four or five of them "
                   "at once.", marks="bcdef")

    # ------------------------------------------------------------------
    def counted(self):
        d = load("melody")["groups"]
        names = ["fourteenth century", "Palestrina", "Monteverdi"]
        tags = [r"14th century", r"Palestrina", r"Monteverdi"]
        cols = [GREY_B, TUNE, EAR]
        panels = VGroup()
        for key, lab_, fmt_, scale in (("forbidden_per_1000", r"forbidden intervals per 1,000 moves", "{:.1f}", 0.18),
                                       ("recovered", r"leaps turned back by step, \ in 100s", "{:.0f}", 5.0),
                                       ("leap_share", r"leaps among all moves, \ in 100s", "{:.0f}", 10.0)):
            bars = VGroup()
            for j, n in enumerate(names):
                v = d[n][key]
                shown = v if key == "forbidden_per_1000" else 100 * v
                h = 2.6 * shown / (14.0 if key == "forbidden_per_1000" else 50.0)
                r = Rectangle(width=0.7, height=max(h, 0.02), stroke_width=0, fill_color=cols[j], fill_opacity=0.9).move_to([j * 0.9, h / 2, 0])
                bars.add(VGroup(r, label(fmt_.format(shown), font_size=20, color=WHITE).next_to(r, UP, buff=0.08)))
            panels.add(VGroup(bars, label(lab_.replace(",", "{,}"), font_size=19, color=GREY_A).next_to(bars, DOWN, buff=0.3)))
        panels.arrange(RIGHT, buff=1.0, aligned_edge=DOWN).move_to(DOWN * 0.2)
        key = VGroup(*[VGroup(Square(side_length=0.22, stroke_width=0, fill_color=cols[j], fill_opacity=0.9), label(tags[j], font_size=19, color=GREY_A)).arrange(RIGHT, buff=0.15)
                       for j in range(3)]).arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.6)
        pf, mf, tf = d["Palestrina"]["forbidden_per_1000"], d["Monteverdi"]["forbidden_per_1000"], d["fourteenth century"]["forbidden_per_1000"]
        with self.voiceover(
            "Count those too. <bookmark mark='a'/> Forbidden intervals, sevenths, tritones, augmented and diminished "
            f"steps and leaps beyond the octave: in Palestrina, {pf:.1f} in every thousand moves, less than one; in the "
            f"fourteenth century about {say(round(tf))}; in Monteverdi's madrigals about {say(round(mf))}. "
            "<bookmark mark='b'/> Leaps turned back by step: "
            f"{say(round(100 * d['Palestrina']['recovered']))} in a hundred in Palestrina, against "
            f"{say(round(100 * d['Monteverdi']['recovered']))} in Monteverdi. <bookmark mark='c'/> And Monteverdi leaps "
            "more often. The madrigal bends the line to the words, and the words sometimes want an ugly interval: a "
            "sigh, a cry, a sudden drop. The rules describe one composer's habits better than they describe music."
        ) as vo:
            self.play(FadeIn(key))
            for mark, p in zip("abc", panels):
                vo.wait_until(mark)
                self.play(FadeIn(p))
        self.wait(0.4)
        self.clear_scene()
