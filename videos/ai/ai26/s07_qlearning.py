from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from explainer.ai.games import value_color
from videos.ai.ai26.common import AGENT, EXPLORE, PART, PENALTY, REWARD, TDERR, VALUE, axes, curve, legend, load

SARSA_C, QL_C = C.INTERVAL, C.SURPRISE


def cliff_grid(rows, cols, cell=0.5, center=ORIGIN):
    g = VGroup()
    sq = {}
    for r in range(rows):
        for c in range(cols):
            cliff = r == rows - 1 and 0 < c < cols - 1
            s = Square(cell, stroke_color=GREY_D, stroke_width=1, fill_color="#3A1D24" if cliff else "#1A2130",
                       fill_opacity=1).move_to([(c - (cols - 1) / 2) * cell, ((rows - 1) / 2 - r) * cell, 0])
            sq[(r, c)] = s
            g.add(s)
    cl = label(r"the cliff: \ $-100$, back to start", font_size=18, color=PENALTY)
    cl.move_to((sq[(rows - 1, 1)].get_center() + sq[(rows - 1, cols - 2)].get_center()) / 2)
    st = label(r"S", font_size=22, color=GREY_A).move_to(sq[(rows - 1, 0)])
    gl = label(r"G", font_size=22, color=REWARD).move_to(sq[(rows - 1, cols - 1)])
    g.add(cl, st, gl)
    g.sq = sq
    g.move_to(center)
    return g


def path_line(grid, path, color, width=5):
    pts = [grid.sq[tuple(p)].get_center() for p in path]
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(pts)


