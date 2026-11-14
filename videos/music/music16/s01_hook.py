from __future__ import annotations

import numpy as np

from videos.music.music16.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.rule()
        self.two()
        self.plan()

    # ------------------------------------------------------------------
    def rule(self):
        rule = VGroup(label(r"``never write parallel fifths''", font_size=40, color=TUNE), label(r"every harmony textbook, \ for three hundred years", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.25).move_to(UP * 1.6)
        demo = duet([[(67, 0, 1), (69, 1, 1), (71, 2, 1), (72, 3, 1)], [(60, 0, 1), (62, 1, 1), (64, 2, 1), (65, 3, 1)]], width=5.0, height=2.0, thick=0.16).move_to(DOWN * 0.9)
        lines = VGroup(*[DashedLine(demo.notes[0][k].get_bottom(), demo.notes[1][k].get_top(), color=EAR, stroke_width=2) for k in range(4)])
        tag = label(r"two voices, \ a fifth apart, \ moving together", font_size=24, color=EAR).next_to(demo, DOWN, buff=0.35)
        with self.voiceover(
            "If you have ever studied harmony, you have been told this. Never write parallel fifths. "
            "<bookmark mark='a'/> Two voices a fifth apart, moving in the same direction to another "
            "fifth: forbidden. Students lose marks for it in examinations to this day, and most of them "
            "are never told why. Here is a stranger fact. A thousand years ago, this was not a mistake. "
            "It was the method."
        ) as vo:
            self.play(FadeIn(rule))
            vo.wait_until("a")
            self.play(FadeIn(demo), Create(lines), FadeIn(tag))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def two(self):
        d = load("hook")
        c = clip("hook.two")
        b = d["beats"]
        on = np.concatenate([[0.0], np.cumsum(b)])[:-1]
        top = [(p, a, w) for p, a, w in zip(d["tune"], on, b)]
        org = [(p, a, w) for p, a, w in zip(d["organum"], on, b)]
        cp = [(p, a, w) for p, a, w in zip(d["counterpoint"], on, b)]
        g1 = duet([top, org], colors=(CF_C, UP_C), width=5.6, height=2.6, lo=50, hi=82, thick=0.13).move_to(LEFT * 3.3 + UP * 0.3)
        g2 = duet([cp, top], colors=(UP_C, CF_C), width=5.6, height=2.6, lo=50, hi=82, thick=0.13).move_to(RIGHT * 3.3 + UP * 0.3)
        l1 = VGroup(label(r"about 900: \ a fifth below, \ always", font_size=26, color=GREY_A)).next_to(g1, UP, buff=0.3)
        l2 = VGroup(label(r"about 1700: \ a line of its own", font_size=26, color=GREY_A)).next_to(g2, UP, buff=0.3)
        with self.voiceover(
            "Listen to two ways of adding a second voice to the Tune, the melody this series keeps "
            "returning to. In the first, the new voice sings the Tune again, a fifth lower, all the way "
            "through, as singers did in the ninth century. In the second, the new voice is a melody of "
            "its own, written by the rules that later forbade the first."
        ):
            self.play(FadeIn(g1), FadeIn(l1), FadeIn(g2), FadeIn(l2))
        ev = c.events
        with self.listen(c) as snd:
            window(snd, r"a fifth below; \ then a voice of its own", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            sing_voice(snd, g1.notes[0] + g1.notes[1], d["times"]["organum"][0] + d["times"]["organum"][1], base=CF_C)
            sing_voice(snd, g2.notes[0], d["times"]["counterpoint"][0], base=UP_C)
            sing_voice(snd, g2.notes[1], d["times"]["counterpoint"][1], base=CF_C)
            pulse(snd, l1, ev["organum"], ev["counterpoint"] - 0.5, buff=0.1)
            pulse(snd, l2, ev["counterpoint"], c.duration, buff=0.1)
        for n in g1.notes[1]:
            n.set_fill(UP_C)
        for n in g2.notes[0]:
            n.set_fill(UP_C)
        cap = VGroup(label(r"the first sounds like one voice, \ made richer", font_size=28, color=WHITE).next_to(g1, DOWN, buff=0.4),
                     label(r"the second sounds like two people", font_size=28, color=WHITE).next_to(g2, DOWN, buff=0.4))
        with self.voiceover(
            "The first does not sound like two melodies. It sounds like one melody, made thicker and "
            "richer, like a choir in a large church. <bookmark mark='a'/> The second sounds like two "
            "people, each going somewhere. That difference is the whole subject of this part. The rules "
            "of counterpoint are not rules of taste. In 2001 the music psychologist David Huron showed "
            "that they can be derived, almost all of them, from how hearing separates sounds into "
            "streams. They are instructions for keeping two voices audible as two."
        ) as vo:
            self.play(FadeIn(cap[0]))
            vo.wait_until("a")
            self.play(FadeIn(cap[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        idea = VGroup(label(r"counterpoint is engineering:", font_size=32, color=GREY_A), label(r"keep two voices audible as two.", font_size=32, color=TUNE)).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.45)
        card = objectives_card([
            r"organum: \ the ninth century's parallel voices",
            r"why some intervals fuse, \ and why moving together merges",
            r"Fux's exercise of 1725: \ a cantus firmus and twelve rules",
            r"every good line, \ counted; \ each rule removed, \ and the damage measured",
            r"the five species: \ passing notes, \ neighbours, \ suspensions",
            r"from organum to Bach: \ independence, \ measured",
        ], title=r"Part 16: \ Two Voices", font_size=26).move_to(DOWN * 0.5)
        with self.voiceover(
            "This part opens Act Three, where music has more than one voice at a time. "
            "<bookmark mark='a'/> We begin with organum, the first written polyphony, which wanted its "
            "voices to merge. <bookmark mark='b'/> We find out why some intervals fuse, and why voices "
            "that move together become one. <bookmark mark='c'/> Then we take the most famous exercise "
            "in music education, Fux's, from 1725. <bookmark mark='d'/> We count every line that "
            "obeys its rules, remove the rules one at a time, and measure what breaks. "
            "<bookmark mark='e'/> We work through the five species. <bookmark mark='f'/> And we measure "
            "how independent two voices are, from organum to the florid counterpoint that prepared "
            "Bach."
        ) as vo:
            self.play(FadeIn(idea))
            self.play(FadeIn(card.head))
            for mark, r in zip("abcdef", card.rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
