from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import (CONTEXT, C_COL, DECODER, D_COL, N_COL, OPEN, PART, PRIOR, F, config_card, human,
                                   load, take_away)


class OpenWeights(VoiceoverScene):
    def construct(self):
        self.card()
        self.llama()
        self.overtrain()
        self.wave()
        self.china()

    def card(self):
        card = chapter_card(9, r"Open weights", r"What happened when anyone could download a strong model?",
                            lit=(2023, 2024), part=PART)
        with self.voiceover("Chapter nine. Open weights."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def llama(self):
        L = F.LLAMA
        hc = history_card(2023, r"LLaMA \ (Touvron et al.; Meta, 24 February)", r"four models trained only on publicly "
                          r"available data; \ weights released to researchers", width=7.6, color=OPEN).to_edge(UP, buff=0.3)
        head = VGroup(*[label(t, font_size=22, color=GREY_A) for t in (r"model", r"parameters", r"tokens")])
        rows = [head] + [VGroup(label(rf"LLaMA-{nm}", font_size=24, color=OPEN), label(human(n), font_size=28),
                                label(human(d), font_size=28)) for nm, n, d in L["sizes"]]
        tab = VGroup(*rows)
        for k, r in enumerate(tab):
            for j, x in enumerate((-2.2, 0.0, 2.0)):
                r[j].move_to([x, -0.55 * k, 0])
        tab.move_to([-3.2, -0.6, 0])
        beat = VGroup(label(r"LLaMA-13B outperformed \\ the 175B GPT-3 \\ on most benchmarks", font_size=30, color=OPEN),
                      label(r"$13$B against $175$B: \ more than $13\times$ smaller", font_size=22, color=GREY_A))
        beat.arrange(DOWN, buff=0.3).move_to([3.5, -0.6, 0])
        eco = label(r"and on its weights: \ Alpaca, Vicuna, \ and thousands of fine-tunes", font_size=22,
                    color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "February 2023. Hugo Touvron and colleagues at Meta released LLaMA: four models, from seven to sixty-five "
            "billion parameters, trained only on publicly available data, one to one point four trillion tokens. "
            "<bookmark mark='a'/> The headline result: LLaMA-13B outperformed the 175-billion-parameter GPT-3 on most "
            "benchmarks, at more than thirteen times smaller. <bookmark mark='b'/> The weights went to researchers, "
            "and a whole open ecosystem was built on them within weeks: Stanford's Alpaca, Vicuna, and many more, "
            "fine-tuned on single machines."
        ) as vo:
            self.play(FadeIn(hc, shift=DOWN * 0.1), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in tab],
                                                                 lag_ratio=0.25), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(beat, shift=LEFT * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(eco))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def overtrain(self):
        P = load("published")
        Ch = F.CHINCHILLA
        tpp = {r["name"]: r for r in P["tpp"]}
        sel = [("GPT-3", PRIOR), ("Chinchilla", C.TRUE_P), ("LLaMA-65B", OPEN), ("LLaMA-7B", OPEN)]
        g = axes([-0.5, 3.5], [0, 2.5], x_length=6.4, y_length=4.0, ylabel=r"training tokens per parameter \ (log)",
                 yticks=[0, 1, 2], yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-2.6, -0.4, 0])
        ax = g.ax
        bars = VGroup()
        for k, (nm, col) in enumerate(sel):
            r = tpp[nm]["ratio"]
            h = ax.c2p(0, math.log10(r))[1] - ax.c2p(0, 0)[1]
            b = Rectangle(width=0.9, height=max(h, 0.02), stroke_width=0, fill_color=col, fill_opacity=0.9)
            b.move_to(ax.c2p(k, 0), aligned_edge=DOWN)
            v = MathTex(f"{r:.1f}" if r < 10 else f"{r:.0f}", font_size=26, color=col).next_to(b, UP, buff=0.08)
            n = label(nm, font_size=20, color=GREY_A).next_to(b, DOWN, buff=0.12)
            bars.add(VGroup(b, v, n))
        opt = DashedLine(ax.c2p(-0.5, math.log10(Ch["per_param"])), ax.c2p(3.5, math.log10(Ch["per_param"])),
                         color=C.TRUE_P, dash_length=0.08)
        ol = VGroup(label(rf"Chinchilla: \ about ${Ch['per_param']}$ tokens per parameter", font_size=24,
                          color=C.TRUE_P),
                    label(r"compute-optimal: \ the best model \\ for a fixed training budget", font_size=20,
                          color=C.TRUE_P)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        ol.next_to(opt.get_end(), RIGHT, buff=0.25).align_to(opt, UP).shift(UP * 0.17)
        side = VGroup(
            ol,
            label(r"over-trained: \ a smaller model, \\ trained longer, \ costs more to train \\ but less to run, "
                  r"for every token it ever serves", font_size=24, color=OPEN),
            label(r"the trade-off, \ derived: \ Part 12", font_size=22, color=GREY_B),
        )
        side[1].next_to(ol, UP, buff=0.55).align_to(ol, LEFT)
        side[2].next_to(ol, DOWN, buff=0.7).align_to(ol, LEFT)
        title = label(r"how did a smaller model win?", font_size=34).to_edge(UP, buff=0.4)
        cite_ = cite(r"Brown et al.\ (2020); \ Hoffmann et al.\ (2022); \ Touvron et al.\ (2023): \ tokens $\div$ parameters")
        r7 = tpp["LLaMA-7B"]["ratio"]
        with self.voiceover(
            "How could a 13-billion-parameter model beat GPT-3? By reading far more text per parameter. "
            "<bookmark mark='a'/> GPT-3 saw about 1.7 tokens for each of its parameters. <bookmark mark='b'/> In 2022, "
            "DeepMind's Chinchilla paper had shown that for a fixed training budget, the best model sees about twenty "
            "tokens per parameter: GPT-3 was far too big for its data. <bookmark mark='c'/> LLaMA went past even that. "
            f"Its 7-billion-parameter model saw about {r7:.0f} tokens per parameter. <bookmark mark='d'/> That is more "
            "training than compute-optimal: you could have trained a better model with the same budget. But a smaller "
            "model is cheaper to run, for every token it ever serves, and once millions of people use a model, "
            "running it costs far more than training it. Part 12 derives the trade."
        ) as vo:
            self.play(FadeIn(title), FadeIn(g), FadeIn(cite_))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1]), FadeIn(bars[0][2]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1]), FadeIn(bars[1][2]), Create(opt))
            self.play(FadeIn(ol))
            vo.wait_until("c")
            self.play(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1]), FadeIn(b[2])) for b in bars[2:]])
            vo.wait_until("d")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wave(self):
        L2, Mx = F.LLAMA2, F.MIXTRAL
        cards = VGroup(
            history_card(2023, r"Llama 2 \ (Meta, July)", rf"${L2['tokens'] / 1e12:.0f}$ trillion tokens, \ "
                         rf"${L2['more']}\%$ more; \ context ${L2['ctx']:,}$; \ chat versions tuned with RLHF; \ "
                         r"commercial use allowed".replace(",", "{,}"), width=6.4, color=OPEN),
            history_card(2023, r"Mistral 7B \ (Mistral AI, September)", r"Apache 2.0: \ beat Llama 2 13B, \ with "
                         rf"grouped-query attention and a ${F.MISTRAL['window']:,}$-token sliding window".replace(",", "{,}"),
                         width=6.4, color=OPEN),
            history_card(2023, r"Mixtral 8x7B \ (Mistral AI, December)", rf"${Mx['experts']}$ experts per layer, "
                         rf"${Mx['top']}$ chosen per token: \ ${Mx['total'] / 1e9:.0f}$B parameters, "
                         rf"${Mx['active'] / 1e9:.0f}$B used per token; \ matched or beat Llama 2 70B and GPT-3.5",
                         width=6.4, color=OPEN),
            history_card(2024, r"Llama 3.1 \ (Meta, July)", rf"$405$B parameters, ${F.LLAMA3['tokens'] / 1e12:.1f}$T "
                         rf"tokens, ${sci(F.LLAMA3['flops'], 1)}$ operations on up to ${F.LLAMA3['gpus']:,}$ GPUs"
                         .replace(",", "{,}"), width=6.4, color=OPEN),
        ).arrange_in_grid(rows=2, cols=2, buff=0.3).move_to(UP * 0.1)
        head = label(r"the open wave, \ 2023 to 2024", font_size=34, color=OPEN).to_edge(UP, buff=0.45)
        stat = label(rf"in ${F.LLAMA3['days']}$ days of that run: \ ${F.LLAMA3['interruptions']}$ interruptions, \ "
                     rf"${F.LLAMA3['unexpected']}$ unexpected \ (Part 18)", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Then came a wave. <bookmark mark='a'/> In July 2023, Llama 2: two trillion tokens, forty percent more, "
            "twice the context, chat versions tuned with RLHF, and a license that allowed commercial use. "
            "<bookmark mark='b'/> In September, Mistral 7B, from a young company in Paris, under the Apache license. "
            "It beat Llama 2's 13-billion-parameter model, with grouped-query attention and a sliding window, both "
            "explained in the next chapter. <bookmark mark='c'/> In December, Mixtral: every layer has eight "
            "feed-forward experts, and a router picks two for each token, so the model holds forty-seven billion "
            "parameters but uses thirteen billion per token. It matched or beat Llama 2 70B and GPT-3.5. Mixtures of "
            "experts are Part 16. <bookmark mark='d'/> And in July 2024, Meta's Llama 3.1: 405 billion parameters, "
            "15.6 trillion tokens, 3.8 times ten to the twenty-five operations, on up to sixteen thousand GPUs. "
            "<bookmark mark='e'/> Its report even counted the failures: 466 interruptions in fifty-four days. "
            "Frontier-scale training, documented in public."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(stat))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def china(self):
        D2 = F.DSV2
        cards = VGroup(
            history_card(2023, r"Qwen \ (Alibaba)", r"from 2023; \ Qwen2.5, late 2024, trained on $18$ trillion "
                         r"tokens, \ open weights from small to large", width=6.4, color=OPEN),
            history_card(2024, r"DeepSeek-V2 \ (DeepSeek, May)", rf"${D2['total'] / 1e9:.0f}$B parameters, "
                         rf"${D2['active'] / 1e9:.0f}$B per token; \ multi-head latent attention: \ the memory of past "
                         rf"tokens ${D2['kv_cut']}\%$ smaller", width=6.4, color=OPEN),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(UP * 1.0)
        lead = label(r"by 2025 the strongest open models came from China: \ DeepSeek, Qwen, Kimi, GLM", font_size=28,
                     color=OPEN).move_to(DOWN * 0.8)
        tw = take_away(r"open weights let everyone read the configurations: \ next, \ what they converged on",
                       color=OPEN, font_size=26)
        cite_ = cite(r"Qwen Team (2024); \ DeepSeek-AI (2024)")
        head = label(r"open models from China", font_size=34, color=OPEN).to_edge(UP, buff=0.45)
        with self.voiceover(
            "And from China came open models that would soon lead. <bookmark mark='a'/> Alibaba's Qwen family began "
            "in 2023; by late 2024 Qwen2.5 was trained on eighteen trillion tokens, in sizes from tiny to large. "
            "<bookmark mark='b'/> DeepSeek's V2, in May 2024, had 236 billion parameters but used only 21 billion for "
            "each token, and a new kind of attention, multi-head latent attention, that cut the memory kept for past "
            "tokens by 93 percent. <bookmark mark='c'/> By 2025, the strongest open models came from Chinese labs: "
            "DeepSeek, Qwen, Moonshot's Kimi and Zhipu's GLM. <bookmark mark='d'/> Open weights mean open "
            "configurations. In the next chapter we read them side by side."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(lead))
            vo.wait_until("d")
            self.play(FadeIn(tw))
        self.wait(0.3)
        self.clear_scene()
