from __future__ import annotations

import numpy as np

from videos.music.music16.common import *  # noqa: F403


class Fusion(SoundScene):
    def construct(self):
        chapter(self, 2, r"When two notes become one", r"Why do some intervals fuse?", extra=((1890, r"Stumpf's tonal fusion"),))
        self.shared()
        self.quiz()

    # ------------------------------------------------------------------
    def shared(self):
        d = load("fusion")
        ch = columns([100 * x for x in d["strength"]], d["names"], width=11.0, height=2.8, color=WEAK, hot=(0, 5, 7, 12), hot_color=TUNE, fmt="{:.0f}", font_size=22, top=100).move_to(DOWN * 0.9)
        yl = label(r"of the upper note's harmonics, \ the share that are also harmonics of the lower note \ (\%, \ just ratios)", font_size=22, color=GREY_B).next_to(ch, DOWN, buff=0.15)
        head = label(r"Carl Stumpf, \ 1890: \ some pairs of notes are heard as one", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Why would two voices merge? In 1890 Carl Stumpf asked listeners a simple question about "
            "two notes played together: one tone, or two? Listeners without training often heard an "
            "octave as a single tone, a fifth quite often, a fourth less often, and thirds and sixths "
            "less often still. Stumpf called this tonal fusion. <bookmark mark='a'/> Part 5 gives the reason. "
            "A note is a whole series of harmonics. Above a C, every harmonic of the C an octave higher "
            "is already a harmonic of the lower C: all of them, a hundred in a hundred. For the fifth, "
            "half. For the fourth, a third. For a major third, a quarter; for a minor second, one in "
            "fifteen. The more of its harmonics a note shares with its partner, the more the ear takes "
            "the two for one harmonic series, which means one sound."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ch), FadeIn(yl))
            self.play(*[Indicate(ch.bars[i], color=TUNE) for i in (12, 7, 5)])
        cap = label(r"the octave, \ the fifth, \ the fourth: \ the intervals of organum, \ and the ones that fuse", font_size=28, color=TUNE).next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "So the intervals that fuse most are the octave, the fifth and the fourth: exactly the "
            "intervals of organum, and exactly the ones that the later rules single out, as perfect "
            "consonances, for special care."
        ):
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("fusion")
        c = clip("fusion.quiz")
        tune = load("organum")["tune"]
        third = d["quiz"]["third"]
        b = load("organum")["beats"]
        on = np.concatenate([[0.0], np.cumsum(b)])[:-1]
        mk = lambda ps: [(p, a, w) for p, a, w in zip(ps, on, b)]                 # noqa: E731
        card = listen_card(r"One phrase, \ with a second voice moving exactly with it, \ twice. \ In which is it easier to hear two voices: \ A or B?", width=9.6)
        with self.voiceover("Try it. One phrase, with a second voice moving exactly with it, twice. In which is it easier to hear two separate voices: A or B?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        gA = duet([mk(tune), mk([p - 12 for p in tune])], colors=(WHITE, WHITE), width=5.0, height=2.6, lo=44, hi=72, thick=0.13).move_to(LEFT * 3.2 + UP * 0.3)
        gB = duet([mk(tune), mk(third)], colors=(WHITE, WHITE), width=5.0, height=2.6, lo=44, hi=72, thick=0.13).move_to(RIGHT * 3.2 + UP * 0.3)
        la, lb = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.2), label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.2)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", kind="synthesized", detail=r"organ tones", corner=DL, tag_corner=DR)
            for nts in gA.notes:
                sing_voice(snd, nts, d["times"]["A"], base=WHITE, hot=TUNE)
            for nts in gB.notes:
                sing_voice(snd, nts, d["times"]["B"], base=WHITE, hot=TUNE)
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.12)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.12)
        ans = VGroup(label(r"A: \ parallel octaves: \ one voice, \ thicker", font_size=26, color=GREY_A).next_to(gA, DOWN, buff=0.35),
                     label(r"B: \ parallel thirds: \ two voices, \ close together", font_size=26, color=TUNE).next_to(gB, DOWN, buff=0.35))
        with self.voiceover(
            "B, for most listeners. In A the second voice was an octave below the first, and the two "
            "melted into one darker voice: a pipe organ does this on purpose, with stops that sound an "
            "octave apart. In B the second voice was a third below, and although it moved exactly with "
            "the first, you could follow either. Thirds and sixths keep their identity, which is why the "
            "rules allow a few of them in a row, and forbid even two perfect fifths."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()
