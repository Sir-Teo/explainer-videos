from __future__ import annotations

from videos.psychology.psych35.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.machines()
        self.perturbed()
        self.open_questions()

    def card(self):
        card = chapter_card(14, r"Frontier: \ minds in machines", r"Can a language model pass a false-belief test?",
                            lit={2023: r"Ullman", 2024: r"Kosinski"}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter fourteen. Frontier: minds in machines."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def machines(self):
        head = heading(r"False-belief tasks for language models")
        A = axes([-0.6, 1.6], [0, 100], x_length=4.4, y_length=3.6, xticks=None, yticks=[0, 25, 50, 75, 100],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"tasks solved", center=[-3.9, -0.3, 0], font_size=15)
        b = bars(A.ax, [0, 1], [20, 75], [CROWD, MODEL], width=0.6)
        names = VGroup(label(r"GPT-3.5", font_size=16, color=CROWD).next_to(A.ax.c2p(0, 0), DOWN, buff=0.15),
                       label(r"GPT-4", font_size=16, color=MODEL).next_to(A.ax.c2p(1, 0), DOWN, buff=0.15))
        tops = VGroup(label(r"20\%", font_size=18, color=CROWD).next_to(A.ax.c2p(0, 20), UP, buff=0.1),
                      label(r"75\%", font_size=18, color=MODEL).next_to(A.ax.c2p(1, 75), UP, buff=0.1))
        rows = rows_of([
            (r"Kosinski, \ 2024, \ \emph{PNAS}: \ 40 false-belief tasks, \ each with controls, \ 640 prompts in all",
             WHITE),
            (r"a 2023 version of GPT-4 solved 75\% of the tasks; \ GPT-3.5 solved 20\%", MODEL),
            (r"the claim: \ the ability to track false beliefs may have emerged in language models as a by-product "
             r"of learning language", CROWD),
            (r"the claim was disputed", YOU),
        ], 6.2, 20, 0.36).move_to([3.0, -0.3, 0])
        tag = published_tag(r"Kosinski (2024)")
        with self.voiceover(
            "The newest minds to be read are machines. <bookmark mark='a'/> In 2024 Michal Kosinski gave large "
            "language models forty false-belief tasks of the kind in chapter nine, each with controls, six hundred "
            "and forty prompts in all. <bookmark mark='b'/> A 2023 version of GPT-4 solved seventy-five percent of "
            "the tasks. GPT-3.5 solved twenty percent. <bookmark mark='c'/> His claim was that tracking false "
            "beliefs may have emerged in language models as a by-product of learning language. "
            "<bookmark mark='d'/> The claim was disputed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b[0], DOWN), GrowFromEdge(b[1], DOWN), FadeIn(tops), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def perturbed(self):
        head = heading(r"Small changes, \ different answers")
        a = VGroup(word_chip(r"the standard task", color=GOOD, font_size=22, width=5.4),
                   wrapped_label(r"a bag full of popcorn is labelled ``chocolate''; \ she has never seen inside; \ "
                                 r"what does she think it holds?", 5.4, 20, WHITE)).arrange(DOWN, buff=0.3)
        b = VGroup(word_chip(r"a small alteration", color=AUTH, font_size=22, width=5.4),
                   wrapped_label(r"the same, \ but the bag is made of clear plastic: \ now she can see the popcorn", 5.4,
                                 20, WHITE)).arrange(DOWN, buff=0.3)
        VGroup(a, b).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to([0, 1.3, 0])
        rows = rows_of([
            (r"Ullman, \ 2023: \ alterations like this, \ which keep the principles of theory of mind, \ flipped "
             r"GPT-3.5's answers", WHITE),
            (r"his point: \ a pass on standard tasks is weak evidence when the tasks are in the training data; \ the "
             r"null hypothesis should be scepticism", YOU),
            (r"the same rule as chapter nine: \ the comparison task decides what you have found; \ Part 60 returns "
             r"with larger tests", MODEL),
        ], 12.0, 21, 0.3).move_to([0, -1.3, 0])
        tag = published_tag(r"Ullman (2023)")
        with self.voiceover(
            "How would you check? <bookmark mark='a'/> Take a standard task. A bag full of popcorn is labelled "
            "chocolate. She has never seen inside. What does she think it holds? <bookmark mark='b'/> Now make a "
            "small change. The bag is clear plastic, so she can see the popcorn. <bookmark mark='c'/> In 2023 Tomer "
            "Ullman showed that alterations like this, which keep the principles of theory of mind intact, flipped "
            "GPT-3.5's answers. <bookmark mark='d'/> His point was that passing standard tasks is weak evidence "
            "when the tasks are in the training data. The default should be scepticism. <bookmark mark='e'/> It's "
            "chapter nine's rule again: the comparison task decides what you've found. Part 60 returns with larger "
            "tests."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(FadeIn(b))
            for m, r in zip("cde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open_questions(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"what survives of social priming when every study is large, \ preregistered and timed by machine?",
             AUTH),
            (r"is the correspondence bias an error, \ or a reasonable bet in a world where situations are hard "
             r"to see?", CROWD),
            (r"how much of the Dunning-Kruger graph is insight, \ and how much is noise?", PERSON),
            (r"can inverse planning scale from mazes to the plans of real people over days?", MODEL),
            (r"what would count as evidence that a machine models minds, \ rather than text about minds?", YOU),
        ], 12.4, 24, 0.46).move_to([0, -0.2, 0])
        with self.voiceover(
            "So, open questions. <bookmark mark='a'/> What survives of social priming when every study is large, "
            "preregistered, and timed by machine? <bookmark mark='b'/> Is the correspondence bias an error, or a "
            "reasonable bet in a world where situations are hard to see? <bookmark mark='c'/> How much of the "
            "Dunning-Kruger graph is insight, and how much is noise? <bookmark mark='d'/> Can inverse planning scale "
            "from mazes to the plans of real people over days? <bookmark mark='e'/> And what would count as evidence "
            "that a machine models minds, rather than text about minds?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
