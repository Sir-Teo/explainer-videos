from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import FAIL, FCOL, GCOST, HEUR, HIST, LEARN, MAXC, MINC, PART, PATH, SYMBOL, load, node_box

FEATURE_TEX = [r"one in a line", r"two in a line", r"three in a line", r"centre column", r"safe threats"]
FEATURE_WORDS = ["lone stones in open lines", "pairs in open lines", "threes in open lines", "stones in the centre",
                 "threats the opponent can't block at once"]



class Samuel(VoiceoverScene):
    def construct(self):
        self.card()
        self.samuel()
        self.rule()
        self.replay()
        self.verdict()
        self.deep_blue()
        self.solved()

    def card(self):
        card = chapter_card(7, r"Machines that learned to play", r"Can a program learn to play better than its "
                            r"programmer?", lit=(1959, 1997), part=PART)
        with self.voiceover("Chapter seven. Machines that learned to play."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def samuel(self):
        hc = history_card(1959, r"Arthur Samuel, IBM: \ \textit{Some Studies in Machine Learning Using the Game of "
                          r"Checkers}", r"``a computer can be programmed so that it will learn to play a better game of "
                          r"checkers than can be played by the person who wrote the program''", width=8.6,
                          color=HIST, font_size=21).to_edge(UP, buff=0.35)
        poly = cmath(r"V(s)", r"=", r"w_1 f_1(s) + w_2 f_2(s) + \dots + w_k f_k(s)", font_size=40)
        poly[0].set_color(LEARN)
        poly.move_to(UP * 0.3)
        pl = label(r"a scoring polynomial: \ features of the board \ (piece advantage, \ mobility, \ control of the "
                   r"centre, \dots), \ weighted", font_size=22, color=GREY_A).next_to(poly, DOWN, buff=0.25)
        if pl.width > 12.8:
            pl.width = 12.8
        facts = VGroup(label(r"an IBM 704; \ look a few moves ahead, \ score the positions with $V$", font_size=22,
                             color=GCOST),
                       label(r"$16$ terms in use, \ chosen from a reserve of $38$", font_size=22, color=GCOST))
        facts.arrange(DOWN, buff=0.12).next_to(pl, DOWN, buff=0.35)
        nealey = VGroup(
            history_card(1962, r"beats Robert Nealey, \ a Connecticut player", r"a famous win, \ though Nealey took the "
                         r"rematch: \ one win, \ five draws", width=4.8, color=PATH, font_size=18),
            history_card(1966, r"loses all eight games", r"to the world champions Walter Hellman and Derek Oldbury",
                         width=4.8, color=FAIL, font_size=18)).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "In 1959 Arthur Samuel of IBM published a checkers program with a striking claim: that a computer can be programmed "
            "so that it will learn to play a better game of checkers than can be played by the person who wrote the program. "
            "<bookmark mark='a'/> It searched a few moves ahead and scored positions with a weighted sum of board features: a "
            "scoring polynomial. <bookmark mark='b'/> What was new: it adjusted the weights itself, by playing. "
            "<bookmark mark='c'/> In 1962 it beat a Connecticut player, Robert Nealey, in a famous game; Nealey won the rematch, "
            "and in 1966 the program lost all eight games against the world champions. But the idea mattered, and Samuel helped "
            "popularize the very words machine learning."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Write(poly), FadeIn(pl))
            vo.wait_until("b")
            self.play(FadeIn(facts))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in nealey], lag_ratio=0.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rule(self):
        t = {"children": [{"children": [{"children": []}, {"children": []}]}, {"children": [{"children": []},
                                                                                         {"children": []}]}]}
        tree = SearchTree(t, width=3.4, level_height=1.0, radius=0.12, center=[3.8, 1.2, 0])
        then = Dot([-4.6, 1.2, 0], radius=0.16, color=LEARN)
        tl = label(r"your last position: \\ static score $V(s_{\text{then}})$", font_size=22, color=LEARN)
        tl.next_to(then, DOWN, buff=0.25)
        now_l = label(r"now: \ the score that search \\ backs up, \ $V_{\text{search}}(s_{\text{now}})$", font_size=22,
                      color=FCOL).next_to(tree, DOWN, buff=0.25)
        arrow = Arrow(then.get_right(), tree.nodes[0].get_left(), buff=0.25, color=GREY_B)
        al = label(r"two moves later", font_size=20, color=GREY_B).next_to(arrow, UP, buff=0.08)
        rows = [
            cmath(r"\delta", r"=", r"V_{\text{search}}(s_{\text{now}}) - V(s_{\text{then}})", font_size=36),
            cmath(r"w", r"\leftarrow", r"w + \eta\, \delta\, \nabla_w V(s_{\text{then}})", font_size=36),
        ]
        rows[0][0].set_color(FCOL)
        rows[1][0].set_color(LEARN)
        whys = [why(r"Samuel's delta: \ how wrong the old score was"), why(r"nudge the weights toward what search found")]
        step = ladder(self, rows, whys, keep=2, top=-1.3, x=-2.2)
        td = label(r"modern semi-gradient analogue: \ temporal-difference learning \ (Part 26)", font_size=22, color=PATH)
        td.to_edge(DOWN, buff=0.25)
        ab = label(r"Alpha learns; \ Beta keeps its weights; \ when Alpha wins, \ Beta copies Alpha", font_size=22,
                   color=GREY_A).to_edge(UP, buff=0.35)
        pair = VGroup(node_box(r"Alpha: \ learns", LEARN, font_size=30), node_box(r"Beta: \ fixed weights", GREY_B,
                                                                                    font_size=30))
        pair.arrange(RIGHT, buff=2.4).move_to(UP * 0.3)
        vs = DoubleArrow(pair[0].get_right(), pair[1].get_left(), buff=0.2, color=GREY_B)
        pair.add(vs, label(r"self-play", font_size=22, color=GREY_B).next_to(vs, UP, buff=0.1))
        with self.voiceover(
            "Samuel's delta idea is a seed of modern reinforcement learning. We write a modern semi-gradient analogue here; "
            "his original program adjusted sign correlations and quantized coefficients instead. <bookmark mark='a'/> Keep the static score "
            "your evaluation gave your previous position. <bookmark mark='b'/> Two moves later, search from the new position "
            "and back up a score: a better-informed opinion of the same game. <bookmark mark='c'/> The difference, Samuel's "
            "delta, says how wrong the old score was. <bookmark mark='d'/> Nudge the weights to shrink it. "
            "<bookmark mark='e'/> Two copies played: Alpha learned, Beta kept its weights, and when Alpha won, Beta took them. "
            "Richard Sutton built on this idea when he formalized temporal-difference learning in 1988."
        ) as vo:
            self.play(FadeIn(ab), FadeIn(pair))
            vo.wait_until("a")
            self.play(FadeOut(pair), run_time=0.5)
            self.play(FadeIn(then), FadeIn(tl))
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(al), Create(tree.edge_group), FadeIn(tree.nodes), FadeIn(now_l))
            vo.wait_until("c")
            step(0)
            vo.wait_until("d")
            step(1)
            vo.wait_until("e")
            self.play(FadeIn(td))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        d = load("samuel")
        runs = d["runs"]
        run = runs[0]
        W = np.asarray(run["weights"])  # every 10 games
        n = len(W)
        wmax = max(np.abs(W).max(), np.abs(np.asarray(d["programmer"])).max()) * 1.1
        k = ValueTracker(0)
        bar_h = 3.0
        base_y = -0.6
        xs = np.linspace(-5.6, -1.4, len(FEATURE_TEX))

        def bars():
            i = int(np.clip(k.get_value(), 0, n - 1))
            g = VGroup()
            for j, x in enumerate(xs):
                v = W[i, j]
                h = max(abs(v) / wmax * bar_h / 2, 0.01)
                r = Rectangle(width=0.55, height=h, stroke_width=0, fill_color=LEARN if v >= 0 else FAIL,
                              fill_opacity=0.9)
                r.move_to([x, base_y + (h / 2 if v >= 0 else -h / 2), 0])
                g.add(r)
            return g

        live = always_redraw(bars)
        axis = Line([-6.0, base_y, 0], [-1.0, base_y, 0], color=GREY_C, stroke_width=1.5)
        prog = VGroup(*[Line([x - 0.36, base_y + d["programmer"][j] / wmax * bar_h / 2, 0],
                             [x + 0.36, base_y + d["programmer"][j] / wmax * bar_h / 2, 0], color=HEUR, stroke_width=4)
                        for j, x in enumerate(xs)])
        names = VGroup(*[label(t, font_size=17, color=GREY_A).rotate(PI / 6).move_to([x - 0.1, base_y - 1.95, 0])
                         for t, x in zip(FEATURE_TEX, xs)])
        wl = label(r"Alpha's weights", font_size=24, color=LEARN).move_to([-3.5, 2.6, 0])
        pl = label(r"\textemdash\ our hand-set weights", font_size=20, color=HEUR).next_to(wl, DOWN, buff=0.12)
        gnum = DecimalNumber(0, num_decimal_places=0, group_with_commas=True, font_size=30, color=LEARN)
        gnum.add_updater(lambda m: m.set_value(10 * int(np.clip(k.get_value(), 0, n - 1))))
        glab = VGroup(label(r"games played", font_size=22, color=GREY_A), gnum).arrange(RIGHT, buff=0.2)
        glab.move_to([-3.5, -3.3, 0])
        gnum.add_updater(lambda m: m.next_to(glab[0], RIGHT, buff=0.2))
        ck = np.asarray(run["ckpt"])
        G = int(d["games"])
        g = axes([0, G], [0, 1], x_length=5.4, y_length=3.6, xlabel=r"games of self-play",
                 ylabel=r"score \ (win $1$, draw $\tfrac12$)", xticks=[0, G // 2, G], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{int(v):,}".replace(",", "{,}"), center=[3.6, 0.2, 0])
        half = DashedLine(g.ax.c2p(0, 0.5), g.ax.c2p(G, 0.5), color=GREY_C, dash_length=0.08)
        c_zero = curve(g.ax, ck, run["vs_zero"], PATH, 3)
        c_prog = curve(g.ax, ck, run["vs_programmer"], HEUR, 3)
        lg = legend([(PATH, r"against the untrained player"), (HEUR, r"against our hand-set weights")],
                    font_size=18).next_to(g, UP, buff=0.1)
        fin = W[-1]
        top = FEATURE_WORDS[int(np.argmax(fin))]
        npos = int((fin > 0).sum())
        signs = f"The largest weight ends up on {top}, and {npos} of the five features count in its favour."
        tag = note(rf"computed: \ Connect Four, \ ${d['depth']}$-move search, \ run 1 of ${len(runs)}$; \ "
                   rf"${d['n_eval_games']}$ games per point").to_corner(DR, buff=0.15)
        with self.voiceover(
            "We gave Samuel's method a game of our own: Connect Four, five features a programmer might choose, and a search three "
            "moves deep. Alpha starts with every weight zero. <bookmark mark='a'/> Here are its weights as it plays; in orange, "
            f"the weights we set by hand before training. <bookmark mark='b'/> Over {G:,} games against Beta, the weights find "
            f"their places. {signs} <bookmark mark='c'/> At intervals we froze Alpha and played it against two fixed "
            "opponents: the untrained player, and our hand-set weights."
        ) as vo:
            self.add(live)
            self.play(Create(axis), FadeIn(names), FadeIn(wl), FadeIn(glab), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(prog), FadeIn(pl))
            vo.wait_until("b")
            self.play(FadeIn(g), Create(half))
            self.play(k.animate.set_value(n - 1), Create(c_zero), Create(c_prog), run_time=9.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(lg))
        live.clear_updaters()
        gnum.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def verdict(self):
        d = load("samuel")
        runs = d["runs"]
        last = lambda key: [float(np.mean(r[key][-3:])) for r in runs]  # the last three checkpoints of each run
        vz, vp, acc = last("vs_zero"), last("vs_programmer"), last("accuracy")
        a0, ap = d["acc_zero"], d["acc_programmer"]
        rows = VGroup(
            label(rf"against the untrained player: \ ${min(vz):.2f}$ to ${max(vz):.2f}$", font_size=26, color=PATH),
            label(rf"against our hand-set weights: \ ${min(vp):.2f}$ to ${max(vp):.2f}$", font_size=26, color=HEUR),
            label(rf"moves that keep the win or draw, \ on ${len(load('testset')['histories'])}$ solved positions:",
                  font_size=24, color=GREY_A),
            label(rf"untrained ${100 * a0:.0f}\%$, \ hand-set ${100 * ap:.0f}\%$, \ learned ${100 * min(acc):.0f}$"
                  rf"--${100 * max(acc):.0f}\%$", font_size=26, color=FCOL),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        if rows.width > 6.6:
            rows.width = 6.6
        rows.move_to([-3.3, 0.2, 0])
        sc = axes([0, 2], [0, 1], x_length=4.4, y_length=3.0, ylabel=r"score per game \ (win 1, draw $\tfrac12$)",
                  yticks=[0, 0.5, 1], center=[3.9, 0.0, 0])
        half = DashedLine(sc.ax.c2p(0, 0.5), sc.ax.c2p(2, 0.5), color=GREY_B, dash_length=0.08)
        sbars = VGroup()
        for gi, (vals, col) in enumerate(((vz, PATH), (vp, HEUR))):
            grp = VGroup()
            for ri, v in enumerate(vals):
                x = gi + 0.25 + 0.25 * ri
                bh = max(sc.ax.c2p(0, v)[1] - sc.ax.c2p(0, 0)[1], 0.01)
                grp.add(Rectangle(width=0.2, height=bh, stroke_width=0, fill_color=col, fill_opacity=0.85)
                        .move_to(sc.ax.c2p(x, 0), aligned_edge=DOWN))
            grp.add(label([r"vs untrained", r"vs hand-set"][gi], font_size=20, color=col)
                    .next_to(sc.ax.c2p(gi + 0.5, 0), DOWN, buff=0.15))
            sbars.add(grp)
        sl = label(r"one bar per run", font_size=18, color=GREY_B).next_to(sc, DOWN, buff=0.45)
        head = label(rf"after ${d['games']:,}$ games, \ {len(runs)} runs \ (mean of the last three checkpoints)"
                     .replace(",", "{,}"), font_size=26, color=GREY_A).to_edge(UP, buff=0.5)
        tag = note(r"computed: \ positions scored by Part 26's perfect solver").to_corner(DR, buff=0.2)
        beat_beginner = min(vz) > 0.5
        beat_prog = min(vp) > 0.5
        tie_prog = max(vp) >= 0.5 and not beat_prog
        if beat_beginner and beat_prog:
            v = ("Every run beats both opponents: on this game, Samuel's claim holds. It learned to play better than "
                 "the weights its programmers wrote.")
        elif beat_beginner and tie_prog:
            v = ("Every run beats the untrained player. Against our hand-set weights the runs come out roughly even, "
                 "some ahead, some behind: it learned, from nothing, to play about as well as its programmers' guess.")
        elif beat_beginner:
            v = ("Every run beats the untrained player, but none beats our hand-set weights: it learned a lot, but "
                 "not, here, to play better than its programmers' own guess.")
        else:
            v = ("Here the learner does not reliably beat even the untrained player; the scores swing from checkpoint "
                 "to checkpoint, as Samuel found his own program could wander.")
        acc_v = (f"Graded against a perfect solver, its moves keep the win or the draw {100 * min(acc):.0f} to "
                 f"{100 * max(acc):.0f} percent of the time, against {100 * a0:.0f} untrained and {100 * ap:.0f} for "
                 "the hand-set weights.")
        with self.voiceover(
            f"After {d['games']:,} games, in each of {len(runs)} runs: <bookmark mark='a'/> " + v +
            " <bookmark mark='b'/> " + acc_v + " The curves were not smooth: Samuel saw his program wander too, and "
            "sometimes had to reset it by hand."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(sc), Create(half))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), *[GrowFromEdge(b, DOWN) for g_ in sbars for b in g_[:-1]],
                      *[FadeIn(g_[-1]) for g_ in sbars], FadeIn(sl))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def deep_blue(self):
        hc = history_card(1997, r"IBM's Deep Blue beats Garry Kasparov, \ $3\tfrac12$--$2\tfrac12$, \ New York",
                          r"after losing to him $4$--$2$ in $1996$", width=7.6, color=MAXC, font_size=22)
        hc.to_edge(UP, buff=0.35)
        specs = VGroup(
            label(r"$30$ processors \ $+$ \ $480$ chess chips built for the job", font_size=26, color=GCOST),
            label(r"alpha--beta search: \ $126$ million positions a second on average", font_size=26, color=GCOST),
            label(r"an evaluation of about $8{,}000$ features, \ almost all created and tuned by hand", font_size=26,
                  color=HEUR),
            label(r"an opening book written by grandmasters; \ endgame databases", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(DOWN * 0.3)
        cite_ = cite(r"Campbell, Hoane \& Hsu, \textit{Deep Blue}, \textit{Artificial Intelligence} (2002)")
        recipe = label(r"search, \ plus a human-designed sense of a good position", font_size=28, color=FCOL)
        recipe.to_edge(DOWN, buff=0.8)
        ways = VGroup(node_box(r"more search", GCOST, font_size=32), node_box(r"more hand-crafted knowledge", HEUR,
                                                                               font_size=32))
        ways.arrange(RIGHT, buff=0.6).move_to(DOWN * 0.3)
        with self.voiceover(
            "Chess went the other way: more search, more hand-crafted knowledge. <bookmark mark='a'/> In 1996 Garry Kasparov "
            "beat IBM's Deep Blue four games to two, and the team doubled the machine. <bookmark mark='b'/> In the 1997 rematch "
            "it ran four hundred and eighty custom chess chips, averaging a hundred and twenty-six million positions a second, "
            "with an evaluation of about eight thousand features, almost all tuned by hand. It won three and a half to two and "
            "a half. <bookmark mark='c'/> Search plus a human-designed sense of a good position: Shannon's recipe of 1950, at "
            "enormous scale."
        ) as vo:
            self.play(FadeIn(cite_), LaggedStart(*[FadeIn(w_, shift=UP * 0.1) for w_ in ways], lag_ratio=0.5))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(ways), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.1) for s_ in specs], lag_ratio=0.35))
            vo.wait_until("c")
            self.play(FadeIn(recipe))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def solved(self):
        cards = VGroup(
            history_card(1994, r"Chinook \ (Jonathan Schaeffer, Alberta)", r"the first program to win a human world "
                         r"championship, \ at checkers", width=5.8, color=MAXC, font_size=20),
            history_card(2007, r"\textit{Checkers Is Solved} \ (Schaeffer et al., \textit{Science})", r"about "
                         r"$5 \times 10^{20}$ positions: \ with perfect play, \ a draw", width=5.8, color=PATH,
                         font_size=20),
        ).arrange(DOWN, buff=0.35).move_to([-3.2, 0.2, 0])
        right = VGroup(label(r"Samuel's checkers, \ $1959$", font_size=26, color=LEARN),
                       MathTex(r"\downarrow", font_size=40),
                       label(r"solved, \ $2007$", font_size=26, color=PATH),
                       MathTex(r"\downarrow", font_size=40),
                       label(r"and Go, \ the game no evaluation could capture: \\ AlphaGo, \ $2016$ \ (Part 26)",
                             font_size=24, color=GREY_A)).arrange(DOWN, buff=0.2).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Checkers itself was finished off by search. <bookmark mark='a'/> Jonathan Schaeffer's Chinook became the first "
            "program to win a human world championship, in 1994. <bookmark mark='b'/> In 2007 his team proved that checkers, "
            "with about five times ten to the twenty positions, is a draw with perfect play. <bookmark mark='c'/> The game that "
            "resisted the recipe was Go, where nobody could write down a good evaluation. That took a learned one: Part 26."
        ) as vo:
            fin = label(r"checkers, \\ finished off by search", font_size=40, color=GREY_A).move_to([-3.4, 0.2, 0])
            self.play(FadeIn(right[0]), FadeIn(fin))
            vo.wait_until("a")
            self.play(FadeOut(fin), run_time=0.4)
            self.play(FadeIn(cards[0], shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.15), FadeIn(right[1]), FadeIn(right[2]))
            vo.wait_until("c")
            self.play(FadeIn(right[3]), FadeIn(right[4]))
        self.wait(0.3)
        self.clear_scene()
