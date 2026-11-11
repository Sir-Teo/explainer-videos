from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs12.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, grid_table, load, region)

POS = {0: (-6.3, 0), 2: (-5.0, 0), 4: (-3.7, 0.95), 6: (-3.7, -0.95), 5: (-2.4, 0.95), 7: (-2.4, -0.95),
       3: (-1.1, 0), 1: (0.2, 0), 8: (1.3, 0), 9: (2.4, 0), 10: (3.3, 0), 11: (4.4, 0), 12: (5.3, 0), 13: (6.35, 0)}
BENDS = {(0, 1): -1.0, (3, 2): 1.2, (3, 1): 0}


def thompson_diagram(t):
    nodes = {str(k): v for k, v in POS.items()}
    edges = []
    for s, d, lab in t["edges"]:
        edges.append((str(s), str(d), lab, BENDS.get((s, d), 0)))
    return StateDiagram(nodes, edges, radius=0.27, font_size=16, edge_font=15, accept=(str(t["accept"]),))


def fragment(kind):
    """Schematic Thompson fragments: entry on the left, exit on the right."""
    c = lambda: Circle(radius=0.16, stroke_color=DATA, stroke_width=2)
    g = VGroup()
    if kind == "sym":
        a, b = c().move_to(LEFT * 0.8), c().move_to(RIGHT * 0.8)
        g.add(a, b, Arrow(a.get_right(), b.get_left(), buff=0.03, color=GREY_B, stroke_width=2),
              Text("a", font="DejaVu Sans Mono", font_size=18, color=CODE).move_to(UP * 0.22))
    elif kind == "cat":
        r = region(0.9, 0.55, r"$r$", HEAD, font_size=20).move_to(LEFT * 0.6)
        s = region(0.9, 0.55, r"$s$", HEAD, font_size=20).move_to(RIGHT * 0.6)
        g.add(r, s, Arrow(r.get_right(), s.get_left(), buff=0.02, color=GREY_B, stroke_width=2),
              Text("ε", font_size=16, color=GREY_B).move_to(UP * 0.38))
    elif kind == "alt":
        a, b = c().move_to(LEFT * 1.3), c().move_to(RIGHT * 1.3)
        r = region(0.9, 0.5, r"$r$", HEAD, font_size=20).move_to(UP * 0.45)
        s = region(0.9, 0.5, r"$s$", HEAD, font_size=20).move_to(DOWN * 0.45)
        g.add(a, b, r, s)
        for x in (r, s):
            g.add(Arrow(a.get_right(), x.get_left(), buff=0.03, color=GREY_B, stroke_width=2),
                  Arrow(x.get_right(), b.get_left(), buff=0.03, color=GREY_B, stroke_width=2))
    else:
        a, b = c().move_to(LEFT * 1.3), c().move_to(RIGHT * 1.3)
        r = region(0.9, 0.5, r"$r$", HEAD, font_size=20)
        g.add(a, b, r, Arrow(a.get_right(), r.get_left(), buff=0.03, color=GREY_B, stroke_width=2),
              Arrow(r.get_right(), b.get_left(), buff=0.03, color=GREY_B, stroke_width=2),
              CurvedArrow(r.get_right() + UP * 0.25, r.get_left() + UP * 0.25, angle=1.6, color=GREY_B,
                          stroke_width=2, tip_length=0.12),
              CurvedArrow(a.get_bottom(), b.get_bottom(), angle=1.0, color=GREY_B, stroke_width=2, tip_length=0.12))
    return g


