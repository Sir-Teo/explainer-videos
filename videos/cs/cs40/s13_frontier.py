from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs40.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, load)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.evidence()
        self.natural()
        self.agents()
        self.open()

    def card(self):
        card = chapter_card(12, r"Frontier: \ evidence, \ and machines that code", r"How would we know what works?",
                            lit=(2012, 2024), extra=((2012, r"Hindle et al.: \ the naturalness of software"),
                                                     (2021, r"Chen et al.: \ HumanEval"),
                                                     (2023, r"Jimenez et al.: \ SWE-bench")), part=PART)
        with self.voiceover("Chapter twelve. Frontier: evidence, and machines that write code."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def evidence(self):
        head = label(r"An evidence base, \ slowly", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"controlled experiments are expensive and small: \ students for a few hours stand in for "
                          r"professionals over years", 12.4, font_size=23, color=NO),
            wrapped_label(r"\textbf{mining software repositories}: \ millions of commits, \ reviews and bug reports \ "
                          r"--- \ correlation at scale, \ causation rarely", 12.4, font_size=23, color=HEAD),
            wrapped_label(r"some findings replicate well, \ and some can be checked in minutes on any codebase, \ "
                          r"as the next one can", 12.4, font_size=23, color=YES),
            wrapped_label(r"natural experiments, \ preregistration and replication are arriving late, \ as in "
                          r"medicine and psychology before", 12.4, font_size=23, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Software engineering is still building its evidence base. <bookmark mark='a'/> Controlled experiments "
            "are expensive and small: a few dozen students for a few hours stand in for professionals working over "
            "years. <bookmark mark='b'/> Mining software repositories gives scale, millions of commits, reviews and "
            "bug reports, but mostly correlations. <bookmark mark='c'/> Some findings have held up well, and some "
            "can be checked in minutes on any codebase. <bookmark mark='d'/> Natural experiments, preregistered studies and replications are arriving, "
            "late, as they did in medicine and psychology."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def agents(self):
        m = load("mutation")["mutation"]
        surv = len(m["survivors"])
        head = label(r"Judging a program that writes programs", font_size=36).to_edge(UP, buff=0.3)
        formula = MathTex(r"\text{pass@}k = 1 - \binom{n-c}{k} \Big/ \binom{n}{k}", font_size=34,
                          color=HEAD).next_to(head, DOWN, buff=0.5)
        lines = VGroup(
            wrapped_label(r"HumanEval \ (2021): \ 164 small functions with tests; \ sample $n$ programs, \ count the "
                          r"$c$ that pass, \ estimate the chance that one of $k$ tries would", 12.4, font_size=21,
                          color=WHITE),
            wrapped_label(r"SWE-bench \ (2023): \ real GitHub issues from Python projects; \ an agent's patch counts "
                          r"as a fix if the project's own new tests pass", 12.4, font_size=21, color=YES),
            wrapped_label(r"but tests are an incomplete oracle: \ audits found accepted patches that were wrong, \ "
                          r"and benchmark problems that leaked into training data", 12.4, font_size=21, color=NO),
            wrapped_label(rf"our own assembler's tests accept {surv} of {m['mutants']} one-site changes to "
                          r"its code \ (Chapter 6): \ any of them, \ submitted as a patch, \ would be scored correct",
                          12.4, font_size=21, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(formula, DOWN, buff=0.45)
        with self.voiceover(
            "Programs that write programs need the same scrutiny as people do. <bookmark mark='a'/> OpenAI's "
            "HumanEval of 2021 posed a hundred and sixty-four small functions, each with tests. Sample n programs "
            "from a model, count the c that pass, and this formula estimates the chance that at least one of k "
            "attempts would. <bookmark mark='b'/> SWE-bench, in 2023, raised the bar to real issues from GitHub "
            "projects: an agent's patch counts as a fix if the tests the human developers wrote for that issue pass. "
            "<bookmark mark='c'/> But tests are an incomplete oracle. Later audits found accepted patches that were "
            "wrong, and benchmark problems that had leaked into the models' training data. "
            "<bookmark mark='d'/> Our own measurements show why. The tests of our assembler, which pass, also pass "
            "on many slightly broken versions of it, as the mutation chapter showed. Any of those, submitted as a "
            "patch, would be scored as correct."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(formula), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.4)
        self.clear_scene()

    def open(self):
        head = label(r"Open", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(
            wrapped_label(r"1. \ \textbf{Oracles}: \ when tests are incomplete, \ how can a patch's correctness be "
                          r"judged automatically? \ Differential testing, \ specifications, \ and mutation-aware "
                          r"scoring are partial answers.", 12.4, font_size=25, color=WHITE),
            wrapped_label(r"2. \ \textbf{Measuring productivity}: \ what does a tool, \ a process or an AI "
                          r"assistant change, \ in controlled field studies, \ beyond self-report?", 12.4,
                          font_size=25, color=YES),
            wrapped_label(r"3. \ \textbf{Maintainability}: \ a measure of how hard code will be to change that "
                          r"predicts real future cost better than size does.", 12.4, font_size=25, color=HEAD),
            wrapped_label(r"4. \ \textbf{Flakiness}: \ predicting flaky tests from their code alone, \ and repairing "
                          r"them automatically.", 12.4, font_size=25, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        star = wrapped_label(r"$\bigstar$ \ this part's research problem: \ a test-adequacy score that predicts "
                             r"whether a patch the tests accept is truly correct, \ validated on our assembler's "
                             r"mutants", 12.4, font_size=24, color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Where the field is. <bookmark mark='a'/> The oracle problem: when tests are incomplete, how can a "
            "machine judge whether a patch is right? Comparing against other implementations, writing "
            "specifications, and scoring tests by the mutants they kill all help, and none is complete. "
            "<bookmark mark='b'/> Measuring productivity: what does a tool, a process or an AI assistant really "
            "change, measured in the field rather than by asking people how they feel? <bookmark mark='c'/> "
            "Maintainability: a number that predicts how expensive code will be to change better than its size "
            "already does. <bookmark mark='d'/> And flaky tests: predicting them from their code, and repairing "
            "them automatically. <bookmark mark='e'/> This part's research problem asks for a score of a test "
            "suite that predicts whether a patch it accepts is really correct, checked on patches whose correctness "
            "we know: our assembler's mutants."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.6)
        self.clear_scene()

    def natural(self):
        n = load("natural")
        head = label(r"Code is natural", font_size=36).to_edge(UP, buff=0.3)
        top = 9.0
        bars = VGroup()
        items = [(r"English: \ the thirty novels", n["english_unigram_bits"], n["english_bits"], LAM),
                 (r"Python: \ this repository's library", n["code_unigram_bits"], n["code_bits"], YES)]
        for i, (name, uni, tri, col) in enumerate(items):
            y = 1.3 - i * 1.7
            nm = label(name, font_size=20, color=col).move_to([-4.2, y + 0.35, 0])
            b1 = Rectangle(width=uni / top * 8.0, height=0.32, stroke_width=0, fill_color=GREY_C,
                           fill_opacity=0.6)
            b1.move_to([-6.0 + b1.width / 2, y - 0.05, 0])
            b2 = Rectangle(width=tri / top * 8.0, height=0.32, stroke_width=0, fill_color=col, fill_opacity=0.85)
            b2.move_to([-6.0 + b2.width / 2, y - 0.45, 0])
            t1 = label(rf"one word at a time: \ {uni:.1f} bits", font_size=17, color=GREY_A).next_to(b1, RIGHT,
                                                                                                buff=0.15)
            t2 = label(rf"from the two before: \ {tri:.1f} bits", font_size=17, color=col).next_to(b2, RIGHT,
                                                                                              buff=0.15)
            bars.add(VGroup(nm, b1, b2, t1, t2))
        nm0 = bars[0][0]
        nm0.align_to(bars[0][1], LEFT)
        bars[1][0].align_to(bars[1][1], LEFT)
        lines = VGroup(
            wrapped_label(rf"a trigram model \ (the $n$-gram models of \textit{{AI, Built}}), \ trained on 80\% and scored on the "
                          rf"held-out 20\%: \ {n['code_tokens']:,} tokens of each; \ bits per token \ = \ surprise", 12.4,
                          font_size=20, color=GREY_A),
            wrapped_label(r"code is far more predictable than prose \ --- \ Hindle, Barr, Su, Gabel and Devanbu found "
                          r"the same in 2012 on Java and C; \ it is why code completion works, \ and why language "
                          r"models write code so well", 12.4, font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Here is a finding from that evidence base that we can replicate in a minute. <bookmark mark='a'/> Train "
            "a trigram model, which predicts each word from the two before it, on four fifths of the thirty "
            "novels, and measure its surprise on the last fifth: about eight bits per word. "
            "<bookmark mark='b'/> Do the same on the Python code of this repository's library, token by token: four "
            "and a half bits. Code is far more predictable than prose. <bookmark mark='c'/> Abram Hindle and his "
            "colleagues found the same in 2012 for Java and C, and called it the naturalness of software. It is why "
            "code completion works, and it is the observation that grew into today's code-writing models."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA,)
