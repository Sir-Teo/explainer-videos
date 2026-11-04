from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant10.common import DEL, GAM, GAIN, LOSS, OPT, PART, REA, SPOT, load

R_COL = {"time": LOSS, "price": SPOT, "delta": DEL, "fukasawa": GAIN}
R_NAME = {"time": r"equal times", "price": r"price band, fixed width", "delta": r"delta band, fixed width",
          "fukasawa": r"band $\propto \Gamma^{-1/2}$ in price"}


class Research(VoiceoverScene):
    def construct(self):
        t = load("hedgetime_theory")
        self.card()
        self.equal_times()
        self.hitting()
        self.optimal()
        self.plot(t)
        self.table(t)
        self.btc(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"When to rebalance a hedge", r"For the same number of trades, how much smaller can the "
                          r"hedging error be?", part=PART)
        with self.voiceover("For the researcher: Chapter 9 hedged at equal times and found the error falls like one "
                            "over the square root of the number of trades. But nobody said the trades must be "
                            "equally spaced. Here is how much choosing when to trade is worth, and the theorem that "
                            "says how far that can go."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def equal_times(self):
        rows = [cmath(r"\varepsilon_k", r"\approx", r"\tfrac12\Gamma\big[(\Delta S)^2 - \sigma^2S^2\Delta t\big] = "
                      r"\tfrac12\Gamma\sigma^2S^2\Delta t\,(Z^2 - 1)", font_size=30, colors={r"\varepsilon_k": LOSS}),
                cmath(r"\operatorname{Var}\varepsilon_k", r"=", r"\tfrac12\Gamma^2\sigma^4S^4\Delta t^2", font_size=32,
                      colors={r"\operatorname{Var}\varepsilon_k": LOSS}),
                cmath(r"N \operatorname{Var}\Big(\sum_k \varepsilon_k\Big)", r"\to", r"\frac{T}{2}\,\mathbb E\!\int_0^T "
                      r"\Gamma^2\sigma^4S^4\,dt", font_size=32, colors={r"N \operatorname{Var}\Big(\sum_k \varepsilon_k\Big)": LOSS})]
        whys = [why(r"Chapter 9: between rebalances the hedge misses half gamma times the squared move, less its "
                    r"average"),
                why(r"$Z^2 - 1$ has variance 2"),
                why(r"$N = T/\Delta t$ steps of variance proportional to $\Delta t^2$: the total falls like $1/N$, with this "
                    r"constant. For a three-month at-the-money call at 20\%, it is 11.9 (per 100 of stock, squared)")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Start from Chapter 9. <bookmark mark='a'/> Between rebalances the hedge misses half gamma times the "
            "squared move, less its average: half gamma sigma squared S squared delta t, times Z squared minus one. "
            "<bookmark mark='b'/> Z squared minus one has variance two. <bookmark mark='c'/> N steps, each with "
            "variance proportional to delta t squared: the total variance falls like one over N, and N times it tends "
            "to T over two times the expected integral of gamma squared sigma to the fourth S to the fourth. For our "
            "three-month call that constant is eleven point nine."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def hitting(self):
        rows = [cmath(r"\tau", r"=", r"\inf\{t : |S_t - S_0| = a\},\qquad (\Delta S)^2 = a^2\ \text{exactly}", font_size=30,
                      colors={r"\tau": SPOT}),
                cmath(r"\varepsilon", r"\approx", r"\tfrac12\Gamma\sigma^2S^2\,(\mathbb E\tau - \tau)", font_size=32,
                      colors={r"\varepsilon": GAIN}),
                cmath(r"\mathbb E\tau = \frac{a^2}{\sigma^2S^2},\quad \operatorname{Var}\tau", r"=", r"\frac23\,\frac{a^4}"
                      r"{\sigma^4S^4}", font_size=32, colors={r"\operatorname{Var}\tau": SPOT}),
                cmath(r"\operatorname{Var}\varepsilon", r"=", r"\tfrac16\Gamma^2a^4\ \ \text{against}\ \ \tfrac12\Gamma^2a^4",
                      font_size=32, colors={r"\operatorname{Var}\varepsilon": GAIN})]
        whys = [why(r"instead, rebalance when the price has moved by $a$: the squared move is no longer random"),
                why(r"the error is now the randomness of the time it took"),
                why(r"the exit time of a Brownian motion from $(-a, a)$: the moments follow from optional stopping on "
                    r"$W^2 - t$ and $W^4 - 6tW^2 + 3t^2$ (Part 4)"),
                why(r"for the same average interval, an equal-time step has variance $\frac12\Gamma^2a^4$: trading on moves "
                    r"cuts the variance by a factor of three, before any optimization")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.44, edge=6.9)
        with self.voiceover(
            "Now trade on moves instead of on the clock. <bookmark mark='a'/> Rebalance when the price has moved by a "
            "fixed amount a. The squared move is then exactly a squared: that source of randomness is gone. "
            "<bookmark mark='b'/> What is left is the randomness of how long the move took. <bookmark mark='c'/> For "
            "the exit time of Brownian motion from an interval, optional stopping, from Part 4, gives the mean and the "
            "variance: two thirds of the mean squared. <bookmark mark='d'/> So the error per interval has variance one "
            "sixth gamma squared a to the fourth, against one half for an equal-time step of the same average length. "
            "Trading on moves cuts the variance by a factor of three, before any optimization at all."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def optimal(self):
        rows = [cmath(r"\min_a\ \mathbb E\!\int \tfrac16\Gamma^2a^2\sigma^2S^2\,dt", r"\ \text{s.t.}\ ",
                      r"\mathbb E\!\int \frac{\sigma^2S^2}{a^2}\,dt = N", font_size=30,
                      colors={r"\min_a\ \mathbb E\!\int \tfrac16\Gamma^2a^2\sigma^2S^2\,dt": GAIN}),
                cmath(r"a^*", r"\propto", r"|\Gamma|^{-1/2}\quad\Longleftrightarrow\quad |\Delta_t - \Delta_{\tau}|^2 = h\,"
                      r"\Gamma_{\tau}", font_size=32, colors={r"a^*": GAM}),
                cmath(r"N\operatorname{Var}", r"\to", r"\frac16\Big(\mathbb E\!\int_0^T |\Gamma|\sigma^2S^2\,dt\Big)^2\ \le\ "
                      r"\frac13\cdot\frac{T}{2}\,\mathbb E\!\int_0^T\Gamma^2\sigma^4S^4\,dt", font_size=28,
                      colors={r"N\operatorname{Var}": GAIN})]
        whys = [why(r"a band of width $a(t, S)$: the error accrues at rate $\frac16\Gamma^2a^2\sigma^2S^2$, trades at rate "
                    r"$\sigma^2S^2/a^2$"),
                why(r"pointwise Lagrange condition: the band is narrow where gamma is large, wide where it is small; in "
                    r"delta terms, trade when the delta has drifted by the square root of gamma"),
                why(r"and by Cauchy--Schwarz this is at most a third of the equal-time constant: for our call 2.64 against "
                    r"11.9, a factor of 4.5. Fixed price or delta bands give 3.98")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        thm = theorem_card(r"Asymptotically efficient discrete hedging", wrapped_label(
            r"among rebalancing rules made of stopping times, $\liminf\ \mathbb E[N]\,\mathbb E\langle \text{error}\rangle "
            r"\ge \frac16\big(\mathbb E\!\int|\Gamma|\sigma^2S^2dt\big)^2$, attained by the band $|\Delta_t - \Delta_\tau|^2 = "
            r"h\Gamma_\tau$ as $h \to 0$", 10.6, 20, GREY_A), who=r"Fukasawa (2011); with jumps, Rosenbaum and Tankov (2014)",
            width=11.6, font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now let the band vary. <bookmark mark='a'/> A band of width a, depending on time and price, accrues error "
            "at one rate and trades at another; minimize the error for a given number of trades. <bookmark mark='b'/> "
            "The Lagrange condition holds point by point: the width is proportional to one over the square root of "
            "gamma. Narrow near the strike close to expiry, wide far from it. In delta terms: trade when the delta has "
            "drifted by the square root of gamma. <bookmark mark='c'/> N times the variance then tends to one sixth of "
            "the squared expected integral of gamma sigma squared S squared, and by Cauchy-Schwarz that is at most a "
            "third of the equal-time constant. For our call, two point six four against eleven point nine. "
            "<bookmark mark='d'/> Masaaki Fukasawa proved in 2011 that no rule built from stopping times does better, "
            "asymptotically, and that this band attains the bound."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            self.play(FadeIn(thm))
        self.wait(0.5)
        self.clear_scene()

    def plot(self, t):
        g = axes([1.0, 2.6], [-1.1, 0.1], x_length=8.0, y_length=4.2, xlabel=r"average number of trades, $N$",
                 ylabel=r"standard deviation of the hedging error, per 100 of stock (log scale)",
                 xticks=[np.log10(16), np.log10(64), np.log10(256)], yticks=[-1.0, -0.5, 0.0],
                 xfmt=lambda v: f"{10 ** v:.0f}", yfmt=lambda v: f"{10 ** v:.2f}", font_size=15,
                 log_x=True).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        xs = np.linspace(1.1, 2.55, 60)
        lines, dots = VGroup(), VGroup()
        for r in ("time", "price", "fukasawa"):
            C = t["theory_NVar"][r]
            lines.add(curve(ax, xs, np.log10(np.sqrt(C / 10 ** xs)), R_COL[r], stroke_width=3))
            dots.add(VGroup(*[Dot(ax.c2p(np.log10(x["N"]), np.log10(x["sd"])), radius=0.07, color=R_COL[r])
                              for x in t["sims"][r]]))
        leg = legend([(R_COL["time"], R_NAME["time"]), (R_COL["price"], R_NAME["price"]),
                      (R_COL["fukasawa"], R_NAME["fukasawa"])], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(r"a short three-month at-the-money call, $\sigma = 20\%$, 3{,}000 paths on a grid of "
                             r"$2^{14}$ steps; lines: $\sqrt{C/N}$ with the constants from the formulas, dots: "
                             r"simulation (a delta band of fixed width lands on the price band's line)", 3.3, 14,
                             GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Simulate all of them on fine paths. <bookmark mark='a'/> Equal times, in red: the error falls like one "
            "over root N, on the line the formula predicts. <bookmark mark='b'/> A band of fixed width in price, in "
            "blue: the same slope, a lower line, a little over half the standard deviation. <bookmark mark='c'/> And the band "
            "proportional to one over root gamma, in green: lower again. To match its error with equal times you "
            "would need four and a half times as many trades."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(Create(lines[k]), FadeIn(dots[k]), FadeIn(leg[k]), run_time=1.3)
        self.wait(0.4)
        self.clear_scene()

    def table(self, t):
        hx = [-3.8, 0.2, 2.1, 3.9, 5.7]
        head = VGroup(label(r"$N \times \operatorname{Var}$ of the error", font_size=18, color=GREY_B),
                      label(r"theory", font_size=20), label(r"$N \approx 16$", font_size=20),
                      label(r"$N \approx 64$", font_size=20), label(r"$N \approx 256$", font_size=20))
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(label(R_NAME[r], font_size=18, color=R_COL[r]),
                                                 MathTex(rf"{t['theory_NVar'][r]:.2f}", font_size=26),
                                                 *[MathTex(rf"{x['NVar']:.2f}", font_size=26) for x in t["sims"][r]])
                                          for r in ("time", "price", "delta", "fukasawa")]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.68 * j, 0])
            row[0].align_to(np.array([hx[0] - 2.6, 0, 0]), LEFT)
            tab.add(row)
        foot = wrapped_label(r"theory: the limits as $N \to \infty$; the simulated values approach them as the band "
                             r"narrows (at $N \approx 16$ the bands are wide and the local approximation is rough). The "
                             r"two fixed-width bands share one constant, $\frac16 \mathbb E\!\int\sigma^2S^2\,dt\cdot \mathbb "
                             r"E\!\int\Gamma^2\sigma^2S^2\,dt$", 11.6, 16, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The constants. <bookmark mark='a'/> Equal times: theory eleven point nine, and the simulations climb to "
            "it as N grows. <bookmark mark='b'/> The fixed-width bands, in price or in delta, share one constant, "
            "about four. <bookmark mark='c'/> The optimal band: two point six four in theory, two point eight in "
            "simulation at two hundred and fifty-six trades, still approaching from above."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(foot))
            vo.wait_until("a")
            self.play(Indicate(tab[1], color=LOSS))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]))
            vo.wait_until("c")
            self.play(FadeIn(tab[4]))
        self.wait(0.4)
        self.clear_scene()

    def btc(self, t):
        b = t["btc"]
        hx = [-3.4, 0.2, 2.5, 4.9]
        head = VGroup(label(r"Bitcoin, 30-day calls", font_size=18, color=GREY_B), label(r"trades", font_size=20),
                      label(r"mean error", font_size=20), label(r"sd of error", font_size=20))
        tab = VGroup()
        rows = []
        for r_ in b["rows"]:
            for rule in ("time", "fukasawa"):
                rows.append((rule, r_[rule]))
        for j, row in enumerate([head] + [VGroup(label(R_NAME[rule], font_size=18, color=R_COL[rule]),
                                                 MathTex(rf"{x['N']:.0f}", font_size=26),
                                                 MathTex(rf"{x['mean_pct_premium']:+.1f}\%", font_size=26),
                                                 MathTex(rf"{x['sd_pct_premium']:.1f}\%", font_size=26))
                                          for rule, x in rows]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.9 - 0.62 * j, 0])
            row[0].align_to(np.array([hx[0] - 2.8, 0, 0]), LEFT)
            tab.add(row)
        foot = wrapped_label(rf"{b['n_options']} at-the-money calls written every 15 days on BTCUSDT one-minute closes, "
                             r"2019--2020, each priced and hedged at the volatility its own month realized (hindsight, so "
                             r"only the timing of trades is tested); errors in \% of the premium, positive when the hedger keeps "
                             r"money. Both rules end with a positive mean; its sources, among them microstructure noise in "
                             r"one-minute realized variance (Part 5), are not separated here. The comparison is of the "
                             r"spread",
                             11.8, 16, GREY_A).to_edge(DOWN, buff=0.4)
        f, l_ = b["rows"][0], b["rows"][1]
        with self.voiceover(
            "And on real prices: Bitcoin calls, a month long, written every fifteen days in 2019 and 2020, hedged on "
            "one-minute closes. Each is priced at the volatility its own month realized, a hindsight that leaves only "
            "the timing of trades to test. <bookmark mark='a'/> With about sixteen trades, the error's standard "
            f"deviation is {f['time']['sd_pct_premium']:.0f} percent of the premium at equal times, and "
            f"{f['fukasawa']['sd_pct_premium']:.0f} percent with the optimal band. <bookmark mark='b'/> With sixty-"
            f"four, {l_['time']['sd_pct_premium']:.0f} against {l_['fukasawa']['sd_pct_premium']:.0f}. Fat tails and "
            "clustered volatility do not erase the advantage; if anything they widen it, because a move-based rule "
            "trades when the market moves, not when the clock says."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: costs and timing together", r"with proportional costs the optimal rule is a band too "
                          r"(Whalley and Wilmott, Part 11), but with width $\propto \varepsilon^{1/3}$; a unified asymptotic "
                          r"theory for many options, costs and a trade budget is incomplete", width=12.4, font_size=18),
            desk_question(r"open: beyond the leading order", r"the bound is asymptotic; at a few dozen trades, where desks "
                          r"live, the gap to the limit is visible (2.8 against 2.64 here), and corrections are known only "
                          r"in special cases", width=12.4, font_size=18),
            desk_question(r"open: rough and jumpy prices", r"with jumps the optimal times change (Rosenbaum and Tankov "
                          r"2014); for rough volatility and for many assets hedged at once the efficient rule is open",
                          width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> With trading costs the optimal rule is also a band, Whalley and "
            "Wilmott's from Part 11, but its width scales like the cube root of the cost; a unified theory for a book "
            "of options, with costs and a budget of trades, is incomplete. <bookmark mark='b'/> The bound is "
            "asymptotic. At a few dozen trades, where desks actually live, the gap is visible, and corrections are "
            "known only in special cases. <bookmark mark='c'/> And with jumps the optimal times change, as Mathieu "
            "Rosenbaum and Peter Tankov showed; for rough volatility, or many assets hedged together, the efficient "
            "rule is open."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"equal-time hedging needs 256 trades to reach some error. Using the constants 11.9 and 2.64, "
                       r"roughly how many trades does the optimal band need for the same error?")
        with self.voiceover(
            "Pause and predict. Equal-time hedging needs two hundred and fifty-six trades to reach some error. Using the "
            "two constants, eleven point nine and two point six four, about how many does the optimal band need?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
