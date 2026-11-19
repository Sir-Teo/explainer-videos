from __future__ import annotations

from videos.economics.econ3.common import *  # noqa: F403

REGION_COLOR = {"East Asia & Pacific": "#F26D6D", "Europe & Central Asia": "#5DADEC",
                "Latin America & Caribbean": "#7BD88F", "Middle East, North Africa, Afghanistan & Pakistan": "#F2B84B",
                "North America": "#B48EF0", "South Asia": "#FF9F5A", "Sub-Saharan Africa": "#C8E07A"}
REGION_SHORT = {"East Asia & Pacific": r"East Asia and Pacific", "Europe & Central Asia": r"Europe and Central Asia",
                "Latin America & Caribbean": r"Latin America",
                "Middle East, North Africa, Afghanistan & Pakistan": r"Middle East, North Africa, Pakistan",
                "North America": r"North America", "South Asia": r"South Asia",
                "Sub-Saharan Africa": r"Sub-Saharan Africa"}
SHOW = {"CHN": r"China", "USA": r"US", "IND": r"India", "RUS": r"Russia", "JPN": r"Japan", "DEU": r"Germany",
        "BRA": r"Brazil", "IDN": r"Indonesia", "GBR": r"UK", "FRA": r"France", "NGA": r"Nigeria", "EGY": r"Egypt"}


