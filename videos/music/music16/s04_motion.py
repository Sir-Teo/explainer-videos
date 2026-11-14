from __future__ import annotations

import numpy as np

from videos.music.music16.common import *  # noqa: F403


class Motion(SoundScene):
    def construct(self):
        chapter(self, 3, r"Moving together", r"Why does motion in the same direction merge?", extra=((1990, r"Bregman's \textit{Auditory Scene Analysis}"),))
        self.four()
        self.fate()
        self.counts()

    # ------------------------------------------------------------------
    def four(self):
        d = load("motions")
        c = clip("motions.four")
        order = ("parallel", "similar", "contrary", "oblique")
        cells = VGroup()
        for name in order:
            pairs = d["demos"][name]
            up = [(u, 2.0 * k, 2.0) for k, (u, l) in enumerate(pairs)]
            lo = [(l, 2.0 * k, 2.0) for k, (u, l) in enumerate(pairs)]
            g = duet([up, lo], colors=(MOTION_C[name], WHITE), width=2.6, height=2.4, lo=52, hi=80, thick=0.14)
            txt = {"parallel": r"the same direction, \ the same interval", "similar": r"the same direction, \ different intervals",
                   "contrary": r"opposite directions", "oblique": r"one voice holds"}[name]
            cells.add(VGroup(label(name, font_size=30, color=MOTION_C[name]), g, label(txt, font_size=20, color=GREY_A)).arrange(DOWN, buff=0.25))
        cells.arrange(RIGHT, buff=0.55).move_to(UP * 0.2)
        with self.voiceover(
            "Two voices can move in four ways relative to each other. Both in the same direction, by "
            "the same interval, so that the interval between them stays the same: parallel motion. "
            "Both in the same direction by different amounts: similar motion. In opposite directions: "
            "contrary motion. Or one moves while the other holds still: oblique. Listen to each."
        ):
            self.play(LaggedStart(*[FadeIn(x) for x in cells], lag_ratio=0.3), run_time=3.0)
        with self.listen(c) as snd:
            window(snd, r"parallel, \ similar, \ contrary, \ oblique", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i, name in enumerate(order):
                g = cells[i][1]
                sing_voice(snd, g.notes[0] + g.notes[1], d["times"][name] + d["times"][name], base=WHITE, hot=MOTION_C[name])
                pulse(snd, cells[i][0], d["starts"][name], d["starts"][order[i + 1]] - 0.3 if i < 3 else c.duration, buff=0.1)
        for i, name in enumerate(order):
            for n in cells[i][1].notes[0]:
                n.set_fill(MOTION_C[name])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fate(self):
        dots = VGroup(*[Dot([x, y, 0], radius=0.06, color=GREY_B) for x in np.linspace(-5.5, -1.5, 9) for y in np.linspace(-1.5, 1.5, 7)])
        movers = VGroup(*[dots[i] for i in (3, 11, 19, 27, 35, 43)])
        head = label(r"the law of common fate", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
        text = VGroup(label(r"things that move together \\ are seen as one thing", font_size=30, color=WHITE),
                      label(r"for the ear: \\ voices that move together \\ are heard as one voice", font_size=30, color=TUNE),
                      label(r"Huron: \ ``pitch co-modulation''", font_size=24, color=GREY_B)).arrange(DOWN, buff=0.45).move_to(RIGHT * 3.2)
        with self.voiceover(
            "Why should moving together matter? Look at a field of dots. <bookmark mark='a'/> When some "
            "of them move together, in the same direction at the same speed, you see them at once as a "
            "single shape. Psychologists call it the law of common fate, and Albert Bregman showed in "
            "his book of 1990 that hearing uses the same law. <bookmark mark='b'/> Sounds whose pitches "
            "rise and fall together are taken to come from one source. Huron calls it pitch "
            "co-modulation. Put that beside tonal fusion: two voices a fifth apart already half fuse; "
            "make them move together, and they become one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dots), FadeIn(text[0]))
            vo.wait_until("a")
            for _ in range(2):
                self.play(movers.animate.shift(UP * 0.6 + RIGHT * 0.25), run_time=0.7)
                self.play(movers.animate.shift(DOWN * 0.6 - RIGHT * 0.25), run_time=0.7)
            movers.set_color(TUNE)
            vo.wait_until("b")
            self.play(FadeIn(text[1]), FadeIn(text[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counts(self):
        d = load("motions")
        order = ("contrary", "similar", "parallel", "oblique")
        rows = [(name, 100 * d["valid"][name], 100 * d["consonant_only"][name]) for name in order]
        g = VGroup(Line([-5.0, 0, 0], [5.0, 0, 0], color=DIM, stroke_width=2))
        w = 10.0 / 4
        groups = VGroup()
        for k, (name, a, b) in enumerate(rows):
            x = (k + 0.5) * w - 5.0
            ba = Rectangle(width=0.6, height=max(2.6 * a / 60, 0.02), stroke_width=0, fill_color=TUNE, fill_opacity=0.9).move_to([x - 0.35, max(2.6 * a / 60, 0.02) / 2, 0])
            bb = Rectangle(width=0.6, height=max(2.6 * b / 60, 0.02), stroke_width=0, fill_color=WEAK, fill_opacity=0.9).move_to([x + 0.35, max(2.6 * b / 60, 0.02) / 2, 0])
            groups.add(VGroup(ba, bb, label(f"{a:.0f}", font_size=22, color=WHITE).next_to(ba, UP, buff=0.08), label(f"{b:.0f}", font_size=22, color=GREY_A).next_to(bb, UP, buff=0.08),
                              label(name, font_size=24, color=MOTION_C[name]).move_to([x, -0.3, 0])))
        chart = VGroup(g, groups).move_to(DOWN * 0.9)
        legend = VGroup(VGroup(Square(0.2, stroke_width=0, fill_color=TUNE, fill_opacity=0.9), label(r"lines that obey Fux's rules", font_size=22, color=GREY_A)).arrange(RIGHT, buff=0.12),
                        VGroup(Square(0.2, stroke_width=0, fill_color=WEAK, fill_opacity=0.9), label(r"lines that are only consonant", font_size=22, color=GREY_A)).arrange(RIGHT, buff=0.12)).arrange(RIGHT, buff=0.8).next_to(chart, UP, buff=0.4)
        head = label(r"how often each motion occurs, \ in a hundred, \ over Fux's cantus firmus", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The rules push hard toward contrary motion. Take every line that obeys Fux's rules over "
            "the cantus firmus we will meet in chapter five, and count the motions. "
            f"<bookmark mark='a'/> Contrary motion: {say(100 * d['valid']['contrary'])} moves in a "
            f"hundred. Lines that are merely consonant, with no other rules, manage "
            f"{say(100 * d['consonant_only']['contrary'])}. Contrary motion is the one kind that can "
            "never co-modulate. When one voice rises and the other falls, nothing in the sound "
            "suggests a single source."
        ) as vo:
            self.play(FadeIn(head), FadeIn(legend), FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in groups], lag_ratio=0.4), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
