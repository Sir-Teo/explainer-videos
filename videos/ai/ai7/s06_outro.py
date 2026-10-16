from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import AUSTEN, BIAS, DICKENS, TEST, TRAIN, VAR, curve, load


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
        g = load("gap")
        ax = axes([0, 150, 50], [0, 0.4, 0.1])
        out.append((VGroup(ax, curve(ax, g["ks"], g["train_err"], TRAIN, 2.5), curve(ax, g["ks"], g["test_err"], TEST, 3)),
                    r"the gap", TEST))
        b = load("biasvar")
        xg, tr = np.asarray(b["xg"]), np.asarray(b["truth"])
        for key, cap, col in (("fits_1", r"bias", BIAS), ("fits_top", r"variance", VAR)):
            a2 = axes([-1.5, 1.5, 1], [-2.2, 2.2, 1])
            fits = VGroup(*[curve(a2, xg, np.clip(f, -2.2, 2.2), col, 1.4).set_stroke(opacity=0.6)
                            for f in np.asarray(b[key])[:12]])
            out.append((VGroup(a2, fits, DashedVMobject(curve(a2, xg, tr, WHITE, 2), num_dashes=30)), cap, col))
        a3 = axes([0, 15, 3], [-1, 1.5, 1])  # (log scale, as in chapter 1)
        out.append((VGroup(a3, curve(a3, b["degs"], np.clip(np.log10(np.asarray(b["total"])), -1, 1.5), TEST, 3)),
                    r"the U", TEST))
        s = load("shatter")
        P3 = np.asarray(s["P3"])
        sh = VGroup(*[Dot([p[0], p[1], 0], radius=0.1, color=c) for p, c in zip(P3, (DICKENS, AUSTEN, DICKENS))],
                    Line([-1.2, 0.5, 0], [1.2, -0.9, 0], color=C.BITS, stroke_width=3))
        out.append((sh, r"VC dimension", C.BITS))
        r = load("rademacher")
        a4 = axes([0, 70, 10], [0.5, 0.75, 0.1])
        out.append((VGroup(a4, curve(a4, r["ds"], np.clip(r["acc"], 0.5, 0.75), C.MODEL_Q, 3)), r"fitting coin flips",
                    C.MODEL_Q))
        rl = load("random")
        S = np.asarray(rl["shuffled"])
        a5 = axes([0, 3.2, 1], [0.4, 1, 0.2])
        out.append((VGroup(a5, curve(a5, np.log10(S[:, 0]), S[:, 1], TRAIN, 2.5), curve(a5, np.log10(S[:, 0]), S[:, 2], TEST, 3)),
                    r"memorizing nonsense", TRAIN))
        d = load("double")
        a6 = axes([1, 3.8, 1], [-1, 2, 1])
        out.append((VGroup(a6, curve(a6, np.log10(d["ps"]), np.clip(np.log10(d["test"]), -1, 2), TEST, 3)),
                    r"double descent", TEST))
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
        head = label(r"Part 7, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. A model's error on new data is what matters, and it can be far from its error on the "
            "data it learned from. The classical story splits that error into bias, variance and noise, and bounds "
            "it by capacity: how many points a model can split every way, how well it can fit coin flips. Then "
            "networks memorized pure nonsense, and still generalized on real labels; and test error, past the point "
            "of fitting everything exactly, came back down."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15, scale=0.95) for t in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"held-out data, \ the honest score", [10, 17]),
            (r"which exact fit training finds", [9]),
            (r"more parameters than data", [10]),
            (r"memorization", [19, 20]),
        ], font_size=26)
        with self.voiceover(
            "Held-out data stays the honest score, from scaling laws in part ten to evaluating reasoning models in "
            "part seventeen. Which of the many fits training finds is the subject of part nine. Models far bigger "
            "than their data are the subject of part ten. And memorization, of facts and of text, comes back when we "
            "look inside models."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 8, \ Networks", font_size=40).to_edge(UP, buff=0.35)
        # a small random ReLU network, 2 -> 12 -> 12 -> 1, carves the plane into linear pieces (illustrative)
        g = np.random.default_rng(8)
        W1, b1 = g.normal(size=(2, 12)), g.normal(size=12) * 0.6
        W2, b2 = g.normal(size=(12, 12)) / math.sqrt(12), g.normal(size=12) * 0.3
        xs, ys = np.linspace(-3, 3, 240), np.linspace(-2, 2, 160)
        X, Y = np.meshgrid(xs, ys)
        P = np.stack([X.ravel(), Y.ravel()], 1)
        h1 = P @ W1 + b1
        h2 = np.maximum(h1, 0) @ W2 + b2
        code = ((h1 > 0).astype(np.int64) @ (1 << np.arange(12))) * 4099 + ((h2 > 0).astype(np.int64) @ (1 << np.arange(12)))
        _, inv = np.unique(code, return_inverse=True)
        hue = (inv * 0.61803) % 1.0
        rgb = np.stack([0.35 + 0.35 * np.sin(2 * math.pi * hue), 0.4 + 0.3 * np.sin(2 * math.pi * (hue + 0.33)),
                        0.55 + 0.3 * np.sin(2 * math.pi * (hue + 0.66))], 1).reshape(len(ys), len(xs), 3)
        img = ImageMobject((np.concatenate([rgb, np.ones(rgb.shape[:2] + (1,))], -1)[::-1] * 255).astype(np.uint8))
        img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        img.stretch_to_fit_width(9.0).stretch_to_fit_height(6.0).move_to(DOWN * 0.4)
        n_regions = len(np.unique(inv))
        tag = label(rf"a small ReLU network cuts the plane into ${n_regions}$ flat pieces \ (illustrative)", font_size=24,
                    color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Next time: networks themselves. Why a stack of simple layers can approximate any function, how depth "
            "cuts space into pieces, how to start and keep signals alive through many layers. <bookmark mark='a'/> "
            "And the first neural language model joins the scoreboard."
        ) as vo:
            self.play(FadeIn(head), FadeIn(img), FadeIn(tag), run_time=2.0)
            vo.wait_until("a")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [
            r"S.~Shalev-Shwartz \& S.~Ben-David, \textit{Understanding Machine Learning} (2014)",
            r"T.~Hastie, R.~Tibshirani \& J.~Friedman, \textit{The Elements of Statistical Learning} (2009), chapter 7",
            r"V.~Vapnik, \textit{The Nature of Statistical Learning Theory} (1995)",
        ]
        papers = [
            r"S.~Geman, E.~Bienenstock \& R.~Doursat, \textit{Neural Networks and the Bias/Variance Dilemma} (1992)",
            r"V.~Vapnik \& A.~Chervonenkis, \textit{On the Uniform Convergence of Relative Frequencies of Events} (1971)",
            r"P.~Bartlett \& S.~Mendelson, \textit{Rademacher and Gaussian Complexities} (2002)",
            r"C.~Zhang et al., \textit{Understanding Deep Learning Requires Rethinking Generalization} (2017)",
            r"M.~Belkin, D.~Hsu, S.~Ma \& S.~Mandal, \textit{Reconciling Modern Machine Learning Practice and the "
            r"Bias-Variance Trade-off} (2019)",
            r"P.~Nakkiran et al., \textit{Deep Double Descent} (2020)",
        ]
        card = reference_card(books, papers)
        data = note(r"Pages: Part 5's Austen and Dickens. \ Every number on screen is computed and checked; \ schematics "
                    r"and illustrations are labeled.", font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover(
            "Shalev-Shwartz and Ben-David's Understanding Machine Learning is the clearest book on the theory. Thanks "
            "for watching, and see you in part eight."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
