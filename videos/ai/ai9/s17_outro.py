from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import (BWD, CLS_A, CLS_B, CRIT, HINGE, NEURON, PART, PLAIN, RES, WEIGHT,
                                  load, region_image)
from videos.ai.ai9.s08_depth import fold_picture
from videos.ai.ai9.s11_chaos import chi_image


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0

        def frame(caption, color):
            box = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                                   stroke_width=1.5, fill_color="#121722", fill_opacity=1)
            return box, label(caption, font_size=22, color=color).move_to(box.get_bottom() + UP * 0.28)

        def axes_(xr, yr):
            return Axes(x_range=xr, y_range=yr, x_length=TW, y_length=TH - 0.2, tips=False,
                        axis_config={"stroke_color": GREY_D, "include_ticks": False})

        out = []
        # 1. the perceptron's final line
        p = load("perceptron")
        X, y, w = np.asarray(p["X"]), np.asarray(p["y"]), np.asarray(p["ws"])[-1]
        s = TH * 0.95 / 4.6
        dots = VGroup(*[Dot([a * s, b * s, 0], radius=0.03, color=CLS_B if v > 0 else CLS_A) for (a, b), v in zip(X, y)])
        from videos.ai.ai9.s03_perceptron import clip_line
        seg = clip_line(w)
        ln = Line([seg[0][0] * s, seg[0][1] * s, 0], [seg[1][0] * s, seg[1][1] * s, 0], color=WEIGHT, stroke_width=3)
        out.append((VGroup(Square(4.6 * s, stroke_color=GREY_D, stroke_width=1), dots, ln),
                    rf"perceptron: \ ${int(p['mistakes'])}$ mistakes", WEIGHT))
        # 2. XOR, learned
        x = load("xor")
        out.append((Group(region_image(x[f"q{x['keep'][-1]}"], np.zeros((2, 2)), x["xs"], TH * 0.95, TH * 0.95, boundary=False)),
                    r"XOR: \ a hidden layer", BWD))
        # 3. hinges
        h = load("hinges")
        a3 = axes_([-3, 3, 1], [-2.2, 2.2, 1])
        out.append((VGroup(a3, curve(a3, h["xs"], np.clip(h["fit16"], -2.2, 2.2), HINGE, 3)), r"any curve, \ from hinges",
                    HINGE))
        # 4. Barron
        b = load("barron")
        a4 = axes_([0, 5, 1], [-4, 0, 1])
        lines = VGroup(a4)
        for d, col in ((1, "#9BE37B"), (4, "#58A6FF"), (8, "#FF9F45")):
            lines.add(DashedVMobject(curve(a4, np.log10(b[f"grid_n{d}"]), np.log10(np.maximum(b[f"grid{d}"], 1e-4)), col, 2.5),
                                     num_dashes=12))
        lines.add(curve(a4, np.log10(b["mc_n"]), np.log10(b["mc64"]), "#FF6B8B", 3))
        out.append((lines, r"Barron: \ $1/\sqrt{n}$ in any $d$", NEURON))
        # 5. folds
        f = load("fold")
        out.append((Group(fold_picture(np.asarray(f["fold4"]), TH * 0.95)), r"depth folds the plane", HINGE))
        # 6. the edge of chaos
        m = load("meanfield")
        out.append((Group(chi_image(m["phase_chi"], TW * 0.95, TH * 0.95)), r"the edge of chaos", CRIT))
        # 7. residual
        r = load("residual")
        a7 = axes_([0, 1500, 500], [0.4, 1, 0.2])
        out.append((VGroup(a7, curve(a7, r["plain"][:, 0], r["plain"][:, 2], PLAIN, 2.5),
                           curve(a7, r["residual"][:, 0], r["residual"][:, 2], RES, 3)), r"residual streams", RES))
        # 8. the neural language model's training
        d = load("lm")
        cv = np.asarray(d["curve"])
        a8 = axes_([0, cv[-1, 0], 10000], [1.6, 4.6, 1])
        out.append((VGroup(a8, curve(a8, cv[:, 0], np.clip(cv[:, 2], 1.6, 4.6), C.NEURAL, 3)),
                    rf"a neural LM: \ ${d['passage_bits']:.2f}$ bits", C.NEURAL))
        tiles = Group()
        for pic, cap, col in out:
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
        head = label(rf"Part {PART}, \ in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        from videos.ai.ai9.s16_lm import load_kn

        lm, kn = load("lm"), load_kn()
        nn_b, kn_b, mix_b = float(lm["passage_bits"]), float(kn["best_bits"]), float(lm["mix_bits"])
        if nn_b < kn_b:
            last = "And a small network, trained on our books, beat every counting model on the scoreboard."
        elif mix_b < kn_b:
            last = ("And a small network, trained on our books, came close to the best counting model, and mixed with "
                    "it, beat every counting model on the scoreboard.")
        else:
            last = (f"And a small network, trained on our books, came within {nn_b - kn_b:.2f} bits of the best "
                    "counting model.")
        with self.voiceover(
            "Let's take stock. A unit is a weighted sum and a threshold, and the perceptron learns one from its "
            "mistakes, provably, whenever a line separates the data. One layer can't do XOR; two can, and "
            "backpropagation trains them, in one sweep backwards. One hidden layer can approximate any curve, and for "
            "smooth enough functions the number of units doesn't explode with the dimension. Depth folds space into "
            "exponentially many pieces. Weights must start on the edge of chaos, two over n for ReLUs, or signals "
            "vanish or explode, and residual streams and normalization keep gradients flowing through many layers. "
            + last
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15, scale=0.95) for t in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"convolution, \ and networks that remember", [10]),
            (r"initialization, width and depth", [11, 12]),
            (r"the residual stream", [13, 30]),
            (r"normalization, \ QK-norm", [13, 18]),
            (r"gated MLPs, \ as experts", [16]),
            (r"learned embeddings", [13, 23]),
        ], font_size=26)
        with self.voiceover(
            "All of this comes back. Weight sharing over space and time gives the convolutional and recurrent "
            "networks of Part 10. How to set the scale of weights and learning rates as networks grow is the subject "
            "of Parts 11 and 12. The residual stream is the backbone of the transformer in Part 13, and what we read "
            "when we look inside models, in Part 30. Normalization comes back inside attention. The gated MLP, "
            "multiplied, becomes the experts of Part 16. And learned embeddings, of characters here, become "
            "embeddings of tokens, images and sounds."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"Show that the perceptron started from $w_0 = 0$ makes exactly the same mistakes with the update "
            r"$w \leftarrow w + \eta\, y\, x$, for any $\eta > 0$, as with $\eta = 1$.",
            r"Find weights for a $2$--$2$--$1$ ReLU network that computes XOR exactly on $\{0, 1\}^2$.",
            r"For sigmoid units, show $\sigma' \le \tfrac14$. \ If every weight matrix has operator norm at most $1$, "
            r"show that $\|\delta^l\|$ shrinks by at least a factor of $4$ per layer.",
            r"For $z \sim N(0, q)$, show $\mathbb{E}[\max(0, z)^2] = q/2$, \ and deduce He's $\operatorname{Var}(W) = 2/n$.",
            r"Show that the $k$-fold composition of the tent map has $2^k$ linear pieces, while one hidden layer of $m$ "
            r"ReLUs on $\mathbb{R}$ has at most $m + 1$.",
            r"For $y = \sqrt{d}\, h / \|h\|$, show $\partial y / \partial h = \tfrac{\sqrt d}{\|h\|}(I - \hat h \hat h^{\top})$. "
            r"\ What does this imply about the gradient with respect to $h$?",
        ], font_size=22)
        with self.voiceover(
            "Here are six problems to try, from the perceptron's learning rate to the Jacobian of RMSNorm. Pause "
            "here and work through them; full solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 10, \ Seeing and Remembering", font_size=40).to_edge(UP, buff=0.4)
        n, s = 8, 0.42
        g = np.random.default_rng(10)  # an image and a filter (schematic)
        img = g.uniform(0, 1, (n, n))
        grid = VGroup(*[Square(s, stroke_width=0.8, stroke_color=GREY_D, fill_color=interpolate_color(
            ManimColor("#141A24"), ManimColor(NEURON), float(img[i, j])), fill_opacity=1)
            .move_to([-4.6 + (j - n / 2 + 0.5) * s, (n / 2 - 0.5 - i) * s - 0.3, 0]) for i in range(n) for j in range(n)])
        m = n - 2
        outg = VGroup(*[Square(s, stroke_width=0.8, stroke_color=GREY_D, fill_color="#141A24", fill_opacity=1)
                        .move_to([0.2 + (j - m / 2 + 0.5) * s, (m / 2 - 0.5 - i) * s - 0.3, 0]) for i in range(m) for j in range(m)])
        win = Square(3 * s, stroke_color=C.BITS, stroke_width=4).move_to(grid[0].get_center() + (RIGHT + DOWN) * s)
        k = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]) / 4.0
        vals = np.array([[(img[i:i + 3, j:j + 3] * k).sum() for j in range(m)] for i in range(m)])
        vals = (vals - vals.min()) / max(np.ptp(vals), 1e-9)
        tag = note(r"schematic").to_corner(DL, buff=0.25)
        items = VGroup(label(r"convolution: \ one small filter, \ slid everywhere", font_size=24, color=C.BITS),
                       label(r"2012: \ AlexNet and the ImageNet moment", font_size=24, color=GREY_A),
                       label(r"recurrent networks, \ LSTMs, \ the first attention", font_size=24, color=GREY_A),
                       label(r"a character LSTM on our scoreboard", font_size=24, color=C.NEURAL))
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.6, -0.3, 0])
        with self.voiceover(
            "Next time: seeing and remembering. A network that slides one small filter over an image, sharing its "
            "weights everywhere; 2012, when one of them won ImageNet by a wide margin; networks with loops that "
            "remember, the LSTM, and the first attention mechanism; and a character LSTM on our scoreboard."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid), FadeIn(outg), Create(win), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(it) for it in items], lag_ratio=0.5), run_time=2.0)
            steps = [(i, j) for i in range(m) for j in range(m)][:: 3]
            for i, j in steps:
                self.play(win.animate.move_to(grid[i * n + j].get_center() + (RIGHT + DOWN) * s),
                          outg[i * m + j].animate.set_fill(interpolate_color(ManimColor("#141A24"), ManimColor(C.BITS),
                                                                             float(vals[i, j]))), run_time=0.18)
            for i in range(m):
                for j in range(m):
                    outg[i * m + j].set_fill(interpolate_color(ManimColor("#141A24"), ManimColor(C.BITS), float(vals[i, j])))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [
            r"I.~Goodfellow, Y.~Bengio \& A.~Courville, \textit{Deep Learning} (2016), chapters 6 and 8",
            r"S.~J.~D.~Prince, \textit{Understanding Deep Learning} (2023), chapters 3--4, 7, 11",
            r"D.~A.~Roberts, S.~Yaida \& B.~Hanin, \textit{The Principles of Deep Learning Theory} (2022)",
            r"M.~Minsky \& S.~Papert, \textit{Perceptrons} (1969); \ D.~E.~Rumelhart, J.~L.~McClelland et al., "
            r"\textit{Parallel Distributed Processing} (1986)",
        ]
        papers = [
            r"McCulloch \& Pitts (1943); \ Hebb (1949); \ Rosenblatt (1958); \ Widrow \& Hoff (1960); \ Novikoff (1962)",
            r"Linnainmaa (1970); \ Werbos (1974); \ Rumelhart, Hinton \& Williams (1986); \ LeCun et al.\ (1989, 1998)",
            r"Cybenko (1989); \ Hornik, Stinchcombe \& White (1989); \ Leshno et al.\ (1993); \ Barron (1993); \ "
            r"Telgarsky (2016); \ Mont\'ufar et al.\ (2014); \ Hanin \& Rolnick (2019)",
            r"Hochreiter (1991); \ Bengio, Simard \& Frasconi (1994); \ Hinton, Osindero \& Teh (2006); \ Glorot \& "
            r"Bengio (2010); \ He et al.\ (2015)",
            r"Poole et al.\ (2016); \ Schoenholz et al.\ (2017); \ Pennington et al.\ (2017); \ Xiao et al.\ (2018)",
            r"He et al., ResNet (2015); \ Srivastava et al.\ (2015); \ Veit et al.\ (2016); \ Ioffe \& Szegedy (2015); \ "
            r"Ba et al.\ (2016); \ Zhang \& Sennrich (2019); \ Xiong et al.\ (2020)",
            r"Hendrycks \& Gimpel (2016); \ Dauphin et al.\ (2017); \ Shazeer (2020); \ Kolmogorov (1957); \ Arnold "
            r"(1957); \ Liu et al., KAN (2024); \ Yu et al.\ (2024)",
            r"Bengio, Ducharme, Vincent \& Jauvin, \textit{A Neural Probabilistic Language Model} (2003)",
        ]
        card = reference_card(books, papers, font_size=19)
        data = note(r"Text: Project Gutenberg (Part 1's $30$ novels). \ Networks trained here, with PyTorch and the series' "
                    r"own autodiff; \ every number on screen is computed or cited.", font_size=18).to_edge(DOWN, buff=0.2)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=18)
        credit.next_to(data, UP, buff=0.08)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.12:
            card.scale((card.height - (credit.get_top()[1] + 0.12 - card.get_bottom()[1])) / card.height)
            card.next_to(credit, UP, buff=0.12)
        with self.voiceover(
            "Simon Prince's Understanding Deep Learning is the clearest modern textbook, and free to read. Thanks "
            "for watching, and see you in Part 10."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
