from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import ro, GAIN, LOSS, PART, TRADE, load, real_data

C_ = {r"\theta_k": QC.HOUSE, r"R^o_t": QC.IDEA, r"\rho_1": QC.IDEA}


def row(*parts, fs=36):
    return cmath(*parts, colors=C_, font_size=fs)


class Business(VoiceoverScene):
    def construct(self):
        fe = load("fees")
        gl = load("glm")
        self.card()
        self.sides()
        self.fees(fe)
        self.option()
        self.shadow(gl)
        self.smooth_math(gl)
        self.mle(gl)

    def card(self):
        c = chapter_card(14, r"Who earns what", r"How does each player get paid, and can returns be too smooth?",
                         lit=(1982, 1990, 2000), part=PART)
        with self.voiceover("Chapter fourteen. Who earns what."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sides(self):
        sell = definition_card(r"Sell side", r"Banks and dealers: make markets, earn spreads and fees, structure "
                               r"products, lend to the buy side. Flow desks live on clients' volume; exotics desks on "
                               r"the margin in complex products. Agency: act for a client; principal: trade against "
                               r"them.", width=5.9, color=TRADE, font_size=20)
        buy = definition_card(r"Buy side", r"Asset managers, pension funds, insurers, hedge funds: invest money and "
                              r"pay the sell side to trade. Paid a fee on assets, and, for hedge funds, a share of "
                              r"profits. Multi-manager platforms often pass their costs through to investors on top.",
                              width=5.9, color=QC.IDEA, font_size=20)
        pair = VGroup(sell, buy).arrange(RIGHT, buff=0.4, aligned_edge=UP).shift(UP * 0.6)
        with self.voiceover(
            "The industry divides in two. The sell side, banks and dealers, makes markets, earns spreads and fees, "
            "designs products and lends to everyone else. Acting as agent it works for the client; as principal it "
            "trades against the client, from its own book. <bookmark mark='a'/> The buy side invests: asset "
            "managers, pension funds, insurers, hedge funds. It charges a fee on assets, and hedge funds take a share "
            "of profits too. The big multi-manager platforms often charge their costs, salaries included, straight "
            "through to investors instead of a fixed management fee."
        ) as vo:
            self.play(FadeIn(sell, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(buy, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def fees(self, fe):
        ys = np.asarray(fe["years"], float)
        wg, wn = np.asarray(fe["wealth_gross"]), np.asarray(fe["wealth_net"])
        g = axes([1926, 2021], [0, 4.2], x_length=7.2, y_length=4.2, ylabel=r"\$1 invested in 1927 (log scale)",
                 xticks=[1930, 1960, 1990, 2020], yticks=[0, 1, 2, 3, 4], xfmt=lambda v: f"{int(v)}",
                 yfmt=lambda v: rf"\${10 ** v:,.0f}".replace(",", "{,}"), font_size=17).to_edge(LEFT, buff=0.6)
        g.shift(DOWN * 0.3)
        ax = g.ax
        k = ValueTracker(0)
        lg = tracing(ax, ys, np.log10(wg), k, TRADE, stroke_width=3)
        ln = tracing(ax, ys, np.log10(wn), k, LOSS, stroke_width=3)
        leg = legend([(TRADE, r"the market, no fees"), (LOSS, r"the same, after 2\% and 20\% (high-water mark)")],
                     font_size=20).to_edge(RIGHT, buff=0.35).shift(UP * 2.2)
        res = VGroup(
            MathTex(rf"\${fe['final_gross']:,.0f}\ \to\ \${fe['final_net']:,.0f}".replace(",", "{,}"), font_size=36),
            MathTex(rf"{100 * fe['geo_gross']:.1f}\%\ \to\ {100 * fe['geo_net']:.1f}\%\ \text{{a year}}", font_size=32),
            MathTex(rf"\text{{the investor keeps}}\ {100 * fe['share_kept']:.1f}\%\ \text{{of the profit}}", font_size=30,
                    color=LOSS),
            MathTex(rf"\text{{a 1\% fee instead:}}\ \${fe['final_1pct']:,.0f}".replace(",", "{,}"), font_size=28, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(leg, DOWN, buff=0.5).align_to(leg, LEFT)
        src = real_data(r"calendar-year returns of the US market, 1927--2020 (Ken French), as a fund's gross returns; "
                        r"fees charged yearly")
        with self.voiceover(
            "Fees compound, just like returns. Take the American market's calendar years from 1927 to 2020 as a "
            f"fund's returns before fees. A dollar becomes {fe['final_gross']:,.0f} dollars. Now charge the classic "
            "hedge-fund fee: two percent of assets a year, and twenty percent of any gain above the fund's previous "
            f"peak, the high-water mark. <bookmark mark='a'/> The same dollar becomes {fe['final_net']:,.0f}. Growth "
            f"falls from {100 * fe['geo_gross']:.1f} percent a year to {100 * fe['geo_net']:.1f}, and the investor "
            f"keeps {100 * fe['share_kept']:.1f} percent of the profit. Even a plain one percent fee leaves "
            f"{fe['final_1pct']:,.0f}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg))
            self.add(lg, ln)
            self.play(k.animate.set_value(len(ys) - 1), run_time=6, rate_func=linear)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in res], lag_ratio=0.4))
        lg.clear_updaters()
        ln.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def option(self):
        g = axes([60, 160], [-2, 12], x_length=6.0, y_length=3.6, xlabel=r"fund value $V_T$ (high-water mark 100)",
                 ylabel=r"performance fee", xticks=[60, 100, 140], yticks=[0, 5, 10], font_size=17)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        pay = curve(ax, [60, 100, 160], [0, 0, 12], QC.HOUSE, stroke_width=4)
        eq = MathTex(r"\text{fee} = \phi\,(V_T - \text{HWM})^+", font_size=40, color=QC.HOUSE).to_edge(RIGHT, buff=0.8).shift(UP * 1.4)
        txt = VGroup(
            label(r"a call option on the fund, struck at its peak", font_size=22),
            label(r"after a loss it is far out of the money:", font_size=22),
            label(r"funds close and relaunch with a fresh mark", font_size=22),
            label(r"the manager is long volatility of the fund", font_size=22, color=LOSS),
            label(r"Fung and Hsieh (1997): hedge-fund returns load on a few", font_size=20, color=GREY_A),
            label(r"dynamic styles, with option-like, nonlinear payoffs", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(eq, DOWN, buff=0.4).align_to(eq, LEFT)
        with self.voiceover(
            "Look at the performance fee as a payoff. Below the high-water mark it pays the manager nothing; above "
            "it, a fifth of the gain. That is a call option on the fund, struck at its peak. <bookmark mark='a'/> "
            "After a bad year the option is far out of the money, which is why funds sometimes close and relaunch "
            "with a fresh mark; and like any option holder, the manager gains from volatility. Fung and Hsieh found "
            "hedge-fund returns themselves look option-like: nonlinear in the market, in ways a linear factor model "
            "misses."
        ) as vo:
            self.play(FadeIn(g), Create(pay), Write(eq))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in txt], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def shadow(self, gl):
        R = np.asarray(gl["R"], float)[:120]
        Ro = np.asarray(gl["Ro"], float)[:118]
        th = np.asarray(gl["theta_true"], float)
        t = np.arange(len(Ro))
        g = axes([0, len(Ro)], [-0.13, 0.13], x_length=7.6, y_length=3.6, xlabel=r"months",
                 ylabel=r"monthly return", yticks=[-0.1, 0, 0.1], yfmt=lambda v: f"{100 * v:+.0f}\\%" if v else "0",
                 font_size=16).to_edge(LEFT, buff=0.6).shift(UP * 0.4)
        ax = g.ax
        k = ValueTracker(0)
        tr = tracing(ax, t, R[2:2 + len(Ro)], k, GREY_B, stroke_width=2)
        rp = tracing(ax, t, Ro, k, QC.IDEA, stroke_width=3)
        leg = legend([(GREY_B, r"true returns"), (QC.IDEA, r"reported: $0.5R_t + 0.3R_{t-1} + 0.2R_{t-2}$")],
                     font_size=18).next_to(g, DOWN, buff=0.3).align_to(g, LEFT)
        sr = ro(r"\text{reported Sharpe} \times", lambda: 1 + (gl["inflate"] - 1) * min(k.get_value() / len(t), 1),
                     digits=2, font_size=32, color=QC.IDEA).to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
        ac = VGroup(
            label(r"stale prices in the wild: lag-1 autocorrelation of daily returns", font_size=20, color=GREY_A),
            MathTex(rf"\text{{smallest size decile: }}{gl['ac1']['early']['small']:.2f}\ (1963\text{{--}}89),\ "
                    rf"{gl['ac1']['late']['small']:.2f}\ (1990\text{{--}}2020)", font_size=24, color=QC.IDEA),
            MathTex(rf"\text{{largest decile: }}{gl['ac1']['early']['big']:.2f},\ {gl['ac1']['late']['big']:.2f}",
                    font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.6)
        src = note(r"simulated: iid normal monthly returns; Ken French size deciles, daily, value-weighted", font_size=15)
        src.to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "Hedge funds report monthly returns on assets that may not trade every day, and illiquid assets get "
            "marked with stale or averaged prices. Watch what that does. The grey line is a fund's true monthly "
            "return; the blue line is what it reports, half this month, a third of last month's, a fifth of the "
            "month before. <bookmark mark='a'/> The reported line is a shadow: same average, less wiggle. Its "
            f"volatility shrinks, and its Sharpe ratio rises by a factor of {gl['inflate']:.2f}, with no extra skill "
            "at all. <bookmark mark='b'/> It happens in plain stock indices too. The smallest decile of American "
            f"stocks had a daily autocorrelation of {gl['ac1']['early']['small']:.2f} before 1990, when many of them "
            f"traded rarely; since then, {gl['ac1']['late']['small']:.2f}. Stale prices are smoothing in the wild."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(sr), FadeIn(src))
            self.add(tr, rp)
            vo.wait_until("a")
            self.play(k.animate.set_value(len(t) - 1), run_time=6, rate_func=linear)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(a_) for a_ in ac], lag_ratio=0.3))
        for m in (tr, rp, sr):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def smooth_math(self, gl):
        rows = [
            row(r"R^o_t", r"=", r"\sum_{k=0}^{2}", r"\theta_k", r"R_{t-k},\qquad \textstyle\sum \theta_k = 1"),
            row(r"\operatorname{Var} R^o", r"=", r"\sigma^2 \sum \theta_k^2 \ \le\ \sigma^2"),
            row(r"\rho_1", r"=", r"\frac{\theta_0\theta_1 + \theta_1\theta_2}{\sum \theta_k^2}"),
            row(r"\text{SR}^o", r"=", r"\frac{\text{SR}}{\sqrt{\sum \theta_k^2}}"),
        ]
        whys = [why(r"Getmansky, Lo and Makarov (2004): reported returns average the true ones", font_size=20),
                why(r"iid true returns: the weights' squares sum to less than one", font_size=20),
                why(r"the MA(2) autocovariance at lag one, over the variance", font_size=20),
                why(r"same mean, less volatility: $\theta = (0.5, 0.3, 0.2)$ gives $\times 1.62$", font_size=20)]
        step = ladder(self, rows, whys, keep=4, top=2.7, x=-1.4, buff=0.5, edge=6.9)
        with self.voiceover(
            "The model is Getmansky, Lo and Makarov's. Reported returns are a weighted average of the true ones, "
            "weights summing to one. <bookmark mark='a'/> With independent true returns, the reported variance is "
            "sigma squared times the sum of the squared weights, which is less than one. <bookmark mark='b'/> And "
            "smoothing leaves a fingerprint: positive autocorrelation, computed from the weights. "
            "<bookmark mark='c'/> The mean is untouched, so the Sharpe ratio is inflated by one over the square root "
            "of the sum of squared weights: one point six two for these weights."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def mle(self, gl):
        paths = np.asarray(gl["paths"], float)        # seeds x iterations x 3
        moms = np.asarray(gl["moments"], float)
        th = np.asarray(gl["theta_true"], float)
        n_it = paths.shape[1]
        err = np.sqrt(((paths - th[None, None, :]) ** 2).sum(2))
        steps = np.arange(n_it)
        ck = sorted(set([0, 1, 2, 3, n_it // 2, n_it - 1]))
        A, B, C = np.array([-1.6, -1.4, 0]), np.array([1.6, -1.4, 0]), np.array([0, 1.4, 0])

        def tri(p):
            p = np.asarray(p, float)
            return p[0] * A + p[1] * B + p[2] * C

        def frame(i):
            j = ck[i]
            g = VGroup(Polygon(A, B, C, stroke_color=GREY_B, stroke_width=2, fill_opacity=0))
            g.add(label(r"$\theta_0$", font_size=20).next_to(A, DL, buff=0.05),
                  label(r"$\theta_1$", font_size=20).next_to(B, DR, buff=0.05),
                  label(r"$\theta_2$", font_size=20).next_to(C, UP, buff=0.05))
            g.add(Star(n=5, outer_radius=0.13, color=YELLOW, fill_opacity=1).move_to(tri(th)))
            for s in range(len(paths)):
                g.add(Dot(tri(paths[s, j]), radius=0.06, color=QC.HOUSE))
            if i == len(ck) - 1:
                for s in range(len(moms)):
                    g.add(Dot(tri(moms[s]), radius=0.05, color=GREY_B))
            return g
        rp = TrainingReplay(steps, err, frame, ck, ylabel=r"distance to the true $\theta$", xlabel=r"BFGS iteration",
                            color=QC.HOUSE, left=LEFT * 3.4 + DOWN * 0.2, right=RIGHT * 3.4 + UP * 0.8, x_length=4.6,
                            y_length=2.8)
        sm = np.asarray(gl["small_theta"], float)
        res = VGroup(
            MathTex(rf"\text{{smallest decile, monthly 1963--89: }}\hat\theta = ({sm[0]:.2f}, {sm[1]:.2f}, {sm[2]:.2f})",
                    font_size=24, color=QC.IDEA),
            MathTex(rf"\text{{Sharpe inflated}} \times {gl['small_inflate']:.2f}", font_size=26, color=QC.IDEA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DR, buff=0.35)
        leg = legend([(QC.HOUSE, r"likelihood fits, 5 seeds"), (GREY_B, r"moment estimator (baseline)"),
                      (YELLOW, r"the true $\theta$")], font_size=17).to_corner(UL, buff=0.35)
        q = desk_question(r"A fund's monthly returns have autocorrelation 0.4. Is its true volatility higher or lower "
                          r"than reported, and by how much?", width=6.0, font_size=19).to_corner(DL, buff=0.25)
        with self.voiceover(
            "Can we undo it? Fit the weights by maximum likelihood, as a moving-average model, on five simulated "
            "funds of six hundred months each. Each dot is a seed's estimate on the triangle of possible weights; "
            "the star is the truth. <bookmark mark='a'/> The optimizer walks every seed to the star within a few "
            "iterations, and the simpler moment estimator, in grey, lands close too. <bookmark mark='b'/> On the "
            "smallest decile's monthly returns before 1990 the fit puts "
            f"{100 * sm[0]:.0f} percent of the weight on the current month and inflates the Sharpe ratio "
            f"{gl['small_inflate']:.2f} times. Pause and predict: a fund with autocorrelation point four. Higher or "
            "lower true volatility, and by how much?"
        ) as vo:
            self.play(FadeIn(rp), FadeIn(leg))
            vo.wait_until("a")
            rp.play(self, run_time=5)
            vo.wait_until("b")
            self.play(FadeIn(res))
            self.play(FadeIn(q))
        self.wait(1.0)
        self.clear_scene()
