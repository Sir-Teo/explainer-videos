from __future__ import annotations

from videos.economics.econ68.common import *  # noqa: F403


class Model(VoiceoverScene):
    def construct(self):
        card(self, 7, r"The smallest model", r"What is the least theory needed to turn these estimates into a "
             r"policy answer?", "Chapter seven. The smallest model.", lit={1963: "Vickrey"}, scale=("city",),
             horizon=("a year",))
        self.pieces()
        self.curve()
        self.externality()

    def pieces(self):
        M = load("model")
        eqs = VGroup(
            MathTex(r"T(V) = T_0\,\big(1 + a\,v^{b}\big)", font_size=40),
            MathTex(r"e \;=\; \frac{d\ln T}{d\ln V} \;=\; \frac{" + f"{-100 * M['dlnT']:.1f}" + r"\%}{"
                    + f"{-100 * M['dlnV']:.1f}" + r"\%} \;=\; " + f"{M['e_tv']:.2f}", font_size=36, color=BUS),
            MathTex(r"V = A\,P^{\eta}, \quad P = \text{toll} + \text{value of time}\times T + \text{other costs}",
                    font_size=34, color=TOLL),
            MathTex(r"\eta = " + f"{M['eta']:.2f}".replace("-", "{-}"), font_size=36, color=TOLL),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.7)
        notes = VGroup(
            label(r"time per trip rises with traffic: \ the Bureau of Public Roads' curve, \ $b = 4$", font_size=18,
                  color=GREY_A),
            label(rf"assumed: \ {ASSUME['miles']:.0f} miles in the zone at {ASSUME['mph']:.0f} mph, \ time worth "
                  rf"\${ASSUME['vot']:.0f} an hour, \ other costs \${ASSUME['other']:.0f} a trip", font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.75)
        tag = published_tag(r"Vickrey (1963); \ Part 15; \ the value of time: \ Part 58 (half the wage, \ DOT)",
                            corner=DL, font_size=12)
        head = label(r"the smallest model that speaks to the estimates", font_size=26, color=E.ACCENT).to_edge(
            UP, buff=0.35)
        eqs.next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "The designs say what happened. To ask what a different toll would do, we need a model, and the rule is "
            "to use the smallest one that speaks to the estimates. <bookmark mark='a'/> Two pieces. First, time per "
            "trip rises with traffic, along the curve road engineers have used since the 1960s. <bookmark mark='b'/> "
            f"Its slope comes from the data: miles in the zone fell {say_pct(-M['dlnV'], 1)}, bus travel time fell "
            f"{say_pct(-M['dlnT'], 1)}, so each percent less traffic saves about {M['e_tv']:.2f} percent of time. "
            "<bookmark mark='c'/> Second, demand for trips falls with their full price: the toll, the time, and "
            "everything else a trip costs. The numbers we do not observe are assumptions, written on the screen: "
            f"{ASSUME['miles']:.0f} miles in the zone at {ASSUME['mph']:.0f} miles an hour, time worth "
            f"{ASSUME['vot']:.0f} dollars an hour, half a typical wage as in Part fifty-eight, other costs of "
            f"{ASSUME['other']:.0f} dollars. <bookmark mark='d'/> Then the observed fall in traffic, when the price "
            f"rose by the toll and fell a little with the faster trip, gives the elasticity: {say_num(M['eta'], 2)}. "
            "Driving into Manhattan is very inelastic."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eqs[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]))
            vo.wait_until("c")
            self.play(Write(eqs[2]), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(Write(eqs[3]))
        self.clear_scene()

    def curve(self):
        M = load("model")
        cv = M["curve"]
        tolls = [c["toll"] for c in cv]
        dv = [100 * (np.exp(c["lnV"]) - 1) for c in cv]
        ax = plane([0, 20], [-10, 0], center=LEFT * 1.4 + DOWN * 0.3, x_length=8.4, y_length=4.8,
                   xticks=[0, 5, 9, 15, 20], yticks=[-10, -8, -6, -4, -2, 0], xlabel=r"toll, \ dollars",
                   ylabel=r"traffic in the zone, \ \% against no toll", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}".replace("-", "{-}"), font_size=14)
        ln = path(ax, tolls, dv, TOLL, 3.2)
        d9 = dot(ax, 9, 100 * (np.exp(M["dlnV"]) - 1), WHITE, 0.09)
        l9 = label(r"\$9: \ observed", font_size=16, color=WHITE).next_to(d9, UR, buff=0.08)
        d15 = dot(ax, 15, 100 * (np.exp(M["at15"]["lnV"]) - 1), TOLL, 0.09)
        l15 = label(rf"\$15: \ {100 * (np.exp(M['at15']['lnV']) - 1):.1f}\%".replace("-", "{-}"), font_size=16,
                    color=TOLL).next_to(d15, UR, buff=0.08)
        side = VGroup(
            label(r"the curve passes through the observed \\ point by construction", font_size=17, color=GREY_A),
            label(r"beyond it, \ the model speaks, \\ not the data", font_size=17, color=TOLL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(ax.ax, RIGHT, buff=0.5)
        if side.get_right()[0] > 6.9:
            side.scale_to_fit_width(6.9 - side.get_left()[0])
        tag = island_tag(r"computed: \ agora.congestion.equilibrium, \ central assumptions", corner=DL, font_size=12)
        with self.voiceover(
            "With both pieces, the model gives traffic at any toll. <bookmark mark='a'/> It passes through the one "
            "point we observed, nine dollars, by construction. <bookmark mark='b'/> Everywhere else, the model is "
            "speaking, not the data: at fifteen dollars, the original plan, traffic would be about "
            f"{say_pct(-(np.exp(M['at15']['lnV']) - 1), 1)} below its uncharged level at the central assumptions."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(d9), FadeIn(l9), FadeIn(side[0]), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(d15, scale=1.4), FadeIn(l15), FadeIn(side[1]))
        self.clear_scene()

    def externality(self):
        M = load("model")
        eq = MathTex(r"\text{marginal external cost} \;=\; e \times T \times \text{value of time}", font_size=36)
        nums = MathTex(rf"= {M['e_tv']:.2f} \times {60 * M['T_old']:.0f}\ \text{{min}} \times \${M['vot']:.0f}/"
                       rf"\text{{h}} \;\approx\; \${M['mec_old']:.2f}", font_size=36, color=BUS)
        VGroup(eq, nums).arrange(DOWN, buff=0.35).move_to(UP * 1.6)
        rows = VGroup(
            label(r"the delay one more car imposes on every other car, \ priced: \ Pigou's tax \ (Part 15)",
                  font_size=20, color=GREY_A),
            label(r"what it leaves out: \ bus riders' time, \ pedestrians, \ safety, \ noise, \ emissions, \ the "
                  r"peak hour", font_size=20, color=TOLL),
            label(r"so the narrow model alone cannot justify \$9; \ the case rests on what it omits, \\ and on "
                  r"the revenue for transit, \ which the law intended", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(nums, DOWN, buff=0.6)
        with self.voiceover(
            "The model also prices the thing a congestion charge is for. <bookmark mark='a'/> One more car adds a "
            "little delay to every other car. Added up, that is the marginal external cost of a trip: the "
            "time elasticity, times the trip's time, times what time is worth. <bookmark mark='b'/> At the central "
            f"assumptions, about {M['mec_old']:.2f} dollars a trip. <bookmark mark='c'/> That is Pigou's tax of Part "
            "fifteen, for drivers' time alone. <bookmark mark='d'/> It leaves out bus riders, whose time the faster "
            "buses save; pedestrians; safety; noise; emissions; and the peak hour, where one more car costs far "
            "more than the day's average. <bookmark mark='e'/> So the narrow model alone cannot justify nine "
            "dollars. The case rests on what it leaves out, and on the revenue for transit, which the law intended. "
            "Saying so is part of the paper."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(Write(nums))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
