from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai26.common import (AGENT, EXPLORE, PART, PENALTY, PRIOR, REWARD, SEARCH, VALUE, go_board, go_point,
                                   go_stone, load, node_box)


def draw_position(board, B, highlight=None, last_color=None, scale=0.92):
    stones = VGroup()
    for y in range(19):
        for x in range(19):
            if B[y][x]:
                stones.add(go_stone(board, x, y, B[y][x] > 0, scale))
    hl = VGroup()
    if highlight is not None:
        x, y = highlight
        hl = VGroup(glow_dot(go_point(board, x, y), color=C.BITS, radius=board.step * 0.18),
                    Circle(radius=board.step * 0.62, color=C.BITS, stroke_width=4).move_to(go_point(board, x, y)))
    return stones, hl


class AlphaGo(VoiceoverScene):
    def construct(self):
        self.card()
        self.move37()
        self.networks()
        self.search()
        self.match()

    def card(self):
        card = chapter_card(12, r"AlphaGo", r"What happens when search gets a learned judge?", lit=(2016,), part=PART)
        with self.voiceover("Chapter twelve. AlphaGo."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def move37(self):
        g = load("go")["game2"]
        B = np.array(g["board"])
        board = go_board(side=5.8, center=[-2.8, 0.25, 0])
        stones, hl = draw_position(board, B, highlight=g["move"])
        last = stones  # the board as it was when move 37 appeared
        x, y = g["move"]
        new = go_stone(board, x, y, True).set_opacity(0)
        info = VGroup(label(r"Seoul, \ 10 March 2016", font_size=24, color=GREY_A),
                      label(r"game 2: \ AlphaGo (black) \ vs. \ Lee Sedol", font_size=24),
                      label(r"move 37", font_size=40, color=C.BITS)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        info.move_to([4.4, 1.9, 0])
        q = label(r"AlphaGo's own estimate that a human \\ would play it: \ about $1$ in $10{,}000$", font_size=24,
                  color=PRIOR).move_to([4.4, -0.2, 0])
        fifth = label(r"a shoulder hit on the fifth line: \\ against the textbook", font_size=22, color=GREY_A)
        fifth.move_to([4.4, -1.6, 0])
        cite_ = cite(r"game record: \ Andries Brouwer's AlphaGo archive; \ quote: \ D.~Silver, in \textit{Wired} (2016)")
        with self.voiceover(
            "This is the position from the opening of this part: Seoul, March 2016, the second game of five between "
            "DeepMind's AlphaGo and Lee Sedol, one of the strongest players of the previous decade. <bookmark mark='a'/> "
            "AlphaGo, playing black, placed its thirty-seventh stone here: a shoulder hit on the fifth line. "
            "<bookmark mark='b'/> Professional commentators thought it was a mistake; textbook play keeps such stones "
            "lower. AlphaGo's own network, trained on human games, put the chance that a human would play it at about "
            "one in ten thousand. <bookmark mark='c'/> It played it anyway, because its search said it was good, and "
            "it went on to win the game."
        ) as vo:
            self.play(FadeIn(board), FadeIn(info[:2]), FadeIn(cite_))
            self.play(LaggedStart(*[FadeIn(s_, scale=1.2) for s_ in stones if not np.allclose(s_.get_center(),
                                                                                               go_point(board, x, y))],
                                  lag_ratio=0.02), run_time=2.0)
            vo.wait_until("a")
            mv = [s_ for s_ in stones if np.allclose(s_.get_center(), go_point(board, x, y))]
            self.play(FadeIn(info[2]), *[FadeIn(m, scale=1.6) for m in mv], FadeIn(hl))
            vo.wait_until("b")
            self.play(FadeIn(q), FadeIn(fifth))
            vo.wait_until("c")
            self.play(Indicate(hl, color=C.BITS, scale_factor=1.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def networks(self):
        boxes = [
            (r"policy network, \ supervised", r"$13$-layer CNN, \ $30$ million positions of \\ strong amateurs' games: "
             r"predict the move. \ $57\%$ right", PRIOR),
            (r"policy network, \ reinforced", r"start from it, \ play against earlier versions, \\ policy gradient "
             r"(REINFORCE): \ wins $80\%$ against it", AGENT),
            (r"value network", r"predict the winner from a position: \\ $30$ million positions, \ each from a different "
             r"self-play game", VALUE),
            (r"fast rollout policy", r"a small linear model: \ $2$ microseconds a move, \\ for random-ish playouts",
             EXPLORE),
        ]
        cards = VGroup()
        for h, b, col in boxes:
            cards.add(definition_card(h, b, color=col, width=6.4, font_size=20, kind=r"AlphaGo"))
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.35)).move_to(UP * 0.3)
        arrows = VGroup(Arrow(cards[0].get_right(), cards[1].get_left(), buff=0.06, color=GREY_B, stroke_width=3),
                        Arrow(cards[1].get_bottom(), cards[3].get_top() + LEFT * 0.0, buff=0.06, color=GREY_B,
                              stroke_width=0).set_opacity(0),
                        Arrow(cards[1].get_bottom(), cards[2].get_top(), buff=0.06, color=GREY_B, stroke_width=3,
                              path_arc=-0.5))
        head = label(r"AlphaGo, \ 2016: \ deep networks inside Monte Carlo tree search", font_size=30)
        head.to_edge(UP, buff=0.3)
        slots = VGroup(*[DashedVMobject(RoundedRectangle(width=c.width, height=c.height, corner_radius=0.1,
                                                         stroke_width=1.5, color=GREY_D), num_dashes=40).move_to(c)
                         for c in cards])  # where the four parts will go
        hum = label(r"from human games", font_size=20, color=PRIOR).next_to(cards[0], UP, buff=0.12)
        selfp = label(r"from self-play", font_size=20, color=AGENT).next_to(cards[1], UP, buff=0.12)
        cite_ = cite(r"D.~Silver et al., \textit{Mastering the game of Go with deep neural networks and tree search}, "
                     r"\textit{Nature} (2016)")
        with self.voiceover(
            "AlphaGo, described in Nature in January 2016, put deep networks inside Monte Carlo tree search. It had "
            "four parts. <bookmark mark='a'/> A policy network, a thirteen-layer convolutional net trained on thirty "
            "million positions from games between strong amateurs to predict the next move: it got the human move "
            "fifty-seven percent of the time, far beyond earlier programs. <bookmark mark='b'/> Then a second copy, "
            "improved by reinforcement learning, the policy gradient of chapter eight, playing against earlier "
            "versions of itself. It beat its supervised parent eighty percent of the time. <bookmark mark='c'/> A "
            "value network, the missing judge: it looks at a position and estimates who will win. It was trained on "
            "positions from the reinforced network's self-play games, only one position per game, so it couldn't "
            "simply memorize games. <bookmark mark='d'/> And a tiny, fast policy for quick playouts, as in classic "
            "MCTS."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(head), Create(slots), run_time=1.5)
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                extra = [FadeIn(hum)] if k == 0 else ([GrowArrow(arrows[0]), FadeIn(selfp)] if k == 1 else
                                                      ([Create(arrows[2])] if k == 2 else []))
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeOut(slots[k]), *extra)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def search(self):
        sel = cmath(r"a_t", r"=", r"\arg\max_a \big(", r"Q(s, a)", r"+", r"u(s, a)", r"\big)", r",\qquad",
                    r"u(s, a)", r"\propto", r"\frac{P(s, a)}{1 + N(s, a)}", font_size=36)
        sel[3].set_color(VALUE)
        sel[5].set_color(PRIOR)
        sel[8].set_color(PRIOR)
        sel[10].set_color(PRIOR)
        sel.move_to(UP * 2.3)
        sl = label(r"select: \ the value so far, \ plus a bonus for moves the policy network likes \ and the search "
                   r"hasn't tried much", font_size=22, color=GREY_A).next_to(sel, DOWN, buff=0.2)
        if sl.width > 13:
            sl.width = 13
        leaf = cmath(r"V(s_L)", r"=", r"(1 - \lambda)\,", r"v_\theta(s_L)", r"+", r"\lambda\,", r"z_L", font_size=38)
        leaf[0].set_color(VALUE)
        leaf[3].set_color(VALUE)
        leaf[6].set_color(EXPLORE)
        leaf.move_to(DOWN * 0.2)
        ll = label(r"evaluate a leaf: \ half the value network, \ half a fast rollout \ ($\lambda = \tfrac12$)",
                   font_size=22, color=GREY_A).next_to(leaf, DOWN, buff=0.2)
        hw = label(r"the distributed version: \ $1{,}202$ CPUs, \ $176$ GPUs", font_size=24, color=GREY_B)
        hw.to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "The search is MCTS with two changes. <bookmark mark='a'/> When it selects a move, the exploration bonus "
            "is weighted by the policy network's prior, P: moves a strong player would consider get explored first, "
            "and the bonus fades as a move's visits pile up. It's the same optimism as UCB, steered by intuition. "
            "<bookmark mark='b'/> And when it reaches a leaf, it doesn't rely on random games alone: the leaf's "
            "value is half the value network's judgment and half the result of one fast rollout. <bookmark mark='c'/> "
            "The policy network narrows the search; the value network shortens it."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(sel), FadeIn(sl))
            vo.wait_until("b")
            self.play(Write(leaf), FadeIn(ll))
            vo.wait_until("c")
            self.play(FadeIn(hw))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def match(self):
        g = load("go")["game4"]
        B = np.array(g["board"])
        board = go_board(side=5.2, center=[3.6, -0.6, 0])
        stones, hl = draw_position(board, B, highlight=g["move"])
        cards = VGroup(
            history_card(2015, r"AlphaGo $5$, \ Fan Hui $0$", r"the first win by a program over a professional on a "
                         r"full board without a head start", width=5.4, color=AGENT),
            history_card(2016, r"AlphaGo $4$, \ Lee Sedol $1$", r"Seoul, \ followed live around the world",
                         width=5.4, color=AGENT),
        ).arrange(DOWN, buff=0.3).to_edge(LEFT, buff=0.4).shift(UP * 0.6)
        m78 = label(r"game 4, \ move 78: \ Lee Sedol (white) \\ finds a move AlphaGo hadn't expected", font_size=22,
                    color=C.BITS).next_to(board, UP, buff=0.2)
        with self.voiceover(
            "In October 2015 AlphaGo had beaten the European champion Fan Hui five games to nothing, the first time a "
            "program beat a professional on a full board without a head start. <bookmark mark='a'/> In Seoul it beat "
            "Lee Sedol four games to one. <bookmark mark='b'/> The one he won, game four, turned on his own move "
            "seventy-eight, a wedge that AlphaGo, by its own policy network, had also rated about one in ten "
            "thousand. Its search hadn't looked there, and it went astray. Search guided by a network inherits the "
            "network's blind spots: remember that for chapter fifteen."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(board), FadeIn(m78), LaggedStart(*[FadeIn(s_) for s_ in stones], lag_ratio=0.01),
                      run_time=1.5)
            self.play(FadeIn(hl))
        self.wait(0.3)
        self.clear_scene()
