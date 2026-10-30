from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import PART, SND_C, curve, load, spectro

ALIAS_C = C.SURPRISE


class Sampling(VoiceoverScene):
    def construct(self):
        self.card()
        self.alias()
        self.tones()
        self.speech()
        self.mel()

    def card(self):
        card = chapter_card(8, r"Sampling sound", r"How many numbers make a second of speech?", part=PART)
        with self.voiceover("Chapter eight. Sampling sound."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def alias(self):
        q = load("nyquist")
        tt, ts = np.asarray(q["tt"]), np.asarray(q["ts"])
        ax = Axes(x_range=[0, 0.002, 0.0005], y_range=[-1.2, 1.2, 1], x_length=6.0, y_length=2.4, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([-3.4, 1.6, 0])
        hi = curve(ax, tt, np.cos(2 * np.pi * 7000 * tt), ALIAS_C, 2.5)
        lo = curve(ax, tt, np.cos(2 * np.pi * 1000 * tt), SND_C, 3.5)
        dots = VGroup(*[Dot(ax.c2p(t, np.cos(2 * np.pi * 7000 * t)), radius=0.07, color=WHITE) for t in ts])
        lh = label(r"$7$ kHz", font_size=22, color=ALIAS_C).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        ll = label(r"$1$ kHz", font_size=22, color=SND_C).next_to(lh, RIGHT, buff=0.4)
        ld = label(r"samples, \ $8{,}000$ a second", font_size=22, color=WHITE).next_to(ll, RIGHT, buff=0.4)
        tl = label(r"$2$ milliseconds", font_size=18, color=GREY_B).next_to(ax, DOWN, buff=0.1)
        colors = {r"f_s": GREY_A, r"f": SND_C}
        rows = [MathTex(r"x_n = \cos\!\big(2\pi f\, n / f_s\big)", font_size=34),
                MathTex(r"\cos\!\big(2\pi (f + k f_s)\, n / f_s\big) = \cos\!\big(2\pi f n / f_s + 2\pi k n\big) = x_n",
                        font_size=32),
                MathTex(r"\cos\!\big(2\pi (f_s - f)\, n / f_s\big) = \cos\!\big(2\pi n - 2\pi f n / f_s\big) = x_n",
                        font_size=32),
                MathTex(r"\text{only } 0 \le f \le f_s / 2 \text{ can be told apart}", font_size=32, color=SND_C)]
        whys = [why(r"a tone of frequency $f$, \ sampled at $f_s$", font_size=20),
                why(r"$2\pi k n$: \ whole turns", font_size=20),
                why(r"cosine is even", font_size=20),
                why(r"Nyquist's frequency, \ $f_s / 2$", font_size=20)]
        step = ladder(self, rows, whys, keep=4, top=0.1, x=-0.6, align_index=None, buff=0.32, edge=6.9)
        cite_ = cite(r"H.~Nyquist (1928); \ C.~E.~Shannon (1949)", corner=UR)
        with self.voiceover(
            "A microphone measures air pressure, and a computer keeps a sample of it at regular ticks. How fast is "
            "fast enough? <bookmark mark='a'/> Take a pure tone of frequency f, sampled f s times a second. "
            "<bookmark mark='b'/> Add f s to the frequency, and at every sample the phase gains a whole number of "
            "turns, so the samples don't change at all. <bookmark mark='c'/> And because cosine is even, f s minus f "
            "gives the same samples as f. <bookmark mark='d'/> So the samples can only tell apart frequencies "
            "between zero and half the sampling rate. A seven kilohertz tone sampled eight thousand times a second "
            "lands exactly on a one kilohertz tone. The converse is the sampling theorem of Nyquist and Shannon: a "
            "signal with nothing above half the rate is fixed exactly by its samples."
        ) as vo:
            self.play(FadeIn(ax), Create(lo), FadeIn(ll), FadeIn(tl), FadeIn(cite_))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            step(2, transform=False)
            vo.wait_until("d")
            step(3, transform=False)
            self.play(Create(hi), FadeIn(lh), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in dots], lag_ratio=0.1), FadeIn(ld), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tones(self):
        q = load("nyquist")
        fs = int(q["fs"])
        true, seen = np.asarray(q["true"]), np.asarray(q["seen"])
        ax = axes([0, 16, 4], [0, 4.4, 1], x_length=10.0, y_length=4.2, xlabel=r"the tone's frequency, \ kHz",
                  ylabel=r"the frequency the samples show, \ kHz", xticks=[0, 4, 8, 12, 16], yticks=[0, 2, 4],
                  center=[-0.4, -0.6, 0])
        zig = curve(ax.ax, true / 1000, seen / 1000, SND_C, 4)
        tones = {int(k): float(v) for k, v in q["tones"].items()}
        pts = VGroup()
        for i, (f, s) in enumerate(sorted(tones.items())):
            pts.add(VGroup(Dot(ax.ax.c2p(f / 1000, s / 1000), radius=0.09, color=WHITE),
                           label(rf"${f / 1000:g} \to {s / 1000:.2f}$", font_size=20, color=WHITE)
                           .next_to(ax.ax.c2p(f / 1000, s / 1000), UL if f < fs / 2 else UR, buff=0.12)))
        ny = DashedLine(ax.ax.c2p(4, 0), ax.ax.c2p(4, 4.3), color=GREY_B)
        nyl = label(r"$f_s / 2$", font_size=22, color=GREY_B).next_to(ax.ax.c2p(4, 4.3), UP, buff=0.05)
        peaks = ", ".join(f"{tones[f] / 1000:.2f}" for f in sorted(tones))
        info = label(rf"measured: \ tones sampled at ${fs // 1000}$ kHz, \\ the peak of each one's spectrum", font_size=22,
                     color=GREY_A).to_corner(UR, buff=0.6)
        with self.voiceover(
            "We can check it numerically. <bookmark mark='a'/> Sample tones of one, three, five and seven kilohertz "
            f"eight thousand times a second, and find the peak of each one's spectrum: {peaks} kilohertz. "
            "<bookmark mark='b'/> Above four kilohertz, every frequency folds back into the band below, a zigzag: "
            "aliasing."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(info), Create(ny), FadeIn(nyl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_, scale=1.3) for p_ in pts], lag_ratio=0.3), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(zig), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def speech(self):
        q = load("nyquist")
        full, naive, proper = (np.asarray(q[k]) for k in ("spec_full", "spec_naive", "spec_proper"))
        lo = max(full.max(), naive.max()) - 70
        hi_ = max(full.max(), naive.max())
        W, H = 5.6, 1.6
        a = spectro(full, W, H, lo=lo, hi=hi_).move_to([-3.2, 1.6, 0])
        b = spectro(naive, W, H, lo=lo, hi=hi_).move_to([-3.2, -0.9, 0])
        c = spectro(proper, W, H, lo=lo, hi=hi_).move_to([3.2, -0.9, 0])
        la = label(r"$16$ kHz: \ the part below $2$ kHz", font_size=20, color=GREY_A).next_to(a, UP, buff=0.1)
        lb = label(r"every fourth sample, \ no filter: \ aliased", font_size=20, color=ALIAS_C).next_to(b, UP, buff=0.1)
        lc = label(r"filter out $2$ kHz and up, \ then every fourth", font_size=20, color=SND_C).next_to(c, UP, buff=0.1)
        above, fold = float(q["above2k"]), float(q["folded_share"])
        rates = VGroup(*[label(t, font_size=22, color=GREY_A) for t in (
            r"the telephone: \ $8$ kHz", r"Whisper: \ $16$ kHz", r"audio codecs, \ the narrator: \ $24$ kHz",
            r"music: \ $44.1$ kHz")]).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.4, 1.25, 0])
        fl = label(r"frequency $\uparrow$, \ time $\to$", font_size=18, color=GREY_B).next_to(a, DOWN, buff=0.08)
        big = label(rf"${100 * above:.0f}\%$ of the energy \\ lies above $2$ kHz", font_size=30, color=SND_C).move_to([3.4, 2.4, 0])
        with self.voiceover(
            "Speech shows why this matters. <bookmark mark='a'/> In this sentence from a held-out Kokoro voice, "
            f"{100 * above:.0f} percent of the energy lies above two kilohertz. <bookmark mark='b'/> Keep every fourth "
            "sample, four thousand a second, and that energy doesn't vanish; it folds down into the band that's left: "
            f"by our measure, {100 * fold:.0f} percent of what remains below two kilohertz is folded energy. "
            "<bookmark mark='c'/> Filter first, then keep every fourth, and the band below two kilohertz is clean. "
            "<bookmark mark='d'/> So every sampling rate is a decision about what to keep: eight kilohertz for the "
            "telephone, sixteen for Whisper, twenty-four for most audio codecs."
        ) as vo:
            self.play(FadeIn(a), FadeIn(la), FadeIn(fl))
            vo.wait_until("a")
            self.play(FadeIn(big))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(lb))
            vo.wait_until("c")
            self.play(FadeIn(c), FadeIn(lc))
            vo.wait_until("d")
            self.play(big.animate.scale(0.7).move_to([3.4, 2.65, 0]), LaggedStart(*[FadeIn(r_) for r_ in rates], lag_ratio=0.3),
                      run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mel(self):
        m = load("mel")
        P = np.asarray(m["power_db"])
        n = int(m["n_frames"])
        P = P[:, :n]
        M = np.asarray(m["mel"])
        Wf = np.asarray(m["filters"])
        lo = P.max() - 80
        spec = spectro(P, 5.4, 2.4, lo=lo, hi=P.max()).move_to([-3.5, 1.4, 0])
        sl = label(r"the STFT: \ $25$ ms windows every $10$ ms \\ $201$ frequencies, \ $0$ to $8$ kHz", font_size=20,
                   color=GREY_A).next_to(spec, UP, buff=0.1)
        # the mel filters as triangles over a linear frequency axis
        fax = Axes(x_range=[0, 8000, 1000], y_range=[0, 1.05, 1], x_length=5.4, y_length=1.6, tips=False,
                   axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([3.5, 1.5, 0])
        freqs = np.linspace(0, 8000, Wf.shape[1])
        tri = VGroup()
        for i in range(0, Wf.shape[0], 2):
            w = Wf[i] / max(Wf[i].max(), 1e-12)
            nz = np.nonzero(w > 0)[0]
            if len(nz) < 1:
                continue
            a, b = max(nz[0] - 1, 0), min(nz[-1] + 1, len(w) - 1)
            tri.add(curve(fax, freqs[a:b + 1], w[a:b + 1], SND_C, 1.6))
        fl = label(r"$80$ mel filters (every other one drawn): \\ even steps in pitch, \ not in hertz", font_size=20,
                   color=GREY_A).next_to(fax, UP, buff=0.1)
        fx = label(r"$0$ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ $8$ kHz",
                   font_size=18, color=GREY_B).next_to(fax, DOWN, buff=0.05)
        mel = spectro(M, 9.0, 2.0, lo=M.min(), hi=M.max()).move_to([0, -1.75, 0])
        ml = label(rf"Whisper's input: \ $80$ log-mel bands every $10$ ms \ (``{m['text']}'')", font_size=20,
                   color=SND_C).next_to(mel, UP, buff=0.1)
        if ml.width > 13:
            ml.width = 13
        diff = float(m["max_diff_hf"])
        colors = {r"m": SND_C}
        f1 = MathTex(r"\log_{10} \textstyle\sum_k W_{mk}\, |X_k|^2, \quad \text{clipped to 8 decades}", font_size=28,
                     color=SND_C).to_edge(DOWN, buff=0.25)
        exp = int(np.floor(np.log10(max(diff, 1e-12))))
        # one window's spectrum, following the window across the picture
        sax = Axes(x_range=[0, 8000, 1000], y_range=[0, 1.05, 1], x_length=5.4, y_length=1.6, tips=False,
                   axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([3.5, 1.5, 0])
        sxl = label(r"$0$ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ $8$ kHz",
                    font_size=18, color=GREY_B).next_to(sax, DOWN, buff=0.05)
        sll = label(r"one window's spectrum: \ energy at each of the $201$ frequencies, \ dB", font_size=20,
                    color=GREY_A).next_to(sax, UP, buff=0.1)
        fz = np.linspace(0, 8000, P.shape[0])
        win_x = ValueTracker(0.0)

        def column_curve():
            j = int(np.clip(round(win_x.get_value() * (n - 1)), 0, n - 1))
            v = np.clip((P[:, j] - lo) / (P.max() - lo), 0, 1)
            return curve(sax, fz, v, SND_C, 2.0)

        live = always_redraw(column_curve)
        stft = MathTex(r"X_k(t) = \sum_{n=0}^{399} w_n\, x_{160t + n}\, e^{-2\pi i\, k n / 400}", font_size=34,
                       color=WHITE).move_to([0, -1.3, 0])
        stw = label(r"$400$ samples $= 25$ ms; \ hop $160 = 10$ ms; \ $w$: \ the Hann taper; \ "
                    r"$k = 0 \dots 200$", font_size=20, color=GREY_A).next_to(stft, DOWN, buff=0.2)
        with self.voiceover(
            "A wave is hard to read, so speech models look at its spectrum, slice by slice. <bookmark mark='a'/> Cut "
            "the signal into windows of 25 milliseconds, one every 10, taper each with a Hann window and take its "
            "Fourier transform: the short-time Fourier transform, a picture of frequency against time. "
            "<bookmark mark='b'/> The ear hears pitch roughly by ratios, so the frequencies are pooled into bands "
            "evenly spaced on the mel scale: narrow below a kilohertz, wider above. <bookmark mark='c'/> Take the "
            "logarithm of each band's energy, keep the top eight decades, and you have exactly what Whisper hears: "
            "80 log-mel bands every 10 milliseconds. Our own implementation agrees with the transformers library's "
            f"to within ten to the minus {abs(exp)}."
        ) as vo:
            self.play(FadeIn(spec), FadeIn(sl))
            vo.wait_until("a")
            win = Rectangle(width=spec.width * 2.5 / max(n, 1) + 0.04, height=spec.height + 0.1, stroke_color=WHITE,
                            stroke_width=2).move_to(spec.get_left() + RIGHT * 0.05)
            x0_, x1_ = spec.get_left()[0] + 0.05, spec.get_right()[0] - 0.05
            win.add_updater(lambda m_: m_.set_x(x0_ + win_x.get_value() * (x1_ - x0_)))
            self.play(Create(win), FadeIn(sax), FadeIn(sxl), FadeIn(sll), FadeIn(live), FadeIn(stft), FadeIn(stw),
                      run_time=0.8)
            self.play(win_x.animate.set_value(0.45), run_time=5.0, rate_func=linear)
            self.play(win_x.animate.set_value(1.0), run_time=5.0, rate_func=linear)
            win.clear_updaters()
            live.clear_updaters()
            vo.wait_until("b")
            self.play(FadeOut(win), FadeOut(live), FadeOut(sax), FadeOut(sxl), FadeOut(sll), run_time=0.5)
            self.play(FadeIn(fax), FadeIn(fl), FadeIn(fx), LaggedStart(*[Create(t_) for t_ in tri], lag_ratio=0.05),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(FadeOut(stft), FadeOut(stw), run_time=0.5)
            self.play(FadeIn(mel), FadeIn(ml), FadeIn(f1))
        self.wait(0.3)
        self.clear_scene()
