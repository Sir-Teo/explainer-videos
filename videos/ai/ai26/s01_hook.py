from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai26.common import AGENT, PART, PRIOR, REWARD, SEARCH, VALUE, go_board, go_point, go_stone, load
from videos.ai.ai26.s13_alphago import draw_position


class Hook(VoiceoverScene):
    def construct(self):
        self.move()
        self.question()
        self.plan()

    # ------------------------------------------------------------------
    def move(self):
        g = load("go")["game2"]
        B = np.array(g["board"])
        board = go_board(side=5.6, center=[-3.0, 0.0, 0])
        stones, hl = draw_position(board, B, highlight=g["move"])
        x, y = g["move"]
        is_new = lambda s_: np.allclose(s_.get_center(), go_point(board, x, y))
        q = label(r"$1$ in $10{,}000$", font_size=48, color=PRIOR).move_to([3.4, 1.6, 0])
        ql = label(r"the chance a human would play it, \\ by AlphaGo's own estimate", font_size=24, color=GREY_A)
        ql.next_to(q, DOWN, buff=0.25)
        z = VGroup(label(r"2017: \ its successor learns Go from nothing,", font_size=26, color=AGENT),
                   label(r"in three days, \ and beats it $100$ games to $0$", font_size=26, color=AGENT))
        z.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.4, -1.0, 0])
        with self.voiceover(
            "Seoul, March 2016. A computer program, AlphaGo, is playing Lee Sedol, one of the best Go players in the "
            "world. <bookmark mark='a'/> On its thirty-seventh move it plays here, a move so unusual that the "
            "commentators assume it's a mistake. <bookmark mark='b'/> AlphaGo's own model of human play put the "
            "chance that a person would play it at one in ten thousand. It wins the game, and the match. "
            "<bookmark mark='c'/> A year and a half later, its successor learns Go with no human games at all, from "
            "random play, in three days, and beats it a hundred games to nothing."
        ) as vo:
            self.play(FadeIn(board), LaggedStart(*[FadeIn(s_) for s_ in stones if not is_new(s_)], lag_ratio=0.02),
                      run_time=2.5)
            vo.wait_until("a")
            self.play(*[FadeIn(s_, scale=1.8) for s_ in stones if is_new(s_)], FadeIn(hl))
            vo.wait_until("b")
            self.play(FadeIn(q), FadeIn(ql))
            vo.wait_until("c")
            self.play(FadeIn(z, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def question(self):
        q = label(r"How do you learn to act, \\ when nobody tells you the right action, \\ only how it turned out?",
                  font_size=40).move_to(UP * 1.0)
        path = VGroup(label(r"Thorndike's cats", font_size=24, color=GREY_A), MathTex(r"\to", font_size=30),
                      label(r"Bellman's equation", font_size=24, color=VALUE), MathTex(r"\to", font_size=30),
                      label(r"TD-Gammon", font_size=24, color=C.TRUE_P), MathTex(r"\to", font_size=30),
                      label(r"DQN", font_size=24, color=C.TRUE_P), MathTex(r"\to", font_size=30),
                      label(r"PPO", font_size=24, color=AGENT), MathTex(r"\to", font_size=30),
                      label(r"AlphaZero", font_size=24, color=SEARCH)).arrange(RIGHT, buff=0.2).move_to(DOWN * 1.4)
        if path.width > 13.2:
            path.width = 13.2
        ours = label(r"and our own AlphaZero, trained on this computer", font_size=28, color=SEARCH).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "That is the question of this part: how do you learn to act, when nobody tells you the right action, only "
            "how things turned out? <bookmark mark='a'/> We'll follow the answer from a psychologist's puzzle boxes, "
            "through Bellman's equation and the algorithms that learned backgammon, Atari and the cart-pole, to "
            "AlphaGo and AlphaZero, deriving each step. <bookmark mark='b'/> And we'll train an AlphaZero of our own, "
            "on the computer making this video, and grade every move it makes against a perfect player."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in path], lag_ratio=0.12), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(ours))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Reinforcement Learning, \ from Bellman to AlphaZero", font_size=44)
        title.to_edge(UP, buff=0.5)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 0.6)
        obj = objectives_card([
            r"the reinforcement learning problem, \ and exploration (bandits, UCB, Thompson)",
            r"Bellman's equation, \ value and policy iteration, \ and why they converge",
            r"learning from experience: \ TD, \ Q-learning, \ deep Q-networks",
            r"policy gradients, \ actor-critic, \ PPO",
            r"search: \ minimax, \ MCTS, \ AlphaGo, \ AlphaZero, \ MuZero",
            r"games of imperfect information: \ regret, \ CFR, \ poker",
        ], font_size=26)
        with self.voiceover(
            "This is Part 26 of AI, Built, and the start of its fifth act: agency. <bookmark mark='a'/> In this part: the "
            "reinforcement learning problem and the dilemma of exploration; Bellman's equation and why its "
            "algorithms converge; learning from experience, from temporal differences to deep Q-networks; policy "
            "gradients and PPO, the algorithm behind ChatGPT's training; search, from minimax to AlphaZero and "
            "MuZero; and games with hidden information, like poker."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.3)
        self.clear_scene()
