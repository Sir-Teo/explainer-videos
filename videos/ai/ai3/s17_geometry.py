from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import HIST, chapter, dots_on, load

RAWC, CENC = C.TRUE_P, C.BITS


class Geometry(VoiceoverScene):
    def construct(self):
        chapter(self, 16, r"GPT-2's lopsided space", r"Are a trained model's vectors spread evenly?",
                "Chapter sixteen. GPT-2's lopsided space.", lit=(2019,))
        self.anisotropy()
        self.directions()
        self.layers()
        self.linear()

    # ------------------------------------------------------------------
    def anisotropy(self):
        g = load("gpt2")
        raw, cen = np.asarray(g["hist_raw"], float), np.asarray(g["hist_centred"], float)
        top = max(raw.max(), cen.max()) / raw.sum()
        bars = LiveBars(raw / raw.sum(), max_value=top, height=3.4, bar_width=0.17, gap=0.03, colors=RAWC)
        bars.place(-2.0)
        x0, w = bars.base.get_start()[0] + 0.15, 60 * 0.2

        def X(c):
            return x0 + w * (c + 0.3) / 0.9

        ticks = VGroup(*[MathTex(t, font_size=26, color=GREY_B).move_to([X(v), -2.2, 0])
                         for t, v in (("-0.3", -0.3), ("0", 0.0), ("0.3", 0.3), ("0.6", 0.6))])
        zero = DashedLine([X(0), -2.0, 0], [X(0), 1.8, 0], color=GREY_B, stroke_width=2)
        head = label(r"GPT-2: \ the cosine between $2{,}000$ random tokens' vectors", font_size=34).to_edge(UP, buff=0.4)
        m1 = label(rf"average ${g['cos_random_mean']:.2f}$, \ not $0$: \ they share a direction", font_size=30, color=RAWC)
        m2 = label(rf"subtract the average vector: \ ${g['cos_centred_mean']:.3f}$", font_size=30, color=CENC)
        for m in (m1, m2):
            m.to_edge(DOWN, buff=0.45)
        pred = label(rf"random directions in $768$ dimensions: \ $0 \pm {1 / np.sqrt(768):.3f}$", font_size=24,
                     color=GREY_A).next_to(head, DOWN, buff=0.2)
        with self.voiceover(
            "Random directions in 768 dimensions are nearly perpendicular, cosines of zero give or take "
            f"{1 / np.sqrt(768):.3f}. Trained vectors are not random. <bookmark mark='a'/> Between two of GPT-2's token "
            f"vectors the average cosine is {g['cos_random_mean']:.2f}: they all lean one way, the space is "
            f"anisotropic. Each makes a cosine of {g['mean_vec_cos']:.2f}, on average, with their mean. "
            f"<bookmark mark='b'/> Subtract the mean, and the average cosine falls to {g['cos_centred_mean']:.3f}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pred), Create(zero), FadeIn(ticks))
            vo.wait_until("a")
            self.play(FadeIn(bars), FadeIn(m1))
            vo.wait_until("b")
            self.play(*bars.to(cen / cen.sum()), FadeOut(m1), FadeIn(m2), run_time=1.6)
        bars.freeze()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def directions(self):
        g = load("gpt2")
        share = np.asarray(g["pc_share"])[:20]
        iso = float(g["pc_share_iso"])
        ga = axes([0, 21, 5], [0, share[0] * 1.15, share[0] / 2], x_length=5.4, y_length=3.4, xticks=[1, 5, 10, 15, 20],
                  yticks=[0, round(share[0], 3)], yfmt=lambda v: f"{100 * v:.1f}\\%",
                  xlabel=r"principal direction", ylabel=r"share of the spread (after centring)", center=[-3.6, -0.6, 0])
        ax = ga.ax
        bars = VGroup(*[Rectangle(width=0.18, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                  fill_color=RAWC, fill_opacity=0.85).move_to(ax.c2p(i + 1, v / 2)) for i, v in
                        enumerate(share)])
        isol = DashedLine(ax.c2p(0, iso), ax.c2p(21, iso), color=GREY_B, stroke_width=2)
        isot = label(r"dashed: \ equal shares, \ $1/768$", font_size=20, color=GREY_B).move_to(ax.c2p(14, share[0] * 0.85))
        pts = np.asarray(g["pc12_sample"])
        ids = np.asarray(g["pc12_ids"])
        gb = axes([float(pts[:, 0].min()), float(pts[:, 0].max()), 1], [float(pts[:, 1].min()), float(pts[:, 1].max()), 1],
                  x_length=5.4, y_length=3.4, xlabel=r"first principal direction", ylabel=r"second",
                  center=[3.4, -0.6, 0])
        bx = gb.ax
        cols = [interpolate_color(ManimColor(C.BITS), ManimColor(C.TRUE_P), min(1.0, i / 50257) ** 0.5) for i in ids]
        dots = VGroup(*[Dot(bx.c2p(x, y), radius=0.022, color=c_, fill_opacity=0.7) for (x, y), c_ in
                        zip(pts[::2], cols[::2])])
        key = legend([(C.BITS, r"early tokens (frequent)"), (C.TRUE_P, r"late tokens (rare)")], font_size=20)
        key.next_to(gb, UP, buff=0.1).align_to(gb, RIGHT)
        abtt = {int(D): m for D, m, _ in g["abtt"]}
        head = label(r"After centring: \ which directions remain lopsided?", font_size=34).to_edge(UP, buff=0.35)
        rho = g["pc1_id_spearman"]
        with self.voiceover(
            "Even centred, the spread is uneven. <bookmark mark='a'/> The top principal direction carries "
            f"{100 * share[0]:.1f} percent of it, against {100 * iso:.2f} for an even share. <bookmark mark='b'/> Colour "
            "each token by its number in GPT-2's vocabulary, which roughly runs from frequent to rare: the first "
            f"direction tracks it, a rank correlation of {rho:.2f}. <bookmark mark='c'/> Jun Gao and colleagues explained "
            "this in 2019: training mostly pushes a rare token's vector away from contexts, so rare tokens drift "
            "together. Removing the top direction too, Mu and Viswanath's all-but-the-top of 2018, brings the average "
            f"cosine from {abtt[0]:.3f} to {abtt[1]:.4f}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ga), FadeIn(gb))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.05), Create(isol), FadeIn(isot))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.0005), FadeIn(key), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(bars[0], color=WHITE))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def layers(self):
        g = load("gpt2")
        L = g["layers"]
        n = len(L)
        ga = axes([-0.5, n - 0.5, 1], [-0.05, 1.0, 0.25], x_length=7.6, y_length=4.0, xticks=list(range(0, n, 2)),
                  yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"layer \ ($0$: the token and position vectors; \ "
                  rf"${n - 1}$: after the final normalization)", ylabel=r"average cosine between two positions",
                  center=[-1.8, -0.5, 0])
        ax = ga.ax
        xs = [d["layer"] for d in L]
        raw = [d["cos"] for d in L]
        cen = [d["cos_centred"] for d in L]
        cr = VGroup(curve(ax, xs, raw, RAWC, 3), dots_on(ax, xs, raw, RAWC, 0.06))
        cc = VGroup(curve(ax, xs, cen, CENC, 3), dots_on(ax, xs, cen, CENC, 0.06))
        leg = legend([(RAWC, r"as is"), (CENC, r"centred, layer by layer")], font_size=22).move_to([4.6, 1.5, 0])
        mid = L[n // 2]
        rog = label(rf"layer ${mid['layer']}$: \ dimensions ${mid['top3_dims'][0]}, {mid['top3_dims'][1]}, "
                    rf"{mid['top3_dims'][2]}$ \\ carry ${100 * mid['top3_share']:.0f}\%$ of the average cosine",
                    font_size=22, color=GREY_A).move_to([4.6, -0.4, 0])
        tag = note(rf"computed: \ GPT-2 reading the scoreboard's passage, \ ${g['passage_tokens']}$ tokens").to_corner(DR, buff=0.2)
        hi = max(L[1:], key=lambda d: d["cos"])
        with self.voiceover(
            "Inside the network it is stronger. <bookmark mark='a'/> GPT-2 reading the scoreboard's passage, layer by "
            f"layer: the average cosine between positions is {L[0]['cos']:.2f} at the input, about {mid['cos']:.2f} in "
            f"the middle, and {hi['cos']:.2f} at the top, the narrow cone Kawin Ethayarajh measured in 2019. "
            f"<bookmark mark='b'/> In layer {mid['layer']}, three of 768 dimensions carry {100 * mid['top3_share']:.0f} "
            "percent of it: rogue dimensions, in Timkey and van Schijndel's phrase. <bookmark mark='c'/> Centre each "
            "layer and the cosines fall to about zero. Raw cosines measure this common lean as much as meaning."
        ) as vo:
            self.play(FadeIn(ga), FadeIn(tag), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(cr), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rog))
            vo.wait_until("c")
            self.play(Create(cc), FadeIn(leg[1]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def linear(self):
        w = load("words")
        an = w["analogies"]["france:paris::england"]
        cards = VGroup(
            history_card(2013, r"T.~Mikolov, W.~Yih \& G.~Zweig",
                         r"linguistic regularities: \ king $-$ man $+$ woman lands near queen", color=HIST, width=4.3,
                         font_size=30),
            history_card(2022, r"N.~Elhage et al., \ Anthropic",
                         r"toy models of superposition: \ more features than dimensions, \ as nearly perpendicular "
                         r"directions", color=HIST, width=4.3, font_size=30),
            history_card(2024, r"K.~Park, Y.~J.~Choe \& V.~Veitch",
                         r"the linear representation hypothesis, \ made precise: \ concepts as directions, \ under the "
                         r"right inner product", color=HIST, width=4.3, font_size=30),
        ).arrange(RIGHT, buff=0.2, aligned_edge=UP).move_to(DOWN * 0.2)
        head = label(r"The linear representation hypothesis", font_size=40).to_edge(UP, buff=0.4)
        tail = label(r"Part 30: \ reading and steering a model along its directions", font_size=28, color=C.BITS)
        tail.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            f"Lopsided or not, directions carry meaning: our counted vectors sent England to {an[0]}. "
            "<bookmark mark='a'/> In 2013 Mikolov, Yih and Zweig found such regularities in neural word vectors. "
            "<bookmark mark='b'/> In 2022 Nelson Elhage and colleagues showed toy networks storing more features than "
            "dimensions, as nearly perpendicular directions. <bookmark mark='c'/> In 2024 Kiho Park, Yo Joong Choe and "
            "Victor Veitch made it precise: concepts as directions, under the right inner product, not always the plain "
            "dot product. <bookmark mark='d'/> Reading and steering along such directions is Part 30's subject."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(tail))
        self.wait(0.3)
        self.clear_scene()
