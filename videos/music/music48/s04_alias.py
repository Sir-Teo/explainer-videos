from __future__ import annotations

import numpy as np

from videos.music.music48.common import *  # noqa: F403


class Alias(SoundScene):
    def construct(self):
        chapter(self, 3, r"Aliasing", r"What happens to a frequency the samples cannot hold?")
        self.wheel()
        self.folding()
        self.tones()
        self.quiz()
        self.filters()

    # ------------------------------------------------------------------
    def wheel(self):
        fs = 8.0
        ax = frame_axes(width=11.6, height=3.0, xlo=0, xhi=2.0, ylo=-1.2, yhi=1.2, center=DOWN * 0.2)
        tt = np.linspace(0, 2.0, 800)
        f_hi, f_lo = 7.0, 1.0
        hi = curve(tt, np.sin(2 * np.pi * f_hi * tt), ax.to, color=GREY_A, width=2)
        lo = curve(tt, -np.sin(2 * np.pi * f_lo * tt), ax.to, color=EAR, width=3)
        n = np.arange(0, 17)
        st = stems(n / fs, np.sin(2 * np.pi * f_hi * n / fs), ax.to, color=TUNE)
        head = label(r"a fast wave and a slow one, \ through the same samples", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"grey: \ 7 cycles a second; \ pink: \ 1 cycle, \ reversed; \ dots: \ 8 samples a second", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "What if the signal does contain something above the Nyquist frequency? <bookmark mark='a'/> Here is a wave of "
            "seven cycles a second, sampled eight times a second, so its Nyquist frequency is four. <bookmark mark='b'/> The "
            "samples land as if on a wave of one cycle a second, running backwards. <bookmark mark='c'/> After sampling, the two "
            "are the same list of numbers: the fast wave has taken the slow one's identity. That is aliasing, and it is the "
            "wagon wheel in old films that turns slowly backwards when it is really spinning fast forwards."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(cap))
            vo.wait_until("a")
            self.play(Create(hi), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(st))
            vo.wait_until("c")
            self.play(Create(lo), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def folding(self):
        fs = 8000
        ax = frame_axes(width=9.0, height=3.2, xlo=0, xhi=16000, ylo=0, yhi=4000, center=DOWN * 0.3)
        from explainer.music.monochord import digital as DG
        fin = np.linspace(0, 16000, 400)
        zig = curve(fin, [DG.alias(f, fs) for f in fin], ax.to, color=TUNE, width=4)
        ticks = VGroup(*[label(f"{v // 1000} k", font_size=16, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.15) for v in (0, 4000, 8000, 12000, 16000)],
                       *[label(f"{v // 1000} k", font_size=16, color=GREY_A).next_to(ax.to(0, v), LEFT, buff=0.15) for v in (0, 2000, 4000)])
        xl = label(r"frequency going in, \ Hz", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.6)
        yl = label(r"frequency the samples hold", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.2).align_to(ax, LEFT)
        marks = VGroup()
        for f, col in ((3000, WHITE), (5000, EAR), (7000, BLUE)):
            h = DG.alias(f, fs)
            marks.add(VGroup(DashedLine(ax.to(f, 0), ax.to(f, h), color=col, stroke_width=2), Dot(ax.to(f, h), radius=0.08, color=col),
                             label(rf"{f // 1000} k $\to$ {int(h) // 1000} k", font_size=17, color=col).next_to(ax.to(f, h), UP, buff=0.12)))
        head = label(r"folding at 8 kHz sampling", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Every frequency going in has a frequency it comes out as. <bookmark mark='a'/> Sample at eight thousand a second. "
            "Up to four thousand, the Nyquist frequency, everything comes out as it went in. Above it, the frequency folds back "
            "down, reaches zero at eight thousand, and climbs again: a zigzag, like paper folded at every multiple of four "
            "thousand. <bookmark mark='b'/> Three thousand stays three thousand. Five thousand comes out as three thousand. "
            "Seven thousand comes out as one thousand."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(zig), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.5), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tones(self):
        d = load("tones")
        c = clip("tones.three")
        cells = VGroup()
        for f, h in zip(d["tones"], d["heard"]):
            cells.add(VGroup(RoundedRectangle(width=3.2, height=1.6, corner_radius=0.15, stroke_color=GREY_B),
                             VGroup(label(rf"{f:,} Hz in", font_size=22, color=WHITE), label(rf"{int(h):,} Hz out", font_size=22, color=TUNE if h == f else EAR)).arrange(DOWN, buff=0.25)).arrange(ORIGIN))
        cells.arrange(RIGHT, buff=0.6).move_to(UP * 0.2)
        cap = label(r"each tone first as it is, \ then sampled at 8 kHz with no filter", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"three tones, \ sampled at 8 kHz", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear it. Each tone first as it is, then after sampling at eight thousand a second with no filter, and rebuilding."):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        each = d["each"]
        with self.listen(c) as snd:
            window(snd, r"three tones", kind="synthesized", detail=r"sine tones, \ sampled", corner=DL, tag_corner=DR)
            for i, k in enumerate(("3000", "5000", "7000")):
                pulse(snd, cells[i][1][0], st[k], st[k] + 1.2, buff=0.06)
                pulse(snd, cells[i][1][1], st[k] + each, st[k] + each + 1.2, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("alias")
        c = clip("alias.two")
        card = listen_card(r"A sine sweeping up from 200 Hz to 12,000 Hz, \ sampled at 8,000 a second, \ twice: \ once with a filter in "
                           r"front of the sampler, \ once without. \ In which does the pitch turn round?", width=10.4)
        with self.voiceover(
            "Now a question. A sine sweeping up from two hundred to twelve thousand hertz, sampled at eight thousand a second, "
            "twice: once with a filter in front of the sampler, and once without. In which does the pitch turn round?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        ts = np.array(d["track_t"])
        def panel(track, color, title):
            ax = frame_axes(width=5.2, height=2.4, xlo=0, xhi=d["seconds"], ylo=0, yhi=12000, center=ORIGIN)
            ins = curve(ts, d["track_in"], ax.to, color=GREY_B, width=1.5)
            ys = [v for v in track]
            pts = [(t, v) for t, v in zip(ts, ys) if v is not None]
            out = curve([p[0] for p in pts], [p[1] for p in pts], ax.to, color=color, width=4)
            ny = DashedLine(ax.to(0, 4000), ax.to(d["seconds"], 4000), color=WHITE, stroke_width=1.2, stroke_opacity=0.6)
            return VGroup(ax, ny, ins, out, label(title, font_size=19, color=color).next_to(ax, UP, buff=0.15))
        a = panel(d["track_raw"], EAR, r"first")
        b = panel(d["track_filtered"], TUNE, r"second")
        g = VGroup(a, b).arrange(RIGHT, buff=1.0).move_to(UP * 0.2)
        cap = label(r"grey: \ the sweep going in; \ coloured: \ what comes out; \ dashed: \ 4 kHz, \ the Nyquist frequency", font_size=16, color=GREY_A).to_edge(DOWN, buff=1.0)
        self.play(FadeOut(card), FadeIn(VGroup(a[0], a[1], a[4], b[0], b[1], b[4])), FadeIn(cap))
        st = d["starts"]
        sec = d["seconds"]
        cur_a = Dot(radius=0.08, color=WHITE)
        cur_b = Dot(radius=0.08, color=WHITE)
        with self.listen(c) as snd:
            window(snd, r"a sweep, \ twice", kind="synthesized", detail=r"a sine, \ sampled at 8 kHz", corner=DL, tag_corner=DR)
            snd.show(cur_a)
            snd.show(cur_b)
            from explainer.music.monochord import digital as DG
            def mover(axg, start, filtered):
                def fn(m, t):
                    u = min(max(t - start, 0.0), sec)
                    f = d["f0"] + (d["f1"] - d["f0"]) * u / sec
                    h = (f if f < 3800 else 0.0) if filtered else DG.alias(f, d["fs"])
                    m.move_to(axg.to(u, h))
                    m.set_opacity(1.0 if (start <= t <= start + sec and (not filtered or f < 3800)) else 0.0)
                return fn
            snd.drive(cur_a, mover(a[0], st["first"], False))
            snd.drive(cur_b, mover(b[0], st["second"], True))
        with self.voiceover(
            "The first. Without a filter, the sweep climbs to four thousand, then folds back down to zero at eight thousand, "
            "and climbs again: the pitch turns round twice. With the filter, the sweep simply fades out at the Nyquist "
            "frequency. Nothing above it reaches the sampler, so nothing can fold."
        ):
            self.play(FadeIn(a[2]), Create(a[3]), FadeIn(b[2]), Create(b[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def filters(self):
        items = [
            (r"so every converter puts a low-pass filter before the sampler: \ the anti-aliasing filter", WHITE),
            (r"it must pass everything up to 20,000 Hz and stop everything above 22,050: \ a steep cliff", WHITE),
            (r"early CD players and recorders used steep analogue filters, \ with ringing and phase shift near the top", WHITE),
            (r"modern converters sample far faster, \ filter digitally, \ then reduce the rate: \ chapter 8", TUNE),
            (r"aliasing is not only a converter's problem: \ any processing that makes new high frequencies can fold them", GREY_A),
        ]
        rows_scene(self, r"the anti-aliasing filter", items,
                   "So every converter puts a low-pass filter in front of the sampler: the anti-aliasing filter. "
                   "<bookmark mark='b'/> At forty-four thousand one hundred it must pass everything up to twenty thousand hertz "
                   "and stop everything above twenty-two thousand and fifty: a steep cliff. <bookmark mark='c'/> Early CD players "
                   "and recorders used steep analogue filters, with ringing and phase shift near the top. <bookmark mark='d'/> "
                   "Modern converters sample far faster, filter digitally, and then reduce the rate, as chapter eight shows. "
                   "<bookmark mark='e'/> And aliasing is not only a converter's problem: any processing that creates new high "
                   "frequencies, distortion for one, can fold them back down.", marks="bcde")
