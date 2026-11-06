from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import bs
from videos.quant.quant10.common import CASH, DEL, GAIN, IMP, LOSS, OPT, PART, QQ, SPOT, computed, load

C_ = {r"q": LOSS, r"r": CASH, r"F": QQ, r"S": SPOT, r"V": OPT, r"\Delta": DEL, r"X": CASH}


def row(*parts, fs=34):
    return cmath(*parts, colors=C_, font_size=fs)


class Carry(VoiceoverScene):
    def construct(self):
        c = load("carry")
        self.card()
        self.slider()
        self.derive()
        self.family()
        self.surface(c)

    def card(self):
        c = chapter_card(13, r"Dividends, borrow and the forward", r"What does the formula need to know about carry?",
                         lit=(1973,), part=PART)
        with self.voiceover("Chapter thirteen. Dividends, borrow and the forward."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def slider(self):
        S0, K, T, sig = 100.0, 100.0, 1.0, 0.25
        n, m = 60, 40
        t = np.linspace(0, T, n + 1)
        rng = np.random.default_rng(1013)
        W = np.concatenate([np.zeros((m, 1)), np.cumsum(rng.standard_normal((m, n)) * np.sqrt(T / n), 1)], 1)
        g = axes([0, 1], [40, 180], x_length=6.4, y_length=4.4, xlabel=r"years", ylabel=r"stock price under $\mathbb Q$",
                 xticks=[0, 0.5, 1], yticks=[50, 100, 150], font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        b = ValueTracker(0.05)

        def fan():
            bb = b.get_value()
            P = S0 * np.exp((bb - 0.5 * sig ** 2) * t + sig * W)
            grp = path_fan(ax, t, P, color=QQ, opacity=0.3, stroke_width=1.2)
            grp.add(curve(ax, t, S0 * np.exp(bb * t), QQ, stroke_width=4))
            return grp

        fan_ = always_redraw(fan)
        kline = DashedLine(ax.c2p(0, K), ax.c2p(1, K), color=QC.STRIKE, stroke_width=1.5)
        r = 0.05

        def bars():
            q = r - b.get_value()
            vals = [(r"call", float(bs.price(S0, K, T, sig, r, q)), OPT),
                    (r"put", float(bs.price(S0, K, T, sig, r, q, -1)), LOSS),
                    (r"call $\Delta$", 20 * float(bs.greeks(S0, K, T, sig, r, q)["delta"]), DEL)]
            grp = VGroup()
            for i, (name, v, col) in enumerate(vals):
                bar = Rectangle(width=0.55, height=max(v * 0.17, 0.02), stroke_width=0, fill_color=col,
                                fill_opacity=0.85).move_to([3.2 + i * 1.3, -2.6, 0], aligned_edge=DOWN)
                txt = (rf"{v:.2f}" if i < 2 else rf"{v / 20:.2f}")
                grp.add(bar, MathTex(txt, font_size=24, color=col).next_to(bar, UP, buff=0.08),
                        label(name, font_size=20, color=col).next_to([3.2 + i * 1.3, -2.6, 0], DOWN, buff=0.12))
            return grp

        bars_ = always_redraw(bars)
        bread = always_redraw(lambda: MathTex(rf"b = r - q = {100 * b.get_value():+.1f}\%", font_size=34, color=QQ)
                              .move_to([4.5, 2.6, 0]))
        fread = always_redraw(lambda: MathTex(rf"F = S e^{{bT}} = {S0 * np.exp(b.get_value() * T):.1f}", font_size=30,
                                              color=QQ).move_to([4.5, 1.9, 0]))
        params = note(r"$S = K = 100$, $T = 1$, $\sigma = 25\%$, $r = 5\%$", font_size=20).to_corner(DR, buff=0.25)
        with self.voiceover(
            """Carry changes the forward: dividends, foreign interest, or securities-lending income under an idealized model enter as a reinvestable yield q. With constant rates, b equals r minus q. <bookmark mark='a'/> Raise q: the risk-neutral fan tilts down, the call loses value and the put gains. Pause: the call's share delta? <bookmark mark='b'/> It falls too, including the yield discount. <bookmark mark='c'/> Treating a borrow fee as this yield requires symmetric access and reinvestment. Actual hard-to-borrow constraints can break that equality, as Part nine emphasized."""
        ) as vo:
            self.play(FadeIn(g), Create(kline), FadeIn(params))
            self.add(fan_, bars_, bread, fread)
            vo.wait_until("a")
            self.play(b.animate.set_value(-0.04), run_time=4)
            vo.wait_until("b")
            self.play(b.animate.set_value(0.05), run_time=2)
            vo.wait_until("c")
            self.play(b.animate.set_value(-0.10), run_time=3)
        for m_ in (fan_, bars_, bread, fread):
            m_.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            row(r"dX", r"=", r"\Delta", r"\,(dS +", r"q", r"S\,dt)", r"+", r"r", r"(X -", r"\Delta", r"S)\,dt"),
            row(r"V_t", r"+", r"(", r"r", r"-", r"q", r")\,", r"S", r"V_S", r"+", r"\tfrac12\sigma^2", r"S", r"^2V_{SS}",
                r"-", r"r", r"V", r"=", r"0"),
            row(r"V", r"=", r"e^{-", r"r", r"T}\big[", r"F", r"N(d_1) - K N(d_2)\big],\quad", r"F", r"=", r"S",
                r"e^{(", r"r", r"-", r"q", r")T}"),
            row(r"\Delta", r"=", r"e^{-", r"q", r"T}N(d_1),\qquad", r"\partial_F V", r"=", r"e^{-", r"r", r"T}N(d_1)"),
        ]
        whys = [why(r"self-financing again, but each share now pays the yield $q$ to its holder"),
                why(r"match the $dW$ and $dt$ terms as in chapter 2: the drift becomes $r - q$"),
                why(r"solve as in chapter 3, with $d_{1,2} = [\ln(F/K) \pm \tfrac12\sigma^2T]/\sigma\sqrt T$"),
                why(r"the hedge in shares, and in futures on $F$")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.4, buff=0.75, edge=6.9)
        with self.voiceover(
            "In symbols, the replication of chapter two with one change: the shares in the hedge pay the yield q "
            "to whoever holds them. <bookmark mark='a'/> Match the terms, and the equation's drift becomes r "
            "minus q. <bookmark mark='b'/> Solve it as in chapter three, and the price is the formula written on "
            "the forward: discount, times forward times N of d one, minus strike times N of d two, with the d's "
            "measured from the forward. <bookmark mark='c'/> The hedge in shares carries an extra discount, e to "
            "the minus q T; hedged with futures on the forward, it is N of d one discounted at r."
        ) as vo:
            step(0, run_time=0.15)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def family(self):
        items = [
            (r"a stock paying a dividend yield", r"$q$ = the yield", r"Merton (1973)"),
            (r"a stock index", r"$q$ = the index's dividend yield", r"Merton (1973)"),
            (r"a hard-to-borrow stock", r"idealized reinvestable borrow yield", r"Part 9: GameStop"),
            (r"a currency", r"$q$ = the foreign interest rate", r"Garman--Kohlhagen (1983)"),
            (r"a futures contract", r"$b = 0$: $F$ is the underlying", r"Black (1976)"),
            (r"a Bitcoin option on Deribit", r"coin premium: $B/F$, $D_{\rm BTC}=1$", r"Alexander, Chen, Imeraj (2023)"),
        ]
        rows = VGroup()
        for a, b_, c in items:
            rows.add(VGroup(label(a, font_size=24), label(b_, font_size=24, color=QQ), label(c, font_size=20,
                                                                                                color=GREY_B)))
        for r_ in rows:
            r_[0].move_to([-4.0, 0, 0], aligned_edge=LEFT)
            r_[1].move_to([0.3, 0, 0], aligned_edge=LEFT)
            r_[2].move_to([4.0, 0, 0], aligned_edge=LEFT)
        for i, r_ in enumerate(rows):
            r_.shift(DOWN * i * 0.62)
        rows.move_to(DOWN * 0.3)
        for r_ in rows:
            r_[0].shift(LEFT * (r_[0].get_left()[0] + 6.6))
        title = label(r"One formula on the forward, many underlyings", font_size=34).to_edge(UP, buff=0.5)
        foot = note(r"discrete cash dividends: the escrowed model, $S$ minus the dividends' present value "
                    r"(chapter 14); the trade around them: Part 11", font_size=20).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            """The same lognormal forward formula serves several models, with their assumptions stated. Continuous yield gives Merton's stock or index extension; foreign interest gives Garman-Kohlhagen for currencies. An idealized borrow yield can enter similarly. <bookmark mark='a'/> With deterministic rates and a lognormal futures price, Black's 1976 formula discounts its expected payoff. An inverse Bitcoin option needs coin-numeraire accounting: write its premium as the undiscounted forward Black value divided by F when the coin discount factor is one. Its spot-dollar value is then spot times that coin premium. Dividing a discounted dollar premium by the forward would mix units. A known cash dividend can instead be modeled with an escrowed risky component; this is a modeling choice, not a universal exact dividend correction."""
        ) as vo:
            self.play(FadeIn(title))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[:4]], lag_ratio=0.5, run_time=5))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[4:]], lag_ratio=0.5, run_time=3))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def surface(self, c):
        T = np.asarray(c["T"], float) * 365
        cr = np.asarray(c["carry"], float)
        par = c["parity"]
        lx = np.log10(T)
        top = axes([0, 2.6], [0.0, 0.06], x_length=5.6, y_length=3.4, xlabel=r"days to expiry (log)",
                   ylabel=r"carry $\ln(F/S)/T$", xticks=[0, 1, 2], yticks=[0, 0.02, 0.04, 0.06],
                   xfmt=lambda v: f"{10 ** v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=18)
        top.to_edge(LEFT, buff=0.5).shift(DOWN * 0.4)
        dots = VGroup(*[(Dot(top.ax.c2p(a, b_), radius=0.07, color=QQ) if p else
                         Circle(radius=0.07, color=QQ, stroke_width=2).move_to(top.ax.c2p(a, b_)))
                        for a, b_, p in zip(lx, cr, par)])
        basis = DashedLine(top.ax.c2p(0, c["basis_rate"]), top.ax.c2p(2.6, c["basis_rate"]), color=GREY_B,
                           stroke_width=1.5)
        leg1 = legend([(QQ, r"filled: from put--call parity; hollow: the median basis")], font_size=18)
        leg1.next_to(top, UP, buff=0.12).align_to(top, LEFT)
        rows = c["rows"]
        days = np.array([r_["days"] for r_ in rows])
        calls = np.array([r_["calls"] if r_["calls"] is not None else np.nan for r_ in rows])
        puts = np.array([r_["puts"] if r_["puts"] is not None else np.nan for r_ in rows])
        bot = axes([0, 2.6], [-4, 4], x_length=5.6, y_length=3.4, xlabel=r"days to expiry (log)",
                   ylabel=r"error from using spot, vol points", xticks=[0, 1, 2], yticks=[-3, 0, 3],
                   xfmt=lambda v: f"{10 ** v:.0f}", font_size=18).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.4)
        zero = DashedLine(bot.ax.c2p(0, 0), bot.ax.c2p(2.6, 0), color=GREY_C, stroke_width=1.2)
        bc = VGroup(*[Rectangle(width=0.14, height=abs(bot.ax.c2p(0, v)[1] - bot.ax.c2p(0, 0)[1]), stroke_width=0,
                                fill_color=GAIN, fill_opacity=0.85).move_to(bot.ax.c2p(np.log10(d_) - 0.03, v / 2))
                      for d_, v in zip(days, calls) if np.isfinite(v)])
        bp = VGroup(*[Rectangle(width=0.14, height=abs(bot.ax.c2p(0, v)[1] - bot.ax.c2p(0, 0)[1]), stroke_width=0,
                                fill_color=LOSS, fill_opacity=0.85).move_to(bot.ax.c2p(np.log10(d_) + 0.03, v / 2))
                      for d_, v in zip(days, puts) if np.isfinite(v)])
        leg2 = legend([(GAIN, r"calls"), (LOSS, r"puts")], font_size=20).next_to(bot, UP, buff=0.12).align_to(bot, LEFT)
        title = label(r"The Surface's carry, and the skew a forgotten forward draws", font_size=30).to_edge(UP, buff=0.3)
        last = rows[-1]
        mid = next(r_ for r_ in rows if r_["days"] > 40)
        with self.voiceover(
            "On the Surface, Bitcoin's carry is real and measured. For each expiry the House reads the forward from "
            "put-call parity, and the annualized basis, the log of forward over spot divided by the time, is "
            f"between {100 * cr.min():.1f} and {100 * cr.max():.1f} percent a year, rising with maturity: the "
            "price of borrowing dollars against coins. <bookmark mark='a'/> Now forget it. Invert every quote "
            "with spot in place of the forward and no carry. The calls' implied volatilities come out too high and "
            f"the puts' too low: at {mid['days']:.0f} days by {mid['calls']:+.1f} and {mid['puts']:+.1f} points, at "
            f"{last['days']:.0f} days by {last['calls']:+.1f} and {last['puts']:+.1f}. A skew, made of pure "
            "bookkeeping, growing with maturity. Problem seven asks you to estimate it by hand."
            " Carry also decides when to exercise early. Next."
        ) as vo:
            self.play(FadeIn(title), FadeIn(top), FadeIn(leg1), Create(basis))
            self.play(LaggedStart(*[FadeIn(x, scale=1.5) for x in dots], lag_ratio=0.15, run_time=2.5))
            vo.wait_until("a")
            self.play(FadeIn(bot), Create(zero), FadeIn(leg2))
            self.play(LaggedStart(*[GrowFromEdge(x, DOWN) for x in bc], lag_ratio=0.1, run_time=2),
                      LaggedStart(*[GrowFromEdge(x, UP) for x in bp], lag_ratio=0.1, run_time=2))
            self.play(FadeIn(computed()))
        self.wait(0.4)
        self.clear_scene()
