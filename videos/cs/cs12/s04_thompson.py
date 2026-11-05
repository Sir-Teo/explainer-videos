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
        nd = label(r"$\varepsilon$-edges are free moves: \ the machine may be in many states at once \ "
                   r"--- \ it is \textit{nondeterministic}", font_size=21, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1968 Ken Thompson, who would go on to write Unix, published a way to run regular expressions. "
            "<bookmark mark='a'/> Build a small machine for each piece of the expression, each with one way in and "
            "one way out. A single symbol is one arrow. <bookmark mark='b'/> To concatenate, join the first "
            "machine's exit to the second's entrance, with an arrow labelled epsilon, which can be taken without "
            "reading anything. <bookmark mark='c'/> For a union, split into both machines with epsilon arrows, and "
            "merge their exits. <bookmark mark='d'/> For a star, add an arrow back to the start, and one that skips "
            "the machine altogether. <bookmark mark='e'/> Because epsilon arrows are free, the machine can be in "
            "several states at once. That makes it nondeterministic, an NFA."
        ) as vo:
            self.play(FadeIn(head))
            for mk, x in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(x))
            vo.wait_until("e")
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
        with self.voiceover(
            "Here is the machine Thompson's construction builds for a b star a b b: any a's and b's, ending in a b "
            "b. <bookmark mark='a'/> Fourteen states: the star's loop on the left, then the three symbols in a row. "
            "<bookmark mark='b'/> To run it, keep the set of every state the machine could be in. At the start, "
            "that is state zero and everything reachable from it by free moves. <bookmark mark='c'/> Then for each "
            "character, move every state in the set across an arrow with that character, and add the free moves "
            "again. The set grows and shrinks, but it can never hold more than fourteen states. <bookmark "
            "mark='d'/> When the input ends, accept if the accepting state is in the set."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sd), FadeIn(braces))
            vo.wait_until("b")
            setl = mk(0)
            self.play(FadeIn(cells), *light(0), FadeIn(setl))
            vo.wait_until("c")
            for k in range(len(text)):
                ptr.next_to(cells[k], UP, buff=0.06)
                new = mk(k + 1)
                self.play(FadeIn(ptr) if k == 0 else ptr.animate.next_to(cells[k], UP, buff=0.06), run_time=0.25)
                self.play(*light(k + 1), Transform(setl, new), cells[k].animate.set_color(GREY_C), run_time=0.6)
            vo.wait_until("d")
            self.play(FadeIn(res), Indicate(sd.node["13"], color=YES))
        self.wait(0.3)
        self.clear_scene()

    def linear(self):
        b = load("blowup")
        head = label(r"Linear time, \ whatever the pattern", font_size=36).to_edge(UP, buff=0.35)
        pts = VGroup(
            label(r"$m$ states, \ $n$ characters: \ at most $m$ states touched per character \ $\Rightarrow$ \ "
                  r"$O(mn)$ time, \ no backing up", font_size=22, color=GREY_A),
            label(r"Thompson compiled the sets into IBM 7094 machine code, \ for the QED editor; \ \texttt{grep} "
                  r"(1973) grew out of the same editors", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(head, DOWN, buff=0.45)
        rows = [[f"{r['n']:,}", f"{1000 * r['s']:.1f} ms"] for r in b["thompson_time"]]
        t = grid_table([r"\texttt{a}'s", r"our NFA simulation \ (Python)"], rows, [2.6, 4.6], row_h=0.5,
                       font_size=21, colors=[[GREY_A, YES]] * len(rows), mono_cols=()).next_to(pts, DOWN, buff=0.5)
        cap = label(rf"\texttt{{(a+)+b}} as a {b['nfa_states']}-state NFA: \ ten times the input, \ about ten times "
                    r"the time", font_size=21, color=YES).next_to(t, DOWN, buff=0.35)
        with self.voiceover(
            "The cost of this method is easy to bound. <bookmark mark='a'/> With m states and n characters of "
            "input, each character touches at most m states, so the time is proportional to m times n, and the "
            "machine never has to go back and try again. <bookmark mark='b'/> Thompson's own version compiled the "
            "state sets into IBM 7094 machine code inside the QED text editor, and grep, in 1973, grew out of the "
            "same line of editors. "
            "<bookmark mark='c'/> Here is our simulation, in plain Python, on the pattern from the start of the "
            "part. Ten times as many a's take about ten times as long. A hundred thousand a's take a fifth of a "
            "second, where Python's own engine needs eight seconds for twenty-eight."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*t.cells[r])) for r in range(1, len(t.cells))], lag_ratio=0.3))
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()
