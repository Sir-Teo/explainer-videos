from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, load, pause, real_data


class Brownian(VoiceoverScene):
    def construct(self):
        q = load("qv_live")
        s = load("signature")
        self.card()
        self.live(q)
        self.proof(q)
        self.signature(s, q)

    def card(self):
        c = chapter_card(2, r"Quadratic variation, accumulating", r"Why is $(dW)^2 = dt$?", part=PART)
        with self.voiceover("Chapter two. Quadratic variation, watched as it accumulates, and then proved."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def live(self, q):
        W = np.asarray(q["W"])
        tW = np.linspace(0, 1, len(W))
        g1 = axes([0, 1], [W.min() - 0.1, W.max() + 0.1], x_length=7.6, y_length=2.2, ylabel=r"one Brownian path $W_t$",
                  xticks=[], yticks=[], font_size=16)
        g2 = axes([0, 1], [0, 2.0], x_length=7.6, y_length=3.0, xlabel=r"time $t$", ylabel=r"running sums over the grid",
                  xticks=[0, 0.5, 1], yticks=[0, 1, 2], font_size=16)
        VGroup(g1, g2).arrange(DOWN, buff=0.35).to_edge(LEFT, buff=0.5)
        a1, a2 = g1.ax, g2.ax
        tk = ValueTracker(0)
        path = tracing(a1, tW, W, tk, BM, stroke_width=2)
        diag = DashedLine(a2.c2p(0, 0), a2.c2p(1, 1), color=GREY_B, stroke_width=2)
        dl = MathTex(r"y = t", font_size=24, color=GREY_B).next_to(a2.c2p(1, 1), RIGHT, buff=0.08)
        cols = {"v1": JUMP, "v2": ITO, "v3": DRIFT}

        def sums(n):
            run = q["run"][str(n)]
            t = np.linspace(0, 1, n + 1)
            return VGroup(*[curve(a2, t, np.minimum(np.asarray(run[k]), 2.0), cols[k], stroke_width=3) for k in
                            ("v1", "v2", "v3")])
        n0 = 256
        run0 = q["run"][str(n0)]
        tt = np.linspace(0, 1, n0 + 1)
        live = VGroup(*[tracing(a2, tt, np.minimum(np.asarray(run0[k]), 2.0), tk, cols[k], stroke_width=3)
                        for k in ("v1", "v2", "v3")])
        leg = legend([(JUMP, r"$\sum |\Delta W|$: the length"), (ITO, r"$\sum (\Delta W)^2$: quadratic variation"),
                      (DRIFT, r"$\sum |\Delta W|^3$")], font_size=21).to_corner(UR, buff=0.4)
        ns = q["ns"]
        finals = VGroup()
        for n in ns:
            run = q["run"][str(n)]
            finals.add(VGroup(MathTex(rf"n = {n:,}".replace(",", "{,}"), font_size=24, color=GREY_A),
                              MathTex(rf"{run['v1'][-1]:.1f}", font_size=24, color=JUMP),
                              MathTex(rf"{run['v2'][-1]:.3f}", font_size=24, color=ITO),
                              MathTex(rf"{run['v3'][-1]:.4f}", font_size=24, color=DRIFT)))
        for r_ in finals:
            r_.arrange(RIGHT, buff=0.35)
        finals.arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(leg, DOWN, buff=0.45).align_to(leg, LEFT)
        regrid(finals, gap=0.35)
        cur = sums(ns[0])
        with self.voiceover(
            "Draw one Brownian path, on a grid of two hundred and fifty-six steps, and keep three running totals over "
            "its steps: the sizes of the moves, their squares, and their cubes. <bookmark mark='a'/> The length races "
            "off the chart. The cubes barely leave the floor. The squares climb along the diagonal, close to the "
            "elapsed time. <bookmark mark='b'/> Now refine the grid, from sixteen steps to four thousand. The length "
            "grows like the square root of the number of steps: a Brownian path is infinitely long on every interval. "
            "The cubes vanish. The squares hug the line y equals t. <bookmark mark='c'/> That is what d W squared "
            "equals d t means: not a rule of algebra, but a sum of many small squares that has become deterministic."
        ) as vo:
            self.add(path, *live)
            self.play(FadeIn(g1), FadeIn(g2), Create(diag), FadeIn(dl), FadeIn(leg))
            vo.wait_until("a")
            self.play(tk.animate.set_value(len(tW) - 1), run_time=5, rate_func=linear)
            for m in live:
                m.clear_updaters()
            vo.wait_until("b")
            self.play(FadeOut(live), FadeIn(cur), FadeIn(finals[0]))
            for k, n in enumerate(ns[1:], 1):
                nxt = sums(n)
                self.play(Transform(cur, nxt), FadeIn(finals[k]), run_time=1.1)
            vo.wait_until("c")
            self.play(Indicate(cur[1], color=ITO), Indicate(diag, color=WHITE))
        self.wait(0.4)
        self.clear_scene()

    def proof(self, q):
        rows = [cmath(r"\mathbb{E}\sum_k (\Delta W_k)^2", r"=", r"\sum_k \Delta t_k = T", font_size=34),
                cmath(r"\operatorname{Var}\sum_k (\Delta W_k)^2", r"=", r"\sum_k 2\,\Delta t_k^2 \;\le\; 2T \max_k \Delta t_k "
                      r"\;\to\; 0", font_size=34, colors={r"\sum_k 2\,\Delta t_k^2 \;\le\; 2T \max_k \Delta t_k \;\to\; 0": ITO}),
                cmath(r"\sum_k |\Delta W_k|", r"\ge", r"\frac{\sum_k (\Delta W_k)^2}{\max_k |\Delta W_k|} \;\to\; \infty",
                      font_size=34, colors={r"\frac{\sum_k (\Delta W_k)^2}{\max_k |\Delta W_k|} \;\to\; \infty": JUMP}),
                cmath(r"\mathbb{E}\,RV_n", r"=", r"\sigma^2 T + 2n\,\mathbb{E}\,\varepsilon^2", font_size=34,
                      colors={r"2n\,\mathbb{E}\,\varepsilon^2": JUMP})]
        whys = [why(r"each increment has variance $\Delta t_k$"),
                why(r"independent increments; a Gaussian's fourth moment is $3\Delta t^2$, so each square has variance "
                    r"$2\Delta t^2$"),
                why(r"so the sum converges to $T$ in mean square; the paths are continuous, so "
                    r"$\max|\Delta W| \to 0$ and the length is infinite: no Stieltjes integral"),
                why(r"observed prices carry noise $\varepsilon$ at each tick: $n$ extra squares, which grow with $n$")]
        step = ladder(self, rows, whys, keep=3, top=3.2, x=-1.5, buff=0.5, edge=6.9)
        ns = q["ns"]
        tab = VGroup(*[MathTex(rf"n = {n:,}:\ \ {sd:.4f} \text{{ against }} \sqrt{{2/n}} = {th:.4f}".replace(",", "{,}"),
                               font_size=24, color=GREY_A) for n, sd, th in
                       zip(ns, q["qv_sd"], q["qv_sd_theory"])]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        tab.to_corner(DL, buff=0.35)
        tl = label(r"spread of $\sum(\Delta W)^2$ over 4{,}000 paths", font_size=20, color=ITO).next_to(tab, UP,
                                                                                                    buff=0.1)
        tl.align_to(tab, LEFT)
        pc, ans = pause(r"Sample twice as fast. By how much does the spread of the estimate shrink?",
                        r"By $\sqrt 2$: its standard deviation is $\sqrt{2/n}\,T$.", width=5.0, font_size=22)
        pc.to_corner(DR, buff=0.35)
        ans.next_to(pc, UP, buff=0.2).align_to(pc, LEFT)
        with self.voiceover(
            "The proof takes two lines. The expected sum of squared increments is the sum of the steps: T. "
            "<bookmark mark='a'/> Its variance: each squared increment has variance twice its step squared, so the "
            "variance of the sum is at most two T times the largest step, which goes to zero. <bookmark mark='b'/> "
            "And the length is at least the sum of squares divided by the largest move, which goes to zero because "
            "the path is continuous. So the length is infinite, no Stieltjes integral exists, and the next chapter "
            "has to build a new one. <bookmark mark='c'/> A pause: sample twice as fast, and by how much does the "
            "spread of the estimate shrink? <bookmark mark='d'/> By the square root of two; four thousand paths agree "
            "at every grid. <bookmark mark='e'/> One more line, for real prices: noise on each observed price adds n "
            "extra squares, and the estimate grows with n instead of settling."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(pc))
            vo.wait_until("d")
            self.play(FadeIn(ans), FadeIn(tl), FadeIn(tab))
            vo.wait_until("e")
            self.play(FadeOut(pc), FadeOut(ans), FadeOut(tab), FadeOut(tl))
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def signature(self, s, q):
        m = np.log10(np.asarray(s["minutes"]))
        vol = np.asarray(s["vol_annual"])
        g = axes([0, np.log10(1440) + 0.1], [0.6, 0.85], x_length=7.4, y_length=4.4,
                 xlabel=r"sampling interval (log scale)", ylabel=r"Bitcoin's 2020 volatility, from realized variance",
                 xticks=list(np.log10([1, 5, 15, 60, 240, 1440])),
                 xfmt=lambda u: {1: "1 min", 5: "5 min", 15: "15 min", 60: "1 h", 240: "4 h", 1440: "1 day"}[round(10 ** u)],
                 yticks=[0.6, 0.7, 0.8], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16).to_edge(LEFT, buff=0.6)
        g.shift(DOWN * 0.2)
        ax = g.ax
        line = curve(ax, m, vol, BM, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=BM) for a, b in zip(m, vol)])
        side = VGroup(
            MathTex(rf"\text{{every minute: }} {100 * vol[0]:.0f}\%", font_size=32, color=JUMP),
            MathTex(rf"\text{{every day: }} {100 * vol[-1]:.0f}\%", font_size=32, color=DRIFT),
            MathTex(r"\widehat{\mathbb{E}\,\varepsilon^2} = \frac{RV_{1\,\mathrm{min}} - RV_{1\,\mathrm{day}}}{2n}",
                    font_size=30, color=ITO),
            MathTex(rf"\text{{noise: about }} {q['noise_bp']:.1f} \text{{ basis points a tick}}", font_size=28, color=ITO),
            wrapped_label(r"the volatility signature plot (Andersen, Bollerslev, Diebold and Labys 2000); "
                          r"subsampling over offsets (Zhang, Mykland and A\"it-Sahalia 2005) averages the noise down",
                          4.6, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.45)
        src = real_data(r"Binance BTCUSDT one-minute candles, 2020; subsampled over up to 30 offsets")
        with self.voiceover(
            "Try it on Bitcoin in 2020. If the price were a Brownian motion with constant volatility, the sum of "
            "squared returns would give the same answer at every sampling interval. <bookmark mark='a'/> Squared "
            f"daily returns give a volatility of {100 * vol[-1]:.0f} percent; squared one-minute returns give "
            f"{100 * vol[0]:.0f}. <bookmark mark='b'/> The last line of the proof explains the rise: the bid-ask "
            "bounce is noise, and its squares pile up as the sampling gets faster. Read backwards, the gap between "
            f"the one-minute and the one-day estimates measures it: about {q['noise_bp']:.1f} basis points a tick. "
            "Practitioners sample every five minutes or so, a compromise between noise and too few observations, or "
            "they subsample: compute the sum from every starting offset and average, as Zhang, Mykland and "
            "Aït-Sahalia proposed. Part seven builds volatility forecasts on these sums."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(dots), FadeIn(side[1]), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()
