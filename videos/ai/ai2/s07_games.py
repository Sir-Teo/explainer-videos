from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import FAIL, FCOL, GCOST, HEUR, HIST, MAXC, MINC, PART, PATH, load, node_box

LEAVES = [5, 3, 9, 1, 6, 2, 8, 4, 7, 2, 1, 6, 9, 8, 3, 4, 2, 7, 6, 5, 3, 8, 1, 9, 4, 2, 5]  # illustrative


def toy_tree(b=3, depth=3):
    it = iter(LEAVES)

    def make(d):
        if d == depth:
            return {"v": next(it), "children": []}
        return {"children": [make(d + 1) for _ in range(b)]}

    return make(0)


def trace_alphabeta(tr: "SearchTree"):
    """Alpha-beta on the drawn tree, recording events: ('visit', i, alpha, beta), ('value', i, v), ('cut', i)."""
    ev = []

    def go(i, depth, a, b):
        ev.append(("visit", i, a, b))
        kids = tr.kids[i]
        if not kids:
            v = tr.node_data[i]["v"]
            ev.append(("value", i, v))
            return v
        if depth % 2 == 0:
            v = -math.inf
            for j, k in enumerate(kids):
                v = max(v, go(k, depth + 1, a, b))
                a = max(a, v)
                if a >= b:
                    for k2 in kids[j + 1:]:
                        ev.append(("cut", k2))
                    break
        else:
            v = math.inf
            for j, k in enumerate(kids):
                v = min(v, go(k, depth + 1, a, b))
                b = min(b, v)
                if a >= b:
                    for k2 in kids[j + 1:]:
                        ev.append(("cut", k2))
                    break
        ev.append(("value", i, v))
        return v

    go(0, 0, -math.inf, math.inf)
    return ev


def fmt_inf(x):
    return r"-\infty" if x == -math.inf else (r"+\infty" if x == math.inf else str(int(x)))


