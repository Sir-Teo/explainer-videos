from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import IMG_C, TOKEN_COLORS, gray_image, load


class VQ(VoiceoverScene):
    def construct(self):
        self.card()
        self.codebook()
        self.residual()

    def card(self):
        card = chapter_card(2, r"Codebooks", r"How do you turn a picture into words?", part=16)
        with self.voiceover("Chapter two. Codebooks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def codebook(self):
        v = load("vq")
        book = np.asarray(v["codebook16"])
        img = np.asarray(v["image"])
        cb = Group(*[gray_image(c, 0.5) for c in book]).arrange_in_grid(rows=2, cols=8, buff=0.08).move_to([3.0, 2.3, 0])
        ids = VGroup(*[MathTex(str(i), font_size=18, color=TOKEN_COLORS[i % 8]).next_to(c, DOWN, buff=0.04)
                       for i, c in enumerate(cb)])
        cbl = label(r"a codebook: \ $16$ typical $4\times4$ patches \ (k-means on the letters)", font_size=22, color=IMG_C)
        cbl.next_to(cb, UP, buff=0.15)
        # the letter, as 25 patches; each patch's nearest code (the token), and the copy built from the codes
        n, P = 5, 0.62
        c0 = np.array([-4.0, 0.1, 0])
        pos = [c0 + np.array([(c - 2) * P, (2 - r) * P, 0]) for r in range(n) for c in range(n)]
        pats = [img[4 * r:4 * r + 4, 4 * c:4 * c + 4] for r in range(n) for c in range(n)]
        code = [int(np.argmin(((book - p_[None]) ** 2).sum((1, 2)))) for p_ in pats]
        tiles = Group(*[gray_image(p_, P).move_to(x) for p_, x in zip(pats, pos)])
        ol = label(r"a letter, \ cut into $4\times4$ patches", font_size=22, color=GREY_A)
        ol.move_to([c0[0], c0[1] + 2 * P * 1.3 + P / 2 + 0.3, 0])  # above the patches once they are spread apart
        spread = [c0 + (x - c0) * 1.3 for x in pos]
        coded = Group(*[gray_image(book[k], P).move_to(x) for k, x in zip(code, spread)])
        nums = VGroup(*[MathTex(str(k), font_size=26, color=TOKEN_COLORS[k % 8]).move_to(x) for k, x in zip(code, spread)])
        seq = VGroup(*[MathTex(str(k), font_size=26, color=TOKEN_COLORS[k % 8]) for k in code]).arrange(RIGHT, buff=0.16)
        if seq.width > 6.2:
            seq.scale_to_fit_width(6.2)
        seq.move_to([2.3, -0.9, 0])
        sql = label(r"the picture, \ as $25$ tokens", font_size=22, color=IMG_C).next_to(seq, UP, buff=0.2)
        recs = Group(*[gray_image(np.asarray(v[f"img_vq{k}"]), 1.6) for k in v["sizes"]]).arrange(RIGHT, buff=0.5)
        recs.move_to([2.3, -2.5, 0])
        rl = VGroup(*[label(rf"${int(k)}$ codes: \ ${float(v[f'err_vq{k}']):.3f}$", font_size=20, color=IMG_C)
                      .next_to(r, DOWN, buff=0.1) for k, r in zip(v["sizes"], recs)])
        cite_ = cite(r"A.~van den Oord, O.~Vinyals \& K.~Kavukcuoglu, \textit{VQ-VAE} (2017)", corner=UR)
        with self.voiceover(
            "Text comes in pieces. Pictures and sound are continuous, so to make tokens of them, we need a "
            "vocabulary of shapes: a codebook. <bookmark mark='a'/> Cut every letter picture into four by four "
            "patches and find sixteen typical ones: that's k-means clustering, which part six's mixtures "
            "generalize. <bookmark mark='b'/> Now any picture becomes a sequence of numbers from zero to fifteen: "
            "replace each patch by its nearest code. <bookmark mark='c'/> With more codes, the copy gets closer: "
            "sixteen, sixty-four, two hundred and fifty-six."
        ) as vo:
            self.play(FadeIn(tiles), FadeIn(ol))
            self.play(*[t_.animate.move_to(x) for t_, x in zip(tiles, spread)], run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(cbl), LaggedStart(*[FadeIn(c, scale=0.6) for c in cb], lag_ratio=0.06), FadeIn(ids), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeTransform(t_, c_) for t_, c_ in zip(tiles, coded)], lag_ratio=0.04), run_time=2.0)
            self.play(LaggedStart(*[FadeIn(m_) for m_ in nums], lag_ratio=0.03), *[c_.animate.set_opacity(0.35) for c_ in coded])
            self.play(LaggedStart(*[TransformFromCopy(m_, q_) for m_, q_ in zip(nums, seq)], lag_ratio=0.04), FadeIn(sql), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.2) for r in recs], lag_ratio=0.4), FadeIn(rl), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def residual(self):
        v = load("vq")
        errs = [float(e) for e in v["rvq_errs"]]
        stages = Group(*[gray_image(np.asarray(v[f"img_rvq{k}"]), 1.6) for k in range(1, 5)]).arrange(RIGHT, buff=0.6)
        stages.move_to(UP * 0.7)
        plus = VGroup(*[MathTex(r"\to", font_size=34, color=GREY_B).move_to((a.get_right() + b.get_left()) / 2)
                        for a, b in zip(stages, stages[1:])])
        sl = VGroup(*[label(rf"${k}$ stage{'s' if k > 1 else ''}: \ ${e:.3f}$", font_size=22, color=IMG_C)
                      .next_to(st, DOWN, buff=0.15) for k, (st, e) in enumerate(zip(stages, errs), start=1)])
        colors = {r"\hat x": IMG_C}
        f = cmath(r"\hat x", "=", r"c^{(1)}_{i_1} + c^{(2)}_{i_2} + c^{(3)}_{i_3} + c^{(4)}_{i_4}", colors=colors,
                  font_size=38).to_edge(UP, buff=0.4)
        fl = label(r"each stage codes what the earlier ones missed", font_size=22, color=GREY_A).next_to(f, DOWN, buff=0.12)
        comp = label(rf"$4$ stages of $16$: \ ${errs[-1]:.3f}$, \ like one codebook of $256$ (${float(v['err_vq256']):.3f}$) \\ "
                     rf"finite scalar quantization, \ rounding $4$ numbers to $5$ levels each: \ ${float(v['err_fsq']):.3f}$",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.5)
        used = label(r"sound codecs: \ SoundStream, \ EnCodec, \ Mimi", font_size=22, color=C.INTERVAL).next_to(comp, UP, buff=0.25)
        with self.voiceover(
            "One codebook can only be so fine. The trick sound models use is to quantize in stages. "
            "<bookmark mark='a'/> The first stage codes the patch roughly; the second codes what the first missed; "
            "then the third, and the fourth. <bookmark mark='b'/> Four stages of sixteen codes do as well here as one "
            "codebook of two hundred and fifty-six, and each token stays a small number. That's residual vector "
            "quantization, inside every neural audio codec. A simpler cousin, finite scalar quantization, just rounds "
            "a few numbers to a few levels, with no codebook at all."
        ) as vo:
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("a")
            for i, st in enumerate(stages):
                self.play(FadeIn(st, shift=RIGHT * 0.2), FadeIn(sl[i]), *([FadeIn(plus[i - 1])] if i else []), run_time=0.8)
            vo.wait_until("b")
            self.play(FadeIn(comp), FadeIn(used))
        self.wait(0.3)
        self.clear_scene()
