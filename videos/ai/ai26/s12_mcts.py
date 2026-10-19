from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai26 import c4
from videos.ai.ai26.common import AGENT, EXPLORE, PART, PENALTY, REWARD, SEARCH, VALUE, axes, curve, load


def tree_dict(t):
    """uct_tree's dump -> SearchTree input, edges as thick as their visits."""
    return {"n": t["N"], "w": t["W"], "move": t["move"], "children": [tree_dict(c) for c in t["children"]]}


class MCTS(VoiceoverScene):
    def construct(self):
        self.card()
        self.playouts()
        self.four_steps()
        self.growth()
        self.quality()
        self.history()

    def card(self):
        card = chapter_card(11, r"Monte Carlo tree search", r"What if you judge a position by playing it out at random?",
                            lit=(2006,), part=PART)
        with self.voiceover("Chapter eleven. Monte Carlo tree search."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def playouts(self):
        d = load("uct_tree")
        seq = list(d["seq"])
        b0 = c4.Board.from_moves(seq)
        board = C4View(cell=0.5, center=[-3.4, 0.0, 0]).play_moves(seq)
        rng = np.random.default_rng(2)
        tally = {"win": 0, "loss": 0, "draw": 0}
        mover = 1 if b0.moves % 2 == 0 else -1
        cnt = VGroup(label(r"wins for yellow", font_size=24, color=FIRST), MathTex(r"0", font_size=36, color=FIRST),
                     label(r"wins for red", font_size=24, color=SECOND), MathTex(r"0", font_size=36, color=SECOND))
        cnt.arrange_in_grid(rows=2, cols=2, buff=(0.4, 0.3), cell_alignment=LEFT).move_to([3.6, 1.0, 0])
        idea = label(r"the value of a position $\approx$ the share of \\ random games from it that you win", font_size=26,
                     color=GREY_A).move_to([3.4, -1.3, 0])
        hc = history_card(1993, r"Bernd Br\"ugmann, \textit{Monte Carlo Go}", r"judge Go positions by random games",
                          width=4.6, color=EXPLORE).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Go programs found a way around the missing evaluation function: don't evaluate, sample. "
            "<bookmark mark='a'/> To judge a position, finish the game from it many times, with both sides playing "
            "at random, and count who wins. <bookmark mark='b'/> A random game is a terrible game, but averaged over "
            "thousands, the share of wins is a rough measure of who stands better. Bernd Brügmann tried it on Go in "
            "1993."
        ) as vo:
            self.play(FadeIn(board), FadeIn(cnt))
            vo.wait_until("a")
            for k in range(6):
                b = b0
                tmp = VGroup()
                p = mover
                while True:
                    legal = b.legal()
                    c = int(legal[rng.integers(len(legal))])
                    st = board.stone(board.height(c), c, p)
                    board.stone_at[(board.height(c), c)] = st
                    tmp.add(st)
                    b = b.play(c)
                    p = -p
                    if c4.last_mover_won(b) or b.full():
                        break
                self.play(LaggedStart(*[FadeIn(s_, shift=DOWN * 0.2) for s_ in tmp], lag_ratio=0.25), run_time=1.2)
                if c4.last_mover_won(b):
                    who = "win" if (b.moves % 2 == 1) == (mover == 1) else "loss"
                    tally[who] += 1
                yellow = tally["win"] if mover == 1 else tally["loss"]
                red = tally["loss"] if mover == 1 else tally["win"]
                self.play(Transform(cnt[1], MathTex(str(yellow), font_size=36, color=FIRST).move_to(cnt[1])),
                          Transform(cnt[3], MathTex(str(red), font_size=36, color=SECOND).move_to(cnt[3])),
                          FadeOut(tmp), run_time=0.5)
                for key in [kk for kk in board.stone_at if kk not in {(r_, c_) for r_ in range(6) for c_ in range(7)
                                                                        if b0.grid()[r_, c_]}]:
                    board.stone_at.pop(key)
            vo.wait_until("b")
            self.play(FadeIn(idea), FadeIn(hc, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def four_steps(self):
        t = {"children": [{"children": [{"children": []}, {"children": []}]}, {"children": [{"children": []}]},
                          {"children": []}]}
        tree = SearchTree(t, width=5.0, level_height=1.2, radius=0.14, center=[-3.4, 1.0, 0])
        Ns = [12, 7, 3, 2, 4, 2, 1]
        nl = VGroup(*[MathTex(str(n), font_size=20, color=SEARCH).next_to(tree.nodes[i], RIGHT, buff=0.08)
                      for i, n in enumerate(Ns)])
        steps = VGroup(*[label(s, font_size=26, color=c) for s, c in
                         ((r"1. \ select: \ at each node, the child with the best UCB score", SEARCH),
                          (r"2. \ expand: \ add one new child", AGENT),
                          (r"3. \ simulate: \ play randomly to the end", EXPLORE),
                          (r"4. \ back up: \ add the result to every node on the path", REWARD))])
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([2.6, 1.0, 0])
        if steps.width > 7.6:
            steps.width = 7.6
        ucb = cmath(r"\text{score}", r"=", r"\frac{W_i}{N_i}", r"+", r"c \sqrt{\frac{\ln N}{N_i}}", font_size=36)
        ucb[2].set_color(VALUE)
        ucb[4].set_color(EXPLORE)
        ucb.move_to([2.6, -2.2, 0])
        ul = label(r"UCB from chapter 2: \ a bandit at every node", font_size=22, color=GREY_A).next_to(ucb, DOWN, buff=0.15)
        path = [0, 1, 4]
        new = Dot(tree.pos[4] + DOWN * 1.2 + LEFT * 0.0, radius=0.14, color=AGENT)
        new_edge = Line(tree.pos[4], new.get_center(), buff=0.14, color=AGENT, stroke_width=3)
        sim = VMobject(stroke_color=EXPLORE, stroke_width=3).set_points_smoothly(
            [new.get_center() + np.array([0.25 * np.sin(3 * y), -y, 0]) for y in np.linspace(0, 1.4, 12)])
        res = MathTex(r"\text{win}", font_size=26, color=REWARD).next_to(sim, DOWN, buff=0.08)
        cite_ = cite(r"Coulom (2006); \ Kocsis \& Szepesv\'ari, \textit{Bandit based Monte-Carlo Planning} (2006)")
        th = theorem_card(r"UCT", r"with enough simulations, \ the move it picks converges to the minimax move",
                          who=r"Kocsis \& Szepesv\'ari (2006)", width=5.4, color=SEARCH).move_to([2.6, -2.0, 0])
        with self.voiceover(
            "Random games from the root waste effort on bad moves. Monte Carlo tree search grows a tree instead, "
            "spending its simulations where they matter. Each simulation has four steps. <bookmark mark='a'/> "
            "Select: from the root, step down the tree, at each node choosing the child with the best score. "
            "<bookmark mark='b'/> The score is the upper confidence bound from chapter two: the win rate so far, plus "
            "a bonus for children tried rarely. Every node is a little bandit problem. <bookmark mark='c'/> Expand: "
            "when you reach the edge of the tree, add a child. <bookmark mark='d'/> Simulate: from there, play "
            "randomly to the end. <bookmark mark='e'/> Back up: add the result to every node on the path. "
            "<bookmark mark='f'/> Rémi Coulom named it Monte Carlo tree search in 2006, and Kocsis and Szepesvári "
            "proved the same year that this UCT rule converges to the minimax move as the simulations grow."
        ) as vo:
            self.play(Create(tree.edge_group), FadeIn(tree.nodes), FadeIn(nl), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), *[tree.edges[i].animate.set_stroke(SEARCH, 6) for i in path[1:]],
                      *[tree.nodes[i].animate.set_color(SEARCH) for i in path])
            vo.wait_until("b")
            self.play(Write(ucb), FadeIn(ul))
            vo.wait_until("c")
            self.play(FadeIn(steps[1]), Create(new_edge), FadeIn(new, scale=1.5))
            vo.wait_until("d")
            self.play(FadeIn(steps[2]), Create(sim), FadeIn(res))
            vo.wait_until("e")
            self.play(FadeIn(steps[3]), *[Transform(nl[i], MathTex(str(Ns[i] + 1), font_size=20, color=REWARD)
                                                   .move_to(nl[i])) for i in path])
            vo.wait_until("f")
            self.play(FadeOut(VGroup(ucb, ul)))
            self.play(FadeIn(th, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def growth(self):
        d = load("uct_tree")
        snaps = list(d["snaps"])
        truth = np.asarray(d["truth"])
        board = C4View(cell=0.32, center=[-5.6, 2.55, 0]).play_moves(list(d["seq"]))

        def build(i):
            tt = tree_dict(d["trees"][i])
            total = max(tt["n"], 1)

            def width(nd):
                return 1.0 + 14.0 * (nd["n"] / total) ** 0.6

            tr = SearchTree(tt, width=9.4, level_height=1.45, radius=0.07, edge_width=width,
                            edge_color=SEARCH, center=[1.6, 0.0, 0])
            for k in tr.kids[0]:
                tr.nodes[k].set_color(SEARCH).scale(1.6)
            return tr

        tree = build(0)
        cnt = label(rf"${snaps[0]}$ simulations", font_size=28, color=SEARCH).to_corner(UR, buff=0.4)

        def col_labels(tr):
            g = VGroup()
            for k in tr.kids[0]:
                mv = tr.node_data[k]["move"]
                g.add(VGroup(MathTex(rf"\text{{col}}\ {mv + 1}", font_size=20, color=GREY_A),
                             MathTex(str(tr.node_data[k]["n"]), font_size=22, color=SEARCH))
                      .arrange(DOWN, buff=0.05).next_to(tr.nodes[k], UP, buff=0.12))
            return g

        labels = col_labels(tree)
        best_mc = int(max(d["trees"][-1]["children"], key=lambda c: c["N"])["move"])
        best_true = int(np.nanargmax(truth))
        with self.voiceover(
            "Here is plain MCTS thinking about a Connect Four position, its tree drawn with each branch as thick as "
            f"the simulations through it. <bookmark mark='a'/> After {snaps[0]} simulations, every move has been "
            "tried once or twice. <bookmark mark='b'/> As the count grows, the tree grows lopsided: the search "
            "keeps returning to the moves that look best, and looks deeper there, while hopeless moves get "
            f"only enough visits to stay hopeless. <bookmark mark='c'/> After {snaps[-1]:,} simulations it likes "
            f"column {best_mc + 1} best."
        ) as vo:
            self.play(FadeIn(board), FadeIn(cnt), Create(tree.edge_group), FadeIn(tree.nodes), FadeIn(labels))
            vo.wait_until("a")
            self.play(Indicate(labels, color=SEARCH, scale_factor=1.05))
            vo.wait_until("b")
            for i in range(1, len(snaps)):
                new = build(i)
                nl = col_labels(new)
                self.play(FadeOut(tree), FadeOut(labels), FadeIn(new), FadeIn(nl),
                          Transform(cnt, label(rf"${snaps[i]:,}$ simulations".replace(",", "{,}"), font_size=28,
                                               color=SEARCH).to_corner(UR, buff=0.4)), run_time=1.4)
                tree, labels = new, nl
                self.wait(0.6)
            vo.wait_until("c")
            k = [j for j in tree.kids[0] if tree.node_data[j]["move"] == best_mc][0]
            self.play(Indicate(labels[tree.kids[0].index(k)], color=SEARCH, scale_factor=1.3))
        self.wait(0.2)
        # the verdict: the perfect solver's score for each move
        ok = [None if np.isnan(v) else bool(np.sign(v) == np.sign(np.nanmax(truth))) for v in truth]
        marks = board.column_marks(ok, font_size=20)
        verdict = label(rf"but the solver says: \ column {best_true + 1} wins; \ column {best_mc + 1} loses", font_size=26,
                        color=PENALTY).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            f"But the perfect solver disagrees: column {best_true + 1} wins by force, and column {best_mc + 1} loses. "
            "<bookmark mark='a'/> Random playouts are a crude judge. In a random game nobody exploits a threat, so a "
            "move that sets up the opponent's win can look fine on average. The search is only as good as its "
            "evaluation."
        ) as vo:
            self.play(FadeIn(marks), FadeIn(verdict))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quality(self):
        d = load("uct")
        sims = np.asarray(d["sims"], float)
        acc = np.asarray(d["acc"])
        lx = np.log10(sims)
        g = axes([1, 3.5], [0, 1], x_length=6.6, y_length=3.8, xlabel=r"simulations per move (log scale)",
                 ylabel=r"how often its move is right", xticks=[1, 2, 3], yticks=[0, 0.5, 1], log_x=True,
                 yfmt=lambda v: rf"{int(100 * v)}\%", center=[-1.2, -0.3, 0])
        line = curve(g.ax, lx, acc, SEARCH, 4)
        pts = VGroup(*[Dot(g.ax.c2p(x, y), radius=0.07, color=SEARCH) for x, y in zip(lx, acc)])
        rnd = DashedLine(g.ax.c2p(1, d["random"]), g.ax.c2p(3.5, d["random"]), color=GREY_B, dash_length=0.08)
        rl = label(rf"a random move: \ ${100 * d['random']:.0f}\%$", font_size=20, color=GREY_B).next_to(rnd, UP, buff=0.05)
        rl.align_to(rnd, RIGHT)
        tag = note(r"computed: \ $200$ test positions, \ every move scored by a perfect solver; \ right $=$ "
                   r"keeps the win, or the draw").to_corner(DR, buff=0.2)
        with self.voiceover(
            "We can measure this exactly. Connect Four is solved, so for two hundred test positions we know every "
            "move's true value. Call a move right if it keeps the best result the position allows: the win, or "
            "the draw. <bookmark mark='a'/> A random move is right "
            f"{100 * d['random']:.0f} percent of the time. <bookmark mark='b'/> Plain MCTS improves with more "
            f"simulations, to {100 * acc[-1]:.0f} percent at {int(sims[-1]):,} per move, and then levels off: more "
            "random games won't fix a biased judge."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(rnd), FadeIn(rl))
            vo.wait_until("b")
            self.play(Create(line), LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.15), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        cards = VGroup(
            history_card(2006, r"Crazy Stone \ (R\'emi Coulom), \ MoGo \ (Gelly, Wang, Munos, Teytaud)",
                         r"MCTS takes over computer Go", width=6.2, color=SEARCH),
            history_card(2013, r"Crazy Stone beats a professional, \ Yoshio Ishida", r"with a four-stone head start",
                         width=6.2, color=SEARCH),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.4)
        need = label(r"missing: \ a judge of positions as good as a strong player's eye", font_size=28, color=VALUE)
        need.to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "MCTS transformed computer Go. Crazy Stone and MoGo, from 2006, climbed from beginner to strong "
            "amateur. <bookmark mark='a'/> In 2013 Crazy Stone beat a professional, but with a four-stone head "
            "start. <bookmark mark='b'/> What was missing was a better judge: something that could look at a "
            "position and see who was winning, the way a strong player does. That is what a neural network would "
            "provide."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(need))
        self.wait(0.3)
        self.clear_scene()
