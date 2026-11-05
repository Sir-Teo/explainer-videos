from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs12.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, ast_tree, code, grid_table, load,
                                   region, tree)


class Pebble(VoiceoverScene):
    def construct(self):
        self.card()
        self.design()
        self.grammar()
        self.tree_()
        self.errors()

    def card(self):
        card = chapter_card(14, r"The Pebble language, \ parsed", r"What does the Job look like to a compiler?",
                            part=PART)
        with self.voiceover("Chapter fourteen. The Pebble language, parsed."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def design(self):
        head = label(r"A language designed to be parsed", font_size=36).to_edge(UP, buff=0.3)
        src = code(["struct Node {", "    next: *Node; letters: *char;", "    length: int; count: int;", "}",
                    "var head: *Node = null;",
                    "fn same(a: *char, b: *char, n: int) -> int {", "    var i: int = 0;", "    while i < n {",
                    "        if a[i] != b[i] { return 0; }", "        i = i + 1;", "    }", "    return 1;", "}"],
                   size=16).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        pts = VGroup(
            label(r"names come first: \ \texttt{x: *int}", font_size=20, color=YES),
            label(r"C's \texttt{a * b;} \ is a multiplication \textit{or} a declaration, \ depending on what "
                  r"\texttt{a} is", font_size=19, color=GREY_A),
            label(r"every statement starts with a keyword or an expression", font_size=20, color=YES),
            label(r"every branch is a \texttt{\{ block \}}: \ no dangling \texttt{else}", font_size=20, color=YES),
            label(r"structs, \ pointers, \ arrays, \ functions: \ enough for the Job", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(src, RIGHT, buff=0.6)
        if pts.get_right()[0] > 6.9:
            pts.scale_to_fit_width(6.9 - pts.get_left()[0])
        with self.voiceover(
            "Now we can design the Pebble language with all of this in mind. <bookmark mark='a'/> It has structs, "
            "pointers, arrays and functions, enough to write the Job. <bookmark mark='b'/> Declarations put the "
            "name first, then its type. C does it the other way round, and pays for it: in C, a star b semicolon "
            "is either a multiplication or the declaration of a pointer, depending on whether a names a type, so a "
            "C parser has to consult the symbol table while it parses. <bookmark mark='c'/> Every statement starts "
            "with a keyword or an expression, so one token of lookahead decides what comes next. <bookmark "
            "mark='d'/> And every branch of an if is a block in braces, so there is no dangling else."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(pts[4]))
            vo.wait_until("b")
            self.play(FadeIn(pts[0]), FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()

    def grammar(self):
        pb = load("pebble")
        head = label(r"Its grammar, \ and its LALR table", font_size=36).to_edge(UP, buff=0.3)
        lines = [l for l in pb["bnf"] if l.split(" ->")[0] in ("Stmt", "IfStmt", "Type", "Add", "Mul", "Un", "Post",
                                                                  "Prim", "FnDecl", "Block")]
        bnf = VGroup(*[Text(l if len(l) < 92 else l[:89] + "...", font="DejaVu Sans Mono", font_size=13,
                            color=CODE) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        bnf.next_to(head, DOWN, buff=0.35)
        if bnf.width > 13:
            bnf.scale_to_fit_width(13)
        stats = VGroup(
            label(rf"{pb['prods']} rules, \ {pb['nonterms']} nonterminals, \ {pb['terms']} kinds of token", font_size=21,
                  color=GREY_A),
            label(rf"our LALR(1) table: \ {pb['lalr_states']} states, \ {pb['lalr_conflicts']} conflicts \ (even SLR has "
                  rf"{pb['slr_conflicts']}); \ bison: \ {pb['bison']['states']} states, \ no conflicts", font_size=21,
                  color=YES),
            label(rf"the Job: \ {pb['tokens']} tokens, \ accepted by the LR parser \textit{{and}} by the hand-written "
                  r"recursive-descent and Pratt parser", font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is part of the grammar of the Pebble language, written as plain context-free rules. <bookmark "
            "mark='a'/> Seventy-nine rules in all, with the expression levels spelled out for the LR tables. "
            "<bookmark mark='b'/> Our LALR construction gives a table of a hundred and forty-six states, with no "
            "conflicts at all, and even the simpler SLR method has none. Bison, given the same rules, agrees: one "
            "more state, as always, and no conflicts. <bookmark mark='c'/> And both parsers we built, the "
            "table-driven LR parser and the hand-written recursive descent parser with Pratt's method for "
            "expressions, accept all six hundred and fifty-one tokens of the Job. Two independent parsers agreeing "
            "on the same grammar is the kind of check this series relies on."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l) for l in bnf], lag_ratio=0.15), FadeIn(stats[0]), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(stats[1]))
            vo.wait_until("c")
            self.play(FadeIn(stats[2]))
        self.wait(0.3)
        self.clear_scene()

    def tree_(self):
        pb = load("pebble")
        from explainer.cs.lang import pebble_lang as P
        prog = P.parse(P.JOB)
        lookup = next(f for f in prog.funcs if f.name == "lookup")
        wh = lookup.body.stmts[1]
        head = label(r"What the parser hands to the compiler", font_size=34).to_edge(UP, buff=0.3)
        src = code(["while p != null {", "    if p.length == n && same(p.letters, w, n) { return p; }",
                    "    p = p.next;", "}"], size=17).next_to(head, DOWN, buff=0.3)
        t = tree(ast_tree(wh), dx=0.78, dy=0.62, font_size=16).next_to(src, DOWN, buff=0.4)
        if t.width > 13:
            t.scale_to_fit_width(13)
        if t.height > 4.0:
            t.scale_to_fit_height(4.0)
        t.next_to(src, DOWN, buff=0.35)
        cap = label(rf"an abstract syntax tree: \ no brackets, \ no semicolons, \ just structure; \ \texttt{{lookup}}: "
                    rf"\ {pb['lookup_nodes']} nodes, \ the Job: \ {pb['nodes']}", font_size=19, color=YES).to_edge(
            DOWN, buff=0.3)
        with self.voiceover(
            "This is what all the machinery produces. <bookmark mark='a'/> The loop at the heart of lookup, "
            "<bookmark mark='b'/> as an abstract syntax tree. The brackets, braces and semicolons are gone; they "
            "were only there to show the structure, and now the structure itself is explicit. The loop has a "
            "condition and a body; the body is an if and an assignment; the condition of the if is an and of a "
            "comparison and a call. <bookmark mark='c'/> The whole Job becomes three hundred and seventy-one nodes "
            "like these. In Part 13, the compiler walks this tree and writes Pebble machine code, replacing the "
            "assembly we have written by hand since Part 6."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(t.edges), LaggedStart(*[FadeIn(m) for m, _ in t.nodes], lag_ratio=0.04), run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    def errors(self):
        pb = load("pebble")
        head = label(r"And when the program is wrong", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup()
        for src, msg in pb["errors"].items():
            rows.add(VGroup(Text(src, font="DejaVu Sans Mono", font_size=19, color=CODE),
                            Text(msg, font="DejaVu Sans Mono", font_size=16, color=NO)).arrange(DOWN, aligned_edge=LEFT,
                                                                                             buff=0.08))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.5)
        pts = VGroup(
            label(r"an LL or LR parser stops at the \textit{first} token that cannot continue any valid program",
                  font_size=20, color=GREY_A),
            label(r"so it can always say where, \ and what it expected: \ the ``viable prefix'' property",
                  font_size=20, color=YES),
            label(r"saying \textit{why}, \ and recovering to find the next error, \ is an art: \ Part 13 and the "
                  r"notes", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Parsers also have to deal with programs that are wrong. <bookmark mark='a'/> Here are four broken "
            "fragments and what our parser says about each: an expression missing after an equals sign, a missing "
            "semicolon, a missing name, a missing colon. <bookmark mark='b'/> LL and LR parsers have a valuable "
            "property: they stop at the very first token that cannot be the continuation of any valid program, so "
            "they can always say exactly where the error is and what they expected instead. <bookmark mark='c'/> "
            "Explaining why, and recovering well enough to report the next error too, is more art than science."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.4), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(pts[0]), FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()
