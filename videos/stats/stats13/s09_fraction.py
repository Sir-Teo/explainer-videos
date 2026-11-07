from __future__ import annotations

import numpy as np

from videos.stats.stats13.common import *  # noqa: F403


class Fraction(VoiceoverScene):
    def construct(self):
        self.card()
        self.explosion()
        self.half_cube()
        self.aliasing()
        self.estimates()
        self.resolution()
        self.saturated()
        self.plackett()

    def card(self):
        card = chapter_card(8, r"Fractional factorials", r"Half the runs, \ and knowing exactly what you gave up", part=PART)
        with self.voiceover("Chapter eight. Fractional factorials."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def explosion(self):
        ks = list(range(2, 11))
        A = axes([1.5, 10.5], [0, 10.5], x_length=7.0, y_length=4.4, xlabel=r"factors, \ $k$", ylabel=r"$\log_2$ runs",
                 xticks=ks, yticks=[0, 2, 4, 6, 8, 10], center=[-2.4, 0.0, 0])
        ax = A.ax
        full = VGroup(*[Dot(ax.c2p(k, k), radius=0.08, color=RES) for k in ks])
        fl = VMobject(stroke_color=RES, stroke_width=3).set_points_as_corners([ax.c2p(k, k) for k in ks])
        need = [k + 1 for k in ks]
        nd = VGroup(*[Dot(ax.c2p(k, np.log2(n)), radius=0.08, color=HIT) for k, n in zip(ks, need)])
        nl = VMobject(stroke_color=HIT, stroke_width=3).set_points_as_corners([ax.c2p(k, np.log2(n)) for k, n in zip(ks, need)])
        rows = fit_rows(VGroup(
            label(r"a full $2^k$ factorial: \ $2^k$ runs", font_size=24, color=RES),
            MathTex(r"2^{7} = 128,\quad 2^{10} = 1024", font_size=30, color=RES),
            label(r"main effects alone need only $k + 1$ numbers", font_size=24, color=HIT),
            label(r"most of a big factorial estimates high-order interactions", font_size=24),
            label(r"effect sparsity: \ few effects are large; \ high-order ones rarely matter", font_size=24, color=OBS),
        ), 5.0, 0.32, [4.3, 0.2, 0])
        with self.voiceover(
            "Factorials have a cost. <bookmark mark='a'/> A full factorial in k factors at two levels needs two to the k runs. "
            "<bookmark mark='b'/> Seven factors need a hundred and twenty-eight; ten need over a thousand. "
            "<bookmark mark='c'/> Yet if what you want is the main effect of each factor, you need only k plus one numbers. "
            "<bookmark mark='d'/> Most of a large factorial goes to estimating four-way, five-way and six-way interactions. "
            "<bookmark mark='e'/> And experience says those are almost always negligible: a few effects are large, and "
            "high-order interactions rarely matter. That's the principle of effect sparsity, and it licenses running only a "
            "fraction of the factorial."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(fl), FadeIn(full), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(nl), FadeIn(nd), FadeIn(rows[2]))
            for k, m_ in enumerate("de"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 3]))
        self.clear_scene()

    def cube(self, center, X, lit, scale=1.0):
        ex, ey, ez = np.array([1.5, 0]) * scale, np.array([0, 1.4]) * scale, np.array([0.8, 0.58]) * scale

        def P(x):
            v = np.array(center[:2]) + 0.5 * (x[0] * ex + x[1] * ey + x[2] * ez)
            return np.array([v[0], v[1], 0])
        corners = [np.array([a, b, c]) for c in (-1, 1) for b in (-1, 1) for a in (-1, 1)]
        edges = VGroup()
        for i in range(8):
            for j in range(i + 1, 8):
                if np.sum(corners[i] != corners[j]) == 1:
                    edges.add(Line(P(corners[i]), P(corners[j]), color=GREY_C, stroke_width=2))
        dots = VGroup(*[Dot(P(x), radius=0.12, color=OBS if lit(x) else GREY_D) for x in corners])
        return VGroup(edges, dots), corners

    def half_cube(self):
        lo, _ = self.cube([-3.6, 0.3, 0], None, lambda x: x[0] * x[1] * x[2] == -1)
        hi, _ = self.cube([2.0, 0.3, 0], None, lambda x: x[0] * x[1] * x[2] == 1)
        l1 = label(r"$D = -$", font_size=28, color=GREY_B).next_to(lo, DOWN, buff=0.4)
        l2 = label(r"$D = +$", font_size=28, color=GREY_B).next_to(hi, DOWN, buff=0.4)
        axl = label(r"axes: \ A across, \ B up, \ C into the page", font_size=22, color=GREY_A).to_edge(UP, buff=0.5)
        foot = fit_rows(VGroup(
            label(r"$2^4 = 16$ runs: \ two cubes, \ one for each level of D", font_size=24),
            label(r"run only the 8 lit corners: \ those with $D = ABC$", font_size=24, color=OBS),
            label(r"each cube gets 4 corners, \ never two on the same edge", font_size=24),
            label(r"a $2^{4-1}$ fractional factorial", font_size=26, color=OBS),
        ), 12.0, 0.25, [0, -2.6, 0])
        intro = label('Choose half the factorial corners using a defining relation', font_size=36)
        with self.voiceover(
            "Take four factors, A, B, C and D. <bookmark mark='a'/> The full factorial is sixteen runs: draw it as two cubes, "
            "one for each level of D. <bookmark mark='b'/> Now run only half: the eight corners where the level of D equals "
            "the product of the levels of A, B and C. <bookmark mark='c'/> Each cube gets four corners, alternate ones, never "
            "two joined by an edge, so every factor is still balanced: four runs high, four low. <bookmark mark='d'/> This is "
            "a two to the four minus one fractional factorial, introduced by David Finney at Rothamsted in 1945. What do we "
            "lose?"
        ) as vo:
            self.play(FadeIn(intro))
            self.play(FadeIn(axl))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(Create(lo[0]), Create(hi[0]), FadeIn(l1), FadeIn(l2), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(lo[1], scale=1.5), FadeIn(hi[1], scale=1.5), FadeIn(foot[1]))
            for k, m_ in enumerate("cd"):
                vo.wait_until(m_)
                self.play(FadeIn(foot[k + 2]))
        self.clear_scene()

    def aliasing(self):
        rows = [
            cmath(r"D", r"=", r"ABC\quad\Rightarrow\quad I = ABCD", font_size=34),
            cmath(r"A \cdot I", r"=", r"A \cdot ABCD = A^2BCD = BCD", font_size=34),
            cmath(r"\hat\ell_A", r"=", r"\text{effect}_A + \text{effect}_{BCD}", font_size=34),
            cmath(r"AB", r"=", r"CD,\quad AC = BD,\quad AD = BC", font_size=34),
        ]
        rows[2][2].set_color(OBS)
        rows[3][2].set_color(RES)
        whys = [why(r"the defining relation: \ the column $ABCD$ is all $+$"), why(r"letters multiply; \ squares vanish ($x^2 = 1$)"),
                why(r"aliases: \ the same column, \ so the same estimate"), why(r"two-factor interactions alias each other")]
        intro = label('A fractional design estimates aliased combinations', font_size=36)
        with self.voiceover(
            "What we lose is aliasing. <bookmark mark='a'/> In the eight runs we kept, the column for D equals the column for "
            "A times B times C. Multiply both sides by D: the column A B C D is plus one in every run. That's the defining "
            "relation, I equals A B C D. <bookmark mark='b'/> Multiply any effect by it, with the rule that a squared letter "
            "vanishes, because plus or minus one squared is one: A times A B C D is B C D. <bookmark mark='c'/> So in these eight "
            "runs, the column for A is identical to the column for the three-factor interaction B C D, and what we estimate is "
            "their sum. They're aliases. <bookmark mark='d'/> The two-factor interactions pair up too: A B with C D, A C with "
            "B D, A D with B C. The half fraction can't tell the members of a pair apart. It can only tell us their sum."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.8, buff=0.65, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def estimates(self):
        d = load("fraction")
        full, half, true = d["full"], d["half"], d["true"]
        keys = [("A", "BCD"), ("B", "ACD"), ("C", "ABD"), ("D", "ABC"), ("AB", "CD"), ("AC", "BD"), ("AD", "BC")]
        rows = [[r"effect", r"alias", r"truth", r"16 runs", r"8 runs"]]
        for a, b in keys:
            tv = true.get(a, 0.0) + true.get(b, 0.0)
            rows.append([a, rf"+ {b}", rf"{tv:.1f}", rf"{full[a]:.2f}", rf"{half[a]:.2f}"])
        tab = table_rows(rows, font_size=24, col_buff=0.8, row_buff=0.2, colors=[GREY_B] + [None] * 7).move_to([-1.6, 0.0, 0])
        for i in range(1, 8):
            tab[i][4].set_color(OBS)
            tab[i][2].set_color(EXACT)
        notes = fit_rows(VGroup(
            label(r"truth: \ A 4, \ C 2, \ D 3, \ AB 1.5, \ all else 0", font_size=22, color=EXACT),
            label(r"with sparsity, \ the 8 runs find the same factors", font_size=22, color=OBS),
            label(r"but AB = 1.68 could be AB or CD: \ the data cannot say", font_size=22, color=RES),
            label(r"complementary fraction: reverse D alone to split the pairs", font_size=22, color=GREY_A),
        ), 4.2, 0.3, [4.7, 0.0, 0])
        tag = simulated_tag(r"simulated, \ noise SD 1", corner=DR)
        intro = label('Compare the full design with its half fraction', font_size=36)
        with self.voiceover(
            "Does it matter? <bookmark mark='a'/> Here's a simulated process in four factors: A truly adds four, C two, D "
            "three, and A and B interact, one and a half; everything else is zero. The table shows the full sixteen-run "
            "estimates and the eight-run half fraction's. <bookmark mark='b'/> The half fraction finds the same important "
            "factors, A, C and D, with estimates close to the full design's, at half the cost. <bookmark mark='c'/> But its A "
            "B row, one point six eight, is really A B plus C D, and the eight runs can't say which. Here it's A B, because "
            "we built it. A real experimenter would need knowledge, or more runs. <bookmark mark='d'/> The standard remedy is "
            "to run the complementary fraction with D changed to minus A B C. Reversing D alone splits these pairs; reversing all four factors would keep the same even-word fraction."
        ) as vo:
            self.play(FadeIn(intro))
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(tab, lag_ratio=0.05), FadeIn(notes[0]), run_time=2.0)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(notes[k + 1]))
        self.clear_scene()

    def resolution(self):
        rows = [
            cmath(r"\text{resolution III}", r":", r"\text{main effects aliased with 2-factor interactions}", font_size=30),
            cmath(r"\text{resolution IV}", r":", r"\text{main effects clear; \ 2fi's aliased with each other}", font_size=30),
            cmath(r"\text{resolution V}", r":", r"\text{main effects and 2fi's all clear}", font_size=30),
            cmath(r"2^{4-1},\ I = ABCD", r":", r"\text{resolution IV: \ the shortest word has 4 letters}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"screening only"), why(r"the common workhorse"), why(r"nearly as good as the full factorial"),
                why(r"Box \& Hunter (1961)")]
        intro = label('Resolution describes which effects share a column', font_size=36)
        with self.voiceover(
            "George Box and Stuart Hunter classified fractions by their resolution. <bookmark mark='a'/> In a resolution three "
            "design, main effects are aliased with two-factor interactions: good only for a first screening. "
            "<bookmark mark='b'/> In resolution four, main effects are clear of two-factor interactions, but those are "
            "aliased with each other. <bookmark mark='c'/> In resolution five, main effects and two-factor interactions are all "
            "clear of each other. <bookmark mark='d'/> The resolution is the length of the shortest word in the defining "
            "relation. Ours, A B C D, has four letters: resolution four, which is exactly what the table showed."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.2, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def sign_grid(self, M, center, cell=0.42, names=None, font_size=20):
        M = np.asarray(M)
        r, c = M.shape
        g = VGroup()
        for i in range(r):
            for j in range(c):
                box = Square(side_length=cell, stroke_width=0.8, stroke_color=GREY_D,
                             fill_color=OBS if M[i, j] > 0 else "#1B2733", fill_opacity=0.85)
                box.move_to([center[0] + (j - (c - 1) / 2) * cell, center[1] + ((r - 1) / 2 - i) * cell, 0])
                g.add(box)
        heads = VGroup()
        if names:
            for j, nm in enumerate(names):
                heads.add(label(nm, font_size=font_size, color=GREY_B).next_to(g[j], UP, buff=0.1))
        return VGroup(g, heads)

    def saturated(self):
        d = load("fraction")
        sat = np.asarray(d["sat"])
        grid = self.sign_grid(sat, [-3.2, 0.0, 0], cell=0.5, names=list("ABCDEFG"))
        rows = fit_rows(VGroup(
            label(r"seven factors in eight runs: \ $2^{7-4}$", font_size=24),
            MathTex(r"D = AB,\ E = AC,\ F = BC,\ G = ABC", font_size=28),
            label(r"every column balanced, \ every pair of columns orthogonal", font_size=24, color=OBS),
            label(r"resolution III: \ a saturated screening design", font_size=24, color=RES),
            label(r"gold = high, \ dark = low", font_size=20, color=GREY_A),
        ), 5.4, 0.34, [3.6, 0.0, 0])
        intro = label('A saturated design leaves no residual error estimate', font_size=36)
        with self.voiceover(
            "Push it to the limit. <bookmark mark='a'/> Seven factors in eight runs: a two to the seven minus four design. "
            "<bookmark mark='b'/> Start with the full factorial in A, B and C, and give the four extra factors the interaction "
            "columns: D is A B, E is A C, F is B C, and G is A B C. <bookmark mark='c'/> Every column is balanced, four high and "
            "four low, and every pair of columns is orthogonal, so the seven column contrasts are uncorrelated under equal-variance uncorrelated errors, and independent under Gaussian errors, each "
            "from all eight runs. <bookmark mark='d'/> It's resolution three, saturated: no degrees of freedom left for error, "
            "and every main effect is aliased with interactions. It's a screening design: it tells you which of many factors "
            "deserve a proper experiment."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(grid[1]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in grid[0]], lag_ratio=0.01), FadeIn(rows[1]), FadeIn(rows[4]), run_time=2.0)
            for k, m_ in enumerate("cd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def plackett(self):
        d = load("fraction")
        pb = np.asarray(d["pb"])
        grid = self.sign_grid(pb, [-3.0, -0.2, 0], cell=0.36, names=[str(k + 1) for k in range(11)], font_size=16)
        hc = history_card(1946, r"Robin Plackett \ and \ J. Peter Burman, \ \emph{Biometrika}",
                          r"``The design of optimum multifactorial experiments'': \ wartime work for the Ministry of Supply; \ "
                          r"up to $N - 1$ factors in $N$ runs, \ for many $N$ divisible by 4", color=S.ALT, width=5.6, font_size=20).move_to([3.7, 1.2, 0])
        rows = fit_rows(VGroup(
            MathTex(r"X^\top X = 12\,I_{11}", font_size=32, color=OBS),
            label(r"11 factors, \ 12 runs: \ each row a shift of the first", font_size=22),
            label(r"no defining relation: \ interactions spread thinly over all columns", font_size=22, color=GREY_A),
        ), 5.4, 0.3, [3.7, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Fractional factorials have two to the p runs. In 1946 Robin Plackett and Peter Burman, working "
            "on wartime problems for Britain's Ministry of Supply, tabulated orthogonal designs for many run counts divisible by "
            "four. Here's their twelve-run design for up to eleven factors: each row is the first row shifted by one place, "
            "plus a final row of all lows. <bookmark mark='b'/> Its columns are exactly orthogonal: X transpose X is twelve "
            "times the identity, so every main effect is estimated with the full precision of all twelve runs. "
            "<bookmark mark='c'/> Unlike a regular fraction, it has no simple aliasing: each two-factor interaction is spread "
            "in small pieces over many columns. Plackett–Burman designs are still standard for screening in chemistry and "
            "manufacturing."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(grid[1]), LaggedStart(*[FadeIn(b_) for b_ in grid[0]], lag_ratio=0.005), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
