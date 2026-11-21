from __future__ import annotations

from videos.economics.econ58.common import *  # noqa: F403


class Unpriced(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Valuing what has none", r"How do you price time, \ quiet, \ a beach?",
             "Chapter three. Valuing what has no price.", lit={1947: r"Hotelling's letter", 1974: r"Rosen",
                                                               1989: r"the Exxon Valdez"},
             scale=("person", "household"), horizon=("a day", "a year"))
        self.value_of_time()
        self.hedonic()
        self.travel()
        self.stated()

    def value_of_time(self):
        V = tables.VALUES_58.data
        B = load("bridge")
        p = B["params"]
        rows = VGroup(
            label(r"the wage: \ what an hour of work is worth to the people who choose it", font_size=23,
                  color=GREY_A),
            label(rf"personal travel: \ {100 * V['vot_share']:.0f}\% of the median hourly household income \ "
                  rf"(US DOT; \ {100 * V['vot_lo']:.0f}\% and {100 * V['vot_hi']:.0f}\% to test)", font_size=23,
                  color=TRAV),
            label(r"travel for work: \ the full cost of the worker's hour to the employer", font_size=23,
                  color=GREY_A),
            label(rf"the Island: \ half of a {p['wage']:.0f}-dollar wage, \ {p['vot_share'] * p['wage']:.0f} "
                  rf"dollars an hour", font_size=24, color=ISL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.3)
        head = label(r"the value of time", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.6)
        saved = label(rf"the bridge saves {p['ferry_minutes'] - p['bridge_minutes']:.0f} minutes on every crossing",
                      font_size=30, color=TRAV).move_to(UP * 0.2)
        tag = published_tag(tables.VALUES_58.tag, corner=DL, font_size=12)
        with self.voiceover(
            "Most of what a transport project produces is time, and time has no price tag. <bookmark mark='a'/> The "
            "starting point is the wage, what people accept for an hour of work. <bookmark mark='b'/> But an hour "
            "of travel is not an hour of work, and studies of how people choose between faster and cheaper trips "
            "find they value it at less. America's Department of Transportation values personal travel at half the "
            "median hourly household income, and asks analysts to try thirty-five and sixty percent too. <bookmark "
            "mark='c'/> Travel on the job is valued at its full cost to the employer. <bookmark mark='d'/> On the "
            f"Island, the bridge's travellers' time is valued at half a wage of {p['wage']:.0f} dollars: "
            f"{p['vot_share'] * p['wage']:.0f} dollars an hour."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(saved, shift=UP * 0.1))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                if mk == "a":
                    self.play(FadeOut(saved), run_time=0.5)
                self.play(FadeIn(r_, shift=RIGHT * 0.15))
        self.clear_scene()

    def hedonic(self):
        H = load("hedonic")
        nz, pr, hb = np.array(H["noise"]), np.array(H["price"]), np.array(H["harbour"])
        ax = plane([44, 74], [80, 400], center=LEFT * 2.6 + DOWN * 0.4, x_length=7.0, y_length=5.2,
                   xticks=[45, 50, 55, 60, 65, 70], yticks=[100, 200, 300, 400], xlabel=r"road noise, \ decibels",
                   ylabel=r"house price, \ thousands", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=15)
        near = hb < 1.5
        pts = VGroup(*[Dot(ax.ax.c2p(x, min(max(y, 80), 400)), radius=0.035,
                           color=SAFE if n_ else GREY_B).set_opacity(0.75) for x, y, n_ in zip(nz, pr, near)])
        b_n = np.polyfit(nz, np.log(pr), 1)
        xs = np.linspace(45, 72, 30)
        naive = path(ax, xs, np.exp(np.polyval(b_n, xs)), COST, 3.0, smooth=False)
        side = VGroup(
            label(rf"price on noise alone: \ ${H['naive']:+.2f}\%$ a decibel".replace("-", "{-}"), font_size=21,
                  color=COST),
            label(r"gold: \ homes within 1.5 km of the harbour", font_size=19, color=SAFE),
            label(rf"noise and the harbour: \ correlation ${H['corr']:.2f}$".replace("-", "{-}"), font_size=19,
                  color=GREY_A),
            label(rf"holding the harbour and rooms fixed: \\ ${H['full']:.2f}\%$ a decibel \ (s.e. {H['full_se']:.2f})"
                  .replace("-", "{-}"), font_size=21, color=BEN),
            label(rf"planted: \ ${H['truth']:.1f}\%$".replace("-", "{-}"), font_size=19, color=ISL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        tag = island_tag(rf"the Island: \ {H['n']:,} house sales, \ 500 shown".replace(",", "{,}"), corner=DR,
                         font_size=12)
        rosen = history_card(1974, r"Sherwin Rosen", r"`Hedonic prices and implicit markets': \ the price of a "
                             r"house is the sum of the prices of what comes with it", color=SAFE, width=6.0,
                             font_size=19).move_to(ax.get_center())
        with self.voiceover(
            "Quiet has no market, but houses do, and a house comes with its noise. Sherwin Rosen's hedonic method, "
            "from 1974, reads the price of a characteristic from the prices of the things that carry it. <bookmark "
            f"mark='a'/> Here are {H['n']:,} house sales on the Island, against the road noise outside each. "
            "<bookmark mark='b'/> Fit price on noise, and noise seems to raise prices, by "
            f"{abs(H['naive']):.2f} percent a decibel. <bookmark mark='c'/> The loud homes are by the coast road, and "
            "the coast road runs along the harbour, which people pay to live near. <bookmark mark='d'/> Hold the "
            "distance to the harbour and the number of rooms fixed, and each decibel lowers the price by "
            f"{abs(H['full']):.2f} percent, close to the {abs(H['truth']):.1f} planted in this simulation. A hedonic "
            "price is only as good as the list of everything else that comes with the house. For the bridge's "
            "approach road, ten decibels for two hundred homes is a loss of about seven percent of their value."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(rosen, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeOut(rosen), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(d) for d in pts], lag_ratio=0.002), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(naive), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.clear_scene()

    def travel(self):
        T = load("travel")
        c, v, pop = np.array(T["cost"]), np.array(T["visits"]), np.array(T["pop"])
        ax = plane([0, 26], [0, 7], center=LEFT * 2.6 + DOWN * 0.4, x_length=7.0, y_length=5.0,
                   xticks=[0, 5, 10, 15, 20, 25], yticks=[0, 2, 4, 6], xlabel=r"cost of a trip, \ fuel and time",
                   ylabel=r"visits a year, \ per resident", xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{y:.0f}",
                   font_size=15)
        pts = VGroup(*[Dot(ax.ax.c2p(x, y), radius=0.02 * np.sqrt(n / 100), color=BEN).set_opacity(0.85)
                       for x, y, n in zip(c, v, pop)])
        xs = np.linspace(0, T["choke"], 20)
        fit = path(ax, xs, T["a"] - T["b"] * xs, WHITE, 2.6, smooth=False)
        k = 3
        area = Polygon(*[ax.ax.c2p(x, T["a"] - T["b"] * x) for x in np.linspace(c[k], T["choke"], 12)],
                       ax.ax.c2p(T["choke"], 0), ax.ax.c2p(c[k], 0), fill_color=SAFE, fill_opacity=0.45,
                       stroke_width=0)
        vline_ = DashedLine(ax.ax.c2p(c[k], 0), ax.ax.c2p(c[k], T["a"] - T["b"] * c[k]), color=SAFE,
                            stroke_width=1.5)
        side = VGroup(
            label(r"ten villages; \ the bigger the dot, \ the more people", font_size=19, color=GREY_A),
            MathTex(rf"v = {T['a']:.2f} - {T['b']:.3f}\,c", font_size=30, color=WHITE),
            label(rf"a resident {T['km'][k]:.0f} km away: \\ a surplus of {T['cs_per_person'][k]:.0f} a year",
                  font_size=20, color=SAFE),
            label(rf"the beach: \ {T['trips'] / 1e3:.0f} thousand visits, \\ worth {T['value'] / 1e3:.0f} thousand a "
                  r"year beyond their cost", font_size=20, color=BEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ visits to its beach", corner=DR, font_size=12)
        hot = history_card(1947, r"Harold Hotelling, \ to the National Park Service", r"the cost of the journey "
                           r"can stand in for the price of a park", color=BEN, width=6.0,
                           font_size=19).move_to(ax.get_center())
        with self.voiceover(
            "A beach has no entry price either, but getting there does. In 1947 Harold Hotelling suggested to the "
            "National Park Service that the cost of the journey could stand in for a price, and Marion Clawson made "
            "it a method. <bookmark mark='a'/> Ten villages on the Island lie at different distances from its beach; "
            "each trip costs fuel and an hour or so of time. <bookmark mark='b'/> The farther the village, the fewer "
            "visits each resident makes: the line through them is the beach's demand curve, with the cost of the "
            "trip as its price. <bookmark mark='c'/> A resident whose trip costs "
            f"{c[k]:.0f} dollars gets the area under the curve above that cost: a surplus of "
            f"{T['cs_per_person'][k]:.0f} dollars a year. <bookmark mark='d'/> Added over everyone, the beach is "
            f"worth about {T['value'] / 1e3:.0f} thousand dollars a year beyond what people spend reaching it, a "
            "number to set against a hotel that would close it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(hot, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeOut(hot), run_time=0.5)
            self.play(LaggedStart(*[GrowFromCenter(d) for d in pts], lag_ratio=0.1), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(vline_), FadeIn(area), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def stated(self):
        S = tables.STATED_58.data
        ax = plane([-0.6, 2.6], [0, 120], center=LEFT * 3.0 + DOWN * 0.6, x_length=5.6, y_length=4.4,
                   xticks=[], yticks=[0, 40, 80, 120], ylabel=r"willingness to pay, \ dollars",
                   yfmt=lambda v: f"{v:.0f}", font_size=15)
        bars, labs, vals = VGroup(), VGroup(), VGroup()
        for k, (n_, w) in enumerate(zip(S["birds"], S["wtp"])):
            p0, p1 = ax.ax.c2p(k - 0.3, 0), ax.ax.c2p(k + 0.3, w)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=NOISE, fill_opacity=0.8,
                               stroke_width=0).move_to((p0 + p1) / 2))
            labs.add(label(f"{n_:,} birds".replace(",", "{,}"), font_size=17, color=GREY_A).next_to(
                ax.ax.c2p(k, 0), DOWN, buff=0.15))
            vals.add(label(f"\\${w}", font_size=20, color=NOISE).next_to(bars[-1], UP, buff=0.08))
        prop = VGroup(label(r"in proportion, \ from \$80: \ \$800 and \$8,000".replace(",", "{,}"), font_size=18,
                            color=GREY_B)).next_to(ax, UP, buff=0.15)
        hc = history_card(1989, r"the \emph{Exxon Valdez}", r"a national survey for Alaska put Americans' willingness "
                          r"to pay to prevent another such spill at about \$3 billion; \ Exxon's experts "
                          r"attacked the method", color=NOISE, width=6.0, font_size=19)
        noaa = history_card(1993, r"the NOAA panel \ (Arrow, \ Solow and others)", r"careful surveys can be a "
                            r"starting point, \ with a referendum format \ and a test that more is worth more",
                            color=BEN, width=6.0, font_size=19)
        dh = history_card(1994, r"Diamond and Hausman", r"`is some number better than no number?' \ No: \ answers "
                          r"that ignore scope measure a warm glow, \ not a value", color=COST, width=6.0,
                          font_size=19)
        VGroup(hc, noaa, dh).arrange(DOWN, buff=0.25).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.STATED_58.tag, corner=DL, font_size=12)
        with self.voiceover(
            "Some things leave no trace in any market: an Alaskan coast that most Americans will never see. <bookmark "
            "mark='a'/> When the Exxon Valdez spilled its oil in 1989, the State of Alaska commissioned a national "
            "survey that asked people what they would pay to prevent another such spill: about three billion "
            "dollars in all. Exxon's experts attacked the method. <bookmark mark='b'/> A study published in 1993 "
            "asked groups what they would pay to keep migrating birds from dying in oil ponds: 2,000 birds, 20,000, or "
            "200,000. <bookmark mark='c'/> The answers: eighty dollars, seventy-eight, eighty-eight. A hundred times "
            "the birds, the same money. <bookmark mark='d'/> A panel led by Kenneth Arrow and Robert Solow concluded "
            "in 1993 that careful surveys could still be a starting point, if they asked as in a referendum and "
            "passed a test that more is worth more. <bookmark mark='e'/> Peter Diamond and Jerry Hausman answered "
            "that answers which ignore the scope measure a warm glow, not a value, and that then no number is "
            "better than some number. Stated preference is still used, with those tests, and still argued over."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(ax), FadeIn(labs))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.3), FadeIn(vals),
                      run_time=1.6)
            self.play(FadeIn(prop))
            vo.wait_until("d")
            self.play(FadeIn(noaa, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(dh, shift=UP * 0.1))
        self.clear_scene()
