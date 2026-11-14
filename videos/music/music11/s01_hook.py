from __future__ import annotations

import numpy as np

from videos.music.music11.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.clicks()
        self.listener()
        self.plan()

    # ------------------------------------------------------------------
    def clicks(self):
        d = load("hook")
        c = clip("hook.clicks")
        dots = VGroup(*[Dot(radius=0.16, color=WEAK) for _ in range(d["count"])]).arrange(RIGHT, buff=0.42).move_to(UP * 1.2)
        card = listen_card(r"Sixteen strokes on a wood block. \ Do you hear them all alike, \ or in groups?", width=9.0).move_to(DOWN * 1.4)
        with self.voiceover("Listen to sixteen strokes on a wood block. Do you hear them all alike, or do you hear them in groups?"):
            self.play(LaggedStart(*[FadeIn(x, scale=1.6) for x in dots], lag_ratio=0.08), FadeIn(card), run_time=2.0)
        self.wait(0.8)
        self.play(FadeOut(card))
        with self.listen(c) as snd:
            window(snd, r"sixteen strokes", detail=r"a wood block, \ modelled", corner=DL, tag_corner=DR)
            flash(snd, list(dots), d["times"], base=WEAK, fade=0.3)
            for k in range(d["count"]):
                snd.wait_until(f"c{k}")
                self.play(dots[k].animate(rate_func=there_and_back).scale(1.5), run_time=0.25)
        bars = VGroup(*[Rectangle(width=0.2, height=1.1, stroke_width=0, fill_color=LEVEL, fill_opacity=0.9).move_to(x.get_center() + DOWN * 1.5) for x in dots])
        same = label(rf"every stroke measured: \ the largest difference between any two is {d['spread_db']:.1f} dB", font_size=28, color=LEVEL).next_to(bars, DOWN, buff=0.35)
        with self.voiceover(
            "Most people hear them in pairs. Tick, tock, tick, tock: strong, weak, strong, weak. Some hear "
            "fours. Hardly anyone hears sixteen equal strokes. <bookmark mark='a'/> But here is the "
            "measurement. Every stroke is the same sound, copied sixteen times, the same distance apart. "
            "The difference in level between any two of them is zero. <bookmark mark='b'/> The tick and the "
            "tock were not in the air. You put them there."
        ) as vo:
            self.play(*[x.animate.set_color(TUNE if k % 2 == 0 else WEAK).scale(1.25 if k % 2 == 0 else 0.85) for k, x in enumerate(dots)], run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), FadeIn(same), run_time=2.0)
            vo.wait_until("b")
            self.play(*[x.animate.set_color(WEAK).scale(1 / 1.25 if k % 2 == 0 else 1 / 0.85) for k, x in enumerate(dots)], run_time=1.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def listener(self):
        card = history_card(1894, r"Thaddeus Bolton, \ ``Rhythm''", r"students who heard identical clicks reported them in twos, \ threes and fours; \ how many depended on the speed", width=7.4, font_size=24).to_edge(UP, buff=0.5)
        row = VGroup(*[Dot(radius=0.14, color=WEAK) for _ in range(12)]).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.3)
        odd = SurroundingRectangle(row[4], color=BAD, buff=0.12, stroke_width=3)
        even = SurroundingRectangle(row[5], color=GREY_B, buff=0.12, stroke_width=3)
        l1 = label(r"a change on a ``tick'': \ a larger response from the brain", font_size=26, color=BAD).next_to(row, DOWN, buff=0.6)
        l2 = label(r"the same change on a ``tock'': \ a smaller one", font_size=26, color=GREY_B).next_to(l1, DOWN, buff=0.25)
        claim = label(r"metre is something the listener adds", font_size=36, color=EAR).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "This was first measured in 1894, when Thaddeus Bolton played trains of identical clicks to "
            "students and asked what they heard. They heard groups of two, of three, of four; which one "
            "depended on the speed. <bookmark mark='a'/> In 2003 a group in France looked for the effect "
            "in the brain itself. They made one click in a train a little softer, and recorded the "
            "listener's brain waves. <bookmark mark='b'/> When the soft click fell on an odd-numbered "
            "place, a tick, the brain's response was larger than when it fell on a tock. The listeners "
            "had been told nothing about ticks and tocks. <bookmark mark='c'/> Meter, the pattern of "
            "strong and weak beats, is something a listener adds to sound. This part is about what the "
            "listener adds, and about how musicians lean on it, and play against it."
        ) as vo:
            self.play(FadeIn(card), FadeIn(row))
            xs = [x.get_x() for x in row]
            y = row.get_y() - 0.4
            br = group_brackets(xs, [2] * 6, y, xs[1] - xs[0], color=TUNE)
            self.wait(4.5)
            self.play(FadeIn(br))
            for size in (3, 4):
                self.wait(0.9)
                nb = group_brackets(xs, [size] * (12 // size), y, xs[1] - xs[0], color=TUNE)
                self.play(ReplacementTransform(br, nb), run_time=0.6)
                br = nb
            vo.wait_until("a")
            self.play(FadeOut(br))
            vo.wait_until("b")
            self.play(row[4].animate.set_opacity(0.5), Create(odd), FadeIn(l1))
            self.play(Create(even), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeOut(l1), FadeOut(l2), FadeIn(claim))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        idea = VGroup(label(r"a rhythm is in the sound;", font_size=32, color=GOOD), label(r"its metre is in the listener.", font_size=32, color=EAR)).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.45)
        card = objectives_card([
            r"a pulse, \ and how fast or slow it can be",
            r"metre: \ counting on several levels; \ what makes a beat strong",
            r"cutting the beat in twos and threes",
            r"syncopation, \ measured; \ three against two",
            r"beats of unequal length; \ swing",
            r"and a rhythm that turns into an interval",
        ], title=r"Part 11: \ Rhythm and Meter", font_size=26).move_to(DOWN * 0.5)
        with self.voiceover(
            "In Part 10 we learned to write down how long a note lasts. But a length on a page is only a "
            "ratio. This part is about what happens when those ratios are played in time, to a listener. "
            "<bookmark mark='a'/> We start with a pulse, and find out how fast and how slow a beat can be. "
            "<bookmark mark='b'/> Then meter: counting on several levels at once, and what makes one beat "
            "stronger than another. <bookmark mark='c'/> We cut the beat into twos and threes. "
            "<bookmark mark='d'/> We put notes where the meter is weak, and measure that with a number; "
            "and we set three against two. <bookmark mark='e'/> We meet beats of unequal length, and "
            "swing, which no notation writes. <bookmark mark='f'/> And at the end we take a rhythm and "
            "speed it up, until it stops being a rhythm and becomes an interval we met in Part 1."
        ) as vo:
            self.play(FadeIn(idea))
            self.play(FadeIn(card.head))
            for mark, r in zip("abcdef", card.rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
