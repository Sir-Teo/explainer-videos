from __future__ import annotations

import numpy as np

from videos.music.music53.common import *  # noqa: F403


class Limits(SoundScene):
    def construct(self):
        chapter(self, 4, r"MIDI's limits, \ MPE and MIDI 2.0", r"What can't a 1983 protocol say?")
        self.steps()
        self.zipper()
        self.bend()
        self.mpe()
        self.two()
        self.right()

    # ------------------------------------------------------------------
    def steps(self):
        d = load("zipper")
        t = np.array(d["curve_t"])
        ax = frame_axes(width=9.0, height=3.2, xlo=0, xhi=t[-1], ylo=150, yhi=2100, center=DOWN * 0.3)
        a = curve(t, d["stepped"], ax.to, color=EAR, width=2.5)
        b = curve(t, d["smooth"], ax.to, color=TUNE, width=2)
        zoom = Rectangle(width=1.2, height=0.6, stroke_color=WHITE, stroke_width=1.5).move_to(ax.to(2.0, 630))
        key = VGroup(label(r"a controller: \ 128 values, \ sent every 10 ms", font_size=17, color=EAR), label(r"smooth", font_size=17, color=TUNE)).arrange(RIGHT, buff=0.8).to_edge(UP, buff=1.0)
        note = label(rf"200 Hz to 2 kHz in 127 steps: \ each step {d['step_cents']:.0f} cents, \ a third of a semitone", font_size=18, color=WHITE).to_edge(DOWN, buff=0.45)
        head = label(r"seven bits", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The first limit is seven bits. <bookmark mark='a'/> A controller has a hundred and twenty-eight values. Sweep a "
            "filter's cutoff from two hundred hertz to two kilohertz with one, and it moves in a staircase of a hundred and "
            f"twenty-seven steps, each {say(d['step_cents'])} cents, a third of a semitone, <bookmark mark='b'/> where the "
            "smooth sweep glides."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ghost(VGroup(a, b), 0.3)))
            vo.wait_until("a")
            self.play(Create(a), FadeIn(key[0]), FadeIn(note), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(b), FadeIn(key[1]), Create(zoom))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def zipper(self):
        d = load("zipper")
        c = clip("zipper.two")
        cells = choice_boxes([r"7-bit controller", r"smooth"], width=3.8, buff=1.0, colors=[EAR, TUNE]).move_to(UP * 0.4)
        cap = label(r"a resonant ladder \ (Part 51), \ $k = 3.6$, \ swept over four seconds", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"zipper noise, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear it with Part 51's resonant ladder: the stepped sweep, then the smooth one."):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"stepped, \ then smooth", kind="synthesized", detail=r"sawtooth and ladder", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["stepped"], st["smooth"] - 0.3, buff=0.08)
            pulse(snd, cells[1], st["smooth"], c.duration, buff=0.08)
        with self.voiceover(
            "The stepped sweep clicks its way up: the resonant whistle jumps from step to step, a sound engineers call zipper "
            "noise. Synthesizers learned to smooth incoming controllers; MIDI 1.0 had in fact allowed fourteen-bit "
            "controllers from the start, two paired together, but few devices used them."
        ):
            self.play(Indicate(cells[0], color=EAR, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bend(self):
        d = load("bytes")
        bc = d["bend_cents"]
        rows = VGroup(
            label(r"pitch bend: \ 14 bits, \ 16,384 steps", font_size=22, color=WHITE),
            label(rf"over $\pm 2$ semitones: \ {bc['2']:.3f} cents a step: \ finer than any ear", font_size=19, color=TUNE),
            label(rf"over $\pm 48$ semitones \ (an MPE default): \ {bc['48']:.2f} cents a step: \ still fine", font_size=19, color=TUNE),
            label(r"but one bend per channel: \ bend one note of a chord and every note on the channel bends", font_size=19, color=EAR),
            label(r"a keyboard sends one pressure per channel too: \ an instrument's voice is not a key", font_size=18, color=GREY_A),
        ).arrange(DOWN, buff=0.35).move_to(DOWN * 0.1)
        head = label(r"the second limit: \ one channel, \ one bend", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Pitch is better served. <bookmark mark='a'/> A bend has fourteen bits. Over two semitones each step is "
            f"{say(bc['2'], 3)} of a cent, finer than any ear; <bookmark mark='b'/> over forty-eight semitones it is still "
            f"{say(bc['48'], 2)} of a cent. <bookmark mark='c'/> The real limit is that there is one bend per channel: bend one "
            "note of a chord and every note on that channel bends with it. <bookmark mark='d'/> A guitarist bends one string; a "
            "violinist slides one finger; MIDI 1.0, built around a keyboard, cannot say that."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mpe(self):
        items = [
            (r"MIDI Polyphonic Expression \ (MPE, \ adopted 2018): \ give every sounding note a channel of its own", WHITE),
            (r"then each note can carry its own bend, \ its own pressure, \ its own controller: \ a slide, \ a swell, \ a vibrato", WHITE),
            (r"fifteen notes at once, \ one channel left for messages to all of them", WHITE),
            (r"made for instruments that sense each finger: \ pressure, \ sideways slide, \ forward glide", TUNE),
            (r"a workaround inside the old protocol: \ no new cable needed", GREY_A),
        ]
        rows_scene(self, r"one note, \ one channel", items,
                   "The first answer was a workaround. <bookmark mark='b'/> MIDI Polyphonic Expression, MPE, adopted in 2018, gives "
                   "every sounding note a channel of its own. <bookmark mark='c'/> Then each note can carry its own bend, its own "
                   "pressure and its own controller: a slide, a swell, a vibrato. <bookmark mark='d'/> That allows fifteen notes at "
                   "once, with one channel left for messages to all of them. <bookmark mark='e'/> It was made for instruments that "
                   "sense each finger's pressure, sideways slide and forward glide. <bookmark mark='f'/> And it lives inside the old "
                   "protocol: no new cable was needed.", marks="bcdef")

    # ------------------------------------------------------------------
    def two(self):
        items = [
            (r"MIDI 2.0 \ (adopted 2020): \ messages in 32-bit packets \ (the Universal MIDI Packet), \ not a byte stream", WHITE),
            (r"velocity with 16 bits, \ controllers with 32: \ no more staircases", WHITE),
            (r"per-note controllers and per-note pitch, \ built in rather than borrowed from channels", WHITE),
            (r"devices that describe themselves to each other, \ and fall back to MIDI 1.0 when they must", WHITE),
            (r"the five-pin cable remains for MIDI 1.0; \ the new packets travel over USB and networks", TUNE),
        ]
        rows_scene(self, r"MIDI 2.0", items,
                   "Then came a new version. <bookmark mark='b'/> MIDI 2.0, adopted in 2020, sends messages in thirty-two-bit "
                   "packets, the Universal MIDI Packet, rather than a byte stream. <bookmark mark='c'/> Velocity gets sixteen bits "
                   "and controllers thirty-two: no more staircases. <bookmark mark='d'/> Per-note controllers and per-note pitch are "
                   "built in rather than borrowed from channels. <bookmark mark='e'/> Devices describe themselves to each other, and "
                   "fall back to MIDI 1.0 when they must. <bookmark mark='f'/> The five-pin cable remains for MIDI 1.0; the new "
                   "packets travel over USB and networks.", marks="bcdef")

    # ------------------------------------------------------------------
    def right(self):
        items = [
            (r"what MIDI got right: \ it describes gestures, \ not sounds, \ so any instrument can obey any controller", WHITE),
            (r"it was small enough for an 8-bit processor of 1983 to read in real time", WHITE),
            (r"it was free to use: \ no licence fee, \ so every maker adopted it", WHITE),
            (r"it was backward compatible for forty years: \ a 1983 keyboard still plays a 2024 plug-in", WHITE),
            (r"few standards have lasted as long with so little change", TUNE),
        ]
        rows_scene(self, r"what MIDI got right", items,
                   "Despite its limits, MIDI got a great deal right. <bookmark mark='b'/> It describes gestures, not sounds, so any "
                   "instrument can obey any controller. <bookmark mark='c'/> It was small enough for an eight-bit processor of 1983 to "
                   "read in real time. <bookmark mark='d'/> It was free to use, with no licence fee, so every maker adopted it. "
                   "<bookmark mark='e'/> And it stayed backward compatible for forty years: a 1983 keyboard still plays a modern "
                   "plug-in. <bookmark mark='f'/> Few standards have lasted as long with so little change.", marks="bcdef")
