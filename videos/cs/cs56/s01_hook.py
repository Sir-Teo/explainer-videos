from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs56.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


class Hook(VoiceoverScene):
    def construct(self):
        self.drawings()
        self.three()
        self.plan()

    def drawings(self):
        head = label(r"Two graphs, \ one number apart", font_size=36).to_edge(UP, buff=0.3)
        import math
        import random
        rng = random.Random(4)
        n = 16

        def ring_graph(center, chords):
            pts = [center + 1.9 * np.array([math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n), 0])
                   for k in range(n)]
            edges = [(k, (k + 1) % n) for k in range(n)] + chords
            lines = VGroup(*[Line(pts[a], pts[b], color=GREY_C, stroke_width=1.6) for a, b in edges])
            dots = VGroup(*[Dot(p, radius=0.07, color=WHITE) for p in pts])
            return VGroup(lines, dots)

        left = ring_graph(LEFT * 3.4 + DOWN * 0.3, [(k, k + 2) for k in range(n) if k % 4 in (0, 1)])
        perm = list(range(n))
        rng.shuffle(perm)
        right = ring_graph(RIGHT * 3.4 + DOWN * 0.3, [(perm[2 * k], perm[2 * k + 1]) for k in range(n // 2)])
        l1 = label(r"each vertex: \ 3 neighbours, \ local chords", font_size=19, color=GREY_A).next_to(left, DOWN,
                                                                                                buff=0.3)
        l2 = label(r"each vertex: \ 3 neighbours, \ random chords", font_size=19, color=GREY_A).next_to(right, DOWN,
                                                                                                 buff=0.3)
        A1 = np.zeros((n, n))
        A2 = np.zeros((n, n))
        for (A, extra) in ((A1, [(k, k + 2) for k in range(n) if k % 4 in (0, 1)]),
                           (A2, [(perm[2 * k], perm[2 * k + 1]) for k in range(n // 2)])):
            for a, b in [(k, (k + 1) % n) for k in range(n)] + extra:
                A[a, b] = A[b, a] = 1
        def gap(A):
            d = A.sum(axis=1)
            N = np.eye(n) - A / np.sqrt(np.outer(d, d))
            return float(np.sort(np.linalg.eigvalsh(N))[1])
        g1 = label(rf"$\lambda_2 = {gap(A1):.3f}$", font_size=28, color=NO).next_to(l1, DOWN, buff=0.2)
        g2 = label(rf"$\lambda_2 = {gap(A2):.3f}$", font_size=28, color=YES).next_to(l2, DOWN, buff=0.2)
        with self.voiceover(
            "Here are two graphs. <bookmark mark='a'/> Each has sixteen vertices arranged in a ring, and some extra "
            "edges. On the left the extra edges are short chords between near neighbours; on the right they are "
            "random. <bookmark mark='b'/> In a drawing they look much alike. But one number tells them apart: the "
            "second smallest eigenvalue of a matrix built from the graph. <bookmark mark='c'/> On the left it is "
            "small: the graph is easy to cut in two, and a random walk on it takes a long time to forget where it "
            "started. On the right it is almost three times larger: no cut is cheap, and walks mix fast. This part is about "
            "what the eigenvalues of a graph know."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(left[0]), FadeIn(left[1]), Create(right[0]), FadeIn(right[1]), run_time=2)
            self.play(FadeIn(l1), FadeIn(l2))
            vo.wait_until("b")
            self.play(Indicate(left), Indicate(right))
            vo.wait_until("c")
            self.play(FadeIn(g1), FadeIn(g2))
        self.wait(0.4)
        self.clear_scene()

    def three(self):
        s = load("series")
        head = label(r"The series' own graphs", font_size=36).to_edge(UP, buff=0.3)
        rows = []
        for name, r in s.items():
            rows.append([name, rf"{r['n']:,}", rf"{r['edges']:,}", rf"{r['lambda2']:.3f}", rf"{r['sweep_phi']:.3f}"])
        tab = grid_table([r"graph", r"vertices", r"edges", r"$\lambda_2$", r"best sweep cut"], rows,
                         widths=[4.4, 1.8, 1.6, 1.6, 2.6], row_h=0.6, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.6)
        notes = VGroup(
            label(r"the city is long and thin to a walker: \ cut it across the middle", font_size=20, color=NO),
            label(r"the internet and the words are far better connected", font_size=20, color=YES),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.5)
        city = s["city grid (Part 18)"]
        with self.voiceover(
            "The same number, computed for three graphs this series has already built. <bookmark mark='a'/> Part 18's "
            f"city grid has {city['n']} intersections, and its second eigenvalue is tiny: about "
            f"{city['lambda2']:.3f}. A grid is easy to cut through the middle, and the cut the eigenvector finds "
            "crosses only a few roads. <bookmark mark='b'/> Part 36's internet of providers and customers, and a graph "
            "of words that occur near each other in one of our novels, are far better connected. "
            "<bookmark mark='c'/> By the end of this part we will know why this one eigenvalue bounds how hard a graph "
            "is to cut, how fast it mixes, and how it carries electric current, and how those facts led, in 2022, to "
            "the fastest known algorithm for maximum flow."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[1])), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[2])), FadeIn(VGroup(*tab.cells[3])), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Indicate(VGroup(*[c[3] for c in tab.cells[1:]]), color=HEAD))
        self.wait(0.4)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Spectral Graphs and Expanders", font_size=36).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"the Laplacian, \ its energy and its eigenvalues",
            r"the Fiedler vector, \ and Cheeger's inequality proved",
            r"random walks and their mixing time",
            r"expanders: \ random, \ Ramanujan and zig-zag",
            r"graphs as circuits, \ and fast Laplacian solvers",
            r"electrical flows to almost-linear max-flow",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 56 of Computer Science, Built, and the first part of Act Eleven, the research frontier. "
            "<bookmark mark='a'/> We will build the Laplacian of a graph and read its eigenvalues; use the Fiedler "
            "vector to cut graphs, and prove Cheeger's inequality; measure how random walks mix; construct expanders, "
            "graphs that are sparse but impossible to cut; treat graphs as electrical circuits; and follow those "
            "circuits to a maximum-flow algorithm that runs in almost linear time."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (BG, DATA, KERN, LAM, NO, YES)