class QLearning(VoiceoverScene):
    def construct(self):
        self.card()
        self.rules()
        self.training()
        self.curves()
        self.triad()

    def card(self):
        card = chapter_card(6, r"Q-learning", r"How do you learn to act, not just to predict?", lit=(1989,), part=PART)
        with self.voiceover("Chapter six. Q-learning."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def rules(self):
        sarsa = cmath(r"Q(s, a)", r"\leftarrow", r"Q(s, a)", r"+", r"\alpha", r"\big[\, r + \gamma", r"Q(s', a')",
                      r"- Q(s, a) \,\big]", font_size=38)
        ql = cmath(r"Q(s, a)", r"\leftarrow", r"Q(s, a)", r"+", r"\alpha", r"\big[\, r + \gamma", r"\max_{a'} Q(s', a')",
                   r"- Q(s, a) \,\big]", font_size=38)
        for m in (sarsa, ql):
            m[0].set_color(VALUE)
            m[2].set_color(VALUE)
        sarsa[6].set_color(SARSA_C)
        ql[6].set_color(QL_C)
        sarsa.move_to(UP * 1.6)
        ql.move_to(DOWN * 0.9)
        sl = label(r"Sarsa: \ the action $a'$ it will actually take next \ (on-policy)", font_size=24, color=SARSA_C)
        sl.next_to(sarsa, UP, buff=0.3)
        qll = label(r"Q-learning: \ the best action at $s'$, \ whatever it does next \ (off-policy)", font_size=24,
                    color=QL_C).next_to(ql, UP, buff=0.3)
        greedy = label(r"knowing $Q$, \ acting is easy: \ $\pi(s) = \arg\max_a Q(s, a)$, \ no model needed",
                       font_size=26, color=AGENT).to_edge(UP, buff=0.35)
        th = theorem_card(r"convergence of Q-learning", r"if every $(s, a)$ is tried infinitely often and the step sizes "
                          r"satisfy $\sum_t \alpha_t = \infty$, \ $\sum_t \alpha_t^2 < \infty$, \ then $Q \to Q^*$ with "
                          r"probability $1$", who=r"Watkins (1989); \ Watkins \& Dayan (1992)", width=8.6,
                          color=QL_C).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "To act without a model, learn values of actions rather than states. With Q, acting is easy: pick the "
            "action with the highest Q, no transition probabilities needed. <bookmark mark='a'/> The TD idea carries "
            "over directly. After each step, nudge Q of s and a toward the reward plus gamma times the value of the "
            "next step. One version uses the action the agent really takes next: state, action, reward, state, "
            "action, so it's called Sarsa. <bookmark mark='b'/> Chris Watkins's version, in his 1989 thesis, uses "
            "the best action at the next state instead, whatever the agent actually does. That's Q-learning. "
            "<bookmark mark='c'/> It learns the value of acting optimally while behaving differently, exploring, "
            "and Watkins and Dayan proved it converges to Q star, provided every action keeps being tried and the "
            "step sizes shrink at the right rate."
        ) as vo:
            self.play(FadeIn(greedy))
            vo.wait_until("a")
            self.play(FadeIn(sl), Write(sarsa))
            vo.wait_until("b")
            self.play(FadeIn(qll), Write(ql))
            vo.wait_until("c")
            self.play(FadeIn(th, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def training(self):
        d = load("cliff")
        R, Cc = int(d["rows"]), int(d["cols"])
        eps_list = list(d["snap_episodes"])
        grids = {}
        heads = {}
        for m, col, y, name in (("sarsa", SARSA_C, 1.75, r"Sarsa"), ("q", QL_C, -1.55, r"Q-learning")):
            grids[m] = cliff_grid(R, Cc, cell=0.5, center=[-1.2, y, 0])
            heads[m] = label(name, font_size=28, color=col).next_to(grids[m], LEFT, buff=0.35)
        k = ValueTracker(0)

        def heat(m):
            def make():
                i = int(k.get_value())
                V = np.asarray(d[f"snapV_{m}"])[i]
                out = VGroup()
                for (r, c), s in grids[m].sq.items():
                    if r == R - 1 and 0 < c < Cc - 1:
                        continue
                    out.add(s.copy().set_fill(value_color((V[r, c] + 10) / 10), opacity=0.9).set_stroke(width=0))
                return out
            return make

        def greedy(m, col):
            return lambda: path_line(grids[m], d[f"snap_path_{m}"][int(k.get_value())], col, 6)

        hs = {m: always_redraw(heat(m)) for m in ("sarsa", "q")}
        ps = {m: always_redraw(greedy(m, c)) for m, c in (("sarsa", SARSA_C), ("q", QL_C))}
        ep = always_redraw(lambda: label(rf"after episode ${eps_list[int(k.get_value())]}$", font_size=30, color=GREY_A)
                           .move_to([4.9, 0.1, 0]))
        key = VGroup(label(r"colour: \ $\max_a Q(s, a)$", font_size=20, color=GREY_A),
                     label(r"line: \ the greedy path", font_size=20, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT)
        key.move_to([4.9, -0.8, 0])
        tag = note(rf"computed: \ $\varepsilon = {d['eps']}$, \ $\alpha = {d['alpha']}$, \ $\gamma = 1$").to_corner(DR, buff=0.2)
        # the very first episode, walked: a random stumble that keeps falling off
        walk = d["snap_walk_q"][0]
        dot = Dot(grids["q"].sq[tuple(walk[0])].get_center(), radius=0.12, color=QL_C)
        falls = sum(1 for a, b in zip(walk, walk[1:]) if tuple(b) == (R - 1, 0) and tuple(a) != (R - 1, 0))
        with self.voiceover(
            "Watch both learn on the cliff walk from Sutton and Barto. Start at S, reach G; every step costs one, "
            "and stepping off the cliff costs a hundred and sends you back to the start. Both explore, taking a "
            "random step one time in ten. <bookmark mark='a'/> Here is Q-learning's very first episode: a blind "
            f"stumble that falls off the cliff {falls} times before it finds the goal. <bookmark mark='b'/> Now the "
            "training, replayed: the colours are the learned values, the line is the path each would take if it "
            "stopped exploring. Every value starts at zero, so at first everywhere looks equally good. "
            "<bookmark mark='c'/> The values grow back from the goal, and the paths straighten "
            "out. <bookmark mark='d'/> And they settle on different answers. Q-learning learns the optimal path, "
            "right along the edge. Sarsa learns the safe path, along the top: it values each action by what its own "
            "exploring self will do next, and one random step on the edge is a fall."
        ) as vo:
            for m in ("sarsa", "q"):
                self.play(FadeIn(grids[m]), FadeIn(heads[m]))
            self.add(tag)
            vo.wait_until("a")
            self.add(dot)
            n = min(len(walk), 160)
            self.play(MoveAlongPath(dot, path_line(grids["q"], walk[:n], QL_C)), run_time=min(9.0, 0.06 * n),
                      rate_func=linear)
            self.remove(dot)
            vo.wait_until("b")
            self.add(hs["sarsa"], hs["q"], ps["sarsa"], ps["q"])
            for m in ("sarsa", "q"):
                grids[m][-3:].set_z_index(5)
            self.play(FadeIn(ep), FadeIn(key))
            vo.wait_until("c")
            self.play(k.animate.set_value(len(eps_list) - 1), run_time=7.0, rate_func=linear)
            vo.wait_until("d")
            self.play(Indicate(heads["q"], color=QL_C), Indicate(heads["sarsa"], color=SARSA_C))
        for m in ("sarsa", "q"):
            hs[m].clear_updaters()
            ps[m].clear_updaters()
        ep.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        d = load("cliff")
        E = len(d["q"])
        g = axes([0, E], [-100, 0], x_length=7.4, y_length=4.0, xlabel=r"episodes",
                 ylabel=r"reward per episode, \ while exploring \ (average of $100$ runs)", xticks=[0, 250, 500],
                 yticks=[-100, -50, 0], center=[-1.2, -0.3, 0])
        ax = g.ax
        sm = lambda y: np.convolve(y, np.ones(10) / 10, mode="valid")
        x = np.arange(len(sm(d["q"]))) + 5
        lq = curve(ax, x, np.maximum(sm(d["q"]), -100), QL_C, 3)
        ls = curve(ax, x, np.maximum(sm(d["sarsa"]), -100), SARSA_C, 3)
        lg = legend([(SARSA_C, r"Sarsa"), (QL_C, r"Q-learning")]).next_to(g, RIGHT, buff=0.3).shift(UP * 0.8)
        late_q, late_s = float(np.mean(d["q"][E // 2:])), float(np.mean(d["sarsa"][E // 2:]))
        ann = wrapped_label(rf"once trained: \ Q-learning ${late_q:.0f}$, \ Sarsa ${late_s:.0f}$ per episode", 3.6,
                            font_size=22, color=GREY_A).next_to(lg, DOWN, buff=0.5).align_to(lg, LEFT)
        with self.voiceover(
            "Which is better depends on what you score. Plot the reward each collects per episode while it is still "
            "exploring. <bookmark mark='a'/> Q-learning's optimal path runs along the edge, and every so often a "
            f"random step tips it over: it averages {late_q:.0f}. <bookmark mark='b'/> Sarsa's longer, safer path "
            f"averages {late_s:.0f}. Off-policy learning finds the best policy for a world without exploration; "
            "on-policy learning finds the best policy for the agent as it actually behaves."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(lq), FadeIn(lg[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(ls), FadeIn(lg[0]), run_time=2.0)
            self.play(FadeIn(ann))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def triad(self):
        parts = [(r"function approximation", r"one network for all states", AGENT),
                 (r"bootstrapping", r"targets built from estimates", TDERR),
                 (r"off-policy", r"learning about a policy \\ you aren't following", QL_C)]
        tri = VGroup()
        pos = [UP * 1.7, DOWN * 1.0 + LEFT * 3.4, DOWN * 1.0 + RIGHT * 3.4]
        for (h, b, col), p in zip(parts, pos):
            tri.add(VGroup(label(h, font_size=28, color=col), label(b, font_size=20, color=GREY_A))
                    .arrange(DOWN, buff=0.12).move_to(p))
        edges = VGroup(*[Line(tri[i].get_center(), tri[j].get_center(), buff=0.9, color=GREY_D, stroke_width=2)
                         for i, j in ((0, 1), (1, 2), (2, 0))])
        mid = label(r"the deadly triad", font_size=34, color=PENALTY).move_to(DOWN * 0.05)
        cite_ = cite(r"Baird, \textit{Residual Algorithms} (1995); \ Sutton \& Barto (2018), \S 11.3")
        nxt = label(r"next: \ how DQN made it work anyway", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.6)
        # a table of numbers, one per state and action, becomes a network that computes them
        table = VGroup(*[Square(0.32, stroke_color=GREY_C, stroke_width=1, fill_color=VALUE,
                                fill_opacity=float(np.random.default_rng(i).uniform(0.05, 0.6)))
                         for i in range(48)]).arrange_in_grid(rows=12, cols=4, buff=0).move_to([-3.0, 0.2, 0])
        tl = label(r"a table: \ one $Q$ per state and action", font_size=22, color=GREY_A).next_to(table, DOWN, buff=0.2)
        layers = [4, 7, 7, 2]
        net = VGroup(*[VGroup(*[Dot([x, (j - (n - 1) / 2) * 0.42, 0], radius=0.07, color=c)
                                for j in range(n)]) for x, n, c in zip([1.4, 2.6, 3.8, 5.0], layers,
                                                                      [GREY_B, AGENT, AGENT, VALUE])])
        wires = VGroup(*[Line(a.get_center(), b.get_center(), stroke_width=0.6, color=GREY_D)
                         for L in range(3) for a in net[L] for b in net[L + 1]])
        nl = label(r"a network: \ $Q(s, a; \theta)$ for any state", font_size=22, color=GREY_A)
        nl.next_to(VGroup(net, wires), DOWN, buff=0.35)
        arrow = Arrow([-1.9, 0.2, 0], [0.9, 0.2, 0], color=GREY_B, stroke_width=3)
        with self.voiceover(
            "A table of Q values can't hold Go, or even a video game screen, so the next step is to approximate Q "
            "with a function, a neural network. <bookmark mark='t'/> And here lies a trap. <bookmark mark='a'/> "
            "Function approximation, "
            "bootstrapping, and off-policy learning: any two are fine, but all three together can make the values "
            "diverge to infinity, even on tiny problems, as Leemon Baird showed in 1995. Sutton and Barto call it "
            "the deadly triad. <bookmark mark='b'/> Q-learning with a neural network has all three."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c_) for c_ in table], lag_ratio=0.01), FadeIn(tl), run_time=1.5)
            self.play(GrowArrow(arrow), Create(wires), FadeIn(net), FadeIn(nl), run_time=2.0)
            vo.wait_until("t")
            self.play(FadeOut(VGroup(table, tl, arrow, wires, net, nl)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t, scale=0.9) for t in tri], lag_ratio=0.4), Create(edges), FadeIn(cite_))
            self.play(FadeIn(mid))
            vo.wait_until("b")
            self.play(FadeIn(nxt))
        self.wait(0.3)
        self.clear_scene()
