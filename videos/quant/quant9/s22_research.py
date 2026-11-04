from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import ALT, ARB, FWD, HEDGE, P_C, PART, Q_C, load

H_COL = {"0.4": ALT, "0.5": GREY_B, "0.6": P_C}
E_COL = {"0": WHITE, "1bp": HEDGE, "10bp": ARB}


def _lg(n):
    return np.log10(np.asarray(n, float))


class Research(VoiceoverScene):
    def construct(self):
        t = load("friction_theory")
        self.card()
        self.fbm_law()
        self.sign_bet()
        self.sharpe_plot(t)
        self.costs()
        self.net_plot(t)
        self.cps()
        self.btc(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"Arbitrage with frictions", r"A price with memory admits arbitrage. Why does a small trading "
                          r"cost make it go away?", part=PART)
        with self.voiceover("For the researcher: Chapter 10's theorem has a corollary. A price that allows no free "
                            "lunch with vanishing risk, even for simple buy-and-hold strategies, must be a "
                            "semimartingale. Here is the classic price that is not one, the arbitrage it allows, and "
                            "the theorem that a trading cost, however small, removes it."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def fbm_law(self):
        rows = [cmath(r"\operatorname{Cov}\big(B^H_s, B^H_t\big)", r"=", r"\tfrac12\big(s^{2H} + t^{2H} - |t - s|^{2H}\big)",
                      font_size=32, colors={r"\operatorname{Cov}\big(B^H_s, B^H_t\big)": P_C}),
                cmath(r"\rho", r"=", r"\operatorname{Corr}\big(\Delta_k, \Delta_{k+1}\big) = 2^{2H - 1} - 1", font_size=32,
                      colors={r"\rho": P_C}),
                cmath(r"\sum_k |\Delta_k|^2", r"\to", r"\begin{cases} 0 & H > \tfrac12 \\ \infty & H < \tfrac12 \end{cases}",
                      font_size=30, colors={r"\sum_k |\Delta_k|^2": ARB})]
        whys = [why(r"fractional Brownian motion (Mandelbrot and Van Ness 1968, Part 14): Gaussian, self-similar, $H = "
                    r"\frac12$ is Brownian motion"),
                why(r"consecutive increments on any grid have the same correlation: $+0.149$ at $H = 0.6$, $-0.129$ at "
                    r"$H = 0.4$. Memory at every scale"),
                why(r"so its quadratic variation is zero or infinite: $B^H$ is not a semimartingale, and by Delbaen and "
                    r"Schachermayer (1994) a frictionless market on it must allow a free lunch with "
                    r"simple strategies")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Take Part 14's fractional Brownian motion as a log price. <bookmark mark='a'/> It is Gaussian and "
            "self-similar, with this covariance; H of one half is ordinary Brownian motion. <bookmark mark='b'/> On any "
            "grid, however fine, consecutive increments have the same correlation, two to the two H minus one, minus "
            "one: plus point one five at H of point six, minus point one three at point four. The memory does not fade "
            "as you look closer. <bookmark mark='c'/> So the sum of squared increments goes to zero or to infinity, "
            "the process is not a semimartingale, and by Delbaen and Schachermayer's corollary a frictionless market "
            "built on it must offer a free lunch."
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

    def sign_bet(self):
        rows = [cmath(r"\pi_k", r"=", r"\operatorname{sign}(\rho)\,\operatorname{sign}(\Delta_{k-1}),\qquad "
                      r"\Delta_k \sim N\big(0, \sigma^2 n^{-2H}\big)", font_size=30, colors={r"\pi_k": FWD}),
                cmath(r"\mathbb E[\pi_k\Delta_k]", r"=", r"\sigma n^{-H}\sqrt{2/\pi}\,|\rho|", font_size=32,
                      colors={r"\mathbb E[\pi_k\Delta_k]": FWD}),
                cmath(r"\mathrm{SR}_{\text{year}}", r"\approx", r"\sqrt n\;\frac{\sqrt{2/\pi}\,|\rho|}{\sqrt{1 - 2\rho^2/\pi}}"
                      r"\ \to\ \infty", font_size=32, colors={r"\mathrm{SR}_{\text{year}}": ARB})]
        whys = [why(r"hold one unit long or short, $n$ times a year, betting that the next increment repeats the last "
                    r"($H > \frac12$) or reverses it ($H < \frac12$)"),
                why(r"for a standard normal pair with correlation $\rho$, $\mathbb E[\operatorname{sign}(X)\,Y] = \rho\,"
                    r"\mathbb E|X| = \rho\sqrt{2/\pi}$"),
                why(r"a year has $n$ bets with nearly uncorrelated outcomes: the mean grows like $n^{1 - H}$, the volatility "
                    r"like $n^{1/2 - H}$, and the Sharpe ratio without bound. This is an approximate arbitrage; Rogers "
                    r"(1997) and Cheridito (2003) build exact ones")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The simplest way to collect it. <bookmark mark='a'/> Hold one unit, long or short, and rebalance n times a "
            "year, betting that the next increment repeats the sign of the last, or reverses it if H is below one half. "
            "<bookmark mark='b'/> For a normal pair with correlation rho, the sign of one times the other has mean rho "
            "times root two over pi. So each bet earns a fixed fraction of the increment's size. <bookmark mark='c'/> "
            "Over a year of n bets the mean grows like n to the one minus H, the volatility only like n to the one half "
            "minus H, and the Sharpe ratio grows like root n, without bound. That is an approximate arbitrage. Chris "
            "Rogers in 1997 and Patrick Cheridito in 2003 built exact ones."
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

    def sharpe_plot(self, t):
        n = np.asarray(t["n"], float)
        x = _lg(n)
        g = axes([1.0, 5.0], [-2, 32], x_length=8.2, y_length=4.2, xlabel=r"trades a year, $n$",
                 ylabel=r"Sharpe ratio over a year, no costs", xticks=list(_lg([16, 256, 4096, 65536])),
                 yticks=[0, 10, 20, 30], xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", r"{,}"), font_size=15,
                 log_x=True).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        lines, dots = VGroup(), VGroup()
        for H in ("0.6", "0.5", "0.4"):
            r = t["H"][H]
            lines.add(curve(ax, x, r["theory"]["0"]["sharpe"], H_COL[H], stroke_width=3))
            dots.add(VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=H_COL[H]) for a, b in zip(x, r["sim"]["0"]["sharpe"])]))
        leg = legend([(H_COL["0.6"], r"$H = 0.6$: follow the last move"), (H_COL["0.5"], r"$H = 0.5$: Brownian"),
                      (H_COL["0.4"], r"$H = 0.4$: reverse it")], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(r"lines: the formula; dots: 160 simulated years of $\sigma B^H$ with $\sigma = 20\%$ "
                             r"(Davies--Harte, $2^{16}$ steps), traded on coarser grids", 3.3, 14, GREY_A).next_to(
            leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Simulate it, with no costs. <bookmark mark='a'/> At H of point six the Sharpe ratio is about one at a "
            "hundred trades a year, five at two thousand, and nearly thirty at sixty-five thousand. "
            "<bookmark mark='b'/> At H of point four, reversing the last move, the same. <bookmark mark='c'/> For "
            "Brownian motion, nothing: the sign of the last move says nothing about the next. The dots are simulations, "
            "the lines the formula."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(dots[0]), FadeIn(leg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines[2]), FadeIn(dots[2]), FadeIn(leg[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(lines[1]), FadeIn(dots[1]), FadeIn(leg[1]))
        self.wait(0.4)
        self.clear_scene()

    def costs(self):
        rows = [cmath(r"\mathbb E|\pi_k - \pi_{k-1}|", r"=", r"2p,\qquad p = \tfrac12 - \tfrac{1}{\pi}\arcsin\rho",
                      font_size=32, colors={r"\mathbb E|\pi_k - \pi_{k-1}|": ARB}),
                cmath(r"m(n)", r"=", r"n\Big[\sigma n^{-H}\sqrt{2/\pi}\,|\rho| - 2\varepsilon p\Big]", font_size=32,
                      colors={r"m(n)": FWD}),
                cmath(r"n^*", r"=", r"\bigg[\frac{(1 - H)\,\sigma\sqrt{2/\pi}\,|\rho|}{2\varepsilon p}\bigg]^{1/H}", font_size=32,
                      colors={r"n^*": HEDGE})]
        whys = [why(r"the position flips when two consecutive increments differ in sign: Sheppard's formula for a normal "
                    r"pair gives the probability $p$, 0.45 at $H = 0.6$"),
                why(r"pay $\varepsilon$ per unit traded: the edge per trade shrinks like $n^{-H}$ as the grid refines, the "
                    r"cost per trade does not"),
                why(r"so the yearly mean rises, peaks and falls: at $H = 0.6$, $\sigma = 20\%$, a cost of 1 bp gives $n^* "
                    r"\approx 2{,}300$ trades a year; 10 bp, about 50. A finite best, and no arbitrage")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Now charge for trading. <bookmark mark='a'/> The position flips when two consecutive increments differ "
            "in sign. For a normal pair the chance of that is Sheppard's formula, one half minus arcsine rho over pi: "
            "forty-five percent at H of point six. <bookmark mark='b'/> Pay epsilon per unit traded. As the grid "
            "refines, the edge per trade shrinks like n to the minus H, and the cost per trade does not shrink at all. "
            "<bookmark mark='c'/> So the yearly mean rises, peaks, and falls. With a one basis point cost the best is "
            "about twenty-three hundred trades a year; with ten basis points, about fifty. There is a best frequency, "
            "a finite profit, and a finite Sharpe ratio. The arbitrage is gone."
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

    def net_plot(self, t):
        r = t["H"]["0.6"]
        n = np.asarray(t["n"], float)
        x = _lg(n)
        lo, hi = -0.3, 0.7
        g = axes([1.0, 5.0], [lo, hi], x_length=8.2, y_length=4.2, xlabel=r"trades a year, $n$",
                 ylabel=r"mean log return a year, $H = 0.6$", xticks=list(_lg([16, 256, 4096, 65536])),
                 yticks=[-0.2, 0, 0.2, 0.4, 0.6], xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", r"{,}"),
                 yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=15, log_x=True).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(1.0, 0), ax.c2p(5.0, 0), color=GREY_C, stroke_width=1.2)
        xf = np.linspace(1.2, 4.82, 200)
        nf = 10 ** xf
        rho, p, sig, H = r["rho"], r["pflip"], t["sigma"], 0.6
        lines, dots, stars = VGroup(), VGroup(), VGroup()
        for k, e in t["eps"].items():
            m = nf * (sig * nf ** -H * np.sqrt(2 / np.pi) * abs(rho) - 2 * e * p)
            keep = (m >= lo) & (m <= hi)
            lines.add(curve(ax, xf[keep], m[keep], E_COL[k], stroke_width=3))
            sm = np.asarray(r["sim"][k]["mean"])
            ok = (sm >= lo) & (sm <= hi)
            dots.add(VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=E_COL[k]) for a, b in zip(x[ok], sm[ok])]))
            if k in r.get("best", {}):
                b = r["best"][k]
                stars.add(VGroup(Star(n=5, outer_radius=0.13, color=E_COL[k], fill_opacity=1).move_to(
                    ax.c2p(np.log10(b["n_star"]), b["mean"])),
                    MathTex(rf"n^* \approx {b['n_star']:,.0f}".replace(",", "{,}"), font_size=20, color=E_COL[k]).next_to(
                        ax.c2p(np.log10(b["n_star"]), b["mean"]), UP, buff=0.18)))
        leg = legend([(E_COL["0"], r"no cost"), (E_COL["1bp"], r"1 bp per unit traded"),
                      (E_COL["10bp"], r"10 bp per unit traded")], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(r"lines: $m(n)$; dots: the same 160 simulated years. Without a cost the mean keeps rising, "
                             r"to 200\% a year at $2^{16}$ trades", 3.3, 14, GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        b1, b10 = r["best"]["1bp"], r["best"]["10bp"]
        with self.voiceover(
            "Here it is at H of point six. <bookmark mark='a'/> Without a cost the mean keeps rising, off the top of "
            "the chart. <bookmark mark='b'/> At one basis point it peaks near twenty-three hundred trades a year, at "
            f"about {100 * b1['mean']:.0f} percent, and turns negative beyond ten thousand. <bookmark mark='c'/> At ten "
            f"basis points the peak is about fifty trades a year and {100 * b10['mean']:.0f} percent. The simulations "
            "sit on the formula."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(dots[0]), FadeIn(leg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines[1]), FadeIn(dots[1]), FadeIn(leg[1]), FadeIn(stars[0]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(lines[2]), FadeIn(dots[2]), FadeIn(leg[2]), FadeIn(stars[1]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def cps(self):
        body = VGroup(
            wrapped_label(r"with proportional cost $\varepsilon$, a market has no arbitrage (robustly) if and only if there "
                          r"is an $\varepsilon$-consistent price system: a measure $Q$ and a $Q$-martingale $\tilde S$ "
                          r"with", 10.4, 21, GREY_A),
            MathTex(r"\frac{S_t}{1 + \varepsilon}\ \le\ \tilde S_t\ \le\ (1 + \varepsilon)\,S_t\quad\text{for all } t",
                    font_size=32, color=Q_C),
            wrapped_label(r"a continuous price with conditional full support (from any point, every nearby path stays "
                          r"possible) has one for every $\varepsilon > 0$. Fractional Brownian motion does", 10.4, 21,
                          GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        thm = theorem_card(r"Consistent price systems", body,
            who=r"Jouini and Kallal (1995); Guasoni (2006); Guasoni, R\'asonyi and Schachermayer (2008)", width=11.6,
            font_size=22).move_to(UP * 0.5)
        note_ = why(r"Part 14's rough volatility is rough in the variance, not the price: its prices stay semimartingales, "
                    r"and its models are arbitrage-free without any cost").to_edge(DOWN, buff=0.45)
        if note_.width > 12.6:
            note_.scale_to_fit_width(12.6)
        with self.voiceover(
            "The general theorem replaces Chapter 4's martingale measure with a band. <bookmark mark='a'/> With a "
            "proportional cost epsilon, there is no arbitrage, robustly, exactly when some martingale under some "
            "measure stays within a factor of one plus epsilon of the price at all times: a consistent price system. "
            "Elyès Jouini and Hédi Kallal proved the first version in 1995. <bookmark mark='b'/> Paolo Guasoni, Miklós "
            "Rásonyi and Walter Schachermayer showed in 2008 that any continuous price with conditional full support, "
            "meaning every nearby path stays possible from wherever you are, has such a martingale for every epsilon, "
            "however small. Fractional Brownian motion qualifies. <bookmark mark='c'/> One clarification. Part 14's "
            "rough volatility is rough in the variance, not the price. Its prices remain semimartingales, and its "
            "models need no cost to be free of arbitrage."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(Indicate(body[2], color=Q_C, scale_factor=1.03))
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.wait(0.5)
        self.clear_scene()

    def btc(self, t):
        b = t["btc"]
        hx = [-4.6, -2.2, 0.0, 2.4, 4.9]
        head = VGroup(label(r"Bitcoin, sampled every", font_size=18, color=GREY_B), label(r"$\rho$", font_size=22),
                      label(r"implied $H$", font_size=20), label(r"break-even cost", font_size=20, color=HEDGE),
                      label(r"net per trade at 1 bp", font_size=20, color=ARB))
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(label(rf"{m} min", font_size=20, color=FWD),
                                                 MathTex(rf"{b[m]['rho']:+.3f}", font_size=26),
                                                 MathTex(rf"{b[m]['H_implied']:.2f}", font_size=26),
                                                 MathTex(rf"{b[m]['breakeven_bp']:.2f}\ \text{{bp}}", font_size=26),
                                                 MathTex(rf"{1e4 * b[m]['net_1bp'] * int(m) / 525600:+.2f}\ \text{{bp}}",
                                                         font_size=26))
                                          for m in ("1", "5", "15", "60")]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.72 * j, 0])
            tab.add(row)
        foot = wrapped_label(r"BTCUSDT one-minute closes, Binance, 2019--2020; $\rho$: first-order autocorrelation of log "
                             r"returns at each sampling; implied $H$ from $\rho = 2^{2H-1} - 1$; the sign strategy reverses "
                             r"the last move ($\rho < 0$); break-even: the cost per unit traded that sets its mean to zero",
                             11.8, 16, GREY_A).to_edge(DOWN, buff=0.45)
        be_max = max(v["breakeven_bp"] for v in b.values())
        with self.voiceover(
            "Is a real price fractional? Bitcoin, sampled every one, five, fifteen and sixty minutes, in 2019 and 2020. "
            "<bookmark mark='a'/> The autocorrelations are small and negative, so the implied H is just under one half, "
            "and the strategy reverses the last move. <bookmark mark='b'/> At one minute it loses even before costs. "
            "At the other samplings its break-even cost is at most about "
            f"{be_max:.1f} basis points per unit traded: at a one basis point "
            "cost it loses everywhere except hourly, where it makes a tenth of a basis point a trade. "
            "<bookmark mark='c'/> The market's memory is about the size of the cost of exploiting it. That is what "
            "the theorem predicts a market with frictions can sustain."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1], r_[2])) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[3], r_[4])) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(*[Indicate(r_[3], color=HEDGE) for r_ in tab[1:]])
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: the size of the price band", r"a consistent price system exists for every "
                          r"$\varepsilon$, but which $Q$ and which band, and so which super-replication prices, "
                          r"follow from a given memory, is known only in special cases", width=12.4, font_size=18),
            desk_question(r"open: optimal trading with memory and costs", r"for fractional prices with costs, the "
                          r"optimal portfolio and its asymptotics as $\varepsilon \to 0$ are incomplete beyond the simplest "
                          r"utilities (Guasoni, Nika and R\'asonyi 2019 solve it with temporary price impact instead)", width=12.4,
                          font_size=18),
            desk_question(r"open: does memory in prices survive anywhere?", r"estimates of $H$ in prices are close to "
                          r"$\frac12$ once microstructure is removed; whether any liquid market keeps memory larger "
                          r"than its cost is an empirical question", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> A consistent price system exists for every epsilon, but which "
            "one, and so which band of super-replication prices a given memory implies, is known only in special "
            "cases. <bookmark mark='b'/> The optimal portfolio for a fractional price with costs, and how it behaves as "
            "the cost shrinks, is incomplete beyond the simplest utilities. <bookmark mark='c'/> And empirically: once "
            "microstructure is removed, estimates of H in prices sit near one half. Whether any liquid market keeps "
            "more memory than it costs to trade is an open question of data."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"at $H = 0.6$ the best trading frequency with a 1 bp cost is about 2,300 a year. If the cost "
                       r"doubles to 2 bp, by what factor does $n^*$ change?")
        with self.voiceover(
            "Pause and predict. At H of point six, a one basis point cost gives a best frequency of about twenty-three "
            "hundred trades a year. If the cost doubles, by what factor does the best frequency change?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
