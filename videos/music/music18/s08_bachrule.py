from __future__ import annotations

import numpy as np

from videos.music.music18.common import *  # noqa: F403


class BachRule(SoundScene):
    def construct(self):
        chapter(self, 7, r"Bach and the rule", r"Did Bach harmonize a scale the Neapolitan way?")
        self.compare()
        self.second()

    def second(self):
        d = load("octave")
        up2 = d["up2"]
        tot = sum(n for _, n in up2)
        rows_ = VGroup(*[VGroup(label(nm, font_size=30, color=TUNE if nm.startswith("vii") else WHITE), label(rf"{n}", font_size=26, color=GREY_A)).arrange(RIGHT, buff=0.5) for nm, n in up2[:4]]).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(LEFT * 3.5 + DOWN * 0.3)
        side = VGroup(label(r"the rule: \ V4/3, \ the dominant seventh with its fifth in the bass", font_size=24, color=WHITE),
                      label(r"vii\textdegree6 is the same chord without its root: \ the rule's, \ in effect", font_size=24, color=TUNE),
                      label(r"ii and ii7: \ D as a root of its own, \ a predominant on the way to V", font_size=24, color=WHITE)).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(RIGHT * 2.4 + DOWN * 0.3)
        head = label(r"over the second degree, \ rising: \ Bach's commonest chords", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Look closer at a degree where they part company: the second, with the bass rising through it. "
            "<bookmark mark='a'/> The rule gives a dominant seventh chord with its fifth in the bass. Bach's commonest "
            "choice there, the diminished triad on seven in first inversion, is that same chord with its root left "
            "out: the rule, in effect. <bookmark mark='b'/> But nearly as often he plays a chord on two itself, two or "
            "two-seven, treating D as a root of its own on the way to the dominant. The rule hears the second degree "
            "as part of the dominant; Bach often hears it as a step before the dominant. Both are good grammar."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def compare(self):
        d = load("octave")
        b = d["bach"]
        up = [b.get(f"up{k}", {"within": 0, "n": 1}) for k in range(1, 8)]
        dn = [b.get(f"down{k}", {"within": 0, "n": 1}) for k in range(7, 0, -1)]
        c1 = columns([100 * x["within"] / max(x["n"], 1) for x in up], [str(k) for k in range(1, 8)], width=5.0, height=2.4, color=WEAK, hot=(6,), hot_color=TUNE, fmt="{:.0f}", font_size=22, top=100).move_to(LEFT * 3.3 + DOWN * 0.5)
        c2 = columns([100 * x["within"] / max(x["n"], 1) for x in dn], [str(k) for k in range(7, 0, -1)], width=5.0, height=2.4, color=WEAK, hot=(0,), hot_color=TUNE, fmt="{:.0f}", font_size=22, top=100).move_to(RIGHT * 3.3 + DOWN * 0.5)
        t1 = label(r"bass rising through the degree", font_size=22, color=GREY_A).next_to(c1, UP, buff=0.35)
        t2 = label(r"bass falling through the degree", font_size=22, color=GREY_A).next_to(c2, UP, buff=0.35)
        head = VGroup(label(r"where Bach's bass moves by step: \ is his chord the rule's?", font_size=28, color=GREY_A),
                      label(r"in a hundred, \ by degree \ (a note left out still counts)", font_size=20, color=GREY_B)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.4)
        cap = label(rf"over {d['n']} stepwise beats: \ the rule's chord {100 * d['within']:.0f} times in a hundred; \ its exact figure {100 * d['agree']:.0f}", font_size=24, color=TUNE).to_edge(DOWN, buff=0.45)
        u7 = up[6]
        with self.voiceover(
            "Did Bach harmonize a moving bass the way Naples taught? He was not a Neapolitan, and the rule was "
            "a teaching device. Take every place in his major chorales where the bass passes by step through a "
            "note, and ask whether his chord there belongs to the rule's chord for that degree and direction. "
            "<bookmark mark='a'/> Rising through the seventh degree, the leading note, most often: "
            f"{say(round(100 * u7['within'] / u7['n']))} times in a hundred, a dominant chord over its third. "
            "<bookmark mark='b'/> Falling through the third and the seventh, often. Elsewhere, much less: on "
            "the second degree Bach often prefers a chord the rule does not offer. "
            f"<bookmark mark='c'/> Over all {say(d['n'])} such beats, his chord is the rule's "
            f"{say(round(100 * d['within']))} times in a hundred. The rule describes a common core of the style, "
            "the part a beginner can learn first; Bach's harmony is richer, and freer, than the core."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(c1), FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeIn(c2), FadeIn(t2))
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()
