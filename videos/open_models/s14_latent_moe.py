from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.open_models.common import (
    Plot, block, cfg, label, model_tag, note, random_values, show_chapter_card, source, vector_strip,
)
from videos.open_models.toys import situ_diag, swiglu_diag


class LatentMoE(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 13, "Kimi: 896 experts, kept stable")
        self.c = cfg("kimi")
        self.tag = model_tag("kimi")
        self.add(self.tag)
        self.traffic()
        self.latent()
        self.situ()

    # ------------------------------------------------------------------
    def traffic(self):
        c = self.c
        assert c["experts"] == 896 and c["experts_per_token"] == 16 and c["hidden"] == 7168
        tok = vector_strip(random_values(14, seed=2), cell=0.2).move_to(LEFT * 5.4)
        tok_l = label(r"7{,}168 numbers", font_size=22, color=C.EMBED).next_to(tok, DOWN, buff=0.15)
        gpus = VGroup()
        for i in range(16):
            box = RoundedRectangle(width=0.55, height=0.42, corner_radius=0.05, stroke_color=GREY_B, stroke_width=1.5)
            e = Square(0.22, stroke_width=0, fill_color=C.EXPERT, fill_opacity=0.9).move_to(box)
            gpus.add(VGroup(box, e))
        gpus.arrange_in_grid(4, 4, buff=(0.35, 0.3)).move_to(RIGHT * 2.6)
        g_l = label(r"16 chosen experts, on different GPUs", font_size=24, color=GREY_A).next_to(gpus, UP, buff=0.25)
        copies = VGroup(*[tok.copy().scale(0.16).move_to(tok) for _ in range(16)])
        targets = [g.get_left() + LEFT * 0.12 for g in gpus]
        cost = label(r"16 copies of a 7{,}168-number vector, per token, per layer (and back)", font_size=26, color=YELLOW)
        cost.to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Finally, Kimi pushes the mixture of experts further than the other two: 896 experts per layer, 16 for each token. "
            "<bookmark mark='t'/> That creates a traffic problem. In a big deployment, the experts live on different "
            "GPUs, <bookmark mark='c'/> so every token's vector has to be shipped to each of its 16 experts, and the "
            "results shipped back: 16 copies of a 7,168-number vector, per token, per layer."
        ) as vo:
            self.play(FadeIn(tok), FadeIn(tok_l))
            vo.wait_until("t")
            self.play(FadeIn(gpus, lag_ratio=0.05), FadeIn(g_l))
            vo.wait_until("c")
            self.play(LaggedStart(*[cp.animate.move_to(t) for cp, t in zip(copies, targets)], lag_ratio=0.05), run_time=2)
            self.play(FadeIn(cost))
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def latent(self):
        c = self.c
        assert c["latent_dim"] == 3584 and c["shared_experts"] == 2 and c["expert_ffn"] == 3072
        x = vector_strip(random_values(14, seed=2), cell=0.2).move_to(LEFT * 5.8 + DOWN * 0.2)
        x_l = label(r"7{,}168", font_size=22, color=C.EMBED).next_to(x, DOWN, buff=0.12)
        down = block(r"$W_\downarrow$", C.LATENT, width=0.8, height=1.2, font_size=28).next_to(x, RIGHT, buff=0.35)
        z = vector_strip(random_values(7, seed=3), cell=0.2, color=C.LATENT).next_to(down, RIGHT, buff=0.35)
        z_l = label(r"3{,}584", font_size=22, color=C.LATENT).next_to(z, DOWN, buff=0.12)
        ex = VGroup(*[Square(0.3, stroke_width=0, fill_color=C.EXPERT, fill_opacity=0.9) for _ in range(16)])
        ex.arrange_in_grid(4, 4, buff=0.12).next_to(z, RIGHT, buff=0.8)
        ex_l = label(r"16 of 896 experts,\\working in the latent space", font_size=22, color=C.EXPERT).next_to(ex, UP, 0.2)
        fan = VGroup(*[Line(z.get_right(), e.get_left(), color=C.LATENT, stroke_width=1).set_stroke(opacity=0.6) for e in ex])
        summ = MathTex(r"\textstyle\sum", font_size=40, color=C.EXPERT).next_to(ex, RIGHT, buff=0.45)
        norm = block(r"RMSNorm", C.NORM, width=1.5, height=0.6, font_size=24).next_to(summ, RIGHT, buff=0.3)
        up = block(r"$W_\uparrow$", C.LATENT, width=0.8, height=1.2, font_size=28).next_to(norm, RIGHT, buff=0.3)
        plus = MathTex("+", font_size=48).next_to(up, RIGHT, buff=0.3)
        shared = block(r"2 shared experts, full width", C.SHARED_EXPERT, width=4.2, height=0.65, font_size=24)
        shared.move_to([0.6, 2.2, 0])
        sh_lines = VGroup(Line(x.get_top(), [x.get_x(), shared.get_y(), 0], color=C.EMBED, stroke_width=2),
                          Arrow([x.get_x(), shared.get_y(), 0], shared.get_left(), buff=0, color=C.EMBED, stroke_width=2),
                          Line(shared.get_right(), [plus.get_x(), shared.get_y(), 0], color=C.SHARED_EXPERT, stroke_width=2),
                          Arrow([plus.get_x(), shared.get_y(), 0], plus.get_top(), buff=0.05, color=C.SHARED_EXPERT,
                                stroke_width=2))
        half = label(r"half the width $\Rightarrow$ half the traffic, and smaller experts: so you can afford more of them",
                     font_size=26, color=YELLOW).to_edge(DOWN, buff=0.55)
        src = note(r"LatentMoE: Elango et al.\ (NVIDIA, 2026); K3 adds the RMSNorm (``Stable LatentMoE'')")
        src.to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "The fix comes from NVIDIA's LatentMoE design. <bookmark mark='l'/> Before dispatching a token, compress it to a "
            "latent vector of half the width: 3,584 numbers. <bookmark mark='e'/> The routed experts work entirely in that "
            "smaller space, <bookmark mark='u'/> and their blended result is projected back up to full width. "
            "<bookmark mark='s'/> The two shared experts still see the full-width vector. <bookmark mark='h'/> Half the "
            "width means half the traffic, and smaller experts, so for the same budget you can afford more of them."
        ) as vo:
            self.play(FadeIn(x), FadeIn(x_l), FadeIn(src))
            vo.wait_until("l")
            self.play(FadeIn(down), TransformFromCopy(x, z), FadeIn(z_l))
            vo.wait_until("e")
            self.play(Create(fan), FadeIn(ex, lag_ratio=0.05), FadeIn(ex_l))
            vo.wait_until("u")
            self.play(FadeIn(summ), FadeIn(norm), FadeIn(up), FadeIn(plus))
            vo.wait_until("s")
            self.play(Create(sh_lines), FadeIn(shared))
            vo.wait_until("h")
            self.play(FadeIn(half, shift=UP * 0.2))
        with self.voiceover(
            "At this extreme sparsity, Moonshot ran into instabilities, and fixed them with two small changes. "
            "<bookmark mark='n'/> First, a normalization right before projecting back up, so the routed branch's scale "
            "can't swing around depending on which experts were picked."
        ) as vo:
            vo.wait_until("n")
            self.play(Indicate(norm, color=YELLOW, scale_factor=1.15), run_time=1.5)
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def situ(self):
        c = self.c
        assert c["activation"] == "situ" and c["situ_beta_gate"] == 4.0 and c["situ_beta_up"] == 25.0
        xs = np.linspace(-10, 100, 600)
        sw, si = swiglu_diag(xs), situ_diag(xs)
        assert abs(si.max() - 100) < 0.5 and sw.max() > 9000
        pl = Plot((-10, 100), (-10, 160), width=5.8, height=4.0, x_ticks=[0, 50, 100], y_ticks=[0, 50, 100, 150],
                  font_size=22).move_to(LEFT * 3.5 + DOWN * 0.4)
        clip = sw < 160
        l_sw = pl.line(xs[clip], sw[clip], GREY_B, 4)
        l_si = pl.line(xs, si, C.EXPERT, 5)
        cap = DashedLine(pl.c2p(-10, 100), pl.c2p(100, 100), color=C.EXPERT, stroke_width=1.5).set_stroke(opacity=0.6)
        cap_l = label(r"cap: $4 \times 25 = 100$", font_size=22, color=C.EXPERT).next_to(pl.c2p(55, 100), UP, buff=0.08)
        up_arrow = Arrow(pl.c2p(11.5, 140), pl.c2p(11.5, 160) + UP * 0.6, buff=0, color=GREY_B, stroke_width=3)
        sw_l = label(r"SwiGLU keeps growing:\\$10{,}000$ at $x = 100$", font_size=22, color=GREY_B)
        sw_l.next_to(up_arrow, RIGHT, buff=0.15).shift(DOWN * 0.3)
        si_l = label(r"SiTU-GLU", font_size=26, color=C.EXPERT).next_to(pl.c2p(80, 100), DOWN, buff=0.3)
        eq1 = MathTex(r"\text{SwiGLU} = ", r"\underbrace{x\,\sigma(x)}_{\text{gate}}", r"\cdot", r"\underbrace{y}_{\text{up}}",
                      font_size=34)
        eq2 = MathTex(r"\text{SiTU-GLU} = ", r"4\tanh\!\big(\tfrac{x}{4}\big)\sigma(x)", r"\cdot",
                      r"25\tanh\!\big(\tfrac{y}{25}\big)", font_size=34)
        eq2[1].set_color(C.EXPERT)
        eq2[3].set_color(C.EXPERT)
        eqs = VGroup(eq1, eq2).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.3).shift(UP * 1.0)
        why = label(r"two big factors that coincide\\make a huge product: dangerous\\in low-precision arithmetic",
                    font_size=24, color=GREY_A).next_to(eqs, DOWN, buff=0.4).align_to(eqs, LEFT)
        diag = note(r"curves: both branches given the same input ($y = x$), as in the K3 report's Figure 4")
        diag.to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "<bookmark mark='s'/> Second, a new activation function. Most modern feed-forward networks use SwiGLU: "
            "one branch goes through a smooth gate, x times the sigmoid of x, and multiplies the other branch. "
            "<bookmark mark='u'/> Both factors grow without limit, so when two big numbers happen to coincide, their "
            "product explodes. That's dangerous in low-precision arithmetic. <bookmark mark='i'/> K3's SiTU-GLU wraps each "
            "factor in a soft cap: beta times tanh of x over beta. <bookmark mark='c'/> Near zero it behaves just like "
            "SwiGLU; far out, it levels off, here at a hundred."
        ) as vo:
            vo.wait_until("s")
            self.play(Write(eq1), Create(pl), FadeIn(diag))
            self.play(Create(l_sw), run_time=1.2)
            vo.wait_until("u")
            self.play(GrowArrow(up_arrow), FadeIn(sw_l), FadeIn(why))
            vo.wait_until("i")
            self.play(Write(eq2))
            vo.wait_until("c")
            self.play(Create(l_si), Create(cap), FadeIn(cap_l), FadeIn(si_l), run_time=1.8)

        res = VGroup(label(r"Moonshot: K3's architecture and training changes reach Kimi K2's loss", font_size=30),
                     label(r"with about $2.5\times$ less compute", font_size=34, color=YELLOW)).arrange(DOWN, buff=0.2)
        res.next_to(eqs, DOWN, buff=0.6).align_to(eqs, LEFT)
        with self.voiceover(
            "<bookmark mark='r'/> Altogether, Moonshot reports that K3's new architecture, data, and training recipe reach "
            "the same loss as its predecessor, Kimi K2, with about two and a half times less compute."
        ) as vo:
            vo.wait_until("r")
            self.play(FadeOut(why), FadeIn(res, shift=UP * 0.2))
        self.clear_scene()
