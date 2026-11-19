from __future__ import annotations

from videos.economics.econ9.common import *  # noqa: F403

PRED = "#C9A0FF"


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ general equilibrium models, \ and NAFTA", r"How are whole-economy models "
             r"used, and how well do they forecast?", "Chapter fifteen. In practice: general equilibrium models, and "
             "NAFTA.", lit={1992: r"the NAFTA models"}, scale=("market", "nation", "world"), horizon=("a decade",))
        self.models()
        self.called()
        self.scatter()

    def models(self):
        head = label(r"computable general equilibrium models", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"the whole economy at once: \ households, \ industries, \ a government, \ the rest of the world",
                  font_size=25),
            label(r"built on an input--output table (Part 3), \ with tastes and technologies of the kinds in "
                  r"Parts 5--8", font_size=24),
            label(r"parameters set so that the model reproduces one year's table exactly: \ \emph{calibration}",
                  font_size=24, color=GREY_A),
            label(r"then change a tax or a tariff, \ solve for the new prices, \ and compare", font_size=25,
                  color=CC),
            label(r"used for trade agreements, \ tax reforms, \ carbon prices, \ by governments and the World Bank",
                  font_size=24),
            label(r"key ingredient for trade: \ how easily buyers switch between home and foreign goods \\ "
                  r"(the Armington elasticity)", font_size=23, color=HOLD),
        ).arrange(DOWN, buff=0.34).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Everything in this part is the theory behind a tool that governments use every week. "
            "<bookmark mark='a'/> A computable general equilibrium model describes a whole economy at once: "
            "households, industries, a government, and the rest of the world. <bookmark mark='b'/> It is built on "
            "an input-output table like the one in Part three, with tastes and technologies of the kinds in Parts "
            "five to eight. <bookmark mark='c'/> Its parameters are set so that it reproduces one year's table "
            "exactly, which is called calibration. <bookmark mark='d'/> Then you change a tax or a tariff, solve "
            "for the new equilibrium prices with methods like those of chapter nine, and compare. "
            "<bookmark mark='e'/> Such models are used to assess trade agreements, tax reforms and carbon prices. "
            "<bookmark mark='f'/> For trade, much depends on one number: how readily buyers switch between home and "
            "foreign versions of a good. In 1992, models like this were used to forecast what the North American "
            "Free Trade Agreement would do."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(rows[0]))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["nafta_1992"]
        n = load("nafta")
        cc = call_card(r"Sobarzo's model of Mexico \ (US International Trade Commission, 1992)", c.when,
                       r"free trade would raise Mexico's imports from North America, \ relative to its GDP, \ most in "
                       r"machinery (+20.7\%), \ iron and steel (+17.7\%) \ and mining (+13.2\%), \ and lower them in "
                       r"tobacco, \ food and paper",
                       rf"1989--2009: \ imports rose relative to GDP in 20 of 21 industries, \ by a median "
                       rf"{n['median_actual']:.0f}\%, \ most in tobacco (+576\%), \ chemicals (+219\%) \ and "
                       r"beverages (+189\%); \ weighted correlation of forecast and outcome: \ $-0.12$",
                       c.verdict, width=12.4, font_size=23).move_to(UP * 0.6)
        q = label(r"``if we look at the correlations of what we predicted with what happened, \\ they average about "
                  r"zero'' \ \ --- Timothy Kehoe, \ who had worked on the model", font_size=22,
                  color=E.ACCENT).to_edge(DOWN, buff=0.55)
        tag = published_tag(r"Kehoe, NAFTA at 20 (Dallas Fed, 2014), table 1; Kehoe (2005)", corner=DR, font_size=13)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> One of the models presented at the US International Trade "
            "Commission's conference in 1992 was Horacio Sobarzo's model of Mexico. It forecast that free trade "
            "would raise Mexico's imports from the rest of North America, relative to its GDP, most in machinery, "
            "iron and steel, and mining, by up to about twenty percent, and lower them in tobacco, food and paper. "
            "<bookmark mark='b'/> From 1989 to 2009, Mexico's imports from North America rose relative to GDP in "
            "twenty of the twenty-one industries, by a median of about ninety-five percent: most in tobacco, "
            "chemicals and beverages, three industries the model expected to shrink. <bookmark mark='c'/> Wrong. "
            "And honestly so: Timothy Kehoe, who had worked on the model, went back and scored it. If we look at "
            "the correlations of what we predicted with what happened, he said, they average about zero."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3), FadeIn(q))
        self.clear_scene()

    def scatter(self):
        n = load("nafta")
        a, s, l_ = np.array(n["actual"]), np.array(n["sobarzo"]), np.array(n["ltp"])
        ax = plane([-15, 25], [-100, 600], center=LEFT * 3.9 + DOWN * 0.3, x_length=5.0, y_length=5.0,
                   xticks=[-10, 0, 10, 20], yticks=[0, 200, 400, 600], xlabel=r"forecast change, \ \%",
                   ylabel=r"actual change, \ \%", font_size=16)
        dots = VGroup(*[Dot(ax.ax.c2p(x, y), radius=0.07, color=PRED) for x, y in zip(s, a)])
        names = VGroup()
        for k in (int(np.argmax(a)), n["industries"].index("Chemicals"), n["industries"].index("Petroleum"),
                  n["industries"].index("Nonelectrical machinery")):
            names.add(label(n["industries"][k].lower(), font_size=15, color=GREY_A).next_to(
                ax.ax.c2p(s[k], a[k]), RIGHT, buff=0.1))
        side = VGroup(
            label(r"21 industries: \ forecast against outcome", font_size=22),
            label(rf"correlation, \ unweighted, \ from the table: \ {signed(n['corr_sobarzo'])}", font_size=22,
                  color=PRED),
            label(r"what the models missed: \ trade grew most in goods \\ that had hardly been traded before",
                  font_size=22, color=HOLD),
            label(rf"Kehoe and coauthors' simple rule, \ from the share of such goods: \\ correlation "
                  rf"{signed(n['corr_ltp'])} unweighted, \ {signed(n['weighted']['ltp'])} weighted", font_size=21,
                  color=CC),
            label(r"a model is only as good as the mechanisms in it: \\ the new-goods margin, \ Parts 35 and 36",
                  font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.45)
        tag = published_tag(r"Kehoe, NAFTA at 20 (Dallas Fed, 2014), table 1", corner=DR, font_size=13)
        with self.voiceover(
            "Here are all twenty-one industries, each forecast against what happened. <bookmark mark='a'/> If "
            "anything, the forecasts point the wrong way: computed from Kehoe's table without weights, the "
            "correlation is about minus nought point four. <bookmark mark='b'/> What the models missed was where new trade comes "
            "from. After a trade agreement, Kehoe and Kim Ruhl found, trade grows most in goods that had hardly "
            "been traded at all before, and the models of 1992 had no way for that to happen. "
            "<bookmark mark='c'/> A simple rule built on that fact, how much of an industry's trade was in such "
            "goods beforehand, does much better than the models did. <bookmark mark='d'/> The lesson is not that "
            "general equilibrium is wrong. It's that a model is only as good as the mechanisms put into it. Parts "
            "thirty-five and thirty-six build trade models with that margin in them."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.05),
                      FadeIn(names), FadeIn(side[0]), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()
