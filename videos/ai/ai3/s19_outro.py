from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import MPC, PART, RANDOM, TRAINED, gray_image, load


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        """The part in twelve pictures, each drawn from its own computed result."""
        TW, TH = 2.05, 1.75
        mk = lambda xr, yr: Axes(x_range=xr, y_range=yr, x_length=TW * 0.9, y_length=TH * 0.85, tips=False,  # noqa: E731
                                 axis_config={"stroke_color": GREY_D, "include_ticks": False})
        out = []
        g = load("gpt2")
        cos = np.asarray(g["barcode_cos"])[0]
        bars = VGroup(*[Rectangle(width=0.32, height=max(1.4 * float(cos[j]), 0.02), stroke_width=0,
                                  fill_color=C.TRUE_P if j != 2 else GREY_B, fill_opacity=0.9)
                        .move_to([0.45 * k, 0, 0], aligned_edge=DOWN) for k, j in enumerate((1, 3, 2))])
        out.append((bars, r"cosine similarity", C.TRUE_P))
        e = load("einsum")
        out.append((VGroup(Rectangle(width=1.6, height=1.2, stroke_width=0, fill_color=C.PENALTY, fill_opacity=0.8),
                           Rectangle(width=1.6 * e["macs_right"] / e["macs_left"] + 0.03, height=1.2, stroke_width=0,
                                     fill_color=C.REWARD, fill_opacity=0.9)).arrange(RIGHT, buff=0.2,
                                                                                       aligned_edge=DOWN),
                    r"einsum: \ order matters", C.REWARD))
        pr = load("project")["rows"]
        ax = mk([0, 17, 1], [-17, 1, 1])
        lk = [math.log10(r["kappa"]) for r in pr]
        out.append((VGroup(ax, *[curve(ax, lk, [math.log10(max(r[k_], 1e-17)) for r in pr], c_, 2.5) for k_, c_ in
                                 (("cgs", C.PENALTY), ("mgs", C.MODEL_Q), ("householder", C.REWARD))]),
                    r"Gram--Schmidt, \ rounded", C.MODEL_Q))
        pw = load("power")
        ax = mk([0, 60, 1], [-16, 0.2, 1])
        out.append((VGroup(ax, *[curve(ax, np.arange(len(pw[k_]["sin"])), np.log10(np.maximum(pw[k_]["sin"], 1e-16)),
                                       c_, 2.5) for k_, c_ in (("gpt2", C.TRUE_P), ("letters", C.MODEL_Q))]),
                    r"power iteration", C.TRUE_P))
        im = load("image")
        out.append((Group(gray_image(np.asarray(im["recon"])[3], TW * 0.9)), r"rank $8$ of a picture", C.BITS))
        nm = load("norms")["rows"]
        ax = mk([-0.5, 11.5, 1], [0, max(r["stable"] for r in nm) * 1.05, 1])
        out.append((VGroup(ax, *[curve(ax, [r["layer"] for r in nm if r["kind"] == k_],
                                       [r["stable"] for r in nm if r["kind"] == k_], c_, 2.5)
                                 for k_, c_ in (("attn", C.QUERY), ("attn_out", C.VALUE), ("mlp_in", C.MLP),
                                                ("mlp_out", C.TRUE_P))]), r"stable ranks", C.MLP))
        mp = load("mp")
        def positive_logs(values):
            values = np.asarray(values, float)
            return np.log10(values[np.isfinite(values) & (values > 0)])

        ev = positive_logs(mp["show"]["ev"])
        es = positive_logs(mp["shuffled"]["ev"])
        ax = mk([-2.5, 1.4, 1], [0, 1, 1])
        hb = VGroup(ax)
        for vals, col in ((es, RANDOM), (ev, TRAINED)):
            c_, edges = np.histogram(vals, bins=30, range=(-2.5, 1.4))
            c_ = c_ / max(1, c_.max())
            for a_, b_, h_ in zip(edges[:-1], edges[1:], c_):
                if h_ > 0:
                    p0, p1 = ax.c2p(a_, 0), ax.c2p(b_, h_)
                    hb.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                                     fill_opacity=0.6).move_to((p0 + p1) / 2))
        out.append((hb, r"spectra: \ separately peak-normalized", TRAINED))
        gl = load("galore")["track"]["tracked"]
        ax = mk([0, math.log10(600), 1], [0, 1, 1])
        out.append((VGroup(ax, curve(ax, [math.log10(t_["step"]) for t_ in gl], [t_["top8"] for t_ in gl], C.SCORE, 2.5)),
                    r"gradients: \ low rank", C.SCORE))
        sg = load("sgns")["lg_exact"]["runs"]
        r0 = sg[str(max(int(k_) for k_ in sg))]
        x_, y_ = np.asarray(r0["x"])[::6], np.asarray(r0["y"])[::6]
        lo_, hi_ = float(np.percentile(x_, 1)), float(np.percentile(x_, 99))
        ax = mk([lo_, hi_, 1], [lo_, hi_, 1])
        out.append((VGroup(ax, *[Dot(ax.c2p(a_, b_), radius=0.012, color=C.REWARD)
                                 for a_, b_ in zip(x_, y_) if lo_ <= a_ <= hi_ and lo_ <= b_ <= hi_]),
                    r"SGNS: generalized shifted PMI", C.REWARD))
        hd = load("highdim")
        ax = mk([0, 4, 1], [-4, 0, 1])
        lds = np.log10(np.asarray(hd["var_dims"], float))
        out.append((VGroup(ax, Line(ax.c2p(0, 0), ax.c2p(4, -4), color=C.BITS, stroke_width=2),
                           *[Dot(ax.c2p(a_, b_), radius=0.03, color=C.TRUE_P) for a_, b_ in
                             zip(lds, np.log10(hd["cos_var"]))]), r"cosines: \ variance $1/d$", C.BITS))
        jl = load("jl")["fine"]
        ax = mk([0.2, 3, 1], [-2.5, 0.1, 1])
        out.append((VGroup(ax, curve(ax, np.log10([f["k"] for f in jl]),
                                     np.log10(np.maximum([f["exact_fail"] for f in jl], 10 ** -2.5)), C.BITS, 2.5),
                           *[Dot(ax.c2p(math.log10(f["k"]), math.log10(max(np.mean(f["fail"]), 10 ** -2.5))),
                                 radius=0.03, color=C.TRUE_P) for f in jl]), r"Johnson--Lindenstrauss", MPC))
        mf = load("mf")
        ks = sorted(int(k_) for k_ in mf["test_rmse"])
        ys = [float(np.mean(mf["test_rmse"][str(k_)])) for k_ in ks]
        ax = mk([0, len(ks) - 1, 1], [min(ys) - 0.01, max(ys) + 0.01, 1])
        out.append((VGroup(ax, curve(ax, range(len(ks)), ys, C.BITS, 2.5),
                           *[Dot(ax.c2p(i, y), radius=0.04, color=C.BITS) for i, y in enumerate(ys)]),
                    r"filling in ratings", C.BITS))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = tile_frame(cap, col, TW, TH)
            if c_.width > TW + 0.1:
                c_.width = TW + 0.1
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=2, cols=6, buff=(0.12, 0.3)).move_to(DOWN * 0.3)
        if tiles.width > 13.7:
            tiles.width = 13.7
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(rf"Part {PART}, in twelve pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Vectors are lists of numbers with geometry; the dot product, kept honest by "
            "Cauchy-Schwarz, measures likeness. Einsum names the axes and counts the cost. Projections find the closest "
            "point, and arithmetic's order matters. Symmetric matrices stretch along perpendicular directions, which "
            "power iteration finds; every matrix is turn, stretch, turn, and its biggest pieces are its best low-rank "
            "copy, with reflections allowed and rectangular singular-value blocks. Some trained weights and gradients "
            "concentrate in strong directions. Counting and guessing connect through related cooccurrence statistics; "
            "smoothed negative sampling gives a generalized shifted PMI. And in high dimensions, independent random "
            "directions are nearly perpendicular. Random projections can preserve squared distances with stated "
            "probability, and low rank helps fill empty tables."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"how the chain rule computes every gradient", [4]),
            (r"keeping each layer's stretch near one", [9]),
            (r"Muon: \ steepest descent in the spectral norm", [11]),
            (r"attention: \ dot products, \ written in einsum", [13]),
            (r"low-rank memory for long contexts", [15]),
            (r"LoRA: \ fine-tuning in a low-rank slice", [27]),
            (r"directions inside a model: \ reading and steering", [30]),
        ], font_size=24)
        with self.voiceover(
            "All of it comes back. Part 4 builds the chain rule that computes every gradient. Part 9 keeps each "
            "layer's stretch near one, so that deep networks train at all. Part 11 builds Muon, steepest descent in "
            "the spectral norm. Part 13 writes attention as dot products, in einsum. Part 15 squeezes a long "
            "context's memory through low rank, Part 27 fine-tunes through it, and Part 30 reads and steers the "
            "directions inside a model."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"Use Cauchy--Schwarz to prove the triangle inequality $|\mathbf{a} + \mathbf{b}| \le |\mathbf{a}| + "
            r"|\mathbf{b}|$, \ and find when it is an equality.",
            r"For $A$ with full column rank, show that $P = A(A^{\top}A)^{-1}A^{\top}$ satisfies $P^2 = P = P^{\top}$, \ and that $I - P$ projects onto "
            r"the vectors perpendicular to every column of $A$.",
            r"For symmetric $A$ with $\lambda_1 > \lambda_2$, \ show that $R(\mathbf{v}_1 + \varepsilon\mathbf{v}_2) = "
            r"\lambda_1 - (\lambda_1 - \lambda_2)\varepsilon^2 + O(\varepsilon^4)$ for unit eigenvectors: \ why the "
            r"eigenvalue converges twice as fast as the vector.",
            r"Prove $\|A\|_F^2 = \sum_i \sigma_i^2$ and $\|A\|_2 \le \|A\|_F \le \sqrt{r}\,\|A\|_2$, \ and find matrices "
            r"that attain each bound.",
            r"Maximize $\ell(x) = a\log\sigma(x) + b\log\sigma(-x)$ over $x$ for $a, b > 0$. \ For $P_n(c)=P(c)$, "
            r"recover Levy and Goldberg's $\mathbf{w}\cdot\mathbf{c} = \mathrm{PMI}(w, c) - \log k$.",
            r"For $\mathbf{x}, \mathbf{y}$ independent and uniform on the unit sphere in $\mathbb{R}^d$, \ show "
            r"$\mathbb{E}[x_1^2] = 1/d$ and $\operatorname{Var}(\mathbf{x}\cdot\mathbf{y}) = 1/d$.",
            r"If $X \sim \chi^2_k$, \ show $\mathbb{E}\,e^{tX} = (1 - 2t)^{-k/2}$ for $t < 1/2$, \ and finish the "
            r"optimization over $t$ in the Johnson--Lindenstrauss proof.",
            r"A rank-$k$ copy of an $m \times n$ picture stores $k(m + n + 1)$ numbers. \ For $180 \times 288$, \ up "
            r"to what $k$ does it save space, \ and what does Eckart--Young say its error is?",
        ], font_size=21)
        with self.voiceover(
            "Here are eight problems to try, from the triangle inequality to the Johnson-Lindenstrauss proof. Pause "
            "here, and work through them; full solutions are in this part's notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 4, \ Change", font_size=40).to_edge(UP, buff=0.35)

        def grad(p):
            x, y = p[0], p[1]
            return np.array([x + 1.2 * math.cos(2 * x) * math.cos(y), 3 * y - 0.6 * math.sin(2 * x) * math.sin(y), 0])

        field = ArrowVectorField(lambda p: -0.18 * grad(p), x_range=[-6, 6, 0.75], y_range=[-3, 2.5, 0.75],
                                 colors=[C.TRUE_P, C.BITS], length_func=lambda n: min(n, 0.55))
        field.shift(DOWN * 0.3)
        path, p = [], np.array([-5.2, 2.0, 0])
        for _ in range(60):
            path.append(p.copy())
            p = p - 0.12 * grad(p)
        trail = VMobject(color=WHITE, stroke_width=4).set_points_smoothly([q + DOWN * 0.3 for q in path])
        ball = glow_dot(path[0] + DOWN * 0.3, color=WHITE, radius=0.09)
        tag = label(r"illustrative", font_size=22, color=GREY_B).to_corner(DR, buff=0.4)
        with self.voiceover(
            "Next time: change. Everything in this part stood still, except in the chapters that trained something, "
            "where we took gradients on trust. <bookmark mark='a'/> Part 4 builds derivatives, the chain rule, and "
            "the machine that runs it backwards through billions of numbers at once."
        ) as vo:
            self.play(FadeIn(head), Create(field), FadeIn(tag), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(ball))
            self.play(MoveAlongPath(ball, trail), Create(trail), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        card = reference_card(
            [r"G.~Strang, \textit{Linear Algebra and Learning from Data} (2019); \ S.~Axler, \textit{Linear Algebra Done "
             r"Right}, 4th ed.\ (2024)",
             r"L.~N.~Trefethen \& D.~Bau, \textit{Numerical Linear Algebra} (1997); \ R.~Vershynin, \textit{High-Dimensional "
             r"Probability} (2018)"],
            [r"Grassmann (1844); \ Cayley (1858); \ Beltrami (1873); \ Jordan (1874); \ Schmidt (1907); \ Weyl (1912); \ "
             r"Eckart \& Young (1936); \ Householder (1958); \ Golub \& Kahan (1965); \ G.~W.~Stewart, \textit{On the "
             r"Early History of the SVD} (1993)",
             r"von Mises \& Pollaczek-Geiringer (1929); \ Lanczos (1950); \ Brin \& Page (1998); \ Miyato et al.\ (2018)",
             r"Wigner (1955); \ Marchenko \& Pastur (1967); \ Martin \& Mahoney (2019, 2021); \ Zhao et al., "
             r"\textit{GaLore} (2024); \ Hu et al., \textit{LoRA} (2021); \ Jordan et al., \textit{Muon} (2024)",
             r"Harris (1954); \ Firth (1957); \ Deerwester et al.\ (1990); \ Mikolov et al.\ (2013a, b); \ Pennington et "
             r"al., \textit{GloVe} (2014); \ Levy \& Goldberg (2014); \ Levy, Goldberg \& Dagan (2015)",
             r"Johnson \& Lindenstrauss (1984); \ Dasgupta \& Gupta (2003); \ Larsen \& Nelson (2017)",
             r"Radford et al., \textit{GPT-2} (2019); \ Mu \& Viswanath (2018); \ Gao et al.\ (2019); \ Ethayarajh (2019); "
             r"\ Timkey \& van Schijndel (2021); \ Elhage et al.\ (2022); \ Park, Choe \& Veitch (2024)",
             r"Bennett \& Lanning, \textit{The Netflix Prize} (2007); \ Koren, Bell \& Volinsky (2009); \ Covington et "
             r"al.\ (2016); \ Johnson, Douze \& J\'egou, \textit{FAISS} (2017); \ Yi et al.\ (2019); \ Karpukhin et "
             r"al., \textit{DPR} (2020)"])
        credit = note(narration_credit(), font_size=18).to_edge(DOWN, buff=0.15)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.1:
            card.shift(UP * (credit.get_top()[1] + 0.1 - card.get_bottom()[1]))
        with self.voiceover(
            "For more, Gilbert Strang's Linear Algebra and Learning from Data is a friendly companion, Trefethen and "
            "Bau explain why the order of arithmetic matters, and Roman Vershynin's High-Dimensional Probability "
            "explains why big spaces behave the way they do. Thanks for watching, and see you in Part 4."
        ):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(1.5)
        self.clear_scene()
