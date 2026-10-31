from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai8.common import BOUND, MEAS, PART, TEST, TRAIN, curve, load


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

        def plane(xr, yr):
            return Axes(x_range=xr, y_range=yr, x_length=TW, y_length=TH - 0.2, tips=False,
                        axis_config={"stroke_color": GREY_D, "include_ticks": False})

        out = []
        r = load("risk")
        a = plane([1, 3.5, 1], [0.12, 0.32, 0.1])
        lx = np.log10(np.asarray(r["ns"], float))
        out.append((VGroup(a, curve(a, lx, np.asarray(r["true_mean"]), TEST, 3),
                           curve(a, lx, np.clip(np.asarray(r["emp_mean"]), 0.12, 0.32), TRAIN, 2.5)),
                    r"risk: \ training error flatters", TEST))
        b = load("biasvar")
        a = plane([0, 15, 3], [-1, 1.5, 1])
        out.append((VGroup(a, curve(a, b["degs"], np.clip(np.log10(np.asarray(b["total"])), -1, 1.5), TEST, 3),
                           curve(a, b["degs"], np.clip(np.log10(np.asarray(b["bias2"])), -1, 1.5), C.TRUE_P, 2),
                           curve(a, b["degs"], np.clip(np.log10(np.asarray(b["var"])), -1, 1.5), C.MODEL_Q, 2)),
                    r"bias$^2$ + variance + noise", TEST))
        h = load("hoeffding")
        a = plane([0, 0.3, 0.1], [-5, 0, 1])
        e = np.asarray(h["eps"])
        tl = np.asarray(h["tail160"])
        ok = tl > 0
        out.append((VGroup(a, curve(a, e[ok], np.log10(tl[ok]), MEAS, 3),
                           curve(a, e, np.log10(np.maximum(np.asarray(h["hoef160"]), 1e-5)), BOUND, 2.5)),
                    r"Hoeffding, \ simulated", BOUND))
        g = load("growth")
        a = plane([0, 16, 4], [0, 16, 4])
        ns = np.asarray(g["ns"])
        out.append((VGroup(a, curve(a, ns, np.log2(np.asarray(g["pow2"], float)), GREY_B, 2),
                           curve(a, ns, np.log2(np.asarray(g["half"], float)), MEAS, 3)),
                    r"growth: \ $n^2 - n + 2$, \ not $2^n$", MEAS))
        p = load("pacbayes")
        a = plane([-0.5, 2.5, 1], [0, 0.6, 0.1])
        bars_ = VGroup()
        for i, (v, col) in enumerate(((p["test_Q"], TEST), (p["bound"], BOUND), (0.5, C.SURPRISE))):
            lo_, hi_ = a.c2p(i - 0.3, 0), a.c2p(i + 0.3, v)
            bars_.add(Rectangle(width=hi_[0] - lo_[0], height=hi_[1] - lo_[1], stroke_width=0, fill_color=col,
                                fill_opacity=0.85).move_to([(lo_[0] + hi_[0]) / 2, (lo_[1] + hi_[1]) / 2, 0]))
        out.append((VGroup(a, bars_), rf"PAC-Bayes: \ ${100 * p['bound']:.0f}\%$, \ non-vacuous", BOUND))
        rl = load("random")
        S = np.asarray(rl["shuffled"])
        a = plane([0, 3.2, 1], [0.4, 1, 0.2])
        out.append((VGroup(a, curve(a, np.log10(S[:, 0]), S[:, 1], TRAIN, 2.5), curve(a, np.log10(S[:, 0]), S[:, 2], TEST, 3)),
                    r"memorizing nonsense", TRAIN))
        d = load("double")
        a = plane([1, 3.8, 1], [-1, 2, 1])
        out.append((VGroup(a, curve(a, np.log10(d["ps"]), np.clip(np.log10(d["test"]), -1, 2), TEST, 3)),
                    r"double descent", TEST))
        c = load("canary")
        gs = [int(x) for x in c["groups"] if int(x) > 0]
        fin = np.asarray(c["exact"])[-1, :len(gs)]
        a = plane([0, math.log2(gs[-1]), 1], [0, 1, 0.5])
        out.append((VGroup(a, curve(a, np.log2(gs), fin, C.SURPRISE, 3),
                           *[Dot(a.c2p(math.log2(x), v), radius=0.04, color=C.SURPRISE) for x, v in zip(gs, fin)]),
                    r"repetition $\to$ memorization", C.SURPRISE))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = tile_frame(cap, col, TW, TH)
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
        head = label(rf"Part {PART}, \ in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Risk is the error on everything the world could send; training error flatters it, "
            "and the gap splits into approximation and estimation. Error splits into bias, variance and noise. One "
            "rule's test score is trustworthy by Hoeffding; choosing among many costs the log of how many, and an "
            "infinite family costs its growth function, a polynomial by Sauer and Shelah. Rademacher complexity and "
            "margins measure capacity by the size of the weights; PAC-Bayes, compression and stability gave bounds "
            "that can say something even for a network, as ours did. Then the puzzles: networks memorize noise, "
            "gradient descent chooses the smallest fit and the widest margin, error descends twice, overfitting can "
            "be benign, and flatness is not the whole story. And when the data moves, or repeats, generalization "
            "gives way to weighting, and to memory."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15, scale=0.95) for t in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"margins: \ the perceptron's convergence proof", [9]),
            (r"which minimum training finds: \ sharpness, \ the edge of stability", [11]),
            (r"more parameters than data: \ grokking, \ scaling laws", [12]),
            (r"held-out scores, \ contamination, \ memorization and privacy", [30, 31]),
        ], font_size=25)
        with self.voiceover(
            "Margins return in part nine, in the perceptron's convergence proof. Which minimum training finds, and "
            "how sharp it is, is part eleven's subject. Models far bigger than their data, grokking and scaling laws "
            "are part twelve's. And held-out scores, contaminated test sets, memorization and privacy come back when "
            "we look inside models and ask whether to trust them, in parts thirty and thirty-one."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"How many test examples guarantee, \ with probability $0.99$, \ that the measured error rates of $100$ "
            r"fixed models are all within $0.02$ of their true error rates?",
            r"Show that intervals on the real line have VC dimension $2$ and growth function $\binom{n}{2} + n + 1$, "
            r"\ exactly the Sauer--Shelah bound.",
            r"For $\{x \mapsto w \cdot x : |w|_1 \le B\}$ with $|x_i|_\infty \le X$, \ show $\hat{\mathfrak R}_S \le "
            r"B X \sqrt{2\ln(2d)/n}$ \ (Massart's lemma).",
            r"Gradient descent on $\tfrac12|Xw - y|^2$ \ with $d > n$, \ from $w_0$, \ small step: \ show it converges to "
            r"$X^+ y + (I - X^+ X)\, w_0$.",
            r"For $Q = \mathcal N(\mu, s^2 I)$ and $P = \mathcal N(\mu_0, \lambda I)$ in $d$ dimensions, \ derive "
            r"$\mathrm{KL}(Q\|P) = \tfrac12\big(d s^2/\lambda + |\mu - \mu_0|^2/\lambda - d - d\ln(s^2/\lambda)\big)$.",
            r"For a fixed predictor and exact weights, show the importance-weighted error is unbiased for the test error, \ and that with $p = "
            r"\mathcal N(0, 1)$, \ $q = \mathcal N(0, 4)$ \ the weights have infinite variance.",
        ], font_size=21)
        with self.voiceover(
            "Here are six problems to try, from sizing a test set to the variance of importance weights. Pause here "
            "and work through them; full solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 9, \ Networks", font_size=40).to_edge(UP, buff=0.35)
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
            "Next time: networks themselves. From the perceptron and its winters to backpropagation; why a stack of "
            "simple layers can approximate any function, how depth cuts space into pieces, and how to start and keep "
            "signals alive through many layers. <bookmark mark='a'/> And the first neural language model joins the "
            "scoreboard."
        ) as vo:
            self.play(FadeIn(head), FadeIn(img), FadeIn(tag), run_time=2.0)
            vo.wait_until("a")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [
            r"S.~Shalev-Shwartz \& S.~Ben-David, \textit{Understanding Machine Learning} (2014); \ M.~Mohri, "
            r"A.~Rostamizadeh \& A.~Talwalkar, \textit{Foundations of Machine Learning}, 2nd ed.\ (2018)",
            r"F.~Bach, \textit{Learning Theory from First Principles} (2024); \ V.~Vapnik, \textit{The Nature of "
            r"Statistical Learning Theory} (1995); \ T.~Hastie, R.~Tibshirani \& J.~Friedman, \textit{The Elements of "
            r"Statistical Learning} (2009)",
        ]
        papers = [
            r"Hoeffding (1963); \ Vapnik \& Chervonenkis (1971); \ Sauer (1972); \ Shelah (1972); \ Valiant (1984); \ "
            r"Littlestone \& Warmuth (1986); \ Geman, Bienenstock \& Doursat (1992); \ Hochreiter \& Schmidhuber (1997)",
            r"Bartlett (1998); \ Schapire, Freund, Bartlett \& Lee (1998); \ McAllester (1999); \ Shimodaira (2000); \ "
            r"Koltchinskii (2001); \ Bartlett \& Mendelson (2002); \ Bousquet \& Elisseeff (2002); \ Seeger (2002); \ "
            r"Maurer (2004)",
            r"Hardt, Recht \& Singer (2016); \ Zhang et al.\ (2017); \ Dziugaite \& Roy (2017); \ Keskar et al.\ (2017); \ "
            r"Dinh et al.\ (2017); \ Soudry et al.\ (2018); \ Arora et al.\ (2018); \ Belkin et al.\ (2019); \ "
            r"Nakkiran et al.\ (2020, two papers); \ Lyu \& Li (2020)",
            r"Bartlett, Long, Lugosi \& Tsigler (2020); \ Heckel \& Yilmaz (2021); \ Foret et al.\ (2021); \ "
            r"Mallinar et al.\ (2022); \ Andriushchenko et al.\ (2023); \ Lotfi et al.\ (2022, 2024, 2024)",
            r"Carlini et al.\ (2019, 2021, 2023); \ Kandpal, Wallace \& Raffel (2022); \ Lee et al.\ (2022); \ Nasr et "
            r"al.\ (2023); \ Cooper et al.\ (2025); \ Ahmed, Cooper et al.\ (2026)",
        ]
        card = reference_card(books, papers, font_size=19)
        data = note(r"Pages: Part 6's Austen and Dickens; \ text: Part 1's $30$ novels. \ Every number on screen is "
                    r"computed by this part's code or cited; \ schematics and illustrations are labeled.",
                    font_size=18).to_edge(DOWN, buff=0.2)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=18)
        credit.next_to(data, UP, buff=0.08)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.12:
            card.scale((card.height - (credit.get_top()[1] + 0.12 - card.get_bottom()[1])) / card.height)
            card.next_to(credit, UP, buff=0.12)
        with self.voiceover(
            "Shalev-Shwartz and Ben-David's Understanding Machine Learning is the clearest book on the theory, and "
            "Francis Bach's Learning Theory from First Principles the most up to date. Thanks for watching, and see "
            "you in part nine."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
