from __future__ import annotations

import numpy as np

from videos.music.music19.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.tristan()
        self.argued()
        self.plan()

    # ------------------------------------------------------------------
    def tristan(self):
        d = load("hook")
        c = clip("hook.tristan")
        card = history_card(1865, r"Munich: \ \textit{Tristan und Isolde}", r"Wagner's opera, \ finished 1859; \ its first chord has been argued over ever since", width=10.4, font_size=26).to_edge(UP, buff=0.4)
        st1 = block_staff([d["first"]["tristan"][::-1], d["first"]["resolution"][::-1]], width=4.4, beats=2).move_to(LEFT * 3.3 + DOWN * 0.8)
        st2 = block_staff([d["second"]["tristan"][::-1], d["second"]["resolution"][::-1]], width=4.4, beats=2).move_to(RIGHT * 3.3 + DOWN * 0.8)
        l1 = label(r"the chord, \ and where it goes", font_size=24, color=GREY_A).next_to(st1, UP, buff=0.3)
        l2 = label(r"the same, \ a minor third higher", font_size=24, color=GREY_A).next_to(st2, UP, buff=0.3)
        with self.voiceover(
            "In 1865, in Munich, Richard Wagner's Tristan und Isolde reached the stage; its prelude had already "
            "puzzled concert audiences for six years. <bookmark mark='a'/> It begins with a single line in the cellos, and then a chord: F, B, "
            "D sharp, G sharp. The top note slides up, the chord moves to another, and the music stops. Then the whole "
            "thing again, a minor third higher. Listen."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(st1), FadeIn(st2), FadeIn(l1), FadeIn(l2))
        with self.listen(c) as snd:
            window(snd, r"the opening of \textit{Tristan}, \ reduced to its harmony", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, l1, d["starts"]["first"], d["starts"]["second"] - 0.5, buff=0.1)
            pulse(snd, l2, d["starts"]["second"], c.duration, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def argued(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"F \ B \ D$\sharp$ \ G$\sharp$: \ four notes, \ no key yet", WHITE),
            (r"called a French sixth, \ a half-diminished seventh, \ an altered dominant, \ and no chord at all", WHITE),
            (r"each reading is a different story of how harmony works", WHITE),
            (r"the road to this chord begins with a single borrowed leading note", TUNE))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"the most analysed chord in music", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "That chord has been argued over for a century and a half. <bookmark mark='a'/> Four notes, and no key "
            "established. <bookmark mark='b'/> Theorists have called it a French sixth, a half-diminished seventh, an "
            "altered dominant, and no chord at all, only a moment in four moving lines. <bookmark mark='c'/> Each "
            "reading is a different theory of what harmony is. <bookmark mark='d'/> And every one of them starts from "
            "something small: a single note borrowed from outside the key, to lean on the note next door."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcd", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        head = label(r"Part 19: \ Chromatic Harmony", font_size=36, color=TUNE).to_edge(UP, buff=0.5)
        steps = VGroup(*[label(t, font_size=27, color=c_) for t, c_ in (
            (r"borrowed leading notes, \ borrowed chords: \ applied dominants, \ mixture", WHITE),
            (r"the Neapolitan and the augmented sixths", WHITE),
            (r"the diminished seventh, \ and trapdoors to distant keys", EAR),
            (r"the comma those trapdoors hide \ (Part 6)", WHITE),
            (r"chromatic mediants, \ a pathfinder between keys, \ a measure of tension", WHITE),
            (r"and back to Tristan", TUNE))]).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(DOWN * 0.1)
        with self.voiceover(
            "This part walks the road from one borrowed note to Tristan. <bookmark mark='a'/> First the borrowed "
            "leading notes and borrowed chords that Bach already used. <bookmark mark='b'/> Then the Neapolitan and the "
            "augmented sixths, the strongest ways of approaching a dominant. <bookmark mark='c'/> Then the diminished "
            "seventh, whose symmetry opens trapdoors to distant keys, <bookmark mark='d'/> and the comma those trapdoors "
            "hide, which only equal temperament closes. <bookmark mark='e'/> Then chromatic mediants, a program that "
            "finds the shortest way to any key, and a number for tension. <bookmark mark='f'/> And then back to the "
            "chord at the start."
        ) as vo:
            self.play(FadeIn(head))
            for mark, s in zip("abcdef", steps):
                vo.wait_until(mark)
                self.play(FadeIn(s))
        self.wait(0.4)
        self.clear_scene()
