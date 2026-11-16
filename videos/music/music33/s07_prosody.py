from __future__ import annotations

import numpy as np

from videos.music.music33.common import *  # noqa: F403


def sl_blocks(word, unit=0.32, h=0.28, short_col=BLUE, long_col=TUNE):
    g = VGroup()
    x = 0.0
    for ch in word:
        w = unit * (2 if ch in "LH1" else 1)
        g.add(Rectangle(width=w - 0.05, height=h, stroke_width=0, fill_color=long_col if ch in "LH1" else short_col, fill_opacity=0.95).move_to([x + w / 2, 0, 0]))
        x += w
    return g


class Prosody(SoundScene):
    def construct(self):
        chapter(self, 6, r"Pingala's syllables", r"How many rhythms last five beats?")
        self.count()
        self.fibonacci()
        self.meru()
        self.yamata()
        self.history()

    # ------------------------------------------------------------------
    def count(self):
        d = load("prosody")
        c = clip("prosody.five")
        rows_ = VGroup(*[VGroup(label(r"\texttt{" + r + "}", font_size=18, color=GREY_A), sl_blocks(r)).arrange(RIGHT, buff=0.4) for r in d["rhythms5"]])
        rows_.arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(LEFT * 2.6 + DOWN * 0.3)
        for r in rows_:
            r[1].align_to(rows_[0][1], LEFT)
        side = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"Sanskrit verse: \ light syllables of one beat, \ heavy of two", WHITE),
            (r"how many patterns fill five beats? \ eight", TUNE),
            (r"each ends in a light syllable \ (the patterns of four beats, \ plus one) \ or a heavy \ (three beats, \ plus two)", WHITE),
            (r"so the count for n is the counts for n -- 1 and n -- 2 added", GREY_A))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 5.4)).move_to(RIGHT * 3.6)
        head = label(r"light and heavy syllables filling five beats", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Sanskrit verse is built from light syllables, one mora long, and heavy ones, two morae long in this metrical model. Indian prosodists "
            "asked how many patterns fill a given number of beats. <bookmark mark='a'/> For five beats there are eight, listed "
            "here. <bookmark mark='b'/> Every pattern ends either in a light syllable, after a pattern of four beats, or in a "
            "heavy one, after a pattern of three. <bookmark mark='c'/> So the count for five is the count for four plus the "
            "count for three: five plus three. Listen to all eight, the heavy syllables louder."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_), FadeIn(side[0]))
            for mark, r in zip("abc", side[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        with self.listen(c) as snd:
            window(snd, r"the eight rhythms of five beats", detail=r"Part 11's woodblock", corner=DL, tag_corner=DR)
            for i, t0 in enumerate(d["times5"]):
                end = d["times5"][i + 1] - 0.2 if i + 1 < len(d["times5"]) else c.duration
                pulse(snd, rows_[i], t0, end, buff=0.05)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fibonacci(self):
        d = load("prosody")
        cnt = d["counts"][:12]
        bars = columns(cnt, [str(i + 1) for i in range(len(cnt))], width=8.4, height=3.0, color=TUNE, fmt="{:.0f}", font_size=16).move_to(DOWN * 0.2)
        xl = label(r"beats", font_size=19, color=GREY_A).next_to(bars, DOWN, buff=0.35)
        head = label(r"1, \ 2, \ 3, \ 5, \ 8, \ 13, \ 21 ... \ : \ the counts of rhythms", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Count for every length and the numbers are one, two, three, five, eight, thirteen, twenty-one: each the sum of "
            "the two before. Europe knows them as the Fibonacci numbers, after Leonardo of Pisa, who wrote them down in 1202 "
            "in a problem about rabbits. Indian scholars had them for metre centuries earlier: Virahanka about the seventh "
            "century, then Gopala and Hemachandra, all counting the rhythms of verse."
        ):
            self.play(FadeIn(head), FadeIn(bars), FadeIn(xl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def yamata(self):
        d = load("prosody")
        syl = VGroup(*[VGroup(label(s.replace("ā", r"\=a"), font_size=24, color=TUNE if b else BLUE), label("H" if b else "L", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.12)
                       for s, b in zip(d["syllables"], d["bits"])]).arrange(RIGHT, buff=0.35).move_to(UP * 1.3)
        wins = VGroup(*[label(w, font_size=20, color=WHITE) for w in d["windows"]]).arrange(RIGHT, buff=0.45).move_to(DOWN * 0.3)
        names = label(r"the eight three-syllable feet, \ each once: \ ya-gana, \ ma-gana, \ ta-gana ...", font_size=21, color=GREY_A).next_to(wins, DOWN, buff=0.45)
        cap = label(rf"{d['distinct']} different windows of three in ten syllables: \ a de Bruijn sequence, \ centuries before de Bruijn \ (1946)", font_size=21, color=EAR).to_edge(DOWN, buff=0.5)
        head = label(r"a mnemonic: \ \textit{yam\=at\=ar\=ajabh\=anasalag\=a\d{h}}", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        c = clip("prosody.yamata")
        with self.voiceover(
            "Indian teachers also had a memory aid for the eight patterns of three syllables. The nonsense word ya-mā-tā-rā-"
            "ja-bhā-na-sa-la-gā, read as light and heavy syllables. <bookmark mark='a'/> Slide a window of three syllables "
            "along it: ya-mā-tā is light, heavy, heavy; mā-tā-rā is heavy, heavy, heavy; and so on. <bookmark mark='b'/> The "
            "eight windows are the eight possible feet, each exactly once. Mathematicians now call a string like this a de "
            "Bruijn sequence, after a paper of 1946; the mnemonic is far older."
        ) as vo:
            self.play(FadeIn(head), FadeIn(syl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(w) for w in wins], lag_ratio=0.25), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(names), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"ya-m\=a-t\=a-r\=a-ja-bh\=a-na-sa-la-g\=a, \ twice", detail=r"Part 11's woodblock", corner=DL, tag_corner=DR)
            for j, t0 in enumerate(d["times"]):
                k = j % len(syl)
                pulse(snd, syl[k], t0, t0 + d["pulse"] * (2 if d["bits"][k] else 1) - 0.03, buff=0.05)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"Pi\.ngala's \textit{Chandah\'s\=astra} \ (date uncertain; often late centuries BCE): \ metres listed as binary patterns", WHITE),
            (r"its rules for listing and numbering the patterns amount to binary numbers", WHITE),
            (r"Halayudha's commentary \ (10th century): \ the triangle of binomial coefficients, \ the \textit{meru}", WHITE),
            (r"rhythm was one of the first places combinatorics was done at all", TUNE),
            (r"Part 34 hears the rhythms of Indian music in their own terms", GREY_A),
        ]
        rows_scene(self, r"combinatorics began here", items,
                   "This tradition is old. <bookmark mark='b'/> Pingala's treatise on metre, of uncertain date, often placed in the last few centuries BCE, lists "
                   "metres as patterns of light and heavy. <bookmark mark='c'/> Its rules for listing and numbering the patterns "
                   "amount to binary numbers. <bookmark mark='d'/> The commentator Halayudha, in the tenth century, drew the "
                   "triangle of binomial coefficients, the meru, to count patterns with a given number of heavy syllables. "
                   "<bookmark mark='e'/> Rhythm was one of the first places anyone did combinatorics at all. "
                   "<bookmark mark='f'/> Part 34 hears the rhythms of Indian music in their own terms.", marks="cdef")

    # ------------------------------------------------------------------
    def meru(self):
        d = load("meru")
        rows_ = VGroup()
        for n, r in enumerate(d["rows"]):
            rows_.add(VGroup(label(rf"{n + 1} beats:", font_size=18, color=GREY_A), *[label(str(x), font_size=22, color=TUNE if j == 0 else WHITE) for j, x in enumerate(r)],
                             label(rf"= \ {sum(r)}", font_size=18, color=EAR)).arrange(RIGHT, buff=0.35))
        rows_.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(LEFT * 1.8 + DOWN * 0.2)
        side = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"split the count by how many heavy syllables a pattern has", WHITE),
            (r"the numbers are binomial coefficients: \ the rows of Halayudha's \textit{meru}, \ read on a slant", TUNE),
            (r"each row's total is a Fibonacci number", EAR))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 4.6)).move_to(RIGHT * 4.3)
        head = label(r"patterns with 0, \ 1, \ 2 ... \ heavy syllables", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Split each count by how many heavy syllables the patterns contain. <bookmark mark='a'/> For eight beats: one "
            "pattern with no heavy syllable, seven with one, fifteen with two, ten with three, one with four. These are "
            "binomial coefficients, the numbers in the triangle the commentator Halayudha called the meru, read along a "
            "slanting line. <bookmark mark='b'/> And each row adds up to a Fibonacci number: the shallow diagonals of the "
            "triangle sum to Fibonacci, a fact found here first through rhythm."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
