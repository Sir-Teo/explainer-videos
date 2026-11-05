from __future__ import annotations

import numpy as np

from videos.philosophy.philosophy2.common import *  # noqa: F403
from explainer.philosophy.reasoner import prop

MT = "((p -> q) & ~q) -> ~p"


def mini_table(bits, sym: str, size=0.36, highlight=False) -> VGroup:
    """A connective's truth table as four little cells (rows TT, TF, FT, FF) under its symbol."""
    cells = VGroup()
    for i, b in enumerate(bits):
        sq = Square(size, stroke_width=1, stroke_color=GREY_D, fill_color=OK if b else BAD, fill_opacity=0.75)
        sq.move_to([0, -i * size, 0])
        cells.add(sq)
    s = MathTex(sym, font_size=30, color=P.CONCL if highlight else WHITE).next_to(cells, UP, buff=0.12)
    g = VGroup(s, cells)
    g.cells, g.sym = cells, s
    return g


class Syntax(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Formulas, trees and truth functions", r"What is a formula, and what can a "
                            r"connective do?", lit=(1879, 1921), part=PART)
        with self.voiceover("Chapter two. Formulas, trees and truth functions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.grammar()
        self.trees()
        self.sixteen()
        self.conditional()

    def grammar(self):
        rules = VGroup(
            label(r"1.\ \ every atom $p, q, r, \dots$ is a formula", font_size=28),
            label(r"2.\ \ if $A$ and $B$ are formulas, so are", font_size=28),
            MathTex(r"\lnot A \quad (A \land B) \quad (A \lor B) \quad (A \to B) \quad (A \leftrightarrow B)",
                    font_size=34, color=CONN),
            label(r"3.\ \ nothing else is a formula", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        rules[2].shift(RIGHT * 0.5)
        box = SurroundingRectangle(rules, buff=0.3, color=CONN, corner_radius=0.12, stroke_width=1.8)
        G = VGroup(box, rules).to_corner(UL, buff=0.45)
        steps = ["p", "q", "p -> q", "~q", "(p -> q) & ~q", "~p", MT]
        built = VGroup(*[fmath(s, font_size=36) for s in steps]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        built.next_to(G, DOWN, buff=0.45).align_to(G, LEFT).shift(RIGHT * 0.4)
        for i in (0, 1):
            built[i].set_color(ATOM)
        built[-1].set_color(GOAL)
        built.arrange_in_grid(rows=4, cols=2, buff=(0.8, 0.2), cell_alignment=LEFT, flow_order="dr")
        built.next_to(G, DOWN, buff=0.4).align_to(G, LEFT)
        atomw = label(r"$p$: `it is raining' \quad $q$: `the streets are wet'", font_size=24, color=ATOM)
        atomw.next_to(G, RIGHT, buff=0.5).align_to(G, UP)
        with self.voiceover(
            "A formula is built by rules, the way a grammar builds sentences. <bookmark mark='a'/>Start with atoms: p, "
            "q, r, each standing for a whole sentence, like 'it is raining'. <bookmark mark='b'/>If A and B are "
            "formulas, then so are not A; A and B; A or B; if A then B; and A if and only if B, each in brackets. "
            "<bookmark mark='c'/>Nothing else is a formula."
        ) as vo:
            self.play(Create(box))
            vo.wait_until("a")
            self.play(FadeIn(rules[0]), FadeIn(atomw))
            vo.wait_until("b")
            self.play(FadeIn(rules[1]), Write(rules[2]))
            vo.wait_until("c")
            self.play(FadeIn(rules[3]))
        with self.voiceover(
            "Here is one formula, built in seven steps: the shape of modus tollens. <bookmark mark='a'/>Two atoms; "
            "if p then q; not q; their conjunction; not p; and the whole conditional. <bookmark mark='b'/>This is "
            "an inductive definition, and every proof about formulas in this part follows its shape: show something "
            "holds for the atoms, then show each rule preserves it. Then it holds for every formula there is."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in built], lag_ratio=0.35), run_time=3.5)
            vo.wait_until("b")
            self.play(Indicate(built[-1], color=GOAL))
        self.clear_scene()

    def trees(self):
        tr = FormulaTree(MT, width=6.6, level_height=1.1, center=[-2.6, 0.2, 0])
        f = fmath(MT, font_size=40, color=GOAL).to_edge(UP, buff=0.4)
        v = {"p": True, "q": False}
        tags = tr.value_tags(v)
        order = tr.order_bottom_up()
        val = label(r"$p = \mathrm{T},\ q = \mathrm{F}$", font_size=30, color=ATOM).next_to(f, DOWN, buff=0.3)
        # ambiguity: p & q | r without brackets
        w = {"p": False, "q": True, "r": True}
        t1 = FormulaTree("(p & q) | r", width=2.6, level_height=0.95, center=[3.2, 1.0, 0], font_size=28)
        t2 = FormulaTree("p & (q | r)", width=2.6, level_height=0.95, center=[3.2, -1.9, 0], font_size=28)
        for t in (t1, t2):
            t.scale(0.85)
        v1 = prop.evaluate(prop.parse("(p & q) | r"), w)
        v2 = prop.evaluate(prop.parse("p & (q | r)"), w)
        assert v1 != v2
        amb = MathTex(r"p \land q \lor r\ ?", font_size=36).move_to([3.2, 2.9, 0])
        r1 = VGroup(tv(v1, 30)).next_to(t1, RIGHT, buff=0.3)
        r2 = VGroup(tv(v2, 30)).next_to(t2, RIGHT, buff=0.3)
        wv = label(r"$p=\mathrm{F},\ q=\mathrm{T},\ r=\mathrm{T}$", font_size=22, color=ATOM).next_to(amb, DOWN,
                                                                                                buff=0.15)
        with self.voiceover(
            "Every formula has exactly one parse tree. <bookmark mark='a'/>Atoms sit at the leaves; each connective "
            "sits above what it connects; the main connective, here the last 'if then', is the root. "
            "<bookmark mark='b'/>The tree says how to compute truth: from the leaves up. Give the atoms values, p "
            "true and q false. <bookmark mark='c'/>Each connective reads its children and writes its own value. If p "
            "then q is false; not q is true; the conjunction false; not p false; and the whole conditional, true."
        ) as vo:
            self.play(Write(f))
            vo.wait_until("a")
            self.play(Create(tr.edges), LaggedStart(*[FadeIn(n, scale=0.8) for n in tr.node], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(val))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(tags[i], scale=1.4) for i in order], lag_ratio=0.35), run_time=4.0)
        with self.voiceover(
            "Brackets are what make the tree unique. <bookmark mark='a'/>Without them, 'p and q or r' could be "
            "built two ways, <bookmark mark='b'/>and the two trees can disagree: with p false and q and r true, one "
            "is true and the other false. A logic for settling arguments cannot leave it to the reader to guess. "
            "Frege, in 1879, was the first to insist on this precision for all of reasoning."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(amb), FadeIn(wv))
            self.play(FadeIn(t1), FadeIn(t2))
            vo.wait_until("b")
            self.play(FadeIn(r1, scale=1.4), FadeIn(r2, scale=1.4))
        self.clear_scene()

    def sixteen(self):
        d = load("connectives")
        tabs = VGroup()
        named = {"∧": r"\land", "∨": r"\lor", "→": r"\to", "↔": r"\leftrightarrow", "⊕": r"\oplus",
                 "↑": r"\uparrow", "↓": r"\downarrow", "⊤": r"\top", "⊥": r"\bot", "¬p": r"\lnot p", "¬q": r"\lnot q",
                 "p": "p", "q": "q", "↚": r"\not\leftarrow", "↛": r"\not\to", "←": r"\leftarrow"}
        for fn in d["functions"]:
            tabs.add(mini_table(fn["bits"], named[fn["sym"]], highlight=fn["sym"] in ("∧", "∨", "→", "↔")))
        tabs.arrange_in_grid(rows=2, cols=8, buff=(0.55, 0.6)).move_to([0.6, -0.4, 0])
        rowlab = VGroup(*[MathTex(s, font_size=24, color=GREY_B) for s in
                          (r"\mathrm{TT}", r"\mathrm{TF}", r"\mathrm{FT}", r"\mathrm{FF}")])
        for k, m in enumerate(rowlab):
            m.next_to(tabs[0].cells[k], LEFT, buff=0.25)
        top = MathTex(r"(p, q)", font_size=26, color=ATOM).next_to(rowlab, UP, buff=0.25)
        count = MathTex(r"2^{4} = 16", font_size=44, color=GOAL).to_edge(UP, buff=0.5)
        cn = d["count_n"]
        more = MathTex(rf"n \text{{ inputs: }}\ 2^{{2^n}} \qquad n=3:\ {cn['3']} \qquad n=5:\ {cn['5']:,}".replace(
            ",", "{,}"), font_size=34).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "What a connective does is captured by its truth table: a function from the truth values of its inputs "
            "to a truth value. With two inputs, there are four rows: both true, true then false, false then true, "
            "both false. <bookmark mark='a'/>Each row's output can be true or false, so there are two to the four, "
            "sixteen, possible connectives of two sentences. <bookmark mark='b'/>Here are all sixteen, green for true "
            "and red for false."
        ) as vo:
            self.play(FadeIn(rowlab), FadeIn(top), FadeIn(tabs[0]))
            vo.wait_until("a")
            self.play(Write(count))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tabs[1:]], lag_ratio=0.1), run_time=3)
        with self.voiceover(
            "Some have names everyone knows: and, or, if then, if and only if. <bookmark mark='a'/>Some have names "
            "only logicians use: exclusive or, nand, nor. <bookmark mark='b'/>Some are barely connectives at all: "
            "always true, always false, or a copy of p. <bookmark mark='c'/>With n inputs there are two to the two "
            f"to the n truth functions: {cn['3']} for three inputs, and for five, over four billion. The question for "
            "the next chapter is how many of them we need."
        ) as vo:
            idx = {fn["sym"]: i for i, fn in enumerate(d["functions"])}
            self.play(*[Indicate(tabs[idx[s]], color=GOAL) for s in ("∧", "∨", "→", "↔")])
            vo.wait_until("a")
            self.play(*[Indicate(tabs[idx[s]], color=CONN) for s in ("⊕", "↑", "↓")])
            vo.wait_until("b")
            self.play(*[Indicate(tabs[idx[s]], color=GREY_A) for s in ("⊤", "⊥", "p")])
            vo.wait_until("c")
            self.play(Write(more))
        self.clear_scene()

    def conditional(self):
        d = load("connectives")
        named = {"∧": r"\land", "∨": r"\lor", "→": r"\to", "↔": r"\leftrightarrow", "q": "q"}
        idx = {fn["sym"]: fn for fn in d["functions"]}
        cheese = label(r"`If the moon is made of cheese, then $2 + 2 = 4$': \ \ true?", font_size=30).to_edge(
            UP, buff=0.45)
        tt = TruthTable(["p -> q"], font_size=36).scale(1.25).move_to([-4.3, -0.5, 0])
        demands = d["conditional"]
        cols = VGroup()
        alive = [fn["sym"] for fn in d["functions"]]
        stages = [alive] + [dm["survivors"] for dm in demands]
        heads = [r"all 16"] + [dm["demand"] for dm in demands]
        hw = {"modus ponens": r"modus ponens is valid", "if p then p": r"`if $p$ then $p$' is always true",
              "not symmetric": r"`if $p$ then $q$' $\neq$ `if $q$ then $p$'"}
        for k, (h, st) in enumerate(zip(heads, stages)):
            if k == 0:
                continue
            row = VGroup(label(hw[h], font_size=29, color=CONN),
                         MathTex(r"\Rightarrow\ " + r",\ ".join(named.get(x, x) for x in st), font_size=38))
            row.arrange(RIGHT, buff=0.3)
            cols.add(row)
        cols.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([2.2, -0.5, 0])
        cols[-1][1].set_color(GOAL)
        with self.voiceover(
            "One of the sixteen deserves a closer look: the Stoic Philo's conditional, false only when the 'if' part "
            "is true and the 'then' part false. <bookmark mark='a'/>It makes 'if the moon is made of cheese, then two "
            "plus two is four' true, and many people feel that is wrong: there is no connection between the parts. "
            "<bookmark mark='b'/>But suppose 'if' is to be a truth function at all. Then three modest demands pick it "
            "out."
        ) as vo:
            self.play(FadeIn(tt))
            vo.wait_until("a")
            self.play(FadeIn(cheese), Indicate(tt.row(2), color=GOAL), Indicate(tt.row(3), color=GOAL))
            vo.wait_until("b")
        with self.voiceover(
            "First, modus ponens must be valid: if p and 'if p then q' are true, q is true. "
            f"{len(demands[0]['survivors'])} of the sixteen pass. <bookmark mark='a'/>Second, 'if p then p' must always "
            f"be true: {len(demands[1]['survivors'])} remain, if-then and if-and-only-if. <bookmark mark='b'/>Third, "
            "'if p then q' must not say the same as 'if q then p'. One remains: Philo's. So the oddity of the cheese "
            "conditional is the price of making 'if' a truth function. Part 14 asks whether 'if' should be one."
        ) as vo:
            self.play(FadeIn(cols[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cols[1], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cols[2], shift=RIGHT * 0.2))
            self.play(Indicate(cols[2][1], color=GOAL))
        self.clear_scene()
