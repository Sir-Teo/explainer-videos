from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, BARRIER, CASH, GOOD, IV, OPT, PART, SPOT, illustration, load


class Static(VoiceoverScene):
    def construct(self):
        b = load("barrier")
        self.card()
        self.unseen()
        self.monitoring(b)
        self.dek(load("dek"))
        self.ceg(load("static"))
        self.skew(load("static"))

    def card(self):
        c = chapter_card(4, r"Watched at the close, hedged without trading", r"What if the barrier is checked once a day, "
                         r"and can a barrier be hedged with vanillas?", lit=(1997,), part=PART)
        with self.voiceover("Chapter four. Watched at the close, and hedged without trading."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def unseen(self):
        g = np.random.default_rng(8)  # a path that slips below the barrier between looks, unseen
        n = 600
        t = np.linspace(0, 1, n + 1)
        x = np.concatenate([[0], np.cumsum(g.standard_normal(n) * np.sqrt(1 / n) * 0.35)]) - 0.25 * np.sin(np.pi * t)
        hb = -0.32
        ax = axes([0, 1], [-0.9, 0.5], x_length=10.5, y_length=4.2, xlabel=r"six months", ylabel=r"log price",
                  xticks=[], yticks=[], font_size=16).to_edge(UP, buff=0.7)
        a = ax.ax
        bar = DashedLine(a.c2p(0, hb), a.c2p(1, hb), stroke_color=BARRIER, stroke_width=3)
        obs = np.arange(0, n + 1, 100)
        ticks = VGroup(*[DashedLine(a.c2p(t[i], -0.9), a.c2p(t[i], 0.5), stroke_color=GREY_D, stroke_width=1.2)
                         for i in obs])
        tr = ValueTracker(0)
        path = tracing(a, t, x, tr, SPOT, stroke_width=2.5)
        below = x < hb
        segs = VGroup()
        i = 0
        while i <= n:
            if below[i]:
                j = i
                while j <= n and below[j]:
                    j += 1
                segs.add(curve(a, t[max(i - 1, 0):j + 1], x[max(i - 1, 0):j + 1], BAD, stroke_width=3.5))
                i = j
            i += 1
        seen = [k for k in obs if x[k] < hb]
        dots = VGroup(*[Dot(a.c2p(t[k], x[k]), radius=0.07, color=WHITE if x[k] >= hb else BAD) for k in obs])
        foot = wrapped_label(r"watched only at the dotted dates, the barrier misses the red excursions: the path dipped "
                             r"below and came back between two looks. A barrier checked less often is harder to hit, so "
                             r"a knock-out is worth more, a knock-in less", 11.5, 20, GREY_A).to_edge(DOWN, buff=0.6)
        src = illustration(r"one simulated path, monthly observation")
        verdict = ("This path dipped through the barrier between observations and was never caught: the knock-out "
                   "survived." if not seen else
                   "This path was caught at an observation, but only after slipping through unseen first.")
        with self.voiceover(
            "The formula of chapter three assumes the barrier is watched at every instant. Term sheets watch it at "
            "the close, once a day, or once a month. Watch a path with monthly looks. <bookmark mark='a'/> In red, "
            f"the moments it spent below the barrier. {verdict} A barrier that is checked less often is harder to "
            "hit, so a knock-out is worth more than the formula says, and a knock-in less."
        ) as vo:
            self.play(FadeIn(ax), Create(bar), FadeIn(ticks), FadeIn(src))
            self.add(path)
            self.play(tr.animate.set_value(n), run_time=5, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(segs), LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.1), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def monitoring(self, b):
        rows = b["rows"]
        tab = VGroup(VGroup(label(r"barrier watched", font_size=22, color=GREY_A),
                            label(r"Monte Carlo", font_size=22, color=GREY_A),
                            label(r"closed form, shifted barrier", font_size=22, color=GREY_A)))
        for r in rows:
            tab.add(VGroup(label(r["name"], font_size=24), MathTex(rf"{r['mc']:.2f} \pm {2 * r['se']:.2f}", font_size=28),
                           MathTex(f"{r['bgk']:.2f}", font_size=28, color=GOOD)))
        tab.add(VGroup(label(r"the textbook formula", font_size=24, color=GREY_A),
                       VectorizedPoint(), MathTex(f"{b['continuous']:.2f}", font_size=28, color=BAD)))
        xs = [-3.8, 0.6, 4.2]
        for i, row in enumerate(tab):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 2.9 - 0.55 * i, 0])
        rows_tex = [
            cmath(r"\mathbb E[\text{overshoot}]", r"\to", r"\beta\,\sigma\sqrt{\Delta t},\quad \beta = "
                  r"-\frac{\zeta(\frac12)}{\sqrt{2\pi}} \approx 0.5826", font_size=30,
                  colors={r"\mathbb E[\text{overshoot}]": BAD}),
            cmath(r"V_{\text{disc}}(H)", r"\approx", r"V_{\text{cont}}\big(H e^{\mp\beta\sigma\sqrt{\Delta t}}\big)",
                  font_size=30, colors={r"V_{\text{disc}}(H)": BARRIER})]
        whys = [why(r"when a discretely watched walk first lands past $H$, it lands past it by about this much "
                    r"(Siegmund's corrected diffusion; the ladder height of a Gaussian walk)", font_size=20),
                why(r"so shift the barrier away from the spot by the mean overshoot (Broadie, Glasserman and Kou "
                    r"1997)", font_size=20)]
        p = b["params"]
        src = illustration(rf"down-and-out call: $S = K = {p['S']:.0f}$, $H = {p['H']:.0f}$, six months, $\sigma = "
                           rf"{100 * p['sigma']:.0f}\%$; 100{{,}}000 paths, 20 steps a day", corner=UR)
        with self.voiceover(
            "How much more? Watched monthly, the knock-out is worth "
            f"{rows[0]['mc']:.2f}, against {b['continuous']:.2f} for the textbook formula; daily, {rows[2]['mc']:.2f}. "
            "<bookmark mark='a'/> Broadie, Glasserman and Kou explained it in 1997: a walk looked at every delta t lands "
            "past the barrier by an overshoot whose mean is beta sigma root delta t, with beta about 0.58, from the Riemann "
            "zeta function. <bookmark mark='b'/> So shift the barrier away by that much and use the continuous formula: the "
            "right-hand column matches every frequency within the noise."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(src), LaggedStart(*[FadeIn(r_[:2]) for r_ in tab[1:-1]], lag_ratio=0.2),
                      FadeIn(tab[-1]))
            vo.wait_until("a")
            rows_tex[0].to_edge(DOWN, buff=1.4)
            whys[0].next_to(rows_tex[0], DOWN, buff=0.12)
            self.play(FadeIn(rows_tex[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeOut(rows_tex[0]), FadeOut(whys[0]))
            rows_tex[1].to_edge(DOWN, buff=1.4)
            whys[1].next_to(rows_tex[1], DOWN, buff=0.12)
            self.play(FadeIn(rows_tex[1]), FadeIn(whys[1]),
                      LaggedStart(*[FadeIn(r_[2]) for r_ in tab[1:-1]], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def dek(self, d):
        rows = d["rows"]
        T, H = d["T"], d["H"]
        g = axes([0, T], [-0.25, 0.25], x_length=7.0, y_length=3.8, xlabel=r"time (years)",
                 ylabel=r"hedge's value on the barrier, $S = H$", xticks=[0, 0.25, 0.5], yticks=[-0.2, 0, 0.2],
                 font_size=15).to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
        ax = g.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(T, 0), stroke_color=GREY_C, stroke_width=1.5)
        cols = [BAD, IV, GOOD, OPT]
        curves = VGroup(*[curve(ax, np.asarray(r["t"]), np.clip(np.asarray(r["along"]), -0.25, 0.25), cols[k],
                                stroke_width=2.5) for k, r in enumerate(rows)])
        marks = VGroup(*[VGroup(*[Dot(ax.c2p(t, 0), radius=0.05, color=cols[k]) for t in r["dates"][:-1]])
                         for k, r in enumerate(rows)])
        tab = VGroup(label(r"dates", font_size=20, color=GREY_A), label(r"cost of the static hedge", font_size=20,
                                                                         color=GREY_A))
        tab = VGroup(tab.arrange(RIGHT, buff=0.6))
        for k, r in enumerate(rows):
            tab.add(VGroup(MathTex(str(r["n"]), font_size=28, color=cols[k]), MathTex(f"{r['cost']:.3f}", font_size=28,
                                                                                    color=cols[k])))
        tab.add(VGroup(label(r"closed form", font_size=20, color=GREY_A), MathTex(f"{d['closed']:.3f}", font_size=28)))
        for i, row in enumerate(tab[1:], 1):
            row[0].move_to([tab[0][0].get_x(), -0.5 * i, 0])
            row[1].move_to([tab[0][1].get_x(), -0.5 * i, 0])
        tab.to_edge(RIGHT, buff=0.6).shift(UP * 0.8)
        cap = wrapped_label(r"Derman, Ergener and Kani (1995): hold the call, and fill the barrier line backward with puts "
                            r"struck at $H$, each sized to make the portfolio worth zero on the barrier at one date. If "
                            r"the barrier is touched, sell everything for about nothing; if not, the puts expire "
                            r"worthless above $H$", 12.0, 19, GREY_A).to_edge(UP, buff=0.35)
        last = rows[-1]
        with self.voiceover(
            "Can a barrier be hedged without trading every day? Emanuel Derman, Deniz Ergener and Iraj Kani said "
            "yes, in 1995, with a static portfolio of vanillas. Hold the call, and add puts struck at the barrier "
            "that cancel its value there at the last date. <bookmark mark='a'/> Step back one date and cancel again "
            "with shorter puts, and so on back to today. The curve is the portfolio's value along the barrier: zero "
            "at each date, close to zero in between. <bookmark mark='b'/> With more dates its cost converges to the "
            f"barrier's price: {last['cost']:.3f} with {last['n']} dates, against {d['closed']:.3f} in closed form. "
            "On a touch, the desk sells it all for about nothing, the dead option's worth."
        ) as vo:
            self.play(FadeIn(cap), FadeIn(g), Create(zero), FadeIn(tab[0]))
            self.play(Create(curves[0]), FadeIn(marks[0]), FadeIn(tab[1]))
            vo.wait_until("a")
            self.play(Create(curves[1]), FadeIn(marks[1]), FadeIn(tab[2]), curves[0].animate.set_stroke(opacity=0.35))
            vo.wait_until("b")
            self.play(Create(curves[2]), FadeIn(tab[3]), curves[1].animate.set_stroke(opacity=0.35))
            self.play(Create(curves[3]), FadeIn(tab[4]), FadeIn(tab[5]), curves[2].animate.set_stroke(opacity=0.35))
        self.wait(0.4)
        self.clear_scene()

    def ceg(self, s):
        rows = [
            cmath(r"C(K)", r"=", r"\frac{K}{F}\,P\Big(\frac{F^2}{K}\Big)", font_size=38, colors={r"C(K)": OPT}),
            cmath(r"\mathbb E\big[(S_T - K)^+\big]", r"=", r"\frac{K}{F}\,\mathbb E\Big[\Big(\frac{F^2}{K} - S_T\Big)^+\Big]",
                  font_size=34, colors={r"\mathbb E\big[(S_T - K)^+\big]": OPT}),
            cmath(r"\text{at the touch, } F = H:\ C(K)", r"=", r"\frac{K}{H}\,P\Big(\frac{H^2}{K}\Big)", font_size=34,
                  colors={r"\text{at the touch, } F = H:\ C(K)": BARRIER}),
        ]
        whys = [why(r"put--call symmetry: $r = q = 0$ and a smile symmetric in $\log K/F$ (Carr, Ellis and Gupta "
                    r"1998; Carr and Lee 2009)"),
                why(r"under Black--Scholes, change measure with density $S_T/F$: the law of $F^2/S_T$ is the law of $S_T$"),
                why(r"so $K/H$ puts struck at $H^2/K$ are worth the call on the barrier, and expire worthless if it is "
                    r"never touched ($H^2/K < H$): a down-and-in call, replicated")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.0, buff=0.8, edge=6.9)
        w, k = s["weight"], s["strike"]
        card = lab_card(r"the static hedge", [
            "def static_dic_hedge(K, H, F):",
            "    # put-call symmetry: r = q = 0, a symmetric smile",
            "    return K / H, H * H / K   # number of puts, strike",
        ], source="explainer/quant/house/exotics.py", width=6.6, font_size=18).to_edge(LEFT, buff=0.4)
        bsm = s["models"]["BS"]
        outs = [f"static_dic_hedge(100, 90, 100)  ->  ({w:.3f}, {k:.1f})",
                f"cost {bsm['hedge']:.3f};  exact down-and-in call {s['exact_dic_bs']:.3f}"]
        with self.voiceover(
            "A simpler static hedge came from Peter Carr, Katrina Ellis and Vishal Gupta in 1998. Under put–call "
            "symmetry, a call struck at K is worth K over F puts struck at F squared over K. "
            "<bookmark mark='a'/> Under Black–Scholes it is one change of measure, with density S over F. "
            "<bookmark mark='b'/> Now apply it at the moment of the touch, when the forward is the barrier. K over "
            "H puts struck at H squared over K are worth exactly the call. So a down-and-in call is replicated by "
            "holding those puts: if the barrier is touched, swap them for the call at no cost; if not, they expire "
            "worthless, below the barrier. <bookmark mark='c'/> In code it is two numbers. For a strike of 100 and "
            f"a barrier of 90: {w:.3f} puts struck at {k:.0f}, costing {bsm['hedge']:.3f}, the exact price of the "
            "down-and-in call."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.clear_scene()
            self.play(FadeIn(card))
            lab_run(self, card, outs, font_size=18, direction=RIGHT)
        self.wait(0.4)
        self.clear_scene()

    def skew(self, s):
        names = ["BS", "Heston, rho = 0", "Heston, rho = -0.7"]
        shown = {"BS": r"Black--Scholes", "Heston, rho = 0": r"Heston, $\rho = 0$",
                 "Heston, rho = -0.7": r"Heston, $\rho = -0.7$"}
        M = s["models"]
        tab = VGroup(VGroup(label(r"model", font_size=21, color=GREY_A), label(r"down-and-in call", font_size=21, color=GREY_A),
                            label(r"static hedge", font_size=21, color=GREY_A), label(r"gap", font_size=21, color=GREY_A)))
        for nm in names:
            m = M[nm]
            tab.add(VGroup(label(shown[nm], font_size=22), MathTex(rf"{m['dic']:.3f} \pm {2 * m['se']:.3f}", font_size=26),
                           MathTex(f"{m['hedge']:.3f}", font_size=26), MathTex(f"{m['gap']:+.3f}", font_size=26,
                                                                                color=BAD if abs(m["gap"]) > 0.3 else GOOD)))
        xs = [-4.4, -0.8, 2.2, 4.6]
        for i, row in enumerate(tab):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 2.9 - 0.55 * i, 0])
        # the ledger at the touch on a few skewed paths
        led = VGroup(label(r"at the touch, Heston $\rho = -0.7$: sell the puts, buy the call", font_size=21,
                           color=GREY_A))
        for p in M["Heston, rho = -0.7"]["paths"][:4]:
            led.add(MathTex(rf"t = {p['touch']:.2f}:\ \ +{p['put']:.2f}\ (\text{{puts}})\ -\ {p['call']:.2f}\ "
                            rf"(\text{{call}})\ =\ {p['put'] - p['call']:+.2f}", font_size=28,
                            color=BAD if p["put"] - p["call"] < -0.05 else GOOD))
        led.arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.5)
        g_bs, g0, g7 = M["BS"]["gap"], M["Heston, rho = 0"]["gap"], M["Heston, rho = -0.7"]["gap"]
        ratio = abs(g7) / max(abs(g_bs), 1e-6)
        verdict = (f"The skew breaks the hedge: the gap is {g7:+.2f}, about {ratio:.0f} times the monitoring error."
                   if abs(g7) > 2 * abs(g_bs) else
                   f"Even with the skew the gap is {g7:+.2f}, not far from the monitoring error.")
        pp = pause_card(r"With a negative skew, is the put-symmetry hedge too dear or too cheap?", width=6.0)
        pp.to_corner(UR, buff=0.3)
        src = illustration(r"$S = K = 100$, $H = 90$, six months, $r = q = 0$; 50{,}000 paths of 500 steps; Heston "
                           r"$v_0 = \theta = 0.0625$, $\kappa = 2$, $\xi = 0.8$", corner=UL)
        with self.voiceover(
            "Pause and predict: with a negative skew, is the put-symmetry hedge too dear or too cheap? "
            "<bookmark mark='a'/> Under Black–Scholes the hedge costs "
            f"{M['BS']['hedge']:.3f} and the barrier is worth {M['BS']['dic']:.3f} on a grid of five hundred steps; "
            f"the gap, {g_bs:+.3f}, is only the monitoring error of the last section. Heston with no correlation "
            f"keeps the smile symmetric, and the gap stays small, {g0:+.3f}. <bookmark mark='b'/> Now give it a "
            f"skew, correlation minus 0.7. {verdict} The puts at 81 carry a higher implied volatility than the call "
            "at 100, so the hedge is too dear. It still covers the barrier, and at every touch the puts sell for more "
            "than the call costs, as the ledger shows; but nobody can charge a client its price. Static hedges are "
            "exact only under symmetry."
            " Next: the simplest exotic of all, the digital."
        ) as vo:
            self.play(FadeIn(pp))
            vo.wait_until("a")
            self.play(FadeOut(pp), FadeIn(src), FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]))
            self.play(FadeIn(led[0]), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in led[1:]], lag_ratio=0.4,
                                                  run_time=3))
        self.wait(0.4)
        self.clear_scene()