class Games(VoiceoverScene):
    def construct(self):
        self.card()
        self.minimax()
        self.pruning()
        self.best_case()
        self.counts()

    def card(self):
        card = chapter_card(6, r"Games and alpha--beta", r"How do you look ahead against an opponent?", lit=(1950,),
                            part=PART)
        with self.voiceover("Chapter six. Games and alpha-beta."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def minimax(self):
        d = load("ttt")
        g = d["games"]
        tot = g["x"] + g["o"] + g["draw"]
        hc1 = history_card(1928, r"John von Neumann", r"the minimax theorem: \ in a two-player zero-sum game, each side "
                           r"can guarantee the game's value", width=5.6, color=HIST, font_size=20)
        hc2 = history_card(1950, r"Claude Shannon, \textit{Programming a Computer for Playing Chess}",
                           r"look ahead, score the positions you reach, \ back the scores up: \ about $10^{120}$ "
                           r"possible games of chess", width=5.6, color=HIST, font_size=20)
        VGroup(hc1, hc2).arrange(DOWN, buff=0.3).to_edge(LEFT, buff=0.4).shift(UP * 0.3)
        rule = VGroup(cmath(r"V(s)", r"=", r"\max_{a} V(s')", font_size=34), label(r"where you move", font_size=20,
                                                                                    color=MAXC),
                      cmath(r"V(s)", r"=", r"\min_{a} V(s')", font_size=34), label(r"where they move", font_size=20,
                                                                                    color=MINC))
        rule[0][2].set_color(MAXC)
        rule[2][2].set_color(MINC)
        rule.arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.2), cell_alignment=LEFT).move_to([3.4, 1.9, 0])
        ttt = VGroup(
            label(r"tic-tac-toe, \ searched to the end on this computer:", font_size=24, color=GREY_A),
            label(rf"${d['minimax']:,}$ positions visited \ \ ${tot:,}$ complete games".replace(",", "{,}"),
                  font_size=24, color=GCOST),
            label(rf"X wins ${g['x']:,}$, \ O wins ${g['o']:,}$, \ ${g['draw']:,}$ draws".replace(",", "{,}"),
                  font_size=22, color=GREY_A),
            label(r"the value with best play on both sides: \ a draw" if d["value"] == 0 else
                  (r"the value with best play: \ X wins" if d["value"] > 0 else r"the value with best play: \ O wins"),
                  font_size=24, color=PATH),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([3.3, -1.0, 0])
        chips = VGroup(*[node_box(t, c, font_size=30) for t, c in ((r"clear rules", GCOST), (r"a clear score", PATH),
                                                                     (r"an opponent who fights back", MINC))])
        chips.arrange(RIGHT, buff=0.4).move_to(UP * 0.2)
        verdict = "a draw" if d["value"] == 0 else ("a win for the first player" if d["value"] > 0 else
                                                    "a win for the second player")
        with self.voiceover(
            "Games were the field's favourite test: clear rules, a clear score, and an opponent who fights back. "
            "<bookmark mark='a'/> In 1928 John von Neumann proved that in a two-player zero-sum game, each side can guarantee "
            "a value by assuming the opponent plays perfectly. <bookmark mark='b'/> So look ahead: where you move, take the "
            "maximum; where the opponent moves, the minimum. That's minimax. <bookmark mark='c'/> In 1950 Claude Shannon "
            "described a chess program built this way, with a formula to score the positions at the end of the look-ahead, and "
            "estimated some ten to the hundred and twenty possible games: far too many to search to the end. "
            "<bookmark mark='d'/> Tic-tac-toe is small enough. Our minimax visits "
            f"{d['minimax']:,} positions and {tot:,} complete games, and finds the game is {verdict} with best play."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.5), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeOut(chips), FadeIn(hc1, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rule))
            vo.wait_until("c")
            self.play(FadeIn(hc2, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ttt], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pruning(self):
        t = toy_tree()
        tree = SearchTree(t, width=11.0, level_height=1.45, radius=0.15, center=[0.3, 0.5, 0])
        n = len(tree.nodes)
        lvl = tree.level
        for i in range(n):
            tree.nodes[i].set_color(MAXC if lvl[i] % 2 == 0 else MINC)
        ev = trace_alphabeta(tree)
        vals = {}
        side = VGroup(label(r"you: \ max", font_size=22, color=MAXC), label(r"they: \ min", font_size=22, color=MINC),
                      label(r"you: \ max", font_size=22, color=MAXC))
        for k, s in enumerate(side):
            s.move_to([-6.2, tree.pos[[i for i in range(n) if lvl[i] == k][0]][1], 0])
        window = VGroup(MathTex(r"[\alpha, \beta]", font_size=30, color=FCOL), MathTex(r"=", font_size=30),
                        MathTex(r"[-\infty, +\infty]", font_size=30, color=FCOL)).arrange(RIGHT, buff=0.12)
        window.to_corner(UR, buff=0.35)
        wl = label(r"$\alpha$: \ the best you are already sure of; \ $\beta$: \ the best they are sure of",
                   font_size=20, color=GREY_A).next_to(window, DOWN, buff=0.12).align_to(window, RIGHT)
        tag = note(r"illustrative").to_corner(DR, buff=0.25)
        marker = Circle(radius=0.26, color=FCOL, stroke_width=4).move_to(tree.pos[0])
        visited = {e[1] for e in ev if e[0] == "visit"}
        pruned_all = [i for i in range(n) if i not in visited]
        with self.voiceover(
            "Most of a game tree never needs to be looked at. Here is a small one: you move, they reply, you move, and the "
            "bottom positions are scored. <bookmark mark='a'/> Search it depth-first, carrying two numbers: alpha, the best "
            "you are already sure of, and beta, the best your opponent is sure of. <bookmark mark='b'/> As soon as a reply "
            "shows a move is worse than one you already have, that move's other replies cannot matter, and are skipped. "
            f"The greyed branches are never examined: {len(pruned_all)} of the {n} positions, and the answer at the top is "
            "still exactly minimax's. This is alpha-beta pruning, suggested by John McCarthy in the mid-nineteen-fifties and "
            "used by every chess program since."
        ) as vo:
            self.play(Create(tree.edge_group), FadeIn(tree.nodes), FadeIn(side), FadeIn(tag), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(window), FadeIn(wl), FadeIn(marker))
            vo.wait_until("b")
            for e in ev:
                if e[0] == "visit":
                    _, i, a, b = e
                    new = MathTex(rf"[{fmt_inf(a)}, {fmt_inf(b)}]", font_size=30, color=FCOL).move_to(window[2], LEFT)
                    self.play(marker.animate.move_to(tree.pos[i]), Transform(window[2], new), run_time=0.22)
                elif e[0] == "value":
                    _, i, v = e
                    col = MAXC if lvl[i] % 2 == 0 else MINC
                    m = MathTex(str(int(v)), font_size=24, color=col if tree.kids[i] else WHITE)
                    m.next_to(tree.nodes[i], DOWN if not tree.kids[i] else LEFT, buff=0.08)
                    vals[i] = m
                    self.play(FadeIn(m), run_time=0.18)
                else:
                    sub = tree.subtree(e[1])
                    dim = [tree.nodes[j] for j in sub] + [tree.edges[j] for j in sub if tree.edges[j] is not None]
                    self.play(*[m.animate.set_opacity(0.15) for m in dim], run_time=0.35)
            self.play(Indicate(vals[0], scale_factor=1.6, color=MAXC))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def best_case(self):
        u = load("uniform")["rows"]
        head = label(r"How much can it save, at best?", font_size=34).to_edge(UP, buff=0.35)
        rows = [
            cmath(r"\text{prove } V = v", r"\iff", r"V \ge v \ \text{and}\ V \le v", font_size=34),
            cmath(r"V \ge v", r":", r"\text{one move of yours, every reply}", r"\Rightarrow", r"b^{\lfloor d/2 \rfloor}",
                  font_size=34),
            cmath(r"V \le v", r":", r"\text{every move of yours, one reply each}", r"\Rightarrow",
                  r"b^{\lceil d/2 \rceil}", font_size=34),
            cmath(r"\text{leaves}", r"=", r"b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1", r"\approx",
                  r"2\, b^{d/2}", font_size=36),
        ]
        whys = [why(r"two bounds"), why(r"$\lfloor d/2 \rfloor$ levels are theirs: all $b$"),
                why(r"$\lceil d/2 \rceil$ levels are yours: all $b$"), why(r"they share one line")]
        rows[1][4].set_color(MINC)
        rows[2][4].set_color(MAXC)
        rows[3][2].set_color(FCOL)
        step = ladder(self, rows, whys, keep=4, top=2.3, align_index=None, x=-1.2)
        th = theorem_card(r"alpha--beta's best case", r"with the best move always tried first, a depth-$d$ search with "
                          r"$b$ moves per position evaluates $b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1$ "
                          r"leaves: \ twice as deep for the same work", who=r"Knuth \& Moore (1975)", width=6.4, color=FCOL, font_size=21).to_corner(DL, buff=0.3)
        hk = history_card(1975, r"Donald Knuth \& Ronald Moore", r"\textit{An Analysis of Alpha-Beta Pruning}, \ "
                          r"\textit{Artificial Intelligence}", width=5.6, color=HIST, font_size=21)
        hk.to_corner(DL, buff=0.3)
        ok = all(r["leaves"] == r["formula"] for r in u)
        chk = label(rf"checked: \ uniform trees, $b = 2$ to $5$, $d = 1$ to $8$: \ ${sum(r['leaves'] == r['formula'] for r in u)}$ "
                    rf"of ${len(u)}$ counts match exactly", font_size=20, color=PATH if ok else FAIL)
        chk.to_corner(DR, buff=0.3)
        if chk.width > 6.2:
            chk.width = 6.2
            chk.to_corner(DR, buff=0.3)
        ex = [r for r in u if r["b"] == 5 and r["d"] == 8][0]
        agree = "all" if ok else "not all"
        with self.voiceover(
            "How much can pruning save? Donald Knuth and Ronald Moore analysed it in full in 1975. <bookmark mark='a'/> To "
            "prove a position is worth exactly v, you need two bounds. <bookmark mark='b'/> At least v: one good move of yours, "
            "and every reply to it, at every level: b to the d over two leaves, rounded down. <bookmark mark='c'/> At most v: "
            "every move of yours, and one refutation of each. <bookmark mark='d'/> The two proofs share one line of play. So "
            "with perfect ordering, alpha-beta evaluates about twice the square root of the full tree: twice as deep for the "
            "same work. <bookmark mark='e'/> We checked on uniform trees with perfect ordering: five moves per position, eight "
            f"deep, {ex['leaves']:,} leaves out of {ex['all']:,}, exactly the formula; {agree} {len(u)} cases agree."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hk, shift=UP * 0.2))
            for i, mk in enumerate("abcd"):
                vo.wait_until(mk)
                step(i)
            vo.wait_until("e")
            self.play(FadeOut(hk), FadeIn(th, shift=UP * 0.2), FadeIn(chk))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def counts(self):
        d = load("alphabeta")
        D = np.asarray(d["depths"])
        Dp = np.arange(1, len(d["ab_perfect"]) + 1)
        g = axes([0.5, 9.5], [0, 8], x_length=6.4, y_length=4.4, xlabel=r"moves looked ahead",
                 ylabel=r"positions examined \ (log scale)", xticks=[1, 3, 5, 7, 9], yticks=[0, 2, 4, 6, 8],
                 yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-2.6, -0.4, 0])
        items = (("minimax", GREY_B, r"minimax", D), ("ab_random", MINC, r"alpha--beta, \ random order", D),
                 ("ab_ordered", MAXC, r"alpha--beta, \ best-looking first", D),
                 ("ab_perfect", PATH, r"alpha--beta, \ truly best first", Dp))
        lines = VGroup(*[curve(g.ax, X, np.log10(np.asarray(d[k])), c, 4) for k, c, _, X in items])
        dots = VGroup(*[VGroup(*[Dot(g.ax.c2p(x, y), radius=0.05, color=c)
                                 for x, y in zip(X, np.log10(np.asarray(d[k])))]) for k, c, _, X in items])
        lg = legend([(c, t) for _, c, t, _ in items], font_size=20).move_to([3.9, 2.0, 0])
        mm, ab, abo = d["minimax"][-1], d["ab_random"][-1], d["ab_ordered"][-1]
        dd = len(D)
        per = d["ab_perfect"][-1]
        dpp = len(d["ab_perfect"])
        txt = VGroup(
            label(rf"at depth ${dd}$: \ ${mm / 1e6:.1f}$ million \ $\to$ \ ${abo:,.0f}$".replace(",", "{,}"),
                  font_size=22, color=MAXC),
            label(rf"at depth ${dpp}$, \ truly best first: \ ${per:,.0f}$, \\ against $\sqrt{{{d['minimax'][dpp - 1]:,.0f}}}"
                  rf"\approx {np.sqrt(d['minimax'][dpp - 1]):,.0f}$".replace(",", "{,}"), font_size=22, color=PATH),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([3.9, -0.6, 0])
        tag = note(rf"computed: \ Connect Four, \ mean of ${len(d['openings'])}$ openings").to_corner(DR, buff=0.2)
        with self.voiceover(
            "On a real game the savings are as large. Connect Four, deeper and deeper. <bookmark mark='a'/> Plain minimax grows "
            f"about sevenfold per move: at depth {dd}, {mm / 1e6:.1f} million positions. <bookmark mark='b'/> Alpha-beta in "
            f"random order: {ab:,.0f}. <bookmark mark='c'/> Best-looking move first: {abo:,.0f}. <bookmark mark='d'/> With an "
            f"oracle that knows the truly best move, at depth {dpp}: {per:,.0f}, the order of the square root of minimax's "
            f"{d['minimax'][dpp - 1]:,.0f}. That is why move ordering became the chess programmer's craft."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            for i, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(Create(lines[i]), FadeIn(dots[i]), FadeIn(lg[i]), run_time=1.3)
                if i == 2:
                    self.play(FadeIn(txt[0]))
            self.play(FadeIn(txt[1]))
        self.wait(0.3)
        self.clear_scene()
