from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs18.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, load, mono)


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


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        a = load("astar")["avg"]
        tiles = Group(
            tile(MathTex(r"\text{all degrees even}", font_size=36, color=HEAD), r"Euler", HEAD),
            tile(MathTex(r"[d(u), f(u)]", font_size=44, color=DATA), r"DFS's parentheses", DATA),
            tile(MathTex(r"d(y) \le \ell(P) < d(u)", font_size=36, color=YES), r"Dijkstra's invariant", YES),
            tile(MathTex(rf"{a['dijkstra'] / a['ch']:.0f}\times \text{{ fewer}}", font_size=40, color=LAM),
                 r"contraction hierarchies", LAM),
            tile(MathTex(r"\max \text{flow} = \min \text{cut}", font_size=36, color=CTRL), r"flows", CTRL),
            tile(MathTex(r"V - E + F = 2", font_size=44, color=FUNC), r"planarity", FUNC),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ Graphs", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            "What we built in this part. Euler's theorem and Hierholzer's circuit. Breadth-first layers and "
            "bipartiteness; depth-first parentheses, edge classes and cycles; topological order; strongly connected "
            "components and 2-SAT. Dijkstra's invariant, Bellman–Ford and arbitrage, all pairs by dynamic "
            "programming and reweighting, and route planning that settles twenty times fewer vertices than Dijkstra. Spanning trees from "
            "the cut property, the max-flow min-cut theorem, stable matching, the gap between Euler and Hamilton, "
            "PageRank, and four colours."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"dynamic programming: \ Floyd--Warshall and Held--Karp generalized", [19]),
            (r"random walks and expanders; \ randomized min cut", [20]),
            (r"linear programming duality: \ max flow and min cut", [23]),
            (r"Hamiltonian cycles, \ 3-colouring and NP-completeness", [26]),
            (r"the APSP conjecture", [27]),
            (r"routing: \ distance vectors and link states", [36]),
            (r"graph databases and query planning", [35]),
            (r"web search: \ crawling, \ ranking", [47]),
        ], font_size=24)
        with self.voiceover(
            "Where this comes back. Part 19 turns Floyd–Warshall and Held–Karp into a general method, dynamic "
            "programming. Part 20 studies random walks and finds minimum cuts by randomly contracting edges. Part 23 "
            "shows that max flow and min cut are dual linear programs. Part 26 is about Hamiltonian cycles, "
            "three-colouring and NP-completeness, and Part 27 about the all-pairs conjecture. The internet's "
            "routing in Part 36 runs Bellman–Ford and Dijkstra across routers, Part 35's databases plan queries "
            "over graphs, and Part 47's search engine ranks the web."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"routing", r"maps use contraction hierarchies and their descendants, \ not plain Dijkstra"),
            (r"builds", r"every build tool is a topological sort with caching"),
            (r"networks", r"OSPF runs Dijkstra on every router; \ BGP is a path-vector Bellman--Ford"),
            (r"data", r"graph databases, \ fraud rings as cycles, \ social graphs as BFS"),
            (r"interviews", r"BFS, \ DFS, \ topological sort, \ Dijkstra and union--find are half of them"),
        ])
        with self.voiceover(
            "In practice. Map services answer routes with contraction hierarchies and their descendants, never "
            "plain Dijkstra. Every build tool is a topological sort with a cache. Inside the internet, OSPF runs "
            "Dijkstra on every router, and BGP is a path-vector cousin of Bellman–Ford. Graph databases find fraud "
            "rings as cycles and friends of friends by breadth-first search. And breadth-first search, depth-first "
            "search, topological sort, Dijkstra and union–find are half of all coding interviews."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that a connected graph with all degrees even has an Euler circuit, \ and that Hierholzer's "
            r"algorithm runs in $O(E)$.",
            r"Prove that BFS dequeues vertices in non-decreasing order of distance, \ and use it to show the BFS "
            r"tree contains shortest paths.",
            r"Show that Dijkstra can fail with a single negative edge, \ and that Johnson's reweighting $w + p(u) - "
            r"p(v)$ preserves every shortest path.",
            r"Prove the cut property, \ and deduce that Kruskal's and Prim's algorithms are correct.",
            r"\textit{Build.} \ Implement Dijkstra in the Pebble language with Part 17's binary heap, \ run it on our city "
            r"grid on the emulator, \ and count instructions per edge.",
            r"$\bigstar$ \textit{Research.} \ Single-source shortest paths in $O(m)$ time on directed graphs with "
            r"non-negative real weights, \ or a lower bound that rules it out.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: Dijkstra in the Pebble language, on the emulator, counting instructions per edge. The last, "
            "marked with a star, is a research problem: its answer is not known, and the notes say where to start."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 19, \ The Great Paradigms", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"divide and conquer: \ FFT, \ closest pair", DATA), (r"greedy, \ and when it is right", LAM),
            (r"dynamic programming: \ edit distance, \ knapsack", YES),
            (r"backtracking and branch-and-bound", COST))]).arrange(DOWN, buff=0.35)
        items.move_to(UP * 0.0)
        q = label(r"four ways to design an algorithm", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time. This part used several design ideas without naming them: divide and conquer, greedy "
            "choices, dynamic programming, search. Part 19 makes them methods: the fast Fourier transform and the "
            "closest pair of points, when greedy choices are provably right, dynamic programming from edit "
            "distance to knapsack, and backtracking. Part 19, The Great Paradigms."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Cormen, Leiserson, Rivest and Stein, \textit{Introduction to Algorithms}, \ chapters 20--26",
             r"Kleinberg and Tardos, \textit{Algorithm Design}, \ chapters 3, 4, 7",
             r"Tarjan, \textit{Data Structures and Network Algorithms}; \ Even, \textit{Graph Algorithms}",
             r"Ahuja, Magnanti and Orlin, \textit{Network Flows}; \ Schrijver, \textit{Combinatorial Optimization}"],
            [r"Euler (1736); \ Hierholzer (1873); \ Moore (1959); \ Tarjan (1972); \ Kahn (1962)",
             r"Dijkstra (1959); \ Ford (1956); \ Bellman (1958); \ Floyd (1962); \ Johnson (1977)",
             r"Hart, Nilsson and Raphael (1968); \ Goldberg and Harrelson (2005); \ Geisberger et al. (2008)",
             r"Bor\r{u}vka (1926); \ Kruskal (1956); \ Prim (1957); \ Karger, Klein and Tarjan (1995)",
             r"Ford and Fulkerson (1956); \ Edmonds and Karp (1972); \ Gale and Shapley (1962); \ Brin and Page (1998)",
             r"Chen et al. (2022); \ Haeupler et al. (2024); \ Duan et al. (2025)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
