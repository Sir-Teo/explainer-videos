from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, illustration, load, real_data


class Arbitrage(VoiceoverScene):
    def construct(self):
        a = load("arbitrage")
        self.card()
        self.vogt(a)
        self.derive()
        self.calendar(a)
        self.lee(a)

    def card(self):
        c = chapter_card(3, r"Static arbitrage: impossible shapes", r"Which smiles can no market draw?", lit=(2014,),
                         part=PART)
        with self.voiceover("Chapter three. Static arbitrage: the shapes no market can draw."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def vogt(self, a):
        k = np.asarray(a["k"])
        w, g = np.asarray(a["w"]), np.asarray(a["g"])
        top = axes([-1.5, 1.5], [0.0, 0.35], x_length=6.6, y_length=2.3, ylabel=r"total variance $w(k)$, $T = 1$",
                   yticks=[0, 0.3], font_size=16)
        bot = axes([-1.5, 1.5], [-0.1, 1.5], x_length=6.6, y_length=2.5, xlabel=r"log-moneyness $k$",  # g peaks at 1.35
                   ylabel=r"Gatheral's $g(k)$", xticks=[-1, 0, 1], yticks=[0, 1], font_size=16)
        VGroup(top, bot).arrange(DOWN, buff=0.45).to_edge(LEFT, buff=0.6)
        wl = curve(top.ax, k, np.clip(w, 0, 0.35), IV, stroke_width=3)
        zero = DashedLine(bot.ax.c2p(-1.5, 0), bot.ax.c2p(1.5, 0), color=GREY_C)
        tr = ValueTracker(-1.5)

        def g_upto():
            m = k <= tr.get_value()
            if m.sum() < 2:
                return VGroup()
            return curve(bot.ax, k[m], g[m], LV, stroke_width=3)
        gl = always_redraw(g_upto)
        lo, hi = a["neg"]
        neg = k[(k >= lo) & (k <= hi)]
        red = VGroup(curve(bot.ax, neg, g[(k >= lo) & (k <= hi)], BAD, stroke_width=6),
                     glow_dot(bot.ax.c2p(a["k_min"], a["g_min"]), color=BAD, radius=0.08))
        params = a["vogt"]
        head = MathTex(rf"a = {params['a']:.4f},\ b = {params['b']:.4f},\ \rho = {params['rho']:.4f},\ m = {params['m']:.4f},"
                       rf"\ \sigma = {params['s']:.4f}", font_size=24, color=GREY_A).to_edge(UP, buff=0.25)
        fly = a["fly"]
        side = VGroup(
            wrapped_label(r"Vogt's smile (Gatheral and Jacquier 2014): raw SVI, looks harmless", 4.6, 20, IV),
            MathTex(rf"g_{{\min}} = {a['g_min']:.3f}\ \text{{at}}\ k = {a['k_min']:.2f}", font_size=30, color=BAD),
            wrapped_label(rf"negative on $k \in [{lo:.2f}, {hi:.2f}]$: the implied density is negative there", 4.6, 20, BAD),
            wrapped_label(rf"butterfly: calls at $K \pm {a['fly_h']:.1f}$ around $K = {a['fly_K']:.2f}$ cost "
                          rf"${fly * 1e6:.1f}$ millionths of the forward", 4.6, 20, OPT),
            wrapped_label(r"you are paid to own a payoff that is never negative: an arbitrage, small and real", 4.6, 20,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = illustration(r"Vogt's example, the parameters as published; computed here")
        flm = fly * 1e6
        with self.voiceover(
            "Here is a smile that looks perfectly reasonable: a raw SVI curve for one year, with parameters an analyst "
            "named Axel Vogt posted online, which Gatheral and Jacquier used as their warning example. "
            "<bookmark mark='a'/> Underneath it, a function of the smile, g of k, drawn from left to right. Watch it "
            "as it crosses the wing. <bookmark mark='b'/> It dips below zero. Where g is negative, the probability "
            f"density hidden in the smile is negative. Build the butterfly there: it costs {flm:.1f} millionths of the "
            "forward, a negative price for a payoff that can never be negative. <bookmark mark='c'/> The amount is "
            "tiny, buried in the far wing, invisible in a plot of prices. That is exactly why desks check g, not "
            "prices: a pricing engine fed this smile would quietly sell arbitrage."
        ) as vo:
            self.play(FadeIn(top), FadeIn(head), FadeIn(src), Create(wl), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(bot), Create(zero))
            self.add(gl)
            self.play(tr.animate.set_value(0.6), run_time=3)
            vo.wait_until("b")
            self.play(tr.animate.set_value(1.5), run_time=2.5)
            gl.clear_updaters()
            self.play(FadeIn(red), FadeIn(side[1]), FadeIn(side[2]))
            self.play(FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"C", r"=", r"F\big[N(d_+) - e^k N(d_-)\big],\quad d_\pm = -\frac{k}{\sqrt w} \pm \frac{\sqrt w}{2}",
                      font_size=34, colors={r"C": OPT}),
                cmath(r"q(K)", r"=", r"\partial_{KK}C = \frac{g(k)}{K\sqrt{2\pi w}}\,e^{-d_-^2/2}", font_size=36,
                      colors={r"q(K)": QC.Q}),
                cmath(r"g(k)", r"=", r"\Big(1 - \frac{k\,w'}{2w}\Big)^2 - \frac{w'^2}{4}\Big(\frac1w + \frac14\Big) + "
                      r"\frac{w''}{2} \;\ge\; 0", font_size=34, colors={r"g(k)": LV}),
                cmath(r"\partial_T w(k, T)", r"\ge", r"0 \quad \text{(at fixed } k\text{)}", font_size=36,
                      colors={r"\partial_T w(k, T)": LV}),
                cmath(r"w(k) \sim \beta |k|", r"\Rightarrow", r"\beta \le 2,\qquad \tilde p = \frac{(2 - \beta)^2}{8\beta}",
                      font_size=36, colors={r"w(k) \sim \beta |k|": BAD})]
        whys = [why(r"Black's formula with total variance $w = \sigma^2 T$ and $k = \ln K/F$: time and volatility enter "
                    r"only through $w$"),
                why(r"Breeden--Litzenberger (Part 9), then differentiate twice in $k$ using $e^k N'(d_-) = N'(d_+)$; "
                    r"every factor but $g$ is positive"),
                why(r"so no butterfly arbitrage $\iff g \ge 0$ everywhere (Gatheral)"),
                why(r"no calendar arbitrage: at fixed moneyness a call is a convex payoff of a martingale, so its value "
                    r"rises with $T$ (Gatheral and Jacquier 2014, Lemma 2.1)"),
                why(r"Lee (2004): $C/F \to 0$ needs $d_+ \to -\infty$, so the wings grow at most like $2|k|$; the slope "
                    r"says which moments $\mathbb{E}\,S^{1+p}$ are finite")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.0, buff=0.72, edge=6.9)
        with self.voiceover(
            "The derivation. Write Black's formula in log-moneyness and total variance. <bookmark mark='a'/> The "
            "density is the call's second strike derivative; differentiate twice, and it collapses to a positive "
            "factor times one function of the smile, g. <bookmark mark='b'/> No butterfly arbitrage exactly when g is "
            "never negative. <bookmark mark='c'/> At fixed moneyness a call is a convex payoff of a martingale, so total "
            "variance must not fall with maturity. <bookmark mark='d'/> And Roger Lee showed in 2004 that the wings can "
            "grow at most like two times the absolute log-moneyness, the slope telling which moments are finite. "
            "Michael Roper's 2010 note collects these into one checklist."
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
        self.wait(0.4)
        self.clear_scene()

    def calendar(self, a):
        kc = np.asarray(a["cross_k"])
        w0, w1 = np.asarray(a["cross_w0"]), np.asarray(a["cross_w1"])
        cr = a["cross"][a["cross_pair"]]
        e0, e1 = cr["pair"]
        hi = float(max(w0.max(), w1.max()) * 1.1)
        g = axes([-1, 1], [0, hi], x_length=6.8, y_length=3.8, xlabel=r"log-moneyness $k$", ylabel=r"total variance",
                 xticks=[-1, -0.5, 0, 0.5, 1], yticks=[0, round(hi / 2, 3)], yfmt=lambda u: f"{u:.3f}", font_size=16
                 ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        l0 = curve(g.ax, kc, w0, IV, stroke_width=3)
        l1 = curve(g.ax, kc, w1, LV, stroke_width=3)
        bad = w1 < w0
        glow = VGroup()
        if bad.any():
            glow = band(g.ax, kc[bad], w1[bad], w0[bad], BAD, 0.5)
        leg = legend([(IV, rf"SVI fit, expiry {e0}"), (LV, rf"SVI fit, expiry {e1}")], font_size=17).next_to(g, UP, buff=0.1
                                                                                                         ).align_to(g, LEFT)
        nb = sum(1 for c in a["cross"] if c["n_bad"] > 0)
        side = VGroup(
            wrapped_label(rf"fitted one expiry at a time, the Surface's SVI slices cross in {nb} of "
                          rf"{len(a['cross'])} neighbouring pairs, all in the first days", 4.6, 20, BAD),
            wrapped_label(r"a calendar spread there costs less than nothing: SSVI (Chapter 5) removes it by "
                          r"construction", 4.6, 20, GREY_A),
            wrapped_label(rf"Part 9's checker on each slice, strike by strike: {a['violations']} violations of "
                          r"monotonicity, convexity or bounds", 4.6, 20, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = real_data(r"the Surface: per-expiry SVI fits")
        viol = a["violations"]
        with self.voiceover(
            "Is the Surface itself clean? Fit SVI one expiry at a time, the way a careless desk would, and compare "
            f"neighbouring expiries. <bookmark mark='a'/> In {nb} of the pairs the later expiry's total variance dips "
            "below the earlier one's: the curves cross, and in the red region a calendar spread would cost less than "
            "nothing. All of them are among the expiries a few days out, where a handful of quotes pin each fit. "
            "<bookmark mark='b'/> Each slice on its own passes Part nine's strike-by-strike checker, with "
            f"{viol} violations. The arbitrage lives between the slices, which is why a surface must be fitted as a "
            "surface."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(l0), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(l1), FadeIn(leg[1]))
            self.play(FadeIn(glow), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def lee(self, a):
        lee = a["lee"]
        g = axes([0, 300], [0, 2.2], x_length=6.6, y_length=3.8, xlabel=r"days to expiry",
                 ylabel=r"wing slope of total variance, $\beta$", xticks=[0, 100, 200, 300], yticks=[0, 1, 2],
                 font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        lim = DashedLine(ax.c2p(0, 2), ax.c2p(300, 2), color=BAD)
        limt = label(r"Lee's limit $\beta = 2$", font_size=18, color=BAD).next_to(ax.c2p(300, 2), UP, buff=0.08).shift(LEFT * 1.2)
        dl = VGroup(*[Dot(ax.c2p(r["days"], r["beta_L"]), radius=0.06, color=BAD) for r in lee])
        dr = VGroup(*[Dot(ax.c2p(r["days"], r["beta_R"]), radius=0.06, color=SPOT) for r in lee])
        leg = legend([(BAD, r"left wing (puts)"), (SPOT, r"right wing (calls)")], font_size=17).next_to(g, UP, buff=0.1
                                                                                                     ).align_to(g, LEFT)
        last = lee[-1]
        side = VGroup(
            MathTex(rf"\beta_L = {last['beta_L']:.2f},\ \ \beta_R = {last['beta_R']:.2f}\ \ ({last['days']:.0f}\ \text{{days}})",
                    font_size=28),
            wrapped_label(rf"so $\mathbb{{E}}\,S_T^{{1+p}}$ is finite up to $p \approx {last['p_R']:.1f}$ and "
                          rf"$\mathbb{{E}}\,S_T^{{-q}}$ up to $q \approx {last['q_L']:.1f}$", 4.6, 20, GREY_A),
            wrapped_label(r"every expiry's wings are far below 2: no wing arbitrage, and the market prices finite but "
                          r"fat tails", 4.6, 20, GREY_B),
            wrapped_label(r"pause and predict: a wing of slope 2.5. What can you do?", 4.6, 20, QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = real_data(r"the Surface: wing slopes $b(1 \pm \rho)$ of each expiry's SVI fit")
        bl, br, pr, ql = last["beta_L"], last["beta_R"], last["p_R"], last["q_L"]
        with self.voiceover(
            "Lee's bound on the Surface. For each expiry, the slopes of the two wings of total variance, puts in red, "
            "calls in blue, against the limit of two. <bookmark mark='a'/> They grow with maturity, and at the last "
            f"expiry they reach {bl:.2f} on the put side and {br:.2f} on the call side: nowhere near the limit. "
            "Read them through Lee's formula and they say something about the distribution: moments of the price "
            f"are finite up to about power {1 + pr:.1f} on the upside. Pause and predict: a wing of slope two and a "
            "half: what can you do? <bookmark mark='b'/> Sell the far calls. Their implied price exceeds what any "
            "distribution with that forward allows, and the bound says so before any model is chosen."
            " Next: a smile in five numbers that can be made to respect those bounds."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(lim), FadeIn(limt), FadeIn(leg))
            self.play(LaggedStart(*[FadeIn(x) for x in dl], lag_ratio=0.1), LaggedStart(*[FadeIn(x) for x in dr],
                                                                                         lag_ratio=0.1), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]))
            self.play(FadeIn(side[3]))
            vo.wait_until("b")
            self.play(Indicate(lim, color=BAD))
        self.wait(0.4)
        self.clear_scene()
