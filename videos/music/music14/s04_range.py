from __future__ import annotations

import numpy as np

from videos.music.music14.common import *  # noqa: F403


class Range(SoundScene):
    def construct(self):
        chapter(self, 3, r"Room to sing", r"How much room does a tune need?")
        self.spans()
        self.middle()

    # ------------------------------------------------------------------
    def spans(self):
        d = load("range")
        c = clip("range.two")
        ev = c.events
        ks = list(range(3, 19))
        vals = [d["counts"].get(str(k), 0) for k in ks]
        ch = columns(vals, [str(k) for k in ks], width=9.0, height=2.3, color=WEAK, hot=[k - 3 for k in ks if k <= 12], hot_color=TUNE, font_size=20).move_to(UP * 0.1)
        xl = label(r"from a tune's lowest note to its highest, \ in semitones", font_size=22, color=GREY_B).next_to(ch, DOWN, buff=0.15)
        head = label(r"how much room each tune uses", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        facts = VGroup(label(rf"the middle tune: \ {d['median']:.0f} semitones, \ an octave", font_size=28, color=WHITE),
                       label(rf"{d['within_octave']} of {d['of']} fit in an octave", font_size=28, color=TUNE)).arrange(RIGHT, buff=1.0).next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "How much room does a melody use? Measure each tune from its lowest note to its highest. "
            "<bookmark mark='a'/> The middle value is exactly an octave. "
            f"{say(d['within_octave'])} of the {say(d['of'])} fit within an octave, and none needs more "
            "than an octave and a fourth. That is the comfortable compass of an untrained voice, and "
            "tunes that everyone sings are tunes that everyone can sing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch), FadeIn(xl), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(facts[0]))
            self.play(FadeIn(facts[1]))
        n, w = d["narrow"], d["wide"]
        rn = roll(n["pitches"], n["beats"], width=4.2, height=2.2, lo=-1, hi=17, lines=(0, 12), color=TUNE).move_to(LEFT * 3.6 + DOWN * 0.3)
        rw = roll(w["pitches"], w["beats"], width=6.4, height=2.2, lo=-1, hi=17, lines=(0, 12), color=EAR).move_to(RIGHT * 2.9 + DOWN * 0.3)
        ln = label(r"Hot Cross Buns: \ three notes", font_size=24, color=TUNE).next_to(rn, UP, buff=0.15)
        lw = label(r"The Star-Spangled Banner: \ a tenth in two lines", font_size=24, color=EAR).next_to(rw, UP, buff=0.15)
        with self.voiceover(
            "At one end is Hot Cross Buns: three notes, a major third from bottom to top. At the other, "
            "Silent Night, which spans an eleventh; and the Star-Spangled Banner, whose first two lines "
            "already cover a tenth, and the whole song an octave and a fifth, which is why crowds dread "
            "it. Listen to the narrowest, and then to the start of the widest."
        ):
            self.play(FadeOut(ch), FadeOut(xl), FadeOut(facts), FadeIn(rn), FadeIn(ln), FadeIn(rw), FadeIn(lw))
        with self.listen(c) as snd:
            window(snd, r"narrow, \ then wide", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            sing(snd, rn, d["times"]["narrow"])
            sing(snd, rw, d["times"]["wide"])
            pulse(snd, ln, ev["narrow"], ev["wide"] - 0.5, buff=0.1)
            pulse(snd, lw, ev["wide"], c.duration, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def middle(self):
        d = load("range")
        ks = list(range(-9, 10))
        ch = columns(d["around"], [str(k) if k % 3 == 0 else "" for k in ks], width=9.0, height=2.5, color=WEAK, hot=[k + 9 for k in (-2, -1, 0, 1, 2)], hot_color=TUNE, font_size=20).move_to(DOWN * 1.0)
        xl = label(r"semitones above or below the middle note of the tune", font_size=22, color=GREY_B).next_to(ch, DOWN, buff=0.15)
        head = label(r"every note, \ measured from the middle note of its own tune", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
        cap = VGroup(label(rf"{100 * d['near']:.0f} notes in a hundred are within a tone or so of the middle", font_size=28, color=WHITE),
                     label(r"a small range, \ mostly occupied near its middle", font_size=30, color=TUNE)).arrange(DOWN, buff=0.2).next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Within its range, a tune does not spread itself evenly. It lives near its middle. Measure "
            "every note from the middle note of its own tune. <bookmark mark='a'/> "
            f"{say(100 * d['near'])} notes in a hundred lie within a tone or so of the middle; singers "
            "call the band where a melody mostly sits its tessitura. The extremes are visited rarely: "
            f"the top note of a tune is about one note in {say(1 / d['top_share'])}, and it is an "
            "event. <bookmark mark='b'/> Keep "
            "this picture in mind: a small range, mostly occupied near its middle. It is about to "
            "explain the rule that we began with."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(cap[0]))
            vo.wait_until("b")
            self.play(FadeIn(cap[1]))
        self.wait(0.4)
        self.clear_scene()
