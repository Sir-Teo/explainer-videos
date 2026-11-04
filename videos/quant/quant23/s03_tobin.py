from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant23.common import BAD, FRONT, GOOD, MKT, PART, TAN, ask, fit_right, illustration, load


class Tobin(VoiceoverScene):
    def construct(self):
        f = load("frontier")
        self.card()
        self.cml()
        self.picture(f)
        self.oos(f)
        self.fixes()

    def card(self):
        c = chapter_card(2, r"Cash, the tangency, and estimation error", r"Why does everyone hold the same risky portfolio?",
                         lit=(1958,), part=PART)
        with self.voiceover("Chapter two. Add a riskless asset, and the frontier becomes a straight line."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def cml(self):
        rows = [cmath(r"\mu_p", r"=", r"R^f + \frac{\mu_T - R^f}{\sigma_T}\,\sigma_p", font_size=42, colors={r"\mu_p": TAN}),
                cmath(r"w_T", r"\propto", r"\Sigma^{-1}(\mu - R^f\mathbf{1}),\quad SR_{\max} = \sqrt{(\mu - R^f)^\top"
                      r"\Sigma^{-1}(\mu - R^f)}", font_size=34, colors={r"w_T": TAN})]
        whys = [why(r"mixing a risky portfolio with cash moves along a straight line in mean and volatility; the steepest "
                    r"line touches the bullet at the tangency portfolio $T$: the capital market line"),
                why(r"Tobin (1958): every investor holds the same risky portfolio, in different amounts. Attitude to risk "
                    r"decides only how much cash. The line's slope is the largest Sharpe ratio the assets allow")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Now add a riskless asset: cash, earning the bill rate. Mixing any risky portfolio with cash moves along a "
            "straight line from the bill rate. The best such line is the steepest, and it touches the bullet at one "
            "portfolio, the tangency. <bookmark mark='a'/> James Tobin's separation theorem follows: everyone who uses "
            "the same estimates holds the same risky portfolio, the tangency, and differs only in how much cash they "
            "hold beside it. The slope of the line is the largest Sharpe ratio the assets can offer. A cautious investor "
            "puts a third of the money in the tangency and the rest in bills; a bold one borrows and holds one and a "
            "half times their capital in it. Both hold the same stocks in the same proportions. Choosing the portfolio "
            "and choosing the risk are separate decisions, which is why a fund can serve investors it has never met."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def picture(self, f):
        ms, sig = np.asarray(f["ms"]), np.asarray(f["sig"])
        g = axes([0, 0.32], [0.0, 0.24], x_length=7.4, y_length=4.4, xlabel=r"volatility, a year", ylabel=r"mean return, a year",
                 xticks=[0, 0.1, 0.2, 0.3], yticks=[0, 0.05, 0.10, 0.15, 0.20], font_size=14).to_edge(LEFT, buff=0.5).shift(
            DOWN * 0.3)
        ax = g.ax
        ok = sig <= 0.32
        line = curve(ax, sig[ok], ms[ok], FRONT, stroke_width=3)
        t = f["tan"]
        rf = f["rf"]
        cml = Line(ax.c2p(0, rf), ax.c2p(0.32, rf + t["sharpe"] * 0.32), color=TAN, stroke_width=3)
        swing = ValueTracker(0.25)
        ray = always_redraw(lambda: Line(ax.c2p(0, rf), ax.c2p(0.32, rf + swing.get_value() * 0.32), color=GREY_B,
                                         stroke_width=2))
        tdot = VGroup(Dot(ax.c2p(t["sd"], t["mu"]), color=TAN, radius=0.08),
                      label(r"tangency", font_size=15, color=TAN).next_to(ax.c2p(t["sd"], t["mu"]), UP, buff=0.08))
        mk = f["mkt"]
        mdot = VGroup(Dot(ax.c2p(mk["sd"], mk["mu"]), color=MKT, radius=0.08),
                      label(r"market", font_size=15, color=MKT).next_to(ax.c2p(mk["sd"], mk["mu"]), DOWN, buff=0.08))
        side = VGroup(
            MathTex(rf"SR_{{\text{{tangency}}}} = {t['sharpe']:.2f}", font_size=26, color=TAN),
            MathTex(rf"SR_{{\text{{market}}}} = {f['mkt_sharpe']:.2f}", font_size=26, color=MKT),
            wrapped_label(r"the bill rate's average since 1990, and the ten industries' sample means and covariance. The "
                          r"market sits inside the frontier: in sample, it was not efficient", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Draw it on the industries. <bookmark mark='a'/> Swing a line up from the bill rate until it just touches "
            "the frontier. <bookmark mark='b'/> That is the capital market line, and the point of contact is the "
            f"tangency portfolio, with a Sharpe ratio of {t['sharpe']:.2f}. The stock market itself, at "
            f"{f['mkt_sharpe']:.2f}, sits inside: in this sample, a mix of industries would have beaten it handily. "
            "Would it, though, in advance?"
        ) as vo:
            self.play(FadeIn(g), Create(line))
            vo.wait_until("a")
            self.add(ray)
            self.play(swing.animate.set_value(t["sharpe"]), run_time=2.5)
            vo.wait_until("b")
            self.remove(ray)
            self.play(Create(cml), FadeIn(tdot), FadeIn(mdot), LaggedStart(*[FadeIn(x_) for x_ in side], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def oos(self, f):
        o = f["oos"]
        rows = [(r"tangency, fitted 1990--2007: in sample", o["in_sharpe"], GREY_A),
                (r"the same weights, 2008--2020", o["oos_sharpe"], BAD),
                (r"minimum variance, fitted 1990--2007", o["gmv_sharpe"], GOOD),
                (r"equal weights, $1/N$", o["eq_sharpe"], TAN),
                (r"the market", o["mkt_sharpe"], MKT)]
        g = axes([0, 1.0], [-0.6, len(rows) - 0.4], x_length=6.0, y_length=4.0, xlabel=r"Sharpe ratio, a year",
                 ylabel=r"", xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[], font_size=14).to_edge(RIGHT, buff=0.8).shift(
            DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for i, (nm, v, c_) in enumerate(rows):
            y = len(rows) - 1 - i
            x0, x1 = ax.c2p(0, 0)[0], ax.c2p(v, 0)[0]
            b_ = Rectangle(width=max(x1 - x0, 0.01), height=0.5, stroke_width=0, fill_color=c_, fill_opacity=0.85).move_to(
                [(x0 + x1) / 2, ax.c2p(0, y)[1], 0])
            bars.add(VGroup(b_, MathTex(f"{v:.2f}", font_size=22).next_to(b_, RIGHT, buff=0.08),
                            label(nm, font_size=16).next_to([x0 - 0.15, ax.c2p(0, y)[1], 0], LEFT, buff=0)))
        foot = wrapped_label(rf"the in-sample tangency held short positions adding to {100 * o['short']:.0f}\% of capital. "
                             r"DeMiguel, Garlappi and Uppal (2009): across many datasets, no optimiser reliably beats "
                             r"$1/N$ out of sample; the estimation error in the means outweighs the gain from optimising",
                             12.4, 17, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Test it honestly. Fit the tangency on 1990 to 2007, then hold those weights from 2008 to 2020, the end of the research window. "
            f"<bookmark mark='a'/> In sample, its Sharpe ratio was {o['in_sharpe']:.2f}. Out of sample it earned "
            f"{o['oos_sharpe']:.2f}, worse than the market's {o['mkt_sharpe']:.2f}, worse than simply holding the ten "
            f"industries in equal amounts, {o['eq_sharpe']:.2f}, and worse than the minimum-variance portfolio, which "
            f"never looked at a mean return, {o['gmv_sharpe']:.2f}. <bookmark mark='b'/> Victor DeMiguel, Lorenzo "
            "Garlappi and Raman Uppal found the same across many datasets: the error in estimated means swamps the gain "
            "from optimising. This is the first lesson of quantitative investing, and Part thirty returns to it."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def fixes(self):
        cards = VGroup(
            desk_question(r"shrink the inputs", r"pull estimated means toward a common value and covariances toward a "
                          r"structured target (Ledoit and Wolf, 2004): less error, at the cost of some bias", width=12.0,
                          font_size=21),
            desk_question(r"constrain the weights", r"no shorts, position limits: Jagannathan and Ma (2003) showed that "
                          r"constraints act like shrinkage on the covariance matrix", width=12.0, font_size=21),
            desk_question(r"start from equilibrium", r"Black and Litterman (1992): begin with the means that make the "
                          r"market portfolio optimal, and tilt them only where you have views", width=12.0, font_size=21),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Practitioners have three remedies, all covered properly in Part thirty. <bookmark mark='a'/> Shrink the "
            "estimates: pull the means toward each other and the covariance toward a simple structure. "
            "<bookmark mark='b'/> Constrain the weights; Ravi Jagannathan and Tongshu Ma showed that a ban on short "
            "sales acts like shrinkage. <bookmark mark='c'/> Or start from equilibrium: Fischer Black and Robert "
            "Litterman began with the expected returns that would make the market portfolio optimal, which is exactly "
            "the idea of the next chapter."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a mean return is estimated from 30 years of data with 18\% volatility. What is its standard error, and "
                r"how many years would halve it?")
        with self.voiceover("A mean return is estimated from thirty years of data with eighteen percent volatility. What "
                            "is its standard error, and how many years would halve it?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
