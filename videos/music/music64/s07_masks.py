from __future__ import annotations

import numpy as np

from videos.music.music64.common import *  # noqa: F403

STEM_NAMES = (("vocals", r"vocals", TUNE), ("bass", r"bass", BLUE), ("drums", r"drums", EAR), ("other", r"other", GREY_B))


class Masks(SoundScene):
    def construct(self):
        chapter(self, 6, r"Masks and their bounds", r"What is the best that any mask could do?")
        self.idea()
        self.pictures()
        self.table()
        self.heard()

    # ------------------------------------------------------------------
    def idea(self):
        lines = VGroup(
            label(r"nearly every separator in this part is a mask: \ a number between 0 and 1 for every time-frequency bin", font_size=20, color=WHITE),
            MathTex(r"\hat S_j(t, f) = M_j(t, f)\, X(t, f)", font_size=38, color=TUNE),
            label(r"if we knew the true sources, \ we could choose the best masks:", font_size=20, color=WHITE),
            MathTex(r"\text{binary: } M_j = \big[\,|S_j| = \max_k |S_k|\,\big], \qquad \text{ratio: } M_j = \frac{|S_j|}{\sum_k |S_k|}", font_size=32, color=WHITE),
            label(r"they need the answer, \ so they are not methods: \ they are the ceiling for every masking method on this STFT", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.4)
        head = label(r"oracle masks", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Step back. <bookmark mark='a'/> Nearly every method so far is a mask: a number between nought and one for every "
            "bin of the spectrogram, <bookmark mark='b'/> multiplied into the mixture. <bookmark mark='c'/> If we knew the "
            "true sources, we could choose the best masks. <bookmark mark='d'/> The ideal binary mask gives each bin to the "
            "loudest source; the ideal ratio mask shares each bin in proportion. <bookmark mark='e'/> They need the answer, so "
            "they are not methods; they are the ceiling for every masking method on this spectrogram."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcde", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        o = load("oracle")["sdr"]
        n = load("nmf")["sdr"]
        g = VGroup()
        for k, name, col in STEM_NAMES:
            g.add(VGroup(label(name, font_size=20, color=col), label(f"{n[k]:.1f}", font_size=20, color=WHITE), label(f"{o['ibm'][k]:.1f}", font_size=20, color=WHITE),
                         label(f"{o['irm'][k]:.1f}", font_size=20, color=WHITE), label(f"{o['true_phase'][k]:.1f}", font_size=20, color=TUNE)))
        g.arrange(DOWN, buff=0.42)
        for r in g:
            for i, x in enumerate((-4.6, -1.8, 0.4, 2.6, 4.9)):
                r[i].set_x(x)
        top = VGroup(*[label(t, font_size=15, color=GREY_A).move_to([x, g.get_top()[1] + 0.5, 0]) for t, x in
                       ((r"NMF", -1.8), (r"ideal binary", 0.4), (r"ideal ratio", 2.6), (r"ratio, \ true phase", 4.9))])
        note = label(r"SDR in dB against each true stem: \ the gap between NMF and the oracles is what better masks could still win", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.45)
        head = label(r"how far from the ceiling?", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here are the ceilings, stem by stem. <bookmark mark='a'/> NMF, from the last chapter. <bookmark mark='b'/> The "
            "ideal binary mask: NMF is already close to it, and for the bass and the piano and guitar a little above it. "
            "<bookmark mark='c'/> The ideal ratio mask is higher for all but the drums, whose hits so dominate their bins that "
            f"giving each bin away wins. NMF's vocals are only {say(o['irm']['vocals'] - n['vocals'], 1)} decibels below this "
            "ceiling. <bookmark mark='d'/> The last column gives the ratio mask the true phase of each source, which no mask "
            f"can, and it is {say(o['true_phase']['vocals'] - o['irm']['vocals'], 1)} decibels higher again for the vocals: the "
            "biggest gap of all, and the next chapter's subject."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*[r[0] for r in g])), FadeIn(note))
            for mark, i in zip("abcd", range(1, 5)):
                vo.wait_until(mark)
                self.play(FadeIn(top[i - 1]), FadeIn(VGroup(*[r[i] for r in g])))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("oracle")
        c = clip("oracle.three")
        boxes = choice_boxes([r"ideal binary", r"ideal ratio", r"the true vocals"], width=3.2, height=0.9, buff=0.5, size=19).move_to(UP * 0.5)
        note = label(r"the binary mask leaves holes, \ a gargle called musical noise; \ the ratio mask is smoother, \ and nearly the truth", font_size=17, color=GREY_A).next_to(boxes, DOWN, buff=0.6)
        head = label(r"the oracles, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the vocals through the ideal binary mask, the ideal ratio mask, and as recorded."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two oracles, \ then truth", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            ks = ["ibm", "irm", "true"]
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.3 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.08)
        with self.voiceover("The binary mask switches bins fully on and off, and the holes it leaves gargle: musical noise. The ratio mask is smoother, and close to the truth."):
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pictures(self):
        d = load("maskimg")
        mx = np.array(d["mix"])
        pics = [heat_image(mx[::-1], mx.max() - 3.5, mx.max(), width=5.6, height=2.3),
                heat_image(np.array(d["ibm"])[::-1], 0, 1, width=5.6, height=2.3, smooth=False),
                heat_image(np.array(d["irm"])[::-1], 0, 1, width=5.6, height=2.3)]
        g = Group(*pics[1:]).arrange(RIGHT, buff=0.5).move_to(DOWN * 1.3)
        pics[0].move_to(UP * 1.4)
        ls = [label(r"the mixture \ (0 to 4.7 kHz, \ the first phrases)", font_size=15, color=GREY_A).next_to(pics[0], UP, buff=0.12),
              label(r"the vocals' ideal binary mask", font_size=15, color=GREY_A).next_to(pics[1], UP, buff=0.12),
              label(r"the vocals' ideal ratio mask", font_size=15, color=GREY_A).next_to(pics[2], UP, buff=0.12)]
        head = label(r"masks, \ as pictures", font_size=24, color=GREY_A).to_edge(UP, buff=0.2)
        with self.voiceover(
            "Here are the vocals' two ideal masks beside the mixture. <bookmark mark='a'/> The binary mask is black and white: "
            "each bin is the voice's or not. <bookmark mark='b'/> The ratio mask has shades of grey, sharing each bin. Both "
            "trace the voice's harmonics, and both need the true vocals to draw."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pics[0]), FadeIn(ls[0]))
            vo.wait_until("a")
            self.play(FadeIn(pics[1]), FadeIn(ls[1]))
            vo.wait_until("b")
            self.play(FadeIn(pics[2]), FadeIn(ls[2]))
        self.wait(0.6)
        self.clear_scene()
