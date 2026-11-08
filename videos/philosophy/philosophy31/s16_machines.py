from __future__ import annotations

from videos.philosophy.philosophy31.common import *  # noqa: F403


class Machines(VoiceoverScene):
    def construct(self):
        card = chapter_card(15, r"Could a machine be conscious?", r"What would count as evidence?", lit=(2023,),
                            part=PART)
        with self.voiceover("Chapter fifteen. Could a machine be conscious?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.indicators()
        self.toys()
        self.reports()
        self.welfare()

    def indicators(self):
        d = load("indicators")
        head = label(r"Fourteen indicator properties \ (Butlin, \ Long et al., \ 2023)", font_size=28,
                     color=CONN).to_edge(UP, buff=0.3)
        assert d["total"] == 14
        theories = {}
        for r in d["indicators"]:
            theories.setdefault(r["theory"], []).append(r)
        cols = {"recurrent processing": SIG, "global workspace": FUNC, "higher-order": SELF,
                "attention schema": FEEL, "predictive processing": PRED, "agency and embodiment": OK}
        rows = VGroup()
        for th, items in theories.items():
            rows.add(VGroup(label(th, font_size=18, color=cols[th]),
                            VGroup(*[label(rf"\texttt{{{r['code']}}} \ {r['text']}", font_size=15, color=GREY_A)
                                     for r in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
                            ).arrange(RIGHT, buff=0.3, aligned_edge=UP))
        for r in rows:
            r[1].shift(RIGHT * (3.2 - r[0].width))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, -0.35, 0])
        foot = label(r"assuming computational functionalism: \ the right computations would suffice", font_size=18,
                     color=GOAL).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "In 2023 nineteen researchers led by Patrick Butlin and Robert Long asked what the science of "
            "consciousness implies for AI. <bookmark mark='a'/>Assuming computational functionalism, that the right "
            "computations would suffice, they drew fourteen indicator properties from the leading theories. "
            "<bookmark mark='b'/>From recurrent processing theory, recurrence in perception. From the global "
            "workspace, specialised modules, a limited-capacity workspace, global broadcast, and attention that "
            "queries modules in turn. From higher-order theories, metacognitive monitoring of perception, among "
            "others. <bookmark mark='c'/>One from attention schema theory, one from predictive processing, and two "
            "from agency and embodiment. <bookmark mark='d'/>Their conclusion: no current AI system was a strong "
            "candidate for consciousness, but there were no obvious technical barriers to building systems that "
            "satisfy many of the indicators."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(foot))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:3]], lag_ratio=0.4), run_time=3)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[3:]], lag_ratio=0.4), run_time=2)
            vo.wait_until("d")
            self.play(Indicate(rows, color=GOAL, scale_factor=1.01))
        self.clear_scene()

    def toys(self):
        d = load("indicators")
        head = label(r"The Reasoner's own toys, \ checked", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["distinct"] == 6 and all(len(v) == 2 for v in d["met"].values())
        hd = [r"\text{toy}", r"\text{indicators met}", r"\text{because}"]
        cells = []
        for toy, codes in d["met"].items():
            why = d["reasons"][toy]
            cells.append([label(toy, font_size=17, color=WHITE),
                          label(r", \ ".join(rf"\texttt{{{c}}}" for c in codes), font_size=17, color=FUNC),
                          VGroup(*[label(why[c], font_size=15, color=GREY_A) for c in codes]).arrange(
                              DOWN, aligned_edge=LEFT, buff=0.06)])
        grid = ValueGrid(hd, cells, col_w=[4.2, 2.6, 6.0], cell_h=0.95, font_size=18).move_to([0, 0.0, 0])
        foot = stack([(r"each toy meets 2 of the 14; \ together, \ 6; \ each is a few dozen lines of code", SIG),
                      (r"indicators are evidence that adds up, \ not a test that is passed", GOAL)], font_size=20,
                     buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The Reasoner can check its own toys against the list, by reading its own code. "
            "<bookmark mark='a'/>The workspace of chapter eight has recurrence, and a bottleneck that a stimulus "
            "must pass through: two indicators. The metacognitive observer of chapter nine has a noisy perception "
            "and a monitor of its reliability: two more. The T-maze agent predicts its observations, and models how "
            "its moves change them: two more. <bookmark mark='b'/>Six indicators between them, in a few dozen lines "
            "each, and no one thinks any of them is conscious. <bookmark mark='c'/>That is not a flaw in the "
            "method, which its authors anticipated. Indicators are evidence that adds up as more of them are met, "
            "and met together, in one system. They are not a test that a system passes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            for r in range(3):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.7)
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def reports(self):
        head = label(r"Why a model's self-reports are weak evidence", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"the training", r"language models learn from human writing, \ full of talk about experience",
                 GREY_A),
                (r"the gaming problem", r"a system trained on our behaviour can produce the markers without what "
                                        r"they mark \ (Birch and Andrews)", BAD),
                (r"the meta-problem", r"chapter 6: \ the reports need explaining; \ for a model, \ the training "
                                      r"already explains them", SELF),
                (r"what would help", r"architecture and mechanism, \ not testimony: \ which computations, \ in what "
                                     r"structure", FUNC)]
        g = rows_table(rows, top=1.6, gap=0.5)
        with self.voiceover(
            "What about simply asking? <bookmark mark='a'/>A language model will talk fluently about its inner "
            "life, or deny having one, depending on how it was trained, because it learned from human writing, "
            "full of talk about experience. <bookmark mark='b'/>Jonathan Birch and Kristin Andrews call this the "
            "gaming problem: a system trained to reproduce our behaviour can produce the behavioural markers of "
            "consciousness without what they mark. <bookmark mark='c'/>In the terms of chapter six, the reports "
            "need explaining, and for a model the training already explains them, whether or not anything is felt. "
            "<bookmark mark='d'/>So the evidence that matters is about mechanism and architecture: which "
            "computations happen, in what structure, which is where the indicators and the theories come back in."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def welfare(self):
        head = label(r"Taking the possibility seriously", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"Chalmers \ (2023)", r"current language models are unlikely to be conscious; \ successors with "
                                       r"recurrence, \ a workspace and unified agency might be", GREY_A),
                (r"Long, \ Sebo et al. \ (2024)", r"`Taking AI Welfare Seriously': \ a realistic possibility, \ not a "
                                                 r"certainty, \ in the near future", FEEL),
                (r"what they ask", r"acknowledge the question; \ assess systems for the markers; \ prepare policies",
                 OK),
                (r"two errors", r"treating a conscious system as a tool, \ or a tool as a someone: \ both have costs",
                 BAD)]
        g = rows_table(rows, top=1.6, gap=0.5)
        with self.voiceover(
            "Where does that leave us? <bookmark mark='a'/>Chalmers argued in 2023 that current language models are "
            "unlikely to be conscious, but that successors with recurrence, a workspace and unified agency might "
            "be. <bookmark mark='b'/>In 2024 Robert Long, Jeff Sebo and colleagues argued that there is a realistic "
            "possibility, not a certainty, that some AI systems will be conscious or robustly agentic in the near "
            "future, and so have interests that matter morally. <bookmark mark='c'/>They asked AI developers to "
            "acknowledge the question, to assess their systems for the relevant markers, and to prepare policies. "
            "<bookmark mark='d'/>Under this kind of uncertainty there are two ways to be wrong: to treat a conscious "
            "system as a mere tool, or to treat a tool as someone. Both have costs, and the next parts on agency, "
            "value and fair machines return to how to weigh them."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
