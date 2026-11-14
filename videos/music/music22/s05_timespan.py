from __future__ import annotations

import numpy as np

from videos.music.music22.common import *  # noqa: F403


class Timespan(SoundScene):
    def construct(self):
        chapter(self, 4, r"A time-span reduction", r"How does a program decide which note is the head?")
        self.rule()
        self.tree()
        self.prolongation()

    # ------------------------------------------------------------------
    def rule(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"split the Tune into spans: \ 2 beats, \ 4, \ 8, \ 16, \ 32", WHITE),
            (r"each span keeps one note, \ its head, \ chosen from its two halves' heads", WHITE),
            (r"score: \ +2 if a note of the chord; \ +3 tonic, \ +2 fifth, \ +1.5 third; \ +0.5 per level of beat strength", WHITE),
            (r"the higher score wins; \ ties go to the earlier note", WHITE),
            (r"Lerdahl and Jackendoff's rules, \ simplified to a sum", TUNE))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"the head of a span", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Here is the reduction of the opening, written as a program. <bookmark mark='a'/> Cut the Tune into spans of "
            "two beats, then four, eight, sixteen and thirty-two. <bookmark mark='b'/> Each span keeps one note, its "
            "head, chosen from the heads of its two halves. <bookmark mark='c'/> The choice is a score: two points if "
            "the note belongs to the chord sounding there; three for the tonic, two for the fifth, one and a half for "
            "the third; half a point for each level of metrical strength. <bookmark mark='d'/> The higher score wins, "
            "and a tie goes to the earlier note. <bookmark mark='e'/> It is Lerdahl and Jackendoff's preference rules, "
            "simplified to a sum: crude, and explicit, which is the point."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tree(self):
        d = load("hook")
        lv = d["levels"]
        rows_ = VGroup()
        for k in (1, 2, 3, 4, 5):
            notes = lv[k]
            line = VGroup(*[label(NAMES.get(n[0] % 12, "?"), font_size=26 if k < 4 else 32, color=TUNE if k >= 4 else WHITE) for n in notes]).arrange(RIGHT, buff=0.32 if k == 1 else 0.6 + 0.4 * (k - 1))
            rows_.add(VGroup(label(rf"every {2 ** k}", font_size=20, color=GREY_B), line).arrange(RIGHT, buff=0.6))
        rows_.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(DOWN * 0.1)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        cap = label(r"C G C at the top: \ tonic, \ dominant, \ tonic, \ the bass of the \textit{Ursatz}", font_size=24, color=TUNE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The levels, read as letters. <bookmark mark='a'/> Every two beats: C G A G F E D C, then G F E D twice, "
            "then the opening again: the Tune with its repeated notes removed. <bookmark mark='b'/> Every four beats, "
            "the strains keep their first and middle notes. <bookmark mark='c'/> Every eight beats, a note a phrase: C C "
            "G G C C. <bookmark mark='d'/> Every sixteen, C G C, and at thirty-two, C C. <bookmark mark='e'/> The top of "
            "the program's tree is tonic, dominant, tonic: Schenker's bass arpeggiation, found by a sum of preferences. "
            "But the program found it in the bass's terms, through the melody's notes; it never found the descending "
            "line, because its rules prefer the stable G and C to the passing F, E and D. A different rule set would "
            "find a different tree. That is the lesson of every reduction."
        ) as vo:
            self.play(FadeIn(rows_[0]))
            for mark, r in zip("bcd", rows_[1:4]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
            self.play(FadeIn(rows_[4]))
            vo.wait_until("e")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def prolongation(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"the fourth structure: \ prolongational reduction", WHITE),
            (r"not which note is most important, \ but which event tenses or relaxes toward which", WHITE),
            (r"a strong prolongation: \ the same chord; \ a weak one: \ the same root, \ another inversion; \ a progression: \ a new chord", WHITE),
            (r"Part 19's tension curves came from Lerdahl's later book: \ distances along this tree", TUNE),
            (r"the tree of tension, \ and the tree of importance, \ are different trees", GREY_A))]).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"tension and relaxation", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Lerdahl and Jackendoff's fourth structure asks a different question. <bookmark mark='a'/> The "
            "prolongational reduction is about tension. <bookmark mark='b'/> Not which note is most important, but which "
            "event tenses away from which, and which relaxes back into which. <bookmark mark='c'/> A chord that returns "
            "unchanged is a strong prolongation; the same root in another position a weak one; a new chord a progression, "
            "a move of tension. <bookmark mark='d'/> Lerdahl's later book, Tonal Pitch Space, put numbers on these moves: "
            "the tension curves of Part 19 were distances along such a tree. <bookmark mark='e'/> The tree of importance "
            "and the tree of tension need not be the same, and the theory keeps them apart."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
