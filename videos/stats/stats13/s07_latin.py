from __future__ import annotations

import numpy as np

from videos.stats.stats13.common import *  # noqa: F403


class Latin(VoiceoverScene):
    def construct(self):
        self.card()
        self.square()
        self.table()
        self.random_square()
        self.euler()
        self.crossover()
        self.carryover()

    def card(self):
        card = chapter_card(6, r"Latin squares", r"Blocking in two directions at once", lit=(1935,), part=PART)
        with self.voiceover("Chapter six. Latin squares, and crossover trials."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def square(self):
        d = load("latin")
        sq = np.asarray(d["square"])
        fert = np.asarray(d["fert"])
        fp = field_from(fert, cell=0.9, center=[-3.4, 0.2, 0], lo=49, hi=62)
        tags = fp.tags(sq, names="ABCDE", colors=TRT, font_size=28)
        ar1 = Arrow(fp.get_corner(DL) + DOWN * 0.35, fp.get_corner(DR) + DOWN * 0.35, buff=0, color=GREY_B, stroke_width=3)
        ar2 = Arrow(fp.get_corner(UL) + LEFT * 0.35, fp.get_corner(DL) + LEFT * 0.35, buff=0, color=GREY_B, stroke_width=3)
        rowbox = fp.outline(2, 2, 0, 4, color=BLOCK)
        colbox = fp.outline(0, 4, 3, 3, color=S.ALT)
        rows = fit_rows(VGroup(
            label(r"fertility rises to the east \ and to the south", font_size=24),
            label(r"row blocks miss the columns, \ and vice versa", font_size=24),
            label(r"a Latin square: \ each variety once per row", font_size=24, color=OBS),
            label(r"and once per column", font_size=24, color=OBS),
            label(r"each row a complete block; \ so is each column", font_size=24, color=BLOCK),
            label(r"rows and columns both cancel", font_size=24, color=OBS),
        ), 5.0, 0.36, [4.1, 0.2, 0])
        tag = simulated_tag(r"simulated field, \ graded both ways", corner=DR)
        with self.voiceover(
            "Sometimes the soil varies in two directions. <bookmark mark='a'/> This field grows richer to the east, and also to "
            "the south. <bookmark mark='b'/> We have five varieties and twenty-five plots. Blocks made of rows would leave "
            "the east-west slope in the error; blocks made of columns would leave the north-south one. <bookmark mark='c'/> "
            "The answer is a Latin square: arrange the five letters so that each appears exactly once in every row and once "
            "in every column, like a Sudoku. <bookmark mark='d'/> Then every row is a complete block, and so is every column. "
            "<bookmark mark='e'/> Compare variety A with variety B, and both sets of soil effects cancel, because each variety "
            "met every row and every column exactly once."
        ) as vo:
            self.play(FadeIn(fp, lag_ratio=0.02), GrowArrow(ar1), GrowArrow(ar2), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(tags, lag_ratio=0.04), FadeIn(rows[2]), FadeIn(rows[3]), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(rowbox), Create(colbox), FadeIn(rows[4]))
            vo.wait_until("e")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def table(self):
        d = load("latin")
        la, ow = d["latin"], d["oneway"]
        t1 = table_rows([
            [r"Latin square", r"df", r"SS", r"MS", r"$F$", r"$p$"],
            [r"rows", r"4", rf"{la['ss_rows']:.1f}", rf"{la['ss_rows'] / 4:.1f}", r"", r""],
            [r"columns", r"4", rf"{la['ss_cols']:.1f}", rf"{la['ss_cols'] / 4:.1f}", r"", r""],
            [r"varieties", r"4", rf"{la['ss_treat']:.1f}", rf"{la['ss_treat'] / 4:.2f}", rf"{la['F']:.1f}", r"$5\times10^{-5}$"],
            [r"residual", r"12", rf"{la['sse']:.1f}", rf"{la['mse']:.2f}", r"", r""],
        ], font_size=26, col_buff=0.55, row_buff=0.26, colors=[GREY_B, BLOCK, S.ALT, OBS, RES]).move_to([-2.5, 0.6, 0])
        rows = fit_rows(VGroup(
            label(r"one-way, \ ignoring rows and columns:", font_size=22),
            MathTex(rf"F = {ow['F']:.2f},\quad p = {ow['p']:.2f}", font_size=28, color=RES),
            label(r"4,000 repetitions, \ power to detect the varieties:", font_size=22),
            MathTex(rf"\text{{Latin}}\ {100 * d['power_latin']:.0f}\%\quad\text{{vs}}\quad\text{{CRD}}\ {100 * d['power_crd']:.0f}\%", font_size=28, color=OBS),
            label(r"the price: \ $(n-1)(n-2) = 12$ error df, \ not 20", font_size=22, color=GREY_A),
        ), 4.4, 0.3, [4.6, 0.4, 0])
        foot = label(r"$\text{SST} = \text{SS}_{\text{rows}} + \text{SS}_{\text{cols}} + \text{SS}_{\text{var}} + \text{SSE}$: \ four perpendicular pieces, \ 24 = 4 + 4 + 4 + 12",
                     font_size=24).move_to([0, -2.9, 0])
        if foot.width > 12.6:
            foot.width = 12.6
        with self.voiceover(
            "<bookmark mark='a'/> The analysis of variance now has a row for rows, a row for columns, and a row for varieties. "
            "Assuming an additive model with independent normal equal-variance errors, rows and columns take two hundred of the sum of squares, leaving a residual of just six point three on twelve "
            "degrees of freedom. The varieties' F is seventeen point eight. <bookmark mark='b'/> Ignore the square, and analyse "
            "the same twenty-five numbers one way: F is point eight eight, p point four nine. <bookmark mark='c'/> Over four "
            "thousand repetitions, the Latin square detects the varieties ninety-six percent of the time, the completely "
            "randomized design twenty percent. <bookmark mark='d'/> The price is degrees of freedom: twelve for error instead "
            "of twenty, which is especially costly for very small squares. <bookmark mark='e'/> And underneath, Pythagoras once more: "
            "four perpendicular pieces."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(t1, lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def grid(self, sq, center, cell=0.55, font_size=22):
        n = len(sq)
        g = VGroup()
        for r in range(n):
            for c in range(n):
                k = int(sq[r][c])
                box = Square(side_length=cell, stroke_width=1, stroke_color=GREY_D, fill_color=TRT[k], fill_opacity=0.35)
                box.move_to([center[0] + (c - (n - 1) / 2) * cell, center[1] + ((n - 1) / 2 - r) * cell, 0])
                g.add(VGroup(box, label("ABCDE"[k], font_size=font_size, color=TRT[k]).move_to(box)))
        return g

    def random_square(self):
        d = load("latin")
        vik = np.asarray(d["vik"])
        g1 = self.grid(vik, [-4.0, 0.6, 0])
        g = np.random.Generator(np.random.PCG64(1935))
        base = (np.arange(5)[:, None] + np.arange(5)[None, :]) % 5
        g2 = self.grid(base, [0.0, 0.6, 0])
        rp, cp, lp = g.permutation(5), g.permutation(5), g.permutation(5)
        sq3 = lp[base[rp][:, cp]]
        g3 = self.grid(sq3, [4.0, 0.6, 0])
        l1 = label(r"Knut Vik: \ a knight's move", font_size=22, color=GREY_A).next_to(g1, DOWN, buff=0.25)
        l2 = label(r"the cyclic square", font_size=22, color=GREY_A).next_to(g2, DOWN, buff=0.25)
        l3 = label(r"rows, \ columns, \ letters shuffled", font_size=22, color=OBS).next_to(g3, DOWN, buff=0.25)
        rows = fit_rows(VGroup(
            label(r"a systematic square can line up with a pattern in the soil, \ like a diagonal drainage ditch", font_size=24, color=RES),
            label(rf"randomize the layout; in total: \ there are {d['n_squares_5']:,} Latin squares of order 5", font_size=24, color=OBS),
            label(r"row/column/letter shuffles sample one permutation class, \ not all squares uniformly", font_size=22, color=GREY_A),
        ), 12.6, 0.26, [0, -2.5, 0])
        with self.voiceover(
            "Which Latin square? <bookmark mark='a'/> Norwegian agronomists liked the Knut Vik square, where each letter moves "
            "like a knight in chess, spreading the varieties evenly over the field. <bookmark mark='b'/> Or the cyclic square, "
            "each row the previous one shifted by one place. <bookmark mark='c'/> Fisher objected to both. A systematic square "
            "can line up with a systematic pattern in the soil, a diagonal ditch, say, and then the error estimate is wrong, "
            "too large or too small, with no way to tell. <bookmark mark='d'/> Randomize the layout. In total, "
            "there are a hundred and sixty-one thousand, two hundred and eighty Latin squares of order five. <bookmark mark='e'/> "
            "In practice, take one square and shuffle its rows, its columns and its letters at random, the recipe in Fisher and "
            "Yates's statistical tables. This samples the chosen square's permutation class, not uniformly all Latin squares. The exact F reference also needs the additive Gaussian model."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(g1, lag_ratio=0.04), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(g2, lag_ratio=0.04), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(TransformFromCopy(g2, g3), FadeIn(l3), FadeIn(rows[2]), run_time=1.8)
        self.clear_scene()

    def euler(self):
        hc = history_card(1782, r"Leonhard Euler, \ the thirty-six officers", r"six regiments, \ six ranks: \ can 36 officers stand in "
                          r"a $6\times6$ square with every regiment and every rank once in each row and column? \ Two orthogonal Latin "
                          r"squares of order 6. \ Euler conjectured there are none, \ for 6, 10, 14, \ldots", color=S.PRIOR, width=10.8,
                          font_size=22).move_to([0, 1.5, 0])
        rows = fit_rows(VGroup(
            label(r"1900: \ Gaston Tarry checks every case: \ none of order 6, \ as Euler thought", font_size=24),
            label(r"1959: \ Bose, \ Shrikhande \& Parker build them for 10, 14, \ldots: \ Euler was wrong for every other case", font_size=24, color=OBS),
            label(r"in experiments: \ Graeco-Latin squares block three ways at once", font_size=24, color=GREY_A),
        ), 12.4, 0.3, [0, -1.7, 0])
        with self.voiceover(
            "Latin squares are also a famous piece of mathematics. <bookmark mark='a'/> In 1782 Leonhard Euler asked whether "
            "thirty-six officers, from six regiments and of six ranks, could stand in a six-by-six square with every regiment "
            "and every rank appearing once in each row and each column. That needs two Latin squares that fit together, "
            "called orthogonal. Euler conjectured it was impossible for six, and for ten, fourteen and every size two more than "
            "a multiple of four. <bookmark mark='b'/> In 1900 Gaston Tarry checked every case and confirmed that six is "
            "impossible. <bookmark mark='c'/> But in 1959 Raj Chandra Bose, Sharadchandra Shrikhande and Ernest Parker "
            "constructed them for ten and every larger case. Bose and Shrikhande were statisticians, led to the problem by "
            "the design of experiments. <bookmark mark='d'/> In a field, a Graeco-Latin square blocks three ways at once."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def crossover(self):
        head = label(r"a crossover trial: \ each patient is a block, \ each period a column", font_size=28).to_edge(UP, buff=0.5)
        cell = 0.7
        g = VGroup()
        seqs = ["AB", "BA", "AB", "BA", "BA", "AB"]
        for i, s_ in enumerate(seqs):
            for j, ch in enumerate(s_):
                k = "AB".index(ch)
                box = Rectangle(width=1.6, height=cell * 0.85, stroke_width=1, stroke_color=GREY_D, fill_color=TRT[k], fill_opacity=0.4)
                box.move_to([-3.6 + j * 2.6, 1.6 - i * cell, 0])
                g.add(VGroup(box, label(ch, font_size=24, color=TRT[k]).move_to(box)))
        wash = VGroup(*[label(r"washout", font_size=16, color=GREY_B).move_to([-2.3, 1.6 - i * cell, 0]) for i in range(6)])
        ph = VGroup(label(r"period 1", font_size=22, color=GREY_B).move_to([-3.6, 2.35, 0]),
                    label(r"period 2", font_size=22, color=GREY_B).move_to([-1.0, 2.35, 0]))
        pl = VGroup(*[label(rf"patient {i + 1}", font_size=20, color=GREY_B).move_to([-5.6, 1.6 - i * cell, 0]) for i in range(6)])
        rows = fit_rows(VGroup(
            label(r"both treatments, \ in a random order", font_size=24),
            label(r"compared within a person:", font_size=24, color=OBS),
            label(r"person-to-person variation cancels", font_size=24, color=OBS),
            label(r"half AB, \ half BA: \ periods cancel", font_size=24, color=BLOCK),
            label(r"a $2\times2$ Latin square per pair", font_size=22, color=GREY_A),
        ), 5.0, 0.34, [4.3, 0.2, 0])
        with self.voiceover(
            "The same idea runs medical trials. <bookmark mark='a'/> In a crossover trial, each patient receives both "
            "treatments, one in each period, separated by a washout so the first wears off, and the order is randomized. "
            "<bookmark mark='b'/> The comparison is within each patient, so the enormous variation from person to person, in "
            "age, weight and severity, cancels. Each patient is a block. <bookmark mark='c'/> Half the patients get A then B, "
            "half B then A, so that a period effect, the disease improving on its own, say, also cancels. "
            "<bookmark mark='d'/> Each pair of patients with opposite orders is a two-by-two Latin square: rows are patients, "
            "columns are periods."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ph), FadeIn(pl))
            vo.wait_until("a")
            self.play(FadeIn(g, lag_ratio=0.06), FadeIn(wash), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            for k, m_ in enumerate("cd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 3], shift=RIGHT * 0.2))
        self.clear_scene()

    def carryover(self):
        rows = [
            cmath(r"y_{ij}", r"=", r"\mu + \pi_j + \tau_{d(i,j)} + s_i + \varepsilon_{ij}", font_size=34),
            cmath(r"\hat\tau_B - \hat\tau_A", r"=", r"\tfrac12\big[(\bar y_{2} - \bar y_{1})_{AB} - (\bar y_{2} - \bar y_{1})_{BA}\big]", font_size=32),
            cmath(r"\text{carryover}", r":", r"\lambda_{d(i,1)}\ \text{in period 2 breaks the cancellation}", font_size=30),
            cmath(r"\text{remedy}", r":", r"\text{washout; \ or more periods (Williams 1949)}", font_size=30),
        ]
        rows[1][2].set_color(OBS)
        rows[2][2].set_color(RES)
        whys = [why(r"period $\pi_j$, \ treatment $\tau$, \ subject $s_i$"), why(r"subjects and periods both cancel"),
                why(r"the first drug's effect lingers"), why(r"designs balanced for carryover")]
        with self.voiceover(
            "<bookmark mark='a'/> The crossover model: a period effect, a treatment effect, a subject effect, and noise. "
            "<bookmark mark='b'/> The treatment difference is estimated by half the difference between the two sequence "
            "groups' within-patient changes; the subjects and the periods both cancel. <bookmark mark='c'/> The danger is "
            "carryover: if the first drug's effect lingers into the second period, the cancellation fails, and in a "
            "two-period design the carryover can't be separated from the treatment effect. <bookmark mark='d'/> The remedies "
            "are a long washout, or designs with more periods, like Evan Williams's 1949 squares, which are balanced so that "
            "every treatment follows every other equally often. Crossovers are standard for chronic conditions and for "
            "bioequivalence studies of generic drugs; they're useless when a treatment cures."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.8, buff=0.65, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
