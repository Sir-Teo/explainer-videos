from __future__ import annotations

from videos.economics.econ49.common import *  # noqa: F403


class Health(VoiceoverScene):
    def construct(self):
        card(self, 10, r"The demand for health", r"Is health something people choose, and buy?",
             "Chapter ten. The demand for health.", lit={1972: r"Grossman", 1996: r"Gruber and Owings",
                                                         2019: r"Cooper et al."}, scale=("person", "market"),
             horizon=("a lifetime",))
        self.capital()
        self.visits()
        self.doctors()

    def capital(self):
        G = load("grossman")
        b, e = G["base"], G["educated"]
        age = np.array(b["age"])
        lg = np.log10
        ax = plane([20, 110], [lg(0.15), lg(8)], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.6, y_length=4.4,
                   xticks=[20, 40, 60, 80, 100], yticks=[lg(v) for v in (0.25, 0.5, 1, 2, 4)], xlabel=r"age",
                   ylabel=r"the health stock it pays to keep \ (log scale)", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{10 ** v:g}", font_size=14)
        hb, he = np.array(b["health"]), np.array(e["health"])
        lb = path(ax, age, lg(np.maximum(hb, 0.15)), HEALTH, 3.2)
        le = path(ax, age, lg(np.maximum(he, 0.15)), SCHOOL, 3.2)
        floor = DashedLine(ax.ax.c2p(20, lg(G["h_min"])), ax.ax.c2p(110, lg(G["h_min"])), color=LOSS,
                           stroke_width=1.6)
        fl = label(r"too little health to live", font_size=14, color=LOSS).next_to(ax.ax.c2p(30, lg(G["h_min"])),
                                                                                   UP, buff=0.05)
        d1 = dot(ax, b["death_age"], lg(G["h_min"]), HEALTH, 0.08)
        d2 = dot(ax, e["death_age"], lg(G["h_min"]), SCHOOL, 0.08)
        eq = MathTex(r"\frac{\text{healthy days}}{\text{health}} = \pi_H\,(r + \delta_{\text{age}})", font_size=32,
                     color=THEORY).to_edge(UP, buff=0.45)
        side = VGroup(
            label(r"health is capital: \\ it yields healthy \\ days, \ and wears out", font_size=17, color=HEALTH),
            label(r"wear rises with age: \\ keeping it up costs \\ more each year", font_size=17, color=WHITE),
            label(rf"green: \ better at \\ making health \\ (schooling): \ lives \\ to {e['death_age']:.0f} "
                  rf"against {b['death_age']:.0f}", font_size=17, color=SCHOOL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "In 1972 Michael Grossman treated health as a stock of capital. <bookmark mark='a'/> People are born "
            "with some, it wears out, and they can invest in it, with doctors' visits, food, exercise and their own "
            "time. Its return is healthy days, for work and for life. <bookmark mark='b'/> It pays to hold health "
            "up to the point where the extra healthy days from one more unit equal what it costs to keep it: the "
            "interest forgone plus the rate at which it wears out. That rate rises with age, so the health it pays "
            "to keep falls, <bookmark mark='c'/> and when it would fall below the minimum for life, life ends: "
            f"here at {b['death_age']:.0f}. <bookmark mark='d'/> People who are better at producing health, Grossman "
            "argued, as schooling makes them, choose more of it and live longer. In the model the death age is a "
            "choice, which is the model's most criticized feature, and its most provocative."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Write(eq), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lb), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(floor), FadeIn(fl))
            self.play(FadeIn(d1, scale=1.5))
            vo.wait_until("d")
            self.play(Create(le), FadeIn(side[2]), run_time=2.0)
            self.play(FadeIn(d2, scale=1.5))
        self.clear_scene()

    def visits(self):
        D = load("doctors")
        g = D["groups"]
        names = list(g)
        ax = plane([-0.5, 3.5], [0, 0.55], center=LEFT * 2.0 + DOWN * 0.4, x_length=7.6, y_length=4.2, xticks=[],
                   yticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], ylabel=r"doctor visits in two weeks, \ average",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        cols = (HEALTH, CHILD, DRUG, REGULAR)
        bars = VGroup()
        for i, (nm, col) in enumerate(zip(names, cols)):
            v = g[nm]["visits"]
            p0, p1 = ax.ax.c2p(i - 0.32, 0), ax.ax.c2p(i + 0.32, v)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            lab = label(nm.replace(" (", r" \\ (").replace("basic public cover only", r"basic public \\ cover only"),
                        font_size=14, color=col).next_to(ax.ax.c2p(i, 0), DOWN, buff=0.15)
            info = label(rf"{v:.2f} \\ age {g[nm]['age']:.0f}", font_size=13, color=WHITE).next_to(r, UP, buff=0.05)
            bars.add(VGroup(r, lab, info))
        side = VGroup(
            label(rf"{D['n']:,} Australians, \ 1977--78".replace(",", "{,}"), font_size=17, color=WHITE),
            label(r"the free-for-age group \\ is old and ill: \\ the raw gap is not \\ the effect of cover",
                  font_size=17, color=HOLD),
            label(rf"with illness, \ age, \\ income held equal: \\ private cover, \ visits \\ $\times$ "
                  rf"{D['rr']['private']:.2f} \ ({D['lo']['private']:.2f}--{D['hi']['private']:.2f})", font_size=17,
                  color=E.ACCENT),
            label(r"and those expecting \\ to be ill buy cover: \\ only an experiment \\ settles it", font_size=17,
                  color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Australian Health Survey, \ 1977--78 \ (Cameron and Trivedi), \ via AER; \ estimated here",
                       corner=DL, font_size=12)
        with self.voiceover(
            "If health care is bought like other things, insurance that lowers its price should raise how much is "
            f"used. <bookmark mark='a'/> Here are {D['n']:,} adults from Australia's health survey of 1977 and 1978, "
            "with their doctor visits in two weeks, by the kind of cover they had. <bookmark mark='b'/> Those with "
            "free cover because of age or war service visit most, but they are also old and ill: a raw comparison "
            "mixes the price of care with the need for it. <bookmark mark='c'/> Holding illness, days of reduced "
            "activity, chronic conditions, age, sex and income equal, in a count regression, private cover goes "
            f"with {100 * (D['rr']['private'] - 1):.0f} percent more visits, but the interval runs from "
            f"{100 * (1 - D['lo']['private']):.0f} percent fewer to {100 * (D['hi']['private'] - 1):.0f} percent "
            "more: these data cannot pin it down. <bookmark mark='d'/> And people who expect to need care also buy "
            "cover, so even the estimate is not clean; that is why the RAND experiment of Part forty-two assigned "
            "cover at random."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(VGroup(b[1], b[2])) for b in bars], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(bars[2], color=WHITE, scale_factor=1.03))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Indicate(bars[0], color=WHITE, scale_factor=1.03))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def doctors(self):
        T = tables.HEALTH_49.data
        cards = point_cards([
            (r"the doctor decides", r"patients know little: \\ the doctor advises \\ and sells the care", HEALTH),
            (r"Gruber and Owings", rf"US births fell \\ {T['births_fall']}\% in 1970--82; \\ where they fell most, "
                                   r"\\ caesareans rose most", CHILD),
            (r"a small part", r"induced demand \\ explains little of \\ the rise in \\ caesareans", GREY_B),
            (r"hospital prices", rf"no rival nearby: \\ prices about \\ {T['monopoly']}\% higher than \\ with four "
                                 r"or more", LOSS),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"where the market for care is not like other markets", font_size=30,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.HEALTH_49.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Health care is also unlike other markets. <bookmark mark='a'/> Patients know little, and the doctor "
            "who advises them is also the one who is paid for the care. <bookmark mark='b'/> Jonathan Gruber and "
            f"Maria Owings looked at America from 1970 to 1982, when births fell by {T['births_fall']} percent and "
            "obstetricians lost income. Where births fell most, caesarean sections, which pay more than natural "
            "deliveries, rose most. <bookmark mark='c'/> The effect was real but small: it explains little of the "
            "overall rise in caesareans. <bookmark mark='d'/> And hospitals with market power charge for it: Zack "
            "Cooper and colleagues found that American hospitals with no competitor nearby charge prices about "
            f"{T['monopoly']} percent higher than those with four or more, the measurement of market power from "
            "Part forty-three applied to medicine."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Indicate(cards.cards[0], color=WHITE, scale_factor=1.04))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
