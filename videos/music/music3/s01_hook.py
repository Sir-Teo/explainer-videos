from __future__ import annotations

import numpy as np

from videos.music.music3.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.cold_open()
        self.academy()
        self.questions()
        self.plan()

    # ------------------------------------------------------------------
    def cold_open(self):
        d = load("square")
        c = clip("square.build")
        g = axes([0, 2], [-1.45, 1.45], x_length=8.6, y_length=3.4, xlabel=r"", ylabel=r"", xticks=[], yticks=[-1, 0, 1], font_size=20)
        g.move_to(LEFT * 1.6 + UP * 0.5)
        target = curve(g.ax, d["t"], d["target"], GREY_C, stroke_width=1.5)
        wave = curve(g.ax, d["t"], d["sums"][0], TUNE, stroke_width=3)
        count = label(r"1 pure tone", font_size=40, color=TUNE).next_to(g, UP, buff=0.25)
        n_show = 30
        amps = np.array([4 / (np.pi * n) if n % 2 else 0.0 for n in range(1, n_show + 1)])
        bars = partial_bars(amps / amps.max(), width=4.2, height=2.6, db=False, numbers=False).move_to(RIGHT * 4.9 + UP * 0.4)
        for b in bars.bars:
            b.set_opacity(0.12)
        blab = label(r"the recipe: \ how much of each", font_size=22, color=GREY_B).next_to(bars, DOWN, buff=0.15)
        self.play(FadeIn(g), FadeIn(target), FadeIn(wave), FadeIn(count), FadeIn(bars), FadeIn(blab), run_time=0.6)
        with self.listen(c) as snd:
            window(snd, r"1, 2, 3, 5, 10, 30 pure tones, \ added up", kind="synthesized", detail=r"sines added in the computer")
            for i, k in enumerate(d["counts"]):
                snd.wait_until(f"k{k}")
                self.remove(wave, count)
                wave = curve(g.ax, d["t"], d["sums"][i], TUNE, stroke_width=3)
                count = label(rf"{k} pure tone" + ("s" if k > 1 else ""), font_size=40, color=TUNE).next_to(g, UP, buff=0.25)
                self.add(wave, count)
                for j, b in enumerate(bars.bars):
                    b.set_opacity(0.95 if (j % 2 == 0 and (j // 2) < k) else 0.12)
                self.play(Indicate(wave, color=WHITE, scale_factor=1.015), run_time=0.9)
        with self.voiceover(
            "That was one note, getting brighter. But look at how it was made. Each step added one more pure tone, a "
            "plain sine wave, at three, five, seven times the frequency of the first. And the smooth curves are "
            "closing in on something with corners."
        ):
            self.play(Indicate(target, color=WHITE, scale_factor=1.0), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def academy(self):
        d = load("square")
        card = history_card(1807, r"Joseph Fourier, \ Paris",
                            r"reads to the Academy a memoir on the flow of heat. It claims that \textit{any} curve, "
                            r"even one with jumps, is a sum of sines. The examiners: Lagrange, Laplace, Monge, Lacroix.",
                            width=6.0).to_corner(UL, buff=0.45)
        g = axes([0, 2], [-1.45, 1.45], x_length=6.0, y_length=2.6, xlabel=r"", ylabel=r"", xticks=[], yticks=[], font_size=20)
        g.move_to(RIGHT * 3.4 + UP * 1.6)
        sq = curve(g.ax, d["t"], d["target"], GREY_B, stroke_width=2)
        s30 = curve(g.ax, d["t"], d["sums"][-1], TUNE, stroke_width=2.5)
        obj = VGroup(label(r"Lagrange: \ sines are smooth.", font_size=30, color=BAD),
                     label(r"A sum of smooth curves cannot have a corner.", font_size=30, color=BAD)).arrange(DOWN, buff=0.2).move_to(DOWN * 1.0)
        fate = label(r"the Academy does not print it; \ Fourier publishes it himself, \ in 1822", font_size=28, color=GREY_A).move_to(DOWN * 2.5)
        with self.voiceover(
            "In December 1807 Joseph Fourier stood before the Paris Academy of Sciences with a memoir about how "
            "heat flows through a metal bar. Buried in it was a claim about curves. <bookmark mark='a'/> Any curve at "
            "all, he said, even one with sudden jumps, can be written as a sum of sine waves. The examiners included "
            "Lagrange and Laplace, the two greatest mathematicians alive. <bookmark mark='b'/> Lagrange would not "
            "have it. A sine is smooth. A sum of smooth things is smooth. How could it ever make a corner? If that "
            "sounds familiar, it should: it is exactly the objection Euler made to Bernoulli about the plucked "
            "string, fifty years earlier, in Part 1. <bookmark mark='c'/> The Academy declined to publish. Fourier "
            "waited fifteen years and printed the work himself."
        ) as vo:
            self.play(FadeIn(card), FadeIn(g), FadeIn(sq))
            vo.wait_until("a")
            self.play(Create(s30), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(obj[0]), FadeIn(obj[1]))
            vo.wait_until("c")
            self.play(FadeIn(fate))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def questions(self):
        qs = VGroup(label(r"Can every sound be taken apart into pure tones?", font_size=38, color=TUNE),
                    label(r"What does the taking apart cost?", font_size=38, color=TUNE),
                    label(r"Is the list of pure tones everything there is to a sound?", font_size=38, color=EAR)
                    ).arrange(DOWN, buff=0.55).move_to(UP * 0.9)
        s = StringView(width=5.0, scale=0.5, stroke_width=3).move_to(DOWN * 2.3)
        xs = np.linspace(0, 1, 121)
        shape = np.minimum(xs / 0.11, (1 - xs) / 0.89)
        clock = {"t": 0.0}

        def ringing(m, dt):
            clock["t"] += dt
            m.set_shape(shape * np.cos(2 * PI * 1.1 * clock["t"]) * np.exp(-0.25 * clock["t"]))

        with self.voiceover(
            "Fourier was right, and this part is about what that means for sound. Three questions. Can every sound "
            "be taken apart into pure tones? <bookmark mark='a'/> What does the taking apart cost you: what can you "
            "no longer know once you have done it? <bookmark mark='b'/> And is the list of pure tones the whole "
            "story? If two sounds have exactly the same recipe, must they sound the same? <bookmark mark='c'/> We "
            "will end by playing one plucked string in a way that keeps its recipe exactly and changes the sound "
            "completely."
        ) as vo:
            self.play(FadeIn(qs[0]))
            vo.wait_until("a")
            self.play(FadeIn(qs[1]))
            vo.wait_until("b")
            self.play(FadeIn(qs[2]))
            vo.wait_until("c")
            s.add_updater(ringing)
            self.play(FadeIn(s))
            self.wait(vo.remaining() + 0.1)
        s.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ The Spectrum", font_size=46).to_edge(UP, buff=0.35)
        smap = series_map(current=PART, done=PART - 1, height=6.3).next_to(title, DOWN, buff=0.3)
        obj = objectives_card([
            r"Fourier series: \ how much of each sine is in a wave, \ and why corners are possible",
            r"the transform as a machine: \ the DFT, \ and the fast algorithm that made it practical",
            r"Ohm's law of hearing, \ Helmholtz's resonators, \ and what phase does and does not do",
            r"the spectrogram; \ what a window costs; \ the limit on knowing when and what at once",
            r"a ruler shaped for music (constant Q); \ sounds with no pitch at all",
            r"timbre: \ why the same spectrum can be two different sounds",
        ], font_size=26).move_to(DOWN * 0.25)
        with self.voiceover(
            "This is Part 3 of Music, Built. Part 1 took a plucked string apart into partials. Part 2 told two pipes "
            "apart by theirs. <bookmark mark='a'/> Now we make the idea exact. How to find the recipe of any wave. "
            "How a computer does it, fast. What the ear seems to do with it. How to watch a recipe change in time, "
            "and the hard limit on doing so. A way of measuring made for music. And last, what the recipe leaves out."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.4)
        self.clear_scene()
