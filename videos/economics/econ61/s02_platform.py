from __future__ import annotations

from videos.economics.econ61.common import *  # noqa: F403


class Platform(VoiceoverScene):
    def construct(self):
        card(self, 1, r"A platform is a designed market", r"What does a platform choose that a market left alone "
             r"would not?", "Chapter one. A platform is a designed market.",
             lit={2003: r"Rochet and Tirole", 2016: r"Einav, Farronato and Levin"}, scale=("firm", "market"),
             horizon=("a day", "a year"))
        self.levers()
        self.tools()

    def levers(self):
        hub = VGroup(RoundedRectangle(width=3.0, height=1.5, corner_radius=0.2, stroke_color=PLAT, stroke_width=3,
                                      fill_color=PLAT, fill_opacity=0.18),
                     label(r"the platform", font_size=26, color=PLAT))
        hub[1].move_to(hub[0])
        riders = VGroup(*[Dot(radius=0.1, color=RIDER) for _ in range(7)]).arrange(DOWN, buff=0.22)
        drivers = VGroup(*[Dot(radius=0.1, color=DRIVER) for _ in range(7)]).arrange(DOWN, buff=0.22)
        rl = label(r"riders, \\ buyers, \\ searchers", font_size=19, color=RIDER)
        dl = label(r"drivers, \\ sellers, \\ advertisers", font_size=19, color=DRIVER)
        left = VGroup(rl, riders).arrange(DOWN, buff=0.25)
        right = VGroup(dl, drivers).arrange(DOWN, buff=0.25)
        net = VGroup(left, hub, right).arrange(RIGHT, buff=2.4).move_to(UP * 0.55)
        links = VGroup(*[Line(d.get_center(), hub[0].get_left() if d in riders else hub[0].get_right(),
                              stroke_width=1.3, color=GREY_C) for d in list(riders) + list(drivers)])
        levers = VGroup(
            label(r"prices: \ the fare, \ the commission, \ the surge", font_size=19, color=SURGE),
            label(r"matching: \ which driver gets which rider", font_size=19, color=RIDER),
            label(r"information: \ ranking, \ ratings, \ what each side sees", font_size=19, color=SELL),
            label(r"rules: \ who may join, \ what may be promised", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(net, DOWN, buff=0.45)
        tag = published_tag(r"Parts 17 and 44; \ Rochet and Tirole (2003); \ Einav, \ Farronato and Levin, \ Annual "
                            r"Review of Economics 8 (2016)", corner=DL, font_size=12)
        with self.voiceover(
            "A market left alone has prices that nobody sets, and information that is wherever it happens to be. "
            "A platform is a market that somebody owns and designs. <bookmark mark='a'/> On one side, riders, "
            "buyers, people searching; on the other, drivers, sellers, advertisers; between them, the platform, "
            "which every transaction passes through. <bookmark mark='b'/> It sets prices: the fare, the commission "
            "it keeps, the surge. Part forty-four showed why a platform may charge one side little or nothing and "
            "the other side most: what matters is the structure of prices across the two sides, not only their "
            "level. <bookmark mark='c'/> It decides who is matched with whom, Part seventeen's question, now run "
            "by an algorithm millions of times a day. <bookmark mark='d'/> It decides what each side sees: the "
            "order of the search results, the ratings, even whether a driver sees where a rider is going before "
            "accepting. <bookmark mark='e'/> And it writes the rules: who may join, what may be promised, what "
            "gets you thrown off."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(net), Create(links), run_time=1.6)
            for mk, r_ in zip("bcde", levers):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def tools(self):
        cards = point_cards([
            (r"theory", r"a model of both sides, \ to say which way a fee or a rule should move \ (Parts 17 and 44)",
             PLAT),
            (r"measurement", r"demand and supply estimated from the platform's own data, \ as in Part 43", RIDER),
            (r"experiments", r"thousands a year, \ randomized by user, \ by time or by city \ (chapters eight and "
             r"nine)", TEST),
        ], width=12.6, cols=3, font_size=20).move_to(UP * 0.4)
        head = label(r"the economist's three tools inside a platform", font_size=30, color=E.ACCENT).to_edge(
            UP, buff=0.5)
        foot = label(r"and one advantage no academic has: \ the platform can change the market it studies",
                     font_size=22, color=GREY_A).next_to(cards, DOWN, buff=0.6)
        tag = published_tag(r"Athey and Luca, \ Journal of Economic Perspectives 33(1) (2019)", corner=DL,
                            font_size=12)
        with self.voiceover(
            "Inside a platform, the economist works with three tools. <bookmark mark='a'/> Theory: a model of both "
            "sides of the market, to say which way a fee or a rule should move, and what the second side will do "
            "when the first one changes. <bookmark mark='b'/> Measurement: demand and supply estimated from the "
            "platform's own records, the methods of Part forty-three with far more data. <bookmark mark='c'/> And "
            "experiments, thousands of them, randomized by user, by hour or by city. <bookmark mark='d'/> Which "
            "gives the economist inside one advantage no academic has: the platform can change the market it is "
            "studying, and watch what happens."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
