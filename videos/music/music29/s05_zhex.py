from __future__ import annotations

import numpy as np

from videos.music.music29.common import *  # noqa: F403


class Zhex(SoundScene):
    def construct(self):
        chapter(self, 4, r"Same intervals, \ different sets", r"Can two different chords have exactly the same intervals?")
        self.ztwo()
        self.zcount()
        self.theorem()
        self.pair()
        self.proof()

    # ------------------------------------------------------------------
    def ztwo(self):
        d = load("zhex")
        c = clip("zhex.z")
        a, b = d["z4"]
        ga = pc_clock(a, radius=1.25, color=TUNE).move_to(LEFT * 3.3 + DOWN * 0.1)
        gb = pc_clock(b, radius=1.25, color=BLUE).move_to(RIGHT * 3.3 + DOWN * 0.1)
        la = label(r"\{0, 1, 4, 6\}", font_size=24, color=TUNE).next_to(ga, UP, buff=0.4)
        lb = label(r"\{0, 1, 3, 7\}", font_size=24, color=BLUE).next_to(gb, UP, buff=0.4)
        cap = label(rf"both: \ interval vector [{''.join(str(x) for x in d['iv_z4'])}]: \ every interval class once", font_size=22, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Two chords with exactly the same intervals but no way to turn one into the other: listen. First zero one four "
            "six, then zero one three seven. Each has six pairs of notes, and in each the six pairs cover all six interval "
            "classes once. Yet no rotation or reflection of the clock carries one onto the other. Forte called such pairs "
            "Z-related."
        ):
            self.play(FadeIn(ga), FadeIn(gb), FadeIn(la), FadeIn(lb), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"two chords, \ one interval vector", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, la, 0.0, 3 * d["unit"] - 0.2, buff=0.08)
            pulse(snd, lb, 3 * d["unit"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def zcount(self):
        d = load("zhex")
        ks = ["4", "5", "6", "7", "8"]
        bars = columns([d["by_size"].get(k, 0) for k in ks], [k + r" notes" for k in ks], width=6.6, height=2.6, color=TUNE, hot=(2,), hot_color=EAR, fmt="{:.0f}", font_size=18)
        bars.move_to(LEFT * 2.6 + DOWN * 0.4)
        t = label(rf"Z-related pairs of set classes: \ {len(d['pairs'])} in all", font_size=21, color=GREY_A).next_to(bars, UP, buff=0.35)
        side = VGroup(*[label(s, font_size=22, color=c_) for s, c_ in (
            (r"one pair of tetrachords, \ the two just heard", WHITE),
            (r"fifteen pairs of hexachords", EAR),
            (r"the counts are symmetric: \ complements of Z-related sets are Z-related", WHITE),
            (r"the same interval content does not mean the same chord", TUNE))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 5.0))
        side.move_to(RIGHT * 3.8 + DOWN * 0.2)
        with self.voiceover(
            "How common are such twins? The program groups every set class by its interval vector. "
            f"<bookmark mark='a'/> There are {say(len(d['pairs']))} Z-related pairs in all, and among four-note chords "
            "only the one pair just heard. <bookmark mark='b'/> Hexachords have fifteen pairs. <bookmark mark='c'/> And the "
            "counts are symmetric, four and eight notes, five and seven, for a reason the next theorem explains. "
            "<bookmark mark='d'/> Interval content does not determine a chord."
        ) as vo:
            self.play(FadeIn(t), FadeIn(bars))
            for mark, r in zip("abcd", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        d = load("zhex")
        e = d["example"]
        ga = pc_clock(e["set"], radius=1.25, color=TUNE).move_to(LEFT * 3.3 + DOWN * 0.1)
        gb = pc_clock(e["complement"], radius=1.25, color=BLUE).move_to(RIGHT * 3.3 + DOWN * 0.1)
        la = label(rf"a hexachord: \ [{''.join(str(x) for x in e['iv'])}]", font_size=22, color=TUNE).next_to(ga, UP, buff=0.4)
        lb = label(rf"its complement: \ [{''.join(str(x) for x in e['iv_c'])}]", font_size=22, color=BLUE).next_to(gb, UP, buff=0.4)
        h = d["hexachord"]
        cap = label(rf"checked on all {h['checked']} hexachords: \ every one has its complement's interval vector", font_size=22, color=EAR).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "Here is the theorem. Take any six pitch classes, and the six that are left over, its complement. "
            "<bookmark mark='a'/> Their interval vectors are always identical. This is Milton Babbitt's hexachord theorem, "
            f"from the 1950s. <bookmark mark='b'/> The program checks all {say(h['checked'])} six-note sets: it holds for every "
            "one. When the complement is in a different set class, the two form one of the fifteen Z-related pairs."
        ) as vo:
            self.play(FadeIn(ga), FadeIn(gb))
            vo.wait_until("a")
            self.play(FadeIn(la), FadeIn(lb))
            vo.wait_until("b")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proof(self):
        rows_ = text_rows([
            (r"take an interval class $i$ \ (not 6). \ Each of the 12 notes has exactly two partners at that distance", WHITE),
            (r"so there are 12 pairs at distance $i$ round the clock, \ each pair: \ inside $S$, \ inside $C$, \ or across", WHITE),
            (r"each note of $S$ has 2 such partners: \ $2 \cdot |S| = 2 \cdot (\text{pairs in } S) + \text{across}$", WHITE),
            (r"the same for $C$; \ with $|S| = |C| = 6$, \ pairs in $S$ = pairs in $C$", TUNE),
            (r"for the tritone, \ half as many pairs, \ the same argument; \ in general $IV(C) - IV(S) = (12 - 2k)(1,1,1,1,1,\tfrac12)$", GREY_A),
        ], font_size=23)
        head = label(r"why it is true", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Why is it true? <bookmark mark='a'/> Fix an interval class, say a minor third. Each of the twelve pitch classes "
            "has exactly two partners a minor third away, one above and one below. <bookmark mark='b'/> So round the clock "
            "there are twelve such pairs, and each lies inside the set, inside the complement, or across. "
            "<bookmark mark='c'/> Count partners from the set's side: its notes have twice six partners, which is twice "
            "the pairs inside the set plus the pairs across. <bookmark mark='d'/> Do the same from the complement's side; "
            "since both have six notes, the pairs inside each must be equal. <bookmark mark='e'/> The tritone works the "
            "same way with half the pairs, and for sets of other sizes the argument gives the difference exactly, which is "
            "why Z-relations come in complementary sizes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pair(self):
        d = load("hexpair")
        c = clip("hexpair.two")
        ga = pc_clock(d["hex"], radius=1.25, color=TUNE).move_to(LEFT * 3.3 + DOWN * 0.1)
        gb = pc_clock(d["comp"], radius=1.25, color=BLUE).move_to(RIGHT * 3.3 + DOWN * 0.1)
        la = label(r"the hexachord", font_size=24, color=TUNE).next_to(ga, UP, buff=0.4)
        lb = label(r"its complement", font_size=24, color=BLUE).next_to(gb, UP, buff=0.4)
        cap = label(r"the same six interval counts; \ not the same chord: \ a Z-related pair", font_size=22, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Hear the example. The hexachord, then the six notes it leaves out, each as one chord. Their interval vectors "
            "are identical, three two two three three two, but they are not the same chord in any transposition or "
            "inversion: this pair is one of the fifteen Z-related hexachord pairs. Do they sound alike to you?"
        ):
            self.play(FadeIn(ga), FadeIn(gb), FadeIn(la), FadeIn(lb), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"a hexachord, \ then its complement", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, la, 0.0, 3.0 * d["unit"], buff=0.08)
            pulse(snd, lb, 3.2 * d["unit"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()
