from __future__ import annotations

import numpy as np

from videos.music.music30.common import *  # noqa: F403


class Phasing(SoundScene):
    def construct(self):
        chapter(self, 6, r"Process and phasing", r"What happens when two copies of one loop drift apart?", extra=((1965, r"\textit{It's Gonna Rain}"),))
        self.reich()
        self.hear()
        self.patterns()
        self.minimal()
        self.speech()
        self.additive()

    # ------------------------------------------------------------------
    def reich(self):
        items = [
            (r"Steve Reich, \ San Francisco, \ 1965: \ a street preacher recorded saying `It's gonna rain'", WHITE),
            (r"two tape loops of the phrase, \ on two machines that run at slightly different speeds", WHITE),
            (r"in unison, \ then an echo, \ then a canon, \ then a texture no one composed", WHITE),
            (r"\textit{Piano Phase} \ (1967): \ two pianists play the same figure, \ one slowly pulling ahead", TUNE),
            (r"`music as a gradual process': \ a process you can hear happening", GREY_A),
        ]
        rows_scene(self, r"phasing", items,
                   "In 1965 Steve Reich recorded a street preacher in San Francisco saying it's gonna rain. "
                   "<bookmark mark='c'/> He made two tape loops of the phrase and played them on two machines that ran at "
                   "slightly different speeds. <bookmark mark='d'/> The loops began in unison, became an echo, then a canon, then "
                   "a texture nobody had composed. <bookmark mark='e'/> In Piano Phase, of 1967, two pianists play the same "
                   "figure, and one slowly pulls ahead of the other. <bookmark mark='f'/> Reich called it music as a gradual "
                   "process: a process you can hear happening, the opposite of a hidden row.", marks="cdef")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("phasing")
        c = clip("phasing.phase")
        fig = d["figure"]
        W = 8.4
        loopA = VGroup(*[RoundedRectangle(width=W / 12 - 0.06, height=0.16, corner_radius=0.05, stroke_width=0, fill_color=TUNE, fill_opacity=1.0)
                         .move_to([-W / 2 + W * (i + 0.5) / 12, 0.6 + 0.12 * (p - 72), 0]) for i, p in enumerate(fig)])
        loopB = loopA.copy().set_color(BLUE).shift(DOWN * 2.0)
        la = label(r"piano 1", font_size=21, color=TUNE).next_to(loopA, LEFT, buff=0.4)
        lb = label(r"piano 2: \ a little faster", font_size=21, color=BLUE).next_to(loopB, LEFT, buff=0.4)
        head = label(r"a twelve-note figure \ (ours, \ from the Tune's first notes), \ against itself", font_size=24, color=GREY_A).to_edge(UP, buff=0.45)
        cap = label(r"piano 2 gains one note on piano 1 every four times round", font_size=21, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Here is the process with a figure of our own, twelve notes built from the Tune's first notes. Two pianos start "
            "together. The second plays a little faster, gaining one note on the first every four times round, so you will "
            "hear the unison smear into an echo, then lock into a new pattern, then smear again. Watch the second line "
            "slide."
        ):
            self.play(FadeIn(head), FadeIn(loopA), FadeIn(loopB), FadeIn(la), FadeIn(lb), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"two pianos, \ drifting", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            unit, n = d["unit"], len(fig)
            snd.drive(loopB, lambda m, t: m.move_to([loopA.get_center()[0] - W * (t * (d["faster"] - 1) / unit / 12 % 1), m.get_center()[1], 0]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def patterns(self):
        d = load("phasing")
        pats = d["patterns"]
        ks = [p["shift"] for p in pats]
        b1 = columns([p["unisons"] for p in pats], [str(k) for k in ks], width=6.4, height=2.4, color=TUNE, fmt="{:.0f}", font_size=17).move_to(LEFT * 3.2 + DOWN * 0.3)
        b2 = columns([p["distinct"] for p in pats], [str(k) for k in ks], width=6.4, height=2.4, color=BLUE, fmt="{:.0f}", font_size=17).move_to(RIGHT * 3.2 + DOWN * 0.3)
        t1 = label(r"unisons, \ by how many notes ahead", font_size=20, color=TUNE).next_to(b1, UP, buff=0.3)
        t2 = label(r"distinct pairs of notes sounding together", font_size=20, color=BLUE).next_to(b2, UP, buff=0.3)
        cap = label(r"the figure passes through twelve alignments; \ symmetric about six, \ because ahead by $k$ is behind by $12 - k$", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The process is a walk through twelve alignments, one for each number of notes the second piano is ahead. "
            "<bookmark mark='a'/> For each, the program counts the unisons, both pianos on the same note: twelve at the "
            "start, none one note later, six at three, six and nine notes ahead, where the figure's repeated three-note "
            "cells line up. <bookmark mark='b'/> And it counts the distinct pairs of notes sounding together, a measure of "
            "how rich the composite is: richest at four, five, seven and eight notes ahead. The pattern is symmetric, "
            "because being k notes ahead is the same as being twelve minus k behind."
        ) as vo:
            self.play(FadeIn(b1), FadeIn(t1), FadeIn(cap))
            vo.wait_until("b")
            self.play(FadeIn(b2), FadeIn(t2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def minimal(self):
        items = [
            (r"Terry Riley, \ \textit{In C} \ (1964); \ Philip Glass, \ \textit{Music in Twelve Parts} \ (1971--74)", WHITE),
            (r"Reich, \ \textit{Music for 18 Musicians} \ (1976): \ eleven chords, \ each the source of a section", WHITE),
            (r"Glass's additive rhythm: \ a figure grows by one note at a time \ (Part 28's Bartók, \ reborn)", WHITE),
            (r"minimalism reached rock, \ ambient and film music within a decade", TUNE),
            (r"Part 33 measures phase patterns as mathematics", GREY_A),
        ]
        rows_scene(self, r"minimalism", items,
                   "Process music became a movement. <bookmark mark='b'/> Terry Riley's In C, of 1964, and Philip Glass's Music "
                   "in Twelve Parts, of the early 1970s, <bookmark mark='c'/> and Reich's Music for Eighteen Musicians, of 1976, "
                   "built from a cycle of eleven chords. <bookmark mark='d'/> Glass grew figures by adding one note at a time, "
                   "the additive rhythm of Part 28, reborn. <bookmark mark='e'/> Within a decade minimalism had reached rock, "
                   "ambient music and film. <bookmark mark='f'/> Part 33 treats phase patterns as mathematics.", marks="cdef")

    # ------------------------------------------------------------------
    def additive(self):
        d = load("additive")
        c = clip("additive.grow")
        g = mroll(d["notes"], width=11.0, height=2.0, lo=70, hi=81, color=TUNE, bar_h=0.12).move_to(DOWN * 0.1)
        head = label(r"additive process: \ a five-note figure, \ one note longer each time \ (ours)", font_size=25, color=GREY_A).to_edge(UP, buff=0.45)
        cap = label(r"1, \ 1, \ 2, \ 2, \ 3, \ 3, \ 4, \ 4, \ 5, \ 5 notes: \ the pulse never changes; \ the cycle grows", font_size=21, color=GREY_A).next_to(g, DOWN, buff=0.4)
        with self.voiceover(
            "Glass's version of process is additive. A figure of five notes, played twice with one note, twice with two, and "
            "so on up to five, the pulse never changing. The ear keeps re-hearing where the cycle begins, which is the "
            "music's whole drama."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"a figure, \ growing", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, g.notes, [n[1] * d["unit"] for n in d["notes"]], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def speech(self):
        items = [
            (r"Reich, \ \textit{Different Trains} \ (1988): \ recorded voices, \ their speech melodies doubled by a string quartet", WHITE),
            (r"memories of train journeys in America and in wartime Europe, \ in the speakers' own words", WHITE),
            (r"the rise and fall of a spoken phrase, \ transcribed as notes", WHITE),
            (r"the closed groove of 1948 and the loop of 1965, \ turned into melody", TUNE),
            (r"Part 40 hears speech and song as one continuum", GREY_A),
        ]
        rows_scene(self, r"speech becomes melody", items,
                   "Reich later turned recorded speech itself into melody. <bookmark mark='b'/> In Different Trains, of 1988, recorded voices speak, and a string quartet doubles the rise and fall of their phrases. <bookmark mark='c'/> The voices remember train journeys in America and in wartime Europe, in the speakers' own words. <bookmark mark='d'/> Each spoken phrase's pitch contour is transcribed as notes, <bookmark mark='e'/> so that the closed groove of 1948 and the tape loop of 1965 become melody. <bookmark mark='f'/> Part 40 hears speech and song as one continuum.", marks="cdef")
