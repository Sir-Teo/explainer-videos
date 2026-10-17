from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import MONO, TEXT_C, load, token_chips


class BPE(VoiceoverScene):
    def construct(self):
        self.card()
        self.merges()
        self.sizes()

    def card(self):
        card = chapter_card(1, r"Cutting text into tokens", r"What is a word, to a model?", part=16)
        with self.voiceover("Chapter one. Cutting text into tokens."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def merges(self):
        b = load("bpe")
        first = [str(x) for x in b["first"]][:24]
        chips = token_chips(first, font_size=24, height=0.46)
        rows = VGroup(*[VGroup(*chips[i:i + 8]).arrange(RIGHT, buff=0.08) for i in range(0, len(chips), 8)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(DOWN * 0.6)
        nums = VGroup(*[MathTex(str(i + 1), font_size=18, color=GREY_B).next_to(c, UP, buff=0.04) for i, c in enumerate(chips)])
        rule = label(r"start from single characters; \\ again and again, \ merge the pair that occurs most often", font_size=28,
                     color=GREY_A).to_edge(UP, buff=0.5)
        hl = label(r"the first merges, \ learned from two million characters of the novels \ ($\cdot$ = a space)",
                   font_size=22, color=TEXT_C).next_to(rows, UP, buff=0.4)
        cite_ = cite(r"P.~Gage (1994); \ R.~Sennrich, B.~Haddow \& A.~Birch (2016)", corner=DR)
        # the learned merges, applied in order to a phrase: adjacent pieces that spell the next merge become one
        learned = [str(x) for x in b["first"]]
        toks = list(" " + " ".join(str(b["sentence"]).split()[:5]))
        steps = []
        for k, m in enumerate(learned):
            i, hit, out = 0, [], []
            while i < len(toks):
                if i + 1 < len(toks) and toks[i] + toks[i + 1] == m:
                    hit.append(len(out))
                    out.append(m)
                    i += 2
                else:
                    out.append(toks[i])
                    i += 1
            if hit:
                steps.append((k + 1, m, hit, list(toks), out))
                toks = out
            if len(steps) == 9:
                break
        phrase = token_chips(steps[0][3], font_size=34, height=0.62, buff=0.08).move_to(UP * 0.4)
        with self.voiceover(
            "This series' models read one character at a time. Real ones read tokens: common chunks of text. The "
            "chunks are learned by byte-pair encoding, a compression trick from 1994. Start from single characters. "
            "Find the pair that occurs most often, and make it a new symbol. Repeat. <bookmark mark='a'/> Here are "
            "the first merges on our novels: common pairs of letters first, then the starts and ends of words, and "
            "soon whole words. Each new symbol is a token."
        ) as vo:
            self.play(FadeIn(rule), FadeIn(cite_))
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in phrase], lag_ratio=0.04), run_time=1.2)
            cur = phrase
            for k, m, hit, before, after in steps:
                ml = label(rf"merge ${k}$: \ ``{m.replace(' ', '·')}''", font_size=26, color=TEXT_C).next_to(cur, DOWN, buff=0.6)
                # where the merged pairs sit in the old row: map each output index back to its input pair
                j, src = 0, []
                for o, t in enumerate(after):
                    if o in hit:
                        src.append((j, j + 1))
                        j += 2
                    else:
                        src.append((j,))
                        j += 1
                boxes = VGroup(*[SurroundingRectangle(VGroup(cur[a_], cur[b_]), color=C.BITS, buff=0.05, corner_radius=0.08)
                                 for a_, b_ in (src[o] for o in hit)])
                self.play(Create(boxes), FadeIn(ml), run_time=0.45)
                new = token_chips(after, font_size=34, height=0.62, buff=0.08).move_to(cur)
                anims = []
                for o, ix in enumerate(src):
                    anims.append(ReplacementTransform(VGroup(*[cur[i_] for i_ in ix]), new[o]))
                self.play(*anims, FadeOut(boxes), FadeOut(ml), run_time=0.6)
                cur = new
            vo.wait_until("a")
            self.play(FadeOut(cur))
            self.play(FadeIn(hl), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.08), FadeIn(nums),
                      run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sizes(self):
        b = load("bpe")
        sizes = [0] + [int(n) for n in b["sizes"]]
        cuts = [[str(x) for x in b[f"cut{n}"]] for n in sizes]
        rows = VGroup()
        for n, cut in zip(sizes, cuts):
            chips = token_chips(cut, font_size=20, height=0.4, buff=0.04)
            if chips.width > 10.5:
                chips.scale_to_fit_width(10.5)
            lab = label(rf"${n:,}$ merges".replace(",", "{,}") if n else r"characters", font_size=22, color=GREY_A)
            cnt = label(rf"${len(cut)}$ tokens", font_size=22, color=TEXT_C)
            rows.add(VGroup(lab, chips, cnt))
        for r_ in rows:
            r_[0].move_to([-5.6, 0, 0], aligned_edge=LEFT)
            r_[1].next_to(r_[0], RIGHT, buff=0.3).align_to([-3.6, 0, 0], LEFT)
            r_[2].next_to(r_[1], RIGHT, buff=0.25)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(UP * 0.6)
        for r_ in rows:
            keep_in_frame(r_)
        cpt = VGroup(*[label(rf"${n:,}$ merges: \ ${float(b[f'cpt_passage{n}']):.2f}$ characters a token".replace(",", "{,}"),
                             font_size=24, color=TEXT_C) for n in sizes[1:]])
        cpt.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.5).shift(LEFT * 2.5)
        cl = label(r"on the scoreboard's passage", font_size=20, color=GREY_B).next_to(cpt, UP, buff=0.12).align_to(cpt, LEFT)
        trade = label(r"bigger vocabulary: \\ shorter sequences, \\ bigger tables", font_size=24, color=GREY_A).to_corner(DR, buff=0.5)
        n8 = float(b["cpt_passage8000"])
        with self.voiceover(
            "The more merges, the bigger the tokens. <bookmark mark='a'/> Here's one sentence, cut by the raw "
            "characters, then after five hundred, two thousand and eight thousand merges. <bookmark mark='b'/> With "
            f"eight thousand, a token covers {n8:.1f} characters of the passage on average, so a transformer reading "
            "tokens sees the same text in a fraction of the steps, and part twelve's attention cost shrinks with the "
            "square. The price is a bigger table of token vectors. Today's models use between a hundred and fifty "
            "thousand and a quarter of a million tokens."
        ) as vo:
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2), run_time=1.0)  # the sentence, one character a token, from the start
            vo.wait_until("a")
            self.play(Indicate(rows[0][1], color=TEXT_C, scale_factor=1.03), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.4), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(cl), FadeIn(cpt), FadeIn(trade))
        self.wait(0.3)
        self.clear_scene()
