from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs22.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, load, mono)


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
        tiles = Group(
            tile(MathTex(r"\det\begin{pmatrix} q - p \\ r - p \end{pmatrix}", font_size=40, color=DATA),
                 r"exact orientation", DATA),
            tile(MathTex(r"\Omega(n \log n)", font_size=46, color=YES), r"hulls and sorting", YES),
            tile(MathTex(r"2n + k", font_size=48, color=LAM), r"the sweep line", LAM),
            tile(MathTex(r"z = x^2 + y^2", font_size=44, color=HEAD), r"Voronoi, \ Delaunay, \ lifting", HEAD),
            tile(MathTex(r"\mathbb{E}[\deg] < 6", font_size=46, color=CTRL), r"backwards analysis", CTRL),
            tile(MathTex(r"\sqrt n + k", font_size=48, color=COST), r"kd-trees; \ HNSW", COST),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ Geometry", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            "What we built in this part. An orientation test that is never wrong, at almost no cost. Five convex "
            "hull algorithms, and the reduction from sorting that bounds them all. The sweep line, and guards for "
            "an art gallery. Voronoi diagrams by Fortune's sweep, Delaunay triangulations by flips and by random "
            "insertion, and the paraboloid that makes them one thing. Backwards analysis, linear programming, "
            "kd-trees, point location, navigable graphs in high dimensions, and a robot that slides between "
            "obstacles."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"linear programming in many dimensions: \ the simplex method", [23]),
            (r"3SUM and the fine-grained lower bounds", [27]),
            (r"vector search: \ embeddings and nearest-neighbour graphs", [47]),
            (r"geospatial indexes and nearest-neighbour services", [48]),
            (r"rasterizing triangles with edge functions; \ ray tracing with BVHs", [51]),
            (r"floating point, \ interval arithmetic and exact reals", [52]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 23 takes linear programming to many dimensions with the simplex method. "
            "Part 27 builds fine-grained complexity on three-sum. Part 47's search engine adds vector search over "
            "embeddings, with the graphs of chapter twelve, and Part 48 serves nearest-neighbour queries on maps. "
            "Part 51 draws triangles with the orientation test, which graphics calls an edge function, and traces "
            "rays through bounding-volume hierarchies. And Part 52 returns to floating point and computing with real "
            "numbers."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"maps", r"PostGIS, \ GEOS and S2: \ exact predicates, \ R-trees, \ point location, \ polygon overlay"),
            (r"meshes", r"CGAL, \ Shewchuk's \texttt{Triangle}, \ TetGen: \ Delaunay meshes for simulation"),
            (r"graphics", r"edge functions on every GPU; \ BVHs for ray tracing; \ collision tests in games"),
            (r"robots", r"configuration spaces, \ sampling planners \ (OMPL), \ visibility graphs"),
            (r"vectors", r"FAISS, \ pgvector, \ Lucene: \ HNSW graphs for embeddings"),
        ])
        with self.voiceover(
            "In practice. Geographic systems like PostGIS and Google's S2 library run on exact predicates, R-trees and "
            "polygon overlay. CGAL and Shewchuk's Triangle build Delaunay meshes for simulation. Every graphics card "
            "rasterizes with orientation tests, and every game tests collisions. Robot planners search configuration "
            "spaces, and every vector database searches a navigable graph."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that after sorting, \ Graham's scan makes fewer than $2n$ orientation tests.",
            r"Prove that the trapezoidal map of $n$ non-crossing segments has at most $3n + 1$ trapezoids.",
            r"Prove the lifting lemma: \ $d$ is inside the circle through $a, b, c$ exactly when its lift is below the "
            r"plane through theirs; \ derive the in-circle determinant from it.",
            r"Show that Seidel's algorithm moves the optimum at most $2H_n$ times in expectation, \ and does $O(n)$ "
            r"expected work.",
            r"\textit{Build.} \ The orientation test and Andrew's monotone chain in the Pebble language, \ with "
            r"coordinates below $2^{15}$ so every product fits in a word: \ hull 10,000 points on the emulator.",
            r"$\bigstar$ \textit{Research.} \ Our HNSW found 99.7\% of the true neighbours with 182 distance "
            r"computations, \ and no theorem explains it. \ Prove a query bound for graphs built by its diversity rule "
            r"on data of low doubling dimension, \ or construct inputs that force $\Omega(n)$ computations.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: the orientation test and the monotone chain in the Pebble language, run on the emulator. The "
            "last, marked with a star, is a research problem: its answer is not known, and the notes say where to "
            "start."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 23, \ Optimization", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"the simplex method, \ walking the edges of a polytope", DATA),
            (r"duality: \ a certificate from the other side", YES),
            (r"LP relaxations and random hyperplanes for hard problems", LAM),
            (r"online algorithms that are competitive without seeing the future", HEAD))]).arrange(DOWN, buff=0.35)
        items.move_to(UP * 0.0)
        q = label(r"choose the best point of a polytope", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time, optimization. Many problems are a choice of the best point of a polytope. The simplex method "
            "walks the polytope's edges; duality certifies the answer from the other side. When integrality makes "
            "a problem hard, relaxations and random hyperplanes still get provably close, and online, without seeing "
            "the future, you can still be competitive. Part 23, Optimization."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"de Berg, \ Cheong, \ van Kreveld and Overmars, \textit{Computational Geometry: Algorithms and "
             r"Applications}",
             r"Preparata and Shamos, \textit{Computational Geometry}; \ O'Rourke, \textit{Computational Geometry in C}",
             r"Devadoss and O'Rourke, \textit{Discrete and Computational Geometry}; \ Edelsbrunner, \textit{Geometry "
             r"and Topology for Mesh Generation}"],
            [r"Graham (1972); \ Jarvis (1973); \ Chan (1996); \ Bentley and Ottmann (1979); \ Chv\'atal (1975); \ "
             r"Fisk (1978)",
             r"Fortune (1987); \ Lawson (1977); \ Brown (1979); \ Guibas, Knuth and Sharir (1992); \ Clarkson and "
             r"Shor (1989)",
             r"Seidel (1991, 1993); \ Bentley (1975); \ Mulmuley (1990); \ Malkov and Yashunin (2016)",
             r"Shewchuk (1997); \ Kettner et al. (2008); \ Gajentaan and Overmars (1995); \ Andoni and Razenshteyn "
             r"(2015)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
