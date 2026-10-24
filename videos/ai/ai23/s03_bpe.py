from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import MONO, PART, TEXT_C, load, token_chips


class BPE(VoiceoverScene):
    def construct(self):
        self.card()
        self.units()
        self.merges()
        self.compression()
        self.sizes()

    def card(self):
        card = chapter_card(2, r"Merges as compression", r"What is a word, to a model?", lit=(1948, 1952, 1976), part=PART)
        with self.voiceover("Chapter two. Merges as compression."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def units(self):
        b = load("bpe")
        sent = str(b["sentence"])
        words = token_chips([w for w in sent.split(" ")], font_size=30, height=0.56, buff=0.12)
        chars = token_chips(list(sent), font_size=22, height=0.42, buff=0.03)
        if chars.width > 12.6:
            chars.width = 12.6
        wl = label(rf"words: \ ${len(sent.split())}$ tokens", font_size=24, color=GREY_A)
        cl = label(rf"characters: \ ${len(sent)}$ tokens", font_size=24, color=GREY_A)
        VGroup(wl, words).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(UP * 2.0)
        VGroup(cl, chars).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(DOWN * 0.1)
        for m in (wl, words, cl, chars):
            m.set_x(0)
        types, oov = int(b["n_word_types"]), float(b["oov_passage"])
        unseen = [str(w) for w in b["unseen_examples"]][:6]
        ex = VGroup(*[data_text(w, font=MONO, font_size=22, color=C.SURPRISE) for w in unseen]).arrange(RIGHT, buff=0.35)
        exl = label(rf"words of the passage never seen in ${b['sample_chars'] / 1e6:.0f}$ million characters of the novels:",
                    font_size=22, color=GREY_A)
        exg = VGroup(exl, ex).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.6)
        if exg.width > 13:
            exg.width = 13
        with self.voiceover(
            "A tokenizer decides what a model's units are. Whole words? <bookmark mark='a'/> In two million "
            f"characters of our novels there are {types:,} different words, and still {100 * oov:.1f} percent of the "
            "words in the scoreboard's passage never appear among them. A model of words has nothing to say about "
            "those. <bookmark mark='b'/> Single characters never run out, but a sentence becomes a long sequence, "
            "and attention's cost grows with the square of its length. Byte-pair encoding finds the units in between."
        ) as vo:
            self.play(FadeIn(wl), LaggedStart(*[FadeIn(w, shift=UP * 0.1) for w in words], lag_ratio=0.08), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(exg))
            vo.wait_until("b")
            self.play(FadeIn(cl), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chars], lag_ratio=0.02), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def merges(self):
        b = load("bpe")
        first = [str(x) for x in b["first"]][:24]
        chips = token_chips(first, font_size=24, height=0.46)
        rows = VGroup(*[VGroup(*chips[i:i + 8]).arrange(RIGHT, buff=0.08) for i in range(0, len(chips), 8)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(DOWN * 0.6)
        nums = VGroup(*[MathTex(str(i + 1), font_size=18, color=GREY_B).next_to(c, UP, buff=0.04) for i, c in enumerate(chips)])
        rule = label(r"start from single characters; \\ again and again, \ merge the pair that occurs most often",
                     font_size=28, color=GREY_A).to_edge(UP, buff=0.5)
        hl = label(r"the first merges, \ learned from two million characters of the novels \ ($\cdot$ = a space)",
                   font_size=22, color=TEXT_C).next_to(rows, UP, buff=0.4)
        cite_ = cite(r"P.~Gage (1994); \ R.~Sennrich, B.~Haddow \& A.~Birch (2016)", corner=DR)
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
            "In 1994 Philip Gage described a way to compress a file: find the pair of bytes that occurs most often, "
            "replace it everywhere with one new symbol, and repeat. In 2016 Rico Sennrich, Barry Haddow and Alexandra "
            "Birch used it to cut words for machine translation. Start from single characters, merge the commonest "
            "neighbouring pair, and repeat. <bookmark mark='a'/> Here are the first merges on our novels: a space "
            "and a t, h and e, then the starts and ends of words, and soon whole words. Each new symbol is a token."
        ) as vo:
            self.play(FadeIn(rule), FadeIn(cite_))
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in phrase], lag_ratio=0.04), run_time=1.2)
            cur = phrase
            for k, m, hit, before, after in steps:
                ml = label(rf"merge ${k}$: \ ``{m.replace(' ', '·')}''", font_size=26, color=TEXT_C).next_to(cur, DOWN, buff=0.6)
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
                anims = [ReplacementTransform(VGroup(*[cur[i_] for i_ in ix]), new[o]) for o, ix in enumerate(src)]
                self.play(*anims, FadeOut(boxes), FadeOut(ml), run_time=0.6)
                cur = new
            vo.wait_until("a")
            self.play(FadeOut(cur))
            self.play(FadeIn(hl), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.08), FadeIn(nums),
                      run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compression(self):
        b = load("bpe")
        L = np.asarray(b["length"], float)
        ks = np.arange(len(L)) * 50
        L0 = float(b["sample_chars"])
        n1 = int(b["first_counts"][0])
        ax = axes([0, ks[-1], 2000], [0, L0 / 1e6 * 1.05, 0.5], x_length=5.6, y_length=3.6,
                  xlabel=r"merges", ylabel=r"length of the text, \ millions of symbols", xticks=[0, 4000, 8000],
                  yticks=[0, 1, 2], center=[-3.4, -0.4, 0])
        cv = curve(ax.ax, ks, L / 1e6, TEXT_C, 4)
        end = Dot(ax.ax.c2p(ks[-1], L[-1] / 1e6), color=TEXT_C)
        endl = label(rf"${100 * L[-1] / L0:.0f}\%$ of the characters", font_size=22, color=TEXT_C).next_to(end, UP, buff=0.15)
        colors = {r"n_k": C.BITS, r"n_i": C.BITS, r"L_k": TEXT_C, r"L_{k-1}": TEXT_C, r"L_0": TEXT_C}
        rows = [cmath(r"L_k", r"=", r"L_{k-1}", r"-", r"n_k", colors=colors, font_size=38),
                cmath(r"L_k", r"=", r"L_0", r"-", r"\textstyle\sum_{i \le k}", r"n_i", colors=colors, font_size=38),
                MathTex(r"\text{merge } \arg\max_{(a,b)} n(a, b)", font_size=34, color=C.BITS)]
        whys = [why(r"pair $(a, b)$ found $n_k$ times: \\ two symbols become one, \ each time", font_size=22),
                why(r"add up the steps", font_size=22),
                why(r"BPE: \ the biggest saving next \\ (greedy, \ so not always the best)", font_size=22)]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=2.0, align_index=None, buff=0.75, edge=6.9)
        with self.voiceover(
            "Why is this compression? <bookmark mark='a'/> Each time the merged pair occurs, two symbols become one, "
            "so a merge that applies n times shortens the text by exactly n. <bookmark mark='b'/> After k merges the "
            "text is its original length minus the sum of the counts, <bookmark mark='c'/> and choosing the "
            "commonest pair means taking the biggest saving next: a greedy compressor. <bookmark mark='d'/> On our "
            f"novels the first merge alone saves {n1:,} symbols, and after {len(b['merges']):,} merges the text is "
            f"{100 * L[-1] / L0:.0f} percent of its length in characters. The savings shrink as the merges get rarer."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2, transform=False)
            vo.wait_until("d")
            self.play(Create(cv), run_time=2.5)
            self.play(FadeIn(end), FadeIn(endl))
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
            if chips.width > 9.2:
                chips.scale_to_fit_width(9.2)
            lab = label(rf"${n:,}$ merges".replace(",", "{,}") if n else r"characters", font_size=22, color=GREY_A)
            cnt = label(rf"${len(cut)}$", font_size=22, color=TEXT_C)
            rows.add(VGroup(lab, chips, cnt))
        for r_ in rows:
            r_[0].move_to([-5.9, 0, 0], aligned_edge=LEFT)
            r_[1].next_to(r_[0], RIGHT, buff=0.3).align_to([-4.1, 0, 0], LEFT)
            r_[2].next_to(r_[1], RIGHT, buff=0.25)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(UP * 1.7)
        for r_ in rows:
            keep_in_frame(r_)
        top = rows.get_top()[1]
        th = label(r"tokens", font_size=20, color=GREY_B).move_to([rows[0][2].get_x(), top + 0.25, 0])
        n_max = sizes[-1]
        cpt = label(rf"on the scoreboard's passage, \ ${n_max:,}$ merges: \ ${float(b[f'cpt_passage{n_max}']):.2f}$ "
                    r"characters a token".replace(",", "{,}"), font_size=24, color=TEXT_C).move_to(DOWN * 0.55)
        wp = [str(x) for x in b["wordpiece"]][:8]
        wpc = token_chips(wp, font_size=20, height=0.4, colors=[GREY_B])
        wpl = label(r"WordPiece (BERT) merges the pair with the highest \ $n(ab) / \big(n(a)\,n(b)\big)$: \ its first merges",
                    font_size=22, color=GREY_A)
        wpg = VGroup(wpl, wpc).arrange(DOWN, buff=0.15).move_to(DOWN * 1.6)
        vocab = label(r"vocabularies today: \ GPT-2 \ $50{,}257$; \ Llama 3 \ $128{,}256$; \ GPT-4o \ about $200{,}000$; \ "
                      r"Gemma 3 \ $262{,}144$", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.35)
        if vocab.width > 13.2:
            vocab.width = 13.2
        n8 = float(b[f"cpt_passage{n_max}"])
        with self.voiceover(
            "The more merges, the bigger the tokens. <bookmark mark='a'/> Here's one sentence, cut into characters, "
            f"then after {sizes[1]:,}, {sizes[2]:,} and {sizes[3]:,} merges. <bookmark mark='b'/> With {n_max:,} merges a "
            f"token covers {n8:.1f} characters of the passage on average, so a transformer sees the same text in a "
            "fraction of the steps. <bookmark mark='c'/> BERT's tokenizer, WordPiece, merges by a different rule: the "
            "pair whose parts rarely occur apart, the merge that most raises the text's likelihood. Its first merges "
            "on our novels are rare pairs that always come together. <bookmark mark='d'/> Real vocabularies run from "
            "fifty thousand tokens in GPT-2 to over a quarter of a million in Gemma 3."
        ) as vo:
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2), FadeIn(th), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.4), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(cpt))
            vo.wait_until("c")
            self.play(FadeIn(wpg))
            vo.wait_until("d")
            self.play(FadeIn(vocab))
        self.wait(0.3)
        self.clear_scene()
