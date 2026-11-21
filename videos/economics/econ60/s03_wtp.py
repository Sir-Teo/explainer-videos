from __future__ import annotations

from videos.economics.econ60.common import *  # noqa: F403


class WTP(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Measuring willingness to pay", r"How do you learn what buyers would pay \ before you set the "
             r"price?", "Chapter two. Measuring willingness to pay.",
             lit={1964: r"Becker, DeGroot and Marschak", 2005: r"hypothetical bias"},
             scale=("person", "firm"), horizon=("a day",))
        self.asking()
        self.conjoint()

    def asking(self):
        cards = point_cards([
            (r"ask", r"`what would you pay?' \ talk is cheap: \ stated values run high; \ the median ratio of stated "
             r"to actual in 83 comparisons, \ 1.35", COST),
            (r"make them choose", r"conjoint analysis: \ choices among priced options, \ as in a shop; \ choosing "
             r"reduces the bias", TEST),
            (r"make it real", r"Becker, \ DeGroot and Marschak's lottery: \ state a price, \ a random price is drawn, "
             r"\ you buy at it if yours is higher; \ honesty is the best strategy", LEIS),
            (r"watch them buy", r"past sales, \ auctions, \ and price experiments: \ chapter three", AIR),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"four ways to learn what buyers would pay", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Murphy, \ Allen, \ Stevens and Weatherhead (2005); \ Becker, \ DeGroot and Marschak "
                            r"(1964)", corner=DL, font_size=12)
        with self.voiceover(
            "There are four ways to learn what buyers would pay. <bookmark mark='a'/> Ask them. It is cheap, and it "
            "runs high: a meta-analysis by James Murphy and coauthors found that across eighty-three comparisons, "
            "stated values were typically about a third above what people actually paid when money changed hands. "
            "<bookmark mark='b'/> Make them choose. Conjoint analysis shows people sets of priced options, as a shop "
            "would, and infers their values from what they pick; the same meta-analysis found choosing reduces the "
            "bias. <bookmark mark='c'/> Make it real. In the mechanism of Becker, DeGroot and Marschak, you state "
            "a price, a random price is drawn, and you buy at the random price if yours is higher. Overstating can "
            "only make you pay more than you wanted, so honesty is the best strategy. <bookmark mark='d'/> Or "
            "watch them buy: past sales, auctions, and price experiments, the subject of chapter three."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()

    def conjoint(self):
        C = load("conjoint")
        opts = VGroup()
        for price, feats in ((120, (1, 0, 1)), (160, (1, 1, 0)), (80, (0, 0, 0))):
            rows = VGroup(label(rf"\${price}", font_size=24, color=WHITE),
                          *[label(n if f else rf"no {n}", font_size=16, color=LEIS if f else GREY_C)
                            for n, f in zip((r"wifi", r"legroom", r"a free bag"), feats)]).arrange(
                DOWN, buff=0.12)
            box = SurroundingRectangle(rows, buff=0.2, color=AIR, corner_radius=0.1, stroke_width=1.6)
            opts.add(VGroup(box, rows))
        none = VGroup(label(r"none of \\ these", font_size=18, color=GREY_B))
        none.add(SurroundingRectangle(none[0], buff=0.25, color=GREY_C, corner_radius=0.1, stroke_width=1.4))
        opts.add(none)
        opts.arrange(RIGHT, buff=0.3).to_edge(LEFT, buff=0.5).shift(UP * 1.5)
        q = label(r"which would you book?", font_size=20, color=GREY_A).next_to(opts, UP, buff=0.2)
        names = (r"wifi", r"legroom", r"a free bag")
        keys = ("wifi", "legroom", "bag")
        ax = plane([-0.6, 2.6], [0, 25], center=RIGHT * 3.8 + DOWN * 0.9, x_length=5.2, y_length=3.8, xticks=[],
                   yticks=[0, 5, 10, 15, 20, 25], ylabel=r"willingness to pay, \ \$", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        est = [C["wtp"][k] for k in keys]
        se = [C["wtp_se"][k] for k in keys]
        tru = [C["truth"][k] for k in keys]
        b = bars(ax, range(3), est, [TEST] * 3, width=0.5)
        errs = VGroup(*[Line(ax.ax.c2p(k, e - 2 * s), ax.ax.c2p(k, e + 2 * s), color=WHITE, stroke_width=2)
                        for k, (e, s) in enumerate(zip(est, se))])
        ticks = VGroup(*[Line(ax.ax.c2p(k - 0.35, t), ax.ax.c2p(k + 0.35, t), color=OPT, stroke_width=3)
                         for k, t in enumerate(tru)])
        labs = VGroup(*[label(n, font_size=15, color=TEST).next_to(ax.ax.c2p(k, 0), DOWN, buff=0.12)
                        for k, n in enumerate(names)])
        side = VGroup(
            MathTex(r"P(j) = \frac{e^{\beta_p p_j + \beta' x_j}}{\sum_k e^{\beta_p p_k + \beta' x_k}}", font_size=30,
                    color=WHITE),
            MathTex(r"\text{WTP}_{\text{feature}} = -\,\beta_{\text{feature}} / \beta_p", font_size=30,
                    color=E.ACCENT),
            label(rf"{C['n_choices']:,} choices by 400 travellers; \ {100 * C['share_none']:.0f}\% chose none"
                  .replace(",", "{,}"), font_size=18, color=GREY_A),
            label(r"bars: \ estimates $\pm$ 2 s.e.; \ orange: \ planted", font_size=16, color=OPT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(LEFT, buff=0.6).shift(DOWN * 1.6)
        tag = island_tag(r"the Island: \ a conjoint survey simulated; \ agora.revenue.conjoint", corner=DR,
                         font_size=12)
        with self.voiceover(
            "Here is a conjoint survey on the Island. <bookmark mark='a'/> Four hundred travellers each see eight "
            "screens like this one: three fares, each with or without wifi, extra legroom and a free bag, at "
            "different prices, and the option of booking none of them. <bookmark mark='b'/> Their choices are fitted "
            "with the multinomial logit of Part forty-three: each option's probability rises with its utility, a "
            "price coefficient times the price plus a weight on each feature. <bookmark mark='c'/> A feature's "
            "willingness to pay is its weight divided by the price coefficient: how many dollars of price it is "
            f"worth. <bookmark mark='d'/> Wifi comes out at {C['wtp']['wifi']:.1f} dollars, legroom at "
            f"{C['wtp']['legroom']:.1f}, a free bag at {C['wtp']['bag']:.1f}, each within its error of the values "
            "the Island planted, in orange. <bookmark mark='e'/> The airline now knows what to charge for each "
            "extra, as long as people choose on a screen the way they would at the gate, which is the conjoint's "
            "own version of hypothetical bias."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(q))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.1) for o in opts], lag_ratio=0.3), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(ax), FadeIn(labs), LaggedStart(*[GrowFromEdge(x, DOWN) for x in b], lag_ratio=0.3),
                      run_time=1.5)
            self.play(Create(errs), Create(ticks), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Indicate(opts, color=WHITE, scale_factor=1.02))
        self.clear_scene()
