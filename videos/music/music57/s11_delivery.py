from __future__ import annotations

import numpy as np

from videos.music.music57.common import *  # noqa: F403


class Delivery(SoundScene):
    def construct(self):
        chapter(self, 10, r"Vinyl, \ files and this series", r"What does each medium ask of a master?")
        self.groove()
        self.riaa()
        self.heard()
        self.files()
        self.ours()

    # ------------------------------------------------------------------
    def groove(self):
        d = load("vinyl")
        f = np.array(d["f"])
        ax = logf_axes(width=7.2, height=3.0, flo=20, fhi=20000, ylo=-1, yhi=3.0, center=DOWN * 0.3 + LEFT * 2.2)
        ax[0].put_start_and_end_on(ax.to(20, -1), ax.to(20000, -1))
        exc = curve(f, np.log10(np.array(d["excursion_um"])), ax.to, color=TUNE, width=3)
        yt = VGroup(*[label(rf"{v} $\mu$m", font_size=14, color=GREY_A).next_to(ax.to(20, np.log10(v)), LEFT, buff=0.1) for v in (0.1, 1, 10, 100, 1000)])
        items = text_rows([(r"a lateral groove: \ the stylus's sideways velocity is the signal", WHITE), (r"excursion $=$ velocity $/ 2\pi f$: \ bass swings wide", WHITE),
                           (rf"5 cm/s: \ {d['exc_50']:.0f} $\mu$m at 50 Hz, \ {d['exc_5k']:.1f} $\mu$m at 5 kHz", TUNE),
                           (r"wide swings mean wide spacing: \ a louder or bassier cut is a shorter side", WHITE)], font_size=17, width=4.4).next_to(ax, RIGHT, buff=0.4)
        head = label(r"the groove", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "First, the oldest medium still sold. <bookmark mark='a'/> A record's groove wiggles sideways, and the stylus's "
            "velocity is the signal. <bookmark mark='b'/> For a given velocity the swing is the velocity over two pi f, so bass "
            "swings wide: at five centimetres a second, a hundred and fifty-nine micrometres at fifty hertz, under two at five "
            "kilohertz. <bookmark mark='c'/> Wide swings need wide spacing between turns, so a louder or bassier cut makes a "
            "shorter side. Vinyl enforced its own loudness limit, and low-frequency stereo difference is often controlled during cutting, depending on level, phase and the lathe, so that the two walls of the groove "
            "swing together."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yt), FadeIn(ghost(exc, 0.3)), FadeIn(items[0]))
            vo.wait_until("a")
            self.play(FadeIn(items[1]), Create(exc), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(items[2]))
            vo.wait_until("c")
            self.play(FadeIn(items[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def riaa(self):
        d = load("vinyl")
        f = np.array(d["f"])
        ax = logf_axes(width=9.6, height=3.0, flo=20, fhi=20000, ylo=-22, yhi=22, center=DOWN * 0.3)
        play_ = curve(f, d["riaa"], ax.to, color=TUNE, width=3)
        cut = curve(f, -np.array(d["riaa"]), ax.to, color=EAR, width=3)
        yt = VGroup(*[label(f"{v:+d} dB" if v else "0 dB", font_size=14, color=GREY_A).next_to(ax.to(20, v), LEFT, buff=0.1) for v in (20, 0, -20)])
        key = VGroup(label(r"cutting: \ bass down, \ treble up", font_size=16, color=EAR), label(r"playback \ (the RIAA curve): \ the inverse", font_size=16, color=TUNE)).arrange(RIGHT, buff=0.8).to_edge(UP, buff=1.0)
        eq = MathTex(r"H(s) = \frac{1 + s\,318\,\mu\text{s}}{(1 + s\,3180\,\mu\text{s})(1 + s\,75\,\mu\text{s})}", font_size=30, color=TUNE).to_edge(DOWN, buff=0.4)
        head = label(r"the RIAA curve \ (1954)", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "So records are cut with the bass turned down and the treble turned up, and every phono stage turns them back. "
            "<bookmark mark='a'/> The cutting curve: bass down by about twenty decibels at twenty hertz, treble up as much at "
            f"twenty kilohertz. <bookmark mark='b'/> The playback curve, the RIAA's of 1954, is its inverse: plus "
            f"{say(d['at']['20'], 1)} decibels at twenty hertz, minus {say(-d['at']['20000'], 1)} at twenty kilohertz, from three "
            "time constants. The treble boost on the way in and cut on the way out also turns down the record's surface noise."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yt), FadeIn(ghost(VGroup(play_, cut), 0.25)))
            vo.wait_until("a")
            self.play(Create(cut), FadeIn(key[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(play_), FadeIn(key[1]), FadeIn(eq), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("vinyl")
        c = clip("vinyl.two")
        boxes = choice_boxes([r"no de-emphasis", r"the RIAA curve"], width=3.2, height=0.9, buff=1.2, size=20).move_to(UP * 0.4)
        note = label(r"a record of our mix, \ played through a phono stage without its curve, \ then with it", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.5)
        head = label(r"a record, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear a record of our mix played without the curve, as a microphone input would, and then with it."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(note))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"flat, \ then RIAA", kind="physical model", detail=r"Part 56's session, \ simulated filters", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["flat"], st["riaa"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["riaa"], c.duration, buff=0.08)
        with self.voiceover("Without the curve the band is thin and harsh, all hi-hat and no bass; with it, the mix comes back."):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def files(self):
        items = [
            (r"CD: \ 44.1 kHz, \ 16 bits, \ dithered; \ the master must stay under 0 dBFS, \ and should stay under $-1$ dBTP", WHITE),
            (r"streaming: \ masters delivered at 24 bits and 44.1 to 96 kHz; \ the service encodes them, \ normalizes, \ and plays", WHITE),
            (r"lossy encoding \ (Part 58) \ overshoots: \ leave $-1$ dBTP, \ or $-2$ at low bit rates", WHITE),
            (r"broadcast: \ R 128's $-23$ LUFS and $-1$ dBTP; \ vinyl: \ its own master, \ mono bass, \ tamed treble, \ a side length", WHITE),
            (r"one mix, \ several masters", TUNE),
        ]
        rows_scene(self, r"one master for each medium", items,
                   "Each medium asks for its own master. <bookmark mark='b'/> The CD: forty-four point one kilohertz, sixteen bits, dithered, under nought dBFS and preferably under minus one true peak. <bookmark mark='c'/> Streaming distributors often accept twenty-four-bit masters, subject to their specifications, which the service encodes, normalizes and plays. <bookmark mark='d'/> Lossy encoding, Part 58's subject, overshoots, so leave minus one dBTP, or minus two at low bit rates. <bookmark mark='e'/> Broadcast: R 128's minus twenty-three. And vinyl its own master, with mono bass, tamed treble and a side length. <bookmark mark='f'/> One mix, several masters.", marks="bcdef")

    # ------------------------------------------------------------------
    def ours(self):
        d = load("series")
        rows = VGroup(VGroup(label(r"what", font_size=17, color=GREY_A), label(r"how it is set", font_size=17, color=GREY_A), label(r"level", font_size=17, color=GREY_A)))
        data = [(r"the narration", r"high-passed at 60 Hz, \ one gain to its loudness, \ a look-ahead limiter", r"$-16$ LUFS, \ limit $-2.5$ dBFS"),
                (r"an example in a listening window", r"one gain, \ set by its loudest 400 ms", rf"{d['example_level']:.0f} LUFS momentary"),
                (r"recent parts' examples", r"the same, \ 2.5 dB lower", rf"{d['part_level']:.1f} LUFS momentary"),
                (r"an example meant to sit back", r"the same", rf"{d['quiet_level']:.0f} LUFS momentary"),
                (r"the finished soundtrack", r"narration and music summed, \ never limited, \ measured", r"the build stops above $-1$ dBTP")]
        for a, b_, c_ in data:
            rows.add(VGroup(label(a, font_size=17, color=WHITE), label(b_, font_size=16, color=GREY_A), label(c_, font_size=17, color=TUNE)))
        rows.arrange(DOWN, buff=0.3)
        for r in rows:
            r[0].next_to([-6.4, r[0].get_y(), 0], RIGHT, buff=0)
            r[1].next_to([-2.0, r[0].get_y(), 0], RIGHT, buff=0)
            r[2].next_to([2.9, r[0].get_y(), 0], RIGHT, buff=0)
        rows.move_to(DOWN * 0.2)
        h = d["hook"]
        note = label(rf"this part's hook: \ loudest 400 ms {h['momentary_max']:.1f} LUFS, \ integrated {h['integrated']:.1f}, \ true peak {h['tp']:.1f} dBTP", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.35)
        head = label(r"how this series is mastered", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "And this series itself, which has been mastering all along. <bookmark mark='a'/> The narration is high-passed at "
            "sixty hertz, brought to minus sixteen LUFS by a single gain, and passed through a look-ahead limiter at about minus "
            "two and a half dBFS for its rare loud syllables. Every example is set by one gain from its loudest four hundred "
            "milliseconds: minus fifteen LUFS, two and a half lower in recent parts, minus twenty-one for one meant to sit back. "
            "<bookmark mark='b'/> The example-normalization stage does not limit music; individual synthesis and mastering demonstrations can intentionally process dynamics: the narration and the music are summed, measured, and the build "
            "stops if a single true peak passes minus one. Loudness differences are stated when they are the lesson, as in this part's bias demonstration; production levels must still be checked on the final narrated film."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:5]], lag_ratio=0.25), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(rows[5]), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()
