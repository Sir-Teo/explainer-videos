from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import load

KN = C.COUNTING
ADD = GREY_B


class KneserNey(VoiceoverScene):
    def construct(self):
        self.card()
        self.orders()
        self.idea()
        self.board()

    def card(self):
        card = chapter_card(7, r"Kneser--Ney", r"How do you count what you've never seen?", part=6)
        with self.voiceover("Chapter seven. The best way to count."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def orders(self):
        k = load("kn")
        p1 = np.asarray(k["part1_rows"])
        kn = np.array([r["test"] for r in k["rows"]])
        M = len(kn) - 1
        ax = Axes(x_range=[0, M, 1], y_range=[1.8, 4.8, 0.5], x_length=8.0, y_length=4.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.4, -0.4, 0])
        xl = VGroup(*[MathTex(str(i), font_size=24, color=GREY_B).next_to(ax.c2p(i, 1.8), DOWN, buff=0.12) for i in range(M + 1)])
        yl = VGroup(*[MathTex(f"{v:.1f}", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12)
                      for v in (2.0, 3.0, 4.0)])
        xn = label(r"characters of context", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.55)
        yn = label(r"bits per character on the passage", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        c1 = VMobject(color=ADD, stroke_width=4).set_points_as_corners([ax.c2p(i, v) for i, v in enumerate(p1[:M + 1])])
        d1 = VGroup(*[Dot(ax.c2p(i, v), radius=0.06, color=ADD) for i, v in enumerate(p1[:M + 1])])
        c2 = VMobject(color=KN, stroke_width=4).set_points_as_corners([ax.c2p(i, v) for i, v in enumerate(kn)])
        d2 = VGroup(*[Dot(ax.c2p(i, v), radius=0.06, color=KN) for i, v in enumerate(kn)])
        l1 = label(r"Part 1: \ add a little to every count", font_size=26, color=ADD).move_to([4.4, 1.2, 0])
        l2 = label(rf"Kneser--Ney: \ ${kn[-1]:.2f}$ at ${M}$ characters", font_size=26, color=KN).next_to(l1, DOWN, buff=0.4)
        l2.align_to(l1, LEFT)
        best1 = int(np.argmin(p1))
        with self.voiceover(
            "Back to part one's scoreboard. The best counting model there used four characters of context and reached "
            f"{p1[best1]:.2f} bits per character on the passage. <bookmark mark='a'/> Longer contexts should help, but "
            "they're rare: most long contexts in the passage appeared only a handful of times in thirty novels, if at "
            "all. With part one's simple smoothing, the score gets worse beyond four characters. "
            "<bookmark mark='b'/> Better smoothing keeps improving."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(xn), FadeIn(yn))
            vo.wait_until("a")
            self.play(Create(c1), LaggedStart(*[FadeIn(d) for d in d1], lag_ratio=0.1), FadeIn(l1), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(c2), LaggedStart(*[FadeIn(d) for d in d2], lag_ratio=0.1), FadeIn(l2), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def idea(self):
        colors = {r"D": C.SURPRISE, r"P_{\mathrm{KN}}(c \mid h')": KN, r"\lambda(h)": C.SURPRISE}
        f = cmath(r"P_{\mathrm{KN}}(c \mid h)", "=", r"\frac{\max\big(N(h c) -", r"D", r",\, 0\big)}{N(h)}", "+",
                  r"\lambda(h)", r"\,", r"P_{\mathrm{KN}}(c \mid h')", colors=colors, font_size=40).to_edge(UP, buff=0.6)
        n1 = label(r"$h$: \ the context; \ $h'$: \ the context with its oldest character dropped", font_size=24,
                   color=GREY_A).next_to(f, DOWN, buff=0.25)
        idea1 = label(r"1. \ take a fixed discount $D$ off every count seen, \\ and hand it to the shorter context",
                      font_size=28, color=C.SURPRISE)
        cont = cmath(r"N(h c)", r"\;\longrightarrow\;", r"N_{1+}(\,\bullet\, h c)", font_size=40)
        idea2 = label(r"2. \ below the top, count how many \emph{different} contexts \\ a character follows, \ not how "
                      r"often it appears", font_size=28, color=KN)
        ex = label(r"the textbook example: \ ``Francisco'' is common, \\ but nearly always after ``San''", font_size=24,
                   color=GREY_A)
        VGroup(idea1, idea2).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([-1.6, -1.2, 0])
        cont.next_to(idea2, DOWN, buff=0.3).align_to(idea2, LEFT).shift(RIGHT * 0.5)
        ex.move_to([4.2, -3.0, 0])
        cite_ = cite(r"R.~Kneser \& H.~Ney (1995); \ S.~Chen \& J.~Goodman (1998)", corner=DR)
        # the discount in a picture (schematic counts): a slice D off each seen count, poured into the shorter context
        U, dh = 0.32, 0.32
        counts = [6, 4, 3, 2]
        cbars = VGroup(*[Rectangle(width=0.45, height=c * U - dh, stroke_width=0, fill_color=KN, fill_opacity=0.85)
                         .move_to([2.6 + 0.65 * i, -1.5 + (c * U - dh) / 2, 0]) for i, c in enumerate(counts)])
        slices = VGroup(*[Rectangle(width=0.45, height=dh, stroke_width=0, fill_color=C.SURPRISE, fill_opacity=0.9)
                          .next_to(b, UP, buff=0) for b in cbars])
        base = Line([2.25, -1.5, 0], [6.9, -1.5, 0], color=GREY_C, stroke_width=2)
        pile = Rectangle(width=0.55, height=dh * len(counts), stroke_color=C.SURPRISE, stroke_width=2)
        pile.move_to([6.2, -1.5 + dh * len(counts) / 2, 0])
        dl = MathTex(r"D", font_size=30, color=C.SURPRISE).next_to(slices[0], LEFT, buff=0.12)
        cl = label(r"counts after $h$", font_size=22, color=KN).next_to(cbars, DOWN, buff=0.12)
        pl = label(r"to $h'$", font_size=22, color=C.SURPRISE).next_to(pile, DOWN, buff=0.12)
        moved = VGroup(*[s.copy().move_to([6.2, -1.5 + dh * (j + 0.5), 0]).set(width=0.55)
                         for j, s in enumerate(slices)])
        with self.voiceover(
            "Kneser and Ney's smoothing, from 1995, has two ideas. <bookmark mark='a'/> First, shave a fixed "
            "discount off every count you've seen, <bookmark mark='c'/> and use the savings to back off to a shorter "
            "context, one character fewer: blend the two. "
            "<bookmark mark='b'/> Second, judge the shorter contexts by their variety. The textbook example: "
            "Francisco is a common word, but nearly always after San, so as a guess after an unfamiliar context it "
            "deserves little. Count how many different contexts something follows, not how often it appears."
        ) as vo:
            self.play(Write(f), FadeIn(n1), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(idea1), Indicate(term(f, r"D"), color=C.SURPRISE), Create(base), FadeIn(cbars),
                      FadeIn(slices), FadeIn(cl))
            self.play(FadeIn(dl))
            vo.wait_until("c")
            self.play(Create(pile), FadeIn(pl), *[ReplacementTransform(s, m) for s, m in zip(slices, moved)],
                      run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(idea2), FadeIn(cont), FadeIn(ex))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def board(self):
        from videos.ai.ai1 import compute as c1

        k = load("kn")
        sb = c1.load("scoreboard")
        rows = [dict(r) for r in sb["rows"]]
        i = next(j for j, r in enumerate(rows) if r["key"] == "best") + 1
        new = dict(key="kn", label=rf"Kneser--Ney, \ ${k['best']}$ characters", bits=k["best_bits"], part=6, kind="count")
        rows.insert(i, new)
        board = scoreboard(rows, highlight=(i,), max_bits=8.0)
        board.scale_to_fit_height(min(board.height, 6.6)).move_to(DOWN * 0.1)
        row = board.rows[i]
        glow = SurroundingRectangle(row, color=KN, buff=0.08, corner_radius=0.08)
        with self.voiceover(
            f"With seven characters of context, Kneser–Ney reaches {k['best_bits']:.2f} bits per character on the "
            "passage. <bookmark mark='a'/> For two decades, from speech recognition to machine translation, this was "
            "the state of the art in language modelling. It's the scoreboard's last counting row. Everything better "
            "is a neural network, and that's where we're going next."
        ) as vo:
            self.play(FadeIn(board))
            vo.wait_until("a")
            self.play(Create(glow), Indicate(row, color=KN, scale_factor=1.05))
        self.wait(0.5)
        self.clear_scene()
