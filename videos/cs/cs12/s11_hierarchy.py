from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs12.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, grid_table, load, region)


def stack_mob(st, w=0.9, h=0.45):
    cells = VGroup()
    for ch in reversed(st):                  # bottom first
        c = YES if ch == "$" else CTRL
        r = Rectangle(width=w, height=h, stroke_color=c, stroke_width=1.6, fill_color=c, fill_opacity=0.18)
        cells.add(VGroup(r, Text(ch, font="DejaVu Sans Mono", font_size=20, color=WHITE).move_to(r)))
    return cells.arrange(UP, buff=0)


class Hierarchy(VoiceoverScene):
    def construct(self):
        self.card()
        self.pda()
        self.guess()
        self.ladder()
        self.edges()

    def card(self):
        card = chapter_card(10, r"Stacks and the Chomsky hierarchy", r"What does one stack add?", lit=(1956,),
                            extra=((1956, r"Chomsky: \ the hierarchy"),), part=PART)
        with self.voiceover("Chapter ten. Stacks, and the Chomsky hierarchy."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def pda(self):
        pd = load("pda")
        path = pd["anbn_path"]
        head = label(r"A pushdown automaton for $a^n b^n$", font_size=34).to_edge(UP, buff=0.3)
        sd = StateDiagram({"p": (-5.0, 1.2), "q": (-1.6, 1.2), "f": (1.8, 1.2)},
                          [("p", "p", "a / +A", UP), ("p", "q", "ε", 0), ("q", "q", "b / −A", UP),
                           ("q", "f", "ε / $", 0)], radius=0.45, accept=("f",), font_size=24, edge_font=17)
        word = "aaabbb"
        cells = VGroup(*[Text(c, font="DejaVu Sans Mono", font_size=32, color=DATA if c == "a" else CTRL)
                         for c in word]).arrange(RIGHT, buff=0.3).move_to([-1.6, -1.4, 0])
        ptr = Triangle(color=HEAD, fill_opacity=1).scale(0.1).rotate(PI)
        st = stack_mob(path[0][2]).move_to([5.0, -1.5, 0], aligned_edge=DOWN)
        stl = label(r"the stack", font_size=19, color=GREY_B).move_to([5.0, -2.2, 0])
        expl = VGroup(
            label(r"in $p$: \ push an $A$ for every $a$", font_size=20, color=DATA),
            label(r"guess the middle, \ move to $q$: \ pop an $A$ for every $b$", font_size=20, color=CTRL),
            label(r"accept if the stack is back to its bottom marker \texttt{\$} as the input ends", font_size=20,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.3).to_edge(LEFT, buff=0.6)
        with self.voiceover(
            "Give a finite automaton one extra thing, a stack: an unbounded pile it can push symbols onto and pop "
            "them from, but only at the top. That is a pushdown automaton. <bookmark mark='a'/> For a to the n b to "
            "the n, it needs only three states. In the first, it pushes a marker for every a. <bookmark mark='b'/> "
            "Then it moves to the second state and pops a marker for every b. <bookmark mark='c'/> If the stack is "
            "back to its bottom exactly when the input runs out, there were as many b's as a's. The stack is the "
            "unbounded counter that the pumping lemma said no finite machine could have."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sd), FadeIn(cells), FadeIn(st), FadeIn(stl))
            self.play(sd.light("p"))
            vo.wait_until("a")
            self.play(FadeIn(expl[0]))
            prev_pos = 0
            for k, (state, pos, stack) in enumerate(path[1:], start=1):
                if k == 4:
                    vo.wait_until("b")
                    self.play(FadeIn(expl[1]))
                if k == 8:
                    vo.wait_until("c")
                    self.play(FadeIn(expl[2]))
                anims = [sd.light(state)]
                if pos != prev_pos:
                    ptr.next_to(cells[pos - 1], UP, buff=0.06)
                    anims += [cells[pos - 1].animate.set_color(GREY_C)]
                new = stack_mob(stack).move_to([5.0, -1.5, 0], aligned_edge=DOWN)
                anims.append(Transform(st, new))
                self.play(*anims, run_time=0.6)
                prev_pos = pos
        self.wait(0.3)
        self.clear_scene()

    def guess(self):
        pd = load("pda")
        head = label(r"Nondeterminism matters here", font_size=34).to_edge(UP, buff=0.3)
        pal = pd["palindromes"]
        g = VGroup(*[VGroup(Text(w, font="DejaVu Sans Mono", font_size=22, color=CODE),
                            label(r"accepted" if ok else r"rejected", font_size=19, color=YES if ok else NO)).arrange(
            RIGHT, buff=0.3) for w, ok in pal.items()]).arrange_in_grid(2, 3, buff=(0.9, 0.3)).next_to(head, DOWN,
                                                                                                buff=0.6)
        pts = VGroup(
            label(r"palindromes: \ push the first half, \ pop against the second \ --- \ but where is the middle?",
                  font_size=21, color=GREY_A),
            label("unmarked palindromes over $\\{a,b\\}$: NPDA guesses the midpoint; no DPDA recognizes this language", font_size=21, color=NO),
            label(r"context-free grammars $\iff$ nondeterministic PDAs \ (Chomsky, \ Evey, \ Schützenberger, \ "
                  r"1962--63)", font_size=21, color=HEAD),
            label("deterministic PDA languages correspond to LR languages under standard end-marker conventions",
                  font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(g, DOWN, buff=0.55)
        with self.voiceover(
            (
            "Nondeterminism does not enlarge the regular languages, but it does enlarge what a single-stack "
            "automaton can recognize. <bookmark mark='a'/> Consider unmarked palindromes over a and b. A stack "
            "can store a first half and compare it with the reverse of the second, but the midpoint is not "
            "announced. <bookmark mark='b'/> A nondeterministic pushdown automaton can guess that midpoint; our "
            "simulator explores guesses and accepts when one succeeds. This unmarked two-symbol palindrome "
            "language is not deterministic context-free. A visible middle separator, or a unary alphabet, changes "
            "that claim. <bookmark mark='c'/> Nondeterministic pushdown automata recognize exactly the "
            "context-free languages. <bookmark mark='d'/> Deterministic pushdown automata recognize a proper "
            "subclass. With the usual end-marker conventions, LR methods characterize deterministic context-free "
            "languages, while a particular grammar may still have conflicts. Programming-language syntax often "
            "aims for a deterministic core."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def ladder(self):
        head = label(r"The Chomsky hierarchy", font_size=36).to_edge(UP, buff=0.3)
        rows = [
            (r"type 3: \ regular", r"$A \to aB$, \ $A \to a$", r"finite automaton", r"tokens", DATA),
            (r"type 2: \ context-free", r"$A \to \alpha$", r"pushdown automaton", r"program structure", CTRL),
            (r"type 1: \ context-sensitive", r"$\alpha A \beta \to \alpha \gamma \beta$", r"linear-bounded automaton",
             r"$a^n b^n c^n$; \ declare before use", YES),
            (r"type 0: \ recursively enumerable", r"any rewriting", r"Turing machine", r"anything a program can "
                                                                                       r"search for", FUNC),
        ]
        g = VGroup()
        for k, (name, rule, mach, ex, c) in enumerate(rows):
            box_ = Rectangle(width=12.6, height=0.8, stroke_color=c, stroke_width=1.8, fill_color=c,
                             fill_opacity=0.08 + 0.03 * k)
            t = VGroup(label(name, font_size=20, color=c), label(rule, font_size=20, color=GREY_A),
                       label(mach, font_size=19, color=GREY_A), label(ex, font_size=18, color=GREY_B))
            for x, pos in zip(t, (-6.0, -2.9, -0.3, 2.6)):
                x.move_to([pos, 0, 0], aligned_edge=LEFT)
            g.add(VGroup(box_, t))
        g.arrange(UP, buff=0.1).next_to(head, DOWN, buff=0.45)
        for r in g:
            for x, pos in zip(r[1], (-6.0, -2.9, -0.3, 2.6)):
                x.align_to([pos, 0, 0], LEFT)
        pump = label("$\\{a^n b^n c^n:n\\ge0\\}$ is not context-free, by the CFL pumping lemma", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.9)
        prog = label("compiler stages: tokens, syntax, then names and types (compiler Part 13; type theory Part 14)", font_size=20, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover("The hierarchy relates grammar restrictions to machine resources. <bookmark mark='a'/> Regular languages correspond to finite automata. They describe the token forms used here. <bookmark mark='b'/> Context-free languages correspond to nondeterministic pushdown automata, including unbounded nested syntax. <bookmark mark='c'/> Context-sensitive languages correspond to linear-bounded machines, under the usual empty-word conventions. Equal runs of a's, b's and c's give a standard language in this class that is not context-free; the context-free pumping lemma supplies a proof. <bookmark mark='d'/> Recursively enumerable languages are recognized by Turing machines. Recognition may run forever on strings outside the language. No finite workspace limit is fixed in advance. <bookmark mark='e'/> Compiler design separates these responsibilities: tokenization, syntax, then name and type checks. Part thirteen implements a small compiler checker; Part fourteen studies types more deeply. The hierarchy guides this separation without assigning every production-language feature a simple grammar class.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            for mk, r in zip('abcd', g):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
                if mk == 'c':
                    self.play(FadeIn(pump))
                if mk == 'a':
                    vo.wait_until(mk)
            vo.wait_until('e')
            self.play(FadeIn(prog))
        self.wait(0.3)
        self.clear_scene()

    def edges(self):
        head = label(r"Real languages at the edges", font_size=36).to_edge(UP, buff=0.3)
        cases = [
            (r"C", code(["typedef int T;", "T * x;       // declares a pointer", "int a, b;", "a * b;       "
                                                                                      "// multiplies"], size=17),
             r"the same tokens parse two ways: \ the parser asks the symbol table \ (the ``lexer hack'')", CTRL),
            (r"C++", code(["a < b > c;   // a comparison, or a template?"], size=17),
             "unbounded template computation makes some semantic decisions undecidable; real compilers have limits", NO),
            (r"Perl", code(["whatever / 25 ; # / ;", "   die \"this dies!\";"], size=17),
             "Perl compilation can execute unrestricted code; resulting semantic decisions exceed fixed-CFG recognition", FUNC),
        ]
        g = VGroup()
        for name, src, why, c in cases:
            top = VGroup(label(name, font_size=26, color=c), src).arrange(RIGHT, buff=0.5, aligned_edge=UP)
            w = label(why, font_size=20, color=GREY_A)
            if w.width > 12.4:
                w.scale_to_fit_width(12.4)
            g.add(VGroup(top, w).arrange(DOWN, aligned_edge=LEFT, buff=0.15))
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        lesson = label(r"the hierarchy is a design tool: \ the Pebble language stays inside the context-free, \ "
                       r"LALR(1) world on purpose", font_size=21, color=YES).to_edge(DOWN, buff=0.4)
        with self.voiceover("Production languages often need information beyond a context-free syntax table. <bookmark mark='a'/> In C, a star b semicolon can declare a pointer when a is a typedef name, or form an expression otherwise. Parsers commonly consult a symbol table; one implementation technique is called the lexer hack. <bookmark mark='b'/> In C plus plus, template-dependent names can affect disambiguation. Unrestricted template computation makes some semantic decisions undecidable in an idealized unbounded model; this is more specific than saying every syntactic parsing task is undecidable. Real implementations impose resource limits. <bookmark mark='c'/> Perl can execute code during compilation, and declarations can change how later text is interpreted. Its unrestricted compilation model has analogous limits, beyond recognizing strings with a fixed grammar. <bookmark mark='d'/> The hierarchy remains useful for separating responsibilities. Pebble uses a deliberately simple context-free syntax, with a conflict-free LALR grammar; later passes check names, types and other semantic conditions.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            for mk, r in zip('abc', g):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
            vo.wait_until('d')
            self.play(FadeIn(lesson))
        self.wait(0.3)
        self.clear_scene()
