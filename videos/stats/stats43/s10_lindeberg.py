from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats43.common import *  # noqa: F403


class Lindeberg(VoiceoverScene):
    def construct(self):
        self.card()
        self.statement()
        self.replacement()
        self.taylor()
        self.counter()
        self.part6()

    def card(self):
        card = chapter_card(9, r"Lindeberg--Feller", r"The central limit theorem, \ exactly", lit=(1922,), part=PART)
        with self.voiceover("Chapter nine. The central limit theorem in its exact form: Lindeberg and Feller."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def statement(self):
        rows = [
            cmath(r"X_{n1}, \ldots, X_{nn}", r":", r"\text{independent, mean } 0, \ \ s_n^2 = \textstyle\sum_k \text{Var}\, X_{nk}", font_size=32),
            cmath(r"L_n(\varepsilon)", r"=", r"\frac{1}{s_n^2} \textstyle\sum_k E\big[X_{nk}^2 \, 1(|X_{nk}| > \varepsilon s_n)\big] \to 0 \ \ \forall \varepsilon", font_size=32),
            cmath(r"\text{Lindeberg}", r":", r"L_n(\varepsilon) \to 0 \ \Rightarrow \ S_n / s_n \Rightarrow N(0, 1)", font_size=34),
            cmath(r"\text{Feller}", r":", r"\max_k \text{Var}\, X_{nk} / s_n^2 \to 0 \text{ and the CLT} \Rightarrow L_n \to 0", font_size=30),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"a triangular array"), why(r"vanishing truncated tail variance at every positive threshold"), why(r"Lindeberg (1922)"), why(r"Feller (1935): \ the converse")]
        with self.voiceover(
            "<bookmark mark='a'/> The general setting is a triangular array: for each n, independent centred "
            "variables, not necessarily identically distributed, with total variance s n squared. <bookmark "
            "mark='b'/> Lindeberg's quantity measures how much of that variance comes from summands larger than "
            "epsilon times s n. <bookmark mark='c'/> Jarl Waldemar Lindeberg proved in 1922 that if it tends to zero "
            "for every epsilon, the standardized sum is asymptotically normal. <bookmark mark='d'/> And William "
            "Feller proved in 1935 that the condition is also necessary, as long as no single summand's variance is a"
            " non-vanishing share of the total. So the theorem is exact: under Feller's maximal-variance condition, "
            "Lindeberg's tail-variance condition is equivalent to the CLT. Without that condition, a dominant summand"
            " can itself be normal and the sum can still be normal."
        ) as vo:
            heading=label('Lindeberg controls the share of variance in large summands',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def replacement(self):
        n = 6
        x0 = -5.4
        row1 = VGroup(*[Square(side_length=0.62, stroke_color=LAWC, stroke_width=2, fill_color=LAWC, fill_opacity=0.5).move_to([x0 + 0.8 * i, 1.6, 0]) for i in range(n)])
        steps = VGroup()
        for j in range(n + 1):
            r = VGroup()
            for i in range(n):
                normal = i < j
                c = LIMC if normal else LAWC
                r.add(Square(side_length=0.62, stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.5).move_to([x0 + 0.8 * i, 2.2 - 0.62 * j, 0]))
            steps.add(r)
        tags = VGroup(*[label(rf"$W_{j}$" if 0 < j < n + 1 else (r"$S_n$" if j == 0 else ""), font_size=20, color=GREY_A).next_to(steps[j], LEFT, buff=0.25) for j in range(n + 1)])
        tags[-1].become(label(r"$Z$", font_size=20, color=GREY_A).next_to(steps[-1], LEFT, buff=0.25))
        side = fit_rows(VGroup(
            label(r"swap the $X_k$ for normals $Z_k$ of the same variance, \ one at a time", font_size=24),
            label(r"$S_n$ (blue) becomes $Z \sim N(0, s_n^2)$ (gold) in $n$ swaps", font_size=24, color=GREY_A),
            label(r"$|E f(S_n) - E f(Z)| \le \sum_k |E f(W_k + X_k) - E f(W_k + Z_k)|$", font_size=24, color=S.ACCENT),
            label(r"a telescoping sum: \ bound each swap", font_size=24, color=GOODC),
        ), 5.4, 0.45, [3.7, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Lindeberg's own proof avoids characteristic functions and is the ancestor of Stein's method. "
            "Take a smooth bounded test function f, and replace the summands by normal variables of the same variance, one "
            "at a time. <bookmark mark='b'/> After n swaps the sum, in blue, has become a normal sum, in gold, exactly "
            "normal with variance s n squared. <bookmark mark='c'/> The difference between E f of the original sum and E f of "
            "the normal is at most the sum of the changes made by each swap, where W k holds the other summands, already "
            "swapped or not yet. <bookmark mark='d'/> So it is enough to show each swap changes very little."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), FadeIn(tags[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(steps[j], tags[j])) for j in range(1, n + 1)], lag_ratio=0.4), FadeIn(side[1]), run_time=3.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def taylor(self):
        rows = [
            cmath(r"\xi_k", r"=", r"X_{nk}/s_n,\quad \eta_k=Z_{nk}/s_n,\quad \sum_k\operatorname{Var}(\xi_k)=1", font_size=30),
            cmath(r"f(W+\xi_k)", r"=", r"f(W)+\xi_k f'(W)+\tfrac12\xi_k^2 f''(W)+R_k", font_size=30),
            cmath(r"|R_k|", r"\le", r"\min\{ |\xi_k|^3\|f'''\|/6,\ \xi_k^2\|f''\|\};\quad \text{matched first two moments cancel}", font_size=28),
            cmath(r"\sum_k E|R_k|", r"\le", r"\varepsilon\|f'''\|/6+\|f''\|L_n(\varepsilon);\quad \text{the normal replacement tails vanish too}", font_size=28),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Taylor, \ two remainders"), why(r"matched moments"), why(r"small summands: \ cubic; \ large: \ Lindeberg"), why(r"standardize")]
        with self.voiceover(
            "<bookmark mark='a'/> First divide every summand and normal replacement by s n, so their total variance "
            "is one. Expand f around the sum of the other standardized terms to second order. The remainder is at "
            "most a sixth of the absolute cube times the third derivative's bound, or the square times the second "
            "derivative's, whichever is smaller. <bookmark mark='b'/> Do the same for the normal replacement. Because"
            " X and its replacement have the same mean and variance and are independent of W, the first three terms "
            "cancel exactly. <bookmark mark='c'/> Use the cubic bound on summands smaller than epsilon s n, and the "
            "quadratic bound on the larger ones, whose total is exactly Lindeberg's quantity. <bookmark mark='d'/> "
            "The error is at most epsilon times a derivative bound plus a constant times L n of epsilon, with the "
            "same bounds for the normal replacements. Lindeberg implies that their largest variance vanishes, so "
            "their tail term also vanishes. Let n grow, then epsilon shrink. Smooth test functions suffice for weak "
            "convergence, and the theorem is proved."
        ) as vo:
            heading=label('Standardize first, then bound the Taylor remainders',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def counter(self):
        d = load("lindeberg")
        mid = np.asarray(d["mid"])
        A = axes([-4, 4], [0, 0.9], x_length=5.4, y_length=3.4, xlabel=r"$S_n / s_n$", ylabel=r"density", xticks=[-4, -2, 0, 2, 4],
                 yticks=[0, 0.4, 0.8], center=[-3.5, 0.8, 0])
        B = axes([-4, 4], [0, 0.9], x_length=5.4, y_length=3.4, xlabel=r"$S_n / s_n$", ylabel=r"density", xticks=[-4, -2, 0, 2, 4],
                 yticks=[0, 0.4, 0.8], center=[3.3, 0.8, 0])
        w = mid[1] - mid[0]
        ha = bars_at(A.ax, mid, d["equal"]["hist"], w, LAWC, opacity=0.75)
        hb = bars_at(B.ax, mid, d["dominant"]["hist"], w, BADC, opacity=0.75)
        xs = np.linspace(-4, 4, 200)
        na = curve(A.ax, xs, stats.norm.pdf(xs), LIMC, 3)
        nb = curve(B.ax, xs, stats.norm.pdf(xs), LIMC, 3)
        side = fit_rows(VGroup(
            label(rf"20 equal uniforms: \ $L_n(1/2)=0$, \ KS distance {d['equal']['ks']:.3f}", font_size=22, color=LAWC),
            label(rf"20 signs with $\text{{Var}}\, X_k = 4^k$: \ the last holds {100 * d['dominant']['share_last']:.0f}\% of the variance", font_size=22, color=BADC),
            label(rf"$L_n(\tfrac12) = {d['L_dominant']:.2f}$ \ as $n\to\infty$: \ the limiting law is uniform, \ KS {d['dominant']['ks']:.3f}", font_size=22, color=BADC),
        ), 12.4, 0.28, [0, -2.3, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Here is the condition doing its work. On the left, twenty independent uniforms of equal size: Lindeberg's quantity is zero once n passes twelve, and the standardized sum is normal to within {say(d['equal']['ks'], 3)} in Kolmogorov distance. <bookmark mark='b'/> On the right, twenty random signs whose variances grow like four to the k: the last one alone carries three quarters of the total. <bookmark mark='c'/> At epsilon one half, Lindeberg's quantity tends to three quarters as this array grows, and the sum is no more normal at twenty terms than at two. Read from the largest term down, the signs have sizes that halve each time: they are the binary digits of chapter two, and their finite sum is uniform on a fine lattice and its limiting law is continuous uniform, not normal. This particular dominant-sign construction fails the CLT; dominance alone is not a universal obstruction."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(exact_tag(r"simulated: 200,000 sums each")))
            vo.wait_until("a")
            self.play(FadeIn(ha), Create(na), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(hb), Create(nb), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def part6(self):
        rows = fit_rows(VGroup(
            label(r"i.i.d. centered, \ $0<\sigma^2<\infty$: \ $L_n(\varepsilon) = E[X^2 1(|X| > \varepsilon\sigma\sqrt n)]/\sigma^2 \to 0$ \ by DCT", font_size=26, color=GOODC),
            label(r"so the classical CLT needs only a finite variance", font_size=26, color=GREY_A),
            label(r"Part 6's proof assumed an MGF: \ it excluded $t$-distributions, \ Pareto tails, \ incomes", font_size=26, color=BADC),
            label(r"Lyapunov's condition, \ $\sum E|X_k|^{2+\delta} / s_n^{2+\delta} \to 0$, \ implies Lindeberg's", font_size=26, color=S.ACCENT),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> For identically distributed summands with finite variance, Lindeberg's quantity is "
            "the expected squared value beyond epsilon sigma root n, which tends to zero by dominated convergence. "
            "<bookmark mark='b'/> So the iid classical CLT needs a positive finite variance, with centering by the "
            "finite mean. <bookmark mark='c'/> Part six's proof assumed a moment generating function, which quietly "
            "excluded t distributions, Pareto tails and the World's incomes; that assumption is now gone. <bookmark "
            "mark='d'/> In practice one often checks Lyapunov's stronger condition on moments slightly above two, "
            "which implies Lindeberg's."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
