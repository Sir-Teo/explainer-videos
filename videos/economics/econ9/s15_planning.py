from __future__ import annotations

from videos.economics.econ9.common import *  # noqa: F403

H = tables.HAYEK_1945.data
PLANK = "#C8A27A"
MAST = "#7EC8F5"


class Planning(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The calculation debate: \ Mises, \ Lange, \ Hayek and Kantorovich", r"Could a planner "
             r"compute what a market computes?", "Chapter thirteen. The calculation debate: Mises, Lange, Hayek, "
             "and Kantorovich.", lit={1939: r"Kantorovich's programme"}, scale=("nation",), horizon=("a year",))
        self.debate()
        self.kantorovich()
        self.prices()
        self.lesson()

    def debate(self):
        cards = VGroup(
            history_card(1920, r"Ludwig von Mises", r"without markets for machines and land there are no prices "
                         r"for them, \ so a socialist economy cannot calculate", color=HOLD, width=11.6, font_size=22),
            history_card(1936, r"Oskar Lange", r"a planning board could find the prices by trial and error, \ "
                         r"like Walras's auctioneer: \ raise them where there's a shortage", color=PLAN, width=11.6,
                         font_size=22),
            history_card(1945, r"Friedrich Hayek", r"the knowledge the board would need is scattered among "
                         r"millions of people; \ prices are how it travels", color=CC, width=11.6, font_size=22),
        ).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.4)
        q = quote_card(tex_safe(H["dials"]), r"Hayek, \emph{American Economic Review} (1945)", width=11.6,
                       font_size=23, color=CC).next_to(cards, DOWN, buff=0.35)
        tag = published_tag(r"Mises (1920); Lange, Review of Economic Studies 4 (1936-37); Hayek, AER 35(4) (1945)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "If an equilibrium is just the solution to a system of equations, why not have a planner solve it? "
            "That was the question of a famous argument between the wars. <bookmark mark='a'/> In 1920 Ludwig von "
            "Mises argued that a socialist economy, with no markets for machines and land, would have no prices for "
            "them, and so no way to calculate which uses were worth it. <bookmark mark='b'/> In 1936 Oskar Lange "
            "replied that a planning board could find the prices by trial and error, exactly like Walras's "
            "auctioneer: raise the price wherever there's a shortage, cut it wherever there's a surplus. "
            "<bookmark mark='c'/> In 1945 Friedrich Hayek answered that the equations are not the problem. The "
            "knowledge they need is scattered among millions of people, each knowing a little about their own "
            "circumstances, and prices are how that knowledge travels: <bookmark mark='d'/> in his words, a "
            "system of telecommunications which enables individual producers to watch merely the movement of a "
            "few pointers, as an engineer might watch the hands of a few dials."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.clear_scene()

    def kantorovich(self):
        k = load("plan")
        R = np.array(k["rates"])
        T = np.array(k["plan"])
        head = VGroup(label(r"machine", font_size=21, color=GREY_A), label(r"planks a day", font_size=21, color=PLANK),
                      label(r"or masts a day", font_size=21, color=MAST), label(r"the plan", font_size=21,
                                                                                 color=E.ACCENT))
        rows = VGroup(head)
        for name, r, t in zip(k["machines"], R, T):
            work = r"planks" if t[0] > 0.5 else r"masts"
            rows.add(VGroup(label(name, font_size=23), label(f"{r[0]:g}", font_size=23, color=PLANK),
                            label(f"{r[1]:g}", font_size=23, color=MAST),
                            label(rf"all day on {work}", font_size=22, color=PLANK if work == r"planks" else MAST)))
        xs = (-6.6, -5.1, -3.5, -1.8)
        for k_, row in enumerate(rows):
            for c, x in zip(row, xs):
                c.move_to([x, 1.6 - 0.6 * k_, 0], aligned_edge=LEFT)
        plan_col = VGroup(*[r[3] for r in rows[1:]])
        hc = history_card(1939, r"Leonid Kantorovich, \ Leningrad", r"asked by a plywood trust how to share work "
                          r"among its machines, \ he invents linear programming", color=PLAN, width=5.0,
                          font_size=21).to_edge(RIGHT, buff=0.35).shift(UP * 1.8)
        side = VGroup(
            label(rf"a boat's set: \ {k['kit'][0]:g} planks and {k['kit'][1]:g} mast", font_size=22),
            label(rf"each machine making whole sets alone: \ {k['alone']:.2f} sets a day", font_size=21,
                  color=GREY_A),
            label(rf"the best plan: \ {k['sets']:.0f} sets a day", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(hc, DOWN, buff=0.4).align_to(hc, LEFT)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "There was a planner who did solve such equations, and found prices inside them. "
            "<bookmark mark='a'/> In the late nineteen thirties, in Leningrad, a plywood trust asked the "
            "mathematician Leonid Kantorovich how to share its work among machines of different abilities. To "
            "answer, he invented what we now call linear programming, and published it in 1939. <bookmark mark='b'/> Here is a problem of his kind for the boatyard. "
            "Four machines can each make planks or masts, at different rates, and a boat needs a set of two planks "
            "and one mast. <bookmark mark='c'/> If each machine split its day to make whole sets on its own, the "
            "yard would make two point eight five sets a day. <bookmark mark='d'/> The best plan puts the saw and "
            "the adze on planks all day, and the lathe and the press on masts: five sets a day, about three-quarters "
            "more, from the same machines."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.2), FadeIn(VGroup(*head[:3])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*[VGroup(*r[:3]) for r in rows[1:]])), FadeIn(head[3]), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in plan_col], lag_ratio=0.3),
                      FadeIn(side[2]))
        self.clear_scene()

    def prices(self):
        k = load("plan")
        V = np.array(k["value_per_day"])
        mv = np.array(k["machine_value"])
        rows = VGroup(VGroup(label(r"machine", font_size=21, color=GREY_A),
                             label(r"a day on planks is worth", font_size=21, color=PLANK),
                             label(r"a day on masts", font_size=21, color=MAST),
                             label(r"a day's value", font_size=21, color=E.ACCENT)))
        for name, v, m in zip(k["machines"], V, mv):
            rows.add(VGroup(label(name, font_size=23), label(f"{v[0]:.2f}", font_size=23, color=PLANK),
                            label(f"{v[1]:.2f}", font_size=23, color=MAST),
                            label(f"{m:.2f}", font_size=23, color=E.ACCENT)))
        xs = (-5.8, -3.6, -0.6, 1.6)
        for k_, row in enumerate(rows):
            for c, x in zip(row, xs):
                c.move_to([x, 2.4 - 0.6 * k_, 0], aligned_edge=LEFT)
        plan = np.array(k["plan"])
        best = VGroup()
        for k_, t in enumerate(plan, start=1):
            j = int(np.argmax(t))                           # the part this machine works on in the plan
            best.add(SurroundingRectangle(rows[k_][1 + j], color=E.ACCENT, buff=0.08))
        notes = VGroup(
            label(rf"the dual of the programme: \ a price for each part \ ({k['part_value'][0]:.2f} of a set each) "
                  r"\\ and for a day on each machine", font_size=23),
            label(r"each machine works where its day is worth the most: \ the prices alone decentralize the plan",
                  font_size=23, color=CC),
            label(r"Kantorovich called them ``resolving multipliers''; \ the lathe is indifferent, \ worth the same "
                  r"either way", font_size=21, color=GREY_A),
            label(r"1975: \ the Nobel prize, \ with Tjalling Koopmans, \ for the optimum allocation of resources",
                  font_size=21, color=PLAN),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "And then Kantorovich found prices in it. <bookmark mark='a'/> Every linear programme has a twin, its "
            "dual, which puts a value on each scarce thing: here, on a plank, on a mast, and on a day of each "
            "machine. <bookmark mark='b'/> Value a day on each machine at what it could make, and every machine "
            "turns out to be working exactly where its day is worth the most. A manager told only these numbers "
            "would choose the plan without being told it. <bookmark mark='c'/> Kantorovich called them resolving "
            "multipliers. They are prices, computed by a planner. <bookmark mark='d'/> In 1975 he shared the Nobel "
            "prize with Tjalling Koopmans, who had found the same mathematics independently in the West."
        ) as vo:
            self.play(FadeIn(rows), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(b_) for b_ in best], lag_ratio=0.3), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.clear_scene()

    def lesson(self):
        head = label(r"so who won the argument?", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"the mathematics: \ a planner who could solve the problem would find prices too", font_size=25),
            label(r"the information: \ the rates of every machine, \ the tastes of every household, \\ are known "
                  r"only to the people who have them", font_size=24, color=CC),
            label(r"the incentives: \ would they report them truthfully? \ (mechanism design, \ Part 17)",
                  font_size=24, color=HOLD),
            label(r"a market is a way of solving the problem \\ without anyone needing to know all of it",
                  font_size=26, color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "So who won? <bookmark mark='a'/> On the mathematics, Lange and Kantorovich: a planner who could solve "
            "the problem would find prices too. <bookmark mark='b'/> On information, Hayek: the rates of every "
            "machine and the tastes of every household are known only to the people who have them, and they "
            "change every day. <bookmark mark='c'/> And there's a third question nobody in the debate fully "
            "answered: would people tell the planner the truth? That's mechanism design, in Part seventeen. "
            "<bookmark mark='d'/> A market is a way of solving the equations of this part without anyone ever "
            "having to know all of them."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
