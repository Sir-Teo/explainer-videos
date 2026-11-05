from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs12.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, grid_table, load, region,
                                   tree)

EXPR_TREE = ("E", [("E", [("T", [("F", ["id"])])]), "+", ("T", [("T", [("F", ["id"])]), "*", ("F", ["id"])])])
LEFT_TREE = ("E", [("E", [("E", ["id"]), "+", ("E", ["id"])]), "*", ("E", ["id"])])
RIGHT_TREE = ("E", [("E", ["id"]), "+", ("E", [("E", ["id"]), "*", ("E", ["id"])])])


class Grammars(VoiceoverScene):
    def construct(self):
        self.card()
        self.rules()
        self.derive()
        self.ambiguity()
        self.dangling()

    def card(self):
        card = chapter_card(9, r"Context-free grammars", r"How do you describe a language with nesting?",
                            lit=(1956, 1960), extra=((1956, r"Chomsky: \ phrase-structure grammars"),
                                                     (1960, r"Backus and Naur: \ ALGOL 60")), part=PART)
        with self.voiceover("Chapter nine. Context-free grammars."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def rules(self):
        head = label(r"A grammar: \ rules for rewriting", font_size=36).to_edge(UP, buff=0.3)
        g = VGroup(*[Text(t, font="DejaVu Sans Mono", font_size=28, color=CODE) for t in
                     ("E → E + T | T", "T → T * F | F", "F → ( E ) | id")]).arrange(DOWN, aligned_edge=LEFT,
                                                                                buff=0.2)
        g.next_to(head, DOWN, buff=0.5)
        parts = VGroup(
            label(r"\textit{nonterminals} \ ($E$, $T$, $F$): \ names for kinds of phrase: \ expression, \ term, \ "
                  r"factor", font_size=21, color=GREY_A),
            label(r"\textit{terminals} \ (\texttt{+}, \texttt{*}, \texttt{(}, \texttt{)}, \texttt{id}): \ the tokens "
                  r"from the lexer", font_size=21, color=GREY_A),
            label(r"a rule $A \to \alpha$: \ wherever $A$ appears, \ it may be replaced by $\alpha$, \ "
                  r"\textit{whatever surrounds it} \ (context-free)", font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(g, DOWN, buff=0.5)
        hist = VGroup(
            label(r"Noam Chomsky, \ 1956: \ grammars as a model of natural language", font_size=20, color=GREY_B),
            label(r"John Backus and Peter Naur, \ 1960: \ the same idea, \ ``BNF'', \ defines ALGOL 60 \ --- \ "
                  r"the first major language defined by a formal grammar", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Nesting needs a more powerful description: a grammar. <bookmark mark='a'/> Here is a grammar for "
            "arithmetic expressions. It has three rules, each with alternatives separated by a bar. <bookmark "
            "mark='b'/> E, T and F are nonterminals: names for kinds of phrase, an expression, a term and a "
            "factor. Plus, times, the brackets and id are terminals: the tokens the lexer produces. A rule says "
            "that wherever its left side appears, it may be replaced by its right side, whatever surrounds it; "
            "that is what context-free means. Notice the third rule: an expression in brackets is a factor, so the "
            "grammar can nest without limit. <bookmark mark='c'/> Noam Chomsky defined such grammars in 1956 as a "
            "model of human language. Four years later John Backus and Peter Naur used the same idea to define "
            "ALGOL 60, the first major programming language defined by a formal grammar, and nearly every language "
            "since has had one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in g], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in parts], lag_ratio=0.6), run_time=5)
            vo.wait_until("c")
            self.play(FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()

    def derive(self):
        head = label(r"A derivation, \ and its parse tree", font_size=36).to_edge(UP, buff=0.3)
        steps = ["E", "E + T", "T + T", "F + T", "id + T", "id + T * F", "id + F * F", "id + id * F", "id + id * id"]
        lines = VGroup(*[Text(("⇒ " if k else "   ") + s, font="DejaVu Sans Mono", font_size=21,
                              color=CODE if k < len(steps) - 1 else YES) for k, s in enumerate(steps)]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        t = tree(EXPR_TREE, dx=0.85, dy=0.68, font_size=22).to_edge(RIGHT, buff=1.0).shift(UP * 0.15)
        note_ = label(r"leftmost: \ always rewrite the leftmost nonterminal", font_size=19, color=GREY_B).next_to(
            lines, UP, buff=0.25).align_to(lines, LEFT)
        cap = label(r"the tree records \textit{which rule built which part}: \ \texttt{*} sits below \texttt{+}, \ "
                    r"so it is done first", font_size=20, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "To show that a string is in the language, derive it. <bookmark mark='a'/> Start from E, and rewrite "
            "one nonterminal at a time, here always the leftmost. E becomes E plus T; that E becomes T, then F, "
            "then id. Then T becomes T times F, and so on, until only tokens are left: id plus id times id. "
            "<bookmark mark='b'/> The same derivation, drawn as a tree, is the parse tree: each nonterminal's "
            "children are what it was rewritten into. <bookmark mark='c'/> And the tree is the point. Because the "
            "multiplication was built inside a T, below the plus, it binds more tightly. The grammar has encoded "
            "the precedence of the operators in its shape."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note_))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l, shift=DOWN * 0.05) for l in lines], lag_ratio=0.5), run_time=7)
            vo.wait_until("b")
            self.play(FadeIn(t.edges), LaggedStart(*[FadeIn(m) for m, _ in t.nodes], lag_ratio=0.08), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    def ambiguity(self):
        c = load("cfg")
        head = label(r"Ambiguity: \ more than one tree", font_size=36).to_edge(UP, buff=0.3)
        gram = Text("E → E + E | E * E | id", font="DejaVu Sans Mono", font_size=24, color=CODE).next_to(head, DOWN,
                                                                                                   buff=0.3)
        t1 = tree(LEFT_TREE, dx=0.65, dy=0.62, font_size=19)
        t2 = tree(RIGHT_TREE, dx=0.65, dy=0.62, font_size=19)
        VGroup(t1, t2).arrange(RIGHT, buff=1.5).next_to(gram, DOWN, buff=0.45).shift(LEFT * 2.0)
        l1 = label(r"$(\mathrm{id} + \mathrm{id}) \times \mathrm{id}$", font_size=20, color=NO).next_to(t1, DOWN,
                                                                                                    buff=0.15)
        l2 = label(r"$\mathrm{id} + (\mathrm{id} \times \mathrm{id})$", font_size=20, color=YES).next_to(t2, DOWN,
                                                                                                     buff=0.15)
        rows = [[str(r["operands"]), f"{r['trees']:,}"] for r in c["catalan"] if r["operands"] in (2, 3, 4, 5, 6, 8,
                                                                                                10, 12)]
        tab = grid_table([r"operands", r"trees"], rows, [1.7, 1.7], row_h=0.38, font_size=18,
                         colors=[[GREY_A, NO]] * len(rows), mono_cols=()).to_edge(RIGHT, buff=0.5).shift(UP * 0.2)
        tl = label(r"counted by CYK \ (chapter 11): \ the Catalan numbers", font_size=18, color=GREY_B).next_to(
            tab, UP, buff=0.15)
        fix = label(rf"the layered $E$, $T$, $F$ grammar: \ exactly {c['unambiguous_trees']} tree, \ always",
                    font_size=21, color=YES).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A simpler grammar for the same expressions would say: an expression is two expressions joined by plus "
            "or times, or an id. <bookmark mark='a'/> But then id plus id times id has two parse trees. In one, "
            "the addition is done first; in the other, the multiplication. Two trees, two meanings, two different "
            "answers. The grammar is ambiguous. <bookmark mark='b'/> And it gets worse quickly. With more "
            "operands, the number of trees grows like the Catalan numbers: fourteen for five operands, and over "
            "fifty-eight thousand for twelve. We counted them with the CYK algorithm of chapter eleven. <bookmark "
            "mark='c'/> The layered grammar with expressions, terms and factors describes the same strings with "
            "exactly one tree each. Removing ambiguity is part of designing a language."
        ) as vo:
            self.play(FadeIn(head), FadeIn(gram))
            vo.wait_until("a")
            self.play(FadeIn(t1), FadeIn(l1))
            self.play(FadeIn(t2), FadeIn(l2))
            vo.wait_until("b")
            self.play(FadeIn(tl), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[r])) for r in range(1, len(tab.cells))], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(fix))
        self.wait(0.3)
        self.clear_scene()

    def dangling(self):
        head = label(r"The dangling \texttt{else}", font_size=36).to_edge(UP, buff=0.3)
        src = Text("if c then if c then x else x", font="DejaVu Sans Mono", font_size=26, color=CODE).next_to(
            head, DOWN, buff=0.4)
        a = code(["if c then", "    if c then x", "    else x       # the inner if"], size=19, color=YES)
        b = code(["if c then", "    if c then x", "else x           # the outer if"], size=19, color=NO)
        VGroup(a, b).arrange(RIGHT, buff=1.5).next_to(src, DOWN, buff=0.5)
        two = label(r"two trees: \ CYK counts 2", font_size=20, color=NO).next_to(VGroup(a, b), DOWN, buff=0.3)
        fixes = VGroup(
            label(r"C, \ Java, \ Pascal: \ a rule outside the grammar \ --- \ \texttt{else} belongs to the nearest "
                  r"\texttt{if}", font_size=20, color=GREY_A),
            label(r"the Pebble language: \ every branch is a \texttt{\{ block \}}, \ so the question never arises",
                  font_size=20, color=YES),
            label(r"and in general? \ ``Is this grammar ambiguous?'' \ is \textit{undecidable} \ (1962; \ Part 25)",
                  font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The most famous ambiguity in programming is the dangling else. <bookmark mark='a'/> In if c then if c "
            "then x else x, does the else belong to the inner if, or the outer one? <bookmark mark='b'/> The usual "
            "grammar allows both, and CYK finds two trees. <bookmark mark='c'/> C, Java and Pascal settle it with a "
            "rule outside the grammar: an else belongs to the nearest if. <bookmark mark='d'/> The Pebble language "
            "avoids the question by requiring braces around every branch. <bookmark mark='e'/> Can a program "
            "always detect ambiguity for us? No. Whether a context-free grammar is ambiguous is undecidable, as "
            "Cantor, Floyd, and Chomsky and Schützenberger showed in the early 1960s; we will see what that means "
            "in Part 25."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(a), FadeIn(b), FadeIn(two))
            for mk, f in zip("cde", fixes):
                vo.wait_until(mk)
                self.play(FadeIn(f, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
