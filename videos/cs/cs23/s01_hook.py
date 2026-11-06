from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs23.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, View3, grid_table, load, mono, words)


class Hook(VoiceoverScene):
    def construct(self):
        self.diet()
        self.three()
        self.plan()

    def diet(self):
        head = label(r"The cheapest diet, \ 1945", font_size=36).to_edge(UP, buff=0.4)
        rows = VGroup(
            label(r"George Stigler: \ 77 foods, \ 9 nutrients, \ the cheapest year that keeps a person healthy",
                  font_size=24, color=WHITE),
            label(r"by trial and insight: \ \$39.93 a year \ (1939 prices)", font_size=24, color=HEAD),
            label(r"1947: \ Dantzig's new simplex method, \ worked by Jack Laderman's team on desk calculators", font_size=24,
                  color=DATA),
            label(r"about 120 person-days of arithmetic: \ \$39.69, \ and a \textbf{proof} that nothing is cheaper",
                  font_size=24, color=YES),
            label(r"today the same problem solves in milliseconds; \ the proof is the part that lasts", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.42).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "In 1945 the economist George Stigler asked what it costs, at the least, to feed a person for a year. He "
            "had seventy-seven foods and nine nutrients, and a person needs enough of each. <bookmark mark='a'/> By "
            "trial and insight he found a diet costing thirty-nine dollars and ninety-three cents a year, at 1939 "
            "prices, mostly wheat flour, cabbage and evaporated milk. He wrote that there was no direct way to find "
            "the true minimum. <bookmark mark='b'/> Two years later George Dantzig invented one. Jack Laderman's "
            "team worked his simplex method by hand on desk calculators, <bookmark mark='c'/> roughly a hundred and "
            "twenty person-days of arithmetic, and found thirty-nine sixty-nine. And it came with something Stigler "
            "could not have: a proof that no diet is cheaper. <bookmark mark='d'/> That proof, which this part calls "
            "duality, is the idea that lasts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            for mk, r in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def three(self):
        d = load("lp")
        ts = load("tsp")
        on = load("online")
        head = label(r"Three kinds of answer", font_size=36).to_edge(UP, buff=0.35)
        view = View3(origin=LEFT * 4.6 + DOWN * 1.1, scale=0.62, th=-0.7, ph=0.55, center=(1.2, 1.2, 1.2))
        poly = view.polytope(d["vertices"], d["faces"], color=DATA, opacity=0.25)
        opt = Dot(view.p(d["opt"]), radius=0.1, color=HEAD)
        P = ts["draw"]["P"]
        sc = 0.42
        o2 = np.array([-0.9, -1.6, 0])

        def T(p):
            return o2 + np.array([p[0] * sc, p[1] * sc, 0])
        cities = VGroup(*[Dot(T(p), radius=0.045, color=WHITE) for p in P])
        tour = ts["draw"]["tour"]
        route = Polygon(*[T(P[i]) for i in tour], color=YES, stroke_width=2.5)
        r = on["rows"][2]
        bars = VGroup()
        for k, (nm, v, col) in enumerate((("LRU", r["lru"], DATA), ("OPT", r["opt"], YES))):
            h = 2.2 * v / r["lru"]
            b = Rectangle(width=0.55, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([3.6 + k * 1.0, -2.2 + h / 2, 0])
            bars.add(VGroup(b, label(nm, font_size=18, color=col).next_to(b, DOWN, buff=0.1)))
        caps = VGroup(
            label(rf"a linear program: \\ optimum {d['opt_value']:.0f}, \\ \textbf{{proved}} optimal", font_size=21,
                  color=DATA).move_to(LEFT * 4.6 + UP * 1.5),
            label(rf"the salesman's 13 cities: \\ hard in general, \\ but heuristics within a few percent",
                  font_size=21, color=YES).move_to(LEFT * 0.2 + UP * 1.5),
            label(rf"a cache that can't see the future: \\ LRU's faults against \\ the clairvoyant optimum", font_size=21,
                  color=HEAD).move_to(RIGHT * 4.1 + UP * 1.5),
        )
        with self.voiceover(
            "This part is about choosing the best, and about the three kinds of answer we can get. <bookmark "
            "mark='a'/> For linear programs, the best point of a polytope, there are fast algorithms and exact answers "
            "that come with a proof. <bookmark mark='b'/> For problems with integer choices, like the travelling "
            "salesman, the exact answer is NP-hard; we settle for algorithms with proven guarantees, and heuristics "
            "that do better than the guarantees promise. <bookmark mark='c'/> And for decisions made without seeing "
            "the future, like which page to evict from a cache, we measure ourselves against a clairvoyant who sees "
            "everything, and prove we are never too far behind."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(poly), FadeIn(opt, scale=1.5), FadeIn(caps[0]))
            vo.wait_until("b")
            self.play(FadeIn(cities), Create(route), FadeIn(caps[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), FadeIn(caps[2]))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Optimization", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"linear programs, \ the simplex method, \ and duality's certificates",
            r"why simplex is exponential in theory and fast in practice; \ ellipsoids and interior points",
            r"integer programs: \ totally unimodular matrices, \ branch and bound",
            r"approximation: \ covers, \ the travelling salesman, \ knapsack, \ and MAX-CUT by a random hyperplane",
            r"online algorithms and multiplicative weights",
            r"convex optimization in a page; \ the frontier: \ faster LPs, \ the Hirsch question, \ the UGC",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "Part 23 of Computer Science, Built: Optimization. <bookmark mark='a'/> In this part: linear programs, "
            "the simplex method and duality; why simplex is exponential in theory and fast in practice, and the "
            "polynomial methods that came after it; integer programs and when they are easy; approximation "
            "algorithms for covers, the travelling salesman, knapsack and MAX-CUT; online algorithms and "
            "multiplicative weights; and convex optimization in a page."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
