from __future__ import annotations

import numpy as np

from videos.music.music48.common import *  # noqa: F403


class Quant(SoundScene):
    def construct(self):
        chapter(self, 5, r"Quantization", r"How precise must each sample be?")
        self.staircase()
        self.six_db()
        self.measured()
        self.floor()
        self.quiz()

    # ------------------------------------------------------------------
    def staircase(self):
        bits = 3
        step = 2 / 2 ** bits
        ax = frame_axes(width=5.0, height=4.0, xlo=-1, xhi=1, ylo=-1, yhi=1, center=LEFT * 3.2 + DOWN * 0.3)
        xs = np.linspace(-1, 1 - 1e-6, 800)
        q = np.clip(step * np.round(xs / step), -1, 1 - step)
        stair = curve(xs, q, ax.to, color=TUNE, width=4)
        ideal = DashedLine(ax.to(-1, -1), ax.to(1, 1), color=GREY_B, stroke_width=1.5)
        ex = frame_axes(width=5.0, height=2.0, xlo=-1, xhi=1, ylo=-0.2, yhi=0.2, center=RIGHT * 3.4 + DOWN * 0.3)
        err = curve(xs, np.clip(q - xs, -0.2, 0.2), ex.to, color=EAR, width=3)
        la = label(r"output against input: \ 3 bits, \ 8 levels", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.2)
        lb = label(r"the error: \ a sawtooth within half a step", font_size=18, color=GREY_A).next_to(ex, UP, buff=0.2)
        head = label(r"rounding to the nearest level", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The second half of digital audio is precision. A sample can only be one of a fixed set of levels: with N bits, two "
            "to the N of them. <bookmark mark='a'/> Here are three bits, eight levels: each input is rounded to the nearest, a "
            "staircase of output against input. <bookmark mark='b'/> The difference, the quantization error, is a sawtooth "
            "that never exceeds half a step. Sixteen bits give 65,536 levels; the steps are tiny, but they are there."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ex), FadeIn(la), FadeIn(lb), FadeIn(ideal))
            vo.wait_until("a")
            self.play(Create(stair), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(err), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def six_db(self):
        rows_ = text_rows([
            (r"if the error is spread evenly over a step $\Delta$, \ its power is $\Delta^2/12$", WHITE),
            (r"a full-scale sine with $N$ bits has amplitude $2^{N-1}\Delta$, \ so power $2^{2N}\Delta^2/8$", WHITE),
            (r"their ratio: \ $\tfrac{3}{2}\,2^{2N}$, \ or $6.02\,N + 1.76$ decibels", TUNE),
            (r"each bit halves the step and buys 6 decibels: \ 16 bits, \ about 98 dB; \ 24 bits, \ about 146", WHITE),
            (r"the assumption that the error is even and random is what dither, \ chapter 6, \ makes true", GREY_A),
        ], font_size=23)
        head = label(r"six decibels a bit", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "How much does each bit buy? <bookmark mark='a'/> If the error is spread evenly across a step of size delta, its "
            "average power is delta squared over twelve. <bookmark mark='b'/> A full-scale sine with N bits has amplitude two "
            "to the N minus one steps, so its power is two to the two N, times delta squared, over eight. "
            "<bookmark mark='c'/> Their ratio is three halves times two to the two N, which in decibels is six point oh two N "
            "plus one point seven six. <bookmark mark='d'/> Each bit halves the step and buys six decibels: sixteen bits give "
            "about ninety-eight, twenty-four about a hundred and forty-six. <bookmark mark='e'/> The assumption that the error "
            "is even and random is the one dither will make true."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        d = load("quant")
        rows = d["rows"]
        b = [r["bits"] for r in rows]
        p = line_plot([[r["theory"] for r in rows], [r["measured"] for r in rows]], width=7.5, height=3.4, ylo=0, yhi=100, xmax=None,
                      colors=[GREY_B, TUNE], xlabel=r"bits", ylabel=r"signal to error, \ dB", yticks=(0, 50, 100), size=17)
        # x positions are indices 0..14 for bits 2..16
        xt = VGroup(*[label(f"{v}", font_size=15, color=GREY_A).next_to(p.to(i, 0), DOWN, buff=0.12) for i, v in enumerate(b) if v % 2 == 0])
        p.add(xt)
        p.move_to(DOWN * 0.2)
        dots = VGroup(*[Dot(p.to(i, r["measured"]), radius=0.06, color=TUNE) for i, r in enumerate(rows)])
        key = VGroup(label(r"grey: \ $6.02N + 1.76$", font_size=17, color=GREY_A), label(r"gold: \ measured, \ a 997 Hz sine at full scale", font_size=17, color=TUNE)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).to_corner(UR, buff=0.6).shift(DOWN * 0.8)
        r2, r8, r16 = rows[0], rows[6], rows[14]
        head = label(r"the rule against the measurement", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Check it. Quantize a full-scale sine at every word length from two bits to sixteen and measure the error. "
            f"<bookmark mark='a'/> At eight bits the rule says {say(r8['theory'], 1)} decibels and we measure "
            f"{say(r8['measured'], 1)}; at sixteen, {say(r16['theory'], 1)} against {say(r16['measured'], 1)}. Only at the very "
            f"shortest words does it fail: at two bits we measure {say(r2['measured'], 1)} against {say(r2['theory'], 1)}, "
            "because there the error is nothing like random: it is the sine's own shape, squared off."
        ) as vo:
            self.play(FadeIn(head), FadeIn(p[0]), FadeIn(p.lines[0]), FadeIn(p[2:]), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(dots), Create(p.lines[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def floor(self):
        items = [
            (r"16 bits put the noise about 98 dB below the loudest sample", WHITE),
            (r"if the loudest peak plays at 110 dB SPL, \ the floor sits near 12 dB SPL: \ below a quiet room's own noise", WHITE),
            (r"so at home, \ 16 bits are enough for almost any music, \ if the level is set well", WHITE),
            (r"studios record at 24 bits: \ not to hear 146 dB, \ but to leave room for levels set too low or too high", TUNE),
            (r"the converter's own noise, \ around 20 bits' worth, \ is the real floor of a 24-bit recording", GREY_A),
        ]
        rows_scene(self, r"where the floor sits", items,
                   "How much is enough? <bookmark mark='b'/> Sixteen bits put the noise about ninety-eight decibels below the "
                   "loudest possible sample. <bookmark mark='c'/> If the loudest peak plays at a hundred and ten decibels of sound "
                   "pressure, the floor sits near twelve: below the noise of a quiet room. <bookmark mark='d'/> So at home, sixteen "
                   "bits are enough for almost any music, if the level is set well. <bookmark mark='e'/> Studios record at "
                   "twenty-four bits, not to hear a hundred and forty-six decibels, but to leave room for levels set too low or "
                   "too high. <bookmark mark='f'/> And the converter's own noise, about twenty bits' worth, is the real floor of a "
                   "twenty-four-bit recording.", marks="bcdef")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("quant")
        c = clip("quant.two")
        card = listen_card(r"The Tune at 4 bits, \ 16 levels, \ twice. \ Once rounded plainly, \ once with a little random noise "
                           r"added before rounding. \ Which had the noise added?", width=10.4)
        with self.voiceover(
            "Now listen to four bits, sixteen levels, where the error is loud. The Tune twice: once rounded plainly, once with "
            "a little random noise added before rounding. Which had the noise added?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=3.0, height=1.2, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=24, color=WHITE)).arrange(ORIGIN)
                         for t in (r"first", r"second")]).arrange(RIGHT, buff=1.6).move_to(UP * 0.8)
        steps = VGroup(*[Line(LEFT * 4 + UP * (-2.2 + 0.1 * k), RIGHT * 4 + UP * (-2.2 + 0.1 * k), color=GREY_B, stroke_width=1, stroke_opacity=0.4) for k in range(16)])
        cap = label(r"sixteen levels: \ every sample must sit on one of these lines", font_size=16, color=GREY_A).next_to(steps, UP, buff=0.15)
        self.play(FadeOut(card), FadeIn(boxes), FadeIn(steps), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"four bits, \ twice", detail=r"Part 7's piano, \ quantized", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        s = d["snr4"]
        with self.voiceover(
            "The second. The first is rough and gritty, and the grit follows the music: it is distortion, the error locked to "
            "the signal. The second hisses, a steady noise like tape, and the piano sounds clean through it. Measured, the "
            f"second is worse: {say(s['tpdf'], 1)} decibels of signal to error against {say(s['none'], 1)}. Yet most listeners "
            "prefer it. Chapter six explains why."
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4))
        self.wait(0.4)
        self.clear_scene()
