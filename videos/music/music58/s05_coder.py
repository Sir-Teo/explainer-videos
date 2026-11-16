from __future__ import annotations

import numpy as np

from videos.music.music58.common import *  # noqa: F403


def box(text, color=GREY_B, w=2.0, h=0.8, size=16):
    return VGroup(RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=color, stroke_width=2.5), label(text, font_size=size, color=color))


class Coder(SoundScene):
    def construct(self):
        chapter(self, 4, r"A perceptual coder", r"How do you spend a fixed number of bits where the ear will notice?")
        self.diagram()
        self.steps()
        self.rate()
        self.table()
        self.heard()

    # ------------------------------------------------------------------
    def diagram(self):
        top = VGroup(box(r"signal"), box(r"MDCT \ (2048, \ hop 1024)", TUNE), box(r"quantize each band", TUNE), box(r"Rice codes", TUNE), box(r"bits")).arrange(RIGHT, buff=0.45).move_to(UP * 0.9)
        arr = VGroup(*[Arrow(top[i].get_right(), top[i + 1].get_left(), buff=0.05, color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.3) for i in range(4)])
        model = box(r"masking model", EAR, w=2.4).next_to(top[2], DOWN, buff=1.0)
        ma = VGroup(Arrow(top[1].get_bottom(), model.get_left(), buff=0.05, color=EAR, stroke_width=3), Arrow(model.get_top(), top[2].get_bottom(), buff=0.05, color=EAR, stroke_width=3))
        rate = box(r"rate control: \ one margin for all", BLUE, w=3.6).next_to(model, DOWN, buff=0.6)
        ra = Arrow(rate.get_top(), model.get_bottom(), buff=0.05, color=BLUE, stroke_width=3)
        head = label(r"Monochord's coder", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        note = label(r"\texttt{codec.encode(x, kbps)}: \ about 150 lines", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is the coder this part builds, the shape of every perceptual codec. <bookmark mark='a'/> The signal is cut "
            "into MDCT frames of two thousand and forty-eight samples, a new frame every twenty-one milliseconds. "
            "<bookmark mark='b'/> The masking model looks at each frame and says how much noise each band can hide. "
            "<bookmark mark='c'/> Each band is quantized with a step size from that allowance, and Rice-code lengths are estimated with a fixed per-band overhead. "
            "<bookmark mark='d'/> And a rate control turns one knob for the whole signal until the estimated bits fit the budget."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(VGroup(top, model, rate), 0.25)), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(top[:2]), FadeIn(arr[0]))
            vo.wait_until("b")
            self.play(FadeIn(model), FadeIn(ma))
            vo.wait_until("c")
            self.play(FadeIn(top[2:]), FadeIn(arr[1:]))
            vo.wait_until("d")
            self.play(FadeIn(rate), FadeIn(ra))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def steps(self):
        lines = VGroup(
            MathTex(r"\text{a uniform quantizer of step } \Delta \text{ has approximate error variance } \Delta^2/12 \text{ per coefficient}", font_size=30),
            MathTex(r"\Delta_b = \sqrt{\frac{12\,M_b}{n_b}}\;10^{-m/20} \qquad (M_b \text{ the band's allowed noise}, \ n_b \text{ its coefficients})", font_size=30, color=TUNE),
            MathTex(r"m > 0: \text{ the noise sits } m \text{ dB below the mask}; \quad m < 0: \text{ above the model threshold}", font_size=30),
            MathTex(r"\text{estimated bits} = \sum_{\text{frames, bands}} \bigl(6 \text{ for the scale factor} + \text{Rice}(q)\bigr)", font_size=30),
        ).arrange(DOWN, buff=0.45).move_to(DOWN * 0.1)
        head = label(r"bit allocation by step size", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The bit allocation is hidden in the step sizes. <bookmark mark='a'/> Under a high-resolution, approximately uniform error model, a quantizer of step delta has error variance delta squared over twelve; coarse, signal-dependent quantization can depart from this. <bookmark mark='b'/> So choose each band's step to put its noise exactly at the band's allowance, and then lower it by a margin, m decibels, the same for every band. <bookmark mark='c'/> A positive margin puts the noise below the mask; a negative one above it, where it can be heard. <bookmark mark='d'/> Our rate estimate charges six bits per scale factor plus Rice-code costs; the teaching implementation does not serialize or quantize these scale factors into a complete interoperable bitstream; bands where everything quantizes to zero cost almost nothing, and that is where most of the saving comes from."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.25)))
            for mark, ln in zip("abcd", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln), run_time=0.8)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rate(self):
        items = [
            (r"rate control: \ find the margin $m$ that makes the whole signal fit the bit rate, \ by bisection", WHITE),
            (r"plenty of bits: \ the margin is positive, \ low predicted noise-to-mask ratio; \ transparency needs listening tests", WHITE),
            (r"too few: \ the margin goes negative, \ and the noise rises above the mask in band after band", WHITE),
            (r"real coders also low-pass at low rates, \ spending nothing above 9 to 16 kHz, \ and keep a bit reservoir between frames", TUNE),
        ]
        rows_scene(self, r"rate control", items,
                   "Then the rate control. <bookmark mark='b'/> Find the one margin that makes the whole signal fit the bit rate, "
                   "by bisection. <bookmark mark='c'/> With plenty of bits the margin is positive, and the noise sits under the mask "
                   "everywhere: the model predicts low audibility; transparency requires controlled listening tests. <bookmark mark='d'/> With too few, the margin goes negative, and the noise "
                   "rises above the mask in band after band. <bookmark mark='e'/> Real coders also cut off the top of the spectrum "
                   "at low rates, spending nothing above nine to sixteen kilohertz, and keep a reservoir of bits so that hard frames "
                   "can borrow from easy ones.", marks="bcde")

    # ------------------------------------------------------------------
    def table(self):
        d = load("rates")
        rows = VGroup(VGroup(label(r"target rate", font_size=16, color=GREY_A), label(r"target ratio", font_size=16, color=GREY_A), label(r"voice: \ margin", font_size=16, color=GREY_A),
                             label(r"mix: \ margin", font_size=16, color=GREY_A), label(r"mix: \ bands over the mask", font_size=16, color=GREY_A), label(r"cut above", font_size=16, color=GREY_A)))
        for v, m in zip(d["voice"], d["mix"]):
            col = TUNE if m["margin"] > 0 else EAR
            rows.add(VGroup(label(f"{v['target']} kbit/s", font_size=18, color=col), label(rf"1/{d['pcm_kbps'] / v['target']:.0f}", font_size=18, color=WHITE),
                            label(f"{v['margin']:+.0f} dB", font_size=18, color=WHITE), label(f"{m['margin']:+.0f} dB", font_size=18, color=col),
                            label(rf"{100 * m['over']:.0f}\%", font_size=18, color=WHITE), label(f"{m['cutoff'] / 1000:.0f} kHz", font_size=18, color=WHITE)))
        rows.arrange(DOWN, buff=0.3)
        xs = [-5.2, -3.2, -1.2, 0.9, 3.0, 5.2]
        for r in rows:
            for i, m_ in enumerate(r):
                m_.set_x(xs[i])
        rows.move_to(UP * 0.1)
        note = label(r"margin: \ how far below the mask the noise sits \ (negative: \ above it); \ mono, \ 48 kHz; \ the original is 768 kbit/s", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.45)
        head = label(r"nominal targets and estimated masking margins", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is our coder on the voice alone and on the mix, at five bit rates. <bookmark mark='a'/> At a hundred and "
            "twenty-eight kilobits both are far under the mask. At sixty-four the voice still has sixteen decibels to spare, the "
            "busy mix only three. <bookmark mark='b'/> At thirty-two the mix's noise is above the mask in most of its bands, and "
            "at sixteen seventeen decibels above. The voice alone is the easier signal for this coder, because its spectrum is "
            "sparse and its bits go a long way; but where a coder does fail on a lone voice, nothing else is playing to hide "
            "the failure, which is what made Tom's Diner such a good test."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[3:]], lag_ratio=0.3), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("rates")
        c = clip("rates.voice")
        names = [f"k{kb}" for kb in (128, 64, 32, 24, 16)]
        boxes = choice_boxes([r"128", r"64", r"32", r"24", r"16"], width=1.8, height=0.9, buff=0.5, size=22).move_to(UP * 0.4)
        note = label(r"the voice alone, \ kbit/s", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.5)
        head = label(r"five rates, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the voice alone at the five rates, from a hundred and twenty-eight kilobits down to sixteen."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(note))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"128 down to 16", kind="physical model", detail=r"Part 8's voice, \ Monochord's coder", corner=DL, tag_corner=DR)
            for i, k in enumerate(names):
                end = st[names[i + 1]] - 0.3 if i + 1 < len(names) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.06)
        with self.voiceover(
            "The first two may sound close to the original; we have not established indistinguishability in a listener study; at thirty-two a faint roughness appears; at twenty-four and "
            "sixteen the voice turns watery and metallic, the sound of a coder starved of bits."
        ):
            self.play(Indicate(boxes[4], color=EAR, scale_factor=1.04))
        self.wait(0.4)
        self.clear_scene()
