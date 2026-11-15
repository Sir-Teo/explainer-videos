from __future__ import annotations

import numpy as np

from videos.music.music49.common import *  # noqa: F403


class Fdn(SoundScene):
    def construct(self):
        chapter(self, 9, r"Feedback delay networks", r"How do modern reverbs make a smooth, \ dense tail?")
        self.idea()
        self.matrix()
        self.decay()
        self.bands()
        self.cathedral()
        self.practice()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"Jean-Marc Jot and Antoine Chaigne \ (1991): \ several delay lines whose outputs are mixed and fed back into all of them", WHITE),
            (r"every echo from every line returns into every line: \ the echoes multiply at each pass", WHITE),
            (r"the mixing matrix must lose no energy: \ an orthogonal matrix, \ like a rotation", WHITE),
            (r"then a gain on each line sets the decay exactly, \ and a low-pass makes the highs die sooner", TUNE),
            (r"Schroeder's combs are the special case where nothing is mixed", GREY_A),
        ]
        rows_scene(self, r"delays that talk to each other", items,
                   "The design that replaced Schroeder's is the feedback delay network. <bookmark mark='b'/> Jean-Marc Jot and "
                   "Antoine Chaigne in 1991 took several delay lines and fed each one's output back into all of them, mixed. "
                   "<bookmark mark='c'/> Every echo from every line returns into every line, so the echoes multiply at each pass. "
                   "<bookmark mark='d'/> The mixing matrix must lose no energy: an orthogonal matrix, like a rotation. "
                   "<bookmark mark='e'/> Then a gain on each line sets the decay exactly, and a low-pass in each loop makes the "
                   "highs die sooner, as in a hall. <bookmark mark='f'/> Schroeder's combs are the special case in which nothing "
                   "is mixed.", marks="bcdef")

    # ------------------------------------------------------------------
    def matrix(self):
        d = load("schroeder")
        H = np.array([[1.0]])
        while H.shape[0] < 8:
            H = np.block([[H, H], [H, -H]])
        cells = VGroup()
        for i in range(8):
            for j in range(8):
                cells.add(Square(side_length=0.42, stroke_width=0.5, stroke_color=GREY_B, fill_color=TUNE if H[i, j] > 0 else BLUE, fill_opacity=0.85).move_to([-3.6 + 0.44 * j, 1.6 - 0.44 * i, 0]))
        lab = label(r"the 8 by 8 Hadamard matrix, \ divided by $\sqrt 8$: \ gold $+$, \ blue $-$", font_size=16, color=GREY_A).next_to(cells, DOWN, buff=0.3)
        lines = VGroup(*[label(rf"line {i + 1}: \ {ms} ms", font_size=17, color=WHITE) for i, ms in enumerate(d["fdn_ms"])]).arrange(DOWN, buff=0.13, aligned_edge=LEFT).move_to(RIGHT * 3.4 + UP * 0.2)
        head = label(r"eight lines, \ one matrix", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Ours has eight delay lines, from about twenty-nine to seventy-three milliseconds, lengths with no common "
            "factors so that their echoes never line up. <bookmark mark='a'/> The mixing matrix is a Hadamard matrix: every "
            "entry plus or minus one, scaled by one over root eight. Each line's output is spread into every line, with "
            "signs that keep the total energy exactly the same."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(cl) for cl in cells], lag_ratio=0.01), FadeIn(lab), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def decay(self):
        d = load("schroeder")
        a = np.array(d["ir_s"])
        b = np.array(d["ir_f"])
        t = np.arange(len(a)) * 12 / 48000 * 1000
        ax1 = frame_axes(width=11.0, height=1.7, xlo=0, xhi=150, ylo=-1, yhi=1, center=UP * 0.9)
        ax2 = frame_axes(width=11.0, height=1.7, xlo=0, xhi=150, ylo=-1, yhi=1, center=DOWN * 1.5)
        c1 = curve(t, a, ax1.to, color=TUNE, width=1.0)
        c2 = curve(t, b, ax2.to, color=BLUE, width=1.0)
        l1 = label(r"Schroeder: \ the first 150 ms", font_size=17, color=TUNE).next_to(ax1, UP, buff=0.1)
        l2 = label(rf"the network: \ the first 150 ms \ (RT60 measured {d['rt_fdn']:.2f} s; \ set to {d['t60']:.0f} s at low frequencies)", font_size=17, color=BLUE).next_to(ax2, UP, buff=0.1)
        head = label(r"two impulse responses", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Compare the first hundred and fifty milliseconds of each. <bookmark mark='a'/> Schroeder's: distinct echoes, in a "
            "regular train. <bookmark mark='b'/> The network's: the echoes start later, from the first line's delay, and then "
            "multiply into a thicker, more even texture. Its broadband reverberation time measures "
            f"{say(d['rt_fdn'], 2)} seconds, a little under the two set, because the low-pass in each loop shortens the highs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ax1), FadeIn(l1), Create(c1), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(ax2), FadeIn(l2), Create(c2), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bands(self):
        d = load("bands")
        cs = ["125", "250", "500", "1000", "2000", "4000"]
        series = (("room", r"the tiled room", GREY_A), ("plate", r"the plate", TUNE), ("fdn", r"the network", BLUE))
        bars = VGroup()
        x0 = -4.6
        for j, (k, name, col) in enumerate(series):
            for i, c in enumerate(cs):
                v = d[k][c] or 0.0
                h = 1.0 * v
                bars.add(Rectangle(width=0.32, height=max(h, 0.02), stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([x0 + 1.55 * i + 0.36 * j, -2.0 + h / 2, 0]))
        ticks = VGroup(*[label(c if int(c) < 1000 else f"{int(c) // 1000} k", font_size=16, color=GREY_A).move_to([x0 + 1.55 * i + 0.36, -2.3, 0]) for i, c in enumerate(cs)])
        ys = VGroup(*[label(f"{v} s", font_size=15, color=GREY_A).move_to([x0 - 0.7, -2.0 + v, 0]) for v in (0, 1, 2, 3)])
        key = VGroup(*[label(n, font_size=17, color=col) for _, n, col in series]).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.35)
        head = label(r"reverberation time in octave bands", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A single reverberation time hides a lot. Split each response into octave bands and measure each. "
            f"<bookmark mark='a'/> The tiled room rings longest in the bass, {say(d['room']['125'], 1)} seconds at a hundred "
            f"and twenty-five hertz against {say(d['room']['4000'], 1)} at four kilohertz. <bookmark mark='b'/> The plate is "
            f"long and bright in the lows, {say(d['plate']['125'], 1)} seconds, falling to {say(d['plate']['4000'], 1)} at "
            f"four kilohertz. <bookmark mark='c'/> The network is nearly flat, from {say(d['fdn']['125'], 1)} to "
            f"{say(d['fdn']['4000'], 1)}: its one-pole damping is gentle. The shape of these bars is much of what makes a "
            "reverb sound like stone, steel or wood."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ticks), FadeIn(ys), FadeIn(key))
            for mark, j in zip("abc", range(3)):
                vo.wait_until(mark)
                self.play(FadeIn(VGroup(*bars[6 * j:6 * j + 6])))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def practice(self):
        items = [
            (r"most algorithmic reverbs today are feedback delay networks, \ or relatives of them", WHITE),
            (r"with modulation: \ the delays wander a little, \ so no resonance settles", WHITE),
            (r"with early reflections in front, \ from a few image sources or a short multi-tap delay", WHITE),
            (r"a pre-delay sets the room's apparent size; \ the decay and its brightness set its material", TUNE),
            (r"convolution with a measured response does the same for one real room", GREY_A),
        ]
        rows_scene(self, r"reverbs in practice", items,
                   "Most algorithmic reverbs today are feedback delay networks, or relatives of them. <bookmark mark='b'/> They add "
                   "modulation: the delays wander a little, so that no resonance settles. <bookmark mark='c'/> They put early "
                   "reflections in front, from a few image sources or a short multi-tap delay. <bookmark mark='d'/> A pre-delay "
                   "sets the room's apparent size; the decay time and its brightness set its material. <bookmark mark='e'/> And "
                   "convolution with a measured response does the same for one real room.", marks="bcde")

    # ------------------------------------------------------------------
    def cathedral(self):
        d = load("cathedral")
        c = clip("cathedral.hits")
        lines = VGroup(*[Rectangle(width=ms / 40.0, height=0.28, stroke_width=0, fill_color=BLUE, fill_opacity=0.8) for ms in d["delays_ms"]]).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to(UP * 0.3)
        tags = VGroup(*[label(rf"{ms:.0f} ms", font_size=14, color=GREY_A).next_to(r, RIGHT, buff=0.15) for r, ms in zip(lines, d["delays_ms"])])
        cap = label(rf"the same network, \ every delay three times longer; \ RT60 set to 5 s, \ measured {d['rt60']:.1f} s", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"a cathedral of eight delay lines", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Make every delay three times longer, from about ninety to two hundred and twenty milliseconds, and set the decay "
            f"to five seconds: a cathedral, out of eight delay lines. It measures {say(d['rt60'], 1)} seconds across all "
            "frequencies. Three snare hits, then a chord."
        ):
            self.play(FadeIn(head), FadeIn(lines), FadeIn(tags), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"a cathedral", kind="synthesized", detail=r"Part 40's snare, \ Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, lines, 0.0, c.duration, buff=0.1)
        self.wait(0.3)
        self.clear_scene()
