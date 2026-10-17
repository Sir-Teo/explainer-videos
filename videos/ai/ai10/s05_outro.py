from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai10.common import BUDGET_COLORS, MUP, SP, WIDTH_COLORS, curve, load


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
            return Axes(x_range=[*xr, (xr[1] - xr[0]) / 4], y_range=[*yr, (yr[1] - yr[0]) / 4], x_length=TW,
                        y_length=TH - 0.2, tips=False, axis_config={"stroke_color": GREY_D, "include_ticks": False})

        out = []
        s = load("scaling")
        lx, L = np.log10(np.asarray(s["params"], float)), np.asarray(s["finals"])
        a1 = axes((lx.min() - 0.2, lx.max() + 0.2), (L.min() - 0.1, L.max() + 0.1))
        out.append((VGroup(a1, curve(a1, lx, L, C.BITS, 3), *[Dot(a1.c2p(x, y), radius=0.04, color=C.BITS) for x, y in zip(lx, L)]),
                    r"a power law", C.BITS))
        z = load("lazy")
        lw, lm = np.log10(np.asarray(z["widths"], float)), np.log10(np.asarray(z["moved"]))
        a2 = axes((lw.min() - 0.2, lw.max() + 0.2), (lm.min() - 0.2, lm.max() + 0.2))
        out.append((VGroup(a2, curve(a2, lw, lm, SP, 3)), r"wide nets: \ lazy", SP))
        m = load("mup")
        lrs = np.log10(np.asarray(m["lrs"]))
        for mode, cap, col in (("sp", r"learning rates, \ the usual way", SP), ("mup", r"learning rates, \ $\mu$P", MUP)):
            vals = np.concatenate([np.asarray(m[f"{mode}{w}"]) for w in m["widths"]])
            vals = vals[np.isfinite(vals)]
            lo, hi = float(vals.min()) - 0.05, float(min(np.percentile(vals, 85), vals.min() + 1.2))
            a3 = axes((lrs[0], lrs[-1]), (lo, hi))
            g = VGroup(a3)
            for w, wc in zip(m["widths"], WIDTH_COLORS):
                v = np.asarray(m[f"{mode}{w}"])
                g.add(curve(a3, lrs, np.where(np.isfinite(v), np.minimum(v, hi), hi), wc, 2.5))
            out.append((g, cap, col))
        d = load("isoflop")
        allp = np.concatenate([np.asarray(d[f"params{b:.0e}"]) for b in d["budgets"]])
        allf = np.concatenate([np.asarray(d[f"finals{b:.0e}"]) for b in d["budgets"]])
        a4 = axes((np.log10(allp.min()) - 0.1, np.log10(allp.max()) + 0.1), (np.nanmin(allf) - 0.05, np.nanmax(allf) + 0.05))
        g4 = VGroup(a4)
        for b, c in zip(d["budgets"], BUDGET_COLORS):
            p, f = np.asarray(d[f"params{b:.0e}"], float), np.asarray(d[f"finals{b:.0e}"])
            ok = np.isfinite(f)
            g4.add(curve(a4, np.log10(p[ok]), f[ok], c, 2.5))
        out.append((g4, r"size or data", C.BITS))
        out.append((VGroup(MathTex(r"D \approx 20\,N", font_size=48, color=C.TRUE_P)), r"Chinchilla", C.TRUE_P))
        gk = load("grok")
        W = np.asarray(gk["wd"])
        a5 = axes((0, 4.1), (0, 1))
        out.append((VGroup(a5, curve(a5, np.log10(W[:, 0]), W[:, 1], GREY_B, 2.5), curve(a5, np.log10(W[:, 0]), W[:, 2], C.BITS, 3)),
                    r"grokking", C.BITS))
        xy = np.asarray(gk["emb_xy"])
        xy = xy / np.abs(xy).max()
        out.append((VGroup(*[Dot([p[0], p[1], 0], radius=0.035, color=interpolate_color(ManimColor(C.TRUE_P), ManimColor(C.MODEL_Q), i / len(xy)))
                             for i, p in enumerate(xy)]), r"addition on circles", C.MODEL_Q))
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
        head = label(r"Part 10, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Loss falls with size along a power law, predictably enough to plan by. Very wide "
            "networks, scaled the usual way, go lazy and stop learning features; mu-P keeps every layer learning, "
            "and lets a learning rate tuned on a small model carry over to a big one. A fixed budget should be split "
            "between size and data, about twenty tokens per parameter by Chinchilla's count. And a network can "
            "memorize first and understand much later, by turning clock arithmetic into rotations."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15, scale=0.95) for t in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"scaling laws", [13, 17]),
            (r"tokens per parameter, \ data", [16, 19]),
            (r"$\mu$P and hyperparameter transfer", [11, 13]),
            (r"circuits inside networks", [20]),
        ], font_size=26)
        with self.voiceover(
            "Act two ends here. Scaling laws return with mixtures of experts, and with reasoning models that scale "
            "the thinking done at test time. And grokking's circuits are a first taste of looking inside models, in "
            "part twenty."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 11, \ Attention as Geometry \ (Act III: Engines)", font_size=36).to_edge(UP, buff=0.35)
        words = ["The", "cat", "sat", "on", "the", "mat", "because", "it", "was", "warm"]
        toks = VGroup(*[Text(w, font="DejaVu Serif", font_size=30) for w in words]).arrange(RIGHT, buff=0.35).move_to(DOWN * 1.6)
        g = np.random.default_rng(11)
        att = g.dirichlet(np.ones(len(words)) * 0.4)
        att[1] += 0.6
        att[5] += 0.2
        att /= att.sum()
        src = toks[7]
        arcs = VGroup(*[ArcBetweenPoints(src.get_top() + UP * 0.05, t.get_top() + UP * 0.05, angle=-PI / 2.2,
                                         stroke_width=1 + 14 * a, color=C.BITS).set_stroke(opacity=float(0.25 + 0.75 * a / att.max()))
                        for t, a in zip(toks, att) if t is not src])
        tag = label(r"which earlier words does ``it'' look at? \ (illustrative)", font_size=24, color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Next time, act three begins: the engines inside today's models. First, attention: how every word "
            "looks back at every earlier word and decides which ones matter, as geometry. <bookmark mark='a'/> And "
            "we'll build a small transformer of our own."
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
            r"A.~Jacot, F.~Gabriel \& C.~Hongler, \textit{Neural Tangent Kernel} (2018)",
            r"G.~Yang \& E.~J.~Hu, \textit{Feature Learning in Infinite-Width Neural Networks} (2021)",
            r"G.~Yang et al., \textit{Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer} (2022)",
            r"J.~Kaplan et al., \textit{Scaling Laws for Neural Language Models} (2020)",
            r"J.~Hoffmann et al., \textit{Training Compute-Optimal Large Language Models} (2022)",
            r"A.~Power et al., \textit{Grokking} (2022); \ N.~Nanda et al., \textit{Progress Measures for Grokking} (2023)",
        ]
        card = reference_card(books, papers)
        data = note(r"Text: Project Gutenberg (Part 1's $30$ novels). \ Every run is computed here; \ every number on screen "
                    r"is computed and checked; \ illustrations are labeled.", font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover(
            "The Chinchilla paper is very readable, and Roberts, Yaida and Hanin's book is the deep end on wide "
            "networks. Thanks for watching, and see you in part eleven."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
