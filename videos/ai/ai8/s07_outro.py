from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import CLS_B, HINGE, NEURON, curve, load, patch_image, region_image


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

        def axes(xr, yr):
            return Axes(x_range=xr, y_range=yr, x_length=TW, y_length=TH - 0.2, tips=False,
                        axis_config={"stroke_color": GREY_D, "include_ticks": False})

        out = []
        # 1. a unit
        a1 = axes([-2, 2, 1], [-0.5, 2, 1])
        out.append((VGroup(a1, VMobject(color=NEURON, stroke_width=4).set_points_as_corners(
            [a1.c2p(-2, 0), a1.c2p(0, 0), a1.c2p(2, 2)])), r"a unit: \ a hinge", NEURON))
        # 2. hinges add up
        h = load("hinges")
        a2 = axes([-3, 3, 1], [-2.2, 2.2, 1])
        out.append((VGroup(a2, curve(a2, h["xs"], np.clip(h["fit16"], -2.2, 2.2), HINGE, 3)), r"any curve", HINGE))
        # 3. the sawtooth
        s = load("sawtooth")
        a3 = axes([0, 1, 1], [0, 1, 1])
        out.append((VGroup(a3, curve(a3, s["xs"], s["tent4"], HINGE, 2.5)), r"depth folds", HINGE))
        # 4. random pieces
        out.append((Group(patch_image(s["map3"], TW * 0.7, TH * 0.95, seed=3)), r"pieces at random", NEURON))
        # 5. signal propagation
        g = load("signal")
        a5 = axes([0, 50, 10], [0, 18, 3])
        ls = np.arange(1, 51)
        sig = VGroup(a5, *[curve(a5, ls, np.clip(np.log10(np.maximum(np.asarray(g[k]), 1e-30)), -9, 9) + 9, col, 2.5)
                           for k, col in (("sd_small", "#7FD3FF"), ("sd_he", C.BITS), ("sd_big", C.SURPRISE))])
        out.append((sig, r"$\mathrm{Var}(w) = 2/n$", C.BITS))
        # 6. residual
        r = load("residual")
        a6 = axes([0, 1500, 500], [0.4, 1, 0.2])
        out.append((VGroup(a6, curve(a6, r["plain"][:, 0], r["plain"][:, 2], C.SURPRISE, 2.5),
                           curve(a6, r["residual"][:, 0], r["residual"][:, 2], C.BITS, 3)), r"residual streams", C.BITS))
        # 7. the spirals
        sp = load("spiral")
        out.append((Group(region_image(sp["prob3000"], sp["regions3000"], sp["xs"], TH * 0.95, TH * 0.95)),
                    r"two spirals", CLS_B))
        # 8. the neural language model's training
        d = load("lm")
        cv = np.asarray(d["curve"])
        a8 = axes([0, cv[-1, 0], 10000], [1.6, 4.6, 1])
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
        head = label(r"Part 8, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        from videos.ai.ai8.s06_lm import load_kn

        lm, kn = load("lm"), load_kn()
        if float(lm["passage_bits"]) < float(kn["best_bits"]):
            last = "And a small network, trained on our books, beat every counting model on the scoreboard."
        else:
            last = ("And a small network, trained on our books, came close to the best counting model, and mixed with "
                    "it, beat every counting model on the scoreboard.")
        with self.voiceover(
            "Let's take stock. A unit is a weighted sum and a bend, and enough of them in one layer can approximate "
            "any curve. Depth can fold space into exponentially many pieces, though random networks don't use that "
            "power. Weights must start at the right size, two over n for ReLUs, or signals vanish or explode. "
            "Residual connections let gradients through forty layers. " + last
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15, scale=0.95) for t in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"initialization, width and depth", [9, 10]),
            (r"the residual stream", [11, 20]),
            (r"normalization", [9, 11]),
            (r"learned embeddings", [11, 16]),
            (r"the neural LM, grown up", [11, 12]),
        ], font_size=26)
        with self.voiceover(
            "How to set the scale of weights and learning rates as networks grow is the subject of parts nine and "
            "ten. The residual stream is the backbone of the transformer in part eleven, and what we read when we "
            "look inside models, in part twenty. And learned embeddings, of characters here, become embeddings of "
            "tokens, images and sounds."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 9, \ Going Downhill", font_size=40).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[-4, 4, 1], y_range=[-2.5, 2.5, 1], x_length=9.0, y_length=5.0, tips=False,
                  axis_config={"stroke_width": 0}).move_to(DOWN * 0.4)

        def f(x, y):
            return 0.08 * x * x + 0.9 * y * y

        cont = contour_lines(ax, f, (-4, 4), (-2.5, 2.5), [0.1, 0.4, 0.9, 1.6, 2.5, 3.6], n=(100, 70), stroke_width=1.6)
        g = np.random.default_rng(9)
        p, pts = np.array([-3.6, 2.0]), []
        for _ in range(60):
            pts.append(p.copy())
            p = p - 0.5 * np.array([0.16 * p[0], 1.8 * p[1]]) + g.normal(scale=0.12, size=2)
        path = VMobject(color=WHITE, stroke_width=3).set_points_as_corners([ax.c2p(*q) for q in pts])
        tag = label(r"noisy steps down a narrow valley \ (illustrative)", font_size=24, color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Next time: the optimizers. Stochastic gradient descent, and why its noise helps; momentum, Adam and "
            "AdamW; the newer Muon; and the learning-rate schedules that large models are trained with. "
            "<bookmark mark='a'/> Part three's valley, revisited with everything we know now."
        ) as vo:
            self.play(FadeIn(head), Create(cont), FadeIn(tag))
            self.play(Create(path), run_time=3.0)
            vo.wait_until("a")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [
            r"I.~Goodfellow, Y.~Bengio \& A.~Courville, \textit{Deep Learning} (2016), chapters 6 and 8",
            r"S.~J.~D.~Prince, \textit{Understanding Deep Learning} (2023), chapters 3--4, 7, 11",
            r"D.~A.~Roberts, S.~Yaida \& B.~Hanin, \textit{The Principles of Deep Learning Theory} (2022)",
        ]
        papers = [
            r"G.~Cybenko (1989); \ K.~Hornik, M.~Stinchcombe \& H.~White (1989): \ universal approximation",
            r"M.~Telgarsky, \textit{Benefits of Depth in Neural Networks} (2016); \ B.~Hanin \& D.~Rolnick (2019)",
            r"X.~Glorot \& Y.~Bengio (2010); \ K.~He, X.~Zhang, S.~Ren \& J.~Sun, \textit{Delving Deep into Rectifiers} (2015)",
            r"K.~He, X.~Zhang, S.~Ren \& J.~Sun, \textit{Deep Residual Learning for Image Recognition} (2015)",
            r"J.~L.~Ba, J.~R.~Kiros \& G.~E.~Hinton, \textit{Layer Normalization} (2016)",
            r"Y.~Bengio, R.~Ducharme, P.~Vincent \& C.~Jauvin, \textit{A Neural Probabilistic Language Model} (2003)",
        ]
        card = reference_card(books, papers)
        data = note(r"Text: Project Gutenberg (Part 1's $30$ novels). \ Networks trained here, with PyTorch; \ every number "
                    r"on screen is computed and checked.", font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover(
            "Simon Prince's Understanding Deep Learning is the clearest modern textbook, and free to read. Thanks "
            "for watching, and see you in part nine."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
