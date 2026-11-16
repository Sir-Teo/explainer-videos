from __future__ import annotations

import numpy as np

from videos.music.music58.common import *  # noqa: F403


class Lossless(SoundScene):
    def construct(self):
        chapter(self, 1, r"Entropy and lossless coding", r"How small can a recording get without losing a single bit?")
        self.entropy()
        self.predict()
        self.table()
        self.rice()
        self.result()
        self.better()

    # ------------------------------------------------------------------
    def entropy(self):
        eq = MathTex(r"H = -\sum_i p_i \log_2 p_i \quad \text{bits per symbol}", font_size=40, color=TUNE).move_to(UP * 1.6)
        items = [
            (r"Shannon \ (1948): \ for uniquely decodable lossless codes under the stated source model, expected length is bounded by entropy; sample correlations require entropy-rate reasoning", WHITE),
            (r"a fair coin: \ 1 bit; \ a coin that lands heads 90\% of the time: \ 0.47 bits", WHITE),
            (r"16-bit samples spend 16 bits each; \ their empirical sample-value entropy can be lower, \ because common values can get short codes", WHITE),
            (r"and lower still once we stop coding the samples and code what we could not predict", TUNE),
        ]
        rows = text_rows(items, font_size=22).move_to(DOWN * 0.8)
        head = label(r"entropy", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Start with the limit. <bookmark mark='a'/> Claude Shannon proved in 1948 that for uniquely decodable lossless codes under the stated source model, expected length is bounded by entropy; sample correlations require entropy-rate reasoning: minus the sum of p log p. <bookmark mark='b'/> A fair coin has one bit of entropy; a coin that lands heads nine times in ten, under half a bit. <bookmark mark='c'/> Sixteen-bit samples spend sixteen bits each, but their empirical sample-value entropy can be lower, because common values can be given short codes. <bookmark mark='d'/> And it falls much further once we stop coding the samples, and code only what we could not predict."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def predict(self):
        d = load("lossless")
        x = np.array(d["trace"]["x"], float)
        e = np.array(d["trace"]["e2"], float)
        top = max(np.max(np.abs(x)), 1)
        a1 = frame_axes(width=10.0, height=1.6, xlo=0, xhi=len(x), ylo=-top, yhi=top, center=UP * 1.0)
        a2 = frame_axes(width=10.0, height=1.6, xlo=0, xhi=len(x), ylo=-top, yhi=top, center=DOWN * 1.4)
        cx = VMobject(stroke_color=TUNE, stroke_width=2).set_points_as_corners([a1.to(i, v) for i, v in enumerate(x)])
        ce = VMobject(stroke_color=EAR, stroke_width=2).set_points_as_corners([a2.to(i, v) for i, v in enumerate(e[: len(x)])])
        l1 = label(r"the voice, \ 400 samples \ (8 ms)", font_size=16, color=TUNE).next_to(a1, UP, buff=0.08).align_to(a1, LEFT)
        l2 = label(r"what the predictor $\hat{x}[n] = 2x[n-1] - x[n-2]$ misses, \ on the same scale", font_size=16, color=EAR).next_to(a2, UP, buff=0.08).align_to(a2, LEFT)
        head = label(r"prediction", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Audio is predictable from one sample to the next. <bookmark mark='a'/> Here are four hundred samples of our "
            "voice. <bookmark mark='b'/> Predict each one by continuing the straight line through the two before it, two x n "
            "minus one minus x n minus two, and keep only the error: the residual, on the same scale, is tiny. Send the first "
            "samples and the residual, and the decoder makes the same predictions and adds the errors back, exactly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a1), FadeIn(a2), FadeIn(ghost(VGroup(cx, ce), 0.25)))
            vo.wait_until("a")
            self.play(Create(cx), FadeIn(l1), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(ce), FadeIn(l2), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        d = load("lossless")["signals"]
        rows = VGroup(VGroup(label(r"predictor order", font_size=17, color=GREY_A), *[label(f"{o}", font_size=17, color=GREY_A) for o in range(5)]))
        for name, col in (("voice", TUNE), ("mix", BLUE)):
            rows.add(VGroup(label(rf"{name}: \ entropy, \ bits", font_size=18, color=col), *[label(f"{d[name]['entropy'][str(o)]:.1f}", font_size=19, color=WHITE) for o in range(5)]))
        rows.arrange(DOWN, buff=0.45)
        for r in rows:
            r[0].set_x(-3.6)
            for i, m in enumerate(r[1:]):
                m.set_x(-0.6 + 1.5 * i)
        rows.move_to(UP * 0.4)
        note = VGroup(label(r"order 0: \ the samples; \ 1: \ $x[n-1]$; \ 2: \ a line; \ 3: \ a parabola; \ 4: \ a cubic \ (Shorten's fixed predictors, \ 1994)", font_size=16, color=GREY_A),
                      label(r"the smooth voice falls from 13 bits to 3.5; \ the busy mix only to 9.5", font_size=18, color=WHITE)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        head = label(r"how much prediction saves", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How much does prediction save? <bookmark mark='a'/> Here is the entropy of the residual for predictors of order "
            "nought to four, Tony Robinson's fixed predictors from his coder Shorten of 1994: nought is the samples "
            "themselves, one the previous sample, two a straight line, three a parabola, four a cubic. <bookmark mark='b'/> "
            "Our smooth synthetic voice falls from thirteen bits a sample to three and a half; the busy mix, full of drums and "
            "noise, only to nine and a half, at order two. Predictability is a property of the music."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(rows[1:]), FadeIn(note[0]))
            vo.wait_until("b")
            self.play(FadeIn(note[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rice(self):
        items = [
            (r"the residual is small and symmetric: \ map it to $0, 1, 2, \dots$ \ (0, \ $-1$, \ 1, \ $-2$, \ ...)", WHITE),
            (r"a Rice code with parameter $k$: \ the value's top bits in unary, \ its low $k$ bits as they are", WHITE),
            (r"$u = 13$, \ $k = 2$: \ $13 = 3 \cdot 4 + 1$: \ \texttt{0001} then \texttt{01}", WHITE),
            (r"choose $k$ per block to fit the residual's size: \ near-optimal for the two-sided exponential shape residuals have", WHITE),
            (r"Golomb \ (1966), \ Rice \ (1979); \ FLAC \ (2001) \ does exactly this, \ with better predictors", TUNE),
        ]
        rows_scene(self, r"Rice codes", items,
                   "Then the residual must be written in as few bits as possible. <bookmark mark='b'/> It is small and symmetric "
                   "about zero, so first fold it onto the counting numbers: nought, minus one, one, minus two, and so on. "
                   "<bookmark mark='c'/> A Rice code with parameter k writes a number's top bits in unary, as a run of zeros and a "
                   "one, and its low k bits as they are. <bookmark mark='d'/> Thirteen, with k equal to two, is three fours and "
                   "one: three zeros and a one, then nought one. <bookmark mark='e'/> Choose k for each block to fit the residual's "
                   "size, and the code comes close to the entropy for the two-sided exponential shape that residuals have. "
                   "<bookmark mark='f'/> Solomon Golomb found the family in 1966 and Robert Rice its simple case in 1979; FLAC, "
                   "since 2001, does exactly this with better predictors.", marks="bcdef")

    # ------------------------------------------------------------------
    def result(self):
        d = load("lossless")["signals"]
        rows = VGroup(VGroup(label(r"signal", font_size=17, color=GREY_A), label(r"bits per sample", font_size=17, color=GREY_A), label(r"of the original size", font_size=17, color=GREY_A),
                             label(r"decoded exactly?", font_size=17, color=GREY_A)))
        for name, col in (("voice", TUNE), ("mix", BLUE)):
            v = d[name]
            rows.add(VGroup(label(name, font_size=19, color=col), label(f"{v['bits_per_sample']:.2f}", font_size=19, color=WHITE), label(rf"{100 * v['ratio']:.0f}\%", font_size=19, color=WHITE),
                            label(r"yes, \ every sample" if v["exact"] else r"no", font_size=19, color=TUNE)))
        rows.arrange(DOWN, buff=0.45)
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(-4.4 + 3.0 * i)
        rows.move_to(UP * 0.3)
        note = label(r"Monochord's coder: \ blocks of 4,096, \ the best of five predictors, \ Rice codes; \ the decoder rebuilds the 16-bit samples bit for bit", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.6)
        head = label(r"a lossless coder, \ round trip", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Monochord's lossless coder puts it together: blocks of four thousand and ninety-six samples, the best of the five "
            "predictors for each block, Rice codes for the residual. <bookmark mark='a'/> The voice shrinks to "
            f"{say(100 * d['voice']['ratio'])} per cent of its size, the mix to {say(100 * d['mix']['ratio'])}, and the decoder "
            "rebuilds every sample, bit for bit. <bookmark mark='b'/> Half the size is about what lossless coding does for real "
            "music. To go further, we have to stop sending what cannot be heard."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(rows[1:]))
            vo.wait_until("b")
            self.play(Indicate(rows[2], color=BLUE, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def better(self):
        items = [
            (r"FLAC and MPEG-4 ALS fit a predictor to each block: \ linear prediction of order up to 32, \ by the Levinson--Durbin recursion", WHITE),
            (r"the coefficients are quantized and sent with the block; \ the decoder runs the same filter in integers, \ so the result is exact", WHITE),
            (r"stereo: \ predict the side from the mid, \ or code the difference", WHITE),
            (r"the best lossless coders reach 40 to 60\% on music; \ noise, \ by definition, \ cannot be compressed at all", TUNE),
        ]
        rows_scene(self, r"better predictors", items,
                   "Real lossless coders go a little further. <bookmark mark='b'/> FLAC and MPEG-4 ALS fit a predictor to each block: linear prediction of orders limited by the format; FLAC supports up to thirty-two, while ALS supports substantially higher orders, by the Levinson-Durbin recursion. <bookmark mark='c'/> The coefficients are quantized and sent with the block, and the decoder runs the same filter in integer arithmetic, so the result is still exact. <bookmark mark='d'/> For stereo they predict one channel from the other, or code the difference. <bookmark mark='e'/> The best reach forty to sixty per cent of the original on music; and independent uniformly distributed full-resolution noise offers little lossless compression; colored or otherwise structured noise can be predictable.", marks="bcde")
