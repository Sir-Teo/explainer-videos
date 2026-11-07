from __future__ import annotations

from datetime import date

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, load, real_data


class Replicate(VoiceoverScene):
    def construct(self):
        r = load("replication")
        self.card()
        self.ledger(r)
        self.lab(r)
        self.scatter(r)
        self.derive(r)
        self.volswap(r)

    def card(self):
        c = chapter_card(10, r"Replicating on real Bitcoin; volatility swaps", r"Does the strip really pay variance?",
                         part=PART)
        with self.voiceover("Chapter ten. Replicating a variance swap on real Bitcoin, and the volatility swap."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def ledger(self, r):
        R = r["replay"]
        S = np.asarray(R["S"])
        strip, hedge, rv = (np.asarray(R[x]) for x in ("strip", "hedge", "rv"))
        n = len(S)
        hrs = np.arange(n) / 24
        g1 = axes([0, 30], [S.min() * 0.97, S.max() * 1.03], x_length=6.2, y_length=2.6, ylabel=r"BTCUSDT, hourly",
                  xticks=[0, 10, 20, 30], yticks=[], font_size=15).to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.6)
        lo = float(min(strip.min(), hedge.min(), rv.min(), (strip + hedge).min()))
        hi = float(max(strip.max(), hedge.max(), rv.max(), (strip + hedge).max()))
        g2 = axes([0, 30], [lo - 0.02, hi + 0.02], x_length=6.2, y_length=2.8, xlabel=r"days since the strip was bought",
                  ylabel=r"variance units (annualized)", xticks=[0, 10, 20, 30], yticks=[0, round(hi, 2)],
                  font_size=15).next_to(g1, DOWN, buff=0.45).align_to(g1, LEFT)
        history_path = curve(g1.ax, hrs, S, GREY_B, stroke_width=1.5).set_opacity(0.6)
        tr = ValueTracker(1)

        def upto(ax, y, col, sw=3):
            i = int(max(tr.get_value(), 2))
            return curve(ax, hrs[:i], y[:i], col, stroke_width=sw)
        pl = always_redraw(lambda: upto(g1.ax, S, SPOT, 2))
        c1 = always_redraw(lambda: upto(g2.ax, strip, OPT))
        c2 = always_redraw(lambda: upto(g2.ax, hedge, LV))
        c3 = always_redraw(lambda: upto(g2.ax, strip + hedge, IV, 4))
        c4 = always_redraw(lambda: upto(g2.ax, rv, RV, 2))
        leg = legend([(OPT, 'intrinsic strip payoff at current spot'), (LV, r"the delta hedge's gains"),
                      (IV, r"strip $+$ hedge"), (RV, r"realized variance so far")], font_size=16).to_edge(RIGHT, buff=0.4
                                                                                                         ).shift(UP * 1.5)

        def at(y):
            return float(y[int(min(max(tr.get_value(), 1), n - 1))])
        ro = VGroup(readout(r"\text{strip} + \text{hedge} =", lambda: at(strip + hedge), digits=3, font_size=26, color=IV),
                    readout(r"\text{realized} =", lambda: at(rv), digits=3, font_size=26, color=RV),
                    MathTex(rf"K_{{\text{{var}}}} = {R['kvar']:.3f}", font_size=26, color=OPT),
                    label(r"paid at the start", font_size=18, color=OPT)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(leg, DOWN, buff=0.5).align_to(leg, LEFT)
        src = real_data(rf"the strip of {R['day']} (SSVI fit), Binance BTCUSDT hourly, hedge rebalanced hourly")
        day = R["day"]
        kv, rvf, tot = 100 * np.sqrt(R["kvar"]), float(rv[-1]), float((strip + hedge)[-1])
        with self.voiceover(
            f"""Take {day} as a hypothetical pricing reconstruction. The reference time is eight, but its fitted Surface pools marks through noon; no executable eight-o'clock purchase is established. Set rates and costs to zero, use a finite model option strip, and follow Binance's hourly path for thirty days. <bookmark mark='a'/> The purple line is the strip's intrinsic payoff evaluated at the running spot, not its remaining-maturity market value. Together with the hypothetical stock hedge, it approximates the running realized-variance line. <bookmark mark='b'/> The final sum is {tot:.3f}, versus hourly variance {rvf:.3f}, and the initial variance strike is {kv:.1f} percent as volatility. Finite strikes, venue/reference differences and discrete returns leave error; this is not exact self-financing execution on Deribit."""
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(src), FadeIn(leg), FadeIn(VGroup(ro[2], ro[3])), Create(history_path))
            self.add(pl, c1, c2, c4, c3)
            vo.wait_until("a")
            self.play(FadeIn(ro[0]), FadeIn(ro[1]))
            self.play(tr.animate.set_value(n - 1), run_time=12, rate_func=linear)
            vo.wait_until("b")
        for m_ in (pl, c1, c2, c3, c4, ro[0].num, ro[1].num):
            m_.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def lab(self, r):
        R = r["replay"]
        card = lab_card(r"a variance swap, replicated", [
            "def strip_replication(K, otm, F, T, path):",
            "    q = 2 / T * np.gradient(K) / K ** 2      # options held",
            "    kvar = float(np.sum(q * otm))               # what they cost",
            "    ST = path[-1]",
            "    strip = np.sum(q * np.where(K < F, np.maximum(K - ST, 0),",
            "                                np.maximum(ST - K, 0)))",
            "    hedge = 2 / T * np.sum((1 / path[:-1] - 1 / F) * np.diff(path))",
            "    rv = np.sum(np.diff(np.log(path)) ** 2) / T",
            "    return kvar, strip + hedge, rv",
        ], source="explainer/quant/house/volsurface.py (abridged)", width=8.8).to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.5)
        rvf = float(np.asarray(R["rv"])[-1])
        tot = float(np.asarray(R["strip"])[-1] + np.asarray(R["hedge"])[-1])
        with self.voiceover(
            "In the House's code, the replication is nine lines: the weights, the cost of the strip, its payoff at "
            "expiry, the hedge's gains along the path, and the realized variance to compare. <bookmark mark='a'/> Run "
            "on that month, and the replicated and realized variances agree to the third decimal."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, [f"strip_replication(K, otm, F, 30/365, btc_hourly['{R['day']}'])",
                                 f"kvar {R['kvar']:.4f}   replicated {tot:.4f}   realized {rvf:.4f}",
                                 f"error {tot - rvf:+.4f}  (the cubic term of Chapter 9)"])
        self.wait(0.6)
        self.clear_scene()

    def scatter(self, r):
        rv = np.asarray(r["rv"])
        rep_h = rv + np.asarray(r["err_h"])
        rep_d = np.asarray(r["rep_d"])
        hi = float(np.max(np.concatenate([rv, rep_h, rep_d]))) * 1.05
        g = axes([0, hi], [0, hi], x_length=4.8, y_length=4.8, xlabel=r"realized variance, hourly",
                 ylabel=r"strip $+$ hedge", xticks=[0, round(hi / 2, 1)], yticks=[0, round(hi / 2, 1)], font_size=15
                 ).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        diag = DashedLine(g.ax.c2p(0, 0), g.ax.c2p(hi, hi), color=GREY_C)
        m = np.isfinite(rv) & np.isfinite(rep_h)
        dh = VGroup(*[Dot(g.ax.c2p(a, b), radius=0.04, color=IV) for a, b in zip(rv[m], rep_h[m])])
        m2 = np.isfinite(rv) & np.isfinite(rep_d)
        dd = VGroup(*[Dot(g.ax.c2p(a, b), radius=0.04, color=LV) for a, b in zip(rv[m2], rep_d[m2])])
        leg = legend([(IV, r"hedged every hour"), (LV, r"hedged once a day")], font_size=17).next_to(g, UP, buff=0.1)
        side = VGroup(
            wrapped_label(rf"{r['n']} overlapping 30-day windows, weekly starts, 2021--2025", width=5.8, font_size=19, color=GREY_A),
            MathTex(rf"\text{{hourly: error sd}}\ {r['err_h_sd']:.4f}\ \text{{on a mean of}}\ {r['rv_mean']:.3f}", font_size=26,
                    color=IV),
            MathTex(rf"\text{{daily hedge vs hourly variance: sd}}\ {r['daily_vs_hourly_sd']:.3f}", font_size=26, color=LV),
            wrapped_label('sampling clocks matter; even matched discrete clocks retain higher-order and finite-strike errors', 5.2, 19, GREY_A),
            wrapped_label(rf"and a listed grid (strikes every 2.5\%, within $\pm 50\%$) reads {r['listed_gap_volpts']:.1f} vol "
                          r"points below the full strip", 5.2, 19, BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        src = real_data(r"weekly strips from Deribit surfaces; Binance BTCUSDT hourly")
        n = r["n"]
        sdh, sdd, mean = r["err_h_sd"], r["daily_vs_hourly_sd"], r["rv_mean"]
        lg = r["listed_gap_volpts"]
        with self.voiceover(
            f"""Here are {n} overlapping thirty-day windows, beginning every Wednesday. They are not independent months. The hourly-hedge error has standard deviation {sdh:.4f}, against mean realized variance {mean:.3f}. <bookmark mark='a'/> Rebalance daily but retain hourly variance as the target, and the difference has standard deviation {sdd:.3f}. Even matching the sampling clock leaves higher-order return and truncation errors; it does not exactly replicate discrete squared log returns. <bookmark mark='b'/> A synthetic listed-style strike grid changes the model variance strike by {lg:.1f} volatility points on average. It is a discretization and truncation comparison, not observed executable contract performance."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(diag), FadeIn(leg[0]), FadeIn(side[0]))
            self.play(LaggedStart(*[FadeIn(x) for x in dh], lag_ratio=0.005, run_time=2.5), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dd], lag_ratio=0.005, run_time=2.5), FadeIn(leg[1]), FadeIn(side[2]),
                      FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def derive(self, r):
        rows = [cmath(r"RV_n", r"=", r"\frac{365}{n}\sum_i \ln^2\frac{S_{i+1}}{S_i}", font_size=38, colors={r"RV_n": RV}),
                cmath(r"\text{replicated} - RV_n", r"=", r"\frac{365}{n}\sum_i\big[2(r_i - \ln(1 + r_i)) - \ln^2(1 + r_i)\big]"
                      r" \approx \frac{365}{n}\sum_i \tfrac23 r_i^3", font_size=30),
                cmath(r"\sqrt V", r"\approx", r"\sqrt K + \frac{V - K}{2\sqrt K} - \frac{(V - K)^2}{8K^{3/2}}", font_size=36,
                      colors={r"\sqrt V": IV}),
                cmath(r"K_{\text{vol}}", r"\approx", r"\sqrt{K_{\text{var}}} - \frac{\text{Var}(V)}{8\,K_{\text{var}}^{3/2}}",
                      font_size=38, colors={r"K_{\text{vol}}": LV})]
        whys = [why(r"the contract: squared log returns, sampled $n$ times, annualized"),
                why(r"the hedge earns $r_i = \Delta S/S$ each period; expand the logarithm: only the cubes are left"),
                why(r"Taylor to second order around $K = \mathbb{E}V$: the square root is concave"),
                why(r"take expectations (Demeterfi et al.\ 1999; Carr and Lee 2009): a volatility swap's fair strike is "
                    r"below the variance swap's, by a convexity term the strip cannot hedge")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.6, buff=0.65, edge=6.9)  # four tall rows do not fit
        with self.voiceover(
            "The algebra. A contract samples the price n times and sums squared log returns. <bookmark mark='a'/> The "
            "hedge earns simple returns; expand the logarithm, and the replication error is a sum of cubed returns. "
            "<bookmark mark='b'/> A volatility swap pays the square root of realized variance. The root is concave: "
            "expand to second order. <bookmark mark='c'/> Its fair strike is the root of the variance strike minus the "
            "variance of variance over eight times the strike to the three halves. No strip delivers that: you would "
            "need to know how volatile volatility will be."
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

    def volswap(self, r):
        rv = np.asarray(r["rv"])
        c = r["convexity"]
        hi = float(np.max(rv)) * 1.05
        g = axes([0, hi], [0, np.sqrt(hi) * 1.05], x_length=6.6, y_length=4.2, xlabel=r"realized variance $V$",
                 ylabel=r"realized volatility $\sqrt V$", xticks=[0, round(hi / 2, 1)], yticks=[0, 0.5, 1.0],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        x = np.linspace(0, hi, 200)
        sq = curve(g.ax, x, np.sqrt(x), IV, stroke_width=3)
        m = rv < hi
        dots = VGroup(*[Dot(g.ax.c2p(v, np.sqrt(v)), radius=0.045, color=RV) for v in rv[m]])
        EV = float(rv.mean())
        p1 = Dot(g.ax.c2p(EV, np.sqrt(EV)), radius=0.08, color=IV)
        p2 = Dot(g.ax.c2p(EV, c["E_sqrt"]), radius=0.08, color=LV)
        gap = Line(p1.get_center(), p2.get_center(), color=BAD, stroke_width=4)
        side = VGroup(
            MathTex(rf"\sqrt{{\mathbb{{E}} V}} = {100 * c['sqrt_E']:.1f}\%", font_size=32, color=IV),
            MathTex(rf"\mathbb{{E}}\sqrt V = {100 * c['E_sqrt']:.1f}\%", font_size=32, color=LV),
            MathTex(rf"\text{{gap}} = {100 * c['gap']:.1f}\ \text{{vol pts; second order: }} {100 * c['approx_gap']:.1f}",
                    font_size=28, color=BAD),
            wrapped_label('physical sample averages, not fair strikes; the local second-order approximation overshoots in this sample', 4.6, 19, GREY_A),
            wrapped_label('under one Q measure and matching contracts, which fair strike is higher as volatility?', 4.6, 19,
                          QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        src = real_data(rf"{r['n']} realized 30-day variances of bitcoin, 2021--2025")
        a, b, gp, ap = 100 * c["sqrt_E"], 100 * c["E_sqrt"], 100 * c["gap"], 100 * c["approx_gap"]
        with self.voiceover(
            f"""Here is Jensen's inequality in historical data. Each dot is one overlapping window's realized variance. <bookmark mark='a'/> The root of its sample mean is {a:.1f} percent; the mean of its roots is {b:.1f}; the gap is {gp:.1f} points. The local second-order approximation gives {ap:.1f}, overshooting because variance fluctuates substantially. These are physical sample averages, not market fair strikes. <bookmark mark='b'/> For the same payoff horizon under a common risk-neutral measure, a volatility swap's fair strike cannot exceed the square root of the fair variance strike. Equality requires constant realized variance under that measure. This pricing inequality does not turn historical means into tradable prices."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(sq))
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.005, run_time=2))
            vo.wait_until("a")
            self.play(FadeIn(p1), FadeIn(side[0]), FadeIn(p2), FadeIn(side[1]), Create(gap))
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()
