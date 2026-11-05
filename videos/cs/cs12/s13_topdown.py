from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs12.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, ast_tree, code, grid_table, load,
                                   region, tree)


class TopDown(VoiceoverScene):
    def construct(self):
        self.card()
        self.descent()
        self.table()
        self.trace()
        self.pratt()

    def card(self):
        card = chapter_card(12, r"Top-down parsing", r"Can the parser predict which rule comes next?",
                            lit=(1968, 1973), extra=((1968, r"Lewis and Stearns: \ LL($k$)"),
                                                     (1973, r"Pratt: \ operator precedence")), part=PART)
        with self.voiceover("Chapter twelve. Top-down parsing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def descent(self):
        l = load("ll1")
        head = label(r"Recursive descent: \ one function per nonterminal", font_size=34).to_edge(UP, buff=0.3)
        bad = code(["def E():          # E -> E + T | T", "    E()           # calls itself first...",
                    "    expect('+')", "    T()"], size=18, color=NO).to_edge(LEFT, buff=0.6).shift(UP * 1.1)
        bl = label(r"left recursion: \ $E$ calls $E$ before reading anything: \ forever", font_size=19,
                   color=NO).next_to(bad, DOWN, buff=0.2).align_to(bad, LEFT)
        fixed = VGroup(*[Text(p, font="DejaVu Sans Mono", font_size=20, color=CODE) for p in l["prods"]]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).to_edge(RIGHT, buff=0.8).shift(UP * 0.6)
        fl = label(r"rewritten: \ $A \to A\alpha \mid \beta$ \ becomes \ $A \to \beta A'$, \ $A' \to \alpha A' \mid "
                   r"\varepsilon$", font_size=19, color=YES).next_to(fixed, DOWN, buff=0.25).to_edge(RIGHT, buff=0.4)
        good = code(["def E():", "    T()", "    while next is '+':", "        expect('+'); T()"], size=18,
                    color=YES).to_edge(LEFT, buff=0.6).to_edge(DOWN, buff=0.7)
        gl = label(r"the same thing as a loop: \ what hand-written parsers do", font_size=19, color=GREY_B).next_to(
            good, RIGHT, buff=0.5)
        with self.voiceover(
            "The simplest way to write a parser is by hand, top down. <bookmark mark='a'/> Write one function for "
            "each nonterminal, which reads exactly the tokens of that kind of phrase, calling the other functions "
            "for the phrases inside it. But try it on our grammar. E is E plus T, so the function for E first "
            "calls the function for E, which calls the function for E, forever, without reading a single token. "
            "<bookmark mark='b'/> The cure is to rewrite left recursion as right recursion: an expression is a "
            "term followed by a tail of plus-terms, which may be empty. <bookmark mark='c'/> Or, as hand-written "
            "parsers really do it, as a loop: parse a term, then as long as the next token is a plus, take it and "
            "parse another term."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bad), FadeIn(bl))
            vo.wait_until("b")
            self.play(FadeIn(fixed), FadeIn(fl))
            vo.wait_until("c")
            self.play(FadeIn(good), FadeIn(gl))
        self.wait(0.3)
        self.clear_scene()

    def table(self):
        l = load("ll1")
        head = label(r"FIRST, \ FOLLOW, \ and the LL(1) table", font_size=34).to_edge(UP, buff=0.3)
        nts = list(l["first"])
        ff = grid_table([r"", r"FIRST", r"FOLLOW"], [[n, " ".join(l["first"][n]), " ".join(l["follow"][n])]
                                                    for n in nts], [1.0, 1.9, 2.6], row_h=0.42, font_size=18,
                        colors=[[CODE, DATA, CTRL]] * len(nts), mono_cols=(0, 1, 2)).to_edge(LEFT, buff=0.5)
        ff.shift(UP * 0.4)
        terms = ["id", "+", "*", "(", ")", "$"]
        body = []
        for n in nts:
            row = [n]
            for t in terms:
                ps = l["table"][n].get(t, [])
                row.append(l["prods"][ps[0]].split(" → ")[1] if ps else "")
            body.append(row)
        tab = grid_table([r""] + [rf"\texttt{{{t}}}" if t != "$" else r"\texttt{\$}" for t in terms], body,
                         [0.9] + [1.15] * 6, row_h=0.42, font_size=15,
                         colors=[[CODE] + [YES] * 6] * len(nts), mono_cols=tuple(range(7))).to_edge(RIGHT, buff=0.4)
        tab.shift(UP * 0.4)
        pts = VGroup(
            label(r"FIRST($\alpha$): \ the tokens a phrase can start with; \ FOLLOW($A$): \ the tokens that can come "
                  r"right after $A$", font_size=19, color=GREY_A),
            label(r"in row $A$, \ column $t$: \ the rule to use for $A$ when the next token is $t$; \ "
                  r"$\varepsilon$-rules go under FOLLOW", font_size=19, color=GREY_A),
            label(rf"one entry per cell: \ the grammar is LL(1) \ (the left-recursive one had "
                  rf"{l['left_recursive_conflicts']} clashes)", font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "To make the choices automatic, compute two sets. <bookmark mark='a'/> FIRST of a phrase is the set "
            "of tokens it can begin with: a term can begin with an id or an opening bracket. FOLLOW of a "
            "nonterminal is the set of tokens that can appear right after it: after an expression, a closing "
            "bracket or the end. <bookmark mark='b'/> From these, fill a table. In the row for each nonterminal and "
            "the column for each token, write the rule to use when that nonterminal is expected and that token is "
            "next. A rule that can produce nothing goes under the tokens that can follow. <bookmark mark='c'/> If "
            "every cell holds at most one rule, the parser never has to guess: the grammar is LL one, for Left to "
            "right, Leftmost derivation, one token of lookahead. The left-recursive grammar had four clashing cells."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ff), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def trace(self):
        l = load("ll1")
        head = label(r"The LL(1) parser at work: \ \texttt{id + id * id}", font_size=34).to_edge(UP, buff=0.3)
        rows = []
        for st in l["trace"][:13]:
            rows.append([" ".join(st["stack"]), " ".join(st["input"]), st["action"]])
        t = grid_table([r"stack \ (top at right)", r"input", r"action"], rows, [4.4, 3.4, 3.4], row_h=0.36,
                       font_size=15, colors=[[CTRL, CODE, YES]] * len(rows), mono_cols=(0, 1, 2)).next_to(head, DOWN,
                                                                                                       buff=0.3)
        more = label(rf"\dots \ {len(l['trace'])} steps in all; \ accepted", font_size=19, color=GREY_B).next_to(
            t, DOWN, buff=0.15)
        with self.voiceover(
            "Here it is running. <bookmark mark='a'/> The parser keeps a stack of what it still expects to see, "
            "starting with E. At each step, if the top is a nonterminal, the table says which rule to expand it "
            "with; if it is a token, it must match the next input token. <bookmark mark='b'/> No backtracking, no "
            "guessing: one look at the next token decides every step, so the time is linear in the input. "
            "<bookmark mark='c'/> Most hand-written compilers, including GCC and Clang for C and C plus plus, are "
            "recursive descent parsers of this kind, with a little extra lookahead where the language demands it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*t.cells[r])) for r in range(1, 8)], lag_ratio=0.5), run_time=5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*t.cells[r])) for r in range(8, len(t.cells))], lag_ratio=0.4),
                      run_time=3)
            self.play(FadeIn(more))
            vo.wait_until("c")
        self.wait(0.3)
        self.clear_scene()

    def pratt(self):
        pb = load("pebble")
        head = label(r"Pratt parsing: \ precedence as numbers \ (the Pebble language)", font_size=32).to_edge(
            UP, buff=0.3)
        bp = VGroup(*[label(t, font_size=19, color=c) for t, c in (
            (r"\texttt{||} \ 1", GREY_A), (r"\texttt{\&\&} \ 2", GREY_A), (r"\texttt{== !=} \ 3", GREY_A),
            (r"\texttt{< <= > >=} \ 4", GREY_A), (r"\texttt{+ -} \ 5", CTRL), (r"\texttt{* / \%} \ 6", CTRL),
            (r"prefix \texttt{- ! * \&} \ 7", FUNC), (r"calls, \ \texttt{[ ]}, \ \texttt{.} \ 8", FUNC))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_edge(LEFT, buff=0.6).shift(UP * 0.5)
        bpl = label(r"binding powers", font_size=19, color=HEAD).next_to(bp, UP, buff=0.15).align_to(bp, LEFT)
        src = code(["fn expr(rbp) {", "    left = prefix()", "    while infix_power(next) > rbp {",
                    "        op = take()", "        left = Binary(op, left, expr(power(op)))", "    }",
                    "    return left", "}"], size=16).next_to(bp, RIGHT, buff=0.8).align_to(bp, UP)
        from explainer.cs.lang import pebble_lang as P
        e = "a + b * c - d"
        t = tree(ast_tree(P.parse_expr(e)), dx=0.7, dy=0.6, font_size=18).next_to(src, DOWN, buff=0.45)
        tl = Text(e + "   →   " + pb["pratt"][e], font="DejaVu Sans Mono", font_size=17, color=YES).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "Expressions with many precedence levels make long, tedious grammars: one nonterminal per level. Vaughan "
            "Pratt's method, from 1973, replaces them with numbers. <bookmark mark='a'/> Each operator gets a "
            "binding power: or binds weakest, then and, comparisons, plus and minus, times and divide, prefix "
            "operators, and strongest of all calls, indexing and field access. <bookmark mark='b'/> The whole "
            "expression parser is one loop. Parse a prefix; then, as long as the next operator binds more tightly "
            "than the caller's limit, take it and parse its right side with that operator's power as the new "
            "limit. <bookmark mark='c'/> On a plus b times c minus d, the times grabs b and c before the plus can, "
            "and the minus, at the same power as the plus, waits its turn, so subtraction groups to the left. This "
            "is the expression parser of the Pebble language, and of many real compilers."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bpl), LaggedStart(*[FadeIn(b) for b in bp], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(src))
            vo.wait_until("c")
            self.play(FadeIn(t), FadeIn(tl))
        self.wait(0.3)
        self.clear_scene()
