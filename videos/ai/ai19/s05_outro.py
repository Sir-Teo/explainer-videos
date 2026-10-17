from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai19.compute import FP4, load
from videos.ai.ai20.compute import load as load20


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

        def bars(vs, cols, dx=0.09):
            top = max(float(np.max(v)) for v in vs)
            g = VGroup()
            for j, (v, col) in enumerate(zip(vs, cols)):
                for i, x in enumerate(v):
                    g.add(Rectangle(width=dx * 0.9, height=max(1.6 * x / top, 0.01), stroke_width=0, fill_color=col, fill_opacity=0.9)
                          .move_to([i * dx * (len(vs) + 1) + j * dx, 0.8 * x / top, 0]))
            return g

        s, q, r, p = load("speculative"), load("quant"), load("roofline"), load("paging")
        draft = VGroup(*[Square(0.4, stroke_color=GREY_B, stroke_width=1.5, fill_color=GREY_B, fill_opacity=0.15) for _ in range(5)])
        draft.arrange(RIGHT, buff=0.08)
        marks = VGroup(*[MathTex(r"\checkmark" if i < 3 else r"\times", font_size=30, color=C.INTERVAL if i < 3 else C.SURPRISE)
                         .next_to(d, DOWN, buff=0.15) for i, d in enumerate(draft)])
        h = np.asarray(q["hist_w"], float)
        e = np.asarray(q["hist_edges"])
        hb = VGroup(*[Rectangle(width=0.032, height=max(1.4 * v / h.max(), 0.005), stroke_width=0, fill_color=GREY_B, fill_opacity=0.8)
                      .move_to([0.0375 * i, 0.7 * v / h.max(), 0]) for i, v in enumerate(h)])
        m = max(abs(e[0]), abs(e[-1]))
        lev = np.concatenate([-FP4[::-1][:-1], FP4]) * m / 6
        ticks = VGroup(*[Line([0, 0, 0], [0, 1.5, 0], color=C.BITS, stroke_width=1.2).set_x(hb.get_left()[0] + (x - e[0]) / (e[-1] - e[0]) * hb.width)
                         for x in lev])
        modes = [str(x) for x in q["modes"]]
        qv = np.array([float(q[f"bits_{x}"]) for x in modes])
        qbars = VGroup(*[Rectangle(width=max(2.6 * (v - qv[0] + 0.03) / (qv.max() - qv[0] + 0.03), 0.02), height=0.22, stroke_width=0,
                                   fill_color=c_, fill_opacity=0.9) for v, c_ in zip(qv, (GREY_B, C.TRUE_P, C.INTERVAL, C.SURPRISE, C.BITS))])
        qbars.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        ax = Axes(x_range=[-1, 3, 1], y_range=[0, 4, 1], x_length=TW * 0.9, y_length=TH * 0.9, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False})
        lb, lp = math.log10(float(r["bandwidth"])), math.log10(float(r["peak"]))
        y0 = math.floor(min(np.log10(r["gflops"]).min(), lb - 1))
        xs = np.linspace(-1, 3, 60)
        roof = VMobject(color=C.BITS, stroke_width=3).set_points_as_corners(
            [ax.c2p(x, np.minimum(lb + x, lp) - y0) for x in xs if np.minimum(lb + x, lp) - y0 >= 0])
        dots = VGroup(*[Dot(ax.c2p(a, b - y0), radius=0.05, color=C.TRUE_P) for a, b in zip(np.log10(r["intensity"]), np.log10(r["gflops"]))])
        grid = VGroup(*[Square(0.2, stroke_width=0.6, stroke_color=GREY_D, fill_color=C.ATTN, fill_opacity=0.5 if i < 3 else 0.08)
                        for i in range(64)]).arrange_in_grid(rows=8, cols=8, buff=0)
        grid.add(SurroundingRectangle(grid[3], color=C.KEY, buff=0, stroke_width=2.5))
        lens = np.asarray(p["lens"])[:10]
        paged = VGroup(*[Rectangle(width=2.8 * L / int(p["max_len"]) + 0.02, height=0.12, stroke_width=0, fill_color=C.TRUE_P, fill_opacity=0.9)
                         for L in lens]).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        boxes = VGroup(*[Rectangle(width=2.8, height=0.12, stroke_width=0.6, stroke_color=GREY_D) for _ in lens]).arrange(DOWN, buff=0.05)
        paged.align_to(boxes, LEFT).align_to(boxes, UP)
        out = [
            (MathTex(r"\frac{\text{tokens}}{\text{s}} \le \frac{\text{bandwidth}}{\text{bytes}}", font_size=36, color=WHITE),
             r"the speed limit", C.BITS),
            (VGroup(draft, marks), r"guess ahead, check at once", C.INTERVAL),
            (bars([np.asarray(s["p_top"]), np.asarray(s["emp_top"])], [C.NEURAL, C.BITS]), r"exactly the big model", C.NEURAL),
            (MathTex(r"\frac{1 - \alpha^{k+1}}{1 - \alpha}", font_size=44, color=C.BITS), r"tokens per run", C.BITS),
            (VGroup(hb, ticks), r"FP4: \ dense near zero", C.BITS),
            (qbars, r"bits lost to rounding", C.INTERVAL),
            (VGroup(roof, dots), r"the roofline", C.TRUE_P),
            (Group(grid, VGroup(boxes, paged)).arrange(RIGHT, buff=0.25), r"tiles and pages", C.ATTN),
        ]
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
        head = label(r"Part 19, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Writing one token reads every weight, so memory sets the speed limit. A small model can "
            "guess ahead and the big one check its guesses at once, with exactly the same output. Numbers can be "
            "stored in eight bits, or four, for little loss. And the roofline says why all of this works: moving "
            "bytes is the cost, so FlashAttention computes in tiles and servers hand out memory in pages."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"the key-value cache, \ now in pages", [12]),
            (r"experts: \ fewer weights read per token", [13]),
            (r"thinking longer: \ more tokens to pay for", [17, 18]),
        ], font_size=26, title=r"Where this came from")
        with self.voiceover(
            "This part paid off ideas from earlier ones. The key-value cache of part twelve is what the pages hold. "
            "Mixture-of-experts, from part thirteen, is the same idea as quantization: read fewer bytes per token. "
            "And the long chains of thought of parts seventeen and eighteen are why speed matters so much."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        sp = load20("superposition")
        W = np.asarray(sp["W0.97"])
        head = label(r"Next: \ Part 20, \ Inside the Model", font_size=40).to_edge(UP, buff=0.4)
        c0 = DOWN * 0.3
        sc = 1.6 / max(np.linalg.norm(W, axis=0).max(), 1e-6)
        circ = Circle(radius=1.6, stroke_color=GREY_D, stroke_width=1.5).move_to(c0)
        arrows = VGroup(*[Arrow(c0, c0 + sc * np.array([W[0, i], W[1, i], 0]), buff=0, stroke_width=4, color=col,
                                max_tip_length_to_length_ratio=0.12)
                          for i, col in enumerate((C.TRUE_P, C.BITS, C.INTERVAL, C.SURPRISE, C.NEURAL))])
        cap = label(r"$5$ features in $2$ dimensions", font_size=24, color=GREY_A).next_to(circ, DOWN, buff=0.3)
        with self.voiceover(
            "Next time, the last part: looking inside the model. How a network packs more ideas than it has "
            "dimensions, <bookmark mark='a'/> five directions squeezed into a plane, and how to pull them back apart."
        ) as vo:
            self.play(FadeIn(head), Create(circ))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in arrows], lag_ratio=0.2), FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [r"J.~L.~Hennessy \& D.~A.~Patterson, \textit{Computer Architecture: A Quantitative Approach} (6th ed., 2017)"]
        papers = [
            r"Y.~Leviathan, M.~Kalman \& Y.~Matias, \textit{Fast Inference from Transformers via Speculative Decoding} (2023); "
            r"\ C.~Chen et al.\ (2023)",
            r"E.~Frantar et al., \textit{GPTQ} (2023); \ T.~Dettmers et al., \textit{LLM.int8()} (2022); "
            r"\ B.~D.~Rouhani et al., \textit{Microscaling Data Formats} (2023)",
            r"T.~Dao et al., \textit{FlashAttention} (2022); \ M.~Milakov \& N.~Gimelshein, \textit{Online normalizer calculation for softmax} (2018)",
            r"S.~Williams, A.~Waterman \& D.~Patterson, \textit{Roofline} (2009); \ W.~Kwon et al., \textit{PagedAttention} (2023)",
        ]
        card = reference_card(books, papers)
        data = note(r"Every number here is computed and checked on this computer; \ chip and model figures as published; "
                    r"\ illustrations are labeled.", font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover("Thanks for watching, and see you in the final part."):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
