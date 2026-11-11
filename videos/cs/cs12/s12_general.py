from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs12.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, grid_table, load, region)


def item_text(prod, dot, origin):
    lhs, rhs = prod.split(" → ")
    syms = [] if rhs == "ε" else rhs.split()
    return f"{lhs} → {' '.join(syms[:dot] + ['•'] + syms[dot:])}   ({origin})"


class General(VoiceoverScene):
    def construct(self):
        self.card()
        self.cyk()
        self.earley()
        self.cost()

    def card(self):
        card = chapter_card(11, r"Parsing any grammar: \ CYK and Earley", r"Can every context-free grammar be "
                                                                          r"parsed efficiently?",
                            lit=(1967, 1970), extra=((1967, r"Younger: \ CYK in $n^3$"), (1970, r"Earley")), part=PART)
        with self.voiceover("Chapter eleven. Parsing any grammar: CYK and Earley."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def cyk(self):
        c = load("cyk")
        toks = c["tokens"]
        n = len(toks)
        head = label(r"CYK: \ dynamic programming over every substring", font_size=34).to_edge(UP, buff=0.3)
        cnf = label(r"first rewrite the grammar so every rule is $A \to BC$ or $A \to a$ \ (Chomsky normal form): \ "
                    rf"{len(c['cnf'])} rules", font_size=19, color=GREY_B).next_to(head, DOWN, buff=0.2)
        W, H = 2.0, 0.62
        cells, texts = {}, VGroup()
        grid = VGroup()
        x0 = -W * n / 2 + W / 2
        y0 = -2.7
        for l in range(1, n + 1):
            for i in range(n - l + 1):
                x = x0 + W * (i + (l - 1) / 2)
                y = y0 + H * (l - 1) * 1.05
                r = Rectangle(width=W * 0.96, height=H * 0.95, stroke_color=GREY_C, stroke_width=1.2, fill_opacity=0)
                r.move_to([x, y, 0])
                nts = c["cells"][f"{i},{l}"]
                t = Text(" ".join(nts) if nts else "·", font="DejaVu Sans Mono", font_size=14,
                         color=YES if "E₀" in nts and l == n else (CTRL if nts else GREY_D))
                if t.width > W * 0.9:
                    t.scale_to_fit_width(W * 0.9)
                t.move_to(r)
                cells[(i, l)] = VGroup(r, t)
                grid.add(cells[(i, l)])
        tokrow = VGroup(*[Text(t, font="DejaVu Sans Mono", font_size=22, color=CODE).move_to(
            [x0 + W * i, y0 - 0.65, 0]) for i, t in enumerate(toks)])
        expl = VGroup(
            label(r"row $\ell$, \ column $i$: \ every nonterminal that derives the $\ell$ tokens starting at $i$",
                  font_size=19, color=GREY_A),
            label(r"fill it from the cells below: \ split the span in two, \ look for a rule $A \to BC$", font_size=19,
                  color=GREY_A),
            label(r"the start symbol in the top cell: \ the sentence is in the language", font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35).shift(DOWN * 1.15)
        with self.voiceover("General context-free recognition can be organized as dynamic programming. <bookmark mark='a'/> Convert the grammar to Chomsky normal form: rules producing two nonterminals or one terminal, with the empty-string case handled separately. Grammar conversion can change size and derivation multiplicities even while preserving the language. <bookmark mark='b'/> In the CYK table, a cell records which nonterminals derive a particular input span. Single-token spans supply the first row. <bookmark mark='c'/> For each larger span, try its split points and rules of the form A to B C. Combine the corresponding smaller cells. <bookmark mark='d'/> The start symbol in the full-span cell means acceptance. For a fixed grammar this gives an O n cubed worst-case upper bound; grammar size contributes when the grammar is also part of the input. The table can retain parse information, but enumerating every tree of an ambiguous grammar can cost much more.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(cnf), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(tokrow), FadeIn(expl[0]))
            self.play(LaggedStart(*[FadeIn(cells[i, 1]) for i in range(n)], lag_ratio=0.2))
            vo.wait_until('c')
            self.play(FadeIn(expl[1]))
            for l in range(2, n + 1):
                self.play(LaggedStart(*[FadeIn(cells[i, l]) for i in range(n - l + 1)], lag_ratio=0.2), run_time=0.9)
            vo.wait_until('d')
            self.play(FadeIn(expl[2]), Indicate(cells[0, n], color=YES))
        self.wait(0.3)
        self.clear_scene()

    def earley(self):
        head = label(r"Earley's parser: \ items with a dot", font_size=34).to_edge(UP, buff=0.3)
        sets = [
            [("E' → E", 0, 0), ("E → E + T", 0, 0), ("E → T", 0, 0), ("T → T * F", 0, 0), ("T → F", 0, 0),
             ("F → ( E )", 0, 0), ("F → id", 0, 0)],
            [("F → id", 1, 0), ("T → F", 1, 0), ("E → T", 1, 0), ("T → T * F", 1, 0), ("E' → E", 1, 0),
             ("E → E + T", 1, 0)],
            [("E → E + T", 2, 0), ("T → T * F", 0, 2), ("T → F", 0, 2), ("F → id", 0, 2)],
            [("F → id", 1, 2), ("T → F", 1, 2), ("E → E + T", 3, 0), ("E' → E", 1, 0)],
        ]
        toks = ["id", "+", "id"]
        cols = VGroup()
        for k, S in enumerate(sets):
            hdr = label(rf"set {k}" + (rf" \ (after \texttt{{{toks[k - 1]}}})" if k else r" \ (start)"),
                        font_size=18, color=HEAD)
            items = VGroup(*[Text(item_text(*it), font="DejaVu Sans Mono", font_size=14,
                                  color=YES if it == ("E' → E", 1, 0) and k == 3 else GREY_A) for it in S]).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08)
            cols.add(VGroup(hdr, items).arrange(DOWN, aligned_edge=LEFT, buff=0.15))
        cols.arrange(RIGHT, buff=0.35, aligned_edge=UP).next_to(head, DOWN, buff=0.4)
        if cols.width > 13.2:
            cols.scale_to_fit_width(13.2)
        ops = VGroup(
            label(r"an item: \ a rule, \ a dot saying how much has been seen, \ and where it started", font_size=19,
                  color=GREY_A),
            label(r"\textbf{predict}: \ dot before a nonterminal $\to$ add its rules \quad \textbf{scan}: \ dot before "
                  r"the next token $\to$ move the dot", font_size=19, color=CTRL),
            label(r"\textbf{complete}: \ a finished item advances the items that were waiting for it", font_size=19,
                  color=DATA),
            label("any CFG, including left recursion: cubic worst-case bound for fixed grammar; faster on suitable classes", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover("Earley's method works directly with context-free grammar rules, including left recursion and ambiguity. <bookmark mark='a'/> At each input position it stores items: a rule, a dot marking progress, and the position where that rule began. <bookmark mark='b'/> Prediction adds rules for an expected nonterminal. Scanning advances a dot across a matching input token. <bookmark mark='c'/> Completion advances items waiting for a nonterminal that has just finished. Duplicate items must be merged, and nullable rules need careful handling. <bookmark mark='d'/> A completed start item spanning the entire input means acceptance. For fixed grammars, the standard worst-case bound is cubic, improving to quadratic for unambiguous grammars; suitable specialized implementations achieve linear bounds on important deterministic families. Those time bounds concern the complete algorithm, not just the number of stored items.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(cols[0]), FadeIn(ops[0]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(cols[1]), FadeIn(cols[2]), FadeIn(ops[1]))
            vo.wait_until('c')
            self.play(FadeIn(cols[3]), FadeIn(ops[2]))
            vo.wait_until('d')
            self.play(FadeIn(ops[3]))
        self.wait(0.3)
        self.clear_scene()

    def cost(self):
        c = load("cyk")
        tm = c["timing"]
        head = label(r"Measured: \ Earley's items, \ ambiguous and not", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 70, 10], y_range=[0, 2500, 500], x_length=7.0, y_length=4.2, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16, "include_numbers": True}).to_edge(LEFT, buff=1.0)
        ax.shift(DOWN * 0.4)
        xl = label(r"tokens", font_size=18, color=GREY_B).next_to(ax, DOWN, buff=0.35)
        yl = label(r"Earley items", font_size=18, color=GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        u = VMobject(color=YES, stroke_width=4).set_points_as_corners([ax.c2p(r["n"], r["earley_items"]) for r in tm])
        a = VMobject(color=NO, stroke_width=4).set_points_as_corners(
            [ax.c2p(r["n"], r["earley_ambiguous_items"]) for r in tm])
        ul = label("$E,T,F$: near-linear items (this sample)", font_size=19, color=YES).next_to(ax.c2p(60, tm[-1]["earley_items"]),
                                                                                  UP, buff=0.15)
        al = label(r"$E \to E + E \mid E * E \mid \dots$: \ quadratic", font_size=19, color=NO).next_to(
            ax.c2p(42, 1800), LEFT, buff=0.1)
        last = tm[-1]
        side = VGroup(
            label(rf"{last['n']} tokens:", font_size=20, color=GREY_B),
            label(rf"Earley, \ unambiguous: \ {last['earley_items']} items", font_size=20, color=YES),
            label(rf"Earley, \ ambiguous: \ {last['earley_ambiguous_items']:,} items", font_size=20, color=NO),
            label(rf"CYK: \ {1000 * last['cyk']:.1f} ms \\ fixed-grammar cubic upper bound", font_size=20, color=CTRL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(ax, RIGHT, buff=0.6)
        with self.voiceover(
            "These curves count stored Earley items, separately from elapsed time. <bookmark mark='a'/> On sums of identifiers in our layered expression grammar, the sampled item counts grow approximately linearly with token count. <bookmark mark='b'/> On the ambiguous grammar, the counts grow faster: the sixty-five-token sample stores two thousand three hundred and seventy-seven items. More parse trees need not mean that every tree is explicitly enumerated. <bookmark mark='c'/> The side panel also records a CYK duration from this host. Its cubic worst-case bound is a mathematical statement for fixed grammars; a finite item-count plot does not prove a runtime bound. Restricted predictive and LR grammars let the next chapters use simpler, linear-time parsing strategies."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(u), FadeIn(ul), FadeIn(side[0]), FadeIn(side[1]), run_time=.6)
            vo.wait_until("a")
            self.play(Indicate(u, color=YES), run_time=.4)
            vo.wait_until("b")
            self.play(Create(a), FadeIn(al), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()
