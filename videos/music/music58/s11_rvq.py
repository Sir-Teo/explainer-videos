from __future__ import annotations

import numpy as np

from videos.music.music58.common import *  # noqa: F403


class Rvq(SoundScene):
    def construct(self):
        chapter(self, 10, r"Vectors and residuals", r"What if the codec learned its own alphabet?")
        self.vq()
        self.residual()
        self.curve_()
        self.heard()
        self.neural()

    # ------------------------------------------------------------------
    def vq(self):
        items = [
            (r"scalar quantization rounds each number on its own", WHITE),
            (r"vector quantization codes several numbers at once, \ as the index of the nearest entry in a codebook", WHITE),
            (r"the codebook is learned from examples \ (k-means: \ Lloyd, \ 1957; \ Linde, \ Buzo and Gray, \ 1980)", WHITE),
            (r"8 neighbouring MDCT coefficients, \ normalized by their band's level; \ 256 entries: \ 8 bits for 8 numbers", WHITE),
            (r"but one codebook of 256 cannot be fine; \ a codebook of $2^{40}$ cannot be searched", TUNE),
        ]
        rows_scene(self, r"vector quantization", items,
                   "There is another way to spend bits. <bookmark mark='b'/> Scalar quantization rounds each number on its own. "
                   "<bookmark mark='c'/> Vector quantization codes several numbers at once, as the index of the nearest entry in a "
                   "codebook. <bookmark mark='d'/> The codebook is learned from examples by k-means, Stuart Lloyd's algorithm of "
                   "1957, as Linde, Buzo and Gray applied it to coding in 1980. <bookmark mark='e'/> Here: eight neighbouring MDCT "
                   "coefficients at a time, divided by their band's level, and a codebook of two hundred and fifty-six entries, so "
                   "eight bits for eight numbers. <bookmark mark='f'/> But one codebook of two hundred and fifty-six cannot be fine, "
                   "and a codebook of two to the fortieth cannot be searched.", marks="bcdef")

    # ------------------------------------------------------------------
    def residual(self):
        rng = np.random.default_rng(4)
        pts = rng.standard_normal((60, 2)) * [1.2, 0.8]
        target = np.array([1.1, 0.7])
        c1 = np.array([1.4, 0.2])
        c2 = np.array([-0.25, 0.45])
        c3 = np.array([-0.05, 0.05])
        origin = np.array([-3.0, -0.6, 0])
        sc = 1.6

        def P(v):
            return origin + sc * np.array([v[0], v[1], 0])
        cloud = VGroup(*[Dot(P(p), radius=0.03, color=GREY_D) for p in pts])
        tgt = Dot(P(target), radius=0.1, color=WHITE)
        a1 = Arrow(P([0, 0]), P(c1), buff=0, color=TUNE, stroke_width=4)
        a2 = Arrow(P(c1), P(c1 + c2), buff=0, color=BLUE, stroke_width=4)
        a3 = Arrow(P(c1 + c2), P(c1 + c2 + c3), buff=0, color=EAR, stroke_width=4, max_tip_length_to_length_ratio=0.5)
        tl = label(r"the vector to code", font_size=15, color=WHITE).next_to(tgt, UR, buff=0.05)
        items = text_rows([(r"stage 1: \ the nearest of 256 entries", TUNE), (r"stage 2: \ a second codebook codes what stage 1 missed", BLUE),
                           (r"stage 3: \ and what stage 2 missed", EAR), (r"each stage adds 8 bits and refines the last; \ stop wherever the bit rate says", WHITE)], font_size=19, width=6.2).move_to(RIGHT * 3.4)
        head = label(r"residual vector quantization", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Residual vector quantization solves both problems. <bookmark mark='a'/> Code the vector with the nearest of two "
            "hundred and fifty-six entries. <bookmark mark='b'/> Then code what that missed, the residual, with a second "
            "codebook trained on residuals, <bookmark mark='c'/> and what that missed with a third. <bookmark mark='d'/> Each "
            "stage adds eight bits and refines the last, and the decoder can stop after any stage: a bit rate chosen by how many "
            "stages are sent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cloud), FadeIn(tgt), FadeIn(tl))
            vo.wait_until("a")
            self.play(GrowArrow(a1), FadeIn(items[0]))
            vo.wait_until("b")
            self.play(GrowArrow(a2), FadeIn(items[1]))
            vo.wait_until("c")
            self.play(GrowArrow(a3), FadeIn(items[2]))
            vo.wait_until("d")
            self.play(FadeIn(items[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curve_(self):
        d = load("rvq")
        rows = d["rows"]
        s = np.array([r["stages"] for r in rows], float)
        ax = frame_axes(width=8.4, height=3.0, xlo=0.5, xhi=8.5, ylo=-40, yhi=25, center=DOWN * 0.3 + LEFT * 0.6)
        ve = VGroup(curve(s, [r["vec_err_db"] for r in rows], ax.to, color=TUNE, width=3), *[Dot(ax.to(x, r["vec_err_db"]), radius=0.06, color=TUNE) for x, r in zip(s, rows)])
        sn = VGroup(curve(s, [r["snr"] for r in rows], ax.to, color=BLUE, width=3), *[Dot(ax.to(x, r["snr"]), radius=0.06, color=BLUE) for x, r in zip(s, rows)])
        xt = VGroup(*[label(f"{int(v)}", font_size=14, color=GREY_A).next_to(ax.to(v, -40), DOWN, buff=0.1) for v in s])
        xl = label(r"stages \ (each about 30 kbit/s here)", font_size=15, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yt = VGroup(*[label(f"{v:+d} dB" if v else "0", font_size=14, color=GREY_A).next_to(ax.to(0.5, v), LEFT, buff=0.1) for v in (20, 0, -20, -40)])
        key = VGroup(label(r"error in the coded vectors", font_size=16, color=TUNE), label(r"the mix's signal-to-noise ratio", font_size=16, color=BLUE)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.3)
        note = label(r"codebooks trained on two other phrases, \ tested on the first two; \ the SNR levels off near 22 dB because the top of the spectrum is not coded", font_size=16, color=WHITE).to_edge(DOWN, buff=0.35)
        head = label(r"stage by stage", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here it is on our mix, with codebooks trained on two other phrases of the Tune. <bookmark mark='a'/> Each stage "
            "cuts the error in the coded vectors by about five decibels, from minus six after one stage to minus thirty-seven "
            "after eight. <bookmark mark='b'/> The mix's signal-to-noise ratio rises from seven decibels to about twenty-two, "
            "where it levels off, because this little coder never sends anything above fifteen kilohertz."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(xl), FadeIn(yt), FadeIn(ghost(VGroup(ve, sn), 0.25)), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(ve), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(FadeIn(sn), FadeIn(key[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("rvq")
        c = clip("rvq.three")
        boxes = choice_boxes([r"1 stage", r"3 stages", r"8 stages"], width=2.6, height=0.9, buff=0.9, size=22).move_to(UP * 0.4)
        head = label(r"stages, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear one stage, three and eight."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"1, \ 3, \ 8 stages", kind="physical model", detail=r"Part 56's mix, \ RVQ of the MDCT", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["s1"], st["s3"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["s3"], st["s8"] - 0.3, buff=0.08)
            pulse(snd, boxes[2], st["s8"], c.duration, buff=0.08)
        with self.voiceover("With one stage the band levels are right but every detail is a guess from the codebook; with eight, the mix is back, a little dull at the top."):
            self.play(Indicate(boxes[2], color=TUNE, scale_factor=1.04))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def neural(self):
        items = [
            (r"neural codecs replace the MDCT with a learned encoder, \ and the inverse with a learned decoder", WHITE),
            (r"between them, \ residual vector quantization of the learned features: \ SoundStream \ (2021), \ EnCodec \ (2022)", WHITE),
            (r"trained end to end, \ with a learned critic deciding whether the decoded audio sounds real", WHITE),
            (r"speech at 3 kbit/s, \ music at 6 to 24: \ a tenth of what a classical codec needs for the same rating", WHITE),
            (r"and their codes are tokens: \ the alphabet that generative audio \ (Part 66) \ writes in", TUNE),
        ]
        rows_scene(self, r"neural codecs", items,
                   "This is where the field has gone. <bookmark mark='b'/> Neural codecs replace the MDCT with a learned encoder, "
                   "and its inverse with a learned decoder. <bookmark mark='c'/> Between them sits residual vector quantization of "
                   "the learned features, as in Google's SoundStream of 2021 and Meta's EnCodec of 2022. <bookmark mark='d'/> They "
                   "are trained end to end, with a second network as critic, judging whether the decoded audio sounds real. "
                   "<bookmark mark='e'/> They code speech in three kilobits a second, and music in six to twenty-four, a fraction of "
                   "what a classical codec needs for the same rating. <bookmark mark='f'/> And their codes are tokens: the alphabet "
                   "in which the generative audio of Part 66 writes.", marks="bcdef")
