from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import DRIFT, INFO, LOSS, MART, P_C, PART, Q_C, load, real_data


class Convergence(VoiceoverScene):
    def construct(self):
        p = load("polya")
        dp = load("drift_posterior")
        self.card()
        self.trader(p)
        self.lemma()
        self.urns(p)
        self.learner(dp)

    def card(self):
        c = chapter_card(10, r"Martingales converge", r"Can a fair game wander forever?", lit=(1953,), part=PART)
        with self.voiceover("Chapter ten. Martingales converge."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def trader(self, p):
        w = np.asarray(p["walk"], float)
        n = len(w) - 1
        lo, hi = float(np.floor(w.min())) - 1, float(np.ceil(w.max())) + 1
        g = axes([0, n], [lo, hi], x_length=9.0, y_length=3.0, ylabel=r"a martingale $M_n$", xticks=[], yticks=[-3, 3],
                 font_size=16).to_edge(UP, buff=0.6).to_edge(LEFT, buff=0.8)
        ax = g.ax
        bandm = Polygon(ax.c2p(0, -3), ax.c2p(n, -3), ax.c2p(n, 3), ax.c2p(0, 3), stroke_width=0, fill_color=INFO,
                        fill_opacity=0.12)
        la = DashedLine(ax.c2p(0, -3), ax.c2p(n, -3), color=QC.GAIN, stroke_width=1.5)
        lb = DashedLine(ax.c2p(0, 3), ax.c2p(n, 3), color=LOSS, stroke_width=1.5)
        tk = ValueTracker(0.0)
        path = tracing(ax, np.arange(n + 1), w, tk, P_C, stroke_width=2.5)
        wealth = np.asarray(p["trader"], float)
        g2 = axes([0, n], [float(min(wealth.min(), -2)), float(wealth.max()) + 2], x_length=9.0, y_length=1.9,
                  ylabel=r"the upcrossing trader's P\&L", xlabel=r"steps", xticks=[0, n], yticks=[0], font_size=16)
        g2.next_to(g, DOWN, buff=0.55).align_to(g, LEFT)
        pl = tracing(g2.ax, np.arange(n + 1), wealth, tk, QC.IDEA, stroke_width=2.5)
        trades = VGroup()
        for a_, b_ in zip(p["starts"], p["ends"]):
            seg = curve(ax, np.arange(a_, b_ + 1), w[a_:b_ + 1], QC.IDEA, stroke_width=4)
            trades.add(VGroup(seg, Dot(ax.c2p(a_, w[a_]), radius=0.06, color=QC.GAIN),
                              Dot(ax.c2p(b_, w[b_]), radius=0.06, color=LOSS)))
        cnt = always_redraw(lambda: MathTex(
            rf"\text{{upcrossings of }} [-3, 3]: {sum(1 for e in p['ends'] if e <= tk.get_value())}", font_size=28,
            color=QC.IDEA).next_to(g, RIGHT, buff=0.3).align_to(g, UP))
        rule = label(r"buy 1 below $a = -3$, sell above $b = 3$; repeat", font_size=20, color=GREY_A).next_to(
            cnt, DOWN, buff=0.2).align_to(cnt, LEFT)
        with self.voiceover(
            "Can a fair game wander forever without settling? Doob's answer is a trading strategy. Draw a band from a "
            "to b; buy one unit when the martingale dips below a, sell when it rises above b. <bookmark mark='a'/> "
            "Each completed round trip, an upcrossing, earns at least b minus a; the only loss is on a last trade "
            "still open. <bookmark mark='b'/> But the stake is decided from the past, so by chapter four the trader "
            "plays a fair game. Its profit cannot grow on average, so the upcrossings cannot pile up without limit."
        ) as vo:
            self.play(FadeIn(g), FadeIn(bandm), Create(la), Create(lb), FadeIn(g2), FadeIn(rule))
            self.add(path, pl, cnt)
            vo.wait_until("a")
            self.play(tk.animate.set_value(float(n)), run_time=7, rate_func=linear)
            for m_ in (path, pl, cnt):
                m_.clear_updaters()
            self.play(LaggedStart(*[FadeIn(t_) for t_ in trades], lag_ratio=0.3))
            vo.wait_until("b")
        self.wait(0.4)
        self.clear_scene()

    def lemma(self):
        rows = [cmath(r"(H \cdot M)_n", r"\ge", r"(b - a)\,U_n[a, b] - (M_n - a)^-", font_size=38),
                cmath(r"0 \ge \mathbb{E}(H \cdot M)_n", r"\Rightarrow",
                      r"(b - a)\,\mathbb{E}U_n \le \mathbb{E}(M_n - a)^-", font_size=38,
                      colors={r"(b - a)\,\mathbb{E}U_n \le \mathbb{E}(M_n - a)^-": MART}),
                cmath(r"\sup_n \mathbb{E}|M_n| < \infty", r"\Rightarrow",
                      r"U_\infty[a, b] < \infty \ \ \forall a < b \text{ rational} \Rightarrow M_n \to M_\infty", font_size=36),
                cmath(r"L_n \to 0,\ \mathbb{E}L_n = 1", r":", r"\text{UI} \iff L^1 \iff M_n = \mathbb{E}[M_\infty \mid \mathcal{F}_n]",
                      font_size=36, colors={r"\text{UI} \iff L^1 \iff M_n = \mathbb{E}[M_\infty \mid \mathcal{F}_n]": LOSS})]
        whys = [why(r"each upcrossing earns at least $b - a$; the open trade loses at most $(M_n - a)^-$"),
                why(r"a supermartingale transform has non-positive mean (chapter 4): Doob's upcrossing lemma"),
                why(r"finitely many crossings of every rational band: no room to oscillate (Doob's forward convergence "
                    r"theorem)"),
                why(r"convergence need not keep the mean (chapter 12); uniform integrability is exactly what does")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.6, buff=0.72, edge=6.9)
        head = label(r"Williams, ch.\ 11 and 13--14", font_size=22, color=GREY_B).to_edge(UP, buff=0.25)
        with self.voiceover(
            "Written out, this is Doob's upcrossing lemma. The trader's wealth is at least b minus a times the "
            "number of upcrossings, minus the loss on the open trade. <bookmark mark='a'/> For a supermartingale the "
            "expected wealth is at most zero, so the expected number of upcrossings is bounded by the expected "
            "shortfall below a over the width of the band. <bookmark mark='b'/> If the martingale's mean size stays "
            "bounded, every band with rational ends is crossed only finitely often, so the path cannot oscillate: it "
            "converges. That is Doob's forward convergence theorem. <bookmark mark='c'/> But converging is not "
            "keeping the mean: in chapter twelve a fair gambler's wealth goes to zero while its mean stays one. "
            "Uniform integrability is exactly what keeps it."
        ) as vo:
            self.play(FadeIn(head))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def urns(self, p):
        S = np.asarray(p["show"], float)
        k = S.shape[1]
        draws = np.arange(k) * 10
        g = axes([0, 2000], [0, 1], x_length=7.0, y_length=4.4, xlabel=r"draws", ylabel=r"red fraction in 100 P\'olya "
                 r"urns", xticks=[0, 1000, 2000], yticks=[0, 0.5, 1], font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        tk = ValueTracker(0.0)
        cols = color_gradient([LOSS, Q_C, P_C], len(S))
        lines = VGroup(*[tracing(ax, draws, row, tk, c, stroke_width=1.2) for row, c in zip(S, cols)])
        for ln in lines:
            ln.set_stroke(opacity=0.5)
        h = np.asarray(p["limits_hist"], float)
        h = h / h.max()
        hist = VGroup()
        for i, v in enumerate(h):
            y0, y1 = ax.c2p(0, i / 20)[1], ax.c2p(0, (i + 1) / 20)[1]
            hist.add(Rectangle(width=1.4 * v, height=y1 - y0 - 0.01, stroke_width=0, fill_color=MART,
                               fill_opacity=0.75).move_to([ax.get_right()[0] + 0.2 + 0.7 * v, (y0 + y1) / 2, 0]))
        side = VGroup(
            MathTex(r"\mathbb{E}[R_{n+1} \mid \mathcal{F}_n] = R_n + \frac{R_n}{n + 2}", font_size=30),
            MathTex(r"\Rightarrow \frac{R_n}{n + 2} \text{ is a bounded martingale}", font_size=30, color=MART),
            label(r"the limits of 10{,}000 urns (right):", font_size=20, color=GREY_A),
            MathTex(rf"\text{{flat: K--S distance from Uniform}}(0,1) = {p['ks']:.3f}", font_size=26, color=MART),
            MathTex(rf"P(\text{{limit}} > 0.9) = {p['p_above_09']:.3f}", font_size=26, color=QC.IDEA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        pred = desk_question(r"P\'olya's urn from one red and one blue: chance the red fraction ends above 90\%?",
                             r"10\%: the limit is uniform on $[0, 1]$.", width=5.4, font_size=20)
        pred.next_to(side, DOWN, buff=0.3).align_to(side, LEFT)
        with self.voiceover(
            "The famous convergent martingale is an urn: one red ball, one blue; draw one, put it back with another "
            "of its colour. <bookmark mark='a'/> The red fraction is a martingale, bounded between zero and one, so "
            "it converges. <bookmark mark='b'/> A hundred urns jump about, then each freezes at its own level: the "
            "urn remembers its first draws forever. <bookmark mark='c'/> The limits of ten thousand urns are flat, "
            "uniform. So the chance the red fraction ends above ninety percent is ten percent; simulated, "
            f"{100 * p['p_above_09']:.1f}."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(side[:2]))
            vo.wait_until("b")
            self.add(lines)
            self.play(tk.animate.set_value(float(k - 1)), run_time=7, rate_func=lambda u: u ** 0.6)
            for ln in lines:
                ln.clear_updaters()
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in hist], lag_ratio=0.05), FadeIn(side[2:]))
            self.play(FadeIn(pred, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def learner(self, dp):
        t = np.asarray(dp["t"])
        m, lo, hi = (100 * np.asarray(dp[k]) for k in ("mean_ann", "lo_ann", "hi_ann"))
        g = axes([1926, 2021], [-40, 60], x_length=8.2, y_length=4.4, ylabel=r"the market's mean return, as learned "
                 r"so far (\% a year)", xticks=[1930, 1960, 1990, 2020], xfmt=lambda x: f"{int(x)}",
                 yticks=[-40, -20, 0, 20, 40, 60], font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        tk = ValueTracker(0.0)

        def bandm():
            i = int(np.clip(tk.get_value(), 1, len(t) - 1))
            return band(ax, t[:i + 1], np.clip(lo[:i + 1], -40, 60), np.clip(hi[:i + 1], -40, 60), MART, 0.25)

        bd = always_redraw(bandm)
        ln = tracing(ax, t, np.clip(m, -40, 60), tk, MART, stroke_width=3)
        yr = always_redraw(lambda: MathTex(rf"{int(at_index(t, tk))}:\ {at_index(m, tk):.1f}\% \pm "
                                           rf"{(at_index(hi, tk) - at_index(lo, tk)) / 2:.1f}\%", font_size=30,
                                           color=MART).to_corner(UR, buff=0.5))
        side = VGroup(
            label(r"L\'evy's upward theorem: $\mathbb{E}[X \mid \mathcal{F}_n] \to \mathbb{E}[X \mid \mathcal{F}_\infty]$",
                  font_size=22, color=GREY_A),
            label(r"a Bayesian's estimate is a Doob martingale (under the model), so it converges: learning", font_size=19,
                  color=GREY_A),
            MathTex(rf"\pm\ \text{{after 10 years: }} {100 * dp['half_1936']:.1f}\%", font_size=26),
            MathTex(rf"\pm\ \text{{after 50 years: }} {100 * dp['half_1976']:.1f}\%", font_size=26),
            MathTex(rf"\text{{2020: }} {100 * dp['end_mean']:.1f}\% \pm {100 * dp['end_half']:.1f}\%", font_size=28,
                    color=MART),
            wrapped_label(r"the drift is learnable only over decades (Merton 1980): it narrows like $1/\sqrt{t}$", 4.4, 19,
                          GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.5)
        for s_ in side[:2]:
            if s_.width > 4.6:
                s_.scale_to_fit_width(4.6)
        src = real_data(r"Kenneth French's daily US market; prior $N(0, (10\text{ bp})^2)$ a day; daily variance known "
                        r"from an EWMA the day before")
        with self.voiceover(
            "Lévy's upward theorem: a forecast refined by information converges to what full information would say. "
            "That is learning. A Bayesian estimates the market's mean return, from a prior centred on zero, updating "
            "every day since 1926; its estimate is a Doob martingale under the model. <bookmark mark='a'/> The band "
            f"narrows like one over the square root of time: plus or minus {100 * dp['half_1936']:.0f} percent a year "
            f"after ten years, {100 * dp['half_1976']:.1f} after fifty. <bookmark mark='b'/> By 2020: "
            f"{100 * dp['end_mean']:.1f} percent a year, give or take {100 * dp['end_half']:.1f}. Drifts are learnable "
            "only over decades, as Robert Merton warned in 1980."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[:2]))
            self.add(bd, ln, yr)
            vo.wait_until("a")
            i36 = float(np.searchsorted(t, 1936.0))
            i76 = float(np.searchsorted(t, 1976.0))
            self.play(tk.animate.set_value(i36), run_time=2.5, rate_func=linear)
            self.play(FadeIn(side[2]))
            self.play(tk.animate.set_value(i76), run_time=3, rate_func=linear)
            self.play(FadeIn(side[3]))
            vo.wait_until("b")
            self.play(tk.animate.set_value(float(len(t) - 1)), run_time=3, rate_func=linear)
            for m_ in (bd, ln, yr):
                m_.clear_updaters()
            self.play(FadeIn(side[4:]))
        self.wait(0.4)
        self.clear_scene()
