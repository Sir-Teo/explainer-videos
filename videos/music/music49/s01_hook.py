from __future__ import annotations

import numpy as np

from videos.music.music49.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.bathroom()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.two")
        card = listen_card(r"The Tune's first phrase, \ twice, \ with reverberation. \ One is a simulated tiled room: \ "
                           r"sound bouncing off six walls. \ The other is pure arithmetic: \ four delays fed back and two more. \ Which is the arithmetic?", width=10.4)
        with self.voiceover(
            "A question for your ears. The Tune's first phrase, twice, with reverberation. One is a simulated tiled room: "
            "sound bouncing between six walls. The other is pure arithmetic: four delays fed back into themselves, and two "
            "more. Both ring for the same time. Which is the arithmetic?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=3.0, height=1.2, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=24, color=WHITE)).arrange(ORIGIN)
                         for t in (r"first", r"second")]).arrange(RIGHT, buff=1.6).move_to(UP * 0.4)
        room = VGroup(Rectangle(width=2.6, height=1.6, stroke_color=GREY_A, stroke_width=2),
                      *[Line(LEFT * 1.3 + UP * (0.8 - 0.2 * k), RIGHT * 1.3 + UP * (0.8 - 0.2 * k), stroke_width=0.6, color=GREY_B) for k in range(1, 8)],
                      *[Line(UP * 0.8 + RIGHT * (-1.3 + 0.2 * k), DOWN * 0.8 + RIGHT * (-1.3 + 0.2 * k), stroke_width=0.6, color=GREY_B) for k in range(1, 13)])
        room.scale(0.7).to_edge(DOWN, buff=0.9)
        self.play(FadeOut(card), FadeIn(boxes), FadeIn(room))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two reverbs", kind="synthesized", detail=r"Part 7's piano, \ reverberated", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        with self.voiceover(
            f"The first was the arithmetic: Manfred Schroeder's reverberator of 1962. It rings for {say(d['rt60_room'], 1)} "
            "seconds, like the room, but listen to its tail: a faint metallic flutter, a pattern repeating. The simulated "
            "room's tail is a smooth wash. Both are nothing but delay and addition, and this part builds them, and the "
            "filters and effects of every studio, from those two operations."
        ):
            self.play(boxes[0][0].animate.set_stroke(TUNE, width=4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bathroom(self):
        items = [
            (r"1947: \ Bill Putnam put a loudspeaker and a microphone in his Chicago studio's tiled bathroom", WHITE),
            (r"the Harmonicats' `Peg o' My Heart', \ recorded with it, \ became a hit: \ the echo was the sound", WHITE),
            (r"studios built echo chambers; \ then steel plates \ (EMT, \ 1957) \ and springs in boxes", WHITE),
            (r"1962: \ Manfred Schroeder at Bell Labs built a room out of arithmetic", TUNE),
            (r"everything an effects rack does is delay and addition", GREY_A),
        ]
        rows_scene(self, r"a bathroom, \ sold as art", items,
                   "The story starts in a bathroom. <bookmark mark='b'/> In 1947 Bill Putnam put a loudspeaker and a microphone in "
                   "the tiled bathroom of his Chicago studio. <bookmark mark='c'/> The Harmonicats' Peg o' My Heart, recorded "
                   "with it, became a hit, and the echo was the sound. <bookmark mark='d'/> Studios built echo chambers, then "
                   "steel plates, from EMT in 1957, and springs in boxes. <bookmark mark='e'/> In 1962 Manfred Schroeder at Bell "
                   "Labs built a room out of arithmetic. <bookmark mark='f'/> Everything an effects rack does is delay and "
                   "addition.", marks="bcdef")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"impulse responses and convolution",
            r"poles, \ zeros, \ and the equalizer",
            r"phase, \ combs, \ flangers, \ choruses and phasers",
            r"a room simulated, \ and measured by a sweep",
            r"Schroeder's reverberator and feedback delay networks",
            r"plates and springs",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. Impulse responses and convolution. <bookmark mark='b'/> Poles, zeros, and the equalizer. "
            "<bookmark mark='c'/> Phase, combs, flangers, choruses and phasers. <bookmark mark='d'/> A room simulated, and "
            "measured by a sweep. <bookmark mark='e'/> Schroeder's reverberator and feedback delay networks. "
            "<bookmark mark='f'/> And plates and springs."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
