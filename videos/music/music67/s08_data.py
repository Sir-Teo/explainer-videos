from __future__ import annotations

import numpy as np

from videos.music.music67.common import *  # noqa: F403


class Data(SoundScene):
    def construct(self):
        chapter(self, 7, r"Datasets, \ leakage and agreement", r"When does a benchmark measure what it claims?")
        self.leakage()
        self.series()
        self.dupes()
        self.agreement()
        self.tappers()
        self.taps_heard()

    # ------------------------------------------------------------------
    def leakage(self):
        d = load("leakage")
        L, H = np.array(d["leaky"]), np.array(d["honest"])
        ax = frame_axes(width=7.0, height=3.0, xlo=-0.5, xhi=9.5, ylo=2.8, yhi=4.4, center=DOWN * 0.4 + LEFT * 1.2)
        dl = VGroup(*[Dot(ax.to(i, v), radius=0.08, color=EAR) for i, v in enumerate(L)])
        dh = VGroup(*[Dot(ax.to(i, v), radius=0.08, color=TUNE) for i, v in enumerate(H)])
        xl = label(r"ten random splits", font_size=14, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"bits per note on the held-out chorales \ (lower looks better)", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        side = VGroup(label(rf"split by chorale: \ {L.mean():.2f} on average", font_size=17, color=EAR),
                      label(rf"split by hymn tune: \ {H.mean():.2f}", font_size=17, color=TUNE),
                      label(rf"in the first chorale split, \ {d['shared_in_first']} of {d['test_size']} held-out chorales \ share their tune with a training chorale", font_size=15, color=GREY_A)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(RIGHT, buff=0.4)
        head = label(r"a leak, \ measured", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Part 65 split Bach's chorales by hymn tune, because Bach harmonized many tunes twice. What if it had not? "
            "<bookmark mark='a'/> Split the chorales at random, ten times, and the order-two chain seems to need "
            f"{say(L.mean(), 2)} bits a note. <bookmark mark='b'/> Split by tune, {say(H.mean(), 2)}. The leaky split looks "
            f"better by more than half a bit, a bigger gain than any method in Part 65 achieved over another, because "
            f"{say(d['shared_in_first'])} of its {say(d['test_size'])} held-out chorales were tunes it had already learnt."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(dl), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(dh), FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def series(self):
        items = [
            (r"Part 63: \ a classifier learnt a mains hum; \ split by excerpt instead of clip, \ a second leak hid its chance-level skill", WHITE),
            (r"Part 64: \ a separator trained on phrases the Tune repeats scored 8.5 dB; \ honestly, \ 6.9", WHITE),
            (r"Part 65: \ an order-8 chain sounded most like Bach because it was Bach", WHITE),
            (r"GTZAN \ (Sturm, \ 2013): \ repeated excerpts, \ mislabels and distortions in a dataset used in a hundred papers", WHITE),
            (r"the rule: \ split by the unit that can repeat, \ and check what the test shares with the training data", TUNE),
        ]
        rows_scene(self, r"this series' leaks", items,
                   "This series has met leaks before, and said so. <bookmark mark='b'/> In Part 63, a classifier learnt a mains hum, "
                   "and a split by excerpt rather than by clip hid how little else it knew. <bookmark mark='c'/> In Part 64, a "
                   "separator trained on phrases the Tune repeats scored eight and a half decibels; honestly, six point nine. "
                   "<bookmark mark='d'/> In Part 65, an order-eight chain sounded most like Bach because it was Bach. "
                   "<bookmark mark='e'/> And Bob Sturm found, in 2013, repeated excerpts, mislabels and distortions in GTZAN, a "
                   "dataset used in a hundred papers. <bookmark mark='f'/> The rule: split by the unit that can repeat, and check "
                   "what the test shares with the training data.", marks="bcdef")

    # ------------------------------------------------------------------
    def agreement(self):
        items = [
            (r"labels come from annotators, \ and annotators disagree: \ on chords, \ on beats, \ on where a section ends", WHITE),
            (r"Part 62: \ two people annotating the same song's chords or structure often differ at the boundaries", WHITE),
            (r"a model cannot be measured more finely than its annotators agree: \ their agreement is a ceiling", WHITE),
            (r"so report agreement between annotators beside every score, \ and keep more than one annotation", TUNE),
        ]
        rows_scene(self, r"how far people agree", items,
                   "The labels themselves are uncertain. <bookmark mark='b'/> They come from annotators, and annotators disagree: on "
                   "chords, on beats, on where a section ends. <bookmark mark='c'/> Part 62 met this: two people annotating the same "
                   "song often differ at the boundaries. <bookmark mark='d'/> A model cannot be measured more finely than its "
                   "annotators agree; their agreement is a ceiling. <bookmark mark='e'/> So report the agreement between annotators "
                   "beside every score, and keep more than one annotation.", marks="bcde")

    # ------------------------------------------------------------------
    def tappers(self):
        d = load("tappers")
        rows_ = VGroup(
            label(r"two simulated people tap the beat of the same performance, \ a little early, \ each with their own jitter", font_size=19, color=WHITE),
            label(rf"the second sometimes taps the off-beat \ ({100 * d['offbeat_share']:.0f}\% of taps)", font_size=19, color=WHITE),
            label(rf"each against the beats as played: \ F = {d['a_vs_played']:.2f} and {d['b_vs_played']:.2f}", font_size=20, color=TUNE),
            label(rf"against each other: \ F = {d['a_vs_b']:.2f}", font_size=20, color=EAR),
            label(r"if they were the annotators, \ no tracker could be shown to beat about that", font_size=18, color=GREY_A),
        ).arrange(DOWN, buff=0.35)
        head = label(r"an agreement ceiling, \ computed", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the ceiling computed. <bookmark mark='a'/> Two simulated people tap the beat of one performance, a little "
            "early as people do, each with their own jitter, <bookmark mark='b'/> and the second sometimes taps the off-beat. "
            f"<bookmark mark='c'/> Scored against the beats as played, with Part 62's seventy-millisecond window, they reach "
            f"{say(d['a_vs_played'], 2)} and {say(d['b_vs_played'], 2)}. <bookmark mark='d'/> Against each other, "
            f"{say(d['a_vs_b'], 2)}. <bookmark mark='e'/> If they were a dataset's annotators, no beat tracker could be shown to "
            "do better than about that."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dupes(self):
        d = load("dupes")
        items = [
            (rf"this series' own library: \ {d['variations_with_copies']} of its {d['variations']} Variations have their audio again in another clip", WHITE),
            (r"Part 63 found them by fingerprint, \ and counted a match to either copy as right", WHITE),
            (r"harmless there; \ in a training set and a test set, \ the same audio twice is a leak", WHITE),
            (r"so a dataset's first audit is for duplicates, \ near-duplicates and versions of one work", TUNE),
        ]
        rows_scene(self, r"duplicates, \ at home", items,
                   f"This series has duplicates of its own. <bookmark mark='b'/> Of its {say(d['variations'])} Variations, "
                   f"{say(d['variations_with_copies'])} have their audio again in another clip of the library, because a part reused "
                   "a sound. <bookmark mark='c'/> Part 63 found them by fingerprint and counted a match to either copy as right. "
                   "<bookmark mark='d'/> Harmless there; but in a training set and a test set, the same audio twice is a leak. "
                   "<bookmark mark='e'/> So a dataset's first audit is for duplicates, near-duplicates, and versions of one work.",
                   marks="bcde")

    # ------------------------------------------------------------------
    def taps_heard(self):
        d = load("tapsheard")
        c = clip("taps.two")
        boxes = choice_boxes([r"the first tapper", r"the second tapper"], width=3.8, height=0.9, buff=0.9, size=19).move_to(UP * 0.6)
        note = label(r"both tap a little early; \ the second, \ more loosely, \ and now and then on the off-beat", font_size=17, color=GREY_A).next_to(boxes, DOWN, buff=0.6)
        head = label(r"two annotators, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the two tappers: the opening of that performance, first with one person's taps as clicks, then with the other's."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two tappers", kind="physical model", detail=r"Part 38's piano; \ clicks", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        with self.voiceover("Both are plausible annotations of the beat; neither is the truth, and a model scored against either inherits its looseness."):
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()
