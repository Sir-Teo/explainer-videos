from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai13.s03_transformer import board_rows
from videos.ai.ai30.common import FEAT, FEATURE_COLORS, NEURON, RESID, arrow2d, context_line, load, vec_bars


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.series()
        self.board()
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
            "Let's take stock, one last time. Models pack more features than they have numbers, as almost "
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
    def series(self):
        title = label(r"AI, Built: \ twenty parts", font_size=48).to_edge(UP, buff=0.5)
        smap = series_map(current=None, done=0).scale(0.95).move_to(DOWN * 0.4)
        acts = [r"guessing the next character, and the mathematics underneath",
                r"learning from data, by counting and by going downhill",
                r"the engines: attention, memory, experts, diffusion, every sense",
                r"reasoning, acting, running fast, and looking inside"]
        cap = label(acts[0], font_size=24, color=C.BITS).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "And that's the series. <bookmark mark='a'/> We began with a guessing game: predicting the next "
            "character, and the probability, linear algebra and calculus underneath it. <bookmark mark='b'/> Then "
            "learning: counting, fitting, networks, and the long walk downhill. <bookmark mark='c'/> Then the engines: "
            "attention, memory, experts, diffusion, and every sense turned into tokens. <bookmark mark='d'/> And "
            "finally what they do with it: reasoning, acting, running fast, and now, looking inside."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            box = None
            for i, m in enumerate("abcd"):
                vo.wait_until(m)
                col = smap.cols[i]
                new = label(acts[i], font_size=24, color=C.BITS).to_edge(DOWN, buff=0.45)
                nb = SurroundingRectangle(col, color=C.BITS, buff=0.15, corner_radius=0.1, stroke_width=2)
                self.play(Transform(cap, new) if i else FadeIn(cap), Transform(box, nb) if box else Create(nb),
                          LaggedStart(*[r_.animate.set_color(WHITE) for r_ in col.rows], lag_ratio=0.15), run_time=1.5)
                box = box or nb
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def board(self):
        rows, i, n, k = board_rows()
        board = scoreboard(rows, highlight=(i,), max_bits=8.0)
        board.scale_to_fit_height(min(board.height, 6.4)).move_to(DOWN * 0.15)
        tf = rows[i]
        human = next(r for r in rows if r.get("kind") == "human")
        with self.voiceover(
            "And the scoreboard from part one, where it all started: bits per character on one passage of a novel. "
            f"Counting got us to {rows[i - 3]['bits']:.2f}; our own transformer, trained on a laptop-sized computer, "
            f"to {tf['bits']:.2f}. The big models reach about one bit, inside the range people manage, between "
            f"{human['lo']:g} and {human['hi']:g}. <bookmark mark='a'/> Every row of it is the same idea: a better "
            "guess at what comes next. Thank you for building it with me."
        ) as vo:
            self.play(FadeIn(board), run_time=2.0)
            vo.wait_until("a")
            self.play(Circumscribe(board.rows[i], color=C.NEURAL, buff=0.05))
        self.wait(0.5)
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
        with self.voiceover("Thanks for watching."):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.5)
        self.play(FadeOut(Group(*self.mobjects)))
