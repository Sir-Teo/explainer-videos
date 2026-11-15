from __future__ import annotations

import numpy as np

from videos.music.music47.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.flute()
        self.question()
        self.plan()

    # ------------------------------------------------------------------
    def flute(self):
        d = load("hook")
        c = clip("hook.flute")
        L = d["length"]
        W = 11.0
        sc = W / L
        pipe = RoundedRectangle(width=W, height=0.55, corner_radius=0.2, stroke_color=GREY_A, stroke_width=2, fill_color="#E7DCC8", fill_opacity=0.25)
        notch = Polygon(pipe.get_corner(UL) + RIGHT * 0.05, pipe.get_corner(UL) + RIGHT * 0.45, pipe.get_corner(UL) + RIGHT * 0.25 + DOWN * 0.22,
                        stroke_width=0, fill_color=BLACK, fill_opacity=1.0)
        holes = VGroup(*[Circle(radius=0.11, stroke_color=GREY_A, stroke_width=2, fill_color=BLACK, fill_opacity=1.0).move_to(pipe.get_left() + RIGHT * sc * h)
                         for h in d["holes"]])
        fl = VGroup(pipe, notch, holes).move_to(UP * 1.6)
        ruler = VGroup(Line(pipe.get_corner(DL) + DOWN * 0.25, pipe.get_corner(DR) + DOWN * 0.25, color=GREY_B, stroke_width=1.5),
                       label(rf"{100 * L:.1f} cm survive; \ the bore is {1000 * d['bore']:.0f} mm across", font_size=17, color=GREY_A).next_to(pipe, DOWN, buff=0.45))
        hz = d["hz"]
        cells = VGroup()
        for k, f in enumerate(hz):
            cells.add(VGroup(RoundedRectangle(width=1.55, height=0.85, corner_radius=0.12, stroke_color=GREY_B, stroke_width=1.5),
                             VGroup(label(rf"{f:.0f} Hz", font_size=19, color=WHITE), label(note_of(f), font_size=15, color=GREY_A)).arrange(DOWN, buff=0.06)).arrange(ORIGIN))
        cells.arrange(RIGHT, buff=0.25).move_to(DOWN * 1.1)
        caps = VGroup(*[label(t, font_size=15, color=GREY_A).next_to(cells[i], DOWN, buff=0.15) for i, t in enumerate([r"all closed"] + [rf"{k} open" for k in range(1, 6)])])
        head = label(r"a wing bone, \ five holes, \ some 40,000 years", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "In 2008, in a cave called Hohle Fels in south-west Germany, archaeologists pieced together twelve fragments of "
            "a griffon vulture's wing bone. <bookmark mark='a'/> Someone had cut five finger holes in it, and a notch at one "
            "end to blow across. It is at least thirty-five thousand years old, and among the oldest instruments anyone has "
            f"found. <bookmark mark='b'/> Here is a pipe of the same size, {say(100 * L, 1)} centimetres and eight millimetres "
            "across, played by Part 8's flute model, with five holes cut evenly, two centimetres apart. Nobody knows where "
            "the real holes put its notes; listen for what even spacing gives."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(cells, 0.15)))
            vo.wait_until("a")
            self.play(FadeIn(fl), FadeIn(ruler))
            vo.wait_until("b")
            self.play(FadeIn(cells), FadeIn(caps))
        seq = d["seq"]
        beat = 0.36
        with self.listen(c) as snd:
            window(snd, r"a pipe with five holes", detail=r"Part 8's flute model, \ not a reconstruction", corner=DL, tag_corner=DR)
            t = 0.0
            for k in seq:
                pulse(snd, cells[k], t, t + beat * 0.95, buff=0.06)
                t += beat
            t += 0.7
            for k, b in d["tune"]:
                pulse(snd, cells[k], t, t + b * beat * 1.4 * 0.95, buff=0.06)
                t += b * beat * 1.4
        steps = d["steps"]
        with self.voiceover(
            f"With every hole closed the pipe sounds about {say(hz[0])} hertz. Opening the holes one by one climbs in steps of "
            f"{say(steps[0])}, {say(steps[1])}, {say(steps[2])}, {say(steps[3])} and {say(steps[4])} cents: even holes do "
            "not give even steps, so whoever made a flute like this chose where the notes would be. That choice, of a few "
            "fixed pitches, is the first thing this part will find everywhere."
        ):
            self.play(*[Indicate(x, color=TUNE, scale_factor=1.05) for x in cells], run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def question(self):
        items = [
            (r"every society that has been studied makes music; \ no one agrees why", WHITE),
            (r"what is shared by all music, \ and what only by some?", WHITE),
            (r"how do tunes travel, \ change and form families as people pass them on?", WHITE),
            (r"what do animals, \ infants and languages tell us?", WHITE),
            (r"and which popular claims about music and the mind survive a careful test?", TUNE),
        ]
        rows_scene(self, r"the questions", items,
                   "Every society that has been studied makes music, and no one agrees why. <bookmark mark='b'/> What is shared "
                   "by all of it, and what only by some? <bookmark mark='c'/> How do tunes travel, change and form families as "
                   "people pass them on? <bookmark mark='d'/> What do animals, infants and languages tell us? "
                   "<bookmark mark='e'/> And which popular claims about music and the mind survive a careful test?", marks="bcde")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"the oldest instruments, \ and what every society does",
            r"statistical universals, \ and what is learned instead",
            r"priors revealed by passing rhythms from ear to hand",
            r"a tune in simulated mouths, \ and tune families",
            r"birds, \ whales, \ a cockatoo, \ infants and language",
            r"amusia, \ the Mozart effect, \ and why there is music at all",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. The oldest instruments, and what every society does. <bookmark mark='b'/> Statistical "
            "universals, and what is learned instead. <bookmark mark='c'/> Priors revealed by passing rhythms from ear to "
            "hand. <bookmark mark='d'/> A tune in simulated mouths, and tune families. <bookmark mark='e'/> Birds, whales, a "
            "dancing cockatoo, infants and language. <bookmark mark='f'/> And amusia, the Mozart effect, and why there is "
            "music at all."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
