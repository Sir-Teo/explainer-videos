from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.common import (EDU, F, KEPT, PAGE, PART, REMOVED, hbars, load, said, spoken_int, stage_row)


class Quality(VoiceoverScene):
    def construct(self):
        self.card()
        self.fineweb_edu()
        self.ours()
        self.applied()
        self.contamination()

    def card(self):
        card = chapter_card(4, r"Quality, \ and keeping the test clean", r"Which pages are worth learning from?",
                            part=PART)
        with self.voiceover("Chapter four. Quality, and keeping the test clean."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def fineweb_edu(self):
        E = F.FINEWEB_EDU
        row = stage_row([(r"a web page", PAGE), (r"Llama 3 70B: \ a score from $0$ to $5$", EDU),
                         (r"a small model learns the scores", C.PROB), (r"keep $\ge 3$", KEPT)], font_size=21)
        row.move_to(UP * 2.3)
        if row.width > 13.2:
            row.width = 13.2
        prompt = VGroup(
            label(r"$+1$ \ some basic information relevant to educational topics", font_size=20, color=GREY_A),
            label(r"$+1$ \ addresses certain elements pertinent to education", font_size=20, color=GREY_A),
            label(r"$+1$ \ appropriate for educational use, \ introduces key concepts of a curriculum", font_size=20,
                  color=GREY_A),
            label(r"$+1$ \ highly relevant and beneficial, \ for a level not higher than grade school", font_size=20,
                  color=GREY_A),
            label(r"$+1$ \ outstanding in its educational value, \ suited to teaching at school", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        ph = label(r"the annotator's additive prompt \ (paraphrased)", font_size=20, color=EDU)
        pg = VGroup(ph, prompt).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-3.2, -0.5, 0])
        nums = VGroup(
            label(rf"${E['annotated'] // 1000}$k pages scored by {E['annotator']}", font_size=22, color=EDU),
            label(rf"a linear head on an embedding model, \ trained on ${E['train'] // 1000}$k", font_size=22,
                  color=C.PROB),
            label(rf"F1 at the threshold $3$: \ ${E['f1']}\%$", font_size=22, color=C.PROB),
            label(rf"run over FineWeb's $15$T tokens: \ ${E['gpu_hours']:,}$ H100 hours".replace(",", "{,}"),
                  font_size=22, color=GREY_A),
            label(rf"FineWeb-Edu: \ ${E['tokens'] / 1e12:.1f}$T tokens", font_size=26, color=KEPT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.6, -0.4, 0])
        res = label(rf"a ${E['model'] / 1e9:.2f}$B model on ${E['ablation_tokens'] / 1e9:.0f}$B tokens: \ "
                    rf"MMLU ${E['mmlu'][0]}\% \to {E['mmlu'][1]}\%$, \ ARC ${E['arc'][0]}\% \to {E['arc'][1]}\%$",
                    font_size=24, color=KEPT).to_edge(DOWN, buff=0.85)
        src = cite(r"Penedo et al., \textit{The FineWeb Datasets} (2024), Sec.\ 4; \ prompt after Yuan et al.\ (2024)",
                   font_size=17)
        with self.voiceover(
            "Language and duplicates are the easy filters. Quality is harder: which pages teach a model the most? "
            "In 2024 Hugging Face's FineWeb team answered with a recipe that is now standard. <bookmark mark='a'/> "
            "Ask a large model to grade pages. They gave Llama 3 70B a prompt that adds a point for each of five "
            "criteria of educational value, and had it score 460 thousand pages from zero to five. "
            "<bookmark mark='b'/> Then train a small, cheap model to imitate those scores: a linear layer on top of "
            "an embedding model, trained on 410 thousand of them. At the threshold three, it agrees with Llama 3's "
            "verdict with an F1 score of 82 percent. <bookmark mark='c'/> Run the small model over all fifteen "
            "trillion tokens, which took six thousand GPU-hours, and keep the pages scored three or more: 1.3 "
            "trillion tokens. <bookmark mark='d'/> On models of 1.7 billion parameters trained on 350 billion tokens, "
            "the filtered data raised MMLU, a test of knowledge, from 33 to 37 percent, and ARC, a test of "
            "reasoning, from 46 to 57."
        ) as vo:
            self.play(FadeIn(row.boxes[0]), FadeIn(src))
            vo.wait_until("a")
            self.play(GrowArrow(row.arrows[0]), FadeIn(row.boxes[1]), FadeIn(pg), FadeIn(nums[0]))
            vo.wait_until("b")
            self.play(GrowArrow(row.arrows[1]), FadeIn(row.boxes[2]), FadeIn(nums[1]), FadeIn(nums[2]))
            vo.wait_until("c")
            self.play(GrowArrow(row.arrows[2]), FadeIn(row.boxes[3]), FadeIn(nums[3]), FadeIn(nums[4]))
            vo.wait_until("d")
            self.play(FadeIn(res, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        Q, E = load("quality"), F.FINEWEB_EDU
        counts = Q["all_labels"]
        mx = max(counts)
        bars = VGroup()
        for k, n in enumerate(counts):
            h = 3.0 * n / mx
            b = Rectangle(width=0.6, height=max(h, 0.02), stroke_width=0, fill_color=KEPT if k >= 3 else EDU,
                          fill_opacity=0.85).move_to([-5.6 + 0.85 * k, -2.2, 0], aligned_edge=DOWN)
            bars.add(VGroup(b, label(str(k), font_size=20, color=GREY_A).next_to(b, DOWN, buff=0.1),
                            label(f"${n:,}$".replace(",", "{,}"), font_size=18, color=GREY_A).next_to(b, UP, buff=0.06)))
        bl = label(rf"Llama 3's scores for ${Q['n']:,}$ pages we downloaded".replace(",", "{,}"), font_size=22,
                   color=EDU).next_to(bars, UP, buff=0.35).align_to(bars, LEFT)
        how = VGroup(
            label(rf"fastText on word pairs, \ trained on ${Q['n_train']:,}$ pages".replace(",", "{,}"), font_size=22),
            label(r"seconds on one core", font_size=22, color=GREY_A),
            label(rf"keep if $\Pr[\text{{score}} \ge 3] \ge {Q['cut']:.2f}$, \ the cut chosen on ${Q['n_val']:,}$ "
                  rf"other pages".replace(",", "{,}"), font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.2, 1.9, 0])
        f1 = Q["f1"]
        cmp_ = hbars([(r"FineWeb-Edu's classifier", E["f1"] / 100, C.PROB), (r"ours", f1, EDU)], 1.0, width=3.4,
                     font_size=22, label_width=3.0, fmt=lambda v: rf"${100 * v:.0f}\%$")
        cmp_.move_to([3.6, -0.8, 0])
        ch = label(rf"F1 at score $\ge 3$, \ on ${Q['n_test']:,}$ held-out pages".replace(",", "{,}"), font_size=20,
                   color=GREY_A).next_to(cmp_, UP, buff=0.25)
        pr = label(rf"precision ${100 * Q['precision']:.0f}\%$, \ recall ${100 * Q['recall']:.0f}\%$", font_size=20,
                   color=GREY_B).next_to(cmp_, DOWN, buff=0.25)
        if f1 > E["f1"] / 100 - 0.05:
            verdict = (f"Ours reaches an F1 of {100 * f1:.0f} percent, close to theirs, from a fraction of the labels.")
        else:
            verdict = (f"Ours reaches an F1 of {100 * f1:.0f} percent, against their 82: with a thirtieth of the labels "
                       "and a bag of words instead of an embedding model, it catches most of the good pages but lets "
                       "through about as many bad ones.")
        tag = note(r"computed: \ Llama 3's labels from FineWeb-Edu's released annotations").to_corner(DR, buff=0.2)
        with self.voiceover(
            "We can run this recipe ourselves, because FineWeb released Llama 3's annotations. <bookmark mark='a'/> "
            f"We downloaded {spoken_int(Q['n'])} of them. Most pages score one: a little information, not much "
            f"teaching. Only {100 * sum(counts[3:]) / Q['n']:.0f} percent score three or more, and none of ours scored "
            "five. <bookmark mark='b'/> For the small model we used fastText, a linear model on words and word pairs "
            f"that trains in seconds, on {spoken_int(Q['n_train'])} pages, with the cut chosen on a thousand others. "
            "<bookmark mark='c'/> " + verdict
        ) as vo:
            self.play(FadeIn(bl), FadeIn(tag), LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1]),
                                                                           FadeIn(b[2])) for b in bars], lag_ratio=0.2),
                      run_time=2.5)
            vo.wait_until("a")
            self.play(Indicate(bars[1][0], color=YELLOW), *[Indicate(b[0], color=KEPT) for b in bars[3:]])
            vo.wait_until("b")
            self.play(FadeIn(how, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(ch), *[FadeIn(r_[0]) for r_ in cmp_], *[GrowFromEdge(r_[1], LEFT) for r_ in cmp_],
                      *[FadeIn(r_[2]) for r_ in cmp_], FadeIn(pr))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def applied(self):
        Q, E = load("quality"), F.FINEWEB_EDU
        best, worst = Q["best"][:2], Q["worst"][:2]
        hi = VGroup(*[said(e["text"], chars=50, font_size=16, max_lines=3, box_color=KEPT) for e in best])
        lo = VGroup(*[said(e["text"], chars=50, font_size=16, max_lines=3, box_color=REMOVED) for e in worst])
        hi.arrange(DOWN, buff=0.2)
        lo.arrange(DOWN, buff=0.2)
        hl = label(r"scored highest", font_size=24, color=KEPT)
        ll = label(r"scored lowest", font_size=24, color=REMOVED)
        left = VGroup(hl, hi).arrange(DOWN, buff=0.2)
        right = VGroup(ll, lo).arrange(DOWN, buff=0.2)
        both = VGroup(left, right).arrange(RIGHT, buff=0.4, aligned_edge=UP)
        if both.width > 13.4:
            both.width = 13.4
        both.to_edge(UP, buff=0.4)
        kept = label(rf"our crawl sample: \ ${Q['cc_kept_n']}$ of ${Q['cc_n']:,}$ English pages kept "
                     rf"(${100 * Q['cc_kept']:.1f}\%$)".replace(",", "{,}"), font_size=26, color=EDU)
        fw = label(rf"FineWeb-Edu kept ${E['tokens'] / 1e12:.1f}$T of FineWeb's $15$T tokens "
                   rf"(${100 * E['tokens'] / F.FINEWEB['tokens']:.1f}\%$)", font_size=24, color=GREY_A)
        dclm = label(rf"DCLM (2024): \ fastText trained to find instruction-like text; \ a ${F.DCLM['params'] / 1e9:.0f}$B "
                     rf"model, ${F.DCLM['tokens'] / 1e12:.1f}$T tokens, \ MMLU ${F.DCLM['mmlu']}\%$", font_size=22,
                     color=GREY_A)
        foot = VGroup(kept, fw, dclm).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.55)
        if foot.width > 13.2:
            foot.width = 13.2
        tag = note(r"computed: \ our classifier on our crawl sample", font_size=18).to_corner(UR, buff=0.15)
        with self.voiceover(
            "Now run it on our crawl sample. <bookmark mark='a'/> Here are the two pages it scores highest, "
            "<bookmark mark='b'/> and the two it scores lowest. <bookmark mark='c'/> "
            f"It keeps {Q['cc_kept_n']} of our {spoken_int(Q['cc_n'])} English pages, "
            f"{100 * Q['cc_kept']:.1f} percent. FineWeb-Edu kept about nine percent of FineWeb's tokens. "
            "<bookmark mark='d'/> Other recipes use other targets. DataComp-LM, DCLM, trained its fastText filter to "
            "find text that looks like instructions and good answers, and a seven-billion-parameter model on 2.6 "
            "trillion of its tokens reached 64 percent on MMLU. Every serious corpus of 2026 has a filter like these; "
            "most, like Qwen3's, have many."
        ) as vo:
            self.play(FadeIn(hl), FadeIn(ll), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(hi, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(lo, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(kept), FadeIn(fw))
            vo.wait_until("d")
            self.play(FadeIn(dclm))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def contamination(self):
        K = load("contamination")
        q = label(r"Is the test already in the training data?", font_size=36).to_edge(UP, buff=0.5)
        idea = VGroup(
            label(r"GPT-3's check (2020): \ any $13$-word sequence shared with the training text", font_size=24,
                  color=GREY_A),
            label(r"a hash of every $13$-gram of the training text; \ look up every $13$-gram of the test",
                  font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(q, DOWN, buff=0.4)
        res = VGroup(
            label(rf"the scoreboard's passage \ (\textit{{The Maltese Falcon}}, ch.~2): \ ${K['passage_hits']}$ of "
                  rf"${K['passage_grams']:,}$ \ $13$-grams found".replace(",", "{,}"), font_size=26, color=KEPT),
            label(rf"\ \ even $8$-word sequences: \ ${K['passage_hits8']}$ of ${K['passage_grams8']:,}$"
                  .replace(",", "{,}"), font_size=22, color=GREY_A),
            label(rf"held-out paragraphs of the thirty novels: \ ${K['valid_flagged']}$ of ${K['valid_paras']:,}$ "
                  r"share a $13$-gram".replace(",", "{,}"), font_size=26, color=EDU),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(DOWN * 0.6)
        ex = said(K["example"] or "", chars=70, font_size=18, max_lines=1, box_color=EDU).next_to(res, DOWN, buff=0.3)
        tag = note(rf"computed: \ ${K['train_grams'] / 1e6:.1f}$M distinct $13$-grams in the training text",
                   font_size=18).to_corner(DR, buff=0.2)
        src = cite(r"Brown et al.\ (2020), App.\ C", font_size=17)
        with self.voiceover(
            "One more filter, pointed the other way. If the questions of a benchmark are on the web, a model can pass "
            "it by memory. <bookmark mark='a'/> GPT-3's authors looked for any thirteen-word sequence shared between "
            "each test and the training text, and flagged what they found. <bookmark mark='b'/> We can check the "
            "series' own test. The scoreboard's passage, chapter two of The Maltese Falcon, has "
            f"{spoken_int(K['passage_grams'])} thirteen-word sequences; {K['passage_hits']} of them occur anywhere in "
            f"the thirty novels we train on, and only {K['passage_hits8']} of its eight-word sequences. Clean. "
            "<bookmark mark='c'/> Our held-out paragraphs are almost clean: "
            f"{K['valid_flagged']} of {spoken_int(K['valid_paras'])} share a sequence with the training text, like "
            "this one, a sentence that a novel repeats. The web isn't so kind: popular benchmarks are copied all "
            "over it, which is why labs now run checks like this on every test they report."
        ) as vo:
            self.play(FadeIn(q), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(idea[0]))
            self.play(FadeIn(idea[1]))
            vo.wait_until("b")
            self.play(FadeIn(res[0]), FadeIn(res[1]), FadeIn(tag))
            vo.wait_until("c")
            self.play(FadeIn(res[2]), FadeIn(ex))
        self.wait(0.3)
        self.clear_scene()
