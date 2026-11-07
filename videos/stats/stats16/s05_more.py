from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats16.common import *  # noqa: F403


class MoreRanks(VoiceoverScene):
    def construct(self):
        self.card()
        self.kruskal()
        self.kw_stat()
        self.friedman()
        self.spearman()
        self.kendall()
        self.outlier()

    def card(self):
        card = chapter_card(4, r"More rank methods", r"Many groups, \ blocks, \ and correlation", part=PART)
        with self.voiceover("Chapter four. More rank methods."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def kruskal(self):
        d = load("more")
        gs = [np.asarray(g) for g in d["groups"]]
        A = axes([0, 185], [0, 3.6], x_length=9.4, y_length=3.2, xlabel=r"income, \ thousands", xticks=[0, 50, 100, 150],
                 center=[0.6, 1.0, 0])
        ax = A.ax
        cols = [TRT[0], TRT[1], TRT[2]]
        strips = VGroup()
        names = VGroup()
        for k, g in enumerate(gs):
            y = 2.9 - k * 1.05
            strips.add(VGroup(*[Dot(ax.c2p(v, y), radius=0.085, color=cols[k], fill_opacity=0.85) for v in g]))
            names.add(label(rf"region {[0, 3, 7][k]}", font_size=20, color=cols[k]).next_to(ax.c2p(0, y), LEFT, buff=0.2))
        rows = fit_rows(VGroup(
            label(r"ten adults from each of three regions of the World", font_size=24),
            label(r"one income of 177 thousand: \ it inflates region 3's variance", font_size=22, color=RES),
            MathTex(rf"\text{{one-way ANOVA (Part 13)}}:\ F = {d['F']:.2f},\ \ p = {d['f_p']:.2f}", font_size=28),
        ), 12.0, 0.3, [0, -1.9, 0])
        tag = simulated_tag(r"the World: \ 30 adults", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> Ranks extend to more than two groups. Here are ten incomes from each of three regions of the "
            "World. <bookmark mark='b'/> Incomes are skewed, and one in region three is a hundred and seventy-seven thousand, "
            "which inflates that group's variance and the ANOVA's error term. <bookmark mark='c'/> Part 13's one-way analysis "
            "of variance gives F equals point three six, p equals point seven oh. What would a test that ignores the sizes say?"
        ) as vo:
            self.play(FadeIn(A), FadeIn(names), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in strips], lag_ratio=0.3), FadeIn(rows[0]))
            vo.wait_until("b")
            out = [dd for dd in strips[1] if ax.p2c(dd.get_center())[0] > 150]
            self.play(*[Circumscribe(o, color=RES, shape=Circle) for o in out], FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def kw_stat(self):
        d = load("more")
        gs = [np.asarray(g) for g in d["groups"]]
        r = stats.rankdata(np.concatenate(gs))
        rb = [r[10 * k:10 * k + 10].mean() for k in range(3)]
        rows = [
            cmath(r"\text{rank all } N = 30", r":", r"\bar R_k = \text{mean rank in group } k", font_size=30),
            cmath(r"H", r"=", r"\frac{12}{N(N+1)} \sum_k n_k \big(\bar R_k - \tfrac{N+1}{2}\big)^2", font_size=30),
            cmath(r"\ ", r"=", rf"{d['H']:.2f},\ \ \bar R = {rb[0]:.1f},\ {rb[1]:.1f},\ {rb[2]:.1f}", font_size=30),
            cmath(r"H \overset{H_0}{\approx} \chi^2_{2}", r":", rf"p = {d['kw_p']:.2f}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"the 177 becomes rank 30, \ no more"), why(r"Kruskal \& Wallis (1952): \ ANOVA on ranks"),
                why(r"expected mean rank: \ 15.5 in each"), why(r"exact by permutation, \ if wanted")]
        with self.voiceover(
            "<bookmark mark='a'/> Rank all thirty incomes together. The hundred and seventy-seven thousand becomes rank thirty, "
            "no more extreme than any other top value. <bookmark mark='b'/> William Kruskal and Allen Wallis, in 1952, did a "
            "one-way analysis of variance on the ranks: the statistic H measures how far each group's mean rank strays from "
            "the overall mean rank, N plus one over two. <bookmark mark='c'/> Here H is one point five three; the mean ranks are "
            "fourteen point three, thirteen point nine and eighteen point three, around the fifteen and a half expected. "
            "<bookmark mark='d'/> Under the null H is approximately chi-squared with two degrees of freedom, so p equals point "
            "four seven, or exactly, by permuting the ranks. With two groups, Kruskal–Wallis is the Wilcoxon–Mann–Whitney test."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def friedman(self):
        tab = table_rows([
            [r"block", r"A", r"B", r"C", r"D"],
            [r"1", r"2", r"1", r"4", r"3"],
            [r"2", r"1", r"2", r"4", r"3"],
            [r"3", r"2", r"1", r"3", r"4"],
            [r"4", r"1", r"3", r"4", r"2"],
            [r"5", r"1", r"2", r"3", r"4"],
            [r"rank sum", r"7", r"9", r"18", r"16"],
        ], font_size=26, colors=[GREY_B, None, None, None, None, None, OBS]).move_to([-3.4, 0.2, 0])
        Rj = np.array([7, 9, 18, 16])
        b, k = 5, 4
        Q = 12 / (b * k * (k + 1)) * np.sum(Rj ** 2) - 3 * b * (k + 1)
        pq = stats.chi2(k - 1).sf(Q)
        rows = fit_rows(VGroup(
            label(r"Part 13's blocks: \ rank \emph{within} each block", font_size=24),
            label(r"block effects vanish: \ only the order inside counts", font_size=22),
            MathTex(r"Q = \frac{12}{bk(k+1)} \sum_j R_j^2 - 3b(k+1)", font_size=28),
            MathTex(rf"Q = {Q:.2f},\ \ p \approx {pq:.3f}\ (\chi^2_3)", font_size=28, color=OBS),
            label(r"Friedman (1937), \ the economist", font_size=22, color=GREY_A),
        ), 5.6, 0.36, [3.6, 0.2, 0])
        tag = label(r"illustrative ranks", font_size=18, color=GREY_B).to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> For Part 13's randomized blocks there's a rank test too. Rank the treatments within each block, "
            "here four treatments in five blocks, <bookmark mark='b'/> so whatever makes one block better than another drops "
            "out: only the order inside a block counts. <bookmark mark='c'/> Milton Friedman, the economist, proposed the "
            "statistic in 1937, as a young statistician: it compares the treatments' rank sums with what chance would give. "
            "<bookmark mark='d'/> For these ranks Q is ten point two. The chi-squared approximation gives p about point oh two, but five blocks is small: exact within-block permutations are preferable under independent exchangeable blocks. "
            "<bookmark mark='e'/> With two treatments it ranks outcomes like a sign test, but its chi-squared p-value is only an approximation to the exact sign-test tail."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r_) for r_ in tab[1:6]], lag_ratio=0.2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[6]), FadeIn(rows[2]), FadeIn(rows[4]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(Indicate(tab[6], color=OBS))
        self.clear_scene()

    def spearman(self):
        d = load("more")
        L, G = np.asarray(museum.LAW_LSAT, float), np.asarray(museum.LAW_GPA, float)
        rl, rg = stats.rankdata(L), stats.rankdata(G)
        A = axes([530, 680], [2.6, 3.6], x_length=5.0, y_length=3.6, xlabel=r"LSAT", ylabel=r"GPA", xticks=[550, 600, 650],
                 yticks=[2.8, 3.2, 3.6], center=[-3.6, 0.6, 0])
        B = axes([0, 16], [0, 16], x_length=3.8, y_length=3.6, xlabel=r"rank of LSAT", ylabel=r"rank of GPA", xticks=[1, 5, 10, 15],
                 yticks=[1, 5, 10, 15], center=[1.4, 0.6, 0])
        d1 = scatter(A.ax, L, G, radius=0.08)
        d2 = scatter(B.ax, rl, rg, color=RANK, radius=0.08)
        rows = fit_rows(VGroup(
            MathTex(r"r_S = \text{corr}\big(\text{rank}(x), \text{rank}(y)\big)", font_size=26),
            MathTex(rf"\text{{Pearson}}\ r = {d['pearson']:.3f}", font_size=28),
            MathTex(rf"\text{{Spearman}}\ r_S = {d['spearman']:.3f}", font_size=28, color=RANK),
            label(r"unchanged by any strictly increasing transformation", font_size=20, color=GREY_A),
        ), 3.6, 0.36, [5.2, 0.6, 0])
        foot = label(r"Spearman (1904), \ the psychologist of general intelligence", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "<bookmark mark='a'/> Ranks measure association too. Take the fifteen law schools <bookmark mark='b'/> and replace "
            "each LSAT and each GPA by its rank among the fifteen. <bookmark mark='c'/> Charles Spearman's correlation, from "
            "1904, is Pearson's correlation computed on the ranks. <bookmark mark='d'/> Pearson's r is point seven seven six; "
            "<bookmark mark='e'/> Spearman's is point seven nine six. <bookmark mark='f'/> Because ranks don't change when you "
            "take logs, square roots, or any strictly increasing transformation, neither does Spearman's correlation. It measures how "
            "monotone the relationship is, not how straight."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(d1))
            vo.wait_until("b")
            self.play(FadeIn(B), TransformFromCopy(d1, d2), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), FadeIn(foot))
            for k, m_ in enumerate("def"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def kendall(self):
        d = load("more")
        L, G = np.asarray(museum.LAW_LSAT, float), np.asarray(museum.LAW_GPA, float)
        A = axes([530, 680], [2.6, 3.6], x_length=6.4, y_length=4.4, xlabel=r"LSAT", ylabel=r"GPA", xticks=[550, 600, 650],
                 yticks=[2.8, 3.2, 3.6], center=[-2.8, 0.2, 0])
        ax = A.ax
        dots = scatter(ax, L, G, radius=0.08)
        iu = list(zip(*np.triu_indices(15, 1)))
        g = np.random.Generator(np.random.PCG64(2))
        pick = [iu[i] for i in g.choice(len(iu), 14, replace=False)]
        segs = VGroup()
        for i, j in pick:
            conc = (L[i] - L[j]) * (G[i] - G[j]) > 0
            segs.add(Line(ax.c2p(L[i], G[i]), ax.c2p(L[j], G[j]), color=HIT if conc else MISS, stroke_width=2.5, stroke_opacity=0.8))
        rows = fit_rows(VGroup(
            label(r"every pair of schools: \ do LSAT and GPA agree in order?", font_size=22),
            label(r"concordant: \ 86 \quad discordant: \ 19 \quad of 105", font_size=22),
            MathTex(r"\tau = \frac{C - D}{\binom{n}{2}} = \frac{86 - 19}{105}", font_size=28),
            MathTex(rf"= {d['kendall']:.3f}", font_size=30, color=RANK),
            label(r"$\frac{1 + \tau}{2}$: \ the chance a random pair agrees, \ 0.82", font_size=22, color=GREY_A),
        ), 5.0, 0.36, [4.2, 0.2, 0])
        with self.voiceover(
            "Maurice Kendall's tau, from 1938, counts pairs, like Mann and Whitney. <bookmark mark='a'/> Take every pair of "
            "schools and ask whether LSAT and GPA put them in the same order. Green pairs agree, concordant; red pairs disagree, "
            "discordant. <bookmark mark='b'/> Of the hundred and five pairs, eighty-six are concordant and nineteen discordant. "
            "<bookmark mark='c'/> Tau is the difference as a share of all pairs: <bookmark mark='d'/> point six three eight. "
            "<bookmark mark='e'/> Its meaning is direct: one plus tau over two, point eight two, is the chance that a random "
            "pair of schools is ordered the same way by both scores. Tau is smaller than Spearman's correlation, as it "
            "usually is, but it's on a different scale, not a weaker finding."
        ) as vo:
            self.play(FadeIn(A), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[Create(s_) for s_ in segs], lag_ratio=0.15), run_time=2.0)
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def outlier(self):
        L, G = np.asarray(museum.LAW_LSAT, float), np.asarray(museum.LAW_GPA, float)
        G2 = G.copy()
        i = int(np.argmin(L))
        G2[i] = 4.2
        A = axes([530, 680], [2.6, 4.4], x_length=6.0, y_length=4.4, xlabel=r"LSAT", ylabel=r"GPA", xticks=[550, 600, 650],
                 yticks=[2.8, 3.4, 4.0], center=[-3.0, 0.2, 0])
        ax = A.ax
        dots = scatter(ax, L, G, radius=0.08)
        moved = Dot(ax.c2p(L[i], 4.2), radius=0.1, color=RES)
        tab = table_rows([
            [r"", r"as recorded", r"one GPA $\to$ 4.2"],
            [r"Pearson", f"{np.corrcoef(L, G)[0, 1]:.3f}", f"{np.corrcoef(L, G2)[0, 1]:.3f}"],
            [r"Spearman", f"{stats.spearmanr(L, G)[0]:.3f}", f"{stats.spearmanr(L, G2)[0]:.3f}"],
            [r"Kendall", f"{stats.kendalltau(L, G)[0]:.3f}", f"{stats.kendalltau(L, G2)[0]:.3f}"],
        ], font_size=24, colors=[GREY_B, None, RANK, RANK]).move_to([3.6, 0.8, 0])
        foot = label(r"a rank can move only so far: \ one point can't dominate", font_size=22, color=OBS).move_to([3.6, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Why prefer ranks? Suppose one school's GPA had been mis-recorded: the school with the lowest "
            "LSAT entered as four point two. <bookmark mark='b'/> Pearson's correlation collapses from point seven seven six to "
            "point one five. Spearman's falls to point four four and Kendall's to point three nine. <bookmark mark='c'/> One "
            "wrong value still hurts the rank correlations, but less, because a point's rank can move only so far, while its "
            "value can move without limit. That's robustness: a bounded influence for every observation. We'll measure it "
            "properly in Part 30, with the influence function."
        ) as vo:
            self.play(FadeIn(A), FadeIn(dots))
            vo.wait_until("a")
            self.play(Transform(dots[i], moved))
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
