from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import (FAIL, FCOL, GCOST, HEUR, HIST, PART, PATH, SYMBOL, cell_center, frontier_rgb,
                                  grid_frame, image_from_rgb, live_image, load, path_line, tile_board)


def neighbours8(p):
    out = []
    b = p.index(0)
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        r, c = b // 3 + dr, b % 3 + dc
        if 0 <= r < 3 and 0 <= c < 3:
            q = list(p)
            j = r * 3 + c
            q[b], q[j] = q[j], q[b]
            out.append((q, q[b]))
    return out


class Search(VoiceoverScene):
    def construct(self):
        self.card()
        self.state_space()
        self.layers()
        self.orders()
        self.dijkstra()

    def card(self):
        card = chapter_card(2, r"Search", r"How do you find a solution when all you can do is try things?",
                            lit=(1956,), part=PART)
        with self.voiceover("Chapter two. Search."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def state_space(self):
        d = load("puzzle8")
        p0 = list(d["path"][0])
        start = tile_board(p0, cell=0.55, center=[-4.6, 0.6, 0], font_size=26)
        sl = label(r"a state", font_size=24, color=GREY_A).next_to(start, UP, buff=0.2)
        kids = neighbours8(p0)
        boards = VGroup(*[tile_board(q, cell=0.42, font_size=20, highlight=(t,)) for q, t in kids])
        boards.arrange(DOWN, buff=0.35).move_to([-0.9, 0.6, 0])
        arrows = VGroup(*[Arrow(start.get_right(), b.get_left(), buff=0.15, color=GREY_B, stroke_width=2.5)
                          for b in boards])
        al = label(r"actions: \ slide a tile into the gap", font_size=22, color=GREY_A).next_to(boards, DOWN, buff=0.3)
        goal = tile_board([1, 2, 3, 4, 5, 6, 7, 8, 0], cell=0.42, font_size=20, color=PATH).move_to([-0.9, -2.9, 0])
        goal.next_to(al, DOWN, buff=0.25)
        gl = label(r"the goal", font_size=22, color=PATH).next_to(goal, LEFT, buff=0.25)
        dc = definition_card(r"search problem", r"states; \ actions and their costs; \ a start state; \ a goal test. "
                             r"\ A solution is a sequence of actions from the start to a goal; \ an optimal one costs "
                             r"least", width=5.6, font_size=23, color=GCOST).move_to([4.0, 1.2, 0])
        count = label(r"$9!/2 = 181{,}440$ reachable states \\ (half of all arrangements: \ a parity invariant)",
                      font_size=22, color=GREY_A).next_to(dc, DOWN, buff=0.4)
        with self.voiceover(
            "Start, apply moves, look for a goal: that pattern is behind everything in this part. Take the eight-puzzle: eight "
            "numbered tiles in a three-by-three frame, and one gap. <bookmark mark='a'/> Each arrangement is a state; an action "
            "slides a tile into the gap. <bookmark mark='b'/> The goal is the tiles in order. <bookmark mark='c'/> That is a "
            "search problem: states, actions with costs, a start and a goal test. A solution reaches the goal; an optimal one "
            "does so most cheaply. <bookmark mark='d'/> The eight-puzzle has a hundred and eighty-one thousand four hundred and "
            "forty reachable states, exactly half of all arrangements: a parity argument rules out the other half."
        ) as vo:
            self.play(FadeIn(start), FadeIn(sl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(b) for b in boards], lag_ratio=0.2), FadeIn(al))
            vo.wait_until("b")
            self.play(FadeIn(goal), FadeIn(gl))
            vo.wait_until("c")
            self.play(FadeIn(dc, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(count))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def layers(self):
        d = load("puzzle8")
        L = np.asarray(d["layers"])
        D = len(L) - 1
        g = axes([0, D + 1], [0, 26000], x_length=8.2, y_length=4.0, xlabel=r"moves from the goal",
                 ylabel=r"states at that distance", xticks=[0, 10, 20, 30], yticks=[0, 10000, 20000],
                 yfmt=lambda v: f"{int(v):,}".replace(",", "{,}"), center=[-1.6, -0.5, 0])
        bw = g.ax.c2p(1, 0)[0] - g.ax.c2p(0, 0)[0]
        bars = VGroup(*[Rectangle(width=bw * 0.8, height=max(g.ax.c2p(0, v)[1] - g.ax.c2p(0, 0)[1], 0.005),
                                  stroke_width=0, fill_color=GCOST, fill_opacity=0.9)
                        .move_to(g.ax.c2p(k + 0.5, v / 2)) for k, v in enumerate(L)])
        hard = VGroup(*[tile_board(p, cell=0.36, font_size=17, color=FAIL) for p in d["hardest"]])
        hard.arrange(DOWN, buff=0.3).move_to([5.4, 0.2, 0])
        hl = label(rf"the only {len(d['hardest'])} states \\ ${d['max_depth']}$ moves away", font_size=22,
                   color=FAIL).next_to(hard, UP, buff=0.25)
        peak = int(np.argmax(L))
        tag = note(r"computed: \ breadth-first search of every state").to_corner(DR, buff=0.2)
        with self.voiceover(
            "The simplest strategy is breadth-first search: everything one move away, then two, ring by ring, with the frontier "
            "in a first-in, first-out queue. <bookmark mark='a'/> Run from the goal, it maps the whole puzzle. The rings swell: "
            f"the widest, at distance {peak}, holds {int(L[peak]):,} states. <bookmark mark='b'/> Every state is solvable in at "
            f"most {d['max_depth']} moves, and exactly {len(d['hardest'])} need all {d['max_depth']}. Breadth-first search finds "
            "shortest solutions, because it finishes each depth before the next. The price is memory: the whole frontier."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08), run_time=4.0)
            vo.wait_until("b")
            self.play(Indicate(bars[-1], color=FAIL, scale_factor=1.6), FadeIn(hard), FadeIn(hl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def orders(self):
        t = {"children": [{"children": [{"children": []}, {"children": []}]},
                          {"children": [{"children": []}, {"children": []}]},
                          {"children": [{"children": []}, {"children": []}]}]}
        left = SearchTree(t, width=4.6, level_height=1.3, radius=0.17, center=[-3.4, 0.2, 0])
        right = SearchTree(t, width=4.6, level_height=1.3, radius=0.17, center=[3.4, 0.2, 0])
        n = len(left.nodes)
        bfs = list(range(n))  # breadth-first numbering is the tree's own

        def dfs_order(tr):
            out = []

            def go(i):
                out.append(i)
                for k in tr.kids[i]:
                    go(k)
            go(0)
            return out
        dfs = dfs_order(right)
        lh = label(r"breadth-first: \ a queue", font_size=28, color=GCOST).next_to(left, UP, buff=0.45)
        rh = label(r"depth-first: \ a stack", font_size=28, color=HEUR).next_to(right, UP, buff=0.45)
        nums_l = VGroup(*[MathTex(str(k + 1), font_size=22, color=GCOST).next_to(left.nodes[i], RIGHT, buff=0.08)
                          for k, i in enumerate(bfs)])
        nums_r = VGroup(*[MathTex(str(k + 1), font_size=22, color=HEUR).next_to(right.nodes[i], RIGHT, buff=0.08)
                          for k, i in enumerate(dfs)])
        cmp_ = VGroup(
            label(r"shortest solution first; \ memory $\sim b^d$", font_size=22, color=GCOST).next_to(left, DOWN, buff=0.4),
            label(r"memory $\sim b\,d$; \ may dive forever", font_size=22, color=HEUR).next_to(right, DOWN, buff=0.4))
        ids = label(r"iterative deepening (Korf 1985): \ depth-first to depth $1, 2, 3, \dots$ \ shortest first, "
                    r"memory $\sim b\,d$", font_size=22, color=PATH).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Search strategies differ only in which frontier state they expand next. <bookmark mark='a'/> Breadth-first takes "
            "the oldest. <bookmark mark='b'/> Depth-first takes the newest, diving down one branch before backing up: a stack "
            "instead of a queue. <bookmark mark='c'/> With b choices per state and a solution d moves deep, breadth-first may "
            "store about b to the d states; depth-first only b times d, but it can dive forever. <bookmark mark='d'/> Iterative "
            "deepening, from Richard Korf in 1985, gets both: depth-first to depth one, then two, then three. The repeated work "
            "is small, because the last level dominates."
        ) as vo:
            self.play(Create(left.edge_group), FadeIn(left.nodes), Create(right.edge_group), FadeIn(right.nodes))
            vo.wait_until("a")
            self.play(FadeIn(lh), LaggedStart(*[AnimationGroup(left.nodes[i].animate.set_color(GCOST), FadeIn(nums_l[k]))
                                                for k, i in enumerate(bfs)], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rh), LaggedStart(*[AnimationGroup(right.nodes[i].animate.set_color(HEUR), FadeIn(nums_r[k]))
                                                for k, i in enumerate(dfs)], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(cmp_))
            vo.wait_until("d")
            self.play(FadeIn(ids, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dijkstra(self):
        d = load("grid")
        free = np.asarray(d["free"]).astype(bool)
        order = np.asarray(d["dijkstra_order"])
        n = int(d["dijkstra_n"])
        H, W = free.shape
        width = 6.2
        t = ValueTracker(0)
        center = [-2.3, -0.3, 0]

        img = live_image(lambda: frontier_rgb(free, order, t.get_value(), band=220.0), width, center)
        base = img
        frame = grid_frame(base)
        sr, sc = d["start"]
        gr, gc = d["goal"]
        sdot = Dot(cell_center(base, (H, W), sr, sc), radius=0.1, color=WHITE)
        gdot = Star(n=5, outer_radius=0.16, color=PATH, fill_opacity=1).move_to(cell_center(base, (H, W), gr, gc))
        pl = path_line(base, (H, W), d["dijkstra_path"], color=PATH)
        num = DecimalNumber(0, num_decimal_places=0, group_with_commas=True, font_size=34, color=GCOST)
        num.add_updater(lambda m: m.set_value(min(t.get_value(), n)))
        cnt = VGroup(label(r"cells expanded", font_size=24, color=GCOST), num).arrange(RIGHT, buff=0.25)
        cnt.move_to([4.2, 2.6, 0])
        num.add_updater(lambda m: m.next_to(cnt[0], RIGHT, buff=0.25))
        rule = VGroup(label(r"uniform cost: \\ expand the cheapest $g$", font_size=24, color=GCOST),
                      label(r"$g$ = cost of the path so far", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.15)
        rule.move_to([4.2, 1.2, 0])
        hc = history_card(1959, r"Edsger Dijkstra", r"shortest paths in a graph \\ with non-negative costs",
                          width=3.6, color=HIST, font_size=20).move_to([4.4, -1.2, 0])
        if hc.get_right()[0] > 6.95:
            hc.shift(LEFT * (hc.get_right()[0] - 6.95))
        cost = label(rf"path cost ${d['dijkstra_cost']:.1f}$", font_size=22, color=PATH).next_to(cnt, DOWN, buff=0.25)
        tag = note(r"computed: \ $16$ move directions, \ each costing its length").to_corner(DL, buff=0.2)
        with self.voiceover(
            "When actions have different costs, expand the cheapest first: the state with the smallest g, the cost of the best "
            "path found to it. On a graph this is Edsger Dijkstra's algorithm of 1959. <bookmark mark='a'/> Here it runs on a "
            "map: start in the middle, goal to the right behind a wall, each move costing its length. The expanded region "
            "grows as a wavefront, bending around the walls. <bookmark mark='b'/> It reaches the goal after expanding "
            f"{n:,} cells, with a provably shortest path. <bookmark mark='c'/> But it searched just as far away from the goal "
            "as toward it. It knows how far it has come, not where it is going."
        ) as vo:
            self.add(img)
            self.play(Create(frame), FadeIn(sdot), FadeIn(gdot), FadeIn(rule), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cnt))
            self.play(t.animate.set_value(n), run_time=8.0, rate_func=linear)
            vo.wait_until("b")
            self.play(Create(pl), FadeIn(cost), FadeIn(hc))
            vo.wait_until("c")
            wasted = SurroundingRectangle(Line(cell_center(base, (H, W), 6, 2), cell_center(base, (H, W), 58, 24)),
                                          color=FAIL, buff=0.05, stroke_width=4)
            self.play(Create(wasted))
        img.clear_updaters()
        num.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
