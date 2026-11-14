from __future__ import annotations

import numpy as np

from videos.music.music15.common import *  # noqa: F403


class Colour(SoundScene):
    def construct(self):
        chapter(self, 11, r"Does it matter which key?", r"Is D major different from C major?")
        self.same()
        self.unequal()

    # ------------------------------------------------------------------
    def same(self):
        d = load("more")["colour"]
        c = clip("colour.two")
        kb = keys(41, 77, width=10.0, height=1.4).move_to(DOWN * 1.1)
        tags = VGroup(label(r"C major", font_size=40, color=TUNE), label(r"D$\flat$ major", font_size=40, color=BLUE)).arrange(RIGHT, buff=2.0).move_to(UP * 1.5)
        with self.voiceover(
            "People have long said that keys have characters: D major is bright and martial, F major "
            "pastoral, D minor grave. Is that true? Here is one cadence in C major, and then in D flat "
            "major, the key furthest from it on the circle."
        ):
            self.play(FadeIn(kb), FadeIn(tags))
        with self.listen(c) as snd:
            window(snd, r"one cadence, \ two keys", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            light_chords(snd, kb, d["chords"]["C"] + d["chords"]["Db"], d["times"]["C"] + d["times"]["Db"], end=c.duration)
            pulse(snd, tags[0], d["starts"]["C"], d["starts"]["Db"] - 0.4, buff=0.12)
            pulse(snd, tags[1], d["starts"]["Db"], c.duration, buff=0.12)
        kb.clear()
        cap = VGroup(label(r"a semitone higher, \ and otherwise the same in every relation", font_size=28, color=WHITE),
                     label(r"on a piano in equal temperament, \ every key is the same key, \ moved", font_size=28, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The second is a semitone higher. Apart from that, nothing differs: every interval, every "
            "chord, every leaning note is the same. Played a day apart, very few listeners could say "
            "which was which. Part 14 said it of melody, and it holds for harmony: a key is a pattern "
            "of relations, and in equal temperament the pattern is identical in all twelve places. Yet "
            "memory is better than that suggests. When Daniel Levitin asked people in 1994 to sing a "
            "favourite recorded song from memory, most of them started within a tone or two of the "
            "record."
        ):
            self.play(FadeOut(kb), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def unequal(self):
        d = load("more")["colour"]
        order = ["C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "Eb", "Bb", "F"]
        vals = [d["thirds"][k] - 380.0 for k in order]
        ch = columns(vals, [tex(k.replace("#", "♯").replace("b", "♭")) for k in order], width=9.0, height=2.6, color=WEAK, hot=(0, 11), hot_color=TUNE, font_size=22, top=30).move_to(DOWN * 1.0 + RIGHT * 1.0)
        for b in (6, 7, 8):
            ch.bars[b].set_fill(EAR)
        nums = VGroup(*[label(f"{d['thirds'][k]:.0f}", font_size=18, color=GREY_A).next_to(ch.bars[i], UP, buff=0.08) for i, k in enumerate(order)])
        pure = DashedLine(ch.get_left() + UP * 0.0, ch.get_right(), color=WHITE, stroke_width=1.5)
        y_pure = ch.bars[0].get_bottom()[1] + 2.6 * (386.3 - 380) / 30
        pure.put_start_and_end_on([ch.get_left()[0], y_pure, 0], [ch.get_right()[0], y_pure, 0])
        pl = label(r"a pure third: \\ 386 cents", font_size=20, color=WHITE).next_to(pure, LEFT, buff=0.15)
        head = label(r"the major third on each key note, \ in Werckmeister's temperament of 1691 \ (Part 6)", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "So where did the characters come from? Partly from instruments: a violin's open strings "
            "ring in D and A, and trumpets were built in D. And partly from tuning. Before equal "
            "temperament, keyboards were tuned so that the common keys were sweeter than the rare ones. "
            "<bookmark mark='a'/> In Werckmeister's temperament, from Part 6, the major third on C is "
            f"{say(d['thirds']['C'])} cents, nearly pure; <bookmark mark='b'/> the third on F sharp is "
            f"{say(d['thirds']['F#'])}, as wide as a third can be without sounding out of tune. Every "
            "key had its own mixture of calm and edge, and a composer of 1720 could choose a key for "
            "its colour. On a modern piano that choice is gone. What remains is height, and habit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch), Create(pure), FadeIn(pl))
            vo.wait_until("a")
            self.play(FadeIn(nums), Indicate(ch.bars[0], color=TUNE), Indicate(ch.bars[11], color=TUNE))
            vo.wait_until("b")
            self.play(*[Indicate(ch.bars[i], color=EAR) for i in (6, 7, 8)])
        self.wait(0.4)
        self.clear_scene()
