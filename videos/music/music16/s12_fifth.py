from __future__ import annotations

import numpy as np

from videos.music.music16.common import *  # noqa: F403
from videos.music.music16.s09_second import species_scene


class Fifth(SoundScene):
    def construct(self):
        chapter(self, 11, r"Florid, \ and independent", r"How independent are two voices?")
        self.hear()
        self.table()
        self.principles()

    def hear(self):
        d = load("species")["5"]
        species_scene(self, 5,
                      "Fifth species, called florid, mixes the others freely: halves, quarters, "
                      "syncopations and suspensions, in whatever order makes the best line. It is the "
                      "nearest thing in Fux to real music. Here is one over the same cantus.",
                      "Florid counterpoint is where Fux leaves his student: a free melody, with every "
                      "dissonance accounted for, over a melody that is not its own. Bach's two-part "
                      "Inventions are that, with both voices free.",
                      r"pink: \ dissonances")

    def table(self):
        d = load("independence")["rows"]
        cols = [("together", r"notes begin together"), ("fused", r"fused moments"), ("contrary", r"contrary motion"), ("parallel", r"parallel motion")]
        xs = (-6.2, -2.4, 0.2, 2.6, 5.0)
        head = VGroup(label(r"", font_size=22, color=GREY_B).move_to([xs[0], 2.6, 0], aligned_edge=LEFT))
        for (k, t), x in zip(cols, xs[1:]):
            head.add(label(t, font_size=22, color=GREY_B).move_to([x, 2.6, 0]))
        rows = VGroup()
        for i, r in enumerate(d):
            y = 1.9 - 0.65 * i
            row = VGroup(label(r["name"], font_size=26, color=EAR if i == 0 else WHITE).move_to([xs[0], y, 0], aligned_edge=LEFT))
            for (k, t), x in zip(cols, xs[1:]):
                row.add(label(rf"{100 * r[k]:.0f}\%", font_size=26, color=TUNE if (k == 'together' and i == 4) or (k == 'fused' and i > 0) else GREY_A).move_to([x, y, 0]))
            rows.add(row)
        with self.voiceover(
            "Now measure every texture in this part the same way, over the same cantus: organum, and "
            "the five species. <bookmark mark='a'/> Organum: every note begins together; every move "
            "lands on a fused interval with both voices moving together; all the motion is parallel. "
            "It is designed to be one voice. <bookmark mark='b'/> First species: still every note "
            "together, but fused moments gone, and contrary motion nearly everywhere. "
            "<bookmark mark='c'/> Then, species by species, the onsets come apart: half together, a "
            "quarter, almost none. The rules attack the three cues of fusion one after another: "
            "first the fused intervals, then the common motion, then the common onsets."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[2:]], lag_ratio=0.5), run_time=4.0)
        self.wait(0.4)
        self.clear_scene()

    def principles(self):
        rows = VGroup(label(r"1. \ toneness: \ use tones with clear pitch", font_size=24, color=WHITE), label(r"2. \ minimum masking: \ space the voices to avoid one critical band", font_size=24, color=WHITE),
                      label(r"3. \ tonal fusion: \ avoid unisons, \ octaves and fifths", font_size=24, color=TUNE), label(r"4. \ pitch proximity: \ move by small steps", font_size=24, color=WHITE),
                      label(r"5. \ pitch co-modulation: \ avoid moving together", font_size=24, color=TUNE), label(r"6. \ onset synchrony: \ avoid starting together", font_size=24, color=TUNE)).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(UP * 0.1)
        head = label(r"Huron, \ 2001: \ six principles of hearing, \ and the rules that follow from them", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        cap = label(r"the rules are not taste. \ They are acoustics, \ and listening.", font_size=30, color=TUNE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Huron's paper of 2001 put it in one table. Start from six principles of hearing, each "
            "established in the laboratory. <bookmark mark='a'/> Use tones with clear pitches. Keep the "
            "voices out of each other's critical bands, the masking of Part 4. Avoid the intervals "
            "that fuse. Move by small steps, so each line stays one stream, as in Part 14. Avoid "
            "moving together. Avoid starting together. <bookmark mark='b'/> From these, with a goal, "
            "to keep the voices audible as independent lines, he derived nearly all the traditional "
            "rules of voice leading, and some that textbooks had never stated but composers had obeyed."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.7), run_time=9.0)
            vo.wait_until("b")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()
