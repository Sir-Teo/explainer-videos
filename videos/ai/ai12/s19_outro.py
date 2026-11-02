from __future__ import annotations

import math

import numpy as np
from manim import config

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import (
    BUDGET_COLORS, LAZY, MUP, PART, QUANT, RICH, SP, TT, WIDTH_COLORS,
    load, mean_seed_loss, visible_values, width_ramp,
)


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

        def axes(xr, yr):
            return Axes(x_range=[*xr, (xr[1] - xr[0]) / 4], y_range=[*yr, (yr[1] - yr[0]) / 4], x_length=TW,
                        y_length=TH - 0.2, tips=False, axis_config={"stroke_color": GREY_D, "include_ticks": False})

        out = []
        # 1. the frontier of the sweep
        s, ch = load("sweep"), load("chinchilla")
        N, D, Lb = np.asarray(s["N"], float), np.asarray(s["D"], float), np.asarray(s["bits"], float)
        lC = np.log10(6 * N[:, None] * D[None])
        ok = np.isfinite(Lb)
        hi = float(np.nanmin(Lb)) + 2.0
        a1 = axes((lC[ok].min(), lC[ok].max()), (float(np.nanmin(Lb)) - 0.05, hi))
        g1 = VGroup(a1)
        for i in range(len(N)):
            k = np.isfinite(Lb[i])
            g1.add(curve(a1, lC[i][k], np.minimum(Lb[i][k], hi), width_ramp(i, len(N)), 2))
        out.append((g1, r"a power law, \ measured", C.BITS))
        # 2. the kernel moves less as the width grows
        z = load("ntk")
        lw, km = np.log10(np.asarray(z["widths"], float)), np.log10(np.asarray(z["kernel_moved"]).mean(1))
        a2 = axes((lw.min(), lw.max()), (km.min() - 0.2, km.max() + 0.2))
        out.append((VGroup(a2, curve(a2, lw, km, LAZY, 3), *[Dot(a2.c2p(a, b), radius=0.04, color=LAZY) for a, b in zip(lw, km)]),
                    r"NTK limit: \ a frozen kernel", LAZY))
        # 3. lazy against rich
        r = load("rich")
        nc, mc = np.asarray(r["ntk_curve"]), np.asarray(r["mf_curve"])
        sx = np.log10(np.maximum(nc[0, :, 0], 1))
        a3 = axes((0, sx.max()), (0, float(r["var"]) * 1.1))
        out.append((VGroup(a3, curve(a3, sx, nc[:, :, 2].mean(0), LAZY, 3), curve(a3, sx, mc[:, :, 2].mean(0), RICH, 3)),
                    r"lazy \ vs \ rich", RICH))
        # 4. muP's learning-rate sweeps
        m = load("mup")
        lrs = np.log10(np.asarray(m["lrs"]))
        vals = np.concatenate([np.asarray(m[f"mup{w}"]).ravel() for w in m["widths"]])
        vals = vals[np.isfinite(vals)]
        lo, hi4 = float(vals.min()) - 0.05, float(min(np.percentile(vals, 80), vals.min() + 1.2))
        a4 = axes((lrs[0], lrs[-1]), (lo, hi4))
        g4 = VGroup(a4)
        for w, wc in zip(m["widths"], WIDTH_COLORS):
            v = mean_seed_loss(np.asarray(m[f"mup{w}"]))
            g4.add(curve(a4, lrs, visible_values(v, lo, hi4), wc, 2.5))
            g4.add(*[Triangle(color=wc, fill_opacity=1, stroke_width=0).scale(0.04).move_to(a4.c2p(x, hi4))
                     for x, value in zip(lrs, v) if not np.isfinite(value) or value > hi4])
        out.append((g4, r"$\mu$P: \ one rate, \ every width", MUP))
        # 5. iso-FLOP valleys
        allp = np.concatenate([np.asarray(ch[f"iso{C_:.0e}"]).reshape(-1, 3) for C_ in ch["budgets"]])
        a5 = axes((np.log10(allp[:, 0]).min(), np.log10(allp[:, 0]).max()), (allp[:, 2].min() - 0.05, min(allp[:, 2].max(), allp[:, 2].min() + 1.4)))
        g5 = VGroup(a5)
        top5 = min(allp[:, 2].max(), allp[:, 2].min() + 1.4)
        for C_, col in zip(ch["budgets"], BUDGET_COLORS):
            p = np.asarray(ch[f"iso{C_:.0e}"]).reshape(-1, 3)
            kk = p[:, 2] <= top5
            g5.add(curve(a5, np.log10(p[kk, 0]), p[kk, 2], col, 2.5))
        out.append((g5, r"Chinchilla's valleys", C.TRUE_P))
        # 6. repeated data's worth
        rp = load("repeat")
        ep = np.log2(np.asarray(rp["epochs"], float))
        worth = np.log2(np.asarray(rp["effective"], float) / np.asarray(rp["unique"], float))
        okw = np.isfinite(worth)  # runs worse than any fresh run are off the curve
        ep, worth = ep[okw], worth[okw]
        a6 = axes((0, ep.max()), (0, max(ep.max(), worth.max())))
        out.append((VGroup(a6, DashedLine(a6.c2p(0, 0), a6.c2p(ep.max(), ep.max()), color=GREY_D, stroke_width=1.5),
                           curve(a6, ep, worth, C.BITS, 3), *[Dot(a6.c2p(a, b), radius=0.04, color=WHITE) for a, b in zip(ep, worth)]),
                    r"repeats: \ worth less", C.BITS))
        # 7. quanta, one subtask at a time
        q = load("quanta")
        per = np.asarray(q["per_task"], float)
        st = np.asarray(q["steps"], float)
        wi = list(q["widths"]).index(128) if 128 in list(q["widths"]) else len(q["widths"]) // 2
        top7 = max(1.1, math.ceil(float(per[wi, 0].max()) * 10) / 10)
        a7 = axes((0, st.max()), (0, top7))
        T = per.shape[-1]
        g7 = VGroup(a7, *[curve(a7, st, per[wi, 0, :, k], interpolate_color(ManimColor(QUANT), ManimColor(GREY_D), k / T), 1.6)
                          for k in range(T)])
        g7.add(curve(a7, st, np.asarray(q["mean"], float)[wi, 0], WHITE, 3))
        out.append((g7, r"quanta: \ tasks \\ white: weighted mean", QUANT))
        # 8. grokking's circles
        gk = load("grok")
        xy = np.asarray(gk["emb_xy"], float)
        xy = xy / np.abs(xy).max()
        out.append((VGroup(*[Dot([p_[0], p_[1], 0], radius=0.035, color=interpolate_color(ManimColor(C.TRUE_P), ManimColor(C.MODEL_Q), i / len(xy)))
                             for i, p_ in enumerate(xy)]), r"grokking: \ numbers on circles", C.MODEL_Q))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = tile_frame(cap, col, TW, TH)
            if c_.width > TW:
                c_.scale_to_fit_width(TW)
            if c_.height > 0.46:
                c_.scale_to_fit_height(0.46)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3))
        if tiles.width > config.frame_width - 0.7:
            tiles.scale_to_fit_width(config.frame_width - 0.7)
        tiles.move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(rf"Part {PART}, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        key = note(r"triangles: \ off-scale or unstable learning-rate points").to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Let's take stock. Over measured ranges, loss often follows power laws in size, data and compute; "
            "forecasts beyond those ranges need validation. With neural-tangent scaling, an infinitely wide "
            "network trains like its own fixed tangent kernel, which learns no new features. Mu-P "
            "keeps every layer learning, and lets one learning rate serve every width and, with CompleteP, every "
            "depth. A budget should be split between size and data along the floor of Chinchilla's valley, then "
            "bent toward smaller models that answer cheaply, and stretched by repeating data, which is worth less "
            "each time. Power laws can come from data on a low-dimensional surface, or from many small skills "
            "learned at different times, whose losses are averaged. And a network can memorize first and understand much later, by "
            "turning clock arithmetic into rotations."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15, scale=0.95) for t in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"mixtures of experts", [16]),
            (r"$\mu$P, \ batch sizes, \ schedules, \ FP8 in a real run", [18]),
            (r"quantization and the cost of answering", [19]),
            (r"reinforcement learning and thinking at answer time", [27, 28]),
            (r"circuits inside networks", [30]),
            (r"forecasting what models will be able to do", [31]),
        ], font_size=24)
        with self.voiceover(
            "Act two ends here, and all of this comes back. Experts are part sixteen. Part eighteen trains a model "
            "with the whole recipe: mu-P, batch sizes, schedules and eight-bit arithmetic. Part nineteen is the cost "
            "of answering. Parts twenty-seven and twenty-eight scale reinforcement learning and thinking. Grokking's "
            "circuit is a first taste of part thirty, and forecasting what models will be able to do is part "
            "thirty-one."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"For $f(x) = \frac{1}{\sqrt n}\sum_j a_j\,\phi(w_j x)$ with independent $\mathcal{N}(0,1)$ weights, write the "
            r"tangent kernel $\Theta(x, x')$ as an average over the $n$ units, and show that its fluctuation is "
            r"$O(1/\sqrt n)$. \ By how much does one gradient step move each $a_j$?",
            r"A hidden layer $h = Wx$ has $n$ inputs of size $\Theta(1)$. \ Show that the update $\Delta W = -\eta\, g x^\top$ "
            r"changes $h_i$ by $\eta\, g_i \|x\|^2 = \Theta(\eta n)$, \ while a random $W$ with variance $\sigma^2$ gives "
            r"$|h_i| = \Theta(\sigma\sqrt n)$. \ Deduce $\mu$P's $\eta \propto 1/n$.",
            r"From $L = E + A N^{-\alpha} + B D^{-\beta}$ and $C = 6ND$, derive $N_{\text{opt}}$ and $D_{\text{opt}}$. \ With "
            r"Chinchilla's published fit and Besiroglu et al.'s refit, \ compute the tokens per parameter at "
            r"$C = 5.76 \times 10^{23}$.",
            r"Minimize $6ND + 2NT$ subject to $L(N, D) = L^*$. \ Show that the optimal $N$ decreases as the inference "
            r"tokens $T$ grow, \ and find its limit as $T \to \infty$.",
            r"Show that $D' = U + U R^*(1 - e^{-R/R^*})$ satisfies $D' \approx U(1 + R)$ for $R \ll R^*$ \ and "
            r"$D' \to U(1 + R^*)$ as $R \to \infty$.",
            r"If one try succeeds with probability $p$, and $p$ has density $c\,p^{\,b-1}$ near $0$, \ show that "
            r"$1 - \mathrm{pass}@k \sim c\,\Gamma(b)\,k^{-b}$. \ What is $b$ for $p$ uniform on $[0, 1]$?",
        ], font_size=21)
        with self.voiceover(
            "Here are six problems, from the tangent kernel to the power law of many tries. Pause here and work "
            "through them; full solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 13, \ Attention as Geometry \ (Act III: The Transformer Era)", font_size=34).to_edge(UP, buff=0.35)
        words = ["The", "cat", "sat", "on", "the", "mat", "because", "it", "was", "warm"]
        toks = VGroup(*[data_text(w, font="DejaVu Serif", font_size=30) for w in words]).arrange(RIGHT, buff=0.35).move_to(DOWN * 1.6)
        source_index = 7
        prefix = toks[:source_index]
        g = np.random.default_rng(11)
        att = g.dirichlet(np.ones(len(prefix)) * 0.4)
        att[1] += 0.6
        att[5] += 0.2
        att /= att.sum()
        src = toks[source_index]
        src.set_color(C.BITS)
        arcs = VGroup(*[ArcBetweenPoints(src.get_top() + UP * 0.18, t.get_top() + UP * 0.18, angle=PI / 2.2,
                                         stroke_width=1 + 14 * a, color=C.BITS).set_stroke(opacity=float(0.25 + 0.75 * a / att.max()))
                        for t, a in zip(prefix, att)])
        tag = label(r"which earlier words does ``it'' look at? \ (illustrative)", font_size=24, color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Next time, act three begins: the transformer era. First, attention: how every word looks back at every "
            "earlier word and decides which ones matter, as geometry. <bookmark mark='a'/> And we'll build a small "
            "transformer of our own."
        ) as vo:
            self.play(FadeIn(head), FadeIn(toks), FadeIn(tag))
            self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.1), Indicate(src, color=C.BITS), run_time=2.5)
            vo.wait_until("a")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [
            r"D.~A.~Roberts, S.~Yaida \& B.~Hanin, \textit{The Principles of Deep Learning Theory} (2022)",
            r"S.~J.~D.~Prince, \textit{Understanding Deep Learning} (2023), chapters 8 and 20",
        ]
        papers = [
            r"Neal (1996); \ Lee et al.\ (2018); \ Jacot, Gabriel \& Hongler (2018); \ Lee et al.\ (2019); \ Chizat, "
            r"Oyallon \& Bach (2019)",
            r"Yang \& Hu (2021); \ Yang et al., \textit{Tensor Programs V} (2022); \ Yang et al.\ (2023); \ Bordelon et "
            r"al.\ (2023); \ Everett et al.\ (2024); \ Dey et al., \textit{CompleteP} (2025)",
            r"McCandlish et al.\ (2018); \ Zhang et al.\ (2024); \ Bergsma et al.\ (2025)",
            r"Hestness et al.\ (2017); \ Kaplan et al.\ (2020); \ Hoffmann et al.\ (2022); \ Besiroglu et al.\ (2024); \ "
            r"Pearce \& Song (2024); \ Porian et al.\ (2024); \ H\"agele et al.\ (2024)",
            r"Sardana et al.\ (2023); \ Muennighoff et al.\ (2023); \ Villalobos et al.\ (2024); \ Clark et al.\ (2022); "
            r"\ Krajewski et al.\ (2024); \ Kumar et al.\ (2024)",
            r"Sharma \& Kaplan (2020); \ Michaud et al.\ (2023); \ Wei et al.\ (2022); \ Schaeffer, Miranda \& Koyejo "
            r"(2023); \ Du et al.\ (2024); \ Snell et al.\ (2024)",
            r"Power et al.\ (2022); \ Nanda et al.\ (2023); \ Kumar, Bordelon, Gershman \& Pehlevan (2023)",
            r"Brown et al.\ (2024); \ Schaeffer et al.\ (2025); \ Khatri et al.\ (2025); \ Ho et al.\ (2024); \ Xiao et "
            r"al., \textit{Densing law} (2024)",
        ]
        card = reference_card(books, papers, font_size=19)
        data = note(r"Text: Project Gutenberg (Part 1's $30$ novels). \ Every run is computed here; \ every number on screen "
                    r"is computed or cited; \ schematics are labelled.", font_size=18).to_edge(DOWN, buff=0.2)
        credit = note(narration_credit(), font_size=18).next_to(data, UP, buff=0.08)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.12:
            card.shift(UP * (credit.get_top()[1] + 0.12 - card.get_bottom()[1]))
        if card.get_top()[1] > 3.9:
            card.scale_to_fit_height(card.height - (card.get_top()[1] - 3.9)).align_to(credit, DOWN).shift(UP * (credit.height + 0.25))
        with self.voiceover(
            "The Chinchilla paper is very readable, and Roberts, Yaida and Hanin's book is the deep end on wide "
            "networks. Thanks for watching, and see you in part thirteen."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
