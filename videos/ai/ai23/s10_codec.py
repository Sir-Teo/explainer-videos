from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import ACOU_C, PART, SEM_C, SND_C, TOKEN_COLORS, code_grid, curve, load, node_box, spectro


def wave_m(y, color, width=2.0, w=2.0, h=0.55):
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [[-w / 2 + w * i / (len(y) - 1), h * float(v), 0] for i, v in enumerate(y)])


class Codec(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.ours()
        self.results()
        self.semantic()

    def card(self):
        card = chapter_card(9, r"Neural codecs", r"How few numbers can carry a voice?", part=PART)
        with self.voiceover("Chapter nine. Neural codecs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def history(self):
        d = load("codec")
        seg = np.sin(np.linspace(0, 9 * np.pi, 90)) * np.exp(-np.linspace(-1, 1, 90) ** 2)
        w_in = wave_m(seg, GREY_A)
        enc = node_box(r"encoder", SND_C, font_size=22)
        q = node_box(r"residual VQ", C.INTERVAL, font_size=22)
        dec = node_box(r"decoder", SND_C, font_size=22)
        w_out = wave_m(0.9 * seg, SND_C)
        pipe = VGroup(w_in, enc, q, dec, w_out).arrange(RIGHT, buff=0.7).move_to(UP * 1.9)
        arrs = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, stroke_width=2.5, color=GREY_B,
                              max_tip_length_to_length_ratio=0.3) for a, b in zip(pipe, pipe[1:])])
        tag = note(r"schematic", font_size=18).next_to(pipe, UP, buff=0.15).align_to(pipe, RIGHT)
        # bitrates on a log scale
        rates = [(r"CD audio", 1411_200, GREY_B), (r"telephone (G.711)", 64_000, GREY_B),
                 (r"$16$ kHz, $16$-bit samples", int(d["pcm_bps"]), GREY_B), (r"EnCodec", 24_000, ACOU_C),
                 (r"EnCodec, lowest", 1_500, ACOU_C), (r"Mimi (Moshi)", 1_100, SEM_C),
                 (r"Qwen3-TTS's tokenizer$^*$", 2_200, SEM_C)]
        order = [0, 2, 1, 3, 4, 6, 5]  # CD, 16 kHz PCM, telephone; EnCodec's two ends; then the speech tokenizers
        rates = [rates[i] for i in order]
        lax = VGroup()
        x0, x1 = -5.0, 3.0
        lo, hi = math.log10(500), math.log10(2e6)

        def X(v):
            return x0 + (x1 - x0) * (math.log10(v) - lo) / (hi - lo)

        lax.add(Line([x0, -2.9, 0], [x1, -2.9, 0], color=GREY_C, stroke_width=1.5))
        for v in (1e3, 1e4, 1e5, 1e6):
            lax.add(Line([X(v), -2.95, 0], [X(v), -2.85, 0], color=GREY_C))
            lax.add(MathTex(rf"10^{{{int(math.log10(v))}}}", font_size=20, color=GREY_B).move_to([X(v), -3.2, 0]))
        lax.add(label(r"bits a second", font_size=20, color=GREY_B).move_to([x1 + 1.3, -2.9, 0]))
        bars = VGroup()
        for i, (nm, v, col) in enumerate(rates):
            y = 0.35 - 0.42 * i
            bar = Rectangle(width=X(v) - x0, height=0.28, stroke_width=0, fill_color=col, fill_opacity=0.55)
            bar.move_to([x0 + (X(v) - x0) / 2, y, 0])
            bars.add(VGroup(bar, label(nm + rf": \ ${v / 1000:g}$ kbps", font_size=18, color=col).next_to(bar, RIGHT, buff=0.12)))
        cite_ = cite(r"N.~Zeghidour et al., \textit{SoundStream} (2021); \ A.~D\'efossez et al., \textit{EnCodec} (2022)", corner=DR)
        star = note(r"$^*$ $12.5$ frames/s $\times$ $16$ codes $\times$ $11$ bits, \ from its configuration", font_size=16)
        star.to_corner(UR, buff=0.3)
        with self.voiceover(
            "For most of a century digital sound meant samples: the telephone's 64 thousand bits a second, a CD's "
            "1.4 million. <bookmark mark='a'/> In 2021 Neil Zeghidour and colleagues at Google learned a codec end to "
            "end. SoundStream's encoder turns the wave into seventy-five vectors a second, residual vector "
            "quantization turns each into a handful of code numbers, and a decoder turns codes back into a wave, all "
            "trained together, with a spectral loss and a GAN's judge. <bookmark mark='b'/> They also dropped "
            "quantizer stages at random during training, so one model works at every bitrate. Meta's EnCodec, in "
            "2022, runs from 1.5 to 24 kilobits a second. <bookmark mark='c'/> The tokenizers of today's speech "
            "models go lower still: one or two kilobits."
        ) as vo:
            self.play(FadeIn(lax), LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.1) for b_ in bars[:3]], lag_ratio=0.3),
                      run_time=1.5)
            vo.wait_until("a")
            self.play(Create(w_in), FadeIn(tag), FadeIn(cite_))
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(m)) for a, m in zip(arrs, pipe[1:])], lag_ratio=0.5),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.1) for b_ in bars[3:5]], lag_ratio=0.3))  # EnCodec
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.1) for b_ in bars[5:]], lag_ratio=0.3), FadeIn(star))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        d = load("codec")
        hz, bits = int(d["hz"]), int(d["bits"])
        stages = [int(s) for s in d["stages"]]
        snaps = np.asarray(d["snaps"])
        steps = [int(s) for s in d["snap_steps"]]
        lo, hi = float(np.asarray(d["ex_orig"]).min()), float(np.asarray(d["ex_orig"]).max())
        W, H = 6.0, 2.0
        orig = spectro(np.asarray(d["ex_orig"]), W, H, lo=lo, hi=hi).move_to([3.3, 1.6, 0])
        ol = label(r"a held-out voice: \ the original log-mel picture", font_size=20, color=GREY_A).next_to(orig, UP, buff=0.1)

        def snap(k):
            return spectro(snaps[k], W, H, lo=lo, hi=hi).move_to([3.3, -1.6, 0])

        cur = snap(0)
        t = ValueTracker(0)
        cnt = always_redraw(lambda: label(rf"rebuilt from $8$ stages, \ after ${int(t.get_value()):,}$ steps".replace(",", "{,}"),
                                          font_size=20, color=SND_C).next_to(cur, UP, buff=0.1))
        rows = [MathTex(rf"\frac{{100 \text{{ mel frames/s}}}}{{2}} = {hz} \text{{ code frames/s}}", font_size=30),
                MathTex(rf"{hz} \times n \times \log_2 {2 ** bits} = {hz * bits}\, n \text{{ bits/s}}", font_size=30),
                MathTex(rf"n = 1, 2, 4, 8: \ {', '.join(str(hz * bits * n) for n in stages)} \text{{ bits/s}}", font_size=28,
                        color=C.INTERVAL)]
        whys = [why(r"one strided convolution", font_size=20), why(r"$n$ stages of $256$ codes", font_size=20),
                why(r"one model, \ quantizer dropout", font_size=20)]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-3.4, align_index=None, buff=0.75, edge=-0.1)
        tr_min = float(d["train_seconds"]) / 60
        S = int(d["steps"])
        params = int(d["params"])
        with self.voiceover(
            "We built a small one, with one simplification. Teaching a network to make a wave takes far more compute "
            "than this computer has, so ours codes the picture Whisper reads, the log-mel spectrogram of chapter "
            "eight, and leaves turning a picture back into sound to a vocoder. <bookmark mark='a'/> A strided "
            f"convolution takes the picture's 100 frames a second down to {hz}. <bookmark mark='b'/> Each frame passes through up to eight "
            f"residual stages of 256 codes, eight bits each, so a stage costs {hz * bits} bits a second. "
            "<bookmark mark='c'/> Stages are dropped at random in training, so the same model runs at "
            f"{', '.join(str(hz * bits * n) for n in stages[:-1])} or {hz * bits * stages[-1]:,} bits a second. "
            f"<bookmark mark='d'/> It has {params / 1e3:.0f} thousand parameters and trained for {S:,} steps on "
            f"{tr_min:.0f} minutes of Kokoro speech in ten voices, with a plain loss: the average error in the "
            "rebuilt picture. Here it learns "
            "to rebuild a sentence from a voice it never heard."
        ) as vo:
            self.play(FadeIn(orig), FadeIn(ol))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            step(2, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(cur))
            self.add(cnt)
            for k in range(1, len(steps)):
                nxt = snap(k)
                self.play(FadeTransform(cur, nxt), t.animate.set_value(steps[k]), run_time=1.0)
                cur = nxt
        self.wait(0.3)
        self.remove(cnt)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        d = load("codec")
        hz, bits = int(d["hz"]), int(d["bits"])
        stages = [int(s) for s in d["stages"]]
        seeds = [int(s) for s in d["seeds"]]
        lo, hi = float(np.asarray(d["ex_orig"]).min()), float(np.asarray(d["ex_orig"]).max())
        W, H = 3.0, 1.2
        imgs = Group(spectro(np.asarray(d["ex_orig"]), W, H, lo=lo, hi=hi),
                     *[spectro(np.asarray(d[f"ex_rec{n}"]), W, H, lo=lo, hi=hi) for n in stages])
        labs = [r"original"] + [rf"${hz * bits * n:,}$ bits/s".replace(",", "{,}") for n in stages]
        tiles = Group(*[Group(im, label(l_, font_size=18, color=GREY_A if i == 0 else SND_C).next_to(im, UP, buff=0.06))
                        for i, (im, l_) in enumerate(zip(imgs, labs))])
        tiles.arrange_in_grid(rows=1, cols=5, buff=0.18).move_to(UP * 2.2)
        if tiles.width > 13.2:
            tiles.width = 13.2
        bps = [hz * bits * n for n in stages]
        wer = np.array([[float(d[f"wer_s{s}_{n}"]) for n in stages] for s in seeds])
        mel = np.array([[float(d[f"mel_s{s}_{n}"]) for n in stages] for s in seeds])
        ax = axes([math.log10(bps[0]) - 0.15, math.log10(bps[-1]) + 0.15, 0.3], [0, max(1.0, float(wer.max()) * 1.1), 0.25],
                  x_length=5.2, y_length=3.0, xlabel=r"bits a second", ylabel=r"Whisper's word error rate",
                  xticks=[math.log10(b) for b in bps], xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"),
                  yticks=[0, 0.5, 1.0], yfmt=lambda v: f"{int(round(100 * v))}\\%", center=[-3.2, -1.3, 0])
        lines = VGroup()
        for s in range(len(seeds)):
            lines.add(curve(ax.ax, [math.log10(b) for b in bps], wer[s], SND_C, 2.5))
            lines.add(VGroup(*[Dot(ax.ax.c2p(math.log10(b), w), radius=0.06, color=SND_C) for b, w in zip(bps, wer[s])]))
        ow = float(d["orig_wer"])
        base = DashedLine(ax.ax.c2p(math.log10(bps[0]) - 0.15, ow), ax.ax.c2p(math.log10(bps[-1]) + 0.15, ow), color=WHITE)
        bl = label(rf"the original picture: \ ${100 * ow:.0f}\%$", font_size=18, color=WHITE).next_to(base, UP, buff=0.05).align_to(base, RIGHT)
        ex = VGroup(label(r"heard by Whisper, \ seed $0$:", font_size=20, color=GREY_A))
        refs = [str(r) for r in d["refs"]]
        for n in (stages[0], stages[-1]):
            hyp = str(d[f"hyps_s{seeds[0]}_{n}"][0])
            ex.add(VGroup(label(rf"${hz * bits * n:,}$:".replace(",", "{,}"), font_size=18, color=SND_C),
                          data_text(hyp[:58], font="DejaVu Sans", font_size=18, color=WHITE)).arrange(RIGHT, buff=0.15))
        ex.add(VGroup(label(r"said:", font_size=18, color=GREY_A),
                      data_text(refs[0][:58], font="DejaVu Sans", font_size=18, color=GREY_A)).arrange(RIGHT, buff=0.15))
        ex.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.4, -1.2, 0])
        if ex.width > 6.6:
            ex.width = 6.6
        w_lo, w_hi = wer.mean(0)[0], wer.mean(0)[-1]
        trend = ("falls" if w_hi < w_lo - 0.02 else "barely changes")
        ratio = int(d["mel_bps"]) / bps[-1]
        pcm = int(d["pcm_bps"]) / bps[-1]
        n_w = int(d["n_wer"])
        with self.voiceover(
            "How good is it? <bookmark mark='a'/> Here is the held-out sentence rebuilt at each bitrate: one stage "
            "keeps the rough shape, eight keep much more of the detail. <bookmark mark='b'/> A blunt but fair "
            f"test: Whisper reads such pictures directly, so can it still understand ours? On {n_w} held-out "
            f"sentences, Whisper's word error rate {trend} "
            f"from {100 * w_lo:.0f} percent at {bps[0]} bits a second to {100 * w_hi:.0f} percent at {bps[-1]:,}, "
            f"against {100 * ow:.0f} percent on the original picture; two seeds. <bookmark mark='c'/> At {bps[-1]:,} "
            f"bits a second the codes are {ratio:.0f} times smaller than the picture stored as 32-bit numbers, and "
            f"{pcm:.0f} times smaller than the samples themselves. A real codec must also make the wave, with a GAN's "
            "judge, far more data and far more steps; ours only has to show the trade."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tiles], lag_ratio=0.25), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(ax), Create(base), FadeIn(bl))
            self.play(LaggedStart(*[Create(l_) if isinstance(l_, VMobject) and not isinstance(l_, VGroup) else FadeIn(l_)
                                    for l_ in lines], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(ex))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def semantic(self):
        d = load("codec")
        codes = np.asarray(d["ex_codes"]).T  # stages x frames
        grid = code_grid(codes[:, :60], cell=0.15, K=256).move_to([-3.2, 1.5, 0])
        gl = label(rf"our codec's codes for the sentence: \ $8$ stages $\times$ ${int(d['hz'])}$ frames a second",
                   font_size=20, color=GREY_A).next_to(grid, UP, buff=0.15)
        stl = VGroup(label(r"stage $1$", font_size=16, color=GREY_B).next_to(grid, LEFT, buff=0.1).align_to(grid, UP),
                     label(r"stage $8$", font_size=16, color=GREY_B).next_to(grid, LEFT, buff=0.1).align_to(grid, DOWN))
        ppl = [float(x) for x in d["perplexity"]]
        spread = "fairly evenly" if min(ppl) > 0.5 * max(ppl) else "unevenly"
        pb = VGroup(*[Rectangle(width=0.4, height=1.6 * p / 256, stroke_width=0, fill_color=C.INTERVAL, fill_opacity=0.7)
                      for p in ppl]).arrange(RIGHT, buff=0.1, aligned_edge=DOWN).move_to([-3.2, -1.3, 0])
        pbl = label(r"perplexity of each stage's codes, \ of $256$", font_size=18, color=GREY_A).next_to(pb, UP, buff=0.15)
        pbn = VGroup(*[MathTex(f"{p:.0f}", font_size=16, color=GREY_A).next_to(b_, UP, buff=0.05) for p, b_ in zip(ppl, pb)])
        two = VGroup(
            node_box(r"semantic tokens: \ what is said \\ (from a self-supervised speech model)", SEM_C, font_size=20),
            node_box(r"acoustic tokens: \ how it sounds \\ (from a codec)", ACOU_C, font_size=20)).arrange(DOWN, buff=0.25)
        two.move_to([3.4, 1.6, 0])
        facts = VGroup(*[label(t, font_size=19, color=c_) for t, c_ in (
            (r"AudioLM (2022): \ semantic tokens first, \ then acoustic", GREY_A),
            (r"Mimi (Kyutai, 2024): \ $24$ kHz, \ $12.5$ frames/s, \ $8$ codebooks of $2{,}048$: \ $1.1$ kbps; \\ "
             r"the first distilled from WavLM, \ a self-supervised model", SEM_C),
            (r"Qwen3-TTS's tokenizer (2026): \ $12.5$ frames/s, \ $16$ codebooks of $2{,}048$; \\ the first taught by "
             r"WavLM, \ $15$ acoustic", SEM_C))]).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.3, -1.3, 0])
        with self.voiceover(
            "Speech tokens come in two kinds. <bookmark mark='a'/> A codec's acoustic tokens carry how the speech "
            "sounds: the voice, the room, the detail. Our codec uses its stages "
            f"{spread}: perplexities from "
            f"{min(ppl):.0f} to {max(ppl):.0f} of 256. <bookmark mark='b'/> Semantic tokens carry what is said, and "
            "they come from a self-supervised speech model, the kind Part 24 builds, clustered into codes. In 2022 "
            "Google's AudioLM generated speech by writing semantic tokens first and acoustic tokens after them. "
            "<bookmark mark='c'/> Then the two were merged into one codec: Kyutai's Mimi teaches its first codebook "
            "to match the self-supervised model WavLM, and keeps seven acoustic stages beside it, at 12.5 frames a "
            "second and 1.1 kilobits. The narrator's own tokenizer, Qwen3-TTS's, does the same with sixteen."
        ) as vo:
            self.play(FadeIn(gl), FadeIn(grid), FadeIn(stl))
            vo.wait_until("a")
            self.play(FadeIn(two[1]), FadeIn(pbl), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in pb], lag_ratio=0.1), FadeIn(pbn))
            vo.wait_until("b")
            self.play(FadeIn(two[0]), FadeIn(facts[0]))
            vo.wait_until("c")
            self.play(FadeIn(facts[1:]))
        self.wait(0.3)
        self.clear_scene()
