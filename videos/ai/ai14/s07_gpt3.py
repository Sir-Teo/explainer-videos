from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import (CONTEXT, C_COL, DECODER, D_COL, N_COL, PART, PRIOR, F, config_card, human, load,
                                   said, take_away)


class GPT3(VoiceoverScene):
    def construct(self):
        self.card()
        self.laws()
        self.params()
        self.compute()
        self.in_context()
        self.results()

    def card(self):
        card = chapter_card(6, r"Scale, and learning in context", r"What happens when the model is a hundred times "
                            r"bigger?", lit=(2020,), part=PART)
        with self.voiceover("Chapter six. Scale, and learning in context."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def laws(self):
        K = F.KAPLAN
        law = cmath(r"L(N)", r"=", r"\left(\frac{N_c}{N}\right)^{\alpha_N}", r",\quad", rf"\alpha_N \approx {K['alpha_n']}",
                    font_size=40).move_to([0, 2.5, 0])
        law[0].set_color(C.LOSS)
        Nc = 8.8e13
        n = np.logspace(5, 11, 60)
        L = (Nc / n) ** K["alpha_n"]
        g = axes([5, 11], [math.log10(1.5), math.log10(6.0)], x_length=6.2, y_length=3.6,
                 xlabel=r"non-embedding parameters $N$ \ (log scale)", ylabel=r"test loss, nats per token \ (log scale)",
                 xticks=[5, 7, 9, 11], yticks=[math.log10(2), math.log10(4)],
                 xfmt=lambda v: rf"10^{{{int(v)}}}", yfmt=lambda v: f"{10 ** v:.0f}", center=[-2.4, -0.9, 0])
        c = curve(g.ax, np.log10(n), np.log10(L), N_COL, 4)
        side = VGroup(
            label(r"the same straight line on log--log axes \\ over more than seven orders of magnitude", font_size=22,
                  color=GREY_A),
            label(r"bigger models get more from each token", font_size=24, color=N_COL),
            label(r"for a fixed budget: \ grow the model faster than the data", font_size=24, color=C_COL),
            label(r"the details, \ and Chinchilla's correction: \ Part 12", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.7, -0.8, 0])
        cite_ = cite(r"Kaplan et al.\ (2020), Eq.\ 1.1, \ $N_c \approx 8.8 \times 10^{13}$; \ the curve is the fitted law")
        with self.voiceover(
            "January 2020. Jared Kaplan, Sam McCandlish and colleagues at OpenAI measured how a language model's loss "
            "falls as it grows. <bookmark mark='a'/> Across more than seven orders of magnitude, the test loss followed "
            "a power law in the number of parameters, with a small exponent, about 0.076, and similar laws in the "
            "data and the compute. <bookmark mark='b'/> The message: bigger models get more out of every token, and "
            "for a fixed budget you should grow the model faster than the data. Part 12 derived these laws, and the "
            "correction that came two years later. In 2020 they were the case for building something enormous."
        ) as vo:
            self.play(Write(law), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(g), Create(c), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s, shift=LEFT * 0.1) for s in side], lag_ratio=0.4), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def params(self):
        G = F.GPT3
        p = load("published")["shape_params"]["gpt3"]
        card = config_card(F.CFG["gpt3"], rows=("layers", "d", "heads", "ctx", "params", "tokens"),
                           width=4.6).move_to([-4.5, 0.2, 0])
        rows = [
            cmath(r"N_{\mathrm{attn}}", r"=", r"4\, d^2", font_size=36),
            cmath(r"N_{\mathrm{mlp}}", r"=", r"2 \cdot d \cdot 4d = 8\, d^2", font_size=36),
            cmath(r"N", r"\approx", r"12\, L\, d^2 + (V + n_{\mathrm{ctx}})\, d", font_size=36),
            cmath(r"N", r"\approx", rf"{p['body'] / 1e9:.1f} \times 10^9 + {p['emb'] / 1e9:.2f} \times 10^9", font_size=36),
            cmath(r"N", r"\approx", rf"{p['total'] / 1e9:.1f} \times 10^9", font_size=36),
        ]
        for r in rows:
            r[0].set_color(N_COL)
        whys = [why(r"queries, keys, values, output: \ $d \times d$ each"),
                why(r"two matrices, \ hidden width $4d$"),
                why(r"$L$ layers; \ token and position embeddings"),
                why(r"$L = 96$, \ $d = 12{,}288$, \ $V = 50{,}257$"),
                why(r"the paper's appendix: \ $174{,}600$M \ \checkmark")]
        step = ladder(self, rows, whys, keep=5, top=2.9, x=0.4, buff=0.45, edge=6.9)
        mix = F.GPT3["mix"]
        mixg = VGroup(*[label(rf"{nm}: \ ${t / 1e9:.0f}$B tokens, \ ${w}\%$ of the mix", font_size=19,
                              color=D_COL if k else GREY_A) for k, (nm, t, w) in enumerate(mix)])
        mixg.arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_corner(DR, buff=0.35)
        with self.voiceover(
            "May 2020. Tom Brown and thirty colleagues at OpenAI: GPT-3. Eight sizes, from 125 million to 175 billion "
            "parameters, all trained on 300 billion tokens. The largest has 96 layers, a width of 12,288, 96 heads, "
            "and a context of 2,048 tokens. Where do 175 billion parameters come from? <bookmark mark='a'/> Each layer "
            "has four attention matrices, for queries, keys, values and the output, each d by d. <bookmark mark='b'/> "
            "The feed-forward network has two matrices of d by four d: eight d squared. <bookmark mark='c'/> So a "
            "layer holds twelve d squared, and the embeddings add the vocabulary and the positions times d. "
            f"<bookmark mark='d'/> For GPT-3 that's {p['body'] / 1e9:.1f} billion in the layers and "
            f"{p['emb'] / 1e9:.2f} billion in the embeddings, <bookmark mark='e'/> {p['total'] / 1e9:.1f} billion in "
            "all, exactly the figure in the paper's appendix. The training mix leaned toward quality: filtered web "
            "pages were most of it, but the smaller, cleaner sources were seen two or three times over."
        ) as vo:
            self.play(FadeIn(card, shift=RIGHT * 0.15))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            self.play(FadeIn(mixg))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compute(self):
        G = F.GPT3
        P = load("published")
        n = G["params_m"] * 1e6
        rows = [
            cmath(r"C", r"\approx", r"(2 + 4)\, N D", font_size=40),
            cmath(r"C", r"\approx", rf"6 \times {n / 1e11:.3f} \times 10^{{11}} \times 3 \times 10^{{11}}", font_size=40),
            cmath(r"C", r"\approx", sci(P["gpt3_6nd"], 2) + r"\ \text{FLOP}", font_size=40),
            cmath(r"C", r"\approx", rf"{P['gpt3_pfdays']:,.0f}".replace(",", "{,}") + r"\ \text{petaflop/s-days}",
                  font_size=40),
        ]
        for r in rows:
            r[0].set_color(C_COL)
        whys = [why(r"forward: \ a multiply and an add per parameter per token; \ backward: \ about twice that"),
                why(r"$N = 174.6$ billion, \ $D = 300$ billion tokens"),
                why(rf"Table D.1: \ ${sci(G['flops'], 2)}$ \ \checkmark"),
                why(r"$1$ petaflop/s-day $= 10^{15} \times 86{,}400 = 8.64 \times 10^{19}$")]
        step = ladder(self, rows, whys, keep=4, top=2.6, x=-2.4, buff=0.6, edge=6.9)
        fw = Rectangle(width=2 * 1.1, height=0.7, stroke_width=0, fill_color=C.ACTS, fill_opacity=0.85)
        bw = Rectangle(width=4 * 1.1, height=0.7, stroke_width=0, fill_color=C.GRADS, fill_opacity=0.85)
        VGroup(fw, bw).arrange(RIGHT, buff=0.06)
        ops = VGroup(VGroup(fw, label(r"forward: \ $2$", font_size=28, color=WHITE).move_to(fw)),
                     VGroup(bw, label(r"backward: \ $4$", font_size=28, color=WHITE).move_to(bw)))
        opl = label(r"operations per parameter, per token", font_size=26, color=GREY_A).next_to(ops, UP, buff=0.2)
        opn = label(r"the backward pass needs the gradient twice: \ for the weights, and for the layer below",
                    font_size=22, color=GREY_B).next_to(ops, DOWN, buff=0.25)
        pic = VGroup(opl, ops, opn).move_to([0, -0.9, 0])
        yrs = P["gpt3_pfdays"] / 365.25
        ratio = round(P["gpt3_6nd"] / P["tf_big_flops"], -3)
        res = label(rf"one petaflop per second, \ sustained for about ${yrs:.0f}$ years", font_size=28, color=C_COL)
        res.to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Now the compute, counted a second way. <bookmark mark='a'/> Training on one token costs about six "
            "operations per parameter: two in the forward pass, a multiply and an add, and about four in the backward "
            "pass, because the gradient is needed both for the weights and for the layer below. So C is about six N D. "
            "<bookmark mark='b'/> Six, times 174.6 billion parameters, times 300 billion tokens, <bookmark mark='c'/> "
            f"is {P['gpt3_6nd'] / 1e23:.2f} times ten to the twenty-three operations, the paper's own figure. "
            f"<bookmark mark='d'/> In the paper's unit, {P['gpt3_pfdays']:,.0f} petaflop-days: a computer doing a "
            f"thousand trillion operations a second, for about {yrs:.0f} years. That is about {ratio:,.0f} times the "
            "compute of chapter one's Transformer."
        ) as vo:
            step(0)
            self.play(FadeIn(pic, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeOut(pic))
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def in_context(self):
        d = definition_card(r"in-context learning", r"the task's description, and perhaps a few examples, are put "
                            r"in the prompt; \ the model continues it. \ No gradient step: \ not one weight changes.",
                            color=CONTEXT, width=6.2, font_size=24).move_to([-3.7, 1.7, 0])
        lines = ["Translate English to French:", "sea otter => loutre de mer", "peppermint => menthe poivrée",
                 "plush girafe => girafe peluche", "cheese =>"]
        prompt = VGroup(*[said(t, chars=34, font_size=19, max_lines=1, box_color=CONTEXT if 0 < i < 4 else GREY_B)
                          for i, t in enumerate(lines)]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        prompt.move_to([3.1, 0.6, 0])
        brace = Brace(prompt[1:4], RIGHT, color=CONTEXT)
        bl = label(r"examples", font_size=20, color=CONTEXT).next_to(brace, RIGHT, buff=0.1)
        kinds = VGroup(label(r"zero-shot: \ the description only", font_size=24, color=GREY_A),
                       label(r"one-shot: \ one example", font_size=24, color=GREY_A),
                       label(r"few-shot: \ as many as fit, \ typically $10$ to $100$", font_size=24, color=CONTEXT))
        kinds.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-3.3, -1.7, 0])
        tag = note(r"after Brown et al.\ (2020), Figure 2.1").to_corner(DR, buff=0.2)
        title = label(r"\textit{Language Models are Few-Shot Learners}", font_size=36, color=CONTEXT).to_edge(UP, buff=0.4)
        with self.voiceover(
            "But GPT-3 is remembered for something else, the thing its title promised: language models are few-shot "
            "learners. <bookmark mark='a'/> In-context learning: put a description of the task, and perhaps a few "
            "examples, in the prompt, and let the model continue. No gradient step is taken; not one weight changes. "
            "<bookmark mark='b'/> Here is the paper's own illustration: translate English to French; sea otter, "
            "loutre de mer; peppermint, menthe poivrée; and then cheese, and an arrow. <bookmark mark='c'/> With only "
            "the description, it's called zero-shot; with one example, one-shot; with as many as fit in the context, "
            "typically ten to a hundred, few-shot."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(title), FadeIn(prompt[0]))
            vo.wait_until("a")
            self.play(FadeOut(title), FadeIn(d, shift=UP * 0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p_, shift=RIGHT * 0.1) for p_ in prompt[1:]], lag_ratio=0.4),
                      Create(brace), FadeIn(bl), run_time=2.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(k, shift=UP * 0.1) for k in kinds], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        G = F.GPT3
        lam, tq = G["lambada"], G["triviaqa"]

        def panel(title, vals, sota=None, center=ORIGIN):
            names = [r"zero-shot", r"one-shot", r"few-shot"]
            cols = [GREY_B, interpolate_color(ManimColor(GREY_B), ManimColor(CONTEXT), 0.5), CONTEXT]
            bars = VGroup()
            for k, (nm, v, c) in enumerate(zip(names, vals, cols)):
                b = Rectangle(width=0.8, height=3.0 * v / 100, stroke_width=0, fill_color=c, fill_opacity=0.9)
                b.move_to([1.15 * k, 0, 0], aligned_edge=DOWN)
                t = MathTex(f"{v:g}", font_size=26, color=c).next_to(b, UP, buff=0.08)
                n_ = label(nm, font_size=20, color=GREY_A).next_to(b, DOWN, buff=0.12)
                bars.add(VGroup(b, t, n_))
            g = VGroup(bars)
            if sota is not None:
                y = 3.0 * sota / 100
                ln = DashedLine([-0.6, y, 0], [2.9, y, 0], color=PRIOR, dash_length=0.08)
                lt = label(rf"previous best ${sota:g}$", font_size=18, color=PRIOR).next_to(ln, RIGHT, buff=0.08)
                g.add(VGroup(ln, lt))
            t = label(title, font_size=24, color=WHITE).next_to(bars, UP, buff=0.75)
            g.add(t)
            return g.move_to(center)

        p1 = panel(r"LAMBADA \ (last word)", [lam["zero"], lam["one"], lam["few"]], lam["sota"], [-3.6, 0.3, 0])
        p2 = panel(r"TriviaQA \ (closed book)", [tq["zero"], tq["one"], tq["few"]], None, [2.6, 0.3, 0])
        trend = label(r"and the gap from zero-shot to few-shot grew with model size: \\ larger models made better use "
                      r"of what was in their context", font_size=24, color=CONTEXT).to_edge(DOWN, buff=0.5)
        cite_ = cite(r"Brown et al.\ (2020), Tables 3.2--3.3, Figure 1.2", corner=UL)
        with self.voiceover(
            "And it worked. <bookmark mark='a'/> On LAMBADA, GPT-3 reached "
            f"{lam['zero']:g} percent zero-shot and {lam['few']:g} percent few-shot, against a previous best of "
            f"{lam['sota']:g}. <bookmark mark='b'/> Answering trivia questions from memory, with no documents to look "
            f"in: {tq['zero']:g} percent zero-shot, {tq['one']:g} one-shot, {tq['few']:g} few-shot. "
            "<bookmark mark='c'/> And across the eight sizes, the gap between zero-shot and few-shot widened: larger "
            "models made better use of what was in their context. Nobody had trained for this. It appeared with "
            "scale. In chapter fourteen we'll look for it in our own small models."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(p1[-1]), FadeIn(p2[-1]))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1]), FadeIn(b[2]))
                                    for b in p1[0]], lag_ratio=0.3), FadeIn(p1[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1]), FadeIn(b[2]))
                                    for b in p2[0]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(trend))
        self.wait(0.3)
        self.clear_scene()
