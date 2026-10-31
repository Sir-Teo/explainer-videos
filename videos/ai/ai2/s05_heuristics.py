from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import (FAIL, FCOL, GCOST, HEUR, HIST, LEARN, PART, PATH, load, tile_board)


def manhattan_parts(p):
    """For each tile: (position, goal position, distance) on the 3 x 3 board, goal 1..8 with the blank last."""
    out = []
    for i, t in enumerate(p):
        if t == 0:
            continue
        gi = t - 1
        out.append((t, i, gi, abs(i // 3 - gi // 3) + abs(i % 3 - gi % 3)))
    return out


class Heuristics(VoiceoverScene):
    def construct(self):
        self.card()
        self.relax()
        self.dominance()
        self.fifteen()
        self.learned()

    def card(self):
        card = chapter_card(4, r"Where heuristics come from", r"How do you invent a good guess?", lit=(1968,),
                            part=PART)
        with self.voiceover("Chapter four. Where heuristics come from."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def relax(self):
        d = load("puzzle8")
        p = list(d["path"][0])
        parts = manhattan_parts(p)
        h1 = sum(1 for t, i, gi, dist in parts if dist > 0)
        h2 = sum(dist for *_, dist in parts)
        board = tile_board(p, cell=0.78, center=[-4.4, 0.4, 0], font_size=30,
                           highlight=tuple(t for t, i, gi, dist in parts if dist > 0))
        rule = label(r"a tile can move from $A$ to $B$ \ if $A$ is next to $B$ \ and $B$ is empty", font_size=28)
        rule.move_to([2.4, 2.6, 0])
        # strike the conditions one at a time
        r1 = label(r"drop ``$B$ is empty'': \ each tile walks home on its own", font_size=24, color=HEUR)
        r2 = label(r"drop both: \ each misplaced tile jumps home in one move", font_size=24, color=FCOL)
        e1 = cmath(r"h_2", r"=", r"\sum_{\text{tiles}} |\Delta \text{row}| + |\Delta \text{column}|", r"=", str(h2),
                   font_size=34)
        e2 = cmath(r"h_1", r"=", r"\#\,\text{misplaced tiles}", r"=", str(h1), font_size=34)
        e1[0].set_color(HEUR)
        e2[0].set_color(FCOL)
        g1 = VGroup(r1, e1).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([2.4, 1.0, 0])
        g2 = VGroup(r2, e2).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([2.4, -0.9, 0])
        true = label(rf"the true distance of this position: \ ${len(d['path']) - 1}$ moves", font_size=24,
                     color=PATH).move_to([2.4, -2.4, 0])
        why_ = label(r"a relaxed problem has more moves, \ so its shortest solution can only be shorter: \ admissible "
                     r"for free (and consistent)", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.25)
        arrows = VGroup()
        for t, i, gi, dist in parts:
            if dist == 0:
                continue
            a = board.tiles[[k for k, x in enumerate([x for x in p if x != 0]) if x == t][0]].get_center()
            cell = 0.78
            gpos = board[0].get_center() + np.array([(gi % 3 - 1) * cell, (1 - gi // 3) * cell, 0])
            arrows.add(Arrow(a, gpos, buff=0.12, color=HEUR, stroke_width=3, max_tip_length_to_length_ratio=0.2))
        with self.voiceover(
            "A star is only as good as its heuristic. Where do good ones come from? <bookmark mark='a'/> Write down the "
            "eight-puzzle's rule: a tile can move from square A to square B if A is next to B, and B is empty. "
            "<bookmark mark='b'/> Now cheat. Drop 'B is empty', and each tile walks home through the others: that easier "
            f"puzzle costs the sum of the tiles' row and column distances, the Manhattan distance. Here, {h2}. "
            "<bookmark mark='c'/> Drop both conditions, and each misplaced tile jumps home in one move: the cost is the number "
            f"of misplaced tiles, here {h1}. <bookmark mark='d'/> The real answer, from our breadth-first map: "
            f"{len(d['path']) - 1} moves. <bookmark mark='e'/> This is the general recipe, made explicit by Judea Pearl in the "
            "early nineteen-eighties: relax the problem until it is easy, and solve that exactly. Removing rules can only shorten "
            "solutions: admissible, for free."
        ) as vo:
            self.play(FadeIn(board), FadeIn(rule))
            vo.wait_until("b")
            self.play(FadeIn(r1), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1))
            self.play(Write(e1))
            vo.wait_until("c")
            self.play(FadeIn(g2[0]), Write(e2))
            vo.wait_until("d")
            self.play(FadeIn(true))
            vo.wait_until("e")
            self.play(FadeIn(why_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dominance(self):
        d = load("puzzle8")
        D = np.asarray(d["depths"])
        series = (("astar_h0", GCOST, r"no heuristic: \ $h = 0$"), ("astar_h1", FCOL, r"misplaced tiles: \ $h_1$"),
                  ("astar_h2", HEUR, r"Manhattan: \ $h_2$"))
        top = np.log10(max(d["astar_h0"])) + 0.5
        g = axes([0, 26], [0, top], x_length=6.4, y_length=4.2, xlabel=r"length of the optimal solution",
                 ylabel=r"states A* expands \ (mean, log scale)", xticks=[0, 8, 16, 24], yticks=[0, 1, 2, 3, 4, 5],
                 yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-2.6, -0.4, 0])
        lines = VGroup(*[curve(g.ax, D, np.log10(np.asarray(d[k])), c, 4) for k, c, _ in series])
        dots = VGroup(*[VGroup(*[Dot(g.ax.c2p(x, y), radius=0.05, color=c) for x, y in zip(D, np.log10(np.asarray(d[k])))])
                        for k, c, _ in series])
        lg = legend([(c, t) for _, c, t in series], font_size=20).move_to([3.9, 2.3, 0])
        last = {k: d[k][-1] for k, _, _ in series}
        ebf = {k: d["ebf_" + k.split("_")[1]][-1] for k, _, _ in series}
        tab = VGroup(*[label(rf"{t}: \ ${last[k]:,.0f}$ states, \ $b^* = {ebf[k]:.2f}$".replace(",", "{,}"),
                             font_size=20, color=c) for k, c, t in series])
        tab.arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([3.9, 0.4, 0])
        if tab.width > 5.8:
            tab.width = 5.8
        tab.set_x(6.9 - tab.width / 2)
        eb = cmath(r"N + 1", r"=", r"1 + b^* + (b^*)^2 + \dots + (b^*)^d", font_size=30).move_to([3.9, -1.5, 0])
        el = label(r"effective branching factor $b^*$: \\ the uniform tree with $N$ nodes at depth $d$", font_size=20,
                   color=GREY_A).next_to(eb, DOWN, buff=0.15)
        dom = label(r"consistent $h_2 \ge h_1$: \ no more mandatory $f<C^*$ states; \\ boundary work depends on ties",
                    font_size=22, color=HEUR).to_edge(DOWN, buff=0.2)
        tag = note(rf"computed: \ up to ${d['per_depth']}$ positions per length").to_corner(UL, buff=0.2)
        dd = int(D[-1])
        with self.voiceover(
            "How much does the better guess buy? A star on the eight-puzzle, up to a hundred positions per solution length. "
            f"<bookmark mark='a'/> With no heuristic, at length {dd}, it expands {last['astar_h0']:,.0f} states on average. "
            f"<bookmark mark='b'/> Counting misplaced tiles: {last['astar_h1']:,.0f}. <bookmark mark='c'/> The Manhattan "
            f"distance: {last['astar_h2']:,.0f}. <bookmark mark='d'/> The effective branching factor, the branching of a uniform "
            f"tree of the same size and depth, falls from {ebf['astar_h0']:.2f} to {ebf['astar_h1']:.2f} to "
            f"{ebf['astar_h2']:.2f}: each step toward one is an exponential saving. <bookmark mark='e'/> The Manhattan distance "
            "is never below the misplaced count. For consistent heuristics, dominance cannot increase the states with f below "
            "the optimal cost that A star must expand. At the boundary, equal f values and tie breaking can change the total."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            for i, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(Create(lines[i]), FadeIn(dots[i]), FadeIn(lg[i]), FadeIn(tab[i]), run_time=1.4)
            vo.wait_until("d")
            self.play(Write(eb), FadeIn(el))
            vo.wait_until("e")
            self.play(FadeIn(dom))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fifteen(self):
        d = load("puzzle15")
        rows = d["rows"]
        names = (("misplaced", FCOL, r"misplaced tiles"), ("manhattan", HEUR, r"Manhattan distance"),
                 ("pdb", PATH, r"pattern database, \ $5$-$5$-$5$"))
        L = np.array([r["pdb_len"] for r in rows])
        lo, hi = int(L.min()) - 2, int(L.max()) + 2
        top = 8.5
        g = axes([lo, hi], [1, top], x_length=6.0, y_length=4.0, xlabel=r"length of the optimal solution",
                 ylabel=r"positions IDA* generates \ (log scale)", xticks=list(range((lo // 10 + 1) * 10, hi, 10)),
                 yticks=[2, 4, 6, 8], yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-3.0, -0.6, 0])
        pts = VGroup()
        capped = VGroup()
        for k, col, _ in names:
            grp = VGroup()
            for r in rows:
                n = r[k]
                if r[k + "_len"] < 0:
                    m = Triangle(color=col, fill_opacity=0.9, stroke_width=0).scale(0.07).rotate(PI)
                    m.move_to(g.ax.c2p(r["pdb_len"], min(np.log10(n), top - 0.1)))
                    capped.add(m)
                    grp.add(m)
                else:
                    grp.add(Dot(g.ax.c2p(r["pdb_len"], np.log10(max(n, 1))), radius=0.055, color=col))
            pts.add(grp)
        lg = legend([(c, t) for _, c, t in names], font_size=20).move_to([3.6, 2.6, 0])
        n_cap = {k: sum(1 for r in rows if r[k + "_len"] < 0) for k, _, _ in names}
        tot = {k: sum(r[k] for r in rows) for k, _, _ in names}
        hm = d["h_mean"]
        pdb_board = VGroup(*[tile_board(list(range(1, 16)) + [0], size=4, cell=0.34, font_size=14,
                                        color=GREY_D, highlight=tuple(range(a, a + 5))) for a in (1, 6, 11)])
        pdb_board.arrange(RIGHT, buff=0.25).move_to([3.6, 0.6, 0])
        pl = label(r"each table: \ exact cost in moves of its five tiles, \\ found by breadth-first search, "
                   rf"${d['pdb_entries']:,}$ entries".replace(",", "{,}"), font_size=19, color=GREY_A)
        pl.next_to(pdb_board, DOWN, buff=0.2)
        means = label(rf"average guess on random positions: \ ${hm['misplaced']:.0f}$, \ ${hm['manhattan']:.0f}$, "
                      rf"\ ${hm['pdb']:.0f}$ moves", font_size=20, color=GREY_A).move_to([3.6, -1.4, 0])
        hcs = VGroup(history_card(1985, r"Korf: \ IDA*", r"A* in the memory of depth-first search", width=3.1,
                                  color=HIST, font_size=18),
                     history_card(1998, r"Culberson \& Schaeffer", r"pattern databases", width=3.1, color=HIST,
                                  font_size=18)).arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.15).set_x(3.6)
        if hcs.get_right()[0] > 6.95:
            hcs.shift(LEFT * (hcs.get_right()[0] - 6.95))
        tag = note(rf"computed: \ ${len(rows)}$ scrambled positions; \ $\blacktriangledown$ = gave up at the cap")
        tag.to_corner(UL, buff=0.2)
        ratio = tot["manhattan"] / max(tot["pdb"], 1)
        with self.voiceover(
            "The fifteen-puzzle has about ten trillion states, too many to map. In 1985 Richard Korf solved random instances "
            "optimally with IDA star: A star's ordering, run as depth-first searches with a rising bound on f, in almost no "
            "memory. <bookmark mark='a'/> Here it is on scrambled positions. Counting misplaced tiles, it soon hits our cap of "
            f"{d['caps']['misplaced']:,} positions and gives up, {n_cap['misplaced']} times out of {len(rows)}. "
            "<bookmark mark='b'/> The Manhattan distance does far better. <bookmark mark='c'/> Better still, solve a smaller "
            "relaxed puzzle exactly and remember the answers: track five tiles, ignore the rest, and breadth-first search gives "
            "the exact cost of homing them from every placement. That is a pattern database, Joseph Culberson and Jonathan "
            "Schaeffer's idea. Each table counts only moves of its own five tiles; moves of other tiles are free. "
            "The groups are disjoint, so each real move is charged to just one table, and the three costs can be added. "
            "<bookmark mark='d'/> It generates about "
            f"{ratio:,.0f} times fewer positions than the Manhattan distance, because it knows more: on a random position it "
            f"guesses {hm['pdb']:.0f} moves on average, against {hm['manhattan']:.0f} and {hm['misplaced']:.0f}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), FadeIn(hcs[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, scale=1.5) for m in pts[0]], lag_ratio=0.03), FadeIn(lg[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m, scale=1.5) for m in pts[1]], lag_ratio=0.03), FadeIn(lg[1]))
            vo.wait_until("c")
            self.play(FadeIn(pdb_board), FadeIn(pl), FadeIn(hcs[1]))
            self.play(LaggedStart(*[FadeIn(m, scale=1.5) for m in pts[2]], lag_ratio=0.03), FadeIn(lg[2]))
            vo.wait_until("d")
            self.play(FadeIn(means))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def learned(self):
        cards = VGroup(
            history_card(1997, r"Korf: \ Rubik's cube, solved optimally", r"IDA* with pattern databases of the "
                         r"corner and edge cubies", width=6.0, color=HIST),
            history_card(2019, r"Agostinelli, McAleer, Shmakov \& Baldi: \ DeepCubeA", r"a neural network learns "
                         r"$h$ by itself, \ weighted A* uses it: \ every test cube solved, \ a shortest solution "
                         r"$60.3\%$ of the time", width=6.0, color=LEARN),
        ).arrange(DOWN, buff=0.35).move_to([-2.9, -0.2, 0])
        f = cmath(r"f", r"=", r"g", r"+", r"h", font_size=72).move_to([3.8, 1.0, 0])
        f[0].set_color(FCOL)
        f[2].set_color(GCOST)
        f[4].set_color(HEUR)
        arrow = Arrow([3.8, -0.4, 0], f[4].get_bottom() + DOWN * 0.05, buff=0.1, color=LEARN, stroke_width=4)
        nl = label(r"a value network: \ $h$, learned", font_size=26, color=LEARN).move_to([3.8, -0.8, 0])
        p26 = label(r"Part 26: \ AlphaZero's search uses one", font_size=22, color=GREY_A).next_to(nl, DOWN, buff=0.2)
        with self.voiceover(
            "The same idea scaled up. <bookmark mark='a'/> In 1997 Korf found optimal solutions to Rubik's cube with pattern "
            "databases. <bookmark mark='b'/> In 2019 a group at Irvine let a neural network learn the heuristic instead, and used "
            "it inside weighted A star: it solved every test cube, with a shortest solution sixty point three percent of the "
            "time. <bookmark mark='c'/> A learned estimate of the cost to go is what reinforcement learning calls a value "
            "function, and search guided by one is how AlphaZero plays, in Part 26."
        ) as vo:
            self.play(FadeIn(f))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(GrowArrow(arrow), FadeIn(nl), FadeIn(p26))
        self.wait(0.3)
        self.clear_scene()
