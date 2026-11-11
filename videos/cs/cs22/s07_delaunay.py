from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.algo import geometry as G
from videos.cs.cs22.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, fit, grid_table, load, mono, words)


def edges_of(tris):
    out = set()
    for t in tris:
        a, b, c = t
        out |= {frozenset((a, b)), frozenset((b, c)), frozenset((a, c))}
    return out


class Delaunay(VoiceoverScene):
    def construct(self):
        self.card()
        self.empty_circles()
        self.flips()
        self.uses()
        self.emst()

    def card(self):
        card = chapter_card(6, r"Delaunay triangulations", r"Which triangulation is the best?", lit=(1934, 1977),
                            extra=((1934, r"Delaunay"), (1977, r"Lawson's flips")), part=PART)
        with self.voiceover("Chapter six. Delaunay triangulations."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def empty_circles(self):
        d = load("voronoi")
        sites = [tuple(s) for s in d["sites"]]
        tris = [tuple(t) for t in d["tris"]]
        f, s = fit(sites, center=LEFT * 2.2 + DOWN * 0.3, w=8.0, h=5.0)
        head = label(r"The empty-circle triangulation", font_size=34).to_edge(UP, buff=0.3)
        sd = VGroup(*[Dot(f(p), radius=0.07, color=HEAD) for p in sites])
        E = VGroup(*[Line(f(sites[min(e)]), f(sites[max(e)]), color=YES, stroke_width=2.2) for e in edges_of(tris)])
        circles = VGroup()
        cc = sorted((G._circumcircle(*[sites[i] for i in t]) for t in tris), key=lambda c: c[2])
        for ux, uy, r in cc[2:len(cc) // 2:max(1, len(cc) // 10)][:4]:
            circles.add(Circle(radius=r * s, color=LAM, stroke_width=1.8).move_to(f((ux, uy))))
        from videos.cs.cs22.s06_voronoi import voronoi_edges
        V = VGroup(*[DashedLine(f(a), f(b), color=DATA, stroke_width=1.6, dash_length=0.08)
                     for a, b, _ in voronoi_edges(sites, tris)
                     if max(abs(a[0]), abs(b[0])) < 7 and max(abs(a[1]), abs(b[1])) < 4])
        side = VGroup(
            label(r"Delaunay (1934): \ join three sites \\ when the circle through them \\ is \textbf{empty}",
                  font_size=22, color=YES),
            label(r"the triangles of the Voronoi vertices: \\ the two diagrams are \textbf{dual}", font_size=22,
                  color=DATA),
            label(r"the in-circle test decides it:", font_size=22, color=WHITE),
            MathTex(r"\det\begin{pmatrix} a_x - d_x & a_y - d_y & |a - d|^2 \\ b_x - d_x & b_y - d_y & |b - d|^2 \\ "
                    r"c_x - d_x & c_y - d_y & |c - d|^2 \end{pmatrix} > 0", font_size=26, color=LAM),
            label(r"$d$ inside the circle of $abc$ \ (counter-clockwise)", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        if side.width > 5.0:
            side.width = 5.0
            side.to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Connect the sites with triangles. There are many ways; which is best? <bookmark mark='a'/> Boris "
            "Delaunay's answer, from 1934: join three sites whenever the circle through them has no other site "
            "inside. <bookmark mark='b'/> Those circles are exactly the empty circles of the Voronoi vertices, so the "
            "Delaunay triangulation is the Voronoi diagram's dual: an edge for every pair of neighbouring regions. "
            "<bookmark mark='c'/> Whether a point lies inside a circle through three others is decided by a sign, "
            "the in-circle test, a three by three determinant with squared distances in its last column. Like the "
            "orientation test, it can be made exact."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sd))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(e) for e in E], lag_ratio=0.03), FadeIn(side[0]), run_time=2.0)
            self.play(LaggedStart(*[Create(c) for c in circles], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeOut(circles), LaggedStart(*[Create(v) for v in V], lag_ratio=0.03), FadeIn(side[1]),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()

    def flips(self):
        d = load("delaunay")
        P = [tuple(p) for p in d["P"]]
        f, s = fit(P, center=LEFT * 2.6 + DOWN * 0.35, w=7.0, h=5.6)
        head = label(r"Lawson's flips", font_size=34).to_edge(UP, buff=0.3)
        sd = VGroup(*[Dot(f(p), radius=0.07, color=HEAD) for p in P])
        lines = {}
        for e in edges_of([tuple(t) for t in d["T0"]]):
            a, b = sorted(e)
            lines[e] = Line(f(P[a]), f(P[b]), color=GREY_B, stroke_width=2)
        side = VGroup(
            label(r"start from any triangulation: \\ here, \ a sweep from left to right", font_size=22, color=WHITE),
            label(rf"smallest angle: \ {d['min0']:.2f}$^\circ$", font_size=22, color=NO),
            label(r"an edge is \textbf{illegal} if the opposite corner \\ lies inside the triangle's circle: \ "
                  r"\textbf{flip} it", font_size=22, color=LAM),
            label(rf"{d['flips']} flips later, \ none is illegal: \\ the Delaunay triangulation", font_size=22,
                  color=YES),
            label(rf"smallest angle: \ {d['min1']:.2f}$^\circ$, \ the largest possible \\ (Sibson, 1978)", font_size=22,
                  color=YES),
            label(r"why it stops: \ every flip lowers the surface \\ of chapter 7's lifted triangles", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.4)
        if side.width > 5.6:
            side.width = 5.6
            side.to_edge(RIGHT, buff=0.4)
        seq = d["seq"]
        a0, b0, c0, d0 = seq[0]
        ux, uy, r = G._circumcircle(P[a0], P[b0], P[c0])
        bad = Circle(radius=r * s, color=NO, stroke_width=2).move_to(f((ux, uy)))
        with self.voiceover(
            "How do we find it? Charles Lawson's method, from 1977, starts from any triangulation at all. <bookmark "
            "mark='a'/> This one connects the points as a sweep from left to right meets them, and it is full of "
            "slivers: <bookmark mark='b'/> its thinnest angle is under half a degree. <bookmark mark='c'/> Look at "
            "two triangles sharing an edge. If the far corner of one lies inside the circle of the other, the edge "
            "is illegal; flip it, replacing it with the other diagonal of the quadrilateral. Repeat. <bookmark "
            "mark='d'/> Seventeen flips later no edge is illegal, and what is left is the Delaunay triangulation. "
            "<bookmark mark='e'/> Its smallest angle has grown tenfold, and Robin Sibson proved that among all "
            "triangulations of the points, Delaunay's maximizes the smallest angle. <bookmark mark='f'/> Why does "
            "flipping ever stop? The next chapter will show that each flip pushes down a surface in three dimensions, "
            "which cannot go down forever."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sd))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(x) for x in lines.values()], lag_ratio=0.03), FadeIn(side[0]),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Create(bad), Indicate(lines[frozenset((a0, b0))], color=NO))
            self.play(FadeOut(bad))
            vo.wait_until("d")
            for a, b, c, dd in seq:
                old = lines.pop(frozenset((a, b)))
                new = Line(f(P[c]), f(P[dd]), color=YES, stroke_width=2.4)
                lines[frozenset((c, dd))] = new
                self.play(old.animate.set_color(NO), run_time=0.1)
                self.play(ReplacementTransform(old, new), run_time=0.15)
            self.play(FadeIn(side[3]), *[x.animate.set_color(YES) for x in lines.values()])
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.wait(0.3)
        self.clear_scene()

    def uses(self):
        head = label(r"What the empty circles buy", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label('mesh refinement adds sites; \\ angle guarantees require input-angle assumptions \\ (Ruppert, 1995)', font_size=22, color=YES),
            label(r"terrain models from scattered heights \ (TINs); \ interpolation by natural neighbours", font_size=22,
                  color=DATA),
            label(r"every point's nearest neighbour, \ and every edge of the minimum spanning tree, \ is a Delaunay edge",
                  font_size=22, color=LAM),
            label(r"$O(n \log n)$ to build: \ by Fortune's sweep, \ by divide and conquer \ (Guibas and Stolfi, 1985), "
                  r"\ or by inserting points at random \ (chapter 8)", font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.34).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "The empty-circle property has useful consequences. <bookmark mark='a'/> Delaunay refinement adds sites to improve simulation meshes. Ruppert's quality and termination guarantees require assumptions about the input geometry; a small required input angle cannot simply be erased. <bookmark mark='b'/> Terrain triangulations and natural-neighbour interpolation use related constructions. <bookmark mark='c'/> In general position, nearest-neighbour edges and the Euclidean minimum spanning tree lie in the Delaunay graph. We check spanning-tree weights next. <bookmark mark='e'/> Sweeps, divide and conquer, and randomized insertion with suitable point location achieve n log n bounds in their arithmetic models. Our walking locator is a simpler implementation and does not acquire that guarantee merely by shuffling."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abce", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def emst(self):
        d = load("emst")
        P = [tuple(p) for p in d["P"]]
        f, s = fit(P, center=LEFT * 4.0 + DOWN * 0.35, w=5.2, h=5.6)
        head = label(r"The minimum spanning tree lives in the triangulation", font_size=30).to_edge(UP, buff=0.3)
        sd = VGroup(*[Dot(f(p), radius=0.05, color=HEAD) for p in P])
        D = VGroup(*[Line(f(P[int(a)]), f(P[int(b)]), color=GREY_D, stroke_width=1.2) for a, b in d["delaunay"]])
        T = VGroup(*[Line(f(P[int(a)]), f(P[int(b)]), color=YES, stroke_width=3) for a, b in d["mst"]])
        rows = [[words(r["n"]), words(r["delaunay_edges"]), words(r["pairs"]), r"yes" if r["same"] else r"NO",
                 f"{r['t_delaunay']:.2f} s", f"{r['t_prim']:.2f} s"] for r in d["rows"]]
        tab = grid_table([r"points", r"Delaunay edges", r"all pairs", 'same weight', r"via Delaunay", r"Prim"],
                         rows, widths=[1.2, 1.8, 1.9, 1.3, 1.6, 1.0], row_h=0.44, font_size=20, mono_cols=(),
                         colors=[[WHITE, YES, NO, YES, YES, GREY_A]] * len(rows))
        side = VGroup(
            label(r"if an MST edge $ab$ were not Delaunay, \\ some point inside the circle on $ab$ \\ would give "
                  r"a shorter swap", font_size=21, color=WHITE),
            tab,
            label(r"Kruskal over $3n$ edges instead of $n^2/2$: \\ $O(n \log n)$ in all \ (Shamos and Hoey, 1975)",
                  font_size=21, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        if side.width > 7.2:
            side.width = 7.2
        side.to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "Here are seventy points, their Delaunay edges, and a minimum spanning tree. <bookmark mark='a'/> Every green edge is present in the triangulation. <bookmark mark='b'/> Remove an MST edge a b and consider its cut. Any site inside the disk with diameter a b is closer to both ends. Joining that site to the endpoint on the other side gives a shorter crossing edge, contradicting minimality. Thus the diameter disk is empty and the edge is Delaunay. <bookmark mark='c'/> Kruskal can search the linear-sized Delaunay graph. For every displayed size, including eight thousand points, we independently run complete-graph Prim after timing and compare total weights within a declared numerical tolerance. Equal weights certify these numerical results; they need not identify a unique tree when ties occur. The two timing columns are separate host measurements."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sd))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(x) for x in D], lag_ratio=0.01), run_time=1.0)
            self.play(LaggedStart(*[Create(x) for x in T], lag_ratio=0.03), run_time=1.3)
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()
