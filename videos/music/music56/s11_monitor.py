from __future__ import annotations

import numpy as np

from videos.music.music56.common import *  # noqa: F403


class Monitor(SoundScene):
    def construct(self):
        chapter(self, 10, r"Monitoring", r"How can a mix sound right everywhere if you can hear it in only one place?")
        self.room()
        self.level()
        self.phone()
        self.heard()
        self.checks()

    # ------------------------------------------------------------------
    def room(self):
        items = [
            (r"nearfield monitors: \ small loudspeakers a metre or two away, \ so that the direct sound outweighs the room's", WHITE),
            (r"the stereo triangle of Part 55, \ the listener at the apex; \ the seat away from the room's halfway planes \ (its modes)", WHITE),
            (r"absorbers at the first reflection points; \ bass traps in the corners; \ diffusers behind", WHITE),
            (r"headphones remove the room entirely, \ and with it the crosstalk that makes stereo images", WHITE),
            (r"every monitor lies a little; \ the craft is to know how yours lies", TUNE),
        ]
        rows_scene(self, r"the mixing room", items,
                   "A mix is only as good as what the engineer hears. <bookmark mark='b'/> Nearfield monitors are small "
                   "loudspeakers a metre or two away, so that their direct sound outweighs the room's. <bookmark mark='c'/> They "
                   "make the stereo triangle of Part 55, with the listener at the apex, and the seat is kept off the room's "
                   "halfway planes, where its modes come and go. <bookmark mark='d'/> Absorbers at the first reflection points, "
                   "bass traps in the corners, diffusers behind. <bookmark mark='e'/> Headphones remove the room entirely, and with "
                   "it the crosstalk that makes stereo images. <bookmark mark='f'/> Every monitor lies a little; the craft is to "
                   "know how yours lies.", marks="bcdef")

    # ------------------------------------------------------------------
    def level(self):
        items = [
            (r"Part 4: \ the ear's sensitivity depends on level: \ quiet sounds lose their bass and extreme treble first \ (Fletcher and Munson, \ 1933)", WHITE),
            (r"mix loud and the bass seems ample; \ the same mix played quietly sounds thin", WHITE),
            (r"mix quietly and the bass gets turned up; \ played loud, \ it booms", WHITE),
            (r"film and broadcast mix at calibrated levels, \ around 79 to 85 dB SPL; \ music studios check at several", TUNE),
            (r"and long sessions at high level fatigue the ear, \ and then damage it \ (Part 4's safe hours)", GREY_A),
        ]
        rows_scene(self, r"how loud to listen", items,
                   "How loud should the engineer listen? <bookmark mark='b'/> As Part 4 showed, the ear's sensitivity depends on "
                   "level: quiet sounds lose their bass and extreme treble first, as Fletcher and Munson measured in 1933. "
                   "<bookmark mark='c'/> Mix loud and the bass seems ample, and the same mix played quietly sounds thin. "
                   "<bookmark mark='d'/> Mix quietly and the bass gets turned up, and played loud it booms. <bookmark mark='e'/> "
                   "Film and broadcast mix at calibrated levels, around seventy-nine to eighty-five decibels; music studios check "
                   "at several. <bookmark mark='f'/> And long sessions at high level tire the ear, and then damage it: Part 4's "
                   "safe hours apply to engineers too.", marks="bcdef")

    # ------------------------------------------------------------------
    def phone(self):
        d = load("monitor")
        f = np.array(d["f"])
        ax = logf_axes(width=9.6, height=3.0, flo=20, fhi=20000, ylo=-40, yhi=5, center=DOWN * 0.3)
        flat = DashedLine(ax.to(20, 0), ax.to(20000, 0), color=GREY_B, stroke_width=2)
        ph = curve(f, np.clip(d["phone_db"], -40, 5), ax.to, color=EAR, width=3)
        bassband = Rectangle(width=abs(ax.to(98, 0)[0] - ax.to(65, 0)[0]), height=3.0, stroke_width=0, fill_color=BLUE, fill_opacity=0.2).move_to((ax.to(65, -17.5) + ax.to(98, -17.5)) / 2)
        bl = label(r"our bass's fundamentals, \ 65 to 98 Hz", font_size=14, color=BLUE).next_to(bassband, UP, buff=0.05)
        yt = VGroup(*[label(f"{v} dB", font_size=14, color=GREY_A).next_to(ax.to(20, v), LEFT, buff=0.1) for v in (0, -20, -40)])
        key = VGroup(label(r"studio monitors \ (taken as flat)", font_size=16, color=GREY_B), label(r"Part 54's phone loudspeaker", font_size=16, color=EAR)).arrange(RIGHT, buff=0.8).to_edge(UP, buff=1.0)
        note = label(rf"the phone loses the bass's fundamentals by 40 dB and more; \ {100 * d['bass_above_844']:.0f}\% of the bass track's energy lies above 844 Hz, \ where the phone works",
                     font_size=16, color=WHITE).to_edge(DOWN, buff=0.35)
        head = label(r"where the mix will be heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "And most listeners will not hear the mix on studio monitors. <bookmark mark='a'/> Here is Part 54's phone "
            "loudspeaker, whose simulated minus-three-decibel point is near eight hundred hertz; real phones vary. <bookmark mark='b'/> Our bass line's fundamentals, "
            "sixty-five to ninety-eight hertz, are forty decibels and more down. <bookmark mark='c'/> But "
            f"{say(100 * d['bass_above_844'])} per cent of the bass track's energy lies in its harmonics above eight hundred "
            "and forty-four hertz, where the phone works, and Part 4's missing fundamental does the rest: the ear hears the "
            "line's pitch from its harmonics."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yt), FadeIn(flat), FadeIn(key[0]), FadeIn(ghost(ph, 0.3)))
            vo.wait_until("a")
            self.play(Create(ph), FadeIn(key[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(bassband), FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("monitor")
        c = clip("monitor.two")
        boxes = choice_boxes([r"monitors", r"a phone"], width=3.0, height=0.9, buff=1.4, size=22).move_to(UP * 0.4)
        head = label(r"one mix, \ two playbacks", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        note = label(r"can you still follow the bass line on the phone?", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.5)
        with self.voiceover("Hear our close-and-dry mix on monitors, then on the phone. Can you still follow the bass line?"):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(note))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"monitors, \ then a phone", kind="physical model", detail=r"our mix, \ Part 54's phone", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["monitors"], st["phone"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["phone"], c.duration, buff=0.08)
        with self.voiceover(
            "On the phone the mix is small and the kick has almost vanished, but the bass line is still there, as a bright, "
            "plucky tone: its harmonics carry it. Engineers add harmonics on purpose, by saturation, so that the bass "
            "survives small loudspeakers."
        ):
            self.play(Indicate(boxes[1], color=EAR, scale_factor=1.04))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def checks(self):
        items = [
            (r"reference tracks: \ finished records in the same style, \ at the same loudness, \ switched in and out", WHITE),
            (r"small speakers: \ the Auratone cube \ (1958) \ and Yamaha's NS-10 \ (1978) \ sat on consoles for decades as the `bad' check", WHITE),
            (r"mono, \ the car, \ earbuds, \ a laptop: \ a mix that works on all of them translates", WHITE),
            (r"meters for what ears miss: \ loudness \ (Part 57), \ correlation, \ a spectrum against the references", WHITE),
            (r"and rest: \ ears adapt in minutes; \ a mix heard fresh the next morning is often a different mix", TUNE),
        ]
        rows_scene(self, r"checking a mix", items,
                   "So engineers check. <bookmark mark='b'/> Against reference tracks: finished records in the same style, at the "
                   "same loudness, switched in and out. <bookmark mark='c'/> On small speakers: the Auratone cube of 1958 and "
                   "Yamaha's NS-10 of 1978 sat on consoles for decades as familiar reference checks, not simply because they were bad. <bookmark mark='d'/> In mono, "
                   "in the car, on earbuds and laptops: a mix that works on all of them is said to translate. "
                   "<bookmark mark='e'/> With meters, for what ears miss: loudness, which is Part 57, correlation, and a spectrum "
                   "against the references. <bookmark mark='f'/> And with rest: ears adapt within minutes, and a mix heard fresh "
                   "the next morning is often a different mix.", marks="bcdef")
