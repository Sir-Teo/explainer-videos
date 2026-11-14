from __future__ import annotations

import numpy as np

from videos.music.music21.common import *  # noqa: F403


class Repetition(SoundScene):
    def construct(self):
        chapter(self, 9, r"Why so much repetition?", r"How much of a tune is a repeat?", extra=((2014, r"Margulis's \textit{On Repeat}"),))
        self.measure()
        self.why()

    # ------------------------------------------------------------------
    def measure(self):
        d = load("repetition")
        vals = sorted([100 * r["share"] for r in d["tunes"]])
        bins = [sum(1 for v in vals if lo <= v < hi) for lo, hi in ((0, 10), (10, 20), (20, 30), (30, 40), (40, 50), (50, 101))]
        ch = columns(bins, [r"0--10", r"10--20", r"20--30", r"30--40", r"40--50", r"50+"], width=7.0, height=2.6, color=WEAK, hot=(), hot_color=TUNE, fmt="{:.0f}", font_size=20).move_to(LEFT * 2.6 + DOWN * 0.5)
        t = label(r"Part 14's tunes: \ how many notes, \ in a hundred, \ belong to a figure heard before", font_size=21, color=GREY_A).next_to(ch, UP, buff=0.4)
        side = VGroup(label(rf"on average {100 * d['mean']:.0f} in a hundred", font_size=26, color=TUNE),
                      label(rf"the same notes shuffled: \ {100 * d['mean_shuffled']:.0f}", font_size=24, color=WHITE),
                      label(rf"the Tune: \ {100 * d['tune']['share']:.0f}", font_size=24, color=EAR),
                      label(r"a figure: \ four notes, \ their intervals and lengths", font_size=20, color=GREY_B)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 4.0 + DOWN * 0.2)
        with self.voiceover(
            "How much does music repeat? Take every tune in Part 14's collection and ask, for each note, whether it "
            "belongs to a four-note figure, the same intervals and the same rhythm, that the tune has already sung "
            f"earlier. <bookmark mark='a'/> On average, {say(round(100 * d['mean']))} notes in a hundred do. "
            f"<bookmark mark='b'/> Shuffle the same notes into a random order and the figure, by chance, repeats for "
            f"about {say(round(100 * d['mean_shuffled']))} in a hundred. <bookmark mark='c'/> The Tune repeats itself "
            f"more than most: {say(round(100 * d['tune']['share']))} notes in a hundred, its last two phrases a copy of its "
            "first two, and its middle phrase sung twice. Prose that repeated a third of its phrases would be thought "
            "broken; music is built that way."
        ) as vo:
            self.play(FadeIn(ch), FadeIn(t), FadeIn(side[3]))
            for mark, r in zip("abc", side[:3]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        rows_ = VGroup(*[label(t, font_size=25, color=c_) for t, c_ in (
            (r"repetition makes a pattern learnable: \ a first hearing becomes a memory", WHITE),
            (r"mere exposure: \ the more often heard, \ the more liked, \ up to a point \ (Zajonc, \ 1968)", WHITE),
            (r"repetition lets the listener move attention: \ from the notes to the shape, \ to the words, \ to the dance", WHITE),
            (r"Margulis, \ 2014: \ repetition is what makes sound feel like music", TUNE),
            (r"and returning to a piece is how most of us listen", GREY_A))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"why repeat?", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Why repeat? <bookmark mark='a'/> Repetition makes a pattern learnable: what was strange at first becomes "
            "something the listener can predict, Part 14's statistical learning. <bookmark mark='b'/> Psychologists "
            "since Robert Zajonc in 1968 have found that mere exposure makes things liked, up to a point, after which "
            "they grow tiresome. <bookmark mark='c'/> And repetition frees attention: once the notes are known, the ear "
            "can follow the shape, the words, the dance. <bookmark mark='d'/> In her 2014 book On Repeat, Elizabeth "
            "Hellmuth Margulis argues that repetition is what makes sounds feel like music at all, the lesson of this "
            "part's opening phrase. <bookmark mark='e'/> And it is how we listen to whole pieces too: most music is heard "
            "many times, and a form is partly a plan for a listener who already knows what is coming."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
