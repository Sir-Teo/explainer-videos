from __future__ import annotations

import numpy as np

from videos.music.music17.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.tune()
        self.three()
        self.verdict()
        self.plan()

    # ------------------------------------------------------------------
    def tune(self):
        d = load("hook")
        card = history_card(1727, r"Leipzig: \ the \textit{St Matthew Passion}", r"a hymn tune of 1601, \ sung five times in the Passion, \ each time harmonized anew", width=10.4, font_size=26).to_edge(UP, buff=0.4)
        g = choir_roll(d["bach"], which=(0,), width=10.0, height=1.6, lo=62, hi=80).move_to(DOWN * 1.2)
        tag = label(r"the tune: \ the Passion Chorale", font_size=26, color=VOICE_C[0]).next_to(g, UP, buff=0.3)
        with self.voiceover(
            "In 1727, in Leipzig, Bach's St Matthew Passion was first performed. Five times in the course "
            "of it, the choir stops the story to sing a hymn the congregation knew, and it is the same "
            "hymn tune each time, written by Hans Leo Hassler in 1601. <bookmark mark='a'/> Bach "
            "harmonized it anew for each moment of the story. Here is its last appearance, as Jesus "
            "dies: the tune alone, its first two phrases."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(tag))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def three(self):
        d = load("hook")
        c = clip("hook.three")
        hi, lo = 80, 38
        rows_ = VGroup()
        specs = (("alone", r"the tune alone", (0,)), ("bach", r"Bach, \ 1727", (0, 1, 2, 3)), ("plain", r"a chord-chooser", (0, 1, 2, 3)))
        for k, (key, text, which) in enumerate(specs):
            voices = d["bach"] if key != "plain" else d["plain"]
            g = choir_roll(voices, which=which, width=9.4, height=1.75, lo=lo, hi=hi, thick=0.08).move_to(RIGHT * 1.1 + UP * (2.25 - 2.25 * k))
            t = label(text, font_size=24, color=GREY_A).next_to(g, LEFT, buff=0.35)
            rows_.add(VGroup(t, g))
        with self.voiceover(
            "Listen to it three times: alone, then as Bach set it for four voices, and then as a simple "
            "machine sets it. The machine knows which chords Bach uses most under each note of a tune, "
            "and which chord tends to follow which, and nothing else."
        ):
            self.play(LaggedStart(*[FadeIn(r) for r in rows_], lag_ratio=0.3), run_time=2.5)
        with self.listen(c) as snd:
            window(snd, r"alone, \ Bach, \ the chord-chooser", kind="synthesized", detail=r"a model choir", corner=DL, tag_corner=DR)
            for k, (key, _, _) in enumerate(specs):
                sing_roll(snd, rows_[k][1], d["times"][key], start=d["starts"][key])
                end = d["starts"][specs[k + 1][0]] - 0.5 if k < 2 else c.duration
                pulse(snd, rows_[k][0], d["starts"][key], end, buff=0.1)
        self.rows = rows_

    # ------------------------------------------------------------------
    def verdict(self):
        d = load("hook")
        g = self.rows[2][1]
        bad = VGroup()
        for k in d["parallels_plain"]:
            # the beat where a pair of voices arrives in parallel: mark it with a red line through the chord
            t = d["first"] + k * TICKS
            bad.add(Line([g.x(t) + 0.05, g.frame.get_bottom()[1], 0], [g.x(t) + 0.05, g.frame.get_top()[1], 0], color=RED, stroke_width=3))
        note = label(rf"{len(d['parallels_plain'])} of its {len(d['plain_chords']) - 1} moves make parallel fifths or octaves; \ its inner voices hardly move", font_size=26, color=RED).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The chord-chooser's chords are not wrong, one at a time. Every one is a chord Bach uses "
            f"under that note. But listen to how they move. In {say(len(d['plain_chords']) - 1)} moves it writes parallel fifths "
            f"or octaves {say(len(d['parallels_plain']))} times, the red lines, and its alto and tenor "
            "mostly sit still. Bach's version is four singers, each with a line of their own, who "
            "happen to make a chord at every beat. That is the craft this part is about."
        ):
            self.play(Create(bad), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        steps = VGroup(*[label(t, font_size=28, color=c_) for t, c_ in (
            (r"the chorales: \ 364 of Bach's, \ as data", WHITE),
            (r"four ranges, \ four lines, \ and the rules that keep them apart", WHITE),
            (r"how often Bach breaks the rules", EAR),
            (r"the chords, \ the cadences, \ the notes between the beats", WHITE),
            (r"a harmonizer, \ built as a search, \ judged against Bach on tunes it has never seen", TUNE))]).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"Part 17: \ Four Voices", font_size=36, color=TUNE).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Part 16 kept two voices apart. Now there are four, and every moment is also a chord. "
            "<bookmark mark='a'/> We take Bach's chorales, three hundred and sixty-four of them, as "
            "data. <bookmark mark='b'/> We measure where each voice sings and how it moves, and state "
            "the rules that keep four lines distinct. <bookmark mark='c'/> We count how often Bach "
            "himself breaks them. <bookmark mark='d'/> We look at his chords, his cadences, and the notes "
            "he puts between the beats. <bookmark mark='e'/> And we build a harmonizer, a search over "
            "chords and voicings, and judge it against Bach on tunes it has never seen."
        ) as vo:
            self.play(FadeIn(head))
            for mark, s in zip("abcde", steps):
                vo.wait_until(mark)
                self.play(FadeIn(s))
        self.wait(0.4)
        self.clear_scene()
