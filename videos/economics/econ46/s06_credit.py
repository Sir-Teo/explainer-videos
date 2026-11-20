from __future__ import annotations

from videos.economics.econ46.common import *  # noqa: F403


class Credit(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Credit", r"Why does the moneylender charge so much, and does microcredit help?",
             "Chapter five. Credit.", lit={1990: r"Aleem", 2015: r"Banerjee, Karlan and Zinman", 2019: r"Meager"},
             scale=("household", "village"), horizon=("a year",))
        self.lender()
        self.groups()
        self.trial()
        self.quantiles()
        self.six()

    def lender(self):
        M = load("lender")
        Ta = tables.CREDIT_46.data
        parts = [(r"the lender's \\ own cost of money", M["cost_of_funds"], CONTROL),
                 (r"covering \\ defaults", M["from_default"], LOSS),
                 (r"screening and \\ chasing loans", M["from_monitoring"], CREDIT)]
        bars = VGroup()
        x = -4.6
        scale = 9.0 / 0.6
        for nm, v, col in parts:
            w = v * scale
            r = Rectangle(width=w, height=0.8, stroke_color=BLACK, stroke_width=1.5, fill_color=col,
                          fill_opacity=0.85).move_to(np.array([x + w / 2, 0.6, 0]))
            bars.add(VGroup(r, label(rf"{nm} \\ {100 * v:.0f} points", font_size=16, color=WHITE).next_to(r, DOWN,
                                                                                                        buff=0.15)))
            x += w
        total = label(rf"= {100 * M['rate']:.0f}\% a year", font_size=28, color=E.ACCENT)
        total.next_to(bars, RIGHT, buff=0.3).shift(UP * 0.45)
        eq = MathTex(r"(1+i)(1-p) = 1 + r + m", font_size=40, color=THEORY).to_edge(UP, buff=1.0)
        eql = label(rf"$i$: \ the rate; \ $p$ = {M['default']:.2f}: \ the share that default; \ $r$ = "
                    rf"{M['cost_of_funds']:.2f}: \ the lender's cost of funds; \ $m$ = {M['monitoring']:.2f}: \ "
                    r"screening and collection", font_size=17, color=GREY_A).next_to(eq, DOWN, buff=0.25)
        aleem = label(rf"Aleem, \ 1990: \ {Ta['lenders']} moneylenders in Sindh, \ Pakistan, \ charging about "
                      rf"{Ta['rate']}\% a year, \\ about what their lending cost them", font_size=19,
                      color=GREY_A).to_edge(DOWN, buff=0.6)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "In villages, moneylenders often charge rates that look like exploitation. In 1990 Irfan Aleem studied "
            f"{Ta['lenders']} of them around the market town of Chambar in Pakistan. They charged about "
            f"{Ta['rate']} percent a year on average. <bookmark mark='a'/> Where does a rate like that come from? A "
            "lender who breaks even must get back, from the borrowers who repay, the cost of its own money plus the "
            "cost of finding good borrowers and chasing the rest. <bookmark mark='b'/> On the Island the lender's "
            f"own money costs {100 * M['cost_of_funds']:.0f} percent. <bookmark mark='c'/> "
            f"{100 * M['default']:.0f} percent of loans are never repaid, which adds "
            f"{100 * M['from_default']:.0f} points. <bookmark mark='d'/> And screening and collection, the "
            f"lender's time and travel, add {100 * M['from_monitoring']:.0f} more: "
            f"{100 * M['rate']:.0f} percent in all. <bookmark mark='e'/> Aleem found his lenders' rates were close "
            "to what their lending cost them. The high price of credit is mostly the high cost of information, not "
            "monopoly profit."
        ) as vo:
            self.play(FadeIn(tag), Write(eq), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(eql))
            for mk, b in zip("bcd", bars):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[0], LEFT), FadeIn(b[1]))
            self.play(FadeIn(total))
            vo.wait_until("e")
            self.play(FadeIn(aleem))
        self.clear_scene()

    def groups(self):
        chain = flow_chain([(r"lend to groups \\ of five", CREDIT), (r"each guarantees \\ the others", CREDIT),
                            (r"neighbours screen \\ and watch", GAIN), (r"repayment \\ without collateral", GAIN)],
                           notes=[r"mostly women, \\ meeting weekly", r"joint liability", r"they know who is \\ "
                                  r"reliable", r"rates below the \\ moneylender's"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 0.5)
        foot = label(r"Muhammad Yunus began lending in 1976; \ he and the Grameen Bank shared the 2006 Nobel Peace "
                     r"Prize", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "If information is the problem, who has it? The neighbours. <bookmark mark='a'/> In 1976 Muhammad Yunus "
            "began lending to poor villagers in Bangladesh, and the Grameen Bank he founded lent to small groups, "
            "mostly of women, meeting every week. "
            "<bookmark mark='b'/> In the classic design each member is liable for the others' loans. <bookmark "
            "mark='c'/> So the group chooses its members, and watches them, using what neighbours know and a bank "
            "does not. <bookmark mark='d'/> Repayment was high without any collateral, and the rates, though high by "
            "a bank's standards, were below the moneylender's. Microcredit spread across the world, with the promise "
            "that it would lift its borrowers out of poverty. That is a claim an experiment can test."
        ) as vo:
            self.play(FadeIn(foot), FadeIn(chain.boxes[0]))
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
        self.clear_scene()

    def trial(self):
        C = load("credit")
        Tr = TRUTH["credit"]
        rows = VGroup(
            label(rf"villages drawn at random to get a microlender, \ at {100 * Tr['interest']:.0f}\% a year",
                  font_size=23, color=TRIAL),
            label(rf"{100 * Tr['share_high']:.0f}\% of businesses: \ a return of {100 * Tr['r_high']:.0f}\% a year "
                  r"on more capital", font_size=23, color=ESCAPE),
            label(rf"the rest: \ {100 * Tr['r_low']:.0f}\% a year, \ below the interest rate", font_size=23,
                  color=TRAP),
            label(rf"take-up: \ {100 * C['take_up']:.0f}\% of those offered borrow", font_size=23, color=CREDIT),
            label(rf"average effect on profits: \ +{C['itt']:.1f} \ (s.e. {C['itt_se']:.1f}) \ on a mean of "
                  rf"{C['mean_control']:.0f}", font_size=23, color=WHITE),
            label(rf"per borrower: \ +{C['tot']:.1f}", font_size=23, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).move_to(DOWN * 0.1)
        head = label(r"a randomized microlender, \ on the Island", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is the test, run on the Island. <bookmark mark='a'/> A microlender opens in villages drawn at "
            f"random, charging {100 * Tr['interest']:.0f} percent a year. <bookmark mark='b'/> In the planted "
            f"truth, {100 * Tr['share_high']:.0f} percent of the villagers' businesses would earn "
            f"{100 * Tr['r_high']:.0f} percent a year on more capital, <bookmark mark='c'/> and the rest only "
            f"{100 * Tr['r_low']:.0f}, less than the loan costs. <bookmark mark='d'/> "
            f"{100 * C['take_up']:.0f} percent of the people offered a loan take one: the high-return businesses, "
            "and some others who borrow to buy a roof or get through a bad month. <bookmark mark='e'/> The average "
            f"effect on profits is {C['itt']:.1f} on a mean of {C['mean_control']:.0f}, about "
            f"{100 * C['itt'] / C['mean_control']:.0f} percent. <bookmark mark='f'/> Per borrower, "
            f"{C['tot']:.1f}. Modest. And yet a few businesses are doing very well."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0], shift=RIGHT * 0.1))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.03))
            for mk, r_ in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def quantiles(self):
        C = load("credit")
        qs = 100 * np.array(C["qs"])
        ax = plane([0, 100], [-10, 40], center=LEFT * 1.8 + DOWN * 0.35, x_length=8.0, y_length=4.8,
                   xticks=[0, 25, 50, 75, 100], yticks=[-10, 0, 10, 20, 30, 40],
                   xlabel=r"percentile of profits", ylabel=r"treated minus control, \ at that percentile",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        zero = DashedLine(ax.ax.c2p(0, 0), ax.ax.c2p(100, 0), color=GREY_B, stroke_width=1.6)
        bd = band(ax, qs, C["qte_lo"], C["qte_hi"], CREDIT, 0.25)
        ln = path(ax, qs, C["qte"], CREDIT, 3.2)
        side = VGroup(
            label(r"quantile treatment \\ effects", font_size=19, color=WHITE),
            label(r"shaded: \ 95\% bootstrap \\ band", font_size=18, color=CREDIT),
            label(r"most of the distribution: \\ no change", font_size=18, color=GREY_A),
            label(r"the top: \ large gains, \\ for the businesses \\ that could use capital", font_size=18,
                  color=ESCAPE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "An average hides where the effect is. <bookmark mark='a'/> Compare the whole distribution of profits "
            "in villages with the lender against villages without it, percentile by percentile: the median against "
            "the median, the ninetieth percentile against the ninetieth. <bookmark mark='b'/> The shading is a "
            "ninety-five percent band from resampling households. <bookmark mark='c'/> Over most of the "
            "distribution, nothing changes: the band includes zero. <bookmark mark='d'/> At the top, large gains. "
            "Microcredit is not useless and not transformative; it works for the few businesses with somewhere "
            "productive to put the money. The real studies found exactly this shape."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(zero), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(ln), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(bd), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def six(self):
        Tc = tables.CREDIT_46.data
        cards = point_cards([
            (r"six trials", rf"{Tc['countries']} countries, \ from \\ Bosnia to Mongolia: \\ modestly positive, \\ "
                            r"not transformative", CREDIT),
            (r"pooled", rf"Meager, \ 2019: \ small \\ effects; \ about {Tc['meager_noise']}\% \\ of the spread "
                        r"across \\ sites is noise", HOLD),
            (r"the top tail", r"gains for existing, \\ high-return \\ businesses", ESCAPE),
            (r"the puzzle", rf"grants to firms earn \\ {Tc['sl_lo']}--{Tc['sl_hi']}\% a month \\ in Sri Lanka: \\ "
                            r"chapter fourteen", POOR),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"what the experiments found", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.CREDIT_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "In 2015 the American Economic Journal published six randomized evaluations of microcredit together, "
            "from Bosnia, Ethiopia, India, Mexico, Mongolia and Morocco. <bookmark mark='a'/> Abhijit Banerjee, "
            "Dean Karlan and Jonathan Zinman summed them up: effects modestly positive, but not transformative. "
            "<bookmark mark='b'/> Rachael Meager pooled seven trials with a hierarchical model and reached the "
            f"same conclusion, adding that about {Tc['meager_noise']} percent of the differences between sites was "
            "just noise, which means the trials agree more than they seem to. <bookmark mark='c'/> The gains were "
            "concentrated among people who already ran businesses. <bookmark mark='d'/> Which leaves a puzzle. When "
            "researchers simply gave cash grants to small firms in Sri Lanka, at random, the firms earned "
            f"{Tc['sl_lo']} to {Tc['sl_hi']} percent a month on it. If capital is that productive, why does credit "
            "do so little? The answer, for the most part, is that the average borrower is not the average grant "
            "recipient, and that returns vary enormously between firms. Chapter fourteen's first dial collects them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Circumscribe(cards.cards[0], color=WHITE, buff=0.05))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