class Countries(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Across countries", r"Is China's economy bigger than America's?",
             "Chapter seven. Across countries.", lit=("world",), scale=("nation", "world"), horizon=("a year",))
        self.haircut()
        self.penn()
        self.redrawn()
        self.revised()

    # ------------------------------------------------------------------
    def haircut(self):
        w = load("world")
        chn, us, ind = w["CHN"], w["USA"], w["IND"]
        head = label(r"GDP in 2024, \ converted at market exchange rates", font_size=30).to_edge(UP, buff=0.5)
        k = 0.135
        rows = VGroup()
        for name, d, col in ((r"United States", us, REGION_COLOR["North America"]),
                             (r"China", chn, REGION_COLOR["East Asia & Pacific"]),
                             (r"India", ind, REGION_COLOR["South Asia"])):
            v = d["gdp_usd"] / 1e12
            r = Rectangle(width=v * k * 2, height=0.6, stroke_width=0, fill_color=col, fill_opacity=0.85)
            nm = label(name, font_size=24, color=col)
            val = label(rf"\${v:.1f} trillion", font_size=24)
            rows.add(VGroup(nm, r, val))
        for i, r in enumerate(rows):
            r[0].move_to([-4.6, 1.6 - 0.9 * i, 0], aligned_edge=RIGHT)
            r[1].move_to([-4.4 + r[1].width / 2, 1.6 - 0.9 * i, 0])
            r[2].next_to(r[1], RIGHT, buff=0.2)
        cuts = VGroup(
            label(r"a haircut in Delhi costs less than one in Dallas", font_size=28, color=E.ACCENT),
            label(r"services that can't be traded are cheap where wages are low", font_size=24, color=GREY_A),
            label(r"so converting at the exchange rate undercounts poor countries' output", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.8)
        tag = data_tag(r"World Bank, World Development Indicators (Nov 2026): GDP, current US dollars", corner=DL,
                       font_size=16)
        with self.voiceover(
            "To compare countries you need one unit, and the obvious one is the dollar. <bookmark mark='a'/> "
            f"Convert each country's GDP at the market exchange rate, and in 2024 the United States produced "
            f"{us['gdp_usd'] / 1e12:.1f} trillion dollars, China {chn['gdp_usd'] / 1e12:.1f} trillion and India "
            f"{ind['gdp_usd'] / 1e12:.1f}. <bookmark mark='b'/> But a dollar changed into rupees buys far more in "
            "Delhi than in Dallas. A haircut, a bus ride or a restaurant meal costs much less there, because those "
            "are services that can't be shipped across borders, and they're cheap where wages are low. "
            "<bookmark mark='c'/> The exchange rate is set by the things that are traded, oil and machines and "
            "money. So converting at the exchange rate undercounts what poor countries actually produce."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]))
                                    for r in rows], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(cuts[0]))
            vo.wait_until("c")
            self.play(FadeIn(cuts[1]), FadeIn(cuts[2]))
        self.clear_scene()

    def penn(self):
        p = load("world")["penn"]
        lo, hi = np.log10(800), np.log10(150000)
        ax = axes([lo, hi], [np.log10(0.08), np.log10(1.6)], x_length=8.4, y_length=5.0,
                  xticks=[np.log10(v) for v in (1000, 10000, 100000)],
                  yticks=[np.log10(v) for v in (0.1, 0.25, 0.5, 1.0)],
                  xfmt=lambda v: rf"\${10 ** v:,.0f}".replace(",", "{,}"), yfmt=lambda v: f"{10 ** v:g}",
                  xlabel=r"GDP per head at purchasing power parity, \ log scale",
                  ylabel=r"price level \ (US $= 1$), \ log scale", font_size=20, center=LEFT * 1.6 + DOWN * 0.2)
        a = ax.ax
        dots = VGroup()
        for c, inc, pl, pop in zip(p["codes"], p["income_ppp"], p["price_level"], p["pop"]):
            r = 0.035 + 0.11 * np.sqrt(pop / 1.45e9)
            dots.add(Dot(a.c2p(np.log10(inc), np.log10(pl)), radius=r, color=GREY_A, fill_opacity=0.55))
        x = np.log10(np.array(p["income_ppp"]))
        b1, b0 = np.polyfit(x, np.log10(np.array(p["price_level"])), 1)
        fit = Line(a.c2p(lo + 0.1, b0 + b1 * (lo + 0.1)), a.c2p(hi - 0.05, b0 + b1 * (hi - 0.05)), color=E.ACCENT,
                   stroke_width=3)
        picks = VGroup()
        for code, nm, side in (("CHE", r"Switzerland", UP), ("USA", r"US", UP), ("CHN", r"China", UP),
                               ("IND", r"India", DOWN), ("ETH", r"Ethiopia", UP), ("NGA", r"Nigeria", DOWN)):
            i = p["codes"].index(code)
            pt = a.c2p(np.log10(p["income_ppp"][i]), np.log10(p["price_level"][i]))
            picks.add(VGroup(Dot(pt, radius=0.06, color=E.ACCENT),
                             label(rf"{nm} \ {p['price_level'][i]:.2f}", font_size=20, color=E.ACCENT).next_to(
                                 pt, side, buff=0.1)))
        note_ = VGroup(label(r"the Penn effect: \\ richer countries \\ are dearer", font_size=26, color=E.ACCENT),
                       label(r"(Balassa and Samuelson, 1964: \\ productivity rises faster in \\ traded goods than "
                             r"in haircuts)", font_size=20, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        note_.to_edge(RIGHT, buff=0.4).shift(UP * 0.8)
        icp = label(r"PPP: \ the World Bank's \\ International Comparison \\ Program prices one list \\ of goods "
                    r"and services \\ in every country", font_size=20, color=GREY_A)
        icp.next_to(note_, DOWN, buff=0.5).align_to(note_, LEFT)
        tag = data_tag(r"WDI (Nov 2026), 2024; price level $=$ GDP at market rates $\div$ GDP at PPP", corner=DL,
                       font_size=15)
        with self.voiceover(
            "The fix is to price the same things everywhere. The World Bank's International Comparison Program "
            "collects prices for one long list of goods and services in nearly every country, and from them "
            "works out purchasing power parities: how many rupees, or yuan, buy what a dollar buys in America. "
            "<bookmark mark='a'/> Divide a country's GDP at market rates by its GDP at those parities and you "
            "get its price level. Here is every country with more than a million people, by income and price "
            "level, each dot sized by population. <bookmark mark='b'/> The pattern is one of the most reliable in "
            "economics: richer countries are dearer. <bookmark mark='c'/> In 2024 prices in Switzerland were "
            "eleven percent above America's, China's were about half, and India's about a quarter. "
            "<bookmark mark='d'/> Bela Balassa and Paul Samuelson explained it in 1964. Rich countries are rich "
            "mostly because their factories and offices are productive, and that pushes up wages for everyone, "
            "barbers included, though a haircut takes as long in Zurich as in Delhi."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(icp))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.01), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(note_[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(pk) for pk in picks], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(note_[1]))
        self.clear_scene()

    def redrawn(self):
        w = load("world")
        codes = w["codes"]
        circles = VGroup()
        names = VGroup()
        for c, reg, pm, rm in zip(codes, w["regions"], w["pos_mkt"], w["r_mkt"]):
            col = REGION_COLOR.get(reg, GREY_B)
            circ = Circle(radius=max(rm, 0.02), stroke_color=col, stroke_width=1.2, fill_color=col, fill_opacity=0.55)
            circ.move_to([pm[0], pm[1] - 0.3, 0])
            circles.add(circ)
            if c in SHOW:
                t = label(SHOW[c], font_size=18 if rm > 0.3 else 15, color=WHITE)
                t.move_to(circ)
                names.add(t)
            else:
                names.add(VectorizedPoint(circ.get_center()))
        targets = []
        for (x, y), r in zip(w["pos_ppp"], w["r_ppp"]):
            targets.append((np.array([x, y - 0.3, 0]), max(r, 0.02)))
        head_m = label(rf"GDP at market exchange rates, 2024: \ world \${w['world_usd'] / 1e12:.0f} trillion",
                       font_size=26).to_edge(UP, buff=0.25)
        head_p = label(rf"GDP at purchasing power parity, 2024: \ world \${w['world_ppp'] / 1e12:.0f} trillion",
                       font_size=26, color=E.ACCENT).to_edge(UP, buff=0.25)
        legend = VGroup(*[VGroup(Dot(radius=0.07, color=col), label(REGION_SHORT[r], font_size=15, color=col)).arrange(
            RIGHT, buff=0.08) for r, col in REGION_COLOR.items()]).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.15)
        if legend.width > 13.4:
            legend.width = 13.4
        note_ = label(r"each circle's area is a country's GDP; \ the US is the same size in both", font_size=19,
                      color=GREY_B).next_to(legend, UP, buff=0.12).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"WDI (Nov 2026): the 70 largest economies at PPP with over a million people", corner=DL,
                       font_size=13)
        with self.voiceover(
            "Now redraw the world. <bookmark mark='a'/> Each circle is a country, placed near its capital, with "
            "its area proportional to its GDP converted at market exchange rates. The United States is the "
            "largest, at twenty-nine trillion dollars, and China second. <bookmark mark='b'/> Now convert at "
            "purchasing power parity instead, keeping America the same size, since by definition a dollar buys "
            "a dollar's worth there. <bookmark mark='c'/> China becomes the largest economy in the world, at "
            f"{w['CHN']['gdp_ppp'] / 1e12:.0f} trillion. India quadruples, to {w['IND']['gdp_ppp'] / 1e12:.1f} "
            "trillion, and the poorer half of the world swells. The world's GDP goes from about 111 trillion "
            "dollars to about 197. <bookmark mark='d'/> Which is right? Both, for different questions. To pay for "
            "imports, or a foreign debt, the exchange rate is what counts. To compare how much people can eat, "
            "wear and live in, use purchasing power."
        ) as vo:
            tag.next_to(legend, UP, buff=0.12).to_edge(LEFT, buff=0.3)
            self.play(FadeIn(head_m), FadeIn(tag), FadeIn(legend), FadeIn(note_))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(c) for c in circles], lag_ratio=0.01), run_time=2.0)
            self.play(FadeIn(names))
            vo.wait_until("b")
            self.wait(0.3)
            vo.wait_until("c")
            anims = []
            for circ, nm, (pos, r) in zip(circles, names, targets):
                tgt = circ.copy().scale(r / max(circ.width / 2, 1e-3)).move_to(pos)
                anims.append(Transform(circ, tgt))
                anims.append(nm.animate.move_to(pos))
            self.play(*anims, FadeTransform(head_m, head_p), run_time=3.5)
            vo.wait_until("d")
            self.wait(0.5)
        self.clear_scene()

    def revised(self):
        w = load("world")
        dh = w["icp2005"]
        cards = VGroup(
            study_card(r"A revision of the world", r"Deaton and Heston (2010)",
                       [(r"what", r"the 2005 round of price comparisons, the first with China's own participation"),
                        (r"China", rf"its economy revised to {dh['china']}\% smaller"),
                        (r"India", rf"revised to {dh['india']}\% smaller"),
                        (r"why", r"prices higher than the older guesses; in China they were collected only in "
                                 r"and around 11 cities")],
                       design="survey", width=8.4, font_size=25),
        ).move_to(LEFT * 1.9 + UP * 0.3)
        lesson = VGroup(
            label(r"same economies, \\ new prices", font_size=30, color=E.ACCENT),
            label(r"a PPP comparison is only \\ as good as its prices", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(cards, RIGHT, buff=0.6)
        bigmac = label(r"The Economist's Big Mac index (since 1986): \ purchasing power parity with a basket of one",
                       font_size=22, color=GREY_B).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Purchasing power parities are estimates, and estimates get revised. <bookmark mark='a'/> In late "
            "2007 the World Bank published a new round of price comparisons for 2005, the first full round in which "
            "China took part. Angus Deaton and Alan Heston later took it apart. <bookmark mark='b'/> China's economy, "
            f"measured at parity, was revised to {dh['china']} percent smaller than before, <bookmark mark='c'/> "
            f"and India's to {dh['india']} percent smaller. Prices there were higher than the older guesses had "
            "assumed. In China they had been collected only in and around eleven cities, where prices are higher "
            "than in the countryside, so the revision may have gone too far. <bookmark mark='d'/> Nothing in "
            "either economy had changed. Only the measure had. <bookmark mark='e'/> If you want a rougher check, "
            "The Economist has published its Big Mac index since 1986: purchasing power parity, with a basket of "
            "one burger."
        ) as vo:
            self.play(FadeIn(cards[0].card), FadeIn(cards[0].head), FadeIn(cards[0][2:]))
            vo.wait_until("a")
            self.play(FadeIn(cards[0].body[0]))
            vo.wait_until("b")
            self.play(FadeIn(cards[0].body[1]))
            vo.wait_until("c")
            self.play(FadeIn(cards[0].body[2]), FadeIn(cards[0].body[3]))
            vo.wait_until("d")
            self.play(FadeIn(lesson, shift=LEFT * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(bigmac))
        self.clear_scene()