class Thompson(VoiceoverScene):
    def construct(self):
        self.card()
        self.pieces()
        self.build()
        self.linear()

    def card(self):
        card = chapter_card(3, r"Thompson's construction", r"How do you run a regular expression?", lit=(1968,),
                            extra=((1968, r"Thompson: \ regular expression search"),), part=PART)
        with self.voiceover("Chapter three. Thompson's construction."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def pieces(self):
        head = label(r"One small machine per operation", font_size=36).to_edge(UP, buff=0.35)
        names = [(r"a symbol", "sym"), (r"$rs$: \ join with an $\varepsilon$", "cat"),
                 (r"$r|s$: \ split, \ then merge", "alt"), (r"$r^*$: \ loop back, \ or skip", "star")]
        g = VGroup()
        for name, k in names:
            f = fragment(k)
            g.add(VGroup(f, label(name, font_size=20, color=GREY_A).next_to(f, DOWN, buff=0.3)))
        g.arrange_in_grid(2, 2, buff=(1.6, 0.9)).next_to(head, DOWN, buff=0.6)
        nd = label("$\\varepsilon$ consumes no input symbol; computing epsilon closure still costs work", font_size=21, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover("Thompson's 1968 construction builds an automaton from fragments. <bookmark mark='a'/> A fragment has one entrance and one exit; a symbol supplies a labeled transition. <bookmark mark='b'/> Concatenation connects an exit to the next entrance with epsilon: a transition consuming no input symbol. <bookmark mark='c'/> Union uses epsilon transitions to choose either fragment and then merge. <bookmark mark='d'/> Star allows both another repetition and an exit without a repetition. <bookmark mark='e'/> Nondeterminism means several paths may be possible for the same input. A simulator tracks all reachable states, including epsilon closure. Those transitions consume no input, but computing that closure still costs work.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            for mk, x in zip('abcd', g):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(x))
                if mk == 'a':
                    vo.wait_until(mk)
            vo.wait_until('e')
            self.play(FadeIn(nd))
        self.wait(0.3)
        self.clear_scene()

    def build(self):
        t = load("thompson")
        head = label(r"\texttt{(a|b)*abb}: \ 14 states, \ and a run on \texttt{babbabb}", font_size=32).to_edge(
            UP, buff=0.35)
        sd = thompson_diagram(t).shift(UP * 0.9)
        braces = VGroup(
            label(r"\texttt{(a|b)*}", font_size=18, color=HEAD).next_to(VGroup(sd.node["0"], sd.node["1"]), UP,
                                                                       buff=1.25),
            label(r"\texttt{a} \ \texttt{b} \ \texttt{b}", font_size=18, color=HEAD).next_to(
                VGroup(sd.node["8"], sd.node["13"]), UP, buff=0.55))
        text = t["text"]
        cells = VGroup(*[Text(c, font="DejaVu Sans Mono", font_size=30, color=CODE) for c in text]).arrange(
            RIGHT, buff=0.3).shift(DOWN * 1.5)
        ptr = Triangle(color=HEAD, fill_opacity=1).scale(0.1).rotate(PI)
        sets = t["sets"]
        setl = Text("", font="DejaVu Sans Mono", font_size=20)

        def mk(k):
            return Text("{" + ", ".join(map(str, sets[k])) + "}", font="DejaVu Sans Mono", font_size=20,
                        color=DATA).next_to(cells, DOWN, buff=0.45)

        def light(k):
            anims = []
            for name, n in sd.node.items():
                on = int(name) in sets[k]
                anims.append(n.circle.animate.set_fill(YES if on else CTRL, opacity=0.55 if on else 0.12))
            return anims
        res = label(r"after the last \texttt{b}, \ the set contains state 13, \ the accepting state: \ a match",
                    font_size=21, color=YES).to_edge(DOWN, buff=0.35)
        with self.voiceover("Here is the construction for parenthesized a-or-b, starred, followed by a b b: any binary-alphabet prefix, then the suffix a b b. <bookmark mark='a'/> This implementation produces fourteen states, including the repetition and the three final symbol fragments. <bookmark mark='b'/> Its starting set contains the start state and every state reachable using only epsilon transitions. <bookmark mark='c'/> For each input character, follow matching transitions from the active set, then compute epsilon closure again. Duplicate paths reaching the same state are merged; the active set has at most fourteen states. <bookmark mark='d'/> After the entire input is consumed, accept exactly when the accepting state is active. This is whole-string membership, distinct from searching for a matching substring.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(sd), FadeIn(braces), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            setl = mk(0)
            self.play(FadeIn(cells), *light(0), FadeIn(setl))
            vo.wait_until('c')
            for k in range(len(text)):
                ptr.next_to(cells[k], UP, buff=0.06)
                new = mk(k + 1)
                self.play(FadeIn(ptr) if k == 0 else ptr.animate.next_to(cells[k], UP, buff=0.06), run_time=0.25)
                self.play(*light(k + 1), Transform(setl, new), cells[k].animate.set_color(GREY_C), run_time=0.6)
            vo.wait_until('d')
            self.play(FadeIn(res), Indicate(sd.node['13'], color=YES))
        self.wait(0.3)
        self.clear_scene()

    def linear(self):
        b = load("blowup")
        head = label("Fixed pattern: linear input-time upper bound", font_size=36).to_edge(UP, buff=0.35)
        pts = VGroup(
            label("bounded-degree Thompson NFA: $O(mn)$ time, $O(m)$ active storage", font_size=22, color=GREY_A),
            label(r"Thompson compiled the sets into IBM 7094 machine code, \ for the QED editor; \ \texttt{grep} "
                  r"(1973) grew out of the same editors", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(head, DOWN, buff=0.45)
        rows = [[f"{r['n']:,}", f"{1000 * r['s']:.1f} ms"] for r in b["thompson_time"]]
        t = grid_table([r"\texttt{a}'s", r"our NFA simulation \ (Python)"], rows, [2.6, 4.6], row_h=0.5,
                       font_size=21, colors=[[GREY_A, YES]] * len(rows), mono_cols=()).next_to(pts, DOWN, buff=0.5)
        cap = label(rf"\texttt{{(a+)+b}} as a {b['nfa_states']}-state NFA: \ ten times the input, \ about ten times "
                    r"the time", font_size=21, color=YES).next_to(t, DOWN, buff=0.35)
        with self.voiceover("The construction gives a useful cost bound. <bookmark mark='a'/> For a Thompson NFA with m states and bounded outgoing degree, visit each active state and each state reached in epsilon closure only a bounded number of times per input character. With n characters, O m n time and O m active storage suffice. This is an upper bound; a particular input may visit fewer states. <bookmark mark='b'/> Thompson used generated IBM 7094 code in the QED editor. Later Unix text tools developed from this line of work; modern engines add their own optimizations and feature choices. <bookmark mark='c'/> The displayed host timings compare our Python simulator with the host backtracking engine on this failing pattern. Inspect their trend and units rather than treating a measured duration as a portable constant. State-work counts and elapsed time answer different questions.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(pts[0]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(pts[1]))
            vo.wait_until('c')
            self.play(FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*t.cells[r])) for r in range(1, len(t.cells))], lag_ratio=0.3))
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()
