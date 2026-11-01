from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import bs
from videos.quant.quant10.common import CASH, IMP, OPT, PART, PP, SPOT


class History(VoiceoverScene):
    def construct(self):
        self.card()
        self.before()
        self.missing()
        self.trio()
        self.exchange()

    def card(self):
        c = chapter_card(1, r"Before the formula", r"Why did it take seventy-three years?",
                         lit=(1900, 1965, 1967, 1969, 1973), part=PART)
        with self.voiceover("Chapter one. Before the formula."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def before(self):
        cards = VGroup(
            history_card(1900, r"Louis Bachelier, Paris", r"prices options on French government bonds with a "
                         r"random walk, and checks them against the market's quotes", width=4.4, font_size=25),
            history_card(1961, r"Case Sprenkle, Yale", r"a lognormal price and an option worth its expected "
                         r"payoff, discounted, but at what rate, and growing at what rate?", width=4.4, font_size=25),
            history_card(1965, r"Paul Samuelson, MIT", r"\textit{Rational theory of warrant pricing}: the same "
                         r"two unknown rates, now with a free boundary", width=4.4, font_size=25),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).to_edge(UP, buff=0.45)
        strip = timeline(lit=(1900, 1965)).to_edge(DOWN, buff=0.7)
        # Bachelier's picture: a random walk whose spread grows like the square root of time (illustrative)
        ax = Axes(x_range=[0, 1, 1], y_range=[-1, 1, 1], x_length=9.0, y_length=2.4, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False, "stroke_width": 1.5})
        ax.next_to(cards, DOWN, buff=0.45)
        rng = np.random.default_rng(1900)
        n = 300
        walks = VGroup()
        for _ in range(14):
            w = np.concatenate([[0], np.cumsum(rng.standard_normal(n))]) / np.sqrt(n) * 0.42
            m = VMobject(stroke_width=1.6, stroke_color=SPOT, stroke_opacity=0.45)
            m.set_points_as_corners([ax.c2p(i / n, y) for i, y in enumerate(w)])
            walks.add(m)
        env = VGroup(*[ax.plot(lambda x, s=s: s * 0.84 * np.sqrt(x), x_range=[0, 1], color=SPOT, stroke_width=2.5)
                       for s in (1, -1)])
        env_lab = MathTex(r"\pm\,\sigma\sqrt t", font_size=30, color=SPOT).next_to(env[0], RIGHT, buff=0.1)
        ill = note(r"illustrative", font_size=18).next_to(ax, DOWN, buff=0.08).align_to(ax, RIGHT)
        with self.voiceover(
            "People priced options long before 1973. Louis Bachelier's thesis of 1900, the one this series began "
            "with, priced options on French government bonds with a random walk and compared his prices with "
            "the quotes on the Paris exchange. <bookmark mark='a'/> Then the idea slept for half a century. In "
            "the 1950s and 60s economists rediscovered Bachelier, replaced his random walk with a lognormal price "
            "that cannot go negative, and wrote down what an option should be worth: its expected payoff, "
            "discounted. Case Sprenkle in 1961, James Boness in 1964, <bookmark mark='b'/> Paul Samuelson in 1965. "
            "Their formulas look almost exactly like the one we will derive. Almost."
        ) as vo:
            self.play(FadeIn(strip), FadeIn(cards[0], shift=UP * 0.2))
            self.play(LaggedStart(*[Create(w) for w in walks], lag_ratio=0.08, run_time=3), FadeIn(ill))
            self.play(Create(env), FadeIn(env_lab))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def missing(self):
        col = {r"\mu": PP, r"\rho": PP, r"r": CASH, r"\sigma": IMP, r"S": SPOT, r"C": OPT}
        f1 = cmath(r"C", r"=", r"e^{-", r"\rho", r"T}", r"\Big[", r"S", r"e^{", r"\mu", r"T}", r"N(d_1)", r"-", r"K",
                   r"N(d_2)", r"\Big]", font_size=46, colors=col)
        d1 = cmath(r"d_{1,2}", r"=", r"\frac{\ln(S/K) + (", r"\mu", r"\pm \tfrac12", r"\sigma", r"^2)T}{",
                   r"\sigma", r"\sqrt T}", font_size=38, colors=col)
        g1 = VGroup(f1, d1).arrange(DOWN, buff=0.45).shift(UP * 0.8)
        f2 = cmath(r"C", r"=", r"e^{-", r"r", r"T}", r"\Big[", r"S", r"e^{", r"r", r"T}", r"N(d_1)", r"-", r"K",
                   r"N(d_2)", r"\Big]", font_size=46, colors=col).move_to(f1)
        d2 = cmath(r"d_{1,2}", r"=", r"\frac{\ln(S/K) + (", r"r", r"\pm \tfrac12", r"\sigma", r"^2)T}{",
                   r"\sigma", r"\sqrt T}", font_size=38, colors=col).move_to(d1)
        mu_note = label(r"$\mu$: how fast the stock is expected to grow", font_size=26, color=PP)
        rho_note = label(r"$\rho$: what return an investor demands for holding the option", font_size=26, color=PP)
        notes = VGroup(mu_note, rho_note).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(g1, DOWN, buff=0.7)
        r_note = label(r"$r$: the riskless interest rate, which anyone can look up", font_size=28, color=CASH)
        r_note.move_to(notes)
        with self.voiceover(
            "Here is the shape of the Sprenkle and Samuelson formula for a call. The stock price S, grown at an "
            "expected rate mu to maturity, times a probability-like weight; the strike K times another; the whole "
            "thing discounted at a rate rho. <bookmark mark='a'/> And there was the problem. Mu is how fast the "
            "stock is expected to grow; rho is the return an investor would demand for holding something as risky "
            "as an option. Nobody knows either. Every investor would plug in different numbers and get a "
            "different price. A formula with two unobservable inputs is not much of a formula. "
            "<bookmark mark='b'/> The Black-Scholes formula is this one with both of them replaced by a single "
            "number anyone can look up: the riskless interest rate r. The expected return of the stock does not "
            "appear. Not because it is small, but because it does not matter. Why it does not matter is the "
            "whole content of this part."
        ) as vo:
            self.play(Write(f1), run_time=2)
            self.play(FadeIn(d1))
            vo.wait_until("a")
            self.play(FadeIn(notes, shift=UP * 0.2))
            for m in (term(f1, r"\mu"), term(f1, r"\rho"), term(d1, r"\mu")):
                self.play(Indicate(m, color=PP, scale_factor=1.4), run_time=0.6)
            vo.wait_until("b")
            self.play(TransformMatchingTex(f1, f2), TransformMatchingTex(d1, d2), ReplacementTransform(notes, r_note),
                      run_time=2)
            self.play(Circumscribe(VGroup(f2, d2), color=CASH, buff=0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def trio(self):
        cards = VGroup(
            history_card(1967, r"Edward Thorp and Sheen Kassouf", r"\textit{Beat the Market}: sell overpriced "
                         r"warrants, hedge with the stock, rebalance as the price moves", width=4.4, font_size=25),
            history_card(1969, r"Fischer Black and Myron Scholes", r"price the hedged position with the CAPM: it "
                         r"has no market risk, so it must earn the riskless rate", width=4.4, font_size=25),
            history_card(1970, r"Robert Merton", r"trade continuously and the hedge is perfect: no CAPM needed, "
                         r"only the absence of arbitrage", width=4.4, font_size=25),
        ).arrange(RIGHT, buff=0.28, aligned_edge=UP).to_edge(UP, buff=0.45)
        # Thorp's hedge: short a warrant (a call), long h shares; near today's price the sum is flat
        hx = axes([70, 130], [-25, 18], x_length=7.4, y_length=2.6, xlabel=r"stock price at the next instant",
                  xticks=[80, 100, 120], font_size=18).next_to(cards, DOWN, buff=0.35)
        a2 = hx.ax
        xs = np.linspace(70, 130, 121)
        c0 = float(bs.price(100, 100, 0.5, 0.3))
        h = float(bs.greeks(100, 100, 0.5, 0.3)["delta"])
        short = a2.plot_line_graph(xs, -(bs.price(xs, 100, 0.5, 0.3) - c0), line_color=OPT, add_vertex_dots=False,
                                   stroke_width=3)
        stock = a2.plot_line_graph(xs, h * (xs - 100), line_color=SPOT, add_vertex_dots=False, stroke_width=3)
        both = a2.plot_line_graph(xs, h * (xs - 100) - (bs.price(xs, 100, 0.5, 0.3) - c0), line_color=WHITE,
                                  add_vertex_dots=False, stroke_width=4)
        hl = VGroup(label(r"short a warrant", font_size=20, color=OPT), label(rf"long ${h:.2f}$ shares",
                    font_size=20, color=SPOT), label(r"together", font_size=20)).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.12)
        hl.next_to(hx, RIGHT, buff=0.3)
        quote = label(r"published 1973: \textit{The Pricing of Options and Corporate Liabilities} (JPE) and "
                      r"\textit{Theory of Rational Option Pricing} (Bell Journal)", font_size=22, color=GREY_A)
        quote.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The way out came from three directions at once. In 1967 Edward Thorp, the mathematician who had "
            "beaten blackjack, and the economist Sheen Kassouf published a book on warrants, long-dated options "
            "issued by companies. Their method: sell the overpriced warrants and hold the stock against them, "
            "adjusting as the price moves. A hedge: the short warrant loses when the stock rises, the shares gain, "
            "and at today's price the two cancel: the white curve is flat there. It bends down only for big moves, "
            "and that bend will turn out to be where all of this part's money is made and lost. Thorp has said he was trading with a formula equivalent to "
            "Black-Scholes by 1969, and kept it to himself. <bookmark mark='a'/> At the same time Fischer Black, "
            "a consultant with a physics degree, and Myron Scholes, a young professor at MIT, asked what a hedged "
            "position is worth. If the hedge removes the market risk, the capital asset pricing model says the "
            "position must earn the riskless rate. <bookmark mark='b'/> Their colleague Robert Merton saw the "
            "deeper reason: trade continuously, and the hedge is not just low risk, it is riskless. Then no model "
            "of investors is needed at all, only the absence of arbitrage. <bookmark mark='c'/> Black and Scholes's "
            "paper was turned down by the first journals they sent it to. It appeared in the Journal of "
            "Political Economy in the spring of 1973, alongside Merton's in the Bell Journal."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            self.play(FadeIn(hx), Create(short), FadeIn(hl[0]))
            self.play(Create(stock), FadeIn(hl[1]))
            self.play(Create(both), FadeIn(hl[2]))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(quote))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def exchange(self):
        card = history_card(1973, r"26 April: the Chicago Board Options Exchange opens",
                            r"standardized calls on 16 stocks, traded in a converted smoking lounge of the Board of "
                            r"Trade", width=7.2, font_size=27).to_corner(UL, buff=0.5)
        pts = VGroup(*[wrapped_label(t, 6.4, 28, GREY_A) for t in (
            r"within a few years: the formula on traders' calculators and printed sheets",
            r"traders quote \emph{volatility}, not price",
            r"1997: the Nobel prize for Scholes and Merton (Black died in 1995)",
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(card, DOWN, buff=0.6).align_to(card, LEFT)

        strip = timeline(lit=(1973, 1997)).to_edge(DOWN, buff=0.6)
        # a sheet of theoretical values, as floor traders carried them (illustrative: stock 45, volatility 25%)
        strikes, months = (40, 45, 50), (3, 6, 9)
        head = VGroup(label(r"strike", font_size=22, color=GREY_B),
                      *[label(rf"{m} months", font_size=22, color=GREY_B) for m in months])
        rows = [head]
        for k in strikes:
            rows.append(VGroup(MathTex(str(k), font_size=28, color=QC.STRIKE),
                               *[MathTex(f"{float(bs.price(45, k, m / 12, 0.25, 0.06)):.2f}", font_size=28,
                                         color=OPT) for m in months]))
        tab = VGroup(*[VGroup(*r) for r in rows])
        for r in tab:
            for j, c in enumerate(r):
                c.move_to([j * 1.55, 0, 0])
        tab.arrange(DOWN, buff=0.28)
        for r in tab:
            for j, c in enumerate(r):
                c.set_x(j * 1.55)
        sheet_title = label(r"Theoretical values: stock 45, volatility 25\%, rate 6\%", font_size=22, color=GREY_A)
        frame = SurroundingRectangle(tab, buff=0.3, color=GREY_D, corner_radius=0.08, stroke_width=1.5)
        sheet = VGroup(sheet_title, VGroup(frame, tab)).arrange(DOWN, buff=0.18)
        sheet.to_edge(RIGHT, buff=0.45).shift(DOWN * 0.4)
        sheet.add(note(r"illustrative", font_size=16).next_to(frame, DOWN, buff=0.06).align_to(frame, RIGHT))
        with self.voiceover(
            "A month before the paper appeared, on the twenty-sixth of April 1973, the Chicago Board Options "
            "Exchange opened, with standardized calls on sixteen stocks. Within a few years traders on the floor "
            "carried the formula on calculators and on printed sheets of theoretical prices, and the sociologist "
            "Donald MacKenzie has argued that the market came to price options the way the formula said "
            "because traders used it. <bookmark mark='a'/> They stopped quoting options in dollars and started "
            "quoting them in volatility, the one input of the formula that cannot be looked up. "
            "<bookmark mark='b'/> In 1997 Scholes and Merton received the Nobel prize; Black had died two years "
            "before. Now let us derive what they found."
        ) as vo:
            self.play(FadeIn(strip), FadeIn(card, shift=UP * 0.2))
            self.play(FadeIn(pts[0]), FadeIn(sheet, shift=LEFT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(pts[1]))
            vo.wait_until("b")
            self.play(FadeIn(pts[2]))
        self.wait(0.4)
        self.clear_scene()
