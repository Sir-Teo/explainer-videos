from __future__ import annotations

import numpy as np

from videos.music.music15.common import *  # noqa: F403


class Profile(SoundScene):
    def construct(self):
        chapter(self, 1, r"The note that fits", r"How well does each of the twelve notes belong?", extra=((1982, r"Krumhansl and Kessler's probe tones"),))
        self.ratings()
        self.levels()
        self.minor()
        self.quiz()

    # ------------------------------------------------------------------
    def ratings(self):
        d = load("profile")
        bars = note_bars(d["kk_major"], NAMES12, width=9.5, height=2.9, color=WEAK, hot=(0, 4, 7), hot_color=TUNE, fmt="{:.1f}", font_size=22, top=7.0).move_to(DOWN * 1.1)
        yl = label(r"how well the note fits, \ from 1 to 7, \ after music in C major", font_size=22, color=GREY_B).next_to(bars, DOWN, buff=0.15)
        card = history_card(1982, r"Carol Krumhansl and Edward Kessler", r"a key-defining passage, \ then one of the twelve notes; \ listeners rate how well it fits", width=9.0, font_size=24).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The method is called the probe-tone experiment. Krumhansl first tried it in 1979 with "
            "Roger Shepard, and in 1982, with Edward Kessler, she did it properly: a passage that sets "
            "up a key, then one of the twelve notes, and a rating; over and over, for every note. The "
            "tones were built with no definite octave, so that only the note's name could matter. "
            "<bookmark mark='a'/> Here are the average ratings after music in C major. This picture is "
            "called the key profile, and it is one of the most replicated results in the psychology of "
            "music."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(bars), FadeIn(yl))
        self.wait(0.3)
        self.bars, self.yl, self.card = bars, yl, card

    # ------------------------------------------------------------------
    def levels(self):
        d = load("profile")
        bars = self.bars
        g = d["group_means"]
        lv = VGroup(label(rf"1. \ the tonic: \ {g['tonic']:.1f}", font_size=28, color=TUNE), label(rf"2. \ the rest of its triad, \ G and E: \ {g['triad']:.1f}", font_size=28, color=TUNE),
                    label(rf"3. \ the rest of the scale: \ {g['scale']:.1f}", font_size=28, color=WHITE), label(rf"4. \ the five notes outside it: \ {g['outside']:.1f}", font_size=28, color=GREY_B)).arrange(DOWN, buff=0.18, aligned_edge=LEFT).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Read it from the top down, and it has four levels. <bookmark mark='a'/> Highest, alone, the "
            "tonic: C. <bookmark mark='b'/> Then the other two notes of the tonic triad, G and then E. "
            "<bookmark mark='c'/> Then the remaining notes of the scale: F, A, D and B. <bookmark mark='d'/> "
            "And at the bottom, all about equal, the five notes that are not in the scale. So a key is "
            "not just a set of seven notes. It is a hierarchy: one note at the top, two under it, four "
            "under those, five outside. Every chapter of Act Two has been a view of this picture. "
            "Part 12 found the seven; Part 13 the triad; Part 14 the leaning of the rest toward it."
        ) as vo:
            self.play(FadeOut(self.card))
            for mark, k, group in zip("abcd", range(4), ((0,), (7, 4), (5, 9, 2, 11), (1, 3, 6, 8, 10))):
                vo.wait_until(mark)
                self.play(FadeIn(lv[k]), *[Indicate(bars.bars[i], color=WHITE if k >= 2 else TUNE) for i in group], run_time=1.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("profile")["quiz"]
        c = clip("profile.quiz")
        card = listen_card(r"The same four chords, \ three times, \ each followed by a different tone. \ Which tone fits least: \ A, \ B or C?", width=9.4)
        with self.voiceover("Try it on your own ear. The same four chords, three times, each followed by a different tone. Which tone fits least: A, B or C?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        bx = boxes(("A", "B", "C"), buff=0.9, width=2.2, height=1.2, font_size=48).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"A, \ B, \ C", detail=r"four chords, \ then a tone with no octave", corner=DL, tag_corner=DR)
            for k, key in enumerate("ABC"):
                pulse(snd, bx[k], d["starts"][key], d["probe_times"][key] + 1.2, buff=0.1)
        ans = VGroup(*[label(rf"{tex(p)}: \ {r:.1f}", font_size=30, color=EAR if k == 1 else GREY_A).next_to(bx[k], DOWN, buff=0.3) for k, (p, r) in enumerate(zip(d["probes"], d["ratings"]))])
        with self.voiceover(
            "B. The three tones were G, C sharp and E. G and E are in the tonic triad; C sharp is "
            "outside the scale altogether, and listeners rate it lowest of all twelve. If B made you "
            "wince a little, you have a key profile in your head, whether or not you can read a note of "
            "music."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def minor(self):
        d = load("profile")
        bars = note_bars(d["kk_minor"], NAMES12, width=9.5, height=2.9, color=WEAK, hot=(0, 3, 7), hot_color=BLUE, fmt="{:.1f}", font_size=22, top=7.0).move_to(DOWN * 1.0)
        yl = label(r"how well each note fits, \ after music in C minor", font_size=22, color=GREY_B).next_to(bars, DOWN, buff=0.15)
        head = label(r"the same experiment, \ in a minor key", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "They ran the same experiment in minor keys. <bookmark mark='a'/> The shape is the same, "
            "with one change. The tonic is on top; then, almost as high, the minor third, E flat, and "
            "then the fifth; then the rest of the minor scale; then the notes outside it. One profile "
            "for major, one for minor, and each can be slid to start on any of the twelve notes. "
            "Twenty-four keys, from two lists of twelve numbers."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bars), FadeIn(yl))
            self.play(*[Indicate(bars.bars[i], color=BLUE) for i in (0, 3, 7)])
        self.wait(0.4)
        self.clear_scene()
