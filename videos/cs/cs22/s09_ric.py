from __future__ import annotations

import random

from explainer.cs import *  # noqa: F403
from explainer.cs.algo import geometry as G
from videos.cs.cs22.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, fit, grid_table, load, mono, words)


class Incremental(VoiceoverScene):
    def construct(self):
        self.card()
        self.insertion()
        self.backwards()
        self.measured()

    def card(self):
        card = chapter_card(8, r"Random order \ and backwards analysis", r"Why insert the points in random order?",
                            lit=(1989, 1993), extra=((1989, r"Clarkson--Shor"), (1993, r"Seidel's backwards analysis")),
                            part=PART)
        with self.voiceover("Chapter eight. Random order and backwards analysis."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def insertion(self):
        rng = random.Random(8)
        P = [(rng.randint(0, 1000), rng.randint(0, 700)) for _ in range(16)]
        p = (480, 340)
        before = G.delaunay(P, seed=1).triangles()
        after = G.delaunay(P + [p], seed=1).triangles()
        k = len(P)
        conflict = [t for t in before if G.incircle_exact(*_ccw([P[i] for i in t]), p) > 0]
        new = [t for t in after if k in t]
        Q = P + [p]
        f, s = fit(Q, center=LEFT * 2.6 + DOWN * 0.3, w=7.4, h=5.4)
        head = label(r"Inserting one point", font_size=34).to_edge(UP, buff=0.3)
        sd = VGroup(*[Dot(f(q), radius=0.065, color=HEAD) for q in P])
        T0 = VGroup(*[Polygon(*[f(P[i]) for i in t], color=YES, stroke_width=1.8) for t in before])
        pd = Dot(f(p), radius=0.09, color=NO)
        bad = VGroup(*[Polygon(*[f(P[i]) for i in t], color=NO, stroke_width=2.2).set_fill(NO, 0.3) for t in conflict])
        circles = VGroup()
        for t in conflict[:3]:
            ux, uy, r = G._circumcircle(*[P[i] for i in t])
            circles.add(Circle(radius=r * s, color=NO, stroke_width=1.4, stroke_opacity=0.7).move_to(f((ux, uy))))
        newt = VGroup(*[Polygon(*[f(Q[i]) for i in t], color=LAM, stroke_width=2.2).set_fill(LAM, 0.25) for t in new])
        side = VGroup(
            label(r"find the triangle containing the new point", font_size=22, color=WHITE),
            label(rf"its \textbf{{conflicts}}: \ the triangles whose circles contain it \ ({len(conflict)} here)",
                  font_size=22, color=NO),
            label(r"remove them, \ and join the new point to the hole's corners", font_size=22, color=LAM),
            label(rf"new triangles $=$ the new point's degree \ ({len(new)})", font_size=22, color=YES),
            label(r"(flipping from the containing triangle does the same thing, \\ one edge at a time)", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        if side.width > 5.6:
            side.width = 5.6
            side.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The simplest way to build a Delaunay triangulation is to add the points one at a time. <bookmark "
            "mark='a'/> Here is a triangulation, and a new point to insert. First find the triangle that contains "
            "it. <bookmark mark='b'/> Then find every triangle whose empty circle the new point spoils, the "
            "triangles in conflict with it. <bookmark mark='c'/> Remove them all, leaving a hole shaped like a star "
            "around the new point, and join the new point to every corner of the hole. <bookmark mark='d'/> The "
            "number of new triangles is the new point's degree. <bookmark mark='e'/> Lawson's flips, starting "
            "from the triangle that contains the point, carry out exactly this change one edge at a time. The "
            "question is what the whole sequence of insertions costs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sd), FadeIn(T0))
            vo.wait_until("a")
            self.play(FadeIn(pd, scale=1.6), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bad), FadeIn(side[1]), LaggedStart(*[Create(c) for c in circles], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeOut(circles), FadeOut(bad), *[T0[before.index(t)].animate.set_stroke(opacity=0.0)
                                                         for t in conflict], FadeIn(side[2]))
            self.play(LaggedStart(*[FadeIn(t) for t in newt], lag_ratio=0.15), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Indicate(pd, color=NO))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()

    def backwards(self):
        head = label(r"Backwards analysis", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"in a bad order, \ each new point can have degree $\Theta(i)$: \ $\Theta(n^2)$ in all", font_size=22,
                  color=NO),
            label(r"in a \textbf{random} order, \ run the algorithm \textbf{backwards}: \ the $i$-th point is a random "
                  r"one of the $i$ present", font_size=22, color=WHITE),
            MathTex(r"\mathbb{E}[\deg] = \frac{1}{i} \sum_{q} \deg(q) \;=\; \frac{2\,|E|}{i} \;\le\; "
                    r"\frac{2\,(3i - 6)}{i} \;<\; 6", font_size=34, color=YES),
            label(r"Euler: \ a planar triangulation with $i$ vertices has at most $3i - 6$ edges", font_size=21,
                  color=GREY_A),
            label(r"so each insertion makes fewer than 6 new triangles on average, \ $O(n)$ in all \ "
                  r"(at most $9n + 1$, \ counting flips)", font_size=22, color=YES),
            label(r"locating points: \ $O(n \log n)$ expected, \ by the same argument over \textit{conflict lists} \ "
                  r"(Clarkson and Shor, 1989)", font_size=22, color=LAM),
            label(r"Seidel (1993) named the trick; \ it prices quicksort, \ treaps and chapter 9's LP the same way",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "In a bad order, a single insertion can change almost everything: a point can arrive connected to all i "
            "points before it, and the total becomes quadratic. <bookmark mark='a'/> In a random order, a beautiful "
            "argument shows it cannot. <bookmark mark='b'/> Run the algorithm backwards. Look at the triangulation "
            "after i insertions. Because the order is random, the point inserted last is equally likely to be any of "
            "the i points present. <bookmark mark='c'/> Its expected degree is the average degree of the "
            "triangulation, twice the number of edges over i, <bookmark mark='d'/> and Euler's formula says a planar "
            "triangulation has fewer than three i edges. <bookmark mark='e'/> So the average degree is below six, and "
            "each insertion creates fewer than six new triangles on average, whatever the points. <bookmark "
            "mark='f'/> Finding where each point goes costs n log n in expectation, by the same argument applied to "
            "lists of conflicts, which Kenneth Clarkson and Peter Shor introduced in 1989. <bookmark mark='g'/> "
            "Raimund Seidel named the trick backwards analysis. It prices randomized quicksort, treaps and the "
            "linear programming of the next chapter in exactly the same way."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("delaunay")
        head = label(r"Measured: \ random order against a bad one", font_size=32).to_edge(UP, buff=0.35)
        rnd = [r for r in d["rows"] if r["order"] == "random"]
        adv = [r for r in d["rows"] if r["order"] == "adversarial"]
        t1 = grid_table([r"random points $n$", r"triangles made", r"per point", r"flips per point"],
                        [[words(r["n"]), words(r["created"]), f"{r['created'] / r['n']:.2f}", f"{r['flips'] / r['n']:.2f}"]
                         for r in rnd], widths=[2.6, 2.4, 1.8, 2.4], row_h=0.46, font_size=21, mono_cols=(),
                        colors=[[WHITE, DATA, YES, LAM]] * len(rnd))
        t2 = grid_table([r"bad set $n$", r"made, \ in its bad order", r"per point", r"made, \ shuffled", r"per point"],
                        [[words(r["n"]), words(r["created"]), f"{r['created'] / r['n']:.0f}", words(r["created_random"]),
                          f"{r['created_random'] / r['n']:.2f}"] for r in adv], widths=[1.9, 3.2, 1.6, 2.6, 1.6],
                        row_h=0.46, font_size=21, mono_cols=(), colors=[[WHITE, NO, NO, YES, YES]] * len(adv))
        VGroup(t1, t2).arrange(DOWN, buff=0.55).next_to(head, DOWN, buff=0.4)
        t1.set_x(0)
        t2.set_x(0)
        note = label(r"the bad set: \ a flat convex chain, \ then points above its middle inserted from the top down: "
                     r"\ each new one is joined to the whole chain", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "We counted the triangles our incremental algorithm creates. <bookmark mark='a'/> On random points, "
            "inserted in random order, it is about nine per point at every size, just under the bound of nine n "
            "plus one, with about three flips per point. <bookmark mark='b'/> Then a set built to be bad: a long, "
            "nearly flat convex chain, followed by points above its middle, inserted from the top down, so that each "
            "new point is joined to the whole chain. In that order the work grows quadratically: for sixteen hundred "
            "points, eight hundred and seventy thousand triangles. <bookmark mark='c'/> Shuffle the same points, and "
            "it is thirteen thousand again, eight per point. The shuffle costs one line of code, and the guarantee "
            "holds for every input."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*t1.cells[0])), FadeIn(t1.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in t1.cells[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*t2.cells[0])), FadeIn(t2.rule), FadeIn(note),
                      LaggedStart(*[FadeIn(VGroup(*r[:3])) for r in t2.cells[1:]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*r[3:])) for r in t2.cells[1:]], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()


def _ccw(T):
    a, b, c = T
    if G.orient_int(a, b, c) < 0:
        return a, c, b
    return a, b, c
