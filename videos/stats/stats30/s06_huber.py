from __future__ import annotations

import numpy as np

from explainer.stats.kit import robust as R
from videos.stats.stats30.common import *  # noqa: F403


class Huber(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.least_favourable()
        self.solution()
        self.ktable()
        self.curves()
        self.princeton()
        self.psis()
        self.irls()
        self.weights()
        self.proposal2()

    def card(self):
        card = chapter_card(5, r"Huber's minimax estimator", r"The best worst case", lit=(1964,), part=PART)
        with self.voiceover("Chapter five. Huber's minimax estimator."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = [
            cmath(r"\mathcal P_\varepsilon", r"=", r"\{(1 - \varepsilon)\Phi + \varepsilon H: \ H \text{ symmetric}\}", font_size=30),
            cmath(r"V(\psi, F)", r"=", r"\dfrac{E_F\, \psi^2}{(E_F\, \psi')^2}", font_size=32),
            cmath(r"\text{goal}", r":", r"\min_\psi \ \max_{F \in \mathcal P_\varepsilon} V(\psi, F)", font_size=32),
            cmath(r"\text{game}", r":", r"\text{statistician picks } \psi, \ \text{nature picks } F", font_size=30),
        ]
        rows[2][2].set_color(HUBC)
        whys = [why(r"Tukey's neighbourhood, \ any contaminant"), why(r"an M-estimator's asymptotic variance"),
                why(r"Huber (1964)"), why(r"a saddle point solves it")]
        with self.voiceover(
            "<bookmark mark='a'/> Peter Huber's 1964 paper made robustness a theorem. Take Tukey's neighbourhood: the normal, "
            "mixed with a share epsilon of any symmetric contaminant at all. <bookmark mark='b'/> An M-estimator defined by "
            "psi has asymptotic variance E psi squared over E psi prime, squared. <bookmark mark='c'/> Find the psi whose "
            "worst-case variance over the whole neighbourhood is smallest. <bookmark mark='d'/> It is a game: the "
            "statistician chooses psi, nature chooses the contaminant, and Huber found its saddle point."
        ) as vo:
            intro=label('Known-scale symmetric contamination defines an asymptotic minimax game',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def least_favourable(self):
        rows = [
            cmath(r"F_0", r":", r"\text{the member with the least Fisher information}", font_size=30),
            cmath(r"f_0(x)", r"=", r"(1 - \varepsilon)\phi(x), \ \ |x| \le k", font_size=32),
            cmath(r"f_0(x)", r"=", r"(1 - \varepsilon)\phi(k)\, e^{-k(|x| - k)}, \ \ |x| > k", font_size=30),
            cmath(r"k", r":", r"\tfrac{2\phi(k)}{k} - 2\Phi(-k) = \tfrac{\varepsilon}{1 - \varepsilon}", font_size=30),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"the hardest distribution to estimate the centre of"), why(r"normal in the middle"),
                why(r"exponential tails: \ the least-information continuation"), why(r"so that $f_0$ integrates to 1")]
        with self.voiceover(
            "<bookmark mark='a'/> Nature's best move is the member of the neighbourhood with the least Fisher "
            "information, the hardest to estimate the centre of. <bookmark mark='b'/> It is normal in the middle, "
            "scaled by one minus epsilon, <bookmark mark='c'/> with exponential tails beyond plus or minus k, the "
            "exponential continuation minimizing Fisher information in this neighbourhood; heavier contaminant tails "
            "are also allowed. <bookmark mark='d'/> k is fixed by requiring the density to integrate to one."
        ) as vo:
            intro=label('The least-information member has normal center and exponential tails',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def solution(self):
        rows = [
            cmath(r"\psi_0", r"=", r"-f_0'/f_0", font_size=32),
            cmath(r"", r"=", r"x \ \text{for } |x| \le k, \ \ k\, \mathrm{sign}(x) \text{ beyond}", font_size=30),
            cmath(r"V(\psi_0, F)", r"\le", r"V(\psi_0, F_0) = 1/I(F_0) \ \ \text{for every } F \in \mathcal P_\varepsilon", font_size=28),
            cmath(r"V(\psi, F_0)", r"\ge", r"1/I(F_0) \ \ \text{for every } \psi", font_size=30),
        ]
        rows[1][-1].set_color(HUBC)
        whys = [why(r"the MLE for $F_0$"), why(r"Huber's $\psi$: \ the mean in the middle, \ clipped"),
                why(r"no contaminant hurts it more than $F_0$"), why(r"Cramér--Rao at $F_0$: \ no $\psi$ does better")]
        with self.voiceover(
            "<bookmark mark='a'/> The statistician's best reply is the maximum likelihood estimator for that worst "
            "distribution, psi equal to minus f naught prime over f naught. <bookmark mark='b'/> In the middle it is x, the "
            "mean's psi; beyond k it is constant: Huber's clipped psi. <bookmark mark='c'/> Against it, no contaminant in the "
            "neighbourhood does more damage than f naught does, <bookmark mark='d'/> and at f naught no psi does better, by "
            "Cramér–Rao. A saddle point: Huber's estimator is minimax."
        ) as vo:
            intro=label('The least-favorable score is a clipped location score',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ktable(self):
        d = load("huber")
        hdr = [r"\textbf{contamination} $\varepsilon$", r"\textbf{Huber's} $k$", r"\textbf{minimax variance}", r"\textbf{vs the mean}"]
        body = [[f"{e:g}", f"{d['k'][f'{e:g}']:.3f}", f"{d['vmin'][f'{e:g}']:.3f}", r"$\infty$"] for e in d["eps"]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.28, colors=[GREY_A] + [None] * 6)
        for r in tb[1:]:
            r[1].set_color(HUBC)
            r[3].set_color(MEANC)
        tb.move_to([0, 0.7, 0])
        foot = fit_rows(VGroup(
            label(r"the mean's worst-case variance is infinite for every $\varepsilon > 0$", font_size=22),
            label(rf"$k = 1.345$: \ 95\% efficient at the normal \ (computed: {d['eff']['huber']:.3f}); \ the usual default", font_size=22, color=HUBC),
        ), 12.0, 0.22, [0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The minimax k for each amount of contamination. At one in a thousand, k is two point six "
            "three, and the price is under one percent of variance. At five percent, k is one point four, and the worst-case "
            "variance one point two six. At twenty percent, k falls below one. <bookmark mark='b'/> Against any of these "
            "neighbourhoods the mean's worst case is infinite. In practice k equal to one point three four five is used: "
            "ninety-five percent efficient at the normal, statkit's computation confirms."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), LaggedStart(*[FadeIn(r) for r in tb[1:]], lag_ratio=0.3), FadeIn(foot[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
        self.wait(1.0)
        self.clear_scene()

    def curves(self):
        d = load("huber")
        kg = np.asarray(d["kgrid"])
        A = axes([0.2, 4], [0.9, 2.0], x_length=7.4, y_length=4.4, xlabel=r"Huber's $k$", ylabel=r"asymptotic variance",
                 xticks=[1, 2, 3, 4], yticks=[1, 1.5, 2], center=[-2.0, 0.3, 0])
        ax = A.ax
        spec = (("0", MEDC), ("0.05", HUBC), ("0.1", RES))
        cs = {k: clip_curve(ax, kg, np.asarray(d["curves"][k]), c, 3, ymin=0.9, ymax=2.0) for k, c in spec}
        mins = {k: Dot(ax.c2p(kg[int(np.argmin(d["curves"][k]))], min(d["curves"][k])), radius=0.07, color=WHITE) for k, _ in spec}
        r = d["ref"]
        rows = fit_rows(VGroup(
            label(r"contaminant: \ $N(0, 10^2)$", font_size=22),
            label(r"green: \ no contamination: \ $k \to \infty$ (the mean) is best", font_size=22, color=MEDC),
            label(rf"gold: \ 5\%: \ best $k \approx 1.5$; \ mean {r['0.05']['mean']:.2f}, \ median {r['0.05']['median']:.2f}", font_size=22, color=HUBC),
            label(rf"red: \ 10\%: \ best $k \approx 1.2$; \ mean {r['0.1']['mean']:.1f}, \ median {r['0.1']['median']:.2f}", font_size=22, color=RES),
            label(r"the curves are flat near the minimum: \ $k$ need not be exact", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The variance of Huber's estimate against k, with the contaminant a normal ten times as "
            "wide. <bookmark mark='b'/> With no contamination, larger k is better, approaching the mean. "
            "<bookmark mark='c'/> With five percent, the best k is about one and a half, variance one point two three, against "
            "the mean's six and the median's one point seven. <bookmark mark='d'/> With ten percent, the best k moves to about "
            "one point two. <bookmark mark='e'/> And the curves are flat near their minima, so k needn't be tuned exactly: one "
            "point three four five is good across the board."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            for k, ((key, _), m_) in enumerate(zip(spec, "bcd")):
                vo.wait_until(m_)
                self.play(Create(cs[key]), FadeIn(mins[key]), FadeIn(rows[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def psis(self):
        u = np.linspace(-9, 9, 400)
        A = axes([-9, 9], [-2.6, 2.6], x_length=7.4, y_length=4.2, xlabel=r"$u = (x - \mu)/s$", ylabel=r"$\psi(u)$",
                 xticks=[-8, -4, 0, 4, 8], yticks=[-2, 0, 2], center=[-2.0, 0.3, 0])
        ax = A.ax
        cm = clip_curve(ax, u, u, MEANC, 2.5, ymin=-2.6, ymax=2.6)
        ch = curve(ax, u, R.psi_huber(u), HUBC, 3.5)
        cb = curve(ax, u, R.psi_biweight(u), BIWC, 3.5)
        ca = curve(ax, u, R.psi_hampel(u), TRIMC, 3)
        rows = fit_rows(VGroup(
            label(r"red: \ the mean, \ $\psi(u) = u$", font_size=22, color=MEANC),
            label(r"gold: \ Huber, \ $k = 1.345$: \ monotone", font_size=22, color=HUBC),
            label(r"purple: \ Tukey's biweight, \ $c = 4.685$: \ redescending", font_size=22, color=BIWC),
            label(r"teal: \ Hampel's three-part: \ redescending, \ piecewise", font_size=22, color=TRIMC),
            label(r"redescenders reject far points, \ but can have several roots", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The zoo of psi functions. The mean's is the identity. <bookmark mark='b'/> Huber's "
            "clips it: monotone, giving a convex objective; a flat interval of roots is possible if no observations "
            "supply local curvature. <bookmark mark='c'/> Tukey's biweight bends back to zero at four point six nine:"
            " redescending, so gross errors get no weight at all. <bookmark mark='d'/> Frank Hampel's three-part psi "
            "does the same with straight pieces. <bookmark mark='e'/> Redescending estimators reject far points "
            "cleanly, but their equations can have several roots, so they need a good, robust starting point, a "
            "lesson MM-regression builds on."
        ) as vo:
            self.play(FadeIn(A))
            for k, (c, m_) in enumerate(zip((cm, ch, cb, ca), "abcd")):
                vo.wait_until(m_)
                self.play(Create(c), FadeIn(rows[k]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def irls(self):
        rows = [
            cmath(r"\textstyle\sum_i \psi\bigl(\tfrac{x_i - \mu}{s}\bigr)", r"=", r"0", font_size=32),
            cmath(r"w_i", r"=", r"\psi(u_i)/u_i", font_size=32),
            cmath(r"\mu", r"\leftarrow", r"\textstyle\sum w_i x_i / \sum w_i", font_size=32),
            cmath(r"s", r":", r"\text{fixed at the MAD: \ scale must be robust too}", font_size=30),
        ]
        rows[2][2].set_color(HUBC)
        whys = [why(r"the estimating equation"), why(r"Huber: \ 1 in the middle, \ $k/|u|$ outside"),
                why(r"iteratively reweighted least squares"), why(r"chapter six")]
        with self.voiceover(
            "<bookmark mark='a'/> To compute it, solve the estimating equation. <bookmark mark='b'/> Write psi of u "
            "as a weight times u: for Huber, weight one in the middle and k over absolute u outside. <bookmark "
            "mark='c'/> Then the equation says mu is a weighted mean, and iterating, recompute the weights, recompute"
            " the mean, converges: iteratively reweighted least squares, Part 24's algorithm again. <bookmark "
            "mark='d'/> The residuals must be standardized by a scale that is itself robust, here the MAD, the "
            "subject of the next chapter."
        ) as vo:
            intro=label('A residual score can be written as an iterative weighting rule',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def princeton(self):
        d = load("princeton")
        e = d["eff"]
        dn = ("normal", "t3", "contam10", "slash", "cauchy")
        hdr = [r"\textbf{estimate}", r"\textbf{normal}", r"\textbf{$t_3$}", r"\textbf{10\% contam.}", r"\textbf{slash}",
               r"\textbf{Cauchy}", r"\textbf{worst}"]
        spec = (("mean", r"mean", MEANC), ("median", r"median", MEDC), ("trim10", r"10\% trimmed", TRIMC),
                ("trim25", r"25\% trimmed", TRIMC), ("hl", r"Hodges--Lehmann", HLC), ("huber", r"Huber", HUBC),
                ("biweight", r"biweight", BIWC))
        body = [[t] + [f"{e[x][k]:.2f}" for x in dn] + [f"{d['worst'][k]:.2f}"] for k, t, _ in spec]
        tb = table_rows([hdr] + body, font_size=24, col_buff=0.55, row_buff=0.26, colors=[GREY_A] + [c for _, _, c in spec])
        tb.move_to([0, 0.6, 0])
        foot = fit_rows(VGroup(
            label(rf"efficiency relative to the best of the seven, \ $n = {d['n']}$, \ {d['R']:,} samples each", font_size=22),
            label(r"mean has infinite MSE for slash/Cauchy; \ worst is over these five cases", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1970 and 1971 six statisticians at Princeton, Andrews, Bickel, Hampel, Huber, "
            "Rogers and Tukey, ran a vast simulation of sixty-eight location estimators. Here is a small version: "
            "seven estimators, five distributions from the normal to the Cauchy, samples of twenty, efficiency "
            "relative to the best on each. <bookmark mark='b'/> In this simulation the mean is best at the normal. "
            "Its population mean-squared error is infinite under slash and Cauchy sampling, so no finite Monte Carlo "
            "average estimates that risk. The median never falls below sixty-eight percent, but never rises much "
            "above it except in the wild tails. Hodges–Lehmann and Huber are excellent until the tails become "
            "extreme. <bookmark mark='c'/> The redescending biweight has the best worst case, eighty-five percent, "
            "alongside the twenty-five percent trimmed mean. This teaching study compares seven estimators on five "
            "distributions; the displayed worst column is the worst of those five, not a minimax guarantee over all "
            "distributions."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(tb[1:3]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tb[3:7]))
            vo.wait_until("c")
            self.play(FadeIn(tb[7]), FadeIn(foot[1]))
        self.clear_scene()

    def proposal2(self):
        rows = [
            cmath(r"\textstyle\sum_i \psi_k\bigl(\tfrac{x_i - \mu}{s}\bigr)", r"=", r"0", font_size=30),
            cmath(r"\tfrac1n \textstyle\sum_i \psi_k^2\bigl(\tfrac{x_i - \mu}{s}\bigr)", r"=", r"E_\Phi\, \psi_k^2(Z)", font_size=30),
            cmath(r"\text{joint}", r":", r"\text{location and scale together}", font_size=30),
            cmath(r"\text{breakdown}", r":", r"\text{lower than with the MAD}", font_size=30),
        ]
        rows[1][2].set_color(HUBC)
        whys = [why(r"location"), why(r"Huber's Proposal 2: \ consistent at the normal"), why(r"an option; ordinary defaults use MAD"),
                why(r"why a fixed MAD scale is often preferred")]
        with self.voiceover(
            "<bookmark mark='a'/> Huber also proposed estimating scale and location together: <bookmark mark='b'/> "
            "his Proposal 2 adds a second equation, matching the average squared psi to its value at the normal. "
            "<bookmark mark='c'/> It is an available scale option in several packages; both MASS rlm and statsmodels "
            "RLM ordinarily use a MAD scale by default. <bookmark mark='d'/> But its breakdown point is lower than "
            "with a fixed MAD, because the scale can be inflated by the outliers it is supposed to judge, which is "
            "why modern practice fixes a high-breakdown scale first."
        ) as vo:
            intro=label('Joint location-scale equations require separate robustness analysis',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def weights(self):
        from explainer.stats.kit import robust as RR
        x = museum.newcomb()
        h = RR.m_location(x, "huber")
        b = RR.m_location(x, "biweight")
        o = np.argsort(x)
        xs = x[o]
        A = axes([-50, 45], [0, 1.15], x_length=7.6, y_length=4.2, xlabel=r"observation", ylabel=r"weight in the final fit",
                 xticks=[-40, -20, 0, 20, 40], yticks=[0, 0.5, 1], center=[-1.8, 0.3, 0])
        ax = A.ax
        hw = VGroup(*[Dot(ax.c2p(v, w), radius=0.06, color=HUBC) for v, w in zip(xs, h["weights"][o])])
        bw = VGroup(*[Dot(ax.c2p(v, w), radius=0.05, color=BIWC) for v, w in zip(xs, b["weights"][o])])
        rows = fit_rows(VGroup(
            label(rf"Huber on Newcomb: \ $\hat\mu = {h['mu']:.2f}$, \ MAD scale {h['scale']:.2f}", font_size=22, color=HUBC),
            label(rf"{int((h['weights'] < 0.999).sum())} points down-weighted; \ $-44$ gets {h['weights'][np.argmin(x)]:.2f}", font_size=22, color=HUBC),
            label(rf"biweight: \ $-44$ and $-2$ get {abs(b['weights'][np.argmin(x)]):.2f} and {abs(b['weights'][np.where(x == -2)[0][0]]):.2f}", font_size=22, color=BIWC),
            label(r"the weights are the robust diagnosis", font_size=22, color=PATH),
        ), 4.4, 0.42, [4.4, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The weights at convergence are worth looking at. Huber's estimate on Newcomb's data, with a "
            "MAD scale of four point four five. <bookmark mark='b'/> Sixteen points get weight below one, and minus forty-four "
            "only eight percent: still counted, but barely. <bookmark mark='c'/> The biweight gives both strays weight zero, "
            "rejecting them outright, and down-weights every other point a little, more the farther it lies from the centre. <bookmark mark='d'/> These weights are "
            "themselves the robust diagnosis: they say which observations the estimate decided not to trust, and how much."
        ) as vo:
            self.add(newcomb_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in hw], lag_ratio=0.02), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p) for p in bw], lag_ratio=0.02), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
