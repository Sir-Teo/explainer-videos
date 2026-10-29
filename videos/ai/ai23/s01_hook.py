from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import IMG_C, PART, SND_C, TEXT_C, gray_image, heat, load, token_chips


class Hook(VoiceoverScene):
    def construct(self):
        self.converge()
        self.question()
        self.plan()

    # ------------------------------------------------------------------
    def converge(self):
        b, v, s = load("bpe"), load("codebooks"), load("speech")
        sz = [int(n) for n in b["sizes"]]
        cut = [str(x) for x in b[f"cut{sz[min(1, len(sz) - 1)]}"]][:8]
        text = token_chips(cut, font_size=28, height=0.5).move_to([-2.2, 2.5, 0])
        # the picture, as 25 patches of 4 x 4 pixels laid exactly over it
        img = np.asarray(v["image"])
        P, n = 1.8 / 5, 5
        c_pic = np.array([-4.2, 0.1, 0])
        patches = Group(*[gray_image(img[4 * r:4 * r + 4, 4 * c:4 * c + 4], P).move_to(c_pic + np.array([(c - 2) * P, (2 - r) * P, 0]))
                          for r in range(n) for c in range(n)])
        # the sound: a held-out voice's sentence as a log-mel spectrogram, in 8 slices
        spec = np.asarray(s["hook_mel"])[::-1]
        k, sw = 8, 0.55
        c_snd = np.array([1.8, 0.1, 0])
        cols = np.array_split(np.arange(spec.shape[1]), k)
        slices = Group(*[heat(spec[:, ix], sw, 1.8, color=SND_C, lo=spec.min(), hi=spec.max(), smooth=True)
                         .move_to(c_snd + np.array([(j - (k - 1) / 2) * sw, 0, 0])) for j, ix in enumerate(cols)])
        labs = VGroup(label(r"text", font_size=26, color=TEXT_C).next_to(text, LEFT, buff=0.3),
                      label(r"a picture", font_size=26, color=IMG_C).next_to(patches, UP, buff=0.25),
                      label(r"a voice", font_size=26, color=SND_C).next_to(slices, UP, buff=0.25))
        picks = [6, 7, 8, 11, 12, 13, 16, 17, 18]  # the middle of the letter
        kinds = [TEXT_C] * len(text) + [IMG_C] * len(picks) + [SND_C] * k
        q = 0.42
        seq = VGroup(*[Square(q, stroke_color=c_, stroke_width=2, fill_color=c_, fill_opacity=0.35) for c_ in kinds])
        seq.arrange(RIGHT, buff=0.06).move_to([0, -2.6, 0])
        sl = label(r"one sequence of tokens", font_size=26, color=WHITE).next_to(seq, DOWN, buff=0.25)
        with self.voiceover(
            "A transformer reads a sequence of tokens. So how does a model look at a picture, or listen to a voice? "
            "<bookmark mark='a'/> Everything is turned into tokens first: text into pieces of words, a picture into "
            "codes for its patches, sound into codes for slices of time. <bookmark mark='b'/> Then it's all one "
            "sequence, and one model can read it, and write it."
        ) as vo:
            self.play(FadeIn(text), FadeIn(patches), FadeIn(slices), FadeIn(labs), run_time=1.5)
            vo.wait_until("a")
            self.play(text.animate.arrange(RIGHT, buff=0.22, center=False),
                      *[p_.animate.shift((p_.get_center() - c_pic) * 0.35) for p_ in patches],
                      *[q_.animate.shift((q_.get_center() - c_snd) * 0.3) for q_ in slices], run_time=1.5)
            vo.wait_until("b")
            movers = list(text) + [patches[i] for i in picks] + list(slices)
            self.play(LaggedStart(*[FadeTransform(m.copy(), sq) for m, sq in zip(movers, seq)], lag_ratio=0.06),
                      *[p_.animate.set_opacity(0.3) for i, p_ in enumerate(patches) if i not in picks], run_time=2.5)
            self.play(FadeIn(sl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def question(self):
        q = label(r"What should a token be, \\ and how are the codes learned?", font_size=42).move_to(UP * 1.9)
        steps = [(r"Audrey, \ 1952", SND_C), (r"hidden Markov models", SND_C), (r"byte pairs", TEXT_C), (r"CTC", SND_C),
                 (r"WaveNet", SND_C), (r"CLIP", IMG_C), (r"Whisper", SND_C), (r"models that listen \\ while they speak", WHITE)]
        path = VGroup()
        for i, (t, c_) in enumerate(steps):
            path.add(label(t, font_size=28, color=c_))
            if i < len(steps) - 1:
                path.add(MathTex(r"\to", font_size=34, color=GREY_B))
        rows = VGroup(VGroup(*path[:8]).arrange(RIGHT, buff=0.2), VGroup(*path[8:]).arrange(RIGHT, buff=0.2))
        rows.arrange(DOWN, buff=0.35).move_to(UP * 0.1)
        if rows.width > 13.2:
            rows.width = 13.2
        ours = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"tokenizers", TEXT_C), (r"codebooks", IMG_C), (r"a speech codec", SND_C), (r"a speech recognizer", SND_C),
            (r"a picture-and-caption model", IMG_C))]).arrange(RIGHT, buff=0.45)
        if ours.width > 13.0:
            ours.width = 13.0
        ours.move_to(DOWN * 2.0)
        ol = label(r"built here, \ on the computer making this video:", font_size=26, color=GREY_A).next_to(ours, UP, buff=0.3)
        with self.voiceover(
            "Every sense poses the same questions. What should a token be? How many does a sentence, a picture or a "
            "second of speech need? And how are the codes learned? <bookmark mark='a'/> We'll follow seventy years of "
            "answers: a machine that recognized ten spoken digits in 1952, the statistical recognizers that followed, "
            "byte-pair encoding, CTC, WaveNet, CLIP and Whisper, up to models that listen while they speak. "
            "<bookmark mark='b'/> And we'll build small versions on the computer making this video: tokenizers, "
            "codebooks, a speech codec, a speech recognizer, and a model that matches pictures with captions."
        ) as vo:
            self.play(FadeIn(q), FadeIn(path.copy().set_opacity(0.18)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in path], lag_ratio=0.12), run_time=3.5)
            vo.wait_until("b")
            self.play(FadeIn(ol), LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in ours], lag_ratio=0.3), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Every Sense Is a Token", font_size=48).to_edge(UP, buff=0.5)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 0.6)
        obj = objectives_card([
            r"tokenizers for text: \ byte pairs, \ the unigram model, \ bytes and patches; \ what a token is worth in bits",
            r"vector quantization: \ codebooks, \ collapse and its cures, \ FSQ, \ LFQ, \ residual stages",
            r"sound: \ sampling, \ spectra, \ the mel scale, \ neural audio codecs",
            r"listening: \ templates, \ hidden Markov models, \ CTC, \ Whisper",
            r"speaking: \ from formants to WaveNet to codec language models, \ and this video's narrator",
            r"pictures and words: \ CLIP, \ SigLIP, \ vision-language and omni models",
        ], font_size=25)
        with self.voiceover(
            "This is Part 23 of AI, Built. <bookmark mark='a'/> In this part: tokenizers for text, and what a token "
            "is worth in bits; vector quantization, its codebooks and how they fail; sampling, spectra and neural "
            "audio codecs; listening, from templates to CTC and Whisper; speaking, up to the model narrating this "
            "video; and matching pictures with words, from CLIP to models that see, hear and talk."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeOut(title), FadeIn(obj))
        self.wait(0.3)
        self.clear_scene()
