from __future__ import annotations

from videos.economics.econ59.common import *  # noqa: F403


class Regulated(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Regulated prices", r"Where a merger cannot be stopped because the monopoly is natural, \ "
             r"who sets the price?", "Chapter thirteen. Regulated prices.",
             lit={1944: r"Hope Natural Gas", 1983: r"Littlechild's RPI--X"}, scale=("firm", "nation"),
             horizon=("a year", "a decade"))
        self.rate_case()
        self.cap()
        self.access()

    def rate_case(self):
        R = load("regulated")["rate"]
        parts = [(r"operating costs", R["om"], SHOPS), (r"depreciation", R["depreciation"], ALDER),
                 (r"taxes", R["taxes"], CEDAR), (rf"{100 * R['allowed']:.0f}\% on a rate base of "
                                                 rf"{R['rate_base']:.0f}", R["return"], BIRCH)]
        bars, labs = VGroup(), VGroup()
        y0 = -2.4
        scale = 4.4 / R["requirement"]
        for t, v, c in parts:
            h = v * scale
            bars.add(Rectangle(width=1.6, height=h, fill_color=c, fill_opacity=0.85, stroke_width=1,
                               stroke_color=BLACK).move_to([-4.0, y0 + h / 2, 0]))
            labs.add(label(rf"{t}: \ {v:.0f}", font_size=18, color=c).next_to(bars[-1], RIGHT, buff=0.25))
            y0 += h
        tot = label(rf"revenue requirement: \ {R['requirement']:.0f}", font_size=22, color=WHITE).next_to(
            bars, UP, buff=0.25)
        head = label(r"cost of service: \ the rate case", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.45)
        nat = label(r"one water main, \ one grid: \ room for one firm only", font_size=21, color=GREY_A).next_to(
            head, DOWN, buff=0.25)
        side = VGroup(
            label(rf"price $=$ requirement $\div$ volume $=$ {R['requirement']:.0f} $\div$ 100 $=$ "
                  rf"\${R['price']:.2f}", font_size=21, color=WHITE),
            label(r"the fight is over the allowed return: \\ `commensurate with returns on investments in other "
                  r"enterprises \\ having corresponding risks' \ (Hope, 1944)", font_size=19, color=REG),
            label(r"and over the rate base: \ was each investment prudent?", font_size=19, color=REG),
            label(r"the catch \ (Part 10): \ a return above the cost of capital \\ rewards too much capital, "
                  r"\ and every saving goes to customers", font_size=19, color=CARTEL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = island_tag(r"the Island: \ the water company, \ one rate case", corner=DL, font_size=12)
        with self.voiceover(
            "Some markets have room for one firm only: one water main, one power grid. There the economics of "
            "merger review gives way to regulation, and economists testify in rate cases. <bookmark mark='a'/> "
            "The classic method is cost of service. The Island's water company may recover its operating costs, "
            "depreciation and taxes, <bookmark mark='b'/> plus an allowed return on the capital it has invested, "
            f"its rate base: seven percent of {R['rate_base']:.0f}. <bookmark mark='c'/> The total is the revenue "
            f"requirement, {R['requirement']:.0f}, and the price is that divided by the volume sold. <bookmark "
            "mark='d'/> The hearings are about the allowed return, which American courts since the Hope Natural Gas "
            "case of 1944 have said must be commensurate with returns on investments of corresponding risk, and "
            "about whether "
            "each investment was prudent. <bookmark mark='e'/> Part ten showed the catch: if the allowed return "
            "beats the cost of capital, the firm uses too much capital; and since every saving is passed straight "
            "to customers at the next case, the firm has little reason to look for one."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head), FadeIn(nat))
            vo.wait_until("a")
            self.play(FadeOut(nat), run_time=0.5)
            for k in range(3):
                self.play(GrowFromEdge(bars[k], DOWN), FadeIn(labs[k]), run_time=0.6)
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[3], DOWN), FadeIn(labs[3]))
            vo.wait_until("c")
            self.play(FadeIn(tot), FadeIn(side[0]))
            vo.wait_until("d")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def cap(self):
        Cp = load("regulated")["cap"]
        t = np.array(Cp["t"])
        ax = plane([0, 15], [0.8, 1.4], center=LEFT * 2.6 + DOWN * 0.4, x_length=6.6, y_length=4.6,
                   xticks=[0, 5, 10, 15], yticks=[0.8, 1.0, 1.2, 1.4], xlabel=r"year",
                   ylabel=r"price and unit cost, \ in money of the day", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        pcos = path(ax, t, Cp["price_cos"], GREY_B, 2.6, smooth=False)
        ccap = path(ax, t, Cp["cost_cap"], SAVE, 2.2, smooth=False)
        pcap = path(ax, t, Cp["price_cap"], REG, 3.0, smooth=False)
        resets = VGroup(*[vline(ax, x, 0.8, 1.4, GREY_C, 1.2) for x in (5, 10, 15)])
        key = VGroup(label(r"grey: \ cost of service \ (price $=$ cost, \ costs fall 1\% a year)", font_size=15,
                           color=GREY_B),
                     label(r"green: \ cost under the cap \ (falls 4\% a year)", font_size=15, color=SAVE),
                     label(r"blue: \ the capped price, \ RPI $-$ X, \ reset every 5 years", font_size=15,
                           color=REG)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax.ax.c2p(0, 1.4),
                                                                                         RIGHT, buff=0.1).shift(
            DOWN * 0.3)
        side = VGroup(
            MathTex(r"P_t = P_{t-1}\,(1 + \text{RPI}_t - X)", font_size=34, color=REG),
            label(rf"inflation {100 * Cp['rpi']:.0f}\%, \ X $=$ {100 * Cp['X']:.0f}\%", font_size=20, color=GREY_A),
            label(r"between resets the firm keeps what it saves: \\ the gap between blue and green", font_size=20,
                  color=SAVE),
            label(r"at each reset the price drops to cost: \\ customers get the savings, \ later", font_size=20,
                  color=REG),
            label(rf"after 15 years, \ in real terms: \ {Cp['real_cap_end']:.2f} under the cap, \ "
                  rf"{Cp['real_cos_end']:.2f} under cost of service", font_size=19, color=E.ACCENT),
            label(r"(the effort each regime induces is assumed, \ not derived)", font_size=16, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        if side.width > 5.6:
            side.width = 5.6
            side.to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Littlechild, \ Regulation of British Telecommunications' Profitability (1983)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "In 1983 Stephen Littlechild proposed a different deal for Britain's soon-to-be-privatized telephone "
            "company: cap the price, not the profit. <bookmark mark='a'/> The price may rise each year by "
            "inflation minus X, a number the regulator sets for five years at a time. <bookmark mark='b'/> Between "
            "resets, whatever the firm saves it keeps, so it has every reason to save. On the Island, assume that "
            "under the cap the water company's costs fall four percent a year in real terms, against one percent "
            "under cost of service. <bookmark mark='c'/> The capped price falls in real terms, and the firm's margin "
            "grows as its costs fall faster. <bookmark mark='d'/> At each reset the regulator brings the price down "
            "to cost, and customers collect the savings, later rather than sooner. <bookmark mark='e'/> After "
            f"fifteen years the real price is {Cp['real_cap_end']:.2f} under the cap against "
            f"{Cp['real_cos_end']:.2f} under cost of service. The numbers hang on the effort each regime is "
            "assumed to induce, which is the part a regulator has to estimate, and the next X is argued over by "
            "economists on both sides, as rate cases were."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(key), FadeIn(resets))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(pcos), Create(ccap), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(pcap), FadeIn(side[2]), run_time=1.8)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), FadeIn(side[5]))
        self.clear_scene()

    def access(self):
        A = load("regulated")["ecpr"]
        chain = flow_chain([(r"the incumbent's \\ network", REG), (r"its retail \\ service", ALDER),
                            (r"customers", WHITE)], box_w=2.6, box_h=1.1, buff=0.9, font_size=20,
                           notes=[rf"cost \${A['network_cost']:.0f}", rf"cost \${A['retail_cost']:.0f}",
                                  rf"pay \${A['retail_price']:.0f}"], note_size=17).move_to(UP * 1.8)
        rows = VGroup(
            label(r"an entrant rents the network and sells its own retail service:", font_size=21, color=GREY_A),
            MathTex(rf"\text{{access}} = \underbrace{{{A['network_cost']:.0f}}}_{{\text{{the network's cost}}}} + "
                    rf"\underbrace{{{A['margin']:.0f}}}_{{\text{{the margin the incumbent loses}}}} = "
                    rf"{A['access']:.0f}", font_size=32, color=BIRCH),
            label(rf"the entrant profits only if its retail cost is below \${A['entrant_break_even']:.0f}: \ "
                  r"only if it is more efficient", font_size=21, color=SAVE),
            label(r"the objection: \ the rule protects the incumbent's monopoly margin; \\ many regulators price "
                  r"access at cost instead", font_size=19, color=CARTEL),
        ).arrange(DOWN, buff=0.35).next_to(chain, DOWN, buff=0.6)
        tag = island_tag(r"the Island: \ the telephone company; \ the efficient component pricing rule",
                         corner=DL, font_size=12)
        with self.voiceover(
            "One more regulated price: access. <bookmark mark='a'/> The Island's telephone company owns the "
            f"network, which costs {A['network_cost']:.0f} dollars a customer, and a retail service costing "
            f"{A['retail_cost']:.0f}; customers pay {A['retail_price']:.0f}. A rival wants to rent the network and "
            "sell its own service. What should it pay? <bookmark mark='b'/> The efficient component pricing rule, "
            "associated with William Baumol and Robert Willig, says: the network's cost plus the margin the "
            f"incumbent loses on each customer it gives up, {A['access']:.0f} dollars. <bookmark mark='c'/> Then the "
            f"entrant profits only if its retail service costs less than {A['entrant_break_even']:.0f}, so only "
            "more efficient rivals enter. <bookmark mark='d'/> The objection is plain: the rule hands the "
            "incumbent its monopoly margin on every customer it loses, and competition never touches it. Many "
            "regulators price access at cost instead, and accept less efficient entrants as the price of "
            "competition. Which rule is right depends on whether the retail margin is a reward for something, "
            "or just a monopoly's rent."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(chain.boxes), FadeIn(chain.arrows), FadeIn(chain.notes), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
