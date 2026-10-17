from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import OPT_COLORS, SCHED_COLORS, curve, load
from videos.ai.ai9.compute import VALLEY


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

        def axes(xr, yr, axis=True):
            return Axes(x_range=xr, y_range=yr, x_length=TW, y_length=TH - 0.2, tips=False,
                        axis_config={"stroke_color": GREY_D, "include_ticks": False, "stroke_width": 2 if axis else 0})

        out = []
        v = load("valley")
        a1 = axes([-5, 1, 1], [-1.2, 1.2, 1], axis=False)
        cont = contour_lines(a1, lambda x, y: 0.5 * (VALLEY[0] * x * x + VALLEY[1] * y * y), (-5, 1), (-1.2, 1.2),
                             [0.3, 1.5, 4, 9], n=(80, 40), stroke_width=1)
        out.append((VGroup(cont, *[VMobject(color=c, stroke_width=2).set_points_as_corners([a1.c2p(*p) for p in np.asarray(v[k])])
                                   for k, c in (("gd", GREY_A), ("momentum", OPT_COLORS["momentum"]), ("adam", OPT_COLORS["adam"]))]),
                    r"three ways down", OPT_COLORS["adam"]))
        nz = load("noise")
        cl = np.asarray(nz["cloud1"])
        cl = cl - nz["w_star"]
        out.append((VGroup(*[Dot([p[0], p[1], 0], radius=0.02, color=C.SURPRISE) for p in cl[::2]]), r"SGD: a noisy cloud",
                    C.SURPRISE))
        e = load("eos")
        eta0 = float(e["etas"][0])
        c = np.asarray(e[f"curve{eta0:g}"])
        a3 = axes([0, 4000, 1000], [0, 2 / eta0 * 1.2, 2 / eta0 / 4])
        out.append((VGroup(a3, curve(a3, c[:, 0], np.minimum(c[:, 2], 2 / eta0 * 1.2), C.TRUE_P, 2.5),
                           DashedLine(a3.c2p(0, 2 / eta0), a3.c2p(4000, 2 / eta0), color=C.TRUE_P, stroke_width=1.5)),
                    r"the edge of stability", C.TRUE_P))
        out.append((VGroup(MathTex(r"\frac{m_t}{\sqrt{v_t}}", font_size=60, color=OPT_COLORS["adam"])), r"Adam", OPT_COLORS["adam"]))
        m = load("muon")
        b, a = np.asarray(m["before"]), np.asarray(m["after"])
        a4 = axes([0, len(b), 64], [0, 1.3, 1])
        out.append((VGroup(a4, curve(a4, np.arange(len(b)), b, GREY_B, 2), curve(a4, np.arange(len(a)), np.minimum(a, 1.3),
                                                                                OPT_COLORS["muon"], 2.5)),
                    r"Muon: \ orthogonal steps", OPT_COLORS["muon"]))
        o = load("optim")
        a5 = axes([0, 2500, 500], [2.0, 4.6, 1])
        out.append((VGroup(a5, *[curve(a5, np.asarray(o[n])[1:, 0], np.clip(np.asarray(o[n])[1:, 1], 2.0, 4.6), OPT_COLORS[n], 2)
                                 for n in o["names"]]), r"five optimizers", WHITE))
        s = load("schedule")
        a6 = axes([0, 4000, 1000], [0, 1.1, 1])
        out.append((VGroup(a6, *[curve(a6, np.arange(len(s[f"lr_{k}"])) * 20, s[f"lr_{k}"], SCHED_COLORS[k], 2.5)
                                 for k in ("constant", "cosine", "wsd")]), r"schedules", SCHED_COLORS["wsd"]))
        out.append((VGroup(MathTex(r"\lambda_{\max} \approx 2/\eta", font_size=44, color=C.BITS)), r"the step sets the sharpness",
                    C.BITS))
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
        head = label(r"Part 9, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. How you walk downhill matters as much as the hill. Small random batches make each step "
            "cheap and noisy, and the noise settles into a cloud whose size is set by the step and the batch. "
            "Training pushes the sharpness up to two over the learning rate, and lives at that edge. Momentum and "
            "Adam reshape each step, and Muon makes a matrix's step push equally in every direction. And the "
            "schedule decides when the cloud finally contracts onto a good answer."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15, scale=0.95) for t in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"learning rates that transfer across sizes", [10]),
            (r"batch size and noise", [10]),
            (r"AdamW and Muon at scale", [12, 13]),
            (r"schedules in pretraining", [10, 17]),
        ], font_size=26)
        with self.voiceover(
            "Next, we scale up. How should the learning rate change when the model gets wider? How big should the "
            "batch be, and how long should we train? That's part ten. And these optimizers return whenever a model "
            "in this series is actually trained."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 10, \ The Mathematics of Scale", font_size=40).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[15, 25, 2], y_range=[1.5, 4.0, 0.5], x_length=9.0, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to(DOWN * 0.4)
        lines = VGroup()
        for k, n in enumerate(np.linspace(16, 22, 5)):
            xs = np.linspace(15, 25, 80)
            ys = 1.7 + 0.25 * np.exp(-(n - 16) * 0.35) * 2 + 2.0 * np.exp(-(xs - n) * 0.9) * (xs > n - 1) + \
                np.where(xs < n - 1, 3, 0)
            ys = np.clip(1.7 + 0.6 * np.exp(-0.25 * (n - 16)) + 1.8 * np.exp(-0.7 * (xs - 15)) * np.exp(-0.1 * (n - 16)), 1.5, 4.0)
            lines.add(VMobject(color=interpolate_color(ManimColor(C.TRUE_P), ManimColor(C.BITS), k / 4), stroke_width=3)
                      .set_points_smoothly([ax.c2p(x, y) for x, y in zip(xs, ys)]))
        env = DashedLine(ax.c2p(15, 3.9), ax.c2p(25, 1.6), color=WHITE, stroke_width=2)
        tag = label(r"loss against compute, \ for models of growing size \ (schematic)", font_size=24, color=GREY_B)
        tag.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Next time: the mathematics of scale. Why bigger models predictably get better, how to split a budget "
            "between parameters and data, and how to set a learning rate once and keep it as the model grows. "
            "<bookmark mark='a'/> Straight lines on log–log plots, and what they promise."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(tag))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("a")
            self.play(Create(env))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [
            r"S.~J.~D.~Prince, \textit{Understanding Deep Learning} (2023), chapter 6",
            r"J.~Nocedal \& S.~J.~Wright, \textit{Numerical Optimization}, 2nd ed.\ (2006)",
            r"L.~Bottou, F.~E.~Curtis \& J.~Nocedal, \textit{Optimization Methods for Large-Scale Machine Learning} (2018)",
        ]
        papers = [
            r"H.~Robbins \& S.~Monro, \textit{A Stochastic Approximation Method} (1951); \ B.~Polyak (1964)",
            r"Q.~Li, C.~Tai \& W.~E, \textit{Stochastic Modified Equations} (2017)",
            r"J.~Cohen et al., \textit{Gradient Descent on Neural Networks Typically Occurs at the Edge of Stability} (2021)",
            r"D.~Kingma \& J.~Ba, \textit{Adam} (2014); \ I.~Loshchilov \& F.~Hutter, \textit{Decoupled Weight Decay} (2017)",
            r"K.~Jordan et al., \textit{Muon} (2024); \ J.~Liu et al., \textit{Muon is Scalable for LLM Training} (2025)",
            r"S.~Hu et al., \textit{MiniCPM} (2024); \ A.~H\"agele et al., \textit{Scaling Laws and Compute-Optimal Training "
            r"Beyond Fixed Training Durations} (2024)",
        ]
        card = reference_card(books, papers)
        data = note(r"Text: Project Gutenberg (Part 1's $30$ novels). \ Every run is computed here; \ every number on screen "
                    r"is computed and checked; \ schematics are labeled.", font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover(
            "Bottou, Curtis and Nocedal's survey is the best single account of stochastic optimization. Thanks for "
            "watching, and see you in part ten."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
