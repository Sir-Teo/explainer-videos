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
            "Chapter fourteen said random directions in 768 dimensions are nearly perpendicular: cosines of zero, "
            f"give or take {1 / np.sqrt(768):.3f}. Trained vectors are not random. <bookmark mark='a'/> Take two "
            f"thousand of GPT-2's token vectors: the average cosine between two of them is {g['cos_random_mean']:.2f}. "
            "They all lean the same way; in the jargon, the space is anisotropic. Each token's vector makes a cosine "
            f"of {g['mean_vec_cos']:.2f}, on average, with the mean of all of them. <bookmark mark='b'/> Subtract that "
            f"mean from every vector, and the average cosine falls to {g['cos_centred_mean']:.3f}."
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
        isot = label(r"equal shares: \ $1/768$", font_size=20, color=GREY_B).next_to(ax.c2p(21, iso), UP, buff=0.05)
        isot.align_to(ax.c2p(21, 0), RIGHT)
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
            "Even after centring, the spread is uneven. <bookmark mark='a'/> The top principal direction carries "
            f"{100 * share[0]:.1f} percent of the spread, against {100 * iso:.2f} percent for an even share. "
            "<bookmark mark='b'/> What is that direction? Colour each token by its number in GPT-2's vocabulary, "
            "which follows the order in which its tokenizer merged pieces, roughly from frequent to rare. The first "
            f"direction tracks it: a rank correlation of {rho:.2f}. Rare tokens sit apart from common ones. "
            "<bookmark mark='c'/> One explanation, from Jun Gao and colleagues in 2019: in training, a rare token's "
            "vector is mostly pushed away from contexts where it doesn't appear, so the rare ones drift together. "
            "Removing the top direction as well as the mean, Jiaqi Mu and Pramod Viswanath's 'all-but-the-top' "
            f"of 2018, brings the average cosine from {abtt[0]:.3f} to {abtt[1]:.4f}."
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
            "Inside the network it gets stronger. <bookmark mark='a'/> Run GPT-2 on the scoreboard's passage and "
            "compare the vectors at different positions, layer by layer. At the input the average cosine is "
            f"{L[0]['cos']:.2f}; in the middle layers it is about {mid['cos']:.2f}, and at the top it reaches "
            f"{hi['cos']:.2f}. Kawin Ethayarajh measured this in 2019: the upper layers' vectors crowd into a narrow "
            f"cone. <bookmark mark='b'/> In layer {mid['layer']}, just three of the 768 dimensions carry "
            f"{100 * mid['top3_share']:.0f} percent of that average cosine: rogue dimensions, as William Timkey and "
            "Marten van Schijndel called them in 2021. <bookmark mark='c'/> Centre each layer, and the cosines fall "
            "back to about zero. Cosine similarity on raw vectors measures this common lean as much as meaning, "
            "which is why retrieval systems centre or normalize their vectors."
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
                         font_size=27),
            history_card(2022, r"N.~Elhage et al., \ Anthropic",
                         r"toy models of superposition: \ more features than dimensions, \ as nearly perpendicular "
                         r"directions", color=HIST, width=4.3, font_size=27),
            history_card(2024, r"K.~Park, Y.~J.~Choe \& V.~Veitch",
                         r"the linear representation hypothesis, \ made precise: \ concepts as directions, \ under the "
                         r"right inner product", color=HIST, width=4.3, font_size=27),
        ).arrange(RIGHT, buff=0.2, aligned_edge=UP).move_to(DOWN * 0.2)
        head = label(r"The linear representation hypothesis", font_size=40).to_edge(UP, buff=0.4)
        tail = label(r"Part 30: \ reading and steering a model along its directions", font_size=28, color=C.BITS)
        tail.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            f"Lopsided or not, directions carry meaning. Our counted vectors sent France to Paris as England to "
            f"{an[0]}. <bookmark mark='a'/> In 2013 Tomas Mikolov, Wen-tau Yih and Geoffrey Zweig found the same "
            "regularities in neural word vectors. <bookmark mark='b'/> In 2022, Nelson Elhage and colleagues at "
            "Anthropic showed in toy models how a network stores more features than it has dimensions, as nearly "
            "perpendicular directions: the room of chapter fourteen, used. <bookmark mark='c'/> In 2024, Kiho Park, "
            "Yo Joong Choe and Victor Veitch made the idea precise: concepts as directions, once you measure with the "
            "right inner product, which is not always the plain dot product, for exactly the reason this chapter "
            "showed. <bookmark mark='d'/> Reading and steering models along such directions is Part 30's subject."
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
