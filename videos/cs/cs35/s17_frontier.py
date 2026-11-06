from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs35.common import (CODE, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono, num)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.triangles()
        self.agm()
        self.learned()
        self.checking()
        self.open_problems()

    def card(self):
        card = chapter_card(16, r"Frontier: \ joins, \ guesses, \ guarantees", r"What is still unsolved?",
                            lit=(2008, 2012, 2019), extra=((2008, r"the AGM bound"),
                                                           (2012, r"worst-case optimal joins"),
                                                           (2019, r"learned optimizers")), part=PART)
        with self.voiceover("Chapter sixteen. Frontier: joins, guesses, and guarantees."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def triangles(self):
        f = load("frontier")["rows"]
        head = label(r"A query every binary plan gets wrong", font_size=36).to_edge(UP, buff=0.3)
        sql = VGroup(mono("SELECT COUNT(*) FROM E AS R, E AS S, E AS T", 17, YES),
                     mono("WHERE R.b = S.a AND S.b = T.b AND R.a = T.a", 17, YES)).arrange(DOWN, aligned_edge=LEFT,
                                                                                          buff=0.06)
        sql.next_to(head, DOWN, buff=0.35)
        tri = VGroup()
        pts = [UP * 0.8, DL * 0.8 + LEFT * 0.2, DR * 0.8 + RIGHT * 0.2]
        for p in pts:
            tri.add(Dot(p, radius=0.08, color=HEAD))
        tri.add(*[Line(pts[i], pts[(i + 1) % 3], color=HEAD, stroke_width=2.5) for i in range(3)])
        tri.move_to([-4.6, 1.0, 0])
        tl = label(r"the triangles of a graph", font_size=18, color=HEAD).next_to(tri, DOWN, buff=0.15)
        hub = VGroup(Dot(ORIGIN, radius=0.1, color=NO))
        for k in range(14):
            a = 2 * math.pi * k / 14
            hub.add(Line(ORIGIN, [0.9 * math.cos(a), 0.9 * math.sin(a), 0], color=GREY_B, stroke_width=1.2))
        hub.move_to([-4.6, -1.15, 0])
        hl = label(r"a hub: \ $d$ edges make $d^2/2$ paths", font_size=18, color=NO).next_to(hub, DOWN, buff=0.12)
        rows = [[num(r["edges"]), num(r["paths"]), num(r["wcoj_work"]), num(r["triangles"])] for r in f]
        tab = grid_table([r"edges $N$", r"binary join: \ 2-paths built", r"generic join: \ work", r"triangles"],
                         rows, widths=[1.8, 3.2, 2.8, 1.8], row_h=0.44, font_size=19, mono_cols=())
        tab.move_to([1.9, 0.2, 0])
        for r in range(1, 4):
            tab.cells[r][1].set_color(NO)
            tab.cells[r][2].set_color(YES)
        lines = VGroup(
            label(r"any plan of two-way joins first joins two copies of the edges: \ every path of length two, \ "
                  r"most of which close no triangle", font_size=19, color=NO),
            label(r"a \textbf{generic join} binds one variable at a time: \ for each edge $(a, b)$, \ intersect the "
                  r"neighbours of $a$ and of $b$", font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.35)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "Everything in this part's optimizer joins two tables at a time. Here is a query where that is "
            "provably the wrong idea. <bookmark mark='a'/> Join an edge table to itself three times to find "
            "triangles in a graph: a and b connected, b and c, and c back to a. <bookmark mark='b'/> Any plan made of "
            "two-way joins must first join two of the three, which produces every path of two edges. In a graph with "
            "a few hubs, a node with d edges makes about d squared over two such paths, and almost none of them close "
            "a triangle. <bookmark mark='c'/> On our graphs, four and a half thousand edges give over a million "
            "paths, to find four hundred and thirty-two triangles. <bookmark mark='d'/> A different kind of join "
            "binds one variable at a time: for each edge, intersect the neighbour lists of its two ends. Ten thousand "
            "steps instead of a million."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sql))
            vo.wait_until("a")
            self.play(FadeIn(tri), FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeIn(hub), FadeIn(hl), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(tab.cells[0][0]), FadeIn(tab.cells[0][1]), FadeIn(tab.cells[0][3]), FadeIn(tab.rule),
                      *[FadeIn(tab.cells[r][c]) for r in range(1, 4) for c in (0, 1, 3)])
            vo.wait_until("d")
            self.play(FadeIn(tab.cells[0][2]), *[FadeIn(tab.cells[r][2]) for r in range(1, 4)], FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def agm(self):
        f = load("frontier")["rows"]
        head = label(r"The AGM bound, \ and joins that meet it", font_size=36).to_edge(UP, buff=0.3)
        eq = MathTex(r"|R \bowtie S \bowtie T| \;\le\; \sqrt{|R|\,|S|\,|T|} \;=\; N^{3/2}", font_size=40,
                     color=HEAD).next_to(head, DOWN, buff=0.5)
        lines = VGroup(
            label(r"Atserias, \ Grohe and Marx \ (2008): \ for any join query, \ the largest possible output is "
                  r"$\prod |R_i|^{x_i}$, \ with $x$ the optimal \textbf{fractional edge cover}", font_size=20,
                  color=WHITE),
            label(rf"for triangles: \ $N^{{3/2}}$; \ with $N$ = {num(f[0]['edges'])}, \ at most "
                  rf"{num(f[0]['agm'])} triangles could exist", font_size=20, color=HEAD),
            label(r"but a binary plan can take $\Theta(N^2)$ time on such inputs: \ worse than the largest output",
                  font_size=20, color=NO),
            label(r"Ngo, \ Porat, \ R\'e and Rudra \ (2012), \ Veldhuizen's leapfrog triejoin \ (2014): \ "
                  r"\textbf{worst-case optimal} joins, \ time $O(\text{AGM bound})$", font_size=20, color=YES),
            label(r"now in LogicBlox, \ Umbra, \ DuckDB extensions and graph databases; \ the open question is when "
                  r"to use them, \ and how to cost them", font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).next_to(eq, DOWN, buff=0.5).set_x(0)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "How large can the answer to a join be? <bookmark mark='a'/> In 2008 Albert Atserias, Martin Grohe and "
            "Dániel Marx gave an exact answer for any join query: the product of the table sizes, each raised to a "
            "weight from a small linear program, the fractional edge cover. <bookmark mark='b'/> For triangles, each "
            "table gets weight one half, and the bound is N to the three halves: with forty-five hundred edges, at "
            "most three hundred thousand triangles could exist. <bookmark mark='c'/> But a plan of binary joins can "
            "take time proportional to N squared on such inputs, more than the largest possible answer. "
            "<bookmark mark='d'/> In 2012 Hung Ngo and colleagues found join algorithms whose running time never "
            "exceeds the bound, and Todd Veldhuizen's leapfrog triejoin is a practical one. They are called "
            "worst-case optimal. <bookmark mark='e'/> They now appear in commercial and research systems, and the "
            "open questions are when to use them instead of ordinary joins, and how to estimate their cost."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def learned(self):
        head = label(r"Learning to guess", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            label(r"chapter 7's problem: \ estimates wrong by $10^4$ in every system \ (Leis et al., 2015)",
                  font_size=21, color=NO),
            label(r"\textbf{learned cardinalities}: \ train a model on the data, \ or on past queries, \ to predict "
                  r"sizes \ (Kipf et al., 2019; \ Yang et al., 2019)", font_size=21, color=HEAD),
            label(r"\textbf{learned optimizers}: \ Neo \ (Marcus et al., 2019) \ learns whole plans; \ Bao \ (2021) "
                  r"\ only steers the existing optimizer with hints", font_size=21, color=YES),
            label(r"the catch: \ a model can be wrong in new ways; \ a plan that regresses in production is worse "
                  r"than a plan that was always mediocre", font_size=21, color=KERN),
            label(r"the open goal: \ learned methods with \textbf{guarantees}: \ never much worse than the classical "
                  r"optimizer", font_size=21, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.55)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "The second frontier is estimation. <bookmark mark='a'/> We saw how badly independence assumptions fail. "
            "<bookmark mark='b'/> One line of research trains models, on the data itself or on the queries already "
            "run, to predict the sizes of results, capturing correlations that histograms miss. "
            "<bookmark mark='c'/> Another learns the plans directly. Neo, in 2019, replaced the optimizer with a "
            "neural network trained on experience. Bao, two years later, was more modest: it keeps the classical "
            "optimizer and learns only which hints to give it, query by query. <bookmark mark='d'/> The difficulty is "
            "trust. A model can be wrong in ways no one predicted, and a query that suddenly takes an hour instead of "
            "a second is worse for its users than one that was always a little slow. <bookmark mark='e'/> The goal is "
            "learning with guarantees: never much worse than the classical method, often much better."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def checking(self):
        head = label(r"Does the database keep its promise?", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            label(r"black-box testing: \ run concurrent transactions, \ record what each read and wrote, \ then ask "
                  r"whether the history meets the promised level", font_size=20, color=WHITE),
            label(r"serializability of a history: \ NP-complete \ (Papadimitriou, 1979); \ snapshot isolation too \ "
                  r"(Biswas and Enea, 2019); \ read committed: \ polynomial", font_size=20, color=NO),
            label(r"the escape: \ design the test so that versions are recoverable \ (append to lists, \ unique "
                  r"values), \ and the graph of chapter 12 can be built directly", font_size=20, color=HEAD),
            label(r"Elle \ (2020) \ and Cobra \ (2020, \ SMT-based) \ check millions of operations; \ Jepsen reports "
                  r"have found anomalies in many shipped systems", font_size=20, color=YES),
            label(r"and proofs: \ verified query optimizers and SQL semantics \ (Cosette, 2017); \ SQL query "
                  r"equivalence is undecidable in general \ (Part 25)", font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.55)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "The third frontier is checking. <bookmark mark='a'/> How do we know a database delivers the isolation "
            "it promises? Run many transactions against it at once, record what each read and wrote, and check the "
            "history. <bookmark mark='b'/> In general this is hard: deciding whether a history is serializable is "
            "NP-complete, and so, it was shown in 2019, is deciding snapshot isolation, although read committed is "
            "easy. <bookmark mark='c'/> The way out is to design the test so that every read reveals which write it "
            "saw, for example by appending to lists and reading whole lists. Then the dependency graph of chapter "
            "twelve can be built directly and searched for cycles. <bookmark mark='d'/> Elle does exactly this, and "
            "Cobra uses a constraint solver; between them they check millions of operations, and they have found real "
            "anomalies in many shipped databases. <bookmark mark='e'/> Further out are proofs: verified semantics for "
            "SQL and verified rewrites, though in general deciding whether two SQL queries are equivalent is "
            "undecidable, a cousin of Part 25's halting problem."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def open_problems(self):
        head = label(r"Open problems", font_size=36).to_edge(UP, buff=0.3)
        probs = VGroup(*[label(t, font_size=21, color=WHITE) for t in (
            r"1. \ Cardinality estimates with provable error bounds, \ for queries with many joins",
            r"2. \ Optimizers that mix binary and worst-case optimal joins, \ and cost both correctly",
            r"3. \ Learned optimizers that are guaranteed never to regress",
            r"4. \ Serializable transactions across continents at the cost of snapshot isolation",
            r"5. \ Efficient checking of isolation levels on arbitrary black-box histories",
            r"6. \ Self-driving databases: \ indexes, \ layouts and settings chosen and changed automatically",
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
        star = label(r"$\bigstar$ \ the part's research problem asks how few aborts a serializable snapshot scheduler "
                     r"can make", font_size=19, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Six problems at the frontier. <bookmark mark='a'/> Size estimates with provable error bounds, even for "
            "queries with many joins. <bookmark mark='b'/> Optimizers that combine ordinary and worst-case optimal "
            "joins in one plan, and cost both correctly. <bookmark mark='c'/> Learned optimizers that are guaranteed "
            "never to make a query slower. <bookmark mark='d'/> Serializable transactions across continents, at the "
            "price of snapshot isolation. <bookmark mark='e'/> Checking isolation levels efficiently on any history, "
            "not just ones designed for checking. <bookmark mark='f'/> And databases that drive themselves, choosing "
            "and changing their own indexes, layouts and settings. The research problem at the end of this part asks "
            "something small and sharp: how few aborts can a serializable snapshot scheduler get away with?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcdef", probs):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()


_ = (CODE, DATA, NO)
