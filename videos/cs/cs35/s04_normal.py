from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs35.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, load, rel_table)

NAMES = {"S": "student", "C": "course", "I": "instructor", "O": "office"}


def attrs(s: str) -> str:
    return r", \ ".join(rf"\textit{{{NAMES[c]}}}" for c in s)


class Normal(VoiceoverScene):
    def construct(self):
        self.card()
        self.anomalies()
        self.dependencies()
        self.decompose()

    def card(self):
        card = chapter_card(3, r"Dependencies and normal forms", r"What makes a table design wrong?",
                            lit=(1974,), extra=((1974, r"Armstrong; \ Boyce--Codd normal form"),), part=PART)
        with self.voiceover("Chapter three. Dependencies and normal forms."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def anomalies(self):
        n = load("normal")
        head = label(r"One table for everything", font_size=36).to_edge(UP, buff=0.3)
        tab = rel_table(["student", "course", "instructor", "office"], n["rows"], font=19).next_to(head, DOWN,
                                                                                                 buff=0.5)
        for r, row in enumerate(n["rows"], start=1):
            if row[2] == "codd":
                tab.cells[r][3].set_color(NO)
        lines = VGroup(
            label(rf"\textbf{{update}}: \ Codd moves office: \ {n['office_rows']} rows must change, \ and missing "
                  r"one leaves two offices", font_size=21, color=NO),
            label(r"\textbf{insertion}: \ a new course with no students yet cannot be recorded at all", font_size=21,
                  color=HEAD),
            label(r"\textbf{deletion}: \ when the last student leaves \texttt{os}, \ Ritchie's office is forgotten",
                  font_size=21, color=KERN),
            label(r"the cause: \ one table records several independent facts, \ each repeated", font_size=21,
                  color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "Tables can be designed badly. Here is one that records students, their courses, each course's instructor, "
            "and the instructor's office. <bookmark mark='a'/> If Codd moves office, three rows must change, and an "
            "update that misses one leaves him with two offices. <bookmark mark='b'/> A course that has no students "
            "yet cannot be recorded at all, because every row needs a student. <bookmark mark='c'/> And when the last "
            "student drops the operating systems course, the fact that Ritchie sits in room w3 disappears with her. "
            "<bookmark mark='d'/> These are update, insertion and deletion anomalies, and they all have one cause: "
            "the table records several independent facts, and repeats each of them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def dependencies(self):
        n = load("normal")
        head = label(r"Functional dependencies", font_size=36).to_edge(UP, buff=0.3)
        fds = VGroup(*[MathTex(rf"\text{{{NAMES[l]}}} \rightarrow \text{{{NAMES[r]}}}", font_size=32, color=c)
                       for (l, r), c in zip(n["fds"], (HEAD, LAM))]).arrange(DOWN, buff=0.2).next_to(head, DOWN,
                                                                                                buff=0.5)
        rules = VGroup(
            label(r"\textbf{Armstrong's axioms} \ (1974): \ reflexivity, \ augmentation, \ transitivity: \ sound and "
                  r"complete", font_size=20, color=WHITE),
            label(rf"closure: \ $\{{\text{{course}}\}}^+ = \{{{attrs(n['closure_C']).replace(chr(92) + ' ', '')}\}}$",
                  font_size=21, color=HEAD),
            label(rf"a \textbf{{key}}: \ attributes whose closure is everything: \ {{{attrs(n['keys'][0])}}}",
                  font_size=21, color=YES),
            label(r"\textbf{BCNF} \ (Boyce and Codd, 1974): \ every dependency's left side is a key", font_size=21,
                  color=DATA),
            label(rf"here \ {attrs(n['violation'][0])} $\rightarrow$ {attrs(n['violation'][1])} \ breaks it: \ "
                  r"\textit{course} alone is not a key", font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(fds, DOWN, buff=0.5)
        with self.voiceover(
            "The theory that names the problem is functional dependency. <bookmark mark='a'/> A course determines its "
            "instructor, and an instructor determines an office: wherever two rows agree on the left side, they agree "
            "on the right. <bookmark mark='b'/> Armstrong's three axioms derive every dependency that follows from "
            "these, and no others. <bookmark mark='c'/> The closure of course is course, instructor and office. "
            "<bookmark mark='d'/> A key is a set whose closure is every attribute: here, the student and the course "
            "together. <bookmark mark='e'/> Boyce-Codd normal form asks that the left side of every dependency be a "
            "key. <bookmark mark='f'/> Course determines instructor and office, but course is not a key, so the table "
            "is not in normal form, and that is exactly where the repetition comes from."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(fds))
            for mk, r in zip("bcdef", rules):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.wait(0.3)
        self.clear_scene()

    def decompose(self):
        n = load("normal")
        head = label(r"Decompose: \ one fact, \ one place", font_size=36).to_edge(UP, buff=0.3)
        parts = VGroup(*[label(r"\{" + attrs(p) + r"\}", font_size=22, color=c) for p, c in
                         zip(n["bcnf"], (LAM, HEAD, YES))]).arrange(RIGHT, buff=0.7).next_to(head, DOWN, buff=0.6)
        lines = VGroup(
            label(r"split on the violating dependency, \ and repeat: \ three tables, \ each in BCNF", font_size=21,
                  color=WHITE),
            label(rf"\textbf{{lossless}}: \ joining them gives back exactly the original \ "
                  rf"(the chase test: \ {'yes' if n['lossless_bcnf'] else 'no'})", font_size=21, color=YES),
            label(rf"a careless split, \ \{{{attrs('CS')}\}} and \{{{attrs('IOS')}\}}, \ invents rows when joined: \ "
                  rf"lossless {'yes' if n['lossless_bad'] else 'no'}", font_size=21, color=NO),
            label(r"the price: \ BCNF can lose a dependency \ (with \textit{student, course} $\rightarrow$ "
                  r"\textit{instructor} and \textit{instructor} $\rightarrow$ \textit{course}, \ no BCNF split keeps "
                  r"both)", font_size=19, color=KERN),
            label(r"\textbf{3NF} \ (Bernstein's synthesis, \ 1976) \ always keeps them, \ allowing a little "
                  r"redundancy", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.18).next_to(parts, DOWN, buff=0.6)
        with self.voiceover(
            "The cure is to decompose. <bookmark mark='a'/> Split the table along the offending dependency, and "
            "repeat until every piece is in normal form: instructors and offices; courses and instructors; students "
            "and courses. Each fact is now stored once. <bookmark mark='b'/> The split must be lossless: joining the "
            "pieces must give back exactly the original rows, and the chase, a mechanical test, confirms it. "
            "<bookmark mark='c'/> A careless split, students and courses in one table, students, instructors and "
            "offices in another, fails the test: joining them invents rows that were never there. <bookmark mark='d'/> "
            "There is a price. Sometimes no Boyce-Codd decomposition keeps every dependency checkable inside one "
            "table. <bookmark mark='e'/> The third normal form, built by Bernstein's synthesis, always keeps them, at "
            "the cost of a little redundancy, and that is the compromise most designs make."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(parts), FadeIn(lines[0]))
            for mk, ln in zip("bcde", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()
