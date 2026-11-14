from __future__ import annotations

import numpy as np

from videos.music.music26.common import *  # noqa: F403

ORDER = ["block", "alberti", "repeated"]
NAME = {"block": r"block chords", "alberti": r"an Alberti bass", "repeated": r"repeated chords"}


class Figures(SoundScene):
    def construct(self):
        chapter(self, 5, r"The accompaniment", r"How do you keep a slow harmony moving?")
        self.three()
        self.counted()

    # ------------------------------------------------------------------
    def three(self):
        d = load("figures")
        c = clip("figures.three")
        rows_ = VGroup()
        rolls = []
        for k in ORDER:
            g = voices_roll([d["melody"], d["acc"][k]], width=7.6, height=1.4, colors=[TUNE, GREY_A], lo=40, hi=84, bar_h=0.08)
            rows_.add(VGroup(label(NAME[k], font_size=21, color=GREY_A), g).arrange(RIGHT, buff=0.5))
            rolls.append(g)
        rows_.arrange(DOWN, buff=0.35, aligned_edge=RIGHT).move_to(DOWN * 0.1 + RIGHT * 0.5)
        head = label(r"one melody, \ one harmony, \ three accompaniments", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The galant harmony changes slowly, a chord every bar or two. The accompaniment keeps it moving. Here is the "
            "Tune's first strain over the same chords three ways: block chords; an Alberti bass, named after Domenico "
            "Alberti, the low note, the high, the middle, the high, in even eighth notes; and repeated chords, a pulse "
            "of eighth notes over a held bass. The harmony is the same; the energy is not."
        ):
            self.play(FadeIn(head), FadeIn(rows_))
        with self.listen(c) as snd:
            window(snd, r"block, \ Alberti, \ repeated", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i, k in enumerate(ORDER):
                st = d["starts"][k]
                flash_voices(snd, rolls[i], [d["melody"], d["acc"][k]], st, d["unit"], colors=[TUNE, GREY_A])
                end = d["starts"][ORDER[i + 1]] - 0.4 if i < 2 else c.duration
                pulse(snd, rows_[i][0], st, end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counted(self):
        d = load("texture")["by"]
        bars = columns([100 * d[c]["accompaniment"] for c in ("haydn", "mozart", "beethoven")], [r"Haydn", r"Mozart", r"Beethoven"], width=5.4, height=2.6, color=TUNE, fmt="{:.0f}", font_size=20)
        bars.move_to(LEFT * 3.2 + DOWN * 0.4)
        t = label(r"bars where a lower voice repeats or breaks one chord, \ in 100", font_size=19, color=GREY_A).next_to(bars, UP, buff=0.35)
        side = VGroup(*[label(s, font_size=23, color=c_) for s, c_ in (
            (r"the quartet's version of the Alberti bass: \ the inner voices pulse", WHITE),
            (r"about a quarter of all bars", WHITE),
            (r"the accompaniment is not filler: \ it is the motor", TUNE),
            (r"in Beethoven it becomes thematic: \ a figure that will itself be developed", EAR))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 6.0))
        side.move_to(RIGHT * 3.4 + DOWN * 0.2)
        with self.voiceover(
            "In a quartet, the second violin and viola do the same job. A program counts the bars in which one of the lower "
            "three instruments plays at least four notes drawn from one chord or one or two pitches: repeated notes, "
            "broken chords. <bookmark mark='a'/> It is the quartet's Alberti bass, the inner voices pulsing. "
            f"<bookmark mark='b'/> About a quarter of all bars have one: {say(round(100 * d['haydn']['accompaniment']))} in a "
            f"hundred in Haydn, {say(round(100 * d['mozart']['accompaniment']))} in Mozart. <bookmark mark='c'/> The "
            "accompaniment is not filler; it is the motor of the style. <bookmark mark='d'/> And in Beethoven an "
            "accompaniment figure often turns out to be the idea the whole movement develops."
        ) as vo:
            self.play(FadeIn(t), FadeIn(bars))
            for mark, r in zip("abcd", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
