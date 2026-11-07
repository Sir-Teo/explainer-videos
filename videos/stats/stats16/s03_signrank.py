from __future__ import annotations

import itertools

import numpy as np
from scipy import stats

from videos.stats.stats16.common import *  # noqa: F403


def diff_bars(ax, z, colors=None, width=0.6):
    """Bars from 0 to each difference z_i at x = i + 1, up or down."""
    g = VGroup()
    for i, v in enumerate(z):
        top, bot = ax.c2p(i + 1, max(v, 0)), ax.c2p(i + 1, min(v, 0))
        h = max(1e-3, top[1] - bot[1])
        w = ax.c2p(width, 0)[0] - ax.c2p(0, 0)[0]
        c = (colors[i] if colors is not None else (S.CTRL if v > 0 else RES))
        g.add(Rectangle(width=w, height=h, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to((top + bot) / 2))
    return g


class SignedRank(VoiceoverScene):
    def construct(self):
        self.card()
        self.darwin()
        self.sign_test()
        self.fisher_flip()
        self.ranks()
        self.null()
        self.compare()
        self.hodges()

    def card(self):
        card = chapter_card(2, r"Signs and signed ranks", r"Darwin's maize, \ three ways", lit=(1945,), part=PART)
        with self.voiceover("Chapter two. Signs and signed ranks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def darwin(self):
        d = load("signrank")
        z = np.asarray(d["z"])
        A = axes([0, 16], [-80, 80], x_length=7.2, y_length=4.4, xlabel=r"pair", ylabel=r"crossed $-$ self-fertilized, \ eighths of an inch",
                 xticks=[1, 5, 10, 15], yticks=[-60, -30, 0, 30, 60], center=[-2.4, 0.0, 0])
        ax = A.ax
        zero = Line(ax.c2p(0, 0), ax.c2p(16, 0), color=GREY_C, stroke_width=2)
        bars = diff_bars(ax, z)
        rows = fit_rows(VGroup(
            label(r"Darwin (1876): \ \emph{Zea mays}, \ 15 pairs", font_size=24),
            label(r"one cross-fertilized, \ one self-fertilized plant, \ same pot", font_size=22),
            label(r"13 of 15 differences positive", font_size=24, color=S.CTRL),
            MathTex(rf"\bar d = {z.mean():.1f},\ \ s = {z.std(ddof=1):.1f}", font_size=30),
            label(r"two large negatives: \ pairs 2 and 15", font_size=22, color=RES),
        ), 4.2, 0.36, [4.6, 0.1, 0])
        tag = historical_tag(r"Darwin (1876); \ Fisher (1935), \ \S 17", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> In 1876 Charles Darwin published an experiment on maize. In each of fifteen pairs, one plant "
            "came from a cross-fertilized seed and one from a self-fertilized seed, grown in the same pot. "
            "<bookmark mark='b'/> Here are the differences in final height, crossed minus self, in eighths of an inch, as "
            "Fisher reprinted them in 1935. <bookmark mark='c'/> Thirteen of the fifteen are positive. "
            "<bookmark mark='d'/> The mean difference is about twenty-one, with a standard deviation near thirty-eight. "
            "<bookmark mark='e'/> And two pairs go strongly the other way. Darwin asked his cousin Francis Galton to analyse "
            "the numbers; the data have been a test case ever since. Is cross-fertilization better? We'll ask three tests, each "
            "making fewer assumptions than a t-test."
        ) as vo:
            self.play(FadeIn(A), Create(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN if v > 0 else UP) for b_, v in zip(bars, z)], lag_ratio=0.08))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def sign_test(self):
        d = load("signrank")
        k = np.arange(16)
        pmf = stats.binom(15, 0.5).pmf(k)
        A = axes([-0.5, 15.5], [0, 0.22], x_length=7.6, y_length=3.8, xlabel=r"number of positive differences", ylabel=r"probability",
                 xticks=[0, 5, 10, 15], yticks=[0, 0.1, 0.2], center=[-1.8, 0.3, 0])
        ax = A.ax
        hi = [i for i in k if i >= 13 or i <= 2]
        bars = bars_at(ax, k, pmf, 0.75, NULLC, highlight=hi, hcolor=OBS)
        rows = [
            cmath(r"H_0", r":", r"\text{median difference} = 0", font_size=30),
            cmath(r"\#\{d_i > 0\}", r"\sim", r"\text{Binomial}(15, \tfrac12)", font_size=30),
            cmath(r"p", r"=", rf"2\,P(\ge 13) = {d['sign_p']:.4f}", font_size=30),
        ]
        rows[2][2].set_color(OBS)
        g = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([4.6, 0.6, 0])
        for r in g:
            if r.width > 4.4:
                r.width = 4.4
        foot = label(r"independent continuous differences: \ no symmetry needed", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "<bookmark mark='a'/> The oldest test of all is the sign test; John Arbuthnot used it in 1710 on London's christening "
            "records. For independent continuous differences with median zero, each sign is equally likely positive or negative. "
            "<bookmark mark='b'/> So the number of positive signs is Binomial fifteen, one half, whatever the shape of the "
            "distribution. <bookmark mark='c'/> Thirteen or more positives, or two or fewer, has probability point oh oh seven "
            "four. <bookmark mark='d'/> The sign test uses only the signs, so it assumes nothing about the distribution, not "
            "even that it's symmetric. The price is that it throws away the sizes: it doesn't notice that the two negative "
            "differences are large."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(g[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.05), FadeIn(g[1]))
            vo.wait_until("c")
            self.play(FadeIn(g[2]), Indicate(VGroup(*[bars[i] for i in hi]), color=OBS))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def fisher_flip(self):
        d = load("signrank")
        z = np.asarray(d["z"])
        a = np.abs(z)
        A = axes([0, 16], [-80, 80], x_length=6.2, y_length=3.0, xlabel=r"", ylabel=r"a sign-flipped copy",
                 xticks=None, yticks=[-60, 0, 60], center=[-3.4, 2.0, 0])
        ax = A.ax
        zero = Line(ax.c2p(0, 0), ax.c2p(16, 0), color=GREY_C, stroke_width=2)
        bars = diff_bars(ax, z)
        s = np.array(list(itertools.product([-1, 1], repeat=15)))
        T = s @ a
        B = axes([-560, 560], [0, 1600], x_length=6.2, y_length=2.3, xlabel=r"$\sum \pm |d_i|$ over all $2^{15}$ sign patterns",
                 ylabel=r"patterns", xticks=[-500, -250, 0, 250, 500], yticks=[0, 800, 1600], center=[-3.4, -2.0, 0], font_size=18)
        bx = B.ax
        e = np.linspace(-560, 560, 57)
        h = np.histogram(T, e)[0]
        hb = VGroup()
        for lo, hh in zip(e[:-1], h):
            c = OBS if abs(lo + 10) >= z.sum() else NULLC
            hb.add(*hist_bars(bx, [lo, lo + 20], [hh], color=c, opacity=0.85))
        cnt = int(np.sum(np.abs(T) >= z.sum()))
        rows = fit_rows(VGroup(
            label(r"Fisher (1935): \ independent symmetric differences: \ signs are fair coins", font_size=22),
            label(r"keep the sizes; \ flip the signs: \ $2^{15} = 32{,}768$ patterns", font_size=22),
            MathTex(rf"\textstyle\sum d_i = {z.sum():.0f}", font_size=30, color=OBS),
            MathTex(rf"{cnt:,}\ \text{{patterns as extreme}}", font_size=26),
            MathTex(rf"p = {cnt} / 32{{,}}768 = {cnt / 32768:.3f}", font_size=30, color=OBS),
        ), 5.4, 0.34, [3.8, 0.2, 0])
        g = np.random.Generator(np.random.PCG64(3))
        with self.voiceover(
            "<bookmark mark='a'/> Fisher's analysis in The Design of Experiments was one of the first permutation tests in print. If "
            "crossing does nothing, and the two plants in a pair were allotted at random, then which plant is the taller is a "
            "coin toss. Alternatively, independent symmetric null differences justify the sign flips. Darwin's historical allocation should not simply be assumed random. <bookmark mark='b'/> So keep the sizes, flip "
            "the signs. Here's one flipped copy, and another, and another. There are two to the fifteen, thirty-two thousand "
            "seven hundred and sixty-eight sign patterns. <bookmark mark='c'/> The observed differences sum to three hundred "
            "and fourteen. <bookmark mark='d'/> Of all the patterns, one thousand seven hundred and twenty-six give a sum at least "
            "that far from zero. <bookmark mark='e'/> p equals point oh five three. Fisher counted them, and found "
            "the answer agreed closely with the t-test, which was his point: here the normal theory is a good approximation to an exact "
            "argument that needs no normality."
        ) as vo:
            self.play(FadeIn(A), Create(zero), FadeIn(bars))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            for _ in range(3):
                sg = g.choice([-1, 1], 15)
                nb = diff_bars(ax, sg * a)
                self.play(Transform(bars, nb), run_time=0.8)
            self.play(Transform(bars, diff_bars(ax, z)), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(B), FadeIn(rows[2]))
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in hb], lag_ratio=0.02), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), Create(DashedLine(bx.c2p(z.sum(), 0), bx.c2p(z.sum(), 1500), color=OBS, stroke_width=3)))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def ranks(self):
        d = load("signrank")
        z = np.asarray(d["z"])
        r = np.asarray(d["ranks"]).astype(int)
        order = np.argsort(np.abs(z))
        hdr = VGroup(label(r"$|d|$", font_size=22, color=GREY_B), label(r"rank", font_size=22, color=GREY_B),
                     label(r"sign", font_size=22, color=GREY_B))
        xs = np.linspace(-5.6, 5.6, 15)
        cols = VGroup()
        for j, i in enumerate(order):
            c = S.CTRL if z[i] > 0 else RES
            cols.add(VGroup(MathTex(f"{abs(z[i]):.0f}", font_size=28, color=c).move_to([xs[j], 1.95, 0]),
                            MathTex(f"{r[i]}", font_size=30, color=c).move_to([xs[j], 1.3, 0]),
                            MathTex("+" if z[i] > 0 else "-", font_size=30, color=c).move_to([xs[j], 0.65, 0])))
        for k, hh in enumerate(hdr):
            hh.next_to(cols[0][k], LEFT, buff=0.45)
        rows = [
            cmath(r"W^+", r"=", r"\textstyle\sum_{d_i > 0} \text{rank}(|d_i|)", font_size=32),
            cmath(r"\ ", r"=", rf"120 - (10 + 14) = {d['W']:.0f}", font_size=32),
            cmath(r"H_0", r":", r"d_i \text{ independent, continuous, symmetric about } 0", font_size=30),
        ]
        rows[1][2].set_color(OBS)
        g = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, -1.9, 0])
        intro = label('Signed ranks combine signs with ordered magnitudes', font_size=36)
        with self.voiceover(
            "In 1945 Frank Wilcoxon, a chemist at American Cyanamid, proposed a compromise between using signs and using sizes. "
            "<bookmark mark='a'/> Sort the absolute differences and replace each by its rank, one to fifteen, keeping its sign. "
            "<bookmark mark='b'/> The two negative differences, sixty-seven and forty-eight, have ranks fourteen and ten. "
            "<bookmark mark='c'/> The signed-rank statistic W-plus is the sum of the ranks of the positive differences: one hundred "
            "and twenty, the total of all fifteen ranks, minus twenty-four, which is ninety-six. <bookmark mark='d'/> The "
            "assumptions here are independent continuous differences symmetric about zero, with distinct nonzero absolute values, stronger than the sign test's, weaker "
            "than normality. Ranks keep the ordering of the sizes and discard the rest, so one wild value can't dominate."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(hdr), LaggedStart(*[FadeIn(c_[0]) for c_ in cols], lag_ratio=0.05))
            self.play(LaggedStart(*[FadeIn(c_[1:]) for c_ in cols], lag_ratio=0.05))
            vo.wait_until("b")
            neg = VGroup(*[cols[j] for j, i in enumerate(order) if z[i] < 0])
            self.play(*[Circumscribe(m, color=RES) for m in neg])
            vo.wait_until("c")
            self.play(FadeIn(g[0]))
            self.play(FadeIn(g[1]))
            vo.wait_until("d")
            self.play(FadeIn(g[2]))
        self.clear_scene()

    def null(self):
        d = load("signrank")
        pmf = np.asarray(d["pmf"])
        w = np.arange(len(pmf))
        A = axes([-2, 122], [0, 0.025], x_length=8.2, y_length=3.8, xlabel=r"$W^+$", ylabel=r"probability under $H_0$",
                 xticks=[0, 24, 60, 96, 120], yticks=[0, 0.01, 0.02], center=[-1.4, 0.3, 0])
        ax = A.ax
        hi = [i for i in w if i >= 96 or i <= 24]
        bars = bars_at(ax, w, pmf, 0.85, NULLC, highlight=hi, hcolor=OBS)
        rows = [
            cmath(r"G(x)", r"=", r"\prod_{k=1}^{15} \frac{1 + x^k}{2}", font_size=30),
            cmath(r"P(W^+ = w)", r"=", r"[x^w]\, G(x)", font_size=30),
            cmath(r"p", r"=", rf"2\,P(W^+ \ge 96) = {d['p']:.4f}", font_size=30),
        ]
        rows[2][2].set_color(OBS)
        g = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([4.7, 0.5, 0])
        for r_ in g:
            if r_.width > 4.0:
                r_.width = 4.0
        foot = label(r"the same table for every symmetric distribution: \ Wilcoxon's tables, \ 1945", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "<bookmark mark='a'/> Under the null, rank k carries a plus sign with probability one half, independently. So W-plus "
            "is a sum of independent terms, each zero or k with equal chance. Its distribution is read off a generating "
            "function: the product over k of one plus x to the k, over two. <bookmark mark='b'/> The probability that W-plus "
            "equals w is the coefficient of x to the w: the share of the thirty-two thousand sign patterns whose positive ranks "
            "sum to w. Multiply out the polynomial and you have the whole distribution: symmetric about sixty, and nearly "
            "normal already. <bookmark mark='c'/> Ninety-six or more, or twenty-four or fewer: p equals point oh four one. "
            "<bookmark mark='d'/> And this table doesn't depend on the distribution of the differences, only on their being "
            "symmetric. One table serves every problem. That's why rank tests spread before computers did: Wilcoxon's paper "
            "came with tables you could carry."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(g[0]))
            vo.wait_until("b")
            self.play(FadeIn(g[1]), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.01), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(g[2]), Indicate(VGroup(*[bars[i] for i in hi]), color=OBS))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def compare(self):
        d = load("signrank")
        tab = table_rows([
            [r"test", r"uses", r"assumes", r"$p$"],
            [r"sign", r"signs", r"median 0", f"{d['sign_p']:.4f}"],
            [r"Wilcoxon signed rank", r"signs and ranks", r"symmetry", f"{d['p']:.3f}"],
            [r"Fisher's sign flip", r"signs and sizes", r"symmetry", r"0.053"],
            [r"paired $t$", r"the mean and $s$", r"normality", f"{d['t_p']:.3f}"],
        ], font_size=26, colors=[GREY_B, None, None, None, None]).move_to([0, 0.6, 0])
        foot = fit_rows(VGroup(
            label(r"four honest answers to four slightly different questions", font_size=24, color=OBS),
            label(r"the sign test is smallest here: \ it can't see that the two misses are big", font_size=22, color=GREY_A),
        ), 12.0, 0.25, [0, -2.6, 0])
        intro = label('Different tests use different information and assumptions', font_size=36)
        with self.voiceover(
            "<bookmark mark='a'/> Side by side. The sign test, using only signs: point oh oh seven. Wilcoxon's, using signs and "
            "ranks: point oh four one. Fisher's flip, using the sizes themselves: point oh five three. And the paired t-test, "
            "assuming normality: point oh five oh. <bookmark mark='b'/> These aren't four estimates of one true p-value. "
            "They're exact answers, or in the t-test's case an approximate one, to slightly different questions, each with "
            "its own assumptions. <bookmark mark='c'/> The sign test gives the smallest p here, because it's blind to the "
            "thing that worries the others: the two negative differences are large. Choose the test before looking, for the "
            "assumptions you're willing to make, and never shop among them for the smallest p."
        ) as vo:
            intro.scale_to_fit_width(min(intro.width, 12.5)).move_to([0, 3.2, 0])
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def hodges(self):
        d = load("signrank")
        z = np.asarray(d["z"])
        walsh = np.sort([(z[i] + z[j]) / 2 for i in range(15) for j in range(i, 15)])
        hl = float(np.median(walsh))
        lo, hi = walsh[25], walsh[94]
        A = axes([-70, 80], [0, 1], x_length=10.0, y_length=1.4, xlabel=r"the 120 Walsh averages $(d_i + d_j)/2,\ i \le j$",
                 xticks=[-60, -30, 0, 30, 60], center=[0, 1.4, 0])
        ax = A.ax
        g = np.random.Generator(np.random.PCG64(5))
        dots = VGroup(*[Dot(ax.c2p(v, 0.15 + 0.7 * g.random()), radius=0.045, color=RANK if lo <= v <= hi else GREY_B) for v in walsh])
        mk = Line(ax.c2p(hl, 0), ax.c2p(hl, 1), color=OBS, stroke_width=4)
        tl = stats.t.interval(0.95, 14, loc=z.mean(), scale=z.std(ddof=1) / np.sqrt(15))
        rows = [
            cmath(r"\hat\theta_{\text{HL}}", r"=", rf"\text{{median of the Walsh averages}} = {hl:.0f}", font_size=30),
            cmath(r"\text{95\% CI}", r":", rf"[w_{{(26)}},\ w_{{(95)}}] = [{lo:.1f},\ {hi:.1f}]", font_size=30),
            cmath(r"\text{compare } t", r":", rf"\bar d = {z.mean():.1f},\ \ [{tl[0]:.2f},\ {tl[1]:.1f}]", font_size=30),
        ]
        rows[0][2].set_color(OBS)
        rows[1][2].set_color(RANK)
        gg = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, -1.6, 0])
        with self.voiceover(
            "A test answers yes or no; we'd like an estimate too. Joseph Hodges and Erich Lehmann found the one that goes with "
            "Wilcoxon's test, in 1963. <bookmark mark='a'/> Average every pair of differences, including each with itself: one "
            "hundred and twenty Walsh averages. W-plus is the number of them that are positive. <bookmark mark='b'/> The "
            "Hodges–Lehmann estimate of the shift is their median, twenty-five. <bookmark mark='c'/> Inverting the test gives "
            "an interval: the shifts that Wilcoxon's test wouldn't reject are those between the twenty-sixth and ninety-fifth "
            "Walsh averages, four to forty-one and a half, with confidence ninety-five point two percent, exactly, for any "
            "symmetric distribution. <bookmark mark='d'/> The t-interval is nearly the same here. The rank methods give up very "
            "little when the data are well behaved, a point we'll make precise in chapter five."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(mk), FadeIn(gg[0]))
            vo.wait_until("c")
            self.play(FadeIn(gg[1]))
            vo.wait_until("d")
            self.play(FadeIn(gg[2]))
        self.clear_scene()
