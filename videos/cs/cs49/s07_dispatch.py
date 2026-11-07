from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs49.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, bar_chart, load, module_box)


def hex_grid(cols=7, rows=5, r=0.46, center=ORIGIN):
    """A flat-topped hexagonal grid (odd columns shifted down half a cell); returns (VGroup, centres)."""
    cells, cs = VGroup(), []
    for c in range(cols):
        for k in range(rows):
            x = c * 1.5 * r
            y = -k * math.sqrt(3) * r - (c % 2) * math.sqrt(3) / 2 * r
            cells.add(RegularPolygon(n=6, radius=r, stroke_color=GREY_D, stroke_width=1.5, fill_color=BG,
                                     fill_opacity=1).move_to([x, y, 0]))
            cs.append(np.array([x, y, 0.0]))
    shift = np.array(center) - cells.get_center()
    cells.shift(shift)
    return cells, [p + shift for p in cs]


class Dispatch(VoiceoverScene):
    def construct(self):
        self.card()
        self.locations()
        self.design()
        self.matching()
        self.eta()
        self.surge()

    def card(self):
        card = chapter_card(6, r"Ride-hailing dispatch", r"Which driver should fetch which rider?",
                            lit=(1955, 2008), extra=((1955, r"Kuhn: \ the Hungarian method"),
                                                     (2008, r"Geisberger et al.: \ contraction hierarchies")),
                            part=PART)
        with self.voiceover("Chapter six. Ride-hailing dispatch."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def locations(self):
        head = label(r"Where is every driver?", font_size=36).to_edge(UP, buff=0.3)
        r = 0.46
        cells, cs = hex_grid(7, 6, r, center=[-3.4, -0.35, 0])
        rng = np.random.default_rng(7)
        picks = rng.choice(len(cs), size=13, replace=False)
        drivers = VGroup(*[Dot(cs[i] + np.array([*rng.uniform(-0.18, 0.18, 2), 0]), radius=0.07, color=DATA)
                           for i in picks])
        rider_cell = int(np.argmin([np.linalg.norm(p - np.array([-3.2, -0.4, 0])) for p in cs]))
        ring = [i for i, p in enumerate(cs) if np.linalg.norm(p - cs[rider_cell]) < 1.05 * math.sqrt(3) * r]
        rider = Star(n=5, outer_radius=0.16, color=HEAD, fill_opacity=1).move_to(cs[rider_cell])
        ill = note(r"drivers illustrative", font_size=16).next_to(cells, DOWN, buff=0.12)
        rows = VGroup(
            wrapped_label(r"say a million drivers online, \ each reporting every 4 seconds: \ \textbf{250{,}000 "
                          r"writes a second}, \ about 25 MB/s at 100 bytes a ping \ (illustrative)", 5.4,
                          font_size=19, color=WHITE),
            wrapped_label(r"keep only the latest position, \ keyed by its cell: \ an in-memory map with a TTL, \ "
                          r"not a database of history \ (that goes to the log, \ Part 46)", 5.4, font_size=19,
                          color=DATA),
            wrapped_label(r"hexagonal cells \ (Uber's H3, \ Part 48): \ all six neighbours are the same distance "
                          r"away, \ so ``near the rider'' is the rider's cell and the ring around it", 5.4,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.7, -0.2, 0])
        with self.voiceover(
            "A dispatcher must know where every driver is, all the time. <bookmark mark='a'/> Say a million drivers "
            "are online, each phone reporting its position every four seconds: that is two hundred and fifty "
            "thousand writes a second, each one replacing the last. <bookmark mark='b'/> So the hot store keeps "
            "only each driver's latest position, in "
            "memory, indexed by map cell, and lets stale entries expire; the history goes "
            "to a log, as in Part 46. <bookmark mark='c'/> The cells are hexagons, as in Uber's H3 index from Part "
            "48. A hexagon's six neighbours are all the same distance away, so the drivers near a rider are simply "
            "those in the rider's cell and the ring around it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(drivers), FadeIn(rows[0]))
            moved = [d.get_center() + np.array([*rng.uniform(-0.3, 0.3, 2), 0]) for d in drivers]
            self.play(*[d.animate.move_to(p) for d, p in zip(drivers, moved)], run_time=1.5)
            vo.wait_until("b")
            lit = []
            for d in drivers:
                k = int(np.argmin([np.linalg.norm(p - d.get_center()) for p in cs]))
                lit.append(k)
            self.play(*[cells[k].animate.set_fill(DATA, opacity=0.25) for k in set(lit)], FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(*[cells[k].animate.set_fill(BG, opacity=1) for k in set(lit)], FadeIn(rider))
            self.play(*[cells[k].animate.set_fill(HEAD, opacity=0.3) for k in ring], FadeIn(rows[2]))
            near = [d for d, k in zip(drivers, lit) if k in ring]
            if near:
                self.play(*[Indicate(d, color=YES, scale_factor=1.8) for d in near])
        self.wait(0.4)
        self.clear_scene()

    def design(self):
        head = label(r"The design", font_size=36).to_edge(UP, buff=0.3)
        rider = module_box(r"rider app", HEAD, w=2.0, h=0.7).move_to([-5.6, 1.3, 0])
        driver = module_box(r"driver apps", DATA, w=2.0, h=0.7).move_to([-5.6, -1.3, 0])
        gate_r = RoundedRectangle(width=1.3, height=3.3, corner_radius=0.1, stroke_color=KERN, stroke_width=2,
                                  fill_color=KERN, fill_opacity=0.12).move_to([-2.7, 0, 0])
        gate = VGroup(gate_r, label(r"connection gateway", font_size=18, color=WHITE).rotate(PI / 2).move_to(gate_r))
        disp = module_box(r"dispatch", YES, w=2.2, h=0.75).move_to([0.5, 1.3, 0])
        loc = module_box(r"location service", DATA, w=2.6, h=0.75).move_to([0.5, -1.3, 0])
        eta = module_box(r"ETA \ (road graph)", LAM, w=2.4, h=0.75).move_to([4.3, 1.95, 0])
        geo = module_box(r"geo index \ (latest, \ by cell)", DATA, w=2.9, h=0.75).move_to([4.3, -0.2, 0])
        boxes = VGroup(rider, driver, gate, disp, loc, eta, geo)

        def arr(a, b, double=False):
            cls = DoubleArrow if double else Arrow
            return cls(a, b, buff=0.08, color=GREY_C, stroke_width=2, tip_length=0.15)
        links = VGroup(arr(rider.get_right(), gate[0].get_left() + UP * 1.3, True),
                       arr(driver.get_right(), gate[0].get_left() + DOWN * 1.3, True),
                       arr(gate[0].get_right() + UP * 1.3, disp.get_left(), True),
                       arr(gate[0].get_right() + DOWN * 1.3, loc.get_left()),
                       arr(loc.get_right(), geo.get_left() + DOWN * 0.2),
                       arr(disp.get_right() + DOWN * 0.2, geo.get_left() + UP * 0.2, True),
                       arr(disp.get_right() + UP * 0.2, eta.get_left(), True))
        notes = VGroup(
            wrapped_label(r"write path: \ pings stream in through the gateway and overwrite the geo index", 12.4,
                          font_size=19, color=DATA),
            wrapped_label(r"read path: \ a request asks the index for nearby drivers, \ the ETA service ranks them by "
                          r"driving time, \ and an offer goes out over the driver's open connection \ (Part 48's "
                          r"real-time block)", 12.4, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        with self.voiceover(
            "Here is the whole service. <bookmark mark='a'/> Phones keep a connection open to a gateway, the same "
            "connection servers as the chat of Chapter 4. <bookmark mark='b'/> On the write path, drivers' pings "
            "flow through a location service that overwrites each driver's entry in the geo index. "
            "<bookmark mark='c'/> On the read path, a rider's request reaches dispatch, which asks the index for the "
            "drivers in the nearby cells, ranks them by driving time from the ETA service, and sends "
            "the chosen driver an offer over the connection that driver already has open. If the driver declines or "
            "does not answer within a few seconds, the offer moves to the next."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.15), run_time=2)
            self.play(LaggedStart(*[GrowFromCenter(a) if isinstance(a, DoubleArrow) else GrowArrow(a)
                                    for a in links], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("b")
            pings = VGroup(*[Dot(radius=0.08, color=DATA).move_to(driver.get_right()) for _ in range(4)])
            wpath = VMobject().set_points_as_corners([driver.get_right(), gate[0].get_left() + DOWN * 1.3,
                                                      gate[0].get_right() + DOWN * 1.3, loc.get_left(),
                                                      loc.get_right(), geo.get_left() + DOWN * 0.2])
            self.play(FadeIn(notes[0]), LaggedStart(*[MoveAlongPath(p, wpath) for p in pings], lag_ratio=0.25),
                      run_time=2.5)
            self.play(Indicate(geo, color=DATA), FadeOut(pings))
            vo.wait_until("c")
            req = Dot(radius=0.1, color=HEAD).move_to(rider.get_right())
            self.play(FadeIn(req), FadeIn(notes[1]))
            legs = [[rider.get_right(), gate[0].get_left() + UP * 1.3, gate[0].get_right() + UP * 1.3,
                     disp.get_left()],
                    [disp.get_right() + DOWN * 0.2, geo.get_left() + UP * 0.2],
                    [geo.get_left() + UP * 0.2, disp.get_right() + DOWN * 0.2],
                    [disp.get_right() + UP * 0.2, eta.get_left()],
                    [eta.get_left(), disp.get_right() + UP * 0.2],
                    [disp.get_left(), gate[0].get_right() + UP * 1.3, gate[0].get_right() + DOWN * 1.3,
                     gate[0].get_left() + DOWN * 1.3, driver.get_right()]]
            for leg in legs:
                self.play(MoveAlongPath(req, VMobject().set_points_as_corners(leg)), run_time=0.8, rate_func=linear)
            self.play(Indicate(driver, color=HEAD), FadeOut(req))
        self.wait(0.4)
        self.clear_scene()

    def matching(self):
        d = load("dispatch")
        head = label(r"Greedy, \ or batched?", font_size=36).to_edge(UP, buff=0.3)
        # an illustrative line of two riders and two drivers: greedy serves A first with the driver B needed
        y = 1.6
        pos = {"A": -1.0, "D1": 0.2, "B": 1.6, "D2": -3.4}
        marks = VGroup()
        for k, x in pos.items():
            if k.startswith("D"):
                m = Dot([x, y, 0], radius=0.13, color=DATA)
            else:
                m = Star(n=5, outer_radius=0.17, color=HEAD, fill_opacity=1).move_to([x, y, 0])
            marks.add(VGroup(m, label(k[0] + (r"$_" + k[1] + "$" if len(k) > 1 else ""), font_size=18,
                                      color=GREY_A).next_to(m, UP, buff=0.12)))
        road = Line([-4.2, y, 0], [2.4, y, 0], color=GREY_D, stroke_width=2)

        def arc(a, b, col):
            sign = 1 if pos[a] < pos[b] else -1           # counter-clockwise from left to right bulges downward
            return ArcBetweenPoints([pos[a], y - 0.12, 0], [pos[b], y - 0.12, 0], angle=sign * PI / 2.2, color=col,
                                    stroke_width=3)
        greedy = VGroup(arc("A", "D1", NO), arc("B", "D2", NO))
        best = VGroup(arc("D2", "A", YES), arc("D1", "B", YES))
        gl = label(r"greedy: \ A arrives first and takes the nearest driver; \ B gets the far one", font_size=18,
                   color=NO).next_to(road, DOWN, buff=1.35).set_x(-0.9)
        bl = label(r"batched: \ match both at once; \ the total is smaller", font_size=18, color=YES)
        bl.next_to(gl, DOWN, buff=0.12).align_to(gl, LEFT)
        ill = note(r"illustrative", font_size=16).next_to(road, RIGHT, buff=0.2)
        vals = [d["greedy_mean"], d["batched_mean"], d["greedy_worst"], d["batched_worst"]]
        chart = bar_chart(vals, [r"greedy, mean", r"batched, mean", r"greedy, worst", r"batched, worst"],
                          [NO, YES, NO, YES], height=1.6, bar_w=0.9, gap=0.9, fmt_=lambda v: f"{v:.2f} km",
                          font_size=18)
        chart.to_edge(DOWN, buff=0.55).set_x(-2.4)
        cap = wrapped_label(rf"{d['riders']} riders and {d['drivers']} drivers at random in a "
                            rf"{d['city_km']:.0f} km city, \ pickup distance as the crow flies, \ averaged over 200 "
                            r"rounds; \ batched = the assignment problem, \ solved exactly \ (after Kuhn) \ "
                            r"(Kuhn 1955, \ Part 18)", 4.6, font_size=18, color=WHITE)
        cap.next_to(chart, RIGHT, buff=0.6).align_to(chart, DOWN)
        with self.voiceover(
            "The hard idea: which driver takes which rider? <bookmark mark='a'/> The obvious rule is "
            "greedy: as each request arrives, give it the nearest free driver. Here rider A arrives first and takes "
            "the only driver near B, so B gets the far one. <bookmark mark='b'/> Collect both requests and match "
            "them together, and the total is smaller. Matching a "
            "batch is the assignment problem of Part 18, solved exactly; Harold Kuhn's Hungarian algorithm of 1955 was the first, and our solver reaches the same optimum by a faster modern method. "
            "<bookmark mark='c'/> We simulated it: sixty riders and seventy drivers scattered over a ten-kilometre "
            "city, two hundred times. Greedy's mean pickup was one point one seven kilometres; batched, zero point "
            "nine six. <bookmark mark='d'/> The worst pickup in each round fell much more, from four point eight to "
            "three point zero, because greedy's last riders get whatever is left. The price is a batching window of "
            "a few seconds."
        ) as vo:
            self.play(FadeIn(head), Create(road), FadeIn(marks), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(greedy[0]))
            self.play(Create(greedy[1]), FadeIn(gl))
            vo.wait_until("b")
            self.play(greedy.animate.set_stroke(opacity=0.25), Create(best), FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeIn(chart.names), Create(chart[0]), FadeIn(cap))
            self.play(GrowFromEdge(chart.bars[0], DOWN), GrowFromEdge(chart.bars[1], DOWN),
                      FadeIn(chart.vals[0]), FadeIn(chart.vals[1]))
            vo.wait_until("d")
            self.play(GrowFromEdge(chart.bars[2], DOWN), GrowFromEdge(chart.bars[3], DOWN),
                      FadeIn(chart.vals[2]), FadeIn(chart.vals[3]))
        self.wait(0.4)
        self.clear_scene()

    def eta(self):
        head = label(r"ETAs: \ contraction hierarchies", font_size=36).to_edge(UP, buff=0.3)
        names = ["s", "a", "v", "b", "t"]
        imp = {"s": 0, "a": 2, "v": 1, "b": 3, "t": 0}
        xs = np.linspace(-5.6, 0.4, 5)
        yb = 0.0
        nodes = {n: Dot([x, yb + 0.55 * imp[n], 0], radius=0.13, color=GREY_A) for n, x in zip(names, xs)}
        nl = VGroup(*[label(n, font_size=18, color=GREY_A).next_to(nodes[n], DOWN, buff=0.12) for n in names])
        w = [3, 2, 4, 3]
        edges = VGroup(*[Line(nodes[a].get_center(), nodes[b].get_center(), color=GREY_C, stroke_width=2)
                         for a, b in zip(names, names[1:])])
        wl = VGroup(*[label(str(k), font_size=16, color=GREY_B).next_to(e, UP, buff=0.05) for k, e in zip(w, edges)])
        short = ArcBetweenPoints(nodes["a"].get_center(), nodes["b"].get_center(), angle=-PI / 3, color=HEAD,
                                 stroke_width=3)
        sl = label(r"shortcut a--b: \ 6", font_size=17, color=HEAD).next_to(short, UP, buff=0.08)
        ill = note(r"a five-node road, \ illustrative; \ height = importance", font_size=16)
        ill.next_to(VGroup(*nodes.values()), DOWN, buff=0.6)
        notes = VGroup(
            wrapped_label(r"preprocess: \ remove the least important junction, \ v; \ if the shortest path between "
                          r"its neighbours ran through it, \ add a shortcut with the same length", 5.3, font_size=19,
                          color=WHITE),
            wrapped_label(r"repeat for every junction, \ in order of importance: \ a hierarchy of shortcuts", 5.3,
                          font_size=19, color=HEAD),
            wrapped_label(r"query: \ Dijkstra from both ends, \ each only climbing upward; \ they meet near the top, "
                          r"\ settling a small fraction of the junctions plain Dijkstra would \ (Part 18)", 5.3,
                          font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.8, -0.1, 0])
        up_s = Arrow(nodes["s"].get_center(), nodes["a"].get_center(), buff=0.15, color=YES, stroke_width=4)
        up_t = Arrow(nodes["t"].get_center(), nodes["b"].get_center(), buff=0.15, color=YES, stroke_width=4)
        with self.voiceover(
            "To choose among drivers, dispatch needs driving times, thousands a second. <bookmark mark='a'/> "
            "Contraction hierarchies, from Robert Geisberger and colleagues in 2008, prepare the road graph in "
            "advance. Remove the least important junction; wherever the shortest path between two of its neighbours "
            "ran through it, add a shortcut of the same length. <bookmark mark='b'/> Repeat for every junction, in "
            "order of importance, and the graph gains a hierarchy of shortcuts. <bookmark mark='c'/> A query then "
            "runs Dijkstra's search from both ends, each only climbing upward, and the two meet near the top. As "
            "Part 18 measured, such a query settles a small fraction of the junctions that plain Dijkstra would."
        ) as vo:
            self.play(FadeIn(head), Create(edges), *[FadeIn(n) for n in nodes.values()], FadeIn(nl), FadeIn(wl),
                      FadeIn(ill))
            vo.wait_until("a")
            self.play(nodes["v"].animate.set_color(GREY_D), edges[1].animate.set_stroke(GREY_D, opacity=0.4),
                      edges[2].animate.set_stroke(GREY_D, opacity=0.4), FadeIn(notes[0]))
            self.play(Create(short), FadeIn(sl))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(GrowArrow(up_s), GrowArrow(up_t), FadeIn(notes[2]))
            self.play(Indicate(short, color=YES))
        self.wait(0.4)
        self.clear_scene()

    def surge(self):
        head = label(r"Surge pricing: \ a market in every cell", font_size=36).to_edge(UP, buff=0.3)
        ax = axes([0, 10, 2], [0, 10, 2], x_length=5.6, y_length=4.2, x_label=r"rides an hour", y_label=r"price")
        ax.move_to([-3.2, -0.3, 0])
        A = ax.ax
        supply = A.plot(lambda q: 1 + 0.8 * q, x_range=[0, 10], color=DATA)
        demand = A.plot(lambda q: 9 - 0.8 * q, x_range=[0, 10], color=HEAD)
        demand2 = A.plot(lambda q: 12 - 0.8 * q, x_range=[2.5, 10], color=NO)
        eq1 = Dot(A.c2p(5, 5), color=WHITE)
        eq2 = Dot(A.c2p(6.875, 6.5), color=NO)
        sl = label(r"supply: \ drivers", font_size=17, color=DATA).next_to(A.c2p(8.5, 7.8), UL, buff=0.05)
        dl = label(r"demand", font_size=17, color=HEAD).next_to(A.c2p(8, 2.6), DL, buff=0.05)
        d2l = label(r"a concert ends", font_size=17, color=NO).next_to(A.c2p(4, 8.8), UR, buff=0.05)
        ill = note(r"curves illustrative", font_size=16).next_to(ax, DOWN, buff=0.1)
        notes = VGroup(
            wrapped_label(r"in each cell, \ every minute or two, \ compare open requests with free drivers", 5.6,
                          font_size=19, color=WHITE),
            wrapped_label(r"when demand jumps, \ a higher price clears the market: \ it draws drivers in and "
                          r"persuades some riders to wait", 5.6, font_size=19, color=NO),
            wrapped_label(r"Hall, \ Kendrick and Nosko \ (2015) \ compared a night when Uber's surge worked with one "
                          r"when it briefly failed: \ without it, \ fewer requests were completed and waits grew", 5.6,
                          font_size=19, color=YES),
            wrapped_label(r"the trade-off is not technical: \ efficiency against fairness, \ and prices are capped "
                          r"in emergencies", 5.6, font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, -0.2, 0])
        with self.voiceover(
            "The last piece is economic. <bookmark mark='a'/> In each cell, every minute or two, the system compares "
            "open requests with free drivers. The price settles where supply and demand cross. "
            "<bookmark mark='b'/> When a concert ends, demand jumps, and at the old price there are not enough "
            "drivers. A higher price clears the market: it draws drivers in and persuades some "
            "riders to wait. <bookmark mark='c'/> Jonathan Hall, Cory Kendrick and Chris Nosko compared, in "
            "2015, a night when Uber's surge pricing worked with one when it briefly failed: without it, fewer "
            "requests were completed and waits grew. <bookmark mark='d'/> The trade-off here is not technical: "
            "efficiency against fairness, and so surge is capped in emergencies."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(supply), Create(demand), FadeIn(sl), FadeIn(dl), FadeIn(notes[0]))
            self.play(FadeIn(eq1))
            vo.wait_until("b")
            self.play(TransformFromCopy(demand, demand2), FadeIn(d2l))
            self.play(TransformFromCopy(eq1, eq2), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
