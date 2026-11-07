from __future__ import annotations

import numpy as np

from explainer.stats.board import load_all
from videos.stats.stats13.common import *  # noqa: F403

NAMES = [r"control", r"A", r"B", r"C", r"D"]


class Contrasts(VoiceoverScene):
    def construct(self):
        self.card()
        self.contrasts()
        self.split_bar()
        self.five()
        self.fwer()
        self.multipliers()
        self.tukey_grid()
        self.dunnett()
        self.advice()

    def card(self):
        card = chapter_card(4, r"Contrasts", r"Asking sharper questions, \ and asking many honestly", part=PART)
        with self.voiceover("Chapter four. Contrasts, and many comparisons."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def contrasts(self):
        d = load("anova")
        cs = d["contrasts"]
        c1, c2, c3 = cs["fertilized vs none"], cs["N vs P, NPK"], cs["P vs NPK"]
        rows = [
            cmath(r"\psi", r"=", r"\textstyle\sum_i c_i\,\mu_i,\qquad \sum_i c_i = 0", font_size=34),
            cmath(r"\text{SS}_\psi", r"=", r"\frac{(\sum_i c_i\,\bar y_i)^2}{\sum_i c_i^2/n},\qquad \text{1 df}", font_size=32),
            cmath(r"(-3, 1, 1, 1)", r":", rf"\text{{fertilized vs none:}}\ \hat\psi = {c1['est']:.2f},\ F = {c1['F']:.1f},\ p = {c1['p']:.4f}", font_size=28),
            cmath(r"(0, -2, 1, 1)", r":", rf"\text{{N vs the P's:}}\ \hat\psi = {c2['est']:.2f},\ F = {c2['F']:.2f}", font_size=28),
            cmath(r"(0, 0, -1, 1)", r":", rf"\text{{P vs NPK:}}\ \hat\psi = {c3['est']:.2f},\ F = {c3['F']:.2f}", font_size=28),
            cmath(r"\textstyle\sum_i c_i c_i' = 0", r"\Rightarrow", rf"{c1['ss']:.2f} + {c2['ss']:.2f} + {c3['ss']:.2f} = {d['anova']['ssb']:.2f} = \text{{SSB}}", font_size=30),
        ]
        rows[5][2].set_color(OBS)
        whys = [why(r"a contrast: \ weights summing to zero"), why(r"its own sum of squares"),
                why(r"the question that matters most"), why(r"N versus the average of P and NPK"), why(r"P versus NPK: both N and K change"),
                why(r"orthogonal contrasts split SSB exactly")]
        intro = label('Choose contrasts from the scientific questions', font_size=36)
        with self.voiceover(
            "The F-test says the four fertilizers differ somehow. It doesn't say how. <bookmark mark='a'/> For that, ask "
            "sharper questions: contrasts, weighted sums of the group means whose weights add to zero. <bookmark mark='b'/> "
            "Each contrast has its own sum of squares, with one degree of freedom; its t and F references assume independent Gaussian, equal-variance errors. <bookmark mark='c'/> First: do fertilizers "
            "help at all? Weights minus three, one, one, one compare the control with the average of the rest. The "
            "estimate is eight point six, in units of the sum, and F is twelve, p point zero zero two. <bookmark mark='d'/> "
            "Second: among the fertilized, is nitrogen alone different from the two with phosphate? Barely: F is point three "
            "four. <bookmark mark='e'/> Third: compare phosphate alone with NPK, which changes both nitrogen and potash. F two point seven six, not clear. "
            "<bookmark mark='f'/> These three contrasts are orthogonal, their weight vectors are perpendicular, so their "
            "sums of squares add up exactly to the between-groups sum of squares. Pythagoras again: three perpendicular "
            "questions, chosen before the data, split the treatment variation into orthogonal pieces; under Gaussian errors their numerator sums of squares are independent."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.6, buff=0.55, edge=6.9)
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def split_bar(self):
        d = load("anova")
        cs = d["contrasts"]
        ss = [cs["fertilized vs none"]["ss"], cs["N vs P, NPK"]["ss"], cs["P vs NPK"]["ss"]]
        total = d["anova"]["sst"]
        W = 11.0
        cols = [OBS, S.ALT, S.PRIOR]
        y0 = 0.9
        whole = Rectangle(width=W, height=0.7, stroke_color=GREY_B, stroke_width=2).move_to([0, y0, 0])
        x = -W / 2
        pieces = VGroup()
        names = [r"fertilized vs none", r"N vs P's", r"P vs NPK"]
        labs = VGroup()
        for s_, c, nm in zip(ss, cols, names):
            w = W * s_ / total
            r = Rectangle(width=w, height=0.7, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to([x + w / 2, y0, 0])
            pieces.add(r)
            x += w
        resid = Rectangle(width=W * d["anova"]["ssw"] / total, height=0.7, stroke_width=0, fill_color=RES, fill_opacity=0.5)
        resid.move_to([x + resid.width / 2, y0, 0])
        for r, nm, c, s_ in zip(pieces, names, cols, ss):
            labs.add(label(rf"{nm}: \ {s_:.1f}", font_size=20, color=c))
        labs.add(label(rf"residual: \ {d['anova']['ssw']:.1f}", font_size=20, color=RES))
        labs.arrange(RIGHT, buff=0.5).next_to(whole, DOWN, buff=0.35)
        head = label(rf"the total sum of squares, \ {total:.1f}, \ cut into four perpendicular pieces", font_size=26).next_to(whole, UP, buff=0.5)
        foot = fit_rows(VGroup(
            label(r"$k - 1$ orthogonal contrasts always exist, \ and always split SSB this way", font_size=24),
            label(r"choose them before the experiment, \ from the questions it was built to answer", font_size=24, color=OBS),
            label(r"chosen after looking at the means, \ the same arithmetic tells you much less", font_size=24, color=RES),
        ), 12.0, 0.28, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here's the whole sum of squares as a bar, a hundred and seven point eight. <bookmark mark='b'/> "
            "The fertilized-versus-none contrast takes thirty-seven of it, the other two contrasts one and eight and a half, "
            "and the residual the remaining sixty-one. <bookmark mark='c'/> With k groups there are always k minus one "
            "orthogonal contrasts, and many ways to choose them. <bookmark mark='d'/> The honest way is to choose them before "
            "the experiment, from the questions it was built to answer. <bookmark mark='e'/> Choose them afterwards, because "
            "the means looked interesting, and the same arithmetic means much less, which is the problem of the rest of this "
            "chapter."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(whole), FadeIn(head))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(p_, LEFT) for p_ in pieces], lag_ratio=0.4), GrowFromEdge(resid, LEFT),
                      FadeIn(labs, lag_ratio=0.2), run_time=2.5)
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(foot[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def five(self):
        d = load("contrasts")
        g = np.random.Generator(np.random.PCG64(1953))
        groups = [g.normal(50 + e, 2.0, 6) for e in d["eff"]]
        A = axes([-0.6, 4.6], [44, 58], x_length=7.0, y_length=4.4, xlabel=r"", ylabel=r"yield", xticks=[], yticks=[46, 50, 54, 58],
                 center=[-2.6, 0.0, 0])
        ax = A.ax
        dots = VGroup()
        for k, v in enumerate(groups):
            for j, val in enumerate(np.sort(v)):
                dots.add(Dot(ax.c2p(k + (j - 2.5) * 0.07, val), radius=0.07, color=TRT[k]))
        names = VGroup(*[label(NAMES[k], font_size=22, color=TRT[k]).move_to(ax.c2p(k, 44) + DOWN * 0.3) for k in range(5)])
        bars = VGroup(*[Line(ax.c2p(k - 0.3, m), ax.c2p(k + 0.3, m), color=TRT[k], stroke_width=5) for k, m in enumerate(d["means"])])
        rows = fit_rows(VGroup(
            label(r"a control and four new fertilizers, \ six plots each", font_size=24),
            label(r"which ones differ from which? \ $\binom52 = 10$ pairs", font_size=24, color=OBS),
            label(r"C vs D: \ pooled-ANOVA $t$-test $p = 0.009$, \ ``significant''", font_size=24, color=RES),
            label(r"but C vs D is the gap we noticed because it looked big", font_size=24),
            label(r"ten chances to find something", font_size=24, color=RES),
        ), 5.0, 0.34, [4.3, 0.2, 0])
        tag = simulated_tag(r"simulated: \ true gains 0, 1, 4, 4.5, 2", corner=DR)
        with self.voiceover(
            "Now the common situation. <bookmark mark='a'/> A control and four new fertilizers, A to D, six plots each. "
            "<bookmark mark='b'/> The experimenter wants to know which differ from which: ten pairs. <bookmark mark='c'/> Run "
            "the t-test using the common ANOVA error on a pair noticed after looking, C against D, and you get p about point zero zero nine: significant! "
            "<bookmark mark='d'/> But C against D was chosen because it looked big. <bookmark mark='e'/> With ten pairs to "
            "look at, something may look big. How often, if nothing is going on at all?"
        ) as vo:
            self.play(FadeIn(A), FadeIn(names), FadeIn(tag), LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in dots], lag_ratio=0.02),
                      run_time=2.0)
            self.play(Create(bars))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1], shift=RIGHT * 0.2))
        self.clear_scene()

    def fwer(self):
        rows_b = {r.method: r for r in load_all(upto=13) if r.part == 13}
        raw = rows_b[r"pairwise $t$-tests, \ unadjusted"].achieved
        tk = rows_b[r"Tukey's HSD"].achieved
        rows = [
            cmath(r"\text{FWER}", r"=", r"P(\text{at least one false rejection})", font_size=34),
            cmath(r"\text{10 independent tests}", r":", r"1 - 0.95^{10} = 0.40", font_size=32),
            cmath(r"\text{10 pairwise } t\text{-tests, 5 groups}", r":", rf"{raw:.3f}\ \ \text{{(simulated, 10{{,}}000 nulls)}}", font_size=30),
            cmath(r"\text{Tukey's HSD}", r":", rf"{tk:.4f}", font_size=32),
        ]
        rows[2][2].set_color(RES)
        rows[3][2].set_color(HIT)
        whys = [why(r"the family-wise error rate"), why(r"an independence benchmark; \ the pairs share data"),
                why(r"a 5\% test that rejects 27\% of the time"), why(r"the promise kept for the whole family")]
        with self.voiceover(
            "<bookmark mark='a'/> The relevant error rate is the family-wise error rate: the chance of at least one false "
            "rejection among all the comparisons. <bookmark mark='b'/> Ten independent five percent tests would make at least "
            "one false rejection forty percent of the time. The pairwise tests aren't independent, they share groups, "
            "<bookmark mark='c'/> but simulating ten thousand experiments with no real differences, five groups of six, at "
            "least one unadjusted t-test comes out significant twenty-six and a half percent of the time. Promise five percent, "
            "deliver twenty-seven. <bookmark mark='d'/> Tukey's method, which we'll build next, holds the whole family to four "
            "point nine five percent. Both rows use independent normal, equal-variance groups and the common pooled error on the Coverage Board."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.4, x=0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def multipliers(self):
        d = load("contrasts")
        mults = [(r"$t$, \ one pair", d["t_crit"], S.LIK), (r"Dunnett, \ 4 vs control", d["dunnett_mult"], S.ALT),
                 (r"Tukey, \ all 10 pairs", d["tukey_mult"], OBS), (r"Bonferroni, \ 10 pairs", d["bonf"], S.PRIOR),
                 (r"Scheff\'e, \ every contrast", d["scheffe"], RES)]
        A = axes([0, 3.6], [-0.5, 4.5], x_length=6.6, y_length=4.2, xlabel=r"multiplier of $\sqrt{2\,\text{MSE}/n}$", ylabel=r"",
                 xticks=[0, 1, 2, 3], yticks=[], center=[0.9, 0.3, 0])
        ax = A.ax
        bars, labs, vals = VGroup(), VGroup(), VGroup()
        for i, (nm, v, c) in enumerate(mults):
            yy = 4 - i
            b = Rectangle(width=ax.c2p(v, 0)[0] - ax.c2p(0, 0)[0], height=0.5, stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to(ax.c2p(0, yy), aligned_edge=LEFT)
            bars.add(b)
            labs.add(label(nm, font_size=22, color=c).next_to(ax.c2p(0, yy), LEFT, buff=0.25))
            vals.add(label(rf"{v:.2f}", font_size=22, color=c).next_to(b, RIGHT, buff=0.15))
        foot = fit_rows(VGroup(
            label(r"the wider the family you protect, \ the wider every interval must be", font_size=24, color=OBS),
            label(r"25 error df; \ Dunnett's multiplier by simulation", font_size=20, color=GREY_A),
        ), 12.4, 0.2, [0, -2.9, 0])
        with self.voiceover(
            "In these Gaussian, equal-variance comparisons, simultaneous protection widens the yardstick. An interval for a difference of two means is "
            "the difference plus or minus a multiplier times its standard error. <bookmark mark='a'/> For one pair chosen in "
            "advance, the multiplier is Student's t, two point oh six. <bookmark mark='b'/> To compare each of four "
            "fertilizers with the control, Charles Dunnett's 1955 method uses about two point six. <bookmark mark='c'/> To "
            "cover all ten pairs, John Tukey's uses two point nine four. <bookmark mark='d'/> The blunt Bonferroni correction "
            "for ten tests, Part 10, is a little wider, three point oh eight. <bookmark mark='e'/> And Henry Scheffé's 1953 "
            "method covers every possible contrast, even ones invented after seeing the data, with three point three two. "
            "<bookmark mark='f'/> The wider the family of questions you protect, the wider every interval must be. That's the "
            "price of looking."
        ) as vo:
            self.play(FadeIn(A))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(GrowFromEdge(bars[k], LEFT), FadeIn(labs[k]), FadeIn(vals[k]))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def tukey_grid(self):
        d = load("contrasts")
        rows = [
            cmath(r"|\bar y_i - \bar y_j|", r">", r"q_{k,\,N-k}\,\sqrt{\text{MSE}/n}", font_size=34),
            cmath(r"q_{5,\,25}", r"=", rf"{d['q']:.2f},\quad \sqrt{{{d['mse']:.2f}/6}} = {np.sqrt(d['mse'] / 6):.3f}", font_size=32),
            cmath(r"\text{HSD}", r"=", rf"{d['hsd']:.2f}", font_size=34),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"Tukey (1953): \ the studentized range"), why(r"the range of 5 normal means, \ over its SE"),
                why(r"``honestly significant difference''")]
        n = 5
        cell = 0.72
        grid = VGroup()
        for i in range(n):
            for j in range(n):
                sq = Square(side_length=cell, stroke_width=1, stroke_color=GREY_D, fill_opacity=0.0)
                sq.move_to([1.9 + j * cell, -0.45 - i * cell, 0])
                grid.add(sq)
        fills, texts = VGroup(), VGroup()
        for p in d["pairs"]:
            i, j = p["i"], p["j"]
            sq = grid[i * n + j]
            col = HIT if p["sig"] else (RES if p["p_raw"] < 0.05 else GREY_D)
            fills.add(sq.copy().set_fill(col, opacity=0.55))
            texts.add(label(rf"{abs(p['diff']):.1f}", font_size=21).move_to(sq))
        heads = VGroup(*[label(NAMES[j] if j else r"ctl", font_size=18, color=TRT[j]).next_to(grid[j], UP, buff=0.1) for j in range(n)])
        sides = VGroup(*[label(NAMES[i] if i else r"ctl", font_size=18, color=TRT[i]).next_to(grid[i * n], LEFT, buff=0.1) for i in range(n)])
        key = VGroup(label(r"beyond HSD", font_size=20, color=HIT), label(r"unadjusted only", font_size=20, color=RES),
                     label(r"neither", font_size=20, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(grid, LEFT, buff=1.1)
        with self.voiceover(
            "Tukey's honestly significant difference. <bookmark mark='a'/> Declare two means different if their gap exceeds "
            "q times the standard error of one mean, where q is a quantile of the studentized range: the range of k normal "
            "means divided by its estimated standard error. Since the largest gap is the range, controlling the range controls "
            "every pair at once. <bookmark mark='b'/> For five groups and twenty-five degrees of freedom, q is four point one "
            "five, <bookmark mark='c'/> so the honestly significant difference is three point five bushels. <bookmark mark='d'/> "
            "In the grid of all ten gaps, two exceed it: C against the control, five bushels, and C against A. One more "
            "pair, C against D, passes an unadjusted t-test and fails Tukey's: red. It might be real. But this "
            "experiment can't honestly claim them."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.8, buff=0.4, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
            vo.wait_until("d")
            self.play(Create(grid), FadeIn(heads), FadeIn(sides))
            self.play(LaggedStart(*[FadeIn(f_) for f_ in fills], lag_ratio=0.1), FadeIn(texts), FadeIn(key), run_time=2.0)
        self.clear_scene()

    def dunnett(self):
        d = load("contrasts")
        pv = d["dunnett_p"]
        hc = history_card(1955, r"Charles Dunnett, \ Lederle Laboratories", r"``A multiple comparison procedure for comparing several "
                          r"treatments with a control'': \ the family is only the $k - 1$ comparisons with the control, \ so the "
                          r"multiplier is smaller than Tukey's", color=S.ALT, width=10.4, font_size=22).move_to([0, 1.5, 0])
        tab = table_rows([[r"vs control", r"A", r"B", r"C", r"D"],
                          [r"Dunnett $p$"] + [rf"{v:.3f}" for v in pv]], font_size=26, col_buff=0.7, row_buff=0.3,
                         colors=[GREY_B, None]).move_to([0, -0.9, 0])
        for j, v in enumerate(pv):
            tab[1][j + 1].set_color(HIT if v < 0.05 else GREY_A)
        foot = label(r"only C beats the control, \ honestly: \ the method matches the question", font_size=24, color=OBS).move_to([0, -2.4, 0])
        with self.voiceover(
            "If the only question is which new fertilizers beat the control, <bookmark mark='a'/> the family is smaller: four "
            "comparisons, not ten. Charles Dunnett's 1955 method, devised while he worked for a pharmaceutical company, "
            "uses that smaller family, and its narrower multiplier. <bookmark mark='b'/> Here only C beats the control, with "
            "an adjusted p of point zero zero one; A, B and D don't. <bookmark mark='c'/> The method matches the question, "
            "and the question should be written down before the harvest."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def advice(self):
        rows = [
            cmath(r"\text{a few planned contrasts}", r":", r"\text{individual }\alpha\text{; family: Bonferroni/Holm}", font_size=30),
            cmath(r"\text{all pairs}", r":", r"\text{Tukey's HSD}", font_size=32),
            cmath(r"\text{each vs a control}", r":", r"\text{Dunnett}", font_size=32),
            cmath(r"\text{anything, chosen after looking}", r":", r"\text{Scheff\'e}", font_size=30),
            cmath(r"\text{thousands of tests}", r":", r"\text{the false discovery rate (Part 33)}", font_size=30),
        ]
        whys = [why(r"the experiment's own questions"), why(r"the studentized range"), why(r"the smaller family"),
                why(r"the price of snooping"), why(r"a different promise: \ Benjamini \& Hochberg (1995)")]
        with self.voiceover(
            "So, a short guide. <bookmark mark='a'/> For a few contrasts planned in advance, each usual-level test gives an individual guarantee; "
            "use Bonferroni or Holm for a family guarantee. <bookmark mark='b'/> For all pairs, Tukey. <bookmark mark='c'/> For each "
            "treatment against a control, Dunnett. <bookmark mark='d'/> For anything at all, including contrasts suggested by "
            "the data, Scheffé, and pay for it. <bookmark mark='e'/> And when there are thousands of tests, as in genomics, "
            "controlling the chance of even one false rejection is too strict. Benjamini and Hochberg's false discovery rate "
            "makes a different promise, and Part 33 builds it."
        ) as vo:
            step = ladder(self, rows, whys, keep=5, top=2.7, x=0.6, buff=0.55, edge=6.9)
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
