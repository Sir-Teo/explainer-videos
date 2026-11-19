from __future__ import annotations

from videos.economics.econ18.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.condorcet()
        self.arrow()
        self.today()
        self.question()
        self.title()
        self.objectives()

    def condorcet(self):
        m = load("cycle")
        hc = history_card(1785, r"the Marquis de Condorcet, \ Paris", r"an essay on decisions made by majority vote",
                          color=CYCLE, width=11.0, font_size=24).to_edge(UP, buff=0.4)
        ballots = VGroup(*[ballot(r, w=1.2) for _, r in m["profile"]]).arrange(RIGHT, buff=0.8).next_to(hc, DOWN,
                                                                                                buff=0.5)
        who = VGroup(*[label(rf"voter {k + 1}", font_size=19, color=GREY_A).next_to(b, UP, buff=0.1)
                       for k, b in enumerate(ballots)])
        rows = VGroup(
            label(r"A beats B, \ 2 to 1", font_size=25, color=VOTE["A"]),
            label(r"B beats C, \ 2 to 1", font_size=25, color=VOTE["B"]),
            label(r"C beats A, \ 2 to 1", font_size=25, color=VOTE["C"]),
            label(r"the majority goes round in a circle: \ there is no majority's choice", font_size=26,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.25).next_to(ballots, DOWN, buff=0.45)
        tag = published_tag(r"Condorcet, \emph{Essai sur l'application de l'analyse} (1785)", corner=DR, font_size=13)
        with self.voiceover(
            "In 1785 the Marquis de Condorcet, a mathematician in Paris, published an essay on decisions made by "
            "majority vote. <bookmark mark='a'/> It contains a puzzle. Three voters rank three options. The first "
            "prefers A to B to C; the second, B to C to A; the third, C to A to B. <bookmark mark='b'/> Put A against "
            "B, and A wins, two to one. <bookmark mark='c'/> Put B against C, and B wins, two to one. "
            "<bookmark mark='d'/> Put C against A, and C wins, two to one. <bookmark mark='e'/> The majority goes "
            "round in a circle. Each voter is perfectly consistent, and the group is not: there is no such thing as "
            "the majority's choice."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ballots), FadeIn(who))
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def arrow(self):
        hc = history_card(1950, r"Kenneth Arrow, \ a graduate student", r"``A Difficulty in the Concept of Social "
                          r"Welfare''", color=RULE, width=11.0, font_size=24).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(r"the trouble is not majority rule", font_size=26),
            label(r"every rule for turning individual rankings into a social ranking \ breaks a reasonable condition",
                  font_size=24, color=CYCLE),
            label(r"unless one person decides for everyone", font_size=26, color=E.ACCENT),
            label(r"the Nobel prize in 1972; \ the theorem that founded a field", font_size=23, color=GREY_A),
        ).arrange(DOWN, buff=0.4).next_to(hc, DOWN, buff=0.6)
        tag = published_tag(r"Arrow, JPE 58(4) (1950); \ \emph{Social Choice and Individual Values} (1951)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "For a century and a half the circle was a curiosity. In 1950 a graduate student, Kenneth Arrow, "
            "published a short paper called A Difficulty in the Concept of Social Welfare. <bookmark mark='a'/> It "
            "showed that the trouble is not majority rule. <bookmark mark='b'/> Every rule for turning individual "
            "rankings into a ranking for society breaks at least one of a few conditions that seem impossible to "
            "give up, <bookmark mark='c'/> unless one person decides for everyone. <bookmark mark='d'/> Arrow shared "
            "the Nobel prize in 1972, and the theorem founded a field."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def today(self):
        rows = point_cards([
            (r"elections", r"which voting rule, \\ and who sets the agenda", VOTE["B"]),
            (r"committees", r"budgets, \ hirings, \\ juries, \ boards", VOTE["A"]),
            (r"policy appraisal", r"adding up gains \\ and losses in money", MONEY),
            (r"inequality", r"how much is a dollar to \\ the poor worth, to the rich?", RAWLS),
            (r"lives and risks", r"what to spend \\ to save a statistical life", LIFE),
            (r"machines", r"whose preferences \\ should an AI follow?", RULE),
        ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
        head = label(r"adding people up, \ everywhere", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "The question is everywhere. <bookmark mark='a'/> Elections choose a voting rule, and somebody sets the "
            "agenda. Committees vote on budgets, hirings and verdicts. Every appraisal of a policy adds up gains and "
            "losses, usually in money, and must decide how much a dollar to a poor family counts against a dollar to "
            "a rich one. Regulators decide how much to spend to save a statistical life. <bookmark mark='b'/> And "
            "the companies building artificial intelligence must decide whose preferences their machines should "
            "follow."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in rows.cards[:5]], lag_ratio=0.7), run_time=10)
            vo.wait_until("b")
            self.play(FadeIn(rows.cards[5], shift=UP * 0.1))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"which voting rule is right, \ if every rule fails somewhere?", font_size=29, color=VOTE["B"]),
            label(r"can a society's welfare be measured, \ and whose counts for how much?", font_size=29, color=WELF),
            label(r"and what is left for someone who must choose a policy?", font_size=29, color=MONEY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "Part seventeen matched people one by one. This part chooses for everyone at once. Can the wants of many "
            "people be added up into what society wants? <bookmark mark='a'/> Which voting rule is right, if every "
            "rule fails somewhere? <bookmark mark='b'/> Can a society's welfare be measured, and whose counts for how "
            "much? <bookmark mark='c'/> And what is left for someone who has to choose a policy?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        logo = VGroup(*[ballot(r, w=1.0, font_size=18) for r in (("A", "B", "C"), ("B", "C", "A"), ("C", "A", "B"))]
                      ).arrange(RIGHT, buff=0.35)
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 18 \ $\cdot$ \ Social Choice and Welfare", font_size=34, color=E.ACCENT)
        VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part eighteen: social choice and welfare."):
            self.play(FadeIn(logo, shift=UP * 0.2), run_time=1.2)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act IV \ $\cdot$ \ Failure and Design", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"one island, \ five rules, \ five winners; \ Borda, \ Condorcet and the agenda",
            r"Arrow's theorem, \ proved by the pivotal voter; \ single peaks, \ May and strategic voting",
            r"comparing people; \ Bentham, \ Rawls and Atkinson; \ two veils",
            r"Pareto and its limits; \ cost-benefit analysis; \ the value of a statistical life",
            r"capabilities; \ a dial for lives; \ quadratic voting and choosing for machines",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part closes Act Four. <bookmark mark='a'/> You'll see one island choose five different winners "
            "with five rules, then Borda against Condorcet, and the power of whoever sets the agenda. "
            "<bookmark mark='b'/> Arrow's theorem, proved step by step; the escape through single-peaked "
            "preferences; and strategic voting. <bookmark mark='c'/> Then welfare: comparing people, the sums of "
            "Bentham, Rawls and Atkinson, and two veils of ignorance. <bookmark mark='d'/> Pareto and its limits, "
            "cost-benefit analysis, and the value of a statistical life. <bookmark mark='e'/> And capabilities, a "
            "dial for lives, and a frontier of new voting rules and choosing for machines."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
