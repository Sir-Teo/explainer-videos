from __future__ import annotations

import numpy as np

from videos.music.music3.common import *  # noqa: F403


class Windows(SoundScene):
    def construct(self):
        chapter(self, 6, r"What a window costs", r"What happens at the edges of the stretch?", lit=(1807,),
                extra=((1978, r"Harris's survey of windows"),))
        self.cut()
        self.shapes()
        self.weak()

    # ------------------------------------------------------------------
    def cut(self):
        x = np.linspace(0, 1, 500)
        g1 = axes([0, 1], [-1.2, 1.2], x_length=5.4, y_length=1.9, xlabel=r"", ylabel=r"", xticks=[], yticks=[0], font_size=18)
        g2 = axes([0, 1], [-1.2, 1.2], x_length=5.4, y_length=1.9, xlabel=r"", ylabel=r"", xticks=[], yticks=[0], font_size=18)
        VGroup(g1, g2).arrange(RIGHT, buff=0.9).move_to(UP * 1.5)
        w1 = curve(g1.ax, x, np.sin(2 * np.pi * 5 * x), GOOD, stroke_width=2.5)
        w2 = curve(g2.ax, x, np.sin(2 * np.pi * 5.5 * x), BAD, stroke_width=2.5)
        c1 = label(r"exactly 5 cycles in the stretch", font_size=24, color=GOOD).next_to(g1, UP, buff=0.1)
        c2 = label(r"$5\tfrac{1}{2}$ cycles: \ it does not join up with itself", font_size=24, color=BAD).next_to(g2, UP, buff=0.1)
        n = 64
        k = np.arange(n)
        s1 = np.abs(np.fft.rfft(np.sin(2 * np.pi * 5 * k / n)))[:16] / (n / 2)
        s2 = np.abs(np.fft.rfft(np.sin(2 * np.pi * 5.5 * k / n)))[:16] / (n / 2)
        b1 = axes([0, 16], [0, 1.1], x_length=5.4, y_length=1.9, xlabel=r"frequency bin", ylabel=r"", xticks=[5, 10, 15], yticks=[], font_size=18)
        b2 = axes([0, 16], [0, 1.1], x_length=5.4, y_length=1.9, xlabel=r"frequency bin", ylabel=r"", xticks=[5, 10, 15], yticks=[], font_size=18)
        VGroup(b1, b2).arrange(RIGHT, buff=0.9).move_to(DOWN * 1.6)
        bars1 = VGroup(*[Line(b1.ax.c2p(i + 0.5, 0), b1.ax.c2p(i + 0.5, max(v, 0.004)), color=GOOD, stroke_width=7) for i, v in enumerate(s1)])
        bars2 = VGroup(*[Line(b2.ax.c2p(i + 0.5, 0), b2.ax.c2p(i + 0.5, max(v, 0.004)), color=BAD, stroke_width=7) for i, v in enumerate(s2)])
        tag = label(r"leakage: \ one pure tone, \ spilled into every bin", font_size=26, color=BAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "There is a catch in cutting a stretch out of a sound, and every picture of a spectrum is shaped by it. "
            "The transform treats the stretch as if it repeated for ever. <bookmark mark='a'/> If a tone fits a "
            "whole number of cycles into the stretch, fine: one tone, one bar. <bookmark mark='b'/> But a real tone "
            "has no reason to fit. Give it five and a half cycles, and the end does not join up with the beginning. "
            "The transform sees a jump there, and a jump, as Fourier and Gibbs taught us, needs every frequency. "
            "<bookmark mark='c'/> One pure tone has spilled into all the bins. This is called leakage."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2))
            vo.wait_until("a")
            self.play(Create(w1), FadeIn(c1), FadeIn(b1), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars1], lag_ratio=0.03), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(w2), FadeIn(c2), FadeIn(b2), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars2], lag_ratio=0.03), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(tag))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shapes(self):
        d = load("windows")
        cols = {"rect": BAD, "hann": TUNE, "blackman": GOOD}
        names = {"rect": r"no fade (a rectangle)", "hann": r"Hann", "blackman": r"Blackman"}
        g = axes([0, 10], [-100, 5], x_length=7.4, y_length=4.2, xlabel=r"bins away from the tone", ylabel=r"spill (dB)",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[-80, -60, -40, -20, 0], font_size=20)
        g.move_to(LEFT * 2.6 + DOWN * 0.3)
        keep = d["bins"] <= 10
        curves = {k: curve(g.ax, d["bins"][keep], d[f"curve_{k}"][keep], c, stroke_width=2.5) for k, c in cols.items()}
        x = np.linspace(0, 1, 100)
        shapes = VGroup()
        for k, fn in (("rect", np.ones_like(x)), ("hann", 0.5 - 0.5 * np.cos(2 * np.pi * x)),
                      ("blackman", 0.42 - 0.5 * np.cos(2 * np.pi * x) + 0.08 * np.cos(4 * np.pi * x))):
            tr_ = Trace(ORIGIN, RIGHT * 1.6, scale=0.55, color=cols[k])
            tr_.set_shape(np.concatenate([[0], fn, [0]]))
            row = next(r for r in d["rows"] if r["name"] == k)
            shapes.add(VGroup(tr_, VGroup(label(names[k], font_size=24, color=cols[k]),
                                          label(rf"spill ${row['side']:.0f}$ dB, \ peak {row['lobe']:.0f} bins wide", font_size=22, color=GREY_A)
                                          ).arrange(DOWN, buff=0.06, aligned_edge=LEFT)).arrange(RIGHT, buff=0.3))
        shapes.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(RIGHT * 4.3 + UP * 0.2)
        with self.voiceover(
            "The cure is to fade the stretch in and out, so that there is no jump at its ends. The shape of the "
            "fade is called a window. <bookmark mark='a'/> With no fade at all, the spill is only thirteen decibels "
            "down next door, and it falls away slowly. <bookmark mark='b'/> With a smooth hump, named after the "
            "meteorologist von Hann, the worst spill is thirty-one decibels down and it drops fast. "
            "<bookmark mark='c'/> A slightly fancier hump, Blackman's, gets to fifty-eight. <bookmark mark='d'/> "
            "But look at what it costs. The better the window hides the spill, the wider the peak itself: two "
            "bins, four, six. You are trading sharpness for cleanliness, and these numbers match the standard "
            "tables to a tenth of a decibel."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(curves["rect"]), FadeIn(shapes[0]))
            vo.wait_until("b")
            self.play(Create(curves["hann"]), FadeIn(shapes[1]))
            vo.wait_until("c")
            self.play(Create(curves["blackman"]), FadeIn(shapes[2]))
            vo.wait_until("d")
            self.play(Indicate(shapes, color=WHITE, scale_factor=1.02))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def weak(self):
        d = load("windows")
        g = axes([80, 130], [-90, 5], x_length=10.0, y_length=3.8, xlabel=r"frequency bin", ylabel=r"level (dB)",
                 xticks=[90, 100, 110, 120], yticks=[-80, -60, -40, -20, 0], font_size=20)
        g.move_to(DOWN * 0.5)
        r = curve(g.ax, d["two_bins"], np.maximum(d["two_rect"], -90), BAD, stroke_width=2.5)
        h = curve(g.ax, d["two_bins"], np.maximum(d["two_hann"], -90), TUNE, stroke_width=2.5)
        head = label(rf"two tones: \ a strong one, \ and one {-d['weak_db']:.0f} dB weaker, \ seven bins away", font_size=28, color=GREY_A).to_edge(UP, buff=0.5)
        arrow = Arrow(g.ax.c2p(d["weak_bin"], -18), g.ax.c2p(d["weak_bin"], d["weak_db"] + 3), color=GOOD, stroke_width=4, buff=0)
        at = label(r"there it is", font_size=24, color=GOOD).next_to(arrow, UP, buff=0.1)
        leg = VGroup(label(r"no fade: \ the weak tone is under the spill", font_size=24, color=BAD),
                     label(r"Hann window: \ it stands clear", font_size=24, color=TUNE)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        leg.move_to(g.ax.c2p(120, -12))
        with self.voiceover(
            "Here is why it matters. A strong tone, and a second tone seven bins away and two hundred times "
            "weaker. That is an ordinary situation: the fifth partial of a note is often that much weaker than "
            "the first. <bookmark mark='a'/> With no fade, the strong tone's spill is louder than the weak tone, "
            "and the weak one is simply not in the picture. <bookmark mark='b'/> With a Hann window, there it is. "
            "<bookmark mark='c'/> So there is no such thing as the spectrum of a sound. There is the spectrum "
            "through a particular window, and the choice of window decides what you can see. Every spectrum in "
            "this series uses a Hann window unless it says otherwise."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(r), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(h), FadeIn(leg[1]), GrowArrow(arrow), FadeIn(at))
            vo.wait_until("c")
        self.wait(0.3)
        self.clear_scene()
