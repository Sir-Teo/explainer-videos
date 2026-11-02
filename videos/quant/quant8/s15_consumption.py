from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import ALT, GOOD, KELLY, OVER, PART, UNDER, VALUE, illustration, load


class Consumption(VoiceoverScene):
    def construct(self):
        c = load("consumption")
        m = load("martingale_check")
        self.card()
        self.consume(c)
        self.life(c)
        self.martingale()
        self.scatter(m)

    def card(self):
        c = chapter_card(6, r"Consumption, and the martingale method", r"How fast should you spend, and what are you "
                         r"really buying?", lit=(1969,), part=PART)
        with self.voiceover("Chapter six. Consumption, and the martingale method."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def consume(self, c):
        rows = [cmath(r"\rho V", r"=", r"\sup_{c,\,\pi}\Big\{u(c) + \big(rx + \pi x(\mu - r) - c\big)V_x + "
                      r"\tfrac12\pi^2\sigma^2x^2V_{xx}\Big\}", font_size=32, colors={r"\rho V": VALUE}),
                cmath(r"u'(c^*)", r"=", r"V_x", font_size=34, colors={r"u'(c^*)": KELLY}),
                cmath(r"V", r"=", r"A\,\frac{x^{1-\gamma}}{1-\gamma}\ \Rightarrow\ c^* = A^{-1/\gamma}\,x", font_size=32,
                      colors={r"V": VALUE}),
                cmath(r"\frac{c^*}{x} = \nu", r"=", r"\frac{\rho - (1-\gamma)\big(r + \theta^2/(2\gamma)\big)}{\gamma}",
                      font_size=34, colors={r"\frac{c^*}{x} = \nu": KELLY}),
                cmath(r"\frac{c^*}{x}", r"=", r"\frac{\nu}{1 - e^{-\nu(T - t)}}", font_size=34,
                      colors={r"\frac{c^*}{x}": KELLY})]
        whys = [why(r"infinite horizon, utility of consumption discounted at $\rho$: the HJB is stationary, and "
                    r"consumption drains wealth", font_size=21),
                why(r"first-order condition in $c$: eat until the marginal utility of eating equals that of saving",
                    font_size=21),
                why(r"the power guess again; $\pi^*$ is unchanged: $(\mu - r)/(\gamma\sigma^2)$", font_size=21),
                why(r"substitute and match the coefficients of $x^{1-\gamma}$ (Merton 1971); needs $\nu > 0$",
                    font_size=21),
                why(r"a finite life of $T$ years with no bequest: the same steps with $A$ replaced by $f(t)$",
                    font_size=21)]
        step = ladder(self, rows, whys, keep=3, top=3.2, x=-0.4, buff=0.9, edge=6.9)
        nu = c["nu"]
        with self.voiceover(
            "In 1971 Merton added the other half of a life: spending. The investor consumes at a rate c, gets utility from "
            "it, and discounts the future at a rate rho. Over an infinite horizon the equation no longer depends on time, and "
            "consumption appears as a drain on wealth. <bookmark mark='a'/> The first-order condition in c is a rule you can "
            "say aloud: eat until the marginal utility of eating equals the marginal value of a saved dollar. "
            "<bookmark mark='b'/> Guess the power form again. Consumption comes out proportional to wealth, and the stock "
            "fraction is exactly the same as before: spending and investing separate. <bookmark mark='c'/> Substitute and "
            "match the powers of wealth, and the spending rate is a constant, nu. With rho at three percent, log utility "
            f"spends exactly rho; gamma three spends {100 * nu[2]:.2f} percent of wealth a year. <bookmark mark='d'/> With a "
            "finite life and nothing left to heirs, the same steps with a function of time give a rate that rises toward the "
            "end."
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

    def life(self, c):
        t, life = np.asarray(c["t"]), np.asarray(c["life"])
        g = axes([0, 40], [0, 0.3], x_length=7.6, y_length=4.2, xlabel=r"years of a 40-year life",
                 ylabel=r"share of wealth spent per year", xticks=[0, 10, 20, 30, 40], yticks=[0, 0.1, 0.2, 0.3],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        ok = life <= 0.3
        tk = ValueTracker(0.0)
        tr = always_redraw(lambda: curve(ax, t[ok & (t <= tk.get_value())], life[ok & (t <= tk.get_value())], KELLY,
                                         stroke_width=4))
        inf = DashedLine(ax.c2p(0, c["nu"][2]), ax.c2p(40, c["nu"][2]), color=GREY_B, stroke_width=2)
        il = label(r"forever: $\nu$", font_size=18, color=GREY_B).next_to(ax.c2p(4, c["nu"][2]), UP, buff=0.08)
        tab = VGroup(*[MathTex(rf"\gamma = {g_:g}:\ \ \nu = {100 * n_:.2f}\%", font_size=28,
                               color=KELLY if g_ == 3 else GREY_A) for g_, n_ in zip(c["gammas"], c["nu"])])
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        q = pause_card(r"A more patient investor (lower $\rho$), $\gamma = 3$: does she spend more or less of her "
                       r"wealth?", width=4.8, font_size=21)
        ans = label(rf"less: at $\rho = 1\%$, $\nu = {100 * c['nu_patient']:.2f}\%$", font_size=22, color=KELLY)
        VGroup(tab, q, ans).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            f"Over a forty-year life with gamma three, the investor spends {100 * c['life_t0']:.1f} percent of wealth in "
            "year one; the rate climbs slowly, then steeply, to everything at the end. <bookmark mark='a'/> Across gammas "
            "the forever rate barely moves: a better market makes you richer, and saving more rewarding, and the two pull "
            "against each other. <bookmark mark='b'/> Pause and predict: a more patient investor, rho of one percent. More "
            f"or less spending? <bookmark mark='c'/> Less: {100 * c['nu_patient']:.2f} percent."
        ) as vo:
            self.play(FadeIn(g), Create(inf), FadeIn(il))
            self.add(tr)
            self.play(tk.animate.set_value(40), run_time=6, rate_func=linear)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(q))
            vo.wait_until("c")
            self.play(FadeIn(ans))
        tr.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def martingale(self):
        rows = [cmath(r"\xi_T", r"=", r"e^{-(r + \theta^2/2)T - \theta W_T}", font_size=34, colors={r"\xi_T": ALT}),
                cmath(r"\max\ \mathbb{E}\,u(X_T)", r"\ \text{s.t.}\ ", r"\mathbb{E}[\xi_T X_T] = x", font_size=34),
                cmath(r"u'(X_T) = y\,\xi_T", r"\ \Rightarrow\ ", r"X_T = (y\,\xi_T)^{-1/\gamma}", font_size=34,
                      colors={r"X_T = (y\,\xi_T)^{-1/\gamma}": KELLY}),
                cmath(r"X_T", r"\propto", r"e^{(\theta/\gamma) W_T} = e^{\pi^*\sigma W_T}\ \propto\ S_T^{\,\pi^*}",
                      font_size=34, colors={r"X_T": KELLY})]
        whys = [why(r"the state-price density: what one dollar in each terminal state costs today (Part 9 derives "
                    r"it)", font_size=21),
                why(r"in a complete market any payoff can be bought; its price is $\mathbb{E}[\xi_T X_T]$: a static "
                    r"budget (Cox and Huang 1989; Karatzas, Lehoczky and Shreve 1987)", font_size=21),
                why(r"maximize state by state with a Lagrange multiplier $y$; $y$ is set by the budget", font_size=21),
                why(r"the Merton investor owns a power claim on the stock: constant-mix rebalancing is how you build "
                    r"it", font_size=21)]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-0.8, buff=0.75, edge=6.9)
        with self.voiceover(
            "There is a second way to the same answer, with no differential equation at all. John Cox and Chi-fu Huang, "
            "and independently Karatzas, Lehoczky and Shreve, asked what the investor is really buying. In a complete market "
            "every terminal state has a price today; collect them into the state-price density xi. <bookmark mark='a'/> Then "
            "the dynamic problem is a static one: choose a payoff, state by state, to maximize expected utility, subject to "
            "one budget: its price must equal today's wealth. <bookmark mark='b'/> Maximize state by state with a Lagrange "
            "multiplier. Marginal utility must be proportional to the state price, so terminal wealth is the state price to "
            "the power minus one over gamma. Buy wealth where it is cheap. <bookmark mark='c'/> Write it out, and terminal "
            "wealth is the stock price to the power pi star. Merton's investor owns a power claim on the stock, and "
            "rebalancing to a constant mix is simply how you manufacture it."
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

    def scatter(self, m):
        xi, XT = np.asarray(m["xi"]), np.asarray(m["XT"])
        xs = np.asarray(m["xs"])
        lx = np.log10(xi)
        g = axes([float(np.log10(xs[0])), float(np.log10(xs[-1]))], [0.3, 4.0], x_length=7.2, y_length=4.4,
                 xlabel=r"state price $\xi_T$ (log scale): cheap $\leftarrow$ $\rightarrow$ dear",
                 ylabel=r"terminal wealth after 10 years", xticks=[-1, 0], xfmt=lambda u: f"10^{{{int(u)}}}",
                 yticks=[1, 2, 3, 4], font_size=16).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        k = ValueTracker(0)
        order = np.random.default_rng(5).permutation(len(xi))[:1200]
        pts = [ax.c2p(a, min(b, 4.0)) for a, b in zip(lx[order], XT[order])]
        dots = VGroup(*[Dot(p, radius=0.022, color=UNDER).set_opacity(0.7) for p in pts])
        for d_ in dots:
            d_.set_opacity(0)
        dots.add_updater(lambda grp: [d_.set_opacity(0.7 if i < k.get_value() else 0) for i, d_ in enumerate(grp)])
        cur = {key: np.asarray(v) for key, v in m["curves"].items()}
        lines = VGroup(*[curve(ax, np.log10(xs), np.minimum(cur[key], 4.0), col, stroke_width=3)
                         for key, col in (("1.5", OVER), ("3", KELLY), ("6", VALUE))])
        leg = legend([(OVER, r"$\gamma = 1.5$"), (KELLY, r"$\gamma = 3$: the investor simulated"),
                      (VALUE, r"$\gamma = 6$")], font_size=18).next_to(g, UP, buff=0.05).align_to(g, RIGHT)
        side = VGroup(
            wrapped_label(r"dots: 2{,}000 investors who rebalance to Merton's fraction every day for ten years; line: "
                          r"$c\,\xi_T^{-1/\gamma}$, the static answer", 4.2, 19, GREY_A),
            MathTex(rf"\text{{largest gap: }} {100 * m['max_rel']:.2f}\%", font_size=28, color=KELLY),
            MathTex(rf"\text{{median gap: }} {100 * m['median_rel']:.3f}\%", font_size=28, color=GREY_A),
            wrapped_label(r"steeper for low $\gamma$: a bolder investor buys more wealth in the cheap states", 4.2, 19,
                          GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = illustration(r"simulation: daily steps, $\mu = 8\%$, $r = 2\%$, $\sigma = 18\%$, $\gamma = 3$")
        with self.voiceover(
            "Check it: two thousand investors rebalance daily for ten years; plot each one's state price against its final "
            "wealth. <bookmark mark='a'/> The dots land on the static curve, to within "
            f"{100 * m['max_rel']:.2f} percent, the cost of rebalancing daily rather than continuously. "
            "<bookmark mark='b'/> Lower gamma tilts the curve: a bolder investor buys more wealth in the cheap states."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), FadeIn(src))
            self.add(dots)
            self.play(k.animate.set_value(len(order)), run_time=5, rate_func=linear)
            vo.wait_until("a")
            self.play(Create(lines[1]), FadeIn(leg[1]), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(Create(lines[0]), Create(lines[2]), FadeIn(leg[0]), FadeIn(leg[2]), FadeIn(side[3]))
        dots.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
