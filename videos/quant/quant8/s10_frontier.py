from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import ALT, GOOD, KELLY, OVER, PART, UNDER, VALUE, illustration, load


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.bsde(load("bsde"))
        self.mfg()
        self.ppo(load("ppo"))

    def card(self):
        c = chapter_card(9, r"Frontiers: BSDEs, mean-field games, reinforcement learning",
                         r"What replaces the equation when it is too hard?", part=PART)
        with self.voiceover("Chapter nine. Frontiers: backward stochastic equations, mean-field games, and "
                            "reinforcement learning."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def bsde(self, b):
        rows = [cmath(r"-dY_t", r"=", r"f(Y_t, Z_t)\,dt - Z_t\,dW_t,\qquad Y_T = g(S_T)", font_size=34,
                      colors={r"-dY_t": VALUE}),
                cmath(r"f", r"=", r"-rY - \theta Z - (R - r)\,\min\!\Big(Y - \tfrac{Z}{\sigma},\, 0\Big)", font_size=32)]
        whys = [why(r"Pardoux and Peng (1990): solve backwards from the payoff for the value $Y$ and the hedge $Z$; "
                    r"El Karoui, Peng and Quenez (1997): this is how finance prices"),
                why(r"borrow at $R = 6\%$, lend at $r = 1\%$: the hedger's cash earns or costs different rates, and "
                    r"the price is no longer linear (Bergman 1995)")]
        step = ladder(self, rows, whys, keep=2, top=3.1, x=-0.4, buff=0.65, edge=6.9)
        runs = b["runs"]
        ns = [int(k) for k in runs]
        means = [np.mean(runs[k]) for k in runs]
        sds = [np.std(runs[k]) for k in runs]
        g = axes([np.log10(3000), np.log10(500000)], [0.5, 1.4], x_length=6.0, y_length=3.0,
                 xlabel=r"simulated paths", ylabel=r"price of the call spread", xticks=[4, 5],
                 xfmt=lambda u: f"10^{{{int(u)}}}", yticks=[0.6, 0.8, 1.0, 1.2, 1.4], font_size=16)
        g.to_edge(LEFT, buff=0.7).to_edge(DOWN, buff=0.45)
        ax = g.ax
        lines = VGroup()
        for val, col, txt in ((b["pde"], GOOD, r"nonlinear PDE"), (b["bs_r"], UNDER, r"Black--Scholes at $r$"),
                              (b["bs_R"], OVER, r"Black--Scholes at $R$")):
            ln = DashedLine(ax.c2p(np.log10(3000), val), ax.c2p(np.log10(500000), val), color=col, stroke_width=2)
            lines.add(VGroup(ln, label(txt + f": {val:.3f}", font_size=17, color=col).next_to(ln, RIGHT, buff=0.1)))
        pts = VGroup(*[VGroup(Line(ax.c2p(np.log10(n), m - 2 * s), ax.c2p(np.log10(n), m + 2 * s), color=VALUE,
                                   stroke_width=3), Dot(ax.c2p(np.log10(n), m), radius=0.06, color=VALUE))
                       for n, m, s in zip(ns, means, sds)])
        side = VGroup(
            label(r"$(S - 95)^+ - 2(S - 105)^+$, half a year, $\sigma = 20\%$", font_size=20, color=GREY_A),
            wrapped_label(r"dots: the BSDE by regression (Gobet, Lemor and Warin 2005), 3 runs each; it converges to "
                          r"the PDE, above both linear prices. The deep BSDE (Han, Jentzen and E 2018) solves this in "
                          r"100 dimensions.", 4.0, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "When the HJB equation is too hard, there is another route. A backward stochastic differential equation, "
            "introduced by Étienne Pardoux and Shige Peng in 1990, runs from the payoff at the end back to today, "
            "solving at once for the value and the hedge. Nicole El Karoui, Peng and Marie-Claire Quenez showed in "
            "1997 that this is exactly what a hedger's pricing problem is. <bookmark mark='a'/> It shines when the "
            "pricing is nonlinear. Suppose the hedger borrows at six percent but lends at one. Then the price of a "
            "position depends on whether its hedge needs cash, and the price is no longer linear. "
            "<bookmark mark='b'/> For a call spread, the regression solution of the BSDE converges, as the paths "
            f"increase, to the nonlinear PDE's {b['pde']:.3f}, above both Black-Scholes prices. Han, Jentzen and E "
            "solved this same problem in a hundred dimensions with neural networks in 2018, where no grid can reach."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(g), FadeIn(lines), FadeIn(side[0]))
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.3), FadeIn(side[1]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def mfg(self):
        rows = [cmath(r"-\partial_t u", r"=", r"H(x, \partial_x u, m) + \tfrac{\sigma^2}{2}\partial_{xx} u", font_size=36,
                      colors={r"-\partial_t u": VALUE}),
                cmath(r"\partial_t m", r"=", r"\partial_x\big(m\,\partial_p H\big) + \tfrac{\sigma^2}{2}\partial_{xx} m",
                      font_size=36, colors={r"\partial_t m": ALT})]
        whys = [why(r"each player's HJB, backwards in time, given how everyone else is distributed ($m$)"),
                why(r"the crowd's distribution, forwards in time, given how each player acts: solve both at once "
                    r"(Lasry and Lions 2006; Huang, Malham\'e and Caines 2006)")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.6, buff=1.0, edge=6.9)
        foot = wrapped_label(r"in markets: many traders liquidating at once move the price each of them trades at "
                             r"(Cardaliaguet and Lehalle 2018); Parts 36 and 37 use it for order books and execution",
                             12.0, 21, GREY_B).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Second frontier: decisions made by millions at once. In a mean-field game each player solves an HJB "
            "equation, backwards in time, taking as given how everyone else is distributed. <bookmark mark='a'/> "
            "And the distribution evolves forwards, driven by everyone's choices. The equilibrium solves both "
            "together. Jean-Michel Lasry and Pierre-Louis Lions, and independently Minyi Huang, Roland Malhamé and "
            "Peter Caines, introduced the idea in 2006. <bookmark mark='b'/> In markets, think of many funds "
            "selling the same stock: each one's trades move the price the others get. Parts thirty-six and "
            "thirty-seven use it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def ppo(self, p):
        m = np.asarray(p["mean_fraction"])
        it = np.arange(len(m))
        g = axes([0, len(m)], [0, 2.4], x_length=6.0, y_length=3.6, xlabel=r"training iteration",
                 ylabel=r"average fraction in stocks", xticks=[0, 100, 200, 300], yticks=[0, 0.5, 1, 1.5, 2],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17).to_edge(LEFT, buff=0.7).to_edge(UP, buff=0.7)
        ax = g.ax
        tgt = DashedLine(ax.c2p(0, p["discrete"]), ax.c2p(len(m), p["discrete"]), color=KELLY, stroke_width=2.5)
        tl = MathTex(rf"\text{{Merton, }}\gamma = 1:\ {100 * p['discrete']:.0f}\%", font_size=26, color=KELLY).next_to(
            ax.c2p(len(m), p["discrete"]), UP, buff=0.08).shift(LEFT * 1.6)
        lm = curve(ax, it, m, ALT, stroke_width=3)
        # the learned policy over (time, log wealth) at the end
        snaps = p["snapshots"]
        last = np.asarray(snaps[list(snaps.keys())[-1]])
        first = np.asarray(snaps[list(snaps.keys())[0]])
        hm = VGroup()
        cells = VGroup()
        nx, ny = last.shape[1], last.shape[0]
        size = 0.075
        for i in range(ny):
            for j in range(nx):
                val = float(np.clip(last[i, j], 0, 2.4)) / 2.4
                cells.add(Square(size, stroke_width=0, fill_color=interpolate_color(ManimColor(UNDER), ManimColor(KELLY), val),
                                 fill_opacity=0.9).move_to([j * size, i * size, 0]))
        cells.move_to(ORIGIN)
        hm.add(cells, label(r"time $\to$", font_size=18, color=GREY_B).next_to(cells, DOWN, buff=0.1),
               label(r"log wealth $\to$", font_size=18, color=GREY_B).rotate(PI / 2).next_to(cells, LEFT, buff=0.1))
        hm.next_to(g, DOWN, buff=0.45).align_to(g, LEFT).shift(RIGHT * 0.6)
        hl = wrapped_label(rf"the learned policy over time and wealth, after training: {100 * last.min():.0f} to "
                           rf"{100 * last.max():.0f}\%, mean {100 * last.mean():.0f}\%: flat, as Merton says",
                           3.6, 19, GREY_A).next_to(hm, RIGHT, buff=0.3)
        side = VGroup(
            wrapped_label(r"PPO (Schulman et al.\ 2017), the algorithm of Part 26 of \textit{AI, Built}: a policy "
                          r"network reads (time, wealth) and proposes a fraction; the reward is each quarter's log "
                          r"growth", 4.4, 20, GREY_A),
            wrapped_label(r"it never sees the formula; it finds the constant fraction, in every state", 4.4, 20, ALT),
            wrapped_label(r"the hard part was the noise: near the optimum, one fraction beats another by a few tenths of "
                          r"a percent a year inside a market moving 18\%. Advantages from one-step errors and a fixed "
                          r"exploration noise were needed to see it.", 4.4, 19, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = illustration(rf"300 iterations of 1{{,}}024 ten-year episodes; trained here on a CPU")
        with self.voiceover(
            "Third frontier: let a learner find the answer without the equation. Here is proximal policy "
            "optimization, the algorithm from part twenty-six of the AI series, on Merton's problem with log "
            "utility. A small network reads the time and the investor's wealth and proposes a fraction; the reward "
            "is each quarter's log growth. It never sees the formula. <bookmark mark='a'/> It starts at fifty "
            f"percent and climbs to Merton's {100 * p['discrete']:.0f} percent, and its policy is flat across time and "
            "wealth, as the theory says it should be. <bookmark mark='b'/> The hard part was not the network but "
            "the noise. Near the optimum, one fraction beats another by a few tenths of a percent a year inside a "
            "market that moves eighteen percent, and the first versions stalled well short. That is the lesson for "
            "learning in finance: the signal is small, and the method has to be built to hear it."
        ) as vo:
            self.play(FadeIn(g), Create(tgt), FadeIn(tl), FadeIn(side[0]), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(lm), run_time=3)
            self.play(FadeIn(hm), FadeIn(hl), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
