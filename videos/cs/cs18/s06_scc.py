from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs18.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, draw_graph, grid_table,
                                   load, mono, words)

POS = {1: (-5.4, 1.2), 2: (-3.8, 1.2), 3: (-4.6, -0.2), 4: (-2.2, 1.2), 5: (-1.4, -0.2), 6: (-3.0, -0.2),
       7: (-0.6, 1.2), 8: (0.6, 1.2)}


class Scc(VoiceoverScene):
    def construct(self):
        self.card()
        self.components()
        self.tarjan()
        self.web()
        self.twosat()

    def card(self):
        card = chapter_card(5, r"Strongly connected components", r"Which vertices can all reach each other?",
                            lit=(1972,), extra=((1972, r"Tarjan: \ one pass"), (1978, r"Kosaraju: \ two passes")),
                            part=PART)
        with self.voiceover("Chapter five. Strongly connected components."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def components(self):
        d = load("scc")
        head = label(r"Mutual reachability", font_size=34).to_edge(UP, buff=0.3)
        edges = [(int(u), v) for u, vs in d["graph"].items() for v in vs]
        g, nodes, es = draw_graph(POS, edges, directed=True)
        cols = [YES, LAM, CTRL]
        hulls = VGroup()
        for c, col in zip(d["comps"], cols):
            grp = VGroup(*[nodes[k] for k in c])
            hulls.add(SurroundingRectangle(grp, buff=0.18, corner_radius=0.2, color=col, stroke_width=2))
        dag = VGroup(
            VGroup(Circle(radius=0.35, color=LAM, fill_color=LAM, fill_opacity=0.3), mono("123", 15, WHITE)),
            VGroup(Circle(radius=0.35, color=YES, fill_color=YES, fill_opacity=0.3), mono("456", 15, WHITE)),
            VGroup(Circle(radius=0.35, color=CTRL, fill_color=CTRL, fill_opacity=0.3), mono("78", 15, WHITE)),
        ).arrange(RIGHT, buff=1.0).move_to(RIGHT * 4.0 + UP * 0.6)
        dag_e = VGroup(Arrow(dag[0].get_right(), dag[1].get_left(), buff=0.05, color=GREY_B, stroke_width=2),
                       Arrow(dag[2].get_left(), dag[1].get_right(), buff=0.05, color=GREY_B, stroke_width=2))
        dl = label(r"the \textbf{condensation}: \ always a DAG", font_size=20, color=GREY_B).next_to(dag, DOWN,
                                                                                               buff=0.25)
        pts = VGroup(
            label(r"$u$ and $v$ are in one \textbf{strongly connected component} if each can reach the other",
                  font_size=22, color=GREY_A),
            label(r"shrink each component to a point: \ what remains has no cycles", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "In a directed graph, reaching is not symmetric: a one-way street can take you somewhere you cannot "
            "come back from. <bookmark mark='a'/> Two vertices belong to the same strongly connected component if "
            "each can reach the other. Here the graph splits into three. <bookmark mark='b'/> Shrink each "
            "component to a single point and the result, the condensation, has no cycles at all: any cycle "
            "between components would merge them. So every directed graph is a DAG of strongly connected pieces."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]), Create(hulls), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(dag), Create(dag_e), FadeIn(dl), FadeIn(pts[1]))
        self.wait(0.3)
        self.clear_scene()

    def tarjan(self):
        d = load("scc")
        head = label(r"Tarjan's algorithm \ (1972): \ one DFS", font_size=34).to_edge(UP, buff=0.3)
        graph = {int(u): vs for u, vs in d["graph"].items()}
        pos = {k: (x - 0.4, y + 0.9) for k, (x, y) in POS.items()}
        g, nodes, es = draw_graph(pos, [(u, v) for u, vs in graph.items() for v in vs], directed=True)
        # the trace, exactly as the algorithm runs: push, low-link update, pop a component
        events, index, low, stack, on = [], {}, {}, [], set()

        def visit(v):
            index[v] = low[v] = len(index) + 1
            stack.append(v)
            on.add(v)
            events.append(("push", v, index[v]))
            for w in graph[v]:
                if w not in index:
                    visit(w)
                    if low[w] < low[v]:
                        low[v] = low[w]
                        events.append(("low", v, low[v]))
                elif w in on and index[w] < low[v]:
                    low[v] = index[w]
                    events.append(("low", v, low[v]))
            if low[v] == index[v]:
                comp = []
                while True:
                    w = stack.pop()
                    on.discard(w)
                    comp.append(w)
                    if w == v:
                        break
                events.append(("pop", comp, None))
        for v in sorted(graph):
            if v not in index:
                visit(v)
        tags = {}
        cells = []
        sl = label(r"stack", font_size=19, color=GREY_B).move_to([1.9, 2.5, 0])
        steps = VGroup(
            label(r"number vertices in discovery order; \ keep the open ones on a stack", font_size=20, color=GREY_A),
            MathTex(r"\mathrm{low}(v) = \text{smallest index reachable from } v\text{'s subtree by one edge back into "
                    r"the stack}", font_size=26, color=LAM),
            label(r"when a vertex finishes with $\mathrm{low}(v) = \mathrm{index}(v)$, \ it is the \textbf{root} of a "
                  r"component: \ pop the stack down to it", font_size=20, color=YES),
            label(r"components come out in reverse topological order of the condensation", font_size=20, color=HEAD),
            label(r"Kosaraju \ (1978): \ DFS for finish times, \ then DFS on the reversed graph in that order; \ "
                  r"also linear", font_size=19, color=GREY_B),
        ).arrange(DOWN, buff=0.17).to_edge(DOWN, buff=0.3)
        cols = [YES, LAM, CTRL]
        with self.voiceover(
            "Robert Tarjan found the components in a single depth-first search. <bookmark mark='a'/> Number the "
            "vertices in order of discovery, and keep the vertices of unfinished components on a stack. <bookmark "
            "mark='b'/> For each vertex, compute its low link: the smallest number reachable from its subtree using "
            "at most one edge back into the stack. <bookmark mark='c'/> When a vertex finishes and its low link is "
            "its own number, nothing below it can climb higher: it is the first-discovered vertex of a component, "
            "and the component is everything above it on the stack. <bookmark mark='d'/> The components emerge in "
            "reverse topological order of the condensation, exactly what 2-SAT will need. <bookmark mark='e'/> "
            "Sambasiva Rao Kosaraju's alternative uses two searches, the second on the reversed graph, and is just "
            "as fast."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(sl))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            ci = 0
            for kind, v, val in events:
                if kind == "push":
                    t = mono(f"{val}/{val}", 15, HEAD).next_to(nodes[v], UP, buff=0.06)
                    tags[v] = t
                    c = VGroup(Square(side_length=0.5, color=DATA, fill_color=DATA, fill_opacity=0.3,
                                      stroke_width=1.5), mono(str(v), 16, WHITE))
                    c.move_to([1.9 + 0.58 * len(cells), 1.9, 0])
                    cells.append((v, c))
                    self.play(FadeIn(t), FadeIn(c), nodes[v][0].animate.set_stroke(HEAD, width=3), run_time=0.4)
                elif kind == "low":
                    t = mono(f"{index[v]}/{val}", 15, LAM).move_to(tags[v])
                    self.play(Transform(tags[v], t), run_time=0.35)
                else:
                    col = cols[ci]
                    ci += 1
                    out = [c for w, c in cells[-len(v):]]
                    del cells[-len(v):]
                    hull = SurroundingRectangle(VGroup(*[nodes[w] for w in v], *[tags[w] for w in v]), buff=0.12,
                                                corner_radius=0.2, color=col, stroke_width=2)
                    self.play(*[FadeOut(c, shift=DOWN * 0.3) for c in out], Create(hull),
                              *[nodes[w][0].animate.set_fill(col, 0.35) for w in v], run_time=0.6)
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
            vo.wait_until("e")
            self.play(FadeIn(steps[4]))
        self.wait(0.3)
        self.clear_scene()

    def web(self):
        d = load("scc")
        head = label(rf"A synthetic web of {words(d['web_n'])} pages", font_size=34).to_edge(UP, buff=0.3)
        n = d["web_n"]
        tab = grid_table([r"", r"pages", r"share"], [
            [r"the giant strongly connected core", words(d["core"]), f"{100 * d['core'] / n:.0f}\\%"],
            [r"pages that reach the core, \ unreachable from it", words(d["in"]), f"{100 * d['in'] / n:.0f}\\%"],
            [r"pages reachable from the core only", words(d["out"]), f"{100 * d['out'] / n:.0f}\\%"],
        ], widths=[6.4, 2.2, 1.8], row_h=0.5, font_size=22, mono_cols=(),
            colors=[[YES, YES, YES], [DATA, DATA, DATA], [LAM, LAM, LAM]]).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"preferential attachment, \ a quarter of links returned: \\ most pages can reach the core, \ but "
                  r"the newest are reached by nobody", font_size=21, color=GREY_A),
            label(r"the real web in 1999 \ (Broder et al., \ 2000): \\ a \textbf{bow tie}, \ 28\% core, \ 21\% in, \ "
                  r"21\% out, \ the rest tendrils", font_size=21, color=HEAD),
            label(r"one linear-time pass over two hundred million pages: \ Tarjan's algorithm at scale", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.3)
        y0 = (tab.get_bottom()[1] + pts.get_top()[1]) / 2
        bow = VGroup(
            Ellipse(width=2.6, height=1.0, color=DATA, fill_color=DATA, fill_opacity=0.25).move_to([-3.0, y0, 0]),
            Circle(radius=0.62, color=YES, fill_color=YES, fill_opacity=0.3).move_to([0, y0, 0]),
            Ellipse(width=2.6, height=1.0, color=LAM, fill_color=LAM, fill_opacity=0.25).move_to([3.0, y0, 0]),
        )
        bow.add(Arrow(bow[0].get_right(), bow[1].get_left(), buff=0.05, color=GREY_B, stroke_width=2),
                Arrow(bow[1].get_right(), bow[2].get_left(), buff=0.05, color=GREY_B, stroke_width=2))
        bow.add(label(r"IN \ 21\%", font_size=19).move_to(bow[0]), label(r"core \ 28\%", font_size=19).move_to(
            bow[1]), label(r"OUT \ 21\%", font_size=19).move_to(bow[2]))
        with self.voiceover(
            "Components describe the large-scale shape of networks. <bookmark mark='a'/> We grew a synthetic web "
            "of twenty thousand pages, where new pages link to popular old ones and a quarter of links are "
            "returned, and computed its components. A giant core holds almost two fifths of the pages; all the "
            "others can reach it, but nothing links to the newest ones. <bookmark mark='b'/> When Andrei Broder and "
            "his colleagues did this to two hundred million real pages in 1999, they found a bow tie: a core of "
            "just over a quarter, a fifth that leads into it, a fifth reachable from it, and tendrils. <bookmark "
            "mark='c'/> It took one linear-time pass of this chapter's algorithm."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]), FadeIn(bow))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def twosat(self):
        head = label(r"2-SAT in linear time \ (Aspvall, \ Plass and Tarjan, \ 1979)", font_size=32).to_edge(
            UP, buff=0.3)
        formula = MathTex(r"(x_1 \lor x_2) \land (\lnot x_1 \lor x_3) \land (\lnot x_2 \lor \lnot x_3) \land "
                          r"(x_2 \lor x_3)", font_size=34).next_to(head, DOWN, buff=0.4)
        lit = {"x1": (-5.4, 0.7), "x2": (-3.6, 0.7), "x3": (-1.8, 0.7), "n1": (-5.4, -1.9), "n2": (-3.6, -1.9),
               "n3": (-1.8, -1.9)}
        tex = {"x1": r"x_1", "x2": r"x_2", "x3": r"x_3", "n1": r"\lnot x_1", "n2": r"\lnot x_2", "n3": r"\lnot x_3"}
        imp = [("n1", "x2"), ("n2", "x1"), ("x1", "x3"), ("n3", "n1"), ("x2", "n3"), ("x3", "n2"), ("n2", "x3"),
               ("n3", "x2")]
        comp = {"x1": 0, "x3": 0, "n2": 0, "n1": 1, "x2": 1, "n3": 1}
        nodes = {k: VGroup(Circle(radius=0.36, color=DATA, stroke_width=2, fill_color=BG, fill_opacity=1),
                           MathTex(tex[k], font_size=26)).move_to([x, y, 0]) for k, (x, y) in lit.items()}
        arrows = VGroup()
        for a_, b_ in imp:
            pa, pb = nodes[a_].get_center(), nodes[b_].get_center()
            # x3 and not-x2 (and x2 and not-x3) imply each other: bend that pair apart
            if {a_, b_} in ({"n2", "x3"}, {"n3", "x2"}):
                u = (pb - pa) / np.linalg.norm(pb - pa)
                arrows.add(CurvedArrow(pa + u * 0.4, pb - u * 0.4, angle=0.3, color=GREY_B, stroke_width=2,
                                       tip_length=0.16))
            else:
                arrows.add(Arrow(pa, pb, buff=0.38, color=GREY_B, stroke_width=2, max_tip_length_to_length_ratio=0.1))
        for a_ in arrows:
            a_.set_z_index(-1)
        steps = VGroup(
            label(r"each clause $a \lor b$ is two implications: \\ $\lnot a \to b$ \ and \ $\lnot b \to a$",
                  font_size=22, color=GREY_A),
            label(r"unsatisfiable \ $\iff$ \ some $x$ and $\lnot x$ \\ lie in the same component", font_size=22,
                  color=NO),
            label(r"otherwise set $x$ true when its component \\ comes later in topological order: \\ here $x_1 = "
                  r"x_3 = \text{true}, \ x_2 = \text{false}$", font_size=21, color=YES),
            label(r"with three literals per clause \\ the problem is NP-complete \ (Part 26)", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.6)
        with self.voiceover(
            "Components also solve a logic problem. <bookmark mark='a'/> Here is a formula in which every clause is "
            "the or of two literals. <bookmark mark='b'/> Each clause, a or b, says: if not a, then b, and if not b, "
            "then a. Make a vertex for every literal and an edge for every implication. <bookmark mark='c'/> The "
            "formula is unsatisfiable exactly when some variable and its negation imply each other, that is, lie in "
            "the same strongly connected component. <bookmark mark='d'/> Otherwise, setting each variable true when "
            "its component comes later in topological order gives a solution; here, x one and x three true, x two "
            "false. <bookmark mark='e'/> With three literals per clause instead of two, no polynomial algorithm is "
            "known, and Part 26 explains why that gap matters."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(formula))
            vo.wait_until("b")
            self.play(FadeIn(steps[0]), *[FadeIn(n) for n in nodes.values()])
            self.play(LaggedStart(*[GrowArrow(a_) if isinstance(a_, Arrow) else Create(a_) for a_ in arrows],
                                  lag_ratio=0.2), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(steps[1]), *[nodes[k][0].animate.set_fill([YES, NO][c], 0.4) for k, c in comp.items()])
            vo.wait_until("d")
            self.play(FadeIn(steps[2]))
            vo.wait_until("e")
            self.play(FadeIn(steps[3]))
        self.wait(0.3)
        self.clear_scene()
