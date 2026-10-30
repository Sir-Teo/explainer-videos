from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import (DENSEC, EXPERTC, F, HISTC, MOEC, PART, ROUTER, SHAREDC, billions, load, ms,
                                   seed_curves, spoken_b, take_away)

UPC = C.BITS  # the upcycled model


class Counting(VoiceoverScene):
    def construct(self):
        self.card()
        self.v3()
        self.stack()
        self.upcycle_idea()
        self.upcycle_result()

    def card(self):
        card = chapter_card(9, r"Counting parameters, and upcycling", r"What does ``671 billion, 37 active'' mean?", part=PART)
        with self.voiceover("Chapter nine. Counting parameters, and upcycling."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def v3(self):
        a = load("accounting")["v3"]
        c = F.DSV3_CONFIG
        P = a["parts"]
        colors = {r"d": GREY_A, r"h": EXPERTC}
        rows = [
            cmath(r"\text{one expert}", r"=", r"3\, d\, h", r"=", rf"3 \cdot {c['d']:,} \cdot {c['moe_ffn']:,}".replace(",", "{,}"),
                  r"=", rf"{a['expert'] / 1e6:.1f}\,\text{{M}}", colors=colors, font_size=36),
            cmath(r"\text{routed}", r"=", rf"{a['n_moe']} \times {c['routed']} \times", r"3\, d\, h", r"=",
                  rf"{P['routed'] / 1e9:.1f}\,\text{{B}}", colors=colors, font_size=36),
            cmath(r"\text{attention}", r"=", rf"{c['layers']} \times {a['attn_layer'] / 1e6:.1f}\,\text{{M}}", r"=",
                  rf"{P['attention'] / 1e9:.1f}\,\text{{B}}", font_size=36),
            cmath(r"\text{total}", r"=", rf"{a['total'] / 1e9:.1f}\,\text{{B}}", font_size=36),
            cmath(r"\text{active}", r"=", rf"{a['n_moe']} \times ({c['k']} + {c['shared']}) \times", r"3\, d\, h",
                  r"+ \ldots =", rf"{a['active_with_embed'] / 1e9:.1f}\,\text{{B}}", colors=colors, font_size=36),
        ]
        whys = [why(r"SwiGLU: \ gate, \ up, \ down"), why(rf"${a['n_moe']}$ MoE layers \ (the first ${c['dense_layers']}$ are dense)"),
                why(r"MLA, \ every layer \ (Part 15)"), why(r"$+$ dense layers, \ shared experts, \ routers, \ embeddings"),
                why(r"$8$ routed $+$ $1$ shared per layer, \ $+$ attention, \ dense, \ embeddings")]
        step = ladder(self, rows, whys, keep=5, top=2.9, x=-2.2, buff=0.5, edge=6.8)
        cite_ = cite(r"deepseek-ai/DeepSeek-V3, \ \texttt{config.json}; \ the report gives $671$B and $37$B", corner=DL,
                     font_size=18)
        with self.voiceover(
            "What do numbers like six hundred and seventy-one billion parameters, thirty-seven billion active, actually "
            "count? We can work them out from DeepSeek-V3's published configuration. <bookmark mark='a'/> One expert "
            f"is a SwiGLU network: three matrices of {c['d']:,} by {c['moe_ffn']:,}, {a['expert'] / 1e6:.0f} million "
            f"parameters. <bookmark mark='b'/> {c['routed']} of them in each of {a['n_moe']} MoE layers: "
            f"{P['routed'] / 1e9:.0f} billion, nearly everything. <bookmark mark='c'/> Attention, part fifteen's "
            f"latent attention, adds {P['attention'] / 1e9:.1f} billion across all {c['layers']} layers. "
            f"<bookmark mark='d'/> With the three dense layers, the shared experts, the routers and the embeddings, "
            f"the total comes to {a['total'] / 1e9:.1f} billion: the report's 671. <bookmark mark='e'/> A token uses "
            f"nine experts per layer, eight routed and one shared, plus all the rest: {a['active_with_embed'] / 1e9:.1f} "
            "billion, the report's thirty-seven."
        ) as vo:
            self.play(FadeIn(cite_))
            step(0)
            for i, mk in zip((1, 2, 3, 4), "bcde"):
                vo.wait_until(mk)
                step(i)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stack(self):
        d = load("accounting")
        a, mx = d["v3"], d["mixtral"]
        P = a["parts"]
        c = F.DSV3_CONFIG
        H = 5.6
        scale = H / a["total"]
        segs = [("routed experts", P["routed"], EXPERTC), ("shared experts", P["shared"], SHAREDC),
                ("attention", P["attention"], C.ATTN), ("dense layers", P["dense_ffn"], GREY_B),
                ("embeddings", P["embed"] + P["head"], C.EMBED)]

        def column(vals, x, w=1.4):
            g = VGroup()
            y = -2.9
            for name, v, col in vals:
                h = max(v * scale, 0.025)
                g.add(Rectangle(width=w, height=h, stroke_width=0.5, stroke_color=BACKGROUND, fill_color=col,
                                fill_opacity=0.85).move_to([x, y + h / 2, 0]))
                y += h
            return g

        tot = column(segs, -3.5)
        act_vals = [("routed experts", a["n_moe"] * c["k"] * a["expert"], EXPERTC), ("shared experts", P["shared"], SHAREDC),
                    ("attention", P["attention"], C.ATTN), ("dense layers", P["dense_ffn"], GREY_B),
                    ("embeddings", P["embed"] + P["head"], C.EMBED)]
        act = column(act_vals, -1.2)
        tl = label(rf"all: \ ${a['total'] / 1e9:.0f}$B", font_size=24).next_to(tot, UP, buff=0.12)
        al = label(rf"used per token: \ ${a['active_with_embed'] / 1e9:.1f}$B", font_size=24, color=C.BITS).next_to(act, UP, buff=0.12)
        key = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=col, fill_opacity=0.85), label(n, font_size=20, color=col))
                       .arrange(RIGHT, buff=0.12) for n, _, col in segs]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        key.move_to([-5.6, 1.0, 0])
        keep_in_frame(key)
        zoom = VGroup(*[Rectangle(width=0.9, height=max(v / a["active_with_embed"] * 3.6, 0.03), stroke_width=0.5,
                                  stroke_color=BACKGROUND, fill_color=col, fill_opacity=0.85) for _, v, col in act_vals])
        zoom.arrange(UP, buff=0).move_to([0.6, -1.1, 0])
        rays = VGroup(Line(act.get_corner(UR), zoom.get_corner(UL), stroke_width=1, color=GREY_C),
                      Line(act.get_corner(DR), zoom.get_corner(DL), stroke_width=1, color=GREY_C))
        zl = VGroup(*[label(rf"${v / 1e9:.1f}$B", font_size=18, color=col).next_to(z_, RIGHT, buff=0.1)
                      for (_, v, col), z_ in zip(act_vals, zoom) if v / a["active_with_embed"] > 0.04])
        mxl = VGroup(label(r"Mixtral 8x7B:", font_size=24, color=MOEC),
                     label(rf"$8 \times 7$B would be $56$B, \ but it has ${mx['total'] / 1e9:.1f}$B", font_size=22),
                     label(r"the attention is shared: \ only the feed-forward layers are copied", font_size=20, color=GREY_A),
                     label(rf"${mx['active'] / 1e9:.1f}$B used per token, \ $2$ experts of $8$", font_size=22, color=C.BITS))
        mxl.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        mxl.scale_to_fit_width(min(mxl.width, 5.0)).move_to([4.3, 1.6, 0])
        mtp = label(rf"Hugging Face lists ${(a['total'] + a['mtp']) / 1e9:.0f}$B: \\ the ${a['mtp'] / 1e9:.0f}$B module "
                    r"that predicts a second token \ (Part 18)", font_size=20, color=GREY_B).move_to([4.3, -1.0, 0])
        ex_share = (act_vals[0][1] + act_vals[1][1]) / a["active_with_embed"]
        at_share = P["attention"] / a["active_with_embed"]
        with self.voiceover(
            "Drawn to scale, DeepSeek-V3's parameters are almost all routed experts. <bookmark mark='a'/> A token "
            f"uses only {100 * a['active_with_embed'] / a['total']:.1f} percent of them. Inside that slice the "
            f"experts are {100 * ex_share:.0f} percent, and attention, which every token uses in full, is "
            f"{100 * at_share:.0f} percent. "
            "<bookmark mark='b'/> The same arithmetic explains Mixtral's name. Eight times seven billion would be "
            f"fifty-six, but Mixtral 8x7B has {mx['total'] / 1e9:.1f} billion, because only the feed-forward layers "
            f"are copied eight times; the attention is shared. It uses {mx['active'] / 1e9:.1f} billion per token. "
            "<bookmark mark='c'/> And when you see six hundred and eighty-five billion for DeepSeek-V3, that includes "
            "a module that predicts a second token ahead, part eighteen's multi-token prediction."
        ) as vo:
            self.play(FadeIn(tot), FadeIn(tl), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(act), FadeIn(al))
            self.play(Create(rays), FadeIn(zoom), FadeIn(zl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m_) for m_ in mxl], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(mtp))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def upcycle_idea(self):
        dense = VGroup(Rectangle(width=1.0, height=1.4, stroke_color=DENSEC, stroke_width=2, fill_color=DENSEC, fill_opacity=0.5),
                       label(r"a trained \\ dense layer", font_size=20, color=DENSEC))
        dense[1].next_to(dense[0], DOWN, buff=0.15)
        dense.move_to([-4.8, 0.3, 0])
        copies = VGroup(*[Rectangle(width=0.55, height=1.4, stroke_color=EXPERTC, stroke_width=1.8, fill_color=DENSEC,
                                    fill_opacity=0.5) for _ in range(8)]).arrange(RIGHT, buff=0.12).move_to([1.2, 0.3, 0])
        arrow = Arrow(dense[0].get_right(), copies.get_left(), buff=0.3, color=GREY_B)
        al = label(r"copy it into every expert", font_size=20, color=GREY_A).next_to(arrow, UP, buff=0.1)
        router = label(r"$+$ a new router", font_size=22, color=ROUTER).next_to(copies, UP, buff=0.3)
        eq = cmath(r"\sum_{i\in\mathcal K} g_i\, \operatorname{FFN}(x)", r"=", r"\operatorname{FFN}(x)",
                   r"\quad\text{when every expert is a copy, \ and } \sum_{i \in \mathcal K} g_i = 1",
                   font_size=30).to_edge(DOWN, buff=1.1)
        card = history_card(2022, r"Aran Komatsuzaki et al.\ (Google)", r"\textit{Sparse Upcycling}: \ beat the dense "
                            r"model while spending about half of its original training again", width=5.4,
                            color=HISTC).to_corner(UR, buff=0.3)
        with self.voiceover(
            "Training a big mixture from scratch is expensive. What if you already have a good dense model? "
            "<bookmark mark='a'/> Copy its feed-forward layer into every expert, add a new router, and keep "
            "training. <bookmark mark='b'/> At the moment of copying, the new model computes exactly what the old one "
            "did: every chosen expert gives the same answer, and the gates add to one. Training then pulls the copies "
            "apart. <bookmark mark='c'/> Aran Komatsuzaki and colleagues called it sparse upcycling, in 2022; Qwen's "
            "first mixture, in 2024, was made this way too."
        ) as vo:
            self.play(FadeIn(dense))
            vo.wait_until("a")
            self.play(GrowArrow(arrow), FadeIn(al), LaggedStart(*[FadeIn(c_, shift=RIGHT * 0.1) for c_ in copies], lag_ratio=0.1),
                      FadeIn(router))
            vo.wait_until("b")
            self.play(Write(eq))
            self.play(*[c_.animate.set_fill(EXPERTC, opacity=0.2 + 0.08 * i) for i, c_ in enumerate(copies)], run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(card, shift=LEFT * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def upcycle_result(self):
        u = load("upcycle")
        at = int(u["at"])
        up, half, moe = (np.asarray(u[k], float) for k in ("up_curve", "half_curve", "moe_curve"))
        allv = np.concatenate([up[:, :, 1].ravel(), half[:, 3:, 1].ravel(), moe[:, 3:, 1].ravel()])
        lo = math.floor((allv.min() - 0.03) * 10) / 10
        hi = lo + 0.8
        ax = Axes(x_range=[0, 2000, 500], y_range=[lo, hi, 0.2], x_length=7.4, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-2.2, -0.3, 0])
        yl = VGroup(*[MathTex(f"{v:.1f}", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in np.arange(lo, hi + 1e-9, 0.2)])
        xv = VGroup(*[MathTex(f"{v:,}".replace(",", "{,}"), font_size=20, color=GREY_B).next_to(ax.c2p(v, lo), DOWN, buff=0.1)
                      for v in (0, 1000, 2000)])
        xl = label(r"training steps", font_size=20, color=GREY_A).next_to(xv, DOWN, buff=0.08)
        yn = label(r"held-out bits per character \ (two seeds)", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)

        def clip(a):
            b = a.copy()
            b[:, :, 1] = np.minimum(b[:, :, 1], hi)
            return b

        c_half = seed_curves(ax, clip(half[:, 1:]), DENSEC)
        c_moe = seed_curves(ax, clip(moe[:, 1:]), MOEC)
        c_up = seed_curves(ax, clip(up), UPC)
        vline = DashedLine(ax.c2p(at, lo), ax.c2p(at, hi), color=GREY_C, stroke_width=1.5)
        vl = label(r"upcycled here", font_size=18, color=GREY_B).next_to(ax.c2p(at, hi), DOWN, buff=0.1)
        names = VGroup(label(r"dense, \ one expert's width, \ kept dense", font_size=20, color=DENSEC),
                       label(r"upcycled at step $1{,}000$", font_size=20, color=UPC),
                       label(r"mixture from scratch", font_size=20, color=MOEC)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        names.move_to([4.6, 1.5, 0])
        keep_in_frame(names)
        vu, vh, vm = ms(u["upcycled_valid"]), ms(u["dense_half_valid"]), ms(u["moe_valid"])
        cu, cm = float(u["compute_up"]), float(u["compute_moe"])
        stats = VGroup(label(rf"end: \ ${vh[0]:.3f}$, \ ${vu[0]:.3f}$, \ ${vm[0]:.3f}$", font_size=22, color=WHITE),
                       label(rf"training compute: \ upcycled ${100 * cu / cm:.0f}\%$ of from scratch", font_size=20, color=GREY_A)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(names, DOWN, buff=0.5).align_to(names, LEFT)
        keep_in_frame(stats)
        if vu[0] < vh[0] - 0.005:
            v1 = (f"The upcycled model drops below the dense one it came from right away, and ends at {vu[0]:.3f} bits "
                  f"against {vh[0]:.3f} for the dense model trained just as long. ")
        else:
            v1 = f"The upcycled model ends at {vu[0]:.3f}, about where the dense model does, {vh[0]:.3f}. "
        pc_ = 100 * cu / cm
        if vu[0] < vm[0] - 0.003:
            v2 = (f"It even ends ahead of the mixture trained from scratch, {vm[0]:.3f}, with {pc_:.0f} percent of its "
                  "training compute.")
        elif abs(vu[0] - vm[0]) <= 0.003:
            v2 = (f"It ends close to the mixture trained from scratch, {vm[0]:.3f}, with {pc_:.0f} percent of its "
                  "training compute.")
        else:
            v2 = (f"It doesn't catch the mixture trained from scratch, {vm[0]:.3f}, but it spent only {pc_:.0f} percent "
                  "of its training compute.")
        with self.voiceover(
            "We tried it. A dense model one expert wide, trained for a thousand steps, then copied into eight experts "
            "and trained for a thousand more, beside the same dense model kept dense, and our mixture trained from "
            "scratch. <bookmark mark='a'/> " + v1 + "<bookmark mark='b'/> " + v2
        ) as vo:
            self.play(Create(ax), FadeIn(yl), FadeIn(xv), FadeIn(xl), FadeIn(yn), FadeIn(c_half), FadeIn(names[0]),
                      FadeIn(c_moe), FadeIn(names[2]))
            vo.wait_until("a")
            self.play(Create(vline), FadeIn(vl))
            self.play(FadeIn(c_up), FadeIn(names[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(stats))
        self.wait(0.3)
        self.clear_scene()
