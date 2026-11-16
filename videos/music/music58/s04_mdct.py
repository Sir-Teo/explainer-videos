from __future__ import annotations

import numpy as np

from videos.music.music58.common import *  # noqa: F403


class Mdct(SoundScene):
    def construct(self):
        chapter(self, 3, r"The MDCT", r"How can a transform overlap its frames and still send no extra numbers?")
        self.why()
        self.basis()
        self.aliases()
        self.cancel()
        self.heard()
        self.bank()

    # ------------------------------------------------------------------
    def why(self):
        items = [
            (r"a coder works on the spectrum: \ masking is decided band by band", WHITE),
            (r"frames must overlap and be windowed, \ or the edges between them click when the coefficients are coarsened", WHITE),
            (r"but overlapping frames by half doubles the numbers \ (an FFT of 2N samples every N gives 2N values for N new samples)", WHITE),
            (r"Princen and Bradley \ (1986): \ a transform of 2N samples to only N coefficients, \ overlapped by half, \ that still rebuilds exactly", TUNE),
        ]
        rows_scene(self, r"why a special transform", items,
                   "A perceptual coder works on the spectrum, because masking is decided band by band. <bookmark mark='b'/> Its "
                   "frames must overlap and be windowed, or the edges between them will click once the coefficients are made "
                   "coarse. <bookmark mark='c'/> But overlapping by half normally doubles the numbers: a Fourier transform of two N "
                   "samples every N samples gives two N values for every N new ones. <bookmark mark='d'/> John Princen and Alan "
                   "Bradley found in 1986 a transform of two N samples to only N coefficients, overlapped by half, that still "
                   "rebuilds the signal exactly.", marks="bcde")

    # ------------------------------------------------------------------
    def basis(self):
        d = load("mdct")
        N = d["N"]
        eq = MathTex(r"X_k = \sum_{n=0}^{2N-1} w_n\, x_n \cos\!\Bigl[\frac{\pi}{N}\Bigl(n + \frac{1}{2} + \frac{N}{2}\Bigr)\Bigl(k + \frac{1}{2}\Bigr)\Bigr], \quad k = 0, \dots, N-1", font_size=30, color=TUNE).to_edge(UP, buff=1.0)
        cols = {"0": TUNE, "1": BLUE, "3": EAR}
        panels = VGroup()
        for i, k in enumerate(("0", "1", "3")):
            ax = frame_axes(width=3.6, height=1.6, xlo=0, xhi=2 * N - 1, ylo=-1.1, yhi=1.1, center=np.array([-4.2 + 4.2 * i, -0.6, 0]))
            ys = d["basis"][k]
            cv = VMobject(stroke_color=cols[k], stroke_width=3).set_points_smoothly([ax.to(n, v) for n, v in enumerate(ys)])
            panels.add(VGroup(ax, cv, label(rf"$k = {k}$", font_size=18, color=cols[k]).next_to(ax, UP, buff=0.1)))
        win = label(r"$w_n = \sin\bigl(\pi(n + \tfrac12)/2N\bigr)$: \ the sine window; \ $w_n^2 + w_{n+N}^2 = 1$", font_size=18, color=WHITE).to_edge(DOWN, buff=0.6)
        head = label(r"the modified discrete cosine transform", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here it is. <bookmark mark='a'/> The modified discrete cosine transform takes a frame of two N samples, windowed, and returns N coefficients, one for each of these windowed cosines: successive half-integer frequency bins, shifted by a quarter frame. <bookmark mark='b'/> The window is a sine, chosen so that the squares of its two halves add to one. The transform appears in MP3 and AAC and in Opus's CELT path; Opus's SILK path uses predictive coding."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in panels], lag_ratio=0.3), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(win))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def aliases(self):
        d = load("mdct")
        N = d["N"]
        x = np.array(d["x"])
        w = np.array(d["w"])
        y = np.array(d["single"])
        ax = frame_axes(width=10.0, height=3.0, xlo=0, xhi=2 * N - 1, ylo=-1.6, yhi=1.6, center=DOWN * 0.4)
        cx = VMobject(stroke_color=GREY_B, stroke_width=2.5).set_points_as_corners([ax.to(n, v) for n, v in enumerate(w * x)])
        cy = VMobject(stroke_color=EAR, stroke_width=3).set_points_as_corners([ax.to(n, v) for n, v in enumerate(y)])
        mid = DashedLine(ax.to(N - 0.5, -1.6), ax.to(N - 0.5, 1.6), color=GREY_D, stroke_width=1.5)
        key = VGroup(label(r"one frame, \ windowed", font_size=16, color=GREY_B), label(r"MDCT then inverse MDCT, \ alone", font_size=16, color=EAR)).arrange(RIGHT, buff=0.8).to_edge(UP, buff=1.0)
        note = label(r"N numbers cannot hold 2N samples: \ each half comes back with its own mirror image added \ (time-domain aliasing)", font_size=17, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"one frame's aliases", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "But N numbers cannot hold two N samples. <bookmark mark='a'/> Take one frame, windowed, in grey, <bookmark mark='b'/> "
            "and send it through the transform and back on its own, in orange. It is not the frame: each half has come back "
            "with its own mirror image added to it, the first half reflected with one sign, the second with the other. This "
            "error is called time-domain aliasing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(mid), FadeIn(ghost(VGroup(cx, cy), 0.25)))
            vo.wait_until("a")
            self.play(Create(cx), FadeIn(key[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(cy), FadeIn(key[1]), FadeIn(note), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cancel(self):
        d = load("mdct")
        sig = np.array(d["sig"])
        y = np.array(d["rebuilt"])
        ax = frame_axes(width=10.0, height=2.6, xlo=0, xhi=len(sig) - 1, ylo=min(sig) - 0.5, yhi=max(sig) + 0.5, center=DOWN * 0.6)
        cs = VMobject(stroke_color=GREY_B, stroke_width=6).set_points_as_corners([ax.to(n, v) for n, v in enumerate(sig)])
        cy = VMobject(stroke_color=TUNE, stroke_width=2).set_points_as_corners([ax.to(n, v) for n, v in enumerate(y)])
        eq = MathTex(r"\text{frame } i \text{'s second half} + \text{frame } i{+}1\text{'s first half}: \quad \text{aliases equal and opposite}", font_size=28).to_edge(UP, buff=1.0)
        note = label(rf"rebuilt by overlap-add: \ the largest error {d['max_err_small']:.0e} here, \ {d['max_err_mix']:.0e} on our whole mix: \ machine precision", font_size=18, color=TUNE).to_edge(DOWN, buff=0.4)
        head = label(r"the aliases cancel", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Now overlap the frames by half, window them again, and add. <bookmark mark='a'/> In each overlap, one frame's "
            "second half and the next frame's first half carry the same alias with opposite signs, and the window's squares add "
            "to one. <bookmark mark='b'/> So the sum is the signal itself. Here, in gold over grey, a signal rebuilt from its "
            f"MDCT frames: the largest error is {say(d['max_err_small'] * 1e15, 0)} times ten to the minus fifteen, and on our "
            "whole mix about ten to the minus thirteen: the limit of the computer's arithmetic. Time-domain aliasing "
            "cancellation, TDAC: N new coefficients for N new samples, and nothing lost."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(cs))
            vo.wait_until("a")
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(Create(cy), FadeIn(note), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("mdct")
        c = clip("mdct.two")
        boxes = choice_boxes([r"every frame", r"every other frame"], width=3.2, height=0.9, buff=1.2, size=20).move_to(UP * 0.4)
        note = label(r"drop every other frame and each survivor's aliases are left uncancelled", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.5)
        head = label(r"aliases, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the aliases: our mix rebuilt from all its frames, then from every other frame alone, so that no alias has a partner to cancel it."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(note))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"all frames, \ then half", kind="physical model", detail=r"Part 56's mix, \ the MDCT", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["whole"], st["alternate"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["alternate"], c.duration, buff=0.08)
        with self.voiceover(
            "The first is the mix exactly. The second flutters and smears, every note followed by a reversed ghost: the aliases "
            "a coder relies on its neighbours to cancel. A coarse coder leaves a little of this behind."
        ):
            self.play(Indicate(boxes[1], color=EAR, scale_factor=1.04))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bank(self):
        items = [
            (r"an MDCT of 1,024 coefficients at 48 kHz is a bank of 1,024 filters, \ each 23 Hz wide, \ refreshed every 21 ms", WHITE),
            (r"critical bands are 100 Hz wide in the bass and several kHz in the treble: \ the coder groups bins into bands to match", WHITE),
            (r"the sine window's filters leak; \ AAC also offers a Kaiser-derived window, \ sharper, \ for tonal music", WHITE),
            (r"the same transform, \ run on shorter frames, \ trades that frequency resolution for time", TUNE),
        ]
        rows_scene(self, r"a bank of filters", items,
                   "Seen another way, the MDCT is a filter bank. <bookmark mark='b'/> With a thousand and twenty-four coefficients "
                   "at forty-eight kilohertz it is a bank of a thousand and twenty-four filters, each twenty-three hertz wide, "
                   "refreshed every twenty-one milliseconds. <bookmark mark='c'/> Critical bands are a hundred hertz wide in the bass "
                   "and several kilohertz in the treble, so the coder groups bins into bands to match the ear. "
                   "<bookmark mark='d'/> The sine window's filters leak into their neighbours; AAC also offers a Kaiser-derived "
                   "window, sharper, for tonal music. <bookmark mark='e'/> And the same transform run on shorter frames trades that "
                   "frequency resolution for time, which is the next chapter's subject.", marks="bcde")
