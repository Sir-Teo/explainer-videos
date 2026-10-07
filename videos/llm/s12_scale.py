from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.llm.common import PROMPT, Mono, Plot, block, label, load, show_chapter_card

# Published configurations (see README for sources).
GPT2_SIZES = [  # name, params (from the real checkpoints), layers, width
    ("gpt2", "small", 12, 768),
    ("gpt2-medium", "medium", 24, 1024),
    ("gpt2-large", "large", 36, 1280),
    ("gpt2-xl", "XL", 48, 1600),
]
KAPLAN_NC, KAPLAN_ALPHA = 8.8e13, 0.076  # L(N) = (N_c / N)^alpha_N, Kaplan et al. 2020, eq. 1.1


def fmt_params(n: float) -> str:
    return f"{n / 1e9:.3g} billion" if n >= 1e9 else f"{n / 1e6:.0f} million"


class Scale(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 11, "Scale")
        self.fam = load("gpt2_family")
        self.family()
        self.power_law()
        self.sizes()
        self.compute()
        self.refinements()

    # ------------------------------------------------------------------
    def family(self):
        fam = self.fam["paris"]
        ps = [fam[name]["probs"][fam[name]["tokens"].index(" Paris")] for name, *_ in GPT2_SIZES]
        assert ps[0] < 0.1 and ps[-1] > 0.9 and all(fam[n]["tokens"][0] == " Paris" for n, *_ in GPT2_SIZES)
        prompt = Mono(PROMPT + " ...", font_size=28).to_edge(UP, buff=0.5)
        pl = Plot((0, 4), (0, 1), width=11.0, height=3.8, y_ticks=[0, 0.5, 1], y_fmt=lambda v: f"{int(v * 100)}\\%")
        pl.move_to(DOWN * 0.2)
        yl = label(r"probability of ``Paris''", font_size=28, color=C.PROB).next_to(pl, UP, buff=0.2).align_to(pl, LEFT)
        bars, vals, names = VGroup(), VGroup(), VGroup()
        for i, ((name, short, L, d), p) in enumerate(zip(GPT2_SIZES, ps)):
            x = i + 0.5
            b = Rectangle(width=1.1, height=max(0.02, 4.0 * p), stroke_width=0, fill_color=C.PROB, fill_opacity=0.85)
            b.move_to(pl.c2p(x, 0), aligned_edge=DOWN)
            bars.add(b)
            vals.add(MathTex(f"{100 * p:.0f}\\%", font_size=34).next_to(b, UP, buff=0.12))
            n = fam[name]["params"]
            nm = VGroup(label(rf"GPT-2 {short}", font_size=28), label(fmt_params(n), font_size=24, color=GREY_A),
                        label(rf"{L} layers, width {d}", font_size=22, color=GREY_B)).arrange(DOWN, buff=0.08)
            nm.next_to(pl.c2p(x, 0), DOWN, buff=0.2)
            names.add(nm)
        with self.voiceover(
            "Everything so far has been GPT-2 small. OpenAI actually released four sizes of GPT-2, all with the same "
            "design, just wider and deeper. Let's give each of them our prompt. <bookmark mark='a'/> The smallest gives "
            "Paris six percent. <bookmark mark='b'/> The next one up: 69. <bookmark mark='c'/> The one after that: 60, so "
            "it's not perfectly smooth for any single prompt. <bookmark mark='d'/> And the largest, with one and a half "
            "billion parameters, puts 93 percent on Paris."
        ) as vo:
            self.play(FadeIn(prompt), Create(pl), FadeIn(yl), FadeIn(names, lag_ratio=0.1))
            for i, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(GrowFromEdge(bars[i], DOWN), FadeIn(vals[i]), run_time=0.8)
        self.clear_scene()

    # ------------------------------------------------------------------
    def power_law(self):
        pl = Plot((1e5, 1e10), (1.5, 6.0), width=8.5, height=4.4, log_x=True, log_y=True,
                  x_ticks=[1e5, 1e6, 1e7, 1e8, 1e9, 1e10], x_fmt=lambda v: f"10^{{{int(np.log10(v))}}}",
                  y_ticks=[2, 3, 4, 5], y_fmt=lambda v: f"{v:g}").move_to(LEFT * 0.6 + DOWN * 0.4)
        N = np.geomspace(1e5, 1e10, 50)
        L = (KAPLAN_NC / N) ** KAPLAN_ALPHA
        line = pl.line(N, L, C.LOSS, 5)
        xl = label(r"non-embedding parameters (log scale)", font_size=28, color=GREY_A).next_to(pl, DOWN, buff=0.55)
        yl = label(r"loss (log scale)", font_size=28, color=C.LOSS).next_to(pl, UP, buff=0.2).align_to(pl, LEFT)
        law = MathTex(r"L(N) \approx \Big(\frac{N_c}{N}\Big)^{0.076}", font_size=42).move_to(RIGHT * 4.4 + UP * 1.8)
        src = label(r"fitted power law from\\Kaplan et al.\ (OpenAI, 2020)", font_size=26, color=GREY_A).next_to(law, DOWN, buff=0.3)
        chin = label(r"Chinchilla (DeepMind, 2022):\\$\approx 20$ training tokens per parameter", font_size=28, color=YELLOW)
        chin.move_to(RIGHT * 4.4 + DOWN * 0.3)
        with self.voiceover(
            "In 2020, researchers at OpenAI measured this systematically, training language models across a huge range of "
            "sizes. <bookmark mark='l'/> The loss followed a smooth power law. On a log-log plot, that's a straight line, "
            "and it held over many orders of magnitude: in model size, in the amount of training data, and in compute."
        ) as vo:
            self.play(Create(pl), FadeIn(xl), FadeIn(yl))
            vo.wait_until("l")
            self.play(Create(line), Write(law), FadeIn(src), run_time=2)

        with self.voiceover(
            "Two years later, DeepMind's Chinchilla study refined the recipe: <bookmark mark='c'/> for a fixed compute "
            "budget, model size and training data should grow together, at roughly twenty tokens of training text for every "
            "parameter. That's how you get the most out of each unit of compute."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeIn(chin, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def sizes(self):
        models = [
            ("GPT-2 small", 2019, 124e6, r"12 layers, width 768", WHITE),
            ("GPT-2 XL", 2019, 1.56e9, r"48 layers, width 1600", C.EMBED),
            ("GPT-3", 2020, 175e9, r"96 layers, width 12{,}288\\300 billion training tokens", C.ATTN),
            ("Llama 3.1 405B", 2024, 405e9, r"126 layers, width 16{,}384\\about 15 trillion training tokens", C.MLP),
        ]
        big = 5.4
        squares = VGroup()
        for name, year, n, spec, col in models:
            side = big * np.sqrt(n / models[-1][2])
            sq = Square(side, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.25)
            squares.add(sq)
        for sq in squares:
            sq.align_to(DOWN * 3.0, DOWN).align_to(LEFT * 6.6, LEFT)
        squares[2].align_to(squares[3], DOWN).align_to(squares[3], LEFT)
        info = VGroup()
        for (name, year, n, spec, col), sq in zip(models, squares):
            t = VGroup(label(rf"{name} ({year})", font_size=30, color=col),
                       label(fmt_params(n) + r" parameters", font_size=28),
                       label(spec, font_size=24, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            info.add(t)
        info.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.6 + DOWN * 0.1)
        speck = Circle(0.22, color=YELLOW, stroke_width=3).move_to(squares[0])
        speck_l = label(r"GPT-2 small", font_size=24, color=YELLOW).next_to(speck, UR, buff=0.05)
        pointers = VGroup(VGroup(speck, speck_l), VectorizedPoint(), VectorizedPoint(), VectorizedPoint())
        title = label(r"area $\propto$ number of parameters", font_size=28, color=GREY_A).to_edge(UP, buff=0.35).shift(LEFT * 3)
        with self.voiceover(
            "Here's how much models have grown, with area showing parameter count. <bookmark mark='a'/> Our GPT-2 small is "
            "this speck. <bookmark mark='b'/> The largest GPT-2: 1.5 billion parameters. <bookmark mark='c'/> GPT-3, in 2020: "
            "175 billion parameters, 96 layers, vectors of 12,288 numbers, trained on 300 billion tokens. "
            "<bookmark mark='d'/> Meta's Llama 3.1, in 2024, one of the largest models whose details are public: 405 billion "
            "parameters, 126 layers, trained on about 15 trillion tokens. Most frontier labs no longer publish these numbers."
        ) as vo:
            self.play(FadeIn(title))
            for i, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(DrawBorderThenFill(squares[i]), FadeIn(info[i]), FadeIn(pointers[i]), run_time=1.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compute(self):
        rule = MathTex(r"\text{training compute}", r"\approx", r"6", r"\times N", r"\times D", font_size=48).move_to(UP * 2.2)
        rule[3].set_color(C.MLP)
        rule[4].set_color(C.TOKEN)
        legend = VGroup(label(r"$N$: parameters", font_size=30, color=C.MLP), label(r"$D$: training tokens", font_size=30),
                        label(r"6: two operations per parameter forward, four backward", font_size=26, color=GREY_A))
        legend.arrange(DOWN, buff=0.15).next_to(rule, DOWN, buff=0.35)
        g3 = MathTex(r"\text{GPT-3:}\quad 6 \times 175\times10^{9} \times 300\times10^{9}", r"\approx 3.2\times10^{23}",
                     font_size=40).move_to(DOWN * 1.3)
        ll = MathTex(r"\text{Llama 3.1 405B:}\quad 6 \times 405\times10^{9} \times 15.6\times10^{12}", r"\approx 3.8\times10^{25}",
                     font_size=40).next_to(g3, DOWN, buff=0.4)
        g3[1].set_color(YELLOW)
        ll[1].set_color(YELLOW)
        assert abs(6 * 175e9 * 300e9 / 3.15e23 - 1) < 0.01 and abs(6 * 405e9 * 15.6e12 / 3.8e25 - 1) < 0.01
        meta = label(r"(Meta reports $3.8\times10^{25}$ operations)", font_size=26, color=GREY_A).next_to(ll, DOWN, buff=0.2)
        with self.voiceover(
            "A handy rule of thumb for the cost: <bookmark mark='r'/> training takes about six arithmetic operations per "
            "parameter, per token of training text: two for the forward pass, and four more for backpropagation. "
            "<bookmark mark='g'/> For GPT-3, that's about 3 times 10 to the 23 operations. <bookmark mark='l'/> For Llama "
            "3.1, about 4 times 10 to the 25, which matches what Meta reported."
        ) as vo:
            vo.wait_until("r")
            self.play(Write(rule), FadeIn(legend))
            vo.wait_until("g")
            self.play(Write(g3))
            vo.wait_until("l")
            self.play(Write(ll), FadeIn(meta))
        self.clear_scene()

    # ------------------------------------------------------------------
    def refinements(self):
        title = label(r"Same blueprint, refined", font_size=40).to_edge(UP, buff=0.45)
        items = VGroup(*[label(t, font_size=30) for t in [
            r"rotary position embeddings",
            r"simpler normalization (RMSNorm)",
            r"gated MLPs (SwiGLU)",
            r"heads that share keys and values, to save memory",
            r"mixture of experts: each token uses only a few of many MLPs",
            r"context windows: 1{,}024 tokens in GPT-2 $\to$ hundreds of thousands today",
        ]]).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(DOWN * 0.1 + RIGHT * 0.2)
        bullets = VGroup(*[Dot(radius=0.05, color=GREY_A).next_to(it, LEFT, buff=0.25) for it in items])
        core = VGroup(block("embeddings", C.EMBED, width=2.2, height=0.6, font_size=24),
                      block("attention", C.ATTN, width=2.0, height=0.6, font_size=24),
                      block("MLP", C.MLP, width=1.3, height=0.6, font_size=24),
                      block("next-token prediction", C.PROB, width=3.2, height=0.6, font_size=24)).arrange(RIGHT, buff=0.3)
        core.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Modern models also refine many details: <bookmark mark='a'/> rotary positions, which we saw, <bookmark mark='b'/> "
            "simpler normalization, <bookmark mark='c'/> gated MLPs, <bookmark mark='d'/> attention heads that share keys "
            "and values to save memory, <bookmark mark='e'/> and mixture-of-experts layers, where each token is routed to "
            "just a few of many MLPs, so a model can hold far more parameters than it uses for any one token. "
            "<bookmark mark='f'/> And context windows have grown from GPT-2's 1,024 tokens to hundreds of thousands. "
            "<bookmark mark='g'/> But the blueprint is the one we've just walked through."
        ) as vo:
            self.play(FadeIn(title))
            for i, m in enumerate("abcdef"):
                vo.wait_until(m)
                self.play(FadeIn(items[i], shift=RIGHT * 0.2), FadeIn(bullets[i]), run_time=0.6)
            vo.wait_until("g")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in core], lag_ratio=0.15))
        self.clear_scene()
