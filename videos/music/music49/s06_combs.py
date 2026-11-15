from __future__ import annotations

import numpy as np

from videos.music.music49.common import *  # noqa: F403


class Combs(SoundScene):
    def construct(self):
        chapter(self, 5, r"Combs, \ flangers, \ choruses and phasers", r"What does a single delay do to a sound?")
        self.combs()
        self.pitch()
        self.mods()
        self.history()
        self.everyday()

    # ------------------------------------------------------------------
    def combs(self):
        d = load("combs")
        f = d["f"]
        a1 = logf_axes(width=5.4, height=2.6, flo=100, fhi=24000, ylo=-30, yhi=22, center=LEFT * 3.3 + DOWN * 0.6, ticks=(1000, 10000))
        a2 = logf_axes(width=5.4, height=2.6, flo=100, fhi=24000, ylo=-30, yhi=22, center=RIGHT * 3.3 + DOWN * 0.6, ticks=(1000, 10000))
        c1 = curve(f, np.clip(d["ff"], -30, 22), a1.to, color=BLUE, width=2.5)
        c2 = curve(f, np.clip(d["fb"], -30, 22), a2.to, color=TUNE, width=2.5)
        l1 = VGroup(MathTex(r"y[n] = x[n] + 0.9\,x[n-48]", font_size=30), label(r"feedforward: \ notches, \ every 1 kHz", font_size=17, color=BLUE)).arrange(DOWN, buff=0.15).next_to(a1, UP, buff=0.3)
        l2 = VGroup(MathTex(r"y[n] = x[n] + 0.9\,y[n-48]", font_size=30), label(r"feedback: \ peaks, \ every 1 kHz", font_size=17, color=TUNE)).arrange(DOWN, buff=0.15).next_to(a2, UP, buff=0.3)
        head = label(r"one delay, \ added back", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            f"Add a sound to a copy of itself delayed by forty-eight samples, one millisecond. <bookmark mark='a'/> Where a "
            "frequency's copy arrives half a cycle late, the two cancel: a notch, at five hundred hertz, fifteen hundred, "
            "twenty-five hundred, a row of them like the teeth of a comb. <bookmark mark='b'/> Feed the output back instead, "
            "and the frequencies whose cycles fit the delay a whole number of times build up: peaks every kilohertz, as tall "
            "as the feedback is strong."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a1), FadeIn(a2))
            vo.wait_until("a")
            self.play(FadeIn(l1), Create(c1))
            vo.wait_until("b")
            self.play(FadeIn(l2), Create(c2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pitch(self):
        d = load("combs")
        c = clip("combs.two")
        a = frame_axes(width=9.0, height=1.6, xlo=0, xhi=1, ylo=-1, yhi=1, center=UP * 0.6)
        rng = np.random.default_rng(1)
        k = np.linspace(0, 1, 300)
        burst = VGroup(a, curve(k, rng.uniform(-0.9, 0.9, 300) * np.exp(-k * 3), a.to, color=GREY_A, width=1.2))
        loop = VGroup(RoundedRectangle(width=4.2, height=1.1, corner_radius=0.2, stroke_color=TUNE),
                      label(rf"delay {d['Dp']} samples, \ gain 0.985, \ fed back", font_size=19, color=TUNE)).arrange(ORIGIN).move_to(DOWN * 1.4)
        out = label(rf"a pitch: \ 48,000 / {d['Dp']} $\approx$ {d['pitch']:.0f} Hz", font_size=22, color=WHITE).next_to(loop, DOWN, buff=0.35)
        head = label(r"noise in, \ a note out", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"A feedback comb is a pitch. Put twenty milliseconds of noise into one with a delay of {say(d['Dp'])} samples and "
            f"a gain of 0.985: every peak is a harmonic of forty-eight thousand over {say(d['Dp'])}, about {say(d['pitch'])} "
            "hertz. Listen: first the burst alone, then through the comb."
        ):
            self.play(FadeIn(head), FadeIn(burst), FadeIn(loop), FadeIn(out))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"noise, \ then a comb", kind="synthesized", detail=r"white noise, \ a feedback comb", corner=DL, tag_corner=DR)
            pulse(snd, burst, st["burst"], st["comb"] - 0.3, buff=0.1)
            pulse(snd, loop, st["comb"], c.duration, buff=0.1)
        with self.voiceover(
            "That is a plucked string, nearly: Part 7's Karplus-Strong algorithm is this comb with a gentle low-pass in the "
            "loop. A delay fed back is a string."
        ):
            self.play(Indicate(out, color=TUNE))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mods(self):
        d = load("mods")
        c = clip("mods.three")
        cells = VGroup()
        for name, desc in ((r"flanger", r"a 0.5 to 4.5 ms delay, \ swept, \ fed back: \ the comb's teeth slide"),
                           (r"chorus", r"three copies 15 to 25 ms late, \ each wandering: \ slightly detuned doubles"),
                           (r"phaser", r"eight all-passes, \ their frequency swept: \ four notches that move")):
            cells.add(VGroup(RoundedRectangle(width=3.8, height=2.2, corner_radius=0.15, stroke_color=GREY_B),
                             VGroup(label(name, font_size=26, color=TUNE), label(desc, font_size=16, color=GREY_A).set_width(3.4)).arrange(DOWN, buff=0.3)).arrange(ORIGIN))
        cells.arrange(RIGHT, buff=0.4).move_to(UP * 0.2)
        head = label(r"a pad, \ through three moving delays", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Now let the delay move. A sustained chord, a pad, through three classic effects. A flanger: a very short delay, "
            "swept, with feedback, so the comb's teeth slide up and down. A chorus: three copies, each delayed a little "
            "longer and wandering, like several players not quite together. A phaser: all-passes whose frequency is swept, "
            "so that, summed with the dry sound, they cut a few notches that move."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"three moving delays", kind="synthesized", detail=r"Part 40's pad", corner=DL, tag_corner=DR)
            keys = d["order"]
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i < 2 else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"flanging began with two tape machines playing the same tape, \ one slowed by a thumb on its reel's flange", WHITE),
            (r"Les Paul experimented with it in the 1940s and 50s; \ it was everywhere in late-1960s rock", WHITE),
            (r"the chorus came in pedals and string machines in the 1970s; \ the phaser too, \ from the all-pass stages of analogue circuits", WHITE),
            (r"all three are one or a few delays, \ changing slowly", TUNE),
            (r"chapter 6: \ what thousands of delays do, \ in a room", GREY_A),
        ]
        rows_scene(self, r"a thumb on a reel", items,
                   "These effects have a mechanical past. <bookmark mark='b'/> Flanging began with two tape machines playing the "
                   "same recording, one slowed by a thumb pressed on the flange of its reel. <bookmark mark='c'/> Les Paul "
                   "experimented with it in the 1940s and 50s, and it was everywhere in late-1960s rock. <bookmark mark='d'/> The "
                   "chorus arrived in pedals and string machines in the 1970s, and the phaser too, built from the all-pass stages "
                   "of analogue circuits. <bookmark mark='e'/> All three are one or a few delays, changing slowly. "
                   "<bookmark mark='f'/> Chapter six asks what thousands of delays do, in a room.", marks="bcdef")

    # ------------------------------------------------------------------
    def everyday(self):
        items = [
            (r"comb filtering happens by accident everywhere sound and its reflection meet", WHITE),
            (r"a microphone 0.5 m from a wall hears the wall's echo 3 ms late: \ notches every 340 Hz", WHITE),
            (r"two microphones on one source at different distances do the same when mixed", WHITE),
            (r"that is why engineers check a mix in mono, \ and why a moving singer can sound phasey", TUNE),
            (r"the cure is distance, \ absorption, \ or a small delay to line the two up", GREY_A),
        ]
        rows_scene(self, r"combs by accident", items,
                   "Comb filtering also happens by accident. <bookmark mark='b'/> Wherever a sound meets its own reflection, "
                   "the two add like a feedforward comb. <bookmark mark='c'/> A microphone half a metre from a wall hears the "
                   "wall's echo about three milliseconds late, with notches every three hundred and forty hertz. "
                   "<bookmark mark='d'/> Two microphones on one source at different distances do the same when they are mixed. "
                   "<bookmark mark='e'/> That is why engineers check a mix in mono, and why a singer moving near a desk can sound "
                   "phasey. <bookmark mark='f'/> The cure is distance, absorption, or a small delay to line the two up.",
                   marks="bcdef")
