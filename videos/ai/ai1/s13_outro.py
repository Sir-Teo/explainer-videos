from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import MONO, area_slivers, load, plain_axes


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        """Part 1 in eight pictures, each redrawn small from the part's own numbers."""
        lt, kl, od, sm, sb = load("letters"), load("kl"), load("orders"), load("softmax"), load("scoreboard")
        TW, TH = 3.0, 2.0  # drawing area of a tile

        def frame(caption, color):
            box = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                                   stroke_width=1.5, fill_color="#121722", fill_opacity=1)
            cap = label(caption, font_size=22, color=color).move_to(box.get_bottom() + UP * 0.28)
            return box, cap

        def axes_box(xr, yr):
            return Axes(x_range=xr, y_range=yr, x_length=TW, y_length=TH - 0.2, tips=False,
                        axis_config={"stroke_color": GREY_D, "stroke_width": 1.5, "include_ticks": False})

        out = []
        # 1. the chain rule: nested slivers
        g = VGroup()
        y = 0.7
        for k, (a, b) in enumerate([(0.30, 0.45), (0.15, 0.75), (0.2, 0.9)]):
            bar = Rectangle(width=TW, height=0.28, stroke_width=1, stroke_color=GREY_C, fill_color="#1B2638", fill_opacity=1)
            bar.move_to([0, y - 0.62 * k, 0])
            hi_ = Rectangle(width=TW * (b - a), height=0.28, stroke_width=0, fill_color=C.INTERVAL, fill_opacity=0.9)
            hi_.move_to(bar.get_left() + RIGHT * TW * (a + b) / 2)
            g.add(bar, hi_)
            if k < 2:
                g.add(Polygon(hi_.get_corner(DL), hi_.get_corner(DR), bar.get_corner(DR) + DOWN * 0.34,
                              bar.get_corner(DL) + DOWN * 0.34, stroke_width=0, fill_color=C.INTERVAL, fill_opacity=0.15))
        out.append((g, r"the chain rule", C.INTERVAL))
        # 2. surprise
        ax = axes_box([0, 1, 1], [0, 6, 1])
        xs = np.linspace(2 ** -6, 1, 200)
        g = VGroup(ax, ax.plot_line_graph(xs, -np.log2(xs), add_vertex_dots=False, line_color=C.SURPRISE,
                                         stroke_width=3.5))
        out.append((g, r"surprise $= \log_2 \frac1p$", C.SURPRISE))
        # 3. entropy: the area picture
        g = area_slivers(lt["p"], W=TW, y0=-TH / 2 + 0.1, scale=0.15, order=list(lt["order"]), color=C.ENTROPY)
        out.append((g, rf"entropy: \ ${float(lt['H']):.2f}$ bits", C.ENTROPY))
        # 4. cross-entropy and KL: a wrong model of two peaks
        x, pp = np.asarray(kl["x"]), np.asarray(kl["p"])
        ax = axes_box([float(x[0]), float(x[-1]), 1], [0, float(pp.max()) * 1.15, 1])
        m, sd = float(kl["mean"]), float(kl["sd"])
        qq = np.exp(-0.5 * ((x - m) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))
        g = VGroup(ax, ax.plot_line_graph(x, pp, add_vertex_dots=False, line_color=C.TRUE_P, stroke_width=3),
                   ax.plot_line_graph(x, qq, add_vertex_dots=False, line_color=C.MODEL_Q, stroke_width=3))
        out.append((g, r"cross-entropy, $D_{\mathrm{KL}}$", C.KL))
        # 5. arithmetic coding: one number for the whole message
        bits = Text("0.11001010000101111011011001110", font=MONO, font_size=16, color=C.BITS)
        bits.width = TW
        bar = Rectangle(width=TW, height=0.3, stroke_width=1, stroke_color=GREY_C).move_to(UP * 0.35)
        sl = Rectangle(width=0.05, height=0.3, stroke_width=0, fill_color=C.INTERVAL, fill_opacity=1).move_to(
            bar.get_left() + RIGHT * TW * 0.79)
        g = VGroup(bar, sl, Line(sl.get_bottom(), bits.get_top() + UP * 0.05, color=C.INTERVAL, stroke_width=1.5),
                   bits.move_to(DOWN * 0.45))
        out.append((g, r"predicting $=$ compressing", C.INTERVAL))
        # 6. generalization: the books vs new text
        rows = od["rows"]
        ks = np.arange(len(rows))
        ax = axes_box([0, 14, 1], [0, 4.5, 1])
        g = VGroup(ax, ax.plot_line_graph(ks, [r["plugin"] for r in rows], add_vertex_dots=False, line_color=C.COUNTING,
                                          stroke_width=3),
                   ax.plot_line_graph(ks, [r["test"] for r in rows], add_vertex_dots=False, line_color=C.SURPRISE,
                                      stroke_width=3))
        out.append((g, r"memorizing $\ne$ generalizing", C.COUNTING))
        # 7. the gradient: guess minus truth
        phat, q = np.asarray(sm["phat"]), np.asarray(sm["q"])[3]
        g = VGroup()
        for k in range(5):
            xk = -TW / 2 + 0.3 + k * (TW - 0.6) / 4
            hp, hq = 2.6 * phat[k], 2.6 * q[k]
            g.add(Rectangle(width=0.36, height=hp, stroke_color=C.TRUE_P, stroke_width=2).move_to([xk, -0.8 + hp / 2, 0]))
            g.add(Rectangle(width=0.24, height=hq, stroke_width=0, fill_color=C.MODEL_Q, fill_opacity=0.85)
                  .move_to([xk, -0.8 + hq / 2, 0]))
            if abs(hq - hp) > 0.05:
                g.add(Arrow([xk + 0.28, -0.8 + hq, 0], [xk + 0.28, -0.8 + hp, 0], buff=0, color=C.BITS, stroke_width=2.5,
                            max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=10))
        out.append((g, r"the gradient: \ $q - \hat p$", C.MODEL_Q))
        # 8. the scoreboard
        vals = [r for r in sb["rows"] if r.get("bits") is not None]
        kind_col = {"counting": C.COUNTING, "compressor": C.COMPRESSOR, "lm": C.NEURAL}
        g = VGroup()
        for k, r in enumerate(vals):
            wdt = TW * r["bits"] / 8.0
            g.add(Rectangle(width=wdt, height=0.11, stroke_width=0, fill_color=kind_col.get(r.get("kind"), GREY_B),
                            fill_opacity=0.9).move_to([-TW / 2 + wdt / 2, TH / 2 - 0.15 - k * 0.15, 0]))
        out.append((g, r"$8 \to 0.87$ bits", WHITE))
        tiles = Group()
        for k, (pic, cap, col) in enumerate(out):
            box, c = frame(cap, col)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(r"Part 1, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. We wrote guesses down as probability distributions, and the chain rule turned them "
            "into a score for a whole text. We found that there's only one sensible measure of surprise, and that "
            "entropy, the average surprise, is the speed limit of compression. We met the price of a wrong model, "
            "the cross-entropy, and the divergence inside it. Arithmetic coding showed that predicting and "
            "compressing are the same thing. Counting models showed us generalization, by failing at it. And we "
            "derived the gradient that trains every language model: the guess, minus the truth."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15, scale=0.95) for t in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"the chain rule: \ next-token prediction", [13, 23, 28]),
            (r"cross-entropy: \ the training loss", [9, 11, 12]),
            (r"forward and reverse $D_{\mathrm{KL}}$", [21, 28]),
            (r"prediction $=$ compression", [12, 30]),
            (r"memorizing vs.\ generalizing", [7, 8]),
            (r"mutual information, long memory", [13, 15]),
            (r"softmax, and its gradient $q - \hat p$", [4, 11]),
        ], font_size=24)
        with self.voiceover(
            "Almost everything here comes back. The chain rule is how language models generate text, and how "
            "reasoning models think out loud. Cross-entropy is the loss we'll be minimizing for the rest of the "
            "series. The two directions of the divergence return in diffusion models and in reinforcement learning. "
            "Compression returns when we study scaling, and when we look inside the models at the end."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        v = load("vectors")
        words = [w.strip() for w in v["words"]]
        cos = np.asarray(v["cos"])
        i = {w: k for k, w in enumerate(words)}
        assert abs(cos[i["dog"], i["puppy"]] - 0.621) < 0.001 and abs(cos[i["dog"], i["tobacco"]] - 0.229) < 0.001
        head = label(r"Next: \ Part 3, \ Vectors That Mean Things", font_size=40).to_edge(UP, buff=0.3)
        # cosine similarity grid of GPT-2's word vectors
        n, cell = len(words), 0.5
        x0, y0 = -6.2, 1.7
        grid = VGroup()
        for a in range(n):
            for b in range(n):
                c = float(cos[a, b])
                col = interpolate_color(ManimColor("#161C28"), ManimColor(C.TRUE_P), min(1.0, max(0.0, (c - 0.15) / 0.65)))
                sq = Square(cell, stroke_width=0.5, stroke_color=BACKGROUND, fill_color=col, fill_opacity=1)
                sq.move_to([x0 + 1.6 + (b + 0.5) * cell, y0 - (a + 0.5) * cell, 0])
                grid.add(sq)
        rl = VGroup(*[Text(w, font=MONO, font_size=16, color=GREY_A).next_to(grid[a * n], LEFT, buff=0.1)
                      for a, w in enumerate(words)])
        cl = VGroup(*[Text(w, font=MONO, font_size=16, color=GREY_A).rotate(PI / 3).next_to(grid[b], UP, buff=0.08)
                      for b, w in enumerate(words)])
        vals = VGroup(*[MathTex(f"{cos[a, b]:.2f}", font_size=15, color=WHITE).move_to(grid[a * n + b])
                        for a in range(n) for b in range(n) if a != b])
        gcap = label(r"GPT-2's own word vectors: \ cosine similarity", font_size=22, color=GREY_A)
        gcap.next_to(grid, DOWN, buff=0.3)
        # random directions: 3 dimensions versus 768
        ax = plain_axes([-1, 1, 0.5], [0, 1, 0.5], 5.2, 3.0).move_to([3.6, -0.2, 0])
        xl = VGroup(*[MathTex(t, font_size=20, color=GREY_B).next_to(ax.c2p(x, 0), DOWN, buff=0.1)
                      for t, x in (("-1", -1), ("0", 0), ("1", 1))])
        bars = VGroup()
        for dim, col, op in ((3, GREY_B, 0.5), (768, C.BITS, 0.9)):
            h = np.asarray(v[f"random{dim}"], float)
            h = h / h.max()
            w = 2 / len(h)
            for k, hv in enumerate(h):
                if hv <= 0:
                    continue
                x = -1 + (k + 0.5) * w
                bars.add(Rectangle(width=ax.x_length * w / 2 * 0.95, height=ax.y_length * hv * (0.5 if dim == 3 else 1),
                                   stroke_width=0, fill_color=col, fill_opacity=op)
                         .move_to(ax.c2p(x, 0), aligned_edge=DOWN))
        hl = VGroup(label(r"random directions in $3$ dimensions", font_size=20, color=GREY_B),
                    label(r"\ldots in $768$: \ almost all at right angles", font_size=20, color=C.BITS))
        hl.arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax, UP, buff=0.2)
        assert abs(v["sd768"] - 0.036) < 0.001
        with self.voiceover(
            "Next time: the problem that broke counting. A counting model can't tell that a dog and a puppy are "
            "alike. <bookmark mark='a'/> Neural models can, because they represent every word as a long list of "
            "numbers, a vector, and similar words get similar vectors. In GPT-2's own vectors, dog sits close to "
            "puppy, and far from tobacco. <bookmark mark='b'/> And high-dimensional space is strange: pick two "
            "random directions in 768 dimensions, and they're almost always at right angles. There's room for an "
            "enormous number of nearly separate meanings. Part three is the linear algebra and geometry behind that."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid), FadeIn(rl), FadeIn(cl), FadeIn(gcap), run_time=1.5)
            self.play(FadeIn(vals))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xl), FadeIn(hl), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                                                                       lag_ratio=0.01), run_time=2.0)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [
            r"T.~M.~Cover \& J.~A.~Thomas, \textit{Elements of Information Theory}, 2nd ed.\ (2006), chapters 2, 5, 13",
            r"D.~J.~C.~MacKay, \textit{Information Theory, Inference, and Learning Algorithms} (2003), chapters 2, 4--6",
            r"C.~M.~Bishop \& H.~Bishop, \textit{Deep Learning: Foundations and Concepts} (2024), chapter 2",
        ]
        papers = [
            r"C.~E.~Shannon, \textit{A Mathematical Theory of Communication}, Bell Syst.~Tech.~J.\ (1948)",
            r"C.~E.~Shannon, \textit{Prediction and Entropy of Printed English}, Bell Syst.~Tech.~J.\ (1951)",
            r"L.~G.~Kraft (1949); \ D.~A.~Huffman, \textit{A Method for the Construction of Minimum-Redundancy Codes} (1952)",
            r"S.~Kullback \& R.~A.~Leibler, \textit{On Information and Sufficiency} (1951); \ R.~A.~Fisher (1922)",
            r"J.~Rissanen (1976); \ R.~Pasco (1976); \ I.~H.~Witten, R.~M.~Neal \& J.~G.~Cleary, \textit{Arithmetic "
            r"Coding for Data Compression} (1987)",
            r"T.~M.~Cover \& R.~C.~King, \textit{A Convergent Gambling Estimate of the Entropy of English} (1978)",
            r"H.~W.~Lin \& M.~Tegmark, \textit{Critical Behavior in Physics and Probabilistic Formal Languages} (2017)",
            r"G.~Del\'etang et al., \textit{Language Modeling Is Compression} (ICLR 2024)",
            r"A.~Radford et al., \textit{Language Models are Unsupervised Multitask Learners} (GPT-2, 2019); \ "
            r"Qwen Team, \textit{Qwen3 Technical Report} (2025)",
        ]
        card = reference_card(books, papers)
        data = note(r"Text: Project Gutenberg (30 novels; \textit{The Maltese Falcon}, eBook \#77600). \ Every "
                    r"number on screen is computed and checked; \ schematics and illustrations are labeled.",
                    font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover(
            "This part followed the first chapters of Cover and Thomas's Elements of Information Theory, and "
            "MacKay's Information Theory, Inference, and Learning Algorithms, both of which go much further. The "
            "papers are all worth reading, starting with Shannon's two. Thanks for watching, and see you in part three."
        ) as vo:
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
