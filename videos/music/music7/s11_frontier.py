from __future__ import annotations

import numpy as np

from videos.music.music7.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ what makes a great violin?", r"What can measurement say about a great instrument, and what can it not?", lit=(2009,), extra=((2012, r"blind tests of old and new violins"),),
                spoken="Chapter 10. The frontier: what makes a great violin?")
        self.hotel()
        self.unknown()
        self.models()

    # ------------------------------------------------------------------
    def hotel(self):
        head = label(r"Back to the hotel room", font_size=38, color=GREY_A).to_edge(UP, buff=0.4)
        rows = rows_card([
            (r"2010, \ Indianapolis", r"21 players, \ 6 violins. \ 13 would take a new one home. \\ The least liked was a Stradivari."),
            (r"2012, \ Paris", r"10 soloists, \ 12 violins, \ a concert hall. \ 6 chose new; \\ the favourite of the twelve, \ by a wide margin, \ was new."),
            (r"2013--14, \ Paris \\ and New York", r"137 listeners in two halls. \ The new violins were judged to carry better, \\ and were preferred. \ Nobody could tell old from new."),
            (r"what the players \\ said they wanted", r"a violin that is loud under the ear, \ answers easily, \ and is even \\ across the strings. \ Age was not something they could hear."),
        ], left=-6.5, text_left=-2.6, top=1.9, step=1.4, name_size=26, text_size=23, color=HIST)
        self.play(FadeIn(head), run_time=0.5)
        with self.voiceover(
            "So, back to the hotel room, with everything this part has built. <bookmark mark='a'/> In "
            "Indianapolis, thirteen players of twenty-one preferred a new violin. <bookmark mark='b'/> Near "
            "Paris, six soloists of ten chose a new one to take on tour, and the single favourite of the "
            "twelve instruments was new. <bookmark mark='c'/> The last objection was that a soloist's violin "
            "is made for the back row of a hall, not for the player's ear. So the same team put a hundred and "
            "thirty-seven listeners in two concert halls, in Paris and in New York. The listeners judged that "
            "the new violins carried better, they preferred them, and they could not tell which were old. "
            "<bookmark mark='d'/> In the terms of this part, every one of those violins was the same machine: "
            "a sawtooth from a bowed string, sent through a wooden box with a few hundred resonances. What "
            "the players said they wanted was a box that is loud under the ear, that answers easily, that is "
            "even from string to string. Three centuries of age was not something they could hear."
        ) as vo:
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def unknown(self):
        head = label(r"What nobody can do yet", font_size=38, color=EAR).to_edge(UP, buff=0.4)
        rows = rows_card([
            (r"predict a preference", r"measure a violin's response, \ and say whether players will like it. \\ Each player is consistent; \ players disagree with each other."),
            (r"explain rosin", r"this part's friction depends only on sliding speed. \ Real rosin warms and softens \\ in every slip: \ its friction depends on its temperature a moment ago."),
            (r"draw the true wedge", r"a bowing machine, \ 2008: \ the smallest bow force did not follow the bow's speed \\ as Schelleng's formula says it should."),
            (r"model felt", r"squeezed felt pushes back less on the way out than on the way in, \\ and remembers the last blow. \ Hammers are still voiced by ear, \ with needles."),
        ], left=-6.5, text_left=-2.9, top=1.9, step=1.4, name_size=26, text_size=23, color=EAR)
        self.play(FadeIn(head), run_time=0.5)
        with self.voiceover(
            "Here is where knowledge runs out. <bookmark mark='a'/> Nobody can yet measure a violin and say "
            "whether players will like it. In careful experiments each player turns out to be consistent, "
            "choosing the same instruments again on another day, but different players choose differently. "
            "There is no single best box. <bookmark mark='b'/> Nobody fully understands rosin. In this part its "
            "friction depended only on how fast the string was sliding. Measurements in the year 2000 showed "
            "that this is wrong: rosin warms and softens during every slip, a few hundred times a second, and "
            "its grip depends on its temperature a moment ago. Models with warm rosin behave more like real "
            "strings, and they are still being worked out. <bookmark mark='c'/> Even Schelleng's diagram is "
            "unfinished. When it was finally measured with a bowing machine, in 2008, the smallest force did "
            "not depend on the bow's speed in the way his formula says. <bookmark mark='d'/> And piano felt "
            "has a memory. Squeezed, it pushes back less on the way out than on the way in, and it has not "
            "fully recovered when the next blow comes. The power law we used is the first approximation. "
            "Piano technicians still voice hammers by ear."
        ) as vo:
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def models(self):
        k, h, b = load("ks"), load("hammer"), load("bow")
        head = label(r"Instruments made of arithmetic", font_size=38, color=GREY_A).to_edge(UP, buff=0.4)
        cols = VGroup(
            VGroup(label(r"1983", font_size=30, color=PLUCK), label(r"Karplus and Strong: \\ a loop of numbers \\ and an average", font_size=24), label(rf"{k['delay']} numbers for one string", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.2),
            VGroup(label(r"1990s", font_size=30, color=STRUCK), label(r"strings, \ hammers and bows \\ as travelling waves \\ and a point of contact", font_size=24), label(r"what this part's bow uses", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.2),
            VGroup(label(r"now", font_size=30, color=BOWED), label(r"whole instruments on a grid: \\ strings, \ soundboard \\ and the air around them", font_size=24), label(r"millions of numbers, \ in real time", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.2),
        ).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to(UP * 0.5)
        arrows = VGroup(*[Arrow(cols[i].get_right(), cols[i + 1].get_left(), color=GREY_C, buff=0.12, stroke_width=3).set_y(cols[0][1].get_y()) for i in range(2)])
        end = VGroup(label(r"a model is a hypothesis you can listen to", font_size=32, color=TUNE),
                     label(r"when it sounds wrong, \ something is missing from the physics", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "And one frontier that is moving fast. Every sound in this part was computed. <bookmark mark='a'/> "
            f"In 1983 that meant Karplus and Strong's loop: {say(k['delay'])} numbers and an average. "
            "<bookmark mark='b'/> Through the nineteen nineties it meant what our bow and hammer use: waves "
            "travelling along a string, and a careful treatment of the one point where something touches it. "
            "<bookmark mark='c'/> Now it means whole instruments laid out on a grid: every string, the "
            "soundboard, the box and the air around it, millions of numbers advanced forty-eight thousand "
            "times a second. A few years ago that took hours for each second of sound. On today's graphics "
            "processors parts of it run as fast as you can play. <bookmark mark='d'/> That matters for more "
            "than convenience. A model is a hypothesis that you can listen to. When the simulated violin "
            "sounds wrong, something is missing from the physics, and the ear, which Part 4 showed to be a "
            "superb instrument, tells you so at once. Much of what this part has shown was found that way."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cols[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[0]), FadeIn(cols[1]))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[1]), FadeIn(cols[2]))
            vo.wait_until("d")
            self.play(FadeIn(end))
        self.wait(0.3)
        self.clear_scene()
