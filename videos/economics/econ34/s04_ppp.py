from __future__ import annotations

from videos.economics.econ34.common import *  # noqa: F403


class PPP(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Purchasing power parity", r"Should a burger cost the same everywhere?",
             "Chapter three. Purchasing power parity.", lit={1964: r"Balassa and Samuelson", 1986: r"the Big Mac "
                                                                                                   r"index",
                                                             1996: r"Rogoff"},
             scale=("market", "world"), horizon=("a year", "a century"))
        self.burgers()
        self.balassa()
        self.halflife()

    def burgers(self):
        Q = load("ppp")
        items = sorted(Q["pick"].items(), key=lambda kv: -kv[1]["price"])
        n = len(items)
        ax = plane([0.4, n + 0.6], [0, 10], center=LEFT * 1.4 + DOWN * 0.5, x_length=9.6, y_length=4.4, xticks=[],
                   yticks=[0, 2, 4, 6, 8, 10], ylabel=r"a Big Mac, \ in dollars at market exchange rates",
                   yfmt=lambda v: f"\\${v:.0f}", font_size=14)
        bars, labs, nms = VGroup(), VGroup(), VGroup()
        for k, (nm, d) in enumerate(items):
            col = USD if nm == "United States" else (CRISIS if d["raw"] > 0 else CALM)
            p0, p1 = ax.ax.c2p(k + 0.65, 0), ax.ax.c2p(k + 1.35, d["price"])
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=col, fill_opacity=0.85,
                               stroke_width=0).move_to((p0 + p1) / 2))
            labs.add(label(rf"\${d['price']:.2f}", font_size=15, color=col).next_to(bars[-1], UP, buff=0.05))
            nms.add(wrapped_label(tex_safe(nm), 1.0, 13, GREY_A).next_to(ax.ax.c2p(k + 1, 0), DOWN, buff=0.1))
        us = seg(ax, 0.4, Q["us_price"], n + 0.6, Q["us_price"], USD, 1.5, dashed=True)
        side = VGroup(
            label(r"the law of one price: \\ the same good, \\ the same price \\ in a common currency", font_size=18,
                  color=WHITE),
            label(r"red: \ dearer than in America \\ (the currency `overvalued')", font_size=17, color=CRISIS),
            label(r"teal: \ cheaper \ (`undervalued')", font_size=17, color=CALM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.25)
        head = label(rf"The Economist's Big Mac index, \ {Q['bigmac_date'][:7]}", font_size=24,
                     color=E.ACCENT).to_edge(UP, buff=0.35)
        tag = data_tag(r"The Economist, \ big-mac-data (CC BY 4.0)", corner=DR, font_size=12)
        sw = Q["pick"].get("Switzerland", {"price": float("nan"), "raw": float("nan")})
        ind = Q["pick"].get("India", {"price": float("nan"), "raw": float("nan")})
        with self.voiceover(
            "If goods can be shipped, the same good should cost the same everywhere once prices are converted at "
            "the exchange rate: the law of one price. Apply it to everything and you get purchasing power parity: "
            "exchange rates should move to equalize price levels. <bookmark mark='a'/> Since 1986 The Economist "
            "has tested this with one good that is the same everywhere, the Big Mac. <bookmark mark='b'/> In "
            f"America it costs {Q['us_price']:.2f} dollars. In Switzerland, converted at the market rate, "
            f"{sw['price']:.2f}: on this measure the franc is {100 * sw['raw']:.0f} percent overvalued. In India, "
            f"{ind['price']:.2f}, which would make the rupee {abs(100 * ind['raw']):.0f} percent undervalued. "
            "<bookmark mark='c'/> The gaps are enormous and they last. A burger is not a ship's cargo."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b, DOWN), FadeIn(lb), FadeIn(nm))
                                    for b, lb, nm in zip(bars, labs, nms)], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(us), FadeIn(side[1:]))
            vo.wait_until("c")
            self.play(Indicate(bars[0], color=WHITE))
        self.clear_scene()

    def balassa(self):
        Q = load("ppp")
        bs = Q["bs"]
        xs = [a for a, _ in Q["scatter"]]
        ax = plane([7.6, 11.8], [-0.8, 0.6], center=LEFT * 2.0 + DOWN * 0.4, x_length=8.0, y_length=4.4,
                   xticks=[float(np.log(x)) for x in (2000, 5000, 10000, 20000, 50000, 100000)],
                   yticks=[-0.8, -0.4, 0, 0.4], xlabel=r"GDP per head, \ dollars (log scale)",
                   ylabel=r"Big Mac valuation against the dollar",
                   xfmt=lambda v: f"{round(np.exp(v) / 1000):.0f}k",
                   yfmt=lambda v: f"{100 * v:+.0f}\\%" if v else "0", font_size=13)
        pts = VGroup(*[Dot(ax.ax.c2p(a, b), radius=0.05, color=PRICE) for a, b in Q["scatter"] if -0.8 <= b <= 0.6])
        fit = seg(ax, min(xs), bs["intercept"] + bs["slope"] * min(xs), max(xs),
                  bs["intercept"] + bs["slope"] * max(xs), CRISIS, 3)
        side = VGroup(
            label(r"in rich countries \\ the labour in a burger \\ is dear", font_size=19, color=WHITE),
            label(r"tradables pin the wage \\ in manufacturing; \\ services follow it", font_size=18, color=GREY_A),
            label(rf"here: \ slope {bs['slope']:.2f}, \\ correlation {bs['corr']:.2f}, \\ {bs['n']} countries",
                  font_size=18, color=CRISIS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"The Economist, \ big-mac-data; \ this film's fit", corner=DR, font_size=12)
        with self.voiceover(
            "Part of the pattern is systematic. <bookmark mark='a'/> Plot each currency's Big Mac valuation "
            "against the country's income per head. Richer countries tend to have dearer burgers. "
            "<bookmark mark='b'/> Bela Balassa and Paul Samuelson explained why in 1964. Productivity in traded "
            "goods is much higher in rich countries, and that sets their wages. Services, like flipping burgers, "
            "are not much more productive there, but they must pay the same wages, so services cost more. "
            f"<bookmark mark='c'/> The tilt is real but loose: a slope of {bs['slope']:.2f} and a correlation of "
            f"{bs['corr']:.2f} across {bs['n']} countries in the latest survey. Much of the spread is something "
            "else."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.03), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(fit), FadeIn(side[2]))
        self.clear_scene()

    def halflife(self):
        Q = load("ppp")
        ax = plane([1870, 2021], [-0.8, 0.8], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.6, y_length=4.4,
                   xticks=[1870, 1900, 1930, 1960, 1990, 2020], yticks=[-0.8, -0.4, 0, 0.4, 0.8],
                   ylabel=r"Britain's real exchange rate against the dollar, \ log, \ demeaned",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.1f}" if v else "0", font_size=13)
        zero = seg(ax, 1870, 0, 2021, 0, GREY_C, 1.2)
        ln = path(ax, Q["gb_t"], Q["gb_q"], GBP, 3.0, smooth=False)
        side = VGroup(
            label(rf"18 countries, \ 1870--2020: \\ half-life {Q['full']['halflife']:.1f} years", font_size=19,
                  color=WHITE),
            label(rf"since 1973: \\ {Q['floating']['halflife']:.1f} years", font_size=19, color=GBP),
            label(r"Rogoff (1996): \\ the consensus, \ 3 to 5 years", font_size=19, color=DEM),
            label(r"the puzzle: \ too slow for \\ sticky prices, \ too volatile \\ for anything else", font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Jord\`a, \ Schularick and Taylor, \ Macrohistory Database R6; \ this film's AR(1)", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Does parity hold in the long run? <bookmark mark='a'/> Here is Britain's real exchange rate against "
            "the dollar since 1870: the pound's purchasing power in America relative to at home. It wanders far "
            "from its average, for years, and comes back. <bookmark mark='b'/> Fitting how fast deviations shrink "
            "across eighteen countries, half of a deviation is gone after "
            f"{Q['full']['halflife']:.1f} years over the whole period, <bookmark mark='c'/> and after "
            f"{Q['floating']['halflife']:.1f} years since the floating era began in 1973. <bookmark mark='d'/> "
            "Kenneth Rogoff's survey of 1996 put the consensus at three to five years, and called it a puzzle. "
            "Deviations that large and that persistent cannot be explained by prices that are sticky for a year or "
            "so; but exchange rates swing far too much from month to month to be explained by real shocks. "
            "Exchange rates return toward parity, slowly."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ln), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()
