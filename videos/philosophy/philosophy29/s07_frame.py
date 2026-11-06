from __future__ import annotations

from videos.philosophy.philosophy29.common import *  # noqa: F403


class Frame(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"The frame problem", r"How does a reasoner know what its actions leave alone?",
                            lit=(1969, 1991), part=PART)
        with self.voiceover("Chapter six. The frame problem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.logic()
        self.robots()
        self.relevance()
        self.wall_brick()
        self.price()

    def logic(self):
        d = load("axioms")
        hc = history_card(1969, r"John McCarthy and Patrick Hayes", r"`Some Philosophical Problems from the "
                                r"Standpoint of Artificial Intelligence'", width=8.6, color=HIST).to_corner(UL, buff=0.3)
        eff = MathTex(r"\text{Holding}(x,\ \text{do}(\text{pickup}(x),\, s))", font_size=28, color=ACT)
        frm = MathTex(r"\text{Colour}(y, c, s) \rightarrow \text{Colour}(y, c,\ \text{do}(\text{pickup}(x),\, s))",
                      font_size=28, color=BAD)
        ssa = MathTex(r"F(\text{do}(a, s)) \;\leftrightarrow\; \gamma^{+}_F(a, s) \;\vee\; \big(F(s) \wedge \neg "
                      r"\gamma^{-}_F(a, s)\big)", font_size=30, color=OK)
        tags = [label(r"an effect axiom: \ what picking up changes", font_size=18, color=ACT),
                label(r"a frame axiom: \ what it leaves alone", font_size=18, color=BAD),
                label(r"Reiter \ (1991): \ one successor-state axiom per fluent", font_size=18, color=OK)]
        col = VGroup(*[VGroup(f, t).arrange(DOWN, buff=0.12) for f, t in zip([eff, frm, ssa], tags)]).arrange(
            DOWN, buff=0.35).move_to([-2.4, -0.6, 0])
        rows_d = d["rows"]
        assert [r["frame_axioms"] for r in rows_d] == [30, 1000, 200000] and [r["ssa"] for r in rows_d] == [5, 50, 1000]
        hd = [r"A", r"F", r"\text{frame axioms}", r"\text{SSAs}"]
        cells = [[MathTex(str(r["actions"]), font_size=22), MathTex(str(r["fluents"]), font_size=22),
                  MathTex(f"{r['frame_axioms']:,}".replace(",", r"\,"), font_size=22, color=BAD),
                  MathTex(str(r["ssa"]), font_size=22, color=OK)] for r in rows_d]
        grid = ValueGrid(hd, cells, col_w=[0.9, 1.0, 1.9, 1.1], cell_h=0.48, font_size=20).move_to([4.6, -0.8, 0])
        with self.voiceover(
            "In 1969 John McCarthy and Patrick Hayes asked what it would take for a machine to reason about action. "
            "Their logic is the situation calculus: a situation s, and do of a and s for the situation after action "
            "a. <bookmark mark='a'/>An effect axiom says what an action changes: after picking up x, the robot is "
            "holding x. <bookmark mark='b'/>But nothing yet says what it leaves alone. Does picking up a block change "
            "the colour of the walls? The logic does not know, unless told by a frame axiom: if y had colour c, it "
            "still has colour c after the pickup. <bookmark mark='c'/>One is needed for nearly every pair of an "
            "action and a property it does not affect, about two times A times F of them. Ten actions and fifty "
            "fluents need a thousand; a hundred actions and a thousand fluents, two hundred thousand. That is the "
            "frame problem, in its original, logical form. <bookmark mark='d'/>In 1991 Ray Reiter, building on "
            "others, compressed them into one successor-state axiom per fluent: F holds after a if a made it true, "
            "or it held before and a did not make it false. A thousand axioms instead of two hundred thousand."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(col[0]))
            vo.wait_until("b")
            self.play(FadeIn(col[1]))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(3):
                self.play(*[FadeIn(c) for c in grid.cell[r][:3]], run_time=0.5)
            vo.wait_until("d")
            self.play(FadeIn(col[2]), *[FadeIn(grid.cell[r][3]) for r in range(3)])
        self.clear_scene()

    def robots(self):
        d = load("robots")
        head = label(r"Dennett's robots, \ built", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["r1_plan"] == ["open_door", "pull_wagon_out"] and d["r1_outcome"] == {"bomb_out": True,
                                                                                       "battery_out": True}
        assert d["plan"] == ["open_door", "remove_bomb", "pull_wagon_out"]
        rows_d = d["rows"]
        assert [r["expanded"] for r in rows_d] == [8, 19, 34, 53, 76]
        assert [r["derived"] for r in rows_d] == [105, 684, 2299, 5694, 11805]
        assert all(r["expanded_relevant"] == 8 for r in rows_d) and rows_d[-1]["derived_relevant"] == 225
        room = Rectangle(width=4.2, height=2.4, color=GREY_B).move_to([-4.3, 1.0, 0])
        door = Line([-2.2, 0.6, 0], [-2.2, 1.4, 0], color=WORLD, stroke_width=6)
        wagon = VGroup(Rectangle(width=1.4, height=0.35, color=OBJ, fill_opacity=0.4),
                       Circle(radius=0.1, color=OBJ).shift(LEFT * 0.45 + DOWN * 0.25),
                       Circle(radius=0.1, color=OBJ).shift(RIGHT * 0.45 + DOWN * 0.25)).move_to([-4.6, 0.4, 0])
        batt = VGroup(Rectangle(width=0.45, height=0.3, color=OK, fill_opacity=0.6),
                      label(r"battery", font_size=13, color=OK).shift(UP * 0.3)).move_to([-4.95, 0.85, 0])
        bomb = VGroup(Circle(radius=0.18, color=BAD, fill_opacity=0.6),
                      label(r"bomb", font_size=13, color=BAD).shift(UP * 0.32)).move_to([-4.25, 0.85, 0])
        story = stack([(r"R1: \ plan \ open the door, \ pull the wagon out \ $\to$ the bomb comes too", BAD),
                       (r"with successor-state axioms: \ open, \ remove the bomb, \ pull \ $\to$ safe", OK)],
                      font_size=19, aligned_edge=LEFT, width=6.0, buff=0.2).move_to([3.3, 1.5, 0])
        hd = [r"\text{irrelevant fluents}", r"\text{states expanded}", r"\text{facts deduced}",
              r"\text{if told what matters}"]
        cells = [[MathTex(str(r["irrelevant"]), font_size=20), MathTex(str(r["expanded"]), font_size=20, color=BAD),
                  MathTex(f"{r['derived']:,}".replace(",", r"\,"), font_size=20, color=BAD),
                  MathTex(rf"{r['expanded_relevant']}\ /\ {r['derived_relevant']}", font_size=20, color=OK)]
                 for r in rows_d]
        grid = ValueGrid(hd, cells, col_w=[2.6, 2.4, 2.2, 2.8], cell_h=0.4, font_size=18).move_to([0.6, -1.8, 0])
        with self.voiceover(
            "In 1984 Daniel Dennett told the problem as a story, and the Reasoner can act it out. "
            "<bookmark mark='a'/>A robot, R1, must fetch its spare battery from a room. The battery is on a wagon, "
            "and so is a time bomb. <bookmark mark='b'/>R1 knows the bomb is on the wagon, but its model of pulling "
            "lists only what it cares about: the wagon and the battery come out. Its plan: open the door, pull the "
            "wagon out. The bomb comes too. <bookmark mark='c'/>With successor-state axioms, which say that whatever "
            "is on the wagon moves with it, the planner finds the right plan: open the door, take the bomb off, pull. "
            "<bookmark mark='d'/>But Dennett's next robot, R1D1, deduced every consequence of every action it "
            "considered, and the bomb went off while it was still at work. The Reasoner's planner does the same: "
            "with no irrelevant fluents in the room, it expands eight states and deduces a hundred and five facts. "
            "Add eight irrelevant ones, a light switch, the paint, and so on, and it expands seventy-six states and "
            "deduces eleven thousand eight hundred and five facts, for the same three-step plan. "
            "<bookmark mark='e'/>Told in advance which actions matter, it needs eight states again. But being told "
            "is the whole problem. Dennett's third robot, R2D1, was built to ignore irrelevant implications; it sat "
            "outside the room, busily ignoring thousands of them, as the bomb went off."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(room), FadeIn(door), FadeIn(wagon), FadeIn(batt), FadeIn(bomb))
            vo.wait_until("b")
            self.play(FadeIn(story[0]), VGroup(wagon, batt, bomb).animate.shift(RIGHT * 3.2))
            vo.wait_until("c")
            self.play(VGroup(wagon, batt, bomb).animate.shift(LEFT * 3.2))
            self.play(bomb.animate.shift(DOWN * 0.5 + LEFT * 1.0))
            self.play(VGroup(wagon, batt).animate.shift(RIGHT * 3.2), FadeIn(story[1]))
            vo.wait_until("d")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(cells)):
                self.play(*[FadeIn(c) for c in grid.cell[r][:3]], run_time=0.4)
            vo.wait_until("e")
            self.play(*[FadeIn(grid.cell[r][3]) for r in range(len(cells))])
        self.clear_scene()

    def relevance(self):
        head = label(r"The logical problem, \ and the philosophical one", font_size=30, color=CONN).to_edge(UP,
                                                                                                           buff=0.35)
        rows = [
            (r"the logical problem", r"representing what does not change, \ compactly: \ largely solved \ "
                                     r"(circumscription, \ 1980; \ successor-state axioms, \ 1991)", OK),
            (r"the philosophical problem", r"deciding what is relevant, \ in a situation never met before, \ without "
                                           r"considering everything", BAD),
            (r"Fodor \ (1983)", r"belief fixation is isotropic: \ anything might bear on anything; \ and Quinean: \ "
                                r"it depends on the whole system", SIGN),
            (r"Hamlet's problem", r"when to stop thinking, \ and act \ (Fodor, \ 1987)", BODY),
            (r"Dreyfus", r"the problem only arises for a reasoner who starts from facts; \ a skilled coper is already "
                         r"in a situation where things matter", WORLD),
        ]
        g = rows_table(rows, top=1.6, gap=0.42)
        with self.voiceover(
            "So there are two frame problems. <bookmark mark='a'/>The logical one, representing compactly what an "
            "action does not change, is largely solved, by circumscription in 1980 and successor-state axioms in "
            "1991, as Murray Shanahan's survey of the field concludes. <bookmark mark='b'/>The philosophical one is "
            "not: deciding, in a situation never met before, what is relevant, without first considering "
            "everything. <bookmark mark='c'/>Jerry Fodor argued in 1983 that this is a problem about all of "
            "thinking. Belief fixation is isotropic: anything you know might bear on anything else. And it is "
            "Quinean: how well a belief is confirmed depends on the whole system. No local rule can capture that. "
            "<bookmark mark='d'/>He called it Hamlet's problem: when to stop thinking. <bookmark mark='e'/>And "
            "Dreyfus said the problem only arises for a reasoner that starts from neutral facts and must work out "
            "what matters. A skilled coper never starts there: it is already in a situation where things matter."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def wall_brick(self):
        w = wall(upto=29, current=29).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(29, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "This is the twenty-ninth brick in the Wall. <bookmark mark='a'/>The dream was relevance by rule: a "
            "finite set of explicit rules that tells a reasoner, in any situation, what matters and what can be "
            "ignored. The frame problem, in its philosophical form, says no such set has been found, and gives "
            "reasons to think none can be. <bookmark mark='b'/>What it forces is attention to background know-how: "
            "the skills, habits and learned sensitivities that settle relevance before any rule is applied, "
            "whether in people or in machines that learn."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(card), Indicate(w.brick[29], color=P.CONCL, scale_factor=1.06))
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()

    def price(self):
        d = load("frame")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert sorted(d["mcs"]) == [["E"], ["H"], ["R"]] and d["mus"] == [["E", "H", "R"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.3, width=4.2, font_size=19,
                       center=[0, -0.6, 0], title=r"The Price List: \ the frame problem")
        positions = [(("E",), r"Dreyfus", r"intelligence is skilled coping, \ not rules over representations"),
                     (("R",), r"the logicists", r"with the right formalism, \ finitely many rules do settle "
                                                r"relevance"),
                     (("H",), r"bounded rationality", r"people do not either: \ they satisfice, \ and get relevance "
                                                      r"wrong outside familiar niches")]
        with self.voiceover(
            "Three claims cannot all be true. <bookmark mark='a'/>Intelligent action is guided by explicit rules "
            "over explicit representations. No finite set of explicit rules settles what is relevant in every "
            "situation. And people do pick out what is relevant, in every situation they meet. If the first and third "
            "are true, the rules people follow are a finite set that settles relevance, and the second is false. "
            "<bookmark mark='b'/>Something has to give. <bookmark mark='c'/>Dreyfus gives up the first: "
            "intelligence is skilled coping, not rules over representations. <bookmark mark='d'/>The logicists, from "
            "McCarthy on, give up the second: with the right formalism, and the right defaults, a finite set of rules "
            "can settle relevance. <bookmark mark='e'/>And a follower of Herbert Simon can give up the third. People "
            "do not solve the problem either. They satisfice, settling for good enough, and outside the niches their "
            "habits were shaped for they get relevance wrong all the time."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cde", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()
