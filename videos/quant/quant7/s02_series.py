from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load, real_data


class Series(VoiceoverScene):
    def construct(self):
        s = load("spurious")
        u = load("unitroot")
        self.card()
        self.funnel()
        self.df_stream(u)
        self.derive()
        self.augment()
        self.lab(u)
        self.spurious(s, u)

    def card(self):
        c = chapter_card(2, r"Unit roots and spurious regression", r"Why do trending series fool regressions?",
                         part=PART)
        with self.voiceover("Chapter two. Unit roots, and the regression that lies."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def funnel(self):
        rng = np.random.default_rng(4)
        n, m = 300, 60
        E = rng.standard_normal((m, n))
        W = np.cumsum(E, 1)
        A = np.zeros((m, n))
        for t in range(1, n):
            A[:, t] = 0.8 * A[:, t - 1] + E[:, t]
        tt = np.arange(n)
        mk = lambda tex, col: axes([0, n], [-45, 45], x_length=5.8, y_length=3.6, xticks=[], yticks=[-30, 0, 30],  # noqa: E731
                                   font_size=14, ylabel=tex)
        g1, g2 = mk(r"$x_t = 0.8\,x_{t-1} + \varepsilon_t$: 60 paths (simulated)", VOL), \
            mk(r"$x_t = x_{t-1} + \varepsilon_t$: 60 paths (simulated)", RET)
        VGroup(g1, g2).arrange(RIGHT, buff=0.8).shift(UP * 0.5)
        f1 = path_fan(g1.ax, tt, np.clip(A, -45, 45), VOL, opacity=0.3)
        f2 = path_fan(g2.ax, tt, np.clip(W, -45, 45), RET, opacity=0.3)
        env = VGroup(curve(g2.ax, tt, 2 * np.sqrt(tt), BAD, stroke_width=3), curve(g2.ax, tt, -2 * np.sqrt(tt), BAD, stroke_width=3))
        e1 = VGroup(curve(g1.ax, tt, np.full(n, 2 / np.sqrt(1 - 0.64)), GOOD, stroke_width=3),
                    curve(g1.ax, tt, np.full(n, -2 / np.sqrt(1 - 0.64)), GOOD, stroke_width=3))
        c1 = label(r"variance $\sigma^2/(1-\phi^2)$: a band", font_size=20, color=GOOD).next_to(g1, DOWN, buff=0.2)
        c2 = label(r"variance $t\sigma^2$: a funnel $\pm 2\sqrt{t}$", font_size=20, color=BAD).next_to(g2, DOWN, buff=0.2)
        with self.voiceover(
            "Let phi reach one, and the spring snaps. On the left, sixty stationary paths, inside a band. <bookmark mark='a'/> On the right, sixty random walks from the same shocks. Every "
            "shock is permanent, and the paths fan out in a funnel that widens like the square root of t. This is a unit root, and log prices have one."
        ) as vo:
            self.play(FadeIn(g1), Create(f1, lag_ratio=0.02), run_time=2.5)
            self.play(Create(e1), FadeIn(c1))
            vo.wait_until("a")
            self.play(FadeIn(g2), Create(f2, lag_ratio=0.02), run_time=2.5)
            self.play(Create(env), FadeIn(c2))
        self.wait(0.3)
        self.clear_scene()

    def df_stream(self, u):
        edges = np.asarray(u["edges"])
        w = edges[1] - edges[0]
        hists = [np.asarray(h, float) for h in u["hists"]]
        dens = [h / (h.sum() * w) for h in hists]
        g = axes([-5, 3], [0, 0.6], x_length=8.6, y_length=4.2, xticks=[-4, -2.86, -1.64, 0, 2],
                 xfmt=lambda v: f"{v:g}", yticks=[], xlabel=r"Dickey--Fuller $t$-statistic on a true random walk ($T = 500$)",
                 font_size=17).to_edge(LEFT, buff=0.5).shift(DOWN * 0.1)
        ax = g.ax

        def hist(d):
            return VGroup(*[Rectangle(width=ax.c2p(w, 0)[0] - ax.c2p(0, 0)[0], height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.001),
                                      stroke_width=0, fill_color=RET, fill_opacity=0.75).move_to(
                ax.c2p(e + w / 2, v / 2)) for e, v in zip(edges[:-1], d)])

        h = hist(dens[0])
        xs = np.linspace(-5, 3, 200)
        normal = DashedVMobject(curve(ax, xs, np.exp(-xs ** 2 / 2) / np.sqrt(2 * np.pi), GREY_A, stroke_width=3), num_dashes=60)
        nlab = label(r"$N(0,1)$, what a $t$-statistic should be", font_size=18, color=GREY_A).next_to(ax.c2p(1.2, 0.42), RIGHT, buff=0.05)
        cnt = MathTex(rf"{u['snaps'][0]:,}".replace(",", "{,}") + r"\text{ walks}", font_size=30).to_corner(UR, buff=0.6)
        q05 = u["q05"]
        line = DashedLine(ax.c2p(q05, 0), ax.c2p(q05, 0.55), color=BAD, stroke_width=3)
        side = VGroup(
            MathTex(rf"5\%\text{{ quantile: }} {q05:.2f}", font_size=30, color=BAD),
            MathTex(rf"\text{{mean: }} {u['mean']:.2f}", font_size=28, color=RET),
            label(rf"{100 * u['share_below_1645']:.0f}\% fall below $-1.645$, the normal 5\% point", font_size=20, color=GREY_A),
            label(r"Dickey and Fuller (1979); MacKinnon's tables: $-2.86$", font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.3)
        with self.voiceover(
            "To test for a unit root, regress the change on yesterday's level and look at the coefficient's "
            "t-statistic. Under the unit root it is not normal. Watch. Twenty thousand simulated random walks, each regressed, their "
            "t-statistics piling up. <bookmark mark='a'/> The pile sits to the left of the normal curve and is skewed. "
            f"Its mean is about {u['mean']:.1f}, not zero, and {100 * u['share_below_1645']:.0f} percent of the walks "
            "would be rejected at the textbook five percent level. <bookmark mark='b'/> The true five percent point "
            f"settles at {q05:.2f}, the number David Dickey and Wayne Fuller tabulated in 1979."
        ) as vo:
            self.play(FadeIn(g), Create(normal), FadeIn(nlab), FadeIn(h), FadeIn(cnt))
            for k in range(1, len(hists)):
                c2 = MathTex(rf"{u['snaps'][k]:,}".replace(",", "{,}") + r"\text{ walks}", font_size=30).move_to(cnt)
                self.play(Transform(h, hist(dens[k])), Transform(cnt, c2), run_time=0.9)
            vo.wait_until("a")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(side[0]), FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"\sum x_{t-1}\varepsilon_t", r"=", r"\tfrac12\Big(x_T^2 - \sum\varepsilon_t^2\Big)", font_size=36),
            cmath(r"T^{-1/2}\,x_{\lfloor rT\rfloor}", r"\Rightarrow", r"\sigma W(r)", font_size=36),
            cmath(r"T(\hat\rho - 1)", r"=", r"\frac{T^{-1}\sum x_{t-1}\varepsilon_t}{T^{-2}\sum x_{t-1}^2} \Rightarrow "
                  r"\frac{\tfrac12\big(W(1)^2 - 1\big)}{\int_0^1 W(r)^2\,dr}", font_size=36),
            cmath(r"t_{DF}", r"\Rightarrow", r"\frac{\tfrac12\big(W(1)^2 - 1\big)}{\sqrt{\int_0^1 W(r)^2\,dr}}", font_size=36),
            cmath(r"\Pr\big(W(1)^2 < 1\big)", r"=", r"0.68", font_size=36),
        ]
        whys = [why(r"square $x_t = x_{t-1} + \varepsilon_t$ and add up: the sum telescopes"),
                why(r"Donsker: a scaled random walk is a Brownian motion"),
                why(r"continuous mapping; $T^{-1}\sum\varepsilon_t^2 \to \sigma^2$"),
                why(r"the same limit, divided by the standard error"),
                why(r"so the numerator is usually negative: the distribution is skewed left")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-2.4, buff=0.55, edge=6.9)
        with self.voiceover(
            "Why it is not normal. Square the walk and add up: the cross term telescopes. <bookmark mark='a'/> "
            "Scale the walk by the square root of T, and Donsker's theorem turns it into a Brownian motion. "
            "<bookmark mark='b'/> So the estimated coefficient, scaled by T, converges to a ratio of two random "
            "quantities built from that Brownian path, <bookmark mark='c'/> and so does the t-statistic. "
            "<bookmark mark='d'/> The numerator is a half of W of one squared minus one, and W of one squared is "
            "below one about two thirds of the time. The statistic leans left, as the simulation drew."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.3)
        self.clear_scene()

    def lab(self, u):
        card = lab_card(r"the augmented Dickey--Fuller test", [
            "def adf(x, lags=1):",
            "    dx = np.diff(x); n = len(dx); rows = n - lags",
            "    X = [np.ones(rows), x[lags:-1]]",
            "    X += [dx[lags-k-1:n-k-1] for k in range(lags)]",
            "    X, y = np.column_stack(X), dx[lags:]",
            "    beta, *_ = np.linalg.lstsq(X, y, rcond=None)",
            "    s2 = (y - X @ beta) @ (y - X @ beta) / (rows - X.shape[1])",
            "    t = beta[1] / np.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])",
            "    return {'t': t, 'reject_5pct': t < -2.86}",
        ], source="explainer/quant/house/vol.py", width=7.0).to_corner(UL, buff=0.3)
        A = u["adf"]
        names = [("btc", "Bitcoin, log price 2017--20"), ("us", "US market, log index 1926--2020"),
                 ("y10", "10-year Treasury yield 1962--2020"), ("vix", "log VIX 1990--2020")]
        outs = [f"{n_:<34s} t = {A[k]['t']:6.2f}   {'reject' if A[k]['reject_5pct'] else 'unit root'}"
                for k, n_ in names]
        pc = pause_card(r"The 10-year yield cannot go to infinity. Does it have a unit root?", width=5.6, font_size=22)
        pc.to_corner(UR, buff=0.3)
        y10_line = ("The ten-year yield: over sixty years the test cannot tell it from a random walk. Bounded in "
                    "principle, a unit root in practice: tests have little power when phi is close to one."
                    if not A["y10"]["reject_5pct"] else "The ten-year yield: the test rejects, the yield is pulled back.")
        vix_line = ("it rejects decisively: fear mean-reverts." if A["vix"]["reject_5pct"] else
                    "even it does not reject a unit root.")
        with self.voiceover(
            f"Lab. The House's test: regress the change on a constant, yesterday's level and five lagged changes, and "
            f"compare the t-statistic with minus two point eight six. Run it on four series. <bookmark mark='a'/> Pause "
            f"and predict first: the ten-year Treasury yield can't go to infinity. Does it have a unit root? <bookmark "
            f"mark='b'/> Bitcoin's log price and the stock market's log index: unit roots, as expected. {y10_line} As "
            f"for the VIX: {vix_line}"
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(pc))
            vo.wait_until("b")
            lab_run(self, card, outs, run_time=3)
        self.wait(0.3)
        self.clear_scene()

    def spurious(self, s, u):
        Ts = np.asarray(u["Ts"])
        mt = np.asarray(u["phillips_t"])
        g = axes([0, 2100], [0, 22], x_length=5.6, y_length=2.6, xticks=[50, 500, 1000, 2000], yticks=[0, 10, 20],
                 xlabel=r"sample length $T$", ylabel=r"median $|t|$, independent walks", font_size=15)
        g.to_corner(UL, buff=0.45)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(T, v), radius=0.07, color=BAD) for T, v in zip(Ts, mt)])
        root = curve(ax, np.linspace(50, 2050, 100), mt[0] * np.sqrt(np.linspace(50, 2050, 100) / Ts[0]), GREY_B, stroke_width=2)
        rlab = label(r"$\propto\sqrt{T}$ (Phillips 1986)", font_size=18, color=GREY_B).next_to(ax.c2p(1300, 17), UP, buff=0.05)
        sl = np.asarray(u["slopes"])
        g2 = axes([50, 2000], [-2.5, 0.5], x_length=5.6, y_length=1.9, xticks=[50, 1000, 2000], yticks=[-2, -1, 0],
                  xlabel=r"$T$", ylabel=r"fitted slope, one pair of independent walks", font_size=15)
        g2.next_to(g, DOWN, buff=0.4).align_to(g, LEFT)
        sline = curve(g2.ax, np.arange(50, 2001, 25)[:len(sl)], np.clip(sl, -2.5, 0.5), FC, stroke_width=3)
        bl, bd = s["btc_levels"], s["btc_diffs"]
        side = VGroup(
            label(r"2{,}000 pairs of independent random walks ($T = 500$):", font_size=21, color=GREY_A),
            MathTex(rf"\text{{levels: }} |t| > 1.96 \text{{ in }} {100 * s['rej_levels']:.0f}\%", font_size=30, color=BAD),
            MathTex(rf"\text{{differences: }} {100 * s['rej_diffs']:.0f}\%", font_size=30, color=GOOD),
            label(rf"median $R^2$ in levels: {s['median_r2']:.2f}", font_size=21, color=GREY_A),
            label(r"Bitcoin on the US market, 2017--2020:", font_size=21, color=GREY_A),
            MathTex(rf"\text{{levels: }} t = {bl['t']:.0f},\ R^2 = {bl['r2']:.2f}", font_size=28, color=BAD),
            MathTex(rf"\text{{daily changes: }} t = {bd['t']:.1f},\ R^2 = {bd['r2']:.2f}", font_size=28, color=GOOD),
            wrapped_label(r"Granger and Newbold (1974): difference the series, or test for cointegration", 5.6, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        side[4:].shift(DOWN * 0.25)
        side.to_edge(RIGHT, buff=0.4)
        grow = mt[-1] / mt[0]
        with self.voiceover(
            "Unit roots matter because regressing one wandering series on another is a trap. Clive Granger and Paul "
            "Newbold showed it in 1974. Take two thousand pairs of random walks that have nothing to do with each "
            f"other, and regress one on the other. The t-statistic exceeds two in {100 * s['rej_levels']:.0f} percent "
            "of them. In changes, five percent, as it should be. <bookmark mark='a'/> Peter Phillips proved why in "
            "1986: in levels, the slope does not converge to zero but to a random number, so as the sample grows the "
            f"t-statistic grows like the square root of T. From fifty days to two thousand it grows {grow:.1f}-fold. "
            "<bookmark mark='b'/> More data, a more confident lie. <bookmark mark='c'/> Bitcoin against the "
            "American stock market, in log levels: a t-statistic of twenty-four. In daily changes the link is real but "
            "weak: five percent of the variance, most of it from 2020."
        ) as vo:
            self.play(FadeIn(side[:4]))
            vo.wait_until("a")
            self.play(FadeIn(g), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.3), run_time=2)
            self.play(Create(root), FadeIn(rlab))
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(sline), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[4:]))
        self.wait(0.3)
        self.clear_scene()

    def augment(self):
        rows = [
            cmath(r"\Delta x_t", r"=", r"\gamma\,x_{t-1} + \varepsilon_t", font_size=36),
            cmath(r"\Delta x_t", r"=", r"a + \gamma\,x_{t-1} + \varepsilon_t", font_size=36),
            cmath(r"\Delta x_t", r"=", r"a + bt + \gamma\,x_{t-1} + \textstyle\sum_{k=1}^{p} c_k\,\Delta x_{t-k} + \varepsilon_t",
                  font_size=36),
        ]
        whys = [why(r"no constant: 5\% critical value $-1.94$"),
                why(r"with a constant (a non-zero mean under the alternative): $-2.86$"),
                why(r"with a trend: $-3.41$; lagged changes soak up autocorrelation (Said and Dickey 1984)")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-2.4, buff=0.6, edge=6.9)
        with self.voiceover(
            "Two practical details. The critical value depends on what else is in the regression. With no "
            "constant, the five percent point is minus one point nine four. <bookmark mark='a'/> With a constant, "
            "which allows the series a non-zero mean, it is minus two point eight six, the number we simulated. "
            "<bookmark mark='b'/> With a time trend as well, minus three point four one: each deterministic term "
            "the regression must estimate pushes the distribution further left. And if the changes are themselves "
            "autocorrelated, the plain test is distorted, so the augmented test adds lagged changes, enough to whiten "
            "the residuals. Choosing the terms wrongly is the most common way to get a unit-root test wrong."
            " Yet two series with unit roots can still be tied together. Next: cointegration."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.3)
        self.clear_scene()
