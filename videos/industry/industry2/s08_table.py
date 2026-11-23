from __future__ import annotations

from videos.industry.industry2.common import *  # noqa: F403


class Table(VoiceoverScene):
    def construct(self):
        card(self, 8, "Leontief's table, 2023", "What does each industry buy from every other?",
             "Chapter eight. Leontief's table, as the statisticians publish it today.", lit=("dollar", "make"))
        self.grid()

    def grid(self):
        io = R["io"]
        A = np.array(io["A"])
        names = io["names"]
        n = len(names)
        s = 0.33
        cells = VGroup()
        for i in range(n):
            for j in range(n):
                v = min(A[i, j] / 0.32, 1.0)
                cells.add(Square(s, fill_color=I.ACCENT, fill_opacity=0.05 + 0.9 * v ** 0.6, stroke_color=BACKGROUND,
                                 stroke_width=1).move_to(np.array([(j - n / 2) * s, (n / 2 - i) * s, 0])))
        cells.move_to(RIGHT * 0.9 + DOWN * 0.75)
        rl = VGroup(*[T(nm, 13, I.DIM).next_to(cells[i * n], LEFT, buff=0.12) for i, nm in enumerate(names)])
        COLS = {"Manufacturing": "Factories", "Information": "Info", "Finance and real estate": "Finance, RE",
                "Business services": "Business svcs", "Education and health": "Educ., health",
                "Leisure and hotels": "Leisure", "Other services": "Other svcs"}
        cl = VGroup(*[T(COLS.get(nm, nm), 13, I.DIM).rotate(PI / 2.3).next_to(cells[j], UP, buff=0.08)
                      for j, nm in enumerate(names)])
        m = names.index("Manufacturing")
        col = SurroundingRectangle(VGroup(*[cells[i * n + m] for i in range(n)]), color=I.CHANNEL, buff=0.02,
                                   stroke_width=2.5)
        row = SurroundingRectangle(VGroup(*cells[m * n:(m + 1) * n]), color=I.TEXT, buff=0.02, stroke_width=2.5)
        cnote = VGroup(TB("The manufacturing column", 20, I.CHANNEL),
                       T(f"per dollar of its output: {100 * A[m, m]:.0f}¢ from other factories,", 17, I.TEXT),
                       T(f"{100 * A[names.index('Wholesale'), m]:.0f}¢ wholesale, {100 * A[names.index('Mining'), m]:.0f}¢ "
                         f"mining, {100 * A[names.index('Farms'), m]:.0f}¢ farms ...", 17, I.TEXT),
                       T(f"{100 * A[:, m].sum():.0f}¢ in all; the rest is its value added", 17, I.TEXT)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.06).to_corner(UL, buff=0.35)
        rnote = VGroup(TB("The manufacturing row", 20, I.TEXT),
                       T(f"per dollar a builder produces, {100 * A[m, names.index('Construction')]:.0f}¢ of", 17, I.TEXT),
                       T("manufactured goods: steel, cement, glass, wiring", 17, I.TEXT)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.06).to_corner(DL, buff=0.35)
        tot = VGroup(T("All sales, 2023:", 18, I.DIM), TB(f"${io['output_total']:.1f}tn", 22, I.COST),
                     T("Value added (GDP):", 18, I.DIM), TB(f"${io['va_total']:.1f}tn", 22, I.MONEY)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).next_to(cells, RIGHT, buff=0.5)
        src = source("BEA, input-output use table, 2023, fifteen sectors (after redefinitions)", corner=DR, size=14)
        with self.voiceover(
            "Here is Leontief's table as the Bureau of Economic Analysis publishes it now, for 2023, squeezed into "
            "fifteen sectors. <bookmark mark='a'/> Each square is how much the industry at the top buys from the "
            "industry on the left, for every dollar of what it produces; the brighter the square, the more it "
            "buys. The bright diagonal is industries buying from themselves: factories from other factories, banks "
            "from other banks. <bookmark mark='b'/> Read down a column to see an industry's recipe. For every dollar "
            "of goods American manufacturers produce, they buy 32 cents from other manufacturers, eight from "
            "wholesalers, six from mines, five from farms, and so on: 62 cents in all. The other 38 cents is their "
            "value added. <bookmark mark='c'/> Read along a row to see an industry's customers. For every dollar a "
            "builder produces, 22 cents goes on manufactured goods. <bookmark mark='d'/> And add up every industry's "
            "output, and you get 48 trillion dollars for 2023, against a GDP of 28 trillion: the gap is all the "
            "buying and selling between businesses, counted once in this table and never in GDP."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.004), FadeIn(rl), FadeIn(cl), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(col), FadeIn(cnote))
            vo.wait_until("c")
            self.play(Create(row), FadeIn(rnote))
            vo.wait_until("d")
            self.play(FadeIn(tot, shift=UP * 0.1))
        self.clear_scene()
