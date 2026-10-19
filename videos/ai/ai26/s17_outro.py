from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai26.common import (AGENT, EXPLORE, PART, PENALTY, PRIOR, REWARD, SEARCH, TDERR, VALUE, curve,
                                   heat_image, load, node_box, tile_frame)
from videos.ai.ai26.s16_beyond import simplex_xy


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0
        out = []
        b = load("bandit")
        T = len(b["coin_ucb"])
        ax = Axes(x_range=[0, math.log10(T), 1], y_range=[0, 200, 100], x_length=TW * 0.9, y_length=TH * 0.85,
                  tips=False, axis_config={"stroke_color": GREY_D, "include_ticks": False})
        idx = np.unique(np.round(np.logspace(0, math.log10(T - 1), 60)).astype(int))
        lt = np.log10(idx + 1)
        lines = VGroup(ax)
        for k, col in (("eps", C.MODEL_Q), ("ucb", C.TRUE_P), ("thompson", C.INTERVAL)):
            y = np.asarray(b[f"coin_{k}"])[idx]
            keep = y <= 200
            lines.add(curve(ax, lt[keep], y[keep], col, 3))
        out.append((lines, r"explore: \ regret like $\log T$", EXPLORE))
        g = load("grid")
        view = GridView(g["layout"], cell=0.3)
        view.set_heat([tuple(c) for c in g["cells"]], np.asarray(g["V"])[-1])
        out.append((view, r"Bellman: \ $V^*$ by iteration", VALUE))
        gap = np.asarray(g["gap"])[:50]
        ax2 = Axes(x_range=[0, 50, 10], y_range=[-6, 1, 1], x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                   axis_config={"stroke_color": GREY_D, "include_ticks": False})
        out.append((VGroup(ax2, curve(ax2, np.arange(len(gap)), np.log10(np.maximum(gap, 1e-6)), VALUE, 3)),
                    r"a $\gamma$-contraction", C.CONTEXT))
        w = load("walk")
        ax3 = Axes(x_range=[0, 100, 50], y_range=[0, 0.25, 0.1], x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                   axis_config={"stroke_color": GREY_D, "include_ticks": False})
        ep = np.arange(101)
        out.append((VGroup(ax3, curve(ax3, ep, w["mc_0.02"], C.MODEL_Q, 3), curve(ax3, ep, w["td_0.1"], C.TRUE_P, 3)),
                    r"TD learns faster than MC", TDERR))
        dq = load("dqn")
        qd = np.asarray(dq["snap_qdiff"])[-1]
        img = heat_image(np.tanh(qd / (np.median(np.abs(qd)) / 2)), vmax=1.0, width=1.8, height=1.8)
        out.append((img, r"DQN's learned push", C.TRUE_P))
        r = np.linspace(0, 2, 200)
        ax4 = Axes(x_range=[0, 2, 1], y_range=[-0.2, 1.4, 1], x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                   axis_config={"stroke_color": GREY_D, "include_ticks": False})
        out.append((VGroup(ax4, curve(ax4, r, np.minimum(r, np.clip(r, 0.8, 1.2)), REWARD, 3)), r"PPO's clip",
                    C.RATIO))
        az = load("az_grade")
        gens = np.asarray(az["gens"])
        ax5 = Axes(x_range=[0, gens[-1], 10], y_range=[0, 1, 0.5], x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                   axis_config={"stroke_color": GREY_D, "include_ticks": False})
        out.append((VGroup(ax5, curve(ax5, gens, az["raw"], PRIOR, 3), curve(ax5, gens, az["mcts"], SEARCH, 3)),
                    r"our AlphaZero", SEARCH))
        rps = load("rps")
        avg = np.asarray(rps["average"])
        tri = Polygon(simplex_xy([1, 0, 0], [0, 0], 2.2), simplex_xy([0, 1, 0], [0, 0], 2.2),
                      simplex_xy([0, 0, 1], [0, 0], 2.2), stroke_color=GREY_C, stroke_width=1.5)
        idx = np.unique(np.round(np.geomspace(1, len(avg), 200)).astype(int)) - 1
        sp = VMobject(stroke_color=C.BITS, stroke_width=2.5).set_points_as_corners([simplex_xy(avg[i], [0, 0], 2.2)
                                                                                     for i in idx])
        out.append((VGroup(tri, sp), r"regret $\to$ Nash", C.BITS))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = tile_frame(cap, col, TW, TH)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(rf"Part {PART}, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Learning to act starts with exploring, and the optimism of an upper confidence bound "
            "explores just enough. Bellman's equation ties each state's value to its neighbours', and because its "
            "operator is a contraction, iterating it always converges. Temporal differences learn values from "
            "experience by bootstrapping, and Q-learning learns to act; with replay and a target network, a deep "
            "network can do it too. Policy gradients improve the policy directly, and PPO's clip keeps each step "
            "safe. Search, guided by a learned policy and value, trained on its own games, gave us AlphaZero. And "
            "where information is hidden, minimizing regret finds the equilibrium."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"PPO with a learned reward and a KL leash", [27]),
            (r"policy gradients on right answers; \ search over thoughts", [28]),
            (r"learned models of the world; \ long horizons", [29]),
            (r"reward hacking; \ superhuman but exploitable", [31]),
        ], font_size=26)
        with self.voiceover(
            "All of this comes back. PPO, with a reward learned from human preferences, is how chat models are "
            "trained, in Part 27. Policy gradients on checkable answers, and search over chains of thought, make "
            "reasoning models, in Part 28. Learned world models and long horizons are the subject of Part 29. And "
            "what happens when an agent optimizes a flawed reward, or a superhuman system has a blind spot, comes "
            "back in the last part."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"For rewards in $[0, 1]$, use Hoeffding's inequality to show that the true mean exceeds "
            r"$\hat\mu_a + \sqrt{2 \ln t / n_a}$ with probability at most $t^{-4}$.",
            r"Show that the Bellman operator $T^\pi$ of a fixed policy is a $\gamma$-contraction in the max norm, and "
            r"deduce that $V^\pi$ is its only fixed point.",
            r"Solve the Bellman equations of the five-state random walk exactly, and check the values "
            r"$\tfrac16, \dots, \tfrac56$.",
            r"Show that a baseline $b(s)$ leaves the policy gradient unbiased. \ Which constant $b$ minimizes the "
            r"variance of $(G - b)\, \nabla \log \pi$?",
            r"For $\hat A > 0$, show that the gradient of PPO's clipped objective is zero once $\rho > 1 + \epsilon$. "
            r"\ What happens for $\hat A < 0$?",
            r"In a two-player zero-sum game, show that if both players' average regrets are at most $\epsilon$, their "
            r"average strategies form a $2\epsilon$-Nash equilibrium.",
        ], font_size=22)
        with self.voiceover(
            "Here are six problems to try, from the confidence bound behind UCB to regret and equilibrium. Pause "
            "here, and work through them; full solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 27, \ Post-Training and Alignment", font_size=40).to_edge(UP, buff=0.5)
        steps = VGroup(*[node_box(t, c, font_size=26) for t, c in ((r"a base model", GREY_B), (r"supervised examples", AGENT),
                                                                  (r"a reward model of preferences", REWARD),
                                                                  (r"PPO with a KL leash", C.KL), (r"an assistant", SEARCH))])
        steps.arrange(RIGHT, buff=0.55).move_to(DOWN * 0.2)
        if steps.width > 13.2:
            steps.width = 13.2
        arrs = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5)
                        for a, b in zip(steps, steps[1:])])
        with self.voiceover(
            "Next time: how a language model that only predicts text becomes an assistant. Supervised examples, a "
            "reward model learned from human preferences, and the PPO of this part, on a leash to the model it "
            "started from: post-training and alignment."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(s_), *( [GrowArrow(arrs[i - 1])] if i else []))
                                    for i, s_ in enumerate(steps)], lag_ratio=0.5), run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        card = reference_card(
            [r"R.~S.~Sutton \& A.~G.~Barto, \textit{Reinforcement Learning: An Introduction}, 2nd ed.\ (2018)",
             r"T.~Lattimore \& C.~Szepesv\'ari, \textit{Bandit Algorithms} (2020)",
             r"D.~P.~Bertsekas \& J.~N.~Tsitsiklis, \textit{Neuro-Dynamic Programming} (1996)"],
            [r"Bellman (1957); \ Howard (1960); \ Thompson (1933); \ Lai \& Robbins (1985); \ Auer, Cesa-Bianchi \& "
             r"Fischer (2002)",
             r"Sutton (1988); \ Watkins \& Dayan (1992); \ Williams (1992); \ Tesauro (1995); \ Schultz, Dayan \& "
             r"Montague (1997)",
             r"Mnih et al.\ (2015); \ van Hasselt et al.\ (2016); \ Hessel et al.\ (2018); \ Badia et al.\ (2020)",
             r"Schulman et al., \textit{TRPO} (2015), \textit{GAE} (2016), \textit{PPO} (2017); \ Haarnoja et al.\ (2018)",
             r"Knuth \& Moore (1975); \ Campbell, Hoane \& Hsu (2002); \ Coulom (2006); \ Kocsis \& Szepesv\'ari (2006)",
             r"Silver et al.\ (2016, 2017, 2018); \ Schrittwieser et al.\ (2020); \ Ye et al.\ (2021); \ Danihelka et "
             r"al.\ (2022)",
             r"Hart \& Mas-Colell (2000); \ Zinkevich et al.\ (2007); \ Bowling et al.\ (2015); \ Brown \& Sandholm "
             r"(2017, 2019)",
             r"Vinyals et al.\ (2019); \ Berner et al.\ (2019); \ Wang et al.\ (2023); \ Fawzi et al.\ (2022); \ "
             r"Mankowitz et al.\ (2023)"])
        credit = note(narration_credit(), font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Sutton and Barto's book is the place to go deeper: everything in this part is in it, written for "
            "people learning it the first time. Thanks for watching, and see you in Part 27."
        ):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(1.5)
        self.clear_scene()
