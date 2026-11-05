from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs12.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, load, region, tree)


class Languages(VoiceoverScene):
    def construct(self):
        self.card()
        self.sets()
        self.recognize()
        self.memory()

    def card(self):
        card = chapter_card(1, r"Languages as sets of strings", r"What does it mean to recognize a language?",
                            lit=(1956,), extra=((1956, r"Chomsky: \ three models of language"),), part=PART)
        with self.voiceover("Chapter one. Languages as sets of strings."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def sets(self):
        head = label(r"A language is a set of strings", font_size=36).to_edge(UP, buff=0.35)
        defs = VGroup(
            label(r"an alphabet $\Sigma$: \ a finite set of symbols, \ say $\{0, 1\}$", font_size=22, color=GREY_A),
            label(r"a string: \ a finite sequence of them, \ including the empty string $\varepsilon$", font_size=22,
                  color=GREY_A),
            label(r"a language: \ \textit{any} set of strings, \ $L \subseteq \Sigma^*$", font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(head, DOWN, buff=0.4)
        rows = [
            (r"binary numbers divisible by 3", ["0", "11", "110", "1001"], ["10", "111"], DATA),
            (r"balanced parentheses", ["()", "(())()", "((()))"], ["())(", "(()"], CTRL),
            (r"$a^n b^n$: \ some $a$'s, \ then as many $b$'s", ["ab", "aabb", "aaabbb"], ["aab", "abab"], YES),
            (r"palindromes over $\{a, b\}$", ["abba", "aba", "baab"], ["ab", "abab"], FUNC),
            (r"Pebble programs", ["the Job"], ["fn f( {"], NO),
        ]
        g = VGroup()
        for name, ins, outs, c in rows:
            r = VGroup(label(name, font_size=21, color=c),
                       VGroup(*[Text(s, font="DejaVu Sans Mono", font_size=17, color=YES) for s in ins]).arrange(
                           RIGHT, buff=0.3),
                       VGroup(*[Text(s, font="DejaVu Sans Mono", font_size=17, color=NO) for s in outs]).arrange(
                           RIGHT, buff=0.3))
            r[0].move_to([-6.6, 0, 0], aligned_edge=LEFT)
            r[1].move_to([-0.6, 0, 0], aligned_edge=LEFT)
            r[2].move_to([3.6, 0, 0], aligned_edge=LEFT)
            g.add(r)
        g.arrange(DOWN, buff=0.32, aligned_edge=LEFT).next_to(defs, DOWN, buff=0.55)
        for r in g:
            r[0].align_to([-6.6, 0, 0], LEFT)
            r[1].align_to([-0.6, 0, 0], LEFT)
            r[2].align_to([3.6, 0, 0], LEFT)
        hdr = VGroup(label(r"in $L$", font_size=18, color=YES).move_to([-0.3, 0, 0], aligned_edge=LEFT),
                     label(r"not in $L$", font_size=18, color=NO).move_to([3.6, 0, 0], aligned_edge=LEFT)).next_to(
            g, UP, buff=0.15)
        hdr[0].align_to([-0.6, 0, 0], LEFT)
        hdr[1].align_to([3.6, 0, 0], LEFT)
        with self.voiceover(
            "Computer science gives the word language a precise and very general meaning. <bookmark mark='a'/> "
            "Fix an alphabet, a finite set of symbols, say zero and one. A string is a finite sequence of them, "
            "including the empty string. A language is any set of strings at all. <bookmark mark='b'/> The binary "
            "numbers divisible by three are a language. So are the balanced strings of parentheses; the strings of "
            "some a's followed by exactly as many b's; the palindromes. <bookmark mark='c'/> And so are the valid "
            "programs of a programming language: the Job is in the language of Pebble programs, and a line with a "
            "missing parenthesis is not."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in defs], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(hdr), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in g[:4]], lag_ratio=0.4),
                      run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(g[4], shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def recognize(self):
        head = label(r"Recognizing, \ and parsing", font_size=36).to_edge(UP, buff=0.35)
        inp = Text("id + id * id", font="DejaVu Sans Mono", font_size=26, color=CODE)
        rec = region(2.6, 1.0, r"recognizer", DATA, font_size=24)
        yes = label(r"yes", font_size=30, color=YES)
        row1 = VGroup(inp.copy(), Arrow(LEFT, RIGHT, color=GREY_B), rec, Arrow(LEFT, RIGHT, color=GREY_B),
                      yes).arrange(RIGHT, buff=0.3).shift(UP * 1.4)
        par = region(2.6, 1.0, r"parser", YES, font_size=24)
        t = tree(("E", [("E", [("T", [("F", ["id"])])]), "+", ("T", [("T", [("F", ["id"])]), "*", ("F", ["id"])])]),
                 dx=0.62, dy=0.55, font_size=17).scale(0.95)
        row2 = VGroup(inp.copy(), Arrow(LEFT, RIGHT, color=GREY_B), par, Arrow(LEFT, RIGHT, color=GREY_B),
                      t).arrange(RIGHT, buff=0.3).shift(DOWN * 1.4)
        n1 = label(r"a decision: \ is the string in the language?", font_size=20, color=DATA).next_to(row1, DOWN,
                                                                                                   buff=0.25)
        n2 = label(r"a structure: \ \textit{how} is it in the language? \ ($\times$ binds tighter than $+$)",
                   font_size=20, color=YES).next_to(row2, DOWN, buff=0.25)
        with self.voiceover(
            "There are two things we might want to do with a language. <bookmark mark='a'/> A recognizer answers a "
            "yes-or-no question: is this string in the language? <bookmark mark='b'/> A parser does more: it says "
            "how the string belongs, by building its structure. For this expression, the tree says that the "
            "multiplication happens first, and the addition last. A compiler needs the tree; but recognizing comes "
            "first, and it is already deep."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(row1), FadeIn(n1))
            vo.wait_until("b")
            self.play(FadeIn(row2), FadeIn(n2))
        self.wait(0.3)
        self.clear_scene()

    def memory(self):
        head = label(r"How much memory does a recognizer need?", font_size=34).to_edge(UP, buff=0.35)
        rungs = [
            (r"a fixed, \ finite memory", r"a finite automaton", r"divisible by 3", DATA),
            (r"plus one stack", r"a pushdown automaton", r"balanced parentheses, \ $a^n b^n$", CTRL),
            (r"plus memory proportional to the input", r"a linear-bounded automaton", r"$a^n b^n c^n$", YES),
            (r"unlimited memory", r"a Turing machine \ (Part 1)", r"anything computable", FUNC),
        ]
        g = VGroup()
        for k, (mem, mach, ex, c) in enumerate(rungs):
            box_ = Rectangle(width=11.5, height=0.85, stroke_color=c, stroke_width=1.8, fill_color=c,
                             fill_opacity=0.08 + 0.04 * k)
            t = VGroup(label(mem, font_size=20, color=c), label(mach, font_size=20, color=GREY_A),
                       label(ex, font_size=19, color=GREY_B))
            t[0].move_to(box_.get_left() + RIGHT * 0.3, aligned_edge=LEFT)
            t[1].move_to(box_.get_center() + RIGHT * 0.3)
            t[2].move_to(box_.get_right() + LEFT * 0.3, aligned_edge=RIGHT)
            g.add(VGroup(box_, t))
        g.arrange(UP, buff=0.12).next_to(head, DOWN, buff=0.55)
        theme = label(r"the theme of this part: \ \textit{what a machine can recognize depends on what it can "
                      r"remember}", font_size=22, color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The question that organizes this part is: how much memory does a recognizer need? <bookmark mark='a'/> "
            "Some languages need only a fixed amount, however long the input: to check divisibility by three you "
            "only need to remember the remainder so far. That is a finite automaton, from Part 5. <bookmark "
            "mark='b'/> Balanced parentheses need more: you have to count how many are open, without limit. A "
            "single stack is enough. <bookmark mark='c'/> Some languages need memory in proportion to the input, "
            "and the most powerful machine, the Turing machine of Part 1, has unlimited memory. <bookmark mark='d'/> "
            "This ladder, which Noam Chomsky described in 1956, is the backbone of the part: what a machine can "
            "recognize depends on what it can remember."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
            self.play(FadeIn(g[3], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(theme))
        self.wait(0.3)
        self.clear_scene()
