from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import IMG_C, SND_C, TEXT_C, TOKEN_COLORS, gray_image, heat, load, token_chips


class Hook(VoiceoverScene):
    def construct(self):
        self.converge()
        self.plan()

    # ------------------------------------------------------------------
    def converge(self):
        b, v, s = load("bpe"), load("vq"), load("sound")
        cut = [str(x) for x in b["cut2000"]][:8]
        text = token_chips(cut, font_size=28, height=0.5).move_to([-2.2, 2.5, 0])
        # the picture, as 25 patches of 4 x 4 pixels laid exactly over it
        img = np.asarray(v["image"])
        P, n = 1.8 / 5, 5
        c_pic = np.array([-4.2, 0.1, 0])
        patches = Group(*[gray_image(img[4 * r:4 * r + 4, 4 * c:4 * c + 4], P).move_to(c_pic + np.array([(c - 2) * P, (2 - r) * P, 0]))
                          for r in range(n) for c in range(n)])
        # the sound, as 8 slices of its spectrogram
        spec = np.asarray(s["spec"])[::-1]
        k, sw = 8, 0.55
        c_snd = np.array([1.8, 0.1, 0])
        cols = np.array_split(np.arange(spec.shape[1]), k)
        slices = Group(*[heat(spec[:, ix], sw, 1.8, color=SND_C, lo=spec.min(), hi=spec.max()).move_to(c_snd + np.array([(j - (k - 1) / 2) * sw, 0, 0]))
                         for j, ix in enumerate(cols)])
        labs = VGroup(label(r"text", font_size=26, color=TEXT_C).next_to(text, LEFT, buff=0.3),
                      label(r"a picture", font_size=26, color=IMG_C).next_to(patches, UP, buff=0.25),
                      label(r"sound", font_size=26, color=SND_C).next_to(slices, UP, buff=0.25))
        # one sequence at the bottom: text tokens, then picture tokens, then sound tokens
        picks = [6, 7, 8, 11, 12, 13, 16, 17, 18]  # the middle of the letter
        kinds = [TEXT_C] * len(text) + [IMG_C] * len(picks) + [SND_C] * k
        q = 0.42
        seq = VGroup(*[Square(q, stroke_color=c_, stroke_width=2, fill_color=c_, fill_opacity=0.35) for c_ in kinds])
        seq.arrange(RIGHT, buff=0.06).move_to([0, -2.6, 0])
        sl = label(r"one sequence of tokens", font_size=26, color=WHITE).next_to(seq, DOWN, buff=0.25)
        with self.voiceover(
            "A transformer reads tokens. So how does a model look at a picture, or listen to a voice? "
            "<bookmark mark='a'/> Everything is turned into tokens first: text into pieces of words, pictures into "
            "codes for patches, sound into codes for slices of time. <bookmark mark='b'/> Then it's all one "
            "sequence, and one model can read it."
        ) as vo:
            self.play(FadeIn(text), FadeIn(patches), FadeIn(slices), FadeIn(labs), run_time=1.5)
            vo.wait_until("a")
            self.play(text.animate.arrange(RIGHT, buff=0.22, center=False),  # center=False: spread from the first chip, in place
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
    def plan(self):
        title = label(r"Part 16: \ Every Sense Is a Token", font_size=52).to_edge(UP, buff=0.6)
        sub = label(r"byte-pair encoding, \ codebooks, \ sound codes, \ CLIP and SigLIP, \ omni models", font_size=28,
                    color=C.BITS).next_to(title, DOWN, buff=0.25)
        smap = series_map(current=16, done=15).scale(0.85).move_to(DOWN * 0.9)
        with self.voiceover(
            "This part is about how the senses become tokens, how pictures and words are matched, "
            "<bookmark mark='a'/> and how one model can see, listen and speak."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(smap))
        self.wait(0.5)
        self.clear_scene()
