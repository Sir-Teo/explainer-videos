from __future__ import annotations

import itertools

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import INFO, LOSS, MART, P_C, PART

OUTCOMES = ["".join(o) for o in itertools.product("HT", repeat=3)]
X = np.array([o.count("H") for o in OUTCOMES], float)


def cond_exp(n):
    """E[X | the first n tosses], outcome by outcome."""
    out = np.empty(8)
    for i, o in enumerate(OUTCOMES):
        same = [j for j, p in enumerate(OUTCOMES) if p[:n] == o[:n]]
        out[i] = X[same].mean()
    return out


class Information(VoiceoverScene, MovingCameraScene):
    def construct(self):
        self.card()
        self.filtration()
        self.questions()
        self.coin_space()

    def card(self):
        c = chapter_card(1, r"Information: $\sigma$-algebras and filtrations", r"What do you know, and when?",
                         lit=(1933,), part=PART)
        with self.voiceover("Chapter one. Information: sigma-algebras and filtrations."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def filtration(self):
        w = 1.32
        cells = VGroup(*[VGroup(RoundedRectangle(width=w - 0.12, height=0.7, corner_radius=0.08, stroke_color=GREY_B,
                                                 stroke_width=1.5),
                                MathTex(o, font_size=30)) for o in OUTCOMES]).arrange(RIGHT, buff=0.12)
        for c in cells:
            c[1].move_to(c[0])
        cells.to_edge(UP, buff=1.0).shift(RIGHT * 0.6)
        xs = VGroup(*[MathTex(rf"{int(v)}", font_size=26, color=GREY_A).next_to(c, UP, buff=0.12)
                      for c, v in zip(cells, X)])
        xlab = MathTex(r"X = \#\text{heads}", font_size=28, color=GREY_A).next_to(xs, LEFT, buff=0.3)

        def blocks(n):
            g = VGroup()
            size = 8 // 2 ** n
            for b in range(2 ** n):
                grp = VGroup(*cells[b * size:(b + 1) * size])
                g.add(SurroundingRectangle(grp, buff=0.05, color=INFO, stroke_width=3, corner_radius=0.1))
            return g

        base_y = cells.get_bottom()[1] - 0.4
        unit = 0.8

        def bars(n):
            vals = cond_exp(n)
            g = VGroup()
            for c, v in zip(cells, vals):
                r = Rectangle(width=w - 0.4, height=v * unit + 1e-3, stroke_width=0, fill_color=MART, fill_opacity=0.8)
                r.move_to([c.get_x(), base_y, 0], aligned_edge=UP)
                t = MathTex(f"{v:g}", font_size=24, color=MART).next_to(r, DOWN, buff=0.08)
                g.add(VGroup(r, t))
            return g

        nlab = [MathTex(rf"\mathcal{{F}}_{n}", r"\text{: after toss } " + str(n) if n else r"\text{: before any toss}",
                        font_size=32, color=INFO) for n in range(4)]
        for m in nlab:
            m.to_corner(DL, buff=0.6)
        elab = MathTex(r"\mathbb{E}[X \mid \mathcal{F}_n]", font_size=34, color=MART).to_corner(DR, buff=0.6)
        current_b, current_bar = blocks(0), bars(0)
        defs = VGroup(
            label(r"a filtration: the questions you can answer at each time, growing", font_size=22, color=INFO),
            label(r"conditional expectation: the best guess of $X$ given what you know", font_size=22, color=MART),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=1.4)
        with self.voiceover(
            "Probability in finance is about information: what you know, and when. Toss a coin three times. There are "
            "eight possible worlds, and X counts the heads in each. <bookmark mark='a'/> Before any toss you cannot "
            "tell the worlds apart: they all sit in one block. Your best guess of X is its average, one and a half, "
            "in every world. <bookmark mark='b'/> After the first toss, the worlds split in two. If it was heads, the "
            "best guess is two; if tails, one. <bookmark mark='c'/> After the second toss, four blocks, and four "
            "guesses. <bookmark mark='d'/> After the third, you know X exactly. <bookmark mark='e'/> The growing "
            "sequence of partitions is called a filtration: the questions you can answer at each time. And the best "
            "guess on each block, the average over the worlds you can't yet tell apart, is the conditional "
            "expectation of X given what you know. Watch the guess: it moves only when information arrives, and "
            "on average it doesn't move at all."
        ) as vo:
            self.play(FadeIn(cells), FadeIn(xs), FadeIn(xlab))
            vo.wait_until("a")
            self.play(Create(current_b), FadeIn(nlab[0]), FadeIn(elab), LaggedStart(*[GrowFromEdge(b[0], UP) for b in current_bar]),
                      FadeIn(VGroup(*[b[1] for b in current_bar])))
            for n, mark in zip((1, 2, 3), ("b", "c", "d")):
                vo.wait_until(mark)
                nb, nbar = blocks(n), bars(n)
                self.play(ReplacementTransform(current_b, nb), ReplacementTransform(current_bar, nbar),
                          ReplacementTransform(nlab[n - 1], nlab[n]), run_time=1.5)
                current_b, current_bar = nb, nbar
            vo.wait_until("e")
            self.play(FadeIn(defs))
        self.wait(0.4)
        self.clear_scene()

    def questions(self):
        # the eight worlds again, small, with F_1's two blocks; two variables tested for F_1-measurability
        w = 0.95
        cells = VGroup(*[VGroup(RoundedRectangle(width=w - 0.1, height=0.55, corner_radius=0.06, stroke_color=GREY_B,
                                                 stroke_width=1.5), MathTex(o, font_size=24))
                         for o in OUTCOMES]).arrange(RIGHT, buff=0.1)
        for c in cells:
            c[1].move_to(c[0])
        cells.to_edge(UP, buff=0.7).to_edge(LEFT, buff=0.6)
        blocks = VGroup(*[SurroundingRectangle(VGroup(*cells[4 * b:4 * b + 4]), buff=0.05, color=INFO, stroke_width=3,
                                               corner_radius=0.08) for b in range(2)])
        deck = VGroup(
            label(r"$\mathcal{F}_n$: every event you can decide after $n$ tosses", font_size=22, color=INFO),
            MathTex(r"\mathcal{F}_n = \{\text{unions of the } 2^n \text{ blocks}\}", font_size=30),
            MathTex(r"|\mathcal{F}_n| = 2^{2^n}: \quad 2,\ 4,\ 16,\ 256", font_size=30, color=INFO),
            label(r"each block in or out of the union", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.5).shift(UP * 1.9)
        first = np.array([1.0 if o[0] == "H" else 0.0 for o in OUTCOMES])
        heads = X

        def bars(vals, col, y0, unit=0.32):
            g = VGroup()
            for c, v in zip(cells, vals):
                r = Rectangle(width=w - 0.4, height=v * unit + 1e-3, stroke_width=0, fill_color=col, fill_opacity=0.85)
                r.move_to([c.get_x(), y0, 0], aligned_edge=DOWN)
                g.add(r)
            return g

        b1 = bars(first, MART, -0.6)
        b2 = bars(heads, LOSS, -2.9)
        t1 = VGroup(MathTex(r"X_1 = \mathbf{1}\{\text{first toss } H\}", font_size=28, color=MART),
                    label(r"constant on each $\mathcal{F}_1$ block: measurable \checkmark", font_size=20, color=MART)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(b1, RIGHT, buff=0.5).align_to(b1, DOWN)
        t2 = VGroup(MathTex(r"X = \#\text{heads}", font_size=28, color=LOSS),
                    label(r"varies inside a block: not $\mathcal{F}_1$-measurable $\times$", font_size=20, color=LOSS)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(b2, RIGHT, buff=0.5).align_to(b2, DOWN)
        guides = VGroup(*[DashedLine([cells[4 * b].get_left()[0], y, 0], [cells[4 * b + 3].get_right()[0], y, 0],
                                     color=INFO, stroke_width=1.5)
                          for b in range(2) for y in (-0.6, -2.9)])
        pred = desk_question(r"Is ``the number of heads in the first two tosses is even'' an $\mathcal{F}_1$ event?",
                             r"No: it needs the second toss, so it is in $\mathcal{F}_2$ but not $\mathcal{F}_1$.",
                             width=6.0, font_size=22).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Make that precise. A sigma-algebra is the collection of yes-or-no questions you can answer. After n "
            "tosses they are exactly the unions of the blocks, each block in or out: two to the two to the n of "
            "them. <bookmark mark='a'/> A random variable is measurable when you can compute it from what you know, "
            "which on a partition means it is constant on every block. The first toss passes. "
            "<bookmark mark='b'/> The number of heads fails: inside each block it still varies. A process measurable "
            "at every time is called adapted. <bookmark mark='c'/> Check yourself: is the event that the first two "
            "tosses hold an even number of heads in F one? No. It needs the second toss."
        ) as vo:
            self.play(FadeIn(cells), Create(blocks), FadeIn(deck[:2]))
            self.play(FadeIn(deck[2:]))
            vo.wait_until("a")
            self.play(FadeIn(guides[0::2]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in b1], lag_ratio=0.1), FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeIn(guides[1::2]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in b2], lag_ratio=0.1), FadeIn(t2))
            vo.wait_until("c")
            self.play(FadeIn(pred, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def coin_space(self):
        # the unit interval as the space of infinite coin tosses: each toss halves the block that holds the world
        W = 12.0
        bar = Rectangle(width=W, height=0.5, stroke_color=GREY_B, stroke_width=2, fill_color=INFO, fill_opacity=0.12)
        bar.move_to(DOWN * 0.4)
        x0 = bar.get_left()[0]
        omega = 0.6180339887  # the hidden world: its binary digits are the tosses (1 = heads)
        digits = []
        v = omega
        for _ in range(7):
            v *= 2
            digits.append(int(v >= 1))
            v -= int(v >= 1)
        gold = Dot([x0 + W * omega, bar.get_y(), 0], radius=0.06, color=QC.IDEA)
        ends = [0.0, 1.0]
        lab0 = MathTex(r"0", font_size=28, color=GREY_B).next_to(bar, DOWN, buff=0.15).align_to(bar, LEFT)
        lab1 = MathTex(r"1", font_size=28, color=GREY_B).next_to(bar, DOWN, buff=0.15).align_to(bar, RIGHT)
        map_ = MathTex(r"\omega = (\omega_1, \omega_2, \dots) \;\mapsto\; \sum_k \omega_k\, 2^{-k} \in [0, 1]",
                       font_size=34).to_edge(UP, buff=0.6)
        cap = label(r"fair tosses $\leftrightarrow$ length on $[0,1]$ (Lebesgue measure): a block after $n$ tosses has "
                    r"length $2^{-n}$", font_size=22, color=GREY_A).next_to(map_, DOWN, buff=0.25)
        kol = history_card(1933, r"Kolmogorov, \textit{Grundbegriffe der Wahrscheinlichkeitsrechnung}",
                           r"a probability space $(\Omega, \mathcal{F}, P)$: $P$ countably additive on a $\sigma$-algebra "
                           r"of events; conditional expectation defined for any $\sigma$-algebra", width=7.2)
        kol.to_edge(DOWN, buff=0.3)
        grid = VGroup()
        shade = VGroup()
        toss_labels = VGroup()
        for n, dgt in enumerate(digits[:6], 1):
            k = 2 ** n
            lines = VGroup(*[Line([x0 + W * j / k, bar.get_bottom()[1], 0], [x0 + W * j / k, bar.get_top()[1], 0],
                                  color=INFO, stroke_width=max(2.6 - 0.35 * n, 0.6)) for j in range(1, k, 2)])
            grid.add(lines)
            mid = (ends[0] + ends[1]) / 2
            ends = [mid, ends[1]] if dgt else [ends[0], mid]
            shade.add(Rectangle(width=W * (ends[1] - ends[0]), height=0.5, stroke_width=0, fill_color=QC.IDEA,
                                fill_opacity=0.35).move_to([x0 + W * (ends[0] + ends[1]) / 2, bar.get_y(), 0]))
            toss_labels.add(MathTex(("H" if dgt else "T"), font_size=30, color=QC.IDEA))
        toss_labels.arrange(RIGHT, buff=0.25).next_to(bar, UP, buff=0.35).align_to(bar, LEFT)
        with self.voiceover(
            "Infinitely many tosses become concrete with one trick: write the tosses as the binary digits of a number "
            "between zero and one. Fair tosses become length on the interval. <bookmark mark='a'/> Somewhere is the "
            "true world, the gold dot. Each toss halves the block that holds it. <bookmark mark='b'/> After six tosses "
            "you know which of sixty-four slivers you are in, and nothing more: that sliver is F six. "
            "<bookmark mark='c'/> Kolmogorov built probability on this picture in 1933, and chapter thirteen reuses "
            "the grid."
        ) as vo:
            self.play(FadeIn(map_), FadeIn(bar), FadeIn(lab0), FadeIn(lab1), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(gold, scale=2))
            for n in range(3):
                self.play(Create(grid[n]), FadeIn(shade[n]), FadeOut(shade[n - 1]) if n else Wait(0.01),
                          FadeIn(toss_labels[n]), run_time=0.8)
            vo.wait_until("b")
            self.play(frame_to(self, shade[2], margin=2.2), run_time=1.6)
            for n in range(3, 6):
                self.play(Create(grid[n]), FadeIn(shade[n]), FadeOut(shade[n - 1]), FadeIn(toss_labels[n]), run_time=0.8)
            self.play(frame_to(self, shade[5], margin=3.0), run_time=1.2)
            self.play(frame_home(self), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(kol, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
