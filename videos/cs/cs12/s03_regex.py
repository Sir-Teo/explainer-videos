from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs12.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, load, region)


def mod3_diagram():
    return StateDiagram({"0": (-3.2, 0), "1": (0, 0), "2": (3.2, 0)},
                        [("0", "0", "0", LEFT), ("0", "1", "1", 0.5), ("1", "0", "1", 0.5), ("1", "2", "0", 0.5),
                         ("2", "1", "0", 0.5), ("2", "2", "1", RIGHT)], radius=0.5, accept=("0",), font_size=28,
                        edge_font=22)


class Regex(VoiceoverScene):
    def construct(self):
        self.card()
        self.operations()
        self.dfa()
        self.plan()

    def card(self):
        card = chapter_card(2, r"Regular expressions and automata", r"Which patterns can a finite machine match?",
                            lit=(1951, 1959), extra=((1951, r"Kleene: \ regular events"),
                                                     (1959, r"Rabin and Scott: \ finite automata")), part=PART)
        with self.voiceover("Chapter two. Regular expressions and automata."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def operations(self):
        head = label(r"Three operations \ (Kleene, \ 1951)", font_size=36).to_edge(UP, buff=0.35)
        ops = VGroup(
            VGroup(Text("r|s", font="DejaVu Sans Mono", font_size=30, color=HEAD),
                   label(r"union: \ a string of $r$ \textit{or} a string of $s$", font_size=22, color=GREY_A)),
            VGroup(Text("rs", font="DejaVu Sans Mono", font_size=30, color=HEAD),
                   label(r"concatenation: \ a string of $r$, \ then one of $s$", font_size=22, color=GREY_A)),
            VGroup(Text("r*", font="DejaVu Sans Mono", font_size=30, color=HEAD),
                   label(r"star: \ zero or more strings of $r$, \ one after another", font_size=22, color=GREY_A)),
        )
        for o in ops:
            o[1].next_to(o[0], RIGHT, buff=0.5)
            o[0].align_to([-5.5, 0, 0], LEFT)
        ops.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.5).align_to([-5.5, 0, 0], LEFT)
        for o in ops:
            o[1].align_to([-3.6, 0, 0], LEFT)
        base = label(r"plus single symbols, \ $\varepsilon$ and $\emptyset$; \ shorthands: \ \texttt{r+} $=$ "
                     r"\texttt{rr*}, \ \texttt{r?} $=$ \texttt{r|}$\varepsilon$, \ \texttt{[a-z]}, \ \texttt{.}",
                     font_size=20, color=GREY_B).next_to(ops, DOWN, buff=0.3).align_to(ops, LEFT)
        ex = [("(0|1)*1", r"binary strings ending in 1", ["1", "0101", "111"]),
              ("a(b|c)*d", r"an $a$, \ any $b$'s and $c$'s, \ a $d$", ["ad", "abcbd", "accd"]),
              ("[a-zA-Z_][a-zA-Z_0-9]*", r"a Pebble identifier", ["lookup", "p", "row_2"]),
              ("(0|1(01*0)*1)*", r"binary multiples of 3 \ (chapter 5)", ["0", "11", "1001"])]
        rows = VGroup()
        for rx, what, ms in ex:
            r = VGroup(Text(rx, font="DejaVu Sans Mono", font_size=20, color=CODE), label(what, font_size=19,
                                                                                         color=GREY_A),
                       Text("  ".join(ms), font="DejaVu Sans Mono", font_size=17, color=YES))
            r[0].move_to([-6.3, 0, 0], aligned_edge=LEFT)
            r[1].move_to([-1.2, 0, 0], aligned_edge=LEFT)
            r[2].move_to([3.9, 0, 0], aligned_edge=LEFT)
            rows.add(r)
        rows.arrange(DOWN, buff=0.28, aligned_edge=LEFT).next_to(base, DOWN, buff=0.55)
        for r in rows:
            r[0].align_to([-6.3, 0, 0], LEFT)
            r[1].align_to([-1.2, 0, 0], LEFT)
            r[2].align_to([3.9, 0, 0], LEFT)
        with self.voiceover("Mathematical regular expressions build languages using three operations, developed by Kleene in his work on finite automata. <bookmark mark='a'/> Union chooses a string from either language. Concatenation joins a string from each. Star joins any finite number of strings from one language, including zero. <bookmark mark='b'/> Ordinary plus, question mark, finite character classes and dot are expressible with these operations over the chosen alphabet. Practical extensions such as backreferences require a separate discussion. <bookmark mark='c'/> The examples include suffixes, identifiers and binary divisibility by three. Our divisibility convention allows leading zeros and also accepts the empty word as representing zero; requiring at least one digit would change that language slightly.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(o, shift=RIGHT * 0.1) for o in ops], lag_ratio=0.5), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(base))
            vo.wait_until('c')
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.5), run_time=4)
        self.wait(0.3)
        self.clear_scene()

    def dfa(self):
        head = label(r"A finite automaton \ (Part 5): \ divisible by 3?", font_size=34).to_edge(UP, buff=0.35)
        sd = mod3_diagram().shift(UP * 0.6)
        rule = label(r"state $r$ = the remainder so far; \ reading bit $b$: \ $r \to (2r + b) \bmod 3$", font_size=22,
                     color=GREY_A).next_to(sd, DOWN, buff=0.6)
        word = "1001"
        cells = VGroup(*[Text(c, font="DejaVu Sans Mono", font_size=34, color=CODE) for c in word]).arrange(
            RIGHT, buff=0.35).next_to(rule, DOWN, buff=0.45)
        ptr = Triangle(color=HEAD, fill_opacity=1).scale(0.1).rotate(PI).next_to(cells[0], UP, buff=0.08)
        states = ["0"]
        for c in word:
            states.append(str((2 * int(states[-1]) + int(c)) % 3))
        verdict = label(r"$1001_2 = 9$: \ it ends in the accepting state 0 \ $\Rightarrow$ \ divisible by 3",
                        font_size=22, color=YES).to_edge(DOWN, buff=0.4)
        with self.voiceover("And here is a machine. <bookmark mark='a'/> A finite automaton with three states, one for each possible remainder when a binary number read so far is divided by three. <bookmark mark='b'/> Reading one more bit doubles the number and adds the bit, so the remainder r becomes two r plus b, modulo three. That is the whole machine: a fixed memory of three states, however long the input. <bookmark mark='c'/> Feed it one, zero, zero, one. It moves to one, to two, to one, and back to zero, the accepting state: nine is divisible by three. Exactly the strings that the strange regular expression on the last slide describes. Is that a coincidence?") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(sd), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(rule))
            vo.wait_until('c')
            self.play(FadeIn(cells), FadeIn(ptr), sd.light('0'))
            for k, c in enumerate(word):
                self.play(ptr.animate.next_to(cells[k], UP, buff=0.08), run_time=0.3)
                self.play(sd.light(states[k + 1]), cells[k].animate.set_color(GREY_B), run_time=0.5)
            self.play(FadeIn(verdict))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        head = label(r"The same languages, \ three ways", font_size=36).to_edge(UP, buff=0.35)
        rx = region(3.4, 1.0, r"regular expression", HEAD, font_size=22)
        nfa = region(3.4, 1.0, r"NFA", DATA, font_size=24)
        dfa = region(3.4, 1.0, r"DFA", CTRL, font_size=24)
        rx.move_to(UP * 1.4)
        nfa.move_to(DOWN * 1.6 + LEFT * 3.6)
        dfa.move_to(DOWN * 1.6 + RIGHT * 3.6)
        a1 = Arrow(rx.get_bottom() + LEFT * 0.6, nfa.get_top(), color=GREY_B, buff=0.1)
        a2 = Arrow(nfa.get_right(), dfa.get_left(), color=GREY_B, buff=0.1)
        a3 = Arrow(dfa.get_top(), rx.get_bottom() + RIGHT * 0.6, color=GREY_B, buff=0.1)
        l1 = label(r"Thompson \ (chapter 3)", font_size=19, color=DATA).next_to(a1.get_center(), LEFT, buff=0.3)
        l2 = label(r"subsets \ (chapter 4)", font_size=19, color=CTRL).next_to(a2, DOWN, buff=0.15)
        l3 = label(r"state elimination \ (chapter 5)", font_size=19, color=HEAD).next_to(a3.get_center(), RIGHT,
                                                                                      buff=0.3)
        thm = label(r"Kleene's theorem: \ a language is regular $\iff$ some finite automaton recognizes it",
                    font_size=22, color=YES).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "It is not. Kleene's theorem says that regular expressions and finite automata describe exactly the "
            "same languages, the regular languages. The next three chapters prove it by going round this "
            "triangle. <bookmark mark='a'/> Ken Thompson's construction turns any regular expression into a "
            "nondeterministic automaton. <bookmark mark='b'/> The subset construction, from Michael Rabin and Dana "
            "Scott, turns that into an ordinary deterministic one. <bookmark mark='c'/> And eliminating states one "
            "at a time turns any automaton back into a regular expression."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rx), FadeIn(nfa), FadeIn(dfa), FadeIn(thm))
            vo.wait_until("a")
            self.play(GrowArrow(a1), FadeIn(l1))
            vo.wait_until("b")
            self.play(GrowArrow(a2), FadeIn(l2))
            vo.wait_until("c")
            self.play(GrowArrow(a3), FadeIn(l3))
        self.wait(0.3)
        self.clear_scene()
