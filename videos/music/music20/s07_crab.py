from __future__ import annotations

import numpy as np

from videos.music.music20.common import *  # noqa: F403


class Crab(SoundScene):
    def construct(self):
        chapter(self, 6, r"The crab canon", r"Can a melody be its own accompaniment, backwards?", extra=((1979, r"Hofstadter's \textit{Gödel, Escher, Bach}"),))
        self.idea()
        self.count()
        self.hear()

    # ------------------------------------------------------------------
    def idea(self):
        d = load("crab")
        n = len(d["melody"])
        dots_a = VGroup(*[Dot([-5.0 + 10.0 * k / (n - 1), 1.2, 0], radius=0.12, color=VOICE_C[0]) for k in range(n)])
        dots_b = VGroup(*[Dot([-5.0 + 10.0 * k / (n - 1), -0.6, 0], radius=0.12, color=VOICE_C[1]) for k in range(n)])
        ia = VGroup(*[label(rf"{k + 1}", font_size=18, color=VOICE_C[0]).next_to(dots_a[k], UP, buff=0.12) for k in range(n)])
        ib = VGroup(*[label(rf"{n - k}", font_size=18, color=VOICE_C[1]).next_to(dots_b[k], DOWN, buff=0.12) for k in range(n)])
        links = VGroup(*[DashedLine(dots_a[k].get_center(), dots_b[k].get_center(), color=DIM, stroke_width=1.5) for k in range(n)])
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"the line against itself backwards: \ note 1 with note 12, \ note 2 with note 11, \ ...", WHITE),
            (r"each pair is heard twice: \ once at the start, \ once at the end", WHITE),
            (r"so fill the melody from both ends at once, \ a pair at a time", TUNE))]).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(DOWN, buff=0.55)
        head = label(r"\textit{canon cancrizans}: \ the crab canon", font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The Musical Offering's crab canon is two voices playing the same line, one forwards and one backwards, "
            "at the same time: crabs were thought to walk backwards. <bookmark mark='a'/> So the first note sounds "
            "against the last, the second against the second-to-last, and so on. <bookmark mark='b'/> Every pair of "
            "notes is heard twice, once near the start and once, the other way round, near the end, and the middle of "
            "the piece is where the two voices cross. <bookmark mark='c'/> That suggests how to find such lines: fill "
            "the melody from both ends at once, a pair of notes at a time, checking each pair against the pair before."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dots_a), FadeIn(ia))
            vo.wait_until("a")
            self.play(FadeIn(dots_b), FadeIn(ib), Create(links), FadeIn(rows_[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows_[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows_[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def count(self):
        d = load("crab")
        ns = ["4", "6", "8", "10", "12"]
        vals = [np.log10(d["counts"][k]) for k in ns]
        ch = columns(vals, [rf"{k} notes" for k in ns], width=7.0, height=2.8, color=WEAK, hot=(4,), hot_color=TUNE, fmt=None, font_size=20, top=9).move_to(LEFT * 2.4 + DOWN * 0.5)
        nums = VGroup(*[label(f"{d['counts'][k]:,}".replace(",", "{,}"), font_size=18, color=WHITE).next_to(ch.bars[i], UP, buff=0.1) for i, k in enumerate(ns)])
        t = label(r"crab canons, \ counted exactly \ (log scale)", font_size=22, color=GREY_A).next_to(ch, UP, buff=0.55)
        side = VGroup(label(r"each two notes more: \ about 25 times as many", font_size=24, color=WHITE),
                      label(r"the same rules as the canon solver", font_size=22, color=GREY_A),
                      label(r"plenty of crabs: \ the hard part is a good one", font_size=24, color=TUNE)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 4.2 + DOWN * 0.3)
        r = d["counts"]["12"] / d["counts"]["10"]
        with self.voiceover(
            "Count them, with the canon solver's rules: every pair consonant, no parallel fifths or octaves, beginning "
            "and ending on notes of the home chord. <bookmark mark='a'/> For four notes there are "
            f"{say(d['counts']['4'])}; for twelve, about {say(round(d['counts']['12'] / 1e6))} million, about "
            f"{say(round(r))} times more for every two notes added, about five times for each note. That is "
            "because each new pair of notes, one at either end, must agree only with itself and with the pair before; "
            "the count grows exponentially, as every such chain of constraints does. <bookmark mark='b'/> Crab "
            "canons are not rare at all. What is rare is one that makes sense forwards and backwards as a melody, with a shape a listener can "
            "follow both ways."
        ) as vo:
            self.play(FadeIn(ch), FadeIn(nums), FadeIn(t))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("crab")
        c = clip("crab.one")
        g1 = voices_roll([d["lines"][0]], width=4.6, height=2.4, lo=46, hi=82, total=12.0).move_to(LEFT * 3.5 + DOWN * 0.3)
        g2 = voices_roll(d["lines"], width=4.6, height=2.4, lo=46, hi=82, total=12.0).move_to(RIGHT * 3.0 + DOWN * 0.3)
        t1 = label(r"the line alone", font_size=24, color=GREY_A).next_to(g1, UP, buff=0.3)
        t2 = label(r"against itself backwards \ (an octave down)", font_size=24, color=GREY_A).next_to(g2, UP, buff=0.3)
        mid = DashedLine([g2.x(6.0), g2.frame.get_bottom()[1], 0], [g2.x(6.0), g2.frame.get_top()[1], 0], color=GREY_B, stroke_width=1.5)
        with self.voiceover(
            "Here is one, found by asking the solver to begin with the Tune's first three different notes, C, G and A. "
            "First the line alone; then against itself backwards, an octave lower. Watch the two voices meet in the "
            "middle and exchange their notes."
        ):
            self.play(FadeIn(g1), FadeIn(t1), FadeIn(g2), FadeIn(t2), FadeIn(mid))
        with self.listen(c) as snd:
            window(snd, r"a crab canon from the solver", detail=r"a plucked string", corner=DL, tag_corner=DR)
            sing_voices(snd, g1, [d["lines"][0]], start=d["starts"]["alone"])
            sing_voices(snd, g2, d["lines"], start=d["starts"]["both"])
        with self.voiceover(
            "In 1979 Douglas Hofstadter wrote a dialogue in this shape for his book Gödel, Escher, Bach: its lines "
            "read the same forwards and backwards, spoken by two characters, the Tortoise and Achilles. A crab canon "
            "is a palindrome that two voices sing at once."
        ):
            self.wait(0.5)
        self.wait(0.4)
        self.clear_scene()
