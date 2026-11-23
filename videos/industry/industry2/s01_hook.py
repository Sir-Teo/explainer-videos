from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry2.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.table()
        self.title()

    def table(self):
        n = 22
        rng = np.random.default_rng(1919)
        cells = VGroup()
        size = 0.2
        for i in range(n):
            for j in range(n):
                v = rng.random() ** 4 if i != j else 0.6 + 0.4 * rng.random()
                cells.add(Square(size, fill_color=I.ACCENT, fill_opacity=0.06 + 0.85 * v, stroke_color=BACKGROUND,
                                 stroke_width=0.8).move_to(np.array([(j - n / 2) * size, (n / 2 - i) * size, 0])))
        cells.move_to(LEFT * 3.2 + DOWN * 0.2)
        place = T("Harvard  ·  1936", 26, I.DIM).to_edge(UP, buff=0.55)
        rows_l = T("each row: who an industry sells to", 20, I.TEXT).next_to(cells, RIGHT, buff=0.6).shift(UP * 1.2)
        cols_l = T("each column: what it buys", 20, I.TEXT).next_to(rows_l, DOWN, buff=0.35, aligned_edge=LEFT)
        ex = VGroup(T("coal  →  steel mills", 20, I.ACCENT), T("steel  →  car makers", 20, I.ACCENT),
                    T("cars  →  farms", 20, I.ACCENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(
            cols_l, DOWN, buff=0.5, aligned_edge=LEFT)
        nobel = T(f"Nobel prize, {get('leontief.nobel'):.0f}", 22, I.DIM).next_to(ex, DOWN, buff=0.5, aligned_edge=LEFT)
        hl_r = SurroundingRectangle(VGroup(*cells[5 * n:6 * n]), color=I.TEXT, buff=0.02, stroke_width=2)
        hl_c = SurroundingRectangle(VGroup(*[cells[i * n + 8] for i in range(n)]), color=I.CHANNEL, buff=0.02,
                                    stroke_width=2)
        src = source("Leontief (1936), Review of Economic Statistics; the grid is a sketch, not his figures")
        with self.voiceover(
            "In 1936 a young economist at Harvard, Wassily Leontief, published a table of the American economy of "
            "1919. <bookmark mark='a'/> He split it into 44 sectors, and for each one he wrote down how much it had "
            "bought from every other: <bookmark mark='b'/> coal from the mines to the steel mills, steel to the car "
            "makers, cars to the farms. <bookmark mark='c'/> Read along a row and you see who an industry sells to. "
            "<bookmark mark='d'/> Read down a column and you see what it buys. <bookmark mark='e'/> One page, and on "
            "it every industry's customers and suppliers. He won the Nobel prize for it in 1973, and statistical "
            "offices around the world now publish tables like his every year."
        ) as vo:
            self.play(FadeIn(place), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.002), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(ex, shift=RIGHT * 0.1))
            vo.wait_until("c")
            self.play(Create(hl_r), FadeIn(rows_l))
            vo.wait_until("d")
            self.play(Create(hl_c), FadeIn(cols_l))
            vo.wait_until("e")
            self.play(FadeIn(nobel))
        self.clear_scene()

    def title(self):
        card_ = part_title(PART, ASK)
        with self.voiceover(
            "Industry, Built. Part two: the economy on one page. How big is each industry, and compared with what? "
            "Part one followed a single phone. This part steps back to the whole economy: how big each industry is, "
            "measured three ways, how they feed one another, and where the profit sits."
        ):
            self.play(FadeIn(card_[0]), run_time=0.8)
            self.play(FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.2)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
