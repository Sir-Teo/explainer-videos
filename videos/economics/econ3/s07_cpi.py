from __future__ import annotations

from videos.economics.econ3.common import *  # noqa: F403

COMP_COLOR = {"upper-level substitution": PAAS, "lower-level substitution": "#4F9FD0",
              "new products and quality": FISHER, "new outlets": E.GAIN, "weighting": GREY_B}
COMP_NAME = {"upper-level substitution": r"substitution between goods",
             "lower-level substitution": r"substitution within a good",
             "new products and quality": r"new products and quality", "new outlets": r"new kinds of shop",
             "weighting": r"weights"}


class CPI(VoiceoverScene):
    def construct(self):
        card(self, 6, r"The consumer price index", r"How biased is the most important price index, and does it "
             r"matter?", "Chapter six. The consumer price index.", lit=("households", "government"),
             scale=("household", "nation"), horizon=("a month", "a decade"))
        self.making()
        self.boskin()
        self.hedonic()
        self.chained()

    # ------------------------------------------------------------------
    def making(self):
        steps = flow_chain([(r"the basket", E.HOUSEHOLDS), (r"the prices", E.DATA), (r"the index", FISHER)],
                           box_w=3.4, box_h=1.0, buff=1.0, font_size=30,
                           notes=[r"what households spend on, from the Consumer Expenditure Survey",
                                  r"every month, in 75 urban areas: about 23,000 shops and 6,000 homes",
                                  r"prices weighted by the basket; weights updated every year since 2023"],
                           note_size=23)
        steps.move_to(UP * 1.1)
        title = label(r"The consumer price index \ (CPI-U)", font_size=36).to_edge(UP, buff=0.45)
        uses = VGroup(
            label(r"Social Security's cost-of-living adjustment \ (the CPI for wage earners)", font_size=24,
                  color=E.ACCENT),
            label(r"federal tax brackets \ (the chained CPI, since 2018)", font_size=24, color=E.ACCENT),
            label(r"many wage contracts, \ rents, \ inflation-protected bonds", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.7)
        ul = label(r"indexed to it:", font_size=24, color=GREY_B).next_to(uses, UP, buff=0.3).align_to(uses, LEFT)
        tag = published_tag(r"BLS, Handbook of Methods: Consumer Price Index", corner=DR, font_size=16)
        with self.voiceover(
            "The most watched price index in America is the consumer price index, made by the Bureau of Labor "
            "Statistics. <bookmark mark='a'/> It starts with a basket: what households spend their money on, from "
            "a survey of their spending. <bookmark mark='b'/> Every month, the bureau's staff record prices in 75 "
            "urban areas, in about 23,000 shops and 6,000 homes for rents. <bookmark mark='c'/> And it combines "
            "them, each price weighted by its share of the basket. Since 2023 the weights have been updated every "
            "year. <bookmark mark='d'/> A great deal is tied to this number. Social Security payments rise each year "
            "with one version of it, the index for wage earners. Federal tax brackets move with another, the chained "
            "index. So do many wage contracts, rents and the government's inflation-protected bonds. If it's wrong by a point a year, a great deal of money moves "
            "for no reason."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(title))
            for i, mk in enumerate("abc"):
                vo.wait_until(mk)
                if i:
                    self.play(GrowArrow(steps.arrows[i - 1]), run_time=0.5)
                self.play(FadeIn(steps.boxes[i], shift=RIGHT * 0.2), FadeIn(steps.notes[i]))
            vo.wait_until("d")
            self.play(FadeIn(ul), LaggedStart(*[FadeIn(u, shift=UP * 0.1) for u in uses], lag_ratio=0.3))
        self.clear_scene()

    def boskin(self):
        c = load("cpi")
        au = c["audit"]
        comps = au["components"]
        who = history_card(r"1995--96", r"the Advisory Commission to Study the Consumer Price Index",
                           r"Michael Boskin, Ellen Dulberger, Robert Gordon, Zvi Griliches, Dale Jorgenson; "
                           r"appointed by the Senate Finance Committee", color=FISHER, width=6.0, font_size=23)
        who.to_corner(UL, buff=0.45)
        k = 9.2
        x0 = -5.7
        y = -0.35
        bars = VGroup()
        legend = VGroup()
        x = x0
        for comp, v in zip(comps, au["boskin_1996"]):
            if v <= 0:
                continue
            r = Rectangle(width=v * k, height=1.0, stroke_color=BACKGROUND, stroke_width=1.5,
                          fill_color=COMP_COLOR[comp], fill_opacity=0.9)
            r.move_to([x + v * k / 2, y, 0])
            t = label(f"{v:.2f}", font_size=24, color=BACKGROUND).move_to(r)
            bars.add(VGroup(r, t))
            legend.add(VGroup(Square(0.22, stroke_width=0, fill_color=COMP_COLOR[comp], fill_opacity=0.9),
                              label(COMP_NAME[comp], font_size=22, color=COMP_COLOR[comp])).arrange(RIGHT, buff=0.12))
            x += v * k
        total = label(r"1.1 percentage points a year", font_size=34, color=FISHER)
        rng = label(r"plausible range: \ 0.8 to 1.6", font_size=24, color=GREY_A)
        VGroup(total, rng).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.6).shift(DOWN * 0.4)
        legend.arrange(RIGHT, buff=0.45).next_to(bars, DOWN, buff=0.4).align_to(bars, LEFT)
        if legend.width > 12.6:
            legend.width = 12.6
        cost = label(r"cost to the federal debt, 1997--2008, if nothing changed: \ about \$1.07 trillion",
                     font_size=26, color=E.MISS).to_edge(DOWN, buff=0.9)
        tag = published_tag(r"Boskin et al.\ (1996), as tabulated by Gordon (2006) and Moulton (2018)", corner=DR,
                            font_size=16)
        with self.voiceover(
            "In 1995 the Senate Finance Committee asked five economists, led by Michael Boskin of Stanford, how "
            "far the index was from a true cost of living. <bookmark mark='a'/> Their report, in December 1996, "
            "said it overstated inflation by about 1.1 percentage points a year, plausibly anywhere from 0.8 to "
            "1.6. <bookmark mark='b'/> They added it up by source. About 0.15 came from substitution between "
            "goods, Bo's problem: a fixed basket ignores that people switch from beef to chicken when beef gets "
            "dear. <bookmark mark='c'/> A quarter of a point came from substitution within a good, between brands "
            "and varieties. <bookmark mark='d'/> A tenth came from new kinds of shop: when a discount store "
            "opens, the index treated its lower prices as lower quality, not as cheaper goods. "
            "<bookmark mark='e'/> And the largest part, 0.6, came from new products and better quality. A "
            "computer that costs the same as last year's but is twice as fast is really cheaper, and the index "
            "mostly didn't see it. <bookmark mark='f'/> The commission also put a price on the bias. Left alone, "
            "it would add about a trillion dollars to the federal debt over twelve years, through indexed "
            "benefits and tax brackets."
        ) as vo:
            self.play(FadeIn(who, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(total), FadeIn(rng))
            for mk, b, l in zip("bcde", bars, legend):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[0], LEFT), FadeIn(b[1]), FadeIn(l))
            vo.wait_until("f")
            self.play(FadeIn(cost))
        self.clear_scene()

    def hedonic(self):
        h = load("hedonic")
        yr = np.array(h["year"])
        L = np.array(h["length"])
        P = np.array(h["price"])
        ax = axes([3.5, 7.5], [10, 50], x_length=6.4, y_length=4.6, xticks=[4, 5, 6, 7], yticks=[10, 20, 30, 40, 50],
                  xlabel=r"boat length, metres", ylabel=r"price, dollars", font_size=20,
                  center=LEFT * 2.9 + DOWN * 0.3)
        a = ax.ax
        dots0 = VGroup(*[Dot(a.c2p(l, p), radius=0.06, color=E.FISH) for l, p, y in zip(L, P, yr) if y == 0])
        dots1 = VGroup(*[Dot(a.c2p(l, p), radius=0.06, color=FISHER) for l, p, y in zip(L, P, yr) if y == 1])
        b = h["beta"]
        f0 = a.plot(lambda x: np.exp(b[0] + b[1] * np.log(x)), x_range=[3.6, 7.4], color=E.FISH, stroke_width=3)
        f1 = a.plot(lambda x: np.exp(b[0] + b[1] * np.log(x) + b[2]), x_range=[3.6, 7.4], color=FISHER,
                    stroke_width=3)
        rows = VGroup(
            label(rf"last year: \ {h['mean_length'][0]:.1f} m, \ \${h['mean_price'][0]:.2f} on average", font_size=23,
                  color=E.FISH),
            label(rf"this year: \ {h['mean_length'][1]:.1f} m, \ \${h['mean_price'][1]:.2f} on average", font_size=23,
                  color=FISHER),
            label(rf"average price: \ {pct(h['naive'], 1, sign=True)}", font_size=26, color=E.MISS),
            label(rf"same length, \ this year vs last: \ {pct(h['pure'], 1, sign=True)}", font_size=26, color=FISHER),
            label(rf"95\% interval \ {pct(h['pure_ci'][0], 1, sign=True)} \ to \ {pct(h['pure_ci'][1], 1, sign=True)}",
                  font_size=21, color=GREY_A),
            label(rf"planted truth: \ {pct(h['truth'], 0, sign=True)}", font_size=24, color=E.TRUTH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.45).shift(UP * 0.2)
        eq = MathTex(r"\log \text{price} = a + b \log \text{length} + c \cdot \text{this year}", font_size=32)
        eq.to_edge(UP, buff=0.35)
        tag = island_tag(r"simulated: the boatyard's sales, 30 boats a year; prices planted to rise 3\% for a "
                         r"boat of given length", corner=DL, font_size=15)
        with self.voiceover(
            "How do you see quality? The usual tool is a hedonic regression, and the Island has a test case. "
            "<bookmark mark='a'/> Here are the boats Crusoe's yard sold last year, by length and price. "
            "<bookmark mark='b'/> And here are this year's. They're longer: fishers want bigger boats. "
            f"<bookmark mark='c'/> The average price rose {100 * h['naive']:.0f} percent. Is that inflation? "
            "Mostly not: this year's buyers got more boat. <bookmark mark='d'/> So fit the price to the length in "
            "both years at once, and let the regression find how much more a boat of the same length costs this "
            f"year. <bookmark mark='e'/> The answer: {100 * h['pure']:.1f} percent. The rest of the rise was "
            "quality. <bookmark mark='f'/> The truth we planted was three percent, inside the interval. Statistical "
            "agencies do this for computers, phones, clothing and housing, and it's one reason the index's bias "
            "has shrunk since 1996."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots0], lag_ratio=0.03), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots1], lag_ratio=0.03), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Write(eq), Create(f0), Create(f1))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]), FadeIn(rows[4]))
            vo.wait_until("f")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def chained(self):
        c = load("cpi")
        s = c["series"]
        months = s["months"]
        xs = [int(m[:4]) + (int(m[5:7]) - 0.5) / 12 for m in months]
        ax = year_axis([1999.9, 2027], [95, 210], x_length=11.4, y_length=4.6, xticks=list(range(2000, 2030, 5)),
                       yticks=[100, 125, 150, 175, 200], ylabel=r"December 1999 $= 100$",
                       center=LEFT * 0.3 + DOWN * 0.3)
        a = ax.ax
        lines = VGroup()
        for key, col in (("cpi", E.DATA), ("chained", FISHER), ("pce", E.HOUSEHOLDS)):
            pts = [a.c2p(x, v) for x, v in zip(xs, s[key]) if np.isfinite(v)]
            lines.add(VMobject(stroke_color=col, stroke_width=3).set_points_as_corners(pts))
        names = VGroup(
            label(rf"CPI-U: \ {c['g_cpi'] * 100:.2f}\% a year", font_size=22, color=E.DATA),
            label(rf"chained CPI-U: \ {c['g_chained'] * 100:.2f}\%", font_size=22, color=FISHER),
            label(rf"PCE price index: \ {c['g_pce'] * 100:.2f}\%", font_size=22, color=E.HOUSEHOLDS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        names.move_to(a.c2p(2001.0, 192), aligned_edge=UL)
        gap = label(rf"the chained index's gap: \ {100 * c['gap_chained']:.2f} points a year, \\ substitution "
                    r"between goods, \ measured", font_size=23, color=FISHER).next_to(names, DOWN, buff=0.35)
        gap.align_to(names, LEFT)
        audits = label(r"later audits: \ Lebow and Rudd (2003) 0.87; \ Moulton (2018) 0.85", font_size=22,
                       color=GREY_A).to_edge(DOWN, buff=0.3).shift(RIGHT * 2.0)
        tag = data_tag(rf"BLS (CPIAUCSL, SUUR0000SA0) and BEA (PCEPI), {data.fred_cite('CPIAUCSL')}", corner=DL,
                       font_size=15)
        with self.voiceover(
            "The bureau changed its methods after the report. It began averaging prices within each item with a "
            "geometric mean, which allows for switching between brands, and widened its quality adjustments. "
            "<bookmark mark='a'/> And it started a second index, the chained CPI, which uses a superlative formula "
            "and so allows for switching between goods, Bo's switch. Here they are since December 1999, both "
            "starting at one hundred. <bookmark mark='b'/> The official index has doubled. The chained one has "
            f"risen less: {100 * c['g_cpi']:.2f} percent a year against {100 * c['g_chained']:.2f}. "
            f"<bookmark mark='c'/> That gap, about a quarter of a point every year for "
            f"{c['years']:.0f} years, is substitution bias, measured directly. <bookmark mark='d'/> The Fed "
            "targets another index, for personal consumption expenditures, which is chained too and covers more "
            f"of what households consume. It has risen {100 * c['gap_pce']:.2f} points a year less than the CPI. "
            "<bookmark mark='e'/> Later audits put the official index's remaining bias at about 0.85 points a "
            "year: smaller than in 1996, and not zero. We'll put the estimates on a dial in chapter thirteen."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lines[1], rate_func=linear), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(lines[0], rate_func=linear), run_time=2.0)
            self.play(FadeIn(names[0]), FadeIn(names[1]))
            vo.wait_until("c")
            self.play(FadeIn(gap))
            vo.wait_until("d")
            self.play(Create(lines[2], rate_func=linear), FadeIn(names[2]), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(audits))
        self.clear_scene()
