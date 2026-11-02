from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load, pause


class Jumps(VoiceoverScene):
    def construct(self):
        j = load("jumps")
        lv = load("levy_layers")
        self.card()
        self.clock(lv)
        self.layers(lv)
        self.formula(j, lv)

    def card(self):
        c = chapter_card(12, r"Jumps: from Poisson to L\'evy--It\^o", r"What if prices don't move continuously?",
                         part=PART)
        with self.voiceover("Chapter twelve. Jumps: from the Poisson clock to the Lévy-Itô decomposition, and Itô's "
                            "lemma for jumps."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def clock(self, lv):
        ev = np.asarray(lv["clock"])
        g1 = axes([0, 1], [0, len(ev) + 1], x_length=7.4, y_length=2.6, ylabel=r"$N_t$: a Poisson clock, rate 6 a year",
                  xticks=[], yticks=[0, len(ev)], font_size=15)
        g2 = axes([0, 1], [-3.5, 3.5], x_length=7.4, y_length=2.4, xlabel=r"time (years)",
                  ylabel=r"$\widetilde N_t = N_t - 6t$: compensated", xticks=[0, 0.5, 1], yticks=[-3, 0, 3], font_size=15)
        VGroup(g1, g2).arrange(DOWN, buff=0.4).to_edge(LEFT, buff=0.5)
        a1, a2 = g1.ax, g2.ax
        tt = np.concatenate([[0], ev, [1]])
        stair = [a1.c2p(0, 0)]
        for k, e in enumerate(ev):
            stair += [a1.c2p(e, k), a1.c2p(e, k + 1)]
        stair.append(a1.c2p(1, len(ev)))
        st = VMobject(stroke_color=JUMP, stroke_width=3).set_points_as_corners(stair)
        ticks = VGroup(*[Line(a1.c2p(e, -0.3), a1.c2p(e, 0.3), color=YELLOW, stroke_width=3) for e in ev])
        comp = [a2.c2p(0, 0)]
        for k, e in enumerate(ev):
            comp += [a2.c2p(e, k - 6 * e), a2.c2p(e, k + 1 - 6 * e)]
        comp.append(a2.c2p(1, len(ev) - 6))
        ct = VMobject(stroke_color=ITO, stroke_width=3).set_points_as_corners(comp)
        rows = [cmath(r"P(\text{gap} > s)", r"=", r"e^{-\lambda s}", font_size=30),
                cmath(r"\mathbb{E}\big[N_t - \lambda t \mid \mathcal{F}_s\big]", r"=", r"N_s - \lambda s", font_size=30,
                      colors={r"N_s - \lambda s": ITO}),
                cmath(r"[\widetilde N]_t", r"=", r"N_t, \quad \mathbb{E}\,\widetilde N_t^2 = \lambda t", font_size=30),
                cmath(r"\mathbb{E}\,e^{iu\sum_{i \le N_t} Y_i}", r"=", r"\exp\big(\lambda t\,(\phi_Y(u) - 1)\big)", font_size=30)]
        whys = [why(r"memoryless gaps: the clock forgets", 18),
                why(r"independent increments: the compensator $\lambda t$ makes it a martingale", 18),
                why(r"each jump has size 1, so $(\Delta N)^2 = \Delta N$", 18),
                why(r"compound Poisson: condition on $N_t$", 18)]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=3.6, buff=0.75, edge=6.9)
        pc, ans = pause(r"Jumps arrive at rate 6 a year. The chance of none in a month?", r"$e^{-6/12} = e^{-0.5} = 0.61$.",
                        width=4.4, font_size=20)
        VGroup(pc, ans).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(DR, buff=0.3)
        res = label(rf"compensated compound Poisson, 50{{,}}000 paths: mean {lv['cp_mean']:+.4f}, variance "
                    rf"{lv['cp_var']:.4f} against $\lambda t\,\mathbb{{E}}Y^2 = {lv['cp_var_theory']:.4f}$", font_size=18,
                    color=GREY_A).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "Brownian paths are continuous; prices are not always. News arrives in lumps. The simplest model of a "
            "lump is a Poisson clock, ringing at random times with independent exponential gaps. <bookmark mark='a'/> "
            "Each ring adds one to a counter, a staircase that climbs on average at rate lambda, so it is not a "
            "martingale. <bookmark mark='b'/> Subtract the average climb, lambda t, and it is: the compensated "
            "Poisson process, a sawtooth. Its quadratic variation is the counter itself, since a jump of one, "
            "squared, is still one. <bookmark mark='c'/> Attach a random size to each ring and you have a compound "
            "Poisson process; its characteristic function follows by conditioning on the count, and fifty thousand "
            f"paths give a mean of {lv['cp_mean']:+.4f} and the predicted variance. <bookmark mark='d'/> A pause: at "
            "six jumps a year, the chance of a month with none? E to the minus a half: sixty-one percent."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2))
            self.play(LaggedStart(*[FadeIn(tk, shift=DOWN * 0.2) for tk in ticks], lag_ratio=0.3))
            step(0)
            vo.wait_until("a")
            self.play(Create(st), run_time=2)
            vo.wait_until("b")
            self.play(Create(ct), run_time=2)
            step(1)
            step(2)
            vo.wait_until("c")
            step(3)
            self.play(FadeIn(res))
            vo.wait_until("d")
            self.play(FadeIn(pc), FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    def layers(self, lv):
        grid = np.asarray(lv["grid"])
        eps_keys = ["0.3", "0.1", "0.03", "0.01", "0.005"]
        comps = [("drift", np.asarray(lv["drift"]), DRIFT, r"drift $b\,t$"),
                 ("brown", np.asarray(lv["brown"]), BM, r"Brownian part $\sigma W_t$"),
                 ("big", np.asarray(lv["big"]), JUMP, r"big jumps, $|x| \ge 1$")]
        small = {k: np.asarray(v) for k, v in lv["small"].items()}
        allv = np.concatenate([c[1] for c in comps] + list(small.values()))
        span = max(np.ptp(c[1]) for c in comps)
        strips = VGroup()
        axs = []
        hs = 1.15
        for name, y, col, txt in comps + [("small", small[eps_keys[0]], STRAT, r"compensated small jumps")]:
            lo, hi = y.min() - 0.05, y.max() + 0.05
            if name == "small":
                lo = min(v.min() for v in small.values()) - 0.05
                hi = max(v.max() for v in small.values()) + 0.05
            a = axes([0, 1], [lo, hi], x_length=6.8, y_length=hs, xticks=[], yticks=[], font_size=14)
            axs.append(a)
            strips.add(VGroup(a, label(txt, font_size=19, color=col).next_to(a, LEFT, buff=0.2)))
        strips.arrange(DOWN, buff=0.25, aligned_edge=RIGHT).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.2)
        lines = [curve(axs[i].ax, grid, comps[i][1], comps[i][2], stroke_width=2.5) for i in range(3)]
        sm = [curve(axs[3].ax, grid, small[k], STRAT, stroke_width=1.8) for k in eps_keys]
        el = VGroup(*[MathTex(rf"\varepsilon = {k}:\ {lv['n_small'][k]}\ \text{{jumps, compensator }} "
                              rf"{lv['comp'][k]:+.2f}\,t", font_size=22, color=STRAT) for k in eps_keys])
        for m in el:
            m.next_to(strips, UP, buff=0.2).align_to(strips, RIGHT)
        eq = MathTex(r"X_t = b\,t + \sigma W_t + \sum_{s \le t} \Delta X_s \mathbf{1}_{|\Delta X_s| \ge 1} + "
                     r"\lim_{\varepsilon \to 0} \Big(\sum_{s \le t} \Delta X_s \mathbf{1}_{\varepsilon \le |\Delta X_s| < 1} - "
                     r"t\int_{\varepsilon \le |x| < 1} x\,\nu(dx)\Big)", font_size=24).to_edge(UP, buff=0.3)
        lk = MathTex(r"\mathbb{E}\,e^{iuX_t} = e^{t\psi(u)},\ \ \psi(u) = iub - \tfrac12\sigma^2u^2 + \int \big(e^{iux} - 1 - "
                     r"iux\mathbf{1}_{|x|<1}\big)\,\nu(dx)", font_size=24, color=ITO).to_edge(DOWN, buff=0.55)
        lkr = label(rf"checked on 20{{,}}000 simulated $X_1$: largest gap between the empirical and the formula's "
                    rf"characteristic function {lv['cf_err']:.3f}", font_size=18, color=GREY_B).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Every process with independent, stationary increments, a Lévy process, is built from four layers. Here "
            f"is one path of a tempered stable process, with infinitely many small jumps and {lv['n_big']} big ones, "
            "taken apart. <bookmark mark='a'/> A drift. A Brownian part. The big jumps, a compound Poisson process. "
            "<bookmark mark='b'/> And the small jumps, so many that their sum converges only after subtracting their "
            f"average, the compensator. Slide the cutoff epsilon toward zero: {lv['n_small']['0.3']} jumps become "
            f"{lv['n_small']['0.005']}, the compensator grows, and the strip turns from sparse spikes into something "
            "almost Brownian. <bookmark mark='c'/> This is the Lévy-Itô decomposition. The layers are independent, so "
            "their characteristic functions multiply: the Lévy-Khintchine formula. Our simulations match it to "
            f"{lv['cf_err']:.2f}, the sampling noise of twenty thousand draws."
        ) as vo:
            self.play(FadeIn(eq), FadeIn(strips))
            vo.wait_until("a")
            for ln in lines:
                self.play(Create(ln), run_time=1.0)
            vo.wait_until("b")
            self.play(Create(sm[0]), FadeIn(el[0]))
            for k in range(1, len(sm)):
                self.play(ReplacementTransform(sm[k - 1], sm[k]), ReplacementTransform(el[k - 1], el[k]), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(lk), FadeIn(lkr))
        self.wait(0.4)
        self.clear_scene()

    def formula(self, j, lv):
        P = np.asarray(j["merton_paths"])
        n = P.shape[1]
        g = axes([0, 1], [0.3, 1.9], x_length=5.4, y_length=3.6, xlabel=r"time (years)", ylabel=r"Merton paths",
                 xticks=[0, 0.5, 1], yticks=[0.5, 1.0, 1.5], font_size=16).to_corner(DL, buff=0.45)
        ax = g.ax
        t = np.linspace(0, 1, n)
        cols = color_gradient([BM, STRAT], len(P))
        paths = VGroup(*[curve(ax, t, np.clip(p, 0.3, 1.9), c, stroke_width=2) for p, c in zip(P, cols)])
        rows = [cmath(r"f(X_t)", r"=", r"f(X_0) + \int_0^t f'(X_{s-})\,dX_s + \tfrac12\int_0^t f''\,d\langle X^c\rangle_s + "
                      r"\sum_{s \le t}\big[f(X_s) - f(X_{s-}) - f'(X_{s-})\,\Delta X_s\big]", font_size=26,
                      colors={r"\sum_{s \le t}\big[f(X_s) - f(X_{s-}) - f'(X_{s-})\,\Delta X_s\big]": JUMP}),
                cmath(r"S_t", r"=", r"S_0\exp\Big(\big(\mu - \tfrac12\sigma^2 - \lambda\bar k\big)t + \sigma W_t + "
                      r"\sum_{i \le N_t} Y_i\Big),\ \ \bar k = e^{m + s^2/2} - 1", font_size=28,
                      colors={r"\lambda\bar k": JUMP})]
        whys = [why(r"between jumps, the continuous lemma; at each jump, replace the linear guess by the true change", 20),
                why(r"Merton (1976): compensate the drift so that $\mathbb{E}S_t = S_0 e^{\mu t}$", 20)]
        step = ladder(self, rows, whys, keep=2, top=3.2, x=-0.6, buff=0.6, edge=6.9)
        side = wrapped_label(r"here: 6 jumps a year, log sizes $N(-5\%, 8\%^2)$, $\sigma = 50\%$; the House's "
                             r"\texttt{merton\_jumps}, its mean checked against $S_0 e^{\mu t}$", 5.6, 20, GREY_A)
        side.to_corner(DR, buff=0.6)
        with self.voiceover(
            "Itô's lemma extends to jumps with one change. Between jumps the old lemma applies; at a jump, replace "
            "the linear guess by the true change of f. <bookmark mark='a'/> Apply it to Merton's 1976 model, Brownian "
            "motion plus log-normal jumps: to keep the expected return at mu, the drift must pay back the average "
            "jump, lambda times k bar. <bookmark mark='b'/> These are its paths: diffusion most of the time, and "
            "gaps. The next chapter looks for gaps in real prices."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(g), LaggedStart(*[Create(p) for p in paths], lag_ratio=0.3, run_time=3), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()
