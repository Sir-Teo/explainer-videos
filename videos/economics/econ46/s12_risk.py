from __future__ import annotations

from videos.economics.econ46.common import *  # noqa: F403


class Risk(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Risk", r"How do villages insure themselves, and why does nobody buy rainfall insurance?",
             "Chapter ten. Risk.", lit={1994: r"Townsend", 2013: r"Cole et al.", 2015: r"Cai, de Janvry and Sadoulet"},
             scale=("household", "village"), horizon=("a season",))
        self.idea()
        self.test()
        self.index()
        self.china()

    def idea(self):
        chain = flow_chain([(r"a bad harvest, \\ an illness", LOSS), (r"gifts and loans \\ from neighbours", RISK),
                            (r"consumption \\ barely moves", GAIN), (r"as if insured", RISK)],
                           notes=[r"one household's \\ shock", r"repaid when \\ times are good", r"it follows the \\ "
                                  r"village, \ not \\ the household", r"with no contract"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 0.9)
        eq = MathTex(r"\Delta \log c_{iv t} = \beta\, \Delta \log y_{ivt} + \text{village-year effect} + e_{ivt}",
                     font_size=34, color=THEORY).to_edge(DOWN, buff=1.5)
        el = label(r"full insurance: \ $\beta$ = 0; \ none: \ $\beta$ = 1", font_size=21, color=GREY_A).next_to(
            eq, DOWN, buff=0.25)
        tag = published_tag(tables.RISK_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Poor households face huge risks, a failed harvest, a sick cow, an illness, and almost none of them "
            "have insurance policies. Yet they are not helpless. <bookmark mark='a'/> When one household is hit, "
            "neighbours and relatives send gifts and lend money, <bookmark mark='b'/> repaid when times are good. "
            "<bookmark mark='c'/> If this works, a household's consumption should follow the fortunes of the "
            "village, which nobody can insure against locally, and not its own luck. <bookmark mark='d'/> The "
            "village insures its members, without a single contract. <bookmark mark='e'/> In 1994 Robert Townsend "
            "turned this into a test. Regress the change in a household's consumption on the change in its own "
            "income, holding the village's fortunes fixed with a separate effect for each village and year. With "
            "full insurance the slope is zero; with none, it is one."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), FadeIn(chain.notes[0]), run_time=1.0)
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            vo.wait_until("d")
            self.play(Indicate(chain.boxes[3], color=WHITE))
            vo.wait_until("e")
            self.play(Write(eq), FadeIn(el))
        self.clear_scene()

    def test(self):
        R = load("townsend")
        rows = R["rows"]
        ax = plane([0, 1], [0, 1.05], center=LEFT * 2.0 + DOWN * 0.35, x_length=6.4, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"share of own shocks the village pools \ (planted)", ylabel=r"the estimated slope, $\beta$",
                   xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:.2f}", font_size=14)
        xs = [r_["pooled"] for r_ in rows]
        w = path(ax, xs, [r_["within"] for r_ in rows], RISK, 3.2, smooth=False)
        wd = VGroup(*[dot(ax, r_["pooled"], r_["within"], RISK, 0.07) for r_ in rows])
        raw = path(ax, xs, [r_["raw"] for r_ in rows], LOSS, 2.6, smooth=False)
        rd = VGroup(*[dot(ax, r_["pooled"], r_["raw"], LOSS, 0.06) for r_ in rows])
        M = R["main"]
        side = VGroup(
            label(rf"the Island: \ three villages, \\ {TRUTH['risk']['households']} households, \ ten years",
                  font_size=18, color=WHITE),
            label(r"gold: \ Townsend's slope, \\ village-years held fixed", font_size=18, color=RISK),
            label(r"red: \ without them, \\ village shocks leak in", font_size=18, color=LOSS),
            label(rf"at 85\% pooling: \\ {M['within']:.2f} against {M['raw']:.2f}", font_size=18, color=E.ACCENT),
            label(r"India's villages: \\ near zero, \ but not zero", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "On the Island, the share of a household's own shocks that its village absorbs is planted, so the test "
            "can be checked. <bookmark mark='a'/> In gold, Townsend's slope, across villages that pool none, a "
            "quarter, a half, eighty-five percent or all of their members' shocks. It recovers one minus the "
            "pooled share exactly. <bookmark mark='b'/> In red, the same regression without the village-year "
            "effects. Now the shocks that hit the whole village, which no neighbour can insure, show up as a lack "
            "of insurance. <bookmark mark='c'/> With eighty-five percent pooling, the right slope is "
            f"{M['within']:.2f}, the wrong one {M['raw']:.2f}. <bookmark mark='d'/> In three villages in semi-arid "
            "India, Townsend rejected full insurance, but found consumption much closer to it than to none: a "
            "good benchmark, with holes, for the poorest and for the largest shocks."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(w), FadeIn(wd), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(raw), FadeIn(rd), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def index(self):
        I = load("index")
        Tr = TRUTH["index"]
        Tk = tables.RISK_46.data
        ax = plane([0, 0.5], [0, 1.05], center=LEFT * 2.0 + DOWN * 0.35, x_length=6.6, y_length=4.6,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"basis risk: \ chance the gauge misses the farm's drought",
                   ylabel=r"the best cover, \ share of the loss", xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.2f}",
                   font_size=14)
        cs = VGroup(path(ax, I["basis"], I["fair"], GAIN, 3.0), path(ax, I["basis"], I["full"], RISK, 3.0),
                    path(ax, I["basis"], I["trust"], LOSS, 3.2))
        side = VGroup(
            label(rf"a drought one year \\ in {round(1 / Tr['p_drought'])}, \ half the harvest", font_size=18,
                  color=WHITE),
            label(r"green: \ priced fairly, \\ fully trusted", font_size=18, color=GAIN),
            label(rf"gold: \ a premium {100 * Tr['load']:.0f}\% \\ above the expected payout", font_size=18,
                  color=RISK),
            label(rf"red: \ and the insurer \\ trusted to pay {100 * Tr['trust']:.0f}\%", font_size=18, color=LOSS),
            label(rf"India: \ take-up {Tk['take_lo']}--{Tk['take_hi']}\% \\ at market prices", font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "What the village cannot insure is the shock that hits everyone at once, like a drought. That is what "
            "rainfall insurance is for: it pays when a rain gauge records a drought, so no claims adjuster has to "
            "visit, and nobody can cheat. Development economists were enthusiastic. Farmers were not. <bookmark "
            f"mark='a'/> On the Island, a drought comes one year in {round(1 / Tr['p_drought'])} and takes half the "
            "harvest. <bookmark mark='b'/> Priced fairly and trusted, a risk-averse farmer buys full cover when "
            "the gauge is perfect, and less as basis risk grows: the chance that the farm suffers a drought the "
            "gauge does not record, or the gauge pays when the farm is fine. <bookmark mark='c'/> Add a premium "
            f"{100 * Tr['load']:.0f} percent above the expected payout, and demand falls. <bookmark mark='d'/> "
            f"And if farmers believe the insurer will pay only {100 * Tr['trust']:.0f} percent of the time, the "
            "cover they want falls to nothing at high basis risk. <bookmark mark='e'/> In India, Shawn Cole and his "
            f"coauthors found take-up of {Tk['take_lo']} to {Tk['take_hi']} percent at market prices, sensitive to "
            "the price and to whether farmers trusted the seller. Insurance is a promise, and promises from "
            "strangers are worth less."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            for mk, k in zip("bcd", range(3)):
                vo.wait_until(mk)
                self.play(Create(cs[k]), FadeIn(side[k + 1]), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def china(self):
        C = load("insure")
        D = C["default"]
        Tk = tables.RISK_46.data
        ax = plane([0, 2], [0, 0.7], center=LEFT * 2.6 + DOWN * 0.4, x_length=4.6, y_length=4.4, xticks=[],
                   yticks=[0, 0.2, 0.4, 0.6], ylabel=r"share who bought", yfmt=lambda v: f"{100 * v:.0f}\\%",
                   font_size=14)
        bars = VGroup()
        for i, (nm, v, col) in enumerate(((r"default: \\ not to buy", D["zero"], CONTROL),
                                          (r"default: \\ to buy", D["one"], RISK))):
            p0, p1 = ax.ax.c2p(0.5 + i - 0.3, 0), ax.ax.c2p(0.5 + i + 0.3, v)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(nm, font_size=15, color=WHITE).next_to(r, DOWN, buff=0.1),
                            label(rf"{100 * v:.0f}\%", font_size=17, color=WHITE).next_to(r, UP, buff=0.06)))
        side = VGroup(
            label(rf"rice farmers in rural China: \\ {C['n']:,} households, \\ {C['villages']} villages"
                  .replace(",", "{,}"), font_size=19, color=WHITE),
            label(r"the default at the end \\ of the session, \ at random", font_size=19, color=TRIAL),
            label(rf"+{100 * D['diff']:.0f} points \ (s.e. {100 * D['se']:.0f})", font_size=21, color=E.ACCENT),
            label(rf"and one more friend trained \\ in insurance did as much as \\ a {Tk['friend_premium']}\% cut in "
                  r"the premium", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"Cai, \ de Janvry and Sadoulet (2015), \ via the R package causaldata 0.1.4", corner=DL,
                       font_size=12)
        with self.voiceover(
            "Jing Cai, Alain de Janvry and Elisabeth Sadoulet studied a new weather insurance for rice farmers in "
            f"rural China. <bookmark mark='a'/> Here are {C['n']:,} of their households, from {C['villages']} "
            "villages. <bookmark mark='b'/> At the end of each information session, farmers were given a default "
            "at random: either they would be signed up unless they said no, or not signed up unless they said "
            f"yes. <bookmark mark='c'/> Where the default was to buy, {100 * D['one']:.0f} percent bought; where "
            f"it was not, {100 * D['zero']:.0f}: a difference of {100 * D['diff']:.0f} points, with a standard "
            f"error of {100 * D['se']:.0f}, computed here. Part forty-five's defaults, in a Chinese village. "
            "<bookmark mark='d'/> Their main finding was about networks: for a farmer not trained directly, one "
            f"more friend who had been through the intensive session raised take-up as much as a "
            f"{Tk['friend_premium']} percent cut in the premium. People learn what insurance is from people they "
            "trust."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), *[FadeIn(b[1]) for b in bars], run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(*[GrowFromEdge(b[0], DOWN) for b in bars], *[FadeIn(b[2]) for b in bars], FadeIn(side[2]),
                      run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
