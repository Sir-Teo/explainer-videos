from __future__ import annotations

import numpy as np

from videos.music.music64.common import *  # noqa: F403


class Network(SoundScene):
    def construct(self):
        chapter(self, 8, r"Networks that separate", r"Can a network learn what a voice looks like in a mix?")
        self.design()
        self.training()
        self.heard()
        self.compare()

    # ------------------------------------------------------------------
    def design(self):
        items = [
            (r"input: \ the mixture's log spectrogram, \ five frames at a time", WHITE),
            (r"output: \ the vocals' ratio mask for the middle frame, \ 384 bins up to 9 kHz", WHITE),
            (r"two hidden layers of 512 units: \ a few hundred thousand weights", WHITE),
            (r"trained on four other stretches of the session, \ tested on the first two phrases", WHITE),
            (r"a toy beside Demucs: \ the same idea, \ a millionth of the data", TUNE),
        ]
        rows_scene(self, r"Monochord's separator", items,
                   "Monochord's network is small. <bookmark mark='b'/> Its input is the mixture's log spectrogram, five frames at "
                   "a time. <bookmark mark='c'/> Its output is the vocals' ratio mask for the middle frame, up to nine kilohertz. "
                   "<bookmark mark='d'/> Two hidden layers of five hundred and twelve units: a few hundred thousand weights. "
                   "<bookmark mark='e'/> It is trained on four other stretches of the session, and tested on the first two phrases. "
                   "<bookmark mark='f'/> A toy beside Demucs: the same idea, with a millionth of the data.", marks="bcdef")

    # ------------------------------------------------------------------
    def training(self):
        d = load("net")
        loss = np.array(d["losses"])
        ax = frame_axes(width=7.0, height=3.0, xlo=0, xhi=len(loss) - 1, ylo=0, yhi=loss.max() * 1.05, center=DOWN * 0.3)
        cv = curve(np.arange(len(loss)), loss, ax.to, color=TUNE, width=3)
        xl = label(r"epochs", font_size=14, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"mean squared error of the mask", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.15)
        head = label(r"training", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Training lowers the error of its masks, epoch by epoch, on the stretches it learns from."):
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xl), FadeIn(yl), Create(cv), run_time=2.0)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("net")
        c = clip("net.two")
        boxes = choice_boxes([r"the network's vocals", r"the true vocals"], width=3.8, height=0.9, buff=0.9, size=19).move_to(UP * 0.5)
        note = label(rf"{d['sdr']:.1f} dB SDR on phrases it never heard", font_size=19, color=TUNE).next_to(boxes, DOWN, buff=0.6)
        head = label(r"the network's vocals, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the vocals as the network separates them, then as recorded."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"network, \ then truth", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["net"], st["true"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["true"], c.duration, buff=0.08)
        with self.voiceover(f"On phrases it never heard, it reaches {say(d['sdr'], 1)} decibels. Its mistakes are softer than the factorization's: it has learnt what this voice looks like, among these instruments."):
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        n, o, net = load("nmf")["sdr"]["vocals"], load("oracle")["sdr"], load("net")["sdr"]
        rows_ = VGroup()
        vals = [("NMF", n, GREY_B), ("the network", net, TUNE), ("ideal binary mask", o["ibm"]["vocals"], BLUE), ("ideal ratio mask", o["irm"]["vocals"], BLUE)]
        top = max(v for _, v, _ in vals)
        for name, v, col in vals:
            rows_.add(VGroup(label(name, font_size=19, color=col), Rectangle(width=max(0.03, 5.5 * max(v, 0) / top), height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.8),
                             label(f"{v:.1f} dB", font_size=18, color=WHITE)))
        rows_.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(LEFT * 1.2)
        for r in rows_:
            r[1].next_to(r[0], RIGHT, buff=0.3).align_to(rows_, LEFT).shift(RIGHT * 3.2)
            r[2].next_to(r[1], RIGHT, buff=0.2)
        head = label(r"the vocals, \ every method", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "All together, for the vocals. <bookmark mark='a'/> The factorization and the network, and above them the two "
            "oracles: what perfect knowledge of the answer could do with a mask on this spectrogram."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows_], lag_ratio=0.25), run_time=1.6)
        self.wait(0.6)
        self.clear_scene()
