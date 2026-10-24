from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import (CLIP_C, IMG_C, LM_COLORS, PART, SND_C, TEXT_C, VQ_COLORS, curve, heat, load,
                                   node_box, tile_frame)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0
        out = []

        def small_axes(xr, yr):
            return Axes(x_range=xr, y_range=yr, x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                        axis_config={"stroke_color": GREY_D, "include_ticks": False})

        b = load("bpe")
        L = np.asarray(b["length"], float)
        ax = small_axes([0, len(L) - 1, 10], [0, L.max() * 1.05, 1e6])
        out.append((VGroup(ax, curve(ax, np.arange(len(L)), L, TEXT_C, 3)), r"merges as compression", TEXT_C))
        d = load("lms")
        names = [str(n) for n in d["configs"]]
        vals = [float(np.mean(d[f"bpc_{n}"])) for n in names]
        bars = VGroup(*[Rectangle(width=0.4, height=1.5 * v / max(vals), stroke_width=0, fill_color=LM_COLORS[n], fill_opacity=0.8)
                        for n, v in zip(names, vals)]).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        out.append((bars, r"bits per character, \ $5$ tokenizers", TEXT_C))
        p = load("patches")
        H = np.nan_to_num(np.asarray(p["example_H"], float))[:40]
        th = float(p["threshold"])
        hb = VGroup(*[Rectangle(width=0.06, height=max(0.02, 0.3 * h), stroke_width=0, fill_color=C.CONTEXT if h > th else GREY_C,
                                fill_opacity=0.9) for h in H]).arrange(RIGHT, buff=0.01, aligned_edge=DOWN)
        out.append((hb, r"entropy patches", C.CONTEXT))
        v = load("vqtrain")
        checks = [int(c) for c in v["checks"]]
        ax2 = small_axes([0, checks[-1], 500], [0, 260, 64])
        g = VGroup(ax2)
        for m in ("vq", "ema", "restart"):
            g.add(curve(ax2, checks, np.asarray(v[f"used_t_{m}"], float).mean(0), VQ_COLORS[m], 3))
        out.append((g, r"codebook collapse, \ and restarts", IMG_C))
        q = load("nyquist")
        ax3 = small_axes([0, 16, 4], [0, 4.5, 1])
        out.append((VGroup(ax3, curve(ax3, np.asarray(q["true"]) / 1000, np.asarray(q["seen"]) / 1000, SND_C, 3)),
                    r"aliasing", SND_C))
        cd = load("codec")
        st = [int(s) for s in cd["stages"]]
        wer = [float(np.mean([cd[f"wer_s{s}_{n}"] for s in cd["seeds"]])) for n in st]
        ax4 = small_axes([0, len(st) - 1, 1], [0, max(1.0, max(wer)), 0.5])
        out.append((VGroup(ax4, curve(ax4, np.arange(len(st)), wer, SND_C, 3)), r"a codec, \ $0.4$ to $3.2$ kbps", SND_C))
        c = load("ctc")
        G = np.asarray(c["lat_gamma"]).T
        out.append((heat(np.sqrt(np.clip(G, 0, 1)), 2.9, 1.7, color=SND_C, lo=0, hi=1), r"CTC's lattice", SND_C))
        cl = load("clip")
        out.append((heat(np.asarray(cl["sim_clip"]), 1.8, 1.8, signed=True), r"pictures meet words", CLIP_C))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = tile_frame(cap, col, TW, TH)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(rf"Part {PART}, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Byte-pair encoding cuts text by merging the commonest pairs, a greedy compressor; the "
            "unigram model puts a probability on every cut; and bits per character is the fair way to compare them. "
            "Bytes and entropy patches spend a model's effort where the surprise is. Pictures and sound become "
            "tokens through codebooks, which collapse unless they are restarted, or replaced by a fixed grid, and "
            "residual stages make codecs that carry speech in a few hundred bits a second. Sampling folds what is "
            "too fast back into the band; spectra and the mel scale are what recognizers hear. CTC learns to "
            "transcribe without alignments by summing over a lattice, Whisper learns from the web, and speech "
            "synthesis became language modelling over codec tokens. Contrastive training puts pictures and words in "
            "one space, and with everything as tokens, one model can see, listen and speak at once."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"self-supervised encoders: \ wav2vec, \ HuBERT, \ DINO", [24]),
            (r"thinking in tokens", [28]),
            (r"actions and video frames as tokens", [29]),
            (r"what the tokens mean inside a model", [30]),
            (r"tokenizer quirks in benchmarks; \ cloned voices", [31]),
        ], font_size=26)
        with self.voiceover(
            "All of this comes back. The self-supervised speech and image encoders that semantic tokens and "
            "vision-language models are built on are the next part, Part 24. Reasoning models think in tokens, in "
            "Part 28. Robots and world models write actions and video frames as tokens, in Part 29. What the tokens "
            "come to mean inside a model is Part 30. And the quirks of tokenizers in benchmarks, and voices cloned "
            "from three seconds of speech, come back in the last part, on trust."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"Show that a BPE merge of a pair found $n$ times (without overlaps) shortens the text by exactly $n$ "
            r"symbols. \ In ``aaaa'', how often does the pair (a, a) occur, \ and how many merges does it allow?",
            r"One model pays $9.6$ bits per token with $3.2$ characters a token; \ another $2.9$ bits per byte on "
            r"plain bytes. \ Which is better per character? \ Show that per-character perplexity is per-token "
            r"perplexity to the power $1/(\text{characters per token})$.",
            r"How many codes do FSQ levels $(8, 5, 5, 5)$ give, \ and how many bits? \ What bitrate do $8$ residual "
            r"stages of $1{,}024$ codes give at $75$ frames a second?",
            r"Show that $\cos(2\pi f t)$ and $\cos(2\pi (f_s - f) t)$ agree at every $t = n / f_s$. \ Sampled at "
            r"$16$ kHz, \ where does a $9$ kHz tone appear?",
            r"List every path of $T = 3$ frames over $\{a, b, \varnothing\}$ that collapses to ``ab'', \ and check the "
            r"count with the forward recursion. \ Why must every path for ``aa'' contain a blank?",
            r"Show that $f^*(x, y) = \log p(y \mid x) / p(y)$ minimizes InfoNCE, \ and that "
            r"$\log N - \mathcal L \le \log N$ for any critic. \ How much information can a batch of $256$ certify?",
        ], font_size=22)
        with self.voiceover(
            "Here are six problems, from counting merges to the information a batch can certify. Pause here, and "
            "work through them; full solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 24, \ Learning Without Labels", font_size=40).to_edge(UP, buff=0.5)
        x = Square(1.2, stroke_color=GREY_B, stroke_width=2).move_to([-4.6, 0.0, 0])
        xl = label(r"one input", font_size=20, color=GREY_A).next_to(x, DOWN, buff=0.15)
        v1 = Square(0.9, stroke_color=TEXT_C, stroke_width=2).move_to([-2.2, 1.0, 0]).rotate(0.2)
        v2 = Square(0.9, stroke_color=TEXT_C, stroke_width=2).move_to([-2.2, -1.0, 0]).rotate(-0.25)
        vl = label(r"two views", font_size=20, color=TEXT_C).next_to(v2, DOWN, buff=0.15)
        enc = node_box(r"encoder", WHITE, font_size=24).move_to([0.6, 0.0, 0])
        sph = Circle(radius=1.2, color=GREY_B).move_to([4.0, 0.0, 0])
        d1 = Dot(sph.point_at_angle(1.0), color=TEXT_C, radius=0.1)
        d2 = Dot(sph.point_at_angle(1.25), color=TEXT_C, radius=0.1)
        others = VGroup(*[Dot(sph.point_at_angle(a), color=GREY_C, radius=0.08) for a in (2.6, 3.5, 4.6, 5.6)])
        sl = label(r"pulled together; \ the rest pushed apart", font_size=20, color=GREY_A).next_to(sph, DOWN, buff=0.2)
        arrs = VGroup(Arrow(x.get_right(), v1.get_left(), buff=0.1, color=GREY_B), Arrow(x.get_right(), v2.get_left(), buff=0.1, color=GREY_B),
                      Arrow(v1.get_right(), enc.get_left(), buff=0.1, color=GREY_B), Arrow(v2.get_right(), enc.get_left(), buff=0.1, color=GREY_B),
                      Arrow(enc.get_right(), sph.get_left(), buff=0.1, color=GREY_B))
        tag = note(r"schematic", font_size=18).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Next time: where encoders like wav2vec 2.0 and DINO come from, when nobody labels anything. Two "
            "views of one input, pulled together, everything else pushed apart, and the other ways to learn from "
            "data alone: learning without labels, Part 24."
        ) as vo:
            self.play(FadeIn(head), FadeIn(x), FadeIn(xl), FadeIn(tag))
            self.play(GrowArrow(arrs[0]), GrowArrow(arrs[1]), FadeIn(v1), FadeIn(v2), FadeIn(vl))
            self.play(GrowArrow(arrs[2]), GrowArrow(arrs[3]), FadeIn(enc), GrowArrow(arrs[4]), Create(sph), FadeIn(others),
                      FadeIn(d1), FadeIn(d2), FadeIn(sl), run_time=max(2.0, vo.duration - 3.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        card = reference_card(
            [r"D.~Jurafsky \& J.~H.~Martin, \textit{Speech and Language Processing}, 3rd ed.\ draft: \ tokenization, \ "
             r"ASR, \ TTS",
             r"L.~Rabiner \& B.-H.~Juang, \textit{Fundamentals of Speech Recognition} (1993); \ P.~Taylor, "
             r"\textit{Text-to-Speech Synthesis} (2009)"],
            [r"Gage (1994); \ Schuster \& Nakajima (2012); \ Sennrich, Haddow \& Birch (2016); \ Kudo (2018); \ Kudo \& "
             r"Richardson (2018); \ Radford et al.\ (2019); \ Xue et al., ByT5 (2021); \ Yu et al., MegaByte (2023); \ "
             r"Pagnoni et al., BLT (2024)",
             r"van den Oord et al., VQ-VAE (2017); \ Razavi et al.\ (2019); \ Mentzer et al., FSQ (2023); \ Yu et al., "
             r"MAGVIT-v2 (2023)",
             r"Nyquist (1928); \ Shannon (1949); \ Zeghidour et al., SoundStream (2021); \ D\'efossez et al., EnCodec "
             r"(2022); \ Borsos et al., AudioLM (2022); \ D\'efossez et al., Moshi and Mimi (2024)",
             r"Davis, Biddulph \& Balashek (1952); \ Vintsyuk (1968); \ Sakoe \& Chiba (1978); \ Baker (1975); \ Jelinek "
             r"(1976); \ Rabiner (1989); \ Hinton et al.\ (2012); \ Graves et al., CTC (2006); \ Hannun et al., Deep "
             r"Speech (2014)",
             r"Baevski et al., wav2vec 2.0 (2020); \ Radford et al., Whisper (2022); \ Qwen Team, Qwen3-ASR (2026)",
             r"Dudley (1939); \ Klatt (1980); \ Hunt \& Black (1996); \ van den Oord et al., WaveNet (2016); \ Shen et al., "
             r"Tacotron 2 (2017); \ Wang et al., VALL-E (2023); \ Qwen Team, Qwen3-TTS (2026)",
             r"Vinyals et al.\ (2015); \ Radford et al., CLIP (2021); \ Zhai et al., SigLIP (2023); \ Alayrac et al., "
             r"Flamingo (2022); \ Li et al., BLIP-2 (2023); \ Liu et al., LLaVA (2023); \ Wang et al., Qwen2-VL (2024)",
             r"Chameleon Team (2024); \ Qwen Team, Qwen2.5-Omni (2025), Qwen3-Omni (2025), Qwen3-VL (2025), "
             r"Qwen3.5-Omni (2026); \ Roy et al., PersonaPlex (2026)"])
        credit = note(narration_credit(), font_size=18).to_edge(DOWN, buff=0.15)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.1:
            card.shift(UP * (credit.get_top()[1] + 0.1 - card.get_bottom()[1]))
        with self.voiceover(
            "Jurafsky and Martin's Speech and Language Processing is the place to go deeper: tokenization, "
            "recognition and synthesis are all in it. Thanks for watching, and see you in Part 24."
        ):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(1.5)
        self.clear_scene()
