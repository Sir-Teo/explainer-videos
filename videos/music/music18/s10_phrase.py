from __future__ import annotations

import numpy as np

from videos.music.music18.common import *  # noqa: F403


class Phrase(SoundScene):
    def construct(self):
        chapter(self, 9, r"A phrase from parts", r"Can schemata make a piece?")
        self.build()
        self.diminution()

    def build(self):
        d = load("schemata")
        c = clip("schemata.phrase")
        g = chord_roll(d["phrase"], width=12.0, height=2.8, lo=38, hi=82, thick=0.1).move_to(DOWN * 0.4)
        brackets = VGroup()
        for name, a, b in d["plan"]:
            x0, x1 = g.xk(a) - 0.22, g.xk(b - 1) + 0.22
            br = VGroup(Line([x0, 1.4, 0], [x1, 1.4, 0], color=GREY_B, stroke_width=2), label(name, font_size=22, color=TUNE).move_to([(x0 + x1) / 2, 1.75, 0]))
            brackets.add(br)
        head = label(r"Do-Re-Mi, \ Prinner \ $\Vert$ \ Fonte, \ Monte, \ Ponte, \ cadence", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Put them in the order Gjerdingen found again and again. Open with a Do-Re-Mi; answer it with a "
            "Prinner. After the double bar, a Fonte, stepping down; a Monte, climbing; a Ponte, a held dominant "
            "that waits for the return; and a cadence. Nothing here was composed, in the usual sense. Every "
            "chord comes from a stock pattern, chained to the next by the shortest way."
        ):
            self.play(FadeIn(head), FadeIn(g), LaggedStart(*[FadeIn(b) for b in brackets], lag_ratio=0.2), run_time=3.0)
        with self.listen(c) as snd:
            window(snd, r"a phrase from schemata", detail=r"a plucked string", corner=DL, tag_corner=DR)
            sing_chords(snd, g, d["phrase_times"])
            for k, (name, a, b) in enumerate(d["plan"]):
                t0 = d["phrase_times"][a]
                t1 = d["phrase_times"][b] - 0.1 if b < len(d["phrase_times"]) else c.duration
                pulse(snd, brackets[k][1], t0, t1, buff=0.06)
        with self.voiceover(
            "It sounds like the music of 1760, without a melody worth the name: the skeleton of a minuet by "
            "nobody. A Neapolitan student would now decorate it, with a tune, rhythms and ornaments, and the "
            "listeners of the time, who knew the schemata as well as the composer did, would hear each one go "
            "by, and enjoy how it was dressed. Gjerdingen's claim is that much of the style really was made "
            "this way, and that this is why so much of it sounds alike."
        ):
            self.wait(0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def diminution(self):
        d = load("more")["diminution"]
        c = clip("more.diminution")
        gp = chord_roll(d["plain"], width=5.0, height=2.6, lo=44, hi=80).move_to(LEFT * 3.4 + DOWN * 0.2)
        gd = chord_roll(d["plain"], width=5.0, height=2.6, lo=44, hi=80).move_to(RIGHT * 3.4 + DOWN * 0.2)
        for col in gd.cols:
            col[0].set_opacity(0.15)
        dots = VGroup()
        for k, notes in enumerate(d["decorated"]):
            x0 = gd.xk(k) - 0.45
            for i, m in enumerate(notes):
                dots.add(Dot([x0 + 0.3 * i, gd.frame.get_bottom()[1] + 2.6 * (m - 44) / 36, 0], radius=0.07, color=VOICE_C[0]))
        lp = label(r"the Prinner, \ plain", font_size=24, color=GREY_A).next_to(gp, UP, buff=0.3)
        ld = label(r"the same, \ its melody decorated", font_size=24, color=GREY_A).next_to(gd, UP, buff=0.3)
        with self.voiceover(
            "How did a skeleton become music? By diminution: the long notes of the schema's melody are divided into "
            "quicker ones that pass between them. Here is the Prinner plain, and then with each melody note "
            "broken into four, the chord notes on the beats and passing notes between."
        ):
            self.play(FadeIn(gp), FadeIn(gd), FadeIn(dots), FadeIn(lp), FadeIn(ld))
        with self.listen(c) as snd:
            window(snd, r"plain, \ then decorated", detail=r"a plucked string", corner=DL, tag_corner=DR)
            sing_chords(snd, gp, d["times"]["plain"])
            flash(snd, list(dots), [d["times"]["decorated"][k // 4] + (k % 4) * 0.31 for k in range(len(dots))], hot=WHITE, base=VOICE_C[0])
            pulse(snd, lp, d["starts"]["plain"], d["starts"]["decorated"] - 0.4, buff=0.1)
            pulse(snd, ld, d["starts"]["decorated"], c.duration, buff=0.1)
        with self.voiceover(
            "Treatises of the time listed hundreds of such figures for each interval, and students copied them out. "
            "The schema is what stays the same; the diminution is what makes one minuet sound different from "
            "another, and it is the same art as the passing notes of Part 17's chorales."
        ):
            self.wait(0.5)
        self.wait(0.4)
        self.clear_scene()

