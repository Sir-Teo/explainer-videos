from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai30.common import FEAT, FEATURE_COLORS, NEURON, RESID, arrow2d, context_line, load, vec_bars


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0

        def frame(caption, color):
            box = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                                   stroke_width=1.5, fill_color="#121722", fill_opacity=1)
            return box, label(caption, font_size=22, color=color).move_to(box.get_bottom() + UP * 0.28)

        sp, sae, at, st = load("superposition"), load("sae"), load("attribution"), load("steering")
        W = np.asarray(sp["W0.97"])
        sc = 0.9 / np.linalg.norm(W, axis=0).max()
        penta = VGroup(Circle(radius=0.9, stroke_color=GREY_D, stroke_width=1),
                       *[arrow2d(ORIGIN, W[:, i], FEATURE_COLORS[i], sc, stroke_width=4) for i in range(5)])
        ar = np.asarray(sp["readout"])
        inter = VGroup(*[Rectangle(width=0.35, height=max(abs(v) * 0.7, 0.01), stroke_width=0, fill_color=FEATURE_COLORS[i],
                                   fill_opacity=0.9).move_to([i * 0.5, v * 0.35, 0]) for i, v in enumerate(ar)])
        e = np.asarray(sp["cos_edges"])
        h = np.asarray(sp["cos_hist128"])
        hist = VGroup(*[Rectangle(width=0.035, height=max(1.6 * v / h.max(), 0.005), stroke_width=0, fill_color=C.TRUE_P, fill_opacity=0.9)
                        .move_to([0.0375 * i, 0.8 * v / h.max(), 0]) for i, v in enumerate(h)])
        eq = MathTex(r"\|x - \hat x\|^2 + \lambda \|f\|_1", font_size=34, color=WHITE)
        Fz = np.asarray(sae["demo_feats"])
        k = int(np.argmax([c.isalpha() for c in str(sae["demo_text"])[20:]])) + 20
        code = VGroup(vec_bars(np.asarray(sae["demo_resid"])[k], 2.8, 0.9, RESID), vec_bars(Fz[k], 2.8, 0.9, FEAT, signed=False))
        code.arrange(DOWN, buff=0.3)
        f0 = sae["features"][0]
        ctxs = VGroup(*[context_line(c, 2.9, font_size=12) for c in f0["contexts"][:4]]).arrange(DOWN, buff=0.06)
        nodes = VGroup(*[Circle(radius=0.14, stroke_color=FEATURE_COLORS[j], stroke_width=2, fill_color=FEATURE_COLORS[j], fill_opacity=0.3)
                         .move_to([-1.0 + 0.4 * j, 0, 0]) for j in range(6)])
        top = Square(0.35, stroke_color=C.TRUE_P, stroke_width=2).move_to([0, 0.9, 0])
        bot = VGroup(*[Square(0.2, stroke_color=GREY_C, stroke_width=1).move_to([-1.2 + 0.25 * i, -0.9, 0]) for i in range(10)])
        edges = VGroup(*[Line(n_.get_top(), top.get_bottom(), stroke_width=2, color=n_.get_stroke_color()) for n_ in nodes],
                       *[Line(bot[(2 * j + 3) % 10].get_top(), n_.get_bottom(), stroke_width=1, color=GREY_C) for j, n_ in enumerate(nodes)])
        graph = VGroup(edges, nodes, top, bot)
        steer = MathTex(r"h \leftarrow h + \alpha\, d_k", font_size=38, color=C.SURPRISE)
        out = [
            (penta, r"$5$ features in $2$ dimensions", C.BITS),
            (inter, r"the price: \ interference", C.SURPRISE),
            (hist, r"room in many dimensions", C.TRUE_P),
            (eq, r"a sparse autoencoder", FEAT),
            (code, r"$128$ numbers, \ a few features", FEAT),
            (ctxs, r"what a feature means", FEAT),
            (graph, r"an attribution graph", C.TRUE_P),
            (steer, r"steering", C.SURPRISE),
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
        head = label(r"Part 30, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Models pack more features than they have numbers, as almost "
            "perpendicular directions, at the price of a little interference. A sparse autoencoder pulls those "
            "directions back apart, and they turn out to mean things. Features chain into circuits we can trace from "
            "input to output. And pushing on a feature changes what the model does."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        def box(text, color):
            t = label(text, font_size=24, color=color)
            r = RoundedRectangle(width=t.width + 0.44, height=max(0.62, t.height + 0.25), corner_radius=0.12,
                                 stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=0.1)
            return VGroup(r, t.move_to(r))

        head = label(r"Next: \ Part 31, \ Can We Trust It?", font_size=40).to_edge(UP, buff=0.5)
        steps = VGroup(*[box(t, c) for t, c in ((r"a score", GREY_B), (r"is it real?", C.INTERVAL),
                                                (r"is it what we meant?", C.PENALTY),
                                                (r"can we oversee it?", C.KL), (r"can we control it?", C.TRUE_P))])
        steps.arrange(RIGHT, buff=0.5).move_to(DOWN * 0.2)
        if steps.width > 13.2:
            steps.width = 13.2
        arrs = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5)
                        for a, b in zip(steps, steps[1:])])
        more = label(r"and, \ one last time, \ the scoreboard", font_size=28, color=C.BITS).next_to(steps, DOWN, buff=0.8)
        with self.voiceover(
            "Next time, the finale: can we trust it? How to measure a model honestly, what happens when an objective "
            "has a loophole, how to supervise a model stronger than its supervisor, the evidence that models can "
            "deceive, and how to watch and control them. And, one last time, the scoreboard."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(s_), *([GrowArrow(arrs[i - 1])] if i else []))
                                    for i, s_ in enumerate(steps)], lag_ratio=0.5), run_time=max(3.0, vo.duration - 2.5))
            self.play(FadeIn(more))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [r"C.~Olah et al., \textit{Zoom In: An Introduction to Circuits} (Distill, 2020)"]
        papers = [
            r"N.~Elhage et al., \textit{Toy Models of Superposition} (2022); \ W.~B.~Johnson \& J.~Lindenstrauss (1984)",
            r"T.~Bricken et al., \textit{Towards Monosemanticity} (2023); \ H.~Cunningham et al., \textit{Sparse Autoencoders Find "
            r"Highly Interpretable Features} (2023); \ A.~Templeton et al., \textit{Scaling Monosemanticity} (2024)",
            r"L.~Gao et al., \textit{Scaling and Evaluating Sparse Autoencoders} (2024); \ S.~Rajamanoharan et al., "
            r"\textit{JumpReLU SAEs} (2024)",
            r"E.~Ameisen et al., \textit{Circuit Tracing} (2025); \ J.~Lindsey et al., \textit{On the Biology of a Large Language Model} (2025)",
            r"A.~Turner et al., \textit{Steering Language Models with Activation Engineering} (2023); \ Y.~Chen et al., "
            r"\textit{Reasoning Models Don't Always Say What They Think} (2025)",
        ]
        card = reference_card(books, papers)
        data = note(r"Every number here is computed and checked on this computer; \ published results are marked; \ "
                    r"illustrations are labeled.", font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover("Thanks for watching, and see you in Part 31, the finale."):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.5)
        self.play(FadeOut(Group(*self.mobjects)))
