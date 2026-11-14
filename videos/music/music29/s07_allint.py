from __future__ import annotations

import numpy as np

from videos.music.music29.common import *  # noqa: F403


class Allint(SoundScene):
    def construct(self):
        chapter(self, 6, r"All-interval rows", r"Can a row use every interval exactly once?", extra=((1926, r"Berg's \textit{Lyric Suite}"),))
        self.berg()
        self.count()
        self.machines()
        self.tritone()
        self.berg_life()

    # ------------------------------------------------------------------
    def berg(self):
        d = load("allint")
        c = clip("allint.berg")
        g = mroll(d["line"], width=9.0, height=2.4, lo=58, hi=73, color=TUNE, bar_h=0.14).move_to(UP * 0.1)
        ivs = d["berg_intervals"]
        nums = VGroup()
        for i, iv in enumerate(ivs):
            x0 = g.notes[i].get_center()
            x1 = g.notes[i + 1].get_center()
            nums.add(label(str(iv), font_size=20, color=EAR).move_to([(x0[0] + x1[0]) / 2, -1.5, 0]))
        head = label(r"the row of Berg's \textit{Lyric Suite} \ (1926)", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        cap = label(r"the eleven steps, \ in semitones upward mod 12: \ 1 to 11, \ each exactly once", font_size=21, color=EAR).next_to(nums, DOWN, buff=0.35)
        with self.voiceover(
            "Alban Berg's Lyric Suite for string quartet, of 1926, opens its first movement on a remarkable row. Here it is, "
            "once up the keyboard. Measure each step upward in semitones, wrapping round the octave: eleven, eight, nine, ten, "
            "seven, six, five, two, three, four, one. Every interval from one to eleven appears exactly once. It is an "
            "all-interval row."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(nums), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"Berg's row", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, g.notes, [n[1] * d["unit"] for n in d["line"]], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def count(self):
        d = load("allint")
        rows_ = text_rows([
            (r"a search: \ start on C, \ try each unused interval, \ never repeat a pitch class, \ back up when stuck", WHITE),
            (rf"the program finds every one: \ {d['count']:,} all-interval rows starting on C".replace(",", "{,}"), TUNE),
            (r"first listed by computer in the 1960s; \ the counts agree", WHITE),
            (rf"{d['symmetric']} of them, \ played backwards, \ are the same row a tritone higher", WHITE),
            (r"out of 39,916,800 rows starting on C: \ about 1 in 10,000".replace(",", "{,}"), GREY_A),
        ], font_size=24)
        head = label(r"how many are there?", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "How many all-interval rows are there? <bookmark mark='a'/> A depth-first search finds them all: start on C, try "
            "each unused interval in turn, never repeat a pitch class, and back up when stuck. "
            f"<bookmark mark='b'/> It finds {say(d['count'])} of them starting on C. <bookmark mark='c'/> The number was first "
            "computed in the 1960s, and the search agrees with it. <bookmark mark='d'/> "
            f"{say(d['symmetric'])} of them, played backwards, turn out to be the same row a tritone higher. "
            "<bookmark mark='e'/> Out of almost forty million rows starting on C, that is about one in ten thousand."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tritone(self):
        d = load("allint")
        rows_ = text_rows([
            (r"the eleven intervals are 1, \ 2, \ ..., \ 11 in some order", WHITE),
            (r"their sum is $1 + 2 + \cdots + 11 = 66$", WHITE),
            (r"so the last note is $66 \equiv 6 \pmod{12}$ semitones above the first", WHITE),
            (r"in every all-interval row, \ the first and last notes are a tritone apart", TUNE),
            (rf"the program checks: \ {d['tritone_ends']:,} of {d['count']:,}".replace(",", "{,}"), GREY_A),
        ], font_size=24)
        head = label(r"a theorem in one line", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "They share one property, and it has a one-line proof. <bookmark mark='a'/> The eleven intervals are one to "
            "eleven in some order. <bookmark mark='b'/> Their sum is sixty-six. <bookmark mark='c'/> So the last note lies "
            "sixty-six semitones above the first, which is six more than five octaves. <bookmark mark='d'/> In every "
            "all-interval row, the first and last notes are a tritone apart: in Berg's, F and B. "
            f"<bookmark mark='e'/> The program checks all {say(d['count'])}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def berg_life(self):
        items = [
            (r"Alban Berg, \ 1885--1935: \ the warmest of the three Viennese", WHITE),
            (r"\textit{Wozzeck} \ (1925): \ an atonal opera that audiences took to", WHITE),
            (r"the \textit{Lyric Suite} hides a programme: \ a secret love, \ in initials spelled as notes", WHITE),
            (r"the Violin Concerto \ (1935): \ a row that contains triads, \ and a Bach chorale", TUNE),
            (r"a row can sound tonal if its segments are tonal: \ the method is not the style", GREY_A),
        ]
        rows_scene(self, r"Berg", items,
                   "Berg was the warmest of the three Viennese composers. <bookmark mark='b'/> His opera Wozzeck, of 1925, is "
                   "atonal, and audiences took to it. <bookmark mark='c'/> The Lyric Suite was later found to hide a "
                   "programme, a secret love affair, with initials spelled out in notes. <bookmark mark='d'/> His Violin "
                   "Concerto, of 1935, uses a row built from interlocking triads, and quotes a Bach chorale. "
                   "<bookmark mark='e'/> A row can sound tonal if its pieces are tonal; the method does not fix the style.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def machines(self):
        items = [
            (r"a row is a permutation: \ 12! = 479{,}001{,}600 of them", WHITE),
            (r"composers searched for rows with properties by hand, \ for weeks", WHITE),
            (r"Lejaren Hiller and Leonard Isaacson, \ \textit{Illiac Suite} \ (1957): \ a string quartet composed by a computer", WHITE),
            (r"its last movement used probabilities and rules: \ the start of algorithmic composition", TUNE),
            (r"Part 65 follows the machines that compose", GREY_A),
        ]
        rows_scene(self, r"rows and machines", items,
                   "Questions like these are made for machines. <bookmark mark='b'/> A row is a permutation of twelve pitch classes: there are almost four hundred and eighty million of them. <bookmark mark='c'/> Composers searched for rows with special properties by hand, sometimes for weeks. <bookmark mark='d'/> In 1957 Lejaren Hiller and Leonard Isaacson at the University of Illinois had a computer compose a string quartet, the Illiac Suite, <bookmark mark='e'/> generating notes and testing them against rules: the beginning of algorithmic composition. <bookmark mark='f'/> Part 65 follows the machines that compose.", marks="cdef")
