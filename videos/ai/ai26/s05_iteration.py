from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai26.common import AGENT, ENV, GAMMA_C, PART, REWARD, VALUE, axes, curve, load, node_box


class Iteration(VoiceoverScene):
    def construct(self):
        self.card()
        self.sweeps()
        self.proof()
        self.two_starts()
        self.policy_iteration()
        self.scale()

    def card(self):
        card = chapter_card(4, r"Why value iteration works", r"Can you solve an equation by just repeating it?",
                            lit=(1957,), part=PART)
        with self.voiceover("Chapter four. Why value iteration works."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def sweeps(self):
        g = load("grid")
        cells = [tuple(c) for c in g["cells"]]
        Vs, pis = np.asarray(g["V"]), np.asarray(g["pi"])
        view = GridView(g["layout"], cell=0.66).move_to([-2.9, -0.3, 0])
        k = ValueTracker(0)
        view.add_updater(lambda m: m.set_heat(cells, Vs[min(int(k.get_value()), len(Vs) - 1)]))
        kl = always_redraw(lambda: MathTex(rf"k = {int(k.get_value())}", font_size=36, color=GREY_A)
                           .next_to(view, UP, buff=0.3))
        eq = cmath(r"V_{k+1}(s)", r"=", r"\max_a \sum_{s'} P(s' \mid s, a)\big[\, r(s, a) + \gamma V_k(s') \,\big]",
                   font_size=32).move_to([2.6, 2.8, 0])
        eq[0].set_color(VALUE)
        if eq.width > 7.4:
            eq.width = 7.4
        name = label(r"value iteration: \ apply the Bellman backup to every state, \ repeat", font_size=24,
                     color=GREY_A).next_to(eq, DOWN, buff=0.25)
        start = cells.index(cells[g["start"]])
        sval = always_redraw(lambda: MathTex(rf"V_k(\text{{start}}) = {Vs[min(int(k.get_value()), len(Vs) - 1), start]:.3f}",
                                             font_size=30, color=VALUE).move_to([3.2, 0.6, 0]))
        tag = note(rf"computed: \ converged after ${g['sweeps']}$ sweeps").to_corner(DR, buff=0.25)
        with self.voiceover(
            "Bellman's own answer to the nonlinear equations was to iterate them. Start with every value at zero. "
            "<bookmark mark='a'/> Apply the right-hand side of the optimality equation to every state at once, and "
            "call the result the new values. Then do it again. <bookmark mark='b'/> After one sweep, only the cells "
            "next to the goal and the pit know anything. <bookmark mark='c'/> Each sweep pushes the news one step "
            "further, and the values spread out from the goal like heat. <bookmark mark='d'/> After a few dozen "
            "sweeps nothing changes any more: we have V star, and the arrows of the last chapter."
        ) as vo:
            self.play(FadeIn(view), FadeIn(kl), Write(eq))
            vo.wait_until("a")
            self.play(FadeIn(name), FadeIn(sval), FadeIn(tag))
            vo.wait_until("b")
            self.play(k.animate.set_value(1), run_time=1.0)
            vo.wait_until("c")
            self.play(k.animate.set_value(12), run_time=6.0, rate_func=linear)
            vo.wait_until("d")
            self.play(k.animate.set_value(len(Vs) - 1), run_time=3.0, rate_func=rate_functions.ease_out_cubic)
        view.clear_updaters()
        kl.clear_updaters()
        sval.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proof(self):
        rows = [
            cmath(r"(TV)(s)", r"=", r"\max_a \Big[\, r(s, a) + \gamma \sum_{s'} P(s' \mid s, a)\, V(s') \,\Big]",
                  font_size=34),
            cmath(r"\big|\max_a f(a) - \max_a g(a)\big|", r"\le", r"\max_a \big|f(a) - g(a)\big|", font_size=34),
            cmath(r"\big|(TV)(s) - (TU)(s)\big|", r"\le", r"\gamma \max_a \sum_{s'} P(s' \mid s, a)\, |V(s') - U(s')|",
                  font_size=34),
            cmath(r"\big|(TV)(s) - (TU)(s)\big|", r"\le", r"\gamma\, \|V - U\|_\infty", font_size=34),
            cmath(r"\|TV - TU\|_\infty", r"\le", r"\gamma\, \|V - U\|_\infty", font_size=34),
        ]
        whys = [why(r"the Bellman operator $T$"), why(r"a lemma: \ if $f \le g + c$ then $\max f \le \max g + c$"),
                why(r"the rewards cancel"), why(r"the $P$'s sum to $1$"), why(r"for every $s$: \ a contraction")]
        step = ladder(self, rows, whys, keep=5, top=3.1, x=-0.8, buff=0.42, edge=6.9)
        th = theorem_card(r"Banach fixed point", r"a contraction $T$ on a complete space has exactly one fixed point "
                          r"$V^* = TV^*$, \ and from any start \ $\|V_k - V^*\|_\infty \le \gamma^k \|V_0 - V^*\|_\infty$",
                          who=r"Stefan Banach (1922)", width=8.2, color=VALUE).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Why must this work? Write the right-hand side as an operator, T, that takes a table of values and "
            "returns a new one. <bookmark mark='a'/> One small lemma: two maxima can't differ by more than the "
            "biggest difference between the things being maximized. <bookmark mark='b'/> Compare T applied to two "
            "different tables, V and U. The rewards are the same, so they cancel, and what's left is gamma times "
            "an average of differences. <bookmark mark='c'/> An average is never bigger than the largest entry. "
            "<bookmark mark='d'/> So T shrinks the distance between any two tables, in the max norm, by a factor "
            "gamma. It's a contraction. <bookmark mark='e'/> And Banach's fixed point theorem from 1922 finishes "
            "the job: a contraction has exactly one fixed point, and repeating it from any start converges there "
            "geometrically, at rate gamma. That fixed point satisfies the Bellman optimality equation: it is V star."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            box = SurroundingRectangle(rows[4], color=GAMMA_C, buff=0.12, corner_radius=0.08)
            self.play(Create(box))
            vo.wait_until("e")
            self.play(*[FadeOut(m) for m in rows[:4]], *[FadeOut(w) for w in whys if w is not None],
                      VGroup(rows[4], box).animate.move_to(UP * 1.6))
            self.play(FadeIn(th.move_to(DOWN * 0.6), shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def two_starts(self):
        g = load("grid")
        gap = np.asarray(g["gap"])
        gamma = g["gamma"]
        K = min(len(gap), 60)
        lg = np.log10(np.maximum(gap[:K], 1e-12))
        lo = math.floor(lg.min())
        a = axes([0, K], [lo, 1], x_length=6.8, y_length=4.0, xlabel=r"sweep $k$",
                 ylabel=r"distance between the two runs, \ $\max_s |V_k - U_k|$ \ (log scale)",
                 xticks=[0, 20, 40, 60], yticks=list(range(lo, 2)), yfmt=lambda v: rf"10^{{{int(v)}}}",
                 center=[-1.2, -0.3, 0])
        ax = a.ax
        ks = np.arange(K)
        pts = VGroup(*[Dot(ax.c2p(k, v), radius=0.05, color=VALUE) for k, v in zip(ks, lg)])
        bound = DashedLine(ax.c2p(0, lg[0]), ax.c2p(K - 1, lg[0] + (K - 1) * math.log10(gamma)), color=GAMMA_C,
                           stroke_width=3, dash_length=0.1)
        bl = label(rf"$\gamma^k$, \ $\gamma = {gamma}$", font_size=24, color=GAMMA_C)
        bl.next_to(bound.get_end(), UP, buff=0.15).shift(LEFT * 0.4)
        ratio = float(np.max(gap[1:K] / gap[:K - 1]))
        note_ = label(rf"each sweep multiplies it by at most $\gamma$: \ worst ${ratio:.3f}$", font_size=24, color=GREY_A)
        note_.to_edge(RIGHT, buff=0.4).shift(UP * 2.3)
        tag = note(r"computed: \ two starts, \ all zeros and random").to_corner(DR, buff=0.25)
        with self.voiceover(
            "Here's the theorem at work. Run value iteration twice on the gridworld: once from all zeros, once from "
            "random values. <bookmark mark='a'/> On a log scale, here is the largest difference between the two "
            "runs, sweep by sweep. <bookmark mark='b'/> The theorem says it must stay under the dashed line, gamma "
            f"to the k. For the first dozen sweeps it rides almost exactly on it: no sweep shrinks it by less than "
            f"{ratio:.3f}. Then, as the cells near the goal settle, it falls even faster. Wherever you start, you "
            "end at the same V star."
        ) as vo:
            self.play(FadeIn(a), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, scale=1.4) for p in pts], lag_ratio=0.04), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(bound), FadeIn(bl))
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def policy_iteration(self):
        g = load("grid")
        cells = [tuple(c) for c in g["cells"]]
        P, V = np.asarray(g["pi_iter"]), np.asarray(g["V_iter"])
        view = GridView(g["layout"], cell=0.6).move_to([-3.4, -0.6, 0])
        view.set_heat(cells, V[0])
        arrows = view.arrows(cells, P[0])
        it = MathTex(r"\text{policy } 1", font_size=32, color=AGENT).next_to(view, UP, buff=0.25)
        ev = node_box(r"evaluate: \ $V^\pi = (I - \gamma P_\pi)^{-1} r_\pi$", VALUE, font_size=22).move_to([3.0, 2.4, 0])
        im = node_box(r"improve: \ $\pi'(s) = \arg\max_a Q^\pi(s, a)$", AGENT, font_size=22).move_to([3.0, 0.8, 0])
        a1 = CurvedArrow(ev.get_right() + DOWN * 0.1, im.get_right() + UP * 0.1, angle=-1.6, color=GREY_B,
                         stroke_width=2.5, tip_length=0.15)
        a2 = CurvedArrow(im.get_left() + UP * 0.1, ev.get_left() + DOWN * 0.1, angle=-1.6, color=GREY_B,
                         stroke_width=2.5, tip_length=0.15)
        th = theorem_card(r"policy improvement", r"if $Q^\pi(s, \pi'(s)) \ge V^\pi(s)$ for every $s$, \ then "
                          r"$V^{\pi'}(s) \ge V^\pi(s)$ for every $s$", who=r"Howard (1960)", width=6.4,
                          color=AGENT).move_to([3.0, -1.2, 0])
        pf = label(r"proof: \ unroll $V^\pi(s) \le \mathbb E[r + \gamma V^\pi(s')] \le \mathbb E[r + \gamma r' + "
                   r"\gamma^2 V^\pi(s'')] \le \cdots \le V^{\pi'}(s)$", font_size=19, color=GREY_A)
        pf.next_to(th, DOWN, buff=0.2)
        if pf.width > 6.8:
            pf.width = 6.8
        pf.set_x(3.0)
        n = len(P)
        with self.voiceover(
            "There's a second classic algorithm, policy iteration, from Ronald Howard in 1960. Start with any "
            "policy: here, always go up. <bookmark mark='a'/> Evaluate it exactly, with the linear solve from "
            "chapter three. <bookmark mark='b'/> Then improve it: in every state, switch to the action that looks "
            "best by those values. <bookmark mark='c'/> The policy improvement theorem says the new policy is at "
            "least as good everywhere. The proof just unrolls the inequality one step at a time. "
            f"<bookmark mark='d'/> Evaluate, improve, evaluate, improve: here it takes {n} policies, and then the "
            "policy stops changing. It is optimal. <bookmark mark='e'/> Evaluation and improvement, chasing each "
            "other: Sutton and Barto call it generalized policy iteration. Almost every method in this part is a "
            "version of it, AlphaZero included."
        ) as vo:
            self.play(FadeIn(view), FadeIn(it), LaggedStart(*[FadeIn(x_) for x_ in arrows], lag_ratio=0.01))
            vo.wait_until("a")
            self.play(FadeIn(ev))
            vo.wait_until("b")
            self.play(FadeIn(im), Create(a1), Create(a2))
            vo.wait_until("c")
            self.play(FadeIn(th, shift=UP * 0.2))
            self.play(FadeIn(pf))
            vo.wait_until("d")
            for i in range(1, n):
                new = view.arrows(cells, P[i])
                newit = MathTex(rf"\text{{policy }} {i + 1}", font_size=32, color=AGENT).move_to(it)
                self.play(*view.heat(cells, V[min(i, len(V) - 1)]), Transform(arrows, new), Transform(it, newit),
                          Indicate(ev[0], color=VALUE, scale_factor=1.03), run_time=0.9)
            vo.wait_until("e")
            self.play(Indicate(VGroup(ev, im, a1, a2), color=AGENT, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scale(self):
        rows = VGroup(
            VGroup(label(r"this gridworld", font_size=28), MathTex(r"44", font_size=36, color=VALUE)),
            VGroup(label(r"backgammon", font_size=28), MathTex(r"\approx 10^{20}", font_size=36, color=VALUE)),
            VGroup(label(r"chess \ (Shannon's estimate)", font_size=28), MathTex(r"\approx 10^{43}", font_size=36,
                                                                                    color=VALUE)),
            VGroup(label(r"Go, \ legal positions", font_size=28), MathTex(r"2.08 \times 10^{170}", font_size=36,
                                                                           color=VALUE)),
        )
        for r_ in rows:
            r_.arrange(RIGHT, buff=0.6)
        rows.arrange(DOWN, aligned_edge=RIGHT, buff=0.35).move_to([-2.0, 0.4, 0])
        for r_ in rows:
            r_[1].align_to(rows, RIGHT)
        head = label(r"states", font_size=26, color=GREY_A).next_to(rows, UP, buff=0.35).align_to(rows, RIGHT)
        cite_ = cite(r"Tesauro (1995); \ Shannon, \textit{Programming a Computer for Playing Chess} (1950); \ Tromp (2016)")
        needs = VGroup(label(r"dynamic programming needs", font_size=28, color=GREY_A),
                       label(r"the model $P(s' \mid s, a)$", font_size=28, color=ENV),
                       label(r"a sweep over every state", font_size=28, color=VALUE)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.25)
        needs.move_to([3.8, 0.6, 0])
        fix = label(r"instead: \ learn from samples, \ approximate $V$ with a function", font_size=28, color=REWARD)
        fix.to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Both algorithms need two things we usually don't have. The model: the transition probabilities, written "
            "down. And a sweep over every state. <bookmark mark='a'/> Our gridworld has forty-four states. "
            "Backgammon has about ten to the twenty. Chess, by Claude Shannon's estimate in 1950, about ten to the "
            "forty-three. Go has two times ten to the "
            "one hundred and seventy legal positions, more than the square of the number of atoms in the visible "
            "universe. <bookmark mark='b'/> The way forward is to learn from samples of experience, without the "
            "model, and to approximate the value function instead of tabulating it. That's the next three chapters."
        ) as vo:
            self.play(FadeIn(needs))
            vo.wait_until("a")
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=UP * 0.15) for r_ in rows], lag_ratio=0.5),
                      FadeIn(cite_), run_time=3.5)
            vo.wait_until("b")
            self.play(FadeIn(fix, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
