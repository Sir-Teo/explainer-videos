from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs12.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, chips, code, load, region, tree)
from videos.cs.cs12.s03_regex import mod3_diagram


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


def lr_actions():
    acts = [a["action"][0] + (str(a["action"][1]) if a["action"][0] != "acc" else "") for a in load("lr")["trace"]]
    return ["  ".join(acts[k:k + 4]) for k in range(0, len(acts), 4)]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        lx = load("lexer")
        tiles = Group(
            tile(mod3_diagram(), r"automata", DATA),
            tile(Text("(0|1(01*0)*1)*", font="DejaVu Sans Mono", font_size=26, color=HEAD), r"Kleene's theorem",
                 HEAD),
            tile(VGroup(*[Text(f"{x}[{y}{y}]{z}", font="DejaVu Sans Mono", font_size=18, color=NO) for x, y, z in
                          (("a", "a", "aaabbbbb"), ("", "aa", "aaabbbbb"), ("aa", "a", "aabbbbb"))]).arrange(DOWN),
                 r"the pumping lemma", NO),
            tile(chips(lx["sample_tokens"][:8], font_size=16, max_width=4), r"tokens", CTRL),
            tile(tree(("E", [("E", [("T", [("F", ["id"])])]), "+", ("T", [("T", [("F", ["id"])]), "*",
                                                                            ("F", ["id"])])]), dx=0.5, dy=0.45,
                      font_size=15), r"grammars and parse trees", YES),
            tile(code(lr_actions(), size=18), r"LR parsing", FUNC),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ Languages and Automata", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            "What we built in this part. Languages as sets of strings, and the machines that recognize them. "
            "Regular expressions and finite automata, joined by Thompson's construction, the subset construction "
            "and state elimination, with minimization and its two-to-the-n price. The pumping lemma, and why "
            "backtracking engines can take exponential time where an automaton takes linear. A lexer for the "
            "Pebble language. Context-free grammars, ambiguity and pushdown automata; CYK and Earley; LL one and "
            "Pratt from the top down, and LR, SLR and LALR from the bottom up, checked against bison. And the "
            "Pebble language's own grammar and parser, run on the Job."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the syntax tree, \ compiled", [13]),
            (r"declare-before-use, \ types: \ beyond context-free", [14]),
            (r"CYK as dynamic programming", [19]),
            (r"string matching, \ suffix automata", [21]),
            (r"``is this grammar ambiguous?'' \ undecidable", [25]),
            (r"back-references, \ SETH", [26]),
            (r"tokenizing the web", [47]),
        ], font_size=24)
        with self.voiceover(
            "Where this comes back. Part 13 compiles the tree that the parser builds. Part 14 handles what a "
            "grammar cannot, such as types and declarations. CYK returns in Part 19 as dynamic programming, and "
            "finite automata in Part 21's string algorithms. Part 25 proves that ambiguity is undecidable, and "
            "Part 26 explains the NP-completeness of back-references and the hypothesis behind the frontier "
            "chapter. And every search engine of Part 47 begins by tokenizing."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"regex engines", r"RE2, \ Go, \ Rust: \ linear time; \ PCRE, \ Python, \ Java: \ backtracking"),
            (r"ReDoS", r"never run an untrusted pattern on a backtracker; \ set timeouts"),
            (r"parser generators", r"bison, \ ANTLR \ (LL(*)), \ tree-sitter \ (incremental, \ for editors)"),
            (r"hand-written", r"GCC, \ Clang, \ Go, \ Rust: \ recursive descent with Pratt-style expressions"),
            (r"formats", r"JSON, \ YAML, \ protocol parsers: \ where security bugs live"),
        ])
        with self.voiceover(
            "In practice. Choose a regular expression engine knowing which kind it is: RE2, Go and Rust guarantee "
            "linear time, while PCRE, Python and Java backtrack. Never run a pattern supplied by a user on a "
            "backtracking engine without a time limit. Parser generators range from bison to ANTLR to tree-sitter, "
            "which reparses incrementally as you type in an editor. Most production compilers are hand-written "
            "recursive descent parsers. And parsers for data formats and network protocols are where a great many "
            "security bugs live."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Draw a DFA for binary numbers divisible by 5, \ and turn it into a regular expression by state "
            r"elimination.",
            r"Use the pumping lemma to show that $\{\, w \in \{a,b\}^* : w$ has as many $a$'s as $b$'s$\,\}$ is not "
            r"regular.",
            r"Show that $S \to S\,S \mid (\,S\,) \mid \varepsilon$ is ambiguous, \ and write an unambiguous grammar "
            r"for the same language.",
            r"Compute FIRST and FOLLOW for the grammar of problem 3's answer, \ and decide whether it is LL(1).",
            r"\textit{Build.} \ Add \texttt{for} loops and the operators \texttt{+=} and \texttt{++} to the Pebble "
            r"language: \ lexer, \ grammar, \ parser. \ Does the grammar stay LALR(1)?",
            r"$\bigstar$ \textit{Research.} \ For which regular expressions can matching be done in time "
            r"$O(n + m)$, \ and for which does SETH forbid it? \ Complete the classification.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: extend the Pebble language with for loops and two new operators, through every stage, and "
            "find out whether its grammar is still LALR. The last, marked with a star, is a research problem: its "
            "answer is not known, and the notes say where to start."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 13, \ The Compiler", font_size=42).to_edge(UP, buff=0.6)
        flow = VGroup(region(2.4, 0.8, r"syntax tree", YES, font_size=22), region(2.6, 0.8, r"control-flow graph",
                                                                                 CTRL, font_size=20),
                      region(2.0, 0.8, r"SSA", DATA, font_size=22), region(2.6, 0.8, r"Pebble machine code", FUNC,
                                                                           font_size=20)).arrange(RIGHT, buff=0.5)
        arrows = VGroup(*[Arrow(flow[k].get_right(), flow[k + 1].get_left(), buff=0.08, color=GREY_B)
                          for k in range(3)])
        q = label(r"can a program write the Job's assembly better than we did by hand?", font_size=28,
                  color=HEAD).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time. The tree becomes a graph, the graph is optimized as a fixed point over lattices, registers "
            "are allocated by colouring, and out comes Pebble machine code: written by a program, for the first "
            "time in this series. Part 13, The Compiler."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(f) for f in flow], lag_ratio=0.3), FadeIn(arrows))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Sipser, \textit{Introduction to the Theory of Computation}, ch. 1--2",
             r"Hopcroft, Motwani and Ullman, \textit{Introduction to Automata Theory, Languages, and Computation}",
             r"Aho, Lam, Sethi and Ullman, \textit{Compilers} (the Dragon Book), ch. 2--4",
             r"Grune and Jacobs, \textit{Parsing Techniques}; \ Nystrom, \textit{Crafting Interpreters}"],
            [r"Kleene, ``Representation of events in nerve nets and finite automata'' (1956)",
             r"Rabin and Scott, ``Finite automata and their decision problems'' (1959)",
             r"Thompson, ``Regular expression search algorithm'' (1968)",
             r"Chomsky, ``Three models for the description of language'' (1956)",
             r"Knuth, ``On the translation of languages from left to right'' (1965)",
             r"Earley, ``An efficient context-free parsing algorithm'' (1970)",
             r"Pratt, ``Top down operator precedence'' (1973)",
             r"Valiant, ``General context-free recognition in less than cubic time'' (1975)",
             r"Cox, ``Regular expression matching can be simple and fast'' (2007)",
             r"Backurs and Indyk, ``Which regular expression patterns are hard to match?'' (2016)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
