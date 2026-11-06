from __future__ import annotations

from videos.philosophy.philosophy35.common import *  # noqa: F403


class Deontology(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Constraints", r"Can it be wrong to minimize wrongdoing?", lit=(1930, 1982),
                            part=PART)
        with self.voiceover("Chapter seven. Constraints."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.ross()
        self.doing()
        self.paradox()
        self.consequentialize()
        self.wall_brick()

    def ross(self):
        hc = history_card(1930, r"W. D. Ross", r"\textit{The Right and the Good}", width=5.0, color=HIST).to_corner(
            UL, buff=0.3)
        duties = stack([(r"fidelity: \ keep promises", DUTY), (r"reparation: \ make up for wrongs", DUTY),
                        (r"gratitude", DUTY), (r"justice", DUTY), (r"beneficence: \ do good", GOOD),
                        (r"self-improvement", VIRT), (r"non-maleficence: \ do no harm", HARM)], font_size=19,
                       aligned_edge=LEFT, buff=0.18).move_to([-3.6, -0.8, 0])
        side = stack([(r"prima facie duties: \ each a real reason, \ any can be outweighed", GREY_A),
                      (r"no master principle ranks them: \ judgment in the case decides", GOAL),
                      (r"constraints: \ limits on what you may do, \ even to bring about the best outcome", DUTY),
                      (r"options: \ permission not to do the best, \ at great cost to yourself", VIRT)],
                     font_size=19, aligned_edge=LEFT, width=5.4, buff=0.3).move_to([3.4, -0.4, 0])
        with self.voiceover(
            "The deontology most philosophers hold is not Kant's but W. D. Ross's, from The Right and the Good of "
            "1930. <bookmark mark='a'/>There are several prima facie duties: fidelity, reparation, gratitude, justice, "
            "beneficence, self-improvement, and not harming others. <bookmark mark='b'/>Each gives a genuine reason; "
            "any can be outweighed by another; <bookmark mark='c'/>and no master principle ranks them, so judgment "
            "in the particular case must decide. <bookmark mark='d'/>What marks deontology off from consequentialism "
            "are constraints, limits on what you may do even to bring about the best outcome, "
            "<bookmark mark='e'/>and options, permissions not to do the best when it would cost you greatly."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in duties], lag_ratio=0.2), run_time=2)
            for mk, r in zip("bcde", side):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def doing(self):
        head = label(r"Doing and allowing", font_size=30, color=CONN).to_edge(UP, buff=0.3)

        def card(name, rows, col, x):
            t = label(name, font_size=22, color=col)
            items = VGroup(*[label(r, font_size=17, color=c) for r, c in rows]).arrange(DOWN, buff=0.2,
                                                                                       aligned_edge=LEFT)
            g = VGroup(t, items).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
            box = SurroundingRectangle(g, buff=0.25, color=col, stroke_width=2, corner_radius=0.1)
            return VGroup(box, g).move_to([x, 1.15, 0])

        smith = card(r"Smith", [(r"gains an inheritance if his cousin dies", GREY_A),
                                (r"drowns the child in the bath", HARM), (r"the child dies", GREY_A)], HARM, -3.3)
        jones = card(r"Jones", [(r"gains an inheritance if his cousin dies", GREY_A),
                                (r"watches him drown, \ ready to push him under", DUTY),
                                (r"the child dies", GREY_A)], DUTY, 3.0)
        diff = VGroup(SurroundingRectangle(smith[1][1][1], buff=0.08, color=WHITE, stroke_width=1.5),
                      SurroundingRectangle(jones[1][1][1], buff=0.08, color=WHITE, stroke_width=1.5))
        rach = label(r"Rachels \ (1975): \ equally monstrous, \ so the bare difference makes no difference",
                     font_size=18, color=GOOD).move_to([0, -0.45, 0])
        quinn = stack([(r"Quinn \ (1989): \ save five drowning people rather than one: \ permitted", GOOD),
                       (r"reach the five only by driving over the one: \ forbidden", HARM)],
                      font_size=18, aligned_edge=LEFT, buff=0.15).move_to([0, -1.45, 0])
        kagan = label(r"Kagan \ (1988): \ the additive fallacy: \ a factor need not weigh the same in every context",
                      font_size=18, color=VIRT).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Most constraints rest on the distinction between doing harm and allowing it. <bookmark mark='a'/>James "
            "Rachels challenged it in 1975 with a pair of cases. Smith will inherit a fortune if his six-year-old "
            "cousin dies, and drowns the child in the bath. <bookmark mark='b'/>Jones stands to gain in the same "
            "way and creeps in to do the same, but the child slips, hits his head and falls face down in the water. "
            "Jones watches, ready to push him back under, and does nothing. <bookmark mark='c'/>The cases differ only "
            "in killing against letting die, and both men are equally monstrous. So, Rachels concluded, the bare "
            "difference makes no moral difference. <bookmark mark='d'/>Warren Quinn's rescue cases, of 1989, point "
            "the other way. If you can save five drowning people or one, you may save the five and let the one "
            "drown. But if you can reach the five only by driving over the one, you may not. Here the difference "
            "decides everything. <bookmark mark='e'/>Shelly Kagan diagnosed the conflict in 1988 as the additive "
            "fallacy: the assumption that a factor contributes the same moral weight in every context. A factor can "
            "matter in one setting and fall silent in another. That is the holism of reasons, which returns with "
            "virtue ethics."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(smith))
            vo.wait_until("b")
            self.play(FadeIn(jones))
            vo.wait_until("c")
            self.play(Create(diff), FadeIn(rach))
            vo.wait_until("d")
            self.play(FadeIn(quinn[0]))
            self.play(FadeIn(quinn[1]))
            vo.wait_until("e")
            self.play(FadeIn(kagan))
        self.clear_scene()

    def paradox(self):
        d = load("paradox")
        head = label(r"The paradox of deontology \ (Scheffler, \ 1982; \ Nozick, \ 1974)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        assert d["victims"] == 5 and d["threshold"] == 5
        you = VGroup(Circle(radius=0.4, color=DUTY, fill_opacity=0.2), label(r"you", font_size=18, color=DUTY))
        one = VGroup(Circle(radius=0.32, color=HARM, fill_opacity=0.2), label(r"1", font_size=18, color=HARM))
        killers = VGroup(*[VGroup(Circle(radius=0.3, color=GREY_B, fill_opacity=0.15),
                                  label(r"K", font_size=16, color=GREY_B)) for _ in range(5)]).arrange(RIGHT, buff=0.3)
        victims = VGroup(*[VGroup(Circle(radius=0.3, color=HARM, fill_opacity=0.15),
                                  label(r"v", font_size=16, color=HARM)) for _ in range(5)]).arrange(RIGHT, buff=0.3)
        you.move_to([-4.6, 1.2, 0])
        one.move_to([-4.6, -0.6, 0])
        killers.move_to([0.6, 1.2, 0])
        victims.move_to([0.6, -0.6, 0])
        a1 = Arrow(you.get_bottom(), one.get_top(), buff=0.1, color=DUTY)
        a2 = VGroup(*[Arrow(k.get_bottom(), v.get_top(), buff=0.1, color=GREY_B, stroke_width=2)
                      for k, v in zip(killers, victims)])
        side = stack([(r"kill one innocent, \ or five others each kill one", GREY_A),
                      (r"fewer killings: \ 1 against 5", GOOD),
                      (r"the constraint: \ you may not kill the one", DUTY),
                      (r"if killing is so bad, \ why not minimize killings? \ the constraint seems irrational", BAD)],
                     font_size=19, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Constraints produce a paradox, stated by Robert Nozick in 1974 and sharpened by Samuel Scheffler in "
            "1982. <bookmark mark='a'/>Suppose you can kill one innocent person, and thereby prevent five others from "
            "each killing one. <bookmark mark='b'/>If you kill, there is one killing; if you refrain, five. "
            "<bookmark mark='c'/>A constraint against killing says you may not. <bookmark mark='d'/>But if killing is "
            "so bad that you may not do it even to prevent worse, why is it not better to minimize killings? A "
            "constraint seems to say that you should care more about your own hands being clean than about the "
            "killings themselves."
        ) as vo:
            self.play(FadeIn(head), FadeIn(you), FadeIn(one), FadeIn(killers), FadeIn(victims))
            vo.wait_until("a")
            self.play(GrowArrow(a1), *[GrowArrow(a) for a in a2], FadeIn(side[0]))
            for mk, r in zip("bcd", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def consequentialize(self):
        d = load("paradox")
        head = label(r"Consequentializing the constraint", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = d["rows"]
        assert [r["verdict"] for r in rows] == ["kill", "kill", "either", "refrain", "refrain"]
        f = MathTex(r"\text{badness}_{\text{you}}(o) \;=\; k \cdot (\text{killings by you}) + (\text{killings by "
                    r"others})", font_size=30, color=AGG).next_to(head, DOWN, buff=0.35)
        hd = [r"k", r"\text{you kill}", r"\text{you refrain}", r"\text{verdict}"]
        cells = [[label(str(r["k"]), font_size=19), label(str(r["kill"]), font_size=19, color=HARM),
                  label(str(r["refrain"]), font_size=19, color=GREY_A),
                  label(r["verdict"], font_size=19, color=DUTY if r["verdict"] == "refrain" else GOOD)]
                 for r in rows]
        grid = ValueGrid(hd, cells, col_w=[1.2, 2.2, 2.4, 2.2], cell_h=0.5, font_size=18).move_to([-2.4, -1.0, 0])
        side = stack([(r"rank outcomes agent-relatively: \ your killings count $k$ times", AGG),
                      (r"for $k > 5$ the ranking says refrain: \ exactly the constraint", DUTY),
                      (r"Dreier \ (1993); \ Portmore \ (2011): \ every deontology can be consequentialized", GOAL),
                      (r"critics: \ then `consequentialism' marks no substantive view", HARM)], font_size=18,
                     aligned_edge=LEFT, width=4.8, buff=0.3).move_to([4.0, -1.0, 0])
        with self.voiceover(
            "One reply dissolves the contrast. <bookmark mark='a'/>Let each agent rank outcomes from her own point of "
            "view, counting her own killings k times as heavily as other people's. <bookmark mark='b'/>With k equal "
            "to one, killing the one is better; at five the options tie; <bookmark mark='c'/>for any k above five, "
            "refraining is better, which is exactly the constraint. <bookmark mark='d'/>James Dreier and Douglas "
            "Portmore argued that every deontological theory can be consequentialized this way, by building "
            "agent-relative values into the ranking. <bookmark mark='e'/>Critics answer that if every theory can be "
            "written so, calling a theory consequentialist says nothing about what it requires."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for c in grid.cell[0]],
                      *[FadeIn(c) for c in grid.cell[1]], *[FadeIn(c) for c in grid.cell[2]])
            vo.wait_until("c")
            self.play(*[FadeIn(c) for c in grid.cell[3]], *[FadeIn(c) for c in grid.cell[4]], FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def wall_brick(self):
        w = wall(upto=35, current=35).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(35, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "This is the thirty fifth brick in the Wall. <bookmark mark='a'/>The dream was a moral theory that "
            "matches every considered intuition. Harsanyi's theorem shows that two mild conditions of rationality "
            "force the utilitarian sum, with all its indifference to who gets what; deontology avoids that, but "
            "only by constraints that seem to forbid minimizing the very wrongs they condemn; and every test of "
            "maxims we built either forbids the innocent or permits the wrong. <bookmark mark='b'/>What it forces is "
            "a choice: some intuition must go."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(card), Indicate(w.brick[35], color=P.CONCL, scale_factor=1.06))
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()
