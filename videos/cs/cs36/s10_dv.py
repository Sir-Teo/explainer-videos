from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs36.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, graph, grid_table, load)

POS6 = {"u": [-5.4, 0.2, 0], "v": [-4.0, 1.5, 0], "x": [-4.0, -1.1, 0], "w": [-2.2, 1.5, 0], "y": [-2.2, -1.1, 0],
        "z": [-0.9, 0.2, 0]}


class Dv(VoiceoverScene):
    def construct(self):
        self.card()
        self.bellman_ford()
        self.count()
        self.fixes()
        self.ours()

    def card(self):
        card = chapter_card(9, r"Distance vector", r"Can routers find shortest paths by gossip?", lit=(1957, 1969, 1988),
                            extra=((1957, r"Bellman"), (1969, r"ARPANET routing"), (1988, r"RIP")), part=PART)
        with self.voiceover("Chapter nine. Distance vector."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def bellman_ford(self):
        d = load("dv")
        head = label(r"Bellman--Ford, \ distributed", font_size=36).to_edge(UP, buff=0.3)
        net = d["net"]
        edges = sorted({tuple(sorted((a, b))) for a in net for b in net[a]})
        g = graph(POS6, edges, weights={(a, b): net[a][b] for a, b in edges}, node_color=HEAD)
        eq = MathTex(r"D_x(y) = \min_{v} \big( c(x, v) + D_v(y) \big)", font_size=34, color=YES).move_to([3.4, 2.0, 0])
        hist = d["history"]
        tabs = []
        for k, t in enumerate(hist[: d["rounds"] + 2]):
            rows = [[y, ("$\\infty$" if t["u"][y][0] >= 99 else str(t["u"][y][0])), str(t["u"][y][1] or "--")]
                    for y in sorted(t["u"])]
            tb = grid_table([rf"$u$'s table, \ round {k}", r"cost", r"via"], rows, widths=[2.6, 1.2, 1.2], row_h=0.36,
                            font_size=18, mono_cols=())
            tb.move_to([3.4, -0.5, 0])
            tabs.append(tb)
        lines = VGroup(
            label(r"each router knows only its links; \ it sends its table, \ its \textit{distance vector}, \ to its "
                  r"neighbours", font_size=20, color=WHITE),
            label(rf"each recomputes from what it heard: \ the Bellman equation of Part 18; \ settled in "
                  rf"{d['rounds']} rounds, \ equal to Dijkstra's answer", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The oldest way to compute routes is to gossip. <bookmark mark='a'/> Each router knows only the cost "
            "of its own links. Periodically it sends its neighbours its current table of distances, its distance "
            "vector. <bookmark mark='b'/> Each router then recomputes: the best distance to y is the cheapest "
            "neighbour, counting the link to that neighbour plus the distance the neighbour claims. This is the "
            "Bellman equation of Part 18, solved by many machines at once. <bookmark mark='c'/> Here is router u's "
            "table, round by round. At first it knows only its neighbours. Each round, news travels one hop further, "
            "<bookmark mark='d'/> and after four rounds every table has settled on the true shortest distances, the "
            "same as Dijkstra computes on the whole map. The ARPANET routed this way from 1969, and RIP still does."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(eq))
            vo.wait_until("c")
            self.play(FadeIn(tabs[0]))
            for a, b in zip(tabs, tabs[1:]):
                self.play(ReplacementTransform(a, b), run_time=0.8)
                self.wait(0.4)
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def count(self):
        d = load("dv")
        head = label(r"Counting to infinity", font_size=36).to_edge(UP, buff=0.3)
        pos = {"A": [-4.5, 1.4, 0], "B": [-2.5, 1.4, 0], "C": [-0.5, 1.4, 0]}
        g = graph(pos, [("A", "B"), ("B", "C")], node_color=HEAD)
        cut = Cross(g.edges[("B", "C")], stroke_color=NO, stroke_width=4).scale(0.4)
        L = d["line"]["plain"]
        ax = Axes(x_range=[0, len(L["A"]), 2], y_range=[0, 16, 4], x_length=6.0, y_length=3.0,
                  axis_config={"color": GREY_D, "include_numbers": False}).move_to([3.2, 0.7, 0])
        ca = VMobject(color=DATA, stroke_width=3).set_points_as_corners([ax.c2p(i, v) for i, v in enumerate(L["A"])])
        cb = VMobject(color=KERN, stroke_width=3).set_points_as_corners([ax.c2p(i, v) for i, v in enumerate(L["B"])])
        yt = VGroup(*[label(str(v), font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.08)
                      for v in (4, 8, 12, 16)])
        lg = VGroup(label(r"A's distance to C", font_size=17, color=DATA), label(r"B's distance to C", font_size=17,
                                                                             color=KERN)).arrange(DOWN, aligned_edge=LEFT)
        lg.next_to(ax, UP, buff=0.1)
        xl = label(r"rounds after the cut", font_size=16, color=GREY_A).next_to(ax, DOWN, buff=0.1)
        lines = VGroup(
            label(r"the link B--C fails; \ B no longer reaches C directly", font_size=20, color=NO),
            label(r"but A still advertises ``C in 2'', \ so B believes it can go through A: \ 3; \ then A, \ through "
                  r"B: \ 4; \ and so on", font_size=20, color=WHITE),
            label(r"bad news travels slowly: \ they count up to the value called infinity, \ 16 in RIP, \ while "
                  r"packets loop between them", font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.4)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "Distance vector has a famous flaw. Take three routers in a line. <bookmark mark='a'/> The link from B to "
            "C fails. B knows at once that its direct route is gone. <bookmark mark='b'/> But A has been telling B, "
            "every round, that A can reach C at distance two. B does not know that A's route runs through B itself, "
            "so B concludes it can reach C through A, at three. Then A hears B say three, and updates to four. "
            "<bookmark mark='c'/> Good news spreads in a few rounds; bad news crawls, one step a round, while packets "
            "for C bounce between A and B. It ends only at the number the protocol calls infinity: sixteen, in RIP, "
            "which is why RIP networks are limited to fifteen hops."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(cut), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(yt), FadeIn(lg), FadeIn(xl), FadeIn(lines[1]))
            self.play(Create(ca), Create(cb), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def fixes(self):
        d = load("dv")
        head = label(r"Split horizon, \ and its limit", font_size=36).to_edge(UP, buff=0.3)
        rows = []
        for mode, name in (("plain", r"plain"), ("split", r"split horizon"), ("poison", r"poisoned reverse")):
            rows.append([name, str(d["line"][mode]["rounds"]), str(d["tri"][mode]["rounds"])])
        tab = grid_table([r"rounds to settle after a cut", r"a line, \ A--B--C", r"a triangle, \ A, B, C, then D"],
                         rows, widths=[4.4, 2.8, 3.6], row_h=0.44, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        for r in (2, 3):
            tab.cells[r][1].set_color(YES)
            tab.cells[r][2].set_color(NO)
        lines = VGroup(
            label(r"\textbf{split horizon}: \ never tell a neighbour about a route that goes through that neighbour",
                  font_size=20, color=YES),
            label(r"\textbf{poisoned reverse}: \ tell it, \ but as infinity", font_size=20, color=YES),
            label(r"both fix loops of two routers; \ with three, \ A and B still mislead each other through C's old "
                  r"news", font_size=20, color=NO),
            label(r"the real cure is to know more than a distance: \ the whole map \ (next chapter) \ or the whole "
                  r"path \ (BGP)", font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(tab, DOWN, buff=0.5)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        lines.set_x(0)
        with self.voiceover(
            "There are patches. <bookmark mark='a'/> Split horizon: never advertise a route to the neighbour you use "
            "for it. A would not tell B about C at all. <bookmark mark='b'/> Poisoned reverse: tell that neighbour the "
            "route is infinitely long. On the line, both settle in two rounds. <bookmark mark='c'/> But in a "
            "triangle feeding a fourth router, the loop has three members, and each can still learn the dead route "
            "from another: our simulation counts to infinity just as before, with either patch. "
            "<bookmark mark='d'/> The real cure is to give routers more than a number: the whole map, which is link "
            "state, or the whole path, which is BGP."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()


    def ours(self):
        d = load("dv_internet")
        head = label(r"Distance vector on our internet", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"converge from scratch", str(d["rounds"]), r"London $\rightarrow$ Frankfurt via Amsterdam, \ 6 ms"],
                [r"cut Amsterdam--Frankfurt, \ plain", str(d["plain"]["rounds"]), r"via Paris, \ 6 ms: \ an equal path existed"],
                [r"the same, \ split horizon", str(d["split"]["rounds"]), r"Amsterdam briefly has no route, \ then 9 ms"]]
        tab = grid_table([r"eight routers, \ costs in ms", r"rounds", r"result"], rows, widths=[4.4, 1.3, 6.0], row_h=0.46,
                         font_size=19, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        for r in range(1, 4):
            tab.cells[r][1].set_color(YES)
        lines = VGroup(
            label(r"with a good alternative, \ bad news is overtaken by good news, \ and distance vector settles in a "
                  r"few rounds", font_size=20, color=YES),
            label(r"the count to infinity needs a destination that is cut off, \ or an alternative much longer than the "
                  r"lost route", font_size=20, color=NO),
            label(r"the same answer as Dijkstra's, \ computed with no router ever seeing the map", font_size=20,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(tab, DOWN, buff=0.5)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        lines.set_x(0)
        with self.voiceover(
            "How does distance vector do on our eight-city internet? <bookmark mark='a'/> From empty tables it "
            "converges in four rounds, the hop count of the longest shortest path. <bookmark mark='b'/> Now cut the "
            "cable from Amsterdam to Frankfurt. London's route had used it; but a path through Paris costs exactly "
            "the same, and the tables settle in three rounds. With split horizon, Amsterdam has no route at all for "
            "a round, then finds the nine-millisecond one through London and Paris. <bookmark mark='c'/> When a good "
            "alternative exists, its good news overtakes the bad. The count to infinity needs a destination that is "
            "really cut off, or an alternative far longer than what was lost. <bookmark mark='d'/> And every answer "
            "matches Dijkstra's, computed without any router ever seeing the map."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab.cells[0][0]), FadeIn(tab.cells[0][1]), FadeIn(tab.cells[0][2]), FadeIn(tab.rule),
                      *[FadeIn(c) for c in tab.cells[1]])
            vo.wait_until("b")
            self.play(*[FadeIn(c) for c in tab.cells[2] + tab.cells[3]])
            vo.wait_until("c")
            self.play(FadeIn(lines[0]), FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()


_ = (LAM,)
