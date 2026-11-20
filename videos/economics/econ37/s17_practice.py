from __future__ import annotations

from videos.economics.econ37.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ planning, \ property and transport", r"Who does this for a living?",
             "Chapter fifteen. In practice: planning, property and transport.", lit={1997: r"Cairncross"},
             scale=("firm", "city"), horizon=("a year", "a decade"))
        self.jobs()
        self.called()

    def jobs(self):
        rows = VGroup(
            label(r"the people who do this", font_size=27, color=E.ACCENT),
            label(r"urban planners and housing economists: \ zoning, \ supply, \ what a rule does to rents",
                  font_size=21, color=CITY),
            label(r"real-estate analysts: \ hedonic prices, \ the rent gradient, \ where a city will grow",
                  font_size=21, color=RENT),
            label(r"transport appraisal: \ time saved, \ and the productivity of a denser city", font_size=21,
                  color=ROAD),
            label(r"retailers and logistics firms: \ gravity models of where customers come from", font_size=21,
                  color=GOLD),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Saiz (2010); \ Rosen (1979); \ Roback (1982)", corner=DR, font_size=12)
        with self.voiceover(
            "Who does this for a living? <bookmark mark='a'/> City governments employ planners and housing "
            "economists who estimate what a zoning rule or a new tower will do to supply and to rents. "
            "<bookmark mark='b'/> Property firms employ analysts who price buildings by their features and their "
            "place on the rent gradient, and forecast where a city will grow. <bookmark mark='c'/> Transport "
            "ministries appraise a new line by the time it saves, and some, as in Britain, add the extra "
            "productivity of a denser, better-connected city, using elasticities like this part's dial. "
            "<bookmark mark='d'/> And retailers and logistics firms use gravity models to decide where to put a "
            "shop or a warehouse."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["cairncross_1997"]
        W = load("wfh")
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=17).move_to(UP * 0.3)
        tag = published_tag(r"Cairncross (1997); \ Barrero, \ Bloom and Davis, \ via FRED", corner=DR, font_size=12)
        foot = label(r"cheaper communication made the best places more valuable, \ not less", font_size=20,
                     color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In 1997 Frances Cairncross, a journalist at The Economist, published "
            "The Death of Distance. As communication became nearly free, she argued, distance would stop deciding "
            "its cost, location would matter less to most decisions of business, and more people would work from "
            "home. <bookmark mark='b'/> The cost of communicating did collapse, and after 2020 about a quarter of "
            f"America's paid working days were worked from home, {W['last12']:.0f} percent over the last year of "
            "data. But economic activity kept concentrating in large, expensive cities, and their wage premium "
            "grew. <bookmark mark='c'/> The verdict: partly right. <bookmark mark='d'/> Cheaper communication made "
            "the places where people meet more valuable, not less."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
