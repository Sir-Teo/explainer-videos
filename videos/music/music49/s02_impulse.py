from __future__ import annotations

import numpy as np

from videos.music.music49.common import *  # noqa: F403


class Impulse(SoundScene):
    def construct(self):
        chapter(self, 1, r"Impulse responses and convolution", r"How can one click describe a whole effect?")
        self.idea()
        self.convolution()
        self.echo()
        self.fft()
        self.fir_iir()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"a linear, \ time-invariant system: \ twice the input gives twice the output; \ later input, \ later output", WHITE),
            (r"feed it a single click, \ an impulse; \ what comes out is its impulse response", WHITE),
            (r"any input is a row of clicks of different sizes", WHITE),
            (r"so the output is a row of impulse responses, \ each scaled and delayed, \ added up: \ convolution", TUNE),
            (r"filters, \ echoes, \ rooms and plates are all linear and time-invariant, \ near enough", GREY_A),
        ]
        rows_scene(self, r"one click says everything", items,
                   "One idea runs through this part. <bookmark mark='b'/> Take a system that is linear and time-invariant: twice "
                   "the input gives twice the output, and a later input gives the same output later. <bookmark mark='c'/> Feed it "
                   "a single click, an impulse. What comes out is its impulse response. <bookmark mark='d'/> Any input is just a "
                   "row of clicks of different sizes, one per sample, <bookmark mark='e'/> so the output is a row of impulse "
                   "responses, each scaled and delayed, added up. That is convolution. <bookmark mark='f'/> Filters, echoes, "
                   "rooms and plates are all linear and time-invariant, near enough.", marks="bcdef")

    # ------------------------------------------------------------------
    def convolution(self):
        d = load("conv")
        x, h, y, rows = d["x"], d["h"], d["y"], d["rows"]
        sc = 0.9
        def row_stems(vals, start, color, y0):
            g = VGroup()
            for k, v in enumerate(vals):
                xk = -5.0 + 1.0 * (start + k)
                g.add(VGroup(Line([xk, y0, 0], [xk, y0 + sc * v, 0], color=color, stroke_width=4), Dot([xk, y0 + sc * v, 0], radius=0.07, color=color)))
            return g
        xin = row_stems(x, 0, WHITE, 2.4)
        hin = row_stems(h, 0, BLUE, 2.4).shift(RIGHT * 6.5)
        lx = label(r"the input: \ four samples", font_size=17, color=WHITE).move_to([-3.5, 3.3, 0])
        lh = label(r"the impulse response: \ four taps", font_size=17, color=BLUE).move_to([3.0, 3.3, 0])
        copies = VGroup()
        for k, r in enumerate(rows):
            copies.add(row_stems(r, k, [TUNE, EAR, GOLD, "#A3E635"][k], 1.0 - 0.75 * k))
        base = VGroup(*[Line([-5.3, 1.0 - 0.75 * k, 0], [3.3, 1.0 - 0.75 * k, 0], color=GREY_B, stroke_width=0.8) for k in range(4)])
        out = row_stems(y, 0, WHITE, -2.9)
        lo = label(r"their sum: \ the output", font_size=17, color=WHITE).move_to([-3.6, -3.55, 0])
        head = label(r"convolution, \ sample by sample", font_size=24, color=GREY_A).to_edge(UP, buff=0.2)
        with self.voiceover(
            "Watch it with four samples. <bookmark mark='a'/> The input: one, a half, minus point three, point eight. "
            "<bookmark mark='b'/> The impulse response: one, nothing, point six, point three, a sound and two faint echoes. "
            "<bookmark mark='c'/> The first input sample launches a copy of the response at full size; <bookmark mark='d'/> "
            "the second, a half-size copy one step later; <bookmark mark='e'/> the third, a small upside-down copy; the "
            "fourth, a copy at point eight. <bookmark mark='f'/> Add the columns: that is the output. Seven numbers, and "
            "every one is a sum of products."
        ) as vo:
            self.play(FadeIn(head), FadeIn(base))
            vo.wait_until("a")
            self.play(FadeIn(xin), FadeIn(lx))
            vo.wait_until("b")
            self.play(FadeIn(hin), FadeIn(lh))
            vo.wait_until("c")
            self.play(TransformFromCopy(hin, copies[0]))
            vo.wait_until("d")
            self.play(TransformFromCopy(hin, copies[1]))
            vo.wait_until("e")
            self.play(TransformFromCopy(hin, copies[2]), TransformFromCopy(hin, copies[3]))
            vo.wait_until("f")
            self.play(TransformFromCopy(copies, out), FadeIn(lo))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def echo(self):
        d = load("echo")
        c = clip("echo.two")
        ax = frame_axes(width=6.0, height=1.8, xlo=0, xhi=200, ylo=0, yhi=1.1, center=DOWN * 0.6)
        st_ = stems([0, d["delay_ms"]], [1.0, d["gain"]], ax.to, color=TUNE, r=0.09)
        ticks = VGroup(*[label(f"{v} ms", font_size=15, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.1) for v in (0, 100, 180)])
        lab = label(rf"an impulse response of two taps: \ the sound, \ and a copy {d['delay_ms']} ms later at {d['gain']}", font_size=18, color=WHITE).next_to(ax, UP, buff=0.3)
        head = label(r"the simplest effect: \ an echo", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The simplest effect of all is a two-tap response: the sound itself, and a copy a hundred and eighty "
            "milliseconds later at six-tenths of the level. Convolve the Tune with it: first dry, then with its echo, the "
            "slapback of a 1950s record."
        ):
            self.play(FadeIn(head), FadeIn(ax), FadeIn(st_), FadeIn(ticks), FadeIn(lab))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"dry, \ then an echo", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, st_[0], st["dry"], st["echo"] - 0.3, buff=0.1)
            pulse(snd, st_, st["echo"], c.duration, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fft(self):
        items = [
            (r"a room's response at 48 kHz lasts 2 seconds: \ 96,000 taps, \ 96,000 multiplications for every output sample", WHITE),
            (r"the Fourier transform turns convolution into multiplication, \ frequency by frequency \ (Part 3)", WHITE),
            (r"by the fast Fourier transform, \ the cost per sample grows only with the logarithm of the length", WHITE),
            (r"convolution reverb splits the response into blocks, \ so the first sound comes out without waiting", TUNE),
            (r"every reverb in this part's Variation is applied this way: \ the room, \ the plate and the spring are their impulse responses", GREY_A),
        ]
        rows_scene(self, r"convolution at scale", items,
                   "Convolution is simple but costly. <bookmark mark='b'/> A room's response at forty-eight kilohertz lasts a "
                   "couple of seconds: ninety-six thousand taps, so ninety-six thousand multiplications for every output sample. "
                   "<bookmark mark='c'/> The Fourier transform of Part 3 turns convolution into multiplication, frequency by "
                   "frequency, <bookmark mark='d'/> and with the fast Fourier transform the cost per sample grows only with the "
                   "logarithm of the length. <bookmark mark='e'/> Convolution reverbs split the response into blocks, so the "
                   "first sound comes out without waiting for the whole. <bookmark mark='f'/> Every reverb in this part's "
                   "Variation is applied this way: the room, the plate and the spring are simply their impulse responses.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def fir_iir(self):
        items = [
            (r"an FIR filter is a finite list of taps: \ its impulse response ends", WHITE),
            (r"an IIR filter feeds its output back: \ its response, \ in principle, \ never ends", WHITE),
            (r"FIR filters are always stable and can have exactly linear phase, \ but need many taps for a sharp edge", WHITE),
            (r"IIR filters make sharp edges and long decays from a few numbers, \ but can ring and can go unstable", TUNE),
            (r"chapter 2 builds the IIR kind from a single number", GREY_A),
        ]
        rows_scene(self, r"finite and infinite", items,
                   "Filters come in two families. <bookmark mark='b'/> An FIR filter, finite impulse response, is a finite list of "
                   "taps: its impulse response ends. <bookmark mark='c'/> An IIR filter feeds its own output back, so its response, "
                   "in principle, never ends. <bookmark mark='d'/> FIR filters are always stable and can have exactly linear "
                   "phase, but need many taps for a sharp edge. <bookmark mark='e'/> IIR filters make sharp edges and long decays "
                   "from a handful of numbers, but they can ring, and they can go unstable. <bookmark mark='f'/> Chapter two builds "
                   "the IIR kind from a single number.", marks="bcdef")
