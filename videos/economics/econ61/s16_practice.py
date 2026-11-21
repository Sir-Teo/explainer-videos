from __future__ import annotations

from videos.economics.econ61.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ economists in tech", r"What does the job look like, \ and what does an "
             r"economist add to a room of engineers?", "Chapter fourteen. In practice: economists in tech.",
             lit={2019: r"Athey and Luca"}, scale=("firm",), horizon=("a day", "a year"))
        self.roles()
        self.questions()

    def roles(self):
        cards = point_cards([
            (r"market design", r"prices, \ fees, \ auctions, \ matching and ranking rules: \ chapters two to six",
             PLAT),
            (r"measurement", r"experiments and their pitfalls, \ demand and supply estimated from the platform's "
             r"own records: \ chapters seven to ten", TEST),
            (r"forecasting and planning", r"how many drivers next Friday, \ how much server capacity next year, \ "
             r"what a change will do before it ships", RIDER),
            (r"policy", r"antitrust, \ privacy, \ labour law: \ the economist who can say what a rule will do to "
             r"both sides", SURGE),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"what economists do inside technology companies", font_size=30, color=E.ACCENT).to_edge(
            UP, buff=0.5)
        tag = published_tag(r"Athey and Luca, \ `Economists (and Economics) in Tech Companies', \ Journal of "
                            r"Economic Perspectives 33(1) (2019)", corner=DL, font_size=12)
        with self.voiceover(
            "Over the past two decades technology companies have become large employers of PhD economists. Susan "
            "Athey and Michael Luca, both of whom have done the work, describe what they do. <bookmark mark='a'/> "
            "Market design: the prices, fees, auctions, matching and ranking rules of chapters two to six. "
            "<bookmark mark='b'/> Measurement: experiments and their pitfalls, and demand and supply estimated "
            "from the platform's own records. <bookmark mark='c'/> Forecasting and planning: how many drivers "
            "next Friday, what a change will do before it ships. <bookmark mark='d'/> And policy: what an "
            "antitrust remedy, a privacy rule or a labour law will do to both sides of the market."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()

    def questions(self):
        head = label(r"three questions the economist asks of every number", font_size=30, color=E.ACCENT).to_edge(
            UP, buff=0.5)
        rows = VGroup(
            VGroup(label(r"1. \ Is it caused, \ or only correlated?", font_size=26, color=TEST),
                   label(r"the dashboard's return against the experiment's \ (chapter seven)", font_size=19,
                         color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"2. \ What does the other side do?", font_size=26, color=DRIVER),
                   label(r"the commission's effect through drivers' waits; \ the A/B test's stolen rides \ "
                         r"(chapters two and nine)", font_size=19, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                          buff=0.1),
            VGroup(label(r"3. \ Whose welfare is it?", font_size=26, color=GAIN),
                   label(r"the platform's take against riders' and drivers' surplus; \ the value of free goods \ "
                         r"(chapters two and twelve)", font_size=19, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                            buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).next_to(head, DOWN, buff=0.7)
        foot = label(r"engineers optimize a metric; \ the economist asks whether it is the right one", font_size=22,
                     color=E.ACCENT).next_to(rows, DOWN, buff=0.6)
        with self.voiceover(
            "What does an economist add to a room of engineers and data scientists, who can all run a regression? "
            "Three questions, asked of every number. <bookmark mark='a'/> Is it caused, or only correlated? The "
            "advertising dashboard of chapter seven was precise and wrong. <bookmark mark='b'/> What does the "
            "other side of the market do? The commission worked through drivers' waits, and the A/B test of "
            "chapter nine counted rides stolen from the control group. <bookmark mark='c'/> And whose welfare is "
            "it? The platform's take, the riders' surplus and the drivers' are different numbers, and so is the "
            "value of a service nobody pays for. <bookmark mark='d'/> Engineers are superb at optimizing a "
            "metric. The economist's job is to ask whether it is the right one."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
