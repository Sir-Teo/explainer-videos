from __future__ import annotations

from videos.economics.econ41.common import *  # noqa: F403


class Salience(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Taxes on the shelf tag", r"Do people respond to taxes they do not see?",
             "Chapter ten. Taxes on the shelf tag.", lit={2009: r"Chetty, \ Looney and Kroft"},
             scale=("household", "firm"), horizon=("a day",))
        self.tags()
        self.meaning()

    def tags(self):
        C = tables.CLK_2009.data
        tag0 = VGroup(RoundedRectangle(width=3.2, height=1.6, corner_radius=0.1, stroke_color=GREY_B, stroke_width=2,
                                       fill_color="#141821", fill_opacity=1),
                      label(r"\$2.99", font_size=40, color=WHITE)).arrange(ORIGIN)
        tag1 = VGroup(RoundedRectangle(width=3.2, height=1.6, corner_radius=0.1, stroke_color=REVENUE, stroke_width=2,
                                       fill_color="#141821", fill_opacity=1),
                      VGroup(label(r"\$2.99", font_size=30, color=GREY_A),
                             label(rf"with tax: \ \${2.99 * (1 + C['tax'] / 100):.2f}", font_size=30,
                                   color=REVENUE)).arrange(DOWN, buff=0.12)).arrange(ORIGIN)
        tags = VGroup(VGroup(label(r"the usual tag \ (an example): \ tax added at the till", font_size=20,
                                   color=GREY_A), tag0)
                      .arrange(DOWN, buff=0.25),
                      VGroup(label(r"the experiment's tag", font_size=20, color=REVENUE), tag1).arrange(DOWN, buff=0.25)
                      ).arrange(RIGHT, buff=1.4).move_to(UP * 1.2)
        bar0 = Rectangle(width=6.0, height=0.5, stroke_width=0, fill_color=GREY_B, fill_opacity=0.8)
        bar1 = Rectangle(width=6.0 * (1 - C["drop"] / 100), height=0.5, stroke_width=0, fill_color=REVENUE,
                         fill_opacity=0.9)
        bars = VGroup(VGroup(label(r"sales, \ usual tags", font_size=20, color=GREY_A), bar0).arrange(RIGHT, buff=0.3),
                      VGroup(label(r"sales, \ tax shown", font_size=20, color=REVENUE), bar1).arrange(RIGHT, buff=0.3)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 1.6)
        res = label(rf"$-${C['drop']}\%: \ about as much as a {C['tax']}\% price rise", font_size=22,
                    color=E.ACCENT).next_to(bars, DOWN, buff=0.3)
        tag = published_tag(tables.CLK_2009.tag, corner=DR, font_size=11)
        with self.voiceover(
            "American shelf prices usually leave out the sales tax, which is added at the till. Does anyone notice? "
            f"<bookmark mark='a'/> In 2006 Raj Chetty, Adam Looney and Kory Kroft posted tags showing the price with "
            f"the {C['tax']} percent sales tax included, on about {C['products']} products in one supermarket, for "
            "three weeks. <bookmark mark='b'/> The tax was the same; only its visibility changed. "
            f"<bookmark mark='c'/> Sales of those products fell by about {C['drop']} percent compared with similar "
            "products and nearby stores, about as much as if the price itself had risen by the tax. Most shoppers "
            "ignore a tax they do not see."
        ) as vo:
            self.play(FadeIn(tags[0]), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(tags[1]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][0]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[1][1], LEFT), FadeIn(bars[1][0]), FadeIn(res))
        self.clear_scene()

    def meaning(self):
        cards = point_cards([
            (r"incidence", r"a hidden tax falls \\ more on buyers, \\ who do not react", WORKER),
            (r"efficiency", r"if people ignore it, \\ a hidden tax distorts \\ less, \ but they \\ misjudge budgets",
             GAIN),
            (r"elasticities", r"the response to a tax \\ is not the response \\ to the same price", RATE),
            (r"design", r"visibility is \\ a policy choice", E.ACCENT),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"what salience changes", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Salience changes the textbook. <bookmark mark='a'/> A tax people do not notice falls more on them, "
            "because they do not react by buying less. <bookmark mark='b'/> It also distorts less, but people who "
            "misjudge prices misjudge their budgets, which has costs of its own. <bookmark mark='c'/> The response to "
            "a tax can differ from the response to the same change in price, so elasticities measured from prices "
            "do not always carry over. <bookmark mark='d'/> And how visible a tax is becomes part of its design."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
