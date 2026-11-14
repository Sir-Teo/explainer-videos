from __future__ import annotations

import numpy as np

from videos.music.music30.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.studio()
        self.groove()
        self.plan()

    # ------------------------------------------------------------------
    def studio(self):
        card = history_card(1948, r"Paris: \ Pierre Schaeffer, \ an engineer at French radio", r"records trains at a station, \ and cuts a disc whose groove closes on itself",
                            width=11.4, font_size=25).to_edge(UP, buff=0.5)
        rows_ = text_rows([
            (r"a closed groove: \ the needle plays the same second of sound again and again", WHITE),
            (r"repeated, \ a noise stops being a train and becomes a rhythm, \ a colour, \ a shape", WHITE),
            (r"\textit{Étude aux chemins de fer}: \ music made from recordings, \ not from notes", TUNE),
            (r"he called it \textit{musique concrète}: \ music made directly in sound", EAR),
        ], font_size=25).move_to(DOWN * 0.9)
        with self.voiceover(
            "Paris, 1948. Pierre Schaeffer, an engineer at French radio, records locomotives at a railway station and "
            "brings the discs back to the studio. <bookmark mark='a'/> He cuts one groove so that it closes on itself, and "
            "the needle plays the same second of sound over and over. <bookmark mark='b'/> Repeated, a noise stops being a "
            "train: it becomes a rhythm, a colour, a shape. <bookmark mark='c'/> His Railway Study was broadcast that year, "
            "music made from recordings rather than notes. <bookmark mark='d'/> He called it musique concrète, music made "
            "directly in sound."
        ) as vo:
            self.play(FadeIn(card))
            for mark, r in zip("abcd", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def groove(self):
        d = load("hook")
        c = clip("hook.groove")
        R = 1.8
        disc = VGroup(Circle(radius=R, color=GREY_B, stroke_width=3), Circle(radius=0.35, color=GREY_B, stroke_width=2),
                      *[Circle(radius=0.5 + 0.12 * k, color=GREY_B, stroke_width=0.6, stroke_opacity=0.5) for k in range(10)])
        groove = Circle(radius=1.25, color=TUNE, stroke_width=5)
        needle = Line([2.6, 1.6, 0], [0.9, 0.9, 0], color=WHITE, stroke_width=3)
        g = VGroup(disc, groove, needle).move_to(LEFT * 3.0 + DOWN * 0.2)
        rows_ = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"one fragment, \ 1.6 seconds: \ a woodblock, \ a drum, \ a low bowed note \ (ours)", WHITE),
            (r"looped eight times, \ like a groove that never moves on", TUNE),
            (r"listen for when it stops sounding like objects", EAR))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(RIGHT * 3.2 + DOWN * 0.2)
        rows_.scale_to_fit_width(min(rows_.width, 6.0))
        with self.voiceover(
            "The film cannot use Schaeffer's discs, so here is a closed groove of our own: one fragment, a second and a half "
            "of a woodblock, a drum and a low bowed note from earlier parts, looped eight times. Listen for the moment it "
            "stops sounding like objects being struck, and starts sounding like a pattern."
        ):
            self.play(FadeIn(g), FadeIn(rows_))
        with self.listen(c) as snd:
            window(snd, r"a closed groove \ (ours)", detail=r"Part 9's woodblock and drum, \ Part 7's bowed string", corner=DL, tag_corner=DR)
            snd.drive(disc, lambda m, t: m.rotate(-0.05, about_point=groove.get_center()))
            for k in range(d["loops"]):
                pulse(snd, rows_[1], k * d["fragment"], k * d["fragment"] + 0.3, buff=0.05)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"music from recordings: \ tape speed, \ reversal, \ the cut attack",
            r"chance, \ silence, \ and the electronic studios",
            r"Xenakis: \ clouds of events counted by Poisson's law, \ and sieves",
            r"sound masses that beat, \ and two loops drifting apart",
            r"a spectrum orchestrated, \ and the first singing computer",
            r"composing with machines, \ and listening to data",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. First, what a tape machine does to a sound. <bookmark mark='b'/> Then chance, silence, and "
            "the electronic studios. <bookmark mark='c'/> Xenakis's clouds, whose onsets obey Poisson's law, and his sieves. "
            "<bookmark mark='d'/> Masses of sound that beat, and two loops of one figure drifting apart. "
            "<bookmark mark='e'/> A single spectrum given to an ensemble, and the first computer to sing. "
            "<bookmark mark='f'/> And at the frontier, composing with machines and listening to data."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
