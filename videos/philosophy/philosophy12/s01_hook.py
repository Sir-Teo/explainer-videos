from __future__ import annotations

from videos.philosophy.philosophy12.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.island()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = VGroup(MathTex(r"K_a\,p, \quad K_b K_a\,p, \quad K_a K_b K_a\,p, \quad K_b K_a K_b K_a\,p, \quad \dots",
                           font_size=40, color=COMMON),
                   label(r"I know that you know that I know \dots", font_size=24, color=GREY_A)).arrange(
            DOWN, buff=0.25).next_to(t, DOWN, buff=0.7)
        with self.voiceover(
            "Part 11 asked what it is for one person to know something. <bookmark mark='a'/>Part 12 asks what happens "
            "when there are many of us: when I know what you know, and you know that I know it, and so on. "
            "<bookmark mark='b'/>Some of the oldest puzzles in logic, and some of the newest theorems in computer "
            "science, live here."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=COMMON, scale_factor=1.03))
        self.clear_scene()

    def island(self):
        head = label(r"A sentence everyone already knew", font_size=34, color=CONN).to_edge(UP, buff=0.4)
        kids = VGroup(*[person(n, color=WHITE, scale=0.9, face=(LOSS if m else None)) for n, m in
                        ((r"Ann", 1), (r"Bob", 1), (r"Cy", 0))]).arrange(RIGHT, buff=1.6).move_to([0, 0.7, 0])
        father = label(r"`at least one of you has mud on your forehead'", font_size=26, color=COMMON).next_to(
            kids, DOWN, buff=0.6)
        rows = VGroup(
            label(r"each child sees the others, \ not herself: \ everyone already knew it", font_size=24),
            label(r"yet after it is said aloud, \ the muddy children can work out that they are muddy",
                  font_size=24, color=KNOW),
            label(r"what changed? \ not what anyone knew, \ but what everyone knew that everyone knew",
                  font_size=25, color=GOAL)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is the puzzle that runs through this part. <bookmark mark='a'/>Three children have been playing; "
            "two of them, Ann and Bob, have mud on their foreheads. Each can see the others' foreheads but not her "
            "own. <bookmark mark='b'/>Their father says: at least one of you has mud on your forehead. "
            "<bookmark mark='c'/>Every child already knew that: each could see a muddy face. <bookmark mark='d'/>Yet "
            "after the father says it aloud, and asks a few times who knows whether they are muddy, the muddy "
            "children can work it out, and without his sentence they never could. <bookmark mark='e'/>What did the "
            "sentence change? Not what anyone knew. It changed what everyone knew that everyone knew, all the way "
            "up. That is common knowledge, and it turns out to be the hinge of conventions, of contracts, of markets, "
            "and of every computer network that has to agree on anything."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(k) for k in kids], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(father))
            for mk, r in zip("cde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"knowledge as a box: \ Hintikka's logic, \ and its critics",
            r"many agents in one model; \ the muddy children, \ solved by the Reasoner",
            r"common knowledge, \ and why messages can never create it \ (the Wall)",
            r"machines that must agree: \ Byzantine generals, \ FLP, \ Paxos; \ the email game",
            r"Aumann: \ no agreeing to disagree; \ secrets, \ lies, \ and Fitch's unknowable truths",
            r"testimony, \ peer disagreement, \ the wisdom of crowds",
            r"networks of scientists: \ when less talk finds more truth",
        ], font_size=25)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Knowledge as a box, Hintikka's logic of knowledge. <bookmark mark='b'/>Many "
            "agents in one model, and the muddy children solved. <bookmark mark='c'/>Common knowledge, and the theorem "
            "that no exchange of messages over an unreliable channel can create it: this part's brick in the Wall. "
            "<bookmark mark='d'/>The engineers who build systems that must agree anyway. <bookmark mark='e'/>Aumann's "
            "theorem that rational people cannot agree to disagree; private messages and lies; and Fitch's proof that "
            "some truths cannot be known. <bookmark mark='f'/>Then knowledge from other people: testimony, "
            "disagreement and crowds. <bookmark mark='g'/>And communities of scientists, where, the Reasoner finds, "
            "less communication can find more truth."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
