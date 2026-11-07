from __future__ import annotations

import numpy as np

from videos.stats.stats43.common import *  # noqa: F403


class StrongLaw(VoiceoverScene):
    def construct(self):
        self.card()
        self.statement()
        self.maximal()
        self.series()
        self.etemadi()
        self.paths()

    def card(self):
        card = chapter_card(6, r"The strong law", r"Why does almost every average settle?", lit=(1981,), part=PART)
        with self.voiceover("Chapter six. The strong law of large numbers, proved."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def statement(self):
        rows = [
            cmath(r"X_i \text{ i.i.d.}, \ E|X| < \infty", r"\Rightarrow", r"\bar X_n \to \mu \ \text{ almost surely}", font_size=34),
            cmath(r"E|X| = \infty", r"\Rightarrow", r"\limsup |\bar X_n| = \infty \ \text{ almost surely}", font_size=34),
            cmath(r"\text{why}", r":", r"\textstyle\sum_n P(|X| > n) \le E|X| \le 1 + \sum_n P(|X| > n)", font_size=32),
            cmath(r"\text{so}", r":", r"\forall M\ge1:\ |X_n|>Mn\ \text{i.o. (BC II)};\ |X_n|/n\le |\bar X_n|+|\bar X_{n-1}|", font_size=30),
        ]
        rows[0][-1].set_color(GOODC)
        rows[1][-1].set_color(BADC)
        whys = [why(r"Kolmogorov (1930s)"), why(r"the converse"), why(r"the layer cake, \ in steps"), why(r"jumps of size $n$")]
        with self.voiceover(
            "<bookmark mark='a'/> The theorem: for independent, identically distributed variables with a finite mean,"
            " the running average converges to the mean, almost surely. <bookmark mark='b'/> And the condition is "
            "exactly right: if the mean of the absolute value is infinite, the running averages are unbounded, almost"
            " surely. <bookmark mark='c'/> The converse takes two lines. The layer-cake formula, in integer steps, "
            "says the expected absolute value is finite exactly when the probabilities that the absolute value "
            "exceeds n have a finite sum. <bookmark mark='d'/> If they don't, for every positive integer M, "
            "Borel–Cantelli gives absolute X n exceeding M n infinitely often. Thus limsup of absolute X n over n is "
            "infinite. Since X n over n equals the current average minus one minus one over n times the previous "
            "average, the averages cannot remain bounded. The Cauchy law is the standard example."
        ) as vo:
            heading=label('The iid strong law needs a finite absolute first moment',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def maximal(self):
        rows = [
            cmath(r"\text{maximal}", r":", r"P\big(\max_{k \le n} |S_k| \ge \lambda\big) \le \text{Var}(S_n) / \lambda^2", font_size=34),
            cmath(r"\text{two series}", r":", r"\textstyle\sum \text{Var}(X_k) < \infty, \ E X_k = 0 \Rightarrow \sum X_k \text{ converges a.s.}", font_size=30),
            cmath(r"\text{three series}", r":", r"\textstyle\sum P(|X_k| > c), \ \sum E Y_k, \ \sum \text{Var}\, Y_k \text{ all converge}", font_size=30),
            cmath(r"\iff", r"\;", r"\textstyle\sum X_k \text{ converges a.s.}; \ \ Y_k = X_k 1(|X_k| \le c)", font_size=30),
        ]
        rows[0][-1].set_color(LAWC)
        whys = [why(r"independent centered summands with finite variances"), why(r"Cauchy criterion, \ a.s."), why(r"Kolmogorov (1928)"), why(r"truncated at any $c > 0$")]
        with self.voiceover(
            "<bookmark mark='a'/> Kolmogorov's route went through series. His maximal inequality is Chebyshev's inequality "
            "for a whole path: the chance that the partial sums ever reach lambda, before time n, is at most the final "
            "variance over lambda squared. <bookmark mark='b'/> It gives the two-series theorem: centred independent terms "
            "whose variances have a finite sum form a series that converges almost surely. <bookmark mark='c'/> The "
            "three-series theorem says exactly when an independent series converges: after truncating each term at some "
            "level c, the chance of exceeding c, the truncated means and the truncated variances must all have convergent "
            "sums. <bookmark mark='d'/> The truncation is the trick: big terms are handled by Borel–Cantelli, small ones by "
            "the maximal inequality."
        ) as vo:
            heading=label('Independent random series are controlled by variance and truncation',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def series(self):
        d = load("series")
        k = np.asarray(d["k"], float)
        A = axes([0, 5000], [-4, 4], x_length=5.6, y_length=3.6, xlabel=r"terms", ylabel=r"$\sum_{j \le k} \pm 1/j$", xticks=[0, 2500, 5000],
                 yticks=[-4, 0, 4], center=[-3.6, 0.9, 0])
        B = axes([0, 5000], [-15, 15], x_length=5.6, y_length=3.6, xlabel=r"terms", ylabel=r"$\sum_{j \le k} \pm 1/j^{0.4}$", xticks=[0, 2500, 5000],
                 yticks=[-15, 0, 15], center=[3.2, 0.9, 0])
        cols = [LAWC, S.ALT, S.ACCENT, S.PRIOR, S.KEPT, S.RESID]
        p1 = VGroup(*[polyline(A.ax, k, np.asarray(d["p1"][i]), cols[i % 6], 1.8) for i in range(6)])
        p4 = VGroup(*[polyline(B.ax, k, np.asarray(d["p4"][i]), cols[i % 6], 1.8) for i in range(6)])
        side = fit_rows(VGroup(
            label(r"random signs, \ $\pm 1/j$: \ $\sum 1/j^2 < \infty$: \ converges, \ almost surely", font_size=24, color=GOODC),
            label(rf"between 50,000 and 100,000 terms it moves {d['tail_mean']:.4f} on average", font_size=22, color=GREY_A),
            label(r"$\pm 1/j^{0.4}$: \ $\sum 1/j^{0.8} = \infty$: \ diverges, \ almost surely", font_size=24, color=BADC),
            label(r"the 0--1 law said one or the other; \ the three series say which", font_size=24, color=S.ACCENT),
        ), 12.4, 0.3, [0, -2.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Two random series. On the left, the harmonic series with random signs: plus or minus one, "
            f"one half, one third, and so on. The variances are one over j squared, with a finite sum, so the series "
            f"converges almost surely, though the harmonic series itself diverges. <bookmark mark='b'/> Each path settles on "
            f"its own random limit; between fifty and a hundred thousand terms the paths move by about "
            f"{say(d['tail_mean'], 4)}. <bookmark mark='c'/> On the right, terms of size one over j to the point four: the "
            f"variances sum to infinity, and the series wanders off. <bookmark mark='d'/> Kolmogorov's zero–one law promised "
            f"that each series converges almost surely or diverges almost surely; the three series tell us which."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B))
            vo.wait_until("a")
            self.play(Create(p1), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(p4), FadeIn(side[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def etemadi(self):
        rows = [
            cmath(r"1.", r":", r"X \ge 0 \ \text{(split } X = X^+ - X^-\text{)}; \ \ Y_k = X_k 1(X_k \le k),\quad T_n=\sum_{k\le n}Y_k", font_size=30),
            cmath(r"2.", r":", r"\textstyle\sum_k P(X_k \ne Y_k) = \sum_k P(X > k) \le E X < \infty: \ \text{BC I}", font_size=30),
            cmath(r"3.", r":", r"k_n = \lfloor \alpha^n \rfloor: \ \textstyle\sum_n P\big(|T_{k_n} - E T_{k_n}| > \varepsilon k_n\big) \le C \sum_k \frac{E Y_k^2}{k^2} < \infty", font_size=28),
            cmath(r"4.", r":", r"k_n \le m < k_{n+1}: \ \frac{T_{k_n}}{k_{n+1}} \le \frac{T_m}{m} \le \frac{T_{k_{n+1}}}{k_n}", font_size=32),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"truncate"), why(r"they differ finitely often"), why(r"Chebyshev along a geometric subsequence"), why(r"so $\mu/\alpha \le \liminf\le\limsup \le \alpha\mu$; \ $\alpha \downarrow 1$")]
        with self.voiceover(
            "<bookmark mark='a'/> The shortest proof is Nasrollah Etemadi's, from 1981, and it needs only pairwise "
            "independence. Split each variable into positive and negative parts, so assume it is non-negative, and "
            "truncate the k-th at k. <bookmark mark='b'/> The truncated and original sequences differ only finitely "
            "often, by the first Borel–Cantelli lemma, because the chances of a difference sum to at most the mean. "
            "<bookmark mark='c'/> Along a geometric subsequence, k n equal to alpha to the n, Chebyshev's inequality "
            "and a careful sum show that the deviation probabilities are summable, so Borel–Cantelli again gives "
            "convergence along the subsequence. <bookmark mark='d'/> Finally, because the variables are non-negative,"
            " the partial sums increase, and every average between two subsequence times is sandwiched between their "
            "averages. The lower and upper limits are pinned between mu over alpha and alpha times mu. Here T n is "
            "the sum of the truncated variables; its expectation divided by n tends to mu by dominated convergence "
            "followed by Cesaro averaging. The variance summability follows by interchanging non-negative sums, "
            "bounded by a constant times the finite mean; and alpha can be taken as close to one as we like."
        ) as vo:
            heading=label('Truncation and geometric subsequences prove the strong law',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def paths(self):
        d = load("slln")
        k = np.log10(np.asarray(d["k"], float))
        A = axes([0, 4.3], [0, 2.5], x_length=5.6, y_length=3.6, xlabel=r"$n$", ylabel=r"$\bar X_n$, \ exponential", xticks=[0, 1, 2, 3, 4],
                 yticks=[0, 1, 2], log_x=True, xfmt=lambda v: f"10^{{{int(v)}}}", center=[-3.6, 0.9, 0])
        B = axes([0, 4.3], [-6, 6], x_length=5.6, y_length=3.6, xlabel=r"$n$", ylabel=r"$\bar X_n$, \ Cauchy", xticks=[0, 1, 2, 3, 4],
                 yticks=[-6, 0, 6], log_x=True, xfmt=lambda v: f"10^{{{int(v)}}}", center=[3.2, 0.9, 0])
        cols = [LAWC, S.ALT, S.ACCENT, S.PRIOR, S.KEPT, S.RESID]
        pe = VGroup(*[polyline(A.ax, k, np.asarray(d["exp"][i]), cols[i], 1.8) for i in range(6)])
        pc = VGroup(*[polyline(B.ax, k, np.asarray(d["cauchy"][i]), cols[i], 1.8) for i in range(6)])
        mu = DashedLine(A.ax.c2p(0, 1), A.ax.c2p(4.3, 1), color=LIMC, stroke_width=2.5)
        sub = np.asarray(d["sub"])
        sd = VGroup(*[Dot(A.ax.c2p(np.log10(s), v), radius=0.05, color=WHITE) for s, v in zip(sub, d["exp_sub"]) if 0 <= v <= 2.5])
        side = fit_rows(VGroup(
            label(r"exponential, \ $E|X| = 1$: \ every path settles on 1", font_size=24, color=GOODC),
            label(r"white: \ the geometric subsequence $\lfloor 1.3^n \rfloor$ of Etemadi's step 3", font_size=22, color=GREY_A),
            label(r"Cauchy, \ $E|X| = \infty$: \ $\bar X_n$ is again Cauchy, \ for every $n$; \ it never settles", font_size=24, color=BADC),
        ), 12.4, 0.3, [0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Six paths of running means for exponential draws, on a log scale of n: each one settles "
            "on the mean of one, as the strong law says almost every path must. <bookmark mark='b'/> The white dots mark the "
            "geometric subsequence on which Etemadi's proof first establishes convergence. <bookmark mark='c'/> And six paths "
            "for the Cauchy law, whose mean does not exist. The average of n Cauchy variables is again standard Cauchy, for "
            "every n, so the running means keep jumping, as the converse of the strong law guarantees."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(mu), FadeIn(exact_tag(r"simulated: six paths of 20,000 draws each")))
            vo.wait_until("a")
            self.play(Create(pe), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(sd), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(pc), FadeIn(side[2]), run_time=2.5)
        self.clear_scene()
