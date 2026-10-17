from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import EXPERT_COLORS, MODES, ROUTER, curve, load, load_image


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0

        def frame(caption, color):
            box = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                                   stroke_width=1.5, fill_color="#121722", fill_opacity=1)
            return box, label(caption, font_size=22, color=color).move_to(box.get_bottom() + UP * 0.28)

        def plane(xr, yr):
            return Axes(x_range=xr, y_range=yr, x_length=TW, y_length=TH, tips=False, axis_config={"stroke_width": 0})

        out = []
        cells = VGroup(*[Square(0.2, stroke_width=0.5, stroke_color=GREY_D, fill_color=C.BITS if i in (3, 17, 40, 58) else GREY_D,
                                fill_opacity=0.9 if i in (3, 17, 40, 58) else 0.3) for i in range(64)])
        out.append((cells.arrange_in_grid(rows=4, cols=16, buff=0.04), r"few experts per token", C.BITS))
        c = load("configs")
        bars = VGroup()
        for r in c["rows"]:
            bars.add(VGroup(Rectangle(width=(math.log10(r["total"]) - 9) * 0.9, height=0.18, stroke_width=0, fill_color=GREY_D,
                                      fill_opacity=0.9),
                            Rectangle(width=(math.log10(r["active"]) - 9) * 0.9, height=0.18, stroke_width=0, fill_color=C.BITS,
                                      fill_opacity=0.9)))
            bars[-1][1].align_to(bars[-1][0], LEFT)
        out.append((bars.arrange(DOWN, buff=0.08, aligned_edge=LEFT), r"total vs.\ active", C.BITS))
        m = load("moe")
        for mode, cap, col in MODES:
            out.append((load_image(np.asarray(m[f"load_{mode}"]), 2.6, 1.3), cap, col))
        R = np.asarray(m["route"])
        grid = VGroup(*[Square(0.11, stroke_width=0, fill_color=EXPERT_COLORS[j], fill_opacity=0.05 + 0.9 * float(R[i, j]))
                        .move_to([i * 0.11, -j * 0.11, 0]) for i in range(R.shape[0]) for j in range(R.shape[1])])
        out.append((grid, r"where characters go", EXPERT_COLORS[1]))
        t = load("topk")
        M = np.asarray(t["mass"])
        ks = np.log2(np.asarray(t["ks"], float))
        a7 = plane([0, ks[-1], 1], [0, 1, 0.5])
        out.append((VGroup(*[curve(a7, ks, M[l_, h], C.INTERVAL, 1.5) for l_ in range(M.shape[0]) for h in range(M.shape[1])]),
                    r"attention is sparse", C.INTERVAL))
        kk = np.log2(np.asarray(t["kk"], float))
        tk, wn = np.asarray(t["bits_topk"]), np.asarray(t["bits_window"])
        a8 = plane([kk[0], kk[-1], 1], [min(tk.min(), wn.min()) - 0.05, max(tk.max(), wn.max()) + 0.05, 0.5])
        out.append((VGroup(curve(a8, kk, wn, C.SURPRISE, 2.5), curve(a8, kk, tk, C.INTERVAL, 3)), r"choose keys by score",
                    C.INTERVAL))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = frame(cap, col)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(r"Part 13, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. A mixture of experts keeps many networks in each layer and runs only a few per token, "
            "chosen by a router: frontier models now use a few percent of their weights at a time. Routers play "
            "favourites unless balanced, by a penalty or by DeepSeek's loss-free bias. The experts split the work by "
            "themselves, and the mixture buys the knowledge of a big model at the cost of a small one. And attention "
            "is sparse too: a few keys hold most of each query's weight, and choosing keys by score beats choosing "
            "the most recent."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"experts for images and video", [15]),
            (r"serving experts across many chips", [19]),
            (r"features that light up sparsely", [20]),
        ], font_size=26)
        with self.voiceover(
            "Image and video models route by experts too, in part fifteen. Spreading hundreds of experts across many "
            "chips is a serving problem, in part nineteen. And sparsity returns in part twenty, inside the "
            "network's own activity: features that light up only rarely."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 14, \ Diffusion and Flow", font_size=40).to_edge(UP, buff=0.4)
        g = np.random.default_rng(14)
        pts = g.normal(size=(300, 2)) * 1.2
        target = np.array([[np.cos(a) * 1.6, np.sin(a) * 1.6] for a in np.linspace(0, 2 * np.pi, 300, endpoint=False)])
        dots = VGroup(*[Dot([p[0], p[1] - 0.4, 0], radius=0.035, color=C.TRUE_P) for p in pts])
        tag = note(r"illustrative").to_corner(DR, buff=0.3)
        ql = label(r"from noise to data, \ one small step at a time", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Next time, act three turns from text to everything else. Diffusion and flow models start from pure "
            "noise <bookmark mark='a'/> and, guessing one small step at a time, carry it to a picture: part four's "
            "Brownian motion, run backwards."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dots), FadeIn(tag))
            vo.wait_until("a")
            self.play(*[d_.animate.move_to([q[0], q[1] - 0.4, 0]) for d_, q in zip(dots, target)], FadeIn(ql), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [r"S.~J.~D.~Prince, \textit{Understanding Deep Learning} (2023)"]
        papers = [
            r"R.~Jacobs, M.~Jordan, S.~Nowlan \& G.~Hinton, \textit{Adaptive Mixtures of Local Experts} (1991)",
            r"N.~Shazeer et al., \textit{Outrageously Large Neural Networks} (2017); \ D.~Lepikhin et al., \textit{GShard} (2020)",
            r"W.~Fedus, B.~Zoph \& N.~Shazeer, \textit{Switch Transformers} (2021)",
            r"L.~Wang et al., \textit{Auxiliary-Loss-Free Load Balancing} (2024); \ DeepSeek-AI, \textit{DeepSeek-V3} (2024)",
            r"J.~Yuan et al., \textit{Native Sparse Attention} (2025); \ DeepSeek-AI, \textit{DeepSeek-V3.2-Exp} (2025)",
        ]
        card = reference_card(books, papers)
        data = note(r"Model sizes as published; \ every other number is computed here and checked; \ illustrations are "
                    r"labeled.", font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover(
            "The Switch Transformer paper is the clearest introduction. Thanks for watching, and see you in part "
            "fourteen."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
