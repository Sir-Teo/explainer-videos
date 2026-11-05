from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant38.common import (BAD, GOOD, HURDLE, INV_C, MAKER_C, PART, SPREAD_C, fit_right, load)


class Fills(VoiceoverScene):
    def construct(self):
        f = load("fills")
        g = load("glft")
        d = load("deep")
        self.card(g)
        self.method()
        self.curve_(f)
        self.by_day(f)
        self.quotes(g)
        self.deep_test(d)
        self.per_hour(d)
        self.why_far(d)
        self.assumption()
        self.alpha_quotes()
        self.question()

    def card(self, g):
        half = g["rows"][0]["half_spread"]
        c = chapter_card(3, r"Fill rates and optimal quotes", r"How far from the mid should a market maker quote?",
                         part=PART)
        with self.voiceover(f"Chapter three, and the answer to the pause: about {half:.0f} ticks, three dollars from the "
                            "mid, not one tick. The model fitted to Bitcoin's tape says quote far away. This chapter shows "
                            "why, and tests whether it is right."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def method(self):
        rows = [cmath(r"\text{each second}", r":", r"\text{quotes at } M_0 \pm \delta", font_size=36),
                cmath(r"P(\delta)", r"=", r"\Pr(\text{a trade reaches } M_0 \pm \delta \text{ within the second})", font_size=30),
                cmath(r"\lambda(\delta)", r"=", r"-\log(1 - P(\delta)) / 1\,\text{s}", font_size=36, colors={r"\lambda(\delta)": SPREAD_C}),
                cmath(r"\log\lambda", r"\approx", r"\log A - k\,\delta", font_size=38)]
        whys = [why(r"imagine quotes at each distance from the mid at the start of every second, two days of the tape"),
                why(r"the share of seconds in which a taker's trade reaches that price, buys for the ask and sells for the "
                    r"bid"),
                why(r"the Poisson intensity that would give that probability"),
                why(r"Avellaneda and Stoikov's exponential: a straight line on a log scale; its slope is $k$")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "How to measure fill rates. <bookmark mark='a'/> At the start of every second, imagine quotes at each "
            "distance from the mid. <bookmark mark='b'/> Count the share of seconds in which a taker's trade reaches "
            "that price. <bookmark mark='c'/> Convert it to a Poisson intensity. <bookmark mark='d'/> And fit the "
            "exponential: on a logarithmic scale, a straight line, whose slope is k."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def curve_(self, f):
        dl = np.asarray(f["deltas"], float)
        lam = np.asarray(f["lam"], float)
        y = np.log10(lam)
        g = axes([0, 50], [-1.5, 0], x_length=6.4, y_length=4.4, xlabel=r"distance from the mid $\delta$, ticks",
                 ylabel=r"fill intensity, per second", xticks=[0, 10, 20, 30, 40, 50], yticks=[-1.5, -1, -0.5, 0],
                 yfmt=lambda v: f"10^{{{v:g}}}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=SPREAD_C) for a, b in zip(dl, y)])
        xs = np.linspace(0, 50, 60)
        fit = curve(ax, xs, np.log10(f["A"]) - f["k"] * xs / np.log(10), HURDLE, stroke_width=2.5)
        st = VGroup(label(rf"$A = {f['A']:.2f}$ per second", font_size=18, color=HURDLE),
                    label(rf"$k = {f['k']:.3f}$ per tick", font_size=18, color=HURDLE),
                    label(rf"$1/k \approx {1 / f['k']:.0f}$ ticks", font_size=18, color=GREY_A))
        st.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.4).shift(UP * 1.4)
        fit_right(st)
        with self.voiceover(
            "On Bitcoin's perpetual. <bookmark mark='a'/> A quote half a tick from the mid is reached in about a third "
            f"of all seconds; one forty-five ticks away in about one in twenty. <bookmark mark='b'/> The fit gives k of "
            f"{f['k']:.3f} per tick: the intensity halves only every {np.log(2) / f['k']:.0f} ticks. Beyond the first "
            "tick the decay is slow, because when Bitcoin moves it moves many ticks at once, Part thirty-six's sweeps. "
            "The very first point sits above the line: the touch is special."
        ) as vo:
            self.play(FadeIn(g), FadeIn(st))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(Create(fit))
        self.wait(0.4)
        self.clear_scene()

    def by_day(self, f):
        days = list(f["days"].keys())
        hx = [-3.4, 0.0, 3.4]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"day", r"$A$, per second", r"$k$, per tick")])
        tab = VGroup(head)
        for d in days:
            r = f["days"][d]
            tab.add(VGroup(label(d[5:], font_size=18), MathTex(f"{r['A']:.3f}", font_size=26),
                           MathTex(f"{r['k']:.4f}", font_size=26, color=SPREAD_C)))
        tab.add(VGroup(label(r"pooled", font_size=18, color=HURDLE), MathTex(f"{f['A']:.3f}", font_size=26, color=HURDLE),
                       MathTex(f"{f['k']:.4f}", font_size=26, color=HURDLE)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.85 * j, 0])
        k0, k1 = f["days"][days[0]]["k"], f["days"][days[1]]["k"]
        with self.voiceover(
            "Is the fit stable? <bookmark mark='a'/> Day by day, k is "
            f"{k0:.3f} and {k1:.3f}: the busier weekday has slower decay, because bigger sweeps reach further. The "
            "parameters move with the market's state, so a real desk re-estimates them through the day, and its quotes "
            "widen and narrow with them."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def quotes(self, g):
        hx = [-3.8, -0.8, 2.0, 4.8]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"risk aversion $\gamma$", r"half-spread at $q = 0$",
                                                                         r"skew per unit", r"base term")])
        tab = VGroup(head)
        for r in g["rows"]:
            tab.add(VGroup(MathTex(f"{r['gamma']:g}", font_size=26), MathTex(f"{r['half_spread']:.1f}", font_size=26,
                                                                               color=MAKER_C),
                           MathTex(f"{r['skew']:.1f}", font_size=26, color=INV_C), MathTex(f"{r['static']:.1f}", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.85 * j, 0])
        foot = wrapped_label(rf"GLFT with Bitcoin's fitted $A$ and $k$ and a volatility of {g['sigma']:.0f} ticks a "
                             r"second; distances in ticks", 11.0, 16, GREY_A).to_edge(DOWN, buff=0.6)
        r0 = g["rows"][0]
        r2 = g["rows"][2]
        with self.voiceover(
            "Feed Bitcoin's fill rates and volatility into Guéant, Lehalle and Fernandez-Tapia's formula. "
            "<bookmark mark='a'/> With little risk aversion, the optimal half-spread is about "
            f"{r0['half_spread']:.0f} ticks, almost all of it the base term one over k. More risk aversion widens the "
            f"quotes and skews them harder with inventory: at gamma of a hundredth, {r2['half_spread']:.0f} ticks, and "
            f"{r2['skew']:.0f} more for each unit held. Nowhere near the touch."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def deep_test(self, d):
        rows = d["rows"]
        x = np.asarray([r["delta"] for r in rows], float)
        y = np.asarray([r["pnl60"] for r in rows], float)
        lo = float(np.floor(y.min() / 5) * 5)
        hi = float(np.ceil(y.max() / 5) * 5)
        g = axes([0, 50], [lo, hi], x_length=6.4, y_length=4.4, xlabel=r"quote distance $\delta$, ticks",
                 ylabel=r"P\&L per fill after a minute, ticks", xticks=[0, 10, 20, 30, 40, 50], yticks=[lo, 0, hi],
                 yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(50, 0), color=GREY_B, stroke_width=1.5)
        c_ = VGroup(curve(ax, x, y, MAKER_C, stroke_width=3), *[Dot(ax.c2p(a, b), radius=0.07, color=MAKER_C)
                                                                for a, b in zip(x, y)])
        r30 = [r for r in rows if r["delta"] == 30][0]
        r45 = [r for r in rows if r["delta"] == 45][0]
        r5 = [r for r in rows if r["delta"] == 5][0]
        with self.voiceover(
            "Is the model right? Test it on the tape. At the start of every second, post quotes delta ticks from the "
            "mid; any trade that reaches them fills them; mark each fill to the mid a minute later. "
            f"<bookmark mark='a'/> Close to the touch the fills are poison: at five ticks, {r5['pnl60']:.0f} ticks a fill. "
            f"<bookmark mark='b'/> The loss shrinks with distance, crosses zero near thirty ticks, {r30['pnl60']:+.0f} "
            f"there, and at forty-five it is {r45['pnl60']:+.0f}. The model's distance is about where the money starts."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(Create(c_), run_time=2.5)
            vo.wait_until("b")
            self.wait(0.2)
        self.wait(0.4)
        self.clear_scene()

    def per_hour(self, d):
        r45 = [r for r in d["rows"] if r["delta"] == 45][0]
        r30 = [r for r in d["rows"] if r["delta"] == 30][0]
        r2 = [r for r in d["rows"] if r["delta"] == 2][0]
        rows = [cmath(r"\delta = 2", r":", rf"{r2['per_hour60']:,.0f}\ \text{{ticks an hour}}".replace(",", "{,}"),
                      font_size=36, colors={r"\delta = 2": BAD}),
                cmath(r"\delta = 30", r":", rf"{r30['per_hour60']:+,.0f}\ \text{{ticks an hour}}".replace(",", "{,}"),
                      font_size=36),
                cmath(r"\delta = 45", r":", rf"{r45['per_hour60']:+,.0f}\ \text{{ticks an hour}}".replace(",", "{,}"),
                      font_size=36, colors={r"\delta = 45": GOOD})]
        whys = [why(r"many fills, each losing: the touch's business is volume times a negative edge"),
                why(r"near breakeven: fewer fills, edges close to zero"),
                why(r"rarer fills with large edges: per unit of size, about \$700 an hour in this optimistic test; a real "
                    r"maker would share these levels with others, pay fees, and hold the inventory")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Per hour, for one unit at each distance. <bookmark mark='a'/> Two ticks out, many fills, each losing: about "
            f"{abs(r2['per_hour60']):,.0f} ticks an hour lost. <bookmark mark='b'/> Thirty ticks out, about break-even. "
            f"<bookmark mark='c'/> Forty-five ticks out, about {r45['per_hour60']:,.0f} ticks an hour gained, roughly seven "
            "hundred dollars per bitcoin of quote, in this optimistic test. Real deep levels are shared, fees are paid, "
            "and the inventory must be carried."
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

    def why_far(self, d):
        r45 = [r for r in d["rows"] if r["delta"] == 45][0]
        cards = VGroup(
            desk_question(r"the far end of a sweep", r"a taker who walks the book pays prices beyond where the mid "
                          r"settles; a quote out there is filled by the overshoot, and the mid comes back toward it",
                          width=12.4, font_size=19),
            desk_question(r"few fills", rf"at 45 ticks a quote is filled only {r45['fills_per_hour']:.0f} times an hour "
                          r"against thousands at the touch: a business of rare, large edges", width=12.4, font_size=19),
            desk_question(r"an upper bound", r"the test assumes our quote is first at its price; real deep levels have "
                          r"queues too, and the best of them belong to whoever got there first", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why far quotes earn. <bookmark mark='a'/> A taker who sweeps the book pays prices beyond where the mid will "
            "settle; a quote out there is filled by the overshoot, and the mid comes back toward it. "
            f"<bookmark mark='b'/> Such fills are rare, about {r45['fills_per_hour']:.0f} an hour at forty-five ticks, "
            "against thousands at the touch. <bookmark mark='c'/> And this is an upper bound: it assumes our quote is "
            "first at its price, while real deep levels have queues of their own."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def assumption(self):
        rows = [cmath(r"\text{AS assumes}", r":", r"\text{fills} \perp \text{future moves}", font_size=38),
                cmath(r"\text{data}", r":", r"\text{fills at the touch} \Rightarrow \text{moves against}", font_size=36,
                      colors={r"\text{data}": BAD}),
                cmath(r"\text{fix}", r":", r"\text{fill rates conditional on the state, and an alpha term}", font_size=32,
                      colors={r"\text{fix}": GOOD})]
        whys = [why(r"the model's fill intensity says how often, not what a fill implies about the price"),
                why(r"near the touch, being filled is news (Part 36's markouts), which the formula ignores; it is "
                    r"right about distance for the wrong reason"),
                why(r"Cartea, Jaimungal and Ricci (2014) add short-term alpha and adverse selection to the market maker's "
                    r"problem; Part 36's microprice is the obvious input")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "What the model gets wrong. <bookmark mark='a'/> It assumes fills are independent of future moves: it says "
            "how often a quote fills, not what the fill implies. <bookmark mark='b'/> On the tape, a fill at the touch is "
            "news, and the price moves against the maker. The formula lands at roughly the right distance, partly for "
            "the wrong reason. <bookmark mark='c'/> The fix is to make fill rates depend on the state, and to add a "
            "short-term alpha, as Cartea, Jaimungal and Jason Ricci did: Part thirty-six's microprice is the obvious "
            "input."
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

    def alpha_quotes(self):
        rows = [cmath(r"\text{centre}", r":", r"M \to M + \hat\alpha", font_size=40, colors={r"\text{centre}": MAKER_C}),
                cmath(r"\hat\alpha", r"=", r"\text{the expected move over the quote's life}", font_size=34),
                cmath(r"\text{e.g.}", r":", r"\text{Part 36's per-horizon table of mean moves}", font_size=34,
                      colors={r"\text{e.g.}": GOOD})]
        whys = [why(r"Cartea, Jaimungal and Ricci (2014): with a short-term alpha, the optimal quotes are centred on the "
                    r"mid plus the expected drift, then widened and skewed as before"),
                why(r"the forecast that matters is over the time a quote is likely to rest"),
                why(r"on Bitcoin, the table that cut the ten-second forecast error is the natural input; the microprice, "
                    r"which overshoots here, is not")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "How alpha enters the quotes. <bookmark mark='a'/> In Cartea, Jaimungal and Ricci's model, the quotes are "
            "centred on the mid plus the expected move, then widened and skewed as before. <bookmark mark='b'/> The "
            "forecast that matters is over the time a quote is likely to rest. <bookmark mark='c'/> On Bitcoin, Part "
            "thirty-six's per-horizon table of mean moves is the natural input, not the microprice, which overshoots "
            "here."
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

    def question(self):
        q = pause_card(r"Bitcoin's perpetual has a one-tick spread almost all the time. If the tick were ten times "
                       r"smaller, would the quoted spread shrink ten times? Who would gain, and who would lose?")
        with self.voiceover(
            "Pause and predict. Bitcoin's perpetual sits at a one-tick spread almost all the time. If the tick were ten "
            "times smaller, would the spread shrink ten times? Who would gain, and who would lose?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
