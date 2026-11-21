from __future__ import annotations

from videos.economics.econ61.common import *  # noqa: F403


class AdWork(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Does advertising work?", r"A dashboard says the ads return twelve times their cost. \ Do "
             r"they?", "Chapter seven. Does advertising work?",
             lit={2014: r"eBay's experiment", 2015: r"Lewis and Rao"}, scale=("firm",), horizon=("a year",))
        self.attribution()
        self.experiment()
        self.ebay()
        self.power()
        self.called()

    def attribution(self):
        A = load("ads")
        f = A["frequent"]
        per = 1000
        reg = 0.5 * f * 0.3 * per             # regulars' purchases through ad clicks, per 1,000 searchers
        new = 0.5 * (1 - f) * 0.023 * per     # newcomers' purchases through ad clicks
        caused = (1 - f) * 0.003 * per        # purchases the ads caused
        ax = plane([-0.6, 1.6], [0, 75], center=LEFT * 3.4 + DOWN * 0.4, x_length=5.0, y_length=4.6, xticks=[],
                   yticks=[0, 20, 40, 60], ylabel=r"purchases per 1,000 searchers".replace(",", "{,}"),
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        p0, p1 = ax.ax.c2p(-0.25, 0), ax.ax.c2p(0.25, reg)
        b_reg = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=DRIVER,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
        q0, q1 = ax.ax.c2p(-0.25, reg), ax.ax.c2p(0.25, reg + new)
        b_new = Rectangle(width=q1[0] - q0[0], height=q1[1] - q0[1], stroke_width=0, fill_color=RIDER,
                          fill_opacity=0.85).move_to((q0 + q1) / 2)
        c0, c1 = ax.ax.c2p(0.75, 0), ax.ax.c2p(1.25, caused)
        b_c = Rectangle(width=c1[0] - c0[0], height=max(c1[1] - c0[1], 0.02), stroke_width=0, fill_color=GAIN,
                        fill_opacity=0.95).move_to((c0 + c1) / 2)
        l1 = label(r"sales through \\ an ad click", font_size=15, color=WHITE).next_to(ax.ax.c2p(0, 0), DOWN, buff=0.1)
        l2 = label(r"sales the ads \\ caused", font_size=15, color=GAIN).next_to(ax.ax.c2p(1, 0), DOWN, buff=0.1)
        v1 = label(rf"{reg + new:.0f}", font_size=16, color=WHITE).next_to(b_new, UP, buff=0.06)
        v2 = label(rf"{caused:.1f}", font_size=16, color=GAIN).next_to(b_c, UP, buff=0.06)
        side = VGroup(
            label(rf"{100 * f:.0f}\% of searchers are regulars, \ who buy 30\% of the time, \ ad or no ad",
                  font_size=18, color=DRIVER),
            label(r"the rest buy 2\% of the time; \ seeing the ad adds 0.3 points", font_size=18, color=RIDER),
            label(r"half of all searchers click the ad when it is there, \\ at 50 cents a click; \ otherwise they "
                  r"click the free link", font_size=18, color=GREY_A),
            label(rf"the dashboard's return: \ +{100 * A['attributed_roi']:,.0f}\%".replace(",", "{,}"),
                  font_size=22, color=AD),
            label(rf"sales on spending across regions: \ +{100 * A['ols_roi']:,.0f}\%".replace(",", "{,}"),
                  font_size=22, color=AD),
            label(rf"the truth: \ {100 * A['true_roi']:.0f}\%".replace("-", "{-}"), font_size=24, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        if side.width > 6.6:
            side.width = 6.6
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ agora.platform.search\_ads; \ the regulars' share and the ad's lift planted",
                         corner=DL, font_size=12)
        with self.voiceover(
            "The Island's marketplace buys ads on a search engine, and its dashboard says they pay twelve times "
            f"over. <bookmark mark='a'/> Here is the truth the Island knows. {100 * f:.0f} percent of the people "
            "searching for it are regulars, who buy thirty percent of the time, ad or no ad. <bookmark mark='b'/> "
            "The rest buy two percent of the time, and seeing the ad raises that by three tenths of a point. "
            "<bookmark mark='c'/> When the ad is there, half of all searchers click it, at fifty cents a click; "
            "when it is not, they click the free link just below. <bookmark mark='d'/> The dashboard counts every "
            f"sale that came through an ad click, about {reg + new:.0f} per thousand searchers, most of them "
            f"regulars. The ads caused {caused:.1f}. So the dashboard reports a return of "
            f"{100 * A['attributed_roi']:,.0f} percent. <bookmark mark='e'/> A regression of sales on ad spending "
            f"across regions and weeks does no better: {100 * A['ols_roi']:,.0f} percent, because spending rises "
            "with searches, and searches rise with the people who were going to buy anyway. <bookmark mark='f'/> "
            f"The true return is minus {abs(100 * A['true_roi']):.0f} percent: every dollar of ads brings back "
            f"{1 + A['true_roi']:.2f}."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(l1), FadeIn(l2), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(b_reg, DOWN), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b_new, DOWN), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(v1), GrowFromEdge(b_c, DOWN), FadeIn(v2), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]), Indicate(b_c, color=WHITE))
        self.clear_scene()

    def experiment(self):
        A = load("ads")
        d = np.array(A["experiment_draws"]) * 100
        ax = plane([-220, 100], [0, 1], center=LEFT * 2.6 + DOWN * 0.2, x_length=7.4, y_length=2.6,
                   xticks=[-200, -150, -100, -50, 0, 50, 100], yticks=[], xlabel=r"the experiment's estimated "
                   r"return, \ \%", xfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=14)
        rng = np.random.default_rng(61)
        pts = VGroup(*[dot(ax, float(np.clip(x, -219, 99)), float(rng.uniform(0.15, 0.85)), TEST, 0.06)
                       for x in d])
        tl = vline(ax, 100 * A["true_roi"], 0, 1, GAIN, 2.2)
        zl = vline(ax, 0, 0, 1, GREY_B, 1.2)
        side = VGroup(
            label(rf"ads switched off in a random {100 * A['off_share']:.0f}\% of {A['regions']} regions, \ for "
                  r"eight weeks", font_size=19, color=TEST),
            label(r"difference in differences: \ sales per searcher, \ on against off, \ before and after",
                  font_size=19, color=WHITE),
            label(rf"each dot: \ one run of the experiment; \ spread $\pm${100 * A['experiment_sd']:.0f} points",
                  font_size=19, color=TEST),
            label(rf"green: \ the truth, \ {100 * A['true_roi']:.0f}\%".replace("-", "{-}"), font_size=19,
                  color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(UP, buff=0.5)
        tag = island_tag(r"the Island: \ 200 runs of the regional experiment", corner=DL, font_size=12)
        with self.voiceover(
            "How would the marketplace find out? By switching the ads off. <bookmark mark='a'/> In a random "
            f"{100 * A['off_share']:.0f} percent of its {A['regions']} regions, the ads stop for eight weeks. "
            "<bookmark mark='b'/> Compare the change in sales per searcher where the ads stopped with the change "
            "where they kept running: a difference in differences. <bookmark mark='c'/> Each dot is one run of "
            "that experiment, with the Island's ordinary noise in weekly sales. They scatter, by about "
            f"{100 * A['experiment_sd']:.0f} points either way, <bookmark mark='d'/> around the truth, minus "
            f"{abs(100 * A['true_roi']):.0f} percent. The experiment is noisy, but it is centred on the right "
            "answer; the dashboard and the regression were precise, and wrong by a factor of thirty or more."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zl), FadeIn(tag))
            for k, mk in enumerate("ab"):
                vo.wait_until(mk)
                self.play(FadeIn(side[k]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in pts], lag_ratio=0.04), FadeIn(side[2]),
                      run_time=2.5)
            vo.wait_until("d")
            self.play(Create(tl), FadeIn(side[3]))
        self.clear_scene()

    def ebay(self):
        cards = point_cards([
            (r"brand keywords", r"eBay stops buying ads on searches for `eBay': \ 99.5\% of the clicks arrive "
             r"anyway, \ through the free link", DRIVER),
            (r"non-brand keywords", r"ads switched off for 60 days in regions with 30\% of American traffic: \ "
             r"a return of {-}63\%, \ 95\% interval {-}124\% to {-}3\%", TEST),
            (r"the same data, \ without the experiment", r"a regression of sales on spending gives returns over "
             r"1,400\%".replace(",", "{,}"), AD),
            (r"who the ads moved", r"new and occasional buyers; \ the frequent buyers who made most of the "
             r"ad-attributed sales were not moved at all", RIDER),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"eBay's experiment", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Blake, \ Nosko and Tadelis, \ NBER Working Paper 20171 (2014), \ table 4; \ "
                            r"Econometrica 83(1) (2015)", corner=DL, font_size=12)
        with self.voiceover(
            "The Island's numbers were planted to echo a real experiment. eBay's economists Thomas Blake and "
            "Chris Nosko, with Steven Tadelis, persuaded the company to switch its search ads off. <bookmark "
            "mark='a'/> First the ads on searches for eBay itself: when they stopped, ninety-nine and a half "
            "percent of the clicks still arrived, through the free link underneath. <bookmark mark='b'/> Then all "
            "other keywords, switched off for sixty days in regions holding thirty percent of eBay's American "
            "traffic. The estimated return was minus sixty-three percent, with a confidence interval from minus "
            "a hundred and twenty-four to minus three. <bookmark mark='c'/> The same data, analysed the usual "
            "way, with a regression of sales on ad spending, gave returns of over fourteen hundred percent. "
            "<bookmark mark='d'/> The ads did move new and occasional buyers; but the frequent buyers, who made "
            "most of the sales the ads were credited with, would have bought anyway."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()

    def power(self):
        P = load("adpower")
        ax = plane([0, 160], [0, 1.0], center=LEFT * 3.0 + DOWN * 0.6, x_length=6.0, y_length=3.0,
                   xticks=[0, 40, 80, 120, 160], yticks=[], xlabel=r"people needed in each arm, \ millions",
                   xfmt=lambda v: f"{v:.0f}", font_size=14)
        n1, n2 = P["n_detect_effect"] / 1e6, P["n_tell_roi_from_zero"] / 1e6
        b1 = Rectangle(width=ax.ax.c2p(n1, 0)[0] - ax.ax.c2p(0, 0)[0], height=0.5, stroke_width=0, fill_color=TEST,
                       fill_opacity=0.85).move_to(ax.ax.c2p(n1 / 2, 0.72))
        b2 = Rectangle(width=ax.ax.c2p(n2, 0)[0] - ax.ax.c2p(0, 0)[0], height=0.5, stroke_width=0, fill_color=AD,
                       fill_opacity=0.85).move_to(ax.ax.c2p(n2 / 2, 0.28))
        l1 = label(rf"to detect any effect: \ {n1:.1f} million", font_size=17, color=TEST).next_to(b1, RIGHT,
                                                                                                   buff=0.15)
        l2 = label(rf"to tell a 25\% return from zero: \ {n2:.0f} million", font_size=17, color=AD).next_to(
            b2, UP, buff=0.1).align_to(b2, LEFT)
        facts = VGroup(
            label(r"a campaign spends 10 cents a person; \ a 25\% return means 12.5 cents of extra sales", font_size=20,
                  color=WHITE),
            label(r"but each person's sales average \$7, \ with a standard deviation of \$75", font_size=20,
                  color=GREY_A),
            label(rf"the effect is {100 * P['share_of_sd']:.2f}\% of one person's noise", font_size=20, color=SURGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(UP, buff=0.5)
        tag = illustrative_tag(r"computed: \ agora.platform.ad\_power, \ after Lewis and Rao, \ QJE 130(4) (2015)",
                               corner=DL, font_size=12)
        with self.voiceover(
            "Why don't firms just run the experiment? Because the arithmetic is brutal. Randall Lewis and Justin "
            "Rao called it the unfavourable economics of measuring the returns to advertising. <bookmark "
            "mark='a'/> Suppose a campaign spends ten cents a person, and returns twenty-five percent: twelve and "
            "a half cents of extra sales per person. <bookmark mark='b'/> But what one person spends is wildly "
            "variable: here an average of seven dollars, with a standard deviation of seventy-five. <bookmark "
            f"mark='c'/> The effect is {100 * P['share_of_sd']:.2f} percent of one person's noise. <bookmark "
            f"mark='d'/> To detect that the campaign does anything at all takes {n1:.1f} million people in each "
            "arm. <bookmark mark='e'/> To tell a twenty-five percent return from breaking even takes "
            f"{n2:.0f} million. Only the largest advertisers, on the largest platforms, can learn whether their "
            "advertising pays; everyone else is guessing, and the dashboards guess high."
        ) as vo:
            self.play(FadeIn(tag))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(facts[k]))
            vo.wait_until("d")
            self.play(FadeIn(ax), GrowFromEdge(b1, LEFT), FadeIn(l1))
            vo.wait_until("e")
            self.play(GrowFromEdge(b2, LEFT), FadeIn(l2))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["adwords_roi"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome).replace("-", "{-}"),
                       c.verdict, width=12.6, font_size=17)
        cc.move_to(UP * 0.6)
        lesson = label(r"the sales that come through an ad are not the sales the ad causes", font_size=22,
                       color=E.ACCENT).next_to(cc, DOWN, buff=0.55)
        tag = published_tag(r"Blake, \ Nosko and Tadelis, \ NBER Working Paper 20171 (2014), \ section 6", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> Blake, Nosko and Tadelis quoted the advice Google gave its "
            "advertisers: determining your return can be a very straightforward process. Take the revenue from "
            "sales made via your ads, subtract their cost, and divide by the cost. <bookmark mark='b'/> eBay's "
            "experiment found that the same calculation, which gave thousands of percent, missed the sign: the "
            "true return on non-brand ads was negative. <bookmark mark='c'/> The verdict: wrong. <bookmark "
            "mark='d'/> The sales that come through an ad are not the sales the ad causes. That sentence is "
            "most of what economists brought to advertising."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(cc.left), FadeIn(tag))
            vo.wait_until("a")
            self.play(Indicate(cc.left, color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(cc.right))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
            vo.wait_until("d")
            self.play(FadeIn(lesson))
        self.clear_scene()
