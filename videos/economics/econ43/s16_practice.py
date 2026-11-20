from __future__ import annotations

from videos.economics.econ43.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ merger review", r"Who decides whether a merger may go ahead, and how?",
             "Chapter fourteen. In practice: merger review.", lit={2008: r"MillerCoors", 2023: r"Merger Guidelines"},
             scale=("firm", "market"), horizon=("a year",))
        self.screens()
        self.upp()
        self.called()
        self.who()

    def screens(self):
        Mg = tables.MERGER_2023.data
        G = load("playit")
        M = load("merger")
        rows = VGroup(
            label(rf"presumed harmful \ (2023): \ Herfindahl above {Mg['hhi']:,} and a rise above {Mg['delta']}; \ "
                  rf"or a firm above {Mg['share']}\% with a rise above {Mg['delta']}", font_size=20, color=LOSS),
            label(rf"before \ (2010--2023): \ above {Mg['hhi2010']:,} with a rise above {Mg['delta2010']}",
                  font_size=19, color=GREY_A),
            label(rf"the game's X: \ {G['x']['hhi1']:,.0f}, \ +{G['x']['dhhi']:,.0f}; \ \ Y: \ "
                  rf"{G['y']['hhi1']:,.0f}, \ +{G['y']['dhhi']:,.0f}: \ both presumed harmful", font_size=20,
                  color=NEST[2]),
            label(rf"the aisle's merger: \ {M['hhi1']:,.0f}, \ +{M['dhhi']:,.0f}: \ presumed harmful; \ simulated "
                  rf"prices +{100 * M['dp_merged']:.1f}\%", font_size=20, color=PRICE),
            label(r"the index starts the conversation; \ diversion, \ margins and simulation finish it", font_size=21,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.1)
        head = label(r"the first screen: \ concentration", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(tables.MERGER_2023.tag, corner=DR, font_size=11)
        with self.voiceover(
            "In America, mergers above a certain size must be notified to the Federal Trade Commission and the "
            "Department of Justice, which can sue to stop them. Their guidelines begin with concentration. "
            "<bookmark mark='a'/> Since December 2023, a merger is presumed to lessen competition if it leaves a "
            f"Herfindahl index above {Mg['hhi']:,} and raises it by more than {Mg['delta']} points, or creates a firm "
            f"with more than {Mg['share']} percent of the market and raises the index by more than {Mg['delta']}. "
            "<bookmark mark='b'/> Those are the thresholds of 1982, restored; from 2010 they were higher. "
            "<bookmark mark='c'/> Both of the game's mergers trip the screen, though one raised prices ten times "
            "as much as the other. <bookmark mark='d'/> The Island aisle's merger trips it too, with simulated "
            f"prices {say_pct(M['dp_merged'], 1)} higher. <bookmark mark='e'/> The presumption can be rebutted, and "
            "the argument then turns to the tools of this part: diversion ratios, margins and simulation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def upp(self):
        G = load("playit")
        P = TRUTH["playit"]
        D = np.array(G["diversion"])
        p, mc = np.array(G["p0"]), np.array(G["mc"])
        e = 0.10
        ux = D[3][4] * (p[4] - mc[4]) - e * mc[3]
        uy = D[0][2] * (p[2] - mc[2]) - e * mc[0]
        eq = MathTex(r"\mathrm{UPP}_1 \;=\;", r"D_{12}\,(p_2 - c_2)", r"\;-\;", r"E_1\, c_1", font_size=46)
        eq[1].set_color(LOSS)
        eq[3].set_color(GAIN)
        eq.to_edge(UP, buff=0.8)
        notes = VGroup(
            label(r"the profit a price rise now keeps: \\ diversion to the partner \\ times the partner's margin",
                  font_size=18, color=LOSS).next_to(eq[1], DOWN, buff=0.5),
            label(r"the credit for \\ cost savings, \\ a share $E_1$ of cost", font_size=18,
                  color=GAIN).next_to(eq[3], DOWN, buff=0.5),
        )
        rows = VGroup(
            label(rf"X, \ {P['names'][3]}: \ {D[3][4]:.2f} $\times$ {p[4] - mc[4]:.2f} $-$ 0.10 $\times$ "
                  rf"{mc[3]:.2f} = {ux:+.3f}: \ upward pressure", font_size=20, color=NEST[2]),
            label(rf"Y, \ {P['names'][0]}: \ {D[0][2]:.2f} $\times$ {p[2] - mc[2]:.2f} $-$ 0.10 $\times$ "
                  rf"{mc[0]:.2f} = {uy:+.3f}: \ {'upward pressure' if uy > 0 else 'none'}", font_size=20,
                  color=NEST[0]),
            label(r"no market to define, \ no full demand system: \ a diversion ratio and a margin", font_size=21,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"Farrell and Shapiro (2010); \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "Between the index and a full simulation sits a test from Joseph Farrell and Carl Shapiro, upward "
            "pricing pressure. <bookmark mark='a'/> When product one's owner buys product two, raising one's price "
            "now keeps the profit on the sales diverted to two: the diversion ratio times two's margin. "
            "<bookmark mark='b'/> Against that, credit the merger with some saving in one's cost, say ten percent. "
            f"<bookmark mark='c'/> For merger X: {D[3][4]:.2f} times {p[4] - mc[4]:.2f}, less a tenth of "
            f"{mc[3]:.2f}, is positive, so prices are pushed up. <bookmark mark='d'/> For merger Y the pressure is "
            f"{'smaller' if uy > 0 else 'gone'}: {say_num(uy, 3)}. <bookmark mark='e'/> The test needs no market "
            "definition and no full demand system, only diversion ratios and margins, which is why agencies use it "
            "as a screen."
        ) as vo:
            self.play(Write(eq), FadeIn(tag), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), Indicate(eq[1], color=WHITE, scale_factor=1.05))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), Indicate(eq[3], color=WHITE, scale_factor=1.05))
            for mk, r_ in zip("cde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["millercoors_2008"]
        Mc = tables.MILLERCOORS.data
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=20)
        tag = published_tag(tables.MILLERCOORS.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In June 2008 the Department of Justice let SABMiller and Molson Coors "
            "combine their American brewing in a joint venture, MillerCoors. After an eight-month investigation it "
            "judged the venture not likely to lessen competition substantially, and its cost savings substantial "
            "and credible. <bookmark mark='b'/> The savings were real. Coors beer could now be brewed in Miller's "
            f"plants, nearer its drinkers, cutting the average shipping distance by {Mc['miles']} miles, and Orley "
            "Ashenfelter, Daniel Hosken and Matthew Weinberg found that the savings offset, on average, the roughly "
            f"{Mc['concentration']:.0f} percent that higher concentration added to prices. But prices of MillerCoors "
            "and of Anheuser-Busch, its rival, jumped together soon after, and Nathan Miller and Weinberg estimate "
            f"them {Mc['lo']} to {Mc['hi']} percent above what competition with those savings would give, "
            "consistent with the two leaders coordinating. <bookmark mark='c'/> The verdict: partly right. The "
            "review weighed the savings against each firm's own incentive to raise prices; the risk that fewer, "
            "larger rivals would follow one another's prices was harder to put a number on."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()

    def who(self):
        rows = VGroup(
            label(r"agency economists: \ the FTC's Bureau of Economics, \ the Justice Department's Economic Analysis "
                  r"Group, \ Europe's competition directorate, \ Britain's CMA", font_size=19, color=DEMAND),
            label(r"consultancies and expert witnesses: \ estimate diversion, \ simulate mergers, \ testify",
                  font_size=19, color=PRICE),
            label(r"in industry: \ pricing and strategy teams estimate the same demand systems \ (Part 59)",
                  font_size=19, color=GAIN),
            label(r"retrospectives: \ studies of mergers after the fact keep the simulations honest",
                  font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(DOWN * 0.1)
        head = label(r"the people who do this", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Who does this work? <bookmark mark='a'/> Economists at the agencies: the Federal Trade Commission's "
            "Bureau of Economics, the Justice Department's Economic Analysis Group, the European Commission's "
            "competition directorate, Britain's Competition and Markets Authority. <bookmark mark='b'/> "
            "Consultancies and expert witnesses on both sides of a case, who estimate diversion, simulate mergers "
            "and defend their numbers in court. <bookmark mark='c'/> In industry, pricing and strategy teams "
            "estimate the same demand systems to set prices and plan products, the subject of Part fifty-nine. "
            "<bookmark mark='d'/> And academics who study mergers after the fact, like the beer studies, which keep "
            "the simulations honest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
