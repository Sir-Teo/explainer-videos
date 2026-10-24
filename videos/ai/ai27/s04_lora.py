from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai27.common import ADAPT, ASSIST, BASE, GOLD, PART, PENALTY, POLICY, REWARD, load
from videos.ai.ai27.compute import LORA_LR, SFT_LR


def pct(x: float) -> str:
    """A share as a percentage with two significant figures, without exponents: 0.38, 6.1, 100."""
    v = 100 * x
    return f"{v:.2g}" if v < 10 else f"{v:.0f}"


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
        tot = int(load("lora")["total_params"])
        rows = [
            cmath(r"\theta", r"=", r"\theta_0 + \Delta\theta", font_size=40),
            cmath(r"\theta", r"=", r"\theta_0 + P\, z", font_size=40),
        ]
        rows[1][2].set_color(ADAPT)
        whys = [why(r"full fine-tuning: \ $\Delta\theta$ has every one of the model's numbers"),
                why(r"$P$: \ a fixed random $D \times d$ matrix; \ train only $z \in \mathbb R^d$")]
        step = ladder(self, rows, whys, keep=2, top=3.3, x=-2.6, buff=0.35, edge=6.9)

        def strip(n, color, opacity=0.45, w=0.21, h=0.3):
            return VGroup(*[Rectangle(width=w, height=h, stroke_color=color, stroke_width=1, fill_color=color,
                                      fill_opacity=opacity) for _ in range(n)]).arrange(RIGHT, buff=0)

        X0 = -3.3  # where every strip starts
        th0 = strip(40, BASE).move_to([X0, 0.95, 0], aligned_edge=LEFT)
        th0_l = label(rf"$\theta_0$: \ ${tot:,}$ numbers".replace(",", "{,}"), font_size=20, color=BASE)
        th0_l.next_to(th0, LEFT, buff=0.25)
        copies = VGroup()
        for k in range(3):
            st = strip(40, ASSIST, 0.3).move_to([X0, 0.35 - 0.5 * k, 0], aligned_edge=LEFT)
            copies.add(VGroup(st, label(rf"task {k + 1}: \ $\Delta\theta$", font_size=20, color=ASSIST)
                              .next_to(st, LEFT, buff=0.25)))
        cost = label(r"a full copy for every task", font_size=22, color=PENALTY).next_to(copies, DOWN, buff=0.2)
        z = strip(3, ADAPT, 0.8).move_to([X0, -0.35, 0], aligned_edge=LEFT)
        z_l = label(r"$z$: \ $d$ numbers, \ trained", font_size=20, color=ADAPT).next_to(z, LEFT, buff=0.25)
        pz = strip(40, ADAPT, 0.25).move_to([X0, 0.35, 0], aligned_edge=LEFT)
        pz_l = label(r"$P z$", font_size=22, color=ADAPT).next_to(pz, LEFT, buff=0.25)
        arr = Arrow(z.get_right() + RIGHT * 0.1, pz[6].get_bottom(), buff=0.05, color=ADAPT, stroke_width=2.5,
                    max_tip_length_to_length_ratio=0.15)
        arr_l = label(r"times $P$: \ fixed, \ random", font_size=20, color=GREY_A).next_to(arr, RIGHT, buff=0.15)
        tag = note(r"schematic").to_corner(UR, buff=0.25)
        hc = VGroup(
            history_card(2018, r"Li et al., \ intrinsic dimension", r"train in a random low-dimensional slice of "
                         r"weight space: \ many problems need surprisingly few dimensions", width=6.0, color=ADAPT),
            history_card(2020, r"Aghajanyan, Zettlemoyer \& Gupta", r"fine-tuning RoBERTa through $200$ numbers "
                         r"reached $90\%$ of full fine-tuning on a paraphrase task", width=6.0, color=ADAPT),
        ).arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Fine-tuning changes every one of a model's weights, and for a large model that means storing a full new "
            "copy for every task. But does it need to? <bookmark mark='a'/> In 2018 Chunyuan Li and colleagues "
            "trained networks in a random low-dimensional slice of weight space: the weights are the starting point "
            "plus a fixed random matrix times a small vector, and only the small vector learns. Many problems needed "
            "surprisingly few dimensions. <bookmark mark='b'/> In 2020 Armen Aghajanyan and colleagues showed that "
            "fine-tuning a pretrained language model is especially low-dimensional: about two hundred numbers got "
            "RoBERTa ninety percent of the way on a paraphrase task. Pretraining had done the hard part."
        ) as vo:
            self.play(FadeIn(th0), FadeIn(th0_l), FadeIn(tag), run_time=0.8)
            step(0)
            self.play(LaggedStart(*[FadeIn(c_, shift=DOWN * 0.1) for c_ in copies], lag_ratio=0.3), FadeIn(cost),
                      run_time=1.5)
            vo.wait_until("a")
            self.play(FadeOut(copies), FadeOut(cost))
            step(1)
            self.play(FadeIn(z), FadeIn(z_l))
            self.play(GrowArrow(arr), FadeIn(arr_l), FadeIn(pz), FadeIn(pz_l), FadeIn(hc[0], shift=UP * 0.15))
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
        Bl, Al = MathTex(r"B", font_size=32, color=ADAPT).next_to(B, RIGHT, buff=0.1), \
            MathTex(r"A", font_size=32, color=ADAPT).next_to(A, UP, buff=0.1)
        dims = VGroup(MathTex(r"d \times r", font_size=22, color=GREY_B).next_to(B, DOWN, buff=0.15),
                      MathTex(r"r \times k", font_size=22, color=GREY_B).next_to(A, RIGHT, buff=0.1))
        rows = VGroup(
            cmath(r"h", r"=", r"W x + \tfrac{\alpha}{r}\, B A\, x", font_size=36),
            cmath(r"\text{trained}", r":\ ", r"r(d + k)\ \text{ instead of }\ d k", font_size=32),
            cmath(r"d = k = 4096,\ r = 8", r":\ ", r"65{,}536 \text{ instead of } 16{,}777{,}216", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        if rows.width > 5.6:
            rows.width = 5.6
        rows.move_to([3.95, -0.2, 0])
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
        start = load("sft")["base_which"]  # every run starts from the same base model
        cols = {1: interpolate_color(ADAPT, WHITE, 0.55), 4: interpolate_color(ADAPT, WHITE, 0.3), 16: ADAPT,
                "full": ASSIST}
        names = {r["rank"]: (rf"rank ${r['rank']}$" if r["rank"] != "full" else r"every weight") for r in runs}
        S = max(int(e[0]) for r in runs for e in r["evals"])
        top = min(1.0, np.ceil(max(e[1] for r in runs for e in r["evals"]) * 10 + 1) / 10)
        g = axes([0, S], [0, top], x_length=5.6, y_length=3.6, xlabel=r"fine-tuning steps",
                 ylabel=r"held-out sentences placed right", xticks=[0, S], yticks=[0, top],
                 yfmt=lambda v: rf"{100 * v:.0f}\%", center=[-3.4, -0.2, 0])
        chance = DashedLine(g.ax.c2p(0, 1 / 30), g.ax.c2p(S, 1 / 30), color=GREY_C, dash_length=0.06)
        cl = label(r"guessing", font_size=18, color=GREY_C).next_to(chance, UP, buff=0.05).align_to(chance, RIGHT)
        lines = VGroup(*[curve(g.ax, [0] + [e[0] for e in r["evals"]], [start] + [e[1] for e in r["evals"]],
                               cols[r["rank"]], stroke_width=5 if r["rank"] in (16, "full") else 4) for r in runs])
        # the table: what each run trained, how well it did, what it forgot
        head = VGroup(VectorizedPoint(), label(r"trained \\ numbers", font_size=20, color=GREY_A),
                      label(r"right", font_size=20, color=GREY_A),
                      label(r"forgetting \\ (nats)", font_size=20, color=GREY_A))
        xs = [1.3, 3.1, 4.6, 5.9]
        for m, x in zip(head, xs):
            m.move_to([x, 2.2, 0])
        rows = VGroup()
        for k, r in enumerate(runs):
            y = 1.3 - 0.75 * k
            rows.add(VGroup(
                label(names[r["rank"]], font_size=22, color=cols[r["rank"]]).move_to([xs[0], y, 0]),
                label(rf"${r['params']:,}$".replace(",", "{,}"), font_size=22).move_to([xs[1], y + 0.12, 0]),
                label(rf"${pct(r['params'] / tot)}\%$", font_size=18, color=GREY_B).move_to([xs[1], y - 0.2, 0]),
                label(rf"${100 * r['which']:.0f}\%$", font_size=22).move_to([xs[2], y, 0]),
                label(rf"${r['heldout'] - d['base_heldout']:+.3f}$", font_size=22).move_to([xs[3], y, 0])))
        tag = note(r"computed: \ the novels model, \ which-book task; \ forgetting = change in loss on novel text")
        tag.to_edge(DOWN, buff=0.35)

        def sci(x):
            e = int(np.floor(np.log10(x)))
            return rf"{x / 10 ** e:g}\times 10^{{{e}}}"

        lrs = label(rf"learning rates: \ adapters ${sci(LORA_LR)}$, \ every weight ${sci(SFT_LR)}$", font_size=18,
                    color=GREY_B).move_to([3.6, -1.75, 0])
        full, r1 = runs[-1], runs[0]
        best = max(runs[:-1], key=lambda r: r["which"])
        forget_full = full["heldout"] - d["base_heldout"]
        forget_lora = min(r["heldout"] for r in runs[:-1]) - d["base_heldout"]
        # the verdict follows the measurement: did the adapters forget less than full fine-tuning?
        less = [r for r in runs[:-1] if r["heldout"] < full["heldout"]]
        ratio = LORA_LR / SFT_LR
        if len(less) == len(runs) - 1:
            verdict = (f"every adapter forgot less than that, as little as {forget_lora:+.3f}. LoRA learns less, and "
                       "forgets less: the title of a 2024 study that found the same at scale.")
        elif less:
            small = min(less, key=lambda r: r["heldout"])
            verdict = (f"only the rank {small['rank']} adapter forgot less, {small['heldout'] - d['base_heldout']:+.3f}, "
                       f"and it learned least. The larger adapters forgot more: they trained with steps {ratio:.0f} "
                       "times larger, as adapters need, and bigger steps carry a model further from where it started. "
                       "A 2024 study found that LoRA learns less and forgets less, at scale and at matched accuracy; at "
                       "ours, only the smallest adapter did.")
        else:
            verdict = (f"every adapter forgot more, at least {forget_lora:+.3f}: they trained with steps {ratio:.0f} "
                       "times larger, as adapters need. A 2024 study found that LoRA forgets less, at scale and at "
                       "matched accuracy; at our scale, with this recipe, it didn't.")
        with self.voiceover(
            "Our own experiment: fine-tune the novels model on the which-book task with LoRA at ranks one, four "
            "and sixteen, and with every weight. <bookmark mark='a'/> Rank one trains "
            f"{r1['params']:,} numbers, {100 * r1['params'] / tot:.2g} percent of the model. "
            f"<bookmark mark='b'/> Full fine-tuning gets {100 * full['which']:.0f} percent of held-out sentences right; "
            f"the best adapter, rank {best['rank']}, {100 * best['which']:.0f} percent. <bookmark mark='c'/> And on "
            f"ordinary novel text, full fine-tuning's loss is {forget_full:+.3f} nats from the base model's; "
            "<bookmark mark='d'/> " + verdict
        ) as vo:
            self.play(FadeIn(g), Create(chance), FadeIn(cl), FadeIn(head), FadeIn(tag),
                      FadeIn(VGroup(*[r_[0] for r_ in rows])))
            # the four runs train while they are named
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.25), run_time=4.0)
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*[VGroup(r_[1], r_[2]) for r_ in rows])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*[r_[3] for r_ in rows])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*[r_[4] for r_ in rows])))
            vo.wait_until("d")
            # each adapter's forgetting against full fine-tuning's: less in green, more in red; and the step sizes
            self.play(*[r_[4].animate.set_color(REWARD if r["heldout"] < full["heldout"] else PENALTY)
                        for r_, r in zip(rows[:-1], runs[:-1])], FadeIn(lrs))
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
