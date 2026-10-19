from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai27.common import ADAPT, ASSIST, BASE, GOLD, PART, PENALTY, POLICY, REWARD, load


class LoRA(VoiceoverScene):
    def construct(self):
        self.card()
        self.intrinsic()
        self.lowrank()
        self.ours()
        self.family()

    def card(self):
        card = chapter_card(3, r"Low-rank adapters", r"How few numbers does fine-tuning really need to change?",
                            lit=(2021, 2023), part=PART)
        with self.voiceover("Chapter three. Low-rank adapters."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def intrinsic(self):
        rows = [
            cmath(r"\theta", r"=", r"\theta_0 + P\, z", font_size=40),
        ]
        rows[0][2].set_color(ADAPT)
        whys = [why(r"$P$: \ a fixed random $D \times d$ matrix; \ train only $z \in \mathbb R^d$")]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-2.0, buff=0.5, edge=6.9)
        hc = VGroup(
            history_card(2018, r"Li et al., \ intrinsic dimension", r"train in a random low-dimensional slice of "
                         r"weight space: \ many problems need surprisingly few dimensions", width=6.0, color=ADAPT),
            history_card(2020, r"Aghajanyan, Zettlemoyer \& Gupta", r"fine-tuning RoBERTa through $200$ numbers "
                         r"reached $90\%$ of full fine-tuning on a paraphrase task", width=6.0, color=ADAPT),
        ).arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Fine-tuning changes every one of a model's weights, and for a large model that means storing a full new "
            "copy for every task. But does it need to? <bookmark mark='a'/> In 2018 Chunyuan Li and colleagues "
            "trained networks in a random low-dimensional slice of weight space: the weights are the starting point "
            "plus a fixed random matrix times a small vector, and only the small vector learns. Many problems needed "
            "surprisingly few dimensions. <bookmark mark='b'/> In 2020 Armen Aghajanyan and colleagues showed that "
            "fine-tuning a pretrained language model is especially low-dimensional: about two hundred numbers got "
            "RoBERTa ninety percent of the way on a paraphrase task. Pretraining had done the hard part."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(hc[0], shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(hc[1], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lowrank(self):
        W = Square(2.6, stroke_color=BASE, stroke_width=2, fill_color=BASE, fill_opacity=0.15).move_to([-4.6, 0.6, 0])
        Wl = MathTex(r"W", font_size=40, color=BASE).move_to(W)
        Wd = MathTex(r"d \times k", font_size=24, color=GREY_B).next_to(W, DOWN, buff=0.15)
        plus = MathTex(r"+", font_size=44).move_to([-2.7, 0.6, 0])
        B = Rectangle(width=0.35, height=2.6, stroke_color=ADAPT, stroke_width=2, fill_color=ADAPT,
                      fill_opacity=0.35).move_to([-2.0, 0.6, 0])
        A = Rectangle(width=2.6, height=0.35, stroke_color=ADAPT, stroke_width=2, fill_color=ADAPT,
                      fill_opacity=0.35).move_to([-0.2, 1.725, 0])
        Bl, Al = MathTex(r"B", font_size=32, color=ADAPT).next_to(B, LEFT, buff=0.1), \
            MathTex(r"A", font_size=32, color=ADAPT).next_to(A, UP, buff=0.1)
        dims = VGroup(MathTex(r"d \times r", font_size=22, color=GREY_B).next_to(B, DOWN, buff=0.15),
                      MathTex(r"r \times k", font_size=22, color=GREY_B).next_to(A, RIGHT, buff=0.1))
        rows = VGroup(
            cmath(r"h", r"=", r"W x + \tfrac{\alpha}{r}\, B A\, x", font_size=36),
            cmath(r"\text{trained}", r":\ ", r"r(d + k)\ \text{ instead of }\ d k", font_size=32),
            cmath(r"d = k = 4096,\ r = 8", r":\ ", r"65{,}536 \text{ instead of } 16{,}777{,}216", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.6, -0.2, 0])
        rows[0][2].set_color(ADAPT)
        init = label(r"$B = 0$ at the start: \ training begins at the model itself; \ afterwards $W + BA$ is one matrix "
                     r"again", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.5)
        hc = note(r"Hu et al., \textit{LoRA: Low-rank adaptation of large language models} (Microsoft, 2021)")
        hc.to_corner(UL, buff=0.3)
        with self.voiceover(
            "LoRA, from Edward Hu and colleagues at Microsoft in 2021, builds that idea into the network. Freeze "
            "every weight matrix W. <bookmark mark='a'/> Next to each one, add the product of two thin matrices, B "
            "times A, of rank r, a handful. Only B and A are trained. <bookmark mark='b'/> A d by k matrix has d "
            "times k numbers; the adapter has r times d plus k. For a four-thousand-wide layer at rank eight, that's "
            "sixty-five thousand trainable numbers instead of sixteen million. <bookmark mark='c'/> B starts at zero, "
            "so training starts from the model exactly; and when it's done, B A can be added into W, so the adapted "
            "model runs as fast as the original."
        ) as vo:
            self.play(FadeIn(W), FadeIn(Wl), FadeIn(Wd), FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(plus), FadeIn(B), FadeIn(A), FadeIn(Bl), FadeIn(Al), FadeIn(dims), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(init))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        d = load("lora")
        runs = d["runs"]
        tot = d["total_params"]
        names = [rf"rank ${r['rank']}$" if r["rank"] != "full" else r"full" for r in runs]
        cols = [ADAPT] * (len(runs) - 1) + [ASSIST]
        x0, dx = -4.6, 2.0
        hdr = VGroup(label(r"", font_size=22),
                     label(r"trained numbers", font_size=22, color=GREY_A),
                     label(r"held-out sentences \\ placed right", font_size=22, color=GREY_A),
                     label(r"loss on novel text \\ (forgetting)", font_size=22, color=GREY_A))
        ys = [1.6, 0.6, -0.5, -1.6]
        for m, y in zip(hdr, ys):
            m.move_to([-5.6, y, 0])
        cells = VGroup()
        for i, (r, nm, c) in enumerate(zip(runs, names, cols)):
            x = x0 + 1.4 + dx * i
            frac = r["params"] / tot
            col = VGroup(label(nm, font_size=26, color=c).move_to([x, 2.5, 0]),
                         label(rf"${r['params']:,}$".replace(",", "{,}") + rf" \\ (${100 * frac:.2g}\%$)",
                               font_size=20, color=WHITE).move_to([x, ys[1] + 1.0, 0]),
                         label(rf"${100 * r['which']:.0f}\%$", font_size=26, color=WHITE).move_to([x, ys[2] + 1.0, 0]),
                         label(rf"${r['heldout']:.3f}$", font_size=26, color=WHITE).move_to([x, ys[3] + 1.0, 0]))
            cells.add(col)
        for m, y in zip(hdr[1:], ys[1:]):
            m.move_to([-5.4, y + 1.0, 0])
        base = note(rf"the base model's loss on novel text: \ ${d['base_heldout']:.3f}$ nats; \ computed").to_edge(
            DOWN, buff=0.4)
        full, r1 = runs[-1], runs[0]
        best = max(runs[:-1], key=lambda r: r["which"])
        forget_full = full["heldout"] - d["base_heldout"]
        forget_lora = min(r["heldout"] for r in runs[:-1]) - d["base_heldout"]
        with self.voiceover(
            "Our own experiment: fine-tune the novels model on the which-book task with LoRA at ranks one, four "
            "and sixteen, and with every weight. <bookmark mark='a'/> Rank one trains "
            f"{r1['params']:,} numbers, {100 * r1['params'] / tot:.2g} percent of the model. "
            f"<bookmark mark='b'/> Full fine-tuning gets {100 * full['which']:.0f} percent of held-out sentences right; "
            f"the best adapter, rank {best['rank']}, {100 * best['which']:.0f} percent. <bookmark mark='c'/> And on "
            f"ordinary novel text, full fine-tuning's loss is {forget_full:+.3f} nats from the base model's, the "
            f"adapters' as little as {forget_lora:+.3f}. LoRA learns less, and forgets less: the title of a 2024 "
            "study that found the same at scale."
        ) as vo:
            self.play(FadeIn(hdr), FadeIn(VGroup(*[c_[0] for c_ in cells])), FadeIn(base))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*[c_[1] for c_ in cells])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*[c_[2] for c_ in cells])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*[c_[3] for c_ in cells])))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def family(self):
        cards = VGroup(
            history_card(2021, r"LoRA on GPT-3", r"$10{,}000$ times fewer trained numbers than full fine-tuning, \ "
                         r"about a third of the GPU memory, \ comparable quality", width=6.2, color=ADAPT),
            history_card(2023, r"QLoRA \ (Dettmers et al.)", r"the frozen model stored in $4$ bits: \ a $65$-billion "
                         r"parameter model fine-tuned on one $48$ GB GPU", width=6.2, color=ADAPT),
            history_card(2024, r"DoRA \ (Liu et al.)", r"split each weight into a length and a direction; \ adapt the "
                         r"direction with LoRA", width=6.2, color=ADAPT),
            history_card(2024, r"Biderman et al.", r"``LoRA learns less and forgets less'': \ full fine-tuning wins on "
                         r"hard new skills, \ LoRA keeps more of the old ones", width=6.2, color=GOLD),
        ).arrange_in_grid(rows=2, cols=2, buff=0.35).move_to(UP * 0.1)
        cite_ = cite(r"Hu et al.\ (2021); \ Dettmers et al.\ (2023); \ Liu et al.\ (2024); \ Biderman et al.\ (2024)")
        with self.voiceover(
            "On GPT-3, LoRA trained ten thousand times fewer numbers than full fine-tuning, with about a third of the "
            "memory and comparable quality. <bookmark mark='a'/> QLoRA in 2023 stored the frozen model in four bits, "
            "and fine-tuned a sixty-five-billion-parameter model on a single forty-eight-gigabyte GPU, which put "
            "fine-tuning within reach of anyone with one good graphics card. <bookmark mark='b'/> DoRA splits each "
            "weight into a length and a direction and adapts the direction. <bookmark mark='c'/> And a careful 2024 "
            "comparison put the trade-off in its title: LoRA learns less and forgets less. For hard new skills, full "
            "fine-tuning still wins."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.15), FadeIn(cite_))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k + 1], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()
