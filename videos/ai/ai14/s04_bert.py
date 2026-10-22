from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import (DECODER, ENCDEC, ENCODER, HUMAN, MONO, PART, PRIOR, F, arch_diagram, chip,
                                   config_card, take_away)


class BERT(VoiceoverScene):
    def construct(self):
        self.card()
        self.masking()
        self.loss()
        self.results()
        self.race()

    def card(self):
        card = chapter_card(3, r"Masked language models and the benchmark era",
                            r"What if every word could see the whole sentence?", lit=(2018,), part=PART)
        with self.voiceover("Chapter three. Masked language models, and the benchmark era."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def masking(self):
        B = F.BERT
        hc = history_card(2018, r"BERT \ (Devlin, Chang, Lee \& Toutanova; Google)",
                          r"the Transformer's encoder alone: \ every position sees the whole input, both ways",
                          width=8.0, color=ENCODER).to_edge(UP, buff=0.35)
        words = ["my", "dog", "is", "hairy", "and", "my", "cat", "is", "not"]
        row = VGroup(*[chip(w, GREY_B, font_size=24) for w in words]).arrange(RIGHT, buff=0.1).move_to(UP * 0.45)
        # which positions are picked (15%), and what happens to each: [MASK] (80%), a random word (10%), kept (10%)
        picks = {3: ("[MASK]", ENCODER), 6: ("apple", C.SURPRISE), 8: ("not", C.INTERVAL)}
        row2 = VGroup(*[chip(picks[i][0], picks[i][1], font_size=24) if i in picks else chip(w, GREY_B, font_size=24)
                        for i, w in enumerate(words)]).arrange(RIGHT, buff=0.1).move_to(row)
        tags = VGroup(*[label(t, font_size=20, color=c).next_to(row2[i], DOWN, buff=0.25) for i, t, c in
                        ((3, rf"${B['mask_split'][0]}\%$: \ mask", ENCODER),
                         (6, rf"${B['mask_split'][1]}\%$: \ random word", C.SURPRISE),
                         (8, rf"${B['mask_split'][2]}\%$: \ kept", C.INTERVAL))])
        pick_l = label(rf"pick ${int(B['mask'] * 100)}\%$ of the positions at random", font_size=26, color=WHITE)
        pick_l.next_to(row, UP, buff=0.5)
        enc = arch_diagram("encoder", 1.1).move_to([-4.4, -2.0, 0])
        goal = label(r"train it to recover the original word \\ at every picked position", font_size=26,
                     color=ENCODER).move_to([1.2, -2.0, 0])
        nsp = label(r"and a second task: \ does passage B follow passage A?", font_size=22, color=GREY_A)
        nsp.next_to(goal, DOWN, buff=0.35)
        tag = note(r"example after Devlin et al.\ (2018), App.\ A.1").to_corner(DR, buff=0.2)
        with self.voiceover(
            "October 2018: Jacob Devlin, Ming-Wei Chang, Kenton Lee and Kristina Toutanova at Google. BERT keeps the "
            "Transformer's encoder alone, so every position sees the whole input, both ways. <bookmark mark='a'/> But "
            "a model that sees everything can't be trained to predict the next word: it would simply look at it. So "
            "BERT hides words instead. Pick fifteen percent of the positions at random. <bookmark mark='b'/> Replace "
            "eighty percent of those with a special mask token, ten percent with a random word, and leave ten percent "
            "unchanged. <bookmark mark='c'/> Then train the model to recover the original word at each picked "
            "position. The random and unchanged words matter: when the model is later fine-tuned there are no mask "
            "tokens, so it can't afford to think hard only where it sees one. <bookmark mark='d'/> A second task asked "
            "whether one passage really follows another."
        ) as vo:
            self.play(FadeIn(hc, shift=DOWN * 0.15), FadeIn(enc))
            vo.wait_until("a")
            self.play(FadeIn(row), FadeIn(pick_l), FadeIn(tag))
            self.play(*[Indicate(row[i], color=YELLOW) for i in picks])
            vo.wait_until("b")
            self.play(ReplacementTransform(row, row2))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tags], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(goal))
            vo.wait_until("d")
            self.play(FadeIn(nsp))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def loss(self):
        B = F.BERT
        rows = [
            cmath(r"\mathcal L_{\mathrm{LM}}", r"=", r"-\sum_{i=1}^{n} \log P(x_i \mid x_{<i})", font_size=38),
            cmath(r"\mathcal L_{\mathrm{MLM}}", r"=", r"-\sum_{i \in M} \log P(x_i \mid \tilde x)", font_size=38),
            cmath(r"\mathbb E\,|M|", r"=", rf"{B['mask']:g}\, n", font_size=38),
            cmath(r"\frac{n}{\mathbb E\,|M|}", r"=", rf"{1 / B['mask']:.1f}", font_size=38),
        ]
        rows[0][0].set_color(DECODER)
        rows[1][0].set_color(ENCODER)
        whys = [why(r"GPT: \ every position is a target, \ seen from the left"),
                why(r"BERT: \ only the picked positions $M$, \ seen from both sides of the corrupted $\tilde x$"),
                why(r"$15\%$ of the positions"),
                why(r"targets per sequence: \ the causal model gets more")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-2.8, buff=0.42, edge=6.9)
        note_ = label(r"BERT's own check: \ the masked model learns a little more slowly per step, \\ "
                      r"but beats the left-to-right model on the tasks almost at once", font_size=22, color=GREY_A)
        note_.to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Put the two objectives side by side. <bookmark mark='a'/> A left-to-right model like GPT makes every "
            "position a target, predicted from the words before it. <bookmark mark='b'/> The masked model's loss sums "
            "only over the picked positions, each predicted from the whole corrupted sentence. <bookmark mark='c'/> "
            "On average that is fifteen percent of the positions, <bookmark mark='d'/> so per sequence of text, the "
            "left-to-right model gets about six and a half times as many targets to learn from. <bookmark mark='e'/> "
            "BERT's authors measured the cost: their masked model learned slightly more slowly, step for step, but "
            "overtook a left-to-right model on the tasks almost immediately. We'll test that claim ourselves in "
            "chapter thirteen."
        ) as vo:
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        B = F.BERT
        card = config_card(F.CFG["bert"], rows=("layers", "d", "heads", "ctx", "params"), width=4.4).move_to([-4.4, 1.0, 0])
        glue = VGroup(label(r"GLUE score", font_size=26, color=WHITE),
                      VGroup(label(r"GPT", font_size=24, color=DECODER), MathTex(f"{B['glue_gpt']}", font_size=40,
                                                                                 color=DECODER)).arrange(RIGHT, buff=0.3),
                      VGroup(label(r"BERT-Large", font_size=24, color=ENCODER), MathTex(f"{B['glue_bert']}", font_size=40,
                                                                                        color=ENCODER)).arrange(RIGHT, buff=0.3))
        glue.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(card, DOWN, buff=0.45)
        # Table 5: the same BERT-Base, pretrained masked or left to right
        abl = B["ablation"]
        W, H = 0.36, 3.0
        x0 = 0.4
        bars = VGroup()
        lo = 70.0
        for k, (task, mlm, ltr) in enumerate(abl):
            x = x0 + 1.25 * k
            bm = Rectangle(width=W, height=H * (mlm - lo) / 25, stroke_width=0, fill_color=ENCODER, fill_opacity=0.9)
            bl = Rectangle(width=W, height=H * (ltr - lo) / 25, stroke_width=0, fill_color=DECODER, fill_opacity=0.9)
            bm.move_to([x - 0.2, -2.2, 0], aligned_edge=DOWN)
            bl.move_to([x + 0.2, -2.2, 0], aligned_edge=DOWN)
            vm = MathTex(f"{mlm:g}", font_size=18, color=ENCODER).next_to(bm, UP, buff=0.06)
            vl = MathTex(f"{ltr:g}", font_size=18, color=DECODER).next_to(bl, UP, buff=0.06)
            t = label(task, font_size=18, color=GREY_A).move_to([x, -2.5, 0])
            bars.add(VGroup(bm, bl, vm, vl, t))
        base = Line([x0 - 0.5, -2.2, 0], [x0 + 1.25 * 4 + 0.5, -2.2, 0], color=GREY_C, stroke_width=1.5)
        bt = label(r"the same BERT-Base, \ pretrained two ways", font_size=26, color=WHITE).move_to([3.0, 1.75, 0])
        lg = legend([(ENCODER, r"masked"), (DECODER, r"left to right, \ like GPT")], font_size=20)
        lg.next_to(bt, DOWN, buff=0.2)
        axis_note = note(rf"bars start at ${lo:g}$; \ dev-set scores, \ Devlin et al.\ (2018), Table 5", font_size=18)
        axis_note.next_to(base, DOWN, buff=0.45)
        facts_ = VGroup(label(rf"BERT-Base: \ $12$ layers, \ ${B['base_params'] / 1e6:.0f}$M parameters: \ GPT's size, "
                              r"\\ chosen for a fair comparison", font_size=24, color=ENCODER),
                        label(rf"data: \ $3.3$ billion words; \\ ${B['steps']:,}$ steps of ${B['batch_tokens']:,}$ tokens"
                              .replace(",", "{,}"), font_size=24, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        facts_.move_to([2.6, 0.6, 0])
        gap = abl[4][1] - abl[4][2]
        with self.voiceover(
            "BERT came in two sizes. Base: twelve layers and 110 million parameters, the same size as GPT, chosen so "
            "the two could be compared. Large: twenty-four layers and 340 million. Both trained on books and English "
            "Wikipedia, 3.3 billion words, for a million steps. <bookmark mark='a'/> On the GLUE leaderboard "
            "BERT-Large scored 80.5, against GPT's 72.8, and it set new records in question answering too. "
            "<bookmark mark='b'/> Better still, the authors checked where the gain came from. They pretrained the "
            "same Base model a second way, left to right like GPT, everything else equal. <bookmark mark='c'/> "
            "Masking won on all five tasks, by a little on sentiment, and by about "
            f"{round(gap)} points on question answering, where seeing the words after a word matters most."
        ) as vo:
            self.play(FadeIn(card, shift=RIGHT * 0.15), FadeIn(facts_, shift=LEFT * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(glue, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeOut(facts_), FadeIn(bt), FadeIn(lg), Create(base), FadeIn(axis_note))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), GrowFromEdge(b[1], DOWN), FadeIn(b[2]),
                                                   FadeIn(b[3]), FadeIn(b[4])) for b in bars], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def race(self):
        G, S = F.GLUE, F.SUPERGLUE
        cards = VGroup(
            history_card(2018, r"GLUE \ (Wang et al.)", rf"${G['tasks']}$ tasks, one score. \ By July 2019 the best "
                         rf"system scored ${G['sota_jul2019']}$, \ above the human estimate of ${G['human']}$",
                         width=6.2, color=PRIOR),
            history_card(2019, r"SuperGLUE \ (Wang et al.)", rf"harder tasks: \ BERT ${S['bert']}$, \ people "
                         rf"${S['human']}$; \ by October, T5 reached ${S['t5']}$", width=6.2, color=HUMAN),
            history_card(2019, r"RoBERTa \ (Liu et al.; Facebook)", r"BERT was undertrained: \ drop next-sentence "
                         r"prediction, train longer on more data, \ and it matches every model published after it",
                         width=6.2, color=ENCODER),
            history_card(2020, r"ELECTRA \ (Clark et al.; Stanford, Google)", r"a small network replaces words; the "
                         r"main one spots replacements, \ so it learns from every position, not $15\%$",
                         width=6.2, color=ENCODER),
        ).arrange_in_grid(rows=2, cols=2, buff=0.3).move_to(UP * 0.35)
        tw = take_away(r"encoders ruled understanding for two years; \ today they power search and retrieval",
                       color=ENCODER, font_size=26)
        cite_ = cite(r"Wang et al.\ (2018, 2019); \ Liu et al.\ (2019); \ Clark et al.\ (2020)", corner=UL)
        with self.voiceover(
            "BERT started a race on the benchmarks. <bookmark mark='a'/> GLUE combined nine tasks into one score; by "
            "July 2019 the best system had passed the estimate of human performance. <bookmark mark='b'/> So a harder "
            "benchmark, SuperGLUE, was built, with a human score of 89.8; BERT scored 69. Within months it too was "
            "nearly solved. <bookmark mark='c'/> RoBERTa, from Facebook, showed that BERT had simply been "
            "undertrained: drop the second task, train longer on more data, and it matched everything published after "
            "it. <bookmark mark='d'/> ELECTRA let a small network replace words and trained the main one to spot the "
            "replacements, so it learned from every position, not fifteen percent. <bookmark mark='e'/> Encoders ruled "
            "language understanding for two years, and they never went away: the embedding models behind search and "
            "retrieval are mostly encoders."
        ) as vo:
            self.play(FadeIn(cite_))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(tw))
        self.wait(0.3)
        self.clear_scene()
