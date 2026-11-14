from __future__ import annotations

import numpy as np

from videos.music.music13.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.three()
        self.mud()
        self.plan()

    # ------------------------------------------------------------------
    def three(self):
        d = load("hook")
        c = clip("hook.three")
        row = chord_row(d["three_names"], width=7.0, space=0.22, below=[r"bass: \ C", r"bass: \ E", r"bass: \ G"], font_size=26).move_to(UP * 1.6)
        kb = keys(48, 84, width=10.5, height=1.5).move_to(DOWN * 1.9)
        with self.voiceover(
            "Here are three notes: C, E and G. Play them together and you have one of the most familiar "
            "sounds in music. <bookmark mark='a'/> Now move the bottom note to the top. And again. Three "
            "different stacks, with three different bottom notes, three different sets of intervals, "
            "three different shapes under the hand. Listen to all three."
        ) as vo:
            self.play(FadeIn(row.staff.systems[0].lines), FadeIn(row.staff.systems[0].clef), FadeIn(row.notes[0]), FadeIn(row.below[0]), FadeIn(kb))
            for m in d["three"][0]:
                kb.on(m)
            vo.wait_until("a")
            self.play(FadeIn(row.notes[1]), FadeIn(row.below[1]), run_time=0.6)
            self.play(FadeIn(row.notes[2]), FadeIn(row.below[2]), FadeIn(row.staff.barlines), run_time=0.6)
        kb.clear()
        with self.listen(c) as snd:
            window(snd, r"one chord, \ three ways up", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            light_chords(snd, kb, d["three"], d["three_times"], end=c.duration)
            light_notes(snd, row.notes, d["three_times"], hold=1.0)
        kb.clear()
        claim = VGroup(label(r"1722, \ Jean-Philippe Rameau:", font_size=28, color=GREY_A), label(r"these are one chord, \ with one root: \ C", font_size=38, color=TUNE)).arrange(DOWN, buff=0.2).move_to(DOWN * 0.6)
        with self.voiceover(
            "In 1722 a French organist, Jean-Philippe Rameau, made a claim that sounds too simple to be a "
            "discovery. <bookmark mark='a'/> Those are not three chords. They are one chord, with one "
            "root, C, standing three ways. Most musicians before him had treated them as three separate "
            "things, each with rules of its own. Rameau's claim turned a thicket of rules into a small "
            "vocabulary, and it is the reason a guitarist today can read the single letter C on a page "
            "and know what to play."
        ) as vo:
            self.play(FadeOut(kb))
            vo.wait_until("a")
            self.play(FadeIn(claim), *[n.ink.animate.set_color(TUNE) for n in row.notes])
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mud(self):
        d = load("hook")
        c = clip("hook.mud")
        kb = keys(36, 72, width=11.0, height=1.9).move_to(UP * 0.9)
        tags = VGroup(label(r"close together", font_size=30, color=GREY_A), label(r"spread out", font_size=30, color=GREY_A)).arrange(RIGHT, buff=2.2).next_to(kb, DOWN, buff=0.5)
        head = label(r"the same three notes, \ at the bottom of the piano", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Here is a second puzzle. Take the same three notes, C, E and G, down to the bottom of the "
            "piano, close together. <bookmark mark='a'/> Then spread them out: the same three notes, over "
            "the same bass."
        ) as vo:
            self.play(FadeIn(head), FadeIn(kb))
            for m in d["low"]:
                kb.on(m)
            self.play(FadeIn(tags[0]))
            vo.wait_until("a")
            kb.clear()
            for m in d["spread"]:
                kb.on(m, BLUE)
            self.play(FadeIn(tags[1]))
        kb.clear()
        with self.listen(c) as snd:
            window(snd, r"close; \ then spread", detail=r"C, \ E and G, \ twice", corner=DL, tag_corner=DR)
            light_chords(snd, kb, [d["low"], d["spread"]], d["mud_times"], end=c.duration, colors=[GOLD, BLUE])
            pulse(snd, tags[0], d["mud_times"][0], d["mud_times"][1] - 0.2, buff=0.12)
            pulse(snd, tags[1], d["mud_times"][1], c.duration, buff=0.12)
        kb.clear()
        q = VGroup(label(r"the first is a growl; \ the second is clear.", font_size=32, color=WHITE), label(r"nothing in the names of the notes says why.", font_size=30, color=EAR)).arrange(DOWN, buff=0.25).next_to(tags, DOWN, buff=0.5)
        with self.voiceover(
            "The first is a growl. The second is clear. And nothing in the names of the notes explains "
            "it: C, E, G both times. The explanation is in the ear, in the critical band of Part 4, and "
            "by the end of this part we will compute where the mud begins."
        ):
            self.play(FadeIn(q))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        idea = VGroup(label(r"a chord is a choice too:", font_size=32, color=GREY_A), label(r"which notes, \ and where to put them.", font_size=32, color=TUNE)).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.45)
        card = objectives_card([
            r"name any interval: \ a number, \ a quality, \ and a place on the line of fifths",
            r"stack thirds: \ four triads, \ and why it is thirds",
            r"Rameau's claim: \ inversion, \ the root, \ and where the root comes from",
            r"seventh chords, \ and the tritone that drives them",
            r"voicing: \ why a low third is muddy, \ what to double, \ what to leave out",
            r"four ways to write a chord; \ Euler's map of all of them",
        ], title=r"Part 13: \ Intervals and Chords", font_size=26).move_to(DOWN * 0.5)
        with self.voiceover(
            "Part 12 chose the notes. This part sounds them together. <bookmark mark='a'/> We start with "
            "two notes, and learn to name any interval exactly. <bookmark mark='b'/> Then three: the "
            "triads, and the reason chords are built in thirds. <bookmark mark='c'/> Then Rameau's "
            "claim, and the question underneath it: why should a chord have a root at all? "
            "<bookmark mark='d'/> Four notes give us seventh chords, and the one interval that makes "
            "harmony move. <bookmark mark='e'/> Then voicing: the same chord can be clear or muddy, and "
            "we will compute which. <bookmark mark='f'/> And last, four ways to write a chord down, and "
            "a map, drawn by Euler, on which every chord has its neighbours."
        ) as vo:
            self.play(FadeIn(idea))
            self.play(FadeIn(card.head))
            for mark, r in zip("abcdef", card.rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
