from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai26.common import (AGENT, LEFT_C, PART, PENALTY, REWARD, RIGHT_C, TDERR, VALUE, axes, band,
                                   cartpole, curve, heat_image, legend, load, node_box, state_map_frame)

FULL, NOTARGET, NOREPLAY = C.TRUE_P, C.MODEL_Q, GREY_B


class DQN(VoiceoverScene):
    def construct(self):
        self.card()
        self.atari()
        self.loss()
        self.replay_training()
        self.ablation()
        self.overestimate()
        self.later()

    def card(self):
        card = chapter_card(7, r"Deep Q-networks", r"Can one network learn to play from the pixels?", lit=(2013,),
                            part=PART)
        with self.voiceover("Chapter seven. Deep Q-networks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def atari(self):
        frames = VGroup(*[Square(1.4, stroke_color=GREY_B, stroke_width=1.5, fill_color="#20283A", fill_opacity=1)
                          .shift(RIGHT * 0.16 * i + UP * 0.16 * i) for i in range(4)])
        fl = label(r"$4$ frames, \ $84 \times 84$ pixels", font_size=20, color=GREY_A).next_to(frames, DOWN, buff=0.2)
        fr = VGroup(frames, fl).move_to([-5.0, 0.6, 0])
        convs = VGroup(*[Prism(dimensions=[0.25, h, h], fill_color=AGENT, fill_opacity=0.35, stroke_width=1)
                         .move_to([-2.9 + 1.0 * i, 0.6, 0]) for i, h in enumerate([1.3, 1.0, 0.8])])
        cl = label(r"$3$ convolutions", font_size=20, color=AGENT).next_to(convs, DOWN, buff=0.45)
        fc = VGroup(*[Dot([0.6, 1.8 - 0.3 * j, 0], radius=0.06, color=AGENT) for j in range(9)])
        qs = VGroup(*[Rectangle(width=0.55 * w, height=0.18, stroke_width=0, fill_color=VALUE, fill_opacity=0.9)
                      .move_to([2.0 + 0.275 * w, 1.6 - 0.26 * j, 0])
                      for j, w in enumerate([0.6, 1.4, 0.9, 2.6, 1.1, 0.4, 1.7, 0.8])])
        ql = label(r"$Q(s, a)$ \ for each joystick action \ (up to $18$)", font_size=20, color=VALUE).next_to(qs, DOWN, buff=0.25)
        arrows = VGroup(Arrow([-4.1, 0.6, 0], [-3.2, 0.6, 0], buff=0, stroke_width=2, color=GREY_B),
                        Arrow([-0.6, 0.6, 0], [0.4, 0.6, 0], buff=0, stroke_width=2, color=GREY_B),
                        Arrow([0.8, 0.6, 0], [1.8, 0.6, 0], buff=0, stroke_width=2, color=GREY_B))
        hc = history_card(2015, r"Mnih et al., \textit{Human-level control through deep reinforcement learning}, "
                          r"\textit{Nature}", r"one network, one set of settings, $49$ Atari games: \ at the level of a "
                          r"professional games tester overall, \ over $75\%$ of the tester's score on $29$ of them",
                          width=8.6, color=AGENT).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In 2013 a small London company, DeepMind, showed a Q-learning agent playing Atari video games from the "
            "raw screen. <bookmark mark='a'/> The input is the last four frames, shrunk to 84 by 84 pixels. "
            "<bookmark mark='b'/> Three convolutional layers, the vision networks of Part 10, and then a layer that "
            "outputs one Q value for each joystick action, up to eighteen. <bookmark mark='c'/> The 2015 paper in Nature trained "
            "the same network, with the same settings, on forty-nine different games, from Pong to Breakout to "
            "Space Invaders. It reached the level of a professional human games tester overall, and over three "
            "quarters of the tester's score on twenty-nine of them. The only signal was the change in the game score."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(fr))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[0]), LaggedStart(*[FadeIn(c_) for c_ in convs], lag_ratio=0.3), FadeIn(cl))
            self.play(GrowArrow(arrows[1]), FadeIn(fc), GrowArrow(arrows[2]),
                      LaggedStart(*[GrowFromEdge(q, LEFT) for q in qs], lag_ratio=0.1), FadeIn(ql))
            vo.wait_until("c")
            self.play(FadeIn(hc, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def loss(self):
        rows = [
            cmath(r"L(\theta)", r"=", r"\mathbb E_{(s, a, r, s') \sim \mathcal D}", r"\Big[\big(",
                  r"r + \gamma \max_{a'} Q(s', a'; \theta^-)", r"- Q(s, a; \theta)", r"\big)^2\Big]", font_size=36),
        ]
        rows[0][4].set_color(TDERR)
        rows[0].move_to(UP * 2.4)
        b1 = brace_note(rows[0][2], r"replay: \ random old transitions", color=AGENT, font_size=22)
        b2 = brace_note(rows[0][4], r"target network: \ a frozen copy $\theta^-$", color=TDERR, font_size=22)
        # the replay buffer: a strip of past transitions, a few sampled at random
        cells = VGroup(*[Rectangle(width=0.32, height=0.5, stroke_color=GREY_D, stroke_width=1, fill_color=GREY_B,
                                   fill_opacity=0.15 + 0.3 * (i / 30)) for i in range(30)]).arrange(RIGHT, buff=0.04)
        cells.move_to([-2.4, -0.9, 0])
        bl = label(r"replay memory \ (the last $10^6$ steps in the Atari paper)", font_size=20, color=GREY_A)
        bl.next_to(cells, DOWN, buff=0.2)
        pick = [3, 11, 17, 24]
        picks = VGroup(*[SurroundingRectangle(cells[i], color=AGENT, buff=0.03, stroke_width=3) for i in pick])
        w1 = label(r"why: \ consecutive frames are nearly identical; \\ random batches look independent, \ and each "
                   r"step is reused", font_size=22, color=GREY_A).move_to([-2.4, -2.6, 0])
        w2 = label(r"why: \ the target doesn't move \\ with every update", font_size=22, color=GREY_A).move_to([4.2, -1.0, 0])
        cp = VGroup(node_box(r"$Q(\cdot\,; \theta)$", AGENT, font_size=22), node_box(r"$Q(\cdot\,; \theta^-)$", TDERR,
                                                                                     font_size=22))
        cp.arrange(RIGHT, buff=1.4).move_to([4.2, 0.4, 0])
        ca = CurvedArrow(cp[0].get_top(), cp[1].get_top(), angle=-1.2, color=GREY_B, stroke_width=2, tip_length=0.15)
        cl = label(r"copy every $10^4$ steps", font_size=20, color=GREY_B).next_to(ca, UP, buff=0.05)
        with self.voiceover(
            "DQN is Q-learning with the update turned into a loss: the squared TD error, minimized by gradient "
            "descent. Two tricks keep the deadly triad at bay. <bookmark mark='a'/> First, experience replay, an "
            "idea of Long-Ji Lin's from 1992. Every transition goes into a large memory, and each update trains on a "
            "random batch from it. <bookmark mark='b'/> Consecutive frames are almost identical, so training on them "
            "in order is like studying one page over and over. Random batches look independent, and each "
            "experience is used many times. <bookmark mark='c'/> Second, a target network: the target is computed "
            "by a frozen copy of the network, <bookmark mark='d'/> refreshed only every ten thousand steps, so the "
            "network isn't chasing a target that moves with every step it takes."
        ) as vo:
            self.play(Write(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(b1), FadeIn(cells), FadeIn(bl))
            self.play(LaggedStart(*[Create(p) for p in picks], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(w1))
            vo.wait_until("c")
            self.play(FadeIn(b2), FadeIn(cp))
            vo.wait_until("d")
            self.play(Create(ca), FadeIn(cl), FadeIn(w2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay_training(self):
        d = load("dqn")
        steps = np.asarray(d["snap_steps"])
        Q = np.asarray(d["snap_qdiff"])
        T, L = np.asarray(d["snap_traj"]), np.asarray(d["snap_len"])
        run0 = np.asarray(d["run0"])
        vmax = float(np.percentile(np.abs(Q[-1]), 95))
        # the learning curve of this run, episode by episode
        S_MAX = int(steps[-1])
        g = axes([0, S_MAX], [0, 520], x_length=5.0, y_length=2.4, xlabel=r"steps of experience",
                 ylabel=r"length of each episode \ (this run)", xticks=[0, S_MAX // 2, S_MAX], yticks=[0, 500],
                 xfmt=lambda v: f"{int(v / 1000)}" + (r"\text{k}" if v else ""), center=[-3.3, -2.15, 0])
        pts = VGroup(*[Dot(g.ax.c2p(t, r), radius=0.025, color=FULL) for t, r in run0])
        marker = Line(g.ax.c2p(0, 0), g.ax.c2p(0, 520), color=C.BITS, stroke_width=3)
        imgs = [heat_image(Q[i], vmax=vmax, width=3.2, height=3.2).move_to([3.5, 0.55, 0]) for i in range(len(steps))]
        frame = state_map_frame(imgs[0])
        mkey = VGroup(label(r"push left", font_size=20, color=LEFT_C), label(r"push right", font_size=20, color=RIGHT_C))
        mkey.arrange(RIGHT, buff=0.4).next_to(frame[0], UP, buff=0.12)
        ml = label(r"the greedy action, \ cart centred and still", font_size=18, color=GREY_A).next_to(mkey, UP, buff=0.1)
        state = ValueTracker(0)
        snap = ValueTracker(0)

        def pole():
            i = int(snap.get_value())
            n = int(L[i])
            j = min(int(state.get_value()), n - 1)
            x, _, th, _ = T[i, j]
            fell = j == n - 1 and n < 500
            return cartpole(x, th, center=[-3.3, 0.75, 0], scale=1.1, color=PENALTY if fell else AGENT)

        cp = always_redraw(pole)
        info = always_redraw(lambda: label(
            rf"after ${int(steps[int(snap.get_value())]):,}$ steps: \ balanced ${min(int(state.get_value()), int(L[int(snap.get_value())]) - 1)}$ "
            rf"of $500$".replace(",", "{,}"), font_size=24, color=GREY_A).move_to([-3.3, 3.25, 0]))
        tag = note(rf"computed: \ our DQN, \ the best of ${len(d['full'])}$ runs").to_corner(DR, buff=0.2)
        img = imgs[0]
        n_runs = len(d["full"])
        with self.voiceover(
            "Here is DQN learning a classic control task on this machine: the cart-pole. Push the cart left or right "
            "to keep the pole upright; plus one for every step it stays up, for up to five hundred. "
            "<bookmark mark='a'/> On the right, what the network has learned: for each pole angle and angular "
            "velocity, which push it prefers. <bookmark mark='b'/> Untrained, it pushes the same way everywhere, and "
            f"the pole falls in a few steps. <bookmark mark='c'/> Let's replay the training of the best of our {n_runs} "
            "runs. Every few thousand steps, freeze the network and let it balance. <bookmark mark='d'/> The map organizes itself into two halves: "
            "if the pole is falling right, push right, so the cart gets back under it. The dividing line tilts, "
            "because a pole moving fast matters as much as a pole leaning far. Nobody told it any physics."
        ) as vo:
            self.add(cp)
            self.play(FadeIn(info), FadeIn(tag))
            self.play(state.animate.set_value(int(L[0]) - 1), run_time=1.0, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(img), FadeIn(frame), FadeIn(mkey), FadeIn(ml))
            vo.wait_until("b")
            self.play(FadeIn(g))
            vo.wait_until("c")
            self.add(marker)
            for i in range(1, len(steps)):
                state.set_value(0)
                self.play(FadeIn(imgs[i]), FadeOut(img), snap.animate.set_value(i),
                          marker.animate.put_start_and_end_on(g.ax.c2p(steps[i], 0), g.ax.c2p(steps[i], 520)),
                          FadeIn(VGroup(*[p for p, (t, _) in zip(pts, run0) if steps[i - 1] < t <= steps[i]])),
                          run_time=0.8)
                img = imgs[i]
                n = int(L[i])
                self.play(state.animate.set_value(n - 1), run_time=min(0.4 + n / 160, 3.6), rate_func=linear)
                if i == 4:
                    vo.wait_until("d")
        best = int(np.argmax(L))
        if L[-1] < 0.8 * L[best]:
            end = (f"Its best moment came at {int(steps[best]):,} steps, balancing {int(L[best])} of five hundred. "
                   f"Then, as training went on, it got worse again: at the end it lasts {int(L[-1])}. That's DQN's "
                   "notorious instability, the deadly triad still at work; in practice people keep the best checkpoint.")
        else:
            end = (f"By {int(steps[best]):,} steps it balances {int(L[best])} of five hundred, and at the end of "
                   f"training, {int(L[-1])}.")
        with self.voiceover(end):
            self.play(Indicate(img, scale_factor=1.03))
        cp.clear_updaters()
        info.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ablation(self):
        d = load("dqn")
        grid = np.asarray(d["grid"])
        S_MAX = int(grid[-1])
        g = axes([0, S_MAX], [0, 500], x_length=7.0, y_length=4.0, xlabel=r"steps of experience",
                 ylabel=rf"episode length \ (mean of ${len(d['full'])}$ runs; \ band: min to max)",
                 xticks=[0, S_MAX // 2, S_MAX],
                 yticks=[0, 250, 500], xfmt=lambda v: f"{int(v / 1000)}" + (r"\text{k}" if v else ""),
                 center=[-1.2, -0.3, 0])
        lines, bands = VGroup(), VGroup()
        for key, col in (("no_replay", NOREPLAY), ("no_target", NOTARGET), ("full", FULL)):
            Y = np.asarray(d[key])
            bands.add(band(g.ax, grid, np.nanmin(Y, 0), np.nanmax(Y, 0), col))
            lines.add(curve(g.ax, grid, np.nanmean(Y, 0), col, 3))
        lg = legend([(FULL, r"replay \ + \ target network"), (NOTARGET, r"replay, \ no target network"),
                     (NOREPLAY, r"no replay")], font_size=20).next_to(g, RIGHT, buff=0.3).shift(UP * 0.7)
        avg = {k: float(np.nanmean(np.asarray(d[k]))) for k in ("full", "no_target", "no_replay")}
        if avg["full"] > max(avg["no_target"], avg["no_replay"]):
            tail = "Each trick earns its place. And look at the bands: even the best version swings from run to run."
        else:
            tail = ("On a problem this small, the tricks matter less than the luck of the seed: look at the bands. "
                    "On Atari they were decisive: in the Nature paper, Breakout without replay scored about ten "
                    "points, against three hundred and seventeen with it.")
        with self.voiceover(
            f"Do the tricks matter? Train it three ways, {len(d['full'])} runs each, and average the episode length "
            "over the whole of training. <bookmark mark='a'/> Without a replay memory, learning from each step as it "
            f"comes: about {avg['no_replay']:.0f}. <bookmark mark='b'/> With replay but no target network: about "
            f"{avg['no_target']:.0f}. <bookmark mark='c'/> With both: about {avg['full']:.0f}. " + tail
        ) as vo:
            self.play(FadeIn(g))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(bands[k]), Create(lines[k]), FadeIn(lg[2 - k]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def overestimate(self):
        d = load("maxbias")
        em = d["emax"]
        k = len(em)
        bars = VGroup(*[Rectangle(width=0.36, height=max(1.6 * v, 0.01), stroke_width=0, fill_color=C.SURPRISE,
                                  fill_opacity=0.9) for v in em]).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        bars.move_to([-4.0, -1.2, 0]).align_to([0, -2.0, 0], DOWN)
        bl = VGroup(*[MathTex(str(i + 1), font_size=18, color=GREY_B).next_to(b, DOWN, buff=0.08) for i, b in enumerate(bars)])
        bt = label(r"$\mathbb E[\max$ of $k$ noisy estimates of $0]$", font_size=22, color=C.SURPRISE)
        bt.next_to(bars, UP, buff=0.3)
        bv = MathTex(rf"{em[-1]:.2f}", font_size=24, color=C.SURPRISE).next_to(bars[-1], UP, buff=0.08)
        kl = label(r"$k$", font_size=22, color=GREY_B).next_to(bl, DOWN, buff=0.12)
        jen = cmath(r"\mathbb E\big[\max_a \hat Q(a)\big]", r"\ge", r"\max_a \mathbb E\big[\hat Q(a)\big]", font_size=34)
        jen.move_to([-3.4, 2.3, 0])
        jl = label(r"Jensen: \ the max is convex", font_size=22, color=GREY_A).next_to(jen, DOWN, buff=0.15)
        dbl = cmath(r"y", r"=", r"r + \gamma\, Q\big(s', \arg\max_{a'} Q(s', a'; \theta);\ \theta^-\big)", font_size=30)
        dbl.move_to([3.4, 2.4, 0])
        dl = label(r"Double DQN: \ one network chooses, \ the other evaluates", font_size=22, color=C.INTERVAL)
        dl.next_to(dbl, DOWN, buff=0.15)
        lq, ld = np.asarray(d["left_q"]), np.asarray(d["left_double"])
        g = axes([0, len(lq)], [0, 1], x_length=5.4, y_length=2.6, xlabel=r"episodes",
                 ylabel=r"how often it takes the bad branch", xticks=[0, 150, 300], yticks=[0, 0.5, 1],
                 yfmt=lambda v: rf"{int(100 * v)}\%", center=[3.4, -1.3, 0])
        ep = np.arange(len(lq))
        cq, cd = curve(g.ax, ep, lq, C.SURPRISE, 3), curve(g.ax, ep, ld, C.INTERVAL, 3)
        opt = DashedLine(g.ax.c2p(0, d["optimal_left"]), g.ax.c2p(len(lq), d["optimal_left"]), color=GREY_B,
                         dash_length=0.08)
        lg = legend([(C.SURPRISE, r"Q-learning"), (C.INTERVAL, r"double Q-learning")], font_size=18)
        lg.next_to(g.ax, UP, buff=0.05).align_to(g.ax, RIGHT)
        cite_ = cite(r"van Hasselt (2010); \ van Hasselt, Guez \& Silver (2016); \ Sutton \& Barto, Example 6.7")
        with self.voiceover(
            "There's a subtler flaw in the max. The Q values are noisy estimates, and the max picks whichever "
            "happens to be too high. <bookmark mark='a'/> By Jensen's inequality, the expected max of the estimates "
            "is at least the max of the true values. <bookmark mark='b'/> If ten actions are all truly worth zero and "
            f"each estimate has noise of size one, the max averages {em[-1]:.2f}. Q-learning keeps bootstrapping on "
            "that optimism. <bookmark mark='c'/> In Sutton and Barto's test, a branch with ten slightly losing "
            "actions looks attractive, and Q-learning goes down it far more often than it should. "
            "<bookmark mark='d'/> The fix, from Hado van Hasselt: let one set of estimates choose the action and "
            "another evaluate it. The errors no longer line up, and double Q-learning heads for the right choice "
            "almost at once. Double DQN applies it with the target network as the second set."
        ) as vo:
            self.play(Write(jen), FadeIn(jl))
            vo.wait_until("a")
            self.play(Indicate(jen[1], color=C.SURPRISE))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), FadeIn(bl), FadeIn(bt),
                      FadeIn(kl))
            self.play(FadeIn(bv))
            vo.wait_until("c")
            self.play(FadeIn(g), Create(opt), Create(cq), FadeIn(lg[0]), FadeIn(cite_), run_time=2.0)
            vo.wait_until("d")
            self.play(Write(dbl), FadeIn(dl))
            self.play(Create(cd), FadeIn(lg[1]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def later(self):
        items = [
            (2016, r"double DQN, \ prioritized replay, \ dueling heads", AGENT),
            (2017, r"distributional RL: \ learn the whole distribution of returns, \ not just its mean", VALUE),
            (2018, r"Rainbow: \ six improvements combined beat each alone", C.BITS),
            (2020, r"Agent57: \ above the human baseline on all $57$ Atari games", REWARD),
        ]
        cards = VGroup(*[history_card(y, t, r"", width=6.0, color=c) for y, t, c in items])
        cards.arrange_in_grid(rows=2, cols=2, buff=0.35).move_to(UP * 0.2)
        cite_ = cite(r"Schaul et al.\ (2016); \ Wang et al.\ (2016); \ Bellemare, Dabney \& Munos (2017); "
                     r"\ Hessel et al.\ (2018); \ Badia et al.\ (2020)")
        with self.voiceover(
            "Atari became the proving ground for a decade. <bookmark mark='a'/> Double DQN, replay that samples "
            "surprising transitions more often, and networks that split value from advantage. <bookmark mark='b'/> "
            "Distributional RL, which learns the whole distribution of returns instead of only its average. "
            "<bookmark mark='c'/> Rainbow combined six of these ideas in 2018, <bookmark mark='d'/> and in 2020 "
            "Agent57 was the first to beat the human baseline on all fifty-seven games, including Montezuma's "
            "Revenge, where rewards are so rare that exploring is everything."
        ) as vo:
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15), *([FadeIn(cite_)] if k == 0 else []))
        self.wait(0.3)
        self.clear_scene()
