from __future__ import annotations

from videos.philosophy.philosophy35.common import *  # noqa: F403


class Contract(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Contractualism", r"Is a wrong act one that others could reasonably reject?",
                            lit=(1998,), part=PART)
        with self.voiceover("Chapter nine. Contractualism."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.scanlon()
        self.numbers()
        self.transmitter()

    def scanlon(self):
        hc = history_card(1998, r"T. M. Scanlon", r"\textit{What We Owe to Each Other}", width=5.4,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = [(r"the test", r"an act is wrong if any principle permitting it could reasonably be rejected by "
                              r"someone affected", AGG),
                (r"complaints", r"each person's objection is weighed one at a time: \ the strongest individual "
                                r"complaint decides", DUTY),
                (r"no summing", r"the separateness of persons \ (Rawls; \ Nozick): \ one person's great loss is not "
                                r"made up by many small gains to others", HARM),
                (r"against Hobbes", r"the motive is not advantage but justifiability to each other: \ Part 34's "
                                    r"bargainers had power; \ Scanlon's have reasons", GOAL)]
        g = rows_table(rows, top=1.2, gap=0.45, width=8.0, x_text=-2.2)
        with self.voiceover(
            "T. M. Scanlon's What We Owe to Each Other, of 1998, grounds morality in what we can justify to each "
            "other. <bookmark mark='a'/>An act is wrong if any principle permitting it could reasonably be rejected "
            "by someone it affects. <bookmark mark='b'/>Objections are weighed one person at a time: the strongest "
            "individual complaint decides. <bookmark mark='c'/>There is no summing across people. The separateness of "
            "persons, stressed by Rawls and Nozick, means that one person's great loss is not made up by many small "
            "gains to others. <bookmark mark='d'/>Unlike the bargainers of Part 34, Scanlon's contractors are moved "
            "not by advantage but by the wish to act on principles they can justify to everyone."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def numbers(self):
        d = load("taurek")
        head = label(r"Should the numbers count? \ (Taurek, \ 1977)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = {r["policy"]: r for r in d["rows"]}
        assert d["many"] == 5 and [r["policy"] for r in d["rows"]] == ["save the many", "fair coin",
                                                                       "weighted lottery"]
        assert [r["expected_saved"] for r in d["rows"]] == [5.0, 3.0, 4.3333]
        assert [r["simulated_saved"] for r in d["rows"]] == [5.0, 2.987, 4.339]
        rock1 = VGroup(Ellipse(width=1.6, height=0.5, color=GREY_B, fill_opacity=0.25),
                       Dot(radius=0.11, color=AGG).shift(UP * 0.28)).move_to([-4.2, 1.5, 0])
        rock5 = VGroup(Ellipse(width=2.6, height=0.5, color=GREY_B, fill_opacity=0.25),
                       *[Dot(radius=0.11, color=GOOD).shift(UP * 0.28 + RIGHT * (0.38 * k - 0.76)) for k in range(5)]
                       ).move_to([2.6, 1.5, 0])
        boat = label(r"you can reach one rock", font_size=17, color=GREY_A).move_to([-0.8, 1.55, 0])
        hd = [r"\text{policy}", r"\text{the one's chance}", r"\text{each of the five}", r"\text{expected saved}",
              r"\text{simulated, } 10^5 \text{ runs}"]
        cols = {"save the many": GOOD, "fair coin": DUTY, "weighted lottery": AGG}
        cells = [[label(n, font_size=17, color=cols[n]), label(f"{r['p_one']:.3f}", font_size=17),
                  label(f"{r['p_many']:.3f}", font_size=17), label(f"{r['expected_saved']:.2f}", font_size=17,
                                                                     color=GOAL),
                  label(f"{r['simulated_saved']:.3f}", font_size=17, color=GREY_A)] for n, r in rows.items()]
        grid = ValueGrid(hd, cells, col_w=[2.8, 2.4, 2.4, 2.2, 2.6], cell_h=0.55, font_size=16).move_to([0, -0.4, 0])
        foot = label(r"Kamm; \ Scanlon: \ one of the five balances the one; \ the other four break the tie",
                     font_size=18, color=AGG).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "John Taurek pressed the point furthest, in Should the Numbers Count? of 1977. <bookmark mark='a'/>One "
            "person is stranded on one rock and five on another; the tide is rising, and you can reach only one rock. "
            "Most people say: save the five. <bookmark mark='b'/>Taurek said no. What is bad is what happens to each "
            "person, not a sum that happens to no one; each of the six has the same claim to be saved, so toss a "
            "fair coin. <bookmark mark='c'/>The Reasoner runs each policy a hundred thousand times. Saving the many "
            "saves five every time, but gives the lone person no chance at all. The coin gives everyone an even "
            "chance, and saves three on average. <bookmark mark='d'/>A weighted lottery, with chances in proportion "
            "to numbers, gives each of the five five sixths and the one a sixth, and saves four and a third. "
            "<bookmark mark='e'/>Frances Kamm and Scanlon answered Taurek without adding anything up: let one of the "
            "five balance the one, and the remaining four break the tie. The tie-breaking argument keeps the "
            "separateness of persons and still lets the numbers count."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rock1), FadeIn(rock5), FadeIn(boat))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for k in range(2) for c in grid.cell[k]])
            vo.wait_until("d")
            self.play(*[FadeIn(c) for c in grid.cell[2]])
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def transmitter(self):
        d = load("transmitter")
        head = label(r"The Transmitter Room, \ and partial aggregation", font_size=30, color=CONN).to_edge(UP,
                                                                                                        buff=0.3)
        rows = d["rows"]
        assert d["harm"] == 100.0 and d["relevance"] == 0.5
        assert [(r["full"], r["individualist"], r["relevance"]) for r in rows] == [
            ("help the many", "save Jones", "save Jones"), ("help the many", "save Jones", "save Jones"),
            ("help the many", "save Jones", "help the many"), ("help the many", "toss up", "help the many")]
        story = label(r"Jones is suffering agonizing shocks \ (harm 100) \ in the transmitter room; \ saving him "
                      r"interrupts a broadcast", font_size=18, color=GREY_A).next_to(head, DOWN, buff=0.3)
        hd = [r"\text{the others each lose}", r"\text{people}", r"\text{sum everything}", r"\text{one at a time}",
              r"\text{relevance view}"]
        nice = {1e9: r"$10^9$", 3: r"3", 2: r"2"}
        cells = [[label(r["each_loses"], font_size=16), label(nice[r["people"]], font_size=17, color=GREY_A),
                  label(r["full"], font_size=16, color=GOOD), label(r["individualist"], font_size=16, color=DUTY),
                  label(r["relevance"], font_size=16, color=AGG)] for r in rows]
        grid = ValueGrid(hd, cells, col_w=[3.8, 1.4, 2.6, 2.4, 2.4], cell_h=0.55, font_size=16).move_to([0, -0.3, 0])
        foot = label(r"relevance \ (Voorhoeve, \ 2014): \ add up only claims at least half as strong as the strongest",
                     font_size=18, color=AGG).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Scanlon's own example tests aggregation. <bookmark mark='a'/>Jones has suffered an accident in the "
            "transmitter room during a World Cup broadcast, and is receiving agonizing shocks. Rescuing him means "
            "interrupting the broadcast for an hour. <bookmark mark='b'/>Summing everything, a billion viewers' small "
            "losses outweigh Jones's agony, and the broadcast should go on. Scanlon, comparing complaints one at a "
            "time, says save Jones, and almost everyone agrees. <bookmark mark='c'/>But pure non-aggregation goes too "
            "far: it would save Jones rather than prevent three people each breaking an arm, or even, as a toss-up, "
            "rather than save two lives. <bookmark mark='d'/>Alex Voorhoeve's relevance view, of 2014, adds up only "
            "claims at least comparable to the strongest. The Reasoner applies it: save Jones against the broadcast "
            "and the migraines; help the many against the broken arms and the two lives. Partial aggregation keeps "
            "the intuitions that full summing and pure individualism each lose."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(story))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for k in range(2) for c in grid.cell[k][:4]])
            vo.wait_until("c")
            self.play(*[FadeIn(c) for k in range(2, 4) for c in grid.cell[k][:4]])
            vo.wait_until("d")
            self.play(*[FadeIn(grid.cell[k][4]) for k in range(4)], FadeIn(foot))
        self.clear_scene()
