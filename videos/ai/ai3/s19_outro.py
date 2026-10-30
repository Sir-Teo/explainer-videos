from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import I_COLOR, J_COLOR, MONO, VOWELS, load


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

        def arr(a, b, col, w=4):
            return Arrow(np.array([*a, 0]), np.array([*b, 0]), buff=0, color=col, stroke_width=w,
                         max_tip_length_to_length_ratio=0.2)

        out = []
        # 1. adding vectors
        out.append((VGroup(arr((0, 0), (1.2, 0.5), I_COLOR), arr((1.2, 0.5), (0.6, 1.5), J_COLOR),
                           arr((0, 0), (0.6, 1.5), C.BITS)), r"vectors: \ add, scale", C.BITS))
        # 2. the dot product as a shadow
        a = np.array([1.6, 0.4])
        b = np.array([0.7, 1.3])
        p = (b @ a) / (a @ a) * a
        out.append((VGroup(arr((0, 0), a, C.TRUE_P), arr((0, 0), b, C.MODEL_Q),
                           DashedLine([*b, 0], [*p, 0], color=GREY_B, stroke_width=2),
                           Line(ORIGIN, [*p, 0], color=C.REWARD, stroke_width=8)), r"the dot product", C.TRUE_P))
        # 3. a matrix moves the grid
        g = NumberPlane(x_range=[-3, 3, 1], y_range=[-3, 3, 1], background_line_style={"stroke_color": BLUE_D,
                        "stroke_width": 1.5}, axis_config={"stroke_width": 1.5}).scale(0.32)
        g.apply_matrix(np.array([[1.0, 0.6], [0.2, 1.0]]))
        out.append((g, r"matrices move space", BLUE_C))
        # 4. eigenvectors of a symmetric matrix
        ell = Ellipse(width=2.6, height=1.0, color=C.BITS, stroke_width=3).rotate(PI / 4)
        out.append((VGroup(ell, arr((0, 0), (0.92, 0.92), I_COLOR), arr((0, 0), (0.36, -0.36), J_COLOR)),
                    r"eigenvectors", I_COLOR))
        # 5. SVD: circle to ellipse
        out.append((VGroup(DashedVMobject(Circle(radius=0.7, color=GREY_B, stroke_width=2), num_dashes=24),
                           Ellipse(width=2.4, height=0.9, color=C.BITS, stroke_width=3).rotate(-0.4)),
                    r"turn, stretch, turn", C.BITS))
        # 6. the vowel axis
        d = load("letters")
        row = np.asarray(d["ca_row"])
        letters = "abcdefghijklmnopqrstuvwxyz"
        lo, hi = float(row.min()), float(row.max())
        line = VGroup(Line([-1.4, 0, 0], [1.4, 0, 0], color=GREY_C, stroke_width=2))
        vx = []
        for i, ch in enumerate(letters):  # every letter a dot on the axis; the vowels gold
            x = -1.4 + 2.8 * (row[i] - lo) / (hi - lo)
            line.add(Dot([x, 0, 0], radius=0.06 if ch in VOWELS else 0.04, color=C.BITS if ch in VOWELS else GREY_A))
            if ch in VOWELS:
                vx.append(x)
        vb = Brace(Line([min(vx) - 0.05, 0, 0], [max(vx) + 0.05, 0, 0]), UP, buff=0.12, color=C.BITS)
        line.add(vb, Text("a e i o u", font=MONO, font_size=20, color=C.BITS).next_to(vb, UP, buff=0.08)
                 .align_to(vb, LEFT))
        out.append((line, r"SVD finds the vowels", C.BITS))
        # 7. the analogy
        xy = np.asarray(load("words")["analogy_xy"])
        xy = xy / np.abs(xy).max() * 1.1
        pts = [np.array([x, y, 0]) for x, y in xy]
        out.append((VGroup(*[Dot(q, radius=0.06, color=C.BITS if k % 2 else C.TRUE_P) for k, q in enumerate(pts)],
                           Arrow(pts[0], pts[1], buff=0.08, color=C.BITS, stroke_width=3),
                           Arrow(pts[2], pts[2] + pts[1] - pts[0], buff=0.08, color=C.BITS, stroke_width=3)),
                    r"france $\to$ paris, \ england $\to$ london", C.BITS))
        # 8. angles in 768 dimensions
        h = load("highdim")
        hist = np.asarray(h["angles768"], float)
        bars = VGroup(*[Rectangle(width=0.07, height=max(1.6 * v / hist.max(), 0.005), stroke_width=0, fill_color=C.TRUE_P,
                                  fill_opacity=0.9).move_to([-1.3 + 0.075 * k, -0.7 + 0.8 * v / hist.max(), 0])
                        for k, v in enumerate(hist)])
        out.append((bars, r"$768$ dimensions: \ room", C.TRUE_P))
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
        head = label(r"Part 3, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Vectors are arrows, and lists of numbers, and they add and stretch. The dot product "
            "measures how alike two of them are, and it's the score behind every next-token guess. Matrices move "
            "the whole space at once. Symmetric ones just stretch along perpendicular directions, and every matrix "
            "is a turn, a stretch, and a turn. Keeping the biggest pieces of that decomposition found the vowels in "
            "letters, and the meanings of words in thirty novels. And in hundreds of dimensions there is room to "
            "spare."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15, scale=0.95) for t in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"dot products as scores", [13]),
            (r"layers of matrices", [9]),
            (r"the stretch per layer; \ the spectral norm", [9, 11]),
            (r"low rank: \ keep the biggest pieces", [7, 15]),
            (r"word vectors, tokens", [23]),
            (r"room in high dimensions: \ superposition", [30]),
        ], font_size=24)
        with self.voiceover(
            "All of it comes back. Attention, the heart of the transformer, is dot products between vectors. A "
            "network is matrices, layer after layer, and keeping their stretch near one is how deep networks train "
            "at all; one of the newest optimizers works directly on the spectral norm. Low-rank pieces compress "
            "the memory of today's largest models. And the room in high dimensions is where models keep more ideas "
            "than they have numbers."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 4, \ Change", font_size=40).to_edge(UP, buff=0.35)

        def f(x, y):
            return 0.5 * x * x + 1.5 * y * y + 0.6 * math.sin(2 * x) * math.cos(y)

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
            "Next time: change. Everything in this part stood still. Training moves: every one of a model's numbers "
            "is nudged, again and again, in the direction that lowers the loss. <bookmark mark='a'/> Finding that "
            "direction for billions of numbers at once is the chain rule, run backwards. Part four builds that "
            "machine from scratch."
        ) as vo:
            self.play(FadeIn(head), Create(field), FadeIn(tag), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(ball))
            self.play(MoveAlongPath(ball, trail), Create(trail), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [
            r"G.~Strang, \textit{Linear Algebra and Learning from Data} (2019)",
            r"S.~Axler, \textit{Linear Algebra Done Right}, 4th ed.\ (2024)",
            r"R.~Vershynin, \textit{High-Dimensional Probability} (2018), chapters 3, 5",
        ]
        papers = [
            r"C.~Eckart \& G.~Young, \textit{The Approximation of One Matrix by Another of Lower Rank} (1936)",
            r"W.~B.~Johnson \& J.~Lindenstrauss (1984); \ S.~Dasgupta \& A.~Gupta, \textit{An Elementary Proof of a "
            r"Theorem of Johnson and Lindenstrauss} (2003)",
            r"S.~Deerwester et al., \textit{Indexing by Latent Semantic Analysis} (1990)",
            r"T.~Mikolov et al., \textit{Distributed Representations of Words and Phrases} (2013)",
            r"O.~Levy \& Y.~Goldberg, \textit{Neural Word Embedding as Implicit Matrix Factorization} (2014)",
            r"K.~Ethayarajh, \textit{How Contextual are Contextualized Word Representations?} (2019)",
            r"A.~Radford et al., \textit{Language Models are Unsupervised Multitask Learners} (GPT-2, 2019)",
            r"N.~Elhage et al., \textit{Toy Models of Superposition} (2022)",
        ]
        card = reference_card(books, papers)
        data = note(r"Text: Project Gutenberg (the same $30$ novels as Part 1); \ GPT-2's own weights. \ Every number "
                    r"on screen is computed and checked; \ schematics and illustrations are labeled.",
                    font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover(
            "For more, Gilbert Strang's Linear Algebra and Learning from Data is a friendly companion, and Roman "
            "Vershynin's High-Dimensional Probability explains why big spaces behave the way they do. The papers "
            "are on screen. Thanks for watching, and see you in part four."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
