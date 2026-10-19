from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai26.common import AGENT, EXPLORE, PART, PENALTY, REWARD, SEARCH, VALUE, axes, curve, load

CUR, AVG = C.ENTROPY, C.BITS  # the current strategy, the average strategy


def simplex_xy(p, center, size):
    """Barycentric (rock, paper, scissors) -> a point in an equilateral triangle."""
    A = np.array([0.0, size * 0.62])
    B = np.array([-size * 0.54, -size * 0.31])
    Cc = np.array([size * 0.54, -size * 0.31])
    xy = p[0] * A + p[1] * B + p[2] * Cc
    return np.array([center[0] + xy[0], center[1] + xy[1], 0.0])


class Beyond(VoiceoverScene):
    def construct(self):
        self.card()
        self.hidden()
        self.regret()
        self.cfr()
        self.poker()
        self.alphastar()
        self.exploits()
        self.algorithms()

    def card(self):
        card = chapter_card(15, r"Beyond perfect information", r"What if you can't see the other player's cards?",
                            lit=(2019,), part=PART)
        with self.voiceover("Chapter fifteen. Beyond perfect information."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def hidden(self):
        cards = VGroup()
        for k, (txt, col) in enumerate([("K", REWARD), ("?", GREY_B)]):
            box = RoundedRectangle(width=1.1, height=1.6, corner_radius=0.12, stroke_color=col, stroke_width=3,
                                   fill_color="#151A22", fill_opacity=1)
            cards.add(VGroup(box, Text(txt, font_size=48, color=col).move_to(box)))
        cards.arrange(RIGHT, buff=2.4).move_to(UP * 1.4)
        cl = VGroup(label(r"your card", font_size=22, color=GREY_A).next_to(cards[0], DOWN, buff=0.15),
                    label(r"theirs: \ hidden", font_size=22, color=GREY_A).next_to(cards[1], DOWN, buff=0.15))
        pts = VGroup(
            label(r"a position is no longer a state: \ you only know an information set", font_size=26),
            label(r"the best play must be random: \ always bet with a good hand, \ never with a bad one, \\ "
                  r"and your bets reveal your cards", font_size=26, color=EXPLORE),
            label(r"the goal: \ a Nash equilibrium, \ a strategy no opponent can exploit", font_size=26, color=VALUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 1.5)
        with self.voiceover(
            "Chess and Go show both players everything. Poker doesn't. <bookmark mark='a'/> You know your own card, "
            "not your opponent's, so you can't search a tree of positions: you only know which set of positions you "
            "might be in, an information set. <bookmark mark='b'/> And the best play is necessarily random. If you "
            "always bet with good hands and never with bad ones, your bets give your cards away; you have to bluff, "
            "with the right probability. <bookmark mark='c'/> The target is a Nash equilibrium: a strategy for each "
            "player such that neither can gain by changing alone. In a two-player zero-sum game, playing it "
            "guarantees you the game's value, against anyone."
        ) as vo:
            self.play(FadeIn(cards), FadeIn(cl))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def regret(self):
        d = load("rps")
        cur, avg = np.asarray(d["current"]), np.asarray(d["average"])
        ctr, size = np.array([-2.6, -0.3]), 5.6
        tri = Polygon(simplex_xy([1, 0, 0], ctr, size), simplex_xy([0, 1, 0], ctr, size), simplex_xy([0, 0, 1], ctr, size),
                      stroke_color=GREY_C, stroke_width=2)
        vl = VGroup(label(r"rock", font_size=24).next_to(simplex_xy([1, 0, 0], ctr, size), UP, buff=0.1),
                    label(r"paper", font_size=24).next_to(simplex_xy([0, 1, 0], ctr, size), DL, buff=0.1),
                    label(r"scissors", font_size=24).next_to(simplex_xy([0, 0, 1], ctr, size), DR, buff=0.1))
        nash = Dot(simplex_xy([1 / 3, 1 / 3, 1 / 3], ctr, size), radius=0.08, color=VALUE)
        nl = label(r"Nash: \ $\tfrac13, \tfrac13, \tfrac13$", font_size=22, color=VALUE).next_to(nash, DOWN, buff=0.12)
        T = len(cur)
        t = ValueTracker(1)

        def trail(P, col, width):
            def make():
                n = max(2, int(t.get_value()))
                idx = np.unique(np.round(np.geomspace(1, n, min(n, 400))).astype(int)) - 1
                pts = [simplex_xy(P[i], ctr, size) for i in idx]
                return VMobject(stroke_color=col, stroke_width=width).set_points_as_corners(pts)
            return make

        tc = always_redraw(trail(cur, CUR, 2))
        ta = always_redraw(trail(avg, AVG, 4))
        dc = always_redraw(lambda: Dot(simplex_xy(cur[int(t.get_value()) - 1], ctr, size), radius=0.07, color=CUR))
        da = always_redraw(lambda: glow_dot(simplex_xy(avg[int(t.get_value()) - 1], ctr, size), color=AVG, radius=0.07))
        rm = cmath(r"\sigma^{t+1}(a)", r"\propto", r"\max\big(0,\ R^t(a)\big)", font_size=34).move_to([3.6, 2.4, 0])
        rml = label(r"regret matching: \ play each action in proportion \\ to how much you regret not having "
                    r"played it", font_size=22, color=GREY_A).next_to(rm, DOWN, buff=0.2)
        th = theorem_card(r"regret minimization", r"in a two-player zero-sum game, if both players' average regret "
                          r"goes to $0$, \ their average strategies converge to a Nash equilibrium",
                          who=r"Hart \& Mas-Colell (2000); \ Zinkevich et al.\ (2007)", width=5.2,
                          color=VALUE).move_to([4.15, -0.6, 0])
        key = VGroup(label(r"current strategy", font_size=20, color=CUR), label(r"average strategy", font_size=20,
                                                                                color=AVG)).arrange(DOWN, aligned_edge=LEFT)
        key.move_to([3.6, -2.6, 0])
        tag = note(rf"computed: \ ${T:,}$ rounds of self-play".replace(",", "{,}")).to_corner(DR, buff=0.2)
        with self.voiceover(
            "The tool is regret. After each round, ask of every action: how much better would I have done had I "
            "played it every time so far? <bookmark mark='a'/> Regret matching plays each action in proportion to "
            "its positive regret. <bookmark mark='b'/> Here two regret matchers play rock-paper-scissors against each "
            "other, the triangle being all mixtures of the three. Their current strategies chase each other round "
            "and round: whatever one favours, the other learns to beat. <bookmark mark='c'/> But the average of their "
            "strategies spirals in to a third, a third, a third: the equilibrium. <bookmark mark='d'/> That's a "
            "theorem: in two-player zero-sum games, if each player's regret grows slower than the number of rounds, "
            "the average strategies approach a Nash equilibrium."
        ) as vo:
            self.play(Create(tri), FadeIn(vl), FadeIn(nash), FadeIn(nl), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(rm), FadeIn(rml))
            vo.wait_until("b")
            self.add(tc, dc, key[0])
            self.play(FadeIn(key[0]), t.animate.set_value(300), run_time=5.0, rate_func=linear)
            vo.wait_until("c")
            self.add(ta, da)
            self.play(FadeIn(key[1]), t.animate.set_value(T), run_time=6.0, rate_func=rate_functions.ease_in_sine)
            vo.wait_until("d")
            self.play(FadeIn(th, shift=UP * 0.2))
        for m in (tc, ta, dc, da):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cfr(self):
        d = load("kuhn")
        it = np.asarray(d["iters"], float)
        ex = np.asarray(d["exploitability"])
        val = np.asarray(d["value"])
        lx, ly = np.log10(it), np.log10(np.maximum(ex, 1e-6))
        g = axes([0, lx[-1]], [math.floor(ly.min()), 0], x_length=6.0, y_length=3.6,
                 xlabel=r"iterations of CFR (log scale)", ylabel=r"exploitability (log scale)",
                 xticks=list(range(0, int(lx[-1]) + 1)), yticks=list(range(math.floor(ly.min()), 1)), log_x=True,
                 yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-2.6, -0.4, 0])
        line = curve(g.ax, lx, ly, VALUE, 4)
        pts = VGroup(*[Dot(g.ax.c2p(x, y), radius=0.05, color=VALUE) for x, y in zip(lx, ly)])
        ref = DashedLine(g.ax.c2p(lx[3], ly[3]), g.ax.c2p(lx[-1], ly[3] - 0.5 * (lx[-1] - lx[3])), color=GREY_B,
                         dash_length=0.08)
        rl = label(r"$\propto 1 / \sqrt{T}$", font_size=22, color=GREY_B).next_to(ref.get_end(), DOWN, buff=0.15)
        kuhn = VGroup(label(r"Kuhn poker: \ $3$ cards (J, Q, K), \ one each,", font_size=22),
                      label(r"one round of check, bet, call or fold", font_size=22)).arrange(DOWN, aligned_edge=LEFT)
        kuhn.move_to([3.6, 2.4, 0])
        v = label(rf"game value for the first player: \ ${val[-1]:.4f}$ \ (exactly $-\tfrac{{1}}{{18}} = {-1 / 18:.4f}$)",
                  font_size=22, color=VALUE).move_to([3.6, 1.2, 0])
        if v.width > 6.6:
            v.width = 6.6
        bluff = d["strategy"].get("Jp") or d["strategy"].get("J-")
        cfr_c = definition_card(r"counterfactual regret minimization", r"regret matching at every information set, "
                                r"each weighted by how likely the opponent's play is to reach it", color=VALUE,
                                width=6.0, font_size=20, kind=r"Algorithm").move_to([3.6, -0.6, 0])
        tag = note(r"computed").to_corner(DR, buff=0.2)
        with self.voiceover(
            "For a card game, apply regret matching separately at every information set, every situation a player "
            "might be in, weighting each by how likely the opponent's play is to lead there. That's counterfactual "
            "regret minimization, CFR, from Martin Zinkevich and colleagues in 2007. <bookmark mark='a'/> Here it is "
            "on Kuhn poker, a toy with three cards. <bookmark mark='b'/> Exploitability, how much a perfect "
            "opponent could win against the average strategy, falls steadily, about like one over the square root of "
            f"the iterations. <bookmark mark='c'/> And the value it settles on is {val[-1]:.4f}: the known value of "
            "the game, minus one eighteenth. The first player is at a slight disadvantage, and the strategy it finds "
            "includes bluffing with the jack."
        ) as vo:
            self.play(FadeIn(cfr_c, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(kuhn), FadeIn(g), FadeIn(tag))
            vo.wait_until("b")
            self.play(Create(line), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.05), run_time=2.5)
            self.play(Create(ref), FadeIn(rl))
            vo.wait_until("c")
            self.play(FadeIn(v))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def poker(self):
        cards = VGroup(
            history_card(2015, r"Cepheus", r"heads-up limit Texas hold'em, \ essentially solved", width=4.2, color=VALUE),
            history_card(2017, r"Libratus", r"beats four top professionals at heads-up no-limit hold'em", width=4.2,
                         color=VALUE),
            history_card(2019, r"Pluribus", r"six-player no-limit: \ beats elite professionals; \ trained for under "
                         r"\$150 of cloud computing", width=4.2, color=VALUE),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 0.4)
        cite_ = cite(r"Bowling et al.\ (2015); \ Brown \& Sandholm (2017, 2019)")
        with self.voiceover(
            "Scaled up with abstraction and real-time search, CFR conquered poker. <bookmark mark='a'/> Cepheus "
            "essentially solved two-player limit Texas hold'em in 2015. <bookmark mark='b'/> Libratus beat top "
            "professionals at no-limit hold'em in 2017, <bookmark mark='c'/> and Pluribus beat elite professionals in "
            "six-player games in 2019, after training that cost under a hundred and fifty dollars of computing."
        ) as vo:
            self.play(FadeIn(cite_))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def alphastar(self):
        nodes = VGroup()
        names = [(r"main agents", AGENT), (r"main exploiters", PENALTY), (r"league exploiters", C.MODEL_Q),
                 (r"past selves", GREY_B)]
        pos = [UP * 1.5, LEFT * 3.2 + DOWN * 0.4, RIGHT * 3.2 + DOWN * 0.4, DOWN * 2.0]
        for (n, col), p in zip(names, pos):
            nodes.add(VGroup(Circle(radius=0.75, color=col, stroke_width=3, fill_color=col, fill_opacity=0.12),
                             label(n, font_size=22, color=col)).move_to(p))
            nodes[-1][1].move_to(nodes[-1][0])
        edges = VGroup(*[DoubleArrow(nodes[i][0].get_center(), nodes[j][0].get_center(), buff=0.8, color=GREY_C,
                                     stroke_width=2, tip_length=0.15) for i, j in ((0, 1), (0, 2), (0, 3), (1, 3), (2, 3))])
        hc = history_card(2019, r"AlphaStar, \ StarCraft II", r"Grandmaster: \ above $99.8\%$ of ranked human players",
                          width=4.6, color=AGENT).to_corner(UR, buff=0.3)
        why_ = label(r"plain self-play can cycle: \ rock beats scissors beats paper beats rock", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.25)
        cite_ = cite(r"O.~Vinyals et al., \textit{Nature} (2019)", corner=DL)
        with self.voiceover(
            "In games with many strategies, plain self-play can go in circles, just like the current strategies in "
            "the triangle: each new version beats the last and forgets how to beat the one before. "
            "<bookmark mark='a'/> For StarCraft II, AlphaStar trained a whole league: main agents, exploiters whose "
            "only job is to find the main agents' weaknesses, and a pool of past selves everyone must keep beating. "
            "<bookmark mark='b'/> It reached Grandmaster, above ninety-nine point eight percent of ranked human players."
        ) as vo:
            self.play(FadeIn(why_))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(n_, scale=0.9) for n_ in nodes], lag_ratio=0.25), Create(edges), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(hc, shift=LEFT * 0.2), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def exploits(self):
        hc = history_card(2023, r"Adversarial policies beat KataGo", r"a deliberately weak program, trained only to "
                          r"exploit a superhuman Go AI, wins by luring it into a looping group it misjudges; \ a human "
                          r"amateur learned the trick and beat a top Go program in $14$ games of $15$", width=7.6,
                          color=PENALTY).move_to(UP * 1.0)
        lesson = label(r"superhuman on average \ $\ne$ \ robust in the worst case", font_size=30, color=PENALTY)
        lesson.move_to(DOWN * 1.6)
        cite_ = cite(r"T.~T.~Wang et al., \textit{Adversarial Policies Beat Superhuman Go AIs}, ICML (2023)")
        with self.voiceover(
            "There's a sobering coda. In 2023, researchers trained a program, weak at Go in any normal sense, for "
            "one purpose: to beat KataGo, an open-source superhuman descendant of AlphaZero. It found a blind spot: a "
            "loop-shaped group of stones that the network misjudges. A human amateur learned the trick and beat a top "
            "program in fourteen games out of fifteen. <bookmark mark='a'/> Remember move seventy-eight. Superhuman "
            "on average is not the same as robust in the worst case, a lesson that returns in the last part of the "
            "series."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(lesson))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def algorithms(self):
        cards = VGroup(
            history_card(2022, r"AlphaTensor", r"matrix multiplication as a one-player game: \ $4 \times 4$ matrices "
                         r"in $47$ multiplications over $\mathbb{Z}_2$, \ beating Strassen's $49$ from 1969", width=6.0,
                         color=SEARCH),
            history_card(2023, r"AlphaDev", r"assembly code as a game: \ faster routines for sorting short lists, \ "
                         r"now in the LLVM C++ library", width=6.0, color=SEARCH),
        ).arrange(RIGHT, buff=0.35).move_to(UP * 0.8)
        nxt = label(r"next: \ the same tools tune language models \ (Parts 27 and 28)", font_size=26, color=GREY_A)
        nxt.to_edge(DOWN, buff=0.8)
        cite_ = cite(r"Fawzi et al., \textit{Nature} (2022); \ Mankowitz et al., \textit{Nature} (2023)")
        with self.voiceover(
            "The AlphaZero recipe has also been turned on problems that aren't games at all, by making them into "
            "games. <bookmark mark='a'/> AlphaTensor treated finding a matrix multiplication algorithm as a "
            "one-player game, and found a way to multiply four by four matrices in forty-seven multiplications in "
            "binary arithmetic, beating the record of forty-nine that had stood since Strassen in 1969. "
            "<bookmark mark='b'/> AlphaDev played a game of writing assembly code, and found faster sorting routines "
            "for short lists that are now part of the standard C++ library used by LLVM. <bookmark mark='c'/> And "
            "the same tools, policy gradients, PPO, search and self-play, are how today's language models are "
            "taught to follow instructions and to reason."
        ) as vo:
            self.play(FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(nxt))
        self.wait(0.3)
        self.clear_scene()
