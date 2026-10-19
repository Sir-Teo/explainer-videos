from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai26 import c4
from videos.ai.ai26.alphazero import BLOCKS, CHANNELS, GAMES_PER_GEN, SIMS
from videos.ai.ai26.common import (AGENT, EXPLORE, PART, PENALTY, PRIOR, REWARD, SEARCH, VALUE, axes, curve, legend,
                                   load, node_box)

RAW, WITH_SEARCH = PRIOR, SEARCH


class Zero(VoiceoverScene):
    def construct(self):
        self.card()
        self.zero()
        self.loop()
        self.alphazero()
        self.ours()
        self.prior_replay()
        self.strength()
        self.games()
        self.why()

    def card(self):
        card = chapter_card(13, r"Learning from zero", r"Can search teach a network, and the network guide the search?",
                            lit=(2016, 2017), part=PART)
        with self.voiceover("Chapter thirteen. Learning from zero."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def zero(self):
        gone = VGroup(label(r"human games", font_size=28), label(r"hand-made input features", font_size=28),
                      label(r"random rollouts", font_size=28), label(r"two separate networks", font_size=28))
        gone.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-3.4, 0.6, 0])
        strikes = VGroup(*[Line(m.get_left() + LEFT * 0.1, m.get_right() + RIGHT * 0.1, color=PENALTY, stroke_width=4)
                           for m in gone])
        gl = label(r"AlphaGo Zero drops:", font_size=26, color=GREY_A).next_to(gone, UP, buff=0.35).align_to(gone, LEFT)
        hc = VGroup(
            history_card(2017, r"AlphaGo Zero, \ \textit{Nature}", r"from random play, $3$ days, $4.9$ million games "
                         r"against itself: \ beats the AlphaGo that beat Lee Sedol $100$ games to $0$", width=6.2,
                         color=AGENT),
            history_card(2017, r"after $40$ days", r"beats AlphaGo Master, \ the version that won $60$ straight online "
                         r"games against professionals, \ $89$ to $11$", width=6.2, color=AGENT),
        ).arrange(DOWN, buff=0.3).move_to([3.4, 0.2, 0])
        cite_ = cite(r"D.~Silver et al., \textit{Mastering the game of Go without human knowledge}, \textit{Nature} (2017)")
        with self.voiceover(
            "Eighteen months after Seoul, DeepMind published AlphaGo Zero, and took almost everything away. "
            "<bookmark mark='a'/> No human games: it starts from random play. No hand-designed features: the input "
            "is just the stones. No random rollouts. And one network instead of separate policy and value networks. "
            "<bookmark mark='b'/> After three days and four point nine million games against itself, it beat the "
            "version that had beaten Lee Sedol, a hundred games to nothing. <bookmark mark='c'/> After forty days, it "
            "beat AlphaGo Master, the version that had won sixty straight online games against top professionals, "
            "eighty-nine to eleven. Less human knowledge made it stronger."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(gl), LaggedStart(*[FadeIn(m) for m in gone], lag_ratio=0.3))
            self.play(LaggedStart(*[Create(s_) for s_ in strikes], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(hc[0], shift=UP * 0.15), FadeIn(cite_))
            vo.wait_until("c")
            self.play(FadeIn(hc[1], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def loop(self):
        net = node_box(r"one network: \ $(\mathbf p, v) = f_\theta(s)$", AGENT, font_size=26).move_to([0, 2.4, 0])
        play = node_box(r"self-play, \ every move chosen by MCTS \ guided by $f_\theta$", SEARCH, font_size=24)
        play.move_to([3.6, 0.2, 0])
        data = node_box(r"every position: \ $(s,\ \boldsymbol\pi,\ z)$", VALUE, font_size=24).move_to([0, -2.0, 0])
        train = node_box(r"train $f_\theta$", REWARD, font_size=26).move_to([-3.6, 0.2, 0])
        arrs = VGroup(CurvedArrow(net.get_right(), play.get_top(), angle=-0.8, color=GREY_B, stroke_width=3, tip_length=0.18),
                      CurvedArrow(play.get_bottom(), data.get_right(), angle=-0.8, color=GREY_B, stroke_width=3, tip_length=0.18),
                      CurvedArrow(data.get_left(), train.get_bottom(), angle=-0.8, color=GREY_B, stroke_width=3, tip_length=0.18),
                      CurvedArrow(train.get_top(), net.get_left(), angle=-0.8, color=GREY_B, stroke_width=3, tip_length=0.18))
        pil = label(r"$\boldsymbol\pi$: \ the search's visit counts, \ normalized", font_size=20, color=SEARCH)
        zl = label(r"$z$: \ who won the game, \ $\pm 1$", font_size=20, color=REWARD)
        VGroup(pil, zl).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(data, DOWN, buff=0.2)
        loss = cmath(r"\ell", r"=", r"(z - v)^2", r"-", r"\boldsymbol\pi^{\!\top} \log \mathbf p", r"+",
                     r"c\, \|\theta\|^2", font_size=34).move_to([0, 0.3, 0])
        loss[2].set_color(VALUE)
        loss[4].set_color(SEARCH)
        b1 = brace_note(loss[2], r"value: \ predict the result", color=VALUE, font_size=18, direction=UP)
        b2 = brace_note(loss[4], r"policy: \ predict the search", color=SEARCH, font_size=18)
        with self.voiceover(
            "The whole algorithm is one loop. A single network looks at a position and outputs two things: a "
            "probability for each move, p, and a value, v, its estimate of who will win. <bookmark mark='a'/> It plays "
            "games against itself, choosing every move by a Monte Carlo tree search guided by the network itself. "
            "<bookmark mark='b'/> Every position played is saved with two labels: pi, the search's visit counts, "
            "and z, who eventually won. <bookmark mark='c'/> Then the network is trained on them: the value head to "
            "predict the result, the policy head to predict what the search chose, plus weight decay. "
            "<bookmark mark='d'/> And the improved network plays the next games."
        ) as vo:
            self.play(FadeIn(net))
            vo.wait_until("a")
            self.play(Create(arrs[0]), FadeIn(play))
            vo.wait_until("b")
            self.play(Create(arrs[1]), FadeIn(data), FadeIn(pil), FadeIn(zl))
            vo.wait_until("c")
            self.play(Create(arrs[2]), FadeIn(train), Write(loss), FadeIn(b1), FadeIn(b2))
            vo.wait_until("d")
            self.play(Create(arrs[3]), Indicate(net, color=AGENT))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def alphazero(self):
        rows = VGroup(
            label(r"search's visit counts $\boldsymbol\pi$ \ $\succ$ \ the network's own $\mathbf p$", font_size=28,
                  color=SEARCH),
            label(r"train $\mathbf p \to \boldsymbol\pi$: \ policy improvement", font_size=28, color=AGENT),
            label(r"train $v \to z$: \ policy evaluation", font_size=28, color=VALUE),
            label(r"chapter 4's policy iteration, \ with search as the improvement step", font_size=28, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-2.3, 1.2, 0])
        az = history_card(2017, r"AlphaZero", r"the same algorithm, unchanged, for chess, shogi and Go: \ beat the "
                          r"strongest programs, Stockfish and Elmo, within hours of starting from random play; \ "
                          r"searching $60$ thousand chess positions a second to Stockfish's $60$ million",
                          width=6.6, color=AGENT).move_to([3.2, -1.8, 0])
        cite_ = cite(r"Silver et al., \textit{Science} (2018); \ see also Anthony, Tian \& Barber, \textit{Expert "
                     r"Iteration} (2017)")
        with self.voiceover(
            "Why does this work? The search, guided by the network, is a better player than the network alone: its "
            "visit counts are a better policy than the network's raw probabilities. <bookmark mark='a'/> So training "
            "the network to imitate the search improves the policy, <bookmark mark='b'/> and training the value head "
            "on game results evaluates it. <bookmark mark='c'/> It is policy iteration from chapter four, with search "
            "doing the improvement and a neural network holding both the policy and its value. Each generation's "
            "network makes the next generation's search stronger. <bookmark mark='d'/> In December 2017 the same "
            "algorithm, with nothing changed but the rules, learned chess and shogi too, and beat the strongest "
            "programs within hours. In chess it looked at sixty thousand positions a second, a thousandth of what "
            "Stockfish needed: the network's judgment replaced brute force."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(az, shift=UP * 0.2), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        g = load("az_grade")
        gens = list(g["gens"])
        spec = VGroup(
            label(rf"a residual network: \ ${BLOCKS}$ blocks of ${CHANNELS}$ channels", font_size=26),
            label(rf"${SIMS}$ simulations per move", font_size=26),
            label(rf"${GAMES_PER_GEN}$ games per generation, \ ${gens[-1]}$ generations", font_size=26),
            label(rf"about ${g['hours']:.1f}$ hours on this computer's $4$ CPU cores", font_size=26, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([2.6, 0.3, 0])
        board = C4View(cell=0.6, center=[-3.6, 0.2, 0])
        head = label(r"our own AlphaZero: \ Connect Four", font_size=34, color=AGENT).to_edge(UP, buff=0.5)
        judge = label(r"and a perfect judge: \ Connect Four is solved, \ so every move can be graded", font_size=24,
                      color=SEARCH).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Now we do it ourselves, at toy scale, on this computer. The game is Connect Four. "
            f"<bookmark mark='a'/> The network is small, {BLOCKS} residual blocks; each move gets {SIMS} simulations "
            f"of search; each generation plays {GAMES_PER_GEN} games against itself and then trains on them. "
            f"{gens[-1]} generations took about {g['hours']:.0f} hours. <bookmark mark='b'/> And unlike Go, Connect Four "
            "is solved: a perfect player exists, so we can grade every move the network makes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(board))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in spec], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(judge))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def prior_replay(self):
        d = load("az_demo")
        seq = list(d["seq"])
        P = np.asarray(d["prior_all"])
        V = np.asarray(d["value_all"])
        gens = list(d["all_gens"])
        truth = np.asarray(d["truth"])
        best = np.nanmax(truth)
        board = C4View(cell=0.62, center=[-2.6, -0.9, 0]).play_moves(seq)
        k = ValueTracker(0)

        def bars():
            i = min(int(k.get_value()), len(gens) - 1)
            return board.bars(P[i], color=PRIOR, height=1.7, vmax=1.0)

        live = always_redraw(bars)
        ok = [None if np.isnan(v) else bool(np.sign(v) == np.sign(best)) for v in truth]
        marks = board.column_marks(ok, font_size=22)
        gl = always_redraw(lambda: label(rf"generation ${gens[min(int(k.get_value()), len(gens) - 1)]}$", font_size=30,
                                         color=AGENT).move_to([3.6, 2.3, 0]))
        vl = always_redraw(lambda: MathTex(rf"v = {V[min(int(k.get_value()), len(gens) - 1)]:+.2f}", font_size=34,
                                           color=VALUE).move_to([3.6, 1.4, 0]))
        who = "yellow" if len(seq) % 2 == 0 else "red"
        tv = int(np.sign(best))
        verdict = {1: "wins", 0: "draws", -1: "loses"}[tv]
        exp = label(rf"truth: \ {who}, to move, \ {verdict} with perfect play", font_size=22, color=GREY_A)
        exp.move_to([3.6, 0.7, 0])
        key = VGroup(label(r"bars: \ the network's probability for each column", font_size=20, color=PRIOR),
                     label(r"marks: \ the solver's verdict on each column", font_size=20, color=GREY_A))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.6, -1.0, 0])
        top_ok = bool(ok[int(np.argmax(P[-1]))])
        sure = np.sign(V[-1]) == tv and abs(V[-1]) > 0.5
        if top_ok and sure:
            end = ("and settles on the right columns, while the value, its estimate of who wins, becomes confident "
                   "and correct.")
        elif top_ok:
            end = ("and settles on the right columns; the value, its estimate of who wins, stays less sure: "
                   f"{V[-1]:+.2f}.")
        else:
            end = ("but even the final network's favourite column here is not a right one: its instinct is still "
                   "wrong in this position, and only search can rescue it.")
        with self.voiceover(
            "Here is the training, replayed through one position. Above each column, the network's probability for "
            "playing there, before any search. Below, the perfect solver's verdict: a tick for the moves that keep "
            "the best result. "
            "<bookmark mark='a'/> In generation zero the network is untrained: nearly flat bars, and a value of "
            f"{V[0]:+.2f}. <bookmark mark='b'/> Watch the generations go by. The probability moves around, as the "
            "network's understanding changes, " + end
        ) as vo:
            self.play(FadeIn(board), FadeIn(marks), FadeIn(key))
            self.add(live, gl, vl)
            self.play(FadeIn(exp))
            vo.wait_until("b")
            self.play(k.animate.set_value(len(gens) - 1), run_time=max(8.0, vo.remaining() - 1.0), rate_func=linear)
        live.clear_updaters()
        gl.clear_updaters()
        vl.clear_updaters()
        self.wait(0.3)
        # search improves the policy: the final network's raw prior against its search's visits
        vis = np.asarray(d["visits"])[-1]
        b2 = board.bars(vis, color=SEARCH, height=1.7, vmax=1.0)
        for b_, b1 in zip(b2, live):
            b_.next_to(b1, RIGHT, buff=0.0).align_to(b1, DOWN)
            b_.stretch_to_fit_width(b1.width / 2).align_to(b1, RIGHT)
        cap = label(rf"with search: \ the {SIMS} simulations' visit shares", font_size=20, color=SEARCH)
        cap.next_to(key, DOWN, buff=0.15).align_to(key, LEFT)
        win = [c for c in range(7) if ok[c]]
        p_win, v_win = float(np.sum(P[-1][win])), float(np.sum(vis[win]))
        if v_win > p_win + 0.05:
            said = (f"And search sharpens it. In orange-gold, where the final network's search spends its {SIMS} "
                    f"simulations from this position: {100 * v_win:.0f} percent on winning columns, against "
                    f"{100 * p_win:.0f} percent for the network's first instinct. That gap, between instinct and "
                    "search, is what the next generation learns from.")
        else:
            said = (f"In orange-gold, where the final network's search spends its {SIMS} simulations from this "
                    f"position: {100 * v_win:.0f} percent on winning columns, close to the network's own "
                    f"{100 * p_win:.0f}. Here the instinct is already as good as the search; the gap between them, "
                    "where there is one, is what the next generation learns from.")
        with self.voiceover(said) as vo:
            self.play(*[b_.animate.stretch_to_fit_width(b_.width / 2).align_to(b_, LEFT) for b_ in live], run_time=0.6)
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b2], lag_ratio=0.1), FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def strength(self):
        g = load("az_grade")
        e = load("az_elo")
        gens = np.asarray(g["gens"])
        raw, mc, va = np.asarray(g["raw"]), np.asarray(g["mcts"]), np.asarray(g["value_acc"])
        u = load("uct")
        G = int(gens[-1])
        a1 = axes([0, G], [0, 1], x_length=5.6, y_length=3.4, xlabel=r"generation",
                  ylabel=r"right moves, \ $400$ test positions", xticks=[0, G // 2, G], yticks=[0, 0.5, 1],
                  yfmt=lambda v: rf"{int(100 * v)}\%", center=[-3.3, 0.2, 0])
        lr = curve(a1.ax, gens, raw, RAW, 3)
        lm = curve(a1.ax, gens, mc, WITH_SEARCH, 4)
        best_uct = float(np.max(u["acc"]))
        uct_sims = int(np.asarray(u["sims"])[int(np.argmax(u["acc"]))])
        lu = DashedLine(a1.ax.c2p(0, best_uct), a1.ax.c2p(G, best_uct), color=GREY_B, dash_length=0.08)
        ul = label(rf"plain MCTS, ${uct_sims:,}$ sims: \ ${100 * best_uct:.0f}\%$".replace(",", "{,}"), font_size=18,
                   color=GREY_B)
        ul.next_to(lu, DOWN, buff=0.05).align_to(lu, RIGHT)
        lg = legend([(RAW, r"network alone"), (WITH_SEARCH, rf"network $+$ {SIMS} sims")], font_size=18)
        lg.next_to(a1.ax, DOWN, buff=0.8).align_to(a1.ax, LEFT)
        names, elo = list(e["names"]), np.asarray(e["elo"])
        ag = [int(n.split()[1]) for n in names if n.startswith("gen")]
        ae = [elo[names.index(f"gen {x}")] for x in ag]
        top = float(max(elo)) + 100
        a2 = axes([0, G], [-200, top], x_length=5.6, y_length=3.4, xlabel=r"generation", ylabel=r"Elo rating",
                  xticks=[0, G // 2, G], yticks=[0, int(round(top / 400.0)) * 400 // 2, int(round(top / 400.0)) * 400],
                  center=[3.3, 0.2, 0])
        le = curve(a2.ax, ag, ae, AGENT, 4)
        pe = VGroup(*[Dot(a2.ax.c2p(x, y), radius=0.06, color=AGENT) for x, y in zip(ag, ae)])
        mcl = VGroup()
        for n in names:
            if n.startswith("MCTS"):
                y = elo[names.index(n)]
                mcl.add(DashedLine(a2.ax.c2p(0, y), a2.ax.c2p(G, y), color=GREY_B, dash_length=0.06))
                mcl.add(label(n.replace("MCTS", r"plain MCTS,"), font_size=16, color=GREY_B)
                        .next_to(a2.ax.c2p(G, y), LEFT, buff=0.05).shift(UP * 0.15))
        tag = note(rf"computed: \ ratings from a round robin, \ ${int(e['games'].sum() / 2)}$ games").to_corner(DR, buff=0.2)
        final_raw, final_mc = 100 * raw[-1], 100 * mc[-1]
        gap = elo[names.index(f"gen {ag[-1]}")]
        mc1000 = elo[names.index("MCTS 1000")]
        # how many plain-MCTS simulations (random playouts) buy the same accuracy: log-linear along its curve
        us, ua = np.log10(np.asarray(u["sims"], float)), np.asarray(u["acc"])
        if final_mc > 100 * best_uct:
            vs_uct = (f"That is beyond the {100 * best_uct:.0f} percent plain MCTS reaches with any number of "
                      "simulations: random playouts can't buy what a learned judge knows.")
        else:
            k = int(np.argmax(ua >= mc[-1]))
            lg_need = us[k - 1] + (mc[-1] - ua[k - 1]) / (ua[k] - ua[k - 1]) * (us[k] - us[k - 1]) if k else us[0]
            need = int(round(10 ** lg_need, -1))
            vs_uct = (f"Plain MCTS, judging by random playouts, needs about {need:,} simulations to do as well: each "
                      f"simulation guided by the network is worth about {need / SIMS:.0f} random ones.")
        ups = int(np.sum(np.diff(ae) > 0))
        climb = ("each generation we rated is stronger than the one before" if ups == len(ae) - 1 else
                 f"the ratings climb, with the odd step back ({ups} of {len(ae) - 1} steps go up)")
        if gap - mc1000 > 100:
            rel = f"and {gap - mc1000:.0f} points above plain MCTS with a thousand simulations a move."
        elif gap > mc1000:
            rel = "and a little above plain MCTS with a thousand simulations a move."
        else:
            rel = "though still below plain MCTS with a thousand simulations a move."
        with self.voiceover(
            "Graded on four hundred test positions, generation by generation. <bookmark mark='a'/> The network alone, "
            f"with no search at all, goes from random to choosing a right move, one that keeps the win or the draw, "
            f"{final_raw:.0f} percent of the time; <bookmark mark='b'/> with its {SIMS} simulations of search, "
            f"{final_mc:.0f} percent. <bookmark mark='c'/> {vs_uct} <bookmark mark='d'/> And in head-to-head games, "
            "rated like chess "
            f"players, {climb}: the final generation is about {gap:.0f} Elo points above the untrained network, {rel}"
        ) as vo:
            self.play(FadeIn(a1), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lr), FadeIn(lg[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(lm), FadeIn(lg[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(lu), FadeIn(ul))
            vo.wait_until("d")
            self.play(FadeIn(a2), FadeIn(mcl))
            self.play(Create(le), LaggedStart(*[FadeIn(p) for p in pe], lag_ratio=0.1), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def games(self):
        d = load("az_demo")
        G = d["games"]
        keys = sorted(G, key=int)
        n0 = len(d["game_start"])
        board = C4View(cell=0.6, center=[-2.4, -0.3, 0])
        sub = label(r"the same position each time: \ only one move keeps the win", font_size=22, color=GREY_A)
        sub.next_to(board, DOWN, buff=0.25)
        first, last = G[keys[0]], G[keys[-1]]
        f_ok, l_ok = sum(first["perfect"]), sum(last["perfect"])
        with self.voiceover(
            "Finally, watch it play out a position where only one move keeps the win, against itself, at different "
            "stages, every move checked by the solver: green for a right move, red for a mistake that gives away a "
            f"win or a draw. <bookmark mark='a'/> Generation {keys[0]} gets {f_ok} of its "
            f"{len(first['perfect'])} moves right. <bookmark mark='b'/> Generation {keys[-1]}, {l_ok} of "
            f"{len(last['perfect'])}."
        ) as vo:
            self.play(FadeIn(board), FadeIn(sub))
            for gi, key in enumerate(keys):
                game = G[key]
                moves, ok = list(game["moves"]), list(game["perfect"])
                head = label(rf"generation {key}", font_size=30, color=AGENT).move_to([3.4, 2.6, 0])
                n_ok = sum(ok)
                stat = label(rf"right: \ ${n_ok}$ of ${len(ok)}$ moves", font_size=24,
                             color=REWARD if n_ok == len(ok) else GREY_A).move_to([3.4, 1.9, 0])
                dots = VGroup()
                self.play(FadeIn(head))
                k0 = len(board.stones)
                board.play_moves(moves[:n0])
                self.play(FadeIn(VGroup(*board.stones[k0:])), run_time=0.5)
                anims = []
                player = 1 if n0 % 2 == 0 else -1
                for c in moves[n0:]:
                    anims.append(board.drop(c, player, run_time=0.18))
                    player = -player
                self.play(Succession(*anims), run_time=0.25 * max(len(moves) - n0, 1))
                for j, o in enumerate(ok):
                    dots.add(Dot(radius=0.07, color=REWARD if o else PENALTY))
                dots.arrange_in_grid(cols=12, buff=0.08).move_to([3.4, 1.1, 0])
                self.play(FadeIn(stat), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.03), run_time=1.0)
                if gi == 0:
                    vo.wait_until("a")
                if gi == len(keys) - 2:
                    vo.wait_until("b")
                self.wait(0.4)
                self.play(FadeOut(VGroup(head, stat, dots)), FadeOut(board.stones), run_time=0.4)
                board.stones.remove(*board.stones.submobjects)
                board.stone_at = {}
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        rows = VGroup(
            label(r"self-play: \ an opponent exactly as strong as you, \ always", font_size=28, color=AGENT),
            label(r"search: \ a teacher one step ahead of the student", font_size=28, color=SEARCH),
            label(r"a value network: \ the judge Go programs never had", font_size=28, color=VALUE),
            label(r"TD-Gammon's three ideas, \ plus search", font_size=28, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 0.2)
        with self.voiceover(
            "Three ingredients made it work. Self-play, which always provides an opponent of exactly the right "
            "strength. <bookmark mark='a'/> Search, which turns a network into a slightly better teacher for "
            "itself. <bookmark mark='b'/> And a learned value function, the judge that Go programs had lacked for "
            "decades. <bookmark mark='c'/> It's TD-Gammon's recipe from 1992, plus search."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.wait(0.3)
        self.clear_scene()
