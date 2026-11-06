from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs26.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load, mono,
                                   words)


def lit_tex(l):
    return rf"x_{l}" if l > 0 else rf"\bar x_{-l}"


def clause_tex(c):
    return r"(" + r" \vee ".join(lit_tex(l) for l in c) + r")"


KARP = [
    (0, "SAT"), (1, "0--1 integer programming"), (1, "clique"), (2, "set packing"), (2, "vertex cover"),
    (3, "set covering"), (3, "feedback node set"), (3, "feedback arc set"), (3, "directed Hamiltonian cycle"),
    (4, "undirected Hamiltonian cycle"), (1, "3-SAT"), (2, "chromatic number"), (3, "clique cover"),
    (3, "exact cover"), (4, "hitting set"), (4, "Steiner tree"), (4, "3-dimensional matching"), (4, "knapsack"),
    (5, "job sequencing"), (5, "partition"), (6, "max cut"),
]


class Web(VoiceoverScene):
    def construct(self):
        self.card()
        self.formula()
        self.independent()
        self.colouring()
        self.subset()
        self.karp()

    def card(self):
        card = chapter_card(6, r"The web of reductions", r"How do you prove the next problem NP-complete?",
                            lit=(1972,), extra=((1972, r"Karp's 21 problems"),), part=PART)
        with self.voiceover("Chapter six. The web of reductions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def formula(self):
        w = load("web")
        head = label(r"One formula, \ four disguises", font_size=34).to_edge(UP, buff=0.35)
        f = MathTex(r" \wedge ".join(clause_tex(c) for c in w["clauses"]), font_size=34, color=HEAD)
        f.next_to(head, DOWN, buff=0.5)
        if f.width > 13:
            f.width = 13
        lines = VGroup(
            label(r"once SAT is NP-complete, \ a new problem $B$ needs only \textbf{one} reduction: \ SAT $\le_p B$",
                  font_size=22, color=WHITE),
            label(r"first, \ SAT $\le_p$ 3-SAT: \ split long clauses with fresh variables: \ $(a \vee b \vee c \vee d)"
                  r"\ \to\ (a \vee b \vee y)(\bar y \vee c \vee d)$", font_size=22, color=DATA),
            label(rf"our formula: \ {len(w['clauses'])} clauses, \ {w['n']} variables, \ {w['solutions']} of the 16 "
                  r"assignments satisfy it", font_size=22, color=GREY_A),
            label(r"we push it through three reductions, \ solve each disguise, \ and map the answer back",
                  font_size=22, color=YES),
        ).arrange(DOWN, buff=0.3).next_to(f, DOWN, buff=0.5)
        with self.voiceover(
            "Once one problem is NP-complete, the rest get easier. <bookmark mark='a'/> To show that a new problem B "
            "is NP-complete, it is enough to put it in NP and reduce SAT, or any known NP-complete problem, to it. "
            "<bookmark mark='b'/> The first step is three-SAT, where every clause has at most three literals: split "
            "a long clause into a chain of short ones linked by new variables. <bookmark mark='c'/> Here is a small "
            "formula: five clauses over four variables, satisfied by seven of the sixteen assignments. <bookmark "
            "mark='d'/> We will push it through three reductions, solve each disguised problem, and translate the "
            "answer back."
        ) as vo:
            self.play(FadeIn(head), FadeIn(f))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def independent(self):
        w = load("web")["is"]
        head = label(r"3-SAT $\le_p$ independent set", font_size=32).to_edge(UP, buff=0.3)
        verts = [tuple(v) for v in w["verts"]]
        pos = {}
        for (j, i) in verts:
            cx = -5.0 + j * 2.5
            ang = PI / 2 + i * 2 * PI / 3
            pos[(j, i)] = np.array([cx + 0.75 * np.cos(ang), 0.9 + 0.75 * np.sin(ang), 0])
        lit = dict(zip(verts, w["lits"]))
        chosen = {tuple(v) for v in w["chosen"]}
        tri, cross = VGroup(), VGroup()
        for a, b in w["edges"]:
            a, b = tuple(a), tuple(b)
            ln = Line(pos[a], pos[b], stroke_width=2 if a[0] == b[0] else 1.2,
                      color=GREY_B if a[0] == b[0] else NO, stroke_opacity=1 if a[0] == b[0] else 0.55)
            (tri if a[0] == b[0] else cross).add(ln)
        nodes = VGroup()
        for v in verts:
            c = Circle(radius=0.3, stroke_color=DATA, stroke_width=2, fill_color=BG, fill_opacity=1).move_to(pos[v])
            t = MathTex(lit_tex(lit[v]), font_size=24, color=WHITE).move_to(pos[v])
            nodes.add(VGroup(c, t))
        hl = VGroup(*[Circle(radius=0.38, color=YES, stroke_width=4).move_to(pos[v]) for v in chosen])
        lines = VGroup(
            label(r"a triangle per clause: \ pick at most one literal from each", font_size=21, color=WHITE),
            label(r"an edge between $x_i$ and $\bar x_i$: \ never pick both", font_size=21, color=NO),
            label(rf"independent set of size $k$ = {w['k']} \ $\iff$ \ one true literal in every clause", font_size=21,
                  color=YES),
            label(rf"complement: \ the same {w['k']} vertices form a \textbf{{clique}} in the complement graph \ "
                  rf"({w['clique_edges']} edges); \ the other {w['cover']} are a \textbf{{vertex cover}}",
                  font_size=20, color=DATA),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "First disguise: independent set. Choose k vertices of a graph, no two joined by an edge. <bookmark "
            "mark='a'/> Make a triangle for each clause, one vertex per literal. Since the vertices of a triangle "
            "are all joined, you can pick at most one from each clause. <bookmark mark='b'/> Then join every literal "
            "to every copy of its negation, so you can never pick both x and not x. <bookmark mark='c'/> An "
            "independent set of five vertices picks one literal from every clause, consistently: a satisfying "
            "assignment. Our solver found one, and the five green vertices are it. <bookmark mark='d'/> The same "
            "five vertices are a clique in the complement graph, and the other ten are a vertex cover. So clique and "
            "vertex cover are NP-complete too, almost for free."
        ) as vo:
            self.play(FadeIn(head), Create(tri), FadeIn(nodes))
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(Create(cross), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(Create(hl), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def colouring(self):
        w = load("web")["col"]
        head = label(r"3-SAT $\le_p$ 3-colouring", font_size=32).to_edge(UP, buff=0.3)
        P = {"T": [-5.2, 1.6], "F": [-3.8, 1.6], "B": [-4.5, 0.5]}
        cols = {"T": YES, "F": NO, "B": DATA}
        pal = VGroup()
        for k_, (x, y) in P.items():
            pal.add(VGroup(Circle(radius=0.28, color=cols[k_], stroke_width=3).set_fill(cols[k_], 0.35).move_to(
                [x, y, 0]), label(k_, font_size=20, color=WHITE).move_to([x, y, 0])))
        pal_e = VGroup(*[Line([*P[a], 0], [*P[b], 0], buff=0.28, color=GREY_B) for a, b in (("T", "F"), ("F", "B"),
                                                                                         ("B", "T"))])
        pl = label(r"the palette: \ True, \ False, \ Base", font_size=19, color=GREY_A).next_to(pal, DOWN, buff=0.2)
        # an OR gadget, drawn
        g = {"a": [-1.2, 1.4], "b": [-1.2, -0.6], "u": [0.2, 1.0], "w": [0.2, -0.2], "o": [1.4, 0.4]}
        gad = VGroup()
        for a_, b_ in (("a", "u"), ("b", "w"), ("u", "w"), ("u", "o"), ("w", "o")):
            gad.add(Line([*g[a_], 0], [*g[b_], 0], buff=0.25, color=GREY_B))
        for k_, (x, y) in g.items():
            col = HEAD if k_ in "ab" else (YES if k_ == "o" else LAM)
            gad.add(VGroup(Circle(radius=0.25, color=col, stroke_width=2.5).set_fill(BG, 1).move_to([x, y, 0]),
                           label(k_, font_size=18, color=WHITE).move_to([x, y, 0])))
        gl = label(r"OR gadget: \ $o$ can be True \\ only if $a$ or $b$ is", font_size=19, color=GREY_A).next_to(
            gad, DOWN, buff=0.2)
        notes = VGroup(
            label(r"each variable: \ $x_i$ and $\bar x_i$ joined to each other and to B: \\ one is True, \ one False",
                  font_size=20, color=WHITE),
            label(r"each clause: \ two OR gadgets in a row; \ the output is joined to F and B, \\ so it must be "
                  r"True: \ some literal is True", font_size=20, color=LAM),
            label(rf"our formula: \ {w['vertices']} vertices, \ {w['edges']} edges; \ as SAT for our solver: \ "
                  rf"{w['cnf_vars']} variables, \ {w['cnf_clauses']} clauses", font_size=20, color=DATA),
            label(r"the colouring it found, \ read back: \ $x_i$ = colour of $x_i$ is T: \ "
                  + ", ".join("T" if b else "F" for b in w["mapped"]) + r" \ (satisfies the formula)",
                  font_size=20, color=YES),
            label(r"an unsatisfiable formula gives a graph with \textbf{no} 3-colouring \ (checked)", font_size=20,
                  color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(gad, RIGHT, buff=0.6).align_to(pal, UP)
        fit_right(notes)
        with self.voiceover(
            "Second disguise: colouring a graph with three colours. <bookmark mark='a'/> Start with a triangle whose "
            "colours we name True, False and Base. <bookmark mark='b'/> For each variable, two vertices, x and not "
            "x, joined to each other and to Base: one must be coloured True and the other False. <bookmark "
            "mark='c'/> For each clause, a small gadget whose output vertex can be True only if one of its inputs is; "
            "chain two for three literals, and join the output to False and Base, forcing it to be True. <bookmark "
            "mark='d'/> Our formula becomes a graph of forty-one vertices. Written as a SAT problem for our solver, "
            "a hundred and twenty-three variables. <bookmark mark='e'/> The colouring it found, read back as truth "
            "values, satisfies the original formula. <bookmark mark='f'/> And an unsatisfiable formula, put through "
            "the same construction, gives a graph that cannot be three-coloured. We checked that too."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pal), Create(pal_e), FadeIn(pl))
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(gad), FadeIn(gl), FadeIn(notes[1]))
            for mk, n_ in zip("def", notes[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def subset(self):
        w = load("web")
        ss = w["ss"]
        n, m = w["n"], len(w["clauses"])
        head = label(r"3-SAT $\le_p$ subset sum: \ the answer is in the digits", font_size=30).to_edge(UP, buff=0.3)
        names = list(ss["nums"])
        chosen = set(ss["chosen"])
        hdr = [r""] + [rf"$x_{i + 1}$" for i in range(n)] + [rf"$C_{j + 1}$" for j in range(m)]
        rows = []
        cols_ = []
        for nm in names:
            digits = list(ss["nums"][nm])
            rows.append([rf"${nm[0]}_{{{nm[1:]}}}$"] + digits)
            c = YES if nm in chosen else GREY_B
            cols_.append([c] * (1 + n + m))
        rows.append([r"target"] + list(ss["target"]))
        cols_.append([HEAD] * (1 + n + m))
        tab = grid_table(hdr, rows, widths=[1.0] + [0.55] * (n + m), row_h=0.26, font_size=16, mono_cols=(),
                         colors=cols_)
        tab.next_to(head, DOWN, buff=0.25).to_edge(LEFT, buff=0.8)
        notes = VGroup(
            label(r"$y_i$: \ 1 in column $x_i$, \ and in each clause containing $x_i$; \\ $z_i$ the same for "
                  r"$\bar x_i$", font_size=20, color=WHITE),
            label(r"target: \ 1 in each variable column: \\ choose exactly one of $y_i$, $z_i$ \ (a truth value)",
                  font_size=20, color=DATA),
            label(r"3 in each clause column: \ the chosen literals give 1 to 3; \\ the slack numbers $g_j, h_j$ add "
                  r"the rest \\ only if at least one literal is true", font_size=20, color=LAM),
            label(r"at most 5 ones per column: \ no carries, \ so the columns never interfere", font_size=20,
                  color=GREY_A),
            label(rf"green rows: \ the subset from our solver's assignment; \\ its sum is {ss['sum']} \ = the target",
                  font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, RIGHT, buff=0.6).align_to(tab, UP)
        fit_right(notes)
        with self.voiceover(
            "Third disguise, with no graphs at all: subset sum. Pick some of these numbers to hit the target "
            "exactly. <bookmark mark='a'/> Each number is written in decimal, one column per variable and one per "
            "clause. The number y i has a one in variable i's column and in every clause where x i appears; z i "
            "does the same for not x i. <bookmark mark='b'/> The target has a one in every variable column, so "
            "exactly one of y i and z i must be chosen: a truth value. <bookmark mark='c'/> It has a three in every "
            "clause column. The chosen literals contribute between one and three there, and two slack numbers per "
            "clause can top it up, but only if at least one literal is true. <bookmark mark='d'/> No column ever "
            "holds more than five ones, so there are no carries and the columns cannot interfere. <bookmark "
            "mark='e'/> The green rows come from our solver's assignment, and they add up to the target exactly. "
            "Numbers have become logic."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, n_ in zip("abcde", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def karp(self):
        head = label(r"Karp \ (1972): \ twenty-one problems, \ one family", font_size=32).to_edge(UP, buff=0.3)
        items = VGroup()
        for d, nm in KARP:
            col = [NO, HEAD, DATA, LAM, YES, CTRL, GREY_A][d]
            t = label(nm, font_size=19, color=col)
            items.add(t)
        left = VGroup(*items[:10]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        right = VGroup(*items[10:]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        for grp, start in ((left, 0), (right, 10)):
            for k, t in enumerate(grp):
                t.shift(RIGHT * 0.45 * KARP[start + k][0])
        VGroup(left, right).arrange(RIGHT, buff=1.2, aligned_edge=UP).next_to(head, DOWN, buff=0.4)
        right.shift(UP * 0)
        notes = VGroup(
            label(r"indent = one more reduction from SAT", font_size=19, color=GREY_A),
            label(r"Garey and Johnson's catalogue \ (1979): \ over 300; \ today, \ thousands", font_size=21,
                  color=WHITE),
            label(r"each new problem joins with \textbf{one} reduction, \ and they all stand or fall together",
                  font_size=21, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In 1972, a year after Cook, Richard Karp showed that twenty-one well-known problems are NP-complete. "
            "<bookmark mark='a'/> Here is his family tree. Satisfiability at the root; from it, integer programming, "
            "clique, and three-SAT. From clique, set packing and vertex cover; from vertex cover, set covering, "
            "feedback sets and the Hamiltonian cycle problems. From three-SAT, chromatic number, then exact cover, "
            "and from there Steiner trees, three-dimensional matching, knapsack, partition and max cut. <bookmark "
            "mark='b'/> Michael Garey and David Johnson's 1979 catalogue listed more than three hundred, and today "
            "there are thousands. <bookmark mark='c'/> Each joined the family with a single reduction, and they "
            "stand or fall together: a fast algorithm for any one of them would solve them all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in items], lag_ratio=0.12), FadeIn(notes[0]),
                      run_time=5.0)
            for mk, n_ in zip("bc", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
