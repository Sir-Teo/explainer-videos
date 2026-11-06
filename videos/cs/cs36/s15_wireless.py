from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs36.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load)


class Wireless(VoiceoverScene):
    def construct(self):
        self.card()
        self.fading()
        self.ofdm()
        self.mimo()

    def card(self):
        card = chapter_card(14, r"Wireless", r"How do you send bits through air that fights back?", lit=(1966, 1998),
                            extra=((1966, r"Chang: \ OFDM"), (1998, r"Foschini and Gans: \ MIMO capacity")), part=PART)
        with self.voiceover("Chapter fourteen. Wireless."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def fading(self):
        w = load("wireless")
        head = label(r"Fading", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 30, 5], y_range=[-5, 0, 1], x_length=6.4, y_length=3.8,
                  axis_config={"color": GREY_D, "include_numbers": False}).move_to([-2.6, -0.3, 0])
        xt = VGroup(*[label(str(x), font_size=16, color=GREY_B).next_to(ax.c2p(x, -5), DOWN, buff=0.1)
                      for x in (0, 10, 20, 30)])
        yt = VGroup(*[MathTex(rf"10^{{{y}}}", font_size=17, color=GREY_B).next_to(ax.c2p(0, y), LEFT, buff=0.1)
                      for y in range(-5, 1)])
        xl = label(r"signal-to-noise, \ dB", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yl = label(r"bit error rate, \ BPSK", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        fa = [f for f in w["fading"]]
        aw = [(f["snr_db"], np.log10(f["awgn"])) for f in fa if f["awgn"] > 0]
        ry = [(f["snr_db"], np.log10(f["rayleigh"])) for f in fa]
        ca = VMobject(color=YES, stroke_width=3).set_points_as_corners([ax.c2p(x, max(y, -5)) for x, y in aw])
        cr = VMobject(color=NO, stroke_width=3).set_points_as_corners([ax.c2p(x, y) for x, y in ry])
        la = label(r"a wire: \ Gaussian noise", font_size=18, color=YES).next_to(ax.c2p(8, -4.6), RIGHT, buff=0.1)
        lr = label(r"radio: \ Rayleigh fading", font_size=18, color=NO).next_to(ax.c2p(18, -2.4), UP, buff=0.1)
        lines = VGroup(
            wrapped_label(r"reflections arrive with different delays; \ they add, \ or cancel: \ the signal's strength "
                  r"swings by 100 times as you move a few centimetres", 6.0, font_size=19, color=WHITE),
            wrapped_label(r"errors fall exponentially with SNR on a wire, \ but only as $1/\text{SNR}$ when fading: \ at 10 dB, "
                  r"\ $4 \times 10^{-6}$ on one, \ $2 \times 10^{-2}$ on the other", 6.0, font_size=19, color=NO),
            wrapped_label(r"the remedy is \textbf{diversity}: \ send over several frequencies, \ times or antennas, \ so "
                  r"that not all fade at once", 6.0, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.5, 0.0, 0])
        lines.move_to([3.6, 0.0, 0])
        with self.voiceover(
            "Radio adds an enemy that wires do not have. <bookmark mark='a'/> A signal reaches the receiver along "
            "many paths, bouncing off walls and buildings, and the copies arrive at slightly different times. They "
            "add or cancel, and moving a few centimetres can change the received power a hundredfold. This is "
            "fading. <bookmark mark='b'/> On a wire, errors fall exponentially as the signal grows. Under fading they "
            "fall only in proportion: in our simulation, at ten decibels, a wire makes four errors in a million "
            "bits, and a fading channel one in forty. <bookmark mark='c'/> The cure is never to depend on one path: "
            "spread the bits over many frequencies, times or antennas, so that they do not all fade together."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(Create(ca), Create(cr), FadeIn(la), FadeIn(lr), FadeIn(lines[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def ofdm(self):
        w = load("wireless")
        head = label(r"OFDM: \ many slow carriers", font_size=36).to_edge(UP, buff=0.3)
        H = w["H"]
        bars = VGroup(*[Rectangle(width=0.08, height=max(0.03, 0.9 * h), stroke_width=0,
                                  fill_color=HEAD if h > 0.5 else NO, fill_opacity=0.85) for h in H]).arrange(
            RIGHT, buff=0.02, aligned_edge=DOWN).move_to([-2.8, 1.0, 0])
        bl = label(r"the channel's gain on each of 64 subcarriers \ (a five-path echo)", font_size=17,
                   color=GREY_A).next_to(bars, DOWN, buff=0.15)
        rows = [[str(o["cp"]), f"{o['ber']:.4f}"] for o in w["ofdm"]]
        tab = grid_table([r"cyclic prefix, \ samples", r"bit errors, \ 30 dB"], rows, widths=[3.0, 2.6], row_h=0.4,
                         font_size=19, mono_cols=())
        tab.move_to([3.6, 1.0, 0])
        for r, o in enumerate(w["ofdm"], start=1):
            tab.cells[r][1].set_color(YES if o["cp"] >= 4 else NO)
        lines = VGroup(
            label(r"split the band into many narrow subcarriers: \ each sees a flat channel, \ one complex gain",
                  font_size=20, color=WHITE),
            label(r"an inverse FFT \ (Part 19) \ builds the symbol; \ an FFT takes it apart; \ divide each carrier by "
                  r"its gain", font_size=20, color=HEAD),
            label(r"a \textbf{cyclic prefix} longer than the echo turns the echo into a circular convolution, \ which "
                  r"the FFT diagonalizes", font_size=20, color=YES),
            label(r"Wi-Fi, \ 4G, \ 5G \ and DSL all work this way; \ deep-faded carriers are rescued by coding",
                  font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.4)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "Echoes also smear one symbol into the next. <bookmark mark='a'/> The modern answer is to send many "
            "slow streams instead of one fast one: split the band into dozens or thousands of narrow subcarriers. "
            "Each is so narrow that the channel looks to it like a single multiplier, which the receiver can divide "
            "out. <bookmark mark='b'/> The transmitter builds the whole symbol with one inverse FFT, the algorithm of "
            "Part 19, and the receiver takes it apart with another. <bookmark mark='c'/> One trick makes it exact: "
            "repeat the end of each symbol at its start, a cyclic prefix longer than the longest echo. Then the echo "
            "is a circular convolution, which the FFT turns into multiplication. In our simulation, without the "
            "prefix, two bits in a hundred are wrong; with a prefix as long as the echo, about one in a thousand, "
            "from carriers in a deep fade. <bookmark mark='d'/> This is OFDM, the waveform of Wi-Fi, 4G, 5G and DSL."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), FadeIn(bl),
                      FadeIn(lines[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def mimo(self):
        w = load("wireless")
        head = label(r"MIMO: \ more antennas, \ more channels", font_size=36).to_edge(UP, buff=0.3)
        eq = MathTex(r"C = \mathbb{E} \log_2 \det\!\Big(I + \frac{\text{SNR}}{n_t} H H^{*}\Big)", font_size=38,
                     color=HEAD).next_to(head, DOWN, buff=0.45)
        rows = [[rf"{m['n']} $\times$ {m['n']}", f"{m['c10']:.1f}", f"{m['c20']:.1f}"] for m in w["mimo"]]
        tab = grid_table([r"antennas", r"bits/s/Hz at 10 dB", r"at 20 dB"], rows, widths=[2.4, 3.0, 2.2], row_h=0.42,
                         font_size=20, mono_cols=())
        tab.next_to(eq, DOWN, buff=0.5).set_x(0)
        for r in range(1, 5):
            tab.cells[r][2].set_color(YES)
        lines = VGroup(
            label(r"with $n$ antennas at each end and a rich scattering of paths, \ the matrix $H$ has $n$ strong "
                  r"independent directions", font_size=20, color=WHITE),
            label(r"capacity grows \textbf{linearly} in $n$, \ with no more power or bandwidth: \ Foschini and Gans, \ "
                  r"Telatar \ (1998--99)", font_size=20, color=YES),
            label(r"the echoes that caused fading become parallel channels: \ 5G base stations carry 64 antennas",
                  font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The last trick turns the enemy into an ally. <bookmark mark='a'/> Put several antennas at each end. With "
            "many paths between them, the channel is a random matrix, and the capacity is the expected log "
            "determinant of this expression. <bookmark mark='b'/> We averaged it over four hundred random channels. "
            "One antenna at each end, at twenty decibels: six bits per second per hertz. Two: eleven. Four: twenty-two. "
            "Eight: forty-four. <bookmark mark='c'/> Capacity grows linearly with the number of antennas, with no extra "
            "power and no extra spectrum. Gerard Foschini and Emre Telatar showed it in the late 1990s. "
            "<bookmark mark='d'/> The scattering that caused fading has become a set of parallel channels, and a 5G "
            "base station now carries sixty-four antennas."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(eq), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()


_ = (DATA, KERN)
