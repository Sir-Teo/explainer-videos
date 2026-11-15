from __future__ import annotations

import numpy as np

from videos.music.music42.common import *  # noqa: F403


class Funnel(SoundScene):
    def construct(self):
        chapter(self, 5, r"Constraints as engines", r"Do rules make composing harder, \ or easier?")
        self.count()
        self.how()
        self.stravinsky()
        self.engines()

    # ------------------------------------------------------------------
    def count(self):
        d = load("funnel")
        cs = d["counts"]
        names = [r"any 8 notes from 15"] + [r"+ \ " + r.replace(" ", r" \ ") for r in d["rules"]]
        x0, W = -1.0, 6.2
        lmax = np.log10(cs[0])
        bars = VGroup()
        for i, (n, v) in enumerate(zip(names, cs)):
            w = W * np.log10(v) / lmax
            y = 1.9 - 0.72 * i
            bars.add(VGroup(label(n, font_size=17, color=WHITE).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT),
                            Rectangle(width=w, height=0.42, stroke_width=0, fill_color=TUNE if i == len(cs) - 1 else BLUE, fill_opacity=0.85).move_to([x0 + w / 2, y, 0]),
                            label(f"{v:,}", font_size=17, color=WHITE).move_to([x0 + w + 0.2, y, 0], aligned_edge=LEFT)))
        cap = label(r"bar length: \ the number of melodies on a logarithmic scale; \ counted exactly by dynamic programming", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(rf"melodies of {d['length']} notes on the {d['notes']} white keys from C4 to C6", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Count what rules do. Take melodies of {say(d['length'])} notes on the {say(d['notes'])} white keys from middle C "
            f"up two octaves. <bookmark mark='a'/> With no rules there are {say(cs[0])}, about two and a half billion. "
            f"<bookmark mark='b'/> Start and end on C, and {say(cs[1])} remain. <bookmark mark='c'/> Allow no leap larger "
            f"than a fifth: {say(cs[2])}. <bookmark mark='d'/> Follow every leap with a step back: {say(cs[3])}. "
            f"<bookmark mark='e'/> No note three times running, and stay within an octave: {say(cs[5])}. Five rules have cut "
            "the space by a factor of about a quarter of a million."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            for i, mark in enumerate("abcde"):
                vo.wait_until(mark)
                if mark == "e":
                    self.play(FadeIn(bars[4]), FadeIn(bars[5]))
                else:
                    self.play(FadeIn(bars[i]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def how(self):
        rows_ = text_rows([
            (r"a melody is built note by note; \ what a rule needs to know about the past is small", WHITE),
            (r"the state: \ the last note, \ the last move, \ how many repeats, \ the lowest and highest so far", WHITE),
            (r"ways(i, \ state) \ = \ sum over allowed next notes x \ of \ ways(i + 1, \ new state)", TUNE),
            (r"a few thousand states and eight steps, \ instead of 2.5 billion melodies: \ under a second", WHITE),
            (r"Part 16 counted Fux's counterpoint the same way", GREY_A),
        ])
        head = label(r"counting without listing", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "How can we count billions without listing them? <bookmark mark='a'/> A melody is built note by note, and what a "
            "rule needs to know about the past is small. <bookmark mark='b'/> Call it the state: the last note, the last "
            "move, how many repeats, the lowest and highest so far. <bookmark mark='c'/> The number of ways to finish from a "
            "state is the sum, over every allowed next note, of the ways to finish from the new state. "
            "<bookmark mark='d'/> That is a few thousand states and eight steps, under a second, instead of two and a half "
            "billion melodies. <bookmark mark='e'/> Part 16 counted Fux's counterpoint the same way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_.copy().set_opacity(0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stravinsky(self):
        items = [
            (r"Stravinsky, \ \textit{Poetics of Music} \ (1942): \ `the more constraints one imposes, \ the more one frees oneself'", WHITE),
            (r"a constraint shrinks the space so that a composer can actually explore it", WHITE),
            (r"but a space can shrink to nothing: \ too many rules and no melody obeys them all", WHITE),
            (r"the art is choosing constraints that leave a small, \ rich space", TUNE),
            (r"rules here are engines, \ not prohibitions", GREY_A),
        ]
        rows_scene(self, r"constraint as freedom", items,
                   "Composers have said this for a long time. <bookmark mark='b'/> Stravinsky, in his Poetics of Music of 1942: "
                   "the more constraints one imposes, the more one frees oneself. <bookmark mark='c'/> A constraint shrinks the "
                   "space so that a composer can actually explore it. <bookmark mark='d'/> But a space can shrink to nothing: "
                   "with too many rules, no melody obeys them all. <bookmark mark='e'/> The art is choosing constraints that "
                   "leave a small but rich space. <bookmark mark='f'/> Rules, seen this way, are engines, not prohibitions.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def engines(self):
        items = [
            (r"canons \ (Part 20): \ one line must also work against itself, \ delayed", WHITE),
            (r"isorhythm \ (Part 23) \ and the twelve-tone row \ (Part 29): \ an order fixed in advance", WHITE),
            (r"Bach's chorale preludes: \ a given hymn tune, \ everything else invented around it", WHITE),
            (r"pop songwriting camps: \ a title, \ a tempo, \ a deadline", TUNE),
            (r"chapter 6: \ the most mechanical constraint of all, \ a table and two dice", GREY_A),
        ]
        rows_scene(self, r"constraints that made music", items,
                   "Many styles are constraints that turned out to be engines. <bookmark mark='b'/> A canon, from Part 20, is a "
                   "line that must also work against itself, delayed. <bookmark mark='c'/> Isorhythm, in Part 23, and the "
                   "twelve-tone row, in Part 29, fix an order in advance. <bookmark mark='d'/> Bach's chorale preludes take a "
                   "given hymn tune and invent everything else around it. <bookmark mark='e'/> And pop songwriting camps work "
                   "from a title, a tempo and a deadline. <bookmark mark='f'/> Chapter six turns to the most mechanical "
                   "constraint of all: a table and two dice.", marks="cdef")
