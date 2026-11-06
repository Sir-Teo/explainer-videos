from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs41.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, code_block)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.structured()
        self.correct()
        self.agents()
        self.open()

    def card(self):
        card = chapter_card(8, r"Frontier: \ merging and building, \ correctly", r"Can tools understand what they "
                            r"merge and build?", lit=(2011, 2022), extra=((2011, r"Apel et al.: \ semistructured "
                                                                          r"merge"),
                                                                         (2020, r"Mokhov et al.: \ build correctness"),
                                                                         (2022, r"Larsén et al.: \ Spork")), part=PART)
        with self.voiceover("Chapter eight. Frontier: merging and building, correctly."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def structured(self):
        head = label(r"Merging syntax, \ not lines", font_size=36).to_edge(UP, buff=0.3)
        ours = code_block(["import os", "import sys", "import json"], size=17)
        theirs = code_block(["import os", "import re", "import sys"], size=17)
        res = code_block(["import json", "import os", "import re", "import sys"], size=17, color=YES)
        cols = VGroup(VGroup(label(r"ours: \ added \texttt{json} at the end", font_size=18, color=DATA), ours).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12),
            VGroup(label(r"theirs: \ added \texttt{re} in the middle", font_size=18, color=LAM), theirs).arrange(
                DOWN, aligned_edge=LEFT, buff=0.12),
            VGroup(label(r"a structured merge: \ a set of imports", font_size=18, color=YES), res).arrange(
                DOWN, aligned_edge=LEFT, buff=0.12)).arrange(RIGHT, buff=0.8, aligned_edge=UP).next_to(
            head, DOWN, buff=0.5)
        lines = VGroup(
            wrapped_label(r"line-based merge knows nothing of the language: \ it flags independent edits that "
                          r"touch neighbouring lines, \ and silently accepts edits that clash in meaning \ (a renamed "
                          r"function and a new call to the old name)", 12.4, font_size=21, color=NO),
            wrapped_label(r"\textbf{structured merge} parses each version and merges trees: \ semistructured merge "
                          r"\ (Apel et al., 2011), \ Spork for Java, \ Mergiraf \ (2024) \ for many languages", 12.4,
                          font_size=21, color=YES),
            wrapped_label(r"open: \ merges that are semantically safe \ --- \ the merged program does what both "
                          r"changes intended \ --- \ checked by tests, \ types or proofs", 12.4, font_size=21,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(cols, DOWN, buff=0.45)
        with self.voiceover(
            "Merging by lines is the frontier's first target. <bookmark mark='a'/> Two branches each add an import, "
            "one in the middle of the list and one at the end. A line-based merge may report a conflict, although "
            "the meaning is simply a set of imports. <bookmark mark='b'/> Worse, it silently accepts edits that clash "
            "in meaning: one branch renames a function, another adds a call to its old name, and the merged "
            "program no longer runs. <bookmark mark='c'/> Structured merge parses each version and merges syntax "
            "trees, as Sven Apel and colleagues proposed in 2011 and newer tools such as Spork and Mergiraf do. "
            "<bookmark mark='d'/> The open problem is the deeper one: a merge that is semantically safe, whose "
            "result does what both changes intended, checked by tests, types or proofs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cols[0]), FadeIn(cols[1]))
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(cols[2]), FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def correct(self):
        head = label(r"Builds you can trust", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"\textbf{correctness}: \ after an incremental build, \ the outputs equal those of a clean "
                          r"build; \ \textbf{minimality}: \ nothing ran that did not need to \ (Mokhov et al.)", 12.4,
                          font_size=23, color=YES),
            wrapped_label(r"both fail when declared dependencies are wrong: \ tools now trace every file a task "
                          r"actually reads \ (forward builds, \ Rattle, \ 2020) \ instead of trusting the declaration",
                          12.4, font_size=23, color=HEAD),
            wrapped_label(r"\textbf{complete version solving}: \ resolvers that find a solution whenever one exists, "
                          r"\ prove none exists otherwise, \ and explain why \ --- \ at the speed of a greedy guess",
                          12.4, font_size=23, color=DATA),
            wrapped_label(r"\textbf{reproducibility at scale}: \ Debian and NixOS rebuild most packages "
                          r"bit-for-bit; \ the remaining few percent are a long tail of compilers, \ archives and "
                          r"clocks", 12.4, font_size=23, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Build systems have their own correctness questions. <bookmark mark='a'/> An incremental build is "
            "correct if its outputs equal those of a clean build, and minimal if nothing ran that did not need to. "
            "<bookmark mark='b'/> Both fail when the declared dependencies are wrong, so newer tools, such as Neil "
            "Mitchell's Rattle, trace every file a task actually reads instead of trusting what it declared. "
            "<bookmark mark='c'/> Version solving wants resolvers that are complete, finding a solution whenever "
            "one exists and proving and explaining it when none does, while staying as fast as a greedy guess on "
            "real universes. <bookmark mark='d'/> And reproducibility at scale is close: Debian and NixOS rebuild "
            "most of their packages bit for bit, and the last few percent are a long tail of compilers, archive "
            "formats and clocks."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def open(self):
        head = label(r"Open", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(
            wrapped_label(r"1. \ \textbf{Semantic merge}: \ detecting, \ before merging, \ that two changes that "
                          r"merge cleanly will break each other.", 12.4, font_size=25, color=WHITE),
            wrapped_label(r"2. \ \textbf{Dependency evolution}: \ predicting which upgrade will break a program, \ "
                          r"and repairing the program automatically.", 12.4, font_size=25, color=YES),
            wrapped_label(r"3. \ \textbf{Test selection}: \ choosing the fewest tests that catch a change's bugs, \ "
                          r"with guarantees, \ when dependencies are dynamic.", 12.4, font_size=25, color=HEAD),
            wrapped_label(r"4. \ \textbf{Safe rollout}: \ the fastest rollout schedule that bounds the expected "
                          r"harm of a bad release.", 12.4, font_size=25, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        star = wrapped_label(r"$\bigstar$ \ this part's research problem: \ the merge-queue policy, \ batch size and "
                             r"bisection order, \ that maximizes throughput when changes fail with different, \ "
                             r"learned probabilities", 12.4, font_size=24, color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Open problems. <bookmark mark='a'/> Semantic merge: detecting, before merging, that two changes which "
            "merge cleanly will break each other. <bookmark mark='b'/> Dependency evolution: predicting which upgrade "
            "will break a program, and repairing it automatically. <bookmark mark='c'/> Test selection with "
            "guarantees, choosing the fewest tests that still catch a change's bugs, even when dependencies are "
            "discovered at run time. <bookmark mark='d'/> And safe rollout: the fastest schedule that bounds the "
            "expected harm a bad release can do. <bookmark mark='e'/> This part's research problem asks for the "
            "best merge-queue policy, its batch sizes and the order of its bisection, when each change has its own "
            "learned probability of failing."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.6)
        self.clear_scene()

    def agents(self):
        head = label(r"When the author is a program", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"automated systems already make more than half of the changes in some large "
                          r"repositories: \ dependency bumps, \ large-scale refactorings, \ generated code \ (Google: "
                          r"about 24{,}000 of 40{,}000 changes a day in 2016)", 12.4, font_size=22, color=WHITE),
            wrapped_label(r"AI coding agents add authors that write many plausible patches quickly: \ the merge "
                          r"queue, \ the tests and the canary become the judge of each one \ (Part 40's oracle "
                          r"problem)", 12.4, font_size=22, color=HEAD),
            wrapped_label(r"provenance matters more: \ who or what wrote a change, \ from which inputs, \ reviewed "
                          r"by whom \ --- \ recorded in signed commits and attestations \ (Chapter 5)", 12.4,
                          font_size=22, color=YES),
            wrapped_label(r"open: \ review and testing that scale with the number of authors rather than the "
                          r"number of reviewers", 12.4, font_size=22, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "One more frontier is arriving quickly: authors that are programs. <bookmark mark='a'/> Automated systems "
            "already made most of the changes to Google's repository in 2016, dependency updates, large refactorings "
            "and generated code, about twenty-four thousand of forty thousand changes a day. "
            "<bookmark mark='b'/> AI coding agents add authors that can write many plausible patches very quickly. "
            "The merge queue, the tests and the canary then become the judge of every one, and Part 40 showed how "
            "much a test suite can miss. <bookmark mark='c'/> Provenance matters more than ever: who or what wrote a "
            "change, from which inputs, and who reviewed it, recorded in signed commits and attestations. "
            "<bookmark mark='d'/> The open question is how to review and test changes at a rate that grows with the "
            "number of authors rather than the number of reviewers."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()


_ = (NO,)
