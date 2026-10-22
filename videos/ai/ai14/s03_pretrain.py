from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import (DECODER, ENCDEC, ENCODER, MONO, PART, PRIOR, F, chip, config_card, human,
                                   node_box, take_away)


class Pretrain(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.ulmfit_elmo()
        self.gpt1()
        self.objective()
        self.next_step()

    def card(self):
        card = chapter_card(2, r"Pretrain, then fine-tune", r"Can a model learn language before it learns a task?",
                            lit=(2018,), part=PART)
        with self.voiceover("Chapter two. Pretrain, then fine-tune."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def problem(self):
        B = F.BERT
        glue = [("MNLI", 392), ("QQP", 363), ("QNLI", 108), ("SST-2", 67), ("CoLA", 8.5), ("STS-B", 5.7),
                ("MRPC", 3.5), ("RTE", 2.5)]  # thousands of labelled training examples (BERT, Table 1)
        mx = 2500 + 800  # millions of words of raw text, for scale
        bars = VGroup()
        for i, (nm, k) in enumerate(glue):
            w = max(5.0 * k / 400, 0.03)
            r = VGroup(label(nm, font_size=20, color=GREY_A),
                       Rectangle(width=w, height=0.26, stroke_width=0, fill_color=PRIOR, fill_opacity=0.9),
                       label(rf"${k:g}$k", font_size=18, color=GREY_B))
            r[0].move_to([-0.25 - r[0].width / 2, 0, 0])
            r[1].move_to([w / 2, 0, 0])
            r[2].next_to(r[1], RIGHT, buff=0.1)
            bars.add(r.shift(DOWN * 0.36 * i))
        bars.move_to([-3.4, -0.4, 0])
        bt = label(r"labelled examples per task \ (GLUE)", font_size=24, color=PRIOR).next_to(bars, UP, buff=0.35)
        raw = VGroup(label(rf"raw text: \ ${B['words_books'] / 1e6:.0f}$ million words of books", font_size=24,
                           color=C.DATA),
                     label(rf"$+ \ {B['words_wiki'] / 1e6:,.0f}$ million words of Wikipedia".replace(",", "{,}"),
                           font_size=24, color=C.DATA),
                     label(r"no labels needed", font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        raw.move_to([3.6, 1.0, 0])
        vision = label(r"vision already did this: \ pretrain on ImageNet, \\ fine-tune for each new task \ (Part 10)",
                       font_size=22, color=GREY_A).move_to([3.6, -0.6, 0])
        d = definition_card(r"pretraining, \ fine-tuning", r"pretrain one network on raw text with a self-supervised "
                            r"objective; \ then fine-tune a copy on each small labelled task", width=6.8,
                            color=C.DATA, font_size=22).move_to([3.4, -2.2, 0])
        cite_ = cite(r"task sizes: \ Devlin et al.\ (2018), Table 1")
        with self.voiceover(
            "In 2017, almost every language task trained its own model, from scratch, on its own labelled data. A "
            "benchmark for sentence understanding, GLUE, collected eight such tasks; their training sets range from "
            "four hundred thousand examples down to two and a half thousand. <bookmark mark='a'/> Labels are "
            "expensive. Raw text is nearly free: billions of words of books and encyclopedias. <bookmark mark='b'/> "
            "Computer vision had already found the way to use the free kind: train one network on ImageNet, then "
            "fine-tune it for each new task. <bookmark mark='c'/> In 2018 language did the same. Pretrain on raw text "
            "with an objective that needs no labels, the guessing game of Part 1, then fine-tune a copy on each task."
        ) as vo:
            self.play(FadeIn(bt), FadeIn(cite_), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in bars],
                                                             lag_ratio=0.15), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(raw, shift=LEFT * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(vision))
            vo.wait_until("c")
            self.play(FadeIn(d, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ulmfit_elmo(self):
        U, E = F.ULMFIT, F.ELMO
        u = history_card(2018, r"ULMFiT \ (Howard \& Ruder; fast.ai, NUI Galway)",
                         rf"a recurrent language model pretrained on Wikipedia ({U['words'] / 1e6:.0f}M words), "
                         rf"fine-tuned layer by layer: \ ${U['error_cut'][0]}$--${U['error_cut'][1]}\%$ less error on "
                         rf"six classification tasks; \ ${U['labelled']}$ labelled examples matched training from "
                         rf"scratch on ${U['equiv']}\times$ more", width=6.3, color=PRIOR)
        e = history_card(2018, r"ELMo \ (Peters et al.; AI2, U.\ Washington)",
                         r"two language models, reading forward and backward; their internal states become word "
                         r"vectors that depend on the sentence: \ better results on six tasks", width=6.3, color=ENCODER)
        VGroup(u, e).arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to(UP * 1.6)
        # ULMFiT's three stages
        st = VGroup(*[node_box(t, c, font_size=18) for t, c in ((r"language model \\ on Wikipedia", PRIOR),
                                                                (r"language model \\ on the task's text", PRIOR),
                                                                (r"classifier, \\ unfrozen layer by layer", C.REWARD))])
        st.arrange(RIGHT, buff=0.45).move_to([-3.2, -1.3, 0])
        st_arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, stroke_width=2.5, color=GREY_B)
                             for a, b in zip(st, st[1:])])
        st_note = label(rf"${U['labelled']}$ labelled examples did as well as ${U['labelled'] * U['equiv']:,}$ "
                        r"from scratch".replace(",", "{,}"), font_size=22, color=C.REWARD).next_to(st, DOWN, buff=0.35)
        # one word, two contexts, two vectors (schematic)
        s1 = data_text("the bank of the river", font=MONO, font_size=22, color=WHITE)
        s2 = data_text("the bank raised its rates", font=MONO, font_size=22, color=WHITE)
        sents = VGroup(s1, s2).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([2.2, -1.2, 0])
        h1 = SurroundingRectangle(s1[3:7], color=ENCODER, buff=0.05)
        h2 = SurroundingRectangle(s2[3:7], color=DECODER, buff=0.05)
        o = np.array([5.2, -2.6, 0])
        v1 = Arrow(o, o + np.array([0.6, 1.5, 0]), buff=0, color=ENCODER, stroke_width=5)
        v2 = Arrow(o, o + np.array([1.5, 0.3, 0]), buff=0, color=DECODER, stroke_width=5)
        vl = label(r"two vectors \\ for one word", font_size=20, color=GREY_A).next_to(o, LEFT, buff=0.3)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "January 2018: Jeremy Howard and Sebastian Ruder's ULMFiT. They pretrained a recurrent language model on "
            "Wikipedia, a hundred and three million words, then fine-tuned it on text classification, carefully, "
            "layer by layer. It cut the error of the best systems by 18 to 24 percent, and with only a hundred "
            "labelled examples it matched training from scratch on a hundred times as many. <bookmark mark='a'/> "
            "February 2018: ELMo, from the Allen Institute and the University of Washington. Two language models, one "
            "reading forward and one backward, whose internal states became word vectors that depend on the sentence. "
            "<bookmark mark='b'/> The bank of a river and the bank that sets interest rates get different vectors. "
            "Added to existing models, they improved the best results on six different tasks."
        ) as vo:
            self.play(FadeIn(u, shift=UP * 0.15))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(b), *([GrowArrow(st_arrows[i - 1])] if i else []))
                                    for i, b in enumerate(st)], lag_ratio=0.6), run_time=3.0)
            self.play(FadeIn(st_note))
            vo.wait_until("a")
            self.play(FadeIn(e, shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(sents), Create(h1), Create(h2), FadeIn(tag))
            self.play(GrowArrow(v1), GrowArrow(v2), FadeIn(vl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gpt1(self):
        G = F.GPT1
        card = config_card(F.CFG["gpt1"], rows=("layers", "d", "heads", "ctx", "params"), width=4.4).move_to([-4.3, 0.5, 0])
        hc = history_card(2018, r"GPT \ (Radford, Narasimhan, Salimans \& Sutskever; OpenAI)",
                          rf"the Transformer's decoder alone, \ pretrained on BooksCorpus: \ over ${G['books']:,}$ "
                          r"unpublished books".replace(",", "{,}"), width=7.6, color=DECODER).move_to([2.6, 2.4, 0])
        # the input transformations: every task as one sequence through the same network
        def seq(parts):
            return VGroup(*[chip(t, c, font_size=18, mono=False) for t, c in parts]).arrange(RIGHT, buff=0.06)

        S, D_, X = (r"start", GREY_B), (r"delim", GREY_B), (r"extract", GREY_B)
        rows = VGroup(
            VGroup(label(r"classification", font_size=20, color=GREY_A), seq([S, (r"text", WHITE), X])),
            VGroup(label(r"entailment", font_size=20, color=GREY_A),
                   seq([S, (r"premise", WHITE), D_, (r"hypothesis", WHITE), X])),
            VGroup(label(r"multiple choice", font_size=20, color=GREY_A),
                   seq([S, (r"context", WHITE), D_, (r"answer $k$", WHITE), X])),
        )
        for k, r in enumerate(rows):
            y = 0.6 - 0.75 * k
            r[0].move_to([1.5, y, 0], aligned_edge=RIGHT)
            r[1].move_to([1.75, y, 0], aligned_edge=LEFT)
        arrow_note = label(r"$\to$ \ the same 12-layer decoder \ $\to$ \ a new linear layer on the last token",
                           font_size=20, color=DECODER).next_to(rows, DOWN, buff=0.3)
        sota = label(rf"new state of the art on ${G['sota']}$ of ${G['tasks']}$ tasks", font_size=30,
                     color=DECODER).to_edge(DOWN, buff=0.7)
        tag = note(r"schematic, \ after Radford et al.\ (2018), Figure 1").to_corner(DR, buff=0.2)
        with self.voiceover(
            "June 2018: OpenAI's GPT, by Alec Radford and colleagues. Instead of a recurrent network, the "
            "Transformer's decoder alone. <bookmark mark='a'/> Twelve layers, a width of 768, twelve heads, 117 "
            "million parameters, pretrained on BooksCorpus, over seven thousand unpublished books, to predict the next "
            "token from the 512 before it. <bookmark mark='b'/> Then one model is fine-tuned for each task, with "
            "every input written as a single sequence: for entailment, the premise, a delimiter, the hypothesis; for "
            "multiple choice, the context with each answer in turn. A new linear layer reads the last position. "
            "<bookmark mark='c'/> It set a new state of the art on nine of the twelve tasks it was tested on."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeIn(card, shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.4), FadeIn(tag))
            self.play(FadeIn(arrow_note))
            vo.wait_until("c")
            self.play(FadeIn(sota, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def objective(self):
        rows = [
            cmath(r"\mathcal L_1", r"=", r"\sum_i \log P(u_i \mid u_{i-k}, \dots, u_{i-1})", font_size=38),
            cmath(r"\mathcal L_2", r"=", r"\sum_{(x, y)} \log P(y \mid x_1, \dots, x_m)", font_size=38),
            cmath(r"\mathcal L_3", r"=", r"\mathcal L_2 + \lambda\, \mathcal L_1", font_size=38),
            cmath(r"\lambda", r"=", r"0.5", font_size=38),
        ]
        rows[0][0].set_color(C.DATA)
        rows[1][0].set_color(DECODER)
        whys = [why(r"pretraining: \ the guessing game of Part 1, \ on raw text"),
                why(r"fine-tuning: \ the label, from the last token's state"),
                why(r"keep predicting text while fine-tuning"),
                why(r"Radford et al.\ (2018), Sec.\ 4.1")]
        step = ladder(self, rows, whys, keep=4, top=2.6, x=-2.6, buff=0.55, edge=6.9)
        tw = take_away(r"pretrain once, \ fine-tune many times", font_size=30)
        with self.voiceover(
            "Written as objectives: <bookmark mark='a'/> pretraining maximizes the log-probability of each token "
            "given the ones before it, the chain rule of Part 1 on raw text. <bookmark mark='b'/> Fine-tuning "
            "maximizes the log-probability of the right label given the input sequence. <bookmark mark='c'/> And GPT "
            "kept the first objective on as a helper while fine-tuning, <bookmark mark='d'/> weighted by one half: it "
            "made learning faster and the result generalize better. <bookmark mark='e'/> Pretrain once, fine-tune many "
            "times: that was the recipe of 2018."
        ) as vo:
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            self.play(FadeIn(tw))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_step(self):
        words = ["the", "man", "went", "to", "the", "store"]
        toks = VGroup(*[chip(w, GREY_B, font_size=22) for w in words]).arrange(RIGHT, buff=0.12).move_to(UP * 1.0)
        tgt = toks[3]
        left = VGroup(*[CurvedArrow(t.get_top() + UP * 0.05, tgt.get_top() + UP * 0.05, angle=-1.0, color=DECODER,
                                    stroke_width=2.5, tip_length=0.14) for t in toks[:3]])
        right = VGroup(*[CurvedArrow(t.get_bottom() + DOWN * 0.05, tgt.get_bottom() + DOWN * 0.05, angle=-1.0,
                                     color=ENCODER, stroke_width=2.5, tip_length=0.14) for t in toks[4:]])
        ll = label(r"GPT: \ each word's state sees only the words before it", font_size=26, color=DECODER)
        ll.next_to(toks, UP, buff=1.0)
        rl = label(r"but understanding often needs the words after it, too", font_size=26, color=ENCODER)
        rl.next_to(toks, DOWN, buff=1.0)
        nxt = label(r"October 2018: \ Google's answer, \ BERT", font_size=32, color=ENCODER).to_edge(DOWN, buff=0.7)
        tag = note(r"illustrative").to_corner(DR, buff=0.25)
        with self.voiceover(
            "What remained open was the objective. GPT predicts from left to right, so each word's representation is "
            "built only from the words before it. <bookmark mark='a'/> For tasks like question answering, where the "
            "meaning of a word can depend on what comes after it, that looked like a handicap. <bookmark mark='b'/> "
            "Four months later, Google had an answer: BERT."
        ) as vo:
            self.play(FadeIn(toks), FadeIn(ll), FadeIn(tag), LaggedStart(*[Create(a) for a in left], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(FadeIn(rl), LaggedStart(*[Create(a) for a in right], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
