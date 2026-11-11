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
        head = label('Rice: nontrivial extensional properties of partial computable functions', font_size=32).to_edge(UP, buff=0.35)
        lines = VGroup(
            label('\\textbf{extensional}: equal partial input-output functions agree; faults and divergence are undefined', font_size=22, color=WHITE),
            label(r"\textbf{non-trivial}: \ some programs have it and some don't", font_size=22, color=WHITE),
            label('examples: defined on 0; total; computes sorting; equals a fixed partial computable function', font_size=21, color=GREY_A),
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
            "Rice's theorem concerns partial computable input-output functions in an effective universal programming system. <bookmark mark='a'/> A property is extensional if equal partial functions always agree on it. Faults and divergence both count as undefined under this convention. <bookmark mark='b'/> Nontrivial means that some computed functions have the property and some lack it. <bookmark mark='c'/> Defined on zero, total, computes sorting, or equals a fixed partial computable function are examples. Never dividing by zero is not an extensional example under these observations. <bookmark mark='d'/> Suppose the nowhere-defined function lacks P and some program Y has it. <bookmark mark='e'/> Construct M prime to simulate M on w, then run Y on its own input if the simulation halts. <bookmark mark='f'/> If M halts, M prime computes Y's function; otherwise it computes the nowhere-defined function. <bookmark mark='g'/> A decider for P would decide halting. If the nowhere-defined function has P, apply the argument to its complement."
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
            label('no exact total detector of a specified nontrivial extensional malicious behaviour',
                  font_size=22, color=NO),
            label('no general all-dead-code detector; optimality claims require a specified objective and model', font_size=22,
                  color=NO),
            label('no total analyzer exactly decides an undecidable property without misses or false alarms', font_size=22, color=NO),
            label(r"the escape: \ \textbf{approximate}. \ Types reject some correct programs \ (Part 14); \ "
                  r"analyzers warn too often", font_size=22, color=YES),
            label('restrict the particular question; totality alone does not decide every semantic property', font_size=22, color=YES),
            label(r"Rice is about \textbf{behaviour}: \ syntactic questions, \ ``has a loop'', \ ``has 10 states'', \ "
                  r"stay decidable", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "These limits guide software design under unbounded semantics. <bookmark mark='a'/> Exact detection of a specified nontrivial extensional malicious behaviour is undecidable. The behaviour and observation model must be stated. <bookmark mark='b'/> Detecting all dead code is impossible in general; optimization impossibility claims likewise require a particular objective and model. <bookmark mark='c'/> No terminating analyzer decides every instance of such an undecidable property both without missed cases and without false alarms. <bookmark mark='d'/> Practical tools use conservative approximations or incomplete searches. <bookmark mark='e'/> Restrictions can make particular questions decidable. Totality alone does not make all semantic questions decidable: even equality of total primitive recursive programs is problematic. <bookmark mark='f'/> Syntactic questions about a finite program description remain decidable by inspection."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
