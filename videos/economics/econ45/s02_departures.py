from __future__ import annotations

from videos.economics.econ45.common import *  # noqa: F403


class Departures(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Three departures", r"Where exactly does the textbook agent go wrong?",
             "Chapter one. Three departures.", lit={2009: r"DellaVigna"}, scale=("person",), horizon=("a day",))
        self.formula()
        self.classes()
        self.agents()

    def formula(self):
        eq = MathTex(r"\max_{x \in X}", r"\;\sum_{t} \delta^{t}", r"\sum_{s} p(s)", r"\,U(x \mid s)",
                     font_size=60).move_to(UP * 1.4)
        eq[0].set_color(FIRM)
        eq[1].set_color(PLAN)
        eq[2].set_color(GYM)
        eq[3].set_color(SOPH)
        notes = VGroup(
            label(r"choose the best \\ of what is on offer", font_size=19, color=FIRM),
            label(r"weigh the future \\ at a steady rate", font_size=19, color=PLAN),
            label(r"with correct \\ beliefs", font_size=19, color=GYM),
            label(r"about your own \\ well-being", font_size=19, color=SOPH),
        )
        notes.arrange(RIGHT, buff=0.55).next_to(eq, DOWN, buff=1.0)
        links = VGroup(*[Line(part.get_bottom() + DOWN * 0.08, nt.get_top() + UP * 0.08, stroke_width=1.6,
                              color=GREY_B) for nt, part in zip(notes, eq)])
        foot = label(r"Part 5's agent: \ every term can fail, \ and each failure has a name", font_size=22,
                     color=E.ACCENT).to_edge(DOWN, buff=0.9)
        tag = published_tag(tables.DEPARTURES_2009.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Write down the agent of Part five in one line. <bookmark mark='a'/> The agent chooses, from what is "
            "on offer, <bookmark mark='b'/> the plan that maximizes the sum over time of well-being, with the future "
            "discounted at a steady rate, <bookmark mark='c'/> weighting each state of the world by its correct "
            "probability, <bookmark mark='d'/> where well-being depends only on the agent's own outcomes. "
            "<bookmark mark='e'/> Behavioural economics asks what happens when one of these pieces fails. Stefano "
            "DellaVigna sorted the evidence into three kinds of failure."
        ) as vo:
            self.play(FadeIn(tag), Write(eq), run_time=2.0)
            for mk, nt, part in zip("abcd", notes, eq):
                vo.wait_until(mk)
                k = list(notes).index(nt)
                self.play(Create(links[k]), FadeIn(nt, shift=UP * 0.1), Indicate(part, scale_factor=1.08))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def classes(self):
        cols = VGroup()
        spec = [
            (r"preferences", PLAN, [r"present bias: \ now \\ weighs too much",
                                    r"reference points: \ losses \\ loom larger than gains",
                                    r"social preferences: \\ others' payoffs matter"]),
            (r"beliefs", GYM, [r"overconfidence, \ about \\ yourself especially",
                               r"the law of small numbers", r"projection: \ assuming \\ tomorrow feels like today"]),
            (r"decision making", FIRM, [r"framing and defaults", r"limited attention",
                                        r"menus, \ persuasion, \\ social pressure, \ emotion"]),
        ]
        for title, col, rows in spec:
            t = label(title, font_size=26, color=col)
            body = VGroup(*[label(r_, font_size=19, color=WHITE) for r_ in rows]).arrange(DOWN, aligned_edge=LEFT,
                                                                                           buff=0.3)
            box = RoundedRectangle(width=3.9, height=3.9, corner_radius=0.14, stroke_color=col, stroke_width=2.2,
                                   fill_color="#141821", fill_opacity=1)
            t.move_to(box.get_top() + DOWN * 0.45)
            body.next_to(t, DOWN, buff=0.4)
            cols.add(VGroup(box, t, body))
        cols.arrange(RIGHT, buff=0.35).move_to(DOWN * 0.1)
        head = label(r"three ways to depart \ (DellaVigna, \ 2009)", font_size=28, color=E.ACCENT).to_edge(UP,
                                                                                                          buff=0.5)
        tag = published_tag(tables.DEPARTURES_2009.tag, corner=DR, font_size=11)
        with self.voiceover(
            "First, preferences that are not the textbook's. <bookmark mark='a'/> People weigh the present too much "
            "against the future, which is the gym; they judge outcomes as gains or losses against a reference point, "
            "and losses loom larger; and they care about what others get. <bookmark mark='b'/> Second, beliefs that "
            "are systematically wrong: overconfidence, especially about ourselves; seeing patterns in small samples; "
            "and projecting today's feelings onto tomorrow, like shopping for food when hungry. "
            "<bookmark mark='c'/> Third, the way decisions are made: the frame and the default matter, attention is "
            "limited, and the menu, the salesperson and the mood all move the choice. <bookmark mark='d'/> Each of "
            "these is a hypothesis with a prediction that the standard model does not make. The work of the field "
            "is to test those predictions where the stakes are real."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cols[0][0]), FadeIn(cols[0][1]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in cols[0][2]], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(cols[1][0]), FadeIn(cols[1][1]),
                      LaggedStart(*[FadeIn(r_) for r_ in cols[1][2]], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(cols[2][0]), FadeIn(cols[2][1]),
                      LaggedStart(*[FadeIn(r_) for r_ in cols[2][2]], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("d")
            self.play(*[Indicate(c[1], scale_factor=1.06) for c in cols])
        self.clear_scene()

    def agents(self):
        cards = point_cards([
            (r"the naif", r"present-biased, \\ and sure tomorrow's \\ self will do better", NAIF),
            (r"the sophisticate", r"present-biased, \\ and knows it", SOPH),
            (r"the loss-averse trader", r"values what \\ it owns more than \\ what it could buy", SELL),
            (r"the inattentive buyer", r"reads the first \\ digit, \ skips \\ the fine print", BUY),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.3)
        head = label(r"new residents of the Island", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.6)
        foot = label(r"each is one equation away from Part 5's agent, \ and drops into the Island's markets",
                     font_size=20, color=GREY_A).to_edge(DOWN, buff=0.7)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The Island gets new residents for this part, each one change away from the agent of Part five. "
            "<bookmark mark='a'/> The naif, who overweights the present and is sure that tomorrow's self will do "
            "better. <bookmark mark='b'/> The sophisticate, who overweights the present too, but knows it. "
            "<bookmark mark='c'/> The loss-averse trader, who values what it owns more than what it could buy. "
            "<bookmark mark='d'/> And the inattentive buyer, who reads the first digit and skips the fine print. "
            "<bookmark mark='e'/> Because the Island knows exactly how each of them is built, we can see what the "
            "methods of the field recover, and what firms and markets do with them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Circumscribe(cards.cards[0], color=WHITE, buff=0.05))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
