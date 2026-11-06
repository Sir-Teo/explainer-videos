from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs22.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, load, mono, words)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.exact()
        self.threesum()
        self.neighbours()
        self.open_()

    def card(self):
        card = chapter_card(15, r"Frontier: \ exactness, \ 3SUM \ and nearest neighbours",
                            r"What can geometry still not do fast, \ or right?", lit=(1995, 2015),
                            extra=((1995, r"Gajentaan--Overmars"), (2015, r"Andoni--Razenshteyn")), part=PART)
        with self.voiceover("Chapter fifteen. Frontier: exactness, three-sum, and nearest neighbours."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def exact(self):
        d = load("frontier")
        head = label(r"Exact geometric computation", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"Yap's paradigm \ (1997): \ decide every predicate exactly; \ the combinatorics are then always "
                  r"right", font_size=22, color=WHITE),
            label(rf"the price, \ on nearly collinear points: \ {d['float_ns']:.0f} ns in floating point, \ "
                  rf"{d['exact_ns'] / 1000:.0f} $\mu$s in rationals, \ {d['exact_ns'] / d['float_ns']:.0f}$\times$",
                  font_size=22, color=NO),
            label(r"adaptive filters \ (chapter 1) \ pay it only where needed: \ CGAL, \ LEDA, \ Shewchuk's "
                  r"\texttt{Triangle}", font_size=22, color=YES),
            label(r"degenerate inputs: \ simulate a symbolic perturbation \ (Edelsbrunner and M\"ucke, 1990)",
                  font_size=22, color=LAM),
            label(r"still hard: \ \textbf{constructions}. \ An intersection point needs more bits than its inputs, \\ "
                  r"and chained constructions explode; \ snap rounding \ (Hobby, 1999) \ trades exactness for size",
                  font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.34).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The frontier has three fronts. The first is the one this part began with. <bookmark mark='a'/> Chee Yap's "
            "paradigm of exact geometric computation says: decide every predicate exactly, and the combinatorial "
            "structure, which points are on the hull, which triangles are Delaunay, will always be right. <bookmark "
            "mark='b'/> Exactness has a price. On nearly collinear points, our rational orientation test is about a "
            "hundred and twenty times slower than floating point. <bookmark mark='c'/> Adaptive filters pay it only "
            "where the answer is in doubt, which is how CGAL, LEDA and Shewchuk's Triangle mesh generator work. "
            "<bookmark mark='d'/> Inputs that really are degenerate, three points exactly on a line, can be handled "
            "by pretending the points were perturbed by infinitesimals, consistently. <bookmark mark='e'/> What "
            "remains hard is constructing new points. An intersection of two segments needs more bits than its "
            "endpoints, and intersecting the results again makes it worse, so long chains of constructions grow "
            "without bound. Snap rounding keeps them small at the cost of moving things slightly, and how to do that "
            "well in three dimensions is still open."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def threesum(self):
        d = load("frontier")
        head = label(r"3SUM: \ the quadratic wall of the plane", font_size=34).to_edge(UP, buff=0.35)
        nums = d["nums"]
        O = np.array([-3.6, -0.5, 0])
        sx, sy = 0.052, 1.05e-5

        def P(x, y):
            return O + np.array([x * sx, y * sy, 0])
        cub = ParametricFunction(lambda t: P(t, t ** 3), t_range=[-64, 64], color=GREY_D, stroke_width=1.5)
        axes = VGroup(Line(P(-66, 0), P(66, 0), color=GREY_D, stroke_width=1),
                      Line(P(0, -2.6e5), P(0, 2.6e5), color=GREY_D, stroke_width=1))
        pts = VGroup(*[Dot(P(a_, a_ ** 3), radius=0.06, color=HEAD) for a_ in nums])
        tl = VGroup()
        for (a_, b_, c_), col in zip(d["triples"], (YES, LAM)):
            xs = sorted((a_, b_, c_))
            m = (xs[2] ** 3 - xs[0] ** 3) / (xs[2] - xs[0])
            k = xs[0] ** 3 - m * xs[0]
            lo, hi = xs[0] - 6, xs[2] + 6
            tl.add(VGroup(Line(P(lo, m * lo + k), P(hi, m * hi + k), color=col, stroke_width=2.5),
                          *[Dot(P(x, x ** 3), radius=0.09, color=col) for x in xs]))
        cap = label(r"the 14 numbers, \ lifted to $(a, a^3)$; \\ the axes are scaled differently, \ which keeps lines "
                    r"straight", font_size=18, color=GREY_A).next_to(axes, DOWN, buff=0.15)
        trip = r"; \ ".join(rf"${a_} + {b_} + {c_} = 0$".replace("+ -", "- ") for a_, b_, c_ in d["triples"])
        lines = VGroup(
            label(r"3SUM: \ do three of $n$ numbers sum to zero? \\ $O(n^2)$ is easy", font_size=22, color=WHITE),
            MathTex(r"a + b + c = 0 \iff (a, a^3),\ (b, b^3),\ (c, c^3) \text{ collinear}", font_size=28, color=LAM),
            label(rf"our 14 numbers: \ {trip}; \\ and exactly {len(d['collinear'])} collinear triples", font_size=21,
                  color=YES),
            label(r"Gajentaan and Overmars (1995): \ collinearity, \\ covering by strips, \ motion planning among "
                  r"segments, \\ \dots\ are all \textbf{3SUM-hard}", font_size=21, color=HEAD),
            label(r"the best algorithms save only logarithms \\ (Gr\o nlund and Pettie, 2014; \ Chan, 2018); \\ the "
                  r"conjecture: \ no $O(n^{2-\varepsilon})$ \ (Part 27)", font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        if lines.width > 6.6:
            lines.width = 6.6
            lines.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "The second front is a wall. <bookmark mark='a'/> The three-sum problem: given n numbers, do three of them "
            "add up to zero? Sorting and walking two pointers takes n squared. <bookmark mark='b'/> Now lift each "
            "number a to the point a, a cubed. Three numbers sum to zero exactly when their three points lie on one "
            "line; the algebra is a single factorization. <bookmark mark='c'/> We checked it on fourteen numbers: "
            "<bookmark mark='d'/> the two triples that sum to zero are exactly the two collinear triples. <bookmark "
            "mark='e'/> So collinearity is at least as hard as three-sum, and Anka Gajentaan and Mark Overmars "
            "showed in 1995 that a whole family of planar problems is: covering by strips, separating segments, "
            "motion planning among segments. <bookmark mark='f'/> The best three-sum algorithms beat n squared only "
            "by logarithmic factors, and the conjecture that nothing truly subquadratic exists has become a "
            "foundation of fine-grained complexity, which Part 27 builds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axes))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]), Create(cub))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x, scale=1.5) for x in pts], lag_ratio=0.1), FadeIn(cap))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]), LaggedStart(*[Create(t) for t in tl], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(lines[3]))
            vo.wait_until("f")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()

    def neighbours(self):
        head = label(r"Nearest neighbours: \ what is possible", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"exact search in high dimensions: \ cell-probe lower bounds suggest no index is both small and fast "
                  r"\\ (Barkol and Rabani; \ P\u{a}tra\c{s}cu and Thorup)", font_size=22, color=NO),
            label(r"$c$-approximate, \ by LSH: \ query time $n^{\rho}$ with $\rho = 1/c^2$ \ (Andoni and Indyk, "
                  r"2006), \\ optimal for hashing that ignores the data \ (O'Donnell, \ Wu and Zhou)", font_size=22,
                  color=LAM),
            label(r"look at the data first: \ $\rho = 1/(2c^2 - 1)$ \ (Andoni and Razenshteyn, 2015), \ and that "
                  r"is optimal too", font_size=22, color=YES),
            label(r"graphs like HNSW beat all of these in practice, \ with almost no theory: \\ Indyk and Xu (2023) "
                  r"found inputs where some take linear time", font_size=22, color=HEAD),
            label(r"guarantees exist for data of low \textbf{doubling dimension}, \ for some graph rules \ (DiskANN's)",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.34).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The third front is the one chapter twelve left open. <bookmark mark='a'/> For exact nearest neighbours in "
            "high dimensions, lower bounds in the cell-probe model suggest that no index can be both small and fast. "
            "<bookmark mark='b'/> For approximate ones there is a sharp theory. Locality-sensitive hashing answers a "
            "query for a c-approximate neighbour in time n to the one over c squared, and no hashing scheme that "
            "ignores the data can do better. <bookmark mark='c'/> Alexandr Andoni and Ilya Razenshteyn showed in 2015 "
            "that hashing adapted to the data does better, one over two c squared minus one, and that this too is "
            "optimal. <bookmark mark='d'/> Yet the graph indexes of chapter twelve beat every one of these methods "
            "in practice, with almost no theory behind them; Piotr Indyk and Haike Xu found inputs on which some "
            "popular graphs need linear time. <bookmark mark='e'/> Guarantees exist only for special data, of low "
            "doubling dimension, and special rules for building the graph."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def open_(self):
        head = label(r"Open questions", font_size=36).to_edge(UP, buff=0.4)
        qs = VGroup(
            label(r"3SUM in $O(n^{2 - \varepsilon})$ time, \ or a proof that it is impossible?", font_size=24,
                  color=NO),
            label(r"Hopcroft's problem: \ do any of $n$ points lie on any of $n$ lines? \ $O(n^{4/3})$ is known; \ "
                  r"is it optimal?", font_size=24, color=LAM),
            label(r"a provable query bound for HNSW-like graphs on real data, \ or inputs that defeat them", font_size=24,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(head, DOWN, buff=0.8)
        star = label(r"$\bigstar$ \ the part's research problem takes the third", font_size=22, color=GREY_A
                     ).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Here is where things stand. <bookmark mark='a'/> Can three-sum be solved in truly subquadratic time? "
            "<bookmark mark='b'/> Hopcroft's problem: given n points and n lines, does any point lie on any line? "
            "Jiří Matoušek's algorithm takes about n to the four thirds, and Jeff Erickson proved that bound optimal "
            "for a natural class of algorithms; for all algorithms, nobody knows. <bookmark mark='c'/> And why do "
            "navigable graphs work so well? A provable bound for HNSW-like graphs on realistic data, or a family of "
            "inputs that defeats them, is open. <bookmark mark='d'/> This part's research problem takes the third."
        ) as vo:
            self.play(FadeIn(head))
            for mk, q in zip("abc", qs):
                vo.wait_until(mk)
                self.play(FadeIn(q, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(star))
        self.wait(0.5)
        self.clear_scene()
