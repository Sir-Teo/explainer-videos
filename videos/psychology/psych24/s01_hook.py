from __future__ import annotations

from videos.psychology.psych24.common import *  # noqa: F403


def card(face: str, color=WHITE, w: float = 1.5, h: float = 2.1, font_size: int = 54) -> VGroup:
    """A playing card with one face showing."""
    box = RoundedRectangle(corner_radius=0.15, width=w, height=h, stroke_color=GREY_B, stroke_width=2,
                           fill_color="#1B2230", fill_opacity=1)
    return VGroup(box, label(face, font_size=font_size, color=color).move_to(box))


class Hook(VoiceoverScene):
    def construct(self):
        self.abstract()
        self.answer()
        self.drinking()
        self.question()
        self.objectives()

    def abstract(self):
        stage = demo_stage(12.4, 5.6, center=[0, 0.1, 0])
        rule = label(r"Rule: \ if a card has a \emph{vowel} on one side, \ it has an \emph{even number} on the other.",
                     font_size=32, color=LOGIC).move_to([0, 1.9, 0])
        cards = VGroup(*[card(f) for f in ("E", "K", "4", "7")]).arrange(RIGHT, buff=0.7).move_to([0, -0.2, 0])
        note = label(r"each card has a letter on one side and a number on the other", font_size=24,
                     color=GREY_A).next_to(cards, DOWN, buff=0.45)
        ask = label(r"Which cards must you turn over to find out whether the rule is true? \ Only those.",
                    font_size=28, color=YOU).to_edge(DOWN, buff=0.75)
        with self.voiceover(
            "Let's start with a puzzle, on you. <bookmark mark='a'/> Here are four cards. Each has a letter on one "
            "side and a number on the other. <bookmark mark='b'/> And here's a rule about them: if a card has a "
            "vowel on one side, it has an even number on the other. <bookmark mark='c'/> Which cards must you turn "
            "over to find out whether the rule is true? Turn only the cards you need. Pause the video if you like, "
            "and choose."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.3), FadeIn(note))
            vo.wait_until("b")
            self.play(Write(rule))
            vo.wait_until("c")
            self.play(FadeIn(ask))
        self.wait(5.0)
        self.cards, self.rule, self.stage, self.note, self.ask = cards, rule, stage, note, ask

    def answer(self):
        cards = self.cards
        why = rows_of([
            (r"E: \ an odd number behind it would break the rule", GOOD),
            (r"7: \ a vowel behind it would break the rule", GOOD),
            (r"4: \ the rule says nothing about what is behind an even number", LOST),
        ], 5.6, 25, 0.3)
        stat = wrapped_label(r"Wason, \ 1966 and 1968: \ about one person in ten chooses E and 7", 5.6, 25,
                             DATA)
        side = VGroup(why, stat).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        tag = historical_tag(r"Wason (1966, \ 1968)")
        with self.voiceover(
            "Most people turn over the E, and many turn over the 4 as well. <bookmark mark='a'/> The answer is the E "
            "and the 7. The E, because an odd number behind it would break the rule. The 7, because a vowel behind "
            "it would break the rule too. <bookmark mark='b'/> The 4 can't break it: the rule says nothing about "
            "what's behind an even number. <bookmark mark='c'/> When Peter Wason set this task in the 1960s, about "
            "one person in ten chose the E and the 7. Students of logic did little better."
        ) as vo:
            self.play(FadeIn(tag), FadeOut(self.stage), FadeOut(self.note), FadeOut(self.ask),
                      cards.animate.scale(0.7).move_to([-3.6, -0.1, 0]),
                      self.rule.animate.scale(0.85).move_to([0, 2.3, 0]))
            marks = VGroup(*[SurroundingRectangle(cards[k], color=GOOD, buff=0.08, corner_radius=0.15)
                             for k in (0, 3)])
            wrong = SurroundingRectangle(cards[2], color=LOST, buff=0.08, corner_radius=0.15)
            side.move_to([3.3, -0.1, 0])
            vo.wait_until("a")
            self.play(Create(marks), FadeIn(why[0]), FadeIn(why[1]))
            vo.wait_until("b")
            self.play(Create(wrong), FadeIn(why[2]))
            vo.wait_until("c")
            self.play(FadeIn(stat, shift=UP * 0.1))
        self.clear_scene()

    def drinking(self):
        stage = demo_stage(12.4, 5.6, center=[0, 0.1, 0])
        rule = label(r"Rule: \ if a person is drinking \emph{beer}, \ they must be \emph{over 18}.", font_size=32,
                     color=CONTENT).move_to([0, 1.9, 0])
        faces = [(r"beer", CONTENT), (r"cola", CONTENT), (r"25", WHITE), (r"16", WHITE)]
        cards = VGroup(*[card(f, c, font_size=40) for f, c in faces]).arrange(RIGHT, buff=0.7).move_to([0, -0.2, 0])
        note = label(r"each card is a person: \ what they drink on one side, \ their age on the other",
                     font_size=24, color=GREY_A).next_to(cards, DOWN, buff=0.45)
        marks = VGroup(*[SurroundingRectangle(cards[k], color=GOOD, buff=0.08, corner_radius=0.15) for k in (0, 3)])
        stat = label(r"Griggs \& Cox, \ 1982: \ about three people in four choose \emph{beer} and \emph{16}",
                     font_size=26, color=DATA).to_edge(DOWN, buff=0.75)
        tag = published_tag(r"Griggs \& Cox (1982)")
        with self.voiceover(
            "Now a second puzzle. <bookmark mark='a'/> You're checking a bar. Each card is a person: what they're "
            "drinking on one side, their age on the other. The rule: if a person is drinking beer, they must be over "
            "eighteen. Which cards must you turn over? <bookmark mark='b'/> Almost everyone sees it at once. The beer "
            "drinker, to check their age, and the sixteen-year-old, to check their drink. <bookmark mark='c'/> In "
            "1982 Richard Griggs and James Cox found that about three people in four got this version right. "
            "<bookmark mark='d'/> Yet it has exactly the logical form of the first: if P then Q, and the cards to "
            "turn are P and not-Q."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(rule), LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.3),
                      FadeIn(note))
            vo.wait_until("b")
            self.play(Create(marks))
            vo.wait_until("c")
            self.play(FadeIn(stat))
            vo.wait_until("d")
            form = label(r"the same form: \ if $P$ then $Q$; \ turn $P$ and not-$Q$", font_size=28, color=LOGIC)
            form.next_to(stat, UP, buff=0.25)
            self.play(FadeIn(form))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ are people logical, \ and if not, \ what are they instead?")
        rows = rows_of([
            (r"deduction: \ syllogisms on 139 people's answers, \ and what logic, \ rules and shortcuts predict", LOGIC),
            (r"why content helps: \ cheaters, \ permissions, \ and the information in each card", CONTENT),
            (r"problem solving as search: \ states, \ moves, \ a production system, \ and insight", SEARCH),
            (r"expertise, \ analogy and mental imagery, \ fitted to open data", INSIGHT),
            (r"causes and everyday predictions, \ and the bounded mind that makes them", MODEL),
        ], 12.6, 27, 0.4).move_to([0, -0.3, 0])
        with self.voiceover(
            "The difference between those two puzzles is the subject of this part. <bookmark mark='a'/> We'll start "
            "with deduction, the oldest kind of reasoning, with the answers of a hundred and thirty-nine people to "
            "every syllogism there is. <bookmark mark='b'/> Then why content helps so much, and an argument that the "
            "wrong cards may not be so wrong after all. <bookmark mark='c'/> Then problem solving as search, from "
            "Newell and Simon to the moment of insight. <bookmark mark='d'/> Then expertise, analogy, and the mind's "
            "eye. <bookmark mark='e'/> And finally reasoning about causes and about everyday life, and the bounded "
            "mind that does it."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 24", font_size=34, color=GREY_B), label(r"Reasoning and Problem Solving",
                                                                            font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"syllogisms: \ validity by brute force, \ and four accounts scored on open data",
            r"the selection task, \ content effects, \ and optimal data selection derived",
            r"the Tower of Hanoi's state space, \ a production system, \ and the nine dots",
            r"chess memory, \ deliberate practice, \ and structure mapping",
            r"mental rotation fitted to 54 people, \ and causal power",
            r"Bayesian everyday predictions, \ and bounded rationality",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 24 of Psychology, Built, the seventh part of Act Five, on thinking: reasoning and problem "
            "solving. <bookmark mark='a'/> We'll find every valid syllogism by brute force and test four accounts of "
            "what people answer instead. We'll derive the information each card carries. We'll draw the whole space "
            "of a puzzle and watch a production system climb through it. We'll prove that the nine-dot puzzle can't "
            "be solved inside the box. We'll fit mental rotation to the open data of fifty-four people, and finish "
            "with causes, everyday predictions and the limits of a mind that has to decide in time."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=24.0)
        self.clear_scene()
