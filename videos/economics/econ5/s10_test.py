from __future__ import annotations

from videos.economics.econ5.common import *  # noqa: F403


class Test(VoiceoverScene):
    def construct(self):
        card(self, 8, r"The test on data", r"How consistent are your choices, and how consistent are people's?",
             "Chapter eight. The test on data.")
        self.score()
        self.random()
        self.people()
        self.america()

    def score(self):
        ch = load("choosers")
        L, P = np.array(load("budgets")["lines"]), np.array(load("budgets")["prices"])
        X = np.array(ch["dara"]["X"])
        C = P @ X.T
        own = np.diag(C)
        n = len(X)
        R0 = (own[:, None] >= C - 1e-9) & ~np.eye(n, dtype=bool)
        bad = {i for pair in ch["dara"]["violations"] for i in pair}
        size = 0.36
        grid = VGroup()
        for i in range(n):
            for j in range(n):
                fill, opacity = GREY_E, 0.35
                if i == j:
                    fill, opacity = BACKGROUND, 0.85
                elif R0[i, j]:
                    fill, opacity = (VIOL if (i in bad and j in bad and R0[j, i]) else BUDGET), 0.85
                sq = Square(size, stroke_color=GREY_D, stroke_width=1, fill_color=fill, fill_opacity=opacity)
                sq.move_to([j * size, -i * size, 0])
                grid.add(sq)
        grid.move_to(LEFT * 3.2 + DOWN * 0.3)
        rl = VGroup(*[label(str(k + 1), font_size=14, color=GREY_B).next_to(grid[k * n], LEFT, buff=0.08)
                      for k in range(n)])
        cl = VGroup(*[label(str(k + 1), font_size=14, color=GREY_B).next_to(grid[k], UP, buff=0.08)
                      for k in range(n)])
        axl = VGroup(label(r"line $i$ (row): \ was choice $j$ (column) affordable?", font_size=19, color=GREY_A)
                     .next_to(grid, UP, buff=0.45))
        steps = VGroup(
            label(r"1. \ for every pair of lines: \\ \hphantom{1. \ }was your choice on one affordable on the other?",
                  font_size=22),
            label(r"2. \ gold: \ yes, so you revealed you preferred \\ \hphantom{2. \ }what you chose", font_size=22,
                  color=BUDGET),
            label(r"3. \ red: \ each of two choices revealed better \\ \hphantom{3. \ }than the other, \ directly or "
                  r"through a chain", font_size=22, color=VIOL),
            label(r"4. \ no red: \ consistent, \ score 1; \ otherwise \\ \hphantom{4. \ }shrink the budgets until the "
                  r"red goes", font_size=22, color=PASS),
            label(r"the course site does all of this as you choose", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = island_tag(r"simulated: Dara's eleven choices, as an example", corner=DR, font_size=13)
        with self.voiceover(
            "Time to score your sheet. Here's how, using Dara's distracted day as the example. "
            "<bookmark mark='a'/> For every pair of lines, ask: was the choice you made on one line affordable on the "
            "other? Your money and that line's prices tell you. <bookmark mark='b'/> If it was, and you chose "
            "something else, you revealed that you preferred what you chose. Those are the gold squares. "
            "<bookmark mark='c'/> A contradiction is two choices each revealed better than the other, directly or "
            "through a chain. Those are red. <bookmark mark='d'/> If there's no red, your choices are consistent "
            "and your score is one. If there is, shrink every budget a little at a time until the red disappears: "
            "the share you had to keep is Afriat's efficiency index. <bookmark mark='e'/> The course site does "
            "this for you as you choose."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(axl))
            vo.wait_until("a")
            self.play(FadeIn(grid, lag_ratio=0.01), FadeIn(rl), FadeIn(cl), FadeIn(steps[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]))
        self.clear_scene()

    def random(self):
        b = load("bronars")
        from explainer.ai.viz import axes

        edges = np.array(b["edges"])
        h = np.array(b["hist"])
        ax = axes([0.4, 1.0], [0, max(h) * 1.15], x_length=6.2, y_length=3.8, xticks=[0.4, 0.6, 0.8, 1.0],
                  yticks=None, xlabel=r"efficiency index of a random chooser, \ on our eleven lines", font_size=18,
                  center=LEFT * 2.7 + DOWN * 0.4)
        a = ax.ax
        bars = VGroup()
        for e0, e1, v in zip(edges[:-1], edges[1:], h):
            if v <= 0:
                continue
            r = Rectangle(width=a.c2p(e1, 0)[0] - a.c2p(e0, 0)[0], height=a.c2p(0, v)[1] - a.c2p(0, 0)[1],
                          stroke_width=0.8, stroke_color=BACKGROUND, fill_color=RANDOM, fill_opacity=0.85)
            r.move_to(a.c2p((e0 + e1) / 2, 0), aligned_edge=DOWN)
            bars.add(r)
        rows = VGroup(
            label(rf"{b['reps']:,} random choosers: \\ a point at random on each line".replace(",", "{,}"),
                  font_size=23),
            label(rf"{100 * b['power']:.1f}\% of them violate GARP", font_size=26, color=VIOL),
            label(rf"their average index: \ {b['ccei_mean']:.2f}; \\ {100 * b['above_95']:.1f}\% score above 0.95",
                  font_size=23, color=GREY_A),
            label(r"so a score near 1 on these lines \\ is evidence, \ not luck", font_size=24, color=PASS),
            label(r"Bronars (1987): \ a test's power \\ against random choice", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.45)
        tag = island_tag(r"simulated: 5,000 random choosers on the Play-it lines".replace(",", "{,}"), corner=DR,
                         font_size=13)
        with self.voiceover(
            "What's a good score? Dara scored above ninety-five percent while choosing at random, so we need a "
            "yardstick. <bookmark mark='a'/> In 1987 Stephen Bronars suggested one: let a computer choose at random "
            f"on the same lines, thousands of times. <bookmark mark='b'/> On our eleven lines, "
            f"{100 * b['power']:.0f} percent of random choosers violate GARP. The lines were chosen to cross a lot, "
            "so that contradictions have room to appear. <bookmark mark='c'/> Their average index is "
            f"{b['ccei_mean']:.2f}, and about one in ten scores above ninety-five percent. "
            "<bookmark mark='d'/> So if your eleven choices are consistent, that's real evidence about you. With "
            "only a few lines, or lines that hardly cross, even random choice would usually pass, and passing would "
            "mean nothing."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(rows[4]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[GrowFromEdge(r, DOWN) for r in bars], lag_ratio=0.05),
                      run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def people(self):
        st = load("studies")
        h = st["harbaugh"]["groups"]
        from explainer.ai.viz import axes

        names = ["second graders", "sixth graders", "undergraduates", "random (bootstrap)"]
        shown = [r"age 7", r"age 11", r"age 21", r"random"]
        ax = axes([0, 4], [0, 10], x_length=4.6, y_length=3.0, xticks=None, yticks=[0, 3, 6, 9],
                  ylabel=r"mean GARP violations, \ of 11", font_size=17, center=LEFT * 4.0 + UP * 0.55)
        a = ax.ax
        cols = [IC, IC, IC, RANDOM]
        bars = VGroup()
        for k, (nm, sh) in enumerate(zip(names, shown)):
            v = h[nm]["violations"]
            r = Rectangle(width=0.7, height=a.c2p(0, v)[1] - a.c2p(0, 0)[1], stroke_width=0, fill_color=cols[k],
                          fill_opacity=0.85).move_to(a.c2p(k + 0.5, 0), aligned_edge=DOWN)
            bars.add(VGroup(r, label(f"{v:.1f}", font_size=17).next_to(r, UP, buff=0.05),
                            label(sh, font_size=16, color=GREY_B).next_to(a.c2p(k + 0.5, 0), DOWN, buff=0.1)))
        ckms = st["ckms2014"]
        rows = VGroup(
            label(r"Harbaugh, Krause and Berry (2001): \ chips and juice, \ 11 choice sets", font_size=21,
                  color=IC),
            label(r"none at all: \ 26\% of 7-year-olds, \ 62\% of 11-year-olds, \ 65\% of students; \ random 2\%",
                  font_size=19, color=GREY_A),
            label(rf"Choi, Fisman, Gale and Kariv (2007): \ {st['choi2007']['subjects']} Berkeley students, "
                  rf"{st['choi2007']['budgets']} budgets: \ average index {st['choi2007']['mean_ccei']:.3f}",
                  font_size=21, color=E.ACCENT),
            label(rf"Choi, Kariv, M\"uller and Silverman (2014): \ {ckms['subjects']:,} Dutch adults, "
                  rf"{ckms['budgets']} budgets: \ {ckms['mean_ccei']:.3f}".replace(",", "{,}"), font_size=21,
                  color=E.ACCENT),
            label(r"less consistent: \ the poorer, \ the less educated, \ the old \ (by 3.3, 2.6 and 5.1 points)",
                  font_size=19, color=GREY_A),
            label(r"one standard deviation more consistent: \ 15--19\% more household wealth", font_size=22,
                  color=PASS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        rows[0].next_to(ax, RIGHT, buff=0.6).align_to(ax, UP)
        rows[1].next_to(rows[0], DOWN, buff=0.18).align_to(rows[0], LEFT)
        rest = VGroup(*rows[2:]).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.7)
        rest.to_edge(LEFT, buff=0.6)
        tag = published_tag(r"Harbaugh et al., AER 91(5) (2001), tables 1--2; Choi et al., AER 97(5) (2007) and "
                            r"AER 104(6) (2014)", corner=DR, font_size=12)
        with self.voiceover(
            "Now real people. <bookmark mark='a'/> In 2001 William Harbaugh, Kate Krause and Timothy Berry gave "
            "children in Eugene, Oregon, eleven choices between bags of potato chips and boxes of juice. "
            "Seven-year-olds made about four contradictions on average; eleven-year-olds about two; college "
            "students no fewer than the eleven-year-olds. Random choice, drawn the way children chose, would make "
            "more than eight. "
            "<bookmark mark='b'/> A quarter of the seven-year-olds, and nearly two thirds of the older children and "
            "students, made none at all. Rational choice, in this sense, develops early, and quickly. "
            "<bookmark mark='c'/> With fifty budgets each, Berkeley students in 2007 averaged an efficiency of "
            f"{st['choi2007']['mean_ccei']:.3f}. <bookmark mark='d'/> When two of the same researchers, with two "
            f"colleagues, ran the experiment online with {ckms['subjects']:,} Dutch adults, the average was "
            f"{ckms['mean_ccei']:.2f}. "
            "<bookmark mark='e'/> The poorer, the less educated and the old were somewhat less consistent. "
            "<bookmark mark='f'/> The striking finding: people who were more consistent in the experiment had more "
            "wealth, fifteen to nineteen percent more per standard deviation, even comparing people with the same "
            "income, education and age. Consistency in a laboratory game seems to measure something that matters "
            "outside it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            for mk, r in zip("cdef", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def america(self):
        am = load("america")
        years = list(am["years"])
        shares = np.array(am["shares"])
        from explainer.ai.viz import axes

        ax = axes([1929, 2025], [0, 50000], x_length=5.6, y_length=3.6, xticks=[1929, 1960, 1990, 2025],
                  yticks=[0, 20000, 40000], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v / 1000:.0f}k",
                  ylabel=r"real spending per head, 2017 \$", font_size=17, center=LEFT * 3.3 + DOWN * 0.2)
        a = ax.ax
        line = VMobject(stroke_color=E.ACCENT, stroke_width=4).set_points_as_corners(
            [a.c2p(y, v) for y, v in zip(years, am["real_total"])])
        w = am["windows"]
        rows = VGroup(
            label(r"America as one consumer: \ 97 years, \ 15 kinds of spending", font_size=24, color=E.ACCENT),
            label(rf"GARP violations: \ {am['violations']}", font_size=26, color=PASS),
            label(rf"a random chooser on the same budgets: \ violates {100 * am['power_random']:.0f}\% of the time",
                  font_size=21, color=GREY_A),
            label(rf"one who copies another year's shares: \ {100 * am['power_shuffle']:.0f}\%", font_size=21,
                  color=GREY_A),
            label(rf"but within 1929--40, 1970--85 or 2000--25, \ copying another year's \\ shares never fails "
                  rf"({100 * w['1929-1940']['shuffle']:.0f}\%): \ incomes grow, \ budgets rarely cross", font_size=21,
                  color=VIOL),
            label(r"passing is informative only where the test had power", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"BEA, PCE by type of product, 1929--2025 (FRED); \ GARP and power computed", corner=DR,
                       font_size=13)
        with self.voiceover(
            "Can a whole country pass? <bookmark mark='a'/> Treat American spending as one consumer's choices: "
            "ninety-seven years, from 1929 to 2025, fifteen kinds of spending, each with its price index. "
            "<bookmark mark='b'/> No violations of GARP. Not one. <bookmark mark='c'/> Is that impressive? A random "
            "chooser on the same budgets would fail every time. <bookmark mark='d'/> Even someone who simply copied "
            f"another year's spending shares would fail {100 * am['power_shuffle']:.0f} percent of the time. "
            "<bookmark mark='e'/> But look within a decade or two, and the test goes blind: copying another year's "
            "shares never fails, because incomes grow so steadily that this year's budget almost always buys more "
            "of everything than last year's. Budgets that never cross can't contradict each other. "
            "<bookmark mark='f'/> The lesson travels well beyond economics: a test passed is evidence only if the "
            "test could have been failed."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(line, run_time=2.0))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
