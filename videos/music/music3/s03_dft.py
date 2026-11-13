from __future__ import annotations

import numpy as np

from videos.music.music3.common import *  # noqa: F403


class Machine(SoundScene):
    def construct(self):
        chapter(self, 2, r"From a recipe to a machine", r"How does a computer find the recipe?", lit=(1807,),
                extra=((1965, r"Cooley and Tukey's fast Fourier transform"),))
        self.definition()
        self.fast()
        self.pluck()
        self.worked()

    # ------------------------------------------------------------------
    def definition(self):
        rng = np.random.default_rng(2)
        n = 32
        x = np.sin(2 * np.pi * 3 * np.arange(n) / n) + 0.5 * np.sin(2 * np.pi * 7 * np.arange(n) / n + 1.0)
        g = axes([0, n], [-1.7, 1.7], x_length=6.0, y_length=2.4, xlabel=r"$N$ samples of a sound", ylabel=r"", xticks=[], yticks=[0], font_size=20)
        g.move_to(LEFT * 3.5 + UP * 1.5)
        stems = VGroup(*[VGroup(Line(g.ax.c2p(i + 0.5, 0), g.ax.c2p(i + 0.5, v), color=AIR, stroke_width=2), Dot(g.ax.c2p(i + 0.5, v), radius=0.045, color=AIR))
                         for i, v in enumerate(x)])
        formula = MathTex(r"X[k]", r"=", r"\sum_{n=0}^{N-1}", r"x[n]", r"\,e^{-2\pi i\, k n / N}", font_size=44).move_to(RIGHT * 3.3 + UP * 1.9)
        formula[0].set_color(TUNE), formula[3].set_color(AIR)
        words = VGroup(label(r"for each frequency $k$: \ multiply the samples", font_size=24, color=GREY_A),
                       label(r"by a sine and a cosine of that frequency,", font_size=24, color=GREY_A),
                       label(r"and add up", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.08).next_to(formula, DOWN, buff=0.3)
        mag = np.abs(np.fft.rfft(x)) / (n / 2)
        gb = axes([0, n // 2 + 1], [0, 1.15], x_length=6.0, y_length=2.0, xlabel=r"frequency $k$ \ (cycles in the stretch)", ylabel=r"", xticks=[3, 7, 16], yticks=[], font_size=20)
        gb.move_to(LEFT * 3.5 + DOWN * 1.9)
        bars = VGroup(*[Line(gb.ax.c2p(k + 0.5, 0), gb.ax.c2p(k + 0.5, max(v, 0.004)), color=TUNE, stroke_width=6) for k, v in enumerate(mag)])
        cost = VGroup(MathTex(r"N\ \text{frequencies} \times N\ \text{samples}", font_size=36),
                      MathTex(r"= N^2\ \text{multiplications}", font_size=40, color=BAD)).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.4 + DOWN * 1.9)
        with self.voiceover(
            "A computer does not have a formula for a sound. It has a list of numbers: the pressure, measured "
            "forty-eight thousand times a second. <bookmark mark='a'/> Fourier's recipe still works. Take a stretch "
            "of N samples. For each frequency that fits a whole number of times into the stretch, multiply the "
            "samples by a wave of that frequency and add up. <bookmark mark='b'/> What comes out is the amount of "
            "each frequency: here, a lot of the third and half as much of the seventh. This is the discrete Fourier "
            "transform. <bookmark mark='c'/> It has one problem. N frequencies, N samples each: N squared "
            "multiplications. One second of sound would take two billion."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[FadeIn(s) for s in stems], lag_ratio=0.03), run_time=1.5)
            vo.wait_until("a")
            self.play(Write(formula), FadeIn(words))
            vo.wait_until("b")
            self.play(FadeIn(gb), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.04), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(cost))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fast(self):
        d = load("dft")
        card = history_card(1965, r"James Cooley and John Tukey",
                            r"the fast Fourier transform: split the samples into the even ones and the odd ones, "
                            r"transform each half, combine. Gauss had the same trick in a notebook of 1805.", width=5.8)
        card.to_corner(UL, buff=0.4)
        tree = VGroup()
        widths = [8, 4, 2, 1]
        for lvl, w in enumerate(widths):
            row = VGroup(*[RoundedRectangle(width=0.62 * w - 0.08, height=0.42, corner_radius=0.06, stroke_color=AIR, stroke_width=1.5,
                                            fill_color=AIR, fill_opacity=0.12 + 0.08 * lvl) for _ in range(8 // w)]).arrange(RIGHT, buff=0.08)
            row.move_to(RIGHT * 3.6 + UP * (2.6 - 0.62 * lvl))
            tree.add(row)
        tl = label(r"$\log_2 N$ levels, \ $N/2$ multiplications in each", font_size=24, color=GREY_A).next_to(tree, DOWN, buff=0.2)
        head = VGroup(*[label(t, font_size=22, color=GREY_B) for t in (r"samples $N$", r"by the definition", r"fast")])
        rows = VGroup(head)
        for r in d["costs"][1:]:
            rows.add(VGroup(label(f"{r['n']:,}".replace(",", "{,}"), font_size=26), label(f"{r['slow']:,}".replace(",", "{,}"), font_size=26, color=BAD),
                            label(f"{r['fast']:,}".replace(",", "{,}"), font_size=26, color=GOOD)))
        xs = [-6.6, -4.9, -1.9]
        for i, r in enumerate(rows):
            for cell, x in zip(r, xs):
                cell.move_to([x, -0.9 - 0.5 * i, 0], aligned_edge=LEFT)
        tm = d["timing"][-1]
        timed = VGroup(label(rf"on this computer, \ {tm['n']:,} samples:".replace(",", "{,}"), font_size=24, color=GREY_A),
                       label(rf"{tm['slow_ms']:.0f} ms by the definition", font_size=26, color=BAD),
                       label(rf"{tm['fast_ms']:.1f} ms fast", font_size=26, color=GOOD),
                       label(r"the same numbers, \ to 15 decimal places", font_size=24, color=GREY_A)
                       ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(RIGHT * 4.6 + DOWN * 2.0)
        ratio = tm["slow_ms"] / tm["fast_ms"]
        with self.voiceover(
            "The way out was published in 1965 by James Cooley and John Tukey, and it changed what could be "
            "computed. <bookmark mark='a'/> Split the samples into the even-numbered ones and the odd-numbered "
            "ones. Each half is a transform of half the size. Combine the two answers with a handful of "
            "multiplications, and you have the whole. Then do the same to each half, and each quarter, all the way "
            "down. <bookmark mark='b'/> The cost falls from N squared to N times the logarithm of N. For a million "
            "samples that is ten million multiplications where there were a million million. "
            f"<bookmark mark='c'/> We wrote both. On this machine, for four thousand samples, the fast one is "
            f"{say(round(ratio, -2))} times quicker, and it gives the same numbers. Every spectrum in this series, "
            "and in every recording studio, phone and streaming service, comes from this algorithm."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in tree], lag_ratio=0.5), FadeIn(tl), run_time=4.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(timed))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pluck(self):
        d = load("dft")
        g = axes([0, 1700], [-80, 5], x_length=10.6, y_length=3.6, xlabel=r"frequency (Hz)", ylabel=r"level (dB)",
                 xticks=[0, 500, 1000, 1500], yticks=[-60, -40, -20, 0], font_size=20)
        g.move_to(DOWN * 0.6)
        line = curve(g.ax, d["f"], np.maximum(d["spec_db"], -80), TUNE, stroke_width=2)
        marks = VGroup(*[label(str(k + 1), font_size=22, color=harmonic_color(k + 1)).move_to(g.ax.c2p(p, 2.5)) for k, p in enumerate(d["peaks"])])
        head = label(r"Part 1's plucked string, \ taken apart by our transform", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
        facts = label(rf"{d['n']:,} samples (a third of a second): \ one bin every {d['bin_hz']:.1f} Hz".replace(",", "{,}"), font_size=26, color=GREY_B)
        facts.next_to(head, DOWN, buff=0.2)
        with self.voiceover(
            "Here is the machine at work on the plucked string of Part 1. <bookmark mark='a'/> A third of a second "
            "of sound goes in. Out come eight thousand numbers, one for every three hertz. <bookmark mark='b'/> And "
            "there are the partials we computed by hand in Part 1: a row of sharp peaks at whole multiples of a "
            "hundred and thirty-one hertz, with almost nothing between them. A picture like this, strength against "
            "frequency, is called a spectrum."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(facts), Create(line), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.1) for m in marks], lag_ratio=0.15), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def worked(self):
        w = load("dft")["worked"]
        title = label(r"A worked example: \ how long must you listen?", font_size=36).to_edge(UP, buff=0.45)
        given = VGroup(label(rf"two low notes a semitone apart: \ {w['a2']:.0f} Hz and {w['a2'] + w['gap_hz']:.1f} Hz", font_size=30, color=FREQ),
                       label(r"a stretch of $T$ seconds gives one bin every $1/T$ hertz", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.25).move_to(UP * 1.5)
        ask = pause_card(r"How long a stretch does the transform need \\ to show these as two peaks?", width=8.4).move_to(DOWN * 0.7)
        ans = VGroup(MathTex(rf"\frac{{1}}{{T}} \le {w['gap_hz']:.1f}\ \text{{Hz}}", r"\quad\Longrightarrow\quad", rf"T \ge {w['seconds']:.2f}\ \text{{s}}", font_size=42),
                     label(rf"about {w['samples']:,.0f} samples: \ in practice, {w['pow2']:,}".replace(",", "{,}"), font_size=28, color=GREY_A),
                     label(r"a fast bass line changes notes more quickly than that", font_size=28, color=TUNE)).arrange(DOWN, buff=0.3).move_to(DOWN * 1.2)
        ans[0][2].set_color(TUNE)
        with self.voiceover(
            "One worked example, because it leads straight to this part's deepest point. Two low notes, a semitone "
            f"apart: a hundred and ten hertz and a hundred and sixteen and a half. <bookmark mark='a'/> A stretch "
            "T seconds long gives one number every one over T hertz. How long a stretch do you need for these two "
            "notes to show as separate peaks? Pause and work it out."
        ) as vo:
            self.play(FadeIn(title), FadeIn(given[0]))
            vo.wait_until("a")
            self.play(FadeIn(given[1]), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            f"The bins must be no wider than the gap, six and a half hertz, so the stretch must be at least "
            f"{say(w['seconds'], 2)} seconds long. <bookmark mark='a'/> And a bass player can change notes faster "
            "than that. To know the frequency finely, you must listen for a long time, and then you no longer know "
            "when things happened. Hold on to that. We will come back to it in chapter seven."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(ans[0]), FadeIn(ans[1]))
            vo.wait_until("a")
            self.play(FadeIn(ans[2]))
        self.wait(0.3)
        self.clear_scene()
