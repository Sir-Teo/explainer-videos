from __future__ import annotations

import numpy as np

from videos.music.music64.common import *  # noqa: F403


class Metrics(SoundScene):
    def construct(self):
        chapter(self, 9, r"Measuring separation", r"Does one number say how good a separation sounds?")
        self.sdr()
        self.quiz()
        self.blind_spots()
        self.faults()

    # ------------------------------------------------------------------
    def sdr(self):
        lines = VGroup(
            MathTex(r"\mathrm{SDR} = 10\log_{10}\frac{\|s\|^2}{\|s - \hat s\|^2}", font_size=38, color=TUNE),
            label(r"squared sample error, without perceptual weighting: \ leakage of another source, \ artifacts, \ a change of level", font_size=19, color=WHITE),
            MathTex(r"\mathrm{SI\text{-}SDR}: \ \alpha = \frac{\hat s^\top s}{\|s\|^2},\quad 10\log_{10}\frac{\|\alpha s\|^2}{\|\hat s - \alpha s\|^2}", font_size=32, color=WHITE),
            label(r"scale-invariant: \ a quieter but otherwise perfect estimate is not penalized \ (Le Roux et al., \ 2019)", font_size=18, color=GREY_A),
            label(r"BSS Eval \ (Vincent et al., \ 2006) \ splits the error into interference, \ artifacts and noise", font_size=18, color=GREY_A),
        ).arrange(DOWN, buff=0.38)
        head = label(r"signal to distortion", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Every number so far has been the signal-to-distortion ratio. <bookmark mark='a'/> The true source's energy "
            "against the energy of the error, in decibels. <bookmark mark='b'/> Squared sample errors are accumulated without a perceptual weighting: another source "
            "leaking in, artifacts, even a change of level. <bookmark mark='c'/> The scale-invariant version first finds the "
            "best gain, <bookmark mark='d'/> so that a quieter but otherwise perfect estimate is not penalized. "
            "<bookmark mark='e'/> And the BSS Eval toolkit of 2006 splits the error into interference, artifacts and noise."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcde", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("metrics")
        c = clip("metrics.two")
        card = listen_card(r"Two separations of the same voice, \ with exactly the same SDR. \ Which would you rather hear?", width=9.0)
        with self.voiceover("Your turn. Two separations of the same voice, with exactly the same SDR. Which would you rather hear?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"same SDR", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["leak"], st["artifacts"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["artifacts"], c.duration, buff=0.08)
        res = label(rf"both {d['sdr_leak']:.1f} dB: \ the first lets the piano and guitar through, \ quietly; \ the second gargles", font_size=19, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover(
            f"Both score {say(d['sdr_leak'], 1)} decibels. The first lets the piano and guitar through, quietly, and still sounds "
            "like music; the second has bins switched off at random and gargles. The first may sound preferable; no listener preference study is reported here. One number "
            "cannot say which error is worse."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def faults(self):
        items = [
            (r"SDR ignores perception: \ masking, \ which errors are audible, \ which are annoying", WHITE),
            (r"listening tests \ (MUSHRA, \ Part 58) \ remain the reference; \ slow and costly", WHITE),
            (r"perceptual measures, \ and networks trained on listening tests, \ are being built \ (Chapter 11)", WHITE),
            (r"report SDR, \ SI-SDR and a listening test, \ and the oracle reference scores beside them", TUNE),
        ]
        rows_scene(self, r"what the numbers miss", items,
                   "So the numbers miss things. <bookmark mark='b'/> SDR ignores perception: masking, which errors are audible, and "
                   "which are merely annoying. <bookmark mark='c'/> Listening tests, like the MUSHRA tests of Part 58, remain the "
                   "reference, and they are slow and costly. <bookmark mark='d'/> Perceptual measures, and networks trained on "
                   "listening tests, are being built. <bookmark mark='e'/> Meanwhile, report SDR, its scale-invariant cousin and a "
                   "listening test, with the oracle reference scores beside them.", marks="bcde")

    # ------------------------------------------------------------------
    def blind_spots(self):
        d = load("gain")
        c = clip("gain.three")
        rows = d["rows"]
        def si(v):
            return r"perfect" if v > 100 else f"{v:.1f} dB"
        g = VGroup()
        for k in ("half as loud", "upside down", "dull (2 kHz low-pass)", "1 ms late"):
            g.add(VGroup(label(k, font_size=19, color=WHITE), label(f"{rows[k]['sdr']:.1f} dB", font_size=19, color=TUNE), label(si(rows[k]["si_sdr"]), font_size=19, color=EAR)))
        g.arrange(DOWN, buff=0.32)
        for r in g:
            for i, x in enumerate((-3.2, 1.0, 3.8)):
                r[i].set_x(x)
        g.move_to(UP * 0.6)
        top = VGroup(label(r"SDR", font_size=16, color=TUNE).move_to([1.0, g.get_top()[1] + 0.4, 0]), label(r"SI-SDR", font_size=16, color=EAR).move_to([3.8, g.get_top()[1] + 0.4, 0]))
        head = label(r"a perfect estimate, \ changed", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Take a perfect estimate and change it in ways whose perceptual effects vary. <bookmark mark='a'/> Half as loud: SDR "
            f"gives {say(rows['half as loud']['sdr'], 0)} decibels, and the scale-invariant version says perfect. Upside down, "
            f"whose polarity reversal alone is often hard to hear, though audibility is signal- and playback-dependent: SDR says minus {say(-rows['upside down']['sdr'], 0)}. <bookmark mark='b'/> Dull, with "
            f"everything above two kilohertz removed: {say(rows['dull (2 kHz low-pass)']['sdr'], 0)} decibels, nearly perfect, "
            "because so little of a voice's energy is up there. And one millisecond late, typically hard to notice in isolated playback: "
            f"{say(rows['1 ms late']['sdr'], 1)} decibels, worse than nothing at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), FadeIn(g[0]))
            vo.wait_until("a")
            self.play(FadeIn(g[1]))
            vo.wait_until("b")
            self.play(FadeIn(g[2]), FadeIn(g[3]))
        boxes = choice_boxes([r"as recorded", r"dull", r"1 ms late"], width=3.0, height=0.8, buff=0.5, size=18).move_to(DOWN * 2.2)
        with self.voiceover("Hear them: the vocals as recorded, the dull ones, and the late ones."):
            self.play(FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"three estimates", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            ks = ["true", "dull", "late"]
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.3 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.06)
        with self.voiceover(
            "The dull voice is the one you can hear is different, if you listen closely, and it scores best. The late one "
            "sounds identical to the original, and scores worst. The scale-invariant measure fixes gain, not time or timbre."
        ):
            self.wait(0.5)
        self.wait(0.4)
        self.clear_scene()
