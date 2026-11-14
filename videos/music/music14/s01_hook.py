from __future__ import annotations

import numpy as np

from videos.music.music14.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.rule()
        self.shuffled()
        self.plan()

    # ------------------------------------------------------------------
    def rule(self):
        d = load("hook")
        demo = roll([0, 9, 7, 5, 4], [1, 1, 1, 1, 2], width=5.0, height=2.2, lines=()).move_to(LEFT * 3.4 + UP * 0.6)
        demo.notes[1].set_fill(EAR)
        leap = Arrow(demo.notes[0].get_right(), demo.notes[1].get_left(), buff=0.08, color=EAR, stroke_width=4, max_tip_length_to_length_ratio=0.15)
        back = Arrow(demo.notes[1].get_right() + DOWN * 0.1, demo.notes[2].get_left() + UP * 0.1, buff=0.05, color=TUNE, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        rule = VGroup(label(r"``after a leap, \ turn back''", font_size=38, color=TUNE), label(r"a rule of melody writing for four hundred years", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.2 + UP * 0.9)
        counts = VGroup(label(rf"{d['tunes']} tunes, \ {d['notes']:,} notes".replace(",", "{,}"), font_size=28, color=WHITE),
                        label(rf"{d['leaps']} leaps of a minor third or more", font_size=28, color=WHITE),
                        label(rf"turned back: \ {100 * d['real']:.0f} in a hundred", font_size=34, color=TUNE)).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Open a textbook on writing melodies and you will find a rule that is four hundred years "
            "old. After a leap, turn back. <bookmark mark='a'/> Jump up, and then step down. Jump down, "
            "and then step up. It sounds like craft: advice that good composers follow. So let us test "
            f"it. This series now has a small library: {say(d['tunes'])} tunes that half the world can "
            f"sing, about nineteen hundred notes. <bookmark mark='b'/> In them there are "
            f"{say(d['leaps'])} leaps of a minor third or more. And when a tune moves on from a leap, it "
            f"turns back {say(100 * d['real'])} times in a hundred. The rule holds."
        ) as vo:
            self.play(FadeIn(rule), FadeIn(demo))
            vo.wait_until("a")
            self.play(GrowArrow(leap))
            self.play(GrowArrow(back))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in counts], lag_ratio=0.8), run_time=6.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shuffled(self):
        d = load("hook")
        c1, c2 = clip("hook.tune"), clip("hook.shuffled")
        t = d["tune"]
        r1 = roll(t["pitches"], t["beats"], width=10.5, height=1.9, lo=-1, hi=10, lines=(0,)).move_to(UP * 1.9)
        r2 = roll(d["shuffled"]["pitches"], d["shuffled"]["beats"], width=10.5, height=1.9, lo=-1, hi=10, lines=(0,), color=CHANCE_C).move_to(DOWN * 0.7)
        l1 = label(r"the Tune", font_size=26, color=GREY_A).next_to(r1, UP, buff=0.15).align_to(r1, LEFT)
        l2 = label(r"the same notes, \ shuffled", font_size=26, color=GREY_A).next_to(r2, UP, buff=0.15).align_to(r2, LEFT)
        with self.voiceover(
            "Now a control experiment. Take the same tunes, and shuffle each one's notes into a random "
            "order. Every note is still there. All of the design is gone. Here is the Tune; and then the "
            "Tune, shuffled."
        ):
            self.play(FadeIn(r1), FadeIn(l1))
            self.play(FadeIn(r2), FadeIn(l2))
        with self.listen(c1) as snd:
            window(snd, r"the Tune", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            sing(snd, r1, d["times"])
        with self.listen(c2) as snd:
            window(snd, r"shuffled", detail=r"the same fourteen notes", corner=DL, tag_corner=DR)
            sing(snd, r2, d["shuffled_times"])
        res = VGroup(label(rf"real tunes: \ {100 * d['real']:.0f} in a hundred", font_size=32, color=REAL_C),
                     label(rf"shuffled tunes: \ {100 * d['chance']:.0f} in a hundred", font_size=32, color=CHANCE_C)).arrange(RIGHT, buff=1.2).to_edge(DOWN, buff=0.75)
        with self.voiceover(
            "Nobody composed that. <bookmark mark='a'/> Yet count the leaps in the shuffled tunes, and "
            f"they turn back {say(100 * d['chance'])} times in a hundred: more often than the real ones "
            "do. Noise obeys the rule better than music does. So whatever this rule is, it is not a "
            "secret of the composer's craft."
        ) as vo:
            self.play(FadeIn(res[0]))
            vo.wait_until("a")
            self.play(FadeIn(res[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        idea = VGroup(label(r"what do melodies do,", font_size=32, color=GREY_A), label(r"and what would they do anyway?", font_size=32, color=TUNE)).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.45)
        card = objectives_card([
            r"a melody is first a shape: \ contour",
            r"how tunes move: \ small steps, \ in a small range, \ in arches",
            r"the leap rule, \ explained: \ regression to the mean",
            r"what chance does not explain: \ tendency tones, \ repetition, \ phrases",
            r"information: \ how many bits in a note",
            r"a model that learns tunes, \ and is surprised in the right places",
        ], title=r"Part 14: \ Melody", font_size=26).move_to(DOWN * 0.5)
        with self.voiceover(
            "That is the question of this part. Part 13 stacked notes into chords; a melody is notes in "
            "a line, and people have been writing rules for it for centuries. We will ask, of each rule: "
            "do melodies really do this? And would they do it anyway, by arithmetic alone? "
            "<bookmark mark='a'/> We begin with what a melody is: before anything else, a shape. "
            "<bookmark mark='b'/> Then how tunes move: in small steps, in a small range, in arches. "
            "<bookmark mark='c'/> Then the leap rule, and why noise obeys it. <bookmark mark='d'/> Then "
            "the things that chance cannot explain: notes that lean, patterns that repeat, phrases that "
            "ask and answer. <bookmark mark='e'/> We measure how much information a note carries. "
            "<bookmark mark='f'/> And we build a model that learns from tunes and is surprised where a "
            "listener is."
        ) as vo:
            self.play(FadeIn(idea))
            self.play(FadeIn(card.head))
            for mark, r in zip("abcdef", card.rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
