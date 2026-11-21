from __future__ import annotations

from videos.economics.econ61.common import *  # noqa: F403

RULES = ("likeliest buyers", "at random", "estimated effect", "true effect")
NAMES = (r"the likeliest \\ buyers", r"at random", r"the largest \\ estimated effect", r"the largest \\ true effect")


class CausalML(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Causal machine learning in production", r"Who should get the coupon, \ and what will it "
             r"do next year?", "Chapter ten. Causal machine learning in production.",
             lit={2016: r"Athey and Imbens", 2019: r"the surrogate index"}, scale=("person", "firm"),
             horizon=("a day", "a year"))
        self.uplift()
        self.qini()
        self.surrogates()

    def uplift(self):
        U = load("uplift")
        g = U["gains"]
        vals = [100 * g[k] for k in RULES]
        ax = plane([-0.6, 3.6], [-2, 15], center=LEFT * 3.0 + DOWN * 0.4, x_length=6.2, y_length=4.6, xticks=[],
                   yticks=[0, 5, 10, 15], ylabel=r"extra purchases per 100 customers coupon'd",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        cols = (SURGE, GREY_B, TEST, TRUE)
        b = bars(ax, range(4), vals, cols, width=0.55)
        labs = VGroup(*[label(n, font_size=14, color=c).next_to(ax.ax.c2p(k, -2), DOWN, buff=0.1)
                        for k, (n, c) in enumerate(zip(NAMES, cols))])
        vl = VGroup(*[label(f"{v:+.1f}".replace("-", "{-}"), font_size=15, color=c).next_to(
            x, UP if v >= 0 else DOWN, buff=0.06) for v, c, x in zip(vals, cols, b)])
        zero = seg(ax, -0.6, 0, 3.6, 0, GREY_C, 1.2)
        side = VGroup(
            label(rf"a coupon for {100 * U['budget']:.0f}\% of 50,000 customers".replace(",", "{,}"), font_size=20,
                  color=WHITE),
            label(rf"it helps most customers a little; \ for {100 * U['share_negative']:.0f}\% it only costs \\ "
                  r"(they would have bought anyway, \ and now pay less)", font_size=18, color=GREY_A),
            label(r"the usual targeting, \ the likeliest buyers: \ worse than random", font_size=19, color=SURGE),
            label(r"target the effect, \ not the outcome: \\ uplift models, \ causal forests, \ meta-learners",
                  font_size=19, color=TEST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ agora.platform.uplift; \ each customer's effect planted", corner=DL,
                         font_size=12)
        with self.voiceover(
            "Experiments say what a change does on average. The next question is for whom. <bookmark mark='a'/> "
            f"The Island's marketplace has a coupon for {100 * U['budget']:.0f} percent of its fifty thousand "
            "customers. <bookmark mark='b'/> It raises most customers' chance of buying a little, but for "
            f"{100 * U['share_negative']:.0f} percent it only costs money: they would have bought anyway. "
            "<bookmark mark='c'/> The usual targeting rule sends coupons to the customers most likely to buy. "
            f"Here that yields {vals[0]:+.1f} purchases per hundred coupons, worse than sending them at random, "
            f"{vals[1]:+.1f}, because the likeliest buyers are exactly the ones who need no coupon. <bookmark "
            f"mark='d'/> Target by the effect instead, estimated from an experiment by an uplift model, and the "
            f"coupons yield {vals[2]:+.1f}, close to the {vals[3]:+.1f} a planner who knew everyone's true effect "
            "would get. This is where machine learning met causal inference in industry: causal forests and "
            "their relatives estimate how an effect varies, the methods Susan Athey and Guido Imbens brought from "
            "statistics into economics."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(b[0], UP if vals[0] < 0 else DOWN), FadeIn(vl[0]), GrowFromEdge(b[1], DOWN),
                      FadeIn(vl[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(GrowFromEdge(b[2], DOWN), FadeIn(vl[2]), GrowFromEdge(b[3], DOWN), FadeIn(vl[3]),
                      FadeIn(side[3]))
        self.clear_scene()

    def qini(self):
        U = load("uplift")
        x, c = np.array(U["curve_x"]), 100 * np.array(U["curve"])
        ax = plane([0, 1], [0, 7.5], center=LEFT * 3.0 + DOWN * 0.4, x_length=6.2, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 2, 4, 6], xlabel=r"share of customers given "
                   r"the coupon, \ by estimated effect", ylabel=r"extra purchases per 100 customers",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{v:.0f}", font_size=14)
        q = path(ax, x, c, TEST, 3.0)
        rnd = path(ax, [0, 1], [0, c[-1]], GREY_B, 2.0, smooth=False)
        k = int(np.argmax(c))
        pk = dot(ax, x[k], c[k], TEST, 0.08)
        side = VGroup(
            label(r"pink: \ coupons to the highest estimated effects first", font_size=19, color=TEST),
            label(r"grey: \ the same number, \ at random", font_size=19, color=GREY_B),
            label(r"the curve bends: \ each extra coupon does less, \\ and the last ones do harm", font_size=19,
                  color=WHITE),
            label(r"the area between the curves scores the model, \\ on customers it was not trained on",
                  font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ the gains curve of the estimated effects", corner=DL, font_size=12)
        with self.voiceover(
            "How is such a model judged? Not by how well it predicts purchases, but by what its ranking is "
            "worth. <bookmark mark='a'/> Give coupons in order of estimated effect, and add up the extra "
            "purchases. <bookmark mark='b'/> Against it, the same number given at random. <bookmark mark='c'/> The "
            "curve rises steeply, flattens, and turns down at the end, where the coupons go to the customers they "
            "harm. <bookmark mark='d'/> The area between the two curves, measured on customers held out of the "
            "training, is the model's score: the economics of targeting, put in a single number."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(q), FadeIn(side[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(rnd), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(pk), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def surrogates(self):
        L = load("longterm")
        chain = flow_chain([(r"the discount", TEST), (r"orders in the first month", RIDER),
                            (r"sessions in the second month", SELL), (r"orders over the year", TRUE)],
                           box_w=2.7, box_h=1.0, buff=0.5, font_size=19).to_edge(UP, buff=0.6)
        ax = plane([-0.6, 2.6], [-6, 45], center=LEFT * 3.0 + DOWN * 0.85, x_length=6.0, y_length=3.2, xticks=[],
                   yticks=[0, 20, 40], ylabel=r"effect, \ \%", yfmt=lambda v: f"{v:.0f}", font_size=14)
        vals = [100 * L["short"], 100 * L["surrogate"], 100 * L["truth"]]
        cols = (RIDER, TEST, TRUE)
        b = bars(ax, range(3), vals, cols, width=0.5)
        names = (r"first month", r"surrogate index, \\ after eight weeks", r"the year \\ (the truth)")
        labs = VGroup(*[label(n, font_size=14, color=c).next_to(ax.ax.c2p(k, -6), DOWN, buff=0.1)
                        for k, (n, c) in enumerate(zip(names, cols))])
        vl = VGroup(*[label(f"{v:+.1f}\\%".replace("-", "{-}"), font_size=15, color=c).next_to(
            x, UP if v >= 0 else DOWN, buff=0.06) for v, c, x in zip(vals, cols, b)])
        zero = seg(ax, -0.6, 0, 2.6, 0, GREY_C, 1.2)
        side = VGroup(
            label(r"fit last year's customers: \ the year's orders on the first two months", font_size=19,
                  color=GREY_A),
            label(r"apply the fit to the experiment's arms after eight weeks", font_size=19, color=TEST),
            label(rf"the index: \ {vals[1]:+.1f}\% \ ($\pm${200 * L['surrogate_se']:.1f}); \ the truth: \ "
                  rf"{vals[2]:+.1f}\%".replace("-", "{-}"), font_size=20, color=WHITE),
            label(r"valid only if the surrogates carry the whole effect", font_size=19, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35).shift(DOWN * 1.0)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Athey, \ Chetty, \ Imbens and Kang, \ NBER Working Paper 26463 (2019); \ the Island: \ "
                            r"agora.platform.long\_term", corner=DL, font_size=12)
        with self.voiceover(
            "The hardest question is the long run. Experiments last weeks; the decisions are about years. "
            "<bookmark mark='a'/> The Island tests a month-long discount. Orders in the first month rise by "
            f"{vals[0]:.0f} percent: a triumph, if the test stops there. <bookmark mark='b'/> But some customers "
            "learn to wait for the next discount, and their visits in the second month fall. The year's orders "
            f"actually fall, by {abs(vals[2]):.1f} percent. <bookmark mark='c'/> Susan Athey, Raj Chetty, Guido "
            "Imbens and Hyunseung Kang proposed the surrogate index: in last year's data, learn how the year's "
            "orders depend on the first two months' behaviour, <bookmark mark='d'/> then apply that relation to "
            "the experiment's two arms after eight weeks. <bookmark mark='e'/> The index predicts "
            f"{vals[1]:+.1f} percent, close to the truth of {vals[2]:+.1f}, ten months early. <bookmark mark='f'/> "
            "It works only if the short-run measures carry the whole effect of the treatment on the long run; "
            "a discount that also changed something the surrogates miss would fool it."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(ax), FadeIn(labs), FadeIn(zero))
            vo.wait_until("a")
            self.play(FadeIn(chain.boxes[0]), GrowArrow(chain.arrows[0]), FadeIn(chain.boxes[1]),
                      GrowFromEdge(b[0], DOWN), FadeIn(vl[0]))
            vo.wait_until("b")
            self.play(GrowArrow(chain.arrows[1]), FadeIn(chain.boxes[2]), GrowArrow(chain.arrows[2]),
                      FadeIn(chain.boxes[3]), GrowFromEdge(b[2], UP), FadeIn(vl[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[0]))
            vo.wait_until("d")
            self.play(FadeIn(side[1]))
            vo.wait_until("e")
            self.play(GrowFromEdge(b[1], UP), FadeIn(vl[1]), FadeIn(side[2]))
            vo.wait_until("f")
            self.play(FadeIn(side[3]))
        self.clear_scene()
