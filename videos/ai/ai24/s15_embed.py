from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai24.common import (MATRY, NEG, PART, POS, SIMCLR, axes, curve, digit_sheet, load, node_box, pct, tag,
                                   take_away, take_away_in)
from videos.ai.ai24.s05_simclr import nn_sheet


class Embeddings(VoiceoverScene):
    def construct(self):
        self.card()
        self.search()
        self.text()
        self.nested()
        self.truncate()
        self.neighbours()

    def card(self):
        card = chapter_card(14, r"Embeddings for search", r"Text embeddings, \ retrieval, \ and Matryoshka vectors",
                            lit=(2013,), part=PART)
        with self.voiceover("Chapter fourteen. Embeddings for search."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def search(self):
        s = load("simclr")
        mt = load("matryoshka")
        pool, pool_y = np.asarray(s["pool"]), np.asarray(s["pool_y"])
        Q = list(mt["queries"])
        sh = nn_sheet(pool, pool_y, Q[:4], np.asarray(mt["plain_nn128"])[:4], size=0.6).move_to([-2.2, -0.3, 0])
        ql = label(r"query", font_size=20, color=GREY_A).next_to(sh, UP, buff=0.15).align_to(sh, LEFT)
        rl = label(r"nearest of $2{,}000$ by the embedding", font_size=20, color=GREY_A).next_to(sh, UP, buff=0.15)
        rl.shift(RIGHT * 0.8)
        same = float(np.mean([pool_y[j] == pool_y[q] for q, row in zip(Q, np.asarray(mt["plain_nn128"]))
                              for j in row]))
        steps = VGroup(node_box(r"embed every item once", SIMCLR, font_size=22),
                       node_box(r"embed the query", SIMCLR, font_size=22),
                       node_box(r"return the nearest vectors", POS, font_size=22)).arrange(DOWN, buff=0.4)
        steps.move_to([4.6, 0.4, 0])
        ann = label(r"at web scale: \ approximate nearest neighbours \\ (graphs such as HNSW)", font_size=20,
                    color=GREY_B).next_to(steps, DOWN, buff=0.4)
        with self.voiceover(
            "Everything so far was judged by how well a classifier could read the vectors. But much of the world "
            "uses them directly, for search. <bookmark mark='a'/> Embed every item once; embed the query; return "
            "the items whose vectors are nearest. <bookmark mark='b'/> Here is our SimCLR network as a search "
            "engine for digits: four queries and their nearest test digits, green when they are the same digit. "
            f"{pct(same, 0)} percent of them are. <bookmark mark='c'/> At the scale of the web, the nearest "
            "neighbours are found approximately, by graphs built over billions of vectors."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(b_) for b_ in steps], lag_ratio=0.4))
            vo.wait_until("a")
            self.play(Indicate(steps[2], color=POS))
            vo.wait_until("b")
            self.play(FadeIn(sh), FadeIn(ql), FadeIn(rl))
            vo.wait_until("c")
            self.play(FadeIn(ann))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def text(self):
        items = [
            (2013, r"word2vec", r"a vector per word"),
            (2019, r"Sentence-BERT", r"a vector per sentence, \\ twin networks"),
            (2020, r"DPR", r"questions and passages, \\ in-batch negatives"),
            (2021, r"SimCSE", r"the same sentence twice: \\ dropout is the augmentation"),
            (2023, r"E5, \ GTE, \ BGE; \ MTEB", r"contrastive pretraining \\ on web text pairs; \ a benchmark"),
            (2025, r"Qwen3-Embedding", r"an LLM as the encoder; \\ InfoNCE, \ Matryoshka"),
            (2026, r"Gemini Embedding 2", r"text, images, video, audio: \\ one space"),
        ]
        y0 = 0.4
        xs = np.linspace(-6.0, 6.0, len(items))
        line = Line([-6.6, y0, 0], [6.6, y0, 0], color=GREY_C, stroke_width=2)
        g = VGroup()
        for k, ((yr, nm, what), x) in enumerate(zip(items, xs)):
            d = Dot([x, y0, 0], radius=0.07, color=MATRY)
            t = VGroup(label(str(yr), font_size=20, color=MATRY), label(nm, font_size=19, color=WHITE),
                       label(what, font_size=16, color=GREY_A)).arrange(DOWN, buff=0.06)
            t.next_to(d, UP if k % 2 == 0 else DOWN, buff=0.25)
            g.add(VGroup(d, t))
        head = label(r"Text embeddings: \ the same contrastive idea", font_size=32).to_edge(UP, buff=0.35)
        nums = label(r"MMTEB, multilingual: \ Qwen3-Embedding-8B $70.58$, \ Gemini Embedding $68.37$ (2025); \ Gemini "
                     r"Embedding 2: $69.9$ (2026)", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.75)
        clip = label(r"and across senses: \ CLIP and SigLIP pair pictures with captions by the same loss \ (Part 23)",
                     font_size=19, color=GREY_B).next_to(nums, DOWN, buff=0.12)
        src = cite(r"Reimers \& Gurevych (2019); \ Karpukhin et al.\ (2020); \ Gao, Yao \& Chen (2021); \ Muennighoff et "
                   r"al.\ (2023); \ Zhang et al.\ (2025); \ Shanbhogue et al.\ (2026)", font_size=17)
        src.next_to(head, DOWN, buff=0.15)
        with self.voiceover(
            "Search engines today mostly embed text, and the history runs from Part 3's word vectors to here. "
            "<bookmark mark='a'/> Sentence-BERT in 2019 trained twin networks to place similar sentences together. "
            "DPR, in 2020, matched questions to passages, using the other passages in each batch as negatives: "
            "InfoNCE again. <bookmark mark='b'/> SimCSE, in 2021, needed no pairs at all: feed the same sentence in "
            "twice, and the network's random dropout makes the two views. <bookmark mark='c'/> Then came "
            "contrastive pretraining on hundreds of millions of web text pairs, and a benchmark, MTEB, to compare "
            "the results. <bookmark mark='d'/> Today's leaders are language models turned into encoders. "
            "Qwen3-Embedding, in 2025, trains with InfoNCE and a temperature; <bookmark mark='e'/> Google's Gemini "
            "Embedding 2, in 2026, puts text, images, video and sound in one space. The same loss, with pictures and "
            "captions as the two views, is how CLIP and SigLIP were trained, in Part 23."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(src))
            self.play(FadeIn(g[0]))
            vo.wait_until("a")
            self.play(FadeIn(g[1]), FadeIn(g[2]))
            vo.wait_until("b")
            self.play(FadeIn(g[3]))
            vo.wait_until("c")
            self.play(FadeIn(g[4]))
            vo.wait_until("d")
            self.play(FadeIn(g[5]), FadeIn(nums))
            vo.wait_until("e")
            self.play(FadeIn(g[6]), FadeIn(clip))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def nested(self):
        dims = [2, 4, 8, 16, 32, 64, 128]
        dolls = VGroup()
        for i, m in enumerate(dims):
            w = 0.4 + 0.1 * m ** 0.85
            dolls.add(Rectangle(width=w, height=0.8, stroke_color=MATRY, stroke_width=2, fill_color=MATRY,
                                fill_opacity=0.08 + 0.1 * (len(dims) - i) / len(dims)).move_to([-6.0 + w / 2, 1.3, 0]))
        dl = VGroup(*[MathTex(str(m), font_size=24, color=MATRY).move_to([d.get_right()[0] - 0.2, 1.98, 0])
                      for m, d in zip(dims, dolls)])
        mem = label(r"$10^9$ items $\times$ $1{,}000$ numbers $\times$ $4$ bytes $=$ $4$ terabytes", font_size=36,
                    color=GREY_A).move_to(UP * 0.4)
        cap = label(r"the first $m$ numbers of one 128-number vector", font_size=22, color=GREY_A).next_to(dolls, DOWN,
                                                                                                       buff=0.3)
        f = MathTex(r"\mathcal L_{\rm MRL}", r"=", r"\frac{1}{|M|} \sum_{m \in M}", r"\mathcal L_{\rm NT\text{-}Xent}"
                    r"\big(z_{1:m},\, z'_{1:m}\big)", font_size=38).move_to([0, -0.9, 0])
        f[3].set_color(MATRY)
        fl = label(r"$M = \{2, 4, 8, \dots, 128\}$: \ the same contrastive loss on every prefix", font_size=22,
                   color=GREY_A).next_to(f, DOWN, buff=0.3)
        oai = label(r"OpenAI's text-embedding-3 (2024): \ shortened to $256$ numbers, \ it still beats the older "
                    r"model's $1{,}536$ on MTEB", font_size=20, color=GREY_B).to_edge(DOWN, buff=0.5)
        src = cite(r"Kusupati et al.\ (2022): \ Matryoshka representation learning", corner=UR)
        with self.voiceover(
            "Vectors cost memory: a billion items at a thousand numbers each is four terabytes. Often you would "
            "like to search with a short vector first and refine with a long one. <bookmark mark='a'/> Matryoshka "
            "representation learning, from Aditya Kusupati and colleagues in 2022, trains one vector so that its "
            "first two numbers, its first four, its first eight, and so on, are each a good embedding by "
            "themselves, like dolls nested inside each other. <bookmark mark='b'/> The loss is just the usual loss "
            "applied to every prefix and averaged. <bookmark mark='c'/> Qwen3-Embedding supports it, and OpenAI's "
            "2024 models can be shortened the same way: cut to 256 numbers, the large model still beats its "
            "predecessor's full 1,536."
        ) as vo:
            self.play(FadeIn(src), FadeIn(mem, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeOut(mem))
            self.play(LaggedStart(*[GrowFromEdge(d, LEFT) for d in dolls[::-1]], lag_ratio=0.15), FadeIn(dl),
                      FadeIn(cap), run_time=2.0)
            vo.wait_until("b")
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("c")
            self.play(FadeIn(oai))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def truncate(self):
        mt = load("matryoshka")
        runs, keys = mt["runs"], mt["keys"]
        dims = list(runs[keys[0]]["extra"]["prefix_dims"])
        lx = [math.log2(d) for d in dims]
        M = np.array([runs[k]["extra"]["prefix_knn"] for k in keys])
        P = np.array(list(mt["plain_prefix"].values()))
        lo = float(np.floor(min(M.min(), P.min()) * 10) / 10)
        ax = axes([lx[0] - 0.3, lx[-1] + 0.3], [lo, 1.0], x_length=7.6, y_length=4.2,
                  xlabel=r"numbers kept, \ out of $128$", ylabel=r"$k$-NN accuracy on the test set", xticks=lx,
                  xfmt=lambda v: f"{int(round(2 ** v))}", yticks=[lo, (lo + 1) / 2, 1.0], center=[-1.0, -0.4, 0])
        def band_of(A, col):
            g = VGroup()
            for row in A:
                g.add(curve(ax.ax, lx, row, col, 1.6).set_stroke(opacity=0.5))
            g.add(curve(ax.ax, lx, A.mean(0), col, 3.5))
            g.add(VGroup(*[Dot(ax.ax.c2p(x, y), radius=0.06, color=col) for x, y in zip(lx, A.mean(0))]))
            return g

        cp, cm = band_of(P, GREY_B), band_of(M, MATRY)
        leg = VGroup(label(r"SimCLR, \ cut short", font_size=22, color=GREY_B),
                     label(r"SimCLR + Matryoshka", font_size=22, color=MATRY)).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.12)
        leg.move_to([4.9, -1.2, 0])
        tg = tag(r"computed: \ three seeds each; \ thin lines: seeds", corner=UR)
        i4 = dims.index(4) if 4 in dims else 1
        p4, m4 = P.mean(0)[i4], M.mean(0)[i4]
        pf, mf = P.mean(0)[-1], M.mean(0)[-1]
        v = (f"With only four numbers, the ordinary embedding finds the right digit {pct(p4, 0)} percent of the time; "
             f"the Matryoshka one, {pct(m4, 0)} percent. At the full 128 the two are within "
             f"{pct(abs(pf - mf))} points." if m4 > p4 + 0.02 else
             f"With four numbers: {pct(p4, 0)} percent for the ordinary embedding, {pct(m4, 0)} for the Matryoshka "
             "one.")
        with self.voiceover(
            "We trained SimCLR with the Matryoshka loss, three times, and compared it with ordinary SimCLR, its "
            "vector simply cut short. <bookmark mark='a'/> Keep the first few numbers of each, renormalize, and "
            f"ask the nearest neighbours. <bookmark mark='b'/> {v}"
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tg), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(cp), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(cm), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def neighbours(self):
        s = load("simclr")
        mt = load("matryoshka")
        pool, pool_y = np.asarray(s["pool"]), np.asarray(s["pool_y"])
        Q = list(mt["queries"])
        a = nn_sheet(pool, pool_y, Q, np.asarray(mt["plain_nn4"]), size=0.42).move_to([-3.5, -0.4, 0])
        b = nn_sheet(pool, pool_y, Q, np.asarray(mt["nn4"]), size=0.42).move_to([3.5, -0.4, 0])
        la = label(r"SimCLR, \ first $4$ numbers", font_size=24, color=SIMCLR).next_to(a, UP, buff=0.25)
        lb = label(r"Matryoshka, \ first $4$ numbers", font_size=24, color=MATRY).next_to(b, UP, buff=0.25)
        fa = float(np.mean([pool_y[j] == pool_y[q] for q, row in zip(Q, np.asarray(mt["plain_nn4"])) for j in row]))
        fb = float(np.mean([pool_y[j] == pool_y[q] for q, row in zip(Q, np.asarray(mt["nn4"])) for j in row]))
        ra = label(rf"same digit: \ ${pct(fa, 0)}\%$", font_size=22, color=SIMCLR).next_to(a, DOWN, buff=0.2)
        rb = label(rf"same digit: \ ${pct(fb, 0)}\%$", font_size=22, color=MATRY).next_to(b, DOWN, buff=0.2)
        tk = take_away(r"train every prefix, \ and one vector serves every budget")
        with self.voiceover(
            "Here is what that means for search: the same six queries, answered using only the first four "
            f"numbers. <bookmark mark='a'/> Cut short, ordinary SimCLR returns the same digit {pct(fa, 0)} percent "
            f"of the time; <bookmark mark='b'/> the Matryoshka embedding, {pct(fb, 0)} percent. One vector, "
            "trained once, that can be cut to fit the budget."
        ) as vo:
            self.play(FadeIn(a), FadeIn(la))
            vo.wait_until("a")
            self.play(FadeIn(ra))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(lb), FadeIn(rb))
            self.play(*take_away_in(self, tk))
        self.wait(0.3)
        self.clear_scene()
