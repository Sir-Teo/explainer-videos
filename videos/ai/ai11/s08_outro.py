from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import A, K, OURS, POS, Q, V, curve, heat_image, load, signed_image


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

        def plane(xr, yr):
            return Axes(x_range=xr, y_range=yr, x_length=TW, y_length=TH, tips=False, axis_config={"stroke_width": 0})

        out = []
        # 1. the kernel smoother
        s = load("smoother")
        x, y, xs = np.asarray(s["x"]), np.asarray(s["y"]), np.asarray(s["xs"])
        a1 = plane([0, x[-1], 10], [0, y.max(), 1])
        out.append((VGroup(*[Dot(a1.c2p(a, b), radius=0.02, color=V) for a, b in zip(x, y)],
                           curve(a1, xs, np.asarray(s["fit2.5"]), Q, 2.5, smooth=True)), r"a weighted average", Q))
        # 2. queries and keys
        keys = np.array([[2.4, 0.5], [1.2, 1.9], [-0.6, 2.2], [-2.1, 0.4], [-1.0, -1.9], [1.6, -1.6]])
        a2 = plane([-3, 3, 1], [-3, 3, 1])
        g2 = VGroup(*[Arrow(a2.c2p(0, 0), a2.c2p(*k), buff=0, color=K, stroke_width=3, max_tip_length_to_length_ratio=0.15)
                      for k in keys], Arrow(a2.c2p(0, 0), a2.c2p(1.5, 0.45), buff=0, color=Q, stroke_width=5,
                                            max_tip_length_to_length_ratio=0.2))
        out.append((g2, r"queries and keys", K))
        # 3. our transformer's heads
        t = load("tf")
        maps = np.asarray(t["maps"])
        out.append((Group(*[heat_image(maps[0, h], 0.9, 0.9, mask_upper=True) for h in range(3)]).arrange(RIGHT, buff=0.08),
                    r"our transformer", OURS))
        # 4. rotations
        r = load("rope")
        th = np.asarray(r["theta"])[::2]
        dials = VGroup()
        for j, tj in enumerate(th):
            c_ = Circle(radius=0.3, stroke_color=GREY_C, stroke_width=1.2)
            hand = Line(ORIGIN, 0.27 * np.array([np.cos(1.0 + 20 * tj), np.sin(1.0 + 20 * tj), 0]), color=Q, stroke_width=2.5)
            dials.add(VGroup(c_, hand))
        dials.arrange_in_grid(rows=2, cols=4, buff=0.12)
        out.append((dials, r"positions as rotations", POS))
        # 5. extension
        e = load("extend")
        a5 = plane([0, int(e["T"]), 64], [1.5, 6, 1])
        g5 = VGroup()
        for k_, c_ in (("plain", C.SURPRISE), ("pi", C.TRUE_P), ("ntk", C.INTERVAL), ("yarn", C.BITS)):
            b = np.asarray(e[f"bucket_{k_}"])
            g5.add(curve(a5, np.arange(len(b)) * 64 + 32, np.clip(b, 1.5, 6), c_, 2.5))
        out.append((g5, r"longer contexts", C.BITS))
        # 6. sinks
        sink = np.asarray(t["sink"])
        li, hi = np.unravel_index(np.argmax(sink), sink.shape)
        out.append((heat_image(maps[li, hi], 1.9, 1.9, mask_upper=True), r"attention sinks", POS))
        # 7. induction
        d = load("induction")
        out.append((heat_image(np.asarray(d["map_ind"]), 1.9, 1.9, mask_upper=True), r"induction heads", A))
        # 8. in-context learning
        c = load("icl")
        out.append((Group(signed_image(np.asarray(c["Wkq"]), 1.3, 1.3), signed_image(np.asarray(c["Wpv"]), 1.3, 1.3))
                    .arrange(RIGHT, buff=0.2), r"learning in context", C.BITS))
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
        head = label(r"Part 11, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Attention is a weighted average, Nadaraya and Watson's smoother with a learned "
            "kernel: queries and keys decide the weights, values carry the content, and a square root keeps the "
            "softmax from collapsing. Stacked with MLPs on a residual stream, it made our own transformer. "
            "Positions are rotations, which makes scores depend on distance, and rescaling the rotations stretches "
            "a model's context. And trained heads find tricks of their own: sinks that park attention, induction "
            "heads that copy, and a layer that runs gradient descent on its prompt."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"every past key and value, kept: \ the KV cache", [12, 19]),
            (r"attention to only some of the past", [13]),
            (r"attention over image patches and sounds", [15, 16]),
            (r"learning from the prompt", [17]),
            (r"heads and circuits, \ taken apart", [20]),
        ], font_size=26)
        with self.voiceover(
            "This comes back everywhere. To write fast, a model keeps every past key and value: part twelve is about "
            "that memory, and part nineteen about serving it. Part thirteen attends to only some of the past. Images "
            "and sound become sequences to attend over in parts fifteen and sixteen. Learning from the prompt is "
            "where reasoning starts, in part seventeen, and part twenty opens up heads and circuits in real models."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 12, \ Memory", font_size=40).to_edge(UP, buff=0.4)
        n = 24
        sq = VGroup(*[Square(0.22, stroke_width=0.8, stroke_color=GREY_D, fill_color=A,
                             fill_opacity=0.15 + 0.6 * (j <= i) * np.exp(-0.15 * (i - j)))
                      for i in range(n) for j in range(n)])
        sq.arrange_in_grid(rows=n, cols=n, buff=0).move_to(LEFT * 3.2 + DOWN * 0.4)
        sl = label(r"attention: \ every new character \\ looks at all the old ones", font_size=26, color=A).next_to(sq, RIGHT, buff=0.6)
        state = VGroup(*[Square(0.3, stroke_width=1, stroke_color=GREY_C, fill_color=C.EMBED, fill_opacity=0.6) for _ in range(8)])
        state.arrange_in_grid(rows=2, cols=4, buff=0.04).move_to([3.8, -1.6, 0])
        stl = label(r"or a fixed-size memory, \ updated as it reads?", font_size=26, color=C.EMBED).next_to(state, UP, buff=0.25)
        tag = note(r"schematic").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Next time: memory. Attention makes every new character look at all the old ones, so its cost grows with "
            "every character read. <bookmark mark='a'/> Could a model instead keep a fixed-size memory, updated as it "
            "reads? That's the idea behind state-space models, linear attention and the hybrids in the newest "
            "models."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(s_) for s_ in sq], lag_ratio=0.0008), FadeIn(sl),
                      run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(state), FadeIn(stl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [
            r"S.~J.~D.~Prince, \textit{Understanding Deep Learning} (2023), chapter 12",
            r"D.~Jurafsky \& J.~H.~Martin, \textit{Speech and Language Processing} (3rd ed.\ draft), chapter 9",
        ]
        papers = [
            r"E.~A.~Nadaraya, \textit{On Estimating Regression} (1964); \ G.~S.~Watson, \textit{Smooth Regression Analysis} (1964)",
            r"A.~Vaswani et al., \textit{Attention Is All You Need} (2017)",
            r"J.~Su et al., \textit{RoFormer} (2021); \ S.~Chen et al., \textit{Position Interpolation} (2023); "
            r"\ B.~Peng et al., \textit{YaRN} (2023)",
            r"G.~Xiao et al., \textit{Attention Sinks} (2023)",
            r"N.~Elhage et al., \textit{A Mathematical Framework for Transformer Circuits} (2021); \ C.~Olsson et al., "
            r"\textit{Induction Heads} (2022)",
            r"S.~Garg et al.\ (2022); \ J.~von Oswald et al., \textit{Transformers Learn In-Context by Gradient Descent} (2023)",
        ]
        card = reference_card(books, papers)
        data = note(r"Text: Project Gutenberg (Part 1's $30$ novels). \ Every model here is trained on this video's CPU; "
                    r"\ every number on screen is computed and checked; \ illustrations are labeled.",
                    font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover(
            "Anthropic's 'Mathematical Framework for Transformer Circuits' is the best next read. Thanks for "
            "watching, and see you in part twelve."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
