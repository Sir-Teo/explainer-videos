from __future__ import annotations

import numpy as np

from videos.music.music59.common import *  # noqa: F403


class Arrays(SoundScene):
    def construct(self):
        chapter(self, 4, r"Arrays and curvature", r"Why are line arrays hung in curves?")
        self.maps()
        self.why()
        self.heard()
        self.steer()

    # ------------------------------------------------------------------
    def maps(self):
        d = load("arrays")
        names = [("point", r"one point source", GREY_A), ("straight", r"a straight line of 24", TUNE), ("curved", r"the same, \ curved below", EAR)]
        panels = Group()
        for i, (k, t, col) in enumerate(names):
            a = np.array(d["maps"][k])
            top = np.percentile(a, 99.5)
            pic = picture(np.clip(a - top, -40, 0)[::-1], -40, 0, 4.0, 1.6)
            pic.move_to([0.6, 1.9 - 2.05 * i, 0])
            panels.add(Group(pic, label(t, font_size=17, color=col).next_to(pic, LEFT, buff=0.3)))
        xl = label(r"0 to 90 m from the stage, \ floor to 18 m high; \ 1 kHz, \ third-octave; \ 40 dB of colour", font_size=15, color=GREY_A).to_edge(DOWN, buff=0.25)
        head = label(r"three fields", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here are the sound fields, side views of an arena from the stage to ninety metres, at one kilohertz, bright where "
            "it is loud. <bookmark mark='a'/> One point source: loud near it, falling away in every direction. "
            "<bookmark mark='b'/> A straight vertical line: a horizontal beam, level for a long way, but narrow: the people "
            "below it, close to the stage, are under the beam. <bookmark mark='c'/> Curve the lower part of the line, each box "
            "tilted a little more than the one above, and the beam fans downwards: the top boxes throw to the back, the bottom "
            "ones cover the front."
        ) as vo:
            self.play(FadeIn(head), FadeIn(xl))
            for mark, p in zip("abc", panels):
                vo.wait_until(mark)
                self.play(FadeIn(p), run_time=0.8)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        d = load("arrays")
        items = [
            (r"the far seats are reached by the straight top of the array, \ coupled into a long, \ narrow, \ far-reaching beam", WHITE),
            (rf"the near seats by the curved bottom, \ each box splayed further: \ here 0.3$^\circ$ apart at the top, \ {max(d['splay']):.1f}$^\circ$ at the bottom", WHITE),
            (r"the J shape: \ the angle between boxes grows as the seats come closer", WHITE),
            (r"prediction software computes these fields for a real room, \ box by box, \ before the rig is hung", WHITE),
            (r"the goal: \ the same level and the same tone in every seat, \ within a few decibels", TUNE),
        ]
        rows_scene(self, r"the J", items,
                   "That is the logic of the curve. <bookmark mark='b'/> The far seats are reached by the straight top of the array, "
                   "whose boxes couple into a long, narrow, far-reaching beam. <bookmark mark='c'/> The near seats are reached by "
                   "the curved bottom, each box splayed further than the one above: here three tenths of a degree apart at the top, "
                   f"{say(max(d['splay']), 1)} degrees at the bottom. <bookmark mark='d'/> That is the J shape. And prediction "
                   "software computes fields like these for the real room, box by box, before the rig is ever hung. "
                   "<bookmark mark='e'/> The goal is the same level and the same tone in every seat, within a few decibels.", marks="bcdef")

    # ------------------------------------------------------------------
    def heard(self):
        d = load("arrays")
        c = clip("arrays.three")
        boxes = choice_boxes([r"10 m", r"40 m", r"80 m"], width=2.6, height=0.9, buff=0.9, size=22).move_to(UP * 0.4)
        lv = d["levels"]
        note = label(rf"levels as heard: \ 0, \ {lv['40']:.1f} and {lv['80']:.1f} dB; \ the air takes the treble, \ the room adds its reverberation", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.5)
        head = label(r"three seats, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear our mix from the line array at ten, forty and eighty metres, with the arena's reverberation and the air's absorption at each seat."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(note))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"10, \ 40, \ 80 m", kind="physical model", detail=r"our mix, \ a simulated arena", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["d10"], st["d40"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["d40"], st["d80"] - 0.3, buff=0.08)
            pulse(snd, boxes[2], st["d80"], c.duration, buff=0.08)
        with self.voiceover(
            f"The level falls only {say(-lv['80'])} decibels over eight times the distance, where a single box would lose eighteen; "
            "what changes is the treble, taken by the air, and the share of reverberation."
        ):
            self.play(Indicate(boxes[2], color=EAR, scale_factor=1.04))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def steer(self):
        items = [
            (r"give each box its own amplifier and processor, \ and the curve can be bent electronically, \ by delays \ (Part 55's wave fields)", WHITE),
            (r"steerable columns for speech in churches and stations; \ beam-steered arrays for concerts", WHITE),
            (r"optimizers set each box's filters to match a target coverage, \ seat by seat", WHITE),
            (r"and the same arithmetic as Part 54's microphone array, \ run backwards", TUNE),
        ]
        rows_scene(self, r"steering", items,
                   "And the curve need not be mechanical. <bookmark mark='b'/> Give each box its own amplifier and processor, and "
                   "the beam can be bent by delays, Part 55's wave fields in miniature. <bookmark mark='c'/> Steerable columns "
                   "serve speech in churches and stations; beam-steered arrays serve concerts. <bookmark mark='d'/> Optimizers set "
                   "each box's filters to match a target coverage, seat by seat. <bookmark mark='e'/> It is the arithmetic of Part "
                   "54's microphone array, run backwards.", marks="bcde")
