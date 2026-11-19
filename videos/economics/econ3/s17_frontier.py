from __future__ import annotations

from videos.economics.econ3.common import *  # noqa: F403

NIGHT = "#F7D154"


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ measuring what has no price", r"What are economists trying to measure next?",
             "Chapter fifteen. Frontier: measuring what has no price.", scale=("firm", "nation", "world"),
             horizon=("a year", "a decade"))
        self.intangibles()
        self.lights()
        self.next_sna()

    def intangibles(self):
        cards = VGroup(
            study_card(r"Intangible capital", r"Corrado, Hulten and Sichel (2009)",
                       [(r"what", r"software, research, designs, brands, training, new ways of organizing"),
                        (r"missing", r"as much as \$800 billion of US investment a year (2003), \ more than "
                                     r"\$3 trillion of capital"),
                        (r"so what", r"counted, output per worker grows faster, \ and labour's share falls")],
                       design="calibration", width=6.5, font_size=22),
            study_card(r"Free and new goods", r"the AI question",
                       [(r"what", r"a chatbot's answer, \ a free translation, \ a map"),
                        (r"in GDP", r"the subscriptions and the advertising; \ the answers themselves, \ at a price "
                                    r"of zero"),
                        (r"open", r"how to price a product that did not exist last year")],
                       design="survey", width=6.5, font_size=22, color=E.PRED),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 0.4)
        rd = label(r"research and development: \ counted as investment in the US accounts since 2013", font_size=23,
                   color=E.ACCENT).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The frontier of measurement is mostly about things without prices. <bookmark mark='a'/> The first is "
            "intangible capital: software, research, designs, brands, training, new ways of running a business. "
            "Firms spend heavily on these, and for a long time the accounts treated most of it as a cost, not as "
            "investment. In 2009 Carol Corrado, Charles Hulten and Daniel Sichel estimated that as much as eight "
            "hundred billion dollars a year of American investment was missing, and more than three trillion "
            "dollars of capital. Counted, it changes the story of growth. <bookmark mark='b'/> The accounts have "
            "moved: research and development has been counted as investment since 2013. <bookmark mark='c'/> The "
            "second is new and free goods, and artificial intelligence sharpens the problem. GDP counts what is "
            "paid for, the subscriptions and the advertising. The answers, translations and maps themselves, given "
            "away, appear nowhere. How to price a product that didn't exist last year is the oldest problem in "
            "this part, in its newest form."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(cards[0].card, color=E.ACCENT, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(rd))
            vo.wait_until("c")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.clear_scene()

    def lights(self):
        globe = island_shape(6.0, 3.0, seed=11).move_to(LEFT * 3.2 + UP * 0.6)
        globe.set_fill("#151C28", opacity=1).set_stroke("#2E3A4F", width=1.5)
        rng = np.random.default_rng(5)
        lights = VGroup(*[Dot(globe.get_center() + np.array([rng.normal(0, 1.2), rng.normal(0, 0.55), 0]),
                              radius=rng.uniform(0.02, 0.07), color=NIGHT, fill_opacity=rng.uniform(0.4, 1.0))
                          for _ in range(70)])
        hsw = study_card(r"Growth seen from space", r"Henderson, Storeygard and Weil (2012)",
                         [(r"method", r"night-time lights, recorded by satellite, track economic activity"),
                          (r"result", r"where accounts are poor, weight lights and official growth about equally; "
                                      r"estimates differ by up to 3 points a year")],
                         design="calibration", width=6.6, font_size=21).to_edge(RIGHT, buff=0.35).shift(UP * 1.4)
        mart = study_card(r"The dictator's GDP", r"Martinez (2022)",
                          [(r"method", r"compare reported GDP with lights, \ democracies against autocracies"),
                           (r"result", r"autocracies overstate yearly growth by about 35\%: \ a true 2\% "
                                       r"reported as 2.7\%")],
                          design="calibration", width=6.6, font_size=21).next_to(hsw, DOWN, buff=0.3)
        bars = VGroup()
        for i, (v, col, nm) in enumerate(((2.0, NIGHT, r"growth the lights imply"),
                                          (2.7, E.MISS, r"growth reported"))):
            r = Rectangle(width=v * 1.0, height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.85)
            r.move_to([-6.0 + v * 0.5, -2.2 - 0.62 * i, 0])
            bars.add(VGroup(r, label(rf"{nm}: \ {v:.1f}\%", font_size=20, color=col).next_to(r, RIGHT, buff=0.15)))
        tag = illustrative_tag(r"illustrative: an island at night; the bars restate Martinez's estimate", corner=DL,
                               font_size=14)
        with self.voiceover(
            "Where the accounts can't be trusted, economists have looked down from space. <bookmark mark='a'/> "
            "Satellites photograph the earth at night, and light tracks economic activity. In 2012 Vernon "
            "Henderson, Adam Storeygard and David Weil showed how to combine growth in lights with official growth: "
            "where the accounts are poor, give them about equal weight. Their estimates differed from the official "
            "ones by up to three points a year. <bookmark mark='b'/> In 2022 Luis Martinez used the same lights to "
            "test governments. For the same growth in light, autocracies report more growth of GDP than "
            "democracies do. <bookmark mark='c'/> His estimate: autocracies overstate their yearly growth by about "
            "35 percent, so that a true two percent is reported as two point seven."
        ) as vo:
            self.play(FadeIn(globe), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(l, scale=0.3) for l in lights], lag_ratio=0.02), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(hsw, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(mart, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], LEFT), FadeIn(b[1])) for b in bars],
                                  lag_ratio=0.5))
        self.clear_scene()

    def next_sna(self):
        head = label(r"The System of National Accounts, \ 2025 edition", font_size=32, color=E.WORLD)
        head.to_edge(UP, buff=0.5)
        items = VGroup(
            label(r"data counted as an asset, \ like software and research before it", font_size=26),
            label(r"the depletion of natural resources charged as a cost of production", font_size=26),
            label(r"guidance for digital trade, \ ordered and delivered online", font_size=26),
            label(r"accounts of distribution and of unpaid household work, \ beside GDP", font_size=26,
                  color=UNPAID),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(DOWN * 0.1)
        for it in items:
            it.scale(1.15)
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(DOWN * 0.1)
        back = label(r"Kuznets's three warnings, \ ninety years on: \ two are getting accounts of their own",
                     font_size=24, color=KUZ).to_edge(DOWN, buff=0.55)
        tag = published_tag(r"United Nations Statistical Commission, March 2025", corner=DR, font_size=15)
        with self.voiceover(
            "And the standard itself keeps moving. The new System of National Accounts, adopted in March 2025, "
            "<bookmark mark='a'/> counts data as an asset that firms invest in, as software and research were "
            "counted before it. <bookmark mark='b'/> It charges the running-down of natural resources as a cost of "
            "production, so that a country living off its oil shows a smaller net product. "
            "<bookmark mark='c'/> It adds guidance for trade that is ordered and delivered online. "
            "<bookmark mark='d'/> And it adds guidance for accounts, beside GDP, of how income is distributed and "
            "of the unpaid work done at home. <bookmark mark='e'/> Two of Kuznets's three "
            "warnings, ninety years later, are getting accounts of their own."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(back))
        self.clear_scene()
