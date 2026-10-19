from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai26.common import (AGENT, COLORS, ENV, GAMMA_C, PART, PENALTY, REWARD, VALUE, axes, chip, curve,
                                   load, node_box)


class Problem(VoiceoverScene):
    def construct(self):
        self.card()
        self.thorndike()
        self.loop()
        self.mdp()
        self.returns()
        self.values()
        self.hard()

    def card(self):
        card = chapter_card(1, r"Learning from consequences", r"What is there to learn, when nobody gives the answer?",
                            lit=(1957, 1959), part=PART)
        with self.voiceover("Chapter one. Learning from consequences."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def thorndike(self):
        box = Square(2.2, stroke_color=GREY_B, stroke_width=3).move_to([-3.6, 0.3, 0])
        bars = VGroup(*[Line(box.get_corner(UL) + RIGHT * (0.3 + 0.32 * k), box.get_corner(DL) + RIGHT * (0.3 + 0.32 * k),
                             stroke_width=1.5, color=GREY_C) for k in range(6)])
        loop = VGroup(Line(box.get_top() + LEFT * 0.4, box.get_top() + LEFT * 0.4 + DOWN * 0.9, color=REWARD,
                           stroke_width=3), Circle(radius=0.12, color=REWARD, stroke_width=3)
                      .move_to(box.get_top() + LEFT * 0.4 + DOWN * 1.02))
        door = Line(box.get_corner(UR), box.get_corner(DR), color=REWARD, stroke_width=6)
        bl = label(r"a puzzle box", font_size=22, color=GREY_A).next_to(box, DOWN, buff=0.2)
        # escape time falling trial by trial: the shape of Thorndike's curves (illustrative numbers)
        t = np.arange(1, 25)
        esc = 150 * np.exp(-t / 5) + 8 + 6 * np.sin(1.7 * t) * np.exp(-t / 9)
        g = axes([0, 25], [0, 170], x_length=5.4, y_length=3.0, xlabel=r"trial", ylabel=r"time to escape (s)",
                 xticks=[1, 12, 24], yticks=[0, 150], center=[2.8, 0.2, 0])
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=AGENT) for a, b in zip(t, esc)])
        line = curve(ax, t, esc, AGENT, 2)
        tag = note(r"illustrative: the shape of Thorndike's curves").to_corner(DR, buff=0.25)
        hc = history_card(1911, r"Edward Thorndike, \textit{Animal Intelligence}",
                          r"The law of effect: a response followed by satisfaction is ``stamped in''; "
                          r"one followed by discomfort, ``stamped out''.", width=5.6).to_corner(UL, buff=0.3)
        with self.voiceover(
            "In the 1890s the psychologist Edward Thorndike put cats in puzzle boxes. To get out, and get to the fish "
            "outside, a cat had to pull a loop of string. <bookmark mark='a'/> The first time it took minutes of "
            "scrabbling. Each time after, a little less, until the cat went straight for the loop. "
            "<bookmark mark='b'/> In 1911 he called it the law of effect: what is followed by satisfaction gets "
            "stamped in. <bookmark mark='c'/> Reinforcement learning is that law, made into mathematics. Nobody shows "
            "the learner the right action. There is only a number, a reward, that arrives after it acts, sometimes "
            "long after."
        ) as vo:
            self.play(Create(box), FadeIn(bars), FadeIn(bl))
            self.play(Create(loop), Create(door))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in dots], lag_ratio=0.08), Create(line), run_time=3)
            vo.wait_until("b")
            self.play(FadeOut(VGroup(box, bars, loop, door, bl)), FadeIn(hc, shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(Indicate(hc.head, color=REWARD))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def loop(self):
        agent = node_box(r"agent", AGENT, font_size=30, pad=0.45, height=1.0).move_to([-3.2, 1.2, 0])
        env = node_box(r"environment", ENV, font_size=30, pad=0.45, height=1.0).move_to([3.2, 1.2, 0])
        top = CurvedArrow(agent.get_top() + RIGHT * 0.3, env.get_top() + LEFT * 0.3, angle=-0.7, color=AGENT,
                          stroke_width=3, tip_length=0.2)
        bot = CurvedArrow(env.get_bottom() + LEFT * 0.3, agent.get_bottom() + RIGHT * 0.3, angle=-0.7, color=ENV,
                          stroke_width=3, tip_length=0.2)
        a_l = cmath(r"\text{action } a_t", font_size=32, color=AGENT).next_to(top, UP, buff=0.12)
        s_l = cmath(r"\text{reward } r_{t+1}", r",\ \text{state } s_{t+1}", font_size=32, color=ENV)
        s_l[0].set_color(REWARD)
        s_l.next_to(bot, DOWN, buff=0.12)
        # the same loop unrolled: a trajectory
        traj = VGroup()
        sym = [(r"s_0", ENV), (r"a_0", AGENT), (r"r_1", REWARD), (r"s_1", ENV), (r"a_1", AGENT), (r"r_2", REWARD),
               (r"s_2", ENV), (r"a_2", AGENT), (r"r_3", REWARD), (r"s_3", ENV), (r"\cdots", GREY_B)]
        for tex, col in sym:
            traj.add(MathTex(tex, font_size=40, color=col))
        traj.arrange(RIGHT, buff=0.42).move_to([0, -2.4, 0])
        tl = label(r"a trajectory", font_size=22, color=GREY_A).next_to(traj, UP, buff=0.25).align_to(traj, LEFT)
        with self.voiceover(
            "Here is the setting, in its modern form. An agent and an environment take turns. <bookmark mark='a'/> "
            "At each step t the agent sees the state, s t, and chooses an action, a t. <bookmark mark='b'/> The "
            "environment answers with a reward, r t plus one, and a new state. And again, and again. "
            "<bookmark mark='c'/> Unrolled, the interaction is one long sequence: state, action, reward, state, "
            "action, reward. A game of Go is one such sequence, with every reward zero except the last: plus one "
            "for a win, minus one for a loss."
        ) as vo:
            self.play(FadeIn(agent), FadeIn(env))
            vo.wait_until("a")
            self.play(Create(top), FadeIn(a_l))
            vo.wait_until("b")
            self.play(Create(bot), FadeIn(s_l))
            vo.wait_until("c")
            self.play(FadeIn(tl), LaggedStart(*[FadeIn(m, shift=RIGHT * 0.15) for m in traj], lag_ratio=0.12),
                      run_time=2.4)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mdp(self):
        body = VGroup(
            label(r"states $s \in \mathcal S$, \ actions $a \in \mathcal A$", font_size=26),
            label(r"transitions $P(s' \mid s, a)$, \ rewards $r(s, a)$", font_size=26),
            label(r"a discount $\gamma \in [0, 1)$", font_size=26, color=GAMMA_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        d = definition_card(r"Markov decision process", body, color=AGENT, width=8.6).move_to(UP * 1.6)
        mk = cmath(r"P(s_{t+1} \mid s_t, a_t, s_{t-1}, a_{t-1}, \dots, s_0)", r"=", r"P(s_{t+1} \mid s_t, a_t)",
                   font_size=36).move_to(DOWN * 1.0)
        mk[2].set_color(AGENT)
        ml = label(r"Markov: \ the present state is all the past you need", font_size=26, color=GREY_A)
        ml.next_to(mk, DOWN, buff=0.35)
        hc = history_card(1957, r"Richard Bellman, \textit{Dynamic Programming}",
                          r"names the problem of many decisions in a row, and the equation that solves it",
                          width=5.0, color=GAMMA_C).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The mathematical object is a Markov decision process. A set of states, a set of actions; <bookmark "
            "mark='a'/> the probability of each next state given the current state and action; a reward for each "
            "state and action; and a discount, gamma, that we'll meet in a moment. <bookmark mark='b'/> The word "
            "Markov carries the key assumption: the next state depends on the past only through the present state "
            "and action. Whatever history matters must be folded into the state. <bookmark mark='c'/> The framework "
            "is Richard Bellman's, from the 1950s, made for planning problems at the RAND Corporation long before "
            "anyone thought of learning."
        ) as vo:
            self.play(FadeIn(d.box), FadeIn(d[1]), FadeIn(d.head), FadeIn(body[0]))
            vo.wait_until("a")
            self.play(FadeIn(body[1]))
            self.play(FadeIn(body[2]))
            vo.wait_until("b")
            self.play(Write(mk))
            self.play(FadeIn(ml), Indicate(mk[2], color=AGENT))
            vo.wait_until("c")
            self.play(FadeIn(hc, shift=LEFT * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def returns(self):
        n = 10
        r = np.array([0, 1, 0, 0, 2, 0, 1, 0, 0, 3], float)
        gamma = ValueTracker(0.9)
        base = -0.9
        xs = np.linspace(-6.3, -2.4, n)

        def bars():
            g = gamma.get_value()
            out = VGroup()
            for k, (x, v) in enumerate(zip(xs, r)):
                h = max(0.9 * v * g ** k, 0.004)
                out.add(Rectangle(width=0.3, height=h, stroke_width=0, fill_color=REWARD, fill_opacity=0.9)
                        .move_to([x, base + h / 2, 0]))
            return out

        ghost = VGroup(*[Rectangle(width=0.3, height=max(0.9 * v, 0.004), stroke_color=REWARD, stroke_width=1.5,
                                   fill_opacity=0).move_to([x, base + 0.45 * v, 0]) for x, v in zip(xs, r)])
        live = always_redraw(bars)
        axis = Line([xs[0] - 0.4, base, 0], [xs[-1] + 0.4, base, 0], color=GREY_C, stroke_width=1.5)
        ticks = VGroup(*[MathTex(f"r_{{t+{k + 1}}}", font_size=17, color=REWARD).next_to([x, base, 0], DOWN, buff=0.12)
                         for k, x in enumerate(xs)])
        gam = always_redraw(lambda: MathTex(rf"\gamma = {gamma.get_value():.2f}", font_size=34, color=GAMMA_C)
                            .move_to([-4.35, 2.2, 0]))
        G = always_redraw(lambda: MathTex(
            rf"G_t \approx {float(sum(v * gamma.get_value() ** k for k, v in enumerate(r))):.2f}", font_size=34,
            color=REWARD).move_to([-4.35, 1.55, 0]))
        rows = [
            cmath(r"G_t", r"=", r"r_{t+1}", r"+ \gamma\, r_{t+2}", r"+ \gamma^2 r_{t+3}", r"+ \cdots", font_size=34),
            cmath(r"G_t", r"=", r"\sum_{k=0}^{\infty} \gamma^k\, r_{t+k+1}", font_size=34),
            cmath(r"|G_t|", r"\le", r"r_{\max} \sum_{k=0}^{\infty} \gamma^k", font_size=34),
            cmath(r"|G_t|", r"\le", r"\frac{r_{\max}}{1-\gamma}", font_size=34),
        ]
        whys = [None, None, why(r"$|r| \le r_{\max}$"), why(r"geometric series, \ $\gamma < 1$")]
        for row in rows:
            row[0].set_color(REWARD)
        step = ladder(self, rows, whys, keep=4, top=3.2, x=0.6, buff=0.38, edge=6.9)
        rec = cmath(r"G_t", r"=", r"r_{t+1}", r"+", r"\gamma", r"G_{t+1}", font_size=46)
        rec[0].set_color(REWARD)
        rec[2].set_color(REWARD)
        rec[4].set_color(GAMMA_C)
        rec[5].set_color(REWARD)
        rbox = boxed(rec, color=GAMMA_C, buff=0.25)
        rbox.move_to([3.4, -2.6, 0])
        rnote = label(r"the return is a reward plus a discounted return", font_size=22, color=GREY_A)
        rnote.next_to(rbox, DOWN, buff=0.15)
        with self.voiceover(
            "What the agent wants is not the next reward but all of them. The return from time t, G t, adds them "
            "up, with each reward k steps away discounted by gamma to the k. <bookmark mark='a'/> With gamma "
            "zero point nine, a reward ten steps away counts for a third of one now. <bookmark mark='b'/> Turn gamma "
            "down, and the agent becomes short-sighted; gamma near one is a patient agent. <bookmark mark='c'/> "
            "The discount also keeps the sum finite even if the game never ends: if every reward is at most r max, "
            "the return is at most r max times a geometric series, <bookmark mark='d'/> r max over one minus gamma. "
            "<bookmark mark='e'/> And the return has a recursive shape. Pull out the first reward, and what is "
            "left is gamma times the return from the next step: G t equals r t plus one plus gamma G t plus one. "
            "The next three chapters are built on this one line."
        ) as vo:
            self.play(Create(axis), FadeIn(ghost), FadeIn(ticks))
            self.add(live)
            self.play(FadeIn(gam), FadeIn(G))
            step(0)
            step(1)
            vo.wait_until("a")
            self.play(Indicate(ticks[-1], color=REWARD))
            vo.wait_until("b")
            self.play(gamma.animate.set_value(0.5), run_time=2.5)
            self.play(gamma.animate.set_value(0.97), run_time=2.5)
            self.play(gamma.animate.set_value(0.9), run_time=1.2)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            self.play(FadeIn(rbox, shift=UP * 0.2), FadeIn(rnote))
        self.wait(0.3)
        live.clear_updaters()
        gam.clear_updaters()
        G.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def values(self):
        d_pi = definition_card(r"policy", cmath(r"\pi(a \mid s)", r"=", r"\Pr(\text{take } a \text{ in } s)",
                                                 font_size=34, colors={r"\pi(a \mid s)": AGENT}),
                               color=AGENT, width=6.2)
        d_v = definition_card(r"state value", cmath(r"V^\pi(s)", r"=", r"\mathbb E_\pi[\, G_t \mid s_t = s\,]",
                                                     font_size=34, colors={r"V^\pi(s)": VALUE}),
                              color=VALUE, width=6.2)
        d_q = definition_card(r"action value", cmath(r"Q^\pi(s, a)", r"=",
                                                      r"\mathbb E_\pi[\, G_t \mid s_t = s,\ a_t = a\,]", font_size=34,
                                                      colors={r"Q^\pi(s, a)": VALUE}),
                              color=VALUE, width=6.2)
        cards = VGroup(d_pi, d_v, d_q).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(LEFT, buff=0.5)
        # a small picture: values on the gridworld of chapter three
        gdat = load("grid")
        V = np.asarray(gdat["V"])[-1]
        view = GridView(gdat["layout"], cell=0.5).move_to([3.6, 0.3, 0])
        view.set_heat([tuple(c) for c in gdat["cells"]], V)
        vl = label(r"$V^*(s)$ on a gridworld \ (chapter 3)", font_size=22, color=VALUE).next_to(view, DOWN, buff=0.2)
        rel = cmath(r"V^\pi(s)", r"=", r"\sum_a \pi(a \mid s)\, Q^\pi(s, a)", font_size=34,
                    colors={r"V^\pi(s)": VALUE}).next_to(vl, DOWN, buff=0.45)
        with self.voiceover(
            "Two more definitions, and we have the whole vocabulary. A policy, pi of a given s, is the agent's "
            "rule: a probability for each action in each state. <bookmark mark='a'/> The value of a state under a "
            "policy, V pi of s, is the return you expect if you start there and follow pi. <bookmark mark='b'/> Its "
            "cousin, the action value Q pi of s and a, is the expected return if you first take action a, and only "
            "then follow pi. <bookmark mark='c'/> Averaging Q over the policy's choices gives back V. "
            "<bookmark mark='d'/> Values are what everything in this part computes. Dynamic programming computes "
            "them exactly, temporal differences learn them from experience, and AlphaZero's network guesses them at "
            "a glance."
        ) as vo:
            self.play(FadeIn(d_pi, shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(d_v, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(d_q, shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(view), FadeIn(vl))
            self.play(Write(rel))
            vo.wait_until("d")
            self.play(Indicate(view, color=VALUE, scale_factor=1.04))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hard(self):
        heads = [(r"credit assignment", r"the win arrives $200$ moves later: \\ which moves earned it?", REWARD),
                 (r"exploration", r"you only see the results \\ of actions you try", C.ENTROPY),
                 (r"your data depends on you", r"change the policy, \\ change the states you visit", AGENT)]
        cols = VGroup()
        for h, b, col in heads:
            cols.add(VGroup(label(h, font_size=32, color=col), label(b, font_size=24, color=GREY_A))
                     .arrange(DOWN, buff=0.3))
        cols.arrange(RIGHT, buff=0.8).move_to(UP * 0.4)
        if cols.width > 13:
            cols.width = 13
        sup = label(r"supervised learning: \ every example comes with its answer", font_size=24, color=GREY_B)
        sup.to_edge(DOWN, buff=0.9)
        head = label(r"What makes it hard", font_size=36, color=GREY_A).to_edge(UP, buff=0.7)
        with self.voiceover(
            "Three things make this harder than learning from labelled examples. <bookmark mark='a'/> Credit "
            "assignment: in Go the reward arrives two hundred moves after the moves that earned it. Which of them "
            "deserves the credit? <bookmark mark='b'/> Exploration: you only see what happens after actions you "
            "actually try, so a learner that always does what looks best may never find out what is better. "
            "<bookmark mark='c'/> And the data depends on the learner: change the policy, and you change the states "
            "you see. <bookmark mark='d'/> In supervised learning every example comes with its answer, and the "
            "examples sit still. Here, neither is true."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.15))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cols[k], shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(sup))
        self.wait(0.3)
        self.clear_scene()
