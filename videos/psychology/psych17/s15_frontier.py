from __future__ import annotations

from videos.psychology.psych17.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.solid()
        self.meta()
        self.open_()

    def card(self):
        card = chapter_card(14, r"Frontier: \ learning to learn", r"Does the brain contain a learner that learns "
                            r"how to learn?", lit={2018: r"Wang et al."}, part=PART, scale=("circuit", "mind"),
                            marr=("what", "how"))
        with self.voiceover("Chapter fourteen. The frontier: learning to learn."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def solid(self):
        head = heading(r"What is solid, \ and what is argued")
        left = rows_of([
            (r"what is solid", MODEL),
            (r"dopamine neurons carry reward prediction errors", WHITE),
            (r"errors at reward time teach, \ causally", WHITE),
            (r"rats and people learn maps without reward", WHITE),
            (r"place and grid cells", WHITE),
        ], 5.6, 26, 0.3)
        right = rows_of([
            (r"what is argued", BAD),
            (r"what ramps and movement signals mean", WHITE),
            (r"whether people are ever purely model-free", WHITE),
            (r"what the two-step weight measures", WHITE),
            (r"where the brain stores a model, \ and how it plans", WHITE),
        ], 5.6, 26, 0.3)
        g = VGroup(left, right).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to([0, 0.4, 0])
        with self.voiceover(
            "Here's where things stand. <bookmark mark='a'/> Solid: dopamine neurons carry reward prediction errors; "
            "an error at the time of reward teaches, causally; rats and people learn maps without reward; and place and "
            "grid cells exist. <bookmark mark='b'/> Argued: what dopamine ramps and movement signals mean; whether "
            "people are ever purely model-free; what the two-step task's weight really measures; and where the brain "
            "keeps its model of the world, and how it plans with it. One more question is at the frontier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(left[0]), FadeIn(right[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in left[1:]], lag_ratio=0.8), run_time=5.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in right[1:]], lag_ratio=0.8), run_time=5.0)
        self.clear_scene()

    def meta(self):
        head = heading(r"A learner inside the learner")
        rows = rows_of([
            (r"Harlow, \ 1949: \ monkeys given hundreds of different two-object problems got faster at each new one",
             WHITE),
            (r"by the end they solved a new problem in one trial: \ win-stay, \ lose-shift, \ on objects never seen",
             CUE),
            (r"2018: \ Wang and colleagues: \ dopamine slowly trains the prefrontal cortex's own dynamics", DELTA),
            (r"the trained network then learns each new task fast, \ by its activity, \ without changing its weights",
             MB),
            (r"a recurrent network trained this way reproduces Harlow's monkeys; \ meta-learning, \ Part 58", YOU),
        ], 12.4, 28, 0.38).move_to([0, -0.1, 0])
        tag = published_tag(archive.WANG_2018.cite)
        with self.voiceover(
            "The question is whether the brain contains a learner that learns how to learn. "
            "<bookmark mark='a'/> In 1949 Harry Harlow gave monkeys hundreds of small problems: two objects, one with "
            "a raisin under it. Each problem used new objects. The monkeys got faster and faster. "
            "<bookmark mark='b'/> By the end they solved a new problem in a single trial: if the first object paid, "
            "stay with it; if not, switch. They had learned a strategy, a learning set, not any particular answer. "
            "<bookmark mark='c'/> In 2018 Jane Wang, Matthew Botvinick and colleagues proposed how. Slow, "
            "dopamine-driven learning, of the kind this part describes, gradually tunes the dynamics of the "
            "prefrontal cortex. <bookmark mark='d'/> The tuned circuit then learns each new task quickly, in its "
            "pattern of activity, without needing to change its connections at all. <bookmark mark='e'/> A "
            "recurrent network trained this way behaves like Harlow's monkeys. Learning to learn is one theme of "
            "Part 58."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open_(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"how are states built? \ the TD story assumes the animal knows where it is; \ often it does not", CUE),
            (r"how does the brain represent time inside a trial? \ the delay line was a stand-in", VALUE),
            (r"what tells the brain when to plan and when to rely on habit? \ effort, \ uncertainty, \ stakes", MB),
            (r"can one learning rule explain human learning in a world of language and instruction?", YOU),
        ], 12.4, 29, 0.42).move_to([0, -0.1, 0])
        with self.voiceover(
            "And some questions nobody has answered. <bookmark mark='a'/> The TD story assumes the animal knows what "
            "state it's in. Often it doesn't, and building states, deciding which situations count as the same, may "
            "be the hardest part of learning. <bookmark mark='b'/> How does the brain represent time within a trial? "
            "The delay line was a stand-in. <bookmark mark='c'/> What decides when to plan and when to trust a "
            "habit? Proposals weigh the cost of thinking against what's at stake. <bookmark mark='d'/> And can any "
            "learning rule of this kind explain how people learn in a world of language, where one sentence can "
            "change what we expect? Part 16's frontier asked the same question from the other side."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
