from __future__ import annotations

import numpy as np

from videos.music.music58.common import *  # noqa: F403


class PreEcho(SoundScene):
    def construct(self):
        chapter(self, 5, r"Window switching and pre-echo", r"Why does a codec smear a castanet?")
        self.problem()
        self.zoom()
        self.quiz()
        self.switching()

    # ------------------------------------------------------------------
    def problem(self):
        d = load("preecho")
        items = [
            (rf"a long block \ ({d['block_ms']['long']:.0f} ms) \ gives fine frequency resolution: \ the mask can be followed band by narrow band", WHITE),
            (r"but its quantization noise spreads evenly over the whole block", WHITE),
            (r"a castanet hit in the middle of a block: \ the noise arrives up to 20 ms before the hit, \ in silence", WHITE),
            (r"pre-masking hides only a few milliseconds of it: \ the rest is heard as a swish before each attack, \ pre-echo", TUNE),
        ]
        rows_scene(self, r"time against frequency", items,
                   "Every transform trades time for frequency. <bookmark mark='b'/> A long block, forty-three milliseconds here, resolves the spectrum finely, so the coder can follow the mask band by narrow band. <bookmark mark='c'/> But its quantization error can spread across the transform window, including before an attack. <bookmark mark='d'/> Put a castanet hit in the middle of a block, and its coding noise arrives up to twenty milliseconds before the hit, in silence. <bookmark mark='e'/> Pre-masking hides only a few milliseconds of that; the rest is heard as a swish before each attack: pre-echo.", marks="bcde")

    # ------------------------------------------------------------------
    def zoom(self):
        d = load("preecho")
        z = d["zoom"]
        t = np.array(z["t"])
        x = np.array(z["x"])
        top = np.max(np.abs(x)) * 1.1
        a1 = frame_axes(width=10.0, height=1.6, xlo=t[0], xhi=t[-1], ylo=-top, yhi=top, center=UP * 1.0)
        a2 = frame_axes(width=10.0, height=1.6, xlo=t[0], xhi=t[-1], ylo=-top, yhi=top, center=DOWN * 1.3)
        el = np.array(z["long"]) - x
        es = np.array(z["short"]) - x
        g = 8.0
        cl = VMobject(stroke_color=EAR, stroke_width=1.5).set_points_as_corners([a1.to(a, np.clip(g * b, -top, top)) for a, b in zip(t, el)])
        cs = VMobject(stroke_color=TUNE, stroke_width=1.5).set_points_as_corners([a2.to(a, np.clip(g * b, -top, top)) for a, b in zip(t, es)])
        hx = VGroup(*[VMobject(stroke_color=GREY_D, stroke_width=1.2).set_points_as_corners([a.to(p, q) for p, q in zip(t, x)]) for a in (a1, a2)])
        zero = VGroup(*[DashedLine(a.to(0, -top), a.to(0, top), color=GREY_A, stroke_width=1.5) for a in (a1, a2)])
        l1 = label(rf"long blocks: \ the coding error, \ $\times 8$, \ before the hit: \ {d['pre_long']:.0f} dB re the hit", font_size=16, color=EAR).next_to(a1, UP, buff=0.08).align_to(a1, LEFT)
        l2 = label(rf"short blocks: \ {d['pre_short']:.0f} dB", font_size=16, color=TUNE).next_to(a2, UP, buff=0.08).align_to(a2, LEFT)
        xt = VGroup(*[label(f"{v:+d} ms" if v else "the hit", font_size=13, color=GREY_A).next_to(a2.to(v, -top), DOWN, buff=0.08) for v in (-30, -20, -10, 0, 10, 20)])
        note = label(rf"both with their noise at the mask; \ the long blocks need {d['kbps']['long']:.0f} kbit/s, \ the short ones {d['kbps']['short']:.0f}", font_size=17, color=WHITE).to_edge(DOWN, buff=0.3)
        head = label(r"30 ms before a hit", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the coding error around one castanet hit, magnified eight times, with the hit in grey behind. "
            "<bookmark mark='a'/> With long blocks the error starts long before the hit: "
            f"{say(-d['pre_long'])} decibels below the hit, in the fifteen milliseconds before it. <bookmark mark='b'/> With "
            f"short blocks of five milliseconds it starts just before, {say(-d['pre_short'])} decibels down. "
            "<bookmark mark='c'/> But both put their noise right at the mask, and the short blocks need three times the bits to "
            "do it, because each one carries its own scale factors and resolves the spectrum coarsely."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a1), FadeIn(a2), FadeIn(hx), FadeIn(zero), FadeIn(xt))
            vo.wait_until("a")
            self.play(Create(cl), FadeIn(l1), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(cs), FadeIn(l2), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("preecho")
        c = clip("preecho.two")
        card = listen_card(r"Castanet-like hits through our coder twice: \ once with long blocks, \ once with short ones. \ Which had "
                           r"a swish before each hit?", width=10.0)
        with self.voiceover("Your turn. Castanet-like hits through our coder twice, once with long blocks and once with short ones. Which had a swish before each hit?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"long, \ short?", kind="physical model", detail=r"Part 40's clave, \ Monochord's coder", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["long"], st["short"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["short"], c.duration, buff=0.08)
        res = label(r"the first, \ with long blocks: \ a soft smear before each attack", font_size=19, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover("The first, with long blocks: each hit is preceded by a soft smear, as if the castanet were being rubbed before it is struck. Listen for it on headphones; it is subtle on loudspeakers."):
            self.play(boxes[0][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def switching(self):
        items = [
            (r"window switching: \ long blocks for steady sound, \ eight short blocks the moment an attack is detected", WHITE),
            (r"the window's shape must change smoothly \ (start and stop windows), \ so that the aliases still cancel", WHITE),
            (r"AAC: \ 2,048 and 256 samples; \ MP3: \ 576 and 192, \ inside a filter bank; \ Opus: \ 2.5 to 20 ms", WHITE),
            (r"temporal noise shaping \ (AAC): \ predicts across frequency, \ which shapes the noise in time inside a long block", WHITE),
            (r"a bit reservoir pays for the expensive short blocks from the cheap frames around them", TUNE),
        ]
        rows_scene(self, r"window switching", items,
                   "The cure is to switch. <bookmark mark='b'/> Use long blocks for steady sound, and eight short blocks the moment an attack is detected. <bookmark mark='c'/> The window's shape must change smoothly, through start and stop windows, so that the aliases still cancel. <bookmark mark='d'/> Common AAC-LC modes use two-thousand-and-forty-eight-sample long windows and two-hundred-and-fifty-six-sample short windows; other frame configurations exist; MP3 between five hundred and seventy-six and a hundred and ninety-two, inside a filter bank; Opus uses frames of two and a half to twenty milliseconds. <bookmark mark='e'/> AAC adds temporal noise shaping, a prediction across frequency that shapes the noise in time within a long block. <bookmark mark='f'/> And the bit reservoir pays for the expensive short blocks from the cheap frames around them.", marks="bcdef")
