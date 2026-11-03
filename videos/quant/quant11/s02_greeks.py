from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import bs
from videos.quant.quant11.common import (ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, axes3d, fixed, hint3d, load, pause,
                                         real_data, surf)

K, SIG = 100.0, 0.5


def straddle(S, tau):
    tau = np.maximum(tau, 1e-6)
    return bs.price(S, K, tau, SIG, cp=1) + bs.price(S, K, tau, SIG, cp=-1)


class Greeks(VoiceoverScene, ThreeDScene):
    def construct(self):
        e = load("explain")
        self.card()
        self.bowl()
        self.derive()
        self.lab(e)
        self.explain(e)

    def card(self):
        c = chapter_card(1, r"Positions as Greeks, and the P\&L explain", r"What does a book make when the world moves?",
                         part=PART)
        with self.voiceover("Chapter one. Positions as Greeks, and the profit and loss explain."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def bowl(self):
        ax = axes3d([70, 130, 10], [0, 40, 10], [0, 40, 10], x_length=7.6, y_length=5.0, z_length=3.6)
        f = lambda s, d: float(straddle(s, d / 365))  # noqa: E731
        sf = surf(ax, f, (70, 130), (0.5, 40), [(QC.SPOT, 2), (OPT, 15), (QC.LOSS, 32)], resolution=(24, 18),
                  opacity=0.55)
        hint = hint3d((r"bitcoin-like underlying $S$", SPOT), (r"days to expiry $\tau$", THETA),
                      (r"straddle value $V$", OPT), ax=ax)
        par = note(r"a straddle struck at 100, 50\% vol", font_size=19).to_corner(DR, buff=0.3)
        tau = ValueTracker(30.0)
        xs = np.linspace(70, 130, 61)
        slice0 = VMobject(stroke_color=YELLOW, stroke_width=5).set_points_as_corners(
            [ax.c2p(x, 30, f(x, 30)) for x in xs])
        d0 = float(bs.greeks(100.0, K, 30 / 365, SIG)["delta"] + bs.greeks(100.0, K, 30 / 365, SIG, cp=-1)["delta"])
        v0 = f(100, 30)
        tang = Line(ax.c2p(70, 30, v0 - 30 * d0), ax.c2p(130, 30, v0 + 30 * d0), color=WHITE, stroke_width=3)
        moving = always_redraw(lambda: VMobject(stroke_color=THETA, stroke_width=5).set_points_as_corners(
            [ax.c2p(x, tau.get_value(), f(x, tau.get_value())) for x in xs]))
        dS = 100 * SIG * np.sqrt(10 / 365)
        bowl_seg = Line(ax.c2p(100 + dS, 30, v0), ax.c2p(100 + dS, 30, f(100 + dS, 30)), color=GAMMA, stroke_width=7)
        drop_seg = Line(ax.c2p(100, 30, v0), ax.c2p(100, 20, f(100, 20)), color=THETA, stroke_width=7)
        cap = VGroup(label(r"green: $\tfrac12\Gamma\,dS^2$, the bowl above the tangent", font_size=22, color=GAMMA),
                     label(r"red: $\Theta\,dt$, ten days of decay", font_size=22, color=THETA),
                     label(rf"they balance at a move of $\sigma\sqrt{{dt}} \approx {dS:.1f}$", font_size=22, color=GREY_A),
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DL, buff=0.35)
        self.set_camera_orientation(phi=66 * DEGREES, theta=-62 * DEGREES, zoom=0.9)
        fixed(self, hint, par, cap)
        with self.voiceover(
            "An options trader's book is one surface: its value over the price of the underlying and the time left. "
            "Here is a straddle's: a valley along the strike, which becomes the payoff's V at expiry. <bookmark mark='a'/> Take today, thirty days "
            "out: the yellow slice. Draw its tangent at the strike, the white line, whose slope is delta. The slice "
            "curves up away from the tangent on both sides: that bowl is gamma, and for a move dS the book gains one "
            "half gamma dS squared, the green length. <bookmark mark='b'/> Now let ten days pass. The whole slice sinks "
            "toward the payoff: that drop, the red length, is theta, what the book pays for the bowl. "
            "<bookmark mark='c'/> A long-gamma trader is betting that the green beats the red: that the underlying "
            f"moves more than about {dS:.1f} in those ten days, one volatility times the square root of the time."
        ) as vo:
            self.play(Create(ax), FadeIn(hint), FadeIn(par), run_time=1.5)
            self.play(Create(sf), run_time=2.5)
            vo.wait_until("a")
            self.play(Create(slice0), Create(tang), run_time=1.5)
            self.play(Create(bowl_seg), FadeIn(cap[0]))
            vo.wait_until("b")
            self.add(moving)
            self.play(tau.animate.set_value(20.0), run_time=3)
            self.play(Create(drop_seg), FadeIn(cap[1]))
            vo.wait_until("c")
            self.play(FadeIn(cap[2]))
            self.move_camera(theta=-35 * DEGREES, phi=72 * DEGREES, run_time=max(vo.remaining(1.0) - 0.5, 1.0))
        moving.clear_updaters()
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0,
                         added_anims=[FadeOut(VGroup(ax, sf, slice0, tang, moving, bowl_seg, drop_seg)),
                                      FadeOut(hint), FadeOut(par), FadeOut(cap)], run_time=1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"d\Pi", r"=", r"\Delta\,dS + \tfrac12\Gamma\,dS^2 + \Theta\,dt + \mathcal{V}\,d\sigma "
                  r"+ \text{vanna}\,dS\,d\sigma + \tfrac12\,\text{volga}\,d\sigma^2 + \dots", font_size=32,
                  colors={r"d\Pi": OPT}),
            cmath(r"\Delta = N(d_1),", r"\quad", r"\Gamma = \frac{\varphi(d_1)}{S\sigma\sqrt\tau},\quad "
                  r"\mathcal{V} = S\varphi(d_1)\sqrt\tau", font_size=34, colors={r"\Delta = N(d_1),": QC.DELTA}),
            cmath(r"\Theta", r"=", r"-\tfrac12\,\sigma^2 S^2\,\Gamma \qquad (r = 0)", font_size=36,
                  colors={r"\Theta": THETA}),
            cmath(r"\tfrac12\Gamma\,dS^2 + \Theta\,dt", r"=", r"\tfrac12\Gamma S^2\left[\left(\tfrac{dS}{S}\right)^2 "
                  r"- \sigma^2 dt\right]", font_size=36, colors={r"\tfrac12\Gamma\,dS^2 + \Theta\,dt": GAMMA}),
            cmath(r"\mathcal{V}", r"=", r"\sigma\,\tau\,S^2\,\Gamma", font_size=38, colors={r"\mathcal{V}": VEGA}),
        ]
        whys = [
            why(r"Taylor's theorem in spot, time and volatility: the book is a sum of legs, so its Greeks are sums too"),
            why(r"differentiate the Black--Scholes formula; the cross terms cancel because "
                r"$S\varphi(d_1) = Ke^{-r\tau}\varphi(d_2)$"),
            why(r"the Black--Scholes equation (Part 10) at zero rates: time decay is the price of gamma"),
            why(r"substitute: the day's P\&L is gamma times realized minus implied variance; it is zero when "
                r"$|dS/S| = \sigma\sqrt{dt}$"),
            why(r"compare $\mathcal{V}$ and $\Gamma$: for plain options long gamma means long vega, and a risk report "
                r"shows both"),
        ]
        step = ladder(self, rows, whys, keep=3, top=3.2, x=-3.4, buff=0.55, edge=6.9)  # room on the right for the long Taylor row
        pc = pause(r"Implied vol 50\%. How far must the underlying move today for a hedged long-gamma book to break "
                   r"even?", width=5.4, font_size=21)
        be = 100 * 0.5 * np.sqrt(1 / 365)
        with self.voiceover(
            "Now the algebra, step by step. Taylor's theorem in three variables: spot, time and implied volatility. "
            "The terms a trader names are delta, gamma, theta, vega, and two cross terms, vanna and volga. "
            "<bookmark mark='a'/> Differentiate the Black-Scholes formula and each has a closed form. <bookmark mark='b'/> Part ten's "
            "equation, at zero rates, ties theta to gamma: time decay is exactly the price of the bowl. "
            "<bookmark mark='c'/> Substitute it, and a day's profit is one half gamma S squared times the realized "
            "squared return minus the implied variance. Pause and predict: at fifty percent volatility, how far must "
            f"the underlying move in a day to break even? <bookmark mark='d'/> About {be:.1f} percent, fifty percent "
            "times the square root of one three hundred sixty-fifth. <bookmark mark='e'/> And one more identity: "
            "vega equals volatility times time times S squared times gamma. For plain options, long gamma and long "
            "vega come together; a desk that wants one without the other needs two expiries, which chapter ten does."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            self.play(FadeIn(pc))
            vo.wait_until("d")
            self.play(FadeOut(pc))
            vo.wait_until("e")
            step(4)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lab(self, e):
        legs = r", ".join([rf"{n:+d}\,{'C' if cp > 0 else 'P'}\,{100 * m:.0f}\%" for cp, m, n in e["legs"]])
        card = lab_card(r"a book as one set of Greeks", [
            "def book_greeks(legs, S, sigma, t=0.0, r=0.0) -> dict:",
            "    out = {k: 0.0 for k in (\"price\", \"delta\", \"gamma\",",
            "                            \"vega\", \"theta\", \"vanna\", \"volga\")}",
            "    for leg in legs:",
            "        g = bs.greeks(S, leg.K, max(leg.T - t, 0.0), sigma, r, 0.0, leg.cp)",
            "        for k in out:",
            "            out[k] = out[k] + leg.qty * g[k]",
            "    return out",
        ], source="explainer/quant/house/quoting.py", width=7.2).to_edge(LEFT, buff=0.4).to_edge(UP, buff=0.4)
        c = e["cash"]
        conv = VGroup(
            label(r"the desk's units", font_size=26, color=GREY_A),
            label(r"cash delta $= \Delta\cdot S$", font_size=22, color=QC.DELTA),
            label(r"gamma per 1\% $= \tfrac12\Gamma S^2 (0.01)^2$", font_size=22, color=GAMMA),
            label(r"vega per vol point $= \mathcal{V}/100$", font_size=22, color=VEGA),
            label(r"theta per day $= \Theta/365$", font_size=22, color=THETA),
            wrapped_label(rf"the book, 30 days: ${legs}$ of the forward, on one bitcoin of each", 4.6, 20, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4).to_edge(UP, buff=0.5)
        with self.voiceover(
            "In the House this is one function. A book is a list of legs; its Greeks are the sum of theirs. "
            "<bookmark mark='a'/> Desks quote them in cash: delta in dollars of the underlying, gamma as the profit "
            "on a one percent move, vega per volatility point, theta per day. Here is a five-leg Bitcoin book on the "
            "Surface day: long an at-the-money straddle, short two puts ten percent below, long a call ten percent "
            "above. <bookmark mark='b'/> Run it. The book is long "
            f"{c['delta']:,.0f} dollars of delta, makes {c['gamma_1pct']:.0f} dollars on a one percent move from "
            f"gamma, {c['vega_pt']:.0f} per volatility point, and pays {-c['theta_day']:.0f} a day in theta."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in conv], lag_ratio=0.3, run_time=3))
            vo.wait_until("b")
            lab_run(self, card, ["book_greeks(book, S=F, sigma=atm)",
                                 f"cash delta {c['delta']:>9,.0f}   gamma/1% {c['gamma_1pct']:>6.1f}",
                                 f"vega/pt   {c['vega_pt']:>9.1f}   theta/day {c['theta_day']:>6.1f}"])
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def explain(self, e):
        names = ["delta", "gamma", "theta", "vega", "vanna", "volga", "unexplained"]
        cols = [QC.DELTA, GAMMA, THETA, VEGA, ALT, QC.Q, GREY_B]
        vals = [e[n] for n in names]
        lo = min(0.0, np.cumsum(vals).min(), e["actual"]) * 1.12
        hi = max(0.0, np.cumsum(vals).max()) + 0.12 * abs(lo) + 50
        g = axes([0, len(names) + 1], [lo, hi], x_length=8.2, y_length=4.6, ylabel=r"P\&L, dollars per book",
                 yticks=[-1500, -1000, -500, 0], font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
        ax = g.ax
        z = DashedLine(ax.c2p(0, 0), ax.c2p(len(names) + 1, 0), color=GREY_C, stroke_width=1.5)
        bars, labs, run = VGroup(), VGroup(), 0.0
        w = ax.c2p(0.62, 0)[0] - ax.c2p(0, 0)[0]
        for i, (n, v, c) in enumerate(zip(names, vals, cols)):
            a, b = ax.c2p(i + 0.6, run), ax.c2p(i + 0.6, run + v)
            r_ = Rectangle(width=w, height=max(abs(b[1] - a[1]), 0.02), stroke_width=0, fill_color=c,
                           fill_opacity=0.85).move_to((a + b) / 2)
            bars.add(r_)
            labs.add(VGroup(label(n, font_size=17, color=c), MathTex(f"{v:+,.0f}", font_size=20, color=c)).arrange(
                DOWN, buff=0.04).next_to(ax.c2p(i + 0.6, lo), DOWN, buff=0.1))
            run += v
        a, b = ax.c2p(len(names) + 0.6, 0), ax.c2p(len(names) + 0.6, e["actual"])
        act = Rectangle(width=w, height=abs(b[1] - a[1]), stroke_color=WHITE, stroke_width=2.5, fill_color=OPT,
                        fill_opacity=0.5).move_to((a + b) / 2)
        actl = VGroup(label(r"actual", font_size=17), MathTex(f"{e['actual']:+,.0f}", font_size=20)).arrange(
            DOWN, buff=0.04).next_to(ax.c2p(len(names) + 0.6, lo), DOWN, buff=0.1)
        share = 100 * e["share"]
        verdict = (rf"the six terms explain all but {share:.1f}\% of the day" if share < 5 else
                   rf"{share:.0f}\% is left unexplained: a day too big for a second-order Taylor series")
        side = VGroup(
            label(rf"bitcoin {100 * e['move']:+.2f}\% overnight", font_size=22, color=SPOT),
            label(rf"30-day ATM vol {100 * e['atm0']:.1f}\% $\to$ {100 * e['atm1']:.1f}\%", font_size=22, color=VEGA),
            wrapped_label(verdict, 4.0, 21, GREY_A),
            wrapped_label(r"vanna: spot and vol fell together, and the book's delta rose as vol fell", 4.0, 20, ALT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = real_data(r"the Surface: Deribit BTC, 10 and 11 December 2025, 08:00 UTC; SSVI smiles; one bitcoin per leg")
        branch = (f"the six terms explain all but {share:.1f} percent of it." if share < 5 else
                  f"{share:.0f} percent is left over: too big a day for a second-order series.")
        with self.voiceover(
            "Every morning a risk system does what this chart does: the profit and loss explain. Take the book to "
            "the next day's Surface. Overnight Bitcoin moved "
            f"{100 * e['move']:+.1f} percent, and thirty-day volatility fell from {100 * e['atm0']:.1f} to "
            f"{100 * e['atm1']:.1f} percent. <bookmark mark='a'/> Build the day term by term. Delta did most of it, "
            f"{e['delta']:,.0f} dollars. Gamma added {e['gamma']:,.0f}, theta took {-e['theta']:,.0f}, vega "
            f"{e['vega']:,.0f}. <bookmark mark='b'/> Then the cross terms: vanna {e['vanna']:+,.0f}, because spot "
            "and volatility fell together; volga a few dollars. <bookmark mark='c'/> The full revaluation lost "
            f"{-e['actual']:,.0f}, and {branch} When the explain fails, a desk has a risk it is not measuring."
            " Gamma is the term worth watching. Next: trading it on a real path."
        ) as vo:
            self.play(FadeIn(g), Create(z), FadeIn(src), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            for i in range(4):
                self.play(GrowFromEdge(bars[i], UP if vals[i] < 0 else DOWN), FadeIn(labs[i]), run_time=0.8)
            vo.wait_until("b")
            for i in (4, 5):
                self.play(GrowFromEdge(bars[i], UP if vals[i] < 0 else DOWN), FadeIn(labs[i]), run_time=0.7)
            self.play(FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(act), FadeIn(actl), GrowFromEdge(bars[6], DOWN), FadeIn(labs[6]))
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
