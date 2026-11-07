from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.stats.kit import intervals as I
from videos.stats.stats11.common import *  # noqa: F403


class Discrete(VoiceoverScene):
    def construct(self):
        self.card()
        self.why_teeth()
        self.impossible()
        self.midp()
        self.poisson()
        self.median()
        self.choice()

    def card(self):
        card = chapter_card(6, r"Discreteness", r"Why no interval for a count covers exactly 95\%", part=PART)
        with self.voiceover("Chapter six. Discreteness."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def why_teeth(self):
        n = 20
        ints = [I.wilson(x, n) for x in range(n + 1)]
        A = axes([0, 1], [-0.5, 20.5], x_length=7.0, y_length=5.0, xlabel=r"$p$", ylabel=r"count $x$: \ its Wilson interval",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 5, 10, 15, 20], center=[-2.4, -0.2, 0])
        ax = A.ax
        segs = VGroup(*[Line(ax.c2p(lo, x), ax.c2p(hi, x), color=METHOD_COL["wilson"], stroke_width=3) for x, (lo, hi) in enumerate(ints)])
        p0 = ValueTracker(0.3)

        def probe():
            p = p0.get_value()
            ln = DashedLine(ax.c2p(p, -0.5), ax.c2p(p, 20.5), color=OBS, stroke_width=2.5)
            dots = VGroup(*[Dot(ax.c2p(p, x), radius=0.07, color=OBS) for x, (lo, hi) in enumerate(ints) if lo <= p <= hi])
            return VGroup(ln, dots)

        pr = always_redraw(probe)

        def cov():
            p = p0.get_value()
            c = sum(stats.binom.pmf(x, n, p) for x, (lo, hi) in enumerate(ints) if lo <= p <= hi)
            return MathTex(rf"p = {p:.3f}:\ \ \text{{coverage}} = {c:.3f}", font_size=30, color=OBS).move_to([4.2, 1.8, 0])

        cv = always_redraw(cov)
        rows = fit_rows(VGroup(
            MathTex(r"\text{coverage}(p) = \sum_{x:\ p \in C(x)} \binom nx p^x (1 - p)^{n - x}", font_size=26),
            label(r"as $p$ crosses an interval's end, \ a whole term drops out or comes in: \ a jump", font_size=24, color=GREY_A),
            label(r"between jumps, \ a smooth sum: \ the teeth of the saw", font_size=24, color=GREY_A),
        ), 5.0, 0.36, [4.3, -0.8, 0])
        with self.voiceover(
            "Why does every interval for a count sawtooth? <bookmark mark='a'/> Here are the twenty-one Wilson intervals "
            "for twenty trials, one for each possible count, stacked vertically. <bookmark mark='b'/> Fix a true p, the "
            "dashed line. The intervals it crosses are the outcomes that would cover it, and the coverage is their total "
            "binomial probability. <bookmark mark='c'/> Slide p. Between endpoints the set of covering outcomes stays the "
            "same and the coverage changes smoothly. But each time p crosses an endpoint, a whole outcome enters or "
            "leaves the set, and the coverage jumps. Those jumps are the teeth of the saw, and no fixed set of intervals "
            "can avoid them."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(s_) for s_ in segs], lag_ratio=0.05))
            vo.wait_until("b")
            self.add(pr, cv)
            self.play(FadeIn(pr), FadeIn(cv), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(p0.animate.set_value(0.55), run_time=5.0, rate_func=linear)
            self.play(FadeIn(rows[1:]))
            self.play(p0.animate.set_value(0.4), run_time=3.0, rate_func=linear)
        pr.clear_updaters()
        cv.clear_updaters()
        self.clear_scene()

    def impossible(self):
        rows = fit_rows(VGroup(
            label(r"with $n + 1$ possible outcomes, \ coverage is a finite sum of polynomials in $p$, \ with jumps", font_size=26),
            label(r"it cannot equal 0.95 for every $p$: \ exact coverage is impossible without randomization", font_size=28, color=OBS),
            label(r"randomized intervals (Stevens, 1950) achieve it, \ by tossing a coin after seeing the data", font_size=24, color=GREY_A),
            label(r"randomized intervals need an additional random draw: \ so we choose what to give up", font_size=24,
                  color=GREY_A),
        ), 12.6, 0.42, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> It's a theorem, not a failure of imagination. With finitely many outcomes, the coverage "
            "of any fixed family of intervals is a sum of polynomials in p that jumps at the endpoints. "
            "<bookmark mark='b'/> So it can't equal ninety-five percent for every p. Exact coverage is impossible. "
            "<bookmark mark='c'/> Wilfred Stevens showed in 1950 that it can be achieved by randomization: after seeing "
            "the data, toss a coin to decide exactly where the interval ends, just as the Neyman–Pearson lemma "
            "randomized at ties. <bookmark mark='d'/> Many applications avoid intervals that depend on an additional random draw. So we have to choose what to give up."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def midp(self):
        d = load("midp")
        ps = np.asarray(d["ps"])
        A = axes([0, 1], [0.88, 1], x_length=8.0, y_length=4.4, xlabel=r"$p$, \ $n = 25$", ylabel=r"exact coverage",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0.9, 0.95, 1], yfmt=lambda v: f"{v:.2f}", center=[-1.8, -0.3, 0])
        ax = A.ax
        nom = DashedLine(ax.c2p(0, 0.95), ax.c2p(1, 0.95), color=EXACT, stroke_width=2)
        cp = polyline(ax, ps, d["cp"], METHOD_COL["clopper_pearson"], 2.5)
        mp = polyline(ax, ps, d["mid"], S.POST, 2.5)
        leg = legend([(METHOD_COL["clopper_pearson"], rf"Clopper--Pearson: \ grid mean {100 * d['cp_mean']:.1f}\%, \ grid min {100 * d['cp_min']:.1f}\%"),
                      (S.POST, rf"mid-$p$: \ grid mean {100 * d['mid_mean']:.1f}\%, \ grid min {100 * d['mid_min']:.1f}\%")], font_size=22).to_edge(UP, buff=0.35)
        rows = fit_rows(VGroup(
            MathTex(r"p_{\mathrm{mid}} = P(T > t) + \tfrac12 P(T = t)", font_size=28, color=S.POST),
            label(r"count only half the observed outcome's probability", font_size=22, color=GREY_A),
            label(r"Lancaster (1961): \ closer to 95\% on average; \ no longer guaranteed", font_size=22, color=GREY_A),
        ), 4.2, 0.32, [4.8, -0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The Clopper–Pearson interval chooses to guarantee the promise. At twenty-five trials its "
            "coverage never dips below ninety-five percent, but its displayed grid average is ninety-seven and a half: it's too careful "
            "nearly everywhere. <bookmark mark='b'/> The mid-p version, from Henry Lancaster in 1961, counts only half "
            "the probability of the observed outcome when computing the tail. Its displayed grid coverage averages ninety-five point "
            "nine, much closer to the promise, but it dips to ninety-three. <bookmark mark='c'/> That's the choice in a "
            "nutshell: guarantee the promise everywhere, and be wide; or accept some undercoverage in exchange for shorter intervals. There is no deterministic exact ninety-five percent calibration at every p."
        ) as vo:
            self.play(FadeIn(A), Create(nom))
            vo.wait_until("a")
            self.play(Create(cp), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(mp), FadeIn(leg[1]), FadeIn(rows))
        self.clear_scene()

    def choice(self):
        rows = fit_rows(VGroup(
            label(r"guaranteed and approximate uses of ``95\%''", font_size=32, color=OBS),
            label(r"strict: \ at least 95\% for every $p$ \ (Neyman's definition): \ Clopper--Pearson", font_size=26,
                  color=METHOD_COL["clopper_pearson"]),
            label(r"on average: \ close to 95\%, \ dipping a little: \ Wilson, \ Jeffreys, \ mid-$p$", font_size=26, color=METHOD_COL["wilson"]),
            label(r"poor approximation: \ far below 95\% for whole ranges of $p$: \ Wald", font_size=26, color=METHOD_COL["wald"]),
            label(r"the Board's verdicts: \ kept within 3 MC SEs, \ ``conservative'' above, \ ``broken'' below", font_size=24, color=GREY_A),
        ), 12.6, 0.42, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Distinguish guaranteed coverage from approximate nominal coverage. <bookmark mark='b'/> The strict "
            "one, Neyman's: at least ninety-five percent for every p. Clopper–Pearson keeps it. <bookmark mark='c'/> The "
            "approximate one: close to ninety-five percent on the displayed grid, with dips that can be substantial near boundaries. Wilson, Jeffreys and mid-p do not guarantee the strict promise. "
            "<bookmark mark='d'/> And one poor approximation: far below ninety-five for whole ranges of p, which is the "
            "Wald interval. <bookmark mark='e'/> The Coverage Board's verdicts reflect this: kept within Monte Carlo "
            "error, conservative if well above, broken if well below."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def poisson(self):
        from scipy import stats as st

        def garwood(x, a=0.05):
            return (0.0 if x == 0 else st.chi2.ppf(a / 2, 2 * x) / 2, st.chi2.ppf(1 - a / 2, 2 * x + 2) / 2)

        lams = np.linspace(0.1, 10, 300)
        xs = np.arange(0, 60)
        cg, cw = [], []
        for lam in lams:
            pm = st.poisson.pmf(xs, lam)
            cg.append(sum(p for x, p in zip(xs, pm) if garwood(x)[0] <= lam <= garwood(x)[1]))
            cw.append(sum(p for x, p in zip(xs, pm) if x - 1.96 * np.sqrt(x) <= lam <= x + 1.96 * np.sqrt(x)))
        A = axes([0, 10], [0, 1], x_length=7.6, y_length=4.2, xlabel=r"true rate $\lambda$, \ one Poisson count", ylabel=r"exact coverage",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 0.5, 0.95, 1], center=[-2.0, -0.3, 0])
        ax = A.ax
        nom = DashedLine(ax.c2p(0, 0.95), ax.c2p(10, 0.95), color=EXACT, stroke_width=2)
        g1 = polyline(ax, lams, cg, METHOD_COL["clopper_pearson"], 2.2)
        g2 = polyline(ax, lams, cw, METHOD_COL["wald"], 2.2)
        rows = fit_rows(VGroup(
            MathTex(r"\text{Garwood (1936): } \Big[\tfrac12\chi^2_{2x,\,0.025},\ \tfrac12\chi^2_{2x+2,\,0.975}\Big]", font_size=26,
                    color=METHOD_COL["clopper_pearson"]),
            label(rf"never below 95\% \ (min {100 * min(cg):.1f}\%)", font_size=24, color=METHOD_COL["clopper_pearson"]),
            MathTex(r"\text{Wald: } x \pm 1.96\sqrt x", font_size=26, color=METHOD_COL["wald"]),
            label(rf"averages {100 * np.mean(cw):.0f}\%, \ and collapses to $[0,0]$ when $x = 0$", font_size=24, color=METHOD_COL["wald"]),
            MathTex(rf"x = 0:\ \lambda \le {garwood(0)[1]:.2f}", font_size=26),
            label(r"two-sided 95\%: \ 3.69; \ one-sided 95\%: \ 3.00", font_size=22, color=GREY_A),
        ), 5.0, 0.3, [4.4, -0.3, 0])
        with self.voiceover(
            "Counts of events, Poisson rather than binomial, have the same problem and the same cure. <bookmark mark='a'/> "
            "Frank Garwood in 1936 inverted exact Poisson tests, and the chi-squared distribution gives the limits in "
            "closed form. Its coverage, in orange, never falls below ninety-five percent. <bookmark mark='b'/> The Wald "
            "interval, the count plus or minus one point nine six root count, averages eighty-five percent over this range "
            "and is useless when the count is zero. <bookmark mark='c'/> After zero events, Garwood's two-sided upper "
            "limit is three point six nine. The rule of three instead refers to the one-sided ninety-five percent upper bound, minus log point zero five, about three."
        ) as vo:
            self.play(FadeIn(A), Create(nom))
            vo.wait_until("a")
            self.play(Create(g1), FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(Create(g2), FadeIn(rows[2:4]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4:]))
        self.clear_scene()

    def median(self):
        from scipy import stats as st
        n = 20
        covs = [(r, 1 - 2 * st.binom.cdf(r - 1, n, 0.5)) for r in range(4, 9)]
        rows = [
            cmath(r"P\big(X_{(r)} < m < X_{(n+1-r)}\big)", r"=", r"1 - 2\,P\big(\mathrm{Bin}(n, \tfrac12) \le r - 1\big)", font_size=30),
            cmath(r"n = 20,\ r = 6", r":", rf"P = {covs[2][1]:.4f}", r"\quad (X_{(6)}, X_{(15)})", font_size=32),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"each draw is below the median $m$ with chance $\tfrac12$: \ a sign test inverted"),
                why(r"for any continuous distribution; \ $r = 7$ gives only " + f"{covs[3][1]:.3f}")]
        foot = label(r"distribution-free, \ exact, \ and discrete: \ only a few levels are possible \ (Thompson, 1936)", font_size=24,
                     color=GREY_A).to_edge(DOWN, buff=0.6)
        intro = label('Invert the sign test under IID continuous sampling', font_size=36)
        with self.voiceover(
            "One more exact interval, which needs independent identically distributed continuous data, but no parametric shape model. <bookmark mark='a'/> Each observation falls below the "
            "population median with probability one half, whatever the distribution. So the number below the median is "
            "binomial with probability a half, and the interval between the r-th smallest and r-th largest observations "
            "covers the median with a probability we can compute exactly. It's Part 10's sign test, inverted. "
            "<bookmark mark='b'/> With twenty observations, the sixth smallest to the sixth largest covers the median "
            "ninety-five point nine percent of the time, for any continuous distribution. <bookmark mark='c'/> But it's "
            "discrete again: the next choice in only covers eighty-eight percent, so ninety-five exactly isn't available. "
            "William Thompson published it in 1936."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=2, top=1.8, x=0.0, buff=1.0, edge=6.9)
            for k, m_ in enumerate("ab"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
