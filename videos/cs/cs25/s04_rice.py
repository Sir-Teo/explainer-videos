from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs25.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, mono)


class Rice(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.consequences()

    def card(self):
        card = chapter_card(3, r"Rice's theorem", r"Which questions about programs can be answered?", lit=(1953,),
                            extra=((1953, r"Rice"),), part=PART)
        with self.voiceover("Chapter three. Rice's theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def theorem(self):
        head = label(r"Every non-trivial semantic property is undecidable", font_size=32).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"a \textbf{semantic} property depends only on \textbf{what} a program computes, \ not how it is "
                  r"written", font_size=22, color=WHITE),
            label(r"\textbf{non-trivial}: \ some programs have it and some don't", font_size=22, color=WHITE),
            label(r"examples: \ ``halts on input 0'', \ ``never divides by zero'', \ ``computes a sorting function'', \ "
                  r"``is equivalent to this one''", font_size=21, color=GREY_A),
            label(r"\textbf{proof} \ (Rice, 1953): \ say the empty function lacks $P$, \ and a program $Y$ has it",
                  font_size=22, color=HEAD),
            label(r"given $M, w$, \ build $M'$: \ on input $x$, \ first run $M$ on $w$; \ then run $Y$ on $x$",
                  font_size=22, color=DATA),
            label(r"$M$ halts on $w$ $\Rightarrow$ $M'$ computes what $Y$ does: \ has $P$; \ otherwise $M'$ never "
                  r"answers: \ lacks $P$", font_size=22, color=DATA),
            label(r"so a decider for $P$ would decide halting. \ (If the empty function has $P$, \ use the "
                  r"complement.)", font_size=22, color=NO),
        ).arrange(DOWN, buff=0.27).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "Henry Rice proved in 1953 that the halting problem is not an isolated case but the rule. <bookmark "
            "mark='a'/> Call a property of programs semantic if it depends only on what the program computes, its "
            "input-output behaviour, and not on how it is written. <bookmark mark='b'/> Call it non-trivial if some "
            "programs have it and some do not. <bookmark mark='c'/> Halting on zero, never dividing by zero, "
            "computing a sorting function, being equivalent to a given program: all semantic, all non-trivial. "
            "<bookmark mark='d'/> Rice's theorem says every such property is undecidable. The proof is one "
            "construction. Suppose the program that never answers lacks the property, and some program Y has it. "
            "<bookmark mark='e'/> Given any machine M and input w, build M prime: on input x, first run M on w, and "
            "if that ever finishes, run Y on x. <bookmark mark='f'/> If M halts on w, M prime computes exactly what Y "
            "computes, so it has the property. If not, M prime never answers anything, so it lacks it. <bookmark "
            "mark='g'/> A decider for the property would decide halting. If the never-answering program has the "
            "property instead, apply the argument to its complement."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def consequences(self):
        head = label(r"What Rice forbids, \ and how practice escapes", font_size=32).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"no perfect \textbf{virus scanner}: \ ``behaves maliciously'' is semantic \ (Fred Cohen, 1987)",
                  font_size=22, color=NO),
            label(r"no compiler can always find the \textbf{optimal} program, \ or all \textbf{dead code}", font_size=22,
                  color=NO),
            label(r"no static analyzer is both \textbf{sound} \ (never misses a bug) \ and \textbf{complete} \ (never a "
                  r"false alarm)", font_size=22, color=NO),
            label(r"the escape: \ \textbf{approximate}. \ Types reject some correct programs \ (Part 14); \ "
                  r"analyzers warn too often", font_size=22, color=YES),
            label(r"or restrict the language: \ total languages, \ bounded loops \ (Part 54 proves programs correct "
                  r"anyway)", font_size=22, color=YES),
            label(r"Rice is about \textbf{behaviour}: \ syntactic questions, \ ``has a loop'', \ ``has 10 states'', \ "
                  r"stay decidable", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This shapes real software. <bookmark mark='a'/> Fred Cohen showed in 1987 that no program can detect "
            "every virus, since behaving maliciously is a semantic property. <bookmark mark='b'/> No compiler can "
            "always find the best equivalent program, or even all the dead code. <bookmark mark='c'/> And no static "
            "analyzer can be both sound, never missing a bug, and complete, never raising a false alarm. <bookmark "
            "mark='d'/> Practice escapes by approximating. A type checker rejects some correct programs, as Part 14 "
            "showed; analyzers err on the side of warnings. <bookmark mark='e'/> Or it restricts the language until "
            "the question becomes decidable, and Part 54 will prove real programs correct within such limits. "
            "<bookmark mark='f'/> Notice what Rice does not forbid. Questions about the text of a program, how many "
            "states it has or whether it contains a loop, remain easy."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
