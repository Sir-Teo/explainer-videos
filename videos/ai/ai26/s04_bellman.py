from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai26.common import AGENT, ENV, GAMMA_C, PART, REWARD, VALUE, load

COL = {r"V^\pi(s)": VALUE, r"V^\pi(s')": VALUE, r"V^*(s)": VALUE, r"V^*(s')": VALUE, r"\pi(a \mid s)": AGENT,
       r"\gamma": GAMMA_C, r"r(s, a)": REWARD, r"r_{t+1}": REWARD, r"P(s' \mid s, a)": ENV, r"\max_a": AGENT}


class Bellman(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.backup()
        self.linear()
        self.optimal()

    def card(self):
        card = chapter_card(3, r"Bellman's equation", r"How is a state's value tied to its neighbours'?",
                            lit=(1957,), part=PART)
        with self.voiceover("Chapter three. Bellman's equation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"V^\pi(s)", r"=", r"\mathbb E_\pi\big[\, G_t \mid s_t = s \,\big]", font_size=38, colors=COL),
            cmath(r"V^\pi(s)", r"=", r"\mathbb E_\pi\big[\,", r"r_{t+1}", r"+", r"\gamma", r"G_{t+1}",
                  r"\mid s_t = s \,\big]", font_size=38, colors=COL),
            cmath(r"V^\pi(s)", r"=", r"\sum_a", r"\pi(a \mid s)", r"\sum_{s'}", r"P(s' \mid s, a)", r"\Big[",
                  r"r(s, a)", r"+", r"\gamma", r"\,\mathbb E_\pi[\, G_{t+1} \mid s_{t+1} = s' \,]", r"\Big]",
                  font_size=36, colors=COL),
            cmath(r"V^\pi(s)", r"=", r"\sum_a", r"\pi(a \mid s)", r"\sum_{s'}", r"P(s' \mid s, a)", r"\Big[",
                  r"r(s, a)", r"+", r"\gamma", r"V^\pi(s')", r"\Big]", font_size=36, colors=COL),
        ]
        whys = [why(r"the definition"), why(r"$G_t = r_{t+1} + \gamma G_{t+1}$"),
                why(r"average over the action, then the next state"), why(r"Markov: \ the future from $s'$ \\ is "
                                                                          r"worth $V^\pi(s')$")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-3.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "Start from the definition: the value of s is the expected return from s. <bookmark mark='a'/> Now use "
            "the recursion from chapter one: the return is the next reward plus gamma times the return after it. "
            "<bookmark mark='b'/> Take the expectation in two stages: first over the action the policy picks, then "
            "over the state the environment sends you to. <bookmark mark='c'/> And here the Markov property does "
            "its work. Once you are in s prime, the expected return from there is just the value of s prime: "
            "nothing about how you got there matters. <bookmark mark='d'/> This is the Bellman equation. The value "
            "of a state is the reward you expect now, plus gamma times the value of where you expect to land. One "
            "equation per state, each tying a state's value to its neighbours'."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            box = SurroundingRectangle(rows[3], color=VALUE, buff=0.15, corner_radius=0.1)
            name = label(r"the Bellman equation for $V^\pi$", font_size=26, color=VALUE).next_to(box, DOWN, buff=0.2)
            name.align_to(box, LEFT)
            self.play(FadeOut(whys[3]), Create(box), FadeIn(name))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def backup(self):
        top = np.array([0, 2.4, 0])
        s = Circle(radius=0.26, color=VALUE, stroke_width=3, fill_color=VALUE, fill_opacity=0.2).move_to(top)
        sl = MathTex(r"s", font_size=32, color=VALUE).move_to(s)
        acts, nexts, edges1, edges2, lab = VGroup(), VGroup(), VGroup(), VGroup(), VGroup()
        for i, ax_ in enumerate([-3.4, 0, 3.4]):
            a = Dot([ax_, 0.7, 0], radius=0.13, color=AGENT)
            acts.add(a)
            edges1.add(Line(s.get_bottom(), a.get_top(), color=AGENT, stroke_width=2.5))
            for j, dx in enumerate([-0.9, 0, 0.9]):
                n = Circle(radius=0.2, color=VALUE, stroke_width=2.5).move_to([ax_ + dx, -1.1, 0])
                nexts.add(n)
                edges2.add(Line(a.get_bottom(), n.get_top(), color=ENV, stroke_width=2))
        lab.add(MathTex(r"\pi(a \mid s)", font_size=28, color=AGENT).next_to(edges1[0], LEFT, buff=0.1))
        lab.add(MathTex(r"P(s' \mid s, a)", font_size=26, color=ENV).next_to(edges2[0], LEFT, buff=0.1))
        lab.add(MathTex(r"r(s, a)", font_size=26, color=REWARD).next_to(edges2[4], RIGHT, buff=0.05).shift(UP * 0.1))
        vl = VGroup(*[MathTex(r"V^\pi(s')", font_size=20, color=VALUE).next_to(n, DOWN, buff=0.1) for n in nexts[3:6]])
        up = VGroup(*[Arrow(n.get_top() + UP * 0.05, s.get_bottom(), buff=0.25, stroke_width=1.5, color=VALUE,
                            max_tip_length_to_length_ratio=0.06).set_opacity(0.5) for n in nexts[::2]])
        cap = label(r"a backup diagram: \ values flow up from where you might land", font_size=26, color=GREY_A)
        cap.to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Draw it as a tree. At the top, the state s. <bookmark mark='a'/> The policy chooses among the "
            "actions, the small dots, with probabilities pi. <bookmark mark='b'/> Each action can lead to several "
            "next states, with probabilities from the environment, and a reward along the way. <bookmark mark='c'/> "
            "The Bellman equation says: value flows back up this tree. Average the next states' values, weighted by "
            "how likely you are to land there, add the reward, discount, and average over actions. Sutton and "
            "Barto call these backup diagrams. Every algorithm in this part is a different way of doing that "
            "backup: exactly, or from samples, or inside a search tree."
        ) as vo:
            self.play(FadeIn(s), FadeIn(sl))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(e) for e in edges1], lag_ratio=0.2), LaggedStart(*[FadeIn(a) for a in acts]),
                      FadeIn(lab[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(e) for e in edges2], lag_ratio=0.05),
                      LaggedStart(*[FadeIn(n) for n in nexts], lag_ratio=0.05), FadeIn(lab[1]), FadeIn(lab[2]))
            vo.wait_until("c")
            self.play(FadeIn(vl))
            self.play(LaggedStart(*[GrowArrow(u) for u in up], lag_ratio=0.1), FadeIn(cap))
            self.play(Indicate(s, color=VALUE, scale_factor=1.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def linear(self):
        g = load("grid")
        cells = [tuple(c) for c in g["cells"]]
        view = GridView(g["layout"], cell=0.62).move_to([-3.2, 0.2, 0])
        # the slip: from one cell, the intended move and the two sideways ones
        c0 = cells[g["start"]]
        src = view.square(*c0).get_center()
        arr = VGroup(
            Arrow(src, src + UP * 0.62, buff=0.05, color=AGENT, stroke_width=4, max_tip_length_to_length_ratio=0.35),
            Arrow(src, src + RIGHT * 0.62, buff=0.05, color=ENV, stroke_width=2.5, max_tip_length_to_length_ratio=0.35),
            Arrow(src, src + LEFT * 0.62, buff=0.05, color=ENV, stroke_width=2.5, max_tip_length_to_length_ratio=0.35),
        )
        pl = VGroup(MathTex(r"0.8", font_size=22, color=AGENT).next_to(arr[0], UP, buff=0.05),
                    MathTex(r"0.1", font_size=22, color=ENV).next_to(arr[1], DOWN, buff=0.05))
        info = VGroup(label(r"moves go where intended $80\%$ of the time, \\ slip sideways $10\% + 10\%$", font_size=24),
                      label(rf"reward $+1$ or $-1$ on the coloured cells; \ $\gamma = {g['gamma']}$", font_size=24,
                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.4, 2.2, 0])
        rows = [
            cmath(r"V^\pi", r"=", r"r_\pi", r"+", r"\gamma", r"P_\pi", r"V^\pi", font_size=40),
            cmath(r"(I - \gamma P_\pi)", r"V^\pi", r"=", r"r_\pi", font_size=40),
            cmath(r"V^\pi", r"=", r"(I - \gamma P_\pi)^{-1}", r"r_\pi", font_size=40),
        ]
        for r_ in rows:
            for part in r_:
                if part.tex_string.strip() == r"V^\pi":
                    part.set_color(VALUE)
                if part.tex_string.strip() == r"\gamma":
                    part.set_color(GAMMA_C)
        whys = [why(r"all ${n}$ equations at once".replace("{n}", str(len(cells)))), why(r"collect $V^\pi$"),
                why(r"one linear solve")]
        step = ladder(self, rows, whys, keep=3, top=0.9, x=3.2, align_index=None, buff=0.45, edge=6.9)
        Vr = np.asarray(g["V_rand"])
        with self.voiceover(
            "Here is a world to try it on: a grid with walls, a goal worth plus one, and a pit worth minus one, "
            "right below it. <bookmark mark='a'/> Moves are slippery: you go where you meant eighty percent of "
            "the time, and slip to either side ten percent each. <bookmark mark='b'/> For a fixed policy, the "
            f"Bellman equations are {len(cells)} linear equations in {len(cells)} unknowns. In matrix form, V is "
            "the expected reward vector plus gamma times the transition matrix times V. <bookmark mark='c'/> "
            "Gather the V's, <bookmark mark='d'/> and one matrix inverse gives the values exactly. "
            "<bookmark mark='e'/> For the policy that moves at random, here they are: hardly anything is worth "
            f"much, and the start is worth {Vr[g['start']]:+.3f}: a random walker is about as likely to fall into "
            "the pit as to find the goal."
        ) as vo:
            self.play(FadeIn(view))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in arr], lag_ratio=0.2), FadeIn(pl), FadeIn(info[0]))
            vo.wait_until("b")
            self.play(FadeIn(info[1]))
            step(0)
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            step(2)
            vo.wait_until("e")
            self.play(FadeOut(arr), FadeOut(pl), *view.heat(cells, Vr, vmax=1.0), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def optimal(self):
        g = load("grid")
        cells = [tuple(c) for c in g["cells"]]
        Vs = np.asarray(g["V"])
        view = GridView(g["layout"], cell=0.62).move_to([-3.2, -0.2, 0])
        view.set_heat(cells, Vs[-1])
        arrows = view.arrows(cells, np.asarray(g["pistar"]))
        rows = [
            cmath(r"V^*(s)", r"=", r"\max_a", r"\sum_{s'}", r"P(s' \mid s, a)", r"\big[", r"r(s, a)", r"+", r"\gamma",
                  r"V^*(s')", r"\big]", font_size=34, colors=COL),
            cmath(r"\pi^*(s)", r"=", r"\arg\max_a", r"\sum_{s'}", r"P(s' \mid s, a)", r"\big[", r"r(s, a)", r"+",
                  r"\gamma", r"V^*(s')", r"\big]", font_size=34, colors=COL),
        ]
        rows[1][0].set_color(AGENT)
        VGroup(*rows).arrange(DOWN, buff=0.5).move_to([3.2, 2.0, 0])
        for r_ in rows:
            if r_.width > 6.6:
                r_.width = 6.6
        pit = [i for i, (r, c) in enumerate(cells) if g["layout"][r][c] == "P"][0]
        pr, pc = cells[pit]
        below = cells.index((pr + 1, pc))
        assert int(np.asarray(g["pistar"])[below]) == 2  # down: away from the pit and the goal
        ring = SurroundingRectangle(view.square(pr + 1, pc), color=C.PENALTY, buff=0.02, stroke_width=4)
        note_ = label(r"under the pit, the best move is down: \\ up falls in, \ sideways slips in $10\%$ of the time",
                      font_size=24, color=GREY_A).move_to([3.2, -0.6, 0])
        nl = label(r"nonlinear (the max): \ no single matrix solve", font_size=24, color=AGENT).move_to([3.2, -2.2, 0])
        with self.voiceover(
            "That was one policy's value. What we want is the best policy. Its value, V star, satisfies the same "
            "equation with the average over actions replaced by a maximum: the Bellman optimality equation. "
            "<bookmark mark='a'/> And if you know V star, the best policy is to act greedily on it: in each state, "
            "pick the action with the best expected backed-up value. <bookmark mark='b'/> Here is V star for the "
            "gridworld, with its greedy policy. <bookmark mark='c'/> Look at the cell just under the pit. Its arrow "
            "points down, away from the goal. Up would walk into the pit, and a step sideways slips into it one "
            "time in ten, so the best plan takes the long way round. <bookmark mark='d'/> The max makes these equations nonlinear, so there's no "
            "single matrix inverse. The next chapter solves them anyway, by iteration, and proves it works."
        ) as vo:
            self.play(Write(rows[0]))
            vo.wait_until("a")
            self.play(Write(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(view))
            self.play(LaggedStart(*[GrowArrow(a) if isinstance(a, Arrow) else FadeIn(a) for a in arrows],
                                  lag_ratio=0.02), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(ring), FadeIn(note_))
            vo.wait_until("d")
            self.play(FadeIn(nl))
        self.wait(0.3)
        self.clear_scene()
